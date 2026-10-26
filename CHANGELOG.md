# Changelog

## 1.0.0b10 (2026-10-26)

### Added

- Brief airing appears in the logbook: "Aired briefly: waiting until ..." when a window was open for at least the minimum and shorter than the window delay, and "Wait after brief airing finished." when the wait is over. Airings that are too short or a wait of 0 are not logged.
- Two settings per room in the new section *Airing* of the room (dialog and panel), changeable at any time also for existing rooms: *Brief airing from* (default 1 minute, 0 to 60, step 0.5; 0 = every airing counts) and *Wait after brief airing* (default 50 %, 0 to 100, step 5; 0 = no wait). They are not start values and the AI does not adjust them; rooms without them get the defaults.

### Changed

- After brief airing the heating waits a fixed time: the learned recovery time times *Wait after brief airing*. Before, the wait was scaled by how long the window was open, and it ended early as soon as the temperature from before the airing was back. Now it ends only when the time has passed. The normal recovery after a pause (window open for at least the window delay) is unchanged.
- The learning of the recovery time is not affected by the fixed wait: the room is still measured until it is back at its temperature.

## 1.0.0b9 (2026-10-25)

### Changed

- The vacation is set only in the house (Settings > House > Vacation, or the tab *Vacation* of the panel). The heating and the covers no longer offer their own *Vacation entities* and the heating no longer its own *Return date/time*: the external sources and the external return count for every module, as set in the house. Values a module still held from before move to the house when Home Assistant starts (the house's own value wins for the return) and leave the module.
- The options *Ventilation advice rests* and *Heat protection on vacation* are no longer asked a second time in the dialogs of the heating and the covers. They are set with the rest of the vacation in the house (the dialog and the panel tab, which now show their texts).
- The vacation temperature and the preheat reserve stay with the heating, the simulation times and positions with the covers, the leak warning with each meter.
- The overview of the heating shows the vacation temperature instead of the vacation entities.
- A change of the external return entity makes the heating look again at once.

## 1.0.0b8 (2026-10-25)

### Fixed

- A restart of Home Assistant (or a reload of the heating) asked for an extra reading of the heat meter: the first state of the heating after the start counted as a start or end of a heating phase. The state the heating has at the start is now the starting point, only a real change of a room's circuit asks for a reading.

## 1.0.0b7 (2026-10-25)

### Fixed

- After a start of Home Assistant the sensor *Next reading* of the heat meter still showed the old interval: the heating is reachable for the meters only once the integration is loaded. The meters now update the sensor within 5 minutes when the interval changes.

## 1.0.0b6 (2026-10-25)

### Fixed

- The sensor *Next reading* of the heat meter showed the interval from before the start of the heating module (e.g. 30 minutes) instead of the one in effect (15 minutes while a room heats, once a day otherwise). It now follows every change of the heating.

## 1.0.0b5 (2026-10-25)

### Added

- Heat per room: with a floor area per room (field *Floor area*, 1 to 200 m²), every reading of the heat meter is split over the rooms that heated in the phase since the last reading. The split is learned from run time, floor area and heating demand (target minus outdoor temperature); the shares always add up to the reading, what no room heated is *Not assigned*. New sensors per room (*Heat consumption*, *Heat consumption today*, *Estimated heat output*) and for the house (*Not assigned*); the heating panel shows a table per room.
- Heat meter read more often while a room heats: every 15 minutes, otherwise once a day (meter options *Interval while a room heats* and *Interval otherwise*). Switching the heating on and off (the first circuit on, the last one off) asks for a reading, at least 5 minutes after the last one; after the end the short interval lasts 30 more minutes for the last heat of the phase.

### Changed

- Heat meters and meters with the condition *Heating day* use the readings above instead of the intervals *Interval* and *Interval while the condition is off*. Without the heating module the old intervals apply.
- The house panel shows the floor area of the rooms.

### Fixed

- Rooms added or changed in the settings dialog of the heating (a room of the integration) lost their Home Assistant area: it was not saved when the room was added, and every change of the room cleared it. The house panel was not affected.

## 1.0.0b4 (2026-10-25)

### Changed

- Thermostat cards: a tap on the temperature or on the humidity opens the history of the room's sensor (like the room climate tile), the name and the status line still open the thermostat. In the dial card the values below the big number open their sensor.
- The thermostats carry the sensors of their room as attributes `temperature_sensor` and `humidity_sensor` (not recorded).

## 1.0.0b3 (2026-10-25)

### Changed

- Settings the house sets for every module (outdoor values, weather, language, notifications, working days, size of the house, vacation) are no longer offered a second time by the heating and the covers: their panels show them as a note "From the house", their settings dialogs leave them out. Without a value in the house the field of the module stays.
- The panels of the heating and the covers show the values in effect (the house wins) in their overview, hints and live values.
- Transfer: settings that go to the house are no longer kept as a copy in the modules. The heating day sensor of AI Heating Assistant used by the covers (heat need) or by a meter (condition) becomes the link to the heating module. The room entity of a cover window is dropped when it is the thermostat or the temperature sensor of the window's room, which the room provides anyway.

## 1.0.0b2 (2026-10-25)

### Fixed

- Dashboard cards showed "Configuration error" after reloading a view with a media control card (also in the Companion app). The frontend loads its polyfill for scoped custom element registries on demand and then replaces `window.customElements`; cards defined before were unknown to the new registry. The cards and the panel now define their elements again as soon as the registry is replaced.

## 1.0.0b1 (2026-10-25)

First release: AI Heating Assistant 1.7.0, Shutter Assistant 0.9.0 and Zähler-Ablesung 0.8.0 in one integration on one model of the house, with every function of the three.

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
- The house: rooms and windows are entered once and used by every module (panel section House, subentries `room` and `window` independent of the modules). A window has a room, a size (small, medium, large, door), its contacts and optionally a cover; a contact and a cover belong to one window only. A room has an optional Home Assistant area (its device is placed there) and an optional temperature sensor.
- The heating takes the contacts of the windows of a room (the size of the window gives the opening area); rooms without a temperature sensor get no heating entities. The contact fields of a room are gone.
- Covers take the room of their window: without an own room entity the temperature sensor of the room and the target of its thermostat, and the air conditioner of the room (section Sun protection of the room). A window without a cover only serves the heating.
- Covers use the heating day of the heating module as heat need when no own entity is set (option "Heating day of the heating", on by default; only within the heating period).
- Meters can use the days without heating as their condition (option per meter).
- The heating reads a heat meter of the meter module with the time it was read; a confirmed correction downwards is no meter reset.
- Settings of the house for every module (setup step and Settings > House, panel House > General): outdoor temperature and humidity, weather, language of the messages, notification services, workday sensor and weekend days. A value set there applies to every module; without one the value in the settings of the module applies. The setup asks for them once, before the modules; the covers start with the summer day. Logbook and notifications of heating and meters follow the language of the house as well.
- Cross ventilation and draft from the arrangement of the windows: the heating no longer needs combinations entered by hand. A room ventilates across when an own window is open together with a window of another room on the same floor on the opposite or an adjacent wall. A draft passes through a room without an open own window when two windows of other rooms on the same floor (opposite or adjacent walls) are open and the room lies within the draft reach (default 2 m) of the line between them. The floor comes from the Home Assistant area of the room; without floors in Home Assistant every room is on one floor. Without the size of the house only cross ventilation applies.
- Each combination can be switched off per room (panel House > Rooms, the plan of the house with its lines). The thermostat attribute `draft_windows` names the windows that set it off.
- Tilted windows: a window handle reporting `tilted` or a tilt contact of the window counts for the heating as open with 25 % of the opening area. Unknown still counts as closed.
- The plan of the house (orientation, width, depth and the draft reach) is a setting of the house (House > General); the house card of the cover section is gone.
- Vacation of the house for every module: a switch “Vacation” with departure and return on the device House Assistant (kept across restarts), a binary sensor “Vacation active” (source, since, departure, return, start of preheating, presence simulation, leak warning, windows not closed) and the service `house_assistant.set_vacation` (departure, return, clear). At the departure the vacation switches on, at the return off; with only a return it applies from now on; a departure after the return is refused, a return in the past is ignored. Event `house_assistant_vacation` (active, source) and a logbook entry at start and end.
- External sources still count: vacation entities and a return entity of the house (Settings > Vacation, panel House > Vacation); without them the ones in the settings of heating and covers. The heating preheats for the own return first.
- Covers: heat protection on vacation, the sun protection lowers without waiting for room temperature, air conditioner or heat need (summer day, sun sensors and hold times still apply; option, on by default).
- Heating: the ventilation advice rests on vacation (state “vacation”, ventilation recommended off, no minutes for the AI ventilation check, no samples for the humidity profile; option, on by default).
- Open windows: at the start of the vacation a message lists every window not closed (open, tilted, unknown); on vacation a window opened or tilted is reported once it stayed so for 10 s. To the notification services of the house, without any as a notification in Home Assistant (option, on by default).
- Meters warn on vacation (leak warning per meter): amount used since the start and mean flow or power, counted from the last valid reading before the vacation; once per vacation and case with a message, a logbook entry, the event `house_assistant_vacation_alert` and the attribute `vacation_alerts`. On by default for water meters (20 L, 5 L/h), off for gas and electricity, never for the heat meter.
- The panel shows a banner while it is vacation.
- Transfer of an existing installation (`scripts/transfer_legacy.py`, see `docs/transfer.md`): with Home Assistant stopped it turns the entries of the three former integrations into one House Assistant entry with the same entity ids, devices and learned data. Rooms from the heating areas, windows of the covers merged with the heating contacts they share, the other contacts as windows without a cover, stores, pictures of the meters, card types of the dashboards, dashboard resources, service and event names in automations and scripts. A dry run writes a plan and a report first; every file changed is backed up.
- Documentation: README in German and English, one page per module (`docs/heating.md`, `docs/covers.md`, `docs/meters.md`, each also in English), the transfer (`docs/transfer.md`) and the ESPHome example of the meter camera.

### Fixed (compared to the former integrations)

- Dashboard cards sometimes showed “configuration error” (often in the companion app, sometimes in the browser after a reload): a dashboard that opened while Home Assistant was starting asked for the cards before they were served, and the browser kept that failed load until the page was reloaded. The cards are now served and added to the frontend when the integration is set up, before its modules start; the dashboard resource has an address of its own (`cards-resource.js`), so one failed early load does not block the other; all files lie below a folder with the version (cached, never mixed after an update); the cover card loads only its own texts (1 KB instead of the 330 KB of the panel).

## 0.1.0

### Added

- Skeleton of the integration: one config entry for the whole house, translations (German and English), brand icons.
- Tooling: CI with ruff, the check of the generated panel texts, pytest, hassfest and HACS; `scripts/build_labels.py` and `scripts/check_privacy.py`.
- The plan of merging AI Heating Assistant, Shutter Assistant and Zähler-Ablesung in `docs/PLAN.md`.
