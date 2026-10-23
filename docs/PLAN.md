# Plan: House Assistant – Heizung, Rollos und Zähler in einer Integration

## 1. Kontext

Heute gibt es drei getrennte Integrationen desselben Autors, gleich aufgebaut (ein Eintrag, Subentries, Store, Seitenleisten-Panel, `labels.js` aus Übersetzungen, reine Logik in `logic/`):

| | AI Heating Assistant 1.7.0 | Shutter Assistant 0.9.0 | Zähler-Ablesung 0.8.0 |
|---|---|---|---|
| Kern | `coordinator.py` (2950 Z.), 60-s-Takt | `engine.py` (2349 Z.), ereignisgesteuert | `meter.py` (780 Z.), 5-min-Takt |
| Subentries | `heating_area` | `group`, `window` | `meter` |
| Tests | 294 | 213 | 61 |

Probleme: Fenster werden doppelt erfasst (Heizung: Kontakte je Größe im Heizbereich; Rollos: Fenster mit Rollo und Kontakten). Gleiche Einstellungen werden mehrfach gepflegt (Außentemperatur, Wetter, Urlaub). Die Integrationen hängen über Entitäten voneinander ab (Heiztag → Rollo-„Heizbedarf“ und Zähler-„Bedingung“, Wärmezähler-Sensor → Heizung, Thermostat → Rollo-Raumtemperatur). Querlüften muss heute von Hand als Kombination eingetragen werden, obwohl die Rollos die Lage der Fenster am Haus schon kennen.

**Ziel:** eine Integration **House Assistant** (`house_assistant`, Repo `Jumpmaster2/House-Assistant`). Haus, Räume und Fenster werden einmal erfasst. Heizung, Rollos und Zähler bauen darauf auf und sind intern verknüpft. **Keine Funktion fällt weg**; die Checkliste in Abschnitt 17 ist der Nachweis.

## 2. Getroffene Entscheidungen

* Name **House Assistant**, Domain `house_assistant`, neues Repo.
* **Ein** Seitenleisten-Eintrag mit Bereichen; Heizung, Rollos und Zähler lassen sich zusätzlich einzeln in die Seitenleiste legen.
* Kein Import-Assistent in der Integration. Claude Code richtet die neue Integration nach der Umsetzung **genau wie die jetzige Installation** ein, **einschließlich aller gelernten Daten**. Dafür gibt es ein einmaliges Umzugs-Skript (Abschnitt 12): Home Assistant wird gestoppt, Entitäts- und Geräte-IDs bleiben gleich, also laufen Verlauf und Energie-Dashboard weiter. Alte Dienst- und Kartennamen bekommen keine Aliase; das Skript schreibt Automationen und Dashboards um.
* **Gekippt** zählt für die Heizung wie offen, aber nur mit **25 % der Öffnungsfläche**.
* **Querlüften und Luftzug** werden **automatisch** aus der Anordnung der Fenster abgeleitet: gegenüberliegende Wände **und** Wände über Eck. Jede Kombination lässt sich einzeln abschalten.
* **Urlaubsmodus für das ganze Haus** mit eigenem Schalter, Abreise und Rückkehr; externe Quellen wie ein Kalender bleiben möglich. Dazu kommen Hitzeschutz der Rollos, eine ruhende Lüftungsempfehlung, die Meldung offener Fenster und eine Leckwarnung der Zähler (Abschnitt 7a).
* Zusätzliche Schritte nach dem Umbau: **Rollos im Wärmemodell**, **heizungsgeführte Ablesung des Wärmezählers** (nur wenn geheizt wurde, beim Heizen alle 15 min, frisch vor KI-Prüfung und Mitternacht), **Zähler über Claude-Key**.

## 3. Zielbild

```
                      ┌──────────────────── Haus (Kern) ─────────────────────┐
                      │ Räume · Fenster · Himmelsrichtungen · Hausplan       │
                      │ Außenwerte · Wetter/Vorhersage · Urlaub · Werktag    │
                      │ Sprache · Benachrichtigungen · Sonne · KI-Client     │
                      │ Logbuch · Reparaturen · Speicher · Panel-Grundgerüst │
                      └───────▲───────────────▲────────────────▲────────────┘
                              │               │                │
          Heiztag, Thermostat │               │ Rollo-Stellung │
          ┌───────────────────┴──┐   ┌────────┴───────────┐  ┌─┴──────────────┐
          │ Heizung (+ Lüftung)  │◄──┤ Rollos             │  │ Zähler         │
          │ Regelung, Lernen, KI │──►│ Sonne, Abend, Wetter│  │ Kamera + KI    │
          └──────────▲───────────┘   └────────────────────┘  └──▲─────────┬───┘
                     │ Wärmezähler (Wert + Zeitpunkt)            │         │
                     └───────────────────────────────────────────┼─────────┘
                                    Heiztag → Intervall, Ablesung anfordern
```

Module dürfen sich nur über klar definierte Schnittstellen in `core/links.py` ansprechen (`HeatingLink`, `ShutterLink`, `MeterLink`). Ist ein Modul aus, gilt die bisherige Entitäts-Option oder der bisherige Standard.

## 4. Gemeinsames Hausmodell (einmal erfasst)

Alle Objekte sind Subentries des einen Eintrags. Beim Umzug werden die bisherigen Subentry-IDs **weiterverwendet**, damit Stores, `unique_id`s, Mediaordner und Karten-Verweise gleich bleiben.

**Raum** (`room`, entsteht aus dem Heizbereich, ID bleibt)
* Name (eindeutig, Export/Import findet Räume über den Namen), **HA-Bereich** (optional; liefert die **Etage** aus der Etagenverwaltung von Home Assistant, und das Gerät des Raums kommt in diesen Bereich).
* Temperatur- und Feuchtesensor.
* Abschnitt **Heizung**: alles aus dem bisherigen Heizbereich (Schalter, Soll/min/max, Mindestlaufzeiten, Heizungsart, Startwerte bzw. gelernte Werte).
* Abschnitt **Lüftung**: Feuchte-Schwelle, Referenz-Temperatur/-Feuchte, Lüftungs-Sperr-Entität.
* Abschnitt **Luftzug**: die bis zu 4 Kombinationen von Hand (jetzt aus Fenstern statt Kontakten) und die Liste der abgeschalteten automatischen Kombinationen.
* Abschnitt **Sonnenschutz** (Vorgaben für die Fenster des Raums): Raumtemperatur-Quelle (Standard: das Thermostat des Raums, sonst sein Temperatursensor) und Klimaanlage. Ein Fenster kann beides abweichend setzen; bisherige Werte bleiben so erhalten.
* Heizung und Lüftung gelten nur für Räume mit Temperatursensor. Räume nur für Rollos bekommen keine Heiz- oder Lüftungsentitäten. Ein Heizkreis-Schalter verlangt einen Temperatursensor.

