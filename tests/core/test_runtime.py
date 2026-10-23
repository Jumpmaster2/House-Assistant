"""Modules start, stop and restart on their own; the entry is not reloaded."""

from __future__ import annotations

from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN
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
