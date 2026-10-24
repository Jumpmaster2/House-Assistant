"""Warning on vacation: something runs while nobody is at home (pure, without HA).

Counted from the last valid reading before the vacation started: the amount used since
then and the mean flow (or power) over that time. The mean needs at least an hour,
a single reading shortly after the start says nothing about it.
"""

from __future__ import annotations

CASE_AMOUNT = "amount"
CASE_RATE = "rate"
MIN_HOURS = 1.0


def leak_cases(used: float, hours: float, amount_limit: float, rate_limit: float) -> list[str]:
    """Cases above their limit (a limit of 0 is off). ``used`` in L or kWh, the rate in
    L/h or kW."""
    cases: list[str] = []
    if amount_limit > 0 and used > amount_limit:
        cases.append(CASE_AMOUNT)
    if rate_limit > 0 and hours >= MIN_HOURS and used / hours > rate_limit:
        cases.append(CASE_RATE)
    return cases
