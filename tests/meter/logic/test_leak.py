"""Warning of a meter on vacation."""

from custom_components.house_assistant.meter.logic.leak import CASE_AMOUNT, CASE_RATE, leak_cases
from custom_components.house_assistant.meter.logic.units import amount_unit


def test_amount_and_rate() -> None:
    assert leak_cases(10, 5, 20, 5) == []
    assert leak_cases(25, 10, 20, 5) == [CASE_AMOUNT]
    # 12 L in 2 h: 6 L/h above the 5 L/h, below the amount
    assert leak_cases(12, 2, 20, 5) == [CASE_RATE]
    # the mean needs an hour
    assert leak_cases(3, 0.5, 20, 5) == []
    # a limit of 0 is off
    assert leak_cases(1000, 10, 0, 0) == []


def test_amount_units() -> None:
    assert amount_unit("m³") == ("L", 1000.0)
    assert amount_unit("L") == ("L", 1.0)
    assert amount_unit("MWh") == ("kWh", 1000.0)
    assert amount_unit("pulses") == ("pulses", 1.0)
