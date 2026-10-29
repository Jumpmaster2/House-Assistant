"""Validation of manual meter readings before any state change."""

from typing import Any

from homeassistant.exceptions import ServiceValidationError

from ..core.logic.numbers import finite_float
from .const import DOMAIN


def reading_value(value: Any) -> float:
    """A finite, nonnegative meter reading."""
    try:
        result = finite_float(value)
        if result >= 0:
            return result
    except (TypeError, ValueError, OverflowError):
        pass
    raise ServiceValidationError(translation_domain=DOMAIN, translation_key="invalid_reading")
