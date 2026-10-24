"""Fixtures for tests with a Home Assistant test instance."""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("pytest_homeassistant_custom_component")

from homeassistant.config_entries import ConfigEntry, ConfigSubentryData
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.heating.const import (
    CONF_LIMITS,
    CONF_OUTDOOR_TEMP,
    DEFAULTS,
    DOMAIN,
    MODULE_HEATING,
    SUBENTRY_ROOM,
)
from custom_components.house_assistant.heating.logic.ai_schema import default_limits

AREA_DATA = {
    "name": "Living room",
    "temperature_sensor": "sensor.living_room_temperature",
    "humidity_sensor": "sensor.living_room_humidity",
    "window_sensors": ["binary_sensor.living_room_window"],
    "heater_switch": "input_boolean.heating_circuit_1",
    "default_target": 21.0,
    "min_target": 16.0,
    "max_target": 24.0,
    "min_on_time": 10,
    "min_off_time": 10,
    "window_delay": 5,
    "recovery_time": 30,
    "dead_time": 30,
    "puffer": 0.7,
    "ventilation_rh_threshold": 60.0,
}

VENT_ONLY_DATA = {
    "name": "Storage room",
    "temperature_sensor": "sensor.storage_temperature",
    "humidity_sensor": "sensor.storage_humidity",
    "ventilation_rh_threshold": 65.0,
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable loading of custom integrations."""
    return


IN_SEASON = "2026-11-16 10:00:00+01:00"


@pytest.fixture
async def base_states(hass: HomeAssistant, freezer) -> None:
    """Sensors, windows and a switchable heating circuit (created within the heating period)."""
    freezer.move_to(IN_SEASON)
    await hass.config.async_set_time_zone("Europe/Berlin")
    assert await async_setup_component(
        hass, "input_boolean", {"input_boolean": {"heating_circuit_1": {}}}
    )
    hass.states.async_set("sensor.outdoor_temperature", "5.0", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.outdoor_humidity", "85", {"unit_of_measurement": "%"})
    hass.states.async_set("sensor.living_room_temperature", "19.0", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_room_humidity", "55", {"unit_of_measurement": "%"})
    hass.states.async_set("binary_sensor.living_room_window", "off")
    hass.states.async_set("sensor.storage_temperature", "20.0", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.storage_humidity", "70", {"unit_of_measurement": "%"})
    await hass.async_block_till_done()


def make_entry(api_key: str = "", areas: list[dict] | None = None, **options) -> MockConfigEntry:
    """Config entry of the house with the heating: one room with a circuit and one only
    for the ventilation advice."""
    areas = [AREA_DATA, VENT_ONLY_DATA] if areas is None else areas
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": api_key},
        options={
            "core": {"modules": [MODULE_HEATING]},
            MODULE_HEATING: {
                **DEFAULTS,
                CONF_OUTDOOR_TEMP: "sensor.outdoor_temperature",
                "outdoor_humidity": "sensor.outdoor_humidity",
                CONF_LIMITS: default_limits(),
                **options,
            },
        },
        subentries_data=[
            ConfigSubentryData(
                data=area, subentry_type=SUBENTRY_ROOM, title=area["name"], unique_id=None
            )
            for area in areas
        ],
    )


def heating(entry: ConfigEntry) -> Any:
    """The coordinator of the running heating module."""
    return entry.runtime_data.modules[MODULE_HEATING].coordinator


def heating_options(entry: ConfigEntry) -> dict[str, Any]:
    """The options of the heating section."""
    return dict(entry.options[MODULE_HEATING])


def with_heating_options(entry: ConfigEntry, **changes: Any) -> dict[str, Any]:
    """All options of the entry with changed heating options."""
    return {**entry.options, MODULE_HEATING: {**entry.options[MODULE_HEATING], **changes}}


async def open_options(hass: HomeAssistant, entry: ConfigEntry, step: str) -> dict:
    """A settings step of the heating: the menu of the house, then the one of the heating."""
    flow = hass.config_entries.options
    result = await flow.async_init(entry.entry_id)
    result = await flow.async_configure(result["flow_id"], {"next_step_id": MODULE_HEATING})
    return await flow.async_configure(result["flow_id"], {"next_step_id": f"heating_{step}"})


async def start_setup(hass: HomeAssistant) -> dict:
    """The setup of the house with only the heating: its first step."""
    flow = hass.config_entries.flow
    result = await flow.async_init(DOMAIN, context={"source": "user"})
    return await flow.async_configure(result["flow_id"], {"modules": [MODULE_HEATING]})
