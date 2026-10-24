"""Time rules of the vacation of the house (pure, without Home Assistant).

The own vacation is a switch with an optional departure and return:
* at the departure the switch goes on, at the return off; both times are cleared then
  (also when Home Assistant was not running at that moment); a departure ahead keeps the
  switch off until then;
* with only a return the vacation applies from now on until the return;
* switching off by hand ends the vacation: a return without a departure goes with it,
  a departure still ahead stays planned;
* a departure after the return is refused, a return in the past is ignored.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

SOURCE_SWITCH = "switch"
ERROR_DEPARTURE_AFTER_RETURN = "departure_after_return"
ERROR_RETURN_PAST = "return_in_past"


@dataclass(frozen=True, slots=True)
class Times:
    """The switch and the planned times of the own vacation."""

    on: bool = False
    departure: datetime | None = None
    return_at: datetime | None = None


def check(departure: datetime | None, return_at: datetime | None, now: datetime) -> str | None:
    """Error of new times, None when they are fine."""
    if return_at is not None and return_at <= now:
        return ERROR_RETURN_PAST
    if departure is not None and return_at is not None and departure >= return_at:
        return ERROR_DEPARTURE_AFTER_RETURN
    return None


def due(times: Times, now: datetime) -> Times:
    """The times with what is due applied."""
    on, departure, return_at = times.on, times.departure, times.return_at
    if return_at is not None and return_at <= now:
        return Times()
    if departure is not None and departure <= now:
        on, departure = True, None
    if return_at is not None and departure is None:
        on = True
    return Times(on, departure, return_at)


def switched(times: Times, on: bool, now: datetime) -> Times:
    """The switch set by hand."""
    if on:
        return due(Times(True, times.departure, times.return_at), now)
    departure = times.departure if times.departure is not None and times.departure > now else None
    return Times(False, departure, times.return_at if departure is not None else None)


def planned(
    times: Times, departure: datetime | None, return_at: datetime | None, now: datetime
) -> Times:
    """New times (checked with ``check`` before); the switch follows them: a departure
    ahead means the vacation starts then."""
    if departure is not None and departure > now:
        return Times(False, departure, return_at)
    return due(Times(times.on, departure, return_at), now)


def next_change(times: Times) -> datetime | None:
    """When ``due`` changes something next."""
    found = [t for t in (times.departure, times.return_at) if t is not None]
    return min(found) if found else None


def active(on: bool, sources: Iterable[tuple[str, str | None]]) -> tuple[bool, str | None]:
    """Is it vacation, and why: the own switch, else the first external source that is
    on (an input_boolean, a calendar with an event, ...)."""
    if on:
        return True, SOURCE_SWITCH
    for entity_id, state in sources:
        if state == "on":
            return True, entity_id
    return False, None
