"""The modules of the house at runtime.

One config entry holds the house and every module. Changing the settings of one
module must not restart the others (a restart resets hold times of the covers and
interrupts a meter reading), so the entry is not reloaded: every module is started
and stopped on its own and adds its entities to the platforms, which are set up once.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable, Coroutine
from typing import Any, ClassVar

from homeassistant.config_entries import ConfigEntry, ConfigSubentry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_MODULES, LOGGER, MODULE_ORDER, OPT_CORE, SHARED_KEYS
from .core.store import module_store

type HouseConfigEntry = ConfigEntry[HouseRuntime]

# module key -> module class, filled by modules.py
MODULE_TYPES: dict[str, type[Module]] = {}
# the house itself (vacation), running with or without modules; set by core.vacation
HOUSE_TYPE: list[type[Module]] = []


def register_module(cls: type[Module]) -> type[Module]:
    MODULE_TYPES[cls.key] = cls
    return cls


def register_house(cls: type[Module]) -> type[Module]:
    HOUSE_TYPE[:] = [cls]
    return cls


def module_options(entry: ConfigEntry, key: str) -> dict[str, Any]:
    """Options of one section (a module or the house)."""
    return dict(entry.options.get(key) or {})


def shared_options(entry: ConfigEntry) -> dict[str, Any]:
    """Shared settings exclusively from the house, including explicit empty values."""
    house = module_options(entry, OPT_CORE)
    return {key: house[key] for key in SHARED_KEYS if key in house}


def enabled_modules(entry: ConfigEntry) -> list[str]:
    """The modules switched on in the settings of the house, in their fixed order."""
    chosen = module_options(entry, OPT_CORE).get(CONF_MODULES) or []
    return [key for key in MODULE_ORDER if key in chosen and key in MODULE_TYPES]


class Module:
    """One part of the house (heating, covers, meters) with its own lifetime.

    Listeners, timers and background tasks registered here end when the module
    stops, so a module can be restarted without reloading the config entry.
    """

    key: ClassVar[str]
    # subentries the module reads; a change of one of them restarts it
    subentry_types: ClassVar[tuple[str, ...]] = ()

    def __init__(self, runtime: HouseRuntime) -> None:
        self.runtime = runtime
        self.hass = runtime.hass
        self.entry = runtime.entry
        self._entities: list[Entity] = []
        self._tasks: set[asyncio.Task[Any]] = set()
        self._waited: set[asyncio.Task[Any]] = set()
        self._unsubs: list[Callable[[], None]] = []
        # stopped because it was switched off (not for a restart or an unload)
        self.switched_off = False

    @property
    def options(self) -> dict[str, Any]:
        """Options of the module; a setting of the house set for all modules wins."""
        return {
            **{
                k: v
                for k, v in module_options(self.entry, self.key).items()
                if k not in SHARED_KEYS
            },
            **shared_options(self.entry),
        }

    def subentries(self, subentry_type: str | None = None) -> dict[str, ConfigSubentry]:
        types = (subentry_type,) if subentry_type else self.subentry_types
        return {
            sub_id: sub
            for sub_id, sub in self.entry.subentries.items()
            if sub.subentry_type in types
        }

    def signature(self) -> str:
        """Everything the module is built from; it is restarted when this changes."""
        return json.dumps(
            {
                "options": self.options,
                "subentries": [
                    [sub_id, sub.subentry_type, sub.title, dict(sub.data)]
                    for sub_id, sub in sorted(self.subentries().items())
                ],
            },
            sort_keys=True,
            default=str,
        )

    # ------------------------------------------------------------------ lifetime

    async def async_setup(self) -> None:
        """Start the module (load the store, register listeners)."""

    async def async_unload(self) -> None:
        """Stop the module (save the store)."""

    @callback
    def started(self) -> None:
        """The module is running and reachable for the others (``running_module``)."""

    def entities(self, platform: Platform) -> list[tuple[str | None, list[Entity]]]:
        """Entities of a platform, grouped by the subentry they belong to."""
        return []

    def diagnostics(self) -> dict[str, Any]:
        return {}

    @classmethod
    async def async_remove_entry(cls, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """The entry is deleted: remove what the module stored."""
        await module_store(hass, entry, cls.key).async_remove()

    @callback
    def async_on_stop(self, unsub: Callable[[], None]) -> None:
        """Call this when the module stops (unsubscribe a listener)."""
        self._unsubs.append(unsub)

    @callback
    def create_task(
        self, coro: Coroutine[Any, Any, Any], name: str, cancel: bool = True
    ) -> asyncio.Task[Any]:
        """Background task of the module. It is cancelled when the module stops, or with
        ``cancel=False`` waited for (a command to a device should not be cut off)."""
        task = self.entry.async_create_background_task(self.hass, coro, name)
        tasks = self._tasks if cancel else self._waited
        tasks.add(task)
        task.add_done_callback(tasks.discard)
        return task

    async def async_stop(self, switched_off: bool = False, quiet: bool = False) -> None:
        """Stop the module. Its entities stay registered (same ids after a restart).

        Their states leave the state machine when the module is switched off, and also
        on a quiet restart (settings changed): Home Assistant would otherwise write
        "unavailable" and the old state back, which fills the logbook with pairs of
        entries. Unloading the entry keeps the states as unavailable.
        """
        self.switched_off = switched_off
        for task in list(self._tasks):
            task.cancel()
        if self._tasks or self._waited:
            await asyncio.gather(*self._tasks, *self._waited, return_exceptions=True)
        while self._unsubs:
            self._unsubs.pop()()
        for entity in self._entities:
            if entity.hass is not None and entity.platform is not None:
                await entity.async_remove(force_remove=switched_off or quiet)
        self._entities.clear()
        await self.async_unload()


class HouseRuntime:
    """The running modules of the config entry and the platforms they add entities to."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.modules: dict[str, Module] = {}
        # the house: started first and stopped last, the modules read its vacation
        self.house: Any = None
        self._adders: dict[Platform, AddConfigEntryEntitiesCallback] = {}
        self._signatures: dict[str, str] = {}
        self._lock = asyncio.Lock()

    def module(self, key: str) -> Module | None:
        return self.modules.get(key)

    async def async_start(self) -> None:
        """Start the house and the enabled modules (when the entry is set up)."""
        await self._start_house()
        for key in enabled_modules(self.entry):
            await self._start(key)

    async def async_shutdown(self) -> None:
        async with self._lock:
            for key in reversed(list(self.modules)):
                await self._stop(key)
            await self._stop_house()

    async def _start_house(self) -> None:
        if not HOUSE_TYPE:
            return
        house = HOUSE_TYPE[0](self)
        try:
            await house.async_setup()
        except Exception:
            await house.async_stop()
            raise
        self.house = house
        self._signatures[house.key] = house.signature()
        house.started()
        for platform, add_entities in self._adders.items():
            self._add(house, platform, add_entities)

    async def _stop_house(self, quiet: bool = False) -> None:
        house, self.house = self.house, None
        if house is not None:
            self._signatures.pop(house.key, None)
            await house.async_stop(quiet=quiet)

    @callback
    def platform_ready(
        self, platform: Platform, add_entities: AddConfigEntryEntitiesCallback
    ) -> None:
        """A platform is set up: add the entities of the running modules."""
        self._adders[platform] = add_entities
        for module in [self.house, *self.modules.values()]:
            if module is not None:
                self._add(module, platform, add_entities)

    async def async_entry_updated(self) -> None:
        """Options or subentries changed: start, stop or restart only the modules concerned."""
        async with self._lock:
            house = self.house
            if house is not None and house.signature() != self._signatures.get(house.key):
                LOGGER.debug("Restarting the house")
                await self._stop_house(quiet=True)
                try:
                    await self._start_house()
                except Exception:
                    LOGGER.exception("The house could not be started")
            wanted = enabled_modules(self.entry)
            for key in [k for k in self.modules if k not in wanted]:
                await self._stop(key, switched_off=True)
            for key in wanted:
                module = self.modules.get(key)
                if module is None:
                    await self._start_logged(key)
                elif module.signature() != self._signatures.get(key):
                    LOGGER.debug("Restarting the module %s", key)
                    await self._stop(key, quiet=True)
                    await self._start_logged(key)

    async def _start_logged(self, key: str) -> None:
        try:
            await self._start(key)
        except Exception:
            LOGGER.exception("The module %s could not be started", key)

    async def _start(self, key: str) -> None:
        module = MODULE_TYPES[key](self)
        try:
            await module.async_setup()
        except Exception:
            await module.async_stop()
            raise
        self.modules[key] = module
        self._signatures[key] = module.signature()
        module.started()
        for platform, add_entities in self._adders.items():
            self._add(module, platform, add_entities)

    async def _stop(self, key: str, switched_off: bool = False, quiet: bool = False) -> None:
        module = self.modules.pop(key)
        self._signatures.pop(key, None)
        await module.async_stop(switched_off, quiet=quiet)

    @staticmethod
    def _add(
        module: Module, platform: Platform, add_entities: AddConfigEntryEntitiesCallback
    ) -> None:
        for subentry_id, entities in module.entities(platform):
            if not entities:
                continue
            module._entities.extend(entities)
            add_entities(entities, config_subentry_id=subentry_id)
