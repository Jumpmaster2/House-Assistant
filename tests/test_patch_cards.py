"""Offline dashboard patching preserves entities and produces renderable card text."""

import importlib.util
from pathlib import Path

import pytest
from jinja2 import Environment

spec = importlib.util.spec_from_file_location(
    "patch_cards", Path(__file__).resolve().parents[1] / "scripts/patch_cards.py"
)
patcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patcher)


@pytest.mark.parametrize(
    ("reason", "state", "text"),
    [
        ("mould_limit", "ventilate_now", "Innen 66 % feucht, draußen trockener: 5 min stoßlüften."),
        ("airing_running", "airing", "Lüften läuft, noch 3 min."),
        ("target_reached", "close_window", "Ziel erreicht, Fenster schließen."),
        (
            "below_threshold_save_heat",
            "close_window",
            "66 % ist in Ordnung, Fenster zu spart Heizenergie.",
        ),
        (
            "pause_after_airing",
            "do_not_ventilate",
            "Kurz nach dem Lüften, Feuchte setzt sich noch.",
        ),
    ],
)
def test_card_reasons_and_entities(reason, state, text) -> None:
    content = """### Schlafzimmer: {{ states('sensor.advice') }}
{% set a = 'sensor.advice' %}{% set rf = states('sensor.original_humidity') %} Jetzt lüften"""
    card = {
        "type": "conditional",
        "conditions": [{"entity": "sensor.advice", "state": "ventilate_now"}],
        "card": {"type": "markdown", "content": content},
    }
    unrelated = {"type": "markdown", "content": "Weather"}
    document = {"cards": [card, unrelated]}
    assert patcher.patch_dashboard(document) == ["/cards/0/card"]
    assert unrelated["content"] == "Weather"
    assert card["conditions"][0]["state"] == ["ventilate_now", "airing"]
    attrs = {"reason": reason, "airing_minutes": 5, "airing_minutes_left": 3}
    rendered = (
        Environment()
        .from_string(card["card"]["content"])
        .render(
            states=lambda entity: (
                state
                if entity == "sensor.advice"
                else "66.4"
                if entity == "sensor.original_humidity"
                else "ERROR"
            ),
            state_attr=lambda entity, key: attrs.get(key) if entity == "sensor.advice" else None,
        )
    )
    assert text in rendered
    assert "### Schlafzimmer:" in rendered
    assert "ERROR" not in rendered
    assert "—" not in rendered and "–" not in rendered


def test_ambiguous_ventilation_card_fails_instead_of_guessing_sensor() -> None:
    with pytest.raises(ValueError):
        patcher.patch_dashboard({"type": "markdown", "content": "### Room: Jetzt lüften"})
