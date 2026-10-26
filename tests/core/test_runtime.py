"""Modules start, stop and restart on their own; the entry is not reloaded."""

from __future__ import annotations

from homeassistant.config_entries import ConfigSubentryData
from homeassistant.const import EVENT_STATE_CHANGED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_capture_events

from custom_components.house_assistant.const import CONF_VACATION_ENTITIES, DOMAIN
from custom_components.house_assistant.meter.const import meter_defaults

WATER = {**meter_defaults("water"), "camera": "camera.water_cam", "warmup": 0}


def _entry(modules: list[str]) -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={},
        options={
            "core": {"modules": modules},
            "meter": {"ai_task_entity": "ai_task.claude", "notify_rejected": True},
        },
        subentries_data=[
            ConfigSubentryData(data=WATER, subentry_type="meter", title="Water", unique_id=None)
        ],
    )


async def _setup(hass: HomeAssistant, modules: list[str]) -> MockConfigEntry:
    hass.states.async_set("camera.water_cam", "idle")
    entry = _entry(modules)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_module_switched_on_and_off(hass: HomeAssistant) -> None:
    entry = await _setup(hass, [])
    assert hass.states.get("sensor.water_meter_reading") is None

    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": ["meter"]}}
    )
    await hass.async_block_till_done()
    assert hass.states.get("sensor.water_meter_reading") is not None
    assert "meter" in entry.runtime_data.modules

    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": []}}
    )
    await hass.async_block_till_done()
    assert hass.states.get("sensor.water_meter_reading") is None
    assert entry.runtime_data.modules == {}
    # the settings and the subentries stay
    assert entry.options["meter"]["ai_task_entity"] == "ai_task.claude"
    assert len(entry.subentries) == 1


async def test_restart_only_on_own_changes(hass: HomeAssistant) -> None:
    entry = await _setup(hass, ["meter"])
    module = entry.runtime_data.modules["meter"]

    # a change of another section leaves the module running
    hass.config_entries.async_update_entry(entry, options={**entry.options, "other": {"x": 1}})
    await hass.async_block_till_done()
    assert entry.runtime_data.modules["meter"] is module

    # a change of its own settings restarts it, the entities keep their ids
    hass.config_entries.async_update_entry(
        entry,
        options={**entry.options, "meter": {**entry.options["meter"], "notify_rejected": False}},
    )
    await hass.async_block_till_done()
    assert entry.runtime_data.modules["meter"] is not module
    assert hass.states.get("sensor.water_meter_reading") is not None
    assert entry.runtime_data.modules["meter"].manager.options["notify_rejected"] is False


def _unavailable_events(events) -> list[str]:
    """Entities whose state changed to "unavailable" (what the logbook shows as a pair)."""
    return [
        e.data["entity_id"]
        for e in events
        if e.data["new_state"] is not None and e.data["new_state"].state == "unavailable"
    ]


async def test_quiet_restart_writes_no_unavailable_entries(hass: HomeAssistant) -> None:
    """Saving settings restarts the module: its entities keep their ids and registry entries,
    and no "unavailable" state appears in between (the logbook shows nothing for the restart)."""
    entry = await _setup(hass, ["meter"])
    registry = er.async_get(hass)
    before = {
        e.entity_id: (e.id, e.unique_id)
        for e in er.async_entries_for_config_entry(registry, entry.entry_id)
        if e.entity_id.startswith("sensor.water_")
    }
    assert "sensor.water_meter_reading" in before
    events = async_capture_events(hass, EVENT_STATE_CHANGED)

    hass.config_entries.async_update_entry(
        entry,
        options={**entry.options, "meter": {**entry.options["meter"], "notify_rejected": False}},
    )
    await hass.async_block_till_done()

    assert entry.runtime_data.modules["meter"] is not None
    assert _unavailable_events(events) == []
    for entity_id, (entry_id, unique_id) in before.items():
        assert hass.states.get(entity_id) is not None, entity_id
        reg = registry.async_get(entity_id)
        assert reg is not None and (reg.id, reg.unique_id) == (entry_id, unique_id)


async def test_quiet_restart_of_the_house_keeps_its_entities(hass: HomeAssistant) -> None:
    """The house restarts with its own settings; its vacation entities keep their states."""
    entry = await _setup(hass, [])
    registry = er.async_get(hass)
    house_entities = [
        e.entity_id
        for e in er.async_entries_for_config_entry(registry, entry.entry_id)
        if "vacation" in e.entity_id
    ]
    assert house_entities
    before = {eid: hass.states.get(eid) for eid in house_entities}
    assert all(state is not None for state in before.values())
    events = async_capture_events(hass, EVENT_STATE_CHANGED)
    house = entry.runtime_data.house

    # an external source of the vacation is a setting of the house: the house restarts
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "core": {**entry.options["core"], CONF_VACATION_ENTITIES: ["input_boolean.away"]},
        },
    )
    await hass.async_block_till_done()

    assert entry.runtime_data.house is not None and entry.runtime_data.house is not house
    assert _unavailable_events(events) == []
    for eid in house_entities:
        assert hass.states.get(eid) is not None, eid
        assert registry.async_get(eid) is not None


async def test_switched_off_module_leaves_no_state(hass: HomeAssistant) -> None:
    """Switching a module off removes its states at once, as before."""
    entry = await _setup(hass, ["meter"])
    assert hass.states.get("sensor.water_meter_reading") is not None
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": []}}
    )
    await hass.async_block_till_done()
    assert hass.states.get("sensor.water_meter_reading") is None


async def test_unloading_the_entry_keeps_the_unavailable_states(hass: HomeAssistant) -> None:
    """Unloading the entry (or stopping Home Assistant) is not a restart: the states stay
    as "unavailable", as before."""
    entry = await _setup(hass, ["meter"])
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    state = hass.states.get("sensor.water_meter_reading")
    assert state is not None and state.state == "unavailable"
