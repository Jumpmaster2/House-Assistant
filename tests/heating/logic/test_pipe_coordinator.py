"""Pipe payloads, statistics and configuration using the real coordinator methods."""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import probatio as vol
import pytest
from homeassistant.config_entries import ConfigSubentry

from custom_components.house_assistant.core.store_validation import template, validate
from custom_components.house_assistant.heating.config_flow import area_schema, other_areas
from custom_components.house_assistant.heating.const import DEFAULTS
from custom_components.house_assistant.heating.coordinator import (
    HeatingCoordinator,
    _new_check_stats,
)
from custom_components.house_assistant.heating.logic.ai_schema import default_limits
from custom_components.house_assistant.heating.logic.heating_day import RuleResult
from custom_components.house_assistant.heating.logic.learning import (
    AreaLearner,
    Sample,
    learner_schema,
)
from custom_components.house_assistant.heating.websocket import PanelError, _fields, area_data


class PipeCoordinator(HeatingCoordinator):
    """Only external IO is replaced; all pipe, model, count and payload code is real."""

    def __init__(self):
        self.areas = {}
        self.states = {}
        self.hass = SimpleNamespace(
            states=SimpleNamespace(get=self.states.get), config=SimpleNamespace(language="en")
        )
        self.day_state = {"theta": 16}
        self.ai_state = {}
        self.outdoor_temp = 5
        self.pv_kw = 0
        self.sun_scale = SimpleNamespace(value=None)
        self._pv_points = []
        self._forecast = AsyncMock(return_value=[])
        self._ai_call = AsyncMock(return_value=None)
        self._schedule_check = Mock()
        self._log = Mock()
        self.meter = Mock()

    @property
    def opts(self):
        return DEFAULTS

    @property
    def limits(self):
        return default_limits()

    @property
    def pv_assumed(self):
        return self.pv_kw


def _coordinator():
    c = PipeCoordinator()
    for i, (key, sources) in enumerate(
        [("target", ["source", "deleted", "target"]), ("source", ["target"]), ("plain", [])]
    ):
        a = c._build_area(
            key,
            key.title(),
            {"heater_switch": f"switch.{key}", "pipe_sources": sources, "pipe_gain": 0.2},
            {},
            i,
        )
        a.temp = 21.5
        c.areas[key] = a
        c.states[f"switch.{key}"] = SimpleNamespace(state="off")
    c.states["switch.source"].state = "on"
    return c


def test_actual_state_weighting_cycles_and_unavailable_sources():
    c = _coordinator()
    target, source = c.areas["target"], c.areas["source"]
    assert c._pipe_rate(target) == 0.2
    assert c.pipe_active(target)
    assert not c.pipe_active(source)  # requested heat/other pipe gain never feeds back
    source.switch_on = False  # stale cached state must not matter
    assert c._pipe_rate(target) == 0.2
    c.states["switch.source"].state = "unavailable"
    assert c._pipe_rate(target) == 0
    c.states["switch.source"].state = "on"
    target.cfg["pipe_sources"] = ["source", "plain"]
    assert c._pipe_rate(target) == 0.2  # adding an idle source never dilutes active heat
    target.cfg["pipe_source_weights"] = {"source": 2.0, "plain": 0.5, "deleted": 3.0}
    assert c._pipe_rate(target) == 0.4
    assert c._learned_values(target, 0, 1000).pipe_rate_kph == 0.4
    c.states["switch.plain"].state = "on"
    assert c._pipe_rate(target) == 0.5
    c.states["switch.plain"].state = "off"
    del c.areas["source"]
    assert c._pipe_rate(target) == 0
    assert c.pipe_sources(target) == [c.areas["plain"]]


