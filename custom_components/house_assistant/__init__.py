"""House Assistant: heating, covers and meter reading on one model of the house."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from . import modules  # noqa: F401  (the modules register themselves)
from .const import DOMAIN, PLATFORMS
from .core.panel import async_register_panel, async_unregister_panel
from .core.websocket import async_register_websocket
from .meter.services import async_setup_services as async_setup_meter_services
from .runtime import MODULE_TYPES, HouseConfigEntry, HouseRuntime

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the services and the panel commands once."""
    async_setup_meter_services(hass)
    async_register_websocket(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> bool:
    """Start the enabled modules, then the platforms they add their entities to."""
    runtime = HouseRuntime(hass, entry)
    await runtime.async_start()
    entry.runtime_data = runtime
    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except Exception:
        # do not leave listeners and timers behind
        await runtime.async_shutdown()
        raise
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await async_register_panel(hass, entry.entry_id)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: HouseConfigEntry) -> None:
    """Options or subentries changed: only the modules concerned are restarted."""
    await entry.runtime_data.async_entry_updated()


async def async_unload_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_shutdown()
        async_unregister_panel(hass)
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> None:
    """Every module removes what it stored (and switches off what it controlled)."""
    async_unregister_panel(hass)
    for module in MODULE_TYPES.values():
        await module.async_remove_entry(hass, entry)
