"""Service actions of the house: the vacation."""

from __future__ import annotations

from datetime import datetime

import probatio as vol
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.util import dt as dt_util

from ..const import DOMAIN
from ..runtime import HouseRuntime
from .auth import require_admin
from .vacation import HouseModule

SERVICE_SET_VACATION = "set_vacation"
ATTR_DEPARTURE = "departure"
ATTR_RETURN = "return"
ATTR_CLEAR = "clear"

SET_VACATION_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_DEPARTURE): cv.datetime,
        vol.Optional(ATTR_RETURN): cv.datetime,
        vol.Optional(ATTR_CLEAR, default=False): cv.boolean,
    }
)


def _house(hass: HomeAssistant) -> HouseModule:
    for entry in hass.config_entries.async_loaded_entries(DOMAIN):
        runtime = getattr(entry, "runtime_data", None)
        if isinstance(runtime, HouseRuntime) and isinstance(runtime.house, HouseModule):
            return runtime.house
    raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_loaded")


def _aware(value: datetime | None) -> datetime | None:
    """A time without a zone is local time."""
    if value is None or value.tzinfo is not None:
        return value
    return value.replace(tzinfo=dt_util.get_default_time_zone())


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    async def set_vacation(call: ServiceCall) -> None:
        """Plan the vacation: departure and return; ``clear`` first ends it and removes
        both. Only a return: vacation from now on until then."""
        await require_admin(hass, call)
        house = _house(hass)
        data = call.data
        if data[ATTR_CLEAR]:
            house.clear()
        if ATTR_DEPARTURE not in data and ATTR_RETURN not in data:
            return
        house.set_times(
            _aware(data.get(ATTR_DEPARTURE, house.times.departure)),
            _aware(data.get(ATTR_RETURN, house.times.return_at)),
        )

    hass.services.async_register(DOMAIN, SERVICE_SET_VACATION, set_vacation, SET_VACATION_SCHEMA)
