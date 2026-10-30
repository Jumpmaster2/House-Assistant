"""Incidental pipe heat, corrected learning and protected controller paths."""

import hashlib
import json
import math
from dataclasses import replace
from unittest.mock import patch

import pytest

from custom_components.house_assistant.heating.logic.ai_schema import (
    CHECK_SCHEMA,
    default_limits,
    validate_check,
)
from custom_components.house_assistant.heating.logic.controller import (
    AreaRuntime,
    AreaSettings,
    AreaStatus,
    ControlInput,
    ControlParams,
    LearnedValues,
    step,
    thermostat,
)
from custom_components.house_assistant.heating.logic.learning import (
    PIPE_SETTLE_S,
    TRACK_TIMEOUT,
    AreaLearner,
    Sample,
    ThermalModel,
)
from custom_components.house_assistant.heating.logic.pipe_heat import (
    clean_pipe_sources,
    clean_pipe_weights,
    pipe_rate,
)
from custom_components.house_assistant.heating.logic.prompts import check_messages, nightly_messages


def test_sources_and_gain_bounds():
    assert clean_pipe_sources(["self", "deleted", "a", "a", "b"], ["a", "b"]) == ["a", "b"]
    assert pipe_rate(0.15, 1, []) == 0
    assert pipe_rate(0.15, 1, [False, False]) == 0
    assert pipe_rate(0.15, 1, [True, False]) == 0.15
    assert pipe_rate(0.15, 2, [True, True]) == 0.6
    assert pipe_rate(0.15, 1, [1.0, 2.0, 3.0]) == pytest.approx(0.9)
    assert pipe_rate(1, 2, [3.0, 3.0]) == 12
    assert pipe_rate(5, 9, [True]) == 2
    assert pipe_rate(-1, 1, [True]) == 0
    assert pipe_rate(1, -1, [True]) == 0


def test_model_prediction_adds_pipe_heat_without_changing_base():
    model = ThermalModel()
    previous = model.a - model.k * 10 + model.s * 2 * 1.2
    assert model.predict(1, 10, 2, 1.2) == previous
    assert model.predict(1, 10, 2, 1.2, pipe_rate(0.2, 1.5, [True])) == previous + 0.3


def _input(**kwargs):
    return replace(ControlInput(100_000, 20.8, 21, True, True, True, 7, False, False, 0), **kwargs)


def test_target_waits_and_switches_off_earlier_with_source():
    learned = LearnedValues(cool_rate_kph=0.1, dead_time_s=3600, overshoot_k=0.1)
    pipe = replace(learned, pipe_rate_kph=0.3)
    params = ControlParams()
    assert thermostat(_input(), params, learned)[0]
    assert not thermostat(_input(), params, pipe)[0]
    assert thermostat(_input(switch_on=True), params, learned)[0]
    assert not thermostat(_input(switch_on=True), params, pipe)[0]
    # Severe cold still forces heating, independent of any incidental gain.
    assert thermostat(_input(temp=19), params, pipe)[0]


@pytest.mark.parametrize("pipe", [0.0, 2.0])
def test_protected_paths_keep_their_behavior(pipe):
    learned = LearnedValues(pipe_rate_kph=pipe)
    params, settings = ControlParams(), AreaSettings(emergency_duration_s=60)
    assert (
        step(_input(temp=6), params, settings, learned, AreaRuntime()).status
        == AreaStatus.FROST_PROTECTION
    )
    rt = AreaRuntime(window_open_since=99_000, window_paused=True)
    assert (
        step(_input(window_open=True), params, settings, learned, rt).status
        == AreaStatus.WINDOW_OPEN
    )
    rt = AreaRuntime(recovery_until=101_000)
    assert step(_input(), params, settings, learned, rt).status == AreaStatus.RECOVERY
    rt = AreaRuntime(below_emergency_since=99_000)
    assert (
        step(_input(temp=19, heating_day=False), params, settings, learned, rt).status
        == AreaStatus.EMERGENCY
    )


def _rate_window(rate, pipe):
    learner = AreaLearner()
    for minute in range(61):
        learner.add_sample(
            Sample(
                minute * 60,
                20 + rate * minute / 60,
                True,
                5,
                0,
                False,
                pipe_active=True,
                pipe_rate_kph=pipe(minute),
            )
        )
    return learner


def test_model_subtracts_mean_scaled_pipe_gain():
    # The gain varies (e.g. source weights / AI factor change); use every sample,
    # not just the final or initial gain. Mean correction = 0.15 K/h.
    with patch.object(ThermalModel, "update", return_value=True) as update:
        _rate_window(0.8, lambda minute: 0.1 + minute / 600)
    assert update.call_count == 1
    assert update.call_args.args[-1] == pytest.approx(0.65)


@pytest.mark.parametrize(
    ("observed", "pipe", "accepted"),
    [
        (0.4, 0.25, False),
        (0.4, 0.19, True),
        (-0.4, 0.19, True),
        (-0.4, 0.25, False),
        (0, 0.01, False),
    ],
)
def test_model_skips_dominant_correction_in_warming_and_cooling(observed, pipe, accepted):
    learner = _rate_window(observed, lambda minute: pipe)
    assert bool(learner.model.n_heat) == accepted


