"""The transfer on a configuration folder, and the result in Home Assistant: the same
entity ids, the learned data, the pictures of the meters."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import transfer_legacy
from homeassistant.config_entries import ConfigSubentryData
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from legacy import convert as cv
from pytest_homeassistant_custom_component.common import MockConfigEntry

from . import data
from .data import BATH, HEAT, METER, SHUT, WATER

STORES = {
    f"ai_heating_assistant.{HEAT}": {"areas": {BATH: {"target": 23.5}}},
    f"shutter_assistant.{SHUT}": {"windows": {}},
    f"zaehler_ablesung.{METER}": {"meters": {WATER: {"value": 123.456, "automatic": False}}},
}


def _write(path: Path, content: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = content if isinstance(content, str) else json.dumps(content)
    path.write_text(text, encoding="utf-8")


def _config(root: Path) -> Path:
    storage = root / ".storage"
    _write(storage / "core.config_entries", data.config_entries())
    _write(storage / "core.entity_registry", data.entity_registry())
    _write(storage / "core.device_registry", data.device_registry())
    _write(storage / "lovelace", data.DASHBOARD)
    _write(storage / "lovelace_resources", data.RESOURCES)
    for key, content in STORES.items():
        _write(storage / key, {"version": 1, "minor_version": 1, "key": key, "data": content})
    _write(root / "automations.yaml", data.AUTOMATIONS)
    _write(root / "media" / "zaehler_ablesung" / WATER / "letztes.jpg", "jpeg")
    return root


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def test_dry_run_and_apply(tmp_path: Path, capsys) -> None:
    root = _config(tmp_path / "config")
    out = tmp_path / "out"
    out.mkdir()
    before = (root / ".storage" / "core.config_entries").read_text()
    assert transfer_legacy.main(["--config", str(root), "--dry-run", "--out", str(out)]) == 0
    # a dry run changes nothing
    assert (root / ".storage" / "core.config_entries").read_text() == before
    report = (out / "transfer-report.md").read_text()
    assert "weather differs" in report
    assert f"ai_heating_assistant.{HEAT} -> house_assistant." in report
    assert "shutter_assistant.move -> house_assistant.move_cover" in report
    assert "integration_entities('shutter_assistant')" in report
    plan = cv.Plan.from_dict(_load(out / "transfer-plan.json"))

    # only with Home Assistant stopped
    args = ["--config", str(root), "--apply", str(out / "transfer-plan.json")]
    assert transfer_legacy.main(args) == 1
    assert "stop Home Assistant" in capsys.readouterr().err
    assert transfer_legacy.main([*args, "--stopped"]) == 0

    storage = root / ".storage"
    entries = _load(storage / "core.config_entries")["data"]["entries"]
    assert [e["domain"] for e in entries] == ["hue", "house_assistant"]
    new = plan.new_entry_id
    heating = _load(storage / f"house_assistant.{new}.heating")
    assert heating["key"] == f"house_assistant.{new}.heating"
    assert heating["data"] == STORES[f"ai_heating_assistant.{HEAT}"]
    assert (storage / f"ai_heating_assistant.{HEAT}.bak").is_file()
    assert not (storage / f"ai_heating_assistant.{HEAT}").exists()
    assert (root / "media" / "house_assistant" / WATER / "letztes.jpg").is_file()
    assert "custom:house-assistant-cover-card" in (storage / "lovelace").read_text()
    assert len(_load(storage / "lovelace_resources")["data"]["items"]) == 1
    assert "house_assistant.move_cover" in (root / "automations.yaml").read_text()
    # everything changed is in the backup
    (backup,) = (root / "house_assistant_transfer_backup").iterdir()
    assert (backup / ".storage" / "core.config_entries").read_text() == before
    assert (backup / "automations.yaml").read_text() == data.AUTOMATIONS
    # a second run finds the transfer done
    assert transfer_legacy.main(["--config", str(root), "--dry-run", "--out", str(out)]) == 1


def test_unchecked_storage_format(tmp_path: Path, capsys) -> None:
    root = _config(tmp_path / "config")
    registry = _load(root / ".storage" / "core.entity_registry")
    registry["minor_version"] = 99
    _write(root / ".storage" / "core.entity_registry", registry)
    assert transfer_legacy.main(["--config", str(root), "--dry-run", "--out", str(tmp_path)]) == 1
    assert "storage format not checked" in capsys.readouterr().err
    args = ["--config", str(root), "--dry-run", "--out", str(tmp_path), "--force"]
    assert transfer_legacy.main(args) == 0


async def test_the_transferred_entry_runs(hass: HomeAssistant, hass_storage) -> None:
    """The new modules find the converted unique ids (same entity ids, so the history
    goes on) and the learned data."""
    plan = cv.build_plan(data.config_entries(), data.entity_registry(), data.device_registry())
    new = plan.new_entry_id
    entry_data = plan.entry
    entry = MockConfigEntry(
        domain="house_assistant",
        entry_id=new,
        title=entry_data["title"],
        data=entry_data["data"],
        options=entry_data["options"],
        version=entry_data["version"],
        minor_version=entry_data["minor_version"],
        subentries_data=[
            ConfigSubentryData(
                data=s["data"],
                subentry_id=s["subentry_id"],
                subentry_type=s["subentry_type"],
                title=s["title"],
                unique_id=None,
            )
            for s in entry_data["subentries"]
        ],
    )
    entry.add_to_hass(hass)
    for old, key in plan.stores():
        hass_storage[key] = cv.store_content(
            {"version": 1, "minor_version": 1, "key": old, "data": STORES[old]}, key
        )
    # the entity registry as the transfer leaves it
    registry = er.async_get(hass)
    converted = cv.convert_entities(data.entity_registry(), plan)["data"]["entities"]
    for item in converted:
        if item["platform"] != "house_assistant":
            continue
        domain, object_id = item["entity_id"].split(".")
        registry.async_get_or_create(
            domain,
            "house_assistant",
            item["unique_id"],
            suggested_object_id=object_id,
            config_entry=entry,
            config_subentry_id=item["config_subentry_id"],
        )
    for entity_id, state in (
        ("sensor.outdoor", "5"),
        ("sensor.living_temperature", "20"),
        ("sensor.bath_temperature", "21"),
        ("input_boolean.circuit_living", "off"),
        ("input_boolean.circuit_bath", "off"),
        ("cover.living", "open"),
        ("cover.kitchen", "open"),
        ("camera.water", "idle"),
    ):
        hass.states.async_set(
            entity_id,
            state,
            {"unit_of_measurement": "°C"}
            if "temp" in entity_id or entity_id == "sensor.outdoor"
            else {},
        )
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)

    for item in converted:
        if item["platform"] == "house_assistant":
            assert hass.states.get(item["entity_id"]) is not None, item["entity_id"]
    # the learned data of the heating: the target of the bath
    assert hass.states.get("climate.bad").attributes["temperature"] == 23.5
    assert hass.states.get("sensor.wasser_zahlerstand").state == "123.456"
    modules = entry.runtime_data.modules
    assert set(modules) == {"heating", "shutter", "meter"}
    # the windows of the house with their rooms
    assert modules["heating"].coordinator.areas[BATH].cfg["window_sensors_small"] == [
        "binary_sensor.bath_window"
    ]
