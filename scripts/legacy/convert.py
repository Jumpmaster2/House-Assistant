"""Turn the three former integrations into one House Assistant entry (pure, no HA).

Works on the contents of the storage files of Home Assistant (``.storage``, as
loaded from JSON) and on the text of ``automations.yaml`` and ``scripts.yaml``.
Every id stays: rooms keep the ids of the heating areas, windows with a cover the
ids of the windows of Shutter Assistant, groups and meters theirs; entity ids, device
ids and the history of the entities stay as well.

* rooms from the heating areas (their Home Assistant area from the device of the area);
* windows: a window of Shutter Assistant sharing a contact with a heating area becomes
  one window with the size from the heating and the room of the area; its room also
  follows from ``room_entity`` being the thermostat of an area; every other heating
  contact becomes a window without a cover;
* shared settings go to the house, preferring heating on conflicts; the language
  comes from the covers, since heating followed the language of Home Assistant;
* the option migrations of AI Heating Assistant (minor versions 2 to 4) are applied.

Only the standard library: the script runs where the configuration is, not inside
Home Assistant.
"""

from __future__ import annotations

import copy
import re
import secrets
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

DOMAIN = "house_assistant"
HEATING = "ai_heating_assistant"
SHUTTER = "shutter_assistant"
METER = "zaehler_ablesung"
LEGACY = (HEATING, SHUTTER, METER)
MODULE_OF = {HEATING: "heating", SHUTTER: "shutter", METER: "meter"}
# modules with an own device for the module as a whole (identifier: the entry id)
MODULE_DEVICE = {HEATING: "heating", SHUTTER: "shutter"}

SUBENTRY_AREA = "heating_area"
# contact fields of a heating area -> size of the window made of them
WINDOW_FIELDS = {
    "window_sensors_small": "small",
    "window_sensors": "medium",
    "window_sensors_large": "large",
    "door_sensors": "door",
}
SIZE_ORDER = ("small", "medium", "large", "door")
# settings of the house the modules share (see const.SHARED_KEYS; without the language)
SHARED_KEYS = (
    "outdoor_temperature",
    "outdoor_humidity",
    "weather",
    "wind_entity",
    "notify_services",
    "workday_entity",
    "weekend_days",
    "house_azimuth",
    "house_width",
    "house_depth",
    "draft_reach",
    "vacation_entities",
    "return_entity",
)
LIST_KEYS = ("notify_services", "weekend_days", "vacation_entities")

SERVICES = {
    **{
        f"{HEATING}.{name}": f"{DOMAIN}.{name}"
        for name in (
            "export_parameters",
            "import_parameters",
            "reset_learned",
            "run_ai_check",
            "run_ai_ventilation_check",
            "decide_heating_day",
        )
    },
    f"{SHUTTER}.move": f"{DOMAIN}.move_cover",
    f"{SHUTTER}.start_override": f"{DOMAIN}.start_cover_override",
    f"{SHUTTER}.end_override": f"{DOMAIN}.end_cover_override",
    f"{SHUTTER}.resume": f"{DOMAIN}.resume_cover",
    f"{METER}.read": f"{DOMAIN}.read_meter",
    f"{METER}.set_reading": f"{DOMAIN}.set_meter_reading",
}
EVENTS = {
    f"{SHUTTER}_cover_moved": f"{DOMAIN}_cover_moved",
    f"{SHUTTER}_cover_failed": f"{DOMAIN}_cover_failed",
    f"{SHUTTER}_protection": f"{DOMAIN}_protection",
    f"{METER}_reading": f"{DOMAIN}_meter_reading",
    f"{HEATING}_logbook": f"{DOMAIN}_logbook",
    f"{SHUTTER}_logbook": f"{DOMAIN}_logbook",
}
CARDS = {
    "custom:ai-heating-thermostat-card": "custom:house-assistant-thermostat-card",
    "custom:ai-heating-thermostat-compact-card": "custom:house-assistant-thermostat-compact-card",
    "custom:ai-heating-climate-tile-card": "custom:house-assistant-climate-tile-card",
    "custom:shutter-assistant-card": "custom:house-assistant-cover-card",
    "custom:shutter-assistant-tile": "custom:house-assistant-tile",
    "custom:shutter-assistant-window-tile": "custom:house-assistant-window-tile",
}
# dashboard resources of the former integrations (the new one adds its own)
OLD_STATIC = tuple(f"/{domain}_{kind}/" for domain in LEGACY for kind in ("static", "panel"))

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def ulid() -> str:
    """A new id in the form Home Assistant uses for entries and subentries."""
    value = (int(time.time() * 1000) << 80) | secrets.randbits(80)
    return "".join(CROCKFORD[(value >> (5 * i)) & 31] for i in reversed(range(26)))


