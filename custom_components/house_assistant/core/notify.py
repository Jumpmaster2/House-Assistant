"""Messages of the house to the notification services of the house."""

from __future__ import annotations

from homeassistant.components import persistent_notification
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from ..const import CONF_LANGUAGE, CONF_NOTIFY, LOGGER, OPT_CORE
from ..runtime import module_options


def house_language(hass: HomeAssistant, entry: ConfigEntry) -> str:
    """Language of the messages of the house ("auto": the one of Home Assistant)."""
    language = module_options(entry, OPT_CORE).get(CONF_LANGUAGE)
    if not language or language == "auto":
        language = hass.config.language or "en"
    return "de" if str(language).startswith("de") else "en"


async def async_notify(
    hass: HomeAssistant,
    entry: ConfigEntry,
    title: str,
    message: str,
    notification_id: str | None = None,
) -> None:
    """Send to the notification services of the house; without any, the message shows
    as a notification in Home Assistant."""
    services = module_options(entry, OPT_CORE).get(CONF_NOTIFY) or []
    if not services:
        persistent_notification.async_create(
            hass, message, title=title, notification_id=notification_id
        )
        return
    for target in services:
        domain, _, service = str(target).partition(".")
        if domain != "notify" or not service:
            LOGGER.warning("%s is not a notification service, skipped", target)
            continue
        try:
            await hass.services.async_call(
                domain, service, {"title": title, "message": message}, blocking=True
            )
        except (HomeAssistantError, ValueError) as err:
            LOGGER.warning("%s failed: %s", target, err)
