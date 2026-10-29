"""Storage validation and rollback without a running HA instance."""

from copy import deepcopy
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest

from custom_components.house_assistant.core.store import StoreRecovery
from custom_components.house_assistant.core.store_validation import dataclass_schema, validate
from custom_components.house_assistant.heating.logic.ai_policy import Budget
from custom_components.house_assistant.heating.logic.controller import AreaRuntime, ControlParams
from custom_components.house_assistant.heating.logic.energy import HeatMeter, Reading
from custom_components.house_assistant.heating.logic.humidity_learning import HumidityProfile
from custom_components.house_assistant.heating.logic.learning import (
    AreaLearner,
    RecoveryModel,
    ThermalModel,
)
from custom_components.house_assistant.heating.logic.room_energy import RoomEnergyModel
from custom_components.house_assistant.meter.meter import MeterState, meter_state_schema
from custom_components.house_assistant.runtime import HouseRuntime, Module


@pytest.mark.parametrize(
    "cls",
    [Budget, ControlParams, AreaRuntime, HeatMeter, HumidityProfile, ThermalModel, RecoveryModel],
)
def test_valid_dataclass_roundtrip(cls):
    value = cls()
    raw = value.as_dict()
    before = deepcopy(raw)
    validate(raw, dataclass_schema(cls))
    assert cls.from_dict(raw).as_dict() == before
    assert raw == before


def test_meter_roundtrip():
    now = datetime(2026, 10, 29, tzinfo=UTC)
    value = MeterState(
        value=102.345,
        value_time=now,
        rate=0.4,
        status="valid",
        last_check=now,
        readings=["102.345"],
        automatic=False,
        read_value=102.345,
        failures=3,
        streak=2,
        streak_status="error",
        history=[[now.isoformat(), 102.345]],
        vacation={
            "since": now.isoformat(),
            "time": now.isoformat(),
            "value": 100.1,
            "alerts": ["amount"],
        },
    )
    raw = value.as_dict()
    validate(raw, meter_state_schema())
    assert MeterState.from_dict(raw).as_dict() == raw


@pytest.mark.parametrize("field", list(meter_state_schema()))
@pytest.mark.parametrize("bad", ["bad", [], {}, float("nan"), float("inf")])
def test_meter_bad_fields_are_independent(field, bad):
    raw = MeterState(value=42.5).as_dict()
    raw[field] = bad
    try:
        validate(bad, meter_state_schema()[field])
    except (ValueError, TypeError):
        expected = MeterState().as_dict()[field]
        result = MeterState.from_dict(raw).as_dict()
        assert result[field] == expected
        if field != "value":
            assert result["value"] == 42.5


@pytest.mark.parametrize(
    "cls,field",
    [
        (Budget, "spent"),
        (ControlParams, "puffer"),
        (HeatMeter, "demand_kh"),
        (ThermalModel, "theta"),
    ],
)
@pytest.mark.parametrize("bad", ["12", float("nan"), float("inf"), []])
def test_invalid_numeric_record_defaults(cls, field, bad):
    raw = cls().as_dict()
    raw[field] = bad
    assert cls.from_dict(raw).as_dict() == cls().as_dict()


def test_heating_learned_roundtrip():
    learner = AreaLearner.create(2100, 2600)
    learner.model.n_heat = 40
    learner.dead_time.count = 20
    raw = learner.as_dict()
    validate(raw, dataclass_schema(AreaLearner))
    assert AreaLearner.from_dict(raw, 1800, 1800).as_dict() == raw
    energy = RoomEnergyModel()
    energy.set_areas({"living": 32.5, "bed": 18.0})
    energy.coefficients["living"] = 0.0031
    raw = energy.as_dict()
    assert RoomEnergyModel.from_dict(raw).as_dict() == raw
    meter = HeatMeter(last=Reading(321.123, 1790000000, 30.5))
    meter.baselines["day"] = Reading(300.12, 1789990000, 20.1)
    assert HeatMeter.from_dict(meter.as_dict()).as_dict() == meter.as_dict()


@pytest.mark.parametrize("raw", [None, [], {"x": "12"}, {"x": float("nan")}])
async def test_recovery_backup_and_issue(raw, tmp_path):
    from custom_components.house_assistant.core.store_validation import number

    async def executor(fn):
        return fn()

    hass = SimpleNamespace(async_add_executor_job=executor)
    entry = SimpleNamespace(entry_id="test")
    store = SimpleNamespace(path=str(tmp_path / "missing"), async_load=AsyncMock(return_value=raw))
    backup = SimpleNamespace(async_save=AsyncMock())
    recovery = StoreRecovery(hass, entry, "meter")
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
    ):
        data = await recovery.load(store)
        recovery.record("value", data, {"x": number})
        await recovery.finish()
        if raw is None:
            backup.async_save.assert_not_called()
            issue.assert_not_called()
            clear.assert_called_once()
        else:
            backup.async_save.assert_awaited_once()
            issue.assert_called_once()


