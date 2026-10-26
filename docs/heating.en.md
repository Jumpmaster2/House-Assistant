# Heating

[Deutsch](heating.md) | English

The **heating** module (formerly AI Heating Assistant) controls underfloor heating (or radiators per room, see heating type) with one switch per heating circuit (for example a relay that drives the valve actuator) locally, learns the behaviour of every room and lets Claude (Anthropic) review the parameters periodically. Home Assistant makes every switching decision itself. The AI never switches anything; it only adjusts parameters within configurable limits and is asked less often as the local model becomes more reliable.

It typically replaces: thermostat helpers (Generic Thermostat), Better Thermostat, automations for setpoint, weather, cold and vacation handling, and a humidity based ventilation recommendation.

Rooms and windows come from the **house** (panel *House Assistant > House*): a room with a temperature sensor gets heating and ventilation advice, with a heating circuit switch also a thermostat. The window contacts are the contacts of the windows of the room; the size of the window gives the opening area.

## Local control per room

* **Target** with the regular thermostat card. It is stored until you change it. No schedules, no night setback (usually counterproductive with underfloor heating).
* **Predictive switch-on:** the circuit turns on when the temperature would fall below target minus the switch-on hysteresis after the learned dead time (taking cooling rate, outdoor temperature and sun into account).
* **Predictive sun:** for the cooling over the lead time not only the current PV power counts but the power expected during that time. If the sun is going to warm the room anyway, the circuit does not switch on in the morning; in the evening the control no longer counts on sun that is about to go. The source is an optional PV forecast sensor (e.g. Forecast.Solar) or, without it, the hourly weather forecast (cloud cover) together with the position of the sun. For that the module learns on almost cloudless days how much PV power to expect under a clear sky. The forecast counts only 70 % (option "Trust in the sun forecast"), and 1 K below target it heats regardless of any forecast (option "Always heat below target by", 0.3 to 3 K). Without a PV power sensor everything stays as before. If the sensor gives no value in daytime, the PV power counts as unknown: nothing is calibrated or fed into the model, the expected power is used (PV forecast sensor, or sun position and cloud cover once the scale is learned, otherwise 0); with the sun low or hardly any power to expect, 0 applies. If the value is missing for more than an hour in daytime, a warning is logged.
* **Predictive switch-off:** the circuit turns off when the current temperature plus the expected overshoot reaches target plus the switch-off hysteresis. The overshoot of the slow underfloor heating is learned (depending on the run time). After switching off, the heat still in the floor is taken into account when switching on again until the temperature falls; otherwise the circuit would start again right after the minimum pause.
* **Windows:** if a window of the room is open for longer than the window delay, the heat request pauses. After closing, the learned recovery time is awaited because screed and walls often warm the room by themselves. Once the temperature from before the airing is reached, the recovery ends at once (not after brief airing, see *Brief airing*). The recovery time follows the airing itself (see *Learning per room*): after short airing the heating waits less than after long airing in frost or cross ventilation. **Tilted** counts like open but with only 25 % of the opening area: from a window handle (open, tilted, closed) or a tilt contact of the window. An unavailable contact counts as closed, as before.
* **Cross ventilation and draft, automatic:** from the arrangement of the windows on the house (wall and position, floor from the Home Assistant area of the room) the module tells two cases:
  * *Cross ventilation:* an own window is open together with a window of another room on the same floor on an opposite or adjacent wall.
  * *Draft:* two windows of other rooms on the same floor (opposite or adjacent walls) are open and the room lies within the *draft reach* (default 2 m) of the line between them. The room then behaves as with an own open window: pause after the window delay, then recovery, no learning and no counting as "too cold". This needs the length and depth of the house (*House > General*); without them there is only cross ventilation.

  In the room editor (*House > Rooms*) a plan of the house shows the combinations as lines; each can be switched off. Without floors in Home Assistant all rooms are on one floor; a room whose floor cannot be told takes no part. A window without a wall (its own or the one of its direction) takes no part either.
