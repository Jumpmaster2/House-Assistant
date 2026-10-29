"""Usable stored AI limits survive strict validation of new settings."""

from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from custom_components.house_assistant.heating.config_flow import (
    HeatingOptionsSteps,
    _limits_schema,
    _validate_limits,
)
from custom_components.house_assistant.heating.coordinator import HeatingCoordinator
from custom_components.house_assistant.heating.logic.ai_schema import (
    default_limits,
    normalize_limits,
    validate_check,
    validate_limit,
)
from custom_components.house_assistant.heating.validation import normalize_options
from custom_components.house_assistant.heating.websocket import PanelError, _limits

LEGACY = {
    "window_delay_min": {"min": 1, "max": 30, "step": 2},
    "recovery_bias_min": {"min": -30, "max": 90, "step": 10},
}


def stored_limits():
    return {**default_limits(), **deepcopy(LEGACY)}


def test_usable_legacy_limits_unchanged():
    stored = stored_limits()
    before = deepcopy(stored)
    normalized = normalize_limits(stored)
    assert normalized == before == stored
    for key, item in LEGACY.items():
        for field in item:
            assert normalized[key][field] is stored[key][field]
    options = {"limits": stored}
    result = normalize_options(options)
    assert result == options
    assert result["limits"] is stored
    assert normalize_options(result) == result
    coordinator = SimpleNamespace(opt=lambda key: stored)
    assert HeatingCoordinator.limits.fget(coordinator) == stored


@pytest.mark.parametrize(
    "item,expected",
    [
        (None, {"min": 1, "max": 15, "step": 2}),
        ({}, {"min": 1, "max": 15, "step": 2}),
        (
            {"min": float("nan"), "max": float("inf"), "step": "bad"},
            {"min": 1, "max": 15, "step": 2},
        ),
        ({"min": 20, "max": 10, "step": -1}, {"min": 20, "max": 20, "step": 2}),
        ({"min": -100, "max": 100, "step": 99}, {"min": -100, "max": 100, "step": 99}),
        ({"min": 1, "max": 30, "step": 0}, {"min": 1, "max": 30, "step": 0}),
    ],
)
def test_lenient_repair_only_unusable_values(item, expected):
    limits = normalize_limits({"window_delay_min": item})
    assert limits["window_delay_min"] == expected
    assert normalize_limits(limits) == limits
    assert normalize_options({"limits": limits}) == {"limits": limits}


@pytest.mark.parametrize("old,wanted,expected", [(10, 14, 12), (29, 40, 30), (20, 24, 22)])
def test_ai_respects_legacy_range_and_step(old, wanted, expected):
    result = validate_check(
        {
            "adjustments": [{"area": "room", "parameter": "window_delay_min", "value": wanted}],
            "confidence": 90,
        },
        {"room": {"window_delay_min": old}},
        stored_limits(),
    )
    assert not result.rejected
    assert result.applied[0].new == expected


@pytest.mark.parametrize("old", [10, 40])
def test_zero_step_freezes_even_outside_limits(old):
    limits = stored_limits()
    limits["window_delay_min"]["step"] = 0
    result = validate_check(
        {
            "adjustments": [{"area": "room", "parameter": "window_delay_min", "value": 20}],
            "confidence": 90,
        },
        {"room": {"window_delay_min": old}},
        limits,
    )
    assert not result.applied
    assert not result.rejected


@pytest.mark.parametrize("key", list(LEGACY))
@pytest.mark.parametrize(
    "change,error",
    [
        ({}, None),
        ({"max": 1000}, "invalid_value"),
        ({"step": -1}, "invalid_value"),
        ({"step": 100}, "invalid_value"),
        ({"step": float("nan")}, "invalid_value"),
        ({"min": 100}, "min_above_max"),
    ],
)
def test_dialog_panel_legacy_same_result(key, change, error):
    current = stored_limits()
    item = {**current[key], **change}
    submitted = {**current, key: item}
    validated, errors = _validate_limits(submitted, current)
    if error:
        assert errors == {key: error}
        with pytest.raises(PanelError, match=error):
            _limits({key: item}, current)
    else:
        assert not errors
        assert validated == _limits({key: item}, current) == current
        assert validate_limit(key, item, current[key]) == item
    with pytest.raises(ValueError):
        validate_limit(key, item)


@pytest.mark.parametrize(
    "step,error", [(0, None), (2, None), (14, None), (-1, "invalid_value"), (15, "invalid_value")]
)
def test_editing_legacy_parameter_requires_strict_range(step, error):
    current = stored_limits()
    item = {"min": 1, "max": 15, "step": step}
    submitted = {**current, "window_delay_min": item}
    validated, errors = _validate_limits(submitted, current)
    if error:
        assert errors == {"window_delay_min": error}
        with pytest.raises(PanelError, match=error):
            _limits({"window_delay_min": item}, current)
    else:
        assert not errors
        assert validated == _limits({"window_delay_min": item}, current)
        assert validated["window_delay_min"] == item
        assert validated["recovery_bias_min"] == current["recovery_bias_min"]


async def test_dialog_passes_saved_limits_to_validator():
    current = stored_limits()
    flow = SimpleNamespace(
        _heating_values={"limits": current}, _heating_save=Mock(), _heating_form=Mock()
    )
    await HeatingOptionsSteps.async_step_heating_ai_limits(flow, current)
    flow._heating_save.assert_called_once_with({"limits": current})
    flow._heating_form.assert_not_called()


def test_dialog_selectors_allow_unchanged_extreme_legacy_values():
    current = stored_limits()
    current["window_delay_min"] = {"min": -1000000, "max": 1000000, "step": 1000000}
    schema = _limits_schema({"limits": current})
    for marker, section in schema.schema.items():
        key = str(marker)
        assert section.schema(current[key]) == current[key]
    assert not _validate_limits(current, current)[1]
