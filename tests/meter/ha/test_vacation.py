"""Meters on vacation: a warning when water runs while nobody is at home."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

from homeassistant.core import HomeAssistant

from custom_components.house_assistant.const import EVENT_VACATION_ALERT

from .conftest import meters, setup_entry

SWITCH = "switch.house_assistant_vacation"
WATER = "sensor.water_meter_reading"
HEAT = "sensor.heat_meter_reading"


async def _vacation(hass: HomeAssistant, on: bool) -> None:
    await hass.services.async_call(
        "switch", "turn_on" if on else "turn_off", {"entity_id": SWITCH}, blocking=True
    )
    await hass.async_block_till_done()


async def test_leak_warning_once_per_vacation_and_case(
    hass: HomeAssistant, base, ai, freezer
) -> None:
    entry = await setup_entry(hass)
    found = {m.title: m for m in meters(entry).values()}
    for meter in found.values():
        meter.set_automatic(False)
    water, heat = found["Water"], found["Heat"]
    assert water.leak_warning and not heat.leak_warning
    ai.answers = ["100.000"] * 4
    await water.async_read()
    ai.answers = ["1.261"] * 4
    await heat.async_read()
    alerts = []
    hass.bus.async_listen(EVENT_VACATION_ALERT, alerts.append)
    await _vacation(hass, True)
    assert hass.states.get(WATER).attributes["vacation_alerts"] == []
    assert "vacation_alerts" not in hass.states.get(HEAT).attributes

    with patch(
        "custom_components.house_assistant.core.notify.persistent_notification.async_create"
    ) as notified:
        # 12 L in 2 h: 6 L/h above the 5 L/h, below the 20 L
        freezer.tick(timedelta(hours=2))
        ai.answers = ["100.012"] * 2
        assert await water.async_read() == "ok"
        await hass.async_block_till_done(wait_background_tasks=True)
        assert [a.data["case"] for a in alerts] == ["rate"]
        assert alerts[0].data["unit"] == "L"
        assert alerts[0].data["used"] == 12.0
        # 25 L in 4 h: the amount as well; the rate is not reported again
        freezer.tick(timedelta(hours=2))
        ai.answers = ["100.025"] * 2
        await water.async_read()
        await hass.async_block_till_done(wait_background_tasks=True)
        assert [a.data["case"] for a in alerts] == ["rate", "amount"]
        freezer.tick(timedelta(hours=2))
        ai.answers = ["100.050"] * 2
        await water.async_read()
        await hass.async_block_till_done(wait_background_tasks=True)
        assert len(alerts) == 2
        # the heat meter runs as the heating needs, no warning
        ai.answers = ["1.300"] * 2
        await heat.async_read()
        await hass.async_block_till_done(wait_background_tasks=True)
        assert len(alerts) == 2
    # without notification services of the house: a notification in Home Assistant
    assert notified.call_count == 2
    assert "25.0 L used" in notified.call_args_list[1].args[1]
    assert hass.states.get(WATER).attributes["vacation_alerts"] == ["rate", "amount"]

    # the next vacation counts anew, from the last reading before it
    await _vacation(hass, False)
    assert "vacation_alerts" not in hass.states.get(WATER).attributes
    await _vacation(hass, True)
    assert water.state.vacation["value"] == 100.05
    assert water.state.vacation["alerts"] == []
