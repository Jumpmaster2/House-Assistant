"""Stored state: one store per module and entry."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from ..const import DOMAIN, STORAGE_VERSION


def store_key(entry_id: str, module: str) -> str:
    """``.storage/house_assistant.<entry_id>.<module>``"""
    return f"{DOMAIN}.{entry_id}.{module}"


class ModuleStore(Store):
    """Do not overwrite raw data while recovery has not secured rejected records."""

    recovery_pending = False

    async def async_save(self, data: Any) -> None:
        if not self.recovery_pending:
            await super().async_save(data)

    def async_delay_save(self, data_func, delay: float) -> None:
        if not self.recovery_pending:
            super().async_delay_save(data_func, delay)


def module_store(hass: HomeAssistant, entry: ConfigEntry, module: str) -> Store[dict[str, Any]]:
    return ModuleStore(hass, STORAGE_VERSION, store_key(entry.entry_id, module))


async def remove_module_store(hass: HomeAssistant, entry: ConfigEntry, module: str) -> None:
    """Remove normal state and its retained corrupt snapshot."""
    await module_store(hass, entry, module).async_remove()
    await module_store(hass, entry, f"{module}.corrupt").async_remove()


class StoreRecovery:
    """Collect rejected raw records and back them up before any regular save."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, module: str) -> None:
        self.hass = hass
        self.entry = entry
        self.module = module
        self.rejected: dict[str, Any] = {}
        self.store: Store | None = None

    def record(self, name: str, raw: Any, schema: Any) -> dict[str, Any]:
        from .store_validation import validate

        try:
            validate(raw, schema)
        except (ValueError, TypeError, KeyError, OverflowError):
            self.rejected[name] = deepcopy(raw)
            return {}
        return raw

    def mapping(self, name: str, raw: Any) -> dict[str, Any]:
        """Check a container separately so one bad child cannot discard siblings."""
        if not isinstance(raw, dict):
            self.rejected[name] = deepcopy(raw)
            return {}
        return raw

    async def load(self, store: Store) -> dict[str, Any]:
        self.store = store
        if isinstance(store, ModuleStore):
            store.recovery_pending = True
        # HA may rename malformed JSON and return None, indistinguishable from a
        # first start. Keep its original bytes before asking HA to load it.
        import json
        from pathlib import Path

        from ..const import LOGGER

        raw_file: bytes | None = None

        def read_broken_json():
            nonlocal raw_file
            try:
                content = Path(store.path).read_bytes()
                raw_file = content
            except OSError:
                return None
            try:
                json.loads(content)
            except (ValueError, UnicodeError):
                return content.hex()
            return None

        if (broken := await self.hass.async_add_executor_job(read_broken_json)) is not None:
            self.rejected["file_hex"] = broken
        try:
            raw = await store.async_load()
        except Exception as err:
            LOGGER.warning("Could not load stored data for %s: %s", self.module, err)
            self.rejected["load_error"] = str(err)
            if raw_file is not None:
                self.rejected["file_hex"] = raw_file.hex()
            return {}
        if raw is None:
            if raw_file is not None:
                self.rejected["file_hex"] = raw_file.hex()
            return {}
        if not isinstance(raw, dict):
            self.rejected["store"] = raw
            return {}
        return raw

    async def finish(self) -> None:
        from homeassistant.helpers import issue_registry as ir
        from homeassistant.util import dt as dt_util

        from ..const import LOGGER

        issue = f"{self.entry.entry_id}_{self.module}_corrupt_storage"
        if not self.rejected:
            if isinstance(self.store, ModuleStore):
                self.store.recovery_pending = False
            ir.async_delete_issue(self.hass, DOMAIN, issue)
            return
        await module_store(self.hass, self.entry, f"{self.module}.corrupt").async_save(
            {"time": dt_util.utcnow().isoformat(), "data": backup_data(self.rejected)}
        )
        if isinstance(self.store, ModuleStore):
            self.store.recovery_pending = False
        LOGGER.warning(
            "Discarded and backed up corrupt stored data for %s: %s",
            self.module,
            list(self.rejected),
        )
        ir.async_create_issue(
            self.hass,
            DOMAIN,
            issue,
            is_fixable=False,
            severity=ir.IssueSeverity.WARNING,
            translation_key="corrupt_storage",
            translation_placeholders={"module": self.module},
        )


def backup_data(value: Any) -> Any:
    """Represent nonfinite values losslessly in a JSON-compatible snapshot."""
    import math

    if isinstance(value, float) and not math.isfinite(value):
        return {"__nonfinite_float__": repr(value)}
    if isinstance(value, dict):
        return {key: backup_data(item) for key, item in value.items()}
    if isinstance(value, list):
        return [backup_data(item) for item in value]
    return value
