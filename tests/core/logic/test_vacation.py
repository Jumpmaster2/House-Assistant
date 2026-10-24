"""Time rules of the vacation of the house."""

from datetime import UTC, datetime, timedelta

from custom_components.house_assistant.core.logic.vacation import (
    ERROR_DEPARTURE_AFTER_RETURN,
    ERROR_RETURN_PAST,
    SOURCE_SWITCH,
    Times,
    active,
    check,
    due,
    next_change,
    planned,
    switched,
)

NOW = datetime(2026, 11, 20, 12, 0, tzinfo=UTC)
H = timedelta(hours=1)


def test_departure_and_return() -> None:
    times = planned(Times(), NOW + H, NOW + 48 * H, NOW)
    # a departure ahead: off until then
    assert times == Times(False, NOW + H, NOW + 48 * H)
    assert next_change(times) == NOW + H
    times = due(times, NOW + H)
    assert times == Times(True, None, NOW + 48 * H)
    assert next_change(times) == NOW + 48 * H
    # at the return off, nothing planned any more
    assert due(times, NOW + 48 * H) == Times()
    assert next_change(Times()) is None


def test_only_a_return_means_vacation_from_now_on() -> None:
    assert planned(Times(), None, NOW + 24 * H, NOW) == Times(True, None, NOW + 24 * H)
    # the return first, then the departure: the vacation starts at the departure
    times = planned(Times(True, None, NOW + 24 * H), NOW + 2 * H, NOW + 24 * H, NOW)
    assert times == Times(False, NOW + 2 * H, NOW + 24 * H)


def test_missed_times_while_home_assistant_was_down() -> None:
    # both passed: nothing left of the vacation
    assert due(Times(False, NOW - 48 * H, NOW - H), NOW) == Times()
    # the departure passed: vacation now
    assert due(Times(False, NOW - H, NOW + H), NOW) == Times(True, None, NOW + H)


def test_switching_by_hand() -> None:
    # off ends the running vacation, its return goes with it
    assert switched(Times(True, None, NOW + H), False, NOW) == Times()
    # a departure ahead stays planned
    planned_times = Times(True, NOW + H, NOW + 2 * H)
    assert switched(planned_times, False, NOW) == Times(False, NOW + H, NOW + 2 * H)
    # on without times stays on until switched off
    assert switched(Times(), True, NOW) == Times(True)


def test_check() -> None:
    assert check(None, NOW + H, NOW) is None
    assert check(NOW + H, NOW + 2 * H, NOW) is None
    assert check(NOW + 2 * H, NOW + H, NOW) == ERROR_DEPARTURE_AFTER_RETURN
    assert check(None, NOW - H, NOW) == ERROR_RETURN_PAST


def test_active_and_its_source() -> None:
    assert active(True, [("input_boolean.away", "on")]) == (True, SOURCE_SWITCH)
    assert active(False, [("calendar.trips", "off"), ("input_boolean.away", "on")]) == (
        True,
        "input_boolean.away",
    )
    assert active(False, [("input_boolean.away", "unavailable")]) == (False, None)
