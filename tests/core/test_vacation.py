"""Vacation of the house: switch, departure and return, external sources, the heating,
the report of open windows and the panel."""

from __future__ import annotations

from datetime import timedelta
from typing import Any
from unittest.mock import patch

import pytest
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_capture_events,
    async_fire_time_changed,
)

from custom_components.house_assistant.const import DOMAIN, EVENT_LOGBOOK, EVENT_VACATION
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits

SWITCH = "switch.house_assistant_vacation"
DEPARTURE = "datetime.house_assistant_vacation_departure"
RETURN = "datetime.house_assistant_vacation_return"
ACTIVE = "binary_sensor.house_assistant_vacation_active"
IN_SEASON = "2026-11-16 10:00:00+01:00"


def _sub(sub_id: str, subentry_type: str, data: dict[str, Any]) -> ConfigSubentryData:
    return ConfigSubentryData(
        data=data,
        subentry_id=sub_id,
        subentry_type=subentry_type,
        title=data["name"],
        unique_id=None,
    )


def _entry(core: dict[str, Any] | None = None, **heating: Any) -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {
                "modules": ["heating"],
                "outdoor_temperature": "sensor.outdoor",
                "notify_services": ["notify.phone"],
                **(core or {}),
            },
            "heating": {**HEATING_DEFAULTS, "limits": default_limits(), **heating},
        },
        subentries_data=[
            _sub(
                "living",
                "room",
                {
                    "name": "Living room",
                    "temperature_sensor": "sensor.living_temperature",
                    "humidity_sensor": "sensor.living_humidity",
                    "heater_switch": "input_boolean.circuit",
                },
            ),
            _sub(
                "kitchen_window",
                "window",
                {
                    "name": "Kitchen window",
                    "room": "living",
                    "window_sensors": ["binary_sensor.kitchen"],
                },
            ),
            _sub(
                "bath_window",
                "window",
                {
                    "name": "Bath window",
                    "window_sensors": ["binary_sensor.bath"],
                    "tilt_sensors": ["binary_sensor.bath_tilt"],
                },
            ),
        ],
    )


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> list[ServiceCall]:
    await hass.config.async_set_time_zone("Europe/Berlin")
    sent: list[ServiceCall] = []

    async def phone(call: ServiceCall) -> None:
        sent.append(call)

    hass.services.async_register("notify", "phone", phone)
    hass.states.async_set("input_boolean.circuit", "off")
    hass.states.async_set("sensor.outdoor", "5", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_temperature", "20", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_humidity", "70", {"unit_of_measurement": "%"})
    for entity_id in ("binary_sensor.kitchen", "binary_sensor.bath", "binary_sensor.bath_tilt"):
        hass.states.async_set(entity_id, "off")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    return sent


async def _switch(hass: HomeAssistant, on: bool) -> None:
    await hass.services.async_call(
        "switch", "turn_on" if on else "turn_off", {"entity_id": SWITCH}, blocking=True
    )
    await hass.async_block_till_done(wait_background_tasks=True)


def _coordinator(entry: MockConfigEntry) -> Any:
    return entry.runtime_data.modules["heating"].coordinator


async def test_switch_event_logbook_and_restart(hass: HomeAssistant) -> None:
    events = async_capture_events(hass, EVENT_VACATION)
    logbook = async_capture_events(hass, EVENT_LOGBOOK)
    entry = _entry()
    await _setup(hass, entry)
    assert hass.states.get(ACTIVE).state == "off"
    # one device for the house
    assert (
        er.async_get(hass).async_get(SWITCH).device_id
        == er.async_get(hass).async_get(ACTIVE).device_id
    )

    await _switch(hass, True)
    assert hass.states.get(ACTIVE).state == "on"
    assert hass.states.get(ACTIVE).attributes["source"] == "switch"
    assert [e.data for e in events] == [{"active": True, "source": "switch"}]
    assert any(e.data["message"] == "Vacation starts (switch)." for e in logbook)
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert coordinator.vacation
    assert coordinator.areas["living"].effective_target == HEATING_DEFAULTS["vacation_temperature"]

    # kept across a restart, without a second start
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "on"
    assert hass.states.get(ACTIVE).state == "on"
    assert len(events) == 1

    await _switch(hass, False)
    assert hass.states.get(ACTIVE).state == "off"
    assert events[-1].data == {"active": False, "source": None}


async def test_departure_and_return(hass: HomeAssistant, freezer) -> None:
    freezer.move_to(IN_SEASON)
    entry = _entry()
    await _setup(hass, entry)
    now = dt_util.utcnow()
    departure, back = now + timedelta(hours=1), now + timedelta(days=2)
    for entity_id, value in ((RETURN, back), (DEPARTURE, departure)):
        await hass.services.async_call(
            "datetime", "set_value", {"entity_id": entity_id, "datetime": value}, blocking=True
        )
    await hass.async_block_till_done()
    # the return first, then a departure ahead: the vacation starts at the departure
    assert hass.states.get(SWITCH).state == "off"
    assert hass.states.get(ACTIVE).state == "off"
    assert dt_util.parse_datetime(hass.states.get(DEPARTURE).state) == departure

    freezer.tick(timedelta(hours=1, seconds=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "on"
    assert hass.states.get(DEPARTURE).state == "unknown"
    # the heating preheats for the own return
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert coordinator._return_ts() == pytest.approx(back.timestamp())

    freezer.move_to(back + timedelta(seconds=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(SWITCH).state == "off"
    assert hass.states.get(ACTIVE).state == "off"
    assert hass.states.get(RETURN).state == "unknown"


async def test_service(hass: HomeAssistant) -> None:
    await _setup(hass, _entry())
    back = dt_util.now() + timedelta(days=3)
    # only a return: vacation from now on
    await hass.services.async_call(DOMAIN, "set_vacation", {"return": back}, blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(ACTIVE).state == "on"
    # a return in the past is ignored
    await hass.services.async_call(
        DOMAIN, "set_vacation", {"return": dt_util.now() - timedelta(days=1)}, blocking=True
    )
    assert hass.states.get(RETURN).state != "unknown"
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "set_vacation",
            {"departure": back + timedelta(days=1), "return": back},
            blocking=True,
        )
    await hass.services.async_call(DOMAIN, "set_vacation", {"clear": True}, blocking=True)
    await hass.async_block_till_done()
    assert hass.states.get(SWITCH).state == "off"
    assert hass.states.get(RETURN).state == "unknown"


async def test_external_sources(hass: HomeAssistant) -> None:
    hass.states.async_set("input_boolean.away", "off")
    hass.states.async_set("input_boolean.heating_away", "off")
    entry = _entry(vacation_entities=["input_boolean.heating_away"])
    await _setup(hass, entry)
    # without sources of the house the ones of the heating count
    hass.states.async_set("input_boolean.heating_away", "on")
    await hass.async_block_till_done()
    assert hass.states.get(ACTIVE).attributes["source"] == "input_boolean.heating_away"
    hass.states.async_set("input_boolean.heating_away", "off")
    await hass.async_block_till_done()
    assert hass.states.get(ACTIVE).state == "off"

    # sources of the house win, for the heating as well
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "core": {**entry.options["core"], "vacation_entities": ["input_boolean.away"]},
        },
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    hass.states.async_set("input_boolean.away", "on")
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get(ACTIVE).state == "on"
    coordinator = _coordinator(entry)
    await coordinator.async_refresh()
    assert coordinator.opt("vacation_entities") == ["input_boolean.away"]
    assert coordinator.vacation


async def test_open_windows_at_the_departure_and_on_vacation(hass: HomeAssistant, freezer) -> None:
    sent = await _setup(hass, _entry())
    hass.states.async_set("binary_sensor.kitchen", "on")
    hass.states.async_set("binary_sensor.bath", "unavailable")
    await hass.async_block_till_done()
    await _switch(hass, True)
    assert len(sent) == 1
    assert sent[0].data["message"] == (
        "Vacation starts, these windows are not closed: Kitchen window (open), "
        "Bath window (unknown)."
    )
    assert hass.states.get(ACTIVE).attributes["open_windows"] == {
        "Kitchen window": "open",
        "Bath window": "unknown",
    }

    # a contact coming back is no opening
    hass.states.async_set("binary_sensor.bath", "on")
    await hass.async_block_till_done()
    hass.states.async_set("binary_sensor.kitchen", "off")
    hass.states.async_set("binary_sensor.bath", "off")
    await hass.async_block_till_done()
    # tilted on vacation: reported once it stayed so
    hass.states.async_set("binary_sensor.bath_tilt", "on")
    await hass.async_block_till_done()
    assert len(sent) == 1
    freezer.tick(timedelta(seconds=11))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert [c.data["message"] for c in sent[1:]] == ["Bath window was tilted on vacation."]
    # a bounce is not reported
    hass.states.async_set("binary_sensor.kitchen", "on")
    await hass.async_block_till_done()
    hass.states.async_set("binary_sensor.kitchen", "off")
    await hass.async_block_till_done()
    freezer.tick(timedelta(seconds=11))
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert len(sent) == 2


async def test_ventilation_advice_rests(hass: HomeAssistant) -> None:
    entry = _entry()
    await _setup(hass, entry)
    registry = er.async_get(hass)
    advice = registry.async_get_entity_id("sensor", DOMAIN, "living_ventilation")
    assert hass.states.get(advice).state != "vacation"
    await _switch(hass, True)
    coordinator = _coordinator(entry)
    profile = coordinator.areas["living"].humidity_profile
    with patch.object(profile, "add_sample") as add_sample:
        await coordinator.async_refresh()
        await hass.async_block_till_done()
    # vacation days stay out of the humidity profile
    add_sample.assert_not_called()
    assert hass.states.get(advice).state == "vacation"
    recommended = registry.async_get_entity_id(
        "binary_sensor", DOMAIN, "living_ventilation_recommended"
    )
    assert hass.states.get(recommended).state == "off"

    # switched off for the heating: the advice goes on
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "heating": {**entry.options["heating"], "vacation_ventilation_pause": False},
        },
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    await _coordinator(entry).async_refresh()
    await hass.async_block_till_done()
    assert hass.states.get(advice).state != "vacation"


async def test_panel(hass: HomeAssistant, hass_ws_client) -> None:
    entry = _entry()
    client = await hass_ws_client(hass)
    await _setup(hass, entry)
    await client.send_json({"id": 1, "type": "house_assistant/config"})
    assert (await client.receive_json())["result"]["vacation_entity"] == ACTIVE
    await client.send_json({"id": 2, "type": "house_assistant/house/config"})
    vacation = (await client.receive_json())["result"]["vacation"]
    assert vacation["on"] is False
    assert vacation["entities"]["switch"] == SWITCH
    assert vacation["options"] == {"vacation_ventilation_pause": True}

    # the panel refuses a return in the past
    past = (dt_util.now() - timedelta(hours=1)).isoformat()
    await client.send_json({"id": 3, "type": "house_assistant/house/vacation", "return": past})
    msg = await client.receive_json()
    assert not msg["success"] and msg["error"]["message"] == "return_in_past"
    back = (dt_util.now() + timedelta(days=2)).replace(microsecond=0)
    await client.send_json(
        {"id": 4, "type": "house_assistant/house/vacation", "return": back.isoformat()}
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    assert msg["result"]["vacation"]["on"] is True
    assert dt_util.parse_datetime(msg["result"]["vacation"]["return"]) == back

    await client.send_json(
        {
            "id": 5,
            "type": "house_assistant/house/vacation_settings",
            "settings": {
                "vacation_entities": ["input_boolean.away"],
                "vacation_window_alert": False,
            },
            "options": {"vacation_ventilation_pause": False, "vacation_heat_protection": False},
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    await hass.async_block_till_done(wait_background_tasks=True)
    assert entry.options["core"]["vacation_entities"] == ["input_boolean.away"]
    assert entry.options["core"]["vacation_window_alert"] is False
    assert entry.options["heating"]["vacation_ventilation_pause"] is False
    # the covers are not switched on: nothing stored for them
    assert "shutter" not in entry.options
    # the other settings of the house stay
    assert entry.options["core"]["outdoor_temperature"] == "sensor.outdoor"
    # the vacation goes on after the restart of the modules
    assert hass.states.get(ACTIVE).state == "on"
