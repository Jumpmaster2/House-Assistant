# Meters

[Deutsch](meters.md) | English

The **meters** module (formerly Zähler-Ablesung) reads meters (heat, water, gas, electricity) with a camera. A cheap ESP32-CAM with ESPHome photographs the display, an AI task of Home Assistant (`ai_task`, e.g. Anthropic Claude, OpenAI, Google or a local model with image support) reads the value. A majority vote over several pictures and a plausibility check keep misreadings out of the statistics.

Everything is set up in the panel **House Assistant**, section **Meters**: add a meter, choose camera and light, try the brightness with a test picture, set the interval and the checks. No automations, scripts or helpers are needed.

## How it works

### Taking a picture

1. The light (e.g. the flash LED of the ESP32-CAM) is switched on with the configured brightness, once for all pictures of a reading.
2. After the warm-up some pictures are discarded. After a pause the ESP32-CAM otherwise still delivers an old picture without light from its buffer.
3. The pictures are taken, then the light goes off. If it was on before (e.g. for the live picture), it stays on.
4. Optionally the picture is rotated by any angle (up to ±180°), cropped to the **picture section** and adjusted in **exposure**. That matters with wide-angle cameras on which the display is otherwise only a small strip. In the panel you straighten the last picture and drag the section over it with mouse or finger. With **enhance picture** the picture also becomes grey, evenly lit and higher in contrast, which helps with a bright light spot on the display glass or faint LCD digits. While setting up the camera the **live picture** there helps (with the light on if wanted) without taking a test picture each time.
5. The picture the AI gets is stored as `/media/house_assistant/<meter id>/letztes.jpg` (the uncropped one as `original.jpg`) and is visible as the camera entity **Last picture**.

### External light

If the light of the camera is not enough or reflects, an **external light** can be switched on per meter in addition, e.g. LED modules. Any `light` or `switch` entity works; the section is in the meter editor under **External light**. Without an entity everything behaves as before.

| Option | Key | Default | Meaning |
| --- | --- | --- | --- |
| External light | `external_light` | empty | `light` or `switch` entity; empty = no external light |
| Mode | `external_light_mode` | only while taking pictures (`capture`) | `capture`: on before the pictures, off afterwards. Permanent (`permanent`): only switched on when it is off, never switched off |
| Brightness | `external_light_brightness` | 100 % | only for a dimmable `light` entity; a switch is only switched on and off |
| Lead time | `external_light_lead_time` | 2 s | waiting time (0 to 30 s) after switching on before the light of the camera goes on and pictures are taken |
| Switch off afterwards | `external_light_turn_off` | yes | only in the mode "only while taking pictures" |

A reading or test picture in the mode "only while taking pictures": external light on (a `light` with the configured brightness), wait the lead time, then as above the light of the camera, pictures and reading by the AI, then external light off. Switching off also happens when taking or reading fails. If the entity is unavailable or switching fails, a warning is logged and the meter is read anyway.

### Reading with a majority vote

* The AI gets the picture and an instruction made of meter type, unit, decimals and your **hints** (visible in the editor under "Instruction to the AI"). It answers only with the number or with "unreadable".
* With **Edit** the whole instruction can be changed freely; the generated one serves as a template. An own instruction then replaces the generated one completely; unit, decimals and hints are no longer inserted. **Restore default** returns to the generated instruction.
* Pictures are read until a value was read **twice the same**, at most the configured number of pictures (default 4). Without such a value the reading is "unreadable".
* The very first value of a meter is also confirmed by further pictures (default 2), as there is nothing to compare it with yet.
* With **Brightness of 2nd picture** (0 = off) a second picture with another light brightness is taken per attempt (`letztes_2.jpg`), and the AI gets both.
* With **Last readings to the AI** the AI gets the last 3 valid readings as a hint to decide an unclear digit plausibly. It should still only read what is in the picture; majority vote and plausibility check stay unchanged. A reading set by hand replaces the earlier ones.
* If the answer of the AI contains besides the number only a unit or a label ("1234.5 m³", "Reading: 1234.5"), the number counts.

### Plausibility check

* **Rise too large:** if the value rose since the last valid reading by more than *largest rise per hour × hours* (at least half an hour, without a previous value two hours), it is rejected.
* **Smaller than before:** a smaller value is only taken if it is smaller by at most the *largest correction* and further pictures (default 2) all confirm it. It then counts as "corrected" (an earlier misreading is fixed). The heating does not take such a correction for a meter change.
* In the panel a rejected but correctly read value can be taken with one click. The picture is kept below `verworfen/` (the last 20) and visible in the panel on the meter card under **Rejected pictures**.
* The reading sensor has the state class `total` (not `total_increasing`), so a correction downwards does not count as a meter change in the statistics.

### Notifications

Rejected, corrected and failed readings can create a notification in Home Assistant. Per meter the section **Notifications** sets from the how-many-th time in a row it appears (0 = never, 1 = at once):