**Fenster** (`window`; bei Rollo-Fenstern bleibt die ID)
* Name, Raum (optional), **Größe** (klein 0,5 / mittel 1 / groß 1,6 / Tür 2,5).
* Fensterkontakte (binär, `input_boolean` oder Fenstergriff open/tilted/closed) und Kipp-Kontakte.
* Wand und Position an der Wand, Himmelsrichtung (Gruppe).
* **Rollo optional**. Mit Rollo erscheinen alle bisherigen Rollo-Einstellungen des Fensters unverändert (Sonnenschutz, manueller Sonnenschutz, Abend, Übersteuerung, Lüften & Urlaub, Morgenöffnung, Zusatzbedingungen, Wetterschutz & Tür).
* Es muss mindestens ein Kontakt oder ein Rollo gesetzt sein. Ein Kontakt darf nur zu einem Fenster gehören (neuer Fehler `contact_in_use`), ein Rollo nur zu einem (wie bisher `cover_in_use`).
* Für jeden Kontakt gilt die Größe des Fensters. Zwei offene Flügel ergeben also wie bisher die doppelte Fläche.

**Himmelsrichtung** (`group`, wie bisher): Azimut von/bis, Sonnensensoren (PV, Lux, Strahlung), Wand.

**Zähler** (`meter`, wie bisher, ID bleibt).

**Hausplan** (Haus-Einstellungen): Ausrichtung, Länge und Tiefe aus Shutter Assistant, neu dazu die **Luftzug-Reichweite** (Standard 2 m).

## 5. Gemeinsamer Fensterzustand

Eine reine Funktion in `core/logic/contacts.py` liefert je Fenster `open`, `tilted`, `closed` oder `unknown`. Sie übernimmt `contact()` und `window_contact()` aus `shutter_assistant/logic/conditions.py`. Jedes Modul behält seine bisherige Auslegung:

* **Heizung:** Öffnungsfläche = Summe über die Kontakte von Größe × Faktor (offen 1,0, gekippt 0,25, zu oder unbekannt 0). Bisher hieß nur `on` offen, unbekannt also zu; daran ändert sich nichts. Neu ist, dass Fenstergriffe und „gekippt“ erkannt werden. Grundlage sind `own_windows()` und `open_area()` aus `logic/windows.py`.
* **Rollos:** unverändert. Unbekannt zählt als offen bzw. gekippt, `reported_open` nur bei echtem offen, die Entprellung `window_closed_delay` bleibt.

## 6. Querlüften und Luftzug automatisch

Datei `core/logic/geometry.py` (rein, getestet). Begriffe:

* **Wand eines Fensters:** die eigene Wand, sonst die Wand seiner Himmelsrichtung. Ohne Wand nimmt das Fenster nicht teil, und das Panel zeigt den Hinweis „Wand fehlt“.
* **Lage zweier Wände:** gleich, gegenüber (vorn ↔ hinten, links ↔ rechts) oder über Eck (die übrigen Paare). Gegenüber und über Eck zählen beide.
* **Etage:** kommt aus dem HA-Bereich des Raums. Gibt es in Home Assistant keine Etagen, liegen alle Räume auf einer Etage. Räume ohne zuordenbare Etage nehmen nicht teil und bekommen einen Hinweis.

Zwei Regeln, jede Kombination einzeln abschaltbar:

1. **Querlüften eines Raums R:** ein eigenes Fenster *a* ist offen, zusammen mit einem Fenster *b* eines anderen Raums derselben Etage, und die Wand von *b* liegt gegenüber oder über Eck zur Wand von *a*. Wirkung wie heute bei `cross = eigenes Fenster offen und Luftzug`: Statistik `cross_min`, eigener Luftaustausch `rate_cross` in `humidity_learning.py`, Lüftungsart „cross“ für Erholung und KI.
2. **Luftzug durch R ohne eigenes Fenster:** zwei Fenster *b* und *c* anderer Räume derselben Etage sind offen, ihre Wände liegen gegenüber oder über Eck, und **R liegt auf der Linie zwischen ihnen**. Dafür bekommt jedes Fenster einen Punkt am Hausumriss (Wand und Reihenfolge, wie der Kompass sie zeichnet), jeder Raum den Mittelpunkt seiner Fenster. R „liegt auf der Linie“, wenn sein Punkt höchstens die Luftzug-Reichweite von der Strecke *b–c* entfernt ist. Wirkung wie die bisherigen Kombinationen: Pause nach der Fensterverzögerung, Erholung, kein Lernen, keine Zählung als „zu kalt“. Ohne Hausmaße gilt nur Regel 1.

Die Kombinationen von Hand (bis zu 4, auch über Etagen, z. B. Treppenhaus) bleiben unverändert und lösen wie bisher schon allein aus. In `logic/draft.py` werden `has_draft` und `draft_groups` erweitert: Luftzug kommt aus den Kombinationen von Hand oder den automatischen nach Regel 2. Querlüften heißt: eigenes Fenster offen und (Luftzug oder ein Paar nach Regel 1).

Im Panel unter **Haus > Hausplan**: Wählt man einen Raum, zeigt der Kompass seine Kombinationen als Linien, mit einem Schalter je Kombination. Der Raum-Editor listet sie ebenfalls. Das Attribut `draft` am Thermostat und das KI-Protokoll nennen die auslösende Kombination.

## 7. Gemeinsame Dienste im Kern (`core/`)