def test_stats_source_only_overheating_window_and_legacy_store():
    c = _coordinator()
    a = c.areas["target"]
    a.check = {"minutes": 12, "sun_over_kh": 0.25}  # pre-pipe store
    validate(a.check, template(_new_check_stats()))
    c._count(a, 60, 21, 1000)
    assert a.check["pipe_on_min"] == 60
    assert a.check["pipe_over_kh"] == pytest.approx(0.3)
    assert a.check["over_kh"] == pytest.approx(0.3)  # the source supplied paid heat
    assert a.check["sun_over_kh"] == 0.25
    a.window_open = True
    c._count(a, 10, 21, 1600)
    assert a.check["pipe_on_min"] == 70
    assert a.check["pipe_over_kh"] == pytest.approx(0.3)
    c.states["switch.source"].state = "off"
    c._count(a, 10, 21, 2200)
    assert a.check["pipe_on_min"] == 70
    assert AreaLearner.from_dict({"model": {"n_cool": 10}}, 1800, 1800).model.n_cool == 10
    learner = AreaLearner()
    learner.add_sample(Sample(1000, 20, False, 5, 0, False, pipe_active=True))
    stored = learner.as_dict()
    validate(stored, learner_schema())
    restored = AreaLearner.from_dict(stored, 1800, 1800)
    assert restored._pipe_disturbed(2000)
    assert not restored._pipe_disturbed(2200)  # 20 minutes, even for pre-correction stores
    assert restored.as_dict() == stored
    # Pre-pipe stores preserve learned values and running events without migration.
    legacy = {
        "model": {"theta": [1.2, 0.02, 0.4], "n_heat": 48, "n_cool": 96},
        "dead_time": {"value": 900, "count": 5},
        "track_off": {"start": 100, "t_off": 20, "max": 20.3, "run_h": 1},
    }
    validate(legacy, learner_schema())
    restored = AreaLearner.from_dict(legacy, 1800, 1800)
    assert restored.model.theta == legacy["model"]["theta"]
    assert restored.model.n_heat == 48 and restored.model.n_cool == 96
    assert restored.dead_time.value == 900 and restored.dead_time.count == 5
    assert restored.track_off == legacy["track_off"]
    assert restored.pipe_last_on is None


async def test_check_and_nightly_payload_and_parameter_filtering():
    c = _coordinator()
    a = c.areas["target"]
    c._count(a, 30, 21, 1000)
    await c._run_check()
    payload = json.loads(c._ai_call.call_args.args[2])
    target, source, plain = payload["areas"]
    assert target["pipe"] == {
        "sources": ["a2"],
        "source_weights": {"a2": 1.0},
        "gain_kph": 0.2,
        "learned": False,
        "factor": 1,
        "confidence": 0,
    }
    assert target["stats"]["pipe_on_min"] == 30
    assert source["pipes_through"] == ["Target"]
    assert target["pipes_through"] == ["Source"]
    assert "pipe" not in plain and "pipe_factor" not in plain["params"]
    assert "pipe_on_min" not in plain["stats"]
    c._ai_call.return_value = {
        "adjustments": [
            {"area": "a1", "parameter": "pipe_factor", "value": 2, "reason": "pipes"},
            {"area": "a3", "parameter": "pipe_factor", "value": 2, "reason": "none"},
        ],
        "confidence": 80,
        "summary": "Pipes",
    }
    await c._run_check()
    assert a.params.pipe_factor == 1.2
    assert c.areas["plain"].params.pipe_factor == 1
    assert c.ai_state["last_rejected"]
    assert a.check["pipe_on_min"] == a.check["pipe_over_kh"] == 0
    assert c.ai_state["check_history"][-1]["areas"]["a1"]["pipe_on_min"] == 30
    c._ai_call.return_value = None
    await c._ask_nightly(12, 3, [], RuleResult(True, False, True, [], [], None, 12, 16))
    nightly = json.loads(c._ai_call.call_args.args[2])
    assert nightly["areas"][0]["pipe_sources"] == ["a2"]
    assert nightly["areas"][0]["pipe_gain_kph"] == 0.2
    assert nightly["areas"][0]["pipe_source_weights"] == {"a2": 1.0}
    assert "pipe_sources" not in nightly["areas"][2]


def _sub(key, circuit=True):
    return ConfigSubentry(
        subentry_id=key,
        subentry_type="room",
        title=key.title(),
        data={"heater_switch": f"switch.{key}"} if circuit else {},
        unique_id=None,
    )


def test_room_selector_and_cleanup_and_editable_gain():
    target, source, passive = _sub("target"), _sub("source"), _sub("passive", False)
    entry = SimpleNamespace(subentries={s.subentry_id: s for s in [target, source, passive]})
    others = other_areas(entry, "target")
    fields = _fields(area_schema({"pipe_sources": ["source", "deleted"]}, others=others))
    assert fields["pipe_sources"].config["options"] == [{"value": "source", "label": "Source"}]
    schema = area_schema({"pipe_sources": ["source", "deleted"]}, others=others)
    pipe = next(v for k, v in schema.schema.items() if str(k) == "pipe_heat")
    marker = next(k for k in pipe.schema.schema if str(k) == "pipe_sources")
    assert marker.default() == ["source"]
    data = area_data(
        "Target", {"pipe_sources": ["target", "source", "deleted"], "pipe_gain": 0.35}, others
    )
    assert data["pipe_sources"] == ["source"] and data["pipe_gain"] == 0.35
    assert fields["pipe_gain"](0) == 0 and fields["pipe_gain"](1) == 1
    for bad in [-0.1, 1.1]:
        with pytest.raises((vol.Invalid, PanelError)):
            area_data("Target", {"pipe_gain": bad}, others)


