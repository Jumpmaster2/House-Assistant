"""House ownership contracts without a running Home Assistant instance."""

import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from custom_components.house_assistant import _move_vacation_sources
from custom_components.house_assistant.const import SHARED_KEYS
from custom_components.house_assistant.core.house_ws import room_data, room_fields
from custom_components.house_assistant.core.settings import house_schema, validate_house
from custom_components.house_assistant.heating.config_flow import (
    _fields_of,
    area_schema,
    general_schema,
)
from custom_components.house_assistant.heating.websocket import (
    PanelError,
    apply_options,
    option_fields,
)
from custom_components.house_assistant.runtime import Module, shared_options
from custom_components.house_assistant.shutter.config_flow import (
    _protection_schema,
)
from custom_components.house_assistant.shutter.websocket import OPTION_KEYS

BASICS = {"name", "area", "floor_area", "temperature_sensor", "humidity_sensor", "cooling_entity"}


def migrate(options):
    entry = SimpleNamespace(options=options)

    def update(entry, **kwargs):
        entry.options = kwargs["options"]

    hass = SimpleNamespace(
        config_entries=SimpleNamespace(async_update_entry=Mock(side_effect=update))
    )
    _move_vacation_sources(hass, entry)
    first = entry.options
    _move_vacation_sources(hass, entry)
    assert first == entry.options
    assert hass.config_entries.async_update_entry.call_count <= 1
    return entry.options


@pytest.mark.parametrize("key", SHARED_KEYS)
@pytest.mark.parametrize("core", [None, "", []])
def test_migration_empty_house(key, core):
    value = ["input_boolean.vacation"] if key == "vacation_entities" else "first"
    result = migrate(
        {
            "core": {key: core},
            "heating": {key: value},
            "shutter": {key: value},
            "meter": {key: value},
        }
    )
    assert result["core"][key] == value
    assert all(key not in result[m] for m in ("heating", "shutter", "meter"))


@pytest.mark.parametrize("key", SHARED_KEYS)
def test_migration_precedence_and_conflict(key, caplog):
    if key == "vacation_entities":
        result = migrate(
            {
                "core": {key: ["house"]},
                "heating": {key: ["heat"]},
                "shutter": {key: ["heat", "cover"]},
            }
        )
        assert result["core"][key] == ["house", "heat", "cover"]
        return
    result = migrate({"heating": {key: "heat"}, "shutter": {key: "cover"}})
    assert result["core"][key] == "heat"
    assert f"Conflicting shared setting {key} in modules heating and shutter" in caplog.text
    caplog.clear()
    result = migrate({"core": {key: "house"}, "heating": {key: "heat"}, "shutter": {key: "cover"}})
    assert result["core"][key] == "house"
    assert not caplog.text


def test_migration_empty_and_vacation_copies():
    assert migrate({}) == {}
    assert migrate({"heating": {}, "shutter": {}}) == {"heating": {}, "shutter": {}}
    assert migrate(
        {
            "core": {"vacation_ventilation_pause": False, "vacation_heat_protection": True},
            "heating": {"vacation_ventilation_pause": True},
        }
    ) == {"core": {}, "heating": {"vacation_ventilation_pause": True}}


@pytest.mark.parametrize("key", SHARED_KEYS)
@pytest.mark.parametrize(
    "house", [{}, {"notify_services": [], "language": "auto", "wind_entity": "sensor.house_wind"}]
)
def test_runtime_ignores_module_values(key, house):
    entry = SimpleNamespace(options={"core": house, "shutter": {key: "legacy"}})
    runtime = SimpleNamespace(hass=None, entry=entry)
    module = Module(runtime)
    module.key = "shutter"
    assert module.options.get(key) == house.get(key)
    assert shared_options(entry) == house


