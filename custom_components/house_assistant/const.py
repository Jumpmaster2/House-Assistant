"""Constants for House Assistant."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "house_assistant"
NAME: Final = "House Assistant"
LOGGER = logging.getLogger(__package__)

# Every platform is set up once; the modules add and remove their entities there.
PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CAMERA,
    Platform.CLIMATE,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

# Options are kept per section: the house (core) and one section per module, with the
# keys of the former integrations unchanged inside.
OPT_CORE: Final = "core"
CONF_MODULES: Final = "modules"
# Show the panel in the sidebar (it stays reachable from the integration page).
CONF_SHOW_PANEL: Final = "show_panel"

# Settings of the house the modules share, kept in the core section. A value set there
# applies to every module; without one the value of a module applies (the former
# integrations had them each, possibly different).
CONF_OUTDOOR_TEMP: Final = "outdoor_temperature"
CONF_OUTDOOR_HUMIDITY: Final = "outdoor_humidity"
CONF_WEATHER: Final = "weather"
CONF_LANGUAGE: Final = "language"
CONF_NOTIFY: Final = "notify_services"
CONF_WORKDAY: Final = "workday_entity"
CONF_WEEKEND_DAYS: Final = "weekend_days"
SHARED_KEYS: Final = (
    CONF_OUTDOOR_TEMP,
    CONF_OUTDOOR_HUMIDITY,
    CONF_WEATHER,
    CONF_LANGUAGE,
    CONF_NOTIFY,
    CONF_WORKDAY,
    CONF_WEEKEND_DAYS,
)

MODULE_HEATING: Final = "heating"
MODULE_SHUTTER: Final = "shutter"
MODULE_METER: Final = "meter"
# order of the modules in dialogs and in the panel
MODULE_ORDER: Final = (MODULE_HEATING, MODULE_SHUTTER, MODULE_METER)

SUBENTRY_ROOM: Final = "room"
SUBENTRY_GROUP: Final = "group"
SUBENTRY_WINDOW: Final = "window"
SUBENTRY_METER: Final = "meter"

# One logbook event for every module (name, message and entity of the entry).
EVENT_LOGBOOK: Final = f"{DOMAIN}_logbook"

STORAGE_VERSION: Final = 1
