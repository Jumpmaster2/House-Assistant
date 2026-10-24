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


def _add(fields: dict[str, list[str]], step: dict[str, Any]) -> None:
    fields.update({key: value for key, value in _fields(step).items() if key not in fields})


def meter_labels(translation: dict[str, Any]) -> dict[str, Any]:
    """Texts of the meter section, in the form its view (the former panel) reads them."""
    fields: dict[str, list[str]] = {}
    _add(fields, translation["options"]["step"]["meter"])
    meter = translation["config_subentries"]["meter"]
    _add(fields, meter["step"]["user"])
    details = meter["step"]["details"]
    for sec in details["sections"].values():
        _add(fields, sec)
    selectors = translation["selector"]
    return {
        # options of the other select fields, under their translation key
        "external_light_mode": selectors["external_light_mode"]["options"],
        "fields": fields,
        "sections": {
            k: [v["name"], v.get("description", "")] for k, v in details["sections"].items()
        },
        "errors": meter["error"],
        "status": translation["entity"]["sensor"]["meter_status"]["state"],
        "types": selectors["meter_type"]["options"],
    }


SHUTTER_CHOICES = (
    "language",
    "morning_mode",
    "morning_sun_event",
    "override_trigger",
    "weekday",
    "forecast_type",
    "service_action",
    "window_size",
)


def _shutter_steps(translation: dict[str, Any]) -> list[dict[str, Any]]:
    """Steps and sections of the cover dialogs that contain fields."""
    steps = [
        step
        for flow in ("config", "options")
        for key, step in translation[flow]["step"].items()
        if key.startswith("shutter")
    ]
    for sub in ("group", "window"):
        steps.extend(translation["config_subentries"][sub]["step"].values())
    found: list[dict[str, Any]] = []
    for step in steps:
        found.append(step)
        found.extend(step.get("sections", {}).values())
    return found


def shutter_labels(translation: dict[str, Any]) -> dict[str, Any]:
    """Texts of the cover section, in the form its view and the card read them. The
    same field has the same text in every cover dialog."""
    fields: dict[str, list[str]] = {}
    for step in _shutter_steps(translation):
        for key, (name, help_text) in _fields(step).items():
            if key not in fields:
                fields[key] = [name, help_text]
                continue
            known = fields[key]
            if known[0] != name or (help_text and known[1] and known[1] != help_text):
                raise ValueError(f"Field {key} has different texts: {known} / {[name, help_text]}")
            if help_text and not known[1]:
                known[1] = help_text
    sensor = translation["entity"]["sensor"]
    return {
        "LABELS": dict(sorted(fields.items())),
        "CHOICES": {
            key: translation["selector"][key]["options"] for key in sorted(SHUTTER_CHOICES)
        },
        "ERRORS": translation["config"]["error"],
        "STATUS": sensor["window_status"]["state"],
        "NEXT_ACTION": sensor["next_action"]["state_attributes"]["action"]["state"],
    }


HEATING_STEPS = ("general", "vacation", "rules", "ventilation", "ai", "decision")


def heating_labels(translation: dict[str, Any]) -> dict[str, Any]:
    """Texts of the heating section, in the form its view (the former panel) reads them.
    Field names and help texts come from the options dialog and the room dialog."""
    fields: dict[str, list[str]] = {}
    options = translation["options"]["step"]
    for step in HEATING_STEPS:
        _add(fields, options[f"heating_{step}"])
        for sec in options[f"heating_{step}"].get("sections", {}).values():
            _add(fields, sec)
    setup_ai = translation["config"]["step"]["heating_ai"]
    fields["api_key"] = [
        setup_ai["data"]["api_key"],
        setup_ai.get("data_description", {}).get("api_key", ""),
    ]
    room = translation["config_subentries"]["room"]
    area = room["step"]["user"]
    _add(fields, area)
    for sec in area["sections"].values():
        _add(fields, sec)
    # an existing room shows its learned values instead of the start values
    learned_section = room["step"]["reconfigure"]["sections"]["learned_values"]
    learned: dict[str, list[str]] = {}
    _add(learned, learned_section)
    entity = translation["entity"]
    limits = options["heating_ai_limits"]["sections"]
    return {
        "fields": fields,
        "learned": learned,
        "sections": {
            **{k: [v["name"], v.get("description", "")] for k, v in area["sections"].items()},
            "learned_values": [learned_section["name"], learned_section.get("description", "")],
        },
        "limits": {k: v["name"] for k, v in limits.items()},
        "limit_columns": next(iter(limits.values()))["data"],
        "errors": translation["options"]["error"],
        "area_errors": room["error"],
        "states": {
            "status": entity["sensor"]["room_status"]["state"],
            "ventilation": entity["sensor"]["ventilation"]["state"],
            "phase": entity["sensor"]["decision_phase"]["state"],
            "override": entity["select"]["heating_day_override"]["state"],
        },
        "effort": translation["selector"]["effort"]["options"],
        "heating_type": translation["selector"]["heating_type"]["options"],
    }


def house_labels(translation: dict[str, Any]) -> dict[str, Any]:
    """Texts of the house section: the fields of a room and of the basics of a window."""
    room = translation["config_subentries"]["room"]
    window = translation["config_subentries"]["window"]
    room_fields: dict[str, list[str]] = {}
    step = room["step"]["user"]
    _add(room_fields, step)
    for sec in step["sections"].values():
        _add(room_fields, sec)
    window_fields: dict[str, list[str]] = {}
    _add(window_fields, window["step"]["basics"])
    return {
        "fields": {"room": room_fields, "window": window_fields},
        "errors": {**room["error"], **window["error"]},
        "sizes": translation["selector"]["window_size"]["options"],
    }


# name of the export -> texts in the form one section of the panel reads them
SECTIONS = {
    "LABELS": labels,
    "HOUSE": house_labels,
    "HEATING": heating_labels,
    "SHUTTER": shutter_labels,
    "METER": meter_labels,
}


def render() -> str:
    data: dict[str, dict[str, Any]] = {name: {} for name in SECTIONS}
    for language in LANGUAGES:
        path = COMPONENT / "translations" / f"{language}.json"
        translation = json.loads(path.read_text(encoding="utf-8"))
        for name, build in SECTIONS.items():
            data[name][language] = build(translation)
    # the cover section reads every kind of text by language: SHUTTER.LABELS.de
    data["SHUTTER"] = {
        kind: {language: data["SHUTTER"][language][kind] for language in LANGUAGES}
        for kind in data["SHUTTER"][LANGUAGES[0]]
    }
    parts = [HEADER]
    for name, value in data.items():
        parts.append(f"export const {name} = {json.dumps(value, ensure_ascii=False, indent=1)};\n")
    return "".join(parts)


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
