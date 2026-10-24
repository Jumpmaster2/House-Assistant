"""Settings of the house the modules share: outdoor values, weather, language,
notifications and the working days (see ``SHARED_KEYS``)."""

from __future__ import annotations

from typing import Any

import probatio as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..const import (
    CONF_LANGUAGE,
    CONF_NOTIFY,
    CONF_OUTDOOR_HUMIDITY,
    CONF_OUTDOOR_TEMP,
    CONF_WEATHER,
    CONF_WEEKEND_DAYS,
    CONF_WORKDAY,
    MODULE_HEATING,
    MODULE_SHUTTER,
)
from .schema import entity, optional

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
    module_values: list[dict[str, Any]] = (),
) -> dict[str, str]:
    """Heating and covers need an outdoor temperature: a sensor or a weather entity, of the
    house or (without one there) of each module. A numeric sensor, only notification
    services."""
    errors: dict[str, str] = {}
    needed = [key for key in (MODULE_HEATING, MODULE_SHUTTER) if key in modules]
    house = bool(data.get(CONF_OUTDOOR_TEMP) or data.get(CONF_WEATHER))
    own = all(v.get(CONF_OUTDOOR_TEMP) or v.get(CONF_WEATHER) for v in module_values)
    if needed and not house and not (module_values and own):
        errors[CONF_OUTDOOR_TEMP] = "need_temperature_source"
    elif _not_numeric(hass, data.get(CONF_OUTDOOR_TEMP)):
        errors[CONF_OUTDOOR_TEMP] = "not_numeric"
    services = data.get(CONF_NOTIFY) or []
    if any(not str(s).startswith("notify.") or str(s) == "notify." for s in services):
        errors[CONF_NOTIFY] = "invalid_notify_service"
    return errors