@pytest.mark.parametrize("fail", ["house", "heating", "shutter", None])
@pytest.mark.parametrize("cleanup_error", [False, True])
async def test_start_rollback_and_retry(monkeypatch, fail, cleanup_error):
    from custom_components.house_assistant import runtime as rt

    events = []
    failing = fail

    class Fake(Module):
        async def async_setup(self):
            events.append(f"start:{self.key}")
            self.async_on_stop(lambda: events.append(f"unsub:{self.key}"))
            if self.key == failing:
                raise ValueError("original")

        async def async_unload(self):
            events.append(f"stop:{self.key}")
            if cleanup_error:
                raise RuntimeError("cleanup")

        def signature(self):
            return self.key

    types = {k: type(k, (Fake,), {"key": k}) for k in ("house", "heating", "shutter")}
    monkeypatch.setattr(rt, "HOUSE_TYPE", [types["house"]])
    monkeypatch.setattr(rt, "MODULE_TYPES", {k: types[k] for k in ("heating", "shutter")})
    monkeypatch.setattr(rt, "enabled_modules", lambda e: ["heating", "shutter"])
    runtime = HouseRuntime(Mock(), SimpleNamespace())
    if fail:
        with pytest.raises(ValueError, match="original"):
            await runtime.async_start()
        started = ["house", "heating", "shutter"][: ["house", "heating", "shutter"].index(fail) + 1]
        assert [e for e in events if e.startswith("stop:")] == [
            f"stop:{k}" for k in reversed(started)
        ]
        assert [e for e in events if e.startswith("unsub:")] == [
            f"unsub:{k}" for k in reversed(started)
        ]
        assert runtime.house is None and not runtime.modules
        failing = None
    await runtime.async_start()
    assert list(runtime.modules) == ["heating", "shutter"]
    await runtime.async_shutdown()
    assert runtime.house is None and not runtime.modules


async def test_remove_also_deletes_backup():
    from custom_components.house_assistant.core.store import remove_module_store

    store = SimpleNamespace(async_remove=AsyncMock())
    entry = SimpleNamespace(entry_id="test")
    with patch(
        "custom_components.house_assistant.core.store.module_store", return_value=store
    ) as factory:
        await remove_module_store(Mock(), entry, "house")
    assert [call.args[2] for call in factory.call_args_list] == ["house", "house.corrupt"]
    assert store.async_remove.await_count == 2


@pytest.mark.parametrize("error", [ValueError("bad JSON"), RuntimeError("load failed")])
async def test_load_error_and_malformed_file_preserved(error, tmp_path):
    path = tmp_path / "state"
    path.write_bytes(b'{"data":')

    async def executor(fn):
        return fn()

    recovery = StoreRecovery(
        SimpleNamespace(async_add_executor_job=executor), SimpleNamespace(entry_id="test"), "house"
    )
    assert (
        await recovery.load(SimpleNamespace(path=path, async_load=AsyncMock(side_effect=error)))
        == {}
    )
    assert bytes.fromhex(recovery.rejected["file_hex"]) == b'{"data":'
    assert recovery.rejected["load_error"] == str(error)


@pytest.mark.parametrize("module", ["house", "heating", "shutter", "meter"])
async def test_valid_records_never_saved_or_warned(module, caplog):
    recovery = StoreRecovery(Mock(), SimpleNamespace(entry_id="test"), module)
    raw = {"learned": 1.23456789012345, "legacy": -5.234, "nested": {"list": ["unchanged", 42.123]}}
    original = deepcopy(raw)
    backup = SimpleNamespace(async_save=AsyncMock())
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
    ):
        assert recovery.record("record", raw, {}) is raw
        await recovery.finish()
        await recovery.finish()
        assert raw == original
        assert recovery.rejected == {}
        backup.async_save.assert_not_called()
        issue.assert_not_called()
        assert clear.call_count == 2
    assert not caplog.records


