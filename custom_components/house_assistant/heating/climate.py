"""Climate entity per heating area (target is stored permanently, no schedules)."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_TENTHS, UnitOfTemperature

from .const import CONF_HUMIDITY_SENSOR, CONF_MAX_TARGET, CONF_MIN_TARGET, CONF_TEMP_SENSOR
from .coordinator import HeatingCoordinator
from .entity import AreaEntity

# Home Assistant 2026.11 renames the temperature properties to native_*.
_NATIVE = hasattr(ClimateEntity, "native_current_temperature")

# Slack on the limits: a limit shown in °F and converted back misses the °C value by
# a rounding error, the service would reject it.
_LIMIT_SLACK = 0.01


def _tenth(value: float | None) -> float | None:
    return None if value is None else round(value, 1)


class AreaClimate(AreaEntity, ClimateEntity):
    """Thermostat of one area."""

    _attr_name = None
    _attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )
    _attr_target_temperature_step = 0.1
    # Tenths also in °F, otherwise +/- by 0.1 would not move the rounded target.
    _attr_precision = PRECISION_TENTHS
    # Forecast values change almost every minute: not recorded, and rounded so that the
    # state (and its row in the recorder) changes only when the shown value does.
    _unrecorded_attributes = frozenset(
        {
            "predicted_temperature",
            "expected_peak",
            "expected_pv_kw",
            "temperature_sensor",
            "humidity_sensor",
        }
    )

    if _NATIVE:
        _attr_native_temperature_unit = UnitOfTemperature.CELSIUS

        @property
        def native_current_temperature(self) -> float | None:
            return self.area.temp

        @property
        def native_target_temperature(self) -> float | None:
            return self.area.target

    else:
        _attr_temperature_unit = UnitOfTemperature.CELSIUS

        @property
        def current_temperature(self) -> float | None:
            return self.area.temp

        @property
        def target_temperature(self) -> float | None:
            return self.area.target

    def __init__(self, coordinator: HeatingCoordinator, area_id: str) -> None:
        super().__init__(coordinator, area_id, "area")
        self._attr_unique_id = f"{area_id}_climate"
        cfg = coordinator.areas[area_id].cfg
        self._min_target = float(cfg.get(CONF_MIN_TARGET, 16.0))
        self._max_target = float(cfg.get(CONF_MAX_TARGET, 24.0))
        self._attr_min_temp = self._min_target - _LIMIT_SLACK
        self._attr_max_temp = self._max_target + _LIMIT_SLACK

    @property
    def current_humidity(self) -> float | None:
        return self.area.humidity

    @property
    def hvac_mode(self) -> HVACMode:
        return HVACMode.HEAT if self.area.hvac_on else HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction:
        area = self.area
        if area.switch_on:
            return HVACAction.HEATING
        return HVACAction.IDLE if area.hvac_on else HVACAction.OFF

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        area = self.area
        decision = area.decision
        return {
            "status": area.status,
            "draft": area.draft,
            # the windows of the combination behind a draft or a cross ventilation
            "draft_windows": area.draft_windows or None,
            "effective_target": area.effective_target,
            # vacation temperature in force (not while preheating for the return)
            "vacation_active": bool(area.vacation and not area.preheat),
            "heating_day": self.coordinator.heating_day,
            "predicted_temperature": _tenth(decision.predicted_temp) if decision else None,
            "expected_peak": _tenth(decision.expected_peak) if decision else None,
            "expected_pv_kw": _tenth(area.learned_values.pv_plan_kw) if area.has_circuit else None,
            # the sensors of the room: the cards open their history on a tap
            "temperature_sensor": area.cfg.get(CONF_TEMP_SENSOR),
            "humidity_sensor": area.cfg.get(CONF_HUMIDITY_SENSOR) or None,
        }

    async def async_set_temperature(self, **kwargs: Any) -> None:
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            value = min(max(float(temperature), self._min_target), self._max_target)
            await self.coordinator.async_set_target(self.area_id, value)
        if (mode := kwargs.get("hvac_mode")) is not None:
            await self.async_set_hvac_mode(mode)

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        await self.coordinator.async_set_hvac(self.area_id, hvac_mode == HVACMode.HEAT)

    async def async_turn_on(self) -> None:
        await self.coordinator.async_set_hvac(self.area_id, True)

    async def async_turn_off(self) -> None:
        await self.coordinator.async_set_hvac(self.area_id, False)
