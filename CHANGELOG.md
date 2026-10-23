# Changelog

## Unreleased

### Added

- Core of the integration: the modules (for now the meters) are chosen when setting up and under Settings > Modules. The options are kept per section (`core`, `meter`, ...) with the keys of the former integrations unchanged inside.
- Modules start, stop and restart on their own: changing the settings or the subentries of one module restarts only that module, the entry is not reloaded. A module switched off keeps its settings and its entity ids.
- Meter module (formerly Zähler-Ablesung 0.8.0) with every function: pictures with light and external light, rotation, crop, exposure and enhancement, majority vote, plausibility check, corrections, notifications, schedule with condition, second picture and history for the AI, rejected pictures. Services `house_assistant.read_meter` and `house_assistant.set_meter_reading`, event `house_assistant_meter_reading`, pictures below `media/house_assistant/<meter id>/`.
- One sidebar panel for the whole house; the meters are its first section.

## 0.1.0

### Added

- Skeleton of the integration: one config entry for the whole house, translations (German and English), brand icons.
- Tooling: CI with ruff, the check of the generated panel texts, pytest, hassfest and HACS; `scripts/build_labels.py` and `scripts/check_privacy.py`.
- The plan of merging AI Heating Assistant, Shutter Assistant and Zähler-Ablesung in `docs/PLAN.md`.
