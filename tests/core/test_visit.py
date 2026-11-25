"""Visit of the house: switch, start and end, the heating of the areas and the panel."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

import pytest
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_capture_events,
    async_fire_time_changed,
)

from custom_components.house_assistant.const import DOMAIN, EVENT_LOGBOOK
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits
from custom_components.house_assistant.heating.logic.controller import AreaStatus

SWITCH = "switch.house_assistant_visit"
START = "datetime.house_assistant_visit_start"
END = "datetime.house_assistant_visit_end"
ACTIVE = "binary_sensor.house_assistant_visit_active"
VACATION = "switch.house_assistant_vacation"
DAY = "2026-11-16 10:00:00+01:00"
NIGHT = "2026-11-16 22:00:00+01:00"


def _room(sub_id: str, name: str, **data: Any) -> ConfigSubentryData:
    return ConfigSubentryData(
        data={
            "name": name,
            "temperature_sensor": f"sensor.{sub_id}_temperature",
            "heater_switch": f"input_boolean.{sub_id}_circuit",
            **data,
        },
        subentry_id=sub_id,
        subentry_type="room",
        title=name,
        unique_id=None,
    )


def _entry(living: dict[str, Any] | None = None, kids: dict[str, Any] | None = None):
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {"modules": ["heating"], "outdoor_temperature": "sensor.outdoor"},
            "heating": {**HEATING_DEFAULTS, "limits": default_limits()},
        },
        subentries_data=[
            _room("living", "Living room", visit_role="warm_floor", **(living or {})),
            _room("kids", "Kids room", visit_role="reduce", **(kids or {})),
            _room("bath", "Bath"),
        ],
    )


async def _setup(hass: HomeAssistant, entry: MockConfigEntry, temp: float = 20.0) -> None:
    await hass.config.async_set_time_zone("Europe/Berlin")
    hass.states.async_set("sensor.outdoor", "5", {"unit_of_measurement": "°C"})
    for room in ("living", "kids", "bath"):
        hass.states.async_set(f"input_boolean.{room}_circuit", "off")
        hass.states.async_set(
            f"sensor.{room}_temperature", str(temp), {"unit_of_measurement": "°C"}
        )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)


async def _switch(hass: HomeAssistant, entity_id: str, on: bool) -> None:
    await hass.services.async_call(
        "switch", "turn_on" if on else "turn_off", {"entity_id": entity_id}, blocking=True
    )
    await hass.async_block_till_done(wait_background_tasks=True)


async def _advance(hass: HomeAssistant, freezer, delta: timedelta) -> None:
    freezer.tick(delta)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)


def _coordinator(entry: MockConfigEntry) -> Any:
    return entry.runtime_data.modules["heating"].coordinator


async def test_switch_targets_logbook_and_restart(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(DAY)
    logbook = async_capture_events(hass, EVENT_LOGBOOK)
    entry = _entry()
    await _setup(hass, entry)
    coordinator = _coordinator(entry)
    assert hass.states.get(ACTIVE).state == "off"

    await _switch(hass, SWITCH, True)
    assert hass.states.get(ACTIVE).state == "on"
    assert any(e.data["message"] == "Visit starts." for e in logbook)
    await coordinator.async_refresh()
    areas = coordinator.areas
    assert coordinator.visit
    assert areas["living"].effective_target == 21.5
    assert areas["kids"].effective_target == 20.5
    assert areas["bath"].effective_target == 21.0  # no role: unchanged
    climate = hass.states.get("climate.living_room")
    assert climate.attributes["visit_active"] is True
    assert climate.attributes["visit_role"] == "warm_floor"

    # kept across a restart
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "on"

    await _switch(hass, SWITCH, False)
    assert any(e.data["message"] == "Visit ends." for e in logbook)
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert coordinator.areas["living"].effective_target == 21.0
    assert coordinator.areas["kids"].effective_target == 21.0


async def test_targets_stay_within_the_limits(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(DAY)
    entry = _entry(living={"max_target": 21.2}, kids={"min_target": 20.8})
    await _setup(hass, entry)
    await _switch(hass, SWITCH, True)
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert coordinator.areas["living"].effective_target == 21.2
    assert coordinator.areas["kids"].effective_target == 20.8


async def test_vacation_wins(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(DAY)
    entry = _entry()
    await _setup(hass, entry)
    await _switch(hass, SWITCH, True)
    await _switch(hass, VACATION, True)
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert not coordinator.visit
    assert not coordinator.areas["living"].visit
    vacation = HEATING_DEFAULTS["vacation_temperature"]
    assert coordinator.areas["living"].effective_target == vacation
    assert coordinator.areas["kids"].effective_target == vacation


async def test_floor_pulses_by_day_not_at_night(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(DAY)
    entry = _entry()
    await _setup(hass, entry, temp=21.8)  # above the visit target: no thermostat demand
    await _switch(hass, SWITCH, True)
    coordinator = _coordinator(entry)
    living = coordinator.areas["living"]
    # the circuit was switched off just now: the next pulse after 45 minutes
    await coordinator.async_refresh()
    assert living.status == AreaStatus.VISIT
    hass.states.async_set("input_boolean.living_circuit", "off", force_update=True)
    freezer.tick(timedelta(minutes=46))
    hass.states.async_set("sensor.living_temperature", "21.8", {"unit_of_measurement": "°C"})
    await coordinator._tick_area(living, dt_util.utcnow().timestamp(), 1, False, None)
    # a pulse also on a day without heating
    assert living.status == AreaStatus.VISIT_FLOOR
    assert living.decision.want_on
    assert living.visit_pulses
    # the room without a visit role stays off on a day without heating
    bath = coordinator.areas["bath"]
    await coordinator._tick_area(bath, dt_util.utcnow().timestamp(), 1, False, None)
    assert bath.status == AreaStatus.NO_HEATING_DAY

    freezer.move_to(NIGHT)
    await coordinator._tick_area(living, dt_util.utcnow().timestamp(), 1, True, None)
    assert living.status == AreaStatus.VISIT
    assert not living.decision.want_on
    assert living.effective_target == 21.5  # the raised target stays at night


async def test_start_end_and_warming_ahead(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(DAY)
    logbook = async_capture_events(hass, EVENT_LOGBOOK)
    entry = _entry()
    await _setup(hass, entry)
    coordinator = _coordinator(entry)
    now = dt_util.utcnow()
    start, end = now + timedelta(hours=3), now + timedelta(hours=8)
    for entity_id, value in ((END, end), (START, start)):
        await hass.services.async_call(
            "datetime", "set_value", {"entity_id": entity_id, "datetime": value}, blocking=True
        )
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "off"
    await coordinator.async_refresh()
    living, kids = coordinator.areas["living"], coordinator.areas["kids"]
    assert not living.visit
    # dead time and preheat reserve (30 + 30 min by default) ahead of the start
    lead = living.learned_values.dead_time_s + HEATING_DEFAULTS["preheat_reserve"] * 60
    assert living.visit_floor_from == pytest.approx(start.timestamp() - lead)

    freezer.move_to(start - timedelta(seconds=lead - 60))
    await coordinator.async_refresh()
    assert living.visit
    assert living.effective_target == 21.5
    assert not kids.visit  # the others only from the start
    assert kids.effective_target == 21.0
    warmed = [e for e in logbook if e.data["message"] == "Warming the floor ahead of the visit."]
    assert len(warmed) == 1
    await coordinator.async_refresh()
    assert len([e for e in logbook if e.data["message"] == warmed[0].data["message"]]) == 1

    await _advance(hass, freezer, timedelta(hours=1))
    assert hass.states.get(SWITCH).state == "on"
    assert hass.states.get(START).state == "unknown"
    await coordinator.async_refresh()
    assert kids.effective_target == 20.5

    freezer.move_to(end + timedelta(seconds=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "off"
    assert hass.states.get(END).state == "unknown"
    await coordinator.async_refresh()
    assert living.effective_target == 21.0


async def test_end_in_the_past_is_refused(hass: HomeAssistant) -> None:
    entry = _entry()
    await _setup(hass, entry)
    house = entry.runtime_data.house
    past = dt_util.utcnow() - timedelta(hours=1)
    with pytest.raises(ServiceValidationError):
        house.set_visit_times(None, past, strict=True)
    start = dt_util.utcnow() + timedelta(hours=2)
    with pytest.raises(ServiceValidationError):
        house.set_visit_times(start, start - timedelta(hours=1))
    assert not house.visit.on


async def test_panel(hass: HomeAssistant, hass_ws_client) -> None:
    entry = _entry()
    await _setup(hass, entry)
    client = await hass_ws_client(hass)
    await client.send_json({"id": 1, "type": "house_assistant/house/config"})
    visit = (await client.receive_json())["result"]["visit"]
    assert visit["on"] is False
    assert visit["entities"]["switch"] == SWITCH
    assert visit["entities"]["active"] == ACTIVE

    past = (dt_util.now() - timedelta(hours=1)).isoformat()
    await client.send_json({"id": 2, "type": "house_assistant/house/visit", "end": past})
    msg = await client.receive_json()
    assert not msg["success"] and msg["error"]["message"] == "visit_end_in_past"

    end = (dt_util.now() + timedelta(hours=5)).replace(microsecond=0)
    await client.send_json({"id": 3, "type": "house_assistant/house/visit", "end": end.isoformat()})
    msg = await client.receive_json()
    assert msg["success"], msg
    assert msg["result"]["visit"]["on"] is True
    assert dt_util.parse_datetime(msg["result"]["visit"]["end"]) == end
    assert hass.states.get(ACTIVE).state == "on"

    await client.send_json({"id": 4, "type": "house_assistant/house/visit", "clear": True})
    msg = await client.receive_json()
    assert msg["success"], msg
    assert msg["result"]["visit"]["on"] is False
    assert msg["result"]["visit"]["end"] is None
