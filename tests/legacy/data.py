"""A small installation of the three former integrations, as in .storage (HA 2026.10)."""

from __future__ import annotations

import copy
from typing import Any

from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits
from custom_components.house_assistant.meter.const import meter_defaults

HEAT, SHUT, METER = (
    "01HEATENTRY0000000000000AA",
    "01SHUTENTRY0000000000000AA",
    "01METERENTRY000000000000AA",
)
LIVING, BATH = "01AREALIVING00000000000000", "01AREABATH0000000000000000"
GROUP, WIN_LIVING, WIN_KITCHEN = (
    "01GROUPSOUTH00000000000000",
    "01WINLIVING000000000000000",
    "01WINKITCHEN00000000000000",
)
WATER = "01METERWATER00000000000000"


def _sub(sub_id: str, subentry_type: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "data": data,
        "subentry_id": sub_id,
        "subentry_type": subentry_type,
        "title": data["name"],
        "unique_id": None,
    }


def _entry(domain: str, entry_id: str, title: str, **extra: Any) -> dict[str, Any]:
    return {
        "created_at": "2026-01-01T00:00:00+00:00",
        "data": {},
        "disabled_by": None,
        "discovery_keys": {},
        "domain": domain,
        "entry_id": entry_id,
        "minor_version": 1,
        "modified_at": "2026-01-01T00:00:00+00:00",
        "options": {},
        "pref_disable_new_entities": False,
        "pref_disable_polling": False,
        "source": "user",
        "subentries": [],
        "title": title,
        "unique_id": None,
        "version": 1,
        **extra,
    }


HEATING_OPTIONS = {
    **HEATING_DEFAULTS,
    "limits": default_limits(),
    "outdoor_temperature": "sensor.outdoor",
    "weather": "weather.home",
    "vacation_entities": ["input_boolean.away"],
    # values of before minor versions 3 and 4
    "night_start_hour": 22,
    "night_end_hour": 6,
    "max_output_tokens": 4000,
}

SHUTTER_OPTIONS = {
    "outdoor_temperature": "sensor.outdoor",
    "weather": "weather.forecast",
    "language": "de",
    "notify_services": ["notify.phone"],
    "house_azimuth": 180,
    "house_width": 12.0,
    "house_depth": 9.0,
    "vacation_entities": ["input_boolean.away"],
    "heating_entity": "binary_sensor.heating_heating_day",
    "verify_after": 0,
}


def config_entries() -> dict[str, Any]:
    return {
        "version": 1,
        "minor_version": 5,
        "key": "core.config_entries",
        "data": {
            "entries": [
                _entry(
                    "ai_heating_assistant",
                    HEAT,
                    "AI Heating Assistant",
                    data={"api_key": ""},
                    options=copy.deepcopy(HEATING_OPTIONS),
                    minor_version=2,
                    subentries=[
                        _sub(
                            LIVING,
                            "heating_area",
                            {
                                "name": "Wohnzimmer",
                                "temperature_sensor": "sensor.living_temperature",
                                "heater_switch": "input_boolean.circuit_living",
                                "window_sensors": ["binary_sensor.living_window"],
                                "door_sensors": ["binary_sensor.terrace_door"],
                            },
                        ),
                        _sub(
                            BATH,
                            "heating_area",
                            {
                                "name": "Bad",
                                "temperature_sensor": "sensor.bath_temperature",
                                "heater_switch": "input_boolean.circuit_bath",
                                "window_sensors_small": ["binary_sensor.bath_window"],
                            },
                        ),
                    ],
                ),
                _entry(
                    "shutter_assistant",
                    SHUT,
                    "Shutter Assistant",
                    options=copy.deepcopy(SHUTTER_OPTIONS),
                    subentries=[
                        _sub(
                            GROUP, "group", {"name": "Süd", "azimuth_from": 90, "azimuth_to": 270}
                        ),
                        _sub(
                            WIN_LIVING,
                            "window",
                            {
                                "name": "Wohnzimmer",
                                "cover": "cover.living",
                                "window_sensors": ["binary_sensor.living_window"],
                                "group": GROUP,
                            },
                        ),
                        _sub(
                            WIN_KITCHEN,
                            "window",
                            {
                                "name": "Küche",
                                "cover": "cover.kitchen",
                                "window_sensors": ["binary_sensor.kitchen_window"],
                                "group": GROUP,
                                # the thermostat of the bath: the window belongs to it
                                "room_entity": "climate.bad",
                            },
                        ),
                    ],
                ),
                _entry(
                    "zaehler_ablesung",
                    METER,
                    "Zähler-Ablesung",
                    options={"ai_task_entity": "ai_task.claude", "notify_rejected": True},
                    subentries=[
                        _sub(
                            WATER,
                            "meter",
                            {
                                **meter_defaults("water"),
                                "name": "Wasser",
                                "camera": "camera.water",
                                "condition_entity": "binary_sensor.heating_heating_day",
                            },
                        )
                    ],
                ),
                _entry("hue", "01HUE00000000000000000000A", "Hue"),
            ]
        },
    }


