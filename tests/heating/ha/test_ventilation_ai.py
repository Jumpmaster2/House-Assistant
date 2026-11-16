"""AI check of the ventilation thresholds and the learned humidity profile."""

from __future__ import annotations

import json
from datetime import timedelta
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.house_assistant.heating.const import DOMAIN, EVENT_LOGBOOK
from custom_components.house_assistant.heating.logic.ai_schema import VENT_PARAMS

from .conftest import AREA_DATA, VENT_ONLY_DATA, heating, make_entry
from .test_control import STRUCTURED, USAGE, _advance, _setup

SUMMER = "2026-07-15 10:00:00+02:00"


def _answer(*adjustments: dict) -> tuple[dict, dict]:
    return {"adjustments": list(adjustments), "summary": "Fine.", "confidence": 60}, USAGE


async def test_ventilation_check_runs_all_year_and_backs_off(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    change = {"area": "a2", "parameter": "rh_threshold", "value": 60, "reason": "Cellar."}
    with patch(STRUCTURED, side_effect=[_answer(change), _answer()]) as mock:
        await _setup(hass, make_entry(api_key="test-key"))
        coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
        assert not coordinator.season_active
        # first check after the base interval, the statistics need a while
        first = dt_util.parse_datetime(coordinator.vent_state["next_check"])
        assert first - dt_util.utcnow() == timedelta(hours=6)
        events = async_capture_events(hass, EVENT_LOGBOOK)
        await _advance(hass, freezer, 30)
        await coordinator.async_run_vent_check("manual")
        await hass.async_block_till_done(wait_background_tasks=True)
        assert mock.call_count == 1
        system, user = mock.call_args.args[0], mock.call_args.args[1]
        payload = json.loads(user)
        assert mock.call_args.args[2]["properties"]["adjustments"]["items"]["properties"][
            "parameter"
        ]["enum"] == sorted(VENT_PARAMS)
        assert "rh_threshold" in system
        assert not payload["heating_period"]
        storage = next(a for a in payload["areas"] if a["id"] == "a2")
        assert storage["params"]["rh_threshold"] == 65.0
        assert storage["stats"]["humid_min"] == pytest.approx(30, abs=1)  # 70 % >= 65 %
        assert storage["stats"]["rh_mean"] == 70.0
        assert storage["profile"]["season"] == "summer"
        assert storage["profile"]["floor_14d"] is None  # no day completed yet
        area = next(a for a in coordinator.areas.values() if a.prompt_id == "a2")
        assert area.vent_params.rh_threshold == 62.0  # one step of 3 % down from configured 65
        assert any(
            "Feuchte-Schwelle" in e.data["message"] or "humidity threshold" in e.data["message"]
            for e in events
        )
        # a room humid for long keeps the interval at its base
        assert coordinator.vent_state["stable"] == 0
        assert area.vent_check["minutes"] == 0
        assert (
            hass.states.get("sensor.storage_room_ventilation_recommendation").attributes[
                "humidity_threshold"
            ]
            == 62.0
        )

        # dry again and nothing to change: the interval grows
        hass.states.async_set("sensor.storage_humidity", "50", {"unit_of_measurement": "%"})
        await _advance(hass, freezer, 30)
        await coordinator.async_run_vent_check("manual")
        await hass.async_block_till_done(wait_background_tasks=True)
        assert mock.call_count == 2
        history = json.loads(mock.call_args.args[1])["history"]
    assert history[0]["changes"] == ["a2 rh_threshold 65>62"]
    assert coordinator.vent_state["stable"] == 1
    later = dt_util.parse_datetime(coordinator.vent_state["next_check"])
    assert later - dt_util.utcnow() == timedelta(hours=12)
    last = hass.states.get("sensor.heating_last_ai_ventilation_check")
    assert last is not None and last.attributes["summary"] == "Fine."
    stored = coordinator._data_to_save()["areas"][area.area_id]
    assert stored["vent_params"]["rh_threshold"] == 62.0
    assert stored["humidity"]["day"]["n"] > 0


async def test_ventilation_check_off_without_ai_or_option(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    await _setup(hass, make_entry(api_key="test-key", ventilation_ai_enabled=False))
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    assert not coordinator.vent_ai_active
    assert coordinator.vent_state["next_check"] is None
    with patch(STRUCTURED) as mock:
        await coordinator.async_run_vent_check("manual")
    mock.assert_not_called()


async def test_ventilation_switching_ai_off_and_on(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    await _setup(hass, make_entry(api_key="test-key"))
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    await coordinator.async_set_ai_enabled(False)
    assert coordinator.vent_state["next_check"] is None
    await coordinator.async_set_ai_enabled(True)
    soon = dt_util.parse_datetime(coordinator.vent_state["next_check"])
    assert soon - dt_util.utcnow() == timedelta(minutes=5)


async def test_ventilation_parameters_reset_export_and_import(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    await _setup(hass, make_entry(api_key="test-key"))
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    area = next(a for a in coordinator.areas.values() if a.prompt_id == "a2")
    area.vent_params.rh_threshold = 74.0
    exported = coordinator.export_parameters([area.area_id])
    assert exported["areas"]["Storage room"]["vent_params"]["rh_threshold"] == 74.0
    assert "humidity" in exported["areas"]["Storage room"]

    coordinator.reset_learned([area.area_id], include_parameters=True)
    assert area.vent_params.rh_threshold == 65.0  # configured start value
    assert area.humidity_profile.day.n == 0

    exported["areas"]["Storage room"]["vent_params"]["rh_threshold"] = 99
    coordinator.import_parameters(exported, [area.area_id])
    assert area.vent_params.rh_threshold == 65.0  # limited by configured always-air ceiling


async def test_window_sizes_and_suggested_window(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    hass.states.async_set("binary_sensor.storage_door", "off")
    hass.states.async_set("binary_sensor.storage_skylight", "off")
    storage = {
        **VENT_ONLY_DATA,
        "window_sensors_small": ["binary_sensor.storage_skylight"],
        "door_sensors": ["binary_sensor.storage_door"],
    }
    await _setup(hass, make_entry(api_key="test-key", areas=[AREA_DATA, storage]))
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    await _advance(hass, freezer, 2)
    area = next(a for a in coordinator.areas.values() if a.prompt_id == "a2")
    attrs = hass.states.get("sensor.storage_room_ventilation_recommendation").attributes
    assert area.ventilation.state == "ventilate_now"  # 70 % >= 65 %, outside drier
    assert attrs["airing_window"] == "binary_sensor.storage_door"
    # summer at 5 °C outside: 10 minutes for a medium window, a door needs 4
    assert attrs["airing_minutes"] == 4

    hass.states.async_set("binary_sensor.storage_skylight", "on")
    await _advance(hass, freezer, 1)
    assert area.own_window_open and area.opening == 0.5
    assert area.suggested_window is None  # already airing
    payload = coordinator._vent_area_payload(area)
    assert payload["windows"] == {"small": 1, "door": 1}


async def test_cross_ventilation_is_counted_and_shown(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    kids = "binary_sensor.kids_room_window"
    hass.states.async_set(kids, "off")
    window = "binary_sensor.storage_window"
    hass.states.async_set(window, "off")
    storage = {**VENT_ONLY_DATA, "window_sensors": [window], "draft_group_1": [kids]}
    await _setup(hass, make_entry(api_key="test-key", areas=[AREA_DATA, storage]))
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    area = next(a for a in coordinator.areas.values() if a.prompt_id == "a2")
    hass.states.async_set(window, "on")
    await _advance(hass, freezer, 3)
    assert area.vent_check.get("cross_min", 0.0) == 0.0  # own window alone
    hass.states.async_set(kids, "on")
    await _advance(hass, freezer, 3)
    assert area.vent_check["cross_min"] == pytest.approx(3, abs=1)
    assert area.humidity_profile.airing["cross"] is True
    payload = coordinator._vent_area_payload(area)
    assert payload["draft"] is True and payload["draft_groups"] == 1
    assert payload["stats"]["cross_min"] == pytest.approx(3, abs=1)


async def test_legacy_vent_params_clamp_on_load_and_manual_import(
    hass: HomeAssistant, base_states, hass_storage: dict
) -> None:
    from custom_components.house_assistant.heating.const import STORAGE_VERSION

    entry = make_entry(ventilation_mould_rh=70, ventilation_energy_rh_per_k=0.25)
    entry.add_to_hass(hass)
    room = next(s for s in entry.subentries.values() if s.title == "Living room")
    key = f"{DOMAIN}.{entry.entry_id}.heating"
    hass_storage[key] = {
        "version": STORAGE_VERSION,
        "minor_version": 1,
        "key": key,
        "data": {
            "areas": {
                room.subentry_id: {
                    "vent_params": {
                        "rh_threshold": 67,
                        "mould_rh": 70,
                        "energy_rh_per_k": 0.25,
                        "rh_hysteresis": 0,
                    },
                }
            }
        },
    }
    events = async_capture_events(hass, EVENT_LOGBOOK)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    coordinator = heating(entry)
    area = coordinator.areas[room.subentry_id]
    assert area.vent_params.rh_threshold == 62
    assert area.vent_params.mould_rh == 65
    assert area.vent_params.rh_hysteresis == 2
    assert "energy_rh_per_k" not in area.vent_params.as_dict()
    assert entry.options["heating"]["ventilation_mould_rh"] == 65
    assert "ventilation_energy_rh_per_k" not in entry.options["heating"]
    assert any("67" in e.data["message"] and "62" in e.data["message"] for e in events)
    coordinator.import_parameters(
        {
            "areas": {
                "Living room": {
                    "vent_params": {
                        "rh_threshold": 99,
                        "mould_rh": 80,
                        "rh_hysteresis": 10,
                    }
                }
            }
        }
    )
    assert area.vent_params.rh_threshold == 62
    assert area.vent_params.mould_rh == 65
    assert area.vent_params.rh_hysteresis == 5


async def test_ai_cannot_raise_room_threshold_above_comfort_bounds(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(SUMMER)
    with patch(
        STRUCTURED,
        return_value=_answer(
            {"area": "a1", "parameter": "rh_threshold", "value": 67, "reason": "Usual humidity."},
            {"area": "a1", "parameter": "mould_rh", "value": 70, "reason": "Usual humidity."},
        ),
    ) as mock:
        await _setup(hass, make_entry(api_key="test-key"))
        coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
        await coordinator.async_run_vent_check("manual")
        payload = json.loads(mock.call_args.args[1])
    area = next(a for a in coordinator.areas.values() if a.prompt_id == "a1")
    assert area.vent_params.rh_threshold == 62
    assert area.vent_params.mould_rh == 65
    limits = next(a["limits"] for a in payload["areas"] if a["id"] == "a1")
    assert limits["rh_threshold"]["min"] == 55 and limits["rh_threshold"]["max"] == 62
    assert limits["mould_rh"]["max"] == 65


async def test_running_airing_uses_own_open_time_and_keeps_binary_sensor_on(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    hass.states.async_set("sensor.living_room_temperature", "20.9", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_room_humidity", "62.4", {"unit_of_measurement": "%"})
    await _setup(hass, make_entry())
    coordinator = heating(hass.config_entries.async_entries(DOMAIN)[0])
    area = next(a for a in coordinator.areas.values() if a.prompt_id == "a1")
    window = "binary_sensor.living_room_window"
    hass.states.async_set(window, "on")
    await _advance(hass, freezer, 1)
    result = area.ventilation
    assert result.state == "airing" and result.reason == "airing_running"
    assert 8 <= result.airing_minutes_left <= 10
    attrs = hass.states.get("sensor.living_room_ventilation_recommendation").attributes
    assert attrs["always_rh"] == 65 and attrs["reason"] == "airing_running"
    assert attrs["airing_minutes_left"] == result.airing_minutes_left
    assert hass.states.get("binary_sensor.living_room_ventilation_recommended").state == "on"
    duration = result.airing_minutes
    # Learning a different rate during an airing cannot extend its deadline.
    area.humidity_profile.rate.value, area.humidity_profile.rate.count = 0.002, 5
    await _advance(hass, freezer, duration + 2)
    assert area.ventilation.reason == "airing_time_over"
    assert area.ventilation.state == "close_window"
    assert hass.states.get("binary_sensor.living_room_ventilation_recommended").state == "off"
    hass.states.async_set(window, "off")
    await _advance(hass, freezer, 1)
    assert area.ventilation.reason == "pause_after_airing"
    assert area.vent_window_opened is None
    saved = coordinator._data_to_save()["areas"][area.area_id]
    assert "vent_window_opened" not in saved
