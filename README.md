# House Assistant

[English version](README.en.md)

Custom Integration für Home Assistant, die Heizung, Rollos und Zählerablesung auf einem gemeinsamen Modell des Hauses vereint. Räume und Fenster werden nur einmal erfasst, die Module bauen darauf auf und arbeiten zusammen:

* **Heizung** (bisher [AI Heating Assistant](https://github.com/Jumpmaster2/AI-Heating-Assistant)): lokale, lernende Regelung je Raum, Heiztag-Entscheidung und Parameterprüfung durch Claude, Lüftungsempfehlung mit gelerntem Feuchteprofil. Details: [docs/heating.md](docs/heating.md)
* **Rollos** (bisher [Shutter Assistant](https://github.com/Jumpmaster2/Shutter-Assistant)): Sonnenschutz nach Himmelsrichtung, Abendmodus, Lüftungsposition, Wetterschutz, Übersteuerung, Morgenöffnung, Urlaubssimulation. Details: [docs/covers.md](docs/covers.md)
* **Zähler** (bisher [Zähler-Ablesung](https://github.com/Jumpmaster2/Zaehler-Ablesung)): Zähler mit einer Kamera und einer KI ablesen, mit Mehrheitsentscheid und Plausibilitätsprüfung. Details: [docs/meters.md](docs/meters.md)

Jedes Modul lässt sich einzeln ein- und ausschalten. Keine Funktion der bisherigen Integrationen fällt weg; wer sie nutzt, zieht mit einem Skript um, ohne Verlauf und Lernwerte zu verlieren ([docs/transfer.md](docs/transfer.md)).

> Status: Version 1.0.0b1 (Beta). Bitte die ersten Wochen das Logbuch im Blick behalten.

## Zusammenspiel

* **Ein Haus:** Räume (mit Home-Assistant-Bereich und Sensoren) und Fenster (mit Raum, Größe, Kontakten, Wand und optional einem Rollo) gibt es nur einmal. Ein Kontakt und ein Rollo gehören zu genau einem Fenster.
* **Querlüften automatisch:** Aus der Lage der Fenster am Haus erkennt die Heizung Querlüften und Luftzug durch Räume, auch über Eck; jede Kombination lässt sich einzeln abschalten.
* **Kurzlüften:** Wer ein Fenster kürzer als die Fensterverzögerung, aber mindestens eine Minute offen hat, lüftet kurz; danach wartet die Heizung die halbe gelernte Erholungszeit (beides je Raum jederzeit einstellbar im Abschnitt *Lüften*). Das Logbuch zeigt es. Details: [docs/heating.md](docs/heating.md)
* **Gekippt:** Fenstergriffe und Kipp-Kontakte zählen für die Heizung mit 25 % der Öffnungsfläche, für die Rollos wie bisher.
* **Heiztag:** Der Heiztag der Heizung ist der Heizbedarf der Rollos (Sonnenwärme erwünscht) und die Bedingung der Zähler (seltener ablesen, wenn nicht geheizt wird).
* **Raumwerte:** Die Rollos nehmen Temperatur, Thermostat-Sollwert und Klimaanlage des Raums ihres Fensters.
* **Wärmezähler:** Die Heizung liest einen Zähler des Moduls Zähler mit dem echten Zeitpunkt der Ablesung; eine bestätigte Korrektur ist kein Zählertausch. Mit einer Wohnfläche je Raum verteilt sie den Verbrauch auf die Räume (siehe docs/heating.md).
* **Urlaub für das ganze Haus** (siehe unten).
* **Einstellungen des Hauses:** Außenwerte, Wetter, Sprache, Benachrichtigungen und Arbeitstage gelten für alle Module.
* **Ein Panel** mit Bereichen für Haus, Heizung, Rollos und Zähler.
* **Kein Neuladen:** Eine Änderung startet nur das betroffene Modul neu; Haltezeiten der Rollos und eine laufende Zählerablesung bleiben unberührt.

## Installation

### Über HACS

1. HACS öffnen, oben rechts im Menü **Benutzerdefinierte Repositories** wählen.
2. Repository `https://github.com/Jumpmaster2/House-Assistant`, Typ **Integration**, hinzufügen.
3. **House Assistant** herunterladen und Home Assistant neu starten.
4. **Einstellungen > Geräte & Dienste > Integration hinzufügen > House Assistant**.

### Manuell

1. Den Ordner `custom_components/house_assistant` nach `config/custom_components/` von Home Assistant kopieren.
2. Home Assistant neu starten und die Integration wie oben unter Schritt 4 hinzufügen.

Voraussetzung: Home Assistant 2026.10 oder neuer. Optional ein API-Key von Anthropic für die KI der Heizung (ohne Key läuft die lokale Regelung), eine KI-Aufgabe mit Bildunterstützung für die Zähler.

Wer die bisherigen Integrationen nutzt: House Assistant installieren, aber **nicht einrichten**, und dem [Umzug](docs/transfer.md) folgen.

## Einrichtung

1. **Module wählen:** Heizung, Rollos, Zähler (später unter *Konfigurieren > Module* änderbar).
2. **Haus:** Außentemperatur (Sensor oder Wetter-Entität, für Heizung und Rollos nötig), Außenfeuchte, Wetter, Sprache, Benachrichtigungsdienste, Werktag, Wochenendtage, Ausrichtung und Maße des Hauses, Luftzug-Reichweite.
3. **Je Modul** die ersten Einstellungen; mit der Heizung geht es danach direkt mit dem ersten Raum weiter.
4. Im Panel **House Assistant** (Seitenleiste) unter **Haus** die Räume und Fenster anlegen, dann in den Bereichen der Module ihre Einstellungen.

**Konfigurieren** bei der Integration öffnet das Panel. Das Optionsmenü gliedert sich in Module, Haus, Urlaub und je Modul seine Einstellungen; Räume, Fenster, Himmelsrichtungen und Zähler lassen sich auch als Einträge der Integration hinzufügen.

## Das Haus

Im Panel unter **Haus**:

* **Räume:** Name, Home-Assistant-Bereich (das Gerät des Raums kommt dorthin, er liefert die Etage), Temperatur- und Feuchtesensor, Klimaanlage. Mit Temperatursensor bekommt ein Raum Heizung und Lüftungsempfehlung, mit Heizkreis auch ein Thermostat (Bereich Heizung). Der Raum-Editor zeigt den Plan des Hauses mit den Querlüft- und Luftzug-Kombinationen des Raums, jede mit eigenem Schalter.
* **Fenster:** Name, Raum, Größe (klein, mittel, groß, Tür), Fensterkontakte (auch Fenstergriffe), Kipp-Kontakte, Himmelsrichtung, Wand und Position an der Wand, Rollo. Mindestens ein Kontakt oder ein Rollo. Mit Rollo stehen die weiteren Einstellungen im Bereich Rollos.
* **Urlaub:** Schalter, Abreise und Rückkehr, Quellen und Meldungen (siehe unten).
* **Allgemein:** die Einstellungen des Hauses, die Module und ob das Panel in der Seitenleiste steht.

### Einstellungen des Hauses

| Option | Bedeutung |
|---|---|
| Außentemperatur, Außenfeuchte, Wetter | für Heizung und Rollos; ohne Außensensor gilt die aktuelle Temperatur der Wetter-Entität |
| Sprache der Meldungen | Logbuch, letzter Grund, Benachrichtigungen aller Module; Automatisch = die Sprache von Home Assistant |
| Benachrichtigungsdienste | nur `notify.*`; Meldungen der Rollos und des Urlaubs |
| Werktag-Sensor, Wochenendtage | Morgenöffnung der Rollos |
| Vorderseite zeigt nach, Länge, Tiefe | Haus im Sonnenkompass der Rollos; mit Länge und Tiefe erkennt die Heizung Luftzug durch Räume |
| Luftzug-Reichweite | wie weit ein Raum von der Linie zwischen zwei offenen Fenstern anderer Räume entfernt sein darf (Standard 2 m) |

Ein hier eingetragener Wert gilt für alle Module. Ohne Wert gilt der in den Einstellungen des Moduls (die bisherigen Integrationen hatten die Werte jede für sich).

## Urlaub

Ein Urlaub für alle Module, ohne eigene Helfer:

* **Schalter Urlaub** am Gerät „House Assistant“, bleibt über Neustarts erhalten. **Abreise** und **Rückkehr** (`datetime`-Entitäten, beide optional): Zur Abreise schaltet sich der Urlaub ein, zur Rückkehr aus, danach sind beide wieder leer. Ist nur die Rückkehr gesetzt, gilt der Urlaub ab sofort. Eine Abreise nach der Rückkehr wird abgelehnt, eine Rückkehr in der Vergangenheit ignoriert. Einstellbar auch im Panel unter *Haus > Urlaub* und mit dem Dienst `house_assistant.set_vacation`.
* **Externe Quellen** zählen weiterhin: Urlaubs-Entitäten (`input_boolean`, `binary_sensor`, `switch`, `calendar`, `schedule`; an = Urlaub) und eine Rückkehr-Entität. Sie werden nur im Haus eingestellt (Einstellungen > Haus > Urlaub oder im Panel); Heizung und Rollos haben keine eigenen Quellen mehr, und die Optionen *Lüftungsempfehlung ruht* und *Hitzeschutz im Urlaub* stehen ebenfalls dort.
* **Binärsensor Urlaub aktiv** mit Quelle, Beginn, Abreise, Rückkehr, Beginn des Vorheizens, Anwesenheitssimulation, Leckwarnung und nicht geschlossenen Fenstern. Ereignis `house_assistant_vacation` (`active`, `source`) und Logbuch-Eintrag bei Beginn und Ende. Das Panel zeigt im Urlaub ein Banner.

Wirkung:

| Modul | im Urlaub |
|---|---|
| Heizung | Urlaubstemperatur für alle Räume, Vorheizen auf die Rückkehr (die eigene Rückkehr hat Vorrang); die Lüftungsempfehlung ruht (Zustand „Urlaub“, keine Statistik, kein Feuchteprofil; Option) |
| Rollos | Urlaubssimulation morgens und abends; Hitzeschutz: der Sonnenschutz senkt ab, ohne auf Raum, Klimaanlage oder Heizbedarf zu warten, nur an Sommertagen (Option) |
| Haus | Meldung der offenen, gekippten oder unbekannten Fenster zu Beginn und sofort, wenn im Urlaub ein Fenster geöffnet oder gekippt wird (Option) |
| Zähler | Leckwarnung nach Menge und mittlerem Durchfluss bzw. Leistung seit Urlaubsbeginn, einmal je Urlaub und Fall; beim Wasser standardmäßig an (20 L, 5 L/h), nie beim Wärmezähler |

Meldungen gehen an die Benachrichtigungsdienste des Hauses, ohne sie als Benachrichtigung in Home Assistant.

## Dashboard-Karten

Die Karten werden für alle Benutzer und alle Dashboards automatisch geladen, ohne Eintrag von Hand: als Zusatzmodul des Frontends, sobald die Integration startet (auch in einer schon offenen Seite oder der Companion-App), und zusätzlich als Dashboard-Ressource unter eigener Adresse. Alle Dateien liegen unter einem Ordner mit der Version, nach einem Update mischt keine Seite alte und neue Dateien.

| Karte | Modul |
|---|---|
| `custom:house-assistant-thermostat-card` | Heizung: Thermostat mit Luftfeuchte |
| `custom:house-assistant-thermostat-compact-card` | Heizung: Thermostat kompakt |
| `custom:house-assistant-climate-tile-card` | Heizung: Raumklima-Kachel |
| `custom:house-assistant-cover-card` | Rollos: alle Fenster mit Status, Knöpfen und Sonnenkompass |
| `custom:house-assistant-tile` | Rollos: Kachel für ein Rollo oder einen Fensterkontakt |
| `custom:house-assistant-window-tile` | Rollos: Fensterkachel mit Fenster und Rollo |

Beispiele und Optionen stehen in [docs/heating.md](docs/heating.md#dashboard-karten) und [docs/covers.md](docs/covers.md#dashboard-karten).

## Dienste und Ereignisse

| Dienst | Zweck |
|---|---|
| `house_assistant.set_vacation` | Urlaub planen: `departure`, `return`, `clear` |
| `house_assistant.export_parameters`, `import_parameters`, `reset_learned` | Lernwerte der Heizung |
| `house_assistant.run_ai_check`, `run_ai_ventilation_check`, `decide_heating_day` | KI-Prüfungen und Heiztag-Entscheidung jetzt |
| `house_assistant.move_cover`, `start_cover_override`, `end_cover_override`, `resume_cover` | Rollos |
| `house_assistant.read_meter`, `set_meter_reading` | Zähler |

Ereignisse: `house_assistant_vacation`, `house_assistant_vacation_alert`, `house_assistant_cover_moved`, `house_assistant_cover_failed`, `house_assistant_protection`, `house_assistant_meter_reading` und ein gemeinsames Logbuch-Ereignis `house_assistant_logbook`.

## Fehlerbehebung

* **Diagnose:** Einstellungen > Geräte & Dienste > House Assistant > ⋮ > Diagnose herunterladen (API-Key und Benachrichtigungsdienste sind geschwärzt).
* **Debug-Protokoll:** bei der Integration ⋮ > *Debug-Protokollierung aktivieren*, oder in `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.house_assistant: debug
    anthropic: debug
```

* Weitere Hinweise je Modul in [docs/heating.md](docs/heating.md#fehlerbehebung), [docs/covers.md](docs/covers.md#fehlerbehebung).

## Entfernen

Einstellungen > Geräte & Dienste > House Assistant > ⋮ > **Löschen**. Die Heizung schaltet vorher alle eingeschalteten Heizkreise aus. Gespeicherte Daten (`.storage/house_assistant.<Eintrag>.*`), Panel, Karten und Reparaturhinweise werden entfernt; die Bilder der Zähler bleiben im Medienordner (`media/house_assistant`). Danach den Ordner bzw. den HACS-Download entfernen.

## Entwicklung

```bash
pip install -r requirements_test.txt ruff
ruff check custom_components tests scripts
ruff format --check custom_components tests scripts
python scripts/build_labels.py --check
pytest
```

Die Texte des Panels (`frontend/labels.js`) und der Karten (`frontend/card-labels.js`) werden aus den Übersetzungsdateien erzeugt. Nach einer Änderung an `translations/*.json` einmal `python scripts/build_labels.py` ausführen (ein Test prüft das). Die reine Logik in `*/logic/` hat keine Abhängigkeit zu Home Assistant und ist einzeln testbar. Vor dem Veröffentlichen prüft `python scripts/check_privacy.py --patterns <Datei>` auf private Daten. Der Plan des Umbaus steht in [docs/PLAN.md](docs/PLAN.md).

## Lizenz

MIT, siehe [LICENSE](LICENSE).