class _FourHourBlockedLearner(AreaLearner):
    """The former pipe quarantine for comparison with the corrected learner."""

    def _update_model(self, now):
        if self.pipe_last_on is not None and now - self.pipe_last_on <= TRACK_TIMEOUT:
            return False
        return super()._update_model(now)


def test_cycling_sources_still_allow_all_three_coefficients_to_converge():
    corrected, blocked = AreaLearner(), _FourHourBlockedLearner()
    for learner in (corrected, blocked):
        learner.dead_time.value = 0  # this synthetic room has no transport delay
    true_a, true_k, true_s = 1.2, 0.02, 0.4
    temp = 20.0
    # Three weighted circuits cycle every four hours, with staggered on/off edges.
    # Own heating, weather and sun vary independently of these source cycles.
    for minute in range(14 * 24 * 60):
        valve = minute % 310 < 150
        diff = 12 + 6 * math.sin(minute * 2 * math.pi / 1440)
        pv = 1.5 * max(0, math.sin((minute % 1440 - 360) * 2 * math.pi / 1440))
        sources = [0 <= minute % 240 - offset < 90 for offset in (0, 20, 40)]
        pipe = pipe_rate(0.15, 1, (w * on for w, on in zip((1, 0.5, 1.5), sources, strict=True)))
        for learner in (corrected, blocked):
            learner.add_sample(
                Sample(
                    minute * 60,
                    temp,
                    valve,
                    temp - diff,
                    pv,
                    False,
                    pipe_active=any(sources),
                    pipe_rate_kph=pipe,
                )
            )
        temp += (true_a * valve - true_k * diff + true_s * pv + pipe) / 60
    assert corrected.model.n_heat > 100
    assert corrected.model.n_cool > 30
    assert blocked.model.n_heat == blocked.model.n_cool == 0
    for fitted, frozen, truth, tolerance in zip(
        corrected.model.theta,
        blocked.model.theta,
        (true_a, true_k, true_s),
        (0.08, 0.005, 0.05),
        strict=True,
    ):
        assert abs(fitted - truth) < abs(frozen - truth)
        assert fitted == pytest.approx(truth, abs=tolerance)


def test_model_rejects_residual_heat_anywhere_in_rate_window():
    learner = AreaLearner()
    for minute in range(181):
        # At 30 min the source stops. Its 20 min tail must still disqualify
        # the window ending at 105 min, even though it has long been off now.
        learner.add_sample(
            Sample(
                minute * 60,
                20 + minute / 60,
                True,
                5,
                0,
                False,
                pipe_active=minute <= 30,
                pipe_rate_kph=0.1 if minute <= 30 else 0,
            )
        )
        if minute == 105:
            assert learner.model.n_heat == 0
        if minute == 120:
            assert learner.model.n_heat == 1
    assert learner.model.n_heat > 1  # no four-hour quarantine


def test_explicitly_disabled_pipe_samples_are_identical():
    old, new = AreaLearner(), AreaLearner()
    for minute in range(240):
        sample = Sample(minute * 60, 20 - minute / 1000, False, 5, 0, False)
        old.add_sample(sample)
        new.add_sample(replace(sample, pipe_active=False, pipe_rate_kph=0.0))
    assert old.as_dict() == new.as_dict()
    assert old.model.n_cool > 0
    # Snapshot produced with the committed learner before the correction:
    snapshot = json.dumps(old.as_dict(), sort_keys=True).encode()
    assert (
        hashlib.sha256(snapshot).hexdigest()
        == "26fc17dcadc35482380f032ea0ffb1bb3926cdf0f06b104e8aa2c01441347386"
    )


@pytest.mark.parametrize(
    ("old", "wanted", "expected"), [(1, 9, 1.2), (1, -3, 0.8), (1.9, 9, 2), (0.1, -9, 0)]
)
def test_ai_clamps_pipe_factor(old, wanted, expected):
    data = {
        "adjustments": [
            {"area": "a1", "parameter": "pipe_factor", "value": wanted, "reason": "pipes"}
        ],
        "confidence": 80,
    }
    result = validate_check(data, {"a1": {"pipe_factor": old}}, default_limits())
    assert result.applied[0].new == expected
    assert result.applied[0].clamped
    rejected = validate_check(data, {"a1": {"sun_factor": 1}}, default_limits())
    assert rejected.rejected and not rejected.applied
    enum = CHECK_SCHEMA["properties"]["adjustments"]["items"]["properties"]["parameter"]["enum"]
    assert "pipe_factor" in enum


@pytest.mark.parametrize("language", ["de", "en"])
def test_prompts_explain_pipes_and_keep_custom_blocks(language):
    system, _ = check_messages(
        {}, language, {"check": {"custom": [{"text": "Keep my instruction."}]}}
    )
    assert "Keep my instruction." in system
    assert "pipe_on_min" in system and "sun_over_kh" in system
    assert "lower pipe_factor" in system and "raise pipe_factor" in system
    nightly, _ = nightly_messages({}, language)
    assert "pipe_sources" in nightly and "puffer" in nightly


