"""Humidity first ventilation advice with short airings and stable recommendations."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from enum import StrEnum
from math import ceil
from typing import Any

from ...core.store_validation import checked_fields, dataclass_schema
from .physics import absolute_humidity


class VentilationState(StrEnum):
    """Possible recommendations."""

    UNKNOWN = "unknown"
    AIRING = "airing"
    CLOSE_WINDOW = "close_window"
    VENTILATE_NOW = "ventilate_now"
    VENTILATION_USEFUL = "ventilation_useful"
    DO_NOT_VENTILATE = "do_not_ventilate"
    BLOCKED = "blocked"
    OPTIMAL = "optimal"
    VACATION = "vacation"


class VentilationReason(StrEnum):
    """Stable reasons for sensors, cards and the panel."""

    MOULD_LIMIT = "mould_limit"
    HUMID_SHORT_AIRING = "humid_short_airing"
    AIRING_RUNNING = "airing_running"
    TARGET_REACHED = "target_reached"
    AIRING_TIME_OVER = "airing_time_over"
    BELOW_THRESHOLD_SAVE_HEAT = "below_threshold_save_heat"
    OUTSIDE_NOT_DRIER = "outside_not_drier"
    OUTSIDE_WARMER = "outside_warmer"
    PAUSE_AFTER_AIRING = "pause_after_airing"
    LITTLE_EFFECT = "little_effect"
    COOLING = "cooling"
    BLOCKED = "blocked"
    OPTIMAL = "optimal"
    VACATION = "vacation"
    UNKNOWN = "unknown"


MOULD_RH = 65.0  # always air from here if the reference air is drier
RECOMMENDATION_HOLD_MIN = 10.0
AIRING_TOLERANCE_MIN = 2.0
# Airing time by reference temperature while the exchange rate of the room is not
# learned yet: cold air exchanges fast and costs heat.
AIRING_MINUTES = ((0.0, 5), (10.0, 10), (15.0, 15))
AIRING_MINUTES_WARM = 20

RECOMMENDED_STATES = {
    VentilationState.VENTILATE_NOW,
    VentilationState.VENTILATION_USEFUL,
    VentilationState.AIRING,
}

# Domains whose entity blocks the ventilation recommendation while it is "on".
ON_OFF_DOMAINS = {"binary_sensor", "input_boolean", "switch", "fan", "humidifier", "light"}
# domains with a defined blocking state (offered in the dialog; others still work)
BLOCK_DOMAINS = (*sorted(ON_OFF_DOMAINS), "climate", "cover", "water_heater")
NO_STATE = {"unavailable", "unknown", "none", ""}


def is_blocking(domain: str, state: str) -> bool:
    """Does an entity in this state block the recommendation?

    A cover blocks while closed (sun protection down), a climate entity or water heater
    while not off (e.g. an air conditioner running), on/off entities while on; any
    other entity while it is active (not off or idle).
    """
    if state in NO_STATE:
        return False
    if domain == "cover":
        return state in ("closed", "closing")
    if domain in ("climate", "water_heater"):
        return state != "off"
    if domain in ON_OFF_DOMAINS:
        return state == "on"
    return state not in ("off", "idle")


@dataclass(slots=True)
class VentilationSettings:
    """Thresholds of one area. The configuration gives the start values, the AI may
    adjust them within limits."""

    rh_threshold: float = 60.0
    rh_hysteresis: float = 3.0  # humidity stays "high" until this far below the threshold
    min_ah_advantage: float = 0.8
    max_reference_excess: float = 4.0
    min_cooling_advantage: float = 1.0
    cooling_margin: float = 1.0  # heating period: cool only this far above target
    cooling_min_temp: float = 0.0  # cool only from this room temperature on (0 = off)
    min_rh_drop: float = 3.0  # airing must lower the humidity at least this far
    mould_rh: float = MOULD_RH  # from here airing is always recommended
    airing_target_below: float = 5.0  # airing aims this far below the threshold
    airing_time_factor: float = 1.0  # scales the computed airing time
    airing_min_minutes: float = 3.0
    airing_max_minutes: float = 20.0
    airing_pause_min: float = 30.0  # no new drying recommendation this soon after airing

    def as_dict(self) -> dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None, **defaults: float) -> VentilationSettings:
        data = checked_fields(data, dataclass_schema(cls))
        settings = cls(**defaults)
        if data:
            for f in fields(cls):
                if f.name in data:
                    try:
                        setattr(settings, f.name, float(data[f.name]))
                    except (TypeError, ValueError):
                        continue
        return settings


@dataclass(slots=True)
class VentilationInput:
    """Measured values for one area."""

    temp: float | None
    humidity: float | None
    ref_temp: float | None
    ref_humidity: float | None
    window_open: bool = False
    heating_active: bool = False
    blocked: bool = False
    # Cooling advantage counts only at night when the reference is another room.
    reference_is_indoor: bool = False
    is_night: bool = False
    target: float | None = None
    season_active: bool = False
    was_rh_high: bool = False  # humidity was high at the last evaluation (hysteresis)
    was_drying: bool = False  # "ventilate now" at the last evaluation (hysteresis)
    # relative humidity a usual airing reaches immediately, before rebound
    achievable_rh: float | None = None
    # minutes the room needs to reach the airing target (learned exchange rate)
    learned_airing_minutes: float | None = None
    # relative opening area the airing time is meant for (see logic.windows)
    opening: float = 1.0
    minutes_since_airing: float | None = None  # since the own window was last closed
    window_open_minutes: float = 0.0
    # Freeze time and target at opening so a falling humidity cannot move the deadline.
    airing_started_high: bool = False
    running_airing_minutes: int | None = None
    airing_target_rh: float | None = None
    previous_state: VentilationState | None = None
    previous_reason: VentilationReason = VentilationReason.UNKNOWN
    minutes_since_change: float | None = None
    window_changed: bool = False


@dataclass(slots=True)
class VentilationResult:
    """Recommendation plus the values it is based on."""

    state: VentilationState
    ah_inside: float | None = None
    ah_reference: float | None = None
    delta_ah: float | None = None
    delta_t: float | None = None
    rh_high: bool = False
    drying_useful: bool = False
    cooling_useful: bool = False
    rh_after_exchange: float | None = None
    achievable_rh: float | None = None
    pause_hold: bool = False  # drying would help but the room settles after airing
    airing_minutes: int | None = None  # suggested airing time while recommended
    reason: VentilationReason = VentilationReason.UNKNOWN
    airing_minutes_left: int | None = None

    @property
    def recommended(self) -> bool:
        """Return True if opening the window is recommended."""
        return self.state in RECOMMENDED_STATES


def recommend(data: VentilationInput, settings: VentilationSettings) -> VentilationResult:
    """Return the ventilation recommendation for one area."""
    if None in (data.temp, data.humidity, data.ref_temp, data.ref_humidity):
        return VentilationResult(VentilationState.UNKNOWN)
    assert data.temp is not None and data.humidity is not None
    assert data.ref_temp is not None and data.ref_humidity is not None

    ah_inside = absolute_humidity(data.temp, data.humidity)
    ah_ref = absolute_humidity(data.ref_temp, data.ref_humidity)
    delta_ah = ah_inside - ah_ref
    delta_t = data.temp - data.ref_temp
    reference_excess = data.ref_temp - data.temp

    rh_high = data.humidity >= settings.rh_threshold or (
        (data.was_rh_high or data.was_drying)
        and data.humidity >= settings.rh_threshold - settings.rh_hysteresis
    )
    # Relative humidity of the room if its air were replaced by reference air
    # (walls and floor keep the room temperature).
    rh_after = 100.0 * ah_ref / absolute_humidity(data.temp, 100.0)
    drier = (
        delta_ah >= settings.min_ah_advantage and reference_excess <= settings.max_reference_excess
    )
    immediate_effect = (
        data.achievable_rh is None or data.humidity - data.achievable_rh >= settings.min_rh_drop
    )
    drying_useful = drier and immediate_effect
    always = data.humidity >= settings.mould_rh
    cooling_useful = (
        delta_t >= settings.min_cooling_advantage
        and not data.heating_active
        and (not data.reference_is_indoor or data.is_night)
        and (
            not data.season_active
            or data.target is None
            or data.temp >= data.target + settings.cooling_margin
        )
        and (settings.cooling_min_temp <= 0 or data.temp >= settings.cooling_min_temp)
        and rh_after <= settings.rh_threshold
    )
    pause_hold = (
        drier
        and rh_high
        and not always
        and not data.window_open
        and data.minutes_since_airing is not None
        and data.minutes_since_airing < settings.airing_pause_min
    )
    base = data.learned_airing_minutes
    if base is None:
        base = next(
            (m for limit, m in AIRING_MINUTES if data.ref_temp <= limit), AIRING_MINUTES_WARM
        ) / max(0.1, data.opening)
    duration = round(
        max(
            settings.airing_min_minutes,
            min(settings.airing_max_minutes, base * settings.airing_time_factor),
        )
    )
    if data.window_open and data.running_airing_minutes is not None:
        duration = data.running_airing_minutes
    target = data.airing_target_rh
    if target is None:
        target = (
            settings.mould_rh if always else settings.rh_threshold
        ) - settings.airing_target_below
    heat = data.season_active or data.heating_active
    time_over = heat and data.window_open_minutes >= duration + AIRING_TOLERANCE_MIN
    benefit = (
        drier and (always or (rh_high and immediate_effect and not pause_hold))
    ) or cooling_useful
    minutes_left = None

    if data.blocked:
        state = (
            VentilationState.CLOSE_WINDOW
            if data.window_open
            else VentilationState.BLOCKED
            if benefit
            else VentilationState.OPTIMAL
        )
        reason = VentilationReason.BLOCKED
    elif data.window_open:
        below_start = data.humidity < settings.rh_threshold and not (
            data.airing_started_high or data.was_rh_high
        )
        if drier and data.humidity > target and not time_over and not below_start:
            state, reason = VentilationState.AIRING, VentilationReason.AIRING_RUNNING
            minutes_left = max(0, ceil(duration - data.window_open_minutes)) if heat else None
        elif cooling_useful:
            state, reason = VentilationState.VENTILATION_USEFUL, VentilationReason.COOLING
        elif heat:
            state = VentilationState.CLOSE_WINDOW
            if not drier:
                reason = VentilationReason.OUTSIDE_NOT_DRIER
            elif data.humidity <= target:
                reason = VentilationReason.TARGET_REACHED
            elif below_start:
                reason = VentilationReason.BELOW_THRESHOLD_SAVE_HEAT
            else:
                reason = VentilationReason.AIRING_TIME_OVER
        elif (
            delta_ah < 0 and data.humidity >= settings.rh_threshold - settings.rh_hysteresis
        ) or delta_t < 0:
            state = VentilationState.CLOSE_WINDOW
            reason = (
                VentilationReason.OUTSIDE_WARMER
                if delta_t < 0
                else VentilationReason.OUTSIDE_NOT_DRIER
            )
        else:
            state, reason = VentilationState.OPTIMAL, VentilationReason.OPTIMAL
    elif always and drier:
        state, reason = VentilationState.VENTILATE_NOW, VentilationReason.MOULD_LIMIT
    elif rh_high and drier and immediate_effect and not pause_hold:
        state, reason = VentilationState.VENTILATE_NOW, VentilationReason.HUMID_SHORT_AIRING
    elif cooling_useful:
        state, reason = VentilationState.VENTILATION_USEFUL, VentilationReason.COOLING
    elif rh_high and drier:
        state = VentilationState.DO_NOT_VENTILATE
        reason = (
            VentilationReason.PAUSE_AFTER_AIRING if pause_hold else VentilationReason.LITTLE_EFFECT
        )
    elif rh_high:
        state, reason = VentilationState.DO_NOT_VENTILATE, VentilationReason.OUTSIDE_NOT_DRIER
    else:
        state, reason = VentilationState.OPTIMAL, VentilationReason.OPTIMAL

    quiet_states = {VentilationState.OPTIMAL, VentilationState.DO_NOT_VENTILATE}
    flips = (data.previous_state == VentilationState.VENTILATE_NOW and state in quiet_states) or (
        state == VentilationState.VENTILATE_NOW and data.previous_state in quiet_states
    )
    if (
        flips
        and not always
        and not data.blocked
        # Losing the drying advantage ends advice immediately; hold its return instead.
        and (drier or data.previous_state != VentilationState.VENTILATE_NOW)
        and not data.window_open
        and not data.window_changed
        and data.minutes_since_change is not None
        and data.minutes_since_change < RECOMMENDATION_HOLD_MIN
    ):
        state, reason = data.previous_state, data.previous_reason

    airing_minutes = duration if state in RECOMMENDED_STATES else None
    return VentilationResult(
        state=state,
        ah_inside=round(ah_inside, 2),
        ah_reference=round(ah_ref, 2),
        delta_ah=round(delta_ah, 2),
        delta_t=round(delta_t, 2),
        rh_high=rh_high,
        drying_useful=drying_useful,
        cooling_useful=cooling_useful,
        rh_after_exchange=round(rh_after, 1),
        achievable_rh=None if data.achievable_rh is None else round(data.achievable_rh, 1),
        pause_hold=pause_hold,
        airing_minutes=airing_minutes,
        reason=reason,
        airing_minutes_left=minutes_left,
    )


def room_limits(
    configured: dict[str, float],
    limits: dict[str, dict[str, float]],
    mould_rh: float | None = None,
) -> dict[str, dict[str, float]]:
    """Intersect global AI limits with the room's non-negotiable comfort bounds.

    The room's safety ceiling wins if legacy global limits contradict it.
    """
    result = {key: dict(value) for key, value in limits.items()}
    threshold = configured["rh_threshold"]
    always = configured["mould_rh"]
    for key, low, high in (
        ("mould_rh", 55.0, always),
        (
            "rh_threshold",
            threshold - 5.0,
            min(threshold + 2.0, always, mould_rh if mould_rh is not None else always),
        ),
        ("rh_hysteresis", 2.0, 5.0),
    ):
        bound = result[key]
        bound["max"] = min(high, max(low, bound["max"]))
        bound["min"] = min(bound["max"], max(low, bound["min"]))
    return result
