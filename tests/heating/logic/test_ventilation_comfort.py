"""Comfort policy, running airings, recommendation stability and room safety bounds."""

from dataclasses import replace

import pytest

from custom_components.house_assistant.heating.logic.ai_schema import (
    VENT_PARAMS,
    default_limits,
    validate_check,
)
from custom_components.house_assistant.heating.logic.humidity_learning import HumidityProfile
from custom_components.house_assistant.heating.logic.physics import absolute_humidity
from custom_components.house_assistant.heating.logic.ventilation import (
    VentilationInput,
    VentilationSettings,
    recommend,
    room_limits,
)
from custom_components.house_assistant.heating.logic.ventilation import (
    VentilationReason as Reason,
)
from custom_components.house_assistant.heating.logic.ventilation import (
    VentilationState as State,
)
from custom_components.house_assistant.heating.validation import normalize_options

SETTINGS = VentilationSettings()
BEDROOM = VentilationInput(20.9, 66.7, 8.6, 92, season_active=True, heating_active=True)


def test_live_bedroom_high_rebound_still_needs_airing() -> None:
    profile = HumidityProfile()
    profile.exchange.value, profile.exchange.count = 0.6, 5
    profile.rebound.value = 0.8  # lasting exchange only 12 %
    ref = absolute_humidity(8.6, 92)
    immediate = profile.achievable_rh(20.9, 66.7, ref, immediate=True)
    lasting = profile.achievable_rh(20.9, 66.7, ref)
    assert immediate < lasting
    summary = profile.summary("heating", 20.9, 66.7, ref)
    assert summary["achievable_immediate_now"] == round(immediate, 1)
    assert summary["achievable_now"] == round(lasting, 1)
    result = recommend(replace(BEDROOM, achievable_rh=lasting), SETTINGS)
    assert result.state == State.VENTILATE_NOW and result.reason == Reason.MOULD_LIMIT
    # In the short-airing band only the immediate effect counts.
    result = recommend(replace(BEDROOM, humidity=62.4, achievable_rh=immediate), SETTINGS)
    assert result.state == State.VENTILATE_NOW


@pytest.mark.parametrize(
    ("rh", "elapsed", "state", "reason", "left"),
    [
        (62.4, 1, State.AIRING, Reason.AIRING_RUNNING, 9),
        (54, 2, State.CLOSE_WINDOW, Reason.TARGET_REACHED, None),
        (61, 12, State.CLOSE_WINDOW, Reason.AIRING_TIME_OVER, None),
        (57, 1, State.CLOSE_WINDOW, Reason.BELOW_THRESHOLD_SAVE_HEAT, None),
    ],
)
def test_open_window(rh, elapsed, state, reason, left) -> None:
    result = recommend(
        replace(BEDROOM, humidity=rh, window_open=True, window_open_minutes=elapsed), SETTINGS
    )
    assert (result.state, result.reason, result.airing_minutes_left) == (state, reason, left)
    assert result.recommended == (state == State.AIRING)


def test_started_airing_continues_below_start_threshold() -> None:
    result = recommend(
        replace(BEDROOM, humidity=57, window_open=True, airing_started_high=True), SETTINGS
    )
    assert result.state == State.AIRING


def test_frozen_target_and_duration_of_running_airing() -> None:
    result = recommend(
        replace(
            BEDROOM,
            humidity=59,
            window_open=True,
            airing_started_high=True,
            airing_target_rh=60,
            running_airing_minutes=5,
            learned_airing_minutes=15,
        ),
        SETTINGS,
    )
    assert result.reason == Reason.TARGET_REACHED
    result = recommend(
        replace(
            BEDROOM,
            humidity=61,
            window_open=True,
            window_open_minutes=8,
            running_airing_minutes=5,
            learned_airing_minutes=15,
        ),
        SETTINGS,
    )
    assert result.reason == Reason.AIRING_TIME_OVER


def test_pause_is_bypassed_only_from_always_limit() -> None:
    for rh, state, reason in (
        (62, State.DO_NOT_VENTILATE, Reason.PAUSE_AFTER_AIRING),
        (66, State.VENTILATE_NOW, Reason.MOULD_LIMIT),
    ):
        result = recommend(replace(BEDROOM, humidity=rh, minutes_since_airing=20), SETTINGS)
        assert (result.state, result.reason) == (state, reason)


def test_bathroom_uses_configured_65_without_special_room_logic() -> None:
    settings = VentilationSettings(rh_threshold=65, mould_rh=65)
    assert recommend(replace(BEDROOM, humidity=63), settings).state == State.OPTIMAL
    assert recommend(replace(BEDROOM, humidity=65), settings).state == State.VENTILATE_NOW


