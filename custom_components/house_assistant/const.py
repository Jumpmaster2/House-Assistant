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
    Platform.DATETIME,
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

# Shared settings belong exclusively to the house (core section).
CONF_OUTDOOR_TEMP: Final = "outdoor_temperature"
CONF_OUTDOOR_HUMIDITY: Final = "outdoor_humidity"
CONF_WEATHER: Final = "weather"
CONF_WIND_ENTITY: Final = "wind_entity"
CONF_RAIN_ENTITY: Final = "rain_entity"
CONF_LANGUAGE: Final = "language"
CONF_NOTIFY: Final = "notify_services"
CONF_WORKDAY: Final = "workday_entity"
CONF_WEEKEND_DAYS: Final = "weekend_days"
# the house plan: direction of the front, length of front and back, depth, and how far
# from the line between two open windows a room still feels their draft (m)
CONF_HOUSE_AZIMUTH: Final = "house_azimuth"
CONF_HOUSE_WIDTH: Final = "house_width"
CONF_HOUSE_DEPTH: Final = "house_depth"
CONF_DRAFT_REACH: Final = "draft_reach"
# external sources of the vacation (on = vacation) and of the return; besides the own
# switch of the house with departure and return
CONF_VACATION_ENTITIES: Final = "vacation_entities"
CONF_RETURN_ENTITY: Final = "return_entity"
SHARED_KEYS: Final = (
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
    CONF_VACATION_ENTITIES,
    CONF_RETURN_ENTITY,
)
# vacation: report open windows at the departure and windows opened during it
CONF_VACATION_WINDOW_ALERT: Final = "vacation_window_alert"

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
# vacation of the house started or ended (active, source); a meter warns on vacation
EVENT_VACATION: Final = f"{DOMAIN}_vacation"
EVENT_VACATION_ALERT: Final = f"{DOMAIN}_vacation_alert"
# the vacation changed (switch, times, an external source): the modules look again
SIGNAL_VACATION: Final = f"{DOMAIN}_vacation_changed"

STORAGE_VERSION: Final = 1
