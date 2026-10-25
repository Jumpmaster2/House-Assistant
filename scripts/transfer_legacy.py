"""Transfer AI Heating Assistant, Shutter Assistant and Zähler-Ablesung to House Assistant.

One-off, on the configuration folder of Home Assistant (see docs/transfer.md):

    # 1. look first: writes transfer-plan.json and transfer-report.md, changes nothing
    python3 scripts/transfer_legacy.py --config /config --dry-run

    # 2. with Home Assistant stopped: backup, then the transfer
    python3 scripts/transfer_legacy.py --config /config --apply transfer-plan.json --stopped

Open points of the report (rooms of windows, differing settings) can be decided in
transfer-plan.json before step 2. Every file changed is copied to
``<config>/house_assistant_transfer_backup/<time>/`` first; the stores of the former
integrations stay as ``.bak``.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from legacy import convert as cv

# storage formats this transfer was checked with (Home Assistant 2026.10)
CHECKED = {
    "core.config_entries": (1, 5),
    "core.entity_registry": (1, 23),
    "core.device_registry": (3, 4),
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _save(path: Path, data: Any) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


class Config:
    """The configuration folder."""

    def __init__(self, root: Path, media: Path | None = None) -> None:
        self.root = root
        self.storage = root / ".storage"
        self.media = media or root / "media"
        if not (self.storage / "core.config_entries").is_file():
            raise cv.TransferError(f"{root} is no configuration folder of Home Assistant")

    def store(self, key: str) -> Path:
        return self.storage / key

    def load(self, key: str) -> dict[str, Any]:
        return _load(self.store(key))

    def check_formats(self, force: bool) -> list[str]:
        problems = []
        for key, expected in CHECKED.items():
            data = self.load(key)
            found = (data.get("version"), data.get("minor_version", 1))
            if found != expected:
                problems.append(f"{key}: format {found}, checked with {expected}")
        if problems and not force:
            raise cv.TransferError(
                "storage format not checked: " + "; ".join(problems) + " (--force to go on)"
            )
        return problems

    def dashboards(self) -> list[str]:
        return cv.iter_dashboards(p.name for p in self.storage.iterdir())

    def yaml_files(self) -> list[Path]:
        return [
            p for p in (self.root / "automations.yaml", self.root / "scripts.yaml") if p.is_file()
        ]


def _plan(config: Config) -> cv.Plan:
    return cv.build_plan(
        config.load("core.config_entries"),
        config.load("core.entity_registry"),
        config.load("core.device_registry"),
    )


def _report(config: Config, plan: cv.Plan, problems: list[str]) -> str:
    """What the transfer would do, as Markdown."""
    lines = ["# Transfer to House Assistant", ""]
    lines += [f"- {k}: {v}" for k, v in cv.summary(plan).items()]
    lines.append(f"- modules: {', '.join(plan.entry['options']['core']['modules'])}")
    shared = [k for k in plan.entry["options"]["core"] if k != "modules"]
    lines.append(f"- settings of the house: {', '.join(shared) or 'none'}")
    entities = cv.convert_entities(config.load("core.entity_registry"), plan)
    moved = [
        e for e in entities["data"]["entities"] if e.get("config_entry_id") == plan.new_entry_id
    ]
    lines.append(f"- entities moved (entity ids unchanged): {len(moved)}")
    lines += ["", "## Stores", ""]
    for old, new in plan.stores():
        state = "found" if config.store(old).is_file() else "MISSING"
        lines.append(f"- {old} -> {new} ({state})")
    lines += ["", "## Pictures of the meters", ""]
    for meter_id in plan.meter_ids():
        source = config.media / cv.METER / meter_id
        lines.append(
            f"- {source} -> {config.media / cv.DOMAIN / meter_id} "
            f"({'found' if source.is_dir() else 'none'})"
        )
    lines += ["", "## Dashboards", ""]
    for name in config.dashboards():
        _, count = cv.convert_dashboard(config.load(name))
        if count:
            lines.append(f"- {name}: {count} cards")
    if (config.store("lovelace_resources")).is_file():
        _, removed = cv.convert_resources(config.load("lovelace_resources"))
        lines += [f"- resource removed: {url}" for url in removed]
    lines += ["", "## Automations and scripts", ""]
    for path in config.yaml_files():
        _, replaced, left = cv.convert_yaml_text(path.read_text(encoding="utf-8"))
        lines += [f"- {path.name}: {r}" for r in replaced]
        lines += [f"- {path.name}, look at by hand: `{line}`" for line in left]
    lines += ["", "## Open points", ""]
    lines += [f"- {note}" for note in [*problems, *plan.notes]] or ["- none"]
    return "\n".join(lines) + "\n"


def dry_run(config: Config, out: Path, force: bool) -> cv.Plan:
    problems = config.check_formats(force)
    plan = _plan(config)
    cv.convert_devices(config.load("core.device_registry"), plan)  # raises on a conflict
    _save(out / "transfer-plan.json", plan.as_dict())
    (out / "transfer-report.md").write_text(_report(config, plan, problems), encoding="utf-8")
    return plan


def _backup(config: Config, plan: cv.Plan) -> Path:
    target = (
        config.root / "house_assistant_transfer_backup" / datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    (target / ".storage").mkdir(parents=True)
    keys = [*CHECKED, "lovelace_resources", *config.dashboards(), *(o for o, _ in plan.stores())]
    for key in keys:
        if config.store(key).is_file():
            shutil.copy2(config.store(key), target / ".storage" / key)
    for path in config.yaml_files():
        shutil.copy2(path, target / path.name)
    return target


def apply(config: Config, plan: cv.Plan, force: bool) -> list[str]:
    """Write the transfer. Home Assistant must be stopped (it keeps the registries in
    memory and would write them back)."""
    config.check_formats(force)
    done = [f"backup: {_backup(config, plan)}"]
    entries = config.load("core.config_entries")
    _save(config.store("core.config_entries"), cv.convert_config_entries(entries, plan))
    _save(
        config.store("core.entity_registry"),
        cv.convert_entities(config.load("core.entity_registry"), plan),
    )
    _save(
        config.store("core.device_registry"),
        cv.convert_devices(config.load("core.device_registry"), plan),
    )
    done.append(f"entry {plan.new_entry_id} replaces {', '.join(plan.old_entries)}")
    for old, new in plan.stores():
        if config.store(old).is_file():
            _save(config.store(new), cv.store_content(config.load(old), new))
            config.store(old).replace(config.store(old).with_name(old + ".bak"))
            done.append(f"store {old} -> {new}")
    for meter_id in plan.meter_ids():
        source = config.media / cv.METER / meter_id
        if source.is_dir():
            target = config.media / cv.DOMAIN / meter_id
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, target)
            done.append(f"pictures {source} -> {target}")
    for name in config.dashboards():
        dashboard, count = cv.convert_dashboard(config.load(name))
        if count:
            _save(config.store(name), dashboard)
            done.append(f"dashboard {name}: {count} cards")
    if config.store("lovelace_resources").is_file():
        resources, removed = cv.convert_resources(config.load("lovelace_resources"))
        if removed:
            _save(config.store("lovelace_resources"), resources)
            done += [f"resource removed: {url}" for url in removed]
    for path in config.yaml_files():
        text, replaced, _ = cv.convert_yaml_text(path.read_text(encoding="utf-8"))
        if replaced:
            path.write_text(text, encoding="utf-8")
            done.append(f"{path.name}: {len(replaced)} names")
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, required=True, help="configuration folder")
    parser.add_argument("--media", type=Path, help="media folder (default <config>/media)")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true", help="plan and report only")
    action.add_argument("--apply", type=Path, metavar="PLAN", help="transfer-plan.json")
    parser.add_argument("--out", type=Path, default=Path.cwd(), help="folder for plan and report")
    parser.add_argument("--stopped", action="store_true", help="Home Assistant is stopped")
    parser.add_argument("--force", action="store_true", help="also with another storage format")
    args = parser.parse_args(argv)
    try:
        config = Config(args.config, args.media)
        if args.dry_run:
            plan = dry_run(config, args.out, args.force)
            print(f"Plan and report in {args.out}: {cv.summary(plan)}")
            for note in plan.notes:
                print(f"  - {note}")
            return 0
        if not args.stopped:
            raise cv.TransferError("stop Home Assistant first, then add --stopped")
        for line in apply(config, cv.Plan.from_dict(_load(args.apply)), args.force):
            print(line)
        print("Done. Start Home Assistant and check (docs/transfer.md, step 5).")
        return 0
    except cv.TransferError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
