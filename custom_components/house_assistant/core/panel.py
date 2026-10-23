"""Sidebar panel: one page for the whole house, every module as a section."""

from __future__ import annotations

from pathlib import Path

from homeassistant.core import HomeAssistant

from ..const import DOMAIN, LOGGER, NAME

PANEL_URL_PATH = "house-assistant"
PANEL_COMPONENT = "house-assistant-panel"
PANEL_STATIC_URL = f"/{DOMAIN}_panel"
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
DATA_STATIC = f"{DOMAIN}_static_registered"


async def async_register_panel(hass: HomeAssistant, entry_id: str) -> None:
    """Register the panel (only when the frontend runs, not in tests)."""
    if "frontend" not in hass.config.components or hass.http is None:
        return
    from homeassistant.components import frontend, panel_custom
    from homeassistant.components.http import StaticPathConfig

    # The panel is served below a path with the version, so its imports (labels.js, the
    # views of the modules) are new after an update as well. A path can only be
    # registered once per run: keep the version.
    version = hass.data.get(DATA_STATIC)
    if version is None:
        version = await hass.async_add_executor_job(_version)
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    f"{PANEL_STATIC_URL}/{version}", str(FRONTEND_DIR), cache_headers=False
                )
            ]
        )
        hass.data[DATA_STATIC] = version
    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        return
    # config_panel_domain: "Configure" on the integration page opens this panel.
    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=PANEL_URL_PATH,
        webcomponent_name=PANEL_COMPONENT,
        module_url=f"{PANEL_STATIC_URL}/{version}/panel.js",
        sidebar_title=NAME,
        sidebar_icon="mdi:home-automation",
        require_admin=True,
        config={"entry_id": entry_id, "version": version},
        config_panel_domain=DOMAIN,
    )


def async_unregister_panel(hass: HomeAssistant) -> None:
    if "frontend" not in hass.config.components:
        return
    from homeassistant.components import frontend

    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)


def _version() -> str:
    try:
        stamp = max(int(p.stat().st_mtime) for p in FRONTEND_DIR.rglob("*.js"))
    except (OSError, ValueError):
        LOGGER.debug("Frontend files not found")
        stamp = 0
    return str(stamp)
