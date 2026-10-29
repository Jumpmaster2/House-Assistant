"""Finite numeric input shared by modules."""

from math import isfinite
from typing import Any


def finite_float(value: Any) -> float:
    """Convert a number, rejecting NaN and infinities (including numeric strings)."""
    result = float(value)
    if not isfinite(result):
        raise ValueError("number must be finite")
    return result


def reject_constant(value: str) -> None:
    """Reject non-standard JSON numeric constants."""
    raise ValueError(f"invalid JSON constant {value}")