async def test_meter_timeout_releases_busy(monkeypatch):
    import asyncio
    from contextlib import asynccontextmanager

    from custom_components.house_assistant.meter import meter as mm
    from custom_components.house_assistant.meter.const import meter_defaults

    async def blocked(*args, **kwargs):
        await asyncio.Event().wait()

    manager = SimpleNamespace(
        hass=SimpleNamespace(services=SimpleNamespace(async_call=blocked)),
        options={"ai_task_entity": "ai_task.test"},
        language="en",
    )
    meter = mm.Meter(manager, "test", "Water", meter_defaults("water"))

    @asynccontextmanager
    async def session():
        yield

    async def read():
        return await meter._ask_ai()

    monkeypatch.setattr(mm, "AI_TIMEOUT", 0.001)
    monkeypatch.setattr(meter, "_external_light", session)
    monkeypatch.setattr(meter, "_session", session)
    monkeypatch.setattr(meter, "_read", read)
    monkeypatch.setattr(meter, "notify", Mock())
    assert await meter.async_read() == mm.rd.ERROR
    assert meter.busy is None
    assert not meter._lock.locked()


@pytest.mark.parametrize("bad", [[], {"x": "broken"}, {"x": float("nan")}])
def test_bad_sibling_does_not_discard_healthy_record(bad):
    from custom_components.house_assistant.core.store_validation import number

    recovery = StoreRecovery(Mock(), SimpleNamespace(entry_id="test"), "heating")
    healthy = {"x": 12.12345678}
    records = recovery.mapping("areas", {"healthy": healthy, "bad": bad})
    restored = {k: recovery.record(k, raw, {"x": number}) for k, raw in records.items()}
    assert restored["healthy"] is healthy
    assert restored["bad"] == {}
    assert recovery.rejected.keys() == {"bad"}


async def _executor(fn, *args):
    return fn(*args)


@pytest.mark.parametrize("corrupt", [False, True])
async def test_vacation_storage_roundtrip(corrupt, tmp_path, caplog):
    from custom_components.house_assistant.core.vacation import HouseModule

    raw = {
        "on": True,
        "active": True,
        "source": "switch",
        "departure": "2026-10-29T12:00:00+00:00",
        "return": "2026-11-03T12:00:00+00:00",
        "since": "2026-10-29T12:00:00+00:00",
    }
    if corrupt:
        raw["return"] = []
    original = deepcopy(raw)
    house = SimpleNamespace(
        hass=SimpleNamespace(async_add_executor_job=_executor),
        entry=SimpleNamespace(entry_id="test"),
        _store=SimpleNamespace(path=tmp_path / "absent", async_load=AsyncMock(return_value=raw)),
        sources=lambda: [],
        return_entity=None,
        _windows=lambda: {},
        _window_state=Mock(),
        async_on_stop=Mock(),
        _on_state=Mock(),
        _write=Mock(),
        _cancel=Mock(),
        _on_started=Mock(),
    )
    backup = SimpleNamespace(async_save=AsyncMock())
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
        patch(
            "custom_components.house_assistant.core.vacation.async_dispatcher_connect",
            return_value=Mock(),
        ),
        patch(
            "custom_components.house_assistant.core.vacation.async_at_started", return_value=Mock()
        ),
    ):
        await HouseModule.async_setup(house)
        if corrupt:
            assert not house.times.on
            backup.async_save.assert_awaited_once()
            assert backup.async_save.call_args.args[0]["data"]["vacation"] == original
            issue.assert_called_once()
        else:
            assert HouseModule._data(house) == original
            backup.async_save.assert_not_called()
            issue.assert_not_called()
            clear.assert_called_once()
            assert not caplog.records


@pytest.mark.parametrize("corrupt", [False, True])
async def test_shutter_storage_roundtrip(corrupt, tmp_path, caplog):
    from custom_components.house_assistant.shutter.engine import ShutterEngine

    # Stop just after restore: the rest of setup reads devices and schedules HA timers.
    class Restored(Exception):
        pass

    def window():
        return SimpleNamespace(
            override_until=None,
            override_since=None,
            override_sunrise=False,
            override_active=False,
            sun_day=None,
            notified_day=None,
            evening_day=None,
            morning_day=None,
            last_manual=None,
            last_reason={},
            automatic=False,
            sun_enabled=True,
            protection=None,
            wind_guard=None,
            trigger=SimpleNamespace(locked_until=None, pending=False),
        )

    obj = SimpleNamespace(
        automatic=False,
        forecast_day=None,
        forecast_max=28.123456789,
        forecast_night_low=17.5,
        raised_day=None,
        vacation_evening_day=None,
        guards={},
        windows={"healthy": window(), "bad": window()},
    )
    raw = ShutterEngine._data_to_save(obj)
    if corrupt:
        raw["windows"]["bad"] = {"wind_guard": []}
    original = deepcopy(raw)
    obj.hass = SimpleNamespace(async_add_executor_job=_executor)
    obj.config_entry = SimpleNamespace(entry_id="test")
    obj._store = SimpleNamespace(path=tmp_path / "absent", async_load=AsyncMock(return_value=raw))

    def restore(data):
        ShutterEngine._restore(obj, data)
        raise Restored

    obj._restore = restore
    backup = SimpleNamespace(async_save=AsyncMock())
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
    ):
        with pytest.raises(Restored):
            await ShutterEngine.async_setup(obj)
        result = ShutterEngine._data_to_save(obj)
        assert result["windows"]["healthy"] == original["windows"]["healthy"]
        if corrupt:
            backup.async_save.assert_awaited_once()
            issue.assert_called_once()
        else:
            assert result == original
            backup.async_save.assert_not_called()
            issue.assert_not_called()
            clear.assert_called_once()
            assert not caplog.records


