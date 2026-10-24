"""Covers on vacation: sun protection without waiting for the room."""

from __future__ import annotations

from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant

from .conftest import OUTDOOR, SUMMER_NOON, VACATION, advance, engine_of, make_entry, setup_entry

ROOM = "climate.living_room"


async def _cool_room_at_summer_noon(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory, outdoor: str = "25.0", **options
) -> None:
    hass.states.async_set(ROOM, "heat", {"current_temperature": 20.0, "temperature": 21.0})
    freezer.move_to(SUMMER_NOON)
    await setup_entry(hass, make_entry(window={"room_entity": ROOM}, **options))
    hass.states.async_set(OUTDOOR, outdoor)
    await hass.async_block_till_done()


async def test_heat_protection_on_vacation(
    hass: HomeAssistant, base_states, calls, freezer: FrozenDateTimeFactory
) -> None:
    await _cool_room_at_summer_noon(hass, freezer)
    await advance(hass, freezer, 30 * 60)
    # the room is cool: no sun protection
    assert calls["set_cover_position"] == []
    hass.states.async_set(VACATION, "on")
    await hass.async_block_till_done()
    assert engine_of(hass).sun_details(next(iter(engine_of(hass).windows.values())))[
        "vacation_heat_protection"
    ]
    # the sun hold time still applies
    await advance(hass, freezer, 4 * 60)
    assert calls["set_cover_position"] == []
    await advance(hass, freezer, 60)
    assert [c.data["position"] for c in calls["set_cover_position"]] == [10]


async def test_no_heat_protection_when_switched_off(
    hass: HomeAssistant, base_states, calls, freezer: FrozenDateTimeFactory
) -> None:
    await _cool_room_at_summer_noon(hass, freezer, vacation_heat_protection=False)
    hass.states.async_set(VACATION, "on")
    await hass.async_block_till_done()
    await advance(hass, freezer, 30 * 60)
    assert calls["set_cover_position"] == []


async def test_no_heat_protection_without_a_summer_day(
    hass: HomeAssistant, base_states, calls, freezer: FrozenDateTimeFactory
) -> None:
    await _cool_room_at_summer_noon(hass, freezer, outdoor="15.0")
    hass.states.async_set(VACATION, "on")
    await hass.async_block_till_done()
    await advance(hass, freezer, 30 * 60)
    assert calls["set_cover_position"] == []
