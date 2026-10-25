"""Heating module: learning heating control with periodic AI review, heating day and
ventilation advice per room (formerly AI Heating Assistant)."""

from __future__ import annotations

import json
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity import Entity

from ..core.house import CONF_AREA
from ..core.links import heating_changed
from ..core.store import module_store
from ..runtime import Module, register_module
from .binary_sensor import HeatingDaySensor, VentilationRecommended
from .climate import AreaClimate
from .const import (
    CONF_HEAT_METER,
    CONF_SWITCH,
    DOMAIN,
    LOGGER,
    MODULE_HEATING,
    SUBENTRY_ROOM,
    SUBENTRY_WINDOW,
)
from .coordinator import HeatingCoordinator, async_delete_issues, async_turn_off_switches
from .entity import global_device_info
from .select import HeatingDayOverride
from .sensor import (
    AREA_SENSORS,
    ROOM_HEAT_KEYS,
    AiCostSensor,
    AiTimestampSensor,
    AreaSensor,
    HeatingDayPhaseSensor,
    HeatTodaySensor,
    RoomHeatSensor,
    UnassignedHeatSensor,
)
from .switch import AiEnabledSwitch


@register_module
class HeatingModule(Module):
    """The rooms with their heating circuits, the heating day and the AI."""

    key = MODULE_HEATING
    # the windows of a room give its contacts
    subentry_types = (SUBENTRY_ROOM, SUBENTRY_WINDOW)

    coordinator: HeatingCoordinator | None = None
    # what the other modules last heard: heating day and the targets of the rooms
    _announced: Any = None

    def signature(self) -> str:
        # a new or removed API key starts the AI client anew
        return json.dumps([super().signature(), self.entry.data.get(CONF_API_KEY) or ""])

    async def async_setup(self) -> None:
        coordinator = HeatingCoordinator(self)
        # Create the device of the module first so room devices can point to it by id.
        device = dr.async_get(self.hass).async_get_or_create(
            config_entry_id=self.entry.entry_id, **global_device_info(self.entry.entry_id)
        )
        coordinator.global_device_id = device.id
        self.coordinator = coordinator
        await coordinator.async_start()
        self._remove_stale_entities()
        self._place_room_devices()

    @callback
    def started(self) -> None:
        coordinator = self.coordinator
        assert coordinator is not None
        self.async_on_stop(coordinator.async_add_listener(self._announce))
        self._announce()

    @callback
    def _announce(self) -> None:
        """Tell the other modules about a new heating day, target or start of preheating
        (covers compare the room temperature with the target of its thermostat)."""
        coordinator = self.coordinator
        if coordinator is None:
            return
        current = (
            coordinator.heats_now and coordinator.heating_day,
            sorted((a.area_id, a.target) for a in coordinator.areas.values() if a.has_circuit),
            # the house shows when preheating for the return of a vacation starts
            coordinator.preheat_from,
            # start and end of a heating phase: the heat meter is read then
            coordinator.rooms_on(),
            # the short interval of the heat meter, up to 30 minutes after the end
            coordinator.room_heating(),
        )
        if current != self._announced:
            self._announced = current
            heating_changed(self.hass)

    async def async_unload(self) -> None:
        coordinator = self.coordinator
        if coordinator is None:
            return
        # the others go on without the heating
        heating_changed(self.hass)
        # stop the control first, so no tick switches a circuit on again
        await coordinator.async_shutdown()
        if self.switched_off or self.entry.disabled_by is not None:
            # nothing controls the circuits any more: one left on would heat without limit
            reason = "disabled" if self.entry.disabled_by is not None else "switched off"
            await _async_switch_off_circuits(
                self.hass, self.entry, reason, coordinator.pending_release
            )
            async_delete_issues(self.hass)

    @classmethod
    async def async_remove_entry(cls, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Switch off the circuits, then delete the learned data."""
        store = module_store(hass, entry, MODULE_HEATING)
        # switches dropped from rooms but not yet switched off are only kept in the store
        stored = await store.async_load() or {}
        pending = [s for s in stored.get("release") or [] if isinstance(s, str)]
        await _async_switch_off_circuits(hass, entry, "removed", pending)
        async_delete_issues(hass)
        await store.async_remove()

    @callback
    def _remove_stale_entities(self) -> None:
        """Remove entities the configuration no longer provides (heat meter removed,
        circuit removed from a room); they would stay as "unavailable". Judged from the
        configuration, not from what was set up: an entity that failed to load keeps its
        registry entry and the user's settings."""
        coordinator = self.coordinator
        assert coordinator is not None
        stale = set()
        heat_meter = bool(coordinator.opt(CONF_HEAT_METER))
        if not heat_meter:
            stale.add(f"{self.entry.entry_id}_heat_today")
            stale.add(f"{self.entry.entry_id}_unassigned_heat")
        for area in coordinator.areas.values():
            if not heat_meter or not area.has_circuit:
                stale.update(f"{area.area_id}_{key}" for key in ROOM_HEAT_KEYS.values())
            if not area.has_circuit:
                stale.add(f"{area.area_id}_climate")
                stale.update(f"{area.area_id}_{d.key}" for d in AREA_SENSORS if d.circuit_only)
        registry = er.async_get(self.hass)
        for reg_entry in er.async_entries_for_config_entry(registry, self.entry.entry_id):
            if reg_entry.platform == DOMAIN and reg_entry.unique_id in stale:
                LOGGER.info("Removing %s: no longer provided", reg_entry.entity_id)
                registry.async_remove(reg_entry.entity_id)

    @callback
    def _place_room_devices(self) -> None:
        """A room device stays in the Home Assistant area chosen for the room."""
        coordinator = self.coordinator
        assert coordinator is not None
        devices = dr.async_get(self.hass)
        for area in coordinator.areas.values():
            area_id = area.cfg.get(CONF_AREA)
            device = devices.async_get_device_by_identifier(
                (DOMAIN, area.area_id), self.entry.entry_id
            )
            if area_id and device is not None and device.area_id != area_id:
                devices.async_update_device(device.id, area_id=area_id)

    def entities(self, platform: Platform) -> list[tuple[str | None, list[Entity]]]:
        coordinator = self.coordinator
        if coordinator is None:
            return []
        areas = list(coordinator.areas.values())
        if platform is Platform.BINARY_SENSOR:
            return [
                (None, [HeatingDaySensor(coordinator)]),
                *(
                    (area.area_id, [VentilationRecommended(coordinator, area.area_id)])
                    for area in areas
                ),
            ]
        if platform is Platform.CLIMATE:
            return [
                (area.area_id, [AreaClimate(coordinator, area.area_id)])
                for area in areas
                if area.has_circuit
            ]
        if platform is Platform.SELECT:
            return [(None, [HeatingDayOverride(coordinator)])]
        if platform is Platform.SENSOR:
            globals_: list[Entity] = [
                HeatingDayPhaseSensor(coordinator),
                AiTimestampSensor(coordinator, "ai_last_check", "last_check"),
                AiTimestampSensor(coordinator, "ai_next_check", "next_check"),
                AiTimestampSensor(coordinator, "ai_last_vent_check", "last_check", vent=True),
                AiTimestampSensor(coordinator, "ai_next_vent_check", "next_check", vent=True),
                AiCostSensor(coordinator),
            ]
            heat_meter = bool(coordinator.opt(CONF_HEAT_METER))
            if heat_meter:
                globals_.append(HeatTodaySensor(coordinator))
                globals_.append(UnassignedHeatSensor(coordinator))
            return [
                (None, globals_),
                *(
                    (
                        area.area_id,
                        [
                            AreaSensor(coordinator, area.area_id, description)
                            for description in AREA_SENSORS
                            if area.has_circuit or not description.circuit_only
                        ]
                        + (
                            [
                                RoomHeatSensor(coordinator, area.area_id, kind)
                                for kind in ROOM_HEAT_KEYS
                            ]
                            if heat_meter and area.has_circuit
                            else []
                        ),
                    )
                    for area in areas
                ),
            ]
        if platform is Platform.SWITCH:
            return [(None, [AiEnabledSwitch(coordinator)])]
        return []

    def diagnostics(self) -> dict[str, Any]:
        return self.coordinator.diagnostics() if self.coordinator else {}


async def _async_switch_off_circuits(
    hass: HomeAssistant, entry: ConfigEntry, reason: str, pending: list[str]
) -> None:
    """Switch off every circuit of the rooms that is on, and the dropped ones still owed
    a switch-off (a circuit left on would heat without limit once nothing controls it)."""
    switches = [
        sub.data[CONF_SWITCH]
        for sub in entry.subentries.values()
        if sub.subentry_type == SUBENTRY_ROOM and sub.data.get(CONF_SWITCH)
    ]
    switches += [s for s in pending if s not in switches]
    for entity_id in await async_turn_off_switches(hass, switches):
        LOGGER.info("Switched off %s: the heating was %s", entity_id, reason)
