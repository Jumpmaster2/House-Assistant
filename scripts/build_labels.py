"""Build frontend/labels.js for the panel from the translation files.

The panel shows the same names and help texts as the dialogs, so every text stays
in one place. Fields are kept per dialog step: the modules use the same keys with
different meanings (``weather``, ``window_sensors``). Run after changing a
translation (a test checks that the file is current):

    python scripts/build_labels.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
COMPONENT = ROOT / "custom_components" / "house_assistant"
TARGET = COMPONENT / "frontend" / "labels.js"
LANGUAGES = ("de", "en")
HEADER = (
    "// Generated from the translation files by scripts/build_labels.py, do not edit by hand.\n"
)


def _fields(step: dict[str, Any]) -> dict[str, list[str]]:
    """Field key -> [name, help] of one step or section."""
    helps = step.get("data_description", {})
    return {key: [name, helps.get(key, "")] for key, name in step.get("data", {}).items()}


def _step(step: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": step.get("title", ""),
        "fields": _fields(step),
        "sections": {
            key: {
                "name": section.get("name", ""),
                "description": section.get("description", ""),
                "fields": _fields(section),
            }
            for key, section in step.get("sections", {}).items()
        },
    }


def _flows(translation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """The dialogs by name: ``config``, ``options`` and every subentry type."""
    flows = {"config": translation.get("config", {}), "options": translation.get("options", {})}
    flows.update(translation.get("config_subentries", {}))
    return flows


def labels(translation: dict[str, Any]) -> dict[str, Any]:
    flows = _flows(translation)
    states: dict[str, dict[str, str]] = {}
    for platform, entities in translation.get("entity", {}).items():
        for key, entity in entities.items():
            if "state" in entity:
                states[f"{platform}.{key}"] = entity["state"]
            for attribute, values in entity.get("state_attributes", {}).items():
                if "state" in values:
                    states[f"{platform}.{key}.{attribute}"] = values["state"]
    return {
        "steps": {
            f"{flow}.{step_id}": _step(step)
            for flow, content in flows.items()
            for step_id, step in content.get("step", {}).items()
        },
        "errors": {flow: content["error"] for flow, content in flows.items() if "error" in content},
        "choices": {
            key: value["options"]
            for key, value in sorted(translation.get("selector", {}).items())
            if "options" in value
        },
        "states": states,
    }


def render() -> str:
    data = {}
    for language in LANGUAGES:
        path = COMPONENT / "translations" / f"{language}.json"
        data[language] = labels(json.loads(path.read_text(encoding="utf-8")))
    return f"{HEADER}export const LABELS = {json.dumps(data, ensure_ascii=False, indent=1)};\n"


def main() -> int:
    content = render()
    if "--check" in sys.argv:
        current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if current != content:
            print(f"{TARGET.relative_to(ROOT)} is out of date, run python scripts/build_labels.py")
            return 1
        return 0
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(content, encoding="utf-8")
    print(f"Wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
