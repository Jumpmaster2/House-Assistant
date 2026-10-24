"""WebSocket API of the house section of the panel: rooms and windows.

The house section edits what every module builds on: name, area and sensors of a room,
room, size, contacts and cover of a window. The settings of the modules (heating of a
room, sun protection of a window) are edited in their sections; saving here keeps them.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any

import probatio as vol
from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import section
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import Selector

from ..const import DOMAIN, SUBENTRY_GROUP, SUBENTRY_ROOM, SUBENTRY_WINDOW
from ..heating.config_flow import area_schema, other_areas, validate_area
from ..runtime import enabled_modules
from ..shutter.config_flow import window_basics_fields
from ..shutter.websocket import WINDOW_WALL_FIELDS
from .entry import house_entry
from .house import (
    CONF_NAME,
    CONF_ROOM,
    CONF_SIZE,
    rooms,
    subentries,
    window_errors,
    window_size,
    windows,
)
from .schema import PanelError, coerce, spec

PREFIX = f"{DOMAIN}/house"


def _flat(schema: vol.Schema) -> dict[Any, Any]:
    """Fields of a form, sections flattened."""
    fields: dict[Any, Any] = {}
    for marker, value in schema.schema.items():
        if isinstance(value, section):
            fields.update(_flat(value.schema))
        else:
            fields[marker] = value
    return fields


def room_fields() -> dict[Any, Any]:
    """Name, area, sensors and air conditioner of a room (the heating has the rest)."""
    return _flat(area_schema({}, heating=False, covers=True))


def window_fields(entry: ConfigEntry) -> dict[Any, Any]:
    groups = {sub_id: sub.title for sub_id, sub in subentries(entry, SUBENTRY_GROUP).items()}
    room_titles = {sub_id: sub.title for sub_id, sub in rooms(entry).items()}
    return {**window_basics_fields({}, groups, room_titles), **WINDOW_WALL_FIELDS}


def _specs(fields: dict[Any, Any]) -> dict[str, Any]:
    return {
        str(marker): spec(validator)
        for marker, validator in fields.items()
        if isinstance(validator, Selector)
    }


def config_payload(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    registry = er.async_get(hass)
    house_windows = windows(entry)
    return {
        "entry_id": entry.entry_id,
        "modules": enabled_modules(entry),
        "rooms": [
            {
                "id": sub_id,
                "title": sub.title,
                "data": dict(sub.data),
                "windows": [
                    w_id for w_id, w in house_windows.items() if w.data.get(CONF_ROOM) == sub_id
                ],
                "climate": registry.async_get_entity_id("climate", DOMAIN, f"{sub_id}_climate"),
            }
            for sub_id, sub in rooms(entry).items()
        ],
        "windows": [
            {
                "id": sub_id,
                "title": sub.title,
                "data": {**sub.data, "size": window_size(sub.data)},
            }
            for sub_id, sub in house_windows.items()
        ],
        "fields": {"room": _specs(room_fields()), "window": _specs(window_fields(entry))},
    }


def _check(fields: dict[Any, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Values of the form fields, checked with the selectors of the dialogs (an empty
    optional field is left out); raises PanelError."""
    result: dict[str, Any] = {}
    for marker, selector in fields.items():
        key = str(marker)
        if key == CONF_NAME or key not in values:
            continue
        try:
            value = coerce(selector, values[key])
        except (vol.Invalid, TypeError, ValueError) as err:
            raise PanelError("invalid_value", key) from err
        if value is not None and value != []:
            result[key] = value
    return result


def room_data(
    entry: ConfigEntry, sub_id: str | None, title: str, values: dict[str, Any]
) -> dict[str, Any]:
    """Data of a room from the house section: its fields replaced, the heating's kept."""
    fields = room_fields()
    current = dict(entry.subentries[sub_id].data) if sub_id else {}
    kept = {k: v for k, v in current.items() if k not in {str(m) for m in fields}}
    data = {**kept, **_check(fields, values), CONF_NAME: title.strip()}
    errors = validate_area(data, other_areas(entry, sub_id))
    if error := errors.get(CONF_NAME) or errors.get("base"):
        raise PanelError(error)
    return data


