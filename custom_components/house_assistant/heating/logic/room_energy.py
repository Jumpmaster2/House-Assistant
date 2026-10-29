"""Heat consumption per room: the heat meter split over the rooms (pure logic).

The heat meter covers the whole house. A heating phase is the time between two
readings that changed. Every room that switched on in a phase takes a share of the
kWh read, in proportion to ``c_i * x_i``, where ``x_i`` is its floor area times the
run time times the heating demand (target minus outdoor temperature) of the phase.
The shares add up to the reading; what no room heated is counted as not assigned.
A phase can reach over several days (a short phase waits for the next one). The run
time is kept per day, and each share is booked on the days the room ran, in proportion
to its demand hours of that day, so the kWh of an earlier day do not land on today.

``c_i`` is the heat per m² and K at continuous operation (kW/(m²K)). It is learned
from the phases by a least squares fit with forgetting, pulled towards the house-wide
mean and kept non-negative. A phase in which one room alone heated identifies its
``c_i`` directly. Readings have a resolution of 1 kWh, so a phase is only closed once
it has some run time and the meter changed; shorter phases are merged with the next.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from ...core.store_validation import checked, dataclass_schema, number, optional

FLOOR_AREA_BOUNDS = (1.0, 200.0)  # m², as offered in the form
DEFAULT_COEFFICIENT = 0.0025  # kW/(m²K): about 1 kW for 20 m² at a demand of 20 K
COEFFICIENT_BOUNDS = (0.0, 0.05)
FORGETTING = 0.99  # per closed phase: about 100 phases of memory
RIDGE = 0.01  # pull towards the house-wide mean, relative to the size of the data
MIN_RUN_H = 0.25  # h of run time (all rooms) a phase needs before it is closed
MIN_CONFIDENCE_PHASES = 30  # phases for full confidence of a room
SOLVER_STEPS = 200  # sweeps of the coordinate descent (a few rooms, converges fast)
EPS = 1e-9


@dataclass(slots=True)
class Counter:
    """kWh of one room (or of the not assigned part): total, today and this month."""

    total: float = 0.0
    day: str = ""
    day_kwh: float = 0.0
    day_hours: float = 0.0  # run time today
    month: str = ""
    month_kwh: float = 0.0

    def roll(self, day: str, month: str) -> None:
        """Start the day and the month that ``day`` and ``month`` name, if they changed."""
        if self.day != day:
            self.day, self.day_kwh, self.day_hours = day, 0.0, 0.0
        if self.month != month:
            self.month, self.month_kwh = month, 0.0

    def add(self, kwh: float, day: str | None = None, month: str | None = None) -> None:
        """Add kWh; ``day`` and ``month`` name the period they belong to (None: the current
        one). An earlier period only changes the total."""
        self.total += kwh
        if day is None or day == self.day:
            self.day_kwh += kwh
        if month is None or month == self.month:
            self.month_kwh += kwh

    def as_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "day": self.day,
            "day_kwh": self.day_kwh,
            "day_hours": self.day_hours,
            "month": self.month,
            "month_kwh": self.month_kwh,
        }

    @classmethod
    def from_dict(cls, data: Any) -> Counter:
        data = checked(data, dataclass_schema(cls))
        counter = cls()
        if not isinstance(data, dict):
            return counter
        counter.total = _float(data.get("total"))
        counter.day = str(data.get("day") or "")
        counter.day_kwh = _float(data.get("day_kwh"))
        counter.day_hours = _float(data.get("day_hours"))
        counter.month = str(data.get("month") or "")
        counter.month_kwh = _float(data.get("month_kwh"))
        return counter


@dataclass(slots=True)
class Run:
    """Run time of a room in the open phase."""

    hours: float = 0.0
    kh: float = 0.0  # run time times the heating demand (K h)
    days: dict[str, float] = field(default_factory=dict)  # day -> K h of that day

    def add(self, day: str, hours: float, kh: float) -> None:
        self.hours += hours
        if kh > 0:
            self.kh += kh
            self.days[day] = self.days.get(day, 0.0) + kh

    def by_day(self, fallback: str) -> dict[str, float]:
        """K h per day. What no day is known for (state saved by an older version)
        counts for ``fallback``."""
        days = dict(self.days)
        rest = self.kh - sum(days.values())
        if rest > EPS:
            days[fallback] = days.get(fallback, 0.0) + rest
        return days

    def as_dict(self) -> dict[str, Any]:
        return {"hours": self.hours, "kh": self.kh, "days": dict(self.days)}

    @classmethod
    def from_dict(cls, data: Any) -> Run:
        data = checked(data, dataclass_schema(cls))
        if not isinstance(data, dict):
            return cls()
        days = data.get("days")
        return cls(
            _float(data.get("hours")),
            _float(data.get("kh")),
            {str(d): _float(v) for d, v in days.items()} if isinstance(days, dict) else {},
        )


def _float(value: Any) -> float:
    return float(value) if isinstance(value, int | float) and not isinstance(value, bool) else 0.0


class RoomEnergyModel:
    """Learned heat per m² of each room, the open heating phase and the counters."""

    def __init__(self) -> None:
        self.areas: dict[str, float] = {}  # rooms taking part: floor area (m²)
        self.coefficients: dict[str, float] = {}  # learned c_i
        self.gram: dict[str, dict[str, float]] = {}  # sum of x x^T (forgetting)
        self.moment: dict[str, float] = {}  # sum of x y (forgetting)
        self.sum_x: float = 0.0  # house-wide sums: their ratio is the prior of every room
        self.sum_y: float = 0.0
        self.phases: dict[str, int] = {}  # closed phases a room took part in
        self.single: dict[str, int] = {}  # of them: phases in which only this room heated
        self.counters: dict[str, Counter] = {}
        self.unassigned = Counter()
        self.start: float | None = None  # meter kWh at the start of the open phase
        self.runs: dict[str, Run] = {}

    # ------------------------------------------------------------ setup

    def set_areas(self, areas: Mapping[str, float]) -> None:
        """Rooms taking part, with their floor area (m²); others are left out."""
        self.areas = {
            room: float(area)
            for room, area in areas.items()
            if isinstance(area, int | float)
            and FLOOR_AREA_BOUNDS[0] <= area <= FLOOR_AREA_BOUNDS[1]
        }

    def restart(self) -> None:
        """The meter changed: the open phase is dropped, the totals are kept."""
        self.start = None
        self.runs = {}

    def counter(self, room: str) -> Counter:
        return self.counters.setdefault(room, Counter())

    def peek(self, room: str) -> Counter:
        """Counter of a room for reading (a room without one has nothing yet)."""
        return self.counters.get(room) or Counter()

    # ------------------------------------------------------------ inputs

    def roll(self, day: str, month: str) -> None:
        """Start a new day or month in every counter (called every tick)."""
        self.unassigned.roll(day, month)
        for counter in self.counters.values():
            counter.roll(day, month)

    def heating(self, room: str, hours: float, delta_t: float, day: str, month: str) -> None:
        """A room ran for ``hours`` with a demand of ``delta_t`` K (target minus outdoor)."""
        counter = self.counter(room)
        counter.roll(day, month)
        counter.day_hours += hours
        if self.start is None or room not in self.areas:
            return
        self.runs.setdefault(room, Run()).add(day, hours, hours * max(delta_t, 0.0))

    def reading(self, kwh: float, day: str, month: str) -> None:
        """A new meter value (it differs from the last one). Closes the open phase when
        it has run time; the kWh since its start are split over the rooms."""
        if self.start is None or kwh < self.start - EPS:
            # first reading, or a reset: nothing before this value can be divided
            self.start, self.runs = kwh, {}
            return
        if kwh <= self.start + EPS:
            return
        self.roll(day, month)
        kwh_phase = kwh - self.start
        hours = sum(run.hours for run in self.runs.values())
        if hours <= 0:
            # no room heated since the last reading: the water, the pipes, the leaks
            self.unassigned.add(kwh_phase)
        elif hours < MIN_RUN_H:
            return  # too short: the next phase is added to it
        else:
            x = {
                room: self.areas[room] * run.kh
                for room, run in self.runs.items()
                if room in self.areas and run.kh > 0
            }
            self._learn(x, kwh_phase)
            self._split(x, kwh_phase, day)
        self.start, self.runs = kwh, {}

    # ------------------------------------------------------------ learning

    def _learn(self, x: dict[str, float], y: float) -> None:
        total = sum(x.values())
        if total <= 0:
            return  # nothing to learn from: the rooms ran without demand
        for row in self.gram.values():
            for col in row:
                row[col] *= FORGETTING
        for room in self.moment:
            self.moment[room] *= FORGETTING
        self.sum_x = self.sum_x * FORGETTING + total
        self.sum_y = self.sum_y * FORGETTING + y
        for room_i, xi in x.items():
            row = self.gram.setdefault(room_i, {})
            for room_j, xj in x.items():
                row[room_j] = row.get(room_j, 0.0) + xi * xj
            self.moment[room_i] = self.moment.get(room_i, 0.0) + xi * y
            self.phases[room_i] = self.phases.get(room_i, 0) + 1
            if len(x) == 1:
                self.single[room_i] = self.single.get(room_i, 0) + 1
        self._solve()

    def prior(self) -> float:
        """House-wide mean coefficient: the pull of the ridge, and the start of new rooms."""
        return self.sum_y / self.sum_x if self.sum_x > EPS else DEFAULT_COEFFICIENT

    def _solve(self) -> None:
        """Non-negative ridge regression by coordinate descent (projected onto the bounds)."""
        rooms = sorted(self.areas)
        prior = self.prior()
        size = sum(self.gram.get(r, {}).get(r, 0.0) for r in rooms) / len(rooms)
        ridge = RIDGE * size + EPS
        low, high = COEFFICIENT_BOUNDS
        c = {r: min(high, max(low, self.coefficients.get(r, prior))) for r in rooms}
        target = {r: self.moment.get(r, 0.0) + ridge * prior for r in rooms}
        for _ in range(SOLVER_STEPS):
            for i in rooms:
                row = self.gram.get(i, {})
                rest = sum(row.get(j, 0.0) * c[j] for j in rooms if j != i)
                c[i] = min(high, max(low, (target[i] - rest) / (row.get(i, 0.0) + ridge)))
        self.coefficients.update(c)

    def _split(self, x: dict[str, float], y: float, today: str) -> None:
        """Share ``y`` kWh over the rooms and, within a room, over the days it ran."""
        weights: dict[tuple[str, str], float] = {}
        for room in x:
            c = self.coefficient(room) * self.areas[room]
            for day, kh in self.runs[room].by_day(today).items():
                weights[room, day] = c * kh
        total = sum(weights.values())
        if total <= 0:
            self.unassigned.add(y)
            return
        for (room, day), weight in weights.items():
            counter = self.counter(room)
            counter.roll(today, today[:7])  # a room without a counter starts on today
            counter.add(y * weight / total, day, day[:7])

    # ------------------------------------------------------------ outputs

    def coefficient(self, room: str) -> float:
        return self.coefficients.get(room, self.prior())

    def power_kw(self, room: str, delta_t: float) -> float | None:
        """Heat the room gives off at continuous operation with this demand (kW)."""
        if room not in self.areas:
            return None
        return self.coefficient(room) * self.areas[room] * max(delta_t, 0.0)

    def open_kwh(self, room: str) -> float:
        """Estimate of the heat of the room since the last reading (open phase)."""
        run = self.runs.get(room)
        if run is None or room not in self.areas:
            return 0.0
        return self.coefficient(room) * self.areas[room] * run.kh

    def confidence(self, room: str) -> float:
        """0..1: grows with the closed phases the room took part in, and is higher when
        some of them were phases of this room alone."""
        count = self.phases.get(room, 0)
        if not count:
            return 0.0
        share = self.single.get(room, 0) / count
        return min(1.0, count / MIN_CONFIDENCE_PHASES) * (0.5 + 0.5 * share)

    # ------------------------------------------------------------ storage

    def as_dict(self) -> dict[str, Any]:
        return {
            "areas": dict(self.areas),
            "coefficients": dict(self.coefficients),
            "gram": {r: dict(row) for r, row in self.gram.items()},
            "moment": dict(self.moment),
            "sum_x": self.sum_x,
            "sum_y": self.sum_y,
            "phases": dict(self.phases),
            "single": dict(self.single),
            "counters": {r: c.as_dict() for r, c in self.counters.items()},
            "unassigned": self.unassigned.as_dict(),
            "start": self.start,
            "runs": {r: run.as_dict() for r, run in self.runs.items()},
        }

    @classmethod
    def from_dict(cls, data: Any) -> RoomEnergyModel:
        data = checked(data, room_energy_schema())
        model = cls()
        if not isinstance(data, dict):
            return model
        model.set_areas({str(r): _float(a) for r, a in (data.get("areas") or {}).items()})
        model.coefficients = {
            str(r): _float(v) for r, v in (data.get("coefficients") or {}).items()
        }
        model.gram = {
            str(r): {str(c): _float(v) for c, v in (row or {}).items()}
            for r, row in (data.get("gram") or {}).items()
        }
        model.moment = {str(r): _float(v) for r, v in (data.get("moment") or {}).items()}
        model.sum_x = _float(data.get("sum_x"))
        model.sum_y = _float(data.get("sum_y"))
        model.phases = {str(r): int(v) for r, v in (data.get("phases") or {}).items()}
        model.single = {str(r): int(v) for r, v in (data.get("single") or {}).items()}
        model.counters = {
            str(r): Counter.from_dict(v) for r, v in (data.get("counters") or {}).items()
        }
        model.unassigned = Counter.from_dict(data.get("unassigned"))
        start = data.get("start")
        model.start = _float(start) if isinstance(start, int | float) else None
        model.runs = {str(r): Run.from_dict(v) for r, v in (data.get("runs") or {}).items()}
        return model


def room_energy_schema() -> dict[str, Any]:
    numeric_map = {"*": number}
    return {
        **{k: numeric_map for k in ("areas", "coefficients", "moment", "phases", "single")},
        "gram": {"*": numeric_map},
        "sum_x": number,
        "sum_y": number,
        "counters": {"*": dataclass_schema(Counter)},
        "unassigned": dataclass_schema(Counter),
        "start": optional(number),
        "runs": {"*": dataclass_schema(Run)},
    }
