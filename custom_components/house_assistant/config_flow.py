"""Config flow: one entry for the whole house, the settings of every module as options."""

from __future__ import annotations

from typing import Any

import probatio as vol
from homeassistant.config_entries import (
    SOURCE_USER,
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    ConfigSubentryFlow,
    FlowType,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_MODULES,
    CONF_SHOW_PANEL,
    CONF_WEATHER,
    DOMAIN,
    MODULE_HEATING,
    MODULE_METER,
    MODULE_ORDER,
    MODULE_SHUTTER,
    NAME,
    OPT_CORE,
    SHARED_KEYS,
    SUBENTRY_GROUP,
    SUBENTRY_METER,
    SUBENTRY_ROOM,
    SUBENTRY_WINDOW,
)
from .core.settings import house_schema, validate_house
from .heating.config_flow import HeatingOptionsSteps, HeatingSetupSteps, RoomSubentryFlow
from .meter.config_flow import MeterSubentryFlow
from .meter.config_flow import options_schema as meter_schema
from .meter.const import DEFAULTS as METER_DEFAULTS
from .runtime import enabled_modules, module_options
from .shutter.config_flow import (
    GroupSubentryFlow,
    ShutterOptionsSteps,
    ShutterSetupSteps,
    WindowSubentryFlow,
)

# setup and options step of the settings of the house
STEP_HOUSE = "house"
# modules whose settings are one form: the form and the defaults of its options
MODULE_FORMS = {MODULE_METER: (meter_schema, METER_DEFAULTS)}
# modules with setup steps (heating and covers have several)
SETUP_MODULES = (MODULE_HEATING, MODULE_SHUTTER, MODULE_METER)
# subentry types of the house (every module builds on them) and of every module
HOUSE_SUBENTRIES: dict[str, type[ConfigSubentryFlow]] = {
    SUBENTRY_ROOM: RoomSubentryFlow,
    SUBENTRY_WINDOW: WindowSubentryFlow,
}
MODULE_SUBENTRIES: dict[str, dict[str, type[ConfigSubentryFlow]]] = {
    MODULE_SHUTTER: {SUBENTRY_GROUP: GroupSubentryFlow},
    MODULE_METER: {SUBENTRY_METER: MeterSubentryFlow},
}


def _clean(data: dict[str, Any]) -> dict[str, Any]:
    """Drop cleared optional values."""
    return {k: v for k, v in data.items() if v not in (None, "")}


def _single_entity(hass: Any, domain: str) -> str | None:
    """The entity of a domain if there is exactly one (suggestion for the setup)."""
    ids = hass.states.async_entity_ids(domain)
    return ids[0] if len(ids) == 1 else None


def modules_schema(chosen: list[str], show_panel: bool | None = None) -> vol.Schema:
    fields: dict[Any, Any] = {
        vol.Required(CONF_MODULES, default=chosen): SelectSelector(
            SelectSelectorConfig(
                options=list(MODULE_ORDER),
                multiple=True,
                translation_key=CONF_MODULES,
                mode=SelectSelectorMode.LIST,
            )
        )
    }
    if show_panel is not None:
        fields[vol.Required(CONF_SHOW_PANEL, default=show_panel)] = BooleanSelector()
    return vol.Schema(fields)


