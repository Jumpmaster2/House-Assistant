"""The dashboard cards (one bundle for all modules) as a dashboard resource."""

from __future__ import annotations

from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from custom_components.house_assistant.core.panel import async_set_card_resource

V1 = "/house_assistant_static/1/cards-resource.js"
V2 = "/house_assistant_static/2/cards-resource.js"


async def _urls(hass: HomeAssistant) -> list[str]:
    return [item["url"] for item in hass.data[LOVELACE_DATA].resources.async_items()]


async def test_card_resource_is_added_updated_and_removed(hass: HomeAssistant) -> None:
    assert await async_setup_component(hass, "lovelace", {})
    resources = hass.data[LOVELACE_DATA].resources
    await resources.async_load()
    resources.loaded = True
    await resources.async_create_item({"res_type": "module", "url": "/local/other.js"})
    # an entry of an older version (shared address with the extra module) is replaced
    await resources.async_create_item(
        {"res_type": "module", "url": "/house_assistant_static/cards.js?v=1"}
    )

    await async_set_card_resource(hass, V1)
    assert await _urls(hass) == ["/local/other.js", V1]

    # a new version replaces the entry instead of adding a second one
    await async_set_card_resource(hass, V2)
    assert await _urls(hass) == ["/local/other.js", V2]
    assert resources.async_items()[1]["type"] == "module"

    await async_set_card_resource(hass, None)
    assert await _urls(hass) == ["/local/other.js"]


async def test_card_resource_without_lovelace(hass: HomeAssistant) -> None:
    await async_set_card_resource(hass, V1)  # nothing to do, no error
