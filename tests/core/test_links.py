"""What the modules take from each other: heating day, room target and heat meter."""

from __future__ import annotations

from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN
from custom_components.house_assistant.core.links import heating_day, meter_reading
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits
from custom_components.house_assistant.meter.const import meter_defaults

IN_SEASON = "2026-11-16 10:00:00+01:00"
SUMMER = "2026-07-16 10:00:00+02:00"
HEAT_METER_ID = "meter_heat"
READING = "sensor.heat_meter_reading"


def _entry(heating: dict[str, Any] | None = None, shutter: dict[str, Any] | None = None):
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {"modules": ["heating", "shutter", "meter"]},
            "heating": {
                **HEATING_DEFAULTS,
                "outdoor_temperature": "sensor.outdoor",
                "limits": default_limits(),
                **(heating or {}),
            },
            "shutter": {"outdoor_temperature": "sensor.outdoor", **(shutter or {})},
            "meter": {"ai_task_entity": "ai_task.claude"},
        },
        subentries_data=[
            ConfigSubentryData(
                data={
                    "name": "Living room",
                    "temperature_sensor": "sensor.living_temperature",
                    "heater_switch": "input_boolean.circuit",
                },
                subentry_id="room_living",
                subentry_type="room",
                title="Living room",
                unique_id=None,
            ),
            ConfigSubentryData(
                data={
                    **meter_defaults("heat"),
                    "camera": "camera.heat_cam",
                    "warmup": 0,
                    "interval": 30,
                    "interval_off": 360,
                    "condition_heating_day": True,
                },
                subentry_id=HEAT_METER_ID,
                subentry_type="meter",
                title="Heat",
                unique_id=None,
            ),
        ],
    )


async def _setup(hass: HomeAssistant, freezer, entry: MockConfigEntry, when: str = IN_SEASON):
    freezer.move_to(when)
    await hass.config.async_set_time_zone("Europe/Berlin")
    hass.states.async_set("sensor.outdoor", "5", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_temperature", "20", {"unit_of_measurement": "°C"})
    hass.states.async_set("input_boolean.circuit", "off")
    hass.states.async_set("camera.heat_cam", "idle")
    hass.states.async_set("ai_task.claude", "unknown")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)


def _module(entry: MockConfigEntry, key: str) -> Any:
    return entry.runtime_data.modules[key]


async def test_covers_and_meters_follow_the_heating_day(hass: HomeAssistant, freezer) -> None:
    entry = _entry()
    await _setup(hass, freezer, entry)
    heating = _module(entry, "heating").coordinator
    engine = _module(entry, "shutter").engine
    meter = _module(entry, "meter").manager.meters[HEAT_METER_ID]

    await heating.async_set_override("heat_today")
    await hass.async_block_till_done()
    assert heating_day(hass) is True
    assert engine.heating_day
    # a heating day alone does not read the heat meter often: no room heats (idle interval)
    assert meter.interval_minutes() == 1440

    await heating.async_set_override("off_today")
    await hass.async_block_till_done()
    assert heating_day(hass) is False
    assert not engine.heating_day
    assert meter.interval_minutes() == 1440

    # the switch of the covers, and an own entity wins over the heating day
    await heating.async_set_override("heat_today")
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "shutter": {**entry.options["shutter"], "use_heating_day": False},
        },
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    assert not _module(entry, "shutter").engine.heating_day
    hass.states.async_set("input_boolean.season", "on")
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "shutter": {**entry.options["shutter"], "heating_entity": "input_boolean.season"},
        },
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    assert _module(entry, "shutter").engine.heating_day

    # without the heating module there is no heating day: the normal interval
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": ["shutter", "meter"]}}
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    assert heating_day(hass) is None
    assert _module(entry, "meter").manager.meters[HEAT_METER_ID].interval_minutes() == 30


async def test_no_heating_day_outside_the_heating_period(hass: HomeAssistant, freezer) -> None:
    entry = _entry()
    await _setup(hass, freezer, entry, SUMMER)
    # a stale decision of the spring does not count in summer
    assert heating_day(hass) is False
    assert not _module(entry, "shutter").engine.heating_day


async def test_heating_reads_the_meter_module(hass: HomeAssistant, freezer) -> None:
    entry = _entry(heating={"heat_meter": READING})
    await _setup(hass, freezer, entry)
    meter = _module(entry, "meter").manager.meters[HEAT_METER_ID]
    heating = _module(entry, "heating").coordinator

    read_at = dt_util.utcnow() - timedelta(minutes=10)
    # the heat meter counts in MWh
    meter.state.value, meter.state.value_time, meter.state.status = 1.0, read_at, "ok"
    meter.notify()
    await hass.async_block_till_done()
    assert meter_reading(hass, READING).ts == read_at.timestamp()
    assert meter_reading(hass, "sensor.outdoor") is None
    await heating.async_refresh()
    # the time the meter was read, not the time the heating saw the value
    assert heating.meter.last.ts == read_at.timestamp()
    heating.meter.rebase("today")

    later = dt_util.utcnow() - timedelta(minutes=2)
    meter.state.value, meter.state.value_time, meter.state.status = 1.08, later, "ok"
    meter.notify()
    await hass.async_block_till_done()
    await heating.async_refresh()
    # a confirmed correction downwards is no new meter: today keeps its start
    now = dt_util.utcnow()
    meter.state.value, meter.state.value_time, meter.state.status = 1.004, now, "corrected"
    meter.notify()
    await hass.async_block_till_done()
    await heating.async_refresh()
    assert heating.meter.baselines["today"].kwh == pytest.approx(1000.0)
    assert heating.meter.kwh_since("today") == pytest.approx(4.0)


async def test_heat_meter_is_read_while_a_room_heats(hass: HomeAssistant, freezer) -> None:
    entry = _entry(heating={"heat_meter": READING})
    await _setup(hass, freezer, entry)
    manager = _module(entry, "meter").manager
    meter = manager.meters[HEAT_METER_ID]
    heating = _module(entry, "heating").coordinator
    heating._control_area = AsyncMock()  # the circuit is switched by hand here
    assert not heating.room_heating()
    assert meter.interval_minutes() == 1440

    # a room starts heating: the heat meter is read at the short interval, and a reading
    # is asked for at once (the last one is older than the minimum gap)
    meter.state.last_check = dt_util.utcnow() - timedelta(minutes=30)
    with patch.object(manager, "start_reading") as start:
        hass.states.async_set("input_boolean.circuit", "on")
        await heating.async_refresh()
        await hass.async_block_till_done()
        assert heating.room_heating()
        assert meter.interval_minutes() == 15
        start.assert_called_once_with(meter)

        # the room stops: one more reading at the end of the phase
        hass.states.async_set("input_boolean.circuit", "off")
        await heating.async_refresh()
        await hass.async_block_till_done()
        assert meter.interval_minutes() == 1440
        assert start.call_count == 2

        # a change within the minimum gap of the last reading asks for none
        meter.state.last_check = dt_util.utcnow() - timedelta(minutes=2)
        hass.states.async_set("input_boolean.circuit", "on")
        await heating.async_refresh()
        await hass.async_block_till_done()
        assert start.call_count == 2