class HouseAssistantConfigFlow(HeatingSetupSteps, ShutterSetupSteps, ConfigFlow, domain=DOMAIN):
    """Create the single entry: choose the modules, then their first settings. The data
    holds the API key of the AI (empty without)."""

    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        self._options: dict[str, Any] = {}
        self._data: dict[str, Any] = {}
        self._pending: list[str] = []

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return HouseAssistantOptionsFlow()

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        types: dict[str, type[ConfigSubentryFlow]] = dict(HOUSE_SUBENTRIES)
        for key in enabled_modules(config_entry):
            types.update(MODULE_SUBENTRIES.get(key, {}))
        return types

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            chosen = [key for key in MODULE_ORDER if key in user_input[CONF_MODULES]]
            self._options = {OPT_CORE: {CONF_MODULES: chosen}}
            # the settings of the house first, the modules build on them
            self._pending = [key for key in chosen if key in SETUP_MODULES]
            if chosen:
                self._pending.insert(0, STEP_HOUSE)
            return await self._async_next()
        return self.async_show_form(step_id="user", data_schema=modules_schema(list(MODULE_ORDER)))

    async def _async_next(self) -> ConfigFlowResult:
        """The setup steps of the next chosen module, at the end the entry."""
        if self._pending:
            return await getattr(self, f"async_step_{self._pending.pop(0)}")()
        return self.async_create_entry(title=NAME, data=self._data, options=self._options)

    async def async_on_create_entry(self, result: ConfigFlowResult) -> ConfigFlowResult:
        """With the heating, directly continue with the first room."""
        entry = result.get("result")
        if entry is None or MODULE_HEATING not in self._options[OPT_CORE][CONF_MODULES]:
            return result
        sub = await self.hass.config_entries.subentries.async_init(
            (entry.entry_id, SUBENTRY_ROOM), context={"source": SOURCE_USER}
        )
        result["next_flow"] = (FlowType.CONFIG_SUBENTRIES_FLOW, sub["flow_id"])
        return result

    async def async_step_house(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Outdoor values, weather, language, notifications and working days for every
        module."""
        core = self._options[OPT_CORE]
        errors: dict[str, str] = {}
        if user_input is not None:
            errors = validate_house(self.hass, user_input, core[CONF_MODULES])
            if not errors:
                core.update(_clean(user_input))
                return await self._async_next()
        # suggest the only weather entity
        values = user_input or {CONF_WEATHER: _single_entity(self.hass, "weather")}
        return self.async_show_form(
            step_id=STEP_HOUSE, data_schema=house_schema(self.hass, values), errors=errors
        )

    async def async_step_meter(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        schema, defaults = MODULE_FORMS[MODULE_METER]
        if user_input is not None:
            self._options[MODULE_METER] = {**defaults, **user_input}
            return await self._async_next()
        return self.async_show_form(step_id=MODULE_METER, data_schema=schema(dict(defaults)))


class HouseAssistantOptionsFlow(HeatingOptionsSteps, ShutterOptionsSteps, OptionsFlow):
    """The modules and the settings of each module (the panel offers the same)."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        options = [CONF_MODULES, STEP_HOUSE] + [
            k for k in enabled_modules(self.config_entry) if k in SETUP_MODULES
        ]
        return self.async_show_menu(step_id="init", menu_options=options)

    async def async_step_house(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Settings of the house; a value set here applies to every module."""
        entry = self.config_entry
        core = module_options(entry, OPT_CORE)
        errors: dict[str, str] = {}
        if user_input is not None:
            modules = enabled_modules(entry)
            own = [module_options(entry, key) for key in (MODULE_HEATING, MODULE_SHUTTER)]
            errors = validate_house(self.hass, user_input, modules, [v for v in own if v])
            if not errors:
                core = {k: v for k, v in core.items() if k not in SHARED_KEYS}
                return self.async_create_entry(
                    data={**entry.options, OPT_CORE: {**core, **_clean(user_input)}}
                )
        return self.async_show_form(
            step_id=STEP_HOUSE,
            data_schema=house_schema(self.hass, user_input or core),
            errors=errors,
        )

    async def async_step_modules(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        core = module_options(self.config_entry, OPT_CORE)
        if user_input is not None:
            core[CONF_MODULES] = [key for key in MODULE_ORDER if key in user_input[CONF_MODULES]]
            core[CONF_SHOW_PANEL] = bool(user_input.get(CONF_SHOW_PANEL, True))
            return self.async_create_entry(data={**self.config_entry.options, OPT_CORE: core})
        return self.async_show_form(
            step_id="modules",
            data_schema=modules_schema(
                core.get(CONF_MODULES) or [], bool(core.get(CONF_SHOW_PANEL, True))
            ),
        )

    async def async_step_meter(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        schema, defaults = MODULE_FORMS[MODULE_METER]
        current = module_options(self.config_entry, MODULE_METER)
        if user_input is not None:
            return self.async_create_entry(
                data={**self.config_entry.options, MODULE_METER: {**current, **user_input}}
            )
        return self.async_show_form(
            step_id=MODULE_METER, data_schema=schema({**defaults, **current})
        )
