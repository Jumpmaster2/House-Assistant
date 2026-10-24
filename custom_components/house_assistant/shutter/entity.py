"""Base entities."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODULE_SHUTTER, NAME
from .engine import ShutterEngine, Window


def global_device_info(entry_id: str) -> DeviceInfo:
    """Device of the cover module as a whole (its name is translated)."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_{MODULE_SHUTTER}")},
        translation_key=MODULE_SHUTTER,
        manufacturer=NAME,
        model="Covers",
        entry_type=DeviceEntryType.SERVICE,
    )


class GlobalEntity(CoordinatorEntity[ShutterEngine]):
    """Entity of the integration as a whole."""

    _attr_has_entity_name = True

    def __init__(self, engine: ShutterEngine, key: str) -> None:
        super().__init__(engine)
        entry_id = engine.config_entry.entry_id
        self._attr_translation_key = key
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_device_info = global_device_info(entry_id)


class WindowEntity(CoordinatorEntity[ShutterEngine]):
    """Entity belonging to one window."""

    _attr_has_entity_name = True

    def __init__(
        self, engine: ShutterEngine, window_id: str, key: str, translation_key: str | None = None
    ) -> None:
        super().__init__(engine)
        self.window_id = window_id
        window = engine.windows[window_id]
        # the key stays in the unique id; the translation key is unique across all modules
        self._attr_translation_key = translation_key or key
        self._attr_unique_id = f"{window_id}_{key}"
        device_info = DeviceInfo(
            identifiers={(DOMAIN, window_id)},
            name=window.name,
            manufacturer=NAME,
            model="Window",
        )
        # Reference the main device by its id; the identifier based
        # ``via_device`` is deprecated and fails when HA re-adds the entity.
        if engine.global_device_id:
            device_info["via_device_id"] = engine.global_device_id
        self._attr_device_info = device_info

    @property
    def window(self) -> Window:
        return self.coordinator.windows[self.window_id]
