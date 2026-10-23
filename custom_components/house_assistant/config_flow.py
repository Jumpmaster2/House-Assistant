"""Config flow: one entry for the whole house."""

from __future__ import annotations

from typing import Any

import probatio as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN, NAME


class HouseAssistantConfigFlow(ConfigFlow, domain=DOMAIN):
    """Create the single entry of the integration."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=NAME, data={}, options={})
        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
