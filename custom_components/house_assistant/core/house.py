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
from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import floor_registry as fr

from ..const import (
    CONF_DRAFT_REACH,
    CONF_HOUSE_DEPTH,
    CONF_HOUSE_WIDTH,
    MODULE_SHUTTER,
    OPT_CORE,
    SUBENTRY_GROUP,
    SUBENTRY_ROOM,
    SUBENTRY_WINDOW,
)
from ..runtime import module_options, shared_options
from .logic.geometry import DEFAULT_REACH, Plan, WindowPlace, plan

CONF_NAME: Final = "name"
# room: Home Assistant area (the room device is placed there, it gives the floor)
CONF_AREA: Final = "area"
# room: floor area (m²), splits the heat meter over the rooms (heating.logic.room_energy)
CONF_FLOOR_AREA: Final = "floor_area"
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
# window: wall of the house and order on it; without a wall the one of its group counts
CONF_WALL: Final = "wall"
CONF_WALL_POSITION: Final = "wall_position"
CONF_GROUP: Final = "group"
# room: automatic combinations of windows switched off (keys of logic.geometry)
CONF_AUTO_DRAFT_OFF: Final = "auto_draft_off"

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


def room_tilts(entry: ConfigEntry, room_id: str) -> dict[str, list[str]]:
    """Window contact -> tilt contacts of its window, for the windows of a room."""
    found: dict[str, list[str]] = {}
    for sub in windows_of_room(entry, room_id).values():
        tilts = [str(e) for e in sub.data.get(CONF_TILT_SENSORS) or ()]
        for entity_id in sub.data.get(CONF_WINDOW_SENSORS) or ():
            found[str(entity_id)] = tilts
    return found


def window_wall(entry: ConfigEntry, data: Mapping[str, Any]) -> str | None:
    """The wall of a window: its own, else the one of its group (direction)."""
    if data.get(CONF_WALL):
        return str(data[CONF_WALL])
    group = subentries(entry, SUBENTRY_GROUP).get(str(data.get(CONF_GROUP, "")))
    return str(group.data[CONF_WALL]) if group and group.data.get(CONF_WALL) else None


def room_floors(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, str | None]:
    """Room -> floor of its Home Assistant area. Without floors in Home Assistant every
    room is on one floor; a room whose floor cannot be told gets None."""
    if not fr.async_get(hass).async_list_floors():
        return dict.fromkeys(rooms(entry), "")
    areas = ar.async_get(hass)
    result: dict[str, str | None] = {}
    for room_id, sub in rooms(entry).items():
        area = areas.async_get_area(sub.data[CONF_AREA]) if sub.data.get(CONF_AREA) else None
        result[room_id] = area.floor_id if area is not None else None
    return result


def house_dimensions(entry: ConfigEntry) -> dict[str, float | None]:
    """Width and depth of the house (the plan of the house, else the one of the covers)."""
    house = {**module_options(entry, MODULE_SHUTTER), **shared_options(entry)}
    return {
        CONF_HOUSE_WIDTH: _number(house.get(CONF_HOUSE_WIDTH)),
        CONF_HOUSE_DEPTH: _number(house.get(CONF_HOUSE_DEPTH)),
    }


def house_plan(hass: HomeAssistant, entry: ConfigEntry, with_disabled: bool = False) -> Plan:
    """Cross ventilation and draft of every room from the windows (see logic.geometry);
    ``with_disabled``: also the combinations a room switched off."""
    places = []
    for window_id, sub in windows(entry).items():
        position = sub.data.get(CONF_WALL_POSITION)
        places.append(
            WindowPlace(
                window_id,
                str(sub.data[CONF_ROOM]) if sub.data.get(CONF_ROOM) else None,
                window_wall(entry, sub.data),
                float(position) if isinstance(position, int | float) else None,
            )
        )
    size = house_dimensions(entry)
    reach = module_options(entry, OPT_CORE).get(CONF_DRAFT_REACH, DEFAULT_REACH)
    disabled = {
        room_id: sub.data.get(CONF_AUTO_DRAFT_OFF) or [] for room_id, sub in rooms(entry).items()
    }
    return plan(
        places,
        room_floors(hass, entry),
        size[CONF_HOUSE_WIDTH],
        size[CONF_HOUSE_DEPTH],
        float(reach),
        None if with_disabled else disabled,
    )


def _number(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else None
