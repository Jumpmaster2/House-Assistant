"""Vacation of the house: one switch with departure and return for every module.

The house runs always, with or without modules. Its switch, departure and return are
kept in the store of the house (``house_assistant.<entry>.house``). Besides the switch
external sources still count (an input_boolean, a calendar): the ones of the house, or
without them the ones the heating and the covers had. The modules read the vacation
here and look again on ``SIGNAL_VACATION``:

* heating: vacation temperature, preheating for the return (the own return first);
* covers: presence simulation, sun protection without waiting for the room;
* meters: a warning when water runs on vacation.

The house itself reports open windows at the departure and windows opened during the
vacation.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime
from functools import partial
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ENTITY_ID, STATE_UNAVAILABLE, STATE_UNKNOWN, Platform
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, State, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (
    async_call_later,
    async_track_point_in_utc_time,
    async_track_state_change_event,
)
from homeassistant.helpers.start import async_at_started
from homeassistant.util import dt as dt_util

from ..const import (
    CONF_RETURN_ENTITY,
    CONF_VACATION_ENTITIES,
    CONF_VACATION_WINDOW_ALERT,
    DOMAIN,
    EVENT_LOGBOOK,
    EVENT_VACATION,
    LOGGER,
    MODULE_HEATING,
    MODULE_SHUTTER,
    OPT_CORE,
    SIGNAL_VACATION,
    SUBENTRY_WINDOW,
)
from ..runtime import HouseRuntime, Module, enabled_modules, module_options, register_house
from .entities import vacation_entities
from .house import CONF_TILT_SENSORS, CONF_WINDOW_SENSORS, windows
from .links import SIGNAL_HEATING
from .logic import vacation as vac
from .logic.contacts import CLOSED, OPEN, TILTED, UNKNOWN, window_state
from .notify import async_notify, house_language
from .store import module_store

HOUSE: str = "house"
# a window must stay open this long before it is reported (contacts bounce)
OPEN_DEBOUNCE = 10.0
DEFAULT_WINDOW_ALERT = True

TEXTS: dict[str, dict[str, str]] = {
    "title": {"de": "Urlaub", "en": "Vacation"},
    "started": {"de": "Urlaub beginnt ({source}).", "en": "Vacation starts ({source})."},
    "ended": {"de": "Urlaub endet.", "en": "Vacation ends."},
    "switch": {"de": "Schalter", "en": "switch"},
    "open_windows": {
        "de": "Urlaub beginnt, diese Fenster sind nicht zu: {windows}.",
        "en": "Vacation starts, these windows are not closed: {windows}.",
    },
    OPEN: {"de": "offen", "en": "open"},
    TILTED: {"de": "gekippt", "en": "tilted"},
    UNKNOWN: {"de": "unbekannt", "en": "unknown"},
    "opened": {
        "de": "{name} wurde im Urlaub geöffnet.",
        "en": "{name} was opened on vacation.",
    },
    "tilted_now": {
        "de": "{name} wurde im Urlaub gekippt.",
        "en": "{name} was tilted on vacation.",
    },
}


def return_ts(state: State | None) -> float | None:
    """Time of an external return (input_datetime, datetime or timestamp sensor)."""
    if state is None or state.state in (STATE_UNKNOWN, STATE_UNAVAILABLE):
        return None
    stamp = state.attributes.get("timestamp")
    if isinstance(stamp, int | float) and state.attributes.get("has_date", True):
        return float(stamp)
    parsed = dt_util.parse_datetime(state.state)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.get_default_time_zone())
    return parsed.timestamp()


def _dt(value: Any) -> datetime | None:
    parsed = dt_util.parse_datetime(value) if isinstance(value, str) else None
    return dt_util.as_utc(parsed) if parsed is not None else None


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


@register_house
class HouseModule(Module):
    """The vacation of the house (and what else belongs to the house as a whole)."""

    key = HOUSE
    subentry_types = (SUBENTRY_WINDOW,)

    def __init__(self, runtime: HouseRuntime) -> None:
        super().__init__(runtime)
        self._store = module_store(self.hass, self.entry, HOUSE)
        self.times = vac.Times()
        # the vacation as a whole (switch or an external source), when it started
        self.active = False
        self.source: str | None = None
        self.since: datetime | None = None
        self._window_states: dict[str, str] = {}
        self._pending: dict[str, Callable[[], None]] = {}
        self._timer: Callable[[], None] | None = None
        self._listeners: list[Callable[[], None]] = []

    @property
    def options(self) -> dict[str, Any]:
        return module_options(self.entry, OPT_CORE)

    def signature(self) -> str:
        # Only what the listeners are built from: a restart makes the entities briefly
        # unavailable, "vacation active" would turn on anew. Language, notification
        # services and the window report are read when needed.
        return json.dumps([self.sources(), sorted(self._windows().items())])

    # ------------------------------------------------------------------ sources

    def sources(self) -> list[str]:
        """External sources: the ones of the house, else the ones of the modules."""
        own = [str(e) for e in self.options.get(CONF_VACATION_ENTITIES) or []]
        if own:
            return own
        found: list[str] = []
        for key in (MODULE_HEATING, MODULE_SHUTTER):
            if key not in enabled_modules(self.entry):
                continue
            for entity_id in module_options(self.entry, key).get(CONF_VACATION_ENTITIES) or []:
                if entity_id not in found:
                    found.append(str(entity_id))
        return found

    @property
    def return_entity(self) -> str | None:
        """External return: the one of the house, else the one of the heating."""
        return self.options.get(CONF_RETURN_ENTITY) or (
            module_options(self.entry, MODULE_HEATING).get(CONF_RETURN_ENTITY)
            if MODULE_HEATING in enabled_modules(self.entry)
            else None
        )

    def external_return(self) -> str | None:
        """The external return (local time), None without one."""
        ts = return_ts(self.hass.states.get(self.return_entity) if self.return_entity else None)
        return dt_util.as_local(dt_util.utc_from_timestamp(ts)).isoformat() if ts else None

    def applies(self, entities: list[str] | None) -> bool:
        """Vacation for a module: the own switch, or one of the module's sources on."""
        return self.times.on or any(self._value(e) == "on" for e in entities or [])

    def own_return(self) -> datetime | None:
        """Return of the own vacation while it runs (it wins over an external one)."""
        return self.times.return_at if self.times.on else None

    def _value(self, entity_id: str | None) -> str | None:
        state = self.hass.states.get(entity_id) if entity_id else None
        return state.state if state is not None else None

    # ------------------------------------------------------------------ lifetime

    async def async_setup(self) -> None:
        stored = await self._store.async_load() or {}
        self.times = vac.Times(
            bool(stored.get("on")), _dt(stored.get("departure")), _dt(stored.get("return"))
        )
        self.active = bool(stored.get("active"))
        self.source = stored.get("source")
        self.since = _dt(stored.get("since"))
        self._window_states = {wid: self._window_state(wid) for wid in self._windows()}
        watched = set(self.sources())
        for _, contacts, tilts in self._windows().values():
            watched.update(contacts)
            watched.update(tilts)
        if watched:
            self.async_on_stop(
                async_track_state_change_event(self.hass, sorted(watched), self._on_state)
            )
        self.async_on_stop(async_dispatcher_connect(self.hass, SIGNAL_HEATING, self._write))
        self.async_on_stop(self._cancel)
        # what fell due while Home Assistant was down, once the contacts are known
        self.async_on_stop(async_at_started(self.hass, self._on_started))

    async def async_unload(self) -> None:
        await self._store.async_save(self._data())

    @callback
    def _cancel(self) -> None:
        if self._timer is not None:
            self._timer()
            self._timer = None
        for cancel in self._pending.values():
            cancel()
        self._pending.clear()

    async def _on_started(self, _hass: HomeAssistant) -> None:
        self._apply(vac.due(self.times, dt_util.utcnow()))

    @classmethod
    async def async_remove_entry(cls, hass: HomeAssistant, entry: ConfigEntry) -> None:
        await module_store(hass, entry, HOUSE).async_remove()

    def entities(self, platform: Platform) -> list[tuple[str | None, list[Entity]]]:
        return [(None, vacation_entities(self, platform))]

    def add_listener(self, update: Callable[[], None]) -> Callable[[], None]:
        """An entity of the vacation writes its state on every change."""
        self._listeners.append(update)
        return lambda: self._listeners.remove(update)

    @callback
    def _write(self) -> None:
        for update in list(self._listeners):
            update()

    def _data(self) -> dict[str, Any]:
        return {
            "on": self.times.on,
            "departure": _iso(self.times.departure),
            "return": _iso(self.times.return_at),
            "active": self.active,
            "source": self.source,
            "since": _iso(self.since),
        }

    def diagnostics(self) -> dict[str, Any]:
        return {**self._data(), "sources": self.sources(), "return_entity": self.return_entity}

    # ------------------------------------------------------------------ changes

    @callback
    def _apply(self, times: vac.Times) -> None:
        """New times: keep them, plan the next change and look at the vacation."""
        self.times = times
        if self._timer is not None:
            self._timer()
            self._timer = None
        if (when := vac.next_change(times)) is not None:
            self._timer = async_track_point_in_utc_time(self.hass, self._on_due, when)
        self._store.async_delay_save(self._data, 1)
        self._evaluate()

    @callback
    def _on_due(self, now: datetime) -> None:
        self._timer = None
        self._apply(vac.due(self.times, now))

    @callback
    def _evaluate(self) -> None:
        """Start or end of the vacation as a whole; the modules look again."""
        active, source = vac.active(self.times.on, [(e, self._value(e)) for e in self.sources()])
        if active != self.active:
            self.active = active
            self.since = dt_util.utcnow() if active else None
            self._store.async_delay_save(self._data, 1)
            self._announce(active, source)
        if source != self.source:
            self.source = source
            self._store.async_delay_save(self._data, 1)
        async_dispatcher_send(self.hass, SIGNAL_VACATION)
        self._write()

    def _announce(self, active: bool, source: str | None) -> None:
        self.hass.bus.async_fire(EVENT_VACATION, {"active": active, "source": source})
        if active:
            message = self._text("started", source=self._source_name(source))
        else:
            message = self._text("ended")
        self.hass.bus.async_fire(
            EVENT_LOGBOOK,
            {
                "name": self._text("title"),
                "message": message,
                ATTR_ENTITY_ID: self.entity_id("binary_sensor", "vacation_active"),
            },
        )
        if active and self.options.get(CONF_VACATION_WINDOW_ALERT, DEFAULT_WINDOW_ALERT):
            self._report_windows()

    def _source_name(self, source: str | None) -> str:
        if source in (None, vac.SOURCE_SWITCH):
            return self._text("switch")
        state = self.hass.states.get(source)
        return str(state.attributes.get("friendly_name") or source) if state else str(source)

    def _text(self, key: str, **values: Any) -> str:
        texts = TEXTS[key]
        return texts[house_language(self.hass, self.entry)].format(**values)

    def entity_id(self, domain: str, key: str) -> str | None:
        return er.async_get(self.hass).async_get_entity_id(
            domain, DOMAIN, f"{self.entry.entry_id}_{key}"
        )

    # ------------------------------------------------------------------ user actions

    @callback
    def set_on(self, on: bool) -> None:
        self._apply(vac.switched(self.times, on, dt_util.utcnow()))

    @callback
    def set_times(
        self, departure: datetime | None, return_at: datetime | None, strict: bool = False
    ) -> None:
        """New departure and return. A departure after the return is refused; a return
        in the past is ignored (``strict``: refused as well, for the panel)."""
        now = dt_util.utcnow()
        departure = dt_util.as_utc(departure) if departure else None
        return_at = dt_util.as_utc(return_at) if return_at else None
        if return_at is not None and return_at <= now:
            if strict:
                raise ServiceValidationError(
                    translation_domain=DOMAIN, translation_key=vac.ERROR_RETURN_PAST
                )
            LOGGER.info("The return %s is in the past, ignored", return_at)
            return_at = self.times.return_at
        if (error := vac.check(departure, return_at, now)) is not None:
            raise ServiceValidationError(translation_domain=DOMAIN, translation_key=error)
        self._apply(vac.planned(self.times, departure, return_at, now))

    @callback
    def set_departure(self, departure: datetime | None) -> None:
        self.set_times(departure, self.times.return_at)

    @callback
    def set_return(self, return_at: datetime | None) -> None:
        self.set_times(self.times.departure, return_at)

    @callback
    def clear(self) -> None:
        """Switch off, no departure and no return."""
        self._apply(vac.Times())

    # ------------------------------------------------------------------ windows

    def _windows(self) -> dict[str, tuple[str, list[str], list[str]]]:
        return {
            window_id: (
                sub.title,
                [str(e) for e in sub.data.get(CONF_WINDOW_SENSORS) or []],
                [str(e) for e in sub.data.get(CONF_TILT_SENSORS) or []],
            )
            for window_id, sub in windows(self.entry).items()
            if sub.data.get(CONF_WINDOW_SENSORS) or sub.data.get(CONF_TILT_SENSORS)
        }

    def _window_state(self, window_id: str) -> str:
        _, contacts, tilts = self._windows().get(window_id, ("", [], []))
        return window_state([self._value(e) for e in contacts], [self._value(e) for e in tilts])

    def open_windows(self) -> dict[str, str]:
        """Windows that are not closed (open, tilted or unknown), by their name."""
        result: dict[str, str] = {}
        for window_id, (title, _, _) in self._windows().items():
            state = self._window_state(window_id)
            if state != CLOSED:
                result[title] = state
        return result

    def _report_windows(self) -> None:
        found = self.open_windows()
        if not found:
            return
        # open and tilted first, then the unknown ones
        order = {OPEN: 0, TILTED: 1, UNKNOWN: 2}
        listed = ", ".join(
            f"{name} ({self._text(state)})"
            for name, state in sorted(found.items(), key=lambda item: (order[item[1]], item[0]))
        )
        self._send(self._text("open_windows", windows=listed), f"{DOMAIN}_vacation_windows")

    def _send(self, message: str, notification_id: str | None = None) -> None:
        self.create_task(
            async_notify(self.hass, self.entry, self._text("title"), message, notification_id),
            f"{DOMAIN} vacation notify",
            cancel=False,
        )

    @callback
    def _on_state(self, event: Event[EventStateChangedData]) -> None:
        entity_id = event.data["entity_id"]
        if entity_id in self.sources():
            self._evaluate()
        for window_id, (_, contacts, tilts) in self._windows().items():
            if entity_id not in contacts and entity_id not in tilts:
                continue
            new = self._window_state(window_id)
            old = self._window_states.get(window_id)
            self._window_states[window_id] = new
            self._write()
            # only a real opening: from closed (not from an unavailable contact)
            if old == CLOSED and new in (OPEN, TILTED) and self._alerts_on():
                if cancel := self._pending.pop(window_id, None):
                    cancel()
                self._pending[window_id] = async_call_later(
                    self.hass, OPEN_DEBOUNCE, partial(self._confirm_open, window_id)
                )

    def _alerts_on(self) -> bool:
        return self.active and bool(
            self.options.get(CONF_VACATION_WINDOW_ALERT, DEFAULT_WINDOW_ALERT)
        )

    @callback
    def _confirm_open(self, window_id: str, _now: datetime) -> None:
        self._pending.pop(window_id, None)
        state = self._window_state(window_id)
        if state not in (OPEN, TILTED) or not self._alerts_on():
            return
        title = self._windows()[window_id][0]
        self._send(self._text("opened" if state == OPEN else "tilted_now", name=title))