def test_emergency_thermostat_and_carried_peak_exclude_pipe_heat():
    params = ControlParams()
    learned = LearnedValues(cool_rate_kph=0.1, dead_time_s=3600, overshoot_k=0.1)
    pipe = replace(learned, pipe_rate_kph=2.0)
    emergency = _input(heating_day=False, temp=20.7)
    settings = AreaSettings()
    before = step(emergency, params, settings, learned, AreaRuntime(emergency_active=True))
    after = step(emergency, params, settings, pipe, AreaRuntime(emergency_active=True))
    assert before == after and after.want_on
    rt = AreaRuntime()
    step(_input(switch_on=True), params, settings, pipe, rt)
    assert rt.last_peak == 20.9  # only own overshoot, not the source's 2 K/h


def test_switch_event_cannot_learn_before_the_next_active_sample():
    learner = AreaLearner()
    learner.track_off = {"start": 0, "t_off": 20, "max": 21, "run_h": 1}
    learner.on_switch(3600, 20.8, True, 0, pipe_active=True)
    assert learner.overshoot.count == 0
    assert learner.track_on is learner.track_off is None


def test_source_weights_defaults_cleanup_and_fractional_lengths():
    assert clean_pipe_weights(None, ["pia", "bad", "sam"]) == {"pia": 1.0, "bad": 1.0, "sam": 1.0}
    assert clean_pipe_weights({"pia": 0.1, "bad": 3, "deleted": 5}, ["pia", "bad"]) == {
        "pia": 0.1,
        "bad": 3.0,
    }
    weights = clean_pipe_weights({"pia": 0.5, "bad": 2, "sam": 1.5}, ["pia", "bad", "sam"])
    assert pipe_rate(0.15, 1.2, [weights["pia"], weights["bad"], 0]) == pytest.approx(0.45)


@pytest.mark.parametrize("value", [0, -1, 3.1, 0.15, float("nan"), float("inf"), True, None, "no"])
def test_source_weight_validation(value):
    with pytest.raises((TypeError, ValueError, OverflowError)):
        clean_pipe_weights({"pia": value}, ["pia"], strict=True)
    assert clean_pipe_weights({"pia": value}, ["pia"]) == {"pia": 1.0}


@pytest.mark.parametrize("turned_on", [False, True], ids=["overshoot", "dead_time"])
@pytest.mark.parametrize(
    ("source_minute", "learned"),
    [(-21, True), (-20, True), (-19, False), (10, False), (60, True)],
    ids=["before-settling", "settled", "recent", "during", "after"],
)
def test_only_source_activity_near_or_during_event_discards_it(turned_on, source_minute, learned):
    learner = AreaLearner()
    if source_minute < 0:
        learner.add_sample(Sample(source_minute * 60, 20, False, 5, 0, False, pipe_active=True))
    learner.on_switch(0, 20, turned_on, 1)
    for minute in range(41):
        if turned_on:
            temp = 20 if minute < 20 else 20.1 if minute < 25 else 20.2
        else:
            temp = 20 + min(minute, 20) * 0.02 - max(0, minute - 20) * 0.02
        # Missing temperature and exclusion must not hide a source inside an event.
        missing = minute == source_minute
        learner.add_sample(
            Sample(
                minute * 60,
                None if missing else temp,
                turned_on,
                5,
                0,
                missing,
                pipe_active=missing,
                pipe_rate_kph=0.15 if missing else 0,
            )
        )
    if source_minute > 40:
        learner.add_sample(Sample(source_minute * 60, 20, turned_on, 5, 0, False, pipe_active=True))
    assert learner.dead_time.count == (int(learned) if turned_on else 0)
    assert learner.overshoot.count == (0 if turned_on else int(learned))
    assert learner.overshoot_rate.count == learner.overshoot.count


def test_next_clean_event_can_start_after_twenty_minutes():
    learner = AreaLearner()
    learner.add_sample(Sample(0, 20, False, 5, 0, False, pipe_active=True))
    learner.on_switch(PIPE_SETTLE_S - 1, 20, True, 0)
    assert learner.track_on is None
    learner.on_switch(PIPE_SETTLE_S, 20, True, 0)
    for minute in range(31):
        learner.add_sample(
            Sample(
                PIPE_SETTLE_S + minute * 60,
                20 if minute < 20 else 20.2,
                True,
                5,
                0,
                False,
            )
        )
    assert learner.dead_time.count == 1


@pytest.mark.parametrize("turned_on", [False, True], ids=["overshoot", "dead_time"])
def test_switch_cannot_finish_event_during_settling(turned_on):
    learner = AreaLearner()
    learner.pipe_last_on = 0
    if turned_on:
        learner.track_off = {"start": -3600, "t_off": 20, "max": 21, "run_h": 1}
    else:
        learner.track_on = {"start": -3600, "min": 20, "rise": -600}
    learner.on_switch(PIPE_SETTLE_S - 1, 20.8, turned_on, 1)
    assert learner.track_off is learner.track_on is None
    assert learner.dead_time.count == learner.overshoot.count == 0
