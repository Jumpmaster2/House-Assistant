"""Form helpers shared by the dialogs and the panel of every module.

The selectors of the dialogs are the single source of truth: the panel gets them
serialised (types, ranges, domains) and its input is checked with them.
"""

from __future__ import annotations

from typing import Any

import probatio as vol
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    Selector,
)


def number(minimum: float, maximum: float, step: float, unit: str | None = None) -> NumberSelector:
    config = NumberSelectorConfig(min=minimum, max=maximum, step=step, mode=NumberSelectorMode.BOX)
    if unit:
        config["unit_of_measurement"] = unit
    return NumberSelector(config)


def entity(domains: list[str] | None = None, multiple: bool = False) -> EntitySelector:
    config = EntitySelectorConfig(multiple=multiple)
    if domains:
        config["domain"] = domains
    return EntitySelector(config)


def optional(key: str, values: dict[str, Any]) -> vol.Optional:
    """Optional field that can be cleared again."""
    return vol.Optional(key, description={"suggested_value": values.get(key)})


def fields(schema: vol.Schema) -> dict[str, Selector]:
    """Field key -> selector of a form."""
    return {str(marker): value for marker, value in schema.schema.items()}


def spec(selector: Selector) -> dict[str, Any]:
    """A selector as the panel needs it: its kind and its configuration."""
    kind, config = next(iter(selector.serialize()["selector"].items()))
    return {"selector": kind, **dict(config)}


class PanelError(Exception):
    """Error key for the panel, optionally with the field it belongs to."""

    def __init__(self, code: str, field: str | None = None) -> None:
        super().__init__(f"{code}:{field}" if field else code)


def coerce(selector: Selector, value: Any) -> Any:
    """Value of a panel field checked by its selector (None for an empty field)."""
    if isinstance(value, str):
        value = value.strip()
    if value is None or value == "":
        return None
    return selector(value)