@pytest.mark.parametrize("corrupt", [False, True])
async def test_heating_six_rooms_storage_roundtrip(corrupt, tmp_path, caplog):
    from custom_components.house_assistant.const import SUBENTRY_ROOM
    from custom_components.house_assistant.heating.coordinator import HeatingCoordinator
    from custom_components.house_assistant.heating.logic.heating_day import DayAreaStats
    from custom_components.house_assistant.heating.logic.sun import SunScale
    from custom_components.house_assistant.heating.logic.ventilation import VentilationSettings

    class Restored(Exception):
        pass

    areas = {}
    subentries = {}
    for i in range(6):
        key = f"room{i}"
        areas[key] = SimpleNamespace(
            area_id=key,
            target=21.1234567 + i,
            hvac_on=True,
            params=ControlParams(puffer=0.812345),
            learner=AreaLearner.create(2100, 2300),
            runtime=AreaRuntime(carry_peak=22.5, carry_since=1793275200.5),
            day=DayAreaStats(),
            check={},
            start={},
            vent_params=VentilationSettings(),
            vent_check={},
            vent_start={},
            humidity_profile=HumidityProfile(),
            has_circuit=False,
        )
        subentries[key] = SimpleNamespace(
            subentry_id=key,
            title=key,
            subentry_type=SUBENTRY_ROOM,
            data={"temperature_sensor": f"sensor.{key}"},
        )
    obj = SimpleNamespace(
        areas=areas,
        day_state={},
        ai_state={},
        budget=Budget(),
        meter=HeatMeter(),
        room_energy=RoomEnergyModel(),
        sun_scale=SunScale(0.9123456),
        _pending_release=[],
    )
    raw = HeatingCoordinator._data_to_save(obj)
    if corrupt:
        raw["areas"]["room5"]["params"]["puffer"] = float("nan")
    original = deepcopy(raw)
    obj.areas = {}
    obj.hass = SimpleNamespace(async_add_executor_job=_executor)
    obj.config_entry = SimpleNamespace(entry_id="test", subentries=subentries)
    obj.store = SimpleNamespace(path=tmp_path / "absent", async_load=AsyncMock(return_value=raw))
    captured = {}

    def build(area_id, title, cfg, stored, index):
        captured[area_id] = stored
        return areas[area_id]

    obj._build_area = build
    obj._plan_windows = Mock(side_effect=Restored)
    backup = SimpleNamespace(async_save=AsyncMock())
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
    ):
        with pytest.raises(Restored):
            await HeatingCoordinator._async_setup(obj)
        for i in range(5):
            assert captured[f"room{i}"] == original["areas"][f"room{i}"]
        if corrupt:
            assert captured["room5"] == {}
            backup.async_save.assert_awaited_once()
            issue.assert_called_once()
        else:
            assert captured == original["areas"]
            assert obj.meter.as_dict() == original["meter"]
            assert obj.room_energy.as_dict() == original["room_energy"]
            backup.async_save.assert_not_called()
            issue.assert_not_called()
            clear.assert_called_once()
            assert not caplog.records