| Dienst | Heute | Neu |
|---|---|---|
| Außentemperatur | beide, jeweils mit Wetter als Ersatz | `core/sources.py`: eine Quelle (Sensor, sonst Wetter), Plausibilität −50…80 °C, Reparatur `outdoor_unavailable`. Ein Modul darf unter „Erweitert“ abweichen (falls beim Umzug verschieden). |
| Außenfeuchte | Heizung | Kern (Ersatz: Feuchte aus dem Wetter) |
| Wetter/Vorhersage | Heizung: täglich und stündlich, 10 s; Rollos: auto/täglich/zweimal täglich/stündlich, 30 s, Wiederholung nach 30 min | `ForecastService` mit Zwischenspeicher je Art; jedes Modul fragt mit eigenem Höchstalter und eigener Zeitgrenze, Verhalten wie bisher, weniger Abfragen. Reparatur `forecast_unsupported` bleibt. |
| Urlaub | beide eigene Listen, Rückkehr nur bei der Heizung | **Urlaubsmodus für das ganze Haus** mit eigenem Schalter, Abreise und Rückkehr (Abschnitt 7a). Vorheiz-Reserve und Urlaubstemperatur bleiben bei der Heizung. |
| Werktag, Wochenendtage | Rollos | Kern |
| Sprache der Meldungen | Rollos (auto/de/en); Heizung: HA-Sprache | Kern-Option für alle Module, Standard „auto“ (verhält sich wie heute) |
| Benachrichtigungen | Rollos: `notify.*`; Zähler: dauerhafte Benachrichtigung | `core/notify.py`. Beides bleibt, wie bisher je Modul. |
| Sonnenstand | Rollos: astral; Heizung: eigene Formel | Gemeinsames `Observer`-Hilfsmodul. Die Heizung behält ihre Formel, solange `test_sun.py` keine gleichen Werte zeigt. |
| Einheiten | Energie-Faktoren doppelt (`energy.UNIT_TO_KWH`, `units.ENERGY_UNITS`), Temperatur in `units.py` | `core/logic/units.py`. Temperatur-Eingabe wie bisher je Modul: Heizung in °C, Rollos im Einheitensystem. Ein Vereinheitlichen ist ein späterer Schritt. |
| Logbuch | drei Ereignisse | ein Ereignis `house_assistant_logbook` mit Modul; `messages.py` je Modul, gemeinsame Sprachauswahl |
| Reparaturen | je Integration | `core/issues.py`, Kennungen mit Modul-Präfix, Aufräumen wie bisher |
| KI-Client, Budget, Kosten | Heizung (`ai_client.py`, `logic/ai_policy.py`) | `core/ai/`: API-Key, Modell, Effort, Preise, Monatsbudget, max. Tokens, Reauth. KI-spezifische Teile (Nachtlauf, Prüfintervalle, Grenzen, Anweisungen) bleiben bei der Heizung. |
| Formulare, Panel-Grundlage | dreifach gleiche Hilfsfunktionen (`_number`, `_entity`, `_opt`, `_req`, `_clean`, `_flatten`, Spec-Serialisierung) | `core/schema.py` und `frontend/shared/*.js` |
| Werkzeuge | `check_privacy.py` (dreimal identisch), `build_labels.py`/`gen_labels.py`, CI-Workflows (identisch) | einmal im neuen Repo |

## 7a. Urlaubsmodus (für das ganze Haus)

Ein Urlaub für alle Module, ohne eigene Helfer (`input_boolean`, `input_datetime`). Die Logik liegt in `core/vacation.py`, die Zeitregeln rein in `core/logic/vacation.py`.

**Steuerung**
* Schalter **Urlaub** am Hauptgerät, bleibt über Neustarts erhalten.
* **Abreise** und **Rückkehr** als `datetime`-Entitäten, beide optional:
  * Zur Abreise schaltet sich der Urlaub ein, zur Rückkehr aus; danach werden beide Zeitpunkte geleert.
  * Ist nur die Rückkehr gesetzt, gilt der Urlaub ab sofort bis zur Rückkehr.
  * Eine Rückkehr in der Vergangenheit wird ignoriert, wie bisher bei der Heizung: Dann gilt der Urlaub, bis der Schalter aus ist.
  * Eine Abreise nach der Rückkehr wird abgelehnt.
* **Externe Quellen bleiben möglich:** Urlaubs-Entitäten (`input_boolean`, `binary_sensor`, `switch`, `calendar`, `schedule`; „an“ heißt Urlaub) und eine Rückkehr-Entität (`input_datetime`, `datetime`, Zeitstempel-Sensor). Die eigene Rückkehr hat Vorrang. Ein Modul kann eine abweichende Liste haben, falls sie beim Umzug verschieden war.
* Binärsensor **Urlaub aktiv**: an, wenn der Schalter an ist oder eine externe Quelle Urlaub meldet. Attribute: Quelle, Abreise, Rückkehr und der Beginn des Vorheizens.
* Dienst `house_assistant.set_vacation` mit `departure`, `return` und `clear` für Automationen, Ereignis `house_assistant_vacation` mit `active` und `source`, Logbuch-Eintrag bei Beginn und Ende.

**Wirkung je Modul**

| Modul | Wirkung | |
|---|---|---|
| Heizung | Urlaubstemperatur für alle Räume. Vorheizen mit gelernter Aufheizrate und Vorheiz-Reserve, damit zur Rückkehr der normale Sollwert erreicht ist. Heiztag-Entscheidung und KI berücksichtigen den Urlaub wie bisher. | wie bisher |
| Rollos | Urlaubssimulation: morgens und abends zufällige Zeit und Position, der Abendlauf ruht für teilnehmende Fenster. Sonnenschutz und Lüften laufen weiter. | wie bisher |
| Rollos | **Hitzeschutz im Urlaub:** Der Sonnenschutz senkt ab, ohne auf Raumtemperatur, Klimaanlage oder Heizbedarf zu warten. Sommertag, Außentemperatur, Sonnensensoren, Haltezeiten und Sonnenbereich gelten weiter, im Winter wird also nicht abgesenkt. Der Sonnenschutz-Schalter des Fensters bleibt maßgeblich. Option, Standard an. | neu |
| Lüftung | **Lüftungsempfehlung ruht:** neuer Zustand „Urlaub“, „Lüften empfohlen“ ist aus. Die Statistik der KI-Lüftungsprüfung zählt Urlaubsminuten nicht, und Urlaubstage gehen nicht ins Tagesprofil der Feuchte ein. Option, Standard an. | neu |
| Haus | **Offene Fenster bei Abreise:** Zu Beginn des Urlaubs kommt eine Meldung mit allen offenen oder gekippten Fenstern; nicht verfügbare Kontakte werden als „unbekannt“ genannt. Während des Urlaubs gibt es sofort eine Meldung, wenn ein Fenster geöffnet oder gekippt wird (nur echte Meldungen, nach der Entprellung). Option, Standard an. | neu |
| Zähler | **Leckwarnung:** Je Zähler gibt es „Im Urlaub warnen“ mit zwei Grenzen: einer Menge (Verbrauch seit Urlaubsbeginn, gemessen ab dem letzten gültigen Stand davor) und einem mittleren Durchfluss bzw. einer mittleren Leistung über der Grundlast. Standard: beim Wasser an mit 20 L bzw. 5 L/h, bei Gas und Strom aus (dort die Grundlast eintragen). Bei Überschreiten: Meldung, Logbuch, Ereignis `house_assistant_vacation_alert` und ein Attribut am Zähler, einmal je Urlaub und Fall. Der Wärmezähler ist ausgenommen; er wird ohnehin heizungsgeführt abgelesen. | neu |

