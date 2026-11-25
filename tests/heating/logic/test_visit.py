"""Floor pulses of a visit in the per area controller."""

from custom_components.house_assistant.heating.logic.controller import (
    AreaRuntime,
    AreaSettings,
    AreaStatus,
    ControlInput,
    ControlParams,
    LearnedValues,
    floor_pulse,
    step,
)

PARAMS = ControlParams()
SETTINGS = AreaSettings(min_on_s=300, min_off_s=300)
# a warm room: the thermostat alone would never switch on
LEARNED = LearnedValues(cool_rate_kph=0.1, dead_time_s=3600, overshoot_k=0.3)
NOW = 100_000.0


def _input(**kwargs) -> ControlInput:
    base = {
        "now": NOW,
        "temp": 22.1,
        "target": 22.0,
        "hvac_on": True,
        "season_active": True,
        "heating_day": True,
        "frost_temp": 7.0,
        "window_open": False,
        "switch_on": False,
        "last_switch_change": NOW - 7200,
        "visit": True,
        "floor_minutes": 15.0,
        "floor_cap": 22.5,
    }
    base.update(kwargs)
    return ControlInput(**base)


def test_pulse_starts_when_off_long_enough() -> None:
    assert floor_pulse(_input())
    assert floor_pulse(_input(last_switch_change=NOW - 45 * 60))
    assert not floor_pulse(_input(last_switch_change=NOW - 44 * 60))
    assert floor_pulse(_input(last_switch_change=None))


def test_pulse_runs_its_minutes() -> None:
    assert floor_pulse(_input(switch_on=True, last_switch_change=NOW - 14 * 60))
    assert not floor_pulse(_input(switch_on=True, last_switch_change=NOW - 15 * 60))


def test_no_pulse_without_visit_minutes_or_too_warm() -> None:
    assert not floor_pulse(_input(visit=False))
    assert not floor_pulse(_input(floor_minutes=0))  # night or switched off
    assert not floor_pulse(_input(temp=22.6))
    assert floor_pulse(_input(temp=22.5))
    assert not floor_pulse(_input(temp=None))


def test_step_pulse_status_and_idle_visit() -> None:
    rt = AreaRuntime()
    decision = step(_input(), PARAMS, SETTINGS, LEARNED, rt)
    assert decision.want_on
    assert decision.status == AreaStatus.VISIT_FLOOR

    decision = step(_input(last_switch_change=NOW - 600), PARAMS, SETTINGS, LEARNED, rt)
    assert not decision.want_on
    assert decision.status == AreaStatus.VISIT


def test_thermostat_demand_wins_over_the_pulse_status() -> None:
    decision = step(_input(temp=20.5), PARAMS, SETTINGS, LEARNED, AreaRuntime())
    assert decision.want_on
    assert decision.status == AreaStatus.HEATING


def test_pulses_over_hours_give_fifteen_minutes_per_hour() -> None:
    """Simulate the switch following the decision: 15 min on, 45 min off."""
    rt = AreaRuntime()
    switch_on, changed, on_minutes = False, NOW - 7200, 0
    for minute in range(180):
        now = NOW + minute * 60
        data = _input(now=now, switch_on=switch_on, last_switch_change=changed)
        decision = step(data, PARAMS, SETTINGS, LEARNED, rt)
        if decision.may_switch and decision.want_on != switch_on:
            switch_on, changed = decision.want_on, now
        on_minutes += switch_on
    assert on_minutes == 45


def test_pulse_never_overrides_protection() -> None:
    cases = (
        ({"hvac_on": False}, AreaStatus.OFF),
        ({"season_active": False}, AreaStatus.OUT_OF_SEASON),
        ({"temp": None}, AreaStatus.SENSOR_ERROR),
    )
    for changes, status in cases:
        decision = step(_input(**changes), PARAMS, SETTINGS, LEARNED, AreaRuntime())
        assert not decision.want_on
        assert decision.status == status
    # an open window holds a circuit that is off
    decision = step(_input(window_open=True), PARAMS, SETTINGS, LEARNED, AreaRuntime())
    assert not decision.want_on
    assert decision.status == AreaStatus.WINDOW_OPEN
    # airing long enough pauses, the recovery after it as well
    rt = AreaRuntime()
    params = ControlParams(window_delay_min=5)
    for minute in range(6):
        step(_input(now=NOW + minute * 60, window_open=True), params, SETTINGS, LEARNED, rt)
    assert rt.window_paused
    decision = step(_input(now=NOW + 420), params, SETTINGS, LEARNED, rt)
    assert not decision.want_on
    assert decision.status == AreaStatus.RECOVERY


def test_frost_protection_stays() -> None:
    decision = step(_input(temp=5.0, hvac_on=False), PARAMS, SETTINGS, LEARNED, AreaRuntime())
    assert decision.want_on
    assert decision.status == AreaStatus.FROST_PROTECTION


def test_no_heating_day_without_the_visit_flag() -> None:
    # the coordinator passes heating_day for a warm floor; without it nothing runs
    decision = step(_input(heating_day=False), PARAMS, SETTINGS, LEARNED, AreaRuntime())
    assert not decision.want_on
    assert decision.status == AreaStatus.NO_HEATING_DAY


def test_visit_days_are_no_rule_errors() -> None:
    from custom_components.house_assistant.heating.logic import heating_day as hd

    day = {"final": True, "source": "rule", "rule": True, "ai": None, "err_rule": "B"}
    history = [
        hd.DayRecord(date="2026-11-20", **day),
        hd.DayRecord(date="2026-11-21", visit=True, **day),
    ]
    assert hd.rule_errors(history, 7) == 1
    # stored and loaded again
    assert hd.DayRecord.from_dict(history[1].as_dict()).visit