def test_centralized_schemas_and_panels():
    hass = SimpleNamespace(services=SimpleNamespace(async_services_for_domain=lambda _: {}))
    for fields in (
        general_schema({}).schema,
        option_fields(),
        _protection_schema({}, "°C").schema,
        OPTION_KEYS,
    ):
        assert not set(map(str, fields)) & set(SHARED_KEYS)
    assert not set(_fields_of(area_schema({}))) & BASICS
    assert set(map(str, room_fields())) >= BASICS
    assert "wind_entity" in set(map(str, house_schema(hass, {}).schema))
    from custom_components.house_assistant.shutter.config_flow import (
        SHUTTER_MENU,
        ShutterOptionsSteps,
    )

    assert "shutter_general" not in SHUTTER_MENU
    assert not hasattr(ShutterOptionsSteps, "async_step_shutter_general")
    root = Path(__file__).parents[1] / "custom_components/house_assistant/frontend"
    for module in ("heating", "shutter"):
        text = (root / f"{module}.js").read_text()
        assert "_houseNote" not in text
        assert text.count(".house_settings_note") == 1
        assert "fields: []" not in text
        for fields in re.findall(r"fields: \[([^\]]*)\]", text):
            assert not set(re.findall(r'"([^"]+)"', fields)) & set(SHARED_KEYS)
    text = (root / "heating.js").read_text().split("const AREA_GROUPS = [")[1].split("\n];")[0]
    assert not set(re.findall(r'"([^"]+)"', text)) & BASICS
    assert (
        '"floor_area"'
        in (root / "house.js").read_text().split("const ROOM_FIELDS = ")[1].split(";")[0]
    )


@pytest.mark.parametrize("key", SHARED_KEYS)
def test_module_save_rejects_shared(key):
    with pytest.raises(PanelError, match=f"house_settings_only:{key}"):
        apply_options({}, {key: ""}, {"weather": "weather.home"})


@pytest.mark.parametrize("value", [0, 201, "text"])
def test_house_rejects_invalid_floor_area(value):
    entry = SimpleNamespace(subentries={})
    with pytest.raises(Exception, match="invalid_value:floor_area"):
        room_data(entry, None, "Room", {"floor_area": value})


@pytest.mark.parametrize("value", [1, 50.5, 200])
def test_house_saves_floor_area(value):
    entry = SimpleNamespace(subentries={})
    assert room_data(entry, None, "Room", {"floor_area": value})["floor_area"] == value


def test_house_temperature_validation():
    hass = SimpleNamespace(states=SimpleNamespace(get=lambda _: SimpleNamespace(state="text")))
    assert validate_house(hass, {}, ["heating"]) == {
        "outdoor_temperature": "need_temperature_source"
    }
    assert validate_house(hass, {}, ["shutter"]) == {
        "outdoor_temperature": "need_temperature_source"
    }
    assert validate_house(hass, {"weather": "weather.home"}, ["heating", "shutter"]) == {}
    assert validate_house(hass, {"outdoor_temperature": "sensor.x"}, ["heating"]) == {
        "outdoor_temperature": "not_numeric"
    }
    assert validate_house(hass, {}, ["meter"]) == {}


def test_native_room_forms_preserve_basics():
    import asyncio
    from unittest.mock import patch

    from custom_components.house_assistant.heating.config_flow import RoomSubentryFlow

    sub = SimpleNamespace(
        title="Room",
        subentry_id="room",
        subentry_type="room",
        data={
            "name": "Room",
            "area": "ha_area",
            "floor_area": 25,
            "temperature_sensor": "sensor.room",
            "cooling_entity": "climate.ac",
        },
    )
    entry = SimpleNamespace(
        options={"core": {"modules": ["heating", "shutter"]}}, subentries={"room": sub}
    )
    flow = RoomSubentryFlow()
    flow._get_entry = Mock(return_value=entry)
    flow._get_reconfigure_subentry = Mock(return_value=sub)
    flow.async_show_form = Mock(side_effect=lambda **kw: kw)
    flow.async_update_and_abort = Mock(side_effect=lambda *args, **kw: kw)
    flow.async_create_entry = Mock(side_effect=lambda **kw: kw)
    result = asyncio.run(flow.async_step_user())
    assert set(map(str, result["data_schema"].schema)) == {"name"}
    assert asyncio.run(flow.async_step_user({"name": "New"}))["data"] == {"name": "New"}
    with patch(
        "custom_components.house_assistant.heating.config_flow.running_coordinator",
        return_value=None,
    ):
        result = asyncio.run(flow.async_step_reconfigure())
        assert not set(_fields_of(result["data_schema"])) & BASICS
        result = asyncio.run(flow.async_step_reconfigure({"heating": {"default_target": 22}}))
    assert result["title"] == "Room"
    assert {k: result["data"][k] for k in sub.data} == sub.data
    assert result["data"]["default_target"] == 22