Die Meldungen gehen an die Benachrichtigungsdienste des Hauses. Ist dort keiner eingetragen, erscheinen sie als Benachrichtigung in Home Assistant.

## 8. Module und interne Verknüpfungen

Die Module werden zunächst **1:1 umgezogen** (`heating/`, `shutter/`, `meter/`, Logik unverändert in `*/logic/`), damit der Umzug prüfbar bleibt. Danach werden sie auf Haus und Kern umgestellt. Jedes Modul lässt sich in der Einrichtung einzeln an- und abschalten.

| Verknüpfung | heute | neu (Standard, wenn beide Module an sind; Entitäts-Option bleibt wählbar) |
|---|---|---|
| Rollo „Heizbedarf“ (`heating_entity`) | Entität, z. B. `binary_sensor` Heiztag | **Heiztag der Heizung (intern)**, Änderung per Signal |
| Rollo „Raumtemperatur“ (`room_entity`) | je Fenster eingetragen | Vorgabe des Raums: Thermostat (Soll + Abstand) bzw. Temperatursensor |
| Rollo „Klimaanlage“ (`cooling_entity`) | je Fenster | Vorgabe des Raums, je Fenster abweichend möglich |
| Heizung „Wärmezähler“ (`heat_meter`) | Energie-Sensor, 60-s-Abfrage | **Zähler des Moduls direkt**: Wert mit echtem Ablesezeitpunkt (`value_time`). Eine bestätigte Korrektur nach unten (`corrected`) ist kein Zählertausch und setzt die Zeiträume nicht zurück. Ein beliebiger Sensor bleibt möglich. |
| Zähler „Bedingung“ (`condition_entity`) | Entität, nur `off` gilt | **Heiztag (intern)** als Auswahl. „Unbekannt“ zählt wie heute als Heiztag. Für den Wärmezähler kommt in Schritt 13 B der Zeitplan „Heizungsgeführt“ dazu. |
| Heizung „Fenster“ | Kontaktlisten im Bereich | Fenster des Raums (Abschnitt 5) |
| Heizung „Luftzug“ | 4 Kombinationen aus Kontakten | Fenster-Kombinationen und automatische Kombinationen (Abschnitt 6) |
| Außen, Wetter, Werktag, Sprache | doppelt | Kern (Abschnitt 7) |
| Urlaub | zwei Listen, Rückkehr-Entität | Urlaubsmodus des Hauses (Abschnitt 7a) |

**Modul-Neustart statt Neuladen des ganzen Eintrags:** Heute lädt jede Änderung die ganze Integration neu. Zusammengelegt würde das Bearbeiten eines Zählers die Heizung neu starten und Haltezeiten der Rollos zurücksetzen. Deshalb vergleicht der Update-Listener in `__init__.py` die Optionsabschnitte und Subentries nach Typ und startet **nur die betroffenen Module** neu. Jedes Modul trägt seine Entitäten über die gespeicherten `async_add_entities`-Rückrufe der Plattformen nach bzw. entfernt sie. Ändert sich ein Fenster, starten Heizung und Rollos neu. Der Store wird vorher gesichert, wie bisher beim Entladen.

## 9. Paketstruktur (neues Repo)

```
custom_components/house_assistant/
  __init__.py  manifest.json  const.py  config_flow.py  diagnostics.py  logbook.py
  services.py  services.yaml  icons.json  strings.json  translations/{de,en}.json  brand/
  sensor.py binary_sensor.py climate.py switch.py select.py button.py camera.py datetime.py
                                                                                 # sammeln die Entitäten der aktiven Module
  core/   house.py sources.py forecast.py vacation.py notify.py issues.py links.py schema.py store.py
          panel.py websocket.py ai/{client.py,policy.py}
          logic/{contacts.py,geometry.py,units.py,sun.py,vacation.py}             # rein, ohne HA
  heating/  coordinator.py entities.py services.py websocket.py messages.py logic/…  # aus ai_heating_assistant
  shutter/  engine.py entities.py services.py websocket.py messages.py logic/…      # aus shutter_assistant
  meter/    manager.py meter.py entities.py services.py websocket.py logic/…          # aus zaehler_ablesung
  frontend/ panel.js shared/*.js house.js heating.js shutter.js meter.js ai.js
            cards/{thermostat-card.js,cover-card.js,tiles.js} labels.js
scripts/  build_labels.py check_privacy.py transfer_legacy.py legacy/convert.py
docs/     transfer.md migration.md esphome-esp32-cam.yaml
tests/    core/ heating/{logic,ha} shutter/{logic,ha} meter/{logic,ha} legacy/ frontend_labels
```

* `manifest.json`: `requirements: ["anthropic>=0.125.0"]`, `dependencies: ["media_source"]`, `after_dependencies: ai_task, camera, frontend, http, light, lovelace, panel_custom, websocket_api`, `loggers: ["anthropic"]`, `single_config_entry`, `integration_type: service`, `iot_class: calculated`, Version `1.0.0`. In `hacs.json` Home Assistant 2026.10.0.
* Konventionen wie bisher: `from __future__ import annotations`, vollständige Typen, `logic/` ohne HA, kurze englische Kommentare, die das *Warum* erklären, Ruff (py313, Zeilenlänge 100), Oberfläche Deutsch und Englisch, `strings.json` gleich `en.json`.

## 10. Konfiguration, Entitäten, Dienste, Karten

**Eintrag:** `data = {api_key}`. Die `options` sind nach Modulen geschachtelt: `{"core": …, "ai": …, "heating": …, "shutter": …, "meter": …}`. Die Schlüssel in den Abschnitten bleiben wie bisher, deshalb muss der Modul-Code kaum geändert werden, und es gibt keine Namenskollisionen (z. B. `weather`, `night_end`). Die Dialoge bleiben erhalten:
* Einrichtung: Haus → Module wählen → je Modul die bisherigen Einrichtungsschritte.
* Optionsmenü nach Modulen gegliedert.
* Subentry-Dialoge für Raum, Fenster, Himmelsrichtung und Zähler.
* Reauth und Rekonfiguration für den API-Key.