@pytest.mark.parametrize("corrupt", [False, True])
async def test_meter_manager_storage_roundtrip(corrupt, tmp_path, caplog):
    from custom_components.house_assistant.meter import meter as mm
    from custom_components.house_assistant.meter.meter import MeterManager

    raw = {
        "meters": {
            key: MeterState(value=100.123456789, rate=0.1234567, automatic=False).as_dict()
            for key in ("healthy", "bad")
        }
    }
    if corrupt:
        raw["meters"]["bad"]["failures"] = "broken"
    original = deepcopy(raw)
    manager = SimpleNamespace(
        hass=SimpleNamespace(async_add_executor_job=_executor),
        entry=SimpleNamespace(entry_id="test"),
        _store=SimpleNamespace(path=tmp_path / "absent", async_load=AsyncMock(return_value=raw)),
        meters={key: SimpleNamespace(id=key, load_image=Mock()) for key in ("healthy", "bad")},
        module=SimpleNamespace(async_on_stop=Mock(), runtime=Mock()),
        _async_tick=Mock(),
        _sync_vacation=Mock(),
        _heating_changed=Mock(),
    )
    backup = SimpleNamespace(async_save=AsyncMock())
    with (
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch("homeassistant.helpers.issue_registry.async_create_issue") as issue,
        patch("homeassistant.helpers.issue_registry.async_delete_issue") as clear,
        patch.object(mm, "async_track_time_interval", return_value=Mock()),
        patch.object(mm, "async_dispatcher_connect", return_value=Mock()),
        patch.object(mm, "rooms_on_at_setup", return_value=None),
    ):
        await MeterManager.async_setup(manager)
        assert manager.meters["healthy"].state.as_dict() == original["meters"]["healthy"]
        if corrupt:
            assert manager.meters["bad"].state.failures == 0
            backup.async_save.assert_awaited_once()
            issue.assert_called_once()
        else:
            assert MeterManager._data(manager) == original
            backup.async_save.assert_not_called()
            issue.assert_not_called()
            clear.assert_called_once()
            assert not caplog.records


async def test_tasks_and_remaining_unsubs_stop_after_cleanup_error():
    import asyncio

    task_cancelled = asyncio.Event()

    async def background():
        try:
            await asyncio.Event().wait()
        finally:
            task_cancelled.set()

    task = asyncio.create_task(background())
    await asyncio.sleep(0)
    module = Module(SimpleNamespace(hass=Mock(), entry=Mock()))
    module.key = "test"
    module._tasks.add(task)
    remaining = Mock()
    module.async_on_stop(remaining)
    module.async_on_stop(Mock(side_effect=RuntimeError("unsubscribe failed")))
    await module.async_stop()
    assert task_cancelled.is_set()
    assert task.cancelled()
    remaining.assert_called_once()
    assert not module._unsubs


async def test_recovery_does_not_overwrite_raw_if_backup_fails(tmp_path):
    from homeassistant.helpers.storage import Store

    from custom_components.house_assistant.core.store import ModuleStore

    store = object.__new__(ModuleStore)
    store.async_load = AsyncMock(return_value=[])
    recovery = StoreRecovery(
        SimpleNamespace(async_add_executor_job=_executor), SimpleNamespace(entry_id="test"), "house"
    )
    backup = SimpleNamespace(async_save=AsyncMock(side_effect=OSError("disk full")))
    with (
        patch.object(ModuleStore, "path", property(lambda _: str(tmp_path / "missing"))),
        patch("custom_components.house_assistant.core.store.module_store", return_value=backup),
        patch.object(Store, "async_save", new_callable=AsyncMock) as normal_save,
    ):
        await recovery.load(store)
        with pytest.raises(OSError, match="disk full"):
            await recovery.finish()
        await store.async_save({"on": False})
        normal_save.assert_not_called()


def test_truncated_learned_structures_default():
    from custom_components.house_assistant.heating.logic.humidity_learning import humidity_schema
    from custom_components.house_assistant.heating.logic.learning import learner_schema

    for raw, schema in [
        ({"p": [[1.0]]}, dataclass_schema(ThermalModel)),
        ({"hour": [1.0]}, humidity_schema()),
        ({"floor": [["2026-10-29"]]}, humidity_schema()),
        ({"track_on": {"start": 123.0}}, learner_schema()),
    ]:
        with pytest.raises(ValueError):
            validate(raw, schema)


async def test_failed_started_hook_is_removed(monkeypatch):
    from custom_components.house_assistant import runtime as rt

    stopped = Mock()

    class Failed(Module):
        key = "shutter"

        def signature(self):
            return "test"

        def started(self):
            self.async_on_stop(stopped)
            raise ValueError("started failed")

    monkeypatch.setattr(rt, "MODULE_TYPES", {"shutter": Failed})
    runtime = HouseRuntime(Mock(), Mock())
    with pytest.raises(ValueError, match="started failed"):
        await runtime._start("shutter")
    assert not runtime.modules
    assert not runtime._signatures
    stopped.assert_called_once()
