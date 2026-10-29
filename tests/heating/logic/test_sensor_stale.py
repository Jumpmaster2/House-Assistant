"""Threshold decision for unchanged room temperatures."""

import pytest

from custom_components.house_assistant.heating.logic.sensor_stale import sensor_is_stale


@pytest.mark.parametrize(
    ("age", "hours", "valid", "expected"),
    [
        (3599.9, 1, True, False),
        (3600, 1, True, True),
        (3601, 1, True, True),
        (100000, 0, True, False),
        (100000, 1, False, False),
        (-1, 1, True, False),
    ],
)
def test_sensor_stale(age, hours, valid, expected):
    assert sensor_is_stale(age, hours, valid) is expected
