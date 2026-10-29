"""Settings of the house the modules share: outdoor values, weather, language,
notifications and the working days (see ``SHARED_KEYS``)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import probatio as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    BooleanSelector,
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..const import (
    CONF_DRAFT_REACH,
    CONF_HOUSE_AZIMUTH,
    CONF_HOUSE_DEPTH,
    CONF_HOUSE_WIDTH,
    CONF_LANGUAGE,
    CONF_NOTIFY,
    CONF_OUTDOOR_HUMIDITY,
    CONF_OUTDOOR_TEMP,
    CONF_RAIN_ENTITY,
    CONF_RETURN_ENTITY,
    CONF_VACATION_ENTITIES,
    CONF_VACATION_WINDOW_ALERT,
    CONF_WEATHER,
    CONF_WEEKEND_DAYS,
    CONF_WIND_ENTITY,
    CONF_WORKDAY,
    MODULE_HEATING,
    MODULE_SHUTTER,
)
from ..heating.const import CONF_VACATION_VENT_PAUSE
from ..shutter.const import CONF_VACATION_HEAT_PROTECTION
from .logic.geometry import DEFAULT_REACH
from .schema import entity, number, optional

# fields of the forms of the house (saving one replaces only its own fields)
HOUSE_FORM = (
    CONF_OUTDOOR_TEMP,
    CONF_OUTDOOR_HUMIDITY,
    CONF_WEATHER,
    CONF_WIND_ENTITY,
    CONF_RAIN_ENTITY,
    CONF_LANGUAGE,
    CONF_NOTIFY,
    CONF_WORKDAY,
    CONF_WEEKEND_DAYS,
    CONF_HOUSE_AZIMUTH,
    CONF_HOUSE_WIDTH,
    CONF_HOUSE_DEPTH,
    CONF_DRAFT_REACH,
)
VACATION_FORM = (CONF_VACATION_ENTITIES, CONF_RETURN_ENTITY, CONF_VACATION_WINDOW_ALERT)
# vacation options that belong to a module but are set only in the house: module, key, default
VACATION_OPTIONS = (
    (MODULE_HEATING, CONF_VACATION_VENT_PAUSE, True),
    (MODULE_SHUTTER, CONF_VACATION_HEAT_PROTECTION, True),
)

LANGUAGES = ["auto", "de", "en"]
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DEFAULT_WEEKEND = ["sat", "sun"]


def _sensor(device_class: str, units: list[str]) -> EntitySelector:
    """Sensor of one kind; also one without the device class but with a matching unit."""
    return EntitySelector(
        EntitySelectorConfig(
            domain="sensor",
            filter=[
                {"domain": "sensor", "device_class": device_class},
                {"domain": "sensor", "unit_of_measurement": units},
            ],
        )
    )


def notify_services(hass: HomeAssistant) -> list[str]:
    return sorted(f"notify.{name}" for name in hass.services.async_services_for_domain("notify"))


def house_schema(hass: HomeAssistant, v: dict[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            optional(CONF_OUTDOOR_TEMP, v): _sensor("temperature", ["°C", "°F", "K"]),
            optional(CONF_OUTDOOR_HUMIDITY, v): _sensor("humidity", ["%"]),
            optional(CONF_WEATHER, v): entity(["weather"]),
            optional(CONF_WIND_ENTITY, v): entity(["sensor"]),
            optional(CONF_RAIN_ENTITY, v): entity(["binary_sensor", "sensor", "input_boolean"]),
            vol.Required(CONF_LANGUAGE, default=v.get(CONF_LANGUAGE, "auto")): SelectSelector(
                SelectSelectorConfig(
                    options=LANGUAGES, translation_key="language", mode=SelectSelectorMode.LIST
                )
            ),
            vol.Optional(CONF_NOTIFY, default=v.get(CONF_NOTIFY, [])): SelectSelector(
                SelectSelectorConfig(
                    options=notify_services(hass),
                    multiple=True,
                    custom_value=True,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
            optional(CONF_WORKDAY, v): entity(["binary_sensor"]),
            vol.Optional(
                CONF_WEEKEND_DAYS, default=v.get(CONF_WEEKEND_DAYS, DEFAULT_WEEKEND)
            ): SelectSelector(
                SelectSelectorConfig(
                    options=WEEKDAYS,
                    translation_key="weekday",
                    multiple=True,
                    mode=SelectSelectorMode.LIST,
                )
            ),
            # the house plan: compass of the covers and draft through the rooms
            optional(CONF_HOUSE_AZIMUTH, v): number(0, 360, 1, "°"),
            optional(CONF_HOUSE_WIDTH, v): number(1, 500, 0.1, "m"),
            optional(CONF_HOUSE_DEPTH, v): number(1, 500, 0.1, "m"),
            vol.Required(CONF_DRAFT_REACH, default=v.get(CONF_DRAFT_REACH, DEFAULT_REACH)): number(
                0, 20, 0.5, "m"
            ),
        }
    )


def vacation_schema(
    v: dict[str, Any],
    modules: Iterable[str] = (),
    module_values: dict[str, dict[str, Any]] | None = None,
) -> vol.Schema:
    """External sources of the vacation of the house and its reports, plus the vacation
    options of the given modules (Settings > House > Vacation; the panel tab saves the
    module options on its own)."""
    module_values = module_values or {}
    options: dict[Any, Any] = {
        vol.Required(key, default=module_values.get(module, {}).get(key, default)): (
            BooleanSelector()
        )
        for module, key, default in VACATION_OPTIONS
        if module in modules
    }
    return vol.Schema(
        {
            vol.Optional(
                CONF_VACATION_ENTITIES, default=v.get(CONF_VACATION_ENTITIES, [])
            ): EntitySelector(
                EntitySelectorConfig(
                    domain=["input_boolean", "binary_sensor", "switch", "calendar", "schedule"],
                    multiple=True,
                )
            ),
            optional(CONF_RETURN_ENTITY, v): EntitySelector(
                EntitySelectorConfig(
                    filter=[
                        {"domain": ["input_datetime", "datetime"]},
                        {"domain": "sensor", "device_class": "timestamp"},
                    ]
                )
            ),
            vol.Required(
                CONF_VACATION_WINDOW_ALERT, default=v.get(CONF_VACATION_WINDOW_ALERT, True)
            ): BooleanSelector(),
            **options,
        }
    )


def _not_numeric(hass: HomeAssistant, entity_id: str | None) -> bool:
    """The entity reports a value that is not a number (unavailable is fine)."""
    state = hass.states.get(entity_id) if entity_id else None
    if state is None or state.state in ("unavailable", "unknown"):
        return False
    try:
        float(state.state)
    except ValueError:
        return True
    return False


def validate_house(
    hass: HomeAssistant,
    data: dict[str, Any],
    modules: list[str],
) -> dict[str, str]:
    """Validate the shared outdoor source and notification services of the house."""
    errors: dict[str, str] = {}
    needed = [key for key in (MODULE_HEATING, MODULE_SHUTTER) if key in modules]
    house = bool(data.get(CONF_OUTDOOR_TEMP) or data.get(CONF_WEATHER))
    if needed and not house:
        errors[CONF_OUTDOOR_TEMP] = "need_temperature_source"
    elif _not_numeric(hass, data.get(CONF_OUTDOOR_TEMP)):
        errors[CONF_OUTDOOR_TEMP] = "not_numeric"
    services = data.get(CONF_NOTIFY) or []
    if any(not str(s).startswith("notify.") or str(s) == "notify." for s in services):
        errors[CONF_NOTIFY] = "invalid_notify_service"
    return errors
