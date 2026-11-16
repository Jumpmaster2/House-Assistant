"""Idempotent correction of stored heating options on startup."""

from typing import Any

from ..const import LOGGER
from .const import (
    CONF_LIMITS,
    CONF_VENT_MAX_MINUTES,
    CONF_VENT_MIN_MINUTES,
    CONF_VENT_MOULD_RH,
    DEFAULTS,
)
from .logic.ai_schema import normalize_limits


def normalize_options(options: dict[str, Any]) -> dict[str, Any]:
    """Repair unusable AI limits and contradictory airing durations."""
    result = dict(options)
    result.pop("ventilation_energy_rh_per_k", None)
    if result.get(CONF_VENT_MOULD_RH, 70) == 70:
        result[CONF_VENT_MOULD_RH] = 65.0
        LOGGER.info("Migrated ventilation always-air threshold from legacy default to 65 %")
    if CONF_LIMITS in result:
        limits = normalize_limits(result[CONF_LIMITS])
        if limits != result[CONF_LIMITS]:
            result[CONF_LIMITS] = limits
    low = result.get(CONF_VENT_MIN_MINUTES, DEFAULTS[CONF_VENT_MIN_MINUTES])
    high = result.get(CONF_VENT_MAX_MINUTES, DEFAULTS[CONF_VENT_MAX_MINUTES])
    if low > high:
        result[CONF_VENT_MIN_MINUTES] = high
        LOGGER.debug("Clamped stored airing minimum to maximum")
    return result