def test_hysteresis_near_old_ai_threshold_cannot_flap() -> None:
    previous = recommend(BEDROOM, SETTINGS)
    for minute, rh in enumerate([66.6, 67.1, 66.8, 67, 66.6, 67.1]):
        result = recommend(
            replace(
                BEDROOM,
                humidity=rh,
                was_rh_high=previous.rh_high,
                previous_state=previous.state,
                previous_reason=previous.reason,
                minutes_since_change=minute,
            ),
            SETTINGS,
        )
        assert result.state == State.VENTILATE_NOW
        previous = result


@pytest.mark.parametrize("previous", [State.OPTIMAL, State.DO_NOT_VENTILATE, State.VENTILATE_NOW])
def test_ten_minute_hold_both_directions(previous) -> None:
    data = replace(
        BEDROOM,
        humidity=56 if previous == State.VENTILATE_NOW else 62,
        previous_state=previous,
        previous_reason=Reason.OPTIMAL,
        minutes_since_change=9,
    )
    assert recommend(data, SETTINGS).state == previous
    assert recommend(replace(data, minutes_since_change=10), SETTINGS).state != previous
    assert recommend(replace(data, window_changed=True), SETTINGS).state != previous
    assert recommend(replace(data, humidity=66), SETTINGS).state == State.VENTILATE_NOW
    assert recommend(replace(data, blocked=True), SETTINGS).reason == Reason.BLOCKED


def test_summer_open_window_has_no_time_limit_or_energy_close() -> None:
    data = replace(
        BEDROOM,
        season_active=False,
        heating_active=False,
        target=24,
        ref_temp=20.5,
        ref_humidity=40,
        window_open=True,
        window_open_minutes=180,
    )
    assert recommend(replace(data, humidity=62), SETTINGS).state == State.AIRING
    result = recommend(replace(data, humidity=55), SETTINGS)
    assert result.state == State.OPTIMAL
    assert (
        recommend(replace(data, humidity=62, ref_temp=21, ref_humidity=90), SETTINGS).state
        == State.CLOSE_WINDOW
    )
    assert (
        recommend(replace(data, humidity=55, ref_temp=23, ref_humidity=40), SETTINGS).state
        == State.CLOSE_WINDOW
    )


def test_room_ai_bounds_override_unsafe_legacy_global_limits() -> None:
    global_limits = default_limits()
    global_limits["rh_hysteresis"] = {"min": 0, "max": 10, "step": 10}
    configured = SETTINGS.as_dict()
    bounds = room_limits(configured, global_limits)
    answer = {
        "confidence": 80,
        "adjustments": [
            {"area": "a1", "parameter": key, "value": value}
            for key, value in [("rh_threshold", 67), ("mould_rh", 70), ("rh_hysteresis", 0)]
        ],
    }
    result = validate_check(answer, {"a1": configured}, global_limits, VENT_PARAMS, {"a1": bounds})
    effective = {**configured, **{a.parameter: a.new for a in result.applied}}
    assert effective["rh_threshold"] == 62
    assert effective["mould_rh"] == 65
    assert effective["rh_hysteresis"] == 2
    assert room_limits(configured, global_limits, 58)["rh_threshold"]["max"] == 58


def test_legacy_options_are_migrated_once(caplog) -> None:
    for value in ({}, {"ventilation_mould_rh": 70, "ventilation_energy_rh_per_k": 0.25}):
        result = normalize_options(value)
        assert result["ventilation_mould_rh"] == 65
        assert "ventilation_energy_rh_per_k" not in result
        assert normalize_options(result) == result
    assert normalize_options({"ventilation_mould_rh": 63})["ventilation_mould_rh"] == 63


def test_losing_drying_advantage_ends_advice_and_holds_return() -> None:
    wet_outside = replace(
        BEDROOM,
        humidity=62,
        ref_temp=20,
        ref_humidity=90,
        previous_state=State.VENTILATE_NOW,
        previous_reason=Reason.HUMID_SHORT_AIRING,
        minutes_since_change=1,
    )
    result = recommend(wet_outside, SETTINGS)
    assert (result.state, result.reason) == (State.DO_NOT_VENTILATE, Reason.OUTSIDE_NOT_DRIER)
    dry_again = replace(
        BEDROOM,
        humidity=62,
        previous_state=result.state,
        previous_reason=result.reason,
        minutes_since_change=2,
    )
    assert recommend(dry_again, SETTINGS).state == State.DO_NOT_VENTILATE
    assert (
        recommend(replace(dry_again, minutes_since_change=10), SETTINGS).state
        == State.VENTILATE_NOW
    )


def test_useful_cooling_remains_possible_during_drying_pause() -> None:
    result = recommend(
        replace(
            BEDROOM, humidity=62, minutes_since_airing=1, heating_active=False, temp=24, target=21
        ),
        SETTINGS,
    )
    assert result.state == State.VENTILATION_USEFUL and result.reason == Reason.COOLING
