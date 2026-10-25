"""Tests for the heat consumption per room (the heat meter split over the rooms)."""

import math
import random

import pytest

from custom_components.house_assistant.heating.logic.room_energy import (
    DEFAULT_COEFFICIENT,
    RoomEnergyModel,
)

AREAS = {"living": 20.0, "bedroom": 15.0, "office": 25.0}
TRUE_C = {"living": 0.002, "bedroom": 0.003, "office": 0.0025}
DAY, MONTH = "2026-11-16", "2026-11"


def run_phases(
    model: RoomEnergyModel,
    phases: list[dict[str, tuple[float, float]]],
    resolution: float | None,
) -> tuple[float, float]:
    """Feed phases to the model: room -> (hours, demand K). The meter is the sum of the
    true heat, read in steps of ``resolution`` (None: exact). Returns the readings."""
    total = 0.0
    truth = {room: 0.0 for room in TRUE_C}
    shown = 0.0
    model.reading(0.0, DAY, MONTH)  # first reading: starts the phases
    for phase in phases:
        for room, (hours, demand) in phase.items():
            model.heating(room, hours, demand, DAY, MONTH)
            heat = TRUE_C[room] * AREAS[room] * hours * demand
            total += heat
            truth[room] += heat
        shown = total if resolution is None else math.floor(total / resolution) * resolution
        model.reading(shown, DAY, MONTH)
    return shown, total


def random_single_phases(rng: random.Random, count: int) -> list[dict[str, tuple[float, float]]]:
    rooms = list(TRUE_C)
    return [{rooms[i % 3]: (rng.uniform(0.5, 2.0), rng.uniform(8.0, 20.0))} for i in range(count)]


def test_single_room_phases_identify_the_coefficients() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    run_phases(model, random_single_phases(random.Random(1), 90), resolution=None)
    for room, true in TRUE_C.items():
        assert model.coefficient(room) == pytest.approx(true, rel=0.15)


def test_shares_add_up_to_the_meter() -> None:
    rng = random.Random(2)
    rooms = list(TRUE_C)
    phases = []
    for _ in range(60):
        chosen = rng.sample(rooms, rng.randint(1, 3))
        phases.append({room: (rng.uniform(0.3, 2.0), rng.uniform(5.0, 20.0)) for room in chosen})
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    shown, _ = run_phases(model, phases, resolution=None)
    assigned = sum(model.counter(room).total for room in rooms) + model.unassigned.total
    assert assigned == pytest.approx(shown, rel=1e-9)


def test_rounded_readings_do_not_bias_the_split() -> None:
    """Readings in whole kWh: the phases are differences of readings, so the shares
    add up to the meter exactly and each room stays close to its true heat."""
    rng = random.Random(3)
    rooms = list(TRUE_C)
    phases = []
    for _ in range(400):
        chosen = rng.sample(rooms, rng.randint(1, 2))
        phases.append({room: (rng.uniform(0.3, 1.5), rng.uniform(8.0, 20.0)) for room in chosen})
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    shown, total = run_phases(model, phases, resolution=1.0)
    assigned = sum(model.counter(room).total for room in rooms) + model.unassigned.total
    assert assigned == pytest.approx(shown, rel=1e-9)
    assert shown <= total < shown + 1.0
    for room in rooms:
        true_heat = 0.0
        for phase in phases:
            if room in phase:
                hours, demand = phase[room]
                true_heat += TRUE_C[room] * AREAS[room] * hours * demand
        assert model.counter(room).total == pytest.approx(true_heat, rel=0.1)


def test_reset_discards_the_open_phase() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    model.reading(1000.0, DAY, MONTH)
    model.heating("living", 1.0, 15.0, DAY, MONTH)
    before = model.counter("living").total
    model.reading(5.0, DAY, MONTH)  # new meter: the consumption up to here is lost
    assert model.counter("living").total == before
    assert model.runs == {}
    model.heating("living", 1.0, 15.0, DAY, MONTH)
    model.reading(9.0, DAY, MONTH)
    assert model.counter("living").total > before
    assert model.counter("living").total + model.unassigned.total == pytest.approx(4.0)


