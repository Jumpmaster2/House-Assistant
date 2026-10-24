# Changelog

## Unreleased

### Added

- Core of the integration: the modules (heating, covers, meters) are chosen when setting up and under Settings > Modules. The options are kept per section (`core`, `meter`, ...) with the keys of the former integrations unchanged inside.
- Modules start, stop and restart on their own: changing the settings or the subentries of one module restarts only that module, the entry is not reloaded. A module switched off keeps its settings and its entity ids.
- Meter module (formerly Zähler-Ablesung 0.8.0) with every function: pictures with light and external light, rotation, crop, exposure and enhancement, majority vote, plausibility check, corrections, notifications, schedule with condition, second picture and history for the AI, rejected pictures. Services `house_assistant.read_meter` and `house_assistant.set_meter_reading`, event `house_assistant_meter_reading`, pictures below `media/house_assistant/<meter id>/`.
- One sidebar panel for the whole house with a section per module. The option to hide it from the sidebar is a setting of the house (Settings > Modules).
- Cover module (formerly Shutter Assistant 0.9.0) with every function: sun protection by direction with summer day and heat need, evening mode, follow-up closing, ventilation position, tilted windows and window handles, lockout protection, weather protection per window (wind, rain, frost) with own wind threshold, command spacing and position check, override detection, extra conditions, morning opening, vacation simulation, restart protection. Settings under Settings > Covers (the former options menu), groups and windows as subentries. Services `house_assistant.move_cover`, `start_cover_override`, `end_cover_override` and `resume_cover`; events `house_assistant_cover_moved`, `house_assistant_cover_failed` and `house_assistant_protection`.
- Dashboard cards `custom:house-assistant-cover-card`, `custom:house-assistant-tile` and `custom:house-assistant-window-tile` (formerly the card and tiles of Shutter Assistant), loaded on every dashboard and kept as one dashboard resource (`cards.js`).
- Heating module (formerly AI Heating Assistant 1.7.0) with every function: predictive control per room with dead time, overshoot and residual heat, sun forecast, minimum run times, frost protection, window delay, recovery, short airing and draft combinations, outage handling with repeated commands and repair issues, heating period, vacation with preheating, heating day by rule, AI and phase model with emergency rule, learning, AI review with limits and prompt blocks, budget and costs, heat meter, ventilation advice with humidity profile and AI ventilation check. Heating areas are now rooms (subentry `room`, ids unchanged). Settings under Settings > Heating (the former options menu), the API key in the setup and under Reconfigure. Services `house_assistant.export_parameters`, `import_parameters`, `reset_learned`, `run_ai_check`, `run_ai_ventilation_check` and `decide_heating_day` (names unchanged). Switching the heating module off, disabling or removing the integration switches the circuits off.
- Dashboard cards `custom:house-assistant-thermostat-card`, `custom:house-assistant-thermostat-compact-card` and `custom:house-assistant-climate-tile-card` (formerly the cards of AI Heating Assistant), in the same dashboard resource as the cover cards.
- One logbook event `house_assistant_logbook` for every module.

## 0.1.0

### Added

- Skeleton of the integration: one config entry for the whole house, translations (German and English), brand icons.
- Tooling: CI with ruff, the check of the generated panel texts, pytest, hassfest and HACS; `scripts/build_labels.py` and `scripts/check_privacy.py`.
- The plan of merging AI Heating Assistant, Shutter Assistant and Zähler-Ablesung in `docs/PLAN.md`.
