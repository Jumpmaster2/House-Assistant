"""Finding the config entry and the running modules (for services and the panel)."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant

from ..const import DOMAIN
from ..runtime import HouseRuntime, Module


def house_entry(hass: HomeAssistant) -> ConfigEntry | None:
    """The entry of the integration, the loaded one if there is one."""
    entries = hass.config_entries.async_entries(DOMAIN)
    for entry in entries:
        if entry.state is ConfigEntryState.LOADED:
            return entry
    return entries[0] if entries else None


def running_module(hass: HomeAssistant, key: str) -> Module | None:
    """A module of the loaded entry, None while it is not running."""
    for entry in hass.config_entries.async_loaded_entries(DOMAIN):
        runtime = getattr(entry, "runtime_data", None)
        if isinstance(runtime, HouseRuntime):
            return runtime.module(key)
    return None


def update_section(
    hass: HomeAssistant, entry: ConfigEntry, key: str, values: dict[str, Any]
) -> None:
    """Replace the options of one section; the other sections stay as they are."""
    hass.config_entries.async_update_entry(entry, options={**entry.options, key: values})