class TransferError(Exception):
    """Something the transfer cannot decide or would break."""


@dataclass
class Plan:
    """What the transfer does; written as transfer-plan.json by the dry run, so open
    points can be decided in it before ``--apply``."""

    entry: dict[str, Any]
    old_entries: dict[str, str]  # former domain -> its entry id
    notes: list[str] = field(default_factory=list)

    @property
    def new_entry_id(self) -> str:
        return str(self.entry["entry_id"])

    def as_dict(self) -> dict[str, Any]:
        return {"entry": self.entry, "old_entries": self.old_entries, "notes": self.notes}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Plan:
        return cls(data["entry"], dict(data["old_entries"]), list(data.get("notes") or []))

    def stores(self) -> list[tuple[str, str]]:
        """Store keys: former -> new (``.storage/<key>``)."""
        return [
            (f"{domain}.{entry_id}", f"{DOMAIN}.{self.new_entry_id}.{MODULE_OF[domain]}")
            for domain, entry_id in self.old_entries.items()
        ]

    def meter_ids(self) -> list[str]:
        return [s["subentry_id"] for s in self.entry["subentries"] if s["subentry_type"] == "meter"]


# ---------------------------------------------------------------- options


def migrate_heating_options(options: dict[str, Any], minor_version: int) -> dict[str, Any]:
    """The option migrations of AI Heating Assistant up to minor version 4."""
    options = dict(options)
    if minor_version < 2:
        # relay minutes no longer used; steps down as large as up (old defaults only)
        for key in ("relay_need_minutes", "relay_no_need_minutes"):
            options.pop(key, None)
        for key, old, new in (("theta_step_down", 0.5, 1.0), ("puffer_step_down", 0.1, 0.2)):
            if options.get(key) == old:
                options[key] = new
    if minor_version < 3 and options.get("max_output_tokens") == 4000:
        options["max_output_tokens"] = 16000  # thinking counts as output
    if minor_version < 4:
        # the night of the ventilation advice as times instead of hours
        for key in ("night_start_hour", "night_end_hour"):
            if isinstance(options.get(key), int | float) and not isinstance(options[key], bool):
                options[key] = f"{int(options[key]) % 24:02d}:00:00"
    return options


def _empty(value: Any) -> bool:
    return value in (None, "", [])


def _same(key: str, values: list[Any]) -> bool:
    if key in LIST_KEYS:
        return all(sorted(map(str, v)) == sorted(map(str, values[0])) for v in values)
    return all(v == values[0] for v in values)


def shared_settings(sections: dict[str, dict[str, Any]], notes: list[str]) -> dict[str, Any]:
    """Settings for the house, preferring heating and combining vacation sources."""
    core: dict[str, Any] = {}
    for key in SHARED_KEYS:
        found = {m: o[key] for m, o in sections.items() if not _empty(o.get(key))}
        if not found:
            continue
        values = list(found.values())
        if key == "vacation_entities":
            core[key] = list(dict.fromkeys(e for value in values for e in value))
        elif _same(key, values):
            core[key] = values[0]
        else:
            listed = ", ".join(f"{m}: {v}" for m, v in found.items())
            chosen = "heating" if "heating" in found else next(iter(found))
            core[key] = found[chosen]
            notes.append(f"{key} differs ({listed}), using {chosen}")
    return core


# ---------------------------------------------------------------- registries


def _entities(entity_registry: dict[str, Any]) -> list[dict[str, Any]]:
    return list(entity_registry.get("data", {}).get("entities", []))


def _devices(device_registry: dict[str, Any]) -> list[dict[str, Any]]:
    return list(device_registry.get("data", {}).get("devices", []))


def _name(entity_registry: dict[str, Any], entity_id: str) -> str:
    for item in _entities(entity_registry):
        if item.get("entity_id") == entity_id:
            return str(item.get("name") or item.get("original_name") or entity_id)
    return entity_id


def _area_of_device(device_registry: dict[str, Any], domain: str, identifier: str) -> str | None:
    for device in _devices(device_registry):
        if [domain, identifier] in [list(i) for i in device.get("identifiers", [])]:
            return device.get("area_id")
    return None


# ---------------------------------------------------------------- the entry


