"""Meter module: read meters with a camera and an AI task (formerly Zähler-Ablesung)."""

from __future__ import annotations

from typing import Any

from homeassistant.const import Platform
from homeassistant.helpers.entity import Entity

from ..runtime import Module, register_module
from .button import PictureButton, ReadButton
from .camera import LastImageCamera
from .const import MODULE_METER, SUBENTRY_METER
from .meter import Meter, MeterManager
from .sensor import LastCheckSensor, NextCheckSensor, RateSensor, ReadingSensor, StatusSensor
from .switch import AutomaticSwitch

ENTITIES: dict[Platform, tuple[type[Entity], ...]] = {
    Platform.SENSOR: (ReadingSensor, RateSensor, StatusSensor, LastCheckSensor, NextCheckSensor),
    Platform.CAMERA: (LastImageCamera,),
    Platform.BUTTON: (ReadButton, PictureButton),
    Platform.SWITCH: (AutomaticSwitch,),
}


@register_module
class MeterModule(Module):
    """All meters with their cameras."""

    key = MODULE_METER
    subentry_types = (SUBENTRY_METER,)

    manager: MeterManager | None = None

    @property
    def meters(self) -> dict[str, Meter]:
        return self.manager.meters if self.manager else {}

    async def async_setup(self) -> None:
        self.manager = MeterManager(self)
        await self.manager.async_setup()

    async def async_unload(self) -> None:
        if self.manager is None:
            return
        await self.manager.async_unload()
        # the pictures of a deleted meter go with it
        for meter_id in self.manager.meters:
            if meter_id not in self.entry.subentries:
                await self.manager.async_remove_meter_files(meter_id)

    def entities(self, platform: Platform) -> list[tuple[str | None, list[Entity]]]:
        kinds = ENTITIES.get(platform, ())
        return [(meter.id, [kind(meter) for kind in kinds]) for meter in self.meters.values()]

    def diagnostics(self) -> dict[str, Any]:
        return {
            meter.id: {
                "title": meter.title,
                "config": meter.config,
                "state": meter.state.as_dict(),
                "busy": meter.busy,
                "has_image": meter.image is not None,
            }
            for meter in self.meters.values()
        }
