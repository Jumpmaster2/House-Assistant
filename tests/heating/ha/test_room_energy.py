"""The heat meter split over the rooms in Home Assistant: sensors, the phases of the
coordinator and the store."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import AsyncMock

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from custom_components.house_assistant.const import DOMAIN

from .conftest import AREA_DATA, VENT_ONLY_DATA, heating, make_entry

METER = "sensor.heat_meter"
CIRCUIT = "input_boolean.heating_circuit_1"
ROOM = "room_1"  # the living room of the test house (see AREA_DATA)


def _entity(hass: HomeAssistant, unique_id: str) -> str | None:
    return er.async_get(hass).async_get_entity_id("sensor", DOMAIN, unique_id)


async def _tick(hass: HomeAssistant, freezer, coordinator, minutes: float = 5) -> None:
    """One control tick, the clock moves on by ``minutes`` (the tick counts at most 5)."""
    freezer.tick(timedelta(minutes=minutes))
    await coordinator.async_refresh()
    await hass.async_block_till_done()


async def _setup(hass: HomeAssistant, areas: list[dict]):
    hass.states.async_set(METER, "1000", {"unit_of_measurement": "kWh"})
    entry = make_entry(areas=areas, heat_meter=METER)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    coordinator = heating(entry)
    # the circuits are switched by hand in these tests, not by the control
    coordinator._control_area = AsyncMock()
    return entry, coordinator


async def test_heat_meter_is_split_over_the_rooms(hass: HomeAssistant, base_states, freezer):
    entry, coordinator = await _setup(hass, [{**AREA_DATA, "floor_area": 20.0}, VENT_ONLY_DATA])
    await _tick(hass, freezer, coordinator)  # first reading: the first phase starts
    hass.states.async_set(CIRCUIT, "on")
    for _ in range(4):  # 20 minutes of run time
        await _tick(hass, freezer, coordinator)
    hass.states.async_set(METER, "1001", {"unit_of_measurement": "kWh"})
    await _tick(hass, freezer, coordinator)  # the new value closes the phase

    room = coordinator.room_energy.counter(ROOM)
    assert room.total == pytest.approx(1.0)
    assert coordinator.room_energy.unassigned.total == pytest.approx(0.0)
    sensor = _entity(hass, f"{ROOM}_heat_consumption")
    assert sensor is not None
    assert float(hass.states.get(sensor).state) == pytest.approx(1.0)
    assert hass.states.get(sensor).attributes["floor_area_missing"] is False
    power = _entity(hass, f"{ROOM}_heat_power")
    assert float(hass.states.get(power).state) > 0

    # no room heats: the next kWh is not assigned, the room total stays
    hass.states.async_set(CIRCUIT, "off")
    await _tick(hass, freezer, coordinator)
    hass.states.async_set(METER, "1002", {"unit_of_measurement": "kWh"})
    await _tick(hass, freezer, coordinator)
    assert coordinator.room_energy.unassigned.total == pytest.approx(1.0)
    assert room.total == pytest.approx(1.0)
    unassigned = _entity(hass, f"{entry.entry_id}_unassigned_heat")
    assert float(hass.states.get(unassigned).state) == pytest.approx(1.0)


async def test_room_without_floor_area_takes_no_part(hass: HomeAssistant, base_states, freezer):
    _, coordinator = await _setup(hass, [AREA_DATA, VENT_ONLY_DATA])
    await _tick(hass, freezer, coordinator)
    hass.states.async_set(CIRCUIT, "on")
    for _ in range(4):
        await _tick(hass, freezer, coordinator)
    hass.states.async_set(METER, "1001", {"unit_of_measurement": "kWh"})
    await _tick(hass, freezer, coordinator)

    sensor = _entity(hass, f"{ROOM}_heat_consumption")
    state = hass.states.get(sensor)
    assert state.state == "unknown"
    assert state.attributes["floor_area_missing"] is True
    # nothing is assigned to a room without area; the kWh are not assigned to the rest
    assert coordinator.room_energy.unassigned.total == pytest.approx(1.0)


async def test_no_room_sensors_without_heat_meter(hass: HomeAssistant, base_states) -> None:
    entry = make_entry(areas=[{**AREA_DATA, "floor_area": 20.0}, VENT_ONLY_DATA])
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert _entity(hass, f"{ROOM}_heat_consumption") is None
    assert _entity(hass, f"{entry.entry_id}_unassigned_heat") is None


async def test_phases_are_saved(hass: HomeAssistant, base_states, freezer):
    _, coordinator = await _setup(hass, [{**AREA_DATA, "floor_area": 20.0}, VENT_ONLY_DATA])
    await _tick(hass, freezer, coordinator)
    hass.states.async_set(CIRCUIT, "on")
    await _tick(hass, freezer, coordinator)
    saved = coordinator._data_to_save()["room_energy"]
    assert saved["areas"] == {ROOM: 20.0}
    assert saved["runs"][ROOM]["hours"] > 0
    assert saved["start"] == pytest.approx(1000.0)
