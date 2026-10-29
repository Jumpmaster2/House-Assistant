"""Translation files and the panel texts generated from them."""

from __future__ import annotations

import importlib.util
import json
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