Die Migrationen der bisherigen Heizungs-Optionen (`async_migrate_entry`, Minor-Versionen 2 bis 4) übernimmt das Umzugs-Skript. Der neue Eintrag startet mit Eintragsversion 1.1, eigene Migrationen folgen ab dort.

**Entitäten:** Das `unique_id`-Schema bleibt `{subentry_id oder entry_id}_{key}`. Ein Test stellt sicher, dass Schlüssel je Objektart über alle Module eindeutig sind. Gleiche Übersetzungsschlüssel werden getrennt, z. B. `status` in `room_status` und `window_status`; die Entitäts-ID ändert das nicht.

Geräte:
* Hauptgerät „House Assistant“, mit den Urlaubs-Entitäten (Schalter Urlaub, Abreise, Rückkehr, Binärsensor Urlaub aktiv).
* Dienstgeräte „Heizung“ und „Rollos“ für die bisherigen globalen Entitäten.
* Ein Gerät je Raum, je Fenster mit Rollo und je Zähler.

**Dienste** (alle unter `house_assistant.`; Admin-Pflicht und Antworten wie bisher):

| alt | neu |
|---|---|
| `ai_heating_assistant.export_parameters`, `import_parameters`, `reset_learned`, `run_ai_check`, `run_ai_ventilation_check`, `decide_heating_day` | gleicher Name |
| `shutter_assistant.move`, `start_override`, `end_override`, `resume` | `move_cover`, `start_cover_override`, `end_cover_override`, `resume_cover` |
| `zaehler_ablesung.read`, `set_reading` | `read_meter`, `set_meter_reading` |
| (neu) | `set_vacation` (Abschnitt 7a) |

**Ereignisse:** `house_assistant_cover_moved`, `house_assistant_cover_failed`, `house_assistant_protection`, `house_assistant_meter_reading`. Die Felder sind unverändert; Zähler-Ereignisse enthalten zusätzlich `meter_id`. Neu sind `house_assistant_vacation` und `house_assistant_vacation_alert`.

**Karten:** Auch für Nicht-Admins weiterhin als Dashboard-Ressource eingetragen.

| alt | neu |
|---|---|
| `custom:ai-heating-thermostat-card` | `custom:house-assistant-thermostat-card` |
| `custom:ai-heating-thermostat-compact-card` | `custom:house-assistant-thermostat-compact-card` |
| `custom:ai-heating-climate-tile-card` | `custom:house-assistant-climate-tile-card` |
| `custom:shutter-assistant-card` | `custom:house-assistant-cover-card` |
| `custom:shutter-assistant-tile` | `custom:house-assistant-tile` |
| `custom:shutter-assistant-window-tile` | `custom:house-assistant-window-tile` |

## 11. Dashboard (eine Seite, `/house-assistant`)

Oben die Bereiche, darunter die bisherigen Reiter. Jede Karte wird für sich gespeichert, wie bisher.

* **Übersicht:** je Modul eine Zusammenfassung (Heiztag und Phase, Räume mit Temperatur, Status und Lüftung, Rollos mit Automatik, Wetterschutz und Sonnenkompass, Zähler mit Stand und Status), KI-Kosten und gesammelte Hinweise. Im Urlaub zeigt ein Banner Abreise, Rückkehr, den Beginn des Vorheizens, ob Simulation und Leckwarnung aktiv sind, und offene Fenster.
* **Haus:** Räume · Fenster · Himmelsrichtungen · Hausplan (Kompass mit Haus, Fenstern und Querlüft-Linien) · **Urlaub** (Schalter, Abreise, Rückkehr, externe Quellen, die Optionen aus Abschnitt 7a) · Allgemein (Außensensoren, Wetter, Werktag, Sprache, Benachrichtigungen, Module).
  * Der Raum-Editor vereint den bisherigen Heizbereich-Editor und listet die Fenster des Raums mit Link.
  * Der Fenster-Editor zeigt zuerst die Grunddaten (Raum, Größe, Kontakte, Wand, Position, Himmelsrichtung, Rollo) und mit Rollo die bisherigen Karten des Shutter-Assistant-Editors mit Live-Check. „Duplizieren“ bleibt.
* **Heizung:** Übersicht (Heiztag manuell, Wärme-Karte) · Lernwerte · Einstellungen (Heizperiode, Frost, Urlaubstemperatur, PV, Wärmezähler) · Notfall & Lüftung · Heiztag-Entscheidung.
* **Rollos:** Übersicht (Sonnenbedingung-Check, Übersteuerung beenden) · Rollo-Fenster · Allgemein (Übersteuerung, Sommertag, Neustart-Schutz, Wetterschutz, Erweitert) · Abend & Urlaub.
* **Zähler:** Übersicht (Bild, Übernehmen, Stand setzen, verworfene Bilder) · Zähler (Editor mit Zuschnitt, Drehen, Livebild, Testbild, KI-Anweisung) · Einstellungen.
* **KI:** API-Key, Modell, Effort, Budget und Kosten aller Nutzer, Preise, Grenzen, KI-Anweisungen (Nachtlauf, Prüfung, Lüftungsprüfung).

## 12. Umzug der bestehenden Installation (durch Claude Code)

Werkzeug `scripts/transfer_legacy.py` mit dem reinen Umwandler `scripts/legacy/convert.py`. Er wird mit Testdaten im alten Format getestet (`tests/legacy/`). Ablauf, beschrieben in `docs/transfer.md`:

1. **Voraussetzungen:** Zugriff auf den `config`-Ordner, Home Assistant lässt sich stoppen, die HA-Version passt zum geprüften Speicherformat. **Vollständige Sicherung** (HA-Backup und Kopie von `.storage`, `automations.yaml`, `scripts.yaml`, `media/zaehler_ablesung`).
2. House Assistant über HACS installieren, aber **nicht** einrichten. Die alten Integrationen bleiben vorerst.
3. `transfer_legacy.py --dry-run` liest `core.config_entries`, die drei alten Stores sowie die Entitäts-, Geräte-, Bereichs- und Etagen-Registrierung. Es schreibt `transfer-plan.yaml` und einen Bericht. Offene Punkte klärt Claude Code mit dir.
   * **Räume** entstehen aus den Heizbereichen; der HA-Bereich kommt vom Gerät des Heizbereichs.
   * **Fenster** werden zusammengeführt: Steht ein Heizungskontakt auch in einem Rollo-Fenster, wird daraus ein gemeinsames Fenster mit der Größe aus der Heizung. Die übrigen Kontakte werden Fenster ohne Rollo. Der Raum eines Rollo-Fensters folgt aus gemeinsamen Kontakten oder aus `room_entity` = Thermostat des Bereichs, sonst wird gefragt.
   * Offen bleiben z. B. Wand und Position von Fenstern ohne Rollo und abweichende Werte von Außentemperatur oder Urlaub.
   * **Urlaub:** Die bisherigen Urlaubs-Entitäten und die Rückkehr-Entität werden externe Quellen des Urlaubsmodus. Damit ändert sich nichts, bestehende Automationen auf diese Helfer laufen weiter. Auf Wunsch stellt Claude Code danach auf den eigenen Schalter mit Abreise und Rückkehr um.
