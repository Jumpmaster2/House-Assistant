"""State of a window from its contacts.

A contact is binary (on = open, or tilted for a tilt contact) or a window handle with
the states open, tilted and closed. Every module interprets an unknown state its own
way: the covers take it as open (not safe), the heating as closed (as before).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Final

OPEN: Final = "open"
TILTED: Final = "tilted"
CLOSED: Final = "closed"
UNKNOWN: Final = "unknown"

_OPEN_STATES = ("on", "open", "opened")
_TILTED_STATES = ("tilted", "tilt")
_CLOSED_STATES = ("off", "closed", "close")

# Share of the opening area of a tilted window for the heating.
TILTED_SHARE: Final = 0.25


def contact_state(state: str | None, tilt_contact: bool = False) -> str:
    """State of one contact; ``tilt_contact``: on means tilted."""
    if state in _CLOSED_STATES:
        return CLOSED
    if state in _TILTED_STATES:
        return TILTED
    if state in _OPEN_STATES:
        return TILTED if tilt_contact else OPEN
    return UNKNOWN


def window_state(states: Iterable[str | None], tilt_states: Iterable[str | None] = ()) -> str:
    """A tilt contact reporting tilted makes the window tilted, also when its window
    contact reports open (the sash is only tilted) or closed (the window contact only
    notices a fully open sash). Open before tilted before unknown before closed over
    several contacts."""
    found = {contact_state(s) for s in states}
    if any(contact_state(s, True) == TILTED for s in tilt_states):
        found = (found - {OPEN, CLOSED}) | {TILTED}
    for result in (OPEN, TILTED, UNKNOWN):
        if result in found:
            return result
    return CLOSED


def opening_share(state: str) -> float:
    """Share of the opening area for the heating: tilted counts a quarter, unknown as
    closed."""
    if state == OPEN:
        return 1.0
    if state == TILTED:
        return TILTED_SHARE
    return 0.0
