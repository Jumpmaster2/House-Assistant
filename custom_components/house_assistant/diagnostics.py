"""Diagnostics: the settings and the stored state of every running module."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from .runtime import HouseConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: HouseConfigEntry
) -> dict[str, Any]:
    runtime = entry.runtime_data
    return {
        "entry": entry.as_dict(),
        "modules": {key: module.diagnostics() for key, module in runtime.modules.items()},
    }
