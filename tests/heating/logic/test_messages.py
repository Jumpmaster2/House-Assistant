"""The logbook messages of the heating show readable values."""

from __future__ import annotations

from custom_components.house_assistant.heating.messages import label_of, text


def test_logbook_shows_readable_values() -> None:
    msg = text(
        "de",
        "heating_day",
        decision="ja",
        source=label_of("de", "source", "rule_fallback"),
        phase=label_of("de", "phase", "ai_leads"),
        reason="",
    )
    assert "Regel ohne KI" in msg and "KI führt" in msg
    assert label_of("en", "error", "A") == "too cold without heating"
    assert label_of("en", "need", "unclear") == "unclear"
    assert label_of("en", "source", "something_new") == "something_new"  # unknown: as is
