"""Entities of the house: the vacation switch, departure, return and whether it is
vacation (switch or an external source)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.datetime import DateTimeEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import Platform
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util

from ..const import DOMAIN, NAME
from .links import leak_meters, preheat_start, vacation_simulation

if TYPE_CHECKING:
    from .vacation import HouseModule


def house_device_info(entry_id: str) -> DeviceInfo:
    """The device of the house as a whole."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=NAME,
        manufacturer=NAME,
        model="House",
        entry_type=DeviceEntryType.SERVICE,
    )


class HouseEntity(Entity):
    """Entity of the house; written on every change of the vacation."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, house: HouseModule, key: str) -> None:
        self.house = house
        entry_id = house.entry.entry_id
        self._attr_translation_key = key
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_device_info = house_device_info(entry_id)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.house.add_listener(self._changed))

    @callback
    def _changed(self) -> None:
        if self.hass is not None and self.platform is not None:
            self.async_write_ha_state()


class VacationSwitch(HouseEntity, SwitchEntity):
    """The own vacation of the house (kept across restarts)."""

    def __init__(self, house: HouseModule) -> None:
        super().__init__(house, "vacation")

    @property
    def is_on(self) -> bool:
        return self.house.times.on

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.house.set_on(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.house.set_on(False)


class VacationTime(HouseEntity, DateTimeEntity):
    """Departure or return of the own vacation (empty when none is planned)."""

    def __init__(self, house: HouseModule, key: str) -> None:
        super().__init__(house, key)
        self._departure = key == "vacation_departure"

    @property
    def native_value(self) -> datetime | None:
        times = self.house.times
        return times.departure if self._departure else times.return_at

    async def async_set_value(self, value: datetime) -> None:
        if self._departure:
            self.house.set_departure(value)
        else:
            self.house.set_return(value)


class VacationActive(HouseEntity, BinarySensorEntity):
    """On while it is vacation: the own switch or an external source."""

    # change with every window and every minute of the heating
    _unrecorded_attributes = frozenset(
        {"open_windows", "preheat_start", "simulation", "leak_warning"}
    )

    def __init__(self, house: HouseModule) -> None:
        super().__init__(house, "vacation_active")

    @property
    def is_on(self) -> bool:
        return self.house.active

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        house = self.house
        hass = house.hass
        times = house.times
        start = preheat_start(hass) if house.active else None
        return {
            "source": house.source,
            "since": house.since.isoformat() if house.since else None,
            "departure": _local(times.departure),
            "return": _local(house.own_return() or times.return_at) or house.external_return(),
            "preheat_start": _local(dt_util.utc_from_timestamp(start)) if start else None,
            "simulation": vacation_simulation(hass),
            "leak_warning": leak_meters(hass),
            "open_windows": house.open_windows(),
        }


def _local(value: datetime | None) -> str | None:
    return dt_util.as_local(value).isoformat() if value is not None else None


def vacation_entities(house: HouseModule, platform: Platform) -> list[Entity]:
    if platform is Platform.SWITCH:
        return [VacationSwitch(house)]
    if platform is Platform.DATETIME:
        return [
            VacationTime(house, "vacation_departure"),
            VacationTime(house, "vacation_return"),
        ]
    if platform is Platform.BINARY_SENSOR:
        return [VacationActive(house)]
    return []
