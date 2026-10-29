# House Assistant

[Deutsche Version](README.md)

Custom integration for Home Assistant that brings heating, covers and meter reading together on one model of the house. Rooms and windows are entered only once; the modules build on them and work together:

* **Heating** (formerly [AI Heating Assistant](https://github.com/Jumpmaster2/AI-Heating-Assistant)): local, learning control per room, heating day decision and parameter review by Claude, ventilation advice with a learned humidity profile. Details: [docs/heating.en.md](docs/heating.en.md)
* **Covers** (formerly [Shutter Assistant](https://github.com/Jumpmaster2/Shutter-Assistant)): sun protection by direction, evening mode, ventilation position, weather protection, override, morning opening, vacation simulation. Details: [docs/covers.en.md](docs/covers.en.md)
* **Meters** (formerly [Zähler-Ablesung](https://github.com/Jumpmaster2/Zaehler-Ablesung)): read meters with a camera and an AI, with a majority vote and a plausibility check. Details: [docs/meters.en.md](docs/meters.en.md)

Every module can be switched on and off on its own. No function of the former integrations is dropped; their users move with a script, without losing history or learned values ([docs/transfer.md](docs/transfer.md#english)).

> Status: version 1.0.0b1 (beta). Please keep an eye on the logbook during the first weeks.

## Working together

* **One house:** rooms (with Home Assistant area and sensors) and windows (with room, size, contacts, wall and optionally a cover) exist only once. A contact and a cover belong to one window only.
* **Automatic cross ventilation:** from the arrangement of the windows on the house the heating detects cross ventilation and draft through rooms, also round the corner; every combination can be switched off on its own.
* **Brief airing:** a window open for at least one minute but shorter than the window delay counts as brief airing; afterwards the heating waits half the learned recovery time (both configurable per room at any time in the section *Airing*). The logbook shows it. Details: [docs/heating.en.md](docs/heating.en.md)
* **Tilted:** window handles and tilt contacts count for the heating with 25 % of the opening area, for the covers as before.
* **Heating day:** the heating day of the heating is the heat need of the covers (warmth of the sun welcome) and the condition of the meters (read less often when not heating).
* **Room values:** the covers take temperature, thermostat target and air conditioner of the room of their window.
* **Heat meter:** the heating reads a meter of the meters module with the real time of the reading; a confirmed correction is no meter change. With a floor area per room it splits the consumption over the rooms (see docs/heating.en.md).
* **Vacation for the whole house** (see below).
* **Settings of the house:** outdoor values, weather, language, notifications and working days apply to every module.
* **One panel** with sections for house, heating, covers and meters.
* **No reload:** a change restarts only the module concerned; hold times of the covers and a running meter reading stay untouched.

## Installation

### With HACS

1. Open HACS and choose **Custom repositories** in the menu at the top right.
2. Add the repository `https://github.com/Jumpmaster2/House-Assistant` with type **Integration**.
3. Download **House Assistant** and restart Home Assistant.
4. **Settings > Devices & services > Add integration > House Assistant**.

### Manually

1. Copy the folder `custom_components/house_assistant` to `config/custom_components/` of Home Assistant.
2. Restart Home Assistant and add the integration as in step 4 above.

Requires Home Assistant 2026.10 or newer. Optionally an API key of Anthropic for the AI of the heating (without a key the local control runs), an AI task with image support for the meters.

Users of the former integrations: install House Assistant but **do not set it up**, and follow the [transfer](docs/transfer.md#english).

## Setup

1. **Choose the modules:** heating, covers, meters (changeable later under *Configure > Modules*).
2. **House:** outdoor temperature (a sensor or a weather entity, needed for heating and covers), outdoor humidity, weather, language, notification services, workday, weekend days, orientation and size of the house, draft reach.
3. **Per module** the first settings; with the heating it goes on directly with the first room.
4. In the panel **House Assistant** (sidebar) add rooms and windows under **House**, then the settings in the sections of the modules.

**Configure** at the integration opens the panel. The options menu has modules, house, vacation and per module its settings; rooms, windows, directions and meters can also be added as entries of the integration.

## The house

In the panel under **House**:

* **Rooms:** name, Home Assistant area (the device of the room goes there; it gives the floor), temperature and humidity sensor, air conditioner. With a temperature sensor a room gets heating and ventilation advice, with a heating circuit also a thermostat (section heating). The room editor shows the plan of the house with the cross ventilation and draft combinations of the room, each with its own switch.
* **Windows:** name, room, size (small, medium, large, door), window contacts (also window handles), tilt contacts, direction, wall and position on the wall, cover. At least a contact or a cover. With a cover the other settings are in the section covers.
* **Vacation:** switch, departure and return, sources and reports (see below).
* **General:** the settings of the house, the modules and whether the panel is in the sidebar.

### Settings of the house

| Option | Meaning |
|---|---|
| Outdoor temperature, outdoor humidity, weather | for heating and covers; without an outdoor sensor the current temperature of the weather entity applies |
| Wind sensor | shared sensor for wind protection; wind thresholds remain in covers |
| Language of messages | logbook, last reason, notifications of every module; automatic = the language of Home Assistant |
| Notification services | `notify.*` only; messages of the covers and of the vacation |
| Workday sensor, weekend days | morning opening of the covers |
| Front faces, length, depth | the house in the sun compass of the covers; with length and depth the heating detects draft through rooms |
| Draft reach | how far a room may be from the line between two open windows of other rooms (default 2 m) |

Shared settings and room basics are edited only in House. Legacy module values migrate to House at startup: house values take precedence; otherwise heating wins over covers on conflicts. Vacation sources are combined. Empty house values then remain unset.

## Vacation

One vacation for every module, without own helpers:

* **Switch Vacation** on the device "House Assistant", kept across restarts. **Departure** and **return** (`datetime` entities, both optional): at the departure the vacation switches on, at the return off, then both are empty again. With only a return set, the vacation applies from now on. A departure after the return is refused, a return in the past ignored. Also in the panel under *House > Vacation* and with the service `house_assistant.set_vacation`.
* **External sources** still count: vacation entities (`input_boolean`, `binary_sensor`, `switch`, `calendar`, `schedule`; on = vacation) and a return entity. They are set only in the house (Settings > House > Vacation or in the panel); heating and covers have no sources of their own any more, and the options *Ventilation advice rests* and *Heat protection on vacation* are set there as well.
* **Binary sensor Vacation active** with source, start, departure, return, start of preheating, presence simulation, leak warning and windows not closed. Event `house_assistant_vacation` (`active`, `source`) and a logbook entry at start and end. The panel shows a banner during the vacation.

Effect:

| Module | on vacation |
|---|---|
| Heating | vacation temperature for every room, preheating for the return (the own return comes first); the ventilation advice rests (state "vacation", no statistics, no humidity profile; option) |
| Covers | vacation simulation morning and evening; heat protection: the sun protection lowers without waiting for room, air conditioner or heat need, only on summer days (option) |
| House | report of the open, tilted or unknown windows at the start, and right away when a window is opened or tilted on vacation (option) |
| Meters | leak warning by amount and mean flow or power since the start, once per vacation and case; on by default for water (20 L, 5 L/h), never for the heat meter |

Messages go to the notification services of the house, without any as a notification in Home Assistant.

## Dashboard cards

The cards are loaded automatically for every user and every dashboard, without an entry by hand: as an extra module of the frontend as soon as the integration starts (also in a page already open or the companion app), and in addition as a dashboard resource at an address of its own. All files are below a folder with the version, so after an update no page mixes old and new files.

| Card | Module |
|---|---|
| `custom:house-assistant-thermostat-card` | heating: thermostat with humidity |
| `custom:house-assistant-thermostat-compact-card` | heating: thermostat compact |
| `custom:house-assistant-climate-tile-card` | heating: room climate tile |
| `custom:house-assistant-cover-card` | covers: every window with status, buttons and sun compass |
| `custom:house-assistant-tile` | covers: tile for a cover or a window contact |
| `custom:house-assistant-window-tile` | covers: window tile with window and cover |

Examples and options are in [docs/heating.en.md](docs/heating.en.md#dashboard-cards) and [docs/covers.en.md](docs/covers.en.md#dashboard-cards).

## Services and events

| Service | Purpose |
|---|---|
| `house_assistant.set_vacation` | plan the vacation: `departure`, `return`, `clear` |
| `house_assistant.export_parameters`, `import_parameters`, `reset_learned` | learned values of the heating |
| `house_assistant.run_ai_check`, `run_ai_ventilation_check`, `decide_heating_day` | AI reviews and heating day decision now |
| `house_assistant.move_cover`, `start_cover_override`, `end_cover_override`, `resume_cover` | covers |
| `house_assistant.read_meter`, `set_meter_reading` | meters |

Events: `house_assistant_vacation`, `house_assistant_vacation_alert`, `house_assistant_cover_moved`, `house_assistant_cover_failed`, `house_assistant_protection`, `house_assistant_meter_reading` and one shared logbook event `house_assistant_logbook`.

## Troubleshooting

* **Diagnostics:** Settings > Devices & services > House Assistant > ⋮ > Download diagnostics (API key and notification services are redacted).
* **Debug log:** at the integration ⋮ > *Enable debug logging*, or in `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.house_assistant: debug
    anthropic: debug
```

* More per module in [docs/heating.en.md](docs/heating.en.md#troubleshooting), [docs/covers.en.md](docs/covers.en.md#troubleshooting).

## Removal

Settings > Devices & services > House Assistant > ⋮ > **Delete**. The heating switches off every circuit that is on first. Stored data (`.storage/house_assistant.<entry>.*`), panel, cards and repair issues are removed; the pictures of the meters stay in the media folder (`media/house_assistant`). Then remove the folder or the HACS download.

## Development

```bash
pip install -r requirements_test.txt ruff
ruff check custom_components tests scripts
ruff format --check custom_components tests scripts
python scripts/build_labels.py --check
pytest
```

The texts of the panel (`frontend/labels.js`) and of the cards (`frontend/card-labels.js`) are generated from the translation files. After changing `translations/*.json` run `python scripts/build_labels.py` once (a test checks it). The pure logic in `*/logic/` has no dependency on Home Assistant and can be tested on its own. Before publishing, `python scripts/check_privacy.py --patterns <file>` checks for private data. The plan of the rebuild is in [docs/PLAN.md](docs/PLAN.md) (German).

## License

MIT, see [LICENSE](LICENSE).