* **Draft by hand:** in addition each room has up to four combinations of window contacts of other rooms under *Draft from other rooms* (also across floors, e.g. a staircase). As soon as every window of a combination is open, that counts as a draft. A combination with a single window triggers on its own. The ventilation advice of the room still follows only its own windows. The thermostat attributes `draft` and `draft_windows` show whether a draft is detected and through which windows.
* **Brief airing:** while a window is open, a circuit that is off does not switch on, also before the window delay has passed. A running circuit is not interrupted. If the window was open for at least *Brief airing from* (default 1 minute, per room) but shorter than the window delay, the heating then waits a fixed time: the learned recovery time times *Wait after brief airing* (default 50 %, so 15 minutes with 30 minutes learned). This wait ends only when the time has passed, not when the temperature is back, and it does not scale with the length of the airing. 0 % means no wait. The logbook shows "Aired briefly: waiting until ..." and "Wait after brief airing finished."; nothing is logged for an airing that is too short or with no wait. The learning of the recovery time is not affected: it still measures until the room is back at its temperature. Both values are start values set when the room is created (next to the window delay; the AI does not adjust them).
* **Minimum on and off times** are always kept.
* **Frost protection** always applies, also outside the heating period and with the thermostat off.
* **Outages:** if the temperature sensor gives no or an impossible value (outside −50 to 80 °C, `nan`), the circuit stays off (status *sensor error*); frost protection cannot act then either. If the switch is unavailable, the status shows *actuator unavailable*. If such an outage (or the one of the outdoor temperature sensor) lasts longer than 15 minutes, a repair issue appears under Settings > System > Repairs; it disappears by itself once the value is back. An ignored issue stays ignored across restarts as long as the outage lasts. If a switch does not follow the commands, it is switched again after 1, 2, 4, 8 and then every 15 minutes instead of every minute; after three attempts an issue appears as well.
* **Heating period:** outside of it (e.g. 01.04. to 30.09.) all circuits stay off and there are no AI requests.
* **Vacation:** during the vacation of the house (switch *Vacation* with departure and return, or an external source such as a calendar; see [README](../README.en.md#vacation)) the vacation temperature applies to every room. With the learned heating rate it preheats in time so the normal target is reached at the return; the own return of the switch comes before a return entity. A return in the past is ignored and the vacation temperature applies. The ventilation advice rests on vacation (option *Ventilation advice rests*, on by default).

## Heating day decision (nightly run)

Once a night (time configurable) it is decided whether to heat at all today.

1. A **local rule** proposes: heat if the forecast high is below `theta` or a room is below target plus `puffer`.
2. The **AI** gets the weather forecast, room values, learned values and the evaluated last days (with heating minutes and overheating per day) and answers in a structured way (JSON with schema). Comfort comes first, but unnecessary heating days should be avoided.
3. A **phase model** decides who leads: *AI leads* (start), *together* (if they agree that, otherwise the rule if it is confident), *rule leads* (the AI is only asked when the rule is unsure, plus once a week as a check). It moves on after enough days with high agreement and few rule errors, and back one phase on errors.
4. Every day is **evaluated** afterwards. As long as nothing heated, the real room temperature counts (minutes too cold outside airing). Once a circuit ran, the decision kept the room warm itself; then a virtual room counts that goes on with the learned cooling rate without heating. Error A (did not heat although needed) and error B (heated without need) adjust `theta` and `puffer`. Days with a manual override and vacation days are not learned.

On "no heating day" every circuit stays off except frost protection and the optional **emergency rule** (room below target and expected to stay clearly below it after the lead time, without airing). The selection "Heating day manual" overrides the day until the next decision. "Heat today" also works outside the heating period (on a cold spring day, for example); the AI stays off there.

The heating day is available to the other modules: as the heat need of the covers (option *Heating day of the heating*) and as the condition of the meters (option *days without heating*).

## Learning per room

* **Thermal model** (recursive least squares): `dT/dt = a · valve − k · (T_in − T_out) + s · PV`. It gives heating rate, cooling rate, influence of the outdoor temperature (`k`) and of the sun (`s`, PV power as an indicator of sun).
* **Events:** dead time after switching on, overshoot after switching off, recovery time after airing. The dead time only counts once the rise is confirmed (a second sensor step or a step that lasts five minutes), so a single jitter of the sensor does not distort it. The recovery time is also learned when the heating ends the wait early, if the room was warming by itself at the end of the wait; the thermal model forgets slowly (about three weeks).
* **Recovery per airing:** how long a room needs to recover depends on how much it cooled during airing. Every airing is therefore followed: how far the temperature fell until closing (K) and how long and how deep it was below the value before airing (kelvin hours; long airing, cross ventilation and frost also cool walls and floor). A second model (least squares) learns `recovery = base + minutes per K drop + minutes per kelvin hour`. From four evaluated airings the heating waits the time expected for each airing, at most three times and at least a quarter of the mean recovery time. Before that the mean recovery time applies. The model forgets slowly (about 30 airings); the coefficients are attributes of the sensor *Recovery time after airing* and are exported as well.
* Every value is stored, shown as a sensor and can be exported, imported and reset. Export and import find rooms by name, so every room needs a different name. If the AI limits are narrowed, values outside are set to the limit at the next load (with a logbook entry).

## AI review (Claude)

* Only on heating days and within the heating period. It gets a compact summary per room (current, target, learned values, figures since the last review) and returns parameter adjustments as JSON. It writes its reasons in the language of the messages (settings of the house, otherwise the language of Home Assistant, also regional variants like de-CH).
* **Goal:** as little heat as possible without any room falling below its target. Comfort is a fixed limit, not something to trade. Besides the minutes too cold the AI gets:
  * **Overheating** (`over_kh`): kelvin hours more than 0.2 K above target while the circuit runs and up to 4 hours after switching off (heat the heating delivered too much). Heat only from the sun on a day without heating does not count. The share with sun (`sun_over_kh`, PV from 0.3 kW or from 10 % of the learned clear-sky power) shows whether the sun factor is too low.
  * **Heating effort per need** (`on_per_kh`): heating minutes per kelvin hour of difference between target and outdoor temperature, so reviews in different weather are comparable.
  * **Mean run time** per switch-on.
  * **Airing and recovery:** minutes with an open window, of which only draft from other rooms (`draft_min`) and cross ventilation with an own window (`cross_min`), number of airings, minutes in recovery and of those too cold (`rec_cold_min`, not counted as minutes too cold). In addition the last 8 airings one by one: time, duration, kind (own window, cross ventilation, only draft), opening area, outdoor temperature, temperature before, drop, kelvin hours, expected and actual recovery and how it ended. With that the AI can adjust the recovery correction and the window delay specifically.
  * **History of the last 6 reviews** with their figures and the changes made. The AI can judge whether a change helped and otherwise take it back. When a room is reset or a learned value is changed by hand, its history is deleted.
* Adjustable parameters: switch-on and switch-off hysteresis, overshoot factor, lead time factor, sun factor, window delay, recovery correction, `puffer` and `theta`. Every value is limited to a minimum, a maximum and a largest change per review (all configurable).
* **Customise the AI instructions:** in the panel under *Heating > AI > AI instructions* the instructions of both requests (nightly decision and parameter review) are split into blocks. Each default block can be switched off or reworded (*Restore default* resets it). Own blocks (up to 10 per request, at most 2000 characters each, in any language) add knowledge about the house, e.g. "In the living area the wood stove usually burns in the evening". Task and answer format stay fixed so the answer stays valid. A preview shows the complete instruction. Longer instructions cost a little more per request.
* **Ask less often:** the review interval doubles after each review without relevant change and without comfort errors (up to the maximum interval). It drops back to the base interval when it was too cold, a room was clearly overheated (more than 0.5 kelvin hours per day, prorated), the AI changed clearly, or you change settings or a target by at least 0.5 K (smaller steps, e.g. from automations, do not reset the interval). A review already planned stays across the nightly run; after a day without heating the next review follows after the base interval, and if a room was too cold since the last review, the next review comes sooner.
* **Costs:** from the token usage times the prices entered (in USD). If another model answers after a fallback on the server, its list price applies. Before each request it is estimated (output: twice the mean of the answers of the month so far, at most the maximum output tokens, default 16000 including thinking); once the monthly budget is reached there are no requests until the next month.
* **Outage:** on errors, timeouts or invalid answers the control goes on with the last learned values. The API key never appears in the log and is redacted in the diagnostics.
* **Rejected API key:** if Anthropic rejects the key (e.g. revoked), Home Assistant asks for a new key under Settings > Devices & services (re-authentication). Until then the local control goes on without AI; an empty field switches the AI off.
* **Weather service does not answer:** the forecast is awaited for at most 10 seconds; then the heating day rule decides without a forecast and the control goes on. If the heating day decision fails, it is retried after 15 minutes (error in the log).

## Heat meter

Optional. With a heat meter the AI sees the heat actually used instead of only the run time of the circuits. A meter of the **meters** module works best: the heating then gets the real time of the reading, and a confirmed correction downwards is no meter change. Any energy sensor still works.

* Consumption is always calculated **between two meter values**, not between arbitrary times. With every meter value the module remembers the heating need accumulated until then (kelvin hours target minus outdoor temperature, mean over the rooms). Consumption and need cover exactly the same period, also when the meter reports only every few hours and in coarse steps.
* **AI review:** `heat` with kWh, hours and `kwh_per_kh` (kWh per kelvin hour of need, the best measure of efficiency) since the last review; periods below one hour are not reported. `kwh_per_kh` is also in the review history.
* **Nightly run:** kWh per past heating day in the history.
* **Panel:** card **Heat** with today, yesterday, this month and the time of the last meter value. A day counts from the last meter value before midnight to the last one before the next midnight; "yesterday" is missing after a skipped day.
* If the reading goes down (meter change, not a confirmed correction) or another meter is chosen, counting starts anew.

### Heat per room

With a floor area per room (field **Floor area**, m², 1 to 200) the module splits every meter reading over the rooms. A heating phase is the time between two changed readings. Every room that heated in it takes a share: run time times floor area times heating demand (target minus outdoor temperature) times a power per m² and K that the module learns from the phases. The shares always add up to the reading. What no room heated (hot water, pipes) is counted as **Not assigned**. Rooms without floor area take no part.

* **Sensors:** per room **Heat consumption** (total kWh, for the energy dashboard), **Heat consumption today** and **Estimated heat output** (kW at the target and the outdoor temperature of now; attributes `confidence`, `kwh_since_last_reading_estimate`, `minutes_heated_today`). For the house **Not assigned**. The totals only change with the readings and never fall.
* **Confidence:** `confidence` grows with the heating phases of the room. Phases in which this room alone heated teach fastest. The meter only reports whole kWh; short phases are merged with the next one. At the start the shares are rough.
* **Readings:** while a room heats, the heat meter is read every 15 minutes, otherwise once a day (options of the meter "Interval while a room heats" and "Interval otherwise"). Switching the heating on and off (the first circuit on, the last one off) asks for a reading, at least 5 minutes after the last one. After the end the short interval lasts at most 30 more minutes, so the last heat of the phase is still counted for it; with no circuit on nothing is used after that. This applies to heat meters and to meters with the condition "Heating day".

## Ventilation advice

Per room with a temperature sensor (also without a heating circuit) from the absolute humidity inside and outside (or of a reference room):
*Ventilate now* (humidity above the threshold, the outdoor air drier and airing lowers the humidity noticeably), *Ventilation useful* (cools when not heating; in the heating period only when the room is clearly above target; never below the optional minimum temperature and never when the outdoor air would bring the relative humidity of the room above its threshold), *Do not ventilate*, *Close window* (open but useless), *Ventilation blocked* (blocking entity active, e.g. an air conditioner), *All optimal* and *Vacation* (the advice rests on vacation).

**Learned humidity profile per room:** for every room with a humidity sensor the module learns what is usual in the room (daily minimum, mean and maximum, day and night, separately for the heating period and the rest of the year), the lowest humidity of the last 14 days, how fast the humidity rises with the window closed and what airing really achieves: which share of the difference to the outdoor air disappears while airing and how much of it comes back from walls and furniture within 30 minutes. Once two airings are evaluated, the advice works with the humidity airing actually reaches: if it does not fall by at least the minimum humidity drop, the advice is *Do not ventilate* instead of *Ventilate now* (sometimes it just does not get lower). A hysteresis prevents flapping around the threshold. Vacation days stay out of the profile.

**Energy saving airing:** in the heating period airing costs heat, the more the colder the outdoor air. A room only slightly too humid therefore waits: the humidity has to exceed the threshold by the *energy saving surcharge* per kelvin of temperature difference (default 0.25 %/K, so with 21 °C inside and 1 °C outside 5 % more). Until then the advice is *Do not ventilate*, an open window gives *Close window*. Once airing started, it goes on down to the hysteresis below the needed humidity. The surcharge never reaches beyond the *mould limit* (default 70 %, per room, e.g. lower with cold outer walls); from there it always airs against mould. After an airing the room gets a *pause* (default 30 minutes) in which humidity comes back from the walls before drying is advised again.

**Learned airing time:** every room learns from its airings how fast its windows exchange the air (scaled to the temperature difference, as cold air flows faster). From that the attribute `airing_minutes` proposes the minutes needed to reach the *airing target* (default 5 % below the threshold), times the *airing time factor*, limited to the *shortest* and *longest airing time* (3 to 20 minutes). Until two airings are evaluated, a table by outdoor temperature applies (5 minutes in frost, 10 up to 10 °C, 15 up to 15 °C, otherwise 20). The size of the windows counts: a small window has half the opening of a medium one, a large one 1.6 times, a door 2.5 times, a tilted window a quarter of its size. The air exchange is learned per opening area, so the airing time fits every window of the room. The largest opening is proposed (attribute `airing_window`) with its duration; if a window is already open, the duration for the open windows applies. **Cross ventilation** (an own window together with a window of another room, automatic or by hand) exchanges the air much faster; the room learns a separate air exchange for it. Until two cross ventilations are evaluated, the normal (longer) value applies. With every airing the AI sees the proposed and the actual duration, whether it was cross ventilation, the humidity before, at its lowest and 30 minutes after, and adjusts all these values per room.

**AI ventilation check:** all year round the AI checks the ventilation thresholds of every room with a humidity sensor, built like the parameter review of the heating circuits: it gets the humidity profile, the figures since the last check (minutes humid, from 70 %, advised, window open, open needlessly, open while heating, changes of the advice; vacation minutes do not count) and the history of earlier checks, and may adjust per room the humidity threshold, hysteresis, minimum drying advantage, reference excess temperature, minimum humidity drop, energy saving surcharge, mould limit, airing target, airing time factor, shortest and longest airing time, pause after airing, minimum cooling advantage, cooling margin and cooling-from temperature within the AI limits. The values configured are starting values; changing them replaces the value of the AI. The interval starts at the base interval (6 h) and doubles with every check without relevant change up to the maximum interval (72 h); if a room stays humid for long or something changes, it starts again. The check uses the shared monthly budget; its instructions can be customised under *AI instructions* (ventilation check). The tab **Learned values** shows the values learned.

## Panel

In the panel **House Assistant**, section **Heating** (administrators only):

* **Overview:** heating day with phase and reason, heating day manual (automatic, heat today, do not heat today), every room with temperature, target, status and ventilation advice (click opens the thermostat), switch AI enabled, last and next AI review, next nightly run, last heating day decision with its source (AI, rule, both agree), AI costs of the month, notes (missing entities, last AI error, budget reached) and a summary of the settings.
* **Rooms:** the heating per room (circuit, targets, minimum run times, heating type, ventilation, draft by hand); name, area, sensors and windows are in the section **House**.
* **Learned values:** per room with a circuit a compact tile with learning progress, heating and cooling rate, dead time, overshoot, recovery after airing, influence of outdoor temperature and sun; expandable the control parameters the AI may adjust. Plus the heating day rule (`theta`, evaluated days). The pencil edits the learned values.
* **General, Emergency & ventilation, AI, Heating day decision:** every setting by topic in cards, each card is saved on its own. Under **AI** also the API key (checked before saving; the stored key is never shown) and the AI limits.

## Dashboard cards

The cards are loaded automatically for every user and dashboard (see [README](../README.en.md#dashboard-cards)).

**Thermostat** (`custom:house-assistant-thermostat-card`): looks like the thermostat card of Home Assistant and also shows the **humidity** of the room, in the same line as the second temperature. Set the target by dragging the dot on the ring or with the arrow buttons (touching the ring elsewhere only scrolls the page); the three dots open the thermostat. With a fixed height (`grid_options` with `rows` as a number) the ring shrinks to fit the tile.

```yaml
type: custom:house-assistant-thermostat-card
entity: climate.living_area
show_current_as_primary: true   # current temperature large, target small (default: false)
show_humidity: true             # default: true
name: Living area               # optional
```

**Thermostat compact** (`custom:house-assistant-thermostat-compact-card`): without the arc, half as high (default 6 × 2): the name at the top, large the current temperature and the humidity, small the target and the status. The bar on the left is orange while heating, otherwise grey. A tap opens the thermostat.

```yaml
type: custom:house-assistant-thermostat-compact-card
entity: climate.living_area
show_humidity: true   # default: true
name: Living area     # optional
```

**Room climate tile** (`custom:house-assistant-climate-tile-card`): default 6 × 1 like the tile card: the name at the top, below temperature and humidity side by side. The values come from the thermostat of the room or from any sensors (also for rooms without a circuit); a sensor given wins. A tap on a value opens its entity.

```yaml
type: custom:house-assistant-climate-tile-card
entity: climate.living_area            # and/or:
temperature_entity: sensor.bedroom_temperature
humidity_entity: sensor.bedroom_humidity
name: Bedroom                          # optional
```

## Settings

Temperature sensors may report in °C, °F or K; without a unit the unit system of Home Assistant applies. Internally everything is in °C, and every temperature in the settings of the heating (targets, frost protection, `theta`) is entered in °C. The thermostats show values in the unit system of Home Assistant.

Outdoor temperature, outdoor humidity, weather and vacation are **settings of the house** (see [README](../README.en.md#settings-of-the-house)); the fields of the same name of the heating apply only while nothing is set there.

| Option | Default | Meaning |
|---|---|---|
| PV power sensor | | optional, indicator of sun (W or kW; without a unit W, another unit is ignored with a warning) |
| PV forecast sensor | | optional, only with a PV power sensor: energy of the next hour (Wh or kWh) or power in one hour (W or kW); without it the weather forecast is used |
| Heat meter | | optional, reading of the circuits controlled here (a meter of the meters module or an energy sensor in Wh, kWh, MWh, MJ or GJ); rare and coarse values are no problem |
| Heating period | 01.10. to 31.03. (southern hemisphere: 01.05. to 30.09.) | as day and month in the dialog, as DD.MM. in the panel; at setup the proposal follows the latitude of Home Assistant |
| Frost protection | 7 °C | always applies |
| Vacation temperature | 18 °C | for every room |
| Preheating reserve | 30 min | |
| Ventilation advice rests | on | on vacation |
| Starting value `theta` | 16 °C | heating day rule; only at setup, afterwards the learned value is edited |
| API key, model | Claude Opus 5.5 | changeable, own model name possible |
| Nightly run | 03:00 | |
| Monthly budget | 5 USD | |

Order in the options menu (*Settings > Heating*): general, vacation, emergency rule, ventilation, AI, heating day decision (experts), AI limits (experts). Learning steps and decision phases are in collapsible sections.

* **Emergency rule:** on, 1 K below target (expected after the lead time, at least the switch-on hysteresis), 45 min, window 30 min unchanged.
* **Ventilation:** minimum advantage of absolute humidity 0.8 g/m³, outside at most 4 K warmer, minimum cooling advantage 1 K, cooling in the heating period only from 1 K above target, optionally cooling only from a fixed room temperature (e.g. 23.5 °C, all year, default off), night 20:00 to 08:00 (times, to the minute). All thresholds are starting values for the AI ventilation check (on, base interval 6 h, maximum interval 72 h).
* **AI:** model, effort (default low), nightly run, review interval 4 h, maximum interval 48 h, budget, prices in USD per million tokens (Anthropic bills in US dollars; nothing is converted) (input, output, cache write, cache read; preset with the list price of the model), maximum output tokens.
* **AI limits:** minimum, maximum, largest change per review for every parameter.
* **Heating day decision:** learned `theta` (changeable), evaluation thresholds, learning steps, conditions of the phase changes.

Change the API key in the panel under **Heating > AI** or with **Reconfigure**.

## Heating per room

In the panel under **Heating > Rooms** (or in the room dialog of the integration). Per room:

| Option | Default |
|---|---|
| Heating circuit switch | e.g. `switch.heating_circuit_1`; empty = ventilation advice only (needs a temperature sensor) |
| Starting target, lowest and highest target | 21 / 16 / 24 °C |
| Minimum on and off time | 10 / 10 min (fixed) |
| Heating type | underfloor heating (default), radiators or other; the AI judges inertia and learned values by it. The control itself learns the behaviour of every room anyway. |
| Starting values window delay, brief airing from, wait after brief airing, recovery time, dead time, puffer | 5 min, 1 min, 50 %, 30 min, 30 min, 0.7 K; only when created |
| Humidity threshold | 60 % |
| Floor area | optional, 1 to 200 m²; splits the heat meter over the rooms (see Heat per room) |
| Reference temperature and humidity | optional, instead of outside (room without an own window) |
| Ventilation blocking entity | optional |
| Draft from other rooms | optional: up to 4 combinations of window contacts of other rooms that have to be open together |

Starting values (also `theta`) are set only at setup or when created and apply until something is learned. Afterwards the room shows under **Learned values** the values the control currently uses (window delay, recovery time, dead time, puffer; the brief airing values are fixed start values), and the learned `theta` is under **Heating day decision**. Changing one there replaces the learned or AI-adjusted value; learning goes on from there, and the logbook notes it.

## Entities

Entities no longer created after a change (e.g. "Heat today" after removing the heat meter) are removed from the entity registry at the next start of the module. Fast changing forecast values (`predicted_temperature`, `expected_peak`, `expected_pv_kw`) and large attributes (parameter list, last days, rule, AI summary) are not recorded; the values are rounded to the precision shown so that not every minute creates a new state.

On new installations the diagnostic sensors of the learned values (heating and cooling rate, overshoot, dead time, recovery time, influence of outdoor and sun) start disabled; the panel shows the values anyway. AI timestamps, AI costs and the decision phase are diagnostic entities. The device of a room goes into its Home Assistant area.

Device "Heating":

* Binary sensor **Heating day** (with source, reason, confidence, phase, time of the decision `decided_at` and next nightly run `next_decision`)
* Sensors **Decision phase**, **Last AI review** (with summary and last error), **Next AI review**, **Last and next AI ventilation check**, **AI costs this month**
* Sensor **Heat today** (only with a heat meter, kWh; attributes `yesterday`, `month`, `last_month`, `meter_reading_at`)
* per room with floor area and heat meter: **Heat consumption**, **Heat consumption today**, **Estimated heat output**; for the house **Not assigned**
* Switch **AI enabled**
* Select **Heating day manual** (automatic, heat today, do not heat today)

Per room with a temperature sensor (own device):

* **Thermostat** (climate, only with a circuit), attributes among others `predicted_temperature`, `expected_peak`, `expected_pv_kw` (PV power expected over the lead time), `draft` and `draft_windows`
* Sensors **Status**, **Heating rate**, **Cooling rate**, **Overshoot after switch-off**, **Dead time**, **Recovery time after airing**, **Influence of outdoor temperature**, **Influence of sun**, **Learning progress**
* Sensor **Ventilation advice** and binary sensor **Ventilation recommended** (also for rooms without a circuit)

Every important decision and every AI adjustment with its reason is in the **logbook**.

## Services

`import_parameters`, `reset_learned`, `decide_heating_day`, `run_ai_check` and `run_ai_ventilation_check` (the last three may cause AI costs) may only be called by administrators; automations and scripts without a user may still use them.

| Service | Purpose |
|---|---|
| `house_assistant.export_parameters` | learned values and parameters as JSON (service response) |
| `house_assistant.import_parameters` | set learned values and parameters from JSON (e.g. starting values) |
| `house_assistant.reset_learned` | reset the learned values of single rooms to the starting values, optionally the parameters as well |
| `house_assistant.run_ai_check` | start the AI review now |
| `house_assistant.run_ai_ventilation_check` | start the AI ventilation check now |
| `house_assistant.decide_heating_day` | run the heating day decision now, optionally without AI |

Example import:

```yaml
action: house_assistant.import_parameters
data:
  data:
    areas:
      Living room:
        learned:
          dead_time_min: 45
          recovery_min: 40
          loss_per_h: 0.004
        params:
          hysteresis_on: 0.2
```

## Troubleshooting

* **Status *sensor error*:** the temperature sensor gives no value, an impossible one or a unit that is no temperature (warning in the log). The circuit stays off; after 15 minutes a repair issue appears.
* **Status *actuator unavailable*:** the switch is `unavailable`. If it does not follow commands, it is switched again with growing intervals; after three attempts a repair issue appears.
* **AI no longer asked:** budget reached (note in the panel, sensor *AI costs this month* with `budget_reached`) or the API key was rejected (re-authentication under Settings > Devices & services).

## Privacy

Without an API key nothing leaves the house. With a key the following goes to Anthropic: the room names, temperatures, targets and learned values, figures since the last review, outdoor temperature, PV power, a compact weather forecast, heat meter values and the history of the heating day decisions. Entity ids, location and the API key itself are not part of the requests.

## Known limitations

* Every temperature in the settings of the heating is entered in °C (sensors and thermostats may use °F).
* Only switching actuators (on/off) per heating circuit, no continuous valves.
* Cross ventilation and draft are an approximation from wall and order of the windows, without inner doors. Switch off wrong combinations in the room; combinations by hand stay possible.
* The split of the heat meter over the rooms is learned, not measured. A room without floor area takes no share; its heat goes to the other rooms of the phase, or to **Not assigned** when nobody else heated.

## Example automation

Do not heat on a bridge day. The selection applies to the day it is set on; set after midnight and before the nightly run it applies to the new day:

```yaml
automation:
  - alias: "No heating on bridge days"
    triggers:
      - trigger: time
        at: "00:30:00"
    conditions:
      - condition: state
        entity_id: calendar.bridge_days
        state: "on"
    actions:
      - action: select.select_option
        target:
          # the id is under Settings > Entities
          entity_id: select.heating_heating_day_override
        data:
          option: off_today
```

## Switching off

When the heating module is switched off, or the integration disabled or removed, it switches off every circuit that is on; otherwise a running circuit would go on heating without limit. The same applies to the switch of a room that no longer has a circuit and to a switch replaced by another in a room. A restart of the module (e.g. after a change of the settings) or of Home Assistant leaves the circuits unchanged.
