"""The house: rooms and windows, entered once and used by every module.

A room is a subentry ``room`` (formerly a heating area, the id stays). A window is a
subentry ``window`` with its room, its size, its contacts and optionally a cover
(formerly a window of Shutter Assistant, the id stays). The heating takes the
contacts of the windows of a room, the covers take the temperature and the air
conditioner of the room of their window.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Final

from homeassistant.config_entries import ConfigEntry, ConfigSubentry

from ..const import SUBENTRY_ROOM, SUBENTRY_WINDOW

CONF_NAME: Final = "name"
# room: Home Assistant area (the room device is placed there, it gives the floor)
CONF_AREA: Final = "area"
CONF_TEMP_SENSOR: Final = "temperature_sensor"
CONF_HUMIDITY_SENSOR: Final = "humidity_sensor"
# room: air conditioner, the default of the windows of the room for the covers
CONF_COOLING_ENTITY: Final = "cooling_entity"
# window: room, size, contacts and cover
CONF_ROOM: Final = "room"
CONF_SIZE: Final = "size"
CONF_WINDOW_SENSORS: Final = "window_sensors"
CONF_TILT_SENSORS: Final = "tilt_sensors"
CONF_COVER: Final = "cover"

# Sizes of a window; for the heating they stand for a relative opening area
# (see heating.logic.windows).
SIZES: Final = ("small", "medium", "large", "door")
DEFAULT_SIZE: Final = "medium"


def subentries(entry: ConfigEntry, subentry_type: str) -> dict[str, ConfigSubentry]:
    return {
        sub_id: sub
        for sub_id, sub in entry.subentries.items()
        if sub.subentry_type == subentry_type
    }


def rooms(entry: ConfigEntry) -> dict[str, ConfigSubentry]:
    return subentries(entry, SUBENTRY_ROOM)


def windows(entry: ConfigEntry) -> dict[str, ConfigSubentry]:
    return subentries(entry, SUBENTRY_WINDOW)


def window_size(data: Mapping[str, Any]) -> str:
    size = data.get(CONF_SIZE)
    return size if size in SIZES else DEFAULT_SIZE


def contacts(data: Mapping[str, Any]) -> list[str]:
    """Window contacts and tilt contacts of a window."""
    found: list[str] = []
    for key in (CONF_WINDOW_SENSORS, CONF_TILT_SENSORS):
        for entity_id in data.get(key) or ():
            if entity_id and entity_id not in found:
                found.append(str(entity_id))
    return found


def windows_of_room(entry: ConfigEntry, room_id: str) -> dict[str, ConfigSubentry]:
    return {
        sub_id: sub for sub_id, sub in windows(entry).items() if sub.data.get(CONF_ROOM) == room_id
    }


def room_contacts(entry: ConfigEntry, room_id: str) -> dict[str, list[str]]:
    """Window contacts of the windows of a room, by the size of their window."""
    found: dict[str, list[str]] = {size: [] for size in SIZES}
    for sub in windows_of_room(entry, room_id).values():
        for entity_id in sub.data.get(CONF_WINDOW_SENSORS) or ():
            found[window_size(sub.data)].append(str(entity_id))
    return found


def contact_in_use(
    entry: ConfigEntry, entity_ids: Iterable[str], own_id: str | None
) -> tuple[str, str] | None:
    """A contact that already belongs to another window, with the title of that window.
    A contact belongs to one window only: two windows would count one opening twice."""
    wanted = set(entity_ids)
    for sub_id, sub in windows(entry).items():
        if sub_id == own_id:
            continue
        for entity_id in contacts(sub.data):
            if entity_id in wanted:
                return entity_id, sub.title
    return None


def cover_in_use(entry: ConfigEntry, cover: Any, own_id: str | None) -> str | None:
    """Title of another window that already controls ``cover``."""
    if not cover:
        return None
    for sub_id, sub in windows(entry).items():
        if sub_id != own_id and sub.data.get(CONF_COVER) == cover:
            return sub.title
    return None


def window_errors(
    entry: ConfigEntry, data: Mapping[str, Any], own_id: str | None
) -> dict[str, str]:
    """Errors of the basics of a window (name, contacts, cover and room), one per field."""
    errors: dict[str, str] = {}
    if not str(data.get(CONF_NAME) or "").strip():
        errors[CONF_NAME] = "name_required"
    if not data.get(CONF_COVER) and not data.get(CONF_WINDOW_SENSORS):
        # without both the window does nothing for any module
        errors["base"] = "contact_or_cover_required"
    if contact_in_use(entry, contacts(data), own_id) is not None:
        errors[CONF_WINDOW_SENSORS] = "contact_in_use"
    if cover_in_use(entry, data.get(CONF_COVER), own_id) is not None:
        errors[CONF_COVER] = "cover_in_use"
    room = data.get(CONF_ROOM)
    if room and room not in rooms(entry):
        errors[CONF_ROOM] = "unknown_room"
    return errors
