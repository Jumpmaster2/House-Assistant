"""Switch for the automatic readings of a meter."""

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity

from .entity import MeterEntity
from .meter import Meter


class AutomaticSwitch(MeterEntity, SwitchEntity):
    _attr_icon = "mdi:timer-cog-outline"

    def __init__(self, meter: Meter) -> None:
        super().__init__(meter, "automatic", "meter_automatic")

    @property
    def is_on(self) -> bool:
        return self.meter.state.automatic

    async def async_turn_on(self, **kwargs: Any) -> None:
        self.meter.set_automatic(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        self.meter.set_automatic(False)