def test_heating_room_command_rejects_basics_and_keeps_existing():
    import inspect
    from unittest.mock import patch

    from custom_components.house_assistant.heating.websocket import ws_save_area

    original = {
        "name": "Room",
        "area": "ha_area",
        "floor_area": 25,
        "temperature_sensor": "sensor.room",
        "humidity_sensor": "sensor.rh",
        "cooling_entity": "climate.ac",
        "default_target": 21,
    }
    sub = SimpleNamespace(title="Room", subentry_id="room", subentry_type="room", data=original)
    entry = SimpleNamespace(subentries={"room": sub})
    hass = SimpleNamespace(config_entries=SimpleNamespace(async_update_subentry=Mock()))
    connection = Mock()
    command = inspect.unwrap(ws_save_area)
    with (
        patch("custom_components.house_assistant.heating.websocket._entry", return_value=entry),
        patch(
            "custom_components.house_assistant.heating.websocket.running_coordinator",
            return_value=None,
        ),
        patch(
            "custom_components.house_assistant.heating.websocket.config_payload", return_value={}
        ),
    ):
        for key in BASICS:
            command(
                hass,
                connection,
                {"id": 1, "subentry_id": "room", "title": "Room", "data": {key: None}},
            )
            assert connection.send_error.call_args.args[-1] == "room_basics_house_only"
        command(hass, connection, {"id": 1, "title": "New", "data": {}})
        assert connection.send_error.call_args.args[-1] == "create_rooms_in_house"
        assert not hass.config_entries.async_update_subentry.called
        command(
            hass,
            connection,
            {"id": 1, "subentry_id": "room", "title": "Room", "data": {"default_target": 22}},
        )
        saved = hass.config_entries.async_update_subentry.call_args.kwargs["data"]
        assert {k: saved[k] for k in BASICS} == {k: original[k] for k in BASICS}
        assert saved["default_target"] == 22


def test_vacation_dialog_saves_options_only_in_modules():
    import asyncio

    from custom_components.house_assistant.config_flow import HouseAssistantOptionsFlow

    entry = SimpleNamespace(
        options={"core": {"modules": ["heating", "shutter"], "vacation_ventilation_pause": False}}
    )
    flow = SimpleNamespace(config_entry=entry, async_create_entry=Mock(side_effect=lambda **kw: kw))
    result = asyncio.run(
        HouseAssistantOptionsFlow.async_step_vacation(
            flow,
            {
                "vacation_entities": ["calendar.holiday"],
                "vacation_ventilation_pause": True,
                "vacation_heat_protection": False,
            },
        )
    )
    assert result["data"]["core"] == {
        "modules": ["heating", "shutter"],
        "vacation_entities": ["calendar.holiday"],
    }
    assert result["data"]["heating"] == {"vacation_ventilation_pause": True}
    assert result["data"]["shutter"] == {"vacation_heat_protection": False}


def test_covers_read_wind_and_auto_language_from_house():
    from custom_components.house_assistant.shutter.engine import ShutterEngine

    entry = SimpleNamespace(
        options={
            "core": {"wind_entity": "sensor.wind", "language": "auto"},
            "shutter": {"wind_entity": "sensor.legacy", "language": "en"},
        }
    )
    hass = SimpleNamespace(config=SimpleNamespace(language="de-DE"))
    module = Module(SimpleNamespace(hass=hass, entry=entry))
    module.key = "shutter"
    engine = ShutterEngine.__new__(ShutterEngine)
    engine.module = module
    engine.hass = hass
    engine._defaults = {}
    assert engine.opt("wind_entity") == "sensor.wind"
    assert engine.language == "de"
    entry.options["core"] = {"wind_entity": ""}
    assert engine.opt("wind_entity") == ""
    entry.options["core"] = {}
    assert engine.opt("wind_entity") is None


