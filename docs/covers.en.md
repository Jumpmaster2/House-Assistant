# Covers

[Deutsch](covers.md) | English

The **covers** module (formerly Shutter Assistant) controls roller shutters and external venetian blinds automatically (the height; slats are not tilted): sun protection by direction, evening mode, ventilation position, weather protection (wind, rain, frost), manual override, morning opening and vacation simulation. Everything is set in the user interface, nothing is hard-coded. There is no AI and no learning; the rules are easy to follow and every movement is in the logbook with its reason.

It typically replaces a bundle of YAML automations with many helpers (input_boolean, input_number, timer) for sun protection, auto up, evening run, follow-up closing, airing, override and vacation (see [moving from YAML automations](migration.md)).

## How it works

The module is event driven: it reacts only to state changes of the entities configured and to calculated times (sun enters or leaves a sector, start of the evening, hold times, end of an override, day change). There is no polling every second.

### Directions and windows

* A **direction** (group) has an azimuth from and to and any number of sun sensors (PV power, brightness in lux, radiation e.g. from Open-Meteo). A direction has no thresholds.
* A **window with a cover** is a window of the house (*House > Windows*) with a cover, window contact(s) and a direction. All thresholds, positions and times are set on the window (*Covers > Windows*). A window without a cover serves only the heating.
* If the window belongs to a **room**, it takes the values of the room: as room temperature the temperature sensor of the room and as target the thermostat of the room (heating), plus the air conditioner of the room. A value set on the window wins.

### Sun protection

* **Summer day:** sun protection only on summer days. At the day change (default 01:00) the high of the daily forecast is checked. If the outdoor temperature rises above the threshold during the day, it becomes a summer day as well, but only if the forecast low of the coming night is at least 14 °C (configurable). A warm afternoon in spring or autumn with a cool night does not trigger sun protection. Without a low in the forecast the summer day applies as before.
* **Sun condition per window:** summer day AND outdoor temperature above the threshold of the window (with hold time) AND every sun sensor of the direction above its threshold. All of it must hold for the sun hold time and ends at once. After a restart it is evaluated right away; the hold time runs from the start.
* **Heat need (optional):** with a **room temperature** (from the room or on the window) it only lowers when the room is too warm: with a thermostat from target + 2 K, with a temperature sensor from 24 °C. If the chosen **air conditioner** cools, the room counts as too warm; the sun protection relieves it. If it reports no action (e.g. Midea), the mode "cool" counts, and in the mode "auto" a room temperature above its target. With **heating need** the warmth of the sun is welcome: it then only lowers when the room is too warm anyway; windows without a room temperature stay up. Heating need is an own entity (e.g. an input_boolean "heating season") or, without one, the **heating day of the heating** (option, only within the heating period). Opening again does not depend on it; it only follows the position of the sun.
* **Heat protection on vacation:** during the vacation of the house the sun protection lowers without waiting for room temperature, air conditioner or heat need. Summer day, outdoor temperature, sun sensors, hold times and the sun protection switch of the window still apply, so nothing is lowered in winter (option, on by default).
* **Lowering:** when the sun is in the sector of the direction and the sun condition holds, the cover moves to the sun protection position once a day. If it is already further closed, it is only marked and left alone. An open window prevents the movement; then there is a notification once a day (per window switchable), but only if a movement was really prevented. After the window is closed, it is caught up.
* **Auto up:** when the sun leaves the sector, the cover opens again, but only if it still stands at the sun protection position (up to the tolerance above). Covers set differently by hand stay as they are. No auto up in the evening mode, with an override or an opening block. Switchable per window.
* **Detect manual sun protection:** if someone lowers a cover by hand far enough while the sun shines (default at most 25 %), that counts as sun protection for today. Optionally every movement exactly onto the sun protection position counts as well.

### Evening

* **Evening mode:** starts when the sun sinks below the configured elevation (default -4 °), at the earliest at 17:00 and at the latest at 21:00. It ends at 03:30 or at sunrise. Values global or per window.
* **Evening run:** at the start of the evening mode each cover closes once if the window is closed and no override is active (per window: close despite an override, e.g. bedrooms).
* **Evening position:** per window the target of evening run, follow-up closing and vacation in the evening. Default 0 % = closed; e.g. 20 % leaves a gap on warm nights.
* **Follow-up closing:** when a window is closed in the evening, the cover closes (from 16:00, also with an override).
* **Ventilation position:** when a window is opened and the cover is (almost) closed, it moves to the ventilation position (default 30 %). In the evening after 3 s, in daytime after 60 s, if the window is still open then.

