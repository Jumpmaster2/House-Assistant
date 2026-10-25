"""What one module reads from another. Modules talk to each other only here.

A module that is switched off (or not running yet) gives None, the module asking
then behaves as without it. The heating announces changes other modules depend on
(target of a room, heating day, start and stop) with ``SIGNAL_HEATING``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_send

from ..const import DOMAIN, MODULE_HEATING, MODULE_METER, MODULE_SHUTTER
from ..heating.const import CONF_HEAT_METER
from .entry import running_module

# status of a meter reading confirmed below the previous one (meter.logic.reading)
STATUS_CORRECTED = "corrected"

SIGNAL_HEATING = f"{DOMAIN}_heating_changed"


def _heating(hass: HomeAssistant) -> Any:
    return getattr(running_module(hass, MODULE_HEATING), "coordinator", None)


@callback
def heating_changed(hass: HomeAssistant) -> None:
    """The heating changed something the other modules read."""
    async_dispatcher_send(hass, SIGNAL_HEATING)


def heating_day(hass: HomeAssistant) -> bool | None:
    """Is today a heating day? Only within the heating period (or heating chosen by hand
    for today); None without the heating module."""
    coordinator = _heating(hass)
    if coordinator is None:
        return None
    return bool(coordinator.heats_now and coordinator.heating_day)


def room_heating(hass: HomeAssistant) -> bool | None:
    """Does a room heat now, or is a heating phase still open for its reading? None
    without the heating module."""
    coordinator = _heating(hass)
    return None if coordinator is None else coordinator.room_heating()


def rooms_on(hass: HomeAssistant) -> bool | None:
    """Is the circuit of a room on? None without the heating module."""
    coordinator = _heating(hass)
    return None if coordinator is None else coordinator.rooms_on()


def is_heat_meter(hass: HomeAssistant, meter_id: str) -> bool:
    """Is the meter (its config subentry) the heat meter of the heating?"""
    coordinator = _heating(hass)
    entity_id = coordinator.opt(CONF_HEAT_METER) if coordinator is not None else None
    entry = er.async_get(hass).async_get(entity_id) if entity_id else None
    return entry is not None and entry.platform == DOMAIN and entry.config_subentry_id == meter_id


@dataclass(frozen=True, slots=True)
class MeterReading:
    """When a meter of the meter module was read and whether the value was a correction."""

    ts: float
    corrected: bool


def meter_reading(hass: HomeAssistant, entity_id: str | None) -> MeterReading | None:
    """The reading behind a reading sensor of the meter module, None for another entity
    or while the meter module is not running."""
    entry = er.async_get(hass).async_get(entity_id) if entity_id else None
    if entry is None or entry.platform != DOMAIN or not entry.unique_id.endswith("_reading"):
        return None
    manager = getattr(running_module(hass, MODULE_METER), "manager", None)
    meter = manager.meters.get(entry.config_subentry_id) if manager is not None else None
    if meter is None or meter.state.value_time is None:
        return None
    return MeterReading(meter.state.value_time.timestamp(), meter.state.status == STATUS_CORRECTED)


def room_target(hass: HomeAssistant, room_id: str | None) -> float | None:
    """Target temperature (°C) of the thermostat of a room, None without a circuit."""
    coordinator = _heating(hass)
    area = coordinator.areas.get(room_id) if coordinator is not None and room_id else None
    if area is None or not area.has_circuit:
        return None
    return float(area.target)


def preheat_start(hass: HomeAssistant) -> float | None:
    """Earliest start of preheating for the return of a vacation (timestamp), None
    without the heating or without a return ahead."""
    coordinator = _heating(hass)
    return coordinator.preheat_from if coordinator is not None else None


def vacation_simulation(hass: HomeAssistant) -> bool | None:
    """Do covers take part in the presence simulation of a vacation? None without the
    cover module."""
    engine = getattr(running_module(hass, MODULE_SHUTTER), "engine", None)
    if engine is None:
        return None
    return any(win.rules.vacation for win in engine.windows.values())


def leak_meters(hass: HomeAssistant) -> list[str] | None:
    """Meters that warn when something runs on vacation, None without the meter module."""
    manager = getattr(running_module(hass, MODULE_METER), "manager", None)
    if manager is None:
        return None
    return [meter.title for meter in manager.meters.values() if meter.leak_warning]
