"""State of a window from its contacts."""

from custom_components.house_assistant.core.logic.contacts import (
    CLOSED,
    OPEN,
    TILTED,
    UNKNOWN,
    contact_state,
    opening_share,
    window_state,
)


def test_contacts_and_handles() -> None:
    assert contact_state("on") == OPEN
    assert contact_state("off") == CLOSED
    assert contact_state("tilted") == TILTED  # window handle
    assert contact_state("open") == OPEN
    assert contact_state("on", tilt_contact=True) == TILTED
    assert contact_state("unavailable") == UNKNOWN
    assert contact_state(None) == UNKNOWN


def test_window_state() -> None:
    assert window_state(["off", "off"]) == CLOSED
    assert window_state(["off", "on"]) == OPEN  # two sashes, one open
    # the open contact of a window whose tilt contact reports tilted: only tilted
    assert window_state(["on"], ["on"]) == TILTED
    assert window_state(["off"], ["on"]) == TILTED
    assert window_state(["off", "unknown"]) == UNKNOWN
    assert window_state([]) == CLOSED


def test_opening_share() -> None:
    assert opening_share(OPEN) == 1.0
    assert opening_share(TILTED) == 0.25
    assert opening_share(UNKNOWN) == 0.0  # the heating counts it as closed, as before
    assert opening_share(CLOSED) == 0.0
