"""House Assistant: heating, covers and meter reading on one model of the house."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.typing import ConfigType

from . import modules  # noqa: F401  (the modules register themselves)
from .const import (
    CONF_LANGUAGE,
    CONF_SHOW_PANEL,
    CONF_VACATION_ENTITIES,
    DOMAIN,
    LOGGER,
    MODULE_ORDER,
    OPT_CORE,
    PLATFORMS,
    SHARED_KEYS,
)
from .core.panel import (
    async_register_frontend,
    async_register_panel,
    async_unregister_cards,
    async_unregister_panel,
)
from .core.services import async_setup_services as async_setup_house_services
from .core.websocket import async_register_websocket
from .heating.services import async_setup_services as async_setup_heating_services
from .meter.services import async_setup_services as async_setup_meter_services
from .runtime import HOUSE_TYPE, MODULE_TYPES, HouseConfigEntry, HouseRuntime, module_options
from .shutter.services import async_register_services as async_setup_shutter_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the services, the panel commands and the cards once. The cards first:
    a dashboard may already be open (the frontend starts before the integrations)."""
    await async_register_frontend(hass)
    async_setup_house_services(hass)
    async_setup_heating_services(hass)
    async_setup_meter_services(hass)
    async_setup_shutter_services(hass)
    async_register_websocket(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> bool:
    """Start the enabled modules, then the platforms they add their entities to."""
    _move_vacation_sources(hass, entry)
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
    await async_register_panel(hass, entry.entry_id, _sidebar(entry))
    return True


def _move_vacation_sources(hass: HomeAssistant, entry: HouseConfigEntry) -> None:
    """Move legacy shared settings to the house once, without overriding house values."""
    options = dict(entry.options)
    core = dict(options.get(OPT_CORE) or {})
    original_house = dict(core)
    selected: dict[str, tuple[str, object]] = {}
    for module in MODULE_ORDER:
        if module not in options:
            continue
        section = dict(options.get(module) or {})
        for key in SHARED_KEYS:
            if key not in section:
                continue
            value = section.pop(key)
            if value in (None, "", []) or (key == CONF_LANGUAGE and value == "auto"):
                continue
            if key == CONF_VACATION_ENTITIES:
                known = list(core.get(key) or [])
                core[key] = known + [e for e in value if e not in known]
            elif original_house.get(key) in (None, "", []) or (
                key == CONF_LANGUAGE and original_house.get(key) == "auto"
            ):
                if key not in selected:
                    selected[key] = (module, value)
                    core[key] = value
                elif selected[key][1] != value:
                    LOGGER.warning(
                        "Conflicting shared setting %s in modules %s and %s",
                        key,
                        selected[key][0],
                        module,
                    )
        options[module] = section
    for key in ("vacation_ventilation_pause", "vacation_heat_protection"):
        core.pop(key, None)
    if core or OPT_CORE in options:
        options[OPT_CORE] = core
    if options != dict(entry.options):
        hass.config_entries.async_update_entry(entry, options=options)


def _sidebar(entry: HouseConfigEntry) -> bool:
    return bool(module_options(entry, OPT_CORE).get(CONF_SHOW_PANEL, True))


async def _async_update_listener(hass: HomeAssistant, entry: HouseConfigEntry) -> None:
    """Options or subentries changed: only the modules concerned are restarted."""
    await entry.runtime_data.async_entry_updated()
    await async_register_panel(hass, entry.entry_id, _sidebar(entry))


async def async_unload_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.async_shutdown()
        async_unregister_panel(hass)
    return unloaded


async def async_remove_entry(hass: HomeAssistant, entry: HouseConfigEntry) -> None:
    """Every module removes what it stored (and switches off what it controlled)."""
    async_unregister_panel(hass)
    await async_unregister_cards(hass)
    for domain, issue_id in list(ir.async_get(hass).issues):
        if domain == DOMAIN:
            ir.async_delete_issue(hass, DOMAIN, issue_id)
    for module in [*HOUSE_TYPE, *MODULE_TYPES.values()]:
        await module.async_remove_entry(hass, entry)
