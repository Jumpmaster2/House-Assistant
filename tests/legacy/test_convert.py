"""The converter of the transfer (pure, on the contents of the storage files)."""

from __future__ import annotations

import itertools

import pytest
from legacy import convert as cv

from custom_components.house_assistant.const import SHARED_KEYS

from . import data
from .data import BATH, GROUP, HEAT, LIVING, METER, SHUT, WATER, WIN_KITCHEN, WIN_LIVING


def _plan() -> cv.Plan:
    ids = (f"01NEW{n:021d}" for n in itertools.count())
    return cv.build_plan(
        data.config_entries(), data.entity_registry(), data.device_registry(), lambda: next(ids)
    )


def _subs(plan: cv.Plan, subentry_type: str) -> dict[str, dict]:
    return {
        s["subentry_id"]: s for s in plan.entry["subentries"] if s["subentry_type"] == subentry_type
    }


def test_shared_keys_follow_the_integration() -> None:
    assert set(cv.SHARED_KEYS) == set(SHARED_KEYS) - {"language"}


def test_heating_option_migrations() -> None:
    options = cv.migrate_heating_options(
        {
            "relay_need_minutes": 5,
            "theta_step_down": 0.5,
            "puffer_step_down": 0.3,
            "max_output_tokens": 4000,
            "night_start_hour": 22,
            "night_end_hour": 30,
        },
        1,
    )
    assert "relay_need_minutes" not in options
    assert options["theta_step_down"] == 1.0
    assert options["puffer_step_down"] == 0.3  # not the old default: stays
    assert options["max_output_tokens"] == 16000
    assert (options["night_start_hour"], options["night_end_hour"]) == ("22:00:00", "06:00:00")
    # an entry already at minor version 4 stays as it is
    assert cv.migrate_heating_options({"max_output_tokens": 4000}, 4) == {"max_output_tokens": 4000}


def test_entry_rooms_and_windows() -> None:
    plan = _plan()
    entry = plan.entry
    assert entry["domain"] == "house_assistant"
    assert (entry["version"], entry["minor_version"]) == (1, 1)
    assert plan.old_entries == {
        "ai_heating_assistant": HEAT,
        "shutter_assistant": SHUT,
        "zaehler_ablesung": METER,
    }
    rooms = _subs(plan, "room")
    # the ids of the areas, their Home Assistant area from the device, no contact fields
    assert set(rooms) == {LIVING, BATH}
    assert rooms[LIVING]["data"]["area"] == "wohnzimmer"
    assert "window_sensors" not in rooms[LIVING]["data"]
    assert "door_sensors" not in rooms[LIVING]["data"]
    windows = _subs(plan, "window")
    # a window of the covers sharing a contact: one window, size and room from the heating
    assert windows[WIN_LIVING]["data"]["room"] == LIVING
    assert windows[WIN_LIVING]["data"]["size"] == "medium"
    assert windows[WIN_LIVING]["data"]["cover"] == "cover.living"
    # the room from the thermostat of its room entity
    assert windows[WIN_KITCHEN]["data"]["room"] == BATH
    # that thermostat is the one of its room: the room gives temperature and target
    assert "room_entity" not in windows[WIN_KITCHEN]["data"]
    # the other contacts: windows without a cover, named after the contact
    plain = {
        w["data"]["window_sensors"][0]: w["data"]
        for w in windows.values()
        if not w["data"].get("cover")
    }
    assert plain == {
        "binary_sensor.terrace_door": {
            "name": "Terrassentür",
            "room": LIVING,
            "size": "door",
            "window_sensors": ["binary_sensor.terrace_door"],
        },
        "binary_sensor.bath_window": {
            "name": "binary_sensor.bath_window",
            "room": BATH,
            "size": "small",
            "window_sensors": ["binary_sensor.bath_window"],
        },
    }
    assert set(_subs(plan, "group")) == {GROUP}
    assert set(_subs(plan, "meter")) == {WATER}
    # the heating day sensor as condition becomes the link to the heating module
    water = _subs(plan, "meter")[WATER]["data"]
    assert water["condition_heating_day"] is True
    assert "condition_entity" not in water
    assert cv.summary(plan)["windows with a cover"] == 2


def test_options() -> None:
    plan = _plan()
    options = plan.entry["options"]
    assert options["core"]["modules"] == ["heating", "shutter", "meter"]
    # the same in both, or set in one module: the house
    assert options["core"]["outdoor_temperature"] == "sensor.outdoor"
    assert options["core"]["vacation_entities"] == ["input_boolean.away"]
    assert options["core"]["notify_services"] == ["notify.phone"]
    assert options["core"]["house_azimuth"] == 180
    # On conflicts heating wins; no shared module values remain.
    assert options["core"]["weather"] == "weather.home"
    assert any(
        note.startswith("weather differs") and note.endswith("using heating") for note in plan.notes
    )
    # Covers supplied the language before the transfer.
    assert options["core"]["language"] == "de"
    assert "language" not in options["shutter"]
    # set in the house: no copy in the modules
    assert "vacation_entities" not in options["heating"]
    assert "outdoor_temperature" not in options["shutter"]
    assert "notify_services" not in options["shutter"]
    assert "house_azimuth" not in options["shutter"]
    for module in ("heating", "shutter"):
        assert not set(options[module]) & set(SHARED_KEYS)
    # the heating day sensor of the heating becomes the link to the heating module
    assert options["shutter"]["use_heating_day"] is True
    assert "heating_entity" not in options["shutter"]
    assert options["heating"]["max_output_tokens"] == 16000
    assert options["heating"]["night_start_hour"] == "22:00:00"
    assert options["meter"]["ai_task_entity"] == "ai_task.claude"


