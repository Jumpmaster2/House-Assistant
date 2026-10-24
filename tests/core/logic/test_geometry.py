"""Cross ventilation and draft from the arrangement of the windows."""

import pytest

from custom_components.house_assistant.core.logic.geometry import (
    KIND_CROSS,
    KIND_DRAFT,
    WindowPlace,
    distance_to_segment,
    plan,
    relation,
    window_points,
)

# Example house, 12 m wide (front and back) and 8 m deep, one floor, seen from above
# with the front at the bottom (the back wall counts from its right end, as the compass
# draws it):
#
#            bedroom (2)              bath (1)
#   kids
#            living (1)   living (2)   kitchen (3)
#
# The line from the kids room to the bath passes the bedroom, the one from the kids
# room to the kitchen runs along the front through the living area.
W, D = 12.0, 8.0
WINDOWS = [
    WindowPlace("living_1", "living", "front", 1),
    WindowPlace("living_2", "living", "front", 2),
    WindowPlace("kitchen", "kitchen", "front", 3),
    WindowPlace("bedroom", "bedroom", "back", 2),
    WindowPlace("bath", "bath", "back", 1),
    WindowPlace("kids", "kids", "left"),
]
FLOORS = {
    "living": "ground",
    "kitchen": "ground",
    "bedroom": "ground",
    "bath": "ground",
    "kids": "ground",
}


def test_relation_of_walls() -> None:
    assert relation("front", "back") == "opposite"
    assert relation("left", "right") == "opposite"
    assert relation("front", "left") == "adjacent"
    assert relation("back", "back") == "same"


def test_points_follow_the_compass() -> None:
    points = window_points(WINDOWS, W, D)
    # front wall from its left to its right end (seen from inside): f = +4, r from -6 to 6
    assert points["living_1"] == pytest.approx((4.0, -3.0))
    assert points["living_2"] == pytest.approx((4.0, 0.0))
    assert points["kitchen"] == pytest.approx((4.0, 3.0))
    # back wall from right to left: the bath (1) right, the bedroom (2) left
    assert points["bath"] == pytest.approx((-4.0, 2.0))
    assert points["bedroom"] == pytest.approx((-4.0, -2.0))
    assert points["kids"] == pytest.approx((0.0, -6.0))
    assert distance_to_segment((0.0, 0.0), (-1.0, 1.0), (1.0, 1.0)) == pytest.approx(1.0)
    assert distance_to_segment((5.0, 0.0), (-1.0, 0.0), (1.0, 0.0)) == pytest.approx(4.0)


def test_cross_ventilation_rule_one() -> None:
    result = plan(WINDOWS, FLOORS)
    keys = {(c.kind, c.windows) for c in result.combinations["living"]}
    # an own window with one in another room on an opposite or adjacent wall
    assert (KIND_CROSS, ("living_1", "bath")) in keys
    assert (KIND_CROSS, ("living_1", "kids")) in keys
    # not with the kitchen on the same wall
    assert all("kitchen" not in c.windows for c in result.combinations["living"])
    # without the size of the house there is no draft through a room
    assert all(c.kind == KIND_CROSS for cs in result.combinations.values() for c in cs)


def test_draft_rule_two() -> None:
    result = plan(WINDOWS, FLOORS, W, D, reach=2.0)
    living = {c.windows for c in result.combinations["living"] if c.kind == KIND_DRAFT}
    bedroom = {c.windows for c in result.combinations["bedroom"] if c.kind == KIND_DRAFT}
    # kids room and bath: the line from (0, -6) to (-4, 2) passes the living area
    # (point (4, 0)) at 6.3 m, the bedroom (-4, -2) at 1.8 m
    assert ("bath", "kids") not in living
    assert ("bath", "kids") in bedroom
    # kitchen and kids room: the line runs along the front, through the living area
    assert ("kitchen", "kids") in living
    assert ("kitchen", "kids") not in bedroom
    # never two windows of the same room, never two on the same wall
    assert all(
        len({c.windows[0], c.windows[1]}) == 2 for cs in result.combinations.values() for c in cs
    )
    assert ("kitchen", "bedroom") not in bedroom  # an own window: that is rule 1


def test_floors_walls_and_switched_off_combinations() -> None:
    windows = [*WINDOWS, WindowPlace("attic", "attic", "front"), WindowPlace("hall", "hall", None)]
    floors = {**FLOORS, "attic": "upstairs", "hall": "ground"}
    result = plan(windows, floors, W, D)
    # another floor: no combination with the ground floor
    assert "attic" not in result.combinations
    assert result.no_wall == ["hall"]
    # a room whose floor cannot be told takes no part
    result = plan(WINDOWS, {**FLOORS, "kids": None}, W, D)
    assert result.no_floor == ["kids"]
    assert all("kids" not in c.windows for cs in result.combinations.values() for c in cs)
    # a combination switched off in a room
    result = plan(WINDOWS, FLOORS, W, D, disabled={"living": ["kids|living_1"]})
    assert ("living_1", "kids") not in {c.windows for c in result.combinations["living"]}
    assert ("living_1", "bath") in {c.windows for c in result.combinations["living"]}