### Window contacts, tilted and door

* **Open, tilted, closed:** window contacts report "on" = open. Window handles with the states `open`, `tilted` and `closed` work as well, and there are **tilt contacts** ("on" = tilted). For the covers unknown or unavailable counts as open (tilted for tilt contacts).
* **Tilted:** a window that is only tilted does not prevent a closing movement, but the cover moves down to the ventilation position at most. When a window is tilted, it gets the ventilation position as when opened. Fully open prevents closing movements.
* **Lockout protection (door):** while the contact reports open, nothing moves below the ventilation position, not even with a window exception, follow-up closing or weather protection.

### Weather protection

* **Switch on per window:** the weather protection only acts on windows with **Weather protection for this window** switched on (default off). Without the switch wind, rain and frost never move or limit the cover, even with positions entered (they are kept).
* **Automatic off = no weather protection:** with the automatic off (global or for the window), the weather protection does not move either; a running protection ends for these windows without a movement. If the automatic is switched on again while the protection still runs, the covers move to their protection position.
* **Wind and rain:** globally a wind sensor with a threshold (in the unit of the sensor) and a rain sensor (on/off or an amount above a threshold). Per window a **position on wind** and **on rain**, empty = not affected (e.g. venetian blinds to 100 % on wind, a roof window to 0 % on rain). An **own wind threshold** on the window replaces the global one for this window (e.g. a balcony cover from 50 km/h, the others from 75 km/h); it has its own release time, and the binary sensor wind protection is on as long as any window is protected (attribute `windows`). The protection starts at once and moves the covers concerned once to their position, **also with an override** (not during restart protection, caught up afterwards). Someone moving a cover by hand during the protection keeps that position: a restart of the module does not move protected covers again. A cover already **further closed** than its protection position counts as protected and is not raised (option **Further closed counts as protected**, default on; not for 100 %, retracting venetian blinds always runs). Wind comes before rain. An open window only prevents closing movements; they are caught up once it is closed.
* **While the protection runs,** every other rule rests for the window (status "weather protection"). It only ends once the value was back in the safe range for the **release time** (default 15 min). An unavailable sensor never ends a protection. Afterwards the automatic decides anew (sun protection, evening run); the old position is not restored.
* **Frost:** windows with a **lowest position on frost** (e.g. 5 %) close only down to it at an outdoor temperature up to the frost threshold (default 1 °C), so the cover does not freeze to the sill. This applies to all automatic movements and services, not to the wind and rain protection.
* **Display:** while wind or rain protection runs, the overview in the panel and the card show the current value of the triggering sensor (e.g. "wind protection 62 km/h"). The binary sensors wind and rain protection name the sensor in the attribute `sensor`.
* Start and end are in the logbook, plus the event `house_assistant_protection` with `kind` (wind, rain, frost) and `active`.

### Reliability

* **Spacing between commands** (advanced, default 0 = all at once): several covers move one after another, e.g. every 2 s, against radio collisions.
* **Check the position** (advanced, default after 90 s): if a cover has not reached its target by then (± 5 %), the command is repeated once. If that fails as well, there is a notification, a logbook entry and the event `house_assistant_cover_failed`. If the cover is still moving at the check, it looks once more later. A movement by hand ends the check.

### Override

Every manual movement (at the switch, in the app, not by House Assistant and not by other automations or scripts) starts an override for the window, default 60 min. Every further movement restarts it. Optionally it also ends at sunrise, with duration 0 only at sunrise. The module remembers its own movements, so late position reports are not taken for manual ones.

In the settings (panel *Covers > General*, card **Manual override**) you choose when it starts: **only when the cover really moves** (default; the position changes by more than 2 %, for covers without a position it stands differently afterwards) or **on every command by hand, also without a movement**. With the default, e.g. "Alexa, open all covers" starts no override for covers already open.

### Extra conditions instead of special rules

* **Opening block:** while an entity is not in one of the release states, nothing opens automatically (auto up, airing, vacation in the morning, morning opening). Example: TV on.
* **Closing trigger:** when one of the entities becomes active (on delay), the cover closes once per active cycle if it is further open than the minimum position and the window is closed. If the window is open, it closes once it is closed. The cycle ends when all entities are inactive (off delay). Example: switching on the TV closes the living room cover.
* **Window exception:** while an entity is available, an open window does not prevent a closing movement and there is no notification. Example: an air conditioner with its hose through the balcony door.