4. **HA stoppen**, dann `--apply transfer-plan.yaml`:
   * neuen Eintrag anlegen: Optionen geschachtelt, Subentries mit den alten IDs, Format nach dem Muster des bestehenden Heizungseintrags;
   * Stores übernehmen: `house_assistant.<entry>.heating|shutter|meter` mit Lernmodell, Sonnenskala, Heiztag-Verlauf, KI-Verlauf, Budget, Wärmezähler, Übersteuerungen, Markern und Zählerständen;
   * `media/zaehler_ablesung/<id>` nach `media/house_assistant/<id>` verschieben;
   * Entitäten umschreiben: Plattform, Eintrag und `unique_id`. **Die `entity_id` bleibt**, also bleiben auch Statistik und Verlauf;
   * Geräte an Ort und Stelle umschreiben: Kennung und Eintrag. Geräte-ID, Name, Bereich und Labels bleiben;
   * Dashboards im Speicher-Modus umschreiben (Kartentypen) und alte Ressourcen entfernen;
   * Dienst- und Ereignisnamen in `automations.yaml` und `scripts.yaml` ersetzen, alles andere melden;
   * die alten drei Einträge entfernen und ihre Stores als `.bak` behalten.
5. **HA starten und prüfen:** gleiche Entitäts-IDs, Verlauf und Energie-Dashboard lückenlos, Lernwerte im Panel wie vorher, Rollos ohne ungewollte Fahrt (Neustart-Schutz), Zähler ohne Neubeginn, Logbuch. Danach die alten Integrationen in HACS entfernen.
6. **Rückweg:** Sicherung zurückspielen.

Vorher läuft der gesamte Ablauf auf einer **Kopie der echten Konfiguration** in einer lokalen Test-Instanz von Home Assistant (siehe Abschnitt 15).

## 13. Zusätzliche Schritte (nach dem 1:1-Umbau)

**A. Rollos im Wärmemodell**
* Je Raum ein Sonneneintrag-Faktor *f* von 0 bis 1. Für jedes Fenster des Raums: Sonne im Azimut-Bereich seiner Himmelsrichtung × Öffnungsgrad des Rollos (ohne Rollo 1), gewichtet mit der Fenstergröße. Ohne Himmelsrichtung ist *f* = 1, also wie heute.
* Das Modell in `heating/logic/learning.py` wird zu `dT/dt = a·Ventil − k·(Ti−Ta) + s·PV·f`.
* Für die Vorlaufzeit (`planning_pv`) gilt das erwartete *f*: Ist der Sonnenschutz absehbar, gilt die Sonnenschutz-Position.
* Die KI bekommt je Raum die Minuten mit Sonnenschutz und das mittlere *f*.
* Abschaltbar je Raum. Weil sich der gelernte Sonnenfaktor `s` verschiebt, steht der Start im Logbuch, und das langsame Vergessen gleicht ihn in etwa drei Wochen an.

**B. Heizungsgeführte Ablesung des Wärmezählers**

Hat nichts geheizt, steht der Zähler still. Eine Ablesung bringt dann nichts außer KI-Kosten. Deshalb bekommt ein Zähler, der als Wärmezähler der Heizung gewählt ist, neben dem bisherigen Zeitplan „Nach Zeit“ (Intervall, Bedingung, zweites Intervall) den Zeitplan **„Heizungsgeführt“**. Er ist für den Wärmezähler der Standard; Wasser, Gas und Strom bleiben nach Zeit.
* **„Geheizt“** heißt: mindestens ein Heizkreis-Schalter der Heizung ist wirklich an. Gezählt wird der gemeldete Zustand, auch wenn von Hand geschaltet wurde. Die Heizung meldet jeden Wechsel über `HeatingLink`.
* **Während geheizt wird:** alle **15 Minuten** eine Ablesung (einstellbar als „Intervall beim Heizen“, Standard 15 min). Beim Einschalten selbst wird nicht abgelesen, denn der letzte Stand gilt bis dahin.
* **Nach dem Heizen:** eine Schlussablesung, sobald alle Kreise eine **Nachlaufzeit** lang aus sind (einstellbar, Standard 15 min; Wärme fließt nach dem Abschalten noch kurz). Geht während des Nachlaufs wieder ein Kreis an, läuft der 15-Minuten-Takt einfach weiter.
* **Ohne Heizen seit der letzten gültigen Ablesung:** keine Ablesung. „Nächste Ablesung“ ist dann leer, mit dem Attribut `waiting_for_heating`. Der Zustand „seit der letzten Ablesung geheizt“ wird im Store gesichert, damit nach einem Neustart nichts fehlt.
* **Vor jeder KI-Prüfung und um 23:55 Uhr** wird frisch abgelesen, aber nur, wenn seit der letzten gültigen Ablesung geheizt wurde. Die Heizung wartet bis zu 10 Minuten auf das Ergebnis. Weil der Stand ohne Heizen unverändert bleibt, schließen „heute“ und „gestern“ damit genau an Mitternacht an.
* **Bleibt wie bisher:** 15 Minuten nach einer unlesbaren oder fehlgeschlagenen Ablesung kommt der nächste Versuch, solange noch nicht gültig nach dem Heizen abgelesen wurde. „Jetzt ablesen“, Testbild und der Automatik-Schalter funktionieren wie bisher; ohne Automatik wird auch heizungsgeführt nicht abgelesen.
* **Optionale Kontrollablesung:** spätestens alle X Stunden, auch ohne Heizen (Standard 0 = aus). Sie ist für Zähler gedacht, die zusätzlich Warmwasser messen.
* **Plausibilität und KI-Prüfung:** Die Plausibilitätsprüfung rechnet weiter mit den Stunden seit der letzten gültigen Ablesung, längere Pausen sind also kein Problem. Die KI-Prüfung bekommt `heat` wie bisher, nur genauer.

