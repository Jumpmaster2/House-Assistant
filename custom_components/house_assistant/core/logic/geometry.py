"""Cross ventilation and draft from the arrangement of the windows (approximation).

Every window sits in a wall of the house: its own or the one of its direction (group).
Two walls are the same, opposite (front and back, left and right) or adjacent (the
other pairs). Rooms are on the floor of their Home Assistant area.

Rule 1, cross ventilation of a room R: an own window a is open together with a window b
of another room on the same floor, and the wall of b is opposite or adjacent to the
wall of a.

Rule 2, draft through R: two windows b and c of two other rooms on the floor of R are
open, their walls are opposite or adjacent, and R lies on the line between them. Every
window gets a point on the outline of the house (its wall and its order there, as the
compass draws them), every room the centre of the points of its windows; R lies on the
line when its point is at most the draft reach away from the line from b to c. Without
the size of the house only rule 1 applies.

Every combination has a key; a room can switch single combinations off.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Final

WALLS: Final = ("front", "right", "back", "left")
OPPOSITE: Final = {"front": "back", "back": "front", "left": "right", "right": "left"}
DEFAULT_REACH: Final = 2.0  # m

KIND_CROSS: Final = "cross"
KIND_DRAFT: Final = "draft"


@dataclass(frozen=True, slots=True)
class WindowPlace:
    """Where a window is: its room, its wall and its order on the wall."""

    window_id: str
    room_id: str | None
    wall: str | None
    position: float | None = None  # 1 = left as seen from inside, None = after the numbered


@dataclass(frozen=True, slots=True)
class Combination:
    """Windows whose opening together cools a room: ``cross`` = an own window and one of
    another room (rule 1), ``draft`` = two windows of other rooms (rule 2)."""

    kind: str
    windows: tuple[str, str]

    @property
    def key(self) -> str:
        return "|".join(sorted(self.windows))


@dataclass(slots=True)
class Plan:
    """Points of the windows and rooms (m, f towards the front and r towards the right
    seen from inside, the centre of the house at 0), the combinations of every room and
    what keeps a window or a room out."""

    points: dict[str, tuple[float, float]] = field(default_factory=dict)
    room_points: dict[str, tuple[float, float]] = field(default_factory=dict)
    combinations: dict[str, list[Combination]] = field(default_factory=dict)
    no_wall: list[str] = field(default_factory=list)
    no_floor: list[str] = field(default_factory=list)


def relation(wall_a: str, wall_b: str) -> str:
    """same, opposite or adjacent."""
    if wall_a == wall_b:
        return "same"
    return "opposite" if OPPOSITE.get(wall_a) == wall_b else "adjacent"


def window_points(
    windows: Iterable[WindowPlace], width: float, depth: float
) -> dict[str, tuple[float, float]]:
    """Point of every window with a wall on the outline: the windows of a wall in their
    order (numbered first, the others in their given order) evenly along the wall from
    its left to its right end as seen from inside."""
    hw, hd = width / 2, depth / 2
    corners = {"FL": (hd, -hw), "FR": (hd, hw), "BR": (-hd, hw), "BL": (-hd, -hw)}
    ends = {
        "front": (corners["FL"], corners["FR"]),
        "right": (corners["FR"], corners["BR"]),
        "back": (corners["BR"], corners["BL"]),
        "left": (corners["BL"], corners["FL"]),
    }
    by_wall: dict[str, list[tuple[int, WindowPlace]]] = {}
    for index, window in enumerate(windows):
        if window.wall in ends:
            by_wall.setdefault(window.wall, []).append((index, window))
    points: dict[str, tuple[float, float]] = {}
    for wall, items in by_wall.items():
        items.sort(
            key=lambda item: (math.inf if item[1].position is None else item[1].position, item[0])
        )
        (f1, r1), (f2, r2) = ends[wall]
        for i, (_, window) in enumerate(items):
            t = (i + 1) / (len(items) + 1)
            points[window.window_id] = (f1 + (f2 - f1) * t, r1 + (r2 - r1) * t)
    return points


def distance_to_segment(
    point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]
) -> float:
    (px, py), (ax, ay), (bx, by) = point, start, end
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def plan(
    windows: list[WindowPlace],
    floors: Mapping[str, str | None],
    width: float | None = None,
    depth: float | None = None,
    reach: float = DEFAULT_REACH,
    disabled: Mapping[str, Iterable[str]] | None = None,
) -> Plan:
    """The combinations of every room. ``floors``: room -> floor, None when it cannot be
    told (such a room takes no part). ``disabled``: room -> keys switched off."""
    result = Plan()
    placed: list[WindowPlace] = []
    for window in windows:
        if window.room_id is None or window.room_id not in floors:
            continue
        if window.wall not in WALLS:
            result.no_wall.append(window.window_id)
            continue
        if floors[window.room_id] is None:
            if window.room_id not in result.no_floor:
                result.no_floor.append(window.room_id)
            continue
        placed.append(window)
    off = {room: set(keys) for room, keys in (disabled or {}).items()}

    def add(room: str, combination: Combination) -> None:
        if combination.key in off.get(room, set()):
            return
        known = result.combinations.setdefault(room, [])
        if all(c.key != combination.key for c in known):
            known.append(combination)

    def apart(a: WindowPlace, b: WindowPlace) -> bool:
        return relation(str(a.wall), str(b.wall)) != "same"

    # rule 1: an own window and a window of another room on the same floor
    for a in placed:
        for b in placed:
            if b.room_id == a.room_id or floors[b.room_id] != floors[a.room_id]:
                continue
            if apart(a, b):
                add(str(a.room_id), Combination(KIND_CROSS, (a.window_id, b.window_id)))

    if width and depth and width > 0 and depth > 0:
        result.points = window_points(placed, width, depth)
        for room in {w.room_id for w in placed}:
            own = [result.points[w.window_id] for w in placed if w.room_id == room]
            result.room_points[str(room)] = (
                sum(p[0] for p in own) / len(own),
                sum(p[1] for p in own) / len(own),
            )
        # rule 2: two windows of two other rooms, the room between them
        for room, point in result.room_points.items():
            floor = floors[room]
            others = [w for w in placed if w.room_id != room and floors[w.room_id] == floor]
            for i, b in enumerate(others):
                for c in others[i + 1 :]:
                    if b.room_id == c.room_id or not apart(b, c):
                        continue
                    line = (result.points[b.window_id], result.points[c.window_id])
                    if distance_to_segment(point, *line) <= reach:
                        add(room, Combination(KIND_DRAFT, (b.window_id, c.window_id)))
    return result
