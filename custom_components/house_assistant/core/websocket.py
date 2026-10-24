"""WebSocket API of the panel: the house and the commands of every module."""

from __future__ import annotations

import probatio as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant, callback

from ..const import DOMAIN, MODULE_ORDER
from ..heating.websocket import async_register_websocket as async_register_heating
from ..meter.websocket import async_register_websocket as async_register_meter
from ..runtime import enabled_modules
from ..shutter.websocket import async_register_websocket as async_register_shutter
from .entry import house_entry
from .house_ws import COMMANDS as HOUSE_COMMANDS

DATA_WS = f"{DOMAIN}_ws_registered"


@callback
def async_register_websocket(hass: HomeAssistant) -> None:
    if hass.data.get(DATA_WS):
        return
    hass.data[DATA_WS] = True
    websocket_api.async_register_command(hass, ws_config)
    for command in HOUSE_COMMANDS:
        websocket_api.async_register_command(hass, command)
    async_register_heating(hass)
    async_register_meter(hass)
    async_register_shutter(hass)


@websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/config"})
@websocket_api.require_admin
@callback
def ws_config(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict) -> None:
    """The house: which modules exist and which are switched on."""
    entry = house_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_found", "House Assistant is not set up")
        return
    house = getattr(getattr(entry, "runtime_data", None), "house", None)
    connection.send_result(
        msg["id"],
        {
            "entry_id": entry.entry_id,
            "modules": enabled_modules(entry),
            "available": list(MODULE_ORDER),
            # the panel shows a banner while it is vacation
            "vacation_entity": (
                house.entity_id("binary_sensor", "vacation_active") if house is not None else None
            ),
        },
    )
