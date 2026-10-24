"""Diagnostics: the settings and the stored state of every running module."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .runtime import HouseConfigEntry

# Notification services often contain the name of a person or phone.
TO_REDACT = {"notify_services"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: HouseConfigEntry
) -> dict[str, Any]:
    runtime = entry.runtime_data
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "modules": {key: module.diagnostics() for key, module in runtime.modules.items()},
    }
