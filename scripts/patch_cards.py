#!/usr/bin/env python3
"""Patch local dashboard backups only; no Home Assistant connection.

Usage: python3 patch_cards.py [backup-directory] [--output-dir directory]
Defaults to the directory containing this script, so it can be copied beside backups.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

STATES = {
    "ventilate_now": "Jetzt lüften",
    "airing": "Lüften läuft",
    "ventilation_useful": "Lüften sinnvoll",
    "do_not_ventilate": "Nicht lüften",
    "close_window": "Fenster schließen",
    "blocked": "Lüften gesperrt",
    "optimal": "Alles optimal",
    "vacation": "Urlaub",
    "unknown": "Unbekannt",
    "unavailable": "Unbekannt",
}
# Literal Jinja, interpolated only through explicit placeholders.
TEMPLATE = """{% set a = __ADVICE__ %}{% set s = states(a) %}{% set t = __STATES__ %}
### __ROOM__: {{ t.get(s, 'Unbekannt') }}
{% set reason = state_attr(a, 'reason') %}
{% set rh = states(__HUMIDITY__) %}
{% set minutes = state_attr(a, 'airing_minutes') %}
{% set left = state_attr(a, 'airing_minutes_left') %}
{% if s in ['unknown', 'unavailable'] %}Keine Messwerte.
{% elif reason in ['mould_limit', 'humid_short_airing'] %}Innen {{ rh | float(0) | round(0) | int }} % feucht, __REFERENCE__ trockener: {{ minutes if minutes is not none else '?' }} min stoßlüften.
{% elif reason == 'airing_running' %}Lüften läuft{% if left is not none %}, noch {{ left }} min{% endif %}.
{% elif reason == 'target_reached' %}Ziel erreicht, Fenster schließen.
{% elif reason == 'airing_time_over' %}Lüftzeit vorbei, Fenster schließen.
{% elif reason == 'below_threshold_save_heat' %}{{ rh | float(0) | round(0) | int }} % ist in Ordnung, Fenster zu spart Heizenergie.
{% elif reason == 'outside_not_drier' %}__REFERENCE_CAP__ nicht trockener, Lüften hilft nicht.
{% elif reason == 'outside_warmer' %}__REFERENCE_CAP__ wärmer, Fenster schließen.
{% elif reason == 'pause_after_airing' %}Kurz nach dem Lüften, Feuchte setzt sich noch.
{% elif reason == 'little_effect' %}Lüften senkt die Feuchte gerade zu wenig.
{% elif reason == 'cooling' %}Lüften kühlt den Raum.
{% elif reason == 'blocked' %}Lüften ist gesperrt.
{% elif reason == 'vacation' %}Lüftungsempfehlung ruht im Urlaub.
{% elif reason == 'optimal' %}{{ rh | float(0) | round(0) | int }} % ist in Ordnung.
{% else %}Keine Messwerte.{% endif %}"""


def replace_content(content: str) -> tuple[str, str] | None:
    """Keep the original room, advice entity and humidity entity; fail if ambiguous."""
    if "lüften" not in content.lower() and "ventilate_now" not in content:
        return None
    room = re.search(r"^\s*#{1,6}\s+([^:\n]+):", content)
    advice = re.search(r"set\s+a\s*=\s*(['\"])(sensor\.[^'\"]+)\1", content)
    humidity = re.search(r"set\s+rf\s*=\s*states\(\s*(['\"])(sensor\.[^'\"]+)\1\s*\)", content)
    if not (room and advice and humidity):
        raise ValueError(
            "Ventilation markdown lacks room heading or explicit advice/humidity entity"
        )
    reference = "Wohnbereich" if "Wohnbereich trockener" in content else "draußen"
    result = TEMPLATE
    for key, value in {
        "__ROOM__": room[1],
        "__ADVICE__": repr(advice[2]),
        "__HUMIDITY__": repr(humidity[2]),
        "__STATES__": repr(STATES),
        "__REFERENCE__": reference,
        "__REFERENCE_CAP__": reference.capitalize(),
    }.items():
        result = result.replace(key, value)
    return result, advice[2]


def patch_dashboard(document: Any) -> list[str]:
    """Update markdown and the conditional state that displays it, in place."""
    changes: list[str] = []

    def visit(node: Any, path: str) -> set[str]:
        entities: set[str] = set()
        if isinstance(node, dict):
            if node.get("type") == "markdown":
                patched = replace_content(node.get("content", ""))
                if patched:
                    node["content"], entity = patched
                    changes.append(path)
                    entities.add(entity)
            for key, value in node.items():
                entities.update(visit(value, f"{path}/{key}"))
            if node.get("type") == "conditional" and entities:
                # HA's state condition accepts a list, preserving the other conditions.
                for condition in node.get("conditions", []):
                    if (
                        condition.get("entity") in entities
                        and condition.get("state") == "ventilate_now"
                    ):
                        condition["state"] = ["ventilate_now", "airing"]
        elif isinstance(node, list):
            for index, value in enumerate(node):
                entities.update(visit(value, f"{path}/{index}"))
        return entities

    visit(document, "")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = args.output_dir or args.directory
    output.mkdir(parents=True, exist_ok=True)
    report = {}
    # Read and validate both dashboards before writing any output.
    documents = {}
    for name in ("dashboard-home", "dashboard-wohnbereich"):
        source = args.directory / f"backup-{name}.json"
        document = json.loads(source.read_text(encoding="utf-8"))
        report[name] = patch_dashboard(document)
        documents[name] = document
    for name, document in documents.items():
        destination = output / f"patched-{name}.json"
        destination.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{destination}: {len(report[name])} geänderte Karten")
        for path in report[name]:
            print(f"  {path}")
    (output / "changed-cards.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