@pytest.mark.parametrize("key", SHARED_KEYS)
def test_covers_command_rejects_shared(key):
    import inspect
    from unittest.mock import patch

    from custom_components.house_assistant.shutter.websocket import ws_save_options

    connection = Mock()
    with patch("custom_components.house_assistant.shutter.websocket._entry", return_value=object()):
        inspect.unwrap(ws_save_options)(None, connection, {"id": 1, "options": {key: None}})
    assert connection.send_error.call_args.args[-1] == f"house_settings_only:{key}"


@pytest.mark.parametrize(
    ("house", "heating", "shutter", "expected"),
    [
        ("auto", "de", "auto", "de"),
        ("en", "de", "auto", "en"),
        ("auto", "auto", "auto", "auto"),
        ("auto", "auto", "de", "de"),
        ("auto", "de", "en", "de"),
    ],
)
def test_migration_automatic_language(house, heating, shutter, expected, caplog):
    result = migrate(
        {
            "core": {"language": house},
            "heating": {"language": heating},
            "shutter": {"language": shutter},
        }
    )
    assert result["core"]["language"] == expected
    assert "language" not in result["heating"]
    assert "language" not in result["shutter"]
    if house == "auto" and heating == "de" and shutter == "en":
        assert "language in modules heating and shutter" in caplog.text


@pytest.mark.parametrize(
    ("option", "ha_language", "expected"),
    [
        ("auto", "de", "de"),
        ("auto", "en", "en"),
        (None, "de-CH", "de-CH"),
        ("de", "en", "de"),
        ("en", "de", "en"),
        ("auto", None, "en"),
    ],
)
def test_meter_language_uses_house_or_home_assistant(option, ha_language, expected):
    from custom_components.house_assistant.meter.meter import MeterManager

    manager = SimpleNamespace(
        options={"language": option},
        hass=SimpleNamespace(config=SimpleNamespace(language=ha_language)),
    )
    assert MeterManager.language.fget(manager) == expected


@pytest.mark.parametrize(
    ("cfg", "stored", "expected"),
    [
        ({}, {}, (1.0, 50.0)),
        ({}, {"params": {"short_airing_min": 4, "short_recovery_percent": 80}}, (1.0, 50.0)),
        ({"short_airing_min": 0, "short_recovery_percent": 0}, {}, (0.0, 0.0)),
    ],
)
def test_room_build_uses_configured_airing_or_defaults(cfg, stored, expected):
    from custom_components.house_assistant.heating.const import DEFAULTS
    from custom_components.house_assistant.heating.coordinator import HeatingCoordinator

    coordinator = SimpleNamespace(
        opt=lambda key: DEFAULTS.get(key),
        _apply_start_values=Mock(),
        _vent_start_values=lambda _: {},
        _apply_vent_start_values=Mock(),
    )
    area = HeatingCoordinator._build_area(
        coordinator, "room", "Room", {"temperature_sensor": "sensor.room", **cfg}, stored, 0
    )
    assert (area.params.short_airing_min, area.params.short_recovery_percent) == expected


def test_diagnostics_redact_house_notification_services():
    import asyncio

    from custom_components.house_assistant.diagnostics import async_get_config_entry_diagnostics

    entry = SimpleNamespace(
        runtime_data=SimpleNamespace(house=None, modules={}),
        as_dict=lambda: {
            "options": {
                "core": {
                    "notify_services": ["notify.private_phone"],
                    "outdoor_temperature": "sensor.outdoor",
                },
                "shutter": {},
            }
        },
    )
    result = asyncio.run(async_get_config_entry_diagnostics(None, entry))
    assert result["entry"]["options"]["core"]["notify_services"] == "**REDACTED**"
    assert result["entry"]["options"]["core"]["outdoor_temperature"] == "sensor.outdoor"