def find_entries(config_entries: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """The entries of the former integrations (one each)."""
    found: dict[str, dict[str, Any]] = {}
    for entry in config_entries.get("data", {}).get("entries", []):
        domain = entry.get("domain")
        if domain == DOMAIN:
            raise TransferError("House Assistant is already set up: remove its entry first")
        if domain in LEGACY:
            if domain in found:
                raise TransferError(f"{domain} has more than one entry")
            found[domain] = entry
    if not found:
        raise TransferError("none of the former integrations is set up")
    return found


def _subentries(entry: dict[str, Any] | None, subentry_type: str) -> list[dict[str, Any]]:
    if entry is None:
        return []
    return [s for s in entry.get("subentries", []) if s.get("subentry_type") == subentry_type]


def _sub(sub_id: str, subentry_type: str, title: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "data": data,
        "subentry_id": sub_id,
        "subentry_type": subentry_type,
        "title": title,
        "unique_id": None,
    }


def build_plan(
    config_entries: dict[str, Any],
    entity_registry: dict[str, Any],
    device_registry: dict[str, Any],
    new_id: Callable[[], str] = ulid,
    now: datetime | None = None,
) -> Plan:
    entries = find_entries(config_entries)
    heating, shutter, meter = (entries.get(d) for d in LEGACY)
    notes: list[str] = []

    # ------------------------------------------------ options
    sections: dict[str, dict[str, Any]] = {}
    if heating is not None:
        sections["heating"] = migrate_heating_options(
            heating.get("options") or {}, int(heating.get("minor_version") or 1)
        )
    if shutter is not None:
        # the heat need stays as it was: an own entity, or none (the heating day of the
        # heating module can be chosen afterwards)
        sections["shutter"] = {**(shutter.get("options") or {}), "use_heating_day": False}
    if meter is not None:
        sections["meter"] = dict(meter.get("options") or {})
    core: dict[str, Any] = {
        "modules": [MODULE_OF[d] for d in LEGACY if d in entries],
        **shared_settings({k: v for k, v in sections.items() if k != "meter"}, notes),
    }
    if "language" in sections.get("shutter", {}):
        core["language"] = sections["shutter"]["language"]
    # set once in the house: the modules do not keep a copy (the house wins anyway)
    for name in ("heating", "shutter"):
        for key in (*SHARED_KEYS, "language"):
            sections.get(name, {}).pop(key, None)

    # the heating day sensor of the heating becomes the link to the heating module
    heating_day = next(
        (
            item["entity_id"]
            for item in _entities(entity_registry)
            if heating is not None
            and item.get("platform") == HEATING
            and item.get("unique_id") == f"{heating['entry_id']}_heating_day"
        ),
        None,
    )
    if heating_day and sections.get("shutter", {}).get("heating_entity") == heating_day:
        del sections["shutter"]["heating_entity"]
        sections["shutter"]["use_heating_day"] = True
    # ------------------------------------------------ rooms
    subentries: list[dict[str, Any]] = []
    contact_room: dict[str, tuple[str, str]] = {}  # contact -> room, size
    room_data: dict[str, dict[str, Any]] = {}
    for area in _subentries(heating, SUBENTRY_AREA):
        area_id = area["subentry_id"]
        data = {k: v for k, v in area["data"].items() if k not in WINDOW_FIELDS}
        if ha_area := _area_of_device(device_registry, HEATING, area_id):
            data["area"] = ha_area
        subentries.append(_sub(area_id, "room", area["title"], data))
        room_data[area_id] = data
        for key, size in WINDOW_FIELDS.items():
            for contact in area["data"].get(key) or []:
                if contact in contact_room:
                    notes.append(f"{contact} is a contact of two areas, kept in the first")
                    continue
                contact_room[contact] = (area_id, size)
    thermostat_room = {
        item["entity_id"]: item["unique_id"].removesuffix("_climate")
        for item in _entities(entity_registry)
        if item.get("platform") == HEATING
        and item.get("config_entry_id") == (heating or {}).get("entry_id")
        and str(item.get("unique_id", "")).endswith("_climate")
    }

    # ------------------------------------------------ groups and windows with a cover
    subentries += [
        _sub(g["subentry_id"], "group", g["title"], dict(g["data"]))
        for g in _subentries(shutter, "group")
    ]
    taken: set[str] = set()
    for window in _subentries(shutter, "window"):
        data = dict(window["data"])
        contacts = [*(data.get("window_sensors") or []), *(data.get("tilt_sensors") or [])]
        shared = [c for c in contacts if c in contact_room]
        if shared:
            room, size = contact_room[shared[0]]
            data["size"] = size
            taken.update(shared)
            sizes = {contact_room[c][1] for c in shared}
            if len(sizes) > 1:
                notes.append(f"window {window['title']}: contacts of different sizes, took {size}")
        else:
            room = thermostat_room.get(str(data.get("room_entity") or ""))
            data.setdefault("size", "medium")
        if room:
            data["room"] = room
            # the room gives the temperature and the target: the same entity is not kept
            room_conf = room_data.get(room, {})
            own = data.get("room_entity")
            if own and (
                thermostat_room.get(str(own)) == room
                or (
                    own == room_conf.get("temperature_sensor")
                    and not room_conf.get("heater_switch")
                )
            ):
                del data["room_entity"]
        else:
            notes.append(f"window {window['title']}: room unknown, choose it in House > Windows")
        subentries.append(_sub(window["subentry_id"], "window", window["title"], data))

    # ------------------------------------------------ the other heating contacts
    for contact, (room, size) in contact_room.items():
        if contact in taken:
            continue
        title = _name(entity_registry, contact)
        subentries.append(
            _sub(
                new_id(),
                "window",
                title,
                {"name": title, "room": room, "size": size, "window_sensors": [contact]},
            )
        )
    plain = len(contact_room) - len(taken)
    if plain:
        notes.append(
            f"{plain} windows without a cover from heating contacts: wall and position can "
            "be set in House > Windows (for the automatic cross ventilation)"
        )

    # ------------------------------------------------ meters
    for m in _subentries(meter, "meter"):
        data = dict(m["data"])
        if heating_day and data.get("condition_entity") == heating_day:
            # the heating day of the heating module (within the heating period)
            del data["condition_entity"]
            data["condition_heating_day"] = True
        subentries.append(_sub(m["subentry_id"], "meter", m["title"], data))

    # in the form of the existing entries (fields of this Home Assistant version)
    template = heating or shutter or meter
    assert template is not None
    stamp = (now or datetime.now(UTC)).isoformat()
    entry = {
        **copy.deepcopy(template),
        "created_at": stamp,
        "modified_at": stamp,
        "data": {"api_key": (heating or {}).get("data", {}).get("api_key", "")},
        "disabled_by": None,
        "discovery_keys": {},
        "domain": DOMAIN,
        "entry_id": new_id(),
        "minor_version": 1,
        "options": {"core": core, **sections},
        "source": "user",
        "subentries": subentries,
        "title": "House Assistant",
        "unique_id": None,
        "version": 1,
    }
    return Plan(entry, {d: e["entry_id"] for d, e in entries.items()}, notes)


# ---------------------------------------------------------------- conversions


def convert_config_entries(config_entries: dict[str, Any], plan: Plan) -> dict[str, Any]:
    """The former entries replaced by the new one."""
    result = copy.deepcopy(config_entries)
    old = set(plan.old_entries.values())
    entries = [e for e in result["data"]["entries"] if e.get("entry_id") not in old]
    entries.append(copy.deepcopy(plan.entry))
    result["data"]["entries"] = entries
    return result


def _new_unique_id(unique_id: str, old_entry_id: str, new_entry_id: str) -> str:
    prefix = f"{old_entry_id}_"
    return (
        new_entry_id + unique_id[len(old_entry_id) :] if unique_id.startswith(prefix) else unique_id
    )


def convert_entities(entity_registry: dict[str, Any], plan: Plan) -> dict[str, Any]:
    """Entities move to the new entry: same entity ids, the unique ids of the entities of
    a module as a whole get the new entry id (the others are ids of subentries)."""
    result = copy.deepcopy(entity_registry)
    old = {entry_id: domain for domain, entry_id in plan.old_entries.items()}
    seen: dict[tuple[str, str], str] = {}
    for item in result["data"]["entities"]:
        entry_id = item.get("config_entry_id")
        if entry_id in old and item.get("platform") == old[entry_id]:
            item["platform"] = DOMAIN
            item["config_entry_id"] = plan.new_entry_id
            item["unique_id"] = _new_unique_id(str(item["unique_id"]), entry_id, plan.new_entry_id)
        if item.get("platform") == DOMAIN:
            key = (DOMAIN, str(item["unique_id"]))
            if key in seen:
                raise TransferError(
                    f"{item['entity_id']} and {seen[key]} would get the same unique id"
                )
            seen[key] = item["entity_id"]
    return result


def _move_device(device: dict[str, Any], plan: Plan) -> None:
    """One device (or child device) to the new entry. Newer registries keep one entry per
    device (``config_entry_id``), older ones a list (``config_entries``)."""
    old = set(plan.old_entries.values())
    new = plan.new_entry_id
    for key in ("config_entry_id", "primary_config_entry", "composite_primary_config_entry"):
        if device.get(key) in old:
            device[key] = new
    if isinstance(device.get("config_entries"), list):
        device["config_entries"] = list(
            dict.fromkeys(new if e in old else e for e in device["config_entries"])
        )
    if isinstance(device.get("config_entries_subentries"), dict):
        subs: dict[str, list[Any]] = {}
        for entry_id, ids in device["config_entries_subentries"].items():
            key = new if entry_id in old else entry_id
            subs[key] = list(dict.fromkeys([*subs.get(key, []), *ids]))
        device["config_entries_subentries"] = subs
    identifiers = []
    for domain, identifier in device.get("identifiers") or []:
        if domain in LEGACY:
            if identifier == plan.old_entries.get(domain) and domain in MODULE_DEVICE:
                identifier = f"{new}_{MODULE_DEVICE[domain]}"
            domain = DOMAIN
        identifiers.append([domain, identifier])
    device["identifiers"] = identifiers


def _belongs(device: dict[str, Any], plan: Plan) -> bool:
    old = set(plan.old_entries.values())
    entries = {device.get("config_entry_id"), *(device.get("config_entries") or [])}
    return bool(entries & old)


def convert_devices(device_registry: dict[str, Any], plan: Plan) -> dict[str, Any]:
    """Devices stay (same device ids, names, areas and labels) and point to the new entry."""
    result = copy.deepcopy(device_registry)
    data = result["data"]
    for kind in ("devices", "child_devices"):
        for device in data.get(kind) or []:
            if _belongs(device, plan):
                _move_device(device, plan)
    return result


def convert_dashboard(dashboard: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Card types of a dashboard (storage mode); returns the number replaced."""
    count = 0

    def walk(value: Any) -> Any:
        nonlocal count
        if isinstance(value, dict):
            return {k: walk(v) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(v) for v in value]
        if isinstance(value, str) and value in CARDS:
            count += 1
            return CARDS[value]
        return value

    return walk(dashboard), count


def convert_resources(resources: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Drop the dashboard resources of the former integrations."""
    result = copy.deepcopy(resources)
    items = result.get("data", {}).get("items", [])
    removed = [i["url"] for i in items if str(i.get("url", "")).startswith(OLD_STATIC)]
    result.setdefault("data", {})["items"] = [i for i in items if i.get("url") not in removed]
    return result, removed


_NAMES = {**SERVICES, **EVENTS}
_PATTERN = re.compile(
    r"(?<![\w.])("
    + "|".join(re.escape(k) for k in sorted(_NAMES, key=len, reverse=True))
    + r")(?![\w])"
)
_LEFT = re.compile(r"\b(" + "|".join(LEGACY) + r")\b")


def convert_yaml_text(text: str) -> tuple[str, list[str], list[str]]:
    """Service and event names in automations or scripts. Returns the text, what was
    replaced and the lines still naming a former integration (to look at by hand)."""
    replaced: list[str] = []

    def repl(match: re.Match[str]) -> str:
        replaced.append(f"{match.group(1)} -> {_NAMES[match.group(1)]}")
        return _NAMES[match.group(1)]

    result = _PATTERN.sub(repl, text)
    left = [line.strip() for line in result.splitlines() if _LEFT.search(line)]
    return result, replaced, left


def store_content(old: dict[str, Any], new_key: str) -> dict[str, Any]:
    """A store file under its new key (the content stays)."""
    return {**old, "key": new_key}


def summary(plan: Plan) -> dict[str, int]:
    counts: dict[str, int] = {}
    for sub in plan.entry["subentries"]:
        counts[sub["subentry_type"]] = counts.get(sub["subentry_type"], 0) + 1
    counts["windows with a cover"] = sum(
        1
        for s in plan.entry["subentries"]
        if s["subentry_type"] == "window" and s["data"].get("cover")
    )
    return counts


def iter_dashboards(names: Iterable[str]) -> list[str]:
    """Storage files of dashboards (``lovelace`` and ``lovelace.<id>``)."""
    return sorted(
        n
        for n in names
        if n == "lovelace" or (n.startswith("lovelace.") and not n.endswith(".bak"))
    )