**C. Zähler über Claude-Key**
* Neue Zähler-Option „KI-Quelle“: KI-Aufgabe (Standard, wie heute) oder Claude mit dem Key der Integration, Modell wählbar (Standard Haiku).
* Bilder werden als JPEG an die Messages-API geschickt, die Auswertung (`normalize`, Mehrheitsentscheid) bleibt gleich.
* Die Kosten laufen im gemeinsamen Monatsbudget. Der Sensor „KI-Kosten im Monat“ bekommt die Aufteilung nach Heizung, Lüftung und Zähler.
* Ist das Budget erreicht, wird auf eine eingetragene KI-Aufgabe ausgewichen. Sonst ist der Status Fehler, mit Hinweis im Logbuch.

## 14. Umsetzung in Schritten

Jeder Schritt ist ein eigener PR mit grüner CI.

1. **Repo und Werkzeuge:**
   * Grundgerüst, `pyproject.toml`.
   * CI: Ruff mit Prüfung und Format, Labels-Prüfung, pytest unter Python 3.14, hassfest und HACS.
   * `check_privacy.py`, ein neues Symbol, ein README-Gerüst.
2. **Kern:**
   * Eintrag, Einrichtung (Haus und Module), Quellen, `ForecastService`, Benachrichtigungen, Logbuch, Reparaturen, Store-Helfer, Formular-Helfer;
   * Panel-Grundgerüst mit Bereichen und Seitenleisten-Optionen;
   * Modul-Neustart.
3. **Zähler-Modul** (kleinstes Modul, erprobt das Muster): Code, Entitäten, Dienste, Panel-Befehle, Panel-Bereich; die 61 Tests werden portiert.
4. **Rollo-Modul:** Himmelsrichtungen und Fenster als gemeinsame Fenster-Subentries (mit Raum und Größe, zunächst optional); die 213 Tests werden portiert.
5. **Heizungs-Modul:**
   * Heizbereich wird Raum; Kontakte kommen aus den Fenstern (Abschnitt 5), Kombinationen aus Fenster-IDs.
   * Die 294 Tests werden portiert. Die alten Testdaten werden mit dem Umwandler aus Abschnitt 12 erzeugt, der damit gleich mitgetestet ist.
6. **Haus und Verknüpfungen:**
   * Raum-Vorgaben für Rollos;
   * Heiztag nach Rollos und Zähler, Zähler nach Heizung (Abschnitt 8);
   * Kern-Optionen statt doppelter Einstellungen;
   * Panel-Bereich Haus mit Raum- und Fenster-Editor.
7. **Querlüften automatisch** (Abschnitt 6) und gekippt mit 25 % (Abschnitt 5), mit Anzeige im Hausplan.
8. **Urlaubsmodus** (Abschnitt 7a):
   * Schalter, Abreise, Rückkehr, externe Quellen, Dienst und Ereignis;
   * Anbindung von Heizung und Rollos;
   * Hitzeschutz, ruhende Lüftungsempfehlung, Meldung offener Fenster, Leckwarnung der Zähler;
   * Panel-Reiter Urlaub und Banner in der Übersicht.
9. **Umzugs-Skript** mit Probelauf auf der Kopie, `docs/transfer.md`, README de/en, CHANGELOG, Version 1.0.0b1. Danach der echte Umzug durch Claude Code, dann 1.0.0.
10. **Zusätze A, B, C** (Abschnitt 13), jeder als eigener PR (1.1, 1.2, 1.3).

## 15. Prüfung

* **Automatisch:**
  * `ruff check` und `ruff format --check`, `python scripts/build_labels.py --check`, `pytest -q`;
  * alle 568 portierten Tests plus neue: Fensterzustand je Modul, Geometrie mit Beispielhaus (Kinderzimmer + Bad lösen im Wohnbereich aus, Schlafzimmer + Bad nicht), gekippt 25 %, interne Verknüpfungen, Modul-Neustart lässt andere Module unberührt, eindeutige Schlüssel, Umwandler;
  * heizungsgeführte Ablesung: ohne Heizen keine Ablesung, beim Heizen alle 15 min, Schlussablesung nach dem Nachlauf, kein Ablesen vor KI-Prüfung oder um 23:55 Uhr ohne Heizen, Wiederholung nach Fehler, Neustart mit offenem „geheizt“;
  * Urlaubsmodus: automatischer Beginn und automatisches Ende, nur Rückkehr gesetzt, Rückkehr in der Vergangenheit, externe Quellen, Neustart während des Urlaubs, Vorheizen zur eigenen Rückkehr, Hitzeschutz nur an Sommertagen, Lüftungsempfehlung „Urlaub“, Meldung offener Fenster bei Abreise und beim Öffnen, Leckwarnung nach Menge und nach Durchfluss (einmal je Urlaub), Wärmezähler ausgenommen;
  * hassfest und HACS in der CI.
* **Ende zu Ende** in einer Test-Instanz (Home Assistant 2026.10 im Container, Chromium und Playwright sind vorhanden):
  * mit den alten drei Integrationen und einer Kopie der echten `.storage` starten;
  * Umzugs-Skript laufen lassen, neu starten;
  * prüfen: Entitäts-IDs gleich, Statistik-IDs gleich, Lernwerte (Export vorher/nachher vergleichen), Panel-Bereiche (Bildschirmfotos), alte Dashboards mit neuen Kartentypen, Automationen mit neuen Dienstnamen, keine Rollo-Fahrt im Neustart-Schutz, Zähler-Mediapfad.

## 16. Bewusst unverändert und Risiken

* Temperatur-Eingaben bleiben je Modul wie bisher (Heizung °C, Rollos im Einheitensystem). Eine Vereinheitlichung kommt später.
* Lamellen werden weiterhin nicht gewendet. Eine Instanz je Home Assistant. Nur Schaltaktoren für die Heizung.
* Das Umzugs-Skript schreibt in die Speicherdateien von Home Assistant. Das geht nur bei gestopptem HA, mit Probelauf, Sicherung und Prüfung des Formats. Das größte Risiko des Umbaus liegt hier, deshalb gibt es den Durchlauf auf der Kopie.
* Die automatische Luftzug-Ableitung ist eine Näherung aus Wand und Reihenfolge, ohne Innentüren. Falsche Kombinationen schaltest du einzeln ab; Kombinationen von Hand bleiben möglich.
* Die Prompt-IDs der Räume (`a1`, `a2`, …) hängen an der Reihenfolge. Das Skript behält die Reihenfolge der Heizbereiche bei.

