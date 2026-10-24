"""Climate platform: the modules add their entities here."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .runtime import HouseConfigEntry

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HouseConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    entry.runtime_data.platform_ready(Platform.CLIMATE, async_add_entities)
