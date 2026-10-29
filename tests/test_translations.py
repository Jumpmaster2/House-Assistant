"""Translation files and the panel texts generated from them."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "house_assistant"
SCRIPT = ROOT / "scripts" / "build_labels.py"
TRANSLATIONS = ("strings.json", "translations/en.json", "translations/de.json")
ALLOWED_TOP_LEVEL_KEYS = {
    "title",
    "config",
    "options",
    "selector",
    "services",
    "entity",
    "device",
    "exceptions",
    "issues",
    "config_subentries",
    "application_credentials",
    "system_health",
    "device_automation",
    "triggers",
    "conditions",
}
ALLOWED_STEP_KEYS = {
    "title",
    "description",
    "data",
    "data_description",
    "sections",
    "menu_options",
    "menu_option_descriptions",
    "submit",
    "report_issue_url",
}


def _load(name: str) -> dict[str, Any]:
    return json.loads((COMPONENT / name).read_text(encoding="utf-8"))


def _paths(data: Any, prefix: str = "") -> set[str]:
    """Every key path of a nested translation (``config.step.user.title``)."""
    if not isinstance(data, dict):
        return {prefix}
    paths: set[str] = set()
    for key, value in data.items():
        paths |= _paths(value, f"{prefix}.{key}" if prefix else key)
    return paths


def test_strings_equal_english() -> None:
    assert _load("strings.json") == _load("translations/en.json")


def test_languages_have_the_same_keys() -> None:
    assert _paths(_load("translations/de.json")) == _paths(_load("translations/en.json"))


@pytest.mark.parametrize("name", TRANSLATIONS)
def test_translation_top_level_keys(name: str) -> None:
    assert not (set(_load(name)) - ALLOWED_TOP_LEVEL_KEYS)


@pytest.mark.parametrize("name", TRANSLATIONS)
def test_translation_step_keys(name: str) -> None:
    translation = _load(name)
    flows = {"config": translation["config"], "options": translation["options"]}
    flows.update(translation["config_subentries"])
    for flow, content in flows.items():
        for step_id, step in content.get("step", {}).items():
            unknown = set(step) - ALLOWED_STEP_KEYS
            assert not unknown, (name, flow, step_id, unknown)


def test_labels_js_is_up_to_date() -> None:
    spec = importlib.util.spec_from_file_location("build_labels", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.TARGET.read_text(encoding="utf-8") == module.render(), (
        "frontend/labels.js is out of date, run python scripts/build_labels.py"
    )


def test_card_labels_js_is_up_to_date() -> None:
    spec = importlib.util.spec_from_file_location("build_labels", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.CARD_TARGET.read_text(encoding="utf-8") == module.render_cards(), (
        "frontend/card-labels.js is out of date, run python scripts/build_labels.py"
    )


def _frontend_constant(filename: str, name: str) -> str:
    """Read a declarative field list without loading browser components."""
    source = (COMPONENT / "frontend" / filename).read_text(encoding="utf-8")
    match = re.search(rf"const {name} = (.*?);\n", source, re.DOTALL)
    assert match is not None, (filename, name)
    return match[1]


def _js_array(source: str) -> list:
    """The declarative arrays use JSON literals with optional trailing commas."""
    return json.loads(re.sub(r",\s*]", "]", source))


def _builder():
    spec = importlib.util.spec_from_file_location("build_labels", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("language", ("de", "en"))
def test_heating_room_groups_have_labels(language: str) -> None:
    translation = _load(f"translations/{language}.json")
    sections = translation["config_subentries"]["room"]["step"]["reconfigure"]["sections"]
    labels = _builder().heating_labels(translation)
    groups = _js_array(_frontend_constant("heating.js", "AREA_GROUPS"))
    assert groups
    for section, fields, _collapsed in groups:
        assert sections[section]["name"].strip(), (language, section)
        assert labels["sections"][section][0].strip(), (language, section)
        assert fields
        for key in fields:
            assert sections[section]["data"][key].strip(), (language, section, key)
            table = labels["learned"] if section == "learned_values" else labels["fields"]
            assert table[key][0].strip(), (language, section, key)
        if section in ("airing", "start_values"):
            for key in fields:
                assert sections[section]["data_description"][key].strip(), (language, key)
    # Start values share keys with learned values; keep the existing editor's labels.
    for key, name in sections["learned_values"]["data"].items():
        assert labels["fields"][key][0] == name


@pytest.mark.parametrize("language", ("de", "en"))
@pytest.mark.parametrize("kind", ("room", "window"))
def test_house_editor_fields_have_labels(language: str, kind: str) -> None:
    labels = _builder().house_labels(_load(f"translations/{language}.json"))
    fields = _js_array(_frontend_constant("house.js", f"{kind.upper()}_FIELDS"))
    assert fields
    source = (COMPONENT / "frontend" / "house.js").read_text(encoding="utf-8")
    # Geometry fields use the local UI labels, just as house.js label() does.
    local = source.split("\n  en: {", 1)[0 if language == "de" else 1]
    for key in ["name", *fields]:
        label = labels["fields"][kind].get(key)
        if label is None:
            match = re.search(rf"^      {key}: (\[[^\n]*\]),$", local, re.MULTILINE)
            assert match is not None, (language, kind, key)
            label = _js_array(match[1])
        assert label[0].strip(), (language, kind, key)


@pytest.mark.parametrize("language", ("de", "en"))
def test_heating_settings_cards_have_labels(language: str) -> None:
    labels = _builder().heating_labels(_load(f"translations/{language}.json"))
    settings = _frontend_constant("heating.js", "SETTINGS")
    cards = re.findall(r"\{[^{}]*\}", settings)
    assert cards
    for card in cards:
        field_list = re.search(r"fields: (\[[^\]]*\])", card)
        if field_list:
            fields = _js_array(field_list[1])
            assert fields
            for key in fields:
                assert labels["fields"][key][0].strip(), (language, key)
        else:
            special = re.search(r'special: "(\w+)"', card)
            assert special is not None, card
            assert special[1] in {"apikey", "theta", "limits", "prompts"}, card
    # Special cards use these translated fields instead of a declarative field list.
    for key in ("api_key", "theta"):
        assert labels["fields"][key][0].strip(), (language, key)
    assert labels["limits"]
    assert all(name.strip() for name in labels["limits"].values())
    for key in ("min", "max", "step"):
        assert labels["limit_columns"][key].strip(), (language, key)


@pytest.mark.parametrize("language", ("de", "en"))
def test_stale_sensor_setting_has_name_and_help(language: str) -> None:
    translation = _load(f"translations/{language}.json")
    step = translation["options"]["step"]["heating_rules"]
    assert step["data"]["sensor_stale_hours"].strip()
    assert step["data_description"]["sensor_stale_hours"].strip()
    label = _builder().heating_labels(translation)["fields"]["sensor_stale_hours"]
    assert label[0].strip() and label[1].strip()


@pytest.mark.parametrize("language", ("de", "en"))
def test_stale_issue_describes_room_sensor_and_hours(language: str) -> None:
    issue = _load(f"translations/{language}.json")["issues"]["sensor_stale"]
    placeholders = {"area": "Room A", "entity_id": "sensor.room_a", "hours": "12"}
    assert "Room A" in issue["title"].format(**placeholders)
    description = issue["description"].format(**placeholders)
    assert "sensor.room_a" in description and "12" in description
