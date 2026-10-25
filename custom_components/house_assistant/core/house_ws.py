"""WebSocket API of the house section of the panel: rooms, windows and the settings of
the house.

The house section edits what every module builds on: name, area and sensors of a room,
room, size, contacts and cover of a window, the shared settings and the modules. The
settings of the modules (heating of a room, sun protection of a window) are edited in
their sections; saving here keeps them.
"""

from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import Any

import probatio as vol
from homeassistant.components import websocket_api
from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import section
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import Selector
from homeassistant.util import dt as dt_util

from ..const import (
    CONF_MODULES,
    CONF_SHOW_PANEL,
    CONF_VACATION_WINDOW_ALERT,
    DOMAIN,
    MODULE_HEATING,
    MODULE_ORDER,
    MODULE_SHUTTER,
    OPT_CORE,
    SHARED_KEYS,
    SUBENTRY_GROUP,
    SUBENTRY_ROOM,
    SUBENTRY_WINDOW,
)
from ..heating.config_flow import area_schema, other_areas, validate_area
from ..runtime import enabled_modules, module_options
from ..shutter.config_flow import window_basics_fields
from ..shutter.websocket import WINDOW_WALL_FIELDS
from .entry import house_entry, update_section
from .house import (
    CONF_AUTO_DRAFT_OFF,
    CONF_NAME,
    CONF_ROOM,
    CONF_SIZE,
    house_dimensions,
    house_plan,
    rooms,
    subentries,
    window_errors,
    window_size,
    windows,
)
from .logic.geometry import Plan
from .schema import PanelError, coerce, spec
from .settings import (
    HOUSE_FORM,
    VACATION_FORM,
    VACATION_OPTIONS,
    house_schema,
    vacation_schema,
    validate_house,
)
from .vacation import DEFAULT_WINDOW_ALERT, HouseModule

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


def _plan_payload(entry: ConfigEntry, plan: Plan) -> dict[str, Any]:
    """The house plan for the panel: points, the combinations of every room (also the
    ones switched off) and what keeps windows or rooms out."""
    off = {
        sub_id: set(sub.data.get(CONF_AUTO_DRAFT_OFF) or []) for sub_id, sub in rooms(entry).items()
    }
    return {
        "points": plan.points,
        "room_points": plan.room_points,
        "combinations": {
            room_id: [
                {
                    "key": c.key,
                    "kind": c.kind,
                    "windows": list(c.windows),
                    "enabled": c.key not in off.get(room_id, set()),
                }
                for c in combinations
            ]
            for room_id, combinations in plan.combinations.items()
        },
        "no_wall": plan.no_wall,
        "no_floor": plan.no_floor,
    }


