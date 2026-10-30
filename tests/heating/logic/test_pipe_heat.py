"""Incidental pipe heat, isolated learning and protected controller paths."""

from dataclasses import replace

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


def test_pipe_samples_do_not_teach_other_coefficients_or_events():
    learner = AreaLearner()
    original = learner.model.as_dict()
    learner.on_switch(0, 20, True, 0)
    for minute in range(181):
        learner.add_sample(
            Sample(minute * 60, 20 + minute / 600, False, 5, 0, False, pipe_active=True)
        )
    assert learner.model.as_dict() == original
    assert learner.dead_time.count == learner.overshoot.count == 0
    assert learner.track_on is learner.track_off is None
    # Residual warmth remains excluded for four hours after the last active sample.
    for minute in range(181, 420):
        learner.add_sample(Sample(minute * 60, 20, False, 5, 0, False))
    assert learner.model.as_dict() == original
    for minute in range(420, 451):
        learner.add_sample(Sample(minute * 60, 20, False, 5, 0, False))
    assert learner.model.n_cool > 0


def test_explicitly_disabled_pipe_samples_are_identical():
    old, new = AreaLearner(), AreaLearner()
    for minute in range(240):
        sample = Sample(minute * 60, 20 - minute / 1000, False, 5, 0, False)
        old.add_sample(sample)
        new.add_sample(replace(sample, pipe_active=False))
    assert old.as_dict() == new.as_dict()
    assert old.model.n_cool > 0


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