def test_room_without_floor_area_takes_no_part() -> None:
    model = RoomEnergyModel()
    model.set_areas({"living": 20.0, "storage": None, "attic": 0.0})  # type: ignore[dict-item]
    model.reading(100.0, DAY, MONTH)
    model.heating("storage", 1.0, 15.0, DAY, MONTH)
    model.heating("living", 1.0, 15.0, DAY, MONTH)
    model.reading(102.0, DAY, MONTH)
    assert "storage" not in model.areas and "attic" not in model.areas
    assert model.counter("storage").total == 0.0
    assert model.counter("living").total == pytest.approx(2.0)


def test_phase_without_heating_is_not_assigned() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    model.reading(100.0, DAY, MONTH)
    model.reading(101.5, DAY, MONTH)  # hot water: no room heated
    assert model.unassigned.total == pytest.approx(1.5)
    assert all(model.counter(room).total == 0.0 for room in AREAS)


def test_short_phase_is_merged_with_the_next() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    model.reading(100.0, DAY, MONTH)
    model.heating("living", 0.1, 15.0, DAY, MONTH)  # below the minimum run time
    model.reading(101.0, DAY, MONTH)
    assert model.counter("living").total == 0.0
    model.heating("living", 1.0, 15.0, DAY, MONTH)
    model.reading(103.0, DAY, MONTH)
    assert model.counter("living").total + model.unassigned.total == pytest.approx(3.0)
    assert model.unassigned.total == 0.0


def test_no_demand_gives_no_share() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    model.reading(10.0, DAY, MONTH)
    model.heating("living", 2.0, -3.0, DAY, MONTH)  # target below outdoor temperature
    model.reading(11.0, DAY, MONTH)
    assert model.unassigned.total == pytest.approx(1.0)
    assert model.coefficients == {}


def test_power_and_open_estimate() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    assert model.power_kw("living", 10.0) == pytest.approx(DEFAULT_COEFFICIENT * 20 * 10)
    assert model.power_kw("unknown", 10.0) is None
    model.reading(10.0, DAY, MONTH)
    model.heating("living", 0.5, 10.0, DAY, MONTH)
    assert model.open_kwh("living") == pytest.approx(DEFAULT_COEFFICIENT * 20 * 5)
    assert model.open_kwh("bedroom") == 0.0


def test_confidence_grows_with_phases() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    assert model.confidence("living") == 0.0
    run_phases(model, random_single_phases(random.Random(4), 90), resolution=None)
    assert model.confidence("living") == pytest.approx(1.0)


def test_round_trip_keeps_the_state() -> None:
    rng = random.Random(5)
    rooms = list(TRUE_C)
    phases = [
        {rng.choice(rooms): (rng.uniform(0.5, 2.0), rng.uniform(8.0, 20.0))} for _ in range(40)
    ]
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    run_phases(model, phases[:30], resolution=1.0)
    model.heating("office", 0.5, 12.0, DAY, MONTH)  # an open phase
    data = model.as_dict()
    restored = RoomEnergyModel.from_dict(data)
    assert restored.as_dict() == data
    assert RoomEnergyModel.from_dict(None).as_dict() == RoomEnergyModel().as_dict()
    for model_ in (model, restored):
        model_.heating("bedroom", 1.0, 15.0, DAY, MONTH)
        model_.reading(model_.start + 3.0, DAY, MONTH)
    assert restored.as_dict() == model.as_dict()


def test_day_and_month_counters_roll() -> None:
    model = RoomEnergyModel()
    model.set_areas(AREAS)
    model.reading(0.0, DAY, MONTH)
    model.heating("living", 1.0, 15.0, DAY, MONTH)
    model.reading(2.0, DAY, MONTH)
    model.roll("2026-11-17", "2026-11")
    counter = model.counter("living")
    assert counter.total == pytest.approx(2.0)
    assert counter.day_kwh == 0.0
    assert counter.month_kwh == pytest.approx(2.0)
    model.roll("2026-12-01", "2026-12")
    assert counter.month_kwh == 0.0 and counter.total == pytest.approx(2.0)
