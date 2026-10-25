"""Rooms and windows of the house: entered once, used by the heating and the covers."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import SOURCE_USER, ConfigSubentry, ConfigSubentryData
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.house_assistant.const import DOMAIN
from custom_components.house_assistant.core.house import room_contacts, window_errors
from custom_components.house_assistant.heating.const import DEFAULTS as HEATING_DEFAULTS
from custom_components.house_assistant.heating.logic.ai_schema import default_limits

LIVING = "room_living"
STORAGE = "room_storage"
WINDOW = "window_living"
DOOR = "window_door"

ROOM_DATA = {
    "name": "Living room",
    "temperature_sensor": "sensor.living_temperature",
    "heater_switch": "input_boolean.circuit",
    "default_target": 21.0,
}


def _sub(sub_id: str, kind: str, data: dict[str, Any]) -> ConfigSubentryData:
    return ConfigSubentryData(
        data=data, subentry_id=sub_id, subentry_type=kind, title=data["name"], unique_id=None
    )


def make_entry(
    modules: list[str], extra: list[ConfigSubentryData] | None = None
) -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="House Assistant",
        data={"api_key": ""},
        options={
            "core": {"modules": modules},
            "heating": {
                **HEATING_DEFAULTS,
                "outdoor_temperature": "sensor.outdoor",
                "limits": default_limits(),
            },
            "shutter": {"outdoor_temperature": "sensor.outdoor", "verify_after": 0},
        },
        subentries_data=[
            _sub(LIVING, "room", ROOM_DATA),
            _sub(STORAGE, "room", {"name": "Storage"}),
            _sub(
                WINDOW,
                "window",
                {
                    "name": "Living window",
                    "room": LIVING,
                    "size": "large",
                    "window_sensors": ["binary_sensor.living_window"],
                },
            ),
            _sub(
                DOOR,
                "window",
                {
                    "name": "Balcony door",
                    "room": LIVING,
                    "size": "door",
                    "window_sensors": ["binary_sensor.balcony_door"],
                    "cover": "cover.balcony",
                },
            ),
            *(extra or []),
        ],
    )


async def _setup(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    await hass.config.async_set_time_zone("Europe/Berlin")
    hass.states.async_set("sensor.outdoor", "5", {"unit_of_measurement": "°C"})
    hass.states.async_set("sensor.living_temperature", "20", {"unit_of_measurement": "°C"})
    hass.states.async_set("binary_sensor.living_window", "off")
    hass.states.async_set("binary_sensor.balcony_door", "off")
    hass.states.async_set("input_boolean.circuit", "off")
    hass.states.async_set("cover.balcony", "open", {"current_position": 100})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)


async def test_window_basics_are_checked(hass: HomeAssistant) -> None:
    entry = make_entry([])
    entry.add_to_hass(hass)
    assert window_errors(entry, {"name": "", "cover": "cover.x"}, None) == {"name": "name_required"}
    assert window_errors(entry, {"name": "Skylight"}, None) == {"base": "contact_or_cover_required"}
    # a contact or a cover belongs to one window only
    assert window_errors(
        entry, {"name": "Copy", "window_sensors": ["binary_sensor.living_window"]}, None
    ) == {"window_sensors": "contact_in_use"}
    assert (
        window_errors(
            entry, {"name": "Copy", "window_sensors": ["binary_sensor.living_window"]}, WINDOW
        )
        == {}
    )
    assert window_errors(entry, {"name": "Copy", "cover": "cover.balcony"}, None) == {
        "cover": "cover_in_use"
    }
    assert window_errors(entry, {"name": "X", "cover": "cover.x", "room": "room_gone"}, None) == {
        "room": "unknown_room"
    }
    # the contacts of a room by the size of their window
    assert room_contacts(entry, LIVING) == {
        "small": [],
        "medium": [],
        "large": ["binary_sensor.living_window"],
        "door": ["binary_sensor.balcony_door"],
    }


async def test_rooms_and_windows_are_house_subentries(hass: HomeAssistant) -> None:
    from custom_components.house_assistant.config_flow import HouseAssistantConfigFlow

    entry = make_entry([])
    entry.add_to_hass(hass)
    assert set(HouseAssistantConfigFlow.async_get_supported_subentry_types(entry)) == {
        "room",
        "window",
    }
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": ["shutter", "meter"]}}
    )
    assert set(HouseAssistantConfigFlow.async_get_supported_subentry_types(entry)) == {
        "room",
        "window",
        "group",
        "meter",
    }


async def test_heating_takes_the_contacts_of_the_windows(hass: HomeAssistant) -> None:
    entry = make_entry(["heating"])
    await _setup(hass, entry)
    coordinator = entry.runtime_data.modules["heating"].coordinator
    # only rooms with a temperature sensor are heated
    assert set(coordinator.areas) == {LIVING}
    assert hass.states.get("climate.living_room") is not None
    area = coordinator.areas[LIVING]
    assert area.cfg["window_sensors_large"] == ["binary_sensor.living_window"]
    assert area.cfg["door_sensors"] == ["binary_sensor.balcony_door"]

    # a new window of the room restarts the heating with its contact
    skylight = {
        "name": "Skylight",
        "room": LIVING,
        "size": "small",
        "window_sensors": ["binary_sensor.sky"],
    }
    hass.config_entries.async_add_subentry(
        entry,
        ConfigSubentry(data=skylight, subentry_type="window", title="Skylight", unique_id=None),
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    coordinator = entry.runtime_data.modules["heating"].coordinator
    assert coordinator.areas[LIVING].cfg["window_sensors_small"] == ["binary_sensor.sky"]


async def test_room_device_follows_the_area_of_the_room(hass: HomeAssistant) -> None:
    lounge = ar.async_get(hass).async_create("Lounge")
    entry = make_entry(["heating"])
    entry.add_to_hass(hass)
    hass.config_entries.async_update_subentry(
        entry, entry.subentries[LIVING], data={**ROOM_DATA, "area": lounge.id}
    )
    await _setup(hass, entry)
    device = dr.async_get(hass).async_get_device_by_identifier((DOMAIN, LIVING), entry.entry_id)
    assert device is not None and device.area_id == lounge.id

    kitchen = ar.async_get(hass).async_create("Kitchen")
    hass.config_entries.async_update_subentry(
        entry, entry.subentries[LIVING], data={**ROOM_DATA, "area": kitchen.id}
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    device = dr.async_get(hass).async_get_device_by_identifier((DOMAIN, LIVING), entry.entry_id)
    assert device.area_id == kitchen.id


async def test_covers_take_the_room_of_their_window(hass: HomeAssistant) -> None:
    hass.states.async_set("climate.room_ac", "cool")
    entry = make_entry(["heating", "shutter"])
    entry.add_to_hass(hass)
    hass.config_entries.async_update_subentry(
        entry, entry.subentries[LIVING], data={**ROOM_DATA, "cooling_entity": "climate.room_ac"}
    )
    await _setup(hass, entry)
    engine = entry.runtime_data.modules["shutter"].engine
    # a window without a cover only serves the heating
    assert set(engine.windows) == {DOOR}
    win = engine.windows[DOOR]
    assert win.conf["cooling_entity"] == "climate.room_ac"
    # room temperature from the sensor of the room, the target from its thermostat
    assert engine._room(win) == (20.0, 21.0)
    heating = entry.runtime_data.modules["heating"].coordinator
    await heating.async_set_target(LIVING, 19.0)
    await hass.async_block_till_done()
    assert engine._room(win) == (20.0, 19.0)
    assert not engine.room_warm(win)  # too warm only from target + margin (2 K)
    hass.states.async_set("sensor.living_temperature", "21.5", {"unit_of_measurement": "°C"})
    await hass.async_block_till_done()
    assert engine._room(win)[0] == 21.5
    assert engine.room_warm(win)

    # without the heating module the threshold of the window counts (no target)
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "core": {"modules": ["shutter"]}}
    )
    await hass.async_block_till_done(wait_background_tasks=True)
    engine = entry.runtime_data.modules["shutter"].engine
    assert engine._room(engine.windows[DOOR]) == (21.5, None)


async def test_window_dialog_without_and_with_cover(hass: HomeAssistant) -> None:
    entry = make_entry(["heating", "shutter"])
    await _setup(hass, entry)
    flow = hass.config_entries.subentries
    result = await flow.async_init((entry.entry_id, "window"), context={"source": SOURCE_USER})
    assert result["step_id"] == "basics"
    result = await flow.async_configure(
        result["flow_id"],
        {"name": "Hall", "size": "small", "window_sensors": ["binary_sensor.living_window"]},
    )
    assert result["errors"] == {"window_sensors": "contact_in_use"}
    result = await flow.async_configure(
        result["flow_id"],
        {
            "name": "Hall",
            "room": STORAGE,
            "size": "small",
            "window_sensors": ["binary_sensor.hall"],
        },
    )
    # without a cover the window is complete after its basics
    assert result["type"] is FlowResultType.CREATE_ENTRY
    hall = next(s for s in entry.subentries.values() if s.title == "Hall")
    assert hall.data == {
        "name": "Hall",
        "room": STORAGE,
        "size": "small",
        "window_sensors": ["binary_sensor.hall"],
        "tilt_sensors": [],
    }

    result = await flow.async_init((entry.entry_id, "window"), context={"source": SOURCE_USER})
    result = await flow.async_configure(
        result["flow_id"], {"name": "Kitchen", "size": "medium", "cover": "cover.kitchen"}
    )
    # with a cover the settings of the cover follow
    assert result["type"] is FlowResultType.FORM and result["step_id"] == "behavior"


async def test_house_panel_edits_rooms_and_windows(hass: HomeAssistant, hass_ws_client) -> None:
    entry = make_entry(["heating", "shutter"])
    await _setup(hass, entry)
    client = await hass_ws_client(hass)

    await client.send_json({"id": 1, "type": "house_assistant/house/config"})
    msg = await client.receive_json()
    assert msg["success"], msg
    result = msg["result"]
    assert [r["id"] for r in result["rooms"]] == [LIVING, STORAGE]
    living = result["rooms"][0]
    assert living["windows"] == [WINDOW, DOOR] and living["climate"] == "climate.living_room"
    assert {"area", "floor_area", "temperature_sensor", "cooling_entity"} <= set(
        result["fields"]["room"]
    )
    assert {"room", "size", "cover", "window_sensors"} <= set(result["fields"]["window"])
    assert "heater_switch" not in result["fields"]["room"]  # in the heating section

    # changing the basics of a room keeps the settings of the heating
    await client.send_json(
        {
            "id": 2,
            "type": "house_assistant/house/save",
            "subentry_type": "room",
            "subentry_id": LIVING,
            "title": "Lounge",
            "data": {
                "temperature_sensor": "sensor.living_temperature",
                "humidity_sensor": "",
                "floor_area": 18.5,
            },
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    data = entry.subentries[LIVING].data
    assert entry.subentries[LIVING].title == "Lounge"
    assert data["heater_switch"] == "input_boolean.circuit"
    assert data["default_target"] == 21.0
    assert data["floor_area"] == 18.5

    # a floor area outside 1 to 200 m² is refused, the room keeps its area
    await client.send_json(
        {
            "id": 3,
            "type": "house_assistant/house/save",
            "subentry_type": "room",
            "subentry_id": LIVING,
            "title": "Lounge",
            "data": {"temperature_sensor": "sensor.living_temperature", "floor_area": 500},
        }
    )
    msg = await client.receive_json()
    assert not msg["success"]
    assert msg["error"]["message"] == "invalid_value:floor_area"
    assert entry.subentries[LIVING].data["floor_area"] == 18.5

    # a contact of another window is refused, a new window is added
    await client.send_json(
        {
            "id": 4,
            "type": "house_assistant/house/save",
            "subentry_type": "window",
            "title": "Copy",
            "data": {"window_sensors": ["binary_sensor.living_window"]},
        }
    )
    msg = await client.receive_json()
    assert not msg["success"]
    assert msg["error"]["message"] == "contact_in_use:window_sensors"
    await client.send_json(
        {
            "id": 5,
            "type": "house_assistant/house/save",
            "subentry_type": "window",
            "title": "Storage window",
            "data": {"room": STORAGE, "size": "small", "window_sensors": ["binary_sensor.s"]},
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    new_id = msg["result"]["subentry_id"]
    assert entry.subentries[new_id].data["room"] == STORAGE

    # the cover settings of a window stay when its basics change
    hass.config_entries.async_update_subentry(
        entry, entry.subentries[DOOR], data={**entry.subentries[DOOR].data, "sun_position": 30}
    )
    await client.send_json(
        {
            "id": 6,
            "type": "house_assistant/house/save",
            "subentry_type": "window",
            "subentry_id": DOOR,
            "title": "Balcony door",
            "data": {
                "room": LIVING,
                "size": "large",
                "cover": "cover.balcony",
                "window_sensors": ["binary_sensor.balcony_door"],
            },
        }
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    assert entry.subentries[DOOR].data["size"] == "large"
    assert entry.subentries[DOOR].data["sun_position"] == 30

    # the windows of a deleted room stay, without a room
    await client.send_json(
        {"id": 7, "type": "house_assistant/house/delete", "subentry_id": STORAGE}
    )
    msg = await client.receive_json()
    assert msg["success"], msg
    assert STORAGE not in entry.subentries
    assert "room" not in entry.subentries[new_id].data
