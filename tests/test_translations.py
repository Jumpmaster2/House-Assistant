"""Translation files and the panel texts generated from them."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "house_assistant"
SCRIPT = ROOT / "scripts" / "build_labels.py"


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
