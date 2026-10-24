"""Sidebar panel and dashboard cards.

The cards have to be there whenever a dashboard is drawn, and a dashboard can open
before House Assistant runs: Home Assistant starts its frontend first and custom
integrations last, and the companion app keeps its page across restarts. A browser
remembers a failed module load per address until the page is reloaded. Hence:

* the files are served and the cards added as an extra module of the frontend when the
  integration is set up (``async_setup``), before any module starts; an open page is
  told about a new extra module and loads it then;
* the dashboard resource (for pages that load only the resources of a dashboard) has
  an address of its own, so a resource requested too early does not block the extra
  module;
* every file lies below a folder with the version: after an update no page mixes old
  and new files, and the files may be cached.
"""

from __future__ import annotations

from pathlib import Path

from homeassistant.core import HomeAssistant

from ..const import DOMAIN, LOGGER, NAME

PANEL_URL_PATH = "house-assistant"
PANEL_COMPONENT = "house-assistant-panel"
STATIC_URL = f"/{DOMAIN}_static"
# the cards as an extra module of the frontend and as a dashboard resource
CARDS = "cards.js"
CARDS_RESOURCE = "cards-resource.js"
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
DATA_STATIC = f"{DOMAIN}_static_registered"
DATA_SIDEBAR = f"{DOMAIN}_panel_in_sidebar"
DATA_CARD = f"{DOMAIN}_card_url"
DATA_RESOURCE = f"{DOMAIN}_card_resource"


def _has_frontend(hass: HomeAssistant) -> bool:
    return "frontend" in hass.config.components and hass.http is not None


async def async_register_frontend(hass: HomeAssistant) -> str | None:
    """Serve the files and load the cards on every dashboard for every user. Returns
    the folder with the version, None without a frontend (tests)."""
    if not _has_frontend(hass):
        return None
    from homeassistant.components import frontend
    from homeassistant.components.http import StaticPathConfig

    # a path can only be registered once per run: keep the version
    folder = hass.data.get(DATA_STATIC)
    if folder is None:
        folder = f"{STATIC_URL}/{await hass.async_add_executor_job(_version)}"
        await hass.http.async_register_static_paths(
            [StaticPathConfig(folder, str(FRONTEND_DIR), cache_headers=True)]
        )
        hass.data[DATA_STATIC] = folder
    if hass.data.get(DATA_CARD) is None:
        hass.data[DATA_CARD] = f"{folder}/{CARDS}"
        frontend.add_extra_js_url(hass, hass.data[DATA_CARD])
    resource = f"{folder}/{CARDS_RESOURCE}"
    if hass.data.get(DATA_RESOURCE) != resource:
        await async_set_card_resource(hass, resource)
        hass.data[DATA_RESOURCE] = resource
    return folder


async def async_unregister_cards(hass: HomeAssistant) -> None:
    """The entry is deleted: the cards go from the dashboards."""
    if _has_frontend(hass) and (card := hass.data.pop(DATA_CARD, None)):
        from homeassistant.components import frontend

        frontend.remove_extra_js_url(hass, card)
    hass.data.pop(DATA_RESOURCE, None)
    await async_set_card_resource(hass, None)


async def async_register_panel(hass: HomeAssistant, entry_id: str, sidebar: bool = True) -> None:
    """Register the panel (only when the frontend runs, not in tests).

    ``config_panel_domain`` makes the configure button of the integration open the panel
    instead of the options dialog. Without ``sidebar`` the panel has no entry in the
    sidebar but stays reachable from the integration page.
    """
    folder = await async_register_frontend(hass)
    if folder is None:
        return
    from homeassistant.components import frontend, panel_custom

    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        if hass.data.get(DATA_SIDEBAR) == sidebar:
            return
        frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=PANEL_URL_PATH,
        webcomponent_name=PANEL_COMPONENT,
        module_url=f"{folder}/panel.js",
        sidebar_title=NAME if sidebar else None,
        sidebar_icon="mdi:home-automation" if sidebar else None,
        require_admin=True,
        config={"entry_id": entry_id, "version": folder.rsplit("/", 1)[-1]},
        config_panel_domain=DOMAIN,
    )
    hass.data[DATA_SIDEBAR] = sidebar


def async_unregister_panel(hass: HomeAssistant) -> None:
    """The panel goes (the cards stay while the entry exists)."""
    if "frontend" not in hass.config.components:
        return
    from homeassistant.components import frontend

    if frontend.async_panel_exists(hass, PANEL_URL_PATH):
        frontend.async_remove_panel(hass, PANEL_URL_PATH, warn_if_unknown=False)
    hass.data.pop(DATA_SIDEBAR, None)


def _version() -> str:
    try:
        stamp = max(int(p.stat().st_mtime) for p in FRONTEND_DIR.rglob("*.js"))
    except (OSError, ValueError):
        LOGGER.debug("Frontend files not found")
        stamp = 0
    return str(stamp)


def _ours(url: str) -> bool:
    """A dashboard resource of these cards (of any version)."""
    path = url.split("?")[0]
    return path.startswith(f"{STATIC_URL}/") and path.rsplit("/", 1)[-1] in (CARDS, CARDS_RESOURCE)


async def async_set_card_resource(hass: HomeAssistant, url: str | None) -> None:
    """Keep the cards as a dashboard resource (None removes it).

    Some pages (the companion app, a cast device) load only the resources of a
    dashboard, not the extra modules of the frontend. Only for resources managed in
    the UI (storage mode).
    """
    try:
        from homeassistant.components.lovelace.const import LOVELACE_DATA
    except ImportError:
        return
    data = hass.data.get(LOVELACE_DATA)
    if data is None or getattr(data, "resource_mode", None) != "storage":
        return
    resources = data.resources
    try:
        if not resources.loaded:
            await resources.async_load()
            resources.loaded = True
        ours = [i for i in resources.async_items() if _ours(i.get("url", ""))]
        for item in ours[1:] if url else ours:
            await resources.async_delete_item(item["id"])
        if not url:
            return
        if not ours:
            await resources.async_create_item({"res_type": "module", "url": url})
        elif ours[0].get("url") != url:
            await resources.async_update_item(ours[0]["id"], {"res_type": "module", "url": url})
    except Exception:  # the cards are optional, the control must not fail
        LOGGER.warning("Could not register the dashboard cards as a dashboard resource")
