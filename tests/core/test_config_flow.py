"""Setting up the single entry of the integration."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.house_assistant.const import DOMAIN, NAME


async def _create(hass: HomeAssistant) -> dict:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    return await hass.config_entries.flow.async_configure(result["flow_id"], {})


async def test_user_flow_creates_the_entry(hass: HomeAssistant) -> None:
    result = await _create(hass)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == NAME
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED


async def test_only_one_entry(hass: HomeAssistant) -> None:
    await _create(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_unload(hass: HomeAssistant) -> None:
    await _create(hass)
    entry = hass.config_entries.async_entries(DOMAIN)[0]
    await hass.async_block_till_done()
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED
