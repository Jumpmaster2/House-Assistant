"""Shared input validation without a running Home Assistant instance."""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import probatio as vol
import pytest
from homeassistant.core import Context, ServiceCall
from homeassistant.exceptions import ServiceValidationError, Unauthorized

from custom_components.house_assistant.core.auth import require_admin
from custom_components.house_assistant.core.logic.numbers import reject_constant
from custom_components.house_assistant.core.schema import number, spec
from custom_components.house_assistant.heating.config_flow import _number as heating_number
from custom_components.house_assistant.heating.config_flow import _validate_limits, validate_area
from custom_components.house_assistant.heating.logic.ai_schema import (
    VENT_PARAMS,
    AnswerError,
    default_limits,
    normalize_limits,
    validate_check,
    validate_nightly,
)
from custom_components.house_assistant.heating.validation import normalize_options
from custom_components.house_assistant.heating.websocket import PanelError, _limits, apply_options
from custom_components.house_assistant.meter.logic.reading import consensus, normalize
from custom_components.house_assistant.meter.meter import Meter
from custom_components.house_assistant.meter.services import SET_SCHEMA
from custom_components.house_assistant.meter.validation import reading_value
from custom_components.house_assistant.meter.websocket import ws_set_reading
from custom_components.house_assistant.shutter.config_flow import _number as shutter_number


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "nan", "Infinity"])
def test_number_selectors(value):
    for selector in (number(0, 100, 1), heating_number(0, 100, 1), shutter_number(0, 100, 1)):
        with pytest.raises(vol.Invalid):
            selector(value)
    assert spec(number(0, 100, 1))["selector"] == "number"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "nan", -1])
def test_reading_rejected_before_mutation(value):
    with pytest.raises(ServiceValidationError):
        ws_set_reading._ws_schema(
            {
                "id": 1,
                "type": "house_assistant/meter/set_reading",
                "subentry_id": "meter",
                "value": value,
            }
        )
    meter = Mock(state=Mock(value=12, history=[["before", 12]]))
    with pytest.raises(ServiceValidationError):
        Meter.set_reading(meter, value)
    assert meter.state.value == 12
    assert meter.state.history == [["before", 12]]
    meter.manager.async_save.assert_not_called()
    meter.notify.assert_not_called()
    with pytest.raises(ServiceValidationError):
        SET_SCHEMA({"entity_id": ["sensor.meter"], "value": value})
    with pytest.raises(ServiceValidationError):
        reading_value(value)


@pytest.mark.parametrize("value", [0, 12.5, "12.5"])
def test_reading_valid(value):
    assert ws_set_reading._ws_schema(
        {
            "id": 1,
            "type": "house_assistant/meter/set_reading",
            "subentry_id": "meter",
            "value": value,
        }
    )["value"] == float(value)
    assert reading_value(value) == float(value)
    assert SET_SCHEMA({"entity_id": ["sensor.meter"], "value": value})["value"] == float(value)


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
def test_json_constants(constant):
    with pytest.raises(ValueError):
        json.loads('{"value": ' + constant + "}", parse_constant=reject_constant)
    assert json.loads(json.dumps(constant), parse_constant=reject_constant) == constant
    assert consensus([constant, constant]) is None
    assert normalize(constant) == "unreadable"


def test_meter_overflow_is_not_a_reading():
    enormous = "9" * 400
    assert consensus([enormous, enormous]) is None
    assert normalize(enormous) == "unreadable"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), "NaN", "Infinity"])
def test_ai_keeps_other_changes(value):
    result = validate_check(
        {
            "adjustments": [
                {"area": "a", "parameter": "hysteresis_on", "value": value},
                {"area": "a", "parameter": "puffer", "value": 0.8},
            ],
            "confidence": 80,
        },
        {"a": {"hysteresis_on": 0.2, "puffer": 0.7}},
        default_limits(),
    )
    assert [a.parameter for a in result.applied] == ["puffer"]
    assert len(result.rejected) == 1
    with pytest.raises(AnswerError):
        validate_nightly({"heating_day": True, "confidence": value})
    limits = default_limits()
    limits["puffer"]["max"] = value
    result = validate_check(
        {"adjustments": [{"area": "a", "parameter": "puffer", "value": 0.8}], "confidence": 80},
        {"a": {"puffer": 0.7}},
        limits,
    )
    assert result.applied[0].new == 0.8
    assert not result.rejected


@pytest.mark.parametrize(
    "limit,error",
    [
        ({"min": 0, "max": 0.6, "step": 0.1}, None),
        ({"min": -1000000, "max": 1000000, "step": 1}, "invalid_value"),
        ({"min": 0.5, "max": 0.1, "step": 0.1}, "min_above_max"),
        ({"min": 0, "max": 0.6, "step": 0}, None),
        ({"min": 0, "max": 0.6, "step": -1}, "invalid_value"),
        ({"min": 0, "max": 0.6, "step": 1}, "invalid_value"),
        ({"min": float("nan"), "max": 0.6, "step": 0.1}, "invalid_value"),
    ],
)
def test_dialog_panel_same_limits(limit, error):
    submitted = {**default_limits(), "hysteresis_on": limit}
    limits, errors = _validate_limits(submitted)
    if error:
        assert errors["hysteresis_on"] == error
        with pytest.raises(PanelError, match=error):
            _limits({"hysteresis_on": limit}, {})
    else:
        assert not errors
        assert _limits({"hysteresis_on": limit}, {}) == limits


def test_old_limits_and_durations_are_idempotent():
    old = {
        "limits": {"hysteresis_on": {"min": -1000000, "max": 1000000, "step": -1}},
        "ventilation_airing_min_minutes": 15,
        "ventilation_airing_max_minutes": 5,
    }
    new = normalize_options(old)
    assert new["limits"]["hysteresis_on"] == {"min": -1000000, "max": 1000000, "step": 0.1}
    assert new["ventilation_airing_min_minutes"] == 5
    assert normalize_options(new) == new
    assert normalize_limits(new["limits"]) == new["limits"]
    assert old["ventilation_airing_min_minutes"] == 15


@pytest.mark.parametrize("low,high,valid", [(5, 5, True), (3, 20, True), (15, 5, False)])
def test_panel_airing_order(low, high, valid):
    values = {"ventilation_airing_min_minutes": low, "ventilation_airing_max_minutes": high}
    if valid:
        assert apply_options({}, values, {"outdoor_temperature": "sensor.outdoor"}) == values
    else:
        with pytest.raises(PanelError, match="airing_min_above_max"):
            apply_options({}, values, {"outdoor_temperature": "sensor.outdoor"})


@pytest.mark.parametrize("key,value", [("airing_min_minutes", 15), ("airing_max_minutes", 5)])
def test_ai_cannot_invert_airing_order(key, value):
    limits = default_limits()
    limits[key]["step"] = 50 if "max" in key else 10
    result = validate_check(
        {"adjustments": [{"area": "a", "parameter": key, "value": value}], "confidence": 90},
        {"a": {"airing_min_minutes": 10, "airing_max_minutes": 10}},
        limits,
        VENT_PARAMS,
    )
    assert not result.applied and result.rejected


def test_equal_targets_are_a_valid_range():
    assert not validate_area(
        {"name": "Room", "min_target": 21, "default_target": 21, "max_target": 21}
    )


@pytest.mark.parametrize(
    "user,allowed", [(None, True), ("admin", True), ("member", False), ("unknown", False)]
)
async def test_admin_matrix(user, allowed):
    hass = SimpleNamespace(
        auth=SimpleNamespace(
            async_get_user=AsyncMock(
                return_value=None
                if user == "unknown"
                else SimpleNamespace(is_admin=user == "admin")
            )
        )
    )
    call = ServiceCall(hass, "house_assistant", "test", {}, context=Context(user_id=user))
    if allowed:
        await require_admin(hass, call)
    else:
        with pytest.raises(Unauthorized):
            await require_admin(hass, call)


@pytest.mark.parametrize(
    "service,module",
    [
        ("set_vacation", "core"),
        ("set_meter_reading", "meter"),
        ("read_meter", "meter"),
        ("reset_learned", "heating"),
        ("import_parameters", "heating"),
        ("run_ai_check", "heating"),
        ("run_ai_ventilation_check", "heating"),
        ("decide_heating_day", "heating"),
    ],
)
@pytest.mark.parametrize(
    "user,allowed", [(None, True), ("admin", True), ("member", False), ("unknown", False)]
)
async def test_service_admin_matrix(service, module, user, allowed):
    from importlib import import_module
    from unittest.mock import patch

    services = import_module(f"custom_components.house_assistant.{module}.services")
    hass = Mock()
    hass.auth.async_get_user = AsyncMock(
        return_value=None if user == "unknown" else SimpleNamespace(is_admin=user == "admin")
    )
    services.async_setup_services(hass)
    handler = next(
        c.args[2] for c in hass.services.async_register.call_args_list if c.args[1] == service
    )
    target = Mock()
    for key in (
        "async_request_refresh",
        "async_run_ai_check",
        "async_run_vent_check",
        "async_decide_heating_day",
    ):
        setattr(target, key, AsyncMock())
    resolver = (
        "_house" if module == "core" else "meters_for" if module == "meter" else "_coordinator"
    )
    call = ServiceCall(
        hass,
        "house_assistant",
        service,
        {
            "clear": True,
            "entity_id": [],
            "value": 12,
            "include_parameters": False,
            "data": {},
            "use_ai": False,
        },
        context=Context(user_id=user),
    )
    with patch.object(
        services, resolver, return_value=[target] if module == "meter" else target
    ) as resolve:
        if allowed:
            await handler(call)
            resolve.assert_called_once()
            assert target.mock_calls
        else:
            with pytest.raises(Unauthorized):
                await handler(call)
            resolve.assert_not_called()
            assert not target.mock_calls


