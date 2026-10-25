# Umzug von den bisherigen Integrationen / Moving from the former integrations

[Deutsch](#deutsch) | [English](#english)

## Deutsch

Wer AI Heating Assistant, Shutter Assistant oder Zähler-Ablesung nutzt, zieht mit dem Skript `scripts/transfer_legacy.py` einmalig auf House Assistant um. Danach läuft alles **genau wie vorher**:

* gleiche Entitäts-IDs, also lückenloser Verlauf und Energie-Dashboard;
* gleiche Geräte mit Namen, Bereichen und Labels;
* alle gelernten Daten: Lernmodelle, Heiztag-Verlauf, KI-Verlauf und Budget, Wärmezähler, Übersteuerungen und Tagesmarker der Rollos, Zählerstände und Bilder.

Das Skript braucht nur Python 3.11 oder neuer, kein Home Assistant. Es schreibt in die Speicherdateien von Home Assistant, deshalb nur bei **gestopptem** Home Assistant und mit Sicherung.

### Was übernommen wird

* **Räume** entstehen aus den Heizbereichen (gleiche IDs, ihr Home-Assistant-Bereich kommt vom Gerät des Heizbereichs).
* **Fenster:** Steht ein Kontakt eines Heizbereichs auch in einem Fenster von Shutter Assistant, wird daraus ein gemeinsames Fenster mit der Größe aus der Heizung und dem Raum des Heizbereichs. Der Raum eines Rollo-Fensters folgt sonst aus seiner Raumtemperatur-Entität, wenn sie das Thermostat eines Heizbereichs ist. Jeder übrige Kontakt der Heizung wird ein Fenster ohne Rollo, benannt nach dem Kontakt.
* **Himmelsrichtungen** und **Zähler** mit ihren IDs.
* **Einstellungen:** je Modul unverändert (die Migrationen von AI Heating Assistant werden angewendet). Einstellungen, die die Module teilen (Außentemperatur, Wetter, Benachrichtigungen, Werktag, Hausmaße, Urlaub), kommen ins Haus, wenn sie nur in einem Modul stehen oder in beiden gleich sind. Die Sprache bleibt bei den Rollos (die Heizung nutzte die Sprache von Home Assistant). Der Heizbedarf der Rollos bleibt, wie er war (Option „Heiztag der Heizung“ aus).
* **Entitäten und Geräte** wechseln zum neuen Eintrag; die Entitäts-IDs bleiben.
* **Speicher** `.storage/<alte Integration>.<Eintrag>` wird zu `.storage/house_assistant.<Eintrag>.<Modul>`; die alten Dateien bleiben als `.bak`.
* **Bilder** der Zähler wandern von `media/zaehler_ablesung/<ID>` nach `media/house_assistant/<ID>`.
* **Dashboards** (im UI verwaltet): die Kartentypen werden ersetzt (z. B. `custom:shutter-assistant-card` durch `custom:house-assistant-cover-card`), die alten Dashboard-Ressourcen entfernt.
* **Automationen und Skripte** (`automations.yaml`, `scripts.yaml`): Dienste und Ereignisse werden umbenannt (z. B. `shutter_assistant.move` zu `house_assistant.move_cover`, `zaehler_ablesung_reading` zu `house_assistant_meter_reading`). Was sich nicht eindeutig umschreiben lässt, nennt der Bericht.

### Ablauf

1. **Sicherung:** ein vollständiges Backup von Home Assistant. Das Skript kopiert zusätzlich jede Datei, die es ändert, nach `<config>/house_assistant_transfer_backup/<Zeit>/`.
2. **House Assistant installieren** (HACS, siehe [README](../README.md#installation)) und Home Assistant neu starten, aber House Assistant **nicht einrichten**. Die alten Integrationen bleiben vorerst.
3. **Skript holen**, z. B. im Terminal-Add-on (SSH) von Home Assistant OS:

   ```bash
   cd /tmp
   wget -O house-assistant.zip https://github.com/Jumpmaster2/House-Assistant/archive/refs/heads/main.zip
   unzip -o house-assistant.zip
   cd House-Assistant-main
   ```

4. **Probelauf** (ändert nichts):

   ```bash
   python3 scripts/transfer_legacy.py --config /config --media /media --dry-run
   ```

   `--media` ist der Medienordner von Home Assistant; unter Home Assistant OS ist das `/media`, ohne Angabe gilt `<config>/media`. Im Bericht muss bei den Bildern der Zähler „found“ stehen, sonst stimmt der Ordner nicht.

   Er schreibt `transfer-plan.json` und `transfer-report.md`. Im Bericht stehen Räume, Fenster, Entitäten, Speicher, Bilder, Dashboards, Automationen und offene Punkte, z. B. ein Rollo-Fenster ohne Raum oder eine Einstellung, die in den Modulen verschieden war. Offene Punkte lassen sich in `transfer-plan.json` entscheiden (z. B. `"room"` eines Fensters eintragen) oder später im Panel.
5. **Home Assistant stoppen** und umziehen:

   ```bash
   ha core stop
   python3 scripts/transfer_legacy.py --config /config --media /media --apply transfer-plan.json --stopped
   ha core start
   ```

   (Ohne Home Assistant OS: den Container bzw. Dienst stoppen und den Pfad zum `config`-Ordner angeben.)
6. **Prüfen:** gleiche Entitäts-IDs, Verlauf und Energie-Dashboard lückenlos, Lernwerte im Panel wie vorher, Rollos ohne ungewollte Fahrt (Neustart-Schutz), Zähler ohne Neubeginn, Logbuch. Danach im Panel unter *Haus > Fenster* Wand und Position der Fenster ohne Rollo ergänzen (für Querlüften) und die alten drei Integrationen in HACS entfernen.
7. **Zurück:** das Backup zurückspielen (oder die Dateien aus `house_assistant_transfer_backup` zurückkopieren und die `.bak`-Dateien umbenennen).

Das Skript prüft das Speicherformat (geprüft mit Home Assistant 2026.10) und bricht bei einem anderen ab; `--force` geht trotzdem weiter. Läuft der Umzug ein zweites Mal, bricht er ab, weil House Assistant schon eingerichtet ist.

Externe Urlaubs-Entitäten und eine Rückkehr-Entität bleiben Quellen des Urlaubs, bestehende Automationen auf diese Helfer laufen weiter. Auf Wunsch stellst du danach auf den eigenen Schalter *Urlaub* mit Abreise und Rückkehr um.

## English

Users of AI Heating Assistant, Shutter Assistant or Zähler-Ablesung move to House Assistant once with the script `scripts/transfer_legacy.py`. Afterwards everything runs **exactly as before**:

* the same entity ids, so the history and the energy dashboard go on without a gap;
* the same devices with names, areas and labels;
* all learned data: learning models, heating day history, AI history and budget, heat meter, overrides and daily markers of the covers, meter readings and pictures.

The script needs only Python 3.11 or newer, not Home Assistant. It writes the storage files of Home Assistant, so only with Home Assistant **stopped** and with a backup.

### What is transferred

* **Rooms** from the heating areas (same ids; their Home Assistant area from the device of the area).
* **Windows:** if a contact of a heating area is also in a window of Shutter Assistant, they become one window with the size from the heating and the room of the area. Otherwise the room of a cover window follows from its room temperature entity being the thermostat of an area. Every other heating contact becomes a window without a cover, named after the contact.
* **Directions** and **meters** with their ids.
* **Settings:** per module unchanged (the migrations of AI Heating Assistant are applied). Settings the modules share (outdoor temperature, weather, notifications, workday, size of the house, vacation) go to the house when only one module has them or both have the same. The language stays with the covers (the heating used the language of Home Assistant). The heat need of the covers stays as it was (option "heating day of the heating" off).
* **Entities and devices** move to the new entry; the entity ids stay.
* **Storage** `.storage/<former integration>.<entry>` becomes `.storage/house_assistant.<entry>.<module>`; the old files stay as `.bak`.
* **Pictures** of the meters move from `media/zaehler_ablesung/<id>` to `media/house_assistant/<id>`.
* **Dashboards** (managed in the UI): the card types are replaced (e.g. `custom:shutter-assistant-card` by `custom:house-assistant-cover-card`), the old dashboard resources removed.
* **Automations and scripts** (`automations.yaml`, `scripts.yaml`): services and events are renamed (e.g. `shutter_assistant.move` to `house_assistant.move_cover`, `zaehler_ablesung_reading` to `house_assistant_meter_reading`). What cannot be rewritten for sure is named in the report.

### Steps

1. **Backup:** a full backup of Home Assistant. The script also copies every file it changes to `<config>/house_assistant_transfer_backup/<time>/`.
2. **Install House Assistant** (HACS, see [README](../README.en.md#installation)) and restart Home Assistant, but **do not set it up**. The former integrations stay for now.
3. **Get the script**, e.g. in the terminal add-on (SSH) of Home Assistant OS:

   ```bash
   cd /tmp
   wget -O house-assistant.zip https://github.com/Jumpmaster2/House-Assistant/archive/refs/heads/main.zip
   unzip -o house-assistant.zip
   cd House-Assistant-main
   ```

4. **Dry run** (changes nothing):

   ```bash
   python3 scripts/transfer_legacy.py --config /config --media /media --dry-run
   ```

   `--media` is the media folder of Home Assistant; on Home Assistant OS that is `/media`, without it `<config>/media` applies. In the report the pictures of the meters must say "found", otherwise the folder is wrong.

   It writes `transfer-plan.json` and `transfer-report.md`. The report lists rooms, windows, entities, storage, pictures, dashboards, automations and open points, e.g. a cover window without a room or a setting that differed between the modules. Open points can be decided in `transfer-plan.json` (e.g. enter the `"room"` of a window) or later in the panel.
5. **Stop Home Assistant** and transfer:

   ```bash
   ha core stop
   python3 scripts/transfer_legacy.py --config /config --media /media --apply transfer-plan.json --stopped
   ha core start
   ```

   (Without Home Assistant OS: stop the container or service and give the path of the `config` folder.)
6. **Check:** the same entity ids, history and energy dashboard without a gap, learned values in the panel as before, covers without unwanted movements (restart protection), meters without a new start, logbook. Then add wall and position of the windows without a cover in the panel under *House > Windows* (for cross ventilation) and remove the three former integrations in HACS.
7. **Back:** restore the backup (or copy the files from `house_assistant_transfer_backup` back and rename the `.bak` files).

The script checks the storage format (checked with Home Assistant 2026.10) and stops for another one; `--force` goes on anyway. A second run stops because House Assistant is already set up.

External vacation entities and a return entity stay sources of the vacation; existing automations on these helpers keep working. If you like, switch to the own switch *Vacation* with departure and return afterwards.
