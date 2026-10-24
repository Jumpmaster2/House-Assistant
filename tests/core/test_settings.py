"""Settings of the house: one value for every module, else the one of the module."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits
from custom_components.house_assistant.runtime import shared_options


def _entry(core: dict[str, Any], heating: dict[str, Any], shutter: dict[str, Any]):
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {"modules": ["heating", "shutter", "meter"], **core},
            "heating": {**HEATING_DEFAULTS, "limits": default_limits(), **heating},
            "shutter": shutter,
            "meter": {"ai_task_entity": "ai_task.claude"},
        },
    )


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    for entity_id in ("sensor.house_outdoor", "sensor.heating_outdoor", "sensor.cover_outdoor"):
        hass.states.async_set(entity_id, "5", {"unit_of_measurement": "°C"})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)


def _modules(entry: MockConfigEntry) -> dict[str, Any]:
    return entry.runtime_data.modules


async def test_house_value_wins_else_the_module_value(hass: HomeAssistant) -> None:
    entry = _entry(
        {"outdoor_temperature": "sensor.house_outdoor", "language": "de"},
        {"outdoor_temperature": "sensor.heating_outdoor"},
        {"outdoor_temperature": "sensor.cover_outdoor", "language": "en"},
    )
    await _setup(hass, entry)
    modules = _modules(entry)
    assert modules["heating"].coordinator.opt("outdoor_temperature") == "sensor.house_outdoor"
    assert modules["shutter"].engine.opt("outdoor_temperature") == "sensor.house_outdoor"
    assert modules["heating"].coordinator.language == "de"
    assert modules["shutter"].engine.language == "de"
    assert modules["meter"].manager.language == "de"

    # without a value of the house each module keeps its own; "auto" leaves the choice
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "core": {"modules": entry.options["core"]["modules"], "language": "auto"},
        },
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    assert shared_options(entry) == {}
    modules = _modules(entry)
    assert modules["heating"].coordinator.opt("outdoor_temperature") == "sensor.heating_outdoor"
    assert modules["shutter"].engine.opt("outdoor_temperature") == "sensor.cover_outdoor"
    assert modules["shutter"].engine.language == "en"


async def test_house_step_of_the_options(hass: HomeAssistant) -> None:
    entry = _entry({"outdoor_temperature": "sensor.house_outdoor"}, {}, {})
    await _setup(hass, entry)
    flow = hass.config_entries.options
    result = await flow.async_init(entry.entry_id)
    assert result["menu_options"] == ["modules", "house", "vacation", "heating", "shutter", "meter"]
    result = await flow.async_configure(result["flow_id"], {"next_step_id": "house"})
    assert result["step_id"] == "house"
    # heating and covers need an outdoor temperature: the modules have none of their own
    result = await flow.async_configure(result["flow_id"], {"language": "auto"})
    assert result["errors"] == {"outdoor_temperature": "need_temperature_source"}
    result = await flow.async_configure(
        result["flow_id"], {"weather": "weather.home", "language": "en", "weekend_days": ["sun"]}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    core = entry.options["core"]
    assert "outdoor_temperature" not in core
    assert (core["weather"], core["language"], core["weekend_days"]) == (
        "weather.home",
        "en",
        ["sun"],
    )
    assert core["modules"] == ["heating", "shutter", "meter"]
    await hass.async_block_till_done(wait_background_tasks=True)
    assert _modules(entry)["shutter"].engine.opt("weekend_days") == ["sun"]


async def test_house_panel_saves_settings_and_modules(hass: HomeAssistant, hass_ws_client) -> None:
    entry = _entry({"outdoor_temperature": "sensor.house_outdoor"}, {}, {})
    await _setup(hass, entry)
    client = await hass_ws_client(hass)
    await client.send_json({"id": 1, "type": "house_assistant/house/config"})
    result = (await client.receive_json())["result"]
    assert result["settings"] == {"outdoor_temperature": "sensor.house_outdoor"}
    assert {"outdoor_temperature", "weather", "language", "notify_services"} <= set(
        result["fields"]["settings"]
    )

    await client.send_json(
        {
            "id": 2,
            "type": "house_assistant/house/save_settings",
            "settings": {
                "outdoor_temperature": "sensor.house_outdoor",
                "notify_services": ["light.x"],
            },
        }
    )
    msg = await client.receive_json()
    assert not msg["success"]
    assert msg["error"]["message"] == "invalid_notify_service:notify_services"

    await client.send_json(
        {
            "id": 3,
            "type": "house_assistant/house/save_settings",
            "settings": {"outdoor_temperature": "sensor.house_outdoor", "language": "de"},
            "modules": ["meter"],
            "show_panel": False,
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    core = entry.options["core"]
    assert core == {
        "modules": ["meter"],
        "show_panel": False,
        "outdoor_temperature": "sensor.house_outdoor",
        "language": "de",
    }
    await hass.async_block_till_done(wait_background_tasks=True)
    assert set(_modules(entry)) == {"meter"}