@pytest.mark.parametrize("constant", ["NaN", "Infinity", "-Infinity"])
async def test_ai_client_rejects_json_constants(constant):
    from custom_components.house_assistant.heating.ai_client import AiError, ClaudeClient

    sdk = Mock()
    sdk.messages.create = AsyncMock(
        return_value=SimpleNamespace(
            content=[SimpleNamespace(type="text", text='{"confidence": ' + constant + "}")],
            usage=SimpleNamespace(input_tokens=0, output_tokens=0),
            stop_reason="end_turn",
        )
    )
    client = ClaudeClient(sdk, "test", "auto")
    with pytest.raises(AiError, match="not valid JSON"):
        await client.structured("", "", {}, 100)


@pytest.mark.parametrize("low,high,valid", [(5, 5, True), (3, 20, True), (15, 5, False)])
async def test_dialog_airing_order(low, high, valid):
    from custom_components.house_assistant.heating.config_flow import HeatingOptionsSteps
    from custom_components.house_assistant.heating.const import DEFAULTS

    flow = SimpleNamespace(_heating_save=Mock(), _heating_form=Mock(), _heating_values=DEFAULTS)
    values = {
        **DEFAULTS,
        "ventilation_airing_min_minutes": low,
        "ventilation_airing_max_minutes": high,
    }
    await HeatingOptionsSteps.async_step_heating_ventilation(flow, values)
    if valid:
        flow._heating_save.assert_called_once_with(values)
    else:
        flow._heating_save.assert_not_called()
        assert flow._heating_form.call_args.args[2] == {
            "ventilation_airing_min_minutes": "airing_min_above_max"
        }


def test_loaded_airing_parameters_repaired_idempotently():
    from custom_components.house_assistant.heating.coordinator import HeatingCoordinator
    from custom_components.house_assistant.heating.logic.ai_schema import PARAMS

    area = SimpleNamespace(
        area_id="room",
        params=SimpleNamespace(**{k: p.default for k, p in PARAMS.items()}),
        vent_params=SimpleNamespace(**{k: p.default for k, p in VENT_PARAMS.items()}),
    )
    area.vent_params.airing_min_minutes = 15
    area.vent_params.airing_max_minutes = 5
    coordinator = SimpleNamespace(areas={"room": area}, limits=default_limits(), theta=16)
    HeatingCoordinator._clamp_to_limits(coordinator)
    assert area.vent_params.airing_min_minutes == 5
    HeatingCoordinator._clamp_to_limits(coordinator)
    assert area.vent_params.airing_min_minutes == 5


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        (0, True),
        (12, True),
        (72, True),
        (-1, False),
        (73, False),
        (1.5, False),
        (float("nan"), False),
        (float("inf"), False),
        (-float("inf"), False),
    ],
)
def test_stale_hours_dialog_and_panel_agree(value, valid):
    from custom_components.house_assistant.heating.config_flow import rules_schema

    values = {
        "emergency_enabled": True,
        "emergency_delta": 1,
        "emergency_duration": 45,
        "emergency_window_quiet": 30,
        "force_on_below": 1,
        "sensor_stale_hours": value,
    }
    house = {"outdoor_temperature": "sensor.outdoor_temperature"}
    if valid:
        assert rules_schema({})(values)["sensor_stale_hours"] == value
        assert (
            apply_options({}, {"sensor_stale_hours": value}, house)["sensor_stale_hours"] == value
        )
    else:
        with pytest.raises(vol.Invalid):
            rules_schema({})(values)
        with pytest.raises(PanelError, match="invalid_value:sensor_stale_hours"):
            apply_options({}, {"sensor_stale_hours": value}, house)