def window_data(
    entry: ConfigEntry, sub_id: str | None, title: str, values: dict[str, Any]
) -> dict[str, Any]:
    """Data of a window from the house section: its basics replaced, the cover
    settings kept."""
    fields = window_fields(entry)
    current = dict(entry.subentries[sub_id].data) if sub_id else {}
    kept = {k: v for k, v in current.items() if k not in {str(m) for m in fields}}
    data = {**kept, **_check(fields, values), CONF_NAME: title.strip()}
    data[CONF_SIZE] = window_size(data)
    for key, error in window_errors(entry, data, sub_id).items():
        raise PanelError(error, None if key == "base" else key)
    return data


def _error(connection: websocket_api.ActiveConnection, msg_id: int, err: Exception) -> None:
    connection.send_error(msg_id, "invalid", str(err))


@websocket_api.websocket_command({vol.Required("type"): f"{PREFIX}/config"})
@websocket_api.require_admin
@callback
def ws_config(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    entry = house_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not set up")
        return
    connection.send_result(msg["id"], config_payload(hass, entry))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{PREFIX}/save",
        vol.Required("subentry_type"): vol.In([SUBENTRY_ROOM, SUBENTRY_WINDOW]),
        vol.Optional("subentry_id"): str,
        vol.Required("title"): str,
        vol.Required("data"): dict,
    }
)
@websocket_api.require_admin
@callback
def ws_save(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Add or change a room or a window."""
    entry = house_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not set up")
        return
    subentry_type = msg["subentry_type"]
    sub_id = msg.get("subentry_id")
    subentry = entry.subentries.get(sub_id) if sub_id else None
    if sub_id and (subentry is None or subentry.subentry_type != subentry_type):
        connection.send_error(msg["id"], "not_found", "sub item not found")
        return
    build = room_data if subentry_type == SUBENTRY_ROOM else window_data
    try:
        data = build(entry, sub_id, msg["title"], msg["data"])
    except PanelError as err:
        _error(connection, msg["id"], err)
        return
    title = data[CONF_NAME]
    if subentry is not None:
        hass.config_entries.async_update_subentry(entry, subentry, data=data, title=title)
    else:
        subentry = ConfigSubentry(
            data=MappingProxyType(data), subentry_type=subentry_type, title=title, unique_id=None
        )
        hass.config_entries.async_add_subentry(entry, subentry)
    connection.send_result(
        msg["id"], {"subentry_id": subentry.subentry_id, "config": config_payload(hass, entry)}
    )


@websocket_api.websocket_command(
    {vol.Required("type"): f"{PREFIX}/delete", vol.Required("subentry_id"): str}
)
@websocket_api.require_admin
@callback
def ws_delete(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Delete a room or a window. The windows of a deleted room keep going without one."""
    entry = house_entry(hass)
    subentry = entry.subentries.get(msg["subentry_id"]) if entry else None
    if (
        entry is None
        or subentry is None
        or subentry.subentry_type
        not in (
            SUBENTRY_ROOM,
            SUBENTRY_WINDOW,
        )
    ):
        connection.send_error(msg["id"], "not_found", "sub item not found")
        return
    if subentry.subentry_type == SUBENTRY_ROOM:
        for window in windows(entry).values():
            if window.data.get(CONF_ROOM) == subentry.subentry_id:
                data = {k: v for k, v in window.data.items() if k != CONF_ROOM}
                hass.config_entries.async_update_subentry(entry, window, data=data)
    hass.config_entries.async_remove_subentry(entry, subentry.subentry_id)
    connection.send_result(msg["id"], {"config": config_payload(hass, entry)})


COMMANDS = (ws_config, ws_save, ws_delete)
