"""Tilted windows and automatic cross ventilation in the running heating."""

from __future__ import annotations

from typing import Any

import pytest
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits

IN_SEASON = "2026-11-16 10:00:00+01:00"


def _room(sub_id: str, name: str, heated: bool = False) -> ConfigSubentryData:
    data: dict[str, Any] = {"name": name}
    if heated:
        data.update(
            temperature_sensor=f"sensor.{sub_id}_temperature", heater_switch="input_boolean.circuit"
        )
    return ConfigSubentryData(
        data=data, subentry_id=sub_id, subentry_type="room", title=name, unique_id=None
    )


def _window(sub_id: str, room: str, wall: str, size: str = "medium", **extra: Any):
    data = {
        "name": sub_id,
        "room": room,
        "size": size,
        "wall": wall,
        "window_sensors": [f"binary_sensor.{sub_id}"],
        **extra,
    }
    return ConfigSubentryData(
        data=data, subentry_id=sub_id, subentry_type="window", title=sub_id, unique_id=None
    )


def _entry() -> MockConfigEntry:
    # 12 m x 8 m: living room at the front, kitchen front right, kids room on the left wall
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {
                "modules": ["heating"],
                "outdoor_temperature": "sensor.outdoor",
                "house_width": 12.0,
                "house_depth": 8.0,
            },
            "heating": {**HEATING_DEFAULTS, "limits": default_limits()},
        },
        subentries_data=[
            _room("living", "Living room", heated=True),
            _room("kitchen", "Kitchen"),
            _room("kids", "Kids room"),
            _window(
                "living_window",
                "living",
                "front",
                "large",
                wall_position=2,
                tilt_sensors=["binary_sensor.living_tilt"],
            ),
            _window("kitchen_window", "kitchen", "front", wall_position=3),
            _window("kids_window", "kids", "left"),
        ],
    )


async def _setup(hass: HomeAssistant, freezer, entry: MockConfigEntry, move: bool = True) -> Any:
    if move:  # (not with a websocket client: its token would be too old then)
        freezer.move_to(IN_SEASON)
    await hass.config.async_set_time_zone("Europe/Berlin")
    hass.states.async_set("input_boolean.circuit", "off")
    hass.states.async_set("sensor.outdoor", "5", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_temperature", "20", {"unit_of_measurement": "°C"})
    for entity_id in (
        "binary_sensor.living_window",
        "binary_sensor.living_tilt",
        "binary_sensor.kitchen_window",
        "binary_sensor.kids_window",
    ):
        hass.states.async_set(entity_id, "off")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    return entry.runtime_data.modules["heating"].coordinator


async def _tick(hass: HomeAssistant, coordinator: Any) -> Any:
    await coordinator.async_refresh()
    await hass.async_block_till_done()
    return coordinator.areas["living"]


async def test_tilted_window_counts_a_quarter(hass: HomeAssistant, freezer) -> None:
    coordinator = await _setup(hass, freezer, _entry())
    hass.states.async_set("binary_sensor.living_window", "on")
    area = await _tick(hass, coordinator)
    assert area.opening == pytest.approx(1.6)  # large window open
    # the tilt contact of the window: only tilted
    hass.states.async_set("binary_sensor.living_tilt", "on")
    area = await _tick(hass, coordinator)
    assert area.opening == pytest.approx(0.4)
    assert area.own_window_open  # the heating pauses for a tilted window as well
    # a window handle reports the state itself
    hass.states.async_set("binary_sensor.living_tilt", "off")
    hass.states.async_set("binary_sensor.living_window", "tilted")
    area = await _tick(hass, coordinator)
    assert area.opening == pytest.approx(0.4)
    # unknown counts as closed for the heating, as before
    hass.states.async_set("binary_sensor.living_window", "unavailable")
    area = await _tick(hass, coordinator)
    assert area.opening == 0 and not area.own_window_open


async def test_automatic_cross_ventilation_and_draft(hass: HomeAssistant, freezer) -> None:
    coordinator = await _setup(hass, freezer, _entry())
    area = coordinator.areas["living"]
    # own window with the kids room (adjacent wall); kitchen and kids room have the
    # living room between them (front wall to left wall, along the front)
    assert ("living_window", "kids_window") in area.auto_cross
    assert ("kitchen_window", "kids_window") in area.auto_draft
    assert all(pair[1] != "kitchen_window" for pair in area.auto_cross)  # same wall

    hass.states.async_set("binary_sensor.kitchen_window", "on")
    hass.states.async_set("binary_sensor.kids_window", "on")
    area = await _tick(hass, coordinator)
    assert area.draft and area.window_open and not area.own_window_open
    assert area.draft_windows == ["kitchen_window", "kids_window"]
    assert hass.states.get("climate.living_room").attributes["draft_windows"] == [
        "kitchen_window",
        "kids_window",
    ]

    # an own window open with the kids room: cross ventilation
    hass.states.async_set("binary_sensor.kitchen_window", "off")
    hass.states.async_set("binary_sensor.living_window", "on")
    area = await _tick(hass, coordinator)
    assert area.cross and not area.draft
    assert area.draft_windows == ["living_window", "kids_window"]


async def test_combination_switched_off_in_the_panel(
    hass: HomeAssistant, freezer, hass_ws_client
) -> None:
    entry = _entry()
    client = await hass_ws_client(hass)
    await _setup(hass, freezer, entry, move=False)
    await client.send_json({"id": 1, "type": "house_assistant/house/config"})
    plan = (await client.receive_json())["result"]["plan"]
    combinations = {c["key"]: c for c in plan["combinations"]["living"]}
    assert combinations["kids_window|kitchen_window"]["kind"] == "draft"
    assert combinations["kids_window|kitchen_window"]["enabled"]
    assert set(plan["points"]) == {"living_window", "kitchen_window", "kids_window"}

    await client.send_json(
        {
            "id": 2,
            "type": "house_assistant/house/combination",
            "room_id": "living",
            "key": "kids_window|kitchen_window",
            "enabled": False,
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    assert entry.subentries["living"].data["auto_draft_off"] == ["kids_window|kitchen_window"]
    shown = {c["key"]: c for c in msg["result"]["plan"]["combinations"]["living"]}
    assert not shown["kids_window|kitchen_window"]["enabled"]  # still shown, switched off
    await hass.async_block_till_done(wait_background_tasks=True)
    coordinator = entry.runtime_data.modules["heating"].coordinator
    assert ("kitchen_window", "kids_window") not in coordinator.areas["living"].auto_draft
