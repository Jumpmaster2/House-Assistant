"""Missing sensors and switches: status, repair issues and repeated commands."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import issue_registry as ir
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.house_assistant.heating.const import DOMAIN

from .conftest import AREA_DATA, IN_SEASON, heating, make_entry


async def _setup(hass: HomeAssistant, entry) -> None:
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)


async def _advance(hass: HomeAssistant, freezer: FrozenDateTimeFactory, minutes: int) -> None:
    for _ in range(minutes):
        freezer.tick(timedelta(minutes=1))
        async_fire_time_changed(hass)
        await hass.async_block_till_done(wait_background_tasks=True)


def _issue(hass: HomeAssistant, issue_id: str) -> ir.IssueEntry | None:
    return ir.async_get(hass).async_get_issue(DOMAIN, issue_id)


def _area_id(entry) -> str:
    return next(s.subentry_id for s in entry.subentries.values() if s.title == "Living room")


async def test_unavailable_switch_has_its_own_status_and_a_repair(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(IN_SEASON)
    entry = make_entry()
    await _setup(hass, entry)
    issue_id = f"actuator_unavailable_{_area_id(entry)}"

    hass.states.async_set("input_boolean.heating_circuit_1", "unavailable")
    await _advance(hass, freezer, 1)
    assert hass.states.get("sensor.living_room_status").state == "actuator_unavailable"
    assert _issue(hass, issue_id) is None  # not before 15 minutes

    await _advance(hass, freezer, 15)
    issue = _issue(hass, issue_id)
    assert issue is not None and issue.translation_key == "actuator_unavailable"
    assert issue.translation_placeholders["entity_id"] == "input_boolean.heating_circuit_1"

    hass.states.async_set("input_boolean.heating_circuit_1", "off")
    await _advance(hass, freezer, 1)
    assert _issue(hass, issue_id) is None
    assert hass.states.get("sensor.living_room_status").state != "actuator_unavailable"


async def test_missing_temperatures_raise_repairs_until_they_are_back(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(IN_SEASON)
    entry = make_entry()
    await _setup(hass, entry)
    sensor_issue = f"sensor_unavailable_{_area_id(entry)}"

    hass.states.async_set("sensor.living_room_temperature", "unavailable")
    hass.states.async_set("sensor.outdoor_temperature", "unknown")
    await _advance(hass, freezer, 16)
    assert hass.states.get("sensor.living_room_status").state == "sensor_error"
    assert _issue(hass, sensor_issue) is not None
    assert _issue(hass, "outdoor_unavailable") is not None
    # the ventilation only area has no circuit to protect: no issue for it
    assert [i for (d, i) in ir.async_get(hass).issues if d == DOMAIN and "sensor_" in i] == [
        sensor_issue
    ]

    hass.states.async_set("sensor.living_room_temperature", "19.0", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.outdoor_temperature", "5.0", {"unit_of_measurement": "°C"})
    await _advance(hass, freezer, 1)
    assert _issue(hass, sensor_issue) is None
    assert _issue(hass, "outdoor_unavailable") is None


async def test_switch_that_does_not_follow_is_asked_again_with_pauses(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    """A switch that ignores its commands is not hammered every minute."""
    freezer.move_to(IN_SEASON)
    hass.states.async_set("switch.dead_relay", "off")
    calls: list[str] = []

    async def record(call: ServiceCall) -> None:
        calls.append(call.service)

    entry = make_entry(areas=[{**AREA_DATA, "heater_switch": "switch.dead_relay"}])
    await _setup(hass, entry)
    # after the setup: loading the switch platform registers the real services
    hass.services.async_register("switch", "turn_on", record)
    hass.services.async_register("switch", "turn_off", record)
    issue_id = f"actuator_not_responding_{_area_id(entry)}"

    # 19 °C below the target: the first command after the minimum off time (10 min),
    # then after 1, 2, 4 and 8 minutes; every minute would have been 21 commands
    await _advance(hass, freezer, 30)
    assert calls == ["turn_on"] * 5
    assert _issue(hass, issue_id) is not None

    # the switch follows again: counter and issue are reset
    hass.states.async_set("switch.dead_relay", "on")
    await _advance(hass, freezer, 1)
    assert _issue(hass, issue_id) is None
    coordinator = heating(entry)
    assert coordinator.areas[_area_id(entry)].cmd_attempts == 0


async def test_dismissed_repair_survives_a_reload_and_removal_deletes_it(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(IN_SEASON)
    entry = make_entry()
    await _setup(hass, entry)
    hass.states.async_set("sensor.outdoor_temperature", "unavailable")
    await _advance(hass, freezer, 16)
    assert _issue(hass, "outdoor_unavailable") is not None
    ir.async_ignore_issue(hass, DOMAIN, "outdoor_unavailable", True)

    assert await hass.config_entries.async_reload(entry.entry_id)
    await _advance(hass, freezer, 16)
    issue = _issue(hass, "outdoor_unavailable")
    assert issue is not None and issue.dismissed_version is not None

    await hass.config_entries.async_remove(entry.entry_id)
    await hass.async_block_till_done()
    assert [i for (d, i) in ir.async_get(hass).issues if d == DOMAIN] == []


async def test_issue_of_a_deleted_area_is_dropped(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(IN_SEASON)
    entry = make_entry()
    await _setup(hass, entry)
    issue_id = f"sensor_unavailable_{_area_id(entry)}"
    hass.states.async_set("sensor.living_room_temperature", "unavailable")
    await _advance(hass, freezer, 16)
    assert _issue(hass, issue_id) is not None
    hass.config_entries.async_remove_subentry(entry, _area_id(entry))
    await hass.async_block_till_done(wait_background_tasks=True)
    assert _issue(hass, issue_id) is None


async def test_unchanged_temperature_repair_clears(
    hass: HomeAssistant, base_states, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to(IN_SEASON)
    entry = make_entry(sensor_stale_hours=1)
    await _setup(hass, entry)
    sensor = "sensor.living_room_temperature"
    hass.states.async_set(sensor, "19.1", {"unit_of_measurement": "°C"})
    issue_id = f"sensor_stale_{_area_id(entry)}"
    await _advance(hass, freezer, 59)
    assert _issue(hass, issue_id) is None
    with patch.object(ir, "async_create_issue", wraps=ir.async_create_issue) as create_issue:
        await _advance(hass, freezer, 2)
        issue = _issue(hass, issue_id)
        assert issue is not None and issue.translation_key == "sensor_stale"
        assert issue.translation_placeholders == {
            "entity_id": sensor,
            "area": "Living room",
            "hours": "1",
        }
        await _advance(hass, freezer, 2)
        assert sum(call.args[2] == issue_id for call in create_issue.call_args_list) == 1
        hass.states.async_set(sensor, "19.2", {"unit_of_measurement": "°C"})
        await _advance(hass, freezer, 1)
        assert _issue(hass, issue_id) is None


async def test_stale_check_disabled(hass: HomeAssistant, base_states, freezer) -> None:
    entry = make_entry(sensor_stale_hours=0)
    await _setup(hass, entry)
    await _advance(hass, freezer, 65)
    assert _issue(hass, f"sensor_stale_{_area_id(entry)}") is None


@pytest.mark.parametrize("state", ["unavailable", "unknown", "not a number", "100"])
async def test_invalid_temperature_only_raises_unavailable(
    hass: HomeAssistant, base_states, freezer, state: str
) -> None:
    entry = make_entry(sensor_stale_hours=1)
    await _setup(hass, entry)
    await _advance(hass, freezer, 61)
    assert _issue(hass, f"sensor_stale_{_area_id(entry)}") is not None
    hass.states.async_set("sensor.living_room_temperature", state, {"unit_of_measurement": "°C"})
    await _advance(hass, freezer, 16)
    assert _issue(hass, f"sensor_unavailable_{_area_id(entry)}") is not None
    assert _issue(hass, f"sensor_stale_{_area_id(entry)}") is None


async def test_no_circuit_has_no_stale_repair(hass: HomeAssistant, base_states, freezer) -> None:
    entry = make_entry(sensor_stale_hours=1)
    await _setup(hass, entry)
    storage = next(s.subentry_id for s in entry.subentries.values() if s.title == "Storage room")
    await _advance(hass, freezer, 65)
    assert _issue(hass, f"sensor_stale_{storage}") is None
    assert _issue(hass, f"sensor_stale_{_area_id(entry)}") is not None


async def test_stale_repair_does_not_change_control(
    hass: HomeAssistant, base_states, freezer
) -> None:
    entry = make_entry(sensor_stale_hours=1)
    await _setup(hass, entry)
    await _advance(hass, freezer, 59)
    area = heating(entry).areas[_area_id(entry)]
    switch = hass.states.get("input_boolean.heating_circuit_1").state
    target = area.target
    effective_target = area.effective_target
    await _advance(hass, freezer, 2)
    assert _issue(hass, f"sensor_stale_{_area_id(entry)}") is not None
    assert hass.states.get("input_boolean.heating_circuit_1").state == switch
    assert area.target == target
    assert area.effective_target == effective_target
