"""Registration of the sidebar panel and of the dashboard cards."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN


async def _frontend(hass: HomeAssistant) -> AsyncMock:
    """A running frontend: the static paths are recorded instead of served."""
    assert await async_setup_component(hass, "http", {})
    hass.config.components.add("frontend")
    register = AsyncMock()
    hass.http.async_register_static_paths = register
    return register


async def _setup(hass: HomeAssistant, **core) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN, title="House Assistant", data={}, options={"core": {"modules": [], **core}}
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_panel_registered_as_configure_page(hass: HomeAssistant) -> None:
    static_paths = await _frontend(hass)
    with (
        patch("homeassistant.components.frontend.async_panel_exists", return_value=False),
        patch("homeassistant.components.panel_custom.async_register_panel") as register,
        patch("homeassistant.components.frontend.add_extra_js_url") as add_js,
    ):
        await _setup(hass)

    # the dashboard cards are loaded for every user, below a folder with the version
    card = add_js.call_args.args[1]
    assert card.startswith("/house_assistant_static/") and card.endswith("/cards.js")
    kwargs = register.call_args.kwargs
    # the configure button of the integration opens the panel
    assert kwargs["config_panel_domain"] == DOMAIN
    assert kwargs["frontend_url_path"] == "house-assistant"
    assert kwargs["webcomponent_name"] == "house-assistant-panel"
    assert kwargs["require_admin"] is True
    assert kwargs["sidebar_title"] == "House Assistant"
    # the panel in the same folder, so its imports are new after an update as well
    assert kwargs["module_url"] == card.replace("/cards.js", "/panel.js")
    (config,) = static_paths.call_args.args[0]
    assert config.url_path == card.removesuffix("/cards.js")
    # the version is in the path: the files may be cached
    assert config.cache_headers is True
    for name in (
        "panel.js",
        "labels.js",
        "cards.js",
        "cards-resource.js",
        "card-labels.js",
        "meter.js",
        "shutter.js",
        "cover-card.js",
    ):
        assert (Path(config.path) / name).is_file(), name


async def test_panel_without_sidebar(hass: HomeAssistant) -> None:
    await _frontend(hass)
    with (
        patch("homeassistant.components.frontend.async_panel_exists", return_value=False),
        patch("homeassistant.components.panel_custom.async_register_panel") as register,
        patch("homeassistant.components.frontend.add_extra_js_url") as add_js,
    ):
        await _setup(hass, show_panel=False)
    # the cards are there also without the sidebar entry
    add_js.assert_called_once()
    kwargs = register.call_args.kwargs
    assert kwargs["sidebar_title"] is None
    assert kwargs["config_panel_domain"] == DOMAIN


async def test_no_panel_without_frontend(hass: HomeAssistant) -> None:
    with patch("homeassistant.components.panel_custom.async_register_panel") as register:
        await _setup(hass)
    register.assert_not_called()


async def test_cards_before_the_modules_and_until_the_entry_is_removed(
    hass: HomeAssistant,
) -> None:
    """A dashboard may be open before the integration runs: the cards come with the
    setup of the integration, not after the modules started; an unload keeps them."""
    await _frontend(hass)
    entry = MockConfigEntry(
        domain=DOMAIN, title="House Assistant", data={}, options={"core": {"modules": []}}
    )
    entry.add_to_hass(hass)
    seen: list[bool] = []

    async def start(runtime) -> None:
        seen.append(add_js.called)

    with (
        patch("homeassistant.components.frontend.async_panel_exists", return_value=False),
        patch("homeassistant.components.panel_custom.async_register_panel"),
        patch("homeassistant.components.frontend.add_extra_js_url") as add_js,
        patch("homeassistant.components.frontend.remove_extra_js_url") as remove_js,
        patch(
            "custom_components.house_assistant.runtime.HouseRuntime.async_start",
            autospec=True,
            side_effect=start,
        ),
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert seen == [True]
        assert await hass.config_entries.async_unload(entry.entry_id)
        remove_js.assert_not_called()
        # set up again: registered once per run
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        add_js.assert_called_once()
        await hass.config_entries.async_remove(entry.entry_id)
        await hass.async_block_till_done()
        remove_js.assert_called_once_with(hass, add_js.call_args.args[1])
