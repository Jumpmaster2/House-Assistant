"""WebSocket API of the panel."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.core import HomeAssistant

from custom_components.house_assistant.heating.ai_client import AiAuthError
from custom_components.house_assistant.heating.const import DOMAIN

from .conftest import AREA_DATA, heating, heating_options, make_entry, with_heating_options

BASIC_FIELDS = {
    "name",
    "area",
    "floor_area",
    "temperature_sensor",
    "humidity_sensor",
    "cooling_entity",
}


def heating_data(data):
    return {k: v for k, v in data.items() if k not in BASIC_FIELDS}


async def _setup(hass: HomeAssistant, **kwargs):
    entry = make_entry(**kwargs)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def _send(client, **msg):
    await client.send_json_auto_id(msg)
    return await client.receive_json()


async def test_config_payload(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    await _setup(hass, api_key="secret-key")
    client = await hass_ws_client(hass)

    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    assert msg["success"], msg
    cfg = msg["result"]
    assert cfg["has_api_key"] is True
    assert "secret-key" not in str(cfg)
    assert cfg["options"]["frost_temperature"] == 7.0
    assert cfg["options"]["limits"]["theta"]["max"] > cfg["options"]["limits"]["theta"]["min"]
    assert cfg["entities"]["heating_day"] == "binary_sensor.heating_heating_day"
    assert cfg["entities"]["ai_enabled"].startswith("switch.")
    living = next(a for a in cfg["areas"] if a["title"] == "Living room")
    storage = next(a for a in cfg["areas"] if a["title"] == "Storage room")
    assert living["entities"]["climate"].startswith("climate.")
    assert "climate" not in storage["entities"]
    assert living["entities"]["heat_rate"] == "sensor.living_room_heat_up_rate"
    assert living["entities"]["learning_progress"].startswith("sensor.")
    assert "learning_progress" not in storage["entities"]
    assert storage["entities"]["ventilation"].startswith("sensor.")
    spec = cfg["option_specs"]["frost_temperature"]
    assert (spec["selector"], spec["min"], spec["max"]) == ("number", 0, 15)
    # the sources of the vacation are set only in the house
    assert "vacation_entities" not in cfg["option_specs"]
    assert "return_entity" not in cfg["option_specs"]
    assert cfg["option_specs"]["vacation_temperature"]["selector"] == "number"
    assert "temperature_sensor" not in cfg["area_specs"]
    # brief airing: next to the window delay, with the standard values
    short = cfg["area_specs"]["short_airing_min"]
    assert (short["selector"], short["min"], short["max"], short["step"]) == ("number", 0, 60, 0.5)
    percent = cfg["area_specs"]["short_recovery_percent"]
    assert (percent["selector"], percent["min"], percent["max"], percent["step"]) == (
        "number",
        0,
        100,
        5,
    )
    assert cfg["area_defaults"]["short_airing_min"] == 1
    assert cfg["area_defaults"]["short_recovery_percent"] == 50
    assert isinstance(cfg["house"], dict)


async def test_save_options(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    entry = await _setup(hass)
    client = await hass_ws_client(hass)

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_options",
        options={"frost_temperature": "8.5", "preheat_reserve": 45.0},
    )
    assert msg["success"], msg
    assert heating_options(entry)["frost_temperature"] == 8.5
    assert heating_options(entry)["preheat_reserve"] == 45
    assert isinstance(heating_options(entry)["preheat_reserve"], int)
    assert "weather" not in heating_options(entry)

    # a cleared optional entity is removed, a cleared value falls back to the default
    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_options",
        options={"frost_temperature": None},
    )
    assert msg["success"], msg
    assert "weather" not in heating_options(entry)
    assert "outdoor_humidity" not in heating_options(entry)
    assert heating_options(entry)["frost_temperature"] == 7.0

    for options, error in (
        # no weather entity either (removed above): one of both is needed
        ({"outdoor_temperature": ""}, "house_settings_only:outdoor_temperature"),
        ({"frost_temperature": 99}, "invalid_value:frost_temperature"),
        ({"weather": "sensor.not_weather"}, "house_settings_only:weather"),
        ({"season_start": "31.02."}, "invalid_day_month:season_start"),
        ({"check_interval": 10, "check_max_interval": 5}, "max_below_base:check_max_interval"),
        (
            {"ventilation_check_interval": 10, "ventilation_check_max_interval": 5},
            "max_below_base:ventilation_check_max_interval",
        ),
        ({"limits": {"rh_threshold": {"min": 70, "max": 50}}}, "min_above_max:rh_threshold"),
        ({"not_an_option": 1}, "unknown_option:not_an_option"),
        ({"limits": {"theta": {"min": 20, "max": 10}}}, "min_above_max:theta"),
    ):
        msg = await _send(client, type=f"{DOMAIN}/heating/save_options", options=options)
        assert not msg["success"], options
        assert msg["error"]["message"] == error
    assert heating_options(entry)["frost_temperature"] == 7.0


async def test_save_options_model_prices_and_limits(
    hass: HomeAssistant, base_states, hass_ws_client
) -> None:
    entry = await _setup(hass)
    client = await hass_ws_client(hass)

    # prices still at the old model's suggestion follow the new model
    msg = await _send(
        client, type=f"{DOMAIN}/heating/save_options", options={"model": "claude-sonnet-5-5"}
    )
    assert msg["success"], msg
    assert heating_options(entry)["price_input"] == 2.0
    assert msg["result"]["options"]["price_output"] == 10.0

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_options",
        options={"limits": {"theta": {"min": 10, "max": 18, "step": 0.5}}},
    )
    assert msg["success"], msg
    assert heating_options(entry)["limits"]["theta"] == {"min": 10.0, "max": 18.0, "step": 0.5}
    assert "puffer" in heating_options(entry)["limits"]


async def test_save_api_key(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    entry = await _setup(hass)
    client = await hass_ws_client(hass)
    target = "custom_components.house_assistant.heating.config_flow.ClaudeClient.validate"

    with patch(target, side_effect=AiAuthError("authentication failed")):
        msg = await _send(client, type=f"{DOMAIN}/heating/save_api_key", api_key="wrong")
    assert not msg["success"]
    assert msg["error"]["message"] == "invalid_auth"
    assert entry.data["api_key"] == ""

    msg = await _send(client, type=f"{DOMAIN}/heating/save_api_key", api_key=" ")
    assert msg["error"]["message"] == "api_key_required"

    with patch(target):
        msg = await _send(client, type=f"{DOMAIN}/heating/save_api_key", api_key=" good-key ")
        await hass.async_block_till_done(wait_background_tasks=True)
    assert msg["success"], msg
    assert msg["result"]["has_api_key"] is True
    assert entry.data["api_key"] == "good-key"
    assert heating(entry).ai_configured

    # a key saved in the panel ends a reauth flow that asked for one
    await entry.start_reauth_flow(hass)
    assert hass.config_entries.flow.async_progress_by_handler(DOMAIN)
    with patch(target):
        msg = await _send(client, type=f"{DOMAIN}/heating/save_api_key", api_key="other-key")
        await hass.async_block_till_done(wait_background_tasks=True)
    assert msg["success"], msg
    assert not hass.config_entries.flow.async_progress_by_handler(DOMAIN)

    msg = await _send(client, type=f"{DOMAIN}/heating/save_api_key", remove=True)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert msg["success"]
    assert entry.data["api_key"] == ""
    assert not heating(entry).ai_configured


async def test_areas(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    entry = await _setup(hass, areas=[AREA_DATA])
    client = await hass_ws_client(hass)

    msg = await _send(client, type=f"{DOMAIN}/heating/save_area", title="Bath", data={})
    assert msg["error"]["message"] == "create_rooms_in_house"
    sub_id = next(iter(entry.subentries))
    sub = entry.subentries[sub_id]
    basics = {k: v for k, v in sub.data.items() if k in BASIC_FIELDS}
    for field in BASIC_FIELDS:
        msg = await _send(
            client,
            type=f"{DOMAIN}/heating/save_area",
            subentry_id=sub_id,
            title=sub.title,
            data={field: None},
        )
        assert msg["error"]["message"] == "room_basics_house_only"
        assert entry.subentries[sub_id].data == sub.data
    msg = await _send(
        client, type=f"{DOMAIN}/heating/save_area", subentry_id=sub_id, title="Renamed", data={}
    )
    assert msg["error"]["message"] == "room_basics_house_only"
    for data, error in [
        ({"min_target": 22, "max_target": 20}, "min_above_max"),
        ({"reference_temperature": "sensor.y"}, "reference_incomplete"),
    ]:
        msg = await _send(
            client,
            type=f"{DOMAIN}/heating/save_area",
            subentry_id=sub_id,
            title=sub.title,
            data=data,
        )
        assert msg["error"]["message"] == error
    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title=sub.title,
        data={"default_target": 22.5, "draft_group_2": ["binary_sensor.living_room_window"]},
    )
    assert msg["success"], msg
    saved = entry.subentries[sub_id].data
    assert saved["default_target"] == 22.5
    assert saved["draft_group_2"] == ["binary_sensor.living_room_window"]
    assert {k: v for k, v in saved.items() if k in BASIC_FIELDS} == basics
    msg = await _send(client, type=f"{DOMAIN}/heating/delete_area", subentry_id=sub_id)
    assert msg["success"]
    msg = await _send(client, type=f"{DOMAIN}/heating/delete_area", subentry_id=sub_id)
    assert not msg["success"]


async def test_area_change_reloads(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    entry = await _setup(hass, areas=[AREA_DATA])
    client = await hass_ws_client(hass)
    sub_id = next(iter(entry.subentries))
    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data={**heating_data(entry.subentries[sub_id].data), "dead_time": 45},
    )
    assert msg["success"], msg
    await hass.async_block_till_done(wait_background_tasks=True)
    assert heating(entry).areas[sub_id].name == "Living room"
    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    assert msg["result"]["areas"][0]["entities"]["climate"].startswith("climate.")


async def test_airing_values_change_an_existing_room(
    hass: HomeAssistant, base_states, hass_ws_client
) -> None:
    """The brief airing values of a room that exists already are changed in the panel and
    take effect with the reload; the start values stay as they were."""
    entry = await _setup(hass, areas=[AREA_DATA])
    client = await hass_ws_client(hass)
    sub_id = next(iter(entry.subentries))
    assert (
        heating(entry).areas[sub_id].params.short_airing_min,
        heating(entry).areas[sub_id].params.short_recovery_percent,
    ) == (1.0, 50.0)  # the room has no such values: the standard ones

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data={
            **heating_data(entry.subentries[sub_id].data),
            "short_airing_min": 3.0,
            "short_recovery_percent": 20,
            "window_delay": 7,  # a start value: kept as it was
        },
    )
    assert msg["success"], msg
    await hass.async_block_till_done(wait_background_tasks=True)
    area = heating(entry).areas[sub_id]
    assert (area.params.short_airing_min, area.params.short_recovery_percent) == (3.0, 20.0)
    data = entry.subentries[sub_id].data
    assert (data["short_airing_min"], data["short_recovery_percent"]) == (3.0, 20)
    assert data["window_delay"] == 5

    # out of range: refused, nothing changed
    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data={**heating_data(entry.subentries[sub_id].data), "short_recovery_percent": 150},
    )
    assert msg["error"]["message"] == "invalid_value:short_recovery_percent"

    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    assert msg["success"], msg
    assert msg["result"]["area_defaults"]["short_airing_min"] == 1
    assert msg["result"]["area_defaults"]["short_recovery_percent"] == 50
    assert "short_airing_min" in msg["result"]["area_specs"]


async def test_learned_values(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    """Start values stay as created; the panel edits the learned values and theta."""
    entry = await _setup(hass, areas=[AREA_DATA])
    client = await hass_ws_client(hass)
    sub_id = next(iter(entry.subentries))
    area = heating(entry).areas[sub_id]
    area.learner.dead_time.add(2400)  # 30 min -> 35 min

    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    cfg = msg["result"]
    assert cfg["theta"] == 16.0
    assert "theta_start" not in cfg["option_specs"]
    assert cfg["learned_specs"]["theta"]["min"] == cfg["options"]["limits"]["theta"]["min"]
    assert cfg["areas"][0]["learned"] == {
        "window_delay": 5.0,
        "puffer": 0.7,
        "dead_time": 35.0,
        "recovery_time": 30.0,
    }

    msg = await _send(client, type=f"{DOMAIN}/heating/save_options", options={"theta_start": 12})
    assert msg["error"]["message"] == "unknown_option:theta_start"

    msg = await _send(client, type=f"{DOMAIN}/heating/save_theta", theta="14.5")
    assert msg["success"], msg
    assert heating(entry).theta == 14.5
    assert msg["result"]["theta"] == 14.5
    msg = await _send(client, type=f"{DOMAIN}/heating/save_theta", theta=99)
    assert msg["error"]["message"] == "invalid_value:theta"

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data={**heating_data(entry.subentries[sub_id].data), "dead_time": 60, "puffer": 1.5},
        learned={"dead_time": 50, "puffer": 0.4, "window_delay": 5, "recovery_time": 30},
    )
    assert msg["success"], msg
    await hass.async_block_till_done(wait_background_tasks=True)
    data = entry.subentries[sub_id].data
    assert (data["dead_time"], data["puffer"]) == (30, 0.7)
    area = heating(entry).areas[sub_id]
    assert area.learner.dead_time.value == 50 * 60
    assert area.params.puffer == 0.4
    assert area.learner.recovery.count == 0  # unchanged values are not touched

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data=heating_data(entry.subentries[sub_id].data),
        learned={"dead_time": 1},
    )
    assert msg["error"]["message"] == "invalid_value:dead_time"

    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_area",
        subentry_id=sub_id,
        title="Living room",
        data=heating_data(entry.subentries[sub_id].data),
        learned={"heat_rate": 1},
    )
    assert msg["error"]["message"] == "unknown_option:heat_rate"


async def test_learned_rates_for_the_panel(
    hass: HomeAssistant, base_states, hass_ws_client
) -> None:
    """The learned rates reach the panel although their sensors are off by default."""
    from homeassistant.helpers import entity_registry as er

    entry = await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "house_assistant/heating/learned"})
    msg = await client.receive_json()
    assert msg["success"], msg
    living = next(s.subentry_id for s in entry.subentries.values() if s.title == "Living room")
    stats = msg["result"][living]
    assert stats["dead_time"]["unit"] == "min" and stats["dead_time"]["value"] == 30.0
    assert len(msg["result"]) == 1  # the ventilation only area has no circuit
    registry = er.async_get(hass)
    assert registry.async_get("sensor.living_room_dead_time").disabled_by is not None
    assert registry.async_get("sensor.living_room_status").disabled_by is None


async def test_saved_limits_are_in_the_reply_at_once(
    hass: HomeAssistant, base_states, hass_ws_client
) -> None:
    """The reply to a save already uses the new limits (before the reload)."""
    entry = await _setup(hass)
    coordinator = heating(entry)
    assert coordinator.limits["theta"]["max"] != 25.0
    limits = {
        **heating_options(entry)["limits"],
        "theta": {**heating_options(entry)["limits"]["theta"], "max": 25.0},
    }
    hass.config_entries.async_update_entry(
        entry, options=with_heating_options(entry, limits=limits)
    )
    assert coordinator.limits["theta"]["max"] == 25.0


async def test_save_prompt_blocks(hass: HomeAssistant, base_states, hass_ws_client) -> None:
    entry = await _setup(hass)
    client = await hass_ws_client(hass)
    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    defaults = msg["result"]["prompt_defaults"]
    assert {b["id"] for b in defaults["nightly"]["blocks"]} >= {"types", "learn"}
    assert {b["id"] for b in defaults["ventilation"]["blocks"]} >= {"profile", "ranges"}
    groups = {p["key"]: p["group"] for p in msg["result"]["limit_params"]}
    assert groups["rh_threshold"] == "ventilation" and groups["theta"] == "heating"
    assert msg["result"]["entities"]["ai_next_vent_check"].startswith("sensor.")
    assert msg["result"]["options"]["prompt_blocks"] == {}

    prompts = {
        "nightly": {"disabled": ["learn"], "custom": [{"text": " Kaminofen ", "enabled": True}]},
        "check": {"overrides": {"levers": "Own levers."}},
    }
    msg = await _send(
        client, type=f"{DOMAIN}/heating/save_options", options={"prompt_blocks": prompts}
    )
    assert msg["success"], msg
    assert heating_options(entry)["prompt_blocks"] == {
        "nightly": {"disabled": ["learn"], "custom": [{"text": "Kaminofen", "enabled": True}]},
        "check": {"overrides": {"levers": "Own levers."}},
    }
    assert msg["result"]["options"]["prompt_blocks"] == heating_options(entry)["prompt_blocks"]

    for options, error in (
        ({"prompt_blocks": {"nightly": {"disabled": ["x"]}}}, "invalid_value:prompt_blocks"),
        (
            {"prompt_blocks": {"check": {"custom": [{"text": "x" * 2001}]}}},
            "text_too_long:prompt_blocks",
        ),
    ):
        msg = await _send(client, type=f"{DOMAIN}/heating/save_options", options=options)
        assert not msg["success"], options
        assert msg["error"]["message"] == error


async def test_panel_preserves_unchanged_legacy_limits(
    hass: HomeAssistant, base_states, hass_ws_client
):
    from custom_components.house_assistant.heating.logic.ai_schema import default_limits

    limits = default_limits()
    limits["window_delay_min"] = {"min": 1, "max": 30, "step": 2}
    limits["recovery_bias_min"] = {"min": -30, "max": 90, "step": 10}
    entry = await _setup(hass, limits=limits)
    client = await hass_ws_client(hass)
    msg = await _send(client, type=f"{DOMAIN}/heating/config")
    assert msg["result"]["options"]["limits"] == limits
    msg = await _send(
        client,
        type=f"{DOMAIN}/heating/save_options",
        options={"limits": {"window_delay_min": {"max": 31}}},
    )
    assert not msg["success"]
    assert msg["error"]["message"] == "invalid_value:window_delay_min"
    assert heating_options(entry)["limits"] == limits
    changed = {**limits, "hysteresis_on": {"min": 0, "max": 0.6, "step": 0}}
    msg = await _send(client, type=f"{DOMAIN}/heating/save_options", options={"limits": changed})
    assert msg["success"], msg
    assert msg["result"]["options"]["limits"] == changed
    await hass.async_block_till_done(wait_background_tasks=True)
    assert heating_options(entry)["limits"] == changed
