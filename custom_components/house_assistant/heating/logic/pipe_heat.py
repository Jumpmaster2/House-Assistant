"""Pipe heat from other circuits, based only on their actual switch states.

The gain is configured, not fitted alongside a/k/s: the source has no measured
transport delay and normally runs in the same cold periods as the target. A
fourth RLS coefficient would trade heat loss, solar gain and pipe heat against
one another. The AI can instead calibrate the bounded pipe_factor.

The target's RLS learner subtracts the configured, scaled gain averaged over its
rate window. Windows with a correction above 50 % of the absolute observed rate
or any of the first 20 min after source activity are skipped (unmeasured residual
heat). Dead time and overshoot discard only events overlapping source activity
or starting less than 20 min afterwards; there is no four-hour pipe quarantine.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from ...core.logic.numbers import finite_float
from .physics import clamp

PIPE_GAIN_DEFAULT = 0.15
PIPE_GAIN_BOUNDS = (0.0, 1.0)
PIPE_WEIGHT_DEFAULT = 1.0
PIPE_WEIGHT_BOUNDS = (0.1, 3.0)
PIPE_WEIGHT_STEP = 0.1


def clean_pipe_sources(configured: Any, valid: Iterable[str]) -> list[str]:
    """Drop stale/self/non-circuit references and duplicates, retaining order."""
    allowed = set(valid)
    if not isinstance(configured, list):
        return []
    return list(dict.fromkeys(s for s in configured if isinstance(s, str) and s in allowed))


def clean_pipe_weights(
    configured: Any, sources: Iterable[str], *, strict: bool = False
) -> dict[str, float]:
    """Weights for valid selected circuits only; defaults also cover older rooms.

    Saving rejects invalid selected weights. Runtime ignores damaged values,
    retaining the default rather than propagating nonfinite numbers.
    """
    if not isinstance(configured, dict):
        if strict:
            raise ValueError("pipe_source_weights must be a mapping")
        configured = {}
    weights = {}
    for source in sources:
        try:
            raw = configured.get(source, PIPE_WEIGHT_DEFAULT)
            if isinstance(raw, bool):
                raise ValueError("weight must be a number")
            weight = finite_float(raw)
            if not PIPE_WEIGHT_BOUNDS[0] <= weight <= PIPE_WEIGHT_BOUNDS[1]:
                raise ValueError("weight must be between 0.1 and 3.0")
            steps = weight / PIPE_WEIGHT_STEP
            if abs(steps - round(steps)) > 1e-6:
                raise ValueError("weight step must be 0.1")
        except (TypeError, ValueError, OverflowError):
            if strict:
                raise
            weight = PIPE_WEIGHT_DEFAULT
        weights[source] = weight
    return weights


def pipe_rate(gain: float, factor: float, weighted_states: Iterable[float]) -> float:
    """K/h from the sum of weight * actual state; never average or cap at one.

    Unavailable circuits contribute zero. With no configured sources the sum is zero.
    """
    return clamp(gain, *PIPE_GAIN_BOUNDS) * clamp(factor, 0.0, 2.0) * sum(weighted_states)