## 17. Funktions-Checkliste (alt → neu)

**Heizung → Modul Heizung, Raum, Kern**
* **Regelung:** vorausschauend ein und aus (Totzeit, Überschwingen, Restwärme), Sonne vorausschauend (PV-Prognose oder Wetter und Sonnenstand, Vertrauen 70 %, „Immer heizen unter Sollwert“, gelernte Klar-Himmel-Skala, PV-Ausfall-Logik), Mindestlaufzeiten, Frostschutz immer.
* **Fenster:** Fensterverzögerung, Erholung je Lüftung, Kurzlüften, Luftzug und Querlüften → Abschnitt 5 und 6.
* **Ausfälle:** Sensorfehler, Aktor nicht erreichbar, Wiederholungen 1/2/4/8/15 min, Reparaturen nach 15 min; Abschalten beim Deaktivieren und Entfernen, Freigabe-Liste.
* **Heizperiode** (Südhalbkugel-Vorschlag), **Urlaub** und Vorheizen auf die Rückkehr (jetzt über den Urlaubsmodus des Hauses, Abschnitt 7a; Rückkehr in der Vergangenheit wird weiter ignoriert).
* **Heiztag:** Regel θ/puffer, KI, Phasenmodell, Bewertung mit virtuellem Raum, Fehler A und B, Notfallregel, Heiztag manuell (auch außerhalb der Saison).
* **Lernen:** RLS-Wärmemodell, Ereignisse, Erholungsmodell, Speichern, Export, Import, Zurücksetzen, Anpassen an die Grenzen, gelernte Werte bearbeiten.
* **KI-Prüfung:** Kennzahlen inklusive `over_kh`, `sun_over_kh`, `on_per_kh`, Lüftungsliste, Verlauf der letzten 6, Grenzen und Schritt, KI-Anweisungen (Bausteine, eigene, Vorschau), seltener fragen, Kosten, Budget, Fallback-Preis, Ausfälle, Reauth, Wetter-Zeitgrenze, Wiederholung nach 15 min.
* **Wärmezähler** (zwischen zwei Zählerwerten, Bedarf, heute/gestern/Monat), Karte Wärme.
* **Lüftungsempfehlung** (alle Zustände), Feuchteprofil, Energiespar-Zuschlag, Schimmelgrenze, Pause, gelernte Lüftdauer je Öffnungsfläche, Querlüft-Austausch, KI-Lüftungsprüfung mit Intervallen.
* **Entitäten:** alle globalen und je Raum (Diagnose-Sensoren standardmäßig aus, nicht aufgezeichnete Attribute, veraltete Entitäten entfernen).
* **Dienste:** alle 6. Drei Karten. Logbuch, Diagnose (Key geschwärzt).

**Rollos → Modul Rollos, Fenster, Himmelsrichtung, Kern**
* **Sonnenschutz:** Sommertag (Vorhersage und Außentemperatur mit Nacht-Tiefstwert, Vorhersage-Art), Sonnenbedingung mit Haltezeiten, Wärmebedarf (Raum, Klimaanlage auch ohne Aktion, Heizbedarf), Absenken einmal am Tag, Benachrichtigung bei offenem Fenster und Nachholen, Auto-Hoch mit Toleranz, manuellen Sonnenschutz erkennen.
* **Abend:** Abendmodus (Sonnenhöhe, frühestens und spätestens, eigene Zeiten je Fenster), Abendlauf (trotz Übersteuerung), Abendposition, Nachziehen, Lüftungsposition mit Verzögerungen.
* **Fenster:** gekippt, Fenstergriffe, Kipp-Kontakte, unbekannt = offen, Aussperrschutz, Entprellung.
* **Wetterschutz:** je Fenster, Wind und Regen, eigene Windschwelle mit eigener Freigabe, „weiter zu gilt als geschützt“, Frost-Position, Freigabezeit, Automatik aus = kein Schutz, Anzeige des Sensorwerts, Ereignis.
* **Zuverlässigkeit:** Abstand der Befehle, Position prüfen mit Wiederholung und Meldung.
* **Übersteuerung:** echte Fahrt oder jeder Befehl, Kontext-Erkennung, Sonnenaufgang oder Dauer 0.
* **Zusatzbedingungen:** Öffnungssperre, Schließ-Auslöser, Fenster-Ausnahme.
* **Morgenöffnung** in 4 Modi, **Urlaubssimulation** (über den Urlaubsmodus des Hauses), **Neustart-Schutz** und Nachholen, Persistenz.
* **Entitäten:** alle globalen und je Fenster mit Attributen. Dienste (4, umbenannt), 3 Ereignisse.
* **Panel:** Sonnenkompass, Sonnenbedingung-Check, Haus im Kompass, Duplizieren. Karte und zwei Kacheln mit Farben und Editor; Seitenleisten-Option.
* **Reparaturen:** fehlende Gruppe, keine Vorhersage. Diagnose (Benachrichtigungen geschwärzt).

**Zähler → Modul Zähler**
* **Aufnahme:** Licht mit Helligkeit, Vorlauf, Bilder verwerfen, Licht danach nur aus, wenn es vorher aus war; externe Beleuchtung (beide Modi, Helligkeit, Vorlauf, Ausschalten auch bei Fehlern).
* **Bild:** Drehen, Zuschnitt, Belichtung, Aufbereiten, Livebild mit Licht, `letztes.jpg`, `original.jpg`, `letztes_2.jpg`.
* **KI:** Anweisung aus Art, Einheit, Nachkommastellen und Hinweisen, eigene Anweisung, Mehrheitsentscheid, Erstwert-Bestätigung, zweites Bild mit anderer Helligkeit, letzte Stände an die KI, Auswertung mit Einheit oder Bezeichnung und letzter Zeile.
* **Plausibilität:** Anstieg, kleiner, Korrektur mit Bestätigung, Übernehmen per Klick, verworfene Bilder (letzte 20), `total`-Zustandsklasse.
* **Benachrichtigungen:** je Fall mit Schwelle, Hauptschalter.
* **Zeitplan:** Intervall, Bedingung mit zweitem Intervall, 15 min nach Fehlern, Automatik, „Jetzt ablesen“, Testbild. Alles bleibt als „Nach Zeit“; für den Wärmezähler kommt „Heizungsgeführt“ dazu (13 B).
* **Entitäten:** alle 9 je Zähler. Dienste (2, umbenannt), Ereignis. KI-Aufgabe global oder je Zähler. ESPHome-Beispiel.