def test_registries() -> None:
    plan = _plan()
    new = plan.new_entry_id
    entities = {
        e["entity_id"]: e
        for e in cv.convert_entities(data.entity_registry(), plan)["data"]["entities"]
    }
    # same entity ids; the entities of a module as a whole get the new entry id
    assert entities["binary_sensor.heating_heating_day"]["unique_id"] == f"{new}_heating_day"
    assert entities["switch.covers_automatic"]["unique_id"] == f"{new}_automatic"
    assert entities["climate.bad"]["unique_id"] == f"{BATH}_climate"
    assert entities["climate.bad"]["config_subentry_id"] == BATH
    assert entities["sensor.wasser_zahlerstand"]["unique_id"] == f"{WATER}_reading"
    for entity_id in ("climate.bad", "sensor.wohnzimmer_status", "sensor.wasser_zahlerstand"):
        assert entities[entity_id]["platform"] == "house_assistant"
        assert entities[entity_id]["config_entry_id"] == new
    # others untouched
    assert entities["light.hall"]["platform"] == "hue"
    assert entities["binary_sensor.terrace_door"]["platform"] == "zha"

    devices = {
        d["id"]: d for d in cv.convert_devices(data.device_registry(), plan)["data"]["devices"]
    }
    assert devices["dev-heating"]["identifiers"] == [["house_assistant", f"{new}_heating"]]
    assert devices["dev-covers"]["identifiers"] == [["house_assistant", f"{new}_shutter"]]
    assert devices["dev-bath"]["identifiers"] == [["house_assistant", BATH]]
    assert devices["dev-bath"]["area_id"] == "bad"
    assert devices["dev-water"]["config_entry_id"] == new
    assert devices["dev-water"]["primary_config_entry"] == new
    assert devices["dev-hue"]["identifiers"] == [["hue", "bridge"]]

    # an older registry with a list of entries per device
    older = data.device_registry()
    for device in older["data"]["devices"]:
        entry_id = device.pop("config_entry_id")
        device["config_entries"] = [entry_id]
        device["config_entries_subentries"] = {entry_id: [None]}
    converted = cv.convert_devices(older, plan)["data"]["devices"]
    assert converted[0]["config_entries"] == [new]
    assert converted[0]["config_entries_subentries"] == {new: [None]}

    entries = cv.convert_config_entries(data.config_entries(), plan)["data"]["entries"]
    assert [e["domain"] for e in entries] == ["hue", "house_assistant"]


def test_two_entities_with_one_unique_id_are_refused() -> None:
    plan = _plan()
    registry = data.entity_registry()
    registry["data"]["entities"].append(
        {
            **registry["data"]["entities"][0],
            "entity_id": "binary_sensor.other",
            "platform": "house_assistant",
            "config_entry_id": plan.new_entry_id,
            "unique_id": f"{plan.new_entry_id}_heating_day",
        }
    )
    with pytest.raises(cv.TransferError, match="same unique id"):
        cv.convert_entities(registry, plan)


def test_already_transferred() -> None:
    entries = data.config_entries()
    entries["data"]["entries"].append({"domain": "house_assistant", "entry_id": "x"})
    with pytest.raises(cv.TransferError, match="already set up"):
        cv.find_entries(entries)


def test_dashboards_resources_and_automations() -> None:
    dashboard, count = cv.convert_dashboard(data.DASHBOARD)
    cards = dashboard["data"]["config"]["views"][0]["cards"]
    assert count == 3
    assert cards[0]["type"] == "custom:house-assistant-thermostat-card"
    assert cards[1]["type"] == "custom:house-assistant-window-tile"
    assert cards[2]["cards"][0]["type"] == "custom:house-assistant-cover-card"

    resources, removed = cv.convert_resources(data.RESOURCES)
    assert [i["id"] for i in resources["data"]["items"]] == ["c"]
    assert len(removed) == 2

    text, replaced, left = cv.convert_yaml_text(data.AUTOMATIONS)
    assert "event_type: house_assistant_cover_moved" in text
    assert "action: house_assistant.move_cover" in text
    assert "action: house_assistant.read_meter" in text
    assert "action: house_assistant.run_ai_check" in text
    assert len(replaced) == 4
    # what the transfer cannot decide is named
    assert left == ["message: \"{{ integration_entities('shutter_assistant') | count }}\""]


def test_ulid() -> None:
    first, second = cv.ulid(), cv.ulid()
    assert len(first) == 26 and first != second
    assert set(first) <= set(cv.CROCKFORD)


@pytest.mark.parametrize("key", set(SHARED_KEYS) - {"language", "vacation_entities"})
def test_shared_conflicts_prefer_heating(key):
    # Selection must not depend on the order of the input dictionaries.
    sections = {"shutter": {key: "cover"}, "heating": {key: "heat"}}
    notes = []
    assert cv.shared_settings(sections, notes) == {key: "heat"}
    assert notes == [f"{key} differs (shutter: cover, heating: heat), using heating"]


def test_shared_vacation_sources_are_combined():
    sections = {
        "heating": {"vacation_entities": ["calendar.one"]},
        "shutter": {"vacation_entities": ["calendar.one", "calendar.two"]},
    }
    assert cv.shared_settings(sections, []) == {
        "vacation_entities": ["calendar.one", "calendar.two"]
    }