async def test_target_without_own_circuit_still_has_pipe_observations():
    c = _coordinator()
    passive = c._build_area("passive", "Passive", {"pipe_sources": ["source"]}, {}, 3)
    passive.temp = 21.5
    c.areas["passive"] = passive
    c._count(passive, 10, 21, 1000)
    await c._run_check()
    payload = json.loads(c._ai_call.call_args.args[2])
    target = payload["areas"][-1]
    assert target["pipe"]["sources"] == ["a2"]
    assert target["params"] == {"pipe_factor": 1.0}
    assert target["stats"]["pipe_on_min"] == 10


def test_virtual_day_without_heating_does_not_rely_on_sources():
    c = _coordinator()
    target = c.areas["target"]
    target.learner.model.n_cool = 100
    c._track_virtual(target, 60, 21)
    with_source = target.day.as_dict()
    target.day = type(target.day)()
    c.states["switch.source"].state = "off"
    c._track_virtual(target, 60, 21)
    assert target.day.as_dict() == with_source


def test_sun_overlap_is_visible_when_only_a_source_heats():
    c = _coordinator()
    c.pv_kw = 10
    a = c.areas["target"]
    c._count(a, 60, 21, 1000)
    assert not a.switch_on
    assert a.check["pipe_over_kh"] == pytest.approx(0.3)
    assert a.check["sun_over_kh"] == pytest.approx(0.3)
    assert a.check["over_kh"] == pytest.approx(0.3)


@pytest.mark.parametrize("weight", [0.1, 1.0, 3.0])
def test_panel_weights_bounds_and_legacy_clients(weight):
    others = [_sub("source"), _sub("storage", False), _sub("bedroom", False)]
    data = area_data(
        "Target",
        {
            "pipe_sources": ["source", "storage", "bedroom", "deleted"],
            "pipe_source_weights": {"source": weight, "storage": 2.0, "deleted": 3.0},
        },
        others,
    )
    assert data["pipe_sources"] == ["source"]
    assert data["pipe_source_weights"] == {"source": weight}
    # Partial updates from older clients retain existing valid weights and clean stale ones.
    data = area_data("Target", {"pipe_gain": 0.4}, others, current=data)
    assert data["pipe_source_weights"] == {"source": weight}
    data = area_data("Target", {"pipe_sources": []}, others, current=data)
    assert data["pipe_source_weights"] == {}
    legacy = area_data("Target", {"pipe_sources": ["source"]}, others)
    assert legacy["pipe_source_weights"] == {"source": 1.0}


@pytest.mark.parametrize(
    "weights",
    [
        {"source": 0},
        {"source": 3.1},
        {"source": 0.15},
        {"source": float("nan")},
        {"source": True},
        [1],
        "bad",
    ],
)
def test_panel_rejects_invalid_weights(weights):
    with pytest.raises(PanelError):
        area_data(
            "Target", {"pipe_sources": ["source"], "pipe_source_weights": weights}, [_sub("source")]
        )


async def test_live_topology_with_distinct_weights():
    c = PipeCoordinator()
    config = [
        ("living", "Wohnbereich", True),
        ("pia", "Pia", True),
        ("bad", "Bad", True),
        ("sam", "Sam", True),
        ("storage", "Abstellkammer", False),
        ("bedroom", "Schlafzimmer", False),
    ]
    for i, (key, name, circuit) in enumerate(config):
        c.areas[key] = c._build_area(
            key, name, {"heater_switch": f"switch.{key}"} if circuit else {}, {}, i
        )
        c.areas[key].temp = 21
        c.states[f"switch.{key}"] = SimpleNamespace(state="on")
    living = c.areas["living"]
    living.cfg.update(
        {
            "pipe_sources": ["pia", "bad", "sam", "storage", "bedroom", "living"],
            "pipe_source_weights": {"pia": 1, "bad": 2, "sam": 1.5, "storage": 3},
        }
    )
    assert [s.name for s in c.pipe_sources(living)] == ["Pia", "Bad", "Sam"]
    assert c._pipe_rate(living) == pytest.approx(0.15 * 4.5)
    await c._run_check()
    payload = json.loads(c._ai_call.call_args.args[2])
    target = payload["areas"][0]
    assert target["pipe"]["source_weights"] == {"a2": 1.0, "a3": 2.0, "a4": 1.5}
    assert all("pipe" not in a for a in payload["areas"][1:])
    assert all(a["pipes_through"] == ["Wohnbereich"] for a in payload["areas"][1:4])
    assert "Abstellkammer" not in str(target["pipe"])
