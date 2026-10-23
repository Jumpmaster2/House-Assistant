"""Fixtures for tests with a Home Assistant test instance."""

from __future__ import annotations

import pytest

pytest.importorskip("pytest_homeassistant_custom_component")


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable loading of custom integrations."""
    return