def config_payload(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    registry = er.async_get(hass)
    house_windows = windows(entry)
    core = module_options(entry, OPT_CORE)
    # every combination, also the ones switched off (they are shown with their switch)
    plan = house_plan(hass, entry, with_disabled=True)
    return {
        "entry_id": entry.entry_id,
        "modules": enabled_modules(entry),
        "available": list(MODULE_ORDER),
        "show_panel": bool(core.get(CONF_SHOW_PANEL, True)),
        "settings": {key: core[key] for key in SHARED_KEYS if key in core},
        "plan": _plan_payload(entry, plan),
        "house": {k: v for k, v in house_dimensions(entry).items() if v is not None},
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
        "fields": {
            "room": _specs(room_fields()),
            "window": _specs(window_fields(entry)),
            "settings": _specs(house_schema(hass, core).schema),
            "vacation": _specs(vacation_schema(core).schema),
        },
        "vacation": vacation_payload(entry),
    }


def _house(entry: ConfigEntry) -> HouseModule | None:
    house = getattr(getattr(entry, "runtime_data", None), "house", None)
    return house if isinstance(house, HouseModule) else None


def _local(value: datetime | None) -> str | None:
    return dt_util.as_local(value).isoformat() if value is not None else None


def vacation_payload(entry: ConfigEntry) -> dict[str, Any]:
    """The vacation of the house: switch, times, entities and settings (the options of
    heating and covers only while they run)."""
    core = module_options(entry, OPT_CORE)
    modules = enabled_modules(entry)
    options = {
        key: bool(module_options(entry, module).get(key, default))
        for module, key, default in VACATION_OPTIONS
        if module in modules
    }
    house = _house(entry)
    state: dict[str, Any] = {}
    if house is not None:
        state = {
            "on": house.times.on,
            "departure": _local(house.times.departure),
            "return": _local(house.times.return_at),
            "active": house.active,
            "source": house.source,
            "since": _local(house.since),
            "entities": {
                "switch": house.entity_id("switch", "vacation"),
                "departure": house.entity_id("datetime", "vacation_departure"),
                "return": house.entity_id("datetime", "vacation_return"),
                "active": house.entity_id("binary_sensor", "vacation_active"),
            },
        }
    return {
        **state,
        "settings": {
            CONF_VACATION_WINDOW_ALERT: DEFAULT_WINDOW_ALERT,
            **{key: core[key] for key in VACATION_FORM if key in core},
        },
        "options": options,
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


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{PREFIX}/save_settings",
        vol.Required("settings"): dict,
        vol.Optional("modules"): [vol.In(MODULE_ORDER)],
        vol.Optional("show_panel"): bool,
    }
)
@websocket_api.require_admin
@callback
def ws_save_settings(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    """The settings of the house (a value set applies to every module) and the modules."""
    entry = house_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not set up")
        return
    core = module_options(entry, OPT_CORE)
    modules = msg.get("modules", core.get(CONF_MODULES) or [])
    try:
        settings = _check(house_schema(hass, core).schema, msg["settings"])
    except PanelError as err:
        _error(connection, msg["id"], err)
        return
    own = [module_options(entry, key) for key in (MODULE_HEATING, MODULE_SHUTTER)]
    for key, error in validate_house(hass, settings, modules, [v for v in own if v]).items():
        _error(connection, msg["id"], PanelError(error, key))
        return
    core = {k: v for k, v in core.items() if k not in HOUSE_FORM}
    core.update(settings)
    core[CONF_MODULES] = [key for key in MODULE_ORDER if key in modules]
    if "show_panel" in msg:
        core[CONF_SHOW_PANEL] = msg["show_panel"]
    update_section(hass, entry, OPT_CORE, core)
    connection.send_result(msg["id"], config_payload(hass, entry))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{PREFIX}/combination",
        vol.Required("room_id"): str,
        vol.Required("key"): str,
        vol.Required("enabled"): bool,
    }
)
@websocket_api.require_admin
@callback
def ws_combination(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    """Switch an automatic combination of a room on or off."""
    entry = house_entry(hass)
    room = entry.subentries.get(msg["room_id"]) if entry else None
    if entry is None or room is None or room.subentry_type != SUBENTRY_ROOM:
        connection.send_error(msg["id"], "not_found", "room not found")
        return
    off = [key for key in room.data.get(CONF_AUTO_DRAFT_OFF) or [] if key != msg["key"]]
    if not msg["enabled"]:
        off.append(msg["key"])
    data = {k: v for k, v in room.data.items() if k != CONF_AUTO_DRAFT_OFF}
    if off:
        data[CONF_AUTO_DRAFT_OFF] = sorted(off)
    hass.config_entries.async_update_subentry(entry, room, data=data)
    connection.send_result(msg["id"], config_payload(hass, entry))


def _time(value: Any) -> datetime | None:
    """A time from the panel; without a zone it is local time."""
    if value in (None, ""):
        return None
    parsed = dt_util.parse_datetime(str(value))
    if parsed is None:
        raise PanelError("invalid_value")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.get_default_time_zone())
    return parsed


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{PREFIX}/vacation",
        vol.Optional("on"): bool,
        vol.Optional("departure"): vol.Any(str, None),
        vol.Optional("return"): vol.Any(str, None),
        vol.Optional("clear"): bool,
    }
)
@websocket_api.require_admin
@callback
def ws_vacation(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """Switch the vacation, plan departure and return, or clear everything."""
    entry = house_entry(hass)
    house = _house(entry) if entry is not None else None
    if entry is None or house is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not running")
        return
    try:
        if msg.get("clear"):
            house.clear()
        if "departure" in msg or "return" in msg:
            departure = _time(msg["departure"]) if "departure" in msg else house.times.departure
            return_at = _time(msg["return"]) if "return" in msg else house.times.return_at
            house.set_times(departure, return_at, strict=True)
        if "on" in msg:
            house.set_on(msg["on"])
    except PanelError as err:
        _error(connection, msg["id"], err)
        return
    except ServiceValidationError as err:
        _error(connection, msg["id"], PanelError(err.translation_key or "invalid_value"))
        return
    connection.send_result(msg["id"], config_payload(hass, entry))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{PREFIX}/vacation_settings",
        vol.Required("settings"): dict,
        vol.Optional("options"): {str: bool},
    }
)
@websocket_api.require_admin
@callback
def ws_vacation_settings(
    hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict
) -> None:
    """External sources and reports of the vacation; the vacation options of heating
    and covers. One update of the entry, so every module restarts at most once."""
    entry = house_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not set up")
        return
    core = module_options(entry, OPT_CORE)
    try:
        settings = _check(vacation_schema(core).schema, msg["settings"])
    except PanelError as err:
        _error(connection, msg["id"], err)
        return
    options = {**entry.options}
    options[OPT_CORE] = {**{k: v for k, v in core.items() if k not in VACATION_FORM}, **settings}
    modules = enabled_modules(entry)
    for module, key, _default in VACATION_OPTIONS:
        if module in modules and key in msg.get("options", {}):
            options[module] = {**module_options(entry, module), key: msg["options"][key]}
    hass.config_entries.async_update_entry(entry, options=options)
    connection.send_result(msg["id"], config_payload(hass, entry))


COMMANDS = (
    ws_config,
    ws_save,
    ws_delete,
    ws_save_settings,
    ws_combination,
    ws_vacation,
    ws_vacation_settings,
)
