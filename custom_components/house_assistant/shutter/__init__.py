"""Cover module: sun protection, evening, ventilation, weather protection, override,
morning opening and vacation for covers (formerly Shutter Assistant)."""

from __future__ import annotations

from typing import Any

from homeassistant.const import Platform
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import Entity

from ..runtime import Module, register_module
from .binary_sensor import (
    EveningClosed,
    EveningMode,
    Override,
    SummerDay,
    SunCondition,
    SunProtectionToday,
    WeatherProtection,
)
from .const import MODULE_SHUTTER, SUBENTRY_GROUP, SUBENTRY_WINDOW
from .engine import ShutterEngine
from .entity import global_device_info
from .logic.protection import KINDS
from .sensor import ForecastMax, LastReason, NextAction, Status
from .switch import AutomaticSwitch, WindowSwitch


@register_module
class ShutterModule(Module):
    """All covers with their windows and the groups (directions of the sun)."""

    key = MODULE_SHUTTER
    subentry_types = (SUBENTRY_GROUP, SUBENTRY_WINDOW)

    engine: ShutterEngine | None = None

    async def async_setup(self) -> None:
        engine = ShutterEngine(self)
        # Create the device of the module first so window devices can point to it by id.
        device = dr.async_get(self.hass).async_get_or_create(
            config_entry_id=self.entry.entry_id, **global_device_info(self.entry.entry_id)
        )
        engine.global_device_id = device.id
        await engine.async_setup()
        self.engine = engine

    async def async_unload(self) -> None:
        if self.engine is not None:
            await self.engine.async_shutdown()

    def entities(self, platform: Platform) -> list[tuple[str | None, list[Entity]]]:
        engine = self.engine
        if engine is None:
            return []
        windows = list(engine.windows)
        if platform is Platform.BINARY_SENSOR:
            return [
                (
                    None,
                    [
                        SummerDay(engine),
                        EveningMode(engine),
                        *(
                            WeatherProtection(engine, kind)
                            for kind in KINDS
                            if engine.protection_enabled(kind)
                        ),
                    ],
                ),
                *(
                    (
                        wid,
                        [
                            Override(engine, wid),
                            SunCondition(engine, wid),
                            SunProtectionToday(engine, wid),
                            EveningClosed(engine, wid),
                        ],
                    )
                    for wid in windows
                ),
            ]
        if platform is Platform.SENSOR:
            return [
                (None, [ForecastMax(engine)]),
                *(
                    (
                        wid,
                        [Status(engine, wid), LastReason(engine, wid), NextAction(engine, wid)],
                    )
                    for wid in windows
                ),
            ]
        if platform is Platform.SWITCH:
            return [
                (None, [AutomaticSwitch(engine)]),
                *(
                    (
                        wid,
                        [
                            WindowSwitch(engine, wid, "window_automatic", "automatic"),
                            WindowSwitch(engine, wid, "window_sun_protection", "sun_enabled"),
                        ],
                    )
                    for wid in windows
                ),
            ]
        return []

    def diagnostics(self) -> dict[str, Any]:
        return self.engine.diagnostics() if self.engine else {}