### Morning opening (per window, default off)

Modes: fixed time (workday as well as weekend and public holiday via the workday sensor of the house), sunrise or sun elevation with an offset, brightness of the direction above a threshold with a hold time, trigger entity (a timestamp like the next alarm of the phone, or an entity that turns on). Plus a time window at the earliest and at the latest, a target position (open or partly open) and optionally directly the sun protection position when the sun condition holds. Not with an override, an opening block or a cover moved by hand since the evening.

### Vacation simulation

During the vacation of the house (see [README](../README.en.md#vacation)) the normal evening run rests. Instead the windows taking part open in the morning at a random time (default 07:00 to 08:00) to a random position (60 to 100 %) and close at a random time in the evening (19:00 to 20:30). Sun protection (with heat protection) and airing go on.

### Restart protection

After Home Assistant starts there are no movements for a few minutes (default 5). Afterwards everything is evaluated and the evening run is caught up for windows not yet closed (only from 12:00). Overrides, daily markers, a running weather protection and the automatic switches are kept across restarts.

### Temperature units

All temperatures of the covers (thresholds, forecast, room) are in the unit of the unit system of Home Assistant. With °F the defaults are converted (summer day from 73 °F, night from 57 °F, outdoor temperature from 66 °F, room from 75 °F, target plus 4 °F). If the unit system is changed later, please adjust the thresholds by hand. The target of a thermostat of the heating is converted.

## Panel

In the panel **House Assistant**, section **Covers** (administrators only):

* **Overview:** automatic on/off, summer day (forecast and threshold), start of the evening mode, vacation, weather protection and restart protection. Plus the **sun compass** with the current position of the sun and the sectors of the directions, notes (e.g. configured entities that do not exist, or a deleted direction) and every window with status, position, window contact (open, tilted, closed), next action and last reason. A running override can be **ended** right there. The **sun condition check** shows per window every part of the condition with its current value and threshold: summer day (with the night low if the outdoor temperature triggered it), outdoor temperature, every sun sensor, room, air conditioner, heating need, heat protection on vacation, hold time (with the time it is met) and whether the sun is in the sector.
* **Windows:** every window with a cover as a table; click to edit. The editor shows the settings by topic in cards (window, sun protection, detect manual sun protection, evening, override, airing & vacation, morning opening, extra conditions, weather protection & door). Only the fields that apply right now appear: thresholds only for the sensor types of the direction, own evening times only when switched on, for the morning opening only the fields of the chosen mode. **Duplicate** creates a new window with the same settings; only cover and window contacts are chosen anew.
* **Groups:** directions with the current values of their sensors and the windows using them. While editing, the compass shows the sector at once.
* **House in the compass:** with length of the front, depth and orientation of the house set (*House > General*), the house appears to scale and rotated in the middle of the compass. A direction can then get a **wall**: the azimuth sector is set to the orientation of the wall ± 90° (freely changeable afterwards) and the wall appears in its colour. **Windows** appear as marks on their wall (own wall or the one of the direction), coloured live by sun protection, override and evening, hollow with the window open; a click opens the window. With **position on the wall** (1, 2, 3 …) the order of the windows on a wall is set: 1 is far left, looking out through the wall from inside; windows without a number come afterwards. Wall and position are also used by the heating for cross ventilation and draft.
* **General** and **Evening & vacation:** the settings in cards, each card is saved on its own.

Values are checked the same way as in the dialogs (same ranges, units and rules).

## Settings

Outdoor temperature, weather, language of the messages, notification services, workday sensor and weekend days are **settings of the house** (see [README](../README.en.md#settings-of-the-house)); the fields of the same name of the covers apply only while nothing is set there.

| Option (*Settings > Covers*) | Default | Meaning |
|---|---|---|
| Summer day from | 23 °C | high of the forecast |
| Late summer day only with night from | 14 °C | low of the coming night when only the outdoor temperature triggers the summer day |
| Heating need | | optional, e.g. an `input_boolean` "heating season"; on = warmth of the sun welcome |
| Heating day of the heating | on | without an own heating need the heating day of the heating module (only within the heating period) |
| Day change | 01:00 | check the forecast, reset the daily markers |
| Forecast type | automatic | daily, twice daily or hourly; automatic takes the first the weather entity supports |
| Evening mode earliest, sun elevation, latest | 17:00, -4 °, 21:00 | |
| End of the night | 03:30 | |
| Follow-up closing from | 16:00 | |
| Vacation morning from, random window | 07:00, 60 min | |
| Opening position from, to | 60 %, 100 % | |
| Vacation evening from, random window | 19:00, 90 min | |
| Heat protection on vacation | on | sun protection without room, air conditioner and heating need |
| Override starts | only on a real movement | or on every command by hand, also without a movement |
| Wind sensor, wind protection from | , 50 | unit of the sensor (e.g. km/h) |
| Rain sensor, rain protection above | , 0 | on/off or an amount (e.g. mm/h) |
| Frost from (at most) | 1 °C | outdoor temperature, only for windows with a frost position |
| Release after | 15 min | weather protection ends only after this time in the safe range |
| Restart protection | 5 min | |
| Catch up evening run from | 12:00 | |
| Window counts as closed after (advanced) | 5 s | debouncing of the window contacts |
| Spacing between commands (advanced) | 0 s | 0 = all at once |
| Check position after (advanced) | 90 s | repeat once, then report; 0 = off |

### Directions

**Add group**: name, azimuth from and to (90 ° = east, 180 ° = south, 270 ° = west; the limits themselves do not count), radiation, PV and brightness sensors, wall.

### Windows

**Add window** (in the panel under *House > Windows* or *Covers > Windows*, or at the integration):

1. **Window:** name, room, size, cover, window contacts (also window handles), tilt contacts, direction (without one no sun protection), wall and position on the wall. Without a cover the dialog ends here.
2. **Sun protection:** thresholds for the sensor types of the direction, outdoor temperature at least (19 °C), hold times temperature (10 min) and sun (5 min), room temperature (empty = the one of the room; thermostat: too warm from target + 2 K, sensor: from 24 °C), air conditioner (empty = the one of the room), sun protection position (10 %), tolerance for auto up (5 %), auto up, notification with an open window, manual sun protection up to (25 %), detection window (5 min), follow-up time (5 min), a movement onto the sun protection position counts.
3. **Behaviour:** override (60 min, sunrise, evening and vacation movements despite an override), extra conditions, evening (evening run, evening position 0 %, follow-up closing, own evening times), airing (30 %, counts as closed up to 5 %, 3 s in the evening, 60 s in daytime), vacation simulation, weather protection & door (weather protection for this window, position on wind, own wind threshold, position on rain, lowest position on frost, further closed counts as protected, lockout protection).
4. **Morning opening:** on or off, mode and time window, then the settings of the mode.

Positions: 100 % = open, 0 % = closed. A cover and a contact belong to one window only.

## Entities

Device "Covers":

* Switch **Automatic** (off = no automatic movement; kept across restarts)
* Binary sensors **Summer day** and **Evening mode**
* Binary sensors **Wind protection**, **Rain protection** and **Frost protection** (only when set up, with the end of the release time)
* Sensor **Forecast high**

Per window with a cover (own device):

* Sensor **Status** (weather protection, automatic off, restart protection, manual override, closed this evening, sun protection, vacation simulation, ready)
* Sensor **Last reason** (text, code, position, time)
* Sensor **Next action** (time, attribute `action`: evening run, morning opening, end of the override, sun enters or leaves the sector, weather protection may end)
* Switches **Automatic** (only this window; off = no weather protection either) and **Sun protection** (off = do not lower on sun; covers already lowered open again as usual), both kept across restarts
* Binary sensors **Manual override** (with its end), **Sun condition** (with its parts), **Sun protection today**, **Closed this evening**

For check cards on a dashboard **Sun condition** (thresholds, sensors, azimuth sector, hold times and when they run out) and **Status** (cover, window contacts, start of the evening, override until) provide every value as attributes. **Evening mode** has start and end of the current or next evening, **Automatic** the end of a running restart protection. "Sun condition", "Last reason" and "Forecast high" are diagnostic entities; the attributes of "Sun condition" and "Status" are not recorded (they change often).

Every movement and every override is in the **logbook** with its reason.

## Services and events

All services act on the covers of configured windows (`entity_id`, also an entity of the window); without `entity_id` on all windows. They start no override.

| Service | Effect |
|---|---|
| `house_assistant.move_cover` | `action`: `open`, `close`, `evening` (evening position, marked as "closed this evening"), `sun_protection` (sun protection position, marked as sun protection, opens later with auto up), `ventilation` or `position` with `position`. Frost and lockout protection still apply. |
| `house_assistant.start_cover_override` | override like a movement by hand; `duration` in minutes (empty = duration of the window, 0 = until sunrise) |
| `house_assistant.end_cover_override` | end a running override |
| `house_assistant.resume_cover` | end the override and decide right away (sun protection, evening run) |

```yaml
# Example: on a thunderstorm warning all covers on the ground floor to the evening position
action: house_assistant.move_cover
data:
  entity_id: [cover.living_room, cover.kitchen]
  action: evening
```

Events for own automations:

* `house_assistant_cover_moved`: every movement command with `window`, `window_id`, `entity_id`, `position` and `reason` (e.g. `sun_lower`, `evening_close`, `protection_wind`, `service`)
* `house_assistant_cover_failed`: target not reached even after the repetition, with `position` and `current_position`
* `house_assistant_protection`: weather protection starts or ends, with `kind` and `active`

## Dashboard cards

For every user (also without admin rights); the cards are loaded automatically (see [README](../README.en.md#dashboard-cards)).

**Cover card** (`custom:house-assistant-cover-card`): every window with status, position, window contact, next action and a running override (with "resume automatic"), buttons for up, stop and down (they act like a switch, so they start an override), an active weather protection and a small sun compass. Nothing can be set from the card.

```yaml
type: custom:house-assistant-cover-card
title: Covers            # optional
windows: [Living room]   # optional: names or ids, default all
compass: true            # optional: show the sun compass
```

**Tile** (`custom:house-assistant-tile`, 3 × 1): a cover or a window contact. The name at the top, below icon and state (opening or open, tilted, closed). The cover moves into the tile from the top as slats. An open or tilted window colours the tile. A tap opens the more-info dialog.

```yaml
type: custom:house-assistant-tile
entity: cover.living_room   # cover, binary_sensor (on = open) or window handle (open/tilted/closed)
name: Living room           # optional
icon: mdi:blinds            # optional
```

**Window tile** (`custom:house-assistant-window-tile`, 6 × 1): window and cover together: the name at the top, below on the left the window (open, tilted, closed) and on the right the cover with its opening. Without a window contact only the cover.

```yaml
type: custom:house-assistant-window-tile
window: Living room        # window of the house (name or id), or yourself:
cover: cover.living_room
contact: binary_sensor.living_room_window
tilt: binary_sensor.living_room_window_tilted   # optional, on = tilted
```

Colours (both tiles, optional): `color_cover`, `color_closed`, `color_open` and `color_tilted`, each a colour name of the theme (`purple`, `orange`, `teal`, …) or a CSS colour (`"#00897b"`). Everything can also be set in the card editor.

### Own dashboard cards

The attributes of the entities can be used in own cards, for example:

```yaml
type: entities
title: Living room
entities:
  - entity: sensor.living_room_status
  - entity: binary_sensor.living_room_sun_condition
    secondary_info: last-changed
  - type: attribute
    entity: sensor.living_room_status
    attribute: evening_start
    name: Evening from
  - type: attribute
    entity: binary_sensor.living_room_sun_condition
    attribute: condition_on_at
    name: Sun condition met from
```

## Troubleshooting

* **No sun protection:** open the **sun condition check** of the window in the panel. Every part shows value and threshold. Common reasons: no summer day (forecast below the threshold), no direction, a sun sensor below its threshold, the hold time still running, an open window, an active override.
* **Override starts unwanted:** choose "only when the cover really moves" (panel *Covers > General*, card **Manual override**). Movements of other automations and scripts never count.
* **No forecast:** panel and repairs show a note when the weather entity provides no forecast. Choose a forecast type or another weather entity.
* **Cover does not move to a position:** covers without position support can only open and close (a warning is logged).
* **Message "cover did not reach … %":** the cover reports its position not at all or inaccurately. Extend "check position after" (advanced) or set it to 0.
* **Cover stays up or at the ventilation position:** weather protection active (status "weather protection"), window tilted, lockout protection of an open door, or frost. The last reason and the overview show what applies.
