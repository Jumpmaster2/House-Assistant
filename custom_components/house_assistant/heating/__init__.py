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

from ..core.store import module_store
from ..runtime import Module, register_module
from .binary_sensor import HeatingDaySensor, VentilationRecommended
from .climate import AreaClimate
from .const import CONF_HEAT_METER, CONF_SWITCH, DOMAIN, LOGGER, MODULE_HEATING, SUBENTRY_ROOM
from .coordinator import HeatingCoordinator, async_delete_issues, async_turn_off_switches
from .entity import global_device_info
from .select import HeatingDayOverride
from .sensor import (
    AREA_SENSORS,
    AiCostSensor,
    AiTimestampSensor,
    AreaSensor,
    HeatingDayPhaseSensor,
    HeatTodaySensor,
)
from .switch import AiEnabledSwitch


@register_module
class HeatingModule(Module):
    """The rooms with their heating circuits, the heating day and the AI."""

    key = MODULE_HEATING
    subentry_types = (SUBENTRY_ROOM,)

    coordinator: HeatingCoordinator | None = None

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

    async def async_unload(self) -> None:
        coordinator = self.coordinator
        if coordinator is None:
            return
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
        if not coordinator.opt(CONF_HEAT_METER):
            stale.add(f"{self.entry.entry_id}_heat_today")
        for area in coordinator.areas.values():
            if not area.has_circuit:
                stale.add(f"{area.area_id}_climate")
                stale.update(f"{area.area_id}_{d.key}" for d in AREA_SENSORS if d.circuit_only)
        registry = er.async_get(self.hass)
        for reg_entry in er.async_entries_for_config_entry(registry, self.entry.entry_id):
            if reg_entry.platform == DOMAIN and reg_entry.unique_id in stale:
                LOGGER.info("Removing %s: no longer provided", reg_entry.entity_id)
                registry.async_remove(reg_entry.entity_id)

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
            if coordinator.opt(CONF_HEAT_METER):
                globals_.append(HeatTodaySensor(coordinator))
            return [
                (None, globals_),
                *(
                    (
                        area.area_id,
                        [
                            AreaSensor(coordinator, area.area_id, description)
                            for description in AREA_SENSORS
                            if area.has_circuit or not description.circuit_only
                        ],
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