def _entity(
    entity_id: str, platform: str, entry_id: str | None, unique_id: str, sub: str | None = None
) -> dict[str, Any]:
    return {
        "entity_id": entity_id,
        "platform": platform,
        "config_entry_id": entry_id,
        "config_subentry_id": sub,
        "unique_id": unique_id,
        "id": f"id-{entity_id}",
        "name": None,
        "original_name": None,
    }


ENTITIES = [
    (
        "binary_sensor.heating_heating_day",
        "ai_heating_assistant",
        HEAT,
        f"{HEAT}_heating_day",
        None,
    ),
    ("climate.bad", "ai_heating_assistant", HEAT, f"{BATH}_climate", BATH),
    ("climate.wohnzimmer", "ai_heating_assistant", HEAT, f"{LIVING}_climate", LIVING),
    ("switch.covers_automatic", "shutter_assistant", SHUT, f"{SHUT}_automatic", None),
    ("sensor.wohnzimmer_status", "shutter_assistant", SHUT, f"{WIN_LIVING}_status", WIN_LIVING),
    ("sensor.wasser_zahlerstand", "zaehler_ablesung", METER, f"{WATER}_reading", WATER),
    ("binary_sensor.terrace_door", "zha", "01ZHA00000000000000000000A", "00:11:22", None),
    ("light.hall", "hue", "01HUE00000000000000000000A", "hue-1", None),
]


def entity_registry() -> dict[str, Any]:
    entities = [_entity(*e) for e in ENTITIES]
    entities[6]["original_name"] = "Terrassentür"
    return {
        "version": 1,
        "minor_version": 23,
        "key": "core.entity_registry",
        "data": {"entities": entities, "deleted_entities": []},
    }


def _device(dev_id: str, entry_id: str, identifier: list[str], **extra: Any) -> dict[str, Any]:
    return {
        "id": dev_id,
        "config_entry_id": entry_id,
        "config_subentry_id": None,
        "primary_config_entry": entry_id,
        "identifiers": [identifier],
        "area_id": None,
        "name": dev_id,
        **extra,
    }


def device_registry() -> dict[str, Any]:
    return {
        "version": 3,
        "minor_version": 4,
        "key": "core.device_registry",
        "data": {
            "devices": [
                _device("dev-heating", HEAT, ["ai_heating_assistant", HEAT]),
                _device("dev-living", HEAT, ["ai_heating_assistant", LIVING], area_id="wohnzimmer"),
                _device("dev-bath", HEAT, ["ai_heating_assistant", BATH], area_id="bad"),
                _device("dev-covers", SHUT, ["shutter_assistant", SHUT]),
                _device("dev-win", SHUT, ["shutter_assistant", WIN_LIVING], area_id="wohnzimmer"),
                _device("dev-water", METER, ["zaehler_ablesung", WATER], area_id="keller"),
                _device("dev-hue", "01HUE00000000000000000000A", ["hue", "bridge"]),
            ],
            "child_devices": [],
            "deleted_devices": [],
        },
    }


DASHBOARD = {
    "version": 1,
    "minor_version": 1,
    "key": "lovelace",
    "data": {
        "config": {
            "views": [
                {
                    "cards": [
                        {"type": "custom:ai-heating-thermostat-card", "entity": "climate.bad"},
                        {"type": "custom:shutter-assistant-window-tile", "window": "Küche"},
                        {
                            "type": "vertical-stack",
                            "cards": [{"type": "custom:shutter-assistant-card"}],
                        },
                        {"type": "entities", "entities": ["light.hall"]},
                    ]
                }
            ]
        }
    },
}

RESOURCES = {
    "version": 1,
    "minor_version": 1,
    "key": "lovelace_resources",
    "data": {
        "items": [
            {
                "id": "a",
                "type": "module",
                "url": "/ai_heating_assistant_static/thermostat-card.js?v=1",
            },
            {"id": "b", "type": "module", "url": "/shutter_assistant_static/card.js?v=2"},
            {"id": "c", "type": "module", "url": "/hacsfiles/mushroom/mushroom.js"},
        ]
    },
}

AUTOMATIONS = """- alias: Rollos hoch
  triggers:
    - trigger: event
      event_type: shutter_assistant_cover_moved
  actions:
    - action: shutter_assistant.move
      data:
        action: open
    - action: zaehler_ablesung.read
      target:
        entity_id: sensor.wasser_zahlerstand
    - action: ai_heating_assistant.run_ai_check
    - action: notify.phone
      data:
        message: "{{ integration_entities('shutter_assistant') | count }}"
"""
