"""Stored state: one store per module and entry."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from ..const import DOMAIN, STORAGE_VERSION


def store_key(entry_id: str, module: str) -> str:
    """``.storage/house_assistant.<entry_id>.<module>``"""
    return f"{DOMAIN}.{entry_id}.{module}"


def module_store(hass: HomeAssistant, entry: ConfigEntry, module: str) -> Store[dict[str, Any]]:
    return Store(hass, STORAGE_VERSION, store_key(entry.entry_id, module))
