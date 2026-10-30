"""Native room dialog, thermostat attribute and restoration of pipe configuration."""

from homeassistant.data_entry_flow import FlowResultType

from custom_components.house_assistant.heating.websocket import config_payload

from .conftest import AREA_DATA, VENT_ONLY_DATA, heating, make_entry


async def test_pipe_dialog_attribute_panel_and_reload(hass, base_states):
    hass.states.async_set("input_boolean.source", "on")
    hass.states.async_set("sensor.living_room_temperature", "21.0")
    entry = make_entry(
        areas=[
            {
                **AREA_DATA,
                "pipe_sources": ["room_2", "room_3", "room_4", "deleted", "room_1"],
                "pipe_gain": 0.3,
                "pipe_source_weights": {"room_2": 2.0, "room_3": 3.0, "deleted": 3.0},
            },
            {
                **VENT_ONLY_DATA,
                "name": "Pia",
                "heater_switch": "input_boolean.source",
                "min_on_time": 120,
            },
            {**VENT_ONLY_DATA, "name": "Abstellkammer"},
            {**VENT_ONLY_DATA, "name": "Schlafzimmer"},
        ]
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done(wait_background_tasks=True)
    assert hass.states.get("climate.living_room").attributes["pipe_active"] is True
    coordinator = heating(entry)
    a = coordinator.areas["room_1"]
    assert coordinator._pipe_rate(a) == 0.6
    payload = config_payload(hass, entry)
    target = payload["areas"][0]
    assert target["data"]["pipe_sources"] == ["room_2"]
    assert target["data"]["pipe_source_weights"] == {"room_2": 2.0}
    assert target["pipe"]["learned"] is False
    assert target["pipe"]["factor"] == 1
    result = await entry.start_subentry_reconfigure_flow(hass, "room_1")
    schema = result["data_schema"]
    sections = {str(k): v for k, v in schema.schema.items()}
    fields = {str(k): v for k, v in sections["pipe_heat"].schema.schema.items()}
    assert fields["pipe_sources"].config["options"] == [{"value": "room_2", "label": "Pia"}]
    weights = fields["pipe_source_weights"]
    assert set(weights.config["fields"]) == {"room_2"}
    assert weights({"room_2": 0.1}) == {"room_2": 0.1}
    # An older client may omit the section entirely. Its existing gain survives.
    user_input = {str(k): {} for k in schema.schema if str(k) != "pipe_heat"}
    user_input["heating"] = {"heater_switch": AREA_DATA["heater_switch"]}
    result = await hass.config_entries.subentries.async_configure(result["flow_id"], user_input)
    assert result["type"] is FlowResultType.ABORT
    assert entry.subentries["room_1"].data["pipe_sources"] == ["room_2"]
    assert entry.subentries["room_1"].data["pipe_gain"] == 0.3
    assert entry.subentries["room_1"].data["pipe_source_weights"] == {"room_2": 2.0}
    await hass.async_block_till_done(wait_background_tasks=True)
    result = await entry.start_subentry_reconfigure_flow(hass, "room_1")
    user_input = {str(k): {} for k in result["data_schema"].schema}
    user_input["pipe_heat"] = {
        "pipe_sources": ["room_2"],
        "pipe_gain": 0.3,
        "pipe_source_weights": {"room_2": 0.5},
    }
    user_input["heating"] = {"heater_switch": AREA_DATA["heater_switch"]}
    result = await hass.config_entries.subentries.async_configure(result["flow_id"], user_input)
    assert result["type"] is FlowResultType.ABORT
    assert entry.subentries["room_1"].data["pipe_source_weights"] == {"room_2": 0.5}
    await hass.async_block_till_done(wait_background_tasks=True)
    coordinator = heating(entry)
    assert coordinator._pipe_rate(coordinator.areas["room_1"]) == 0.15
    panel = config_payload(hass, entry)
    assert panel["areas"][0]["pipe"]["source_weights"] == {"a2": 0.5}
    assert set(panel["area_specs"]["pipe_source_weights"]["fields"]) == {"room_1", "room_2"}
    result = await entry.start_subentry_reconfigure_flow(hass, "room_1")
    user_input = {str(k): {} for k in result["data_schema"].schema}
    user_input["pipe_heat"] = {"pipe_sources": [], "pipe_gain": 0.45}
    user_input["heating"] = {"heater_switch": AREA_DATA["heater_switch"]}
    result = await hass.config_entries.subentries.async_configure(result["flow_id"], user_input)
    assert result["type"] is FlowResultType.ABORT
    assert entry.subentries["room_1"].data["pipe_sources"] == []
    assert entry.subentries["room_1"].data["pipe_gain"] == 0.45
    assert entry.subentries["room_1"].data["pipe_source_weights"] == {}