| Case | Default |
| --- | --- |
| Smaller than before | 1 |
| Rise too large | 1 |
| Corrected | 1 |
| Unreadable or error (camera/AI unavailable) | 3 |

* A valid reading resets the count and removes the notification.
* Another case starts the count anew (e.g. "rise too large" after "smaller than before" twice). Unreadable readings show no value and do not interrupt the count of the other cases; they are counted on their own.
* The switch in the settings of the meters switches all of these notifications off.

### Leak warning on vacation

During the vacation of the house (see [README](../README.en.md#vacation)) a meter warns when something runs while nobody is at home. Section **Vacation** in the meter editor:

| Option | Default | Meaning |
| --- | --- | --- |
| Warn on vacation | on for a water meter, else off | |
| Amount | water 20 L, else 0 | used since the vacation started, in litres (water, gas) or kWh (electricity); 0 = off |
| Mean flow or power | water 5 L/h, else 0 | mean since the vacation started in L/h or kW, after an hour at the earliest; for gas and electricity enter the base load; 0 = off |

Counted from the last valid reading before the vacation. When a value exceeds its limit there is a message to the notification services of the house (without any a notification in Home Assistant), a logbook entry, the event `house_assistant_vacation_alert` (with `meter_id`, `meter`, `case`, `used`, `hours`, `limit`, `unit`) and the attribute `vacation_alerts` on the reading, once per vacation and case. The heat meter is excluded.

### Schedule

* Every meter is read automatically at the configured **interval** (checked every 5 minutes). After an unreadable or failed reading the next attempt comes after 15 minutes.
* Optionally a **condition**: while this entity is `off`, a second interval applies. With the option **days without heating** the second interval also applies on days the heating module does not heat (unknown counts as a heating day). Example: every 30 minutes on heating days, otherwise every 6 hours.
* The **heat meter** of the heating and meters with **days without heating**: with the heating module **Interval while a room heats** (15 minutes, until 30 minutes after the heating ends) and **Interval otherwise** (once a day) apply instead. Switching the heating on and off asks for a reading, at least 5 minutes after the last one.
* The switch **Automatic** stops the automatic readings; the button **Read now** reads at once.

## Entities per meter

| Entity | Meaning |
| --- | --- |
| Meter reading | last valid value (energy, water or gas, suitable for the energy dashboard). Attributes `last_valid_reading` and on vacation `vacation_alerts`. |
| Mean power / Mean flow | consumption since the previous valid reading (kW for energy, L/h for volume). Reset by a correction. |
| Status | result of the last reading: valid, corrected, unreadable, smaller than before, rise too large, camera or AI error, set by hand. Attribute `readings` with every single reading. |
| Last reading / Next reading | times (diagnostic). |
| Last picture | camera entity with the last picture taken. |
| Read now / Test picture | buttons. The test picture is only taken, not read (to try alignment, focus and brightness). |
| Automatic | automatic readings on or off. |

## Services and events

* `house_assistant.read_meter`: read the meters of the given entities now.
* `house_assistant.set_meter_reading`: set the reading by hand (e.g. after a misreading or at the start). The next readings are checked against this value. Also in the panel under "Set reading by hand".
* Event `house_assistant_meter_reading` after every reading with `meter_id`, `meter`, `valid`, `status`, `value`, `previous`, `readings`, `unit`.

## Setting up

1. Switch the **meters** module on (at setup or under *Settings > Modules*) and choose the AI task.
2. In the panel under **Meters** add a meter: name, meter type, camera, light. Save, then check alignment and brightness with **Test picture**.
3. **Read now** once and check the result. If something is wrong, describe in the **hints** what the AI misreads (e.g. "The line above the digits is the frame, not a segment").

Requirements: an AI task entity with image support (attachments), a camera entity.

### Camera: ESP32-CAM with ESPHome

An example is in [esphome-esp32-cam.yaml](esphome-esp32-cam.yaml). Experience from operation:

* **Camera clock 8 MHz** instead of 20 MHz. The higher clock disturbs the WiFi antenna of the ESP32-CAM; pictures then take more than 10 seconds or break off, OTA updates hang.
* **Two frame buffers** and no permanent streaming (`idle_framerate: 0 fps`). The module discards the first pictures after the light is switched on.
* **Flash LED** with `ledc` on channel 2 (the camera uses the timer of channels 0 and 1) and with limited power, otherwise the display reflects. Usually 10 to 60 % is enough.
* For LCD displays choose the angle so the LED does not reflect directly.

### Costs

One AI request per picture, usually 2 pictures per reading. With a small model (e.g. Claude Haiku) and 1024×768 pixels that is a fraction of a cent per reading. The interval decides the costs: every 30 minutes is about 100 pictures a day.

## Privacy

The pictures go to the provider of the chosen AI task. They show only the meter display if the camera is aligned accordingly.
