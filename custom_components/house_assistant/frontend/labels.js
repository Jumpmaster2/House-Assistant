// Generated from the translation files by scripts/build_labels.py, do not edit by hand.
export const LABELS = {
 "de": {
  "steps": {
   "config.user": {
    "title": "House Assistant",
    "fields": {
     "modules": [
      "Module",
      "Die Teile des Hauses, die House Assistant steuern soll. Später unter Einstellungen > Module änderbar."
     ]
    },
    "sections": {}
   },
   "config.house": {
    "title": "Haus",
    "fields": {
     "outdoor_temperature": [
      "Außentemperatursensor",
      "Für Heizung und Rollos (z. B. ein Helfer, der mehrere Sensoren zusammenfasst). Ohne ihn gilt die aktuelle Temperatur der Wetter-Entität."
     ],
     "outdoor_humidity": [
      "Außenfeuchtesensor",
      "Optional. Für die Lüftungsempfehlung der Heizung; ohne Sensor wird die Luftfeuchte der Wetter-Entität genutzt."
     ],
     "weather": [
      "Wetter-Entität",
      "Empfohlen. Ihre Vorhersage nutzen die Heiztag-Entscheidung, die Sonnenprognose der Heizung und der Sommertag der Rollos. Ohne Außensensor gilt ihre aktuelle Temperatur."
     ],
     "language": [
      "Sprache der Meldungen",
      "Logbuch, letzter Grund, Push-Nachrichten und Benachrichtigungen aller Module. Automatisch = die Sprache von Home Assistant."
     ],
     "notify_services": [
      "Benachrichtigungsdienste",
      "Erhalten die Meldungen des Hauses, z. B. wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
     ],
     "workday_entity": [
      "Werktag-Sensor",
      "Optional, z. B. die Workday-Integration (berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
     ],
     "weekend_days": [
      "Wochenendtage",
      "Nur ohne Werktag-Sensor: an diesen Tagen gilt z. B. die Wochenend-Uhrzeit der Morgenöffnung."
     ],
     "house_azimuth": [
      "Vorderseite zeigt nach",
      "Himmelsrichtung, in die die Vorderseite schaut (90° = Ost, 180° = Süd, 270° = West), z. B. auf einer Karte abgelesen. Für das Haus im Sonnenkompass der Rollos."
     ],
     "house_width": [
      "Länge der Vorderseite",
      "Gilt auch für die Rückseite. Mit der Tiefe erscheint das Haus im Sonnenkompass, und der Luftzug durch Räume zwischen zwei offenen Fenstern wird erkannt."
     ],
     "house_depth": [
      "Tiefe",
      "Länge der beiden Seitenwände."
     ],
     "draft_reach": [
      "Luftzug-Reichweite",
      "Wie weit ein Raum von der Linie zwischen zwei offenen Fenstern anderer Räume entfernt sein darf, um ihren Luftzug abzubekommen (Standard 2 m)."
     ]
    },
    "sections": {}
   },
   "config.heating": {
    "title": "Heizung",
    "fields": {
     "pv_power": [
      "PV-Leistungssensor",
      "Optional. PV-Leistung (W oder kW) als Indikator für Sonne. Daraus wird der Sonneneinfluss je Bereich gelernt."
     ],
     "pv_forecast": [
      "PV-Prognosesensor",
      "Optional, nur zusammen mit dem PV-Leistungssensor. Erwartete PV-Energie der nächsten Stunde (Wh oder kWh, z. B. Forecast.Solar) oder erwartete Leistung in einer Stunde (W oder kW). Ohne diesen Sensor wird die Sonne aus der stündlichen Wettervorhersage und dem Sonnenstand geschätzt."
     ],
     "heat_meter": [
      "Wärmezähler",
      "Optional. Zählerstand des Wärmezählers der hier geregelten Heizkreise (Wh, kWh, MWh, MJ oder GJ, z. B. total_increasing). Die KI sieht dann die gemessene Wärme, außerdem steht sie im Panel. Seltene und grobe Werte sind kein Problem."
     ],
     "season_start": [
      "Beginn der Heizperiode (TT.MM.)",
      "Außerhalb der Heizperiode bleiben alle Kreise aus (nur Frostschutz) und die KI wird nicht gefragt."
     ],
     "season_end": [
      "Ende der Heizperiode (TT.MM.)",
      "Letzter Tag der Heizperiode, darf im Folgejahr liegen (z. B. 31.03.)."
     ],
     "frost_temperature": [
      "Frostschutz-Mindesttemperatur",
      "Gilt immer, auch außerhalb der Heizperiode und bei ausgeschaltetem Thermostat."
     ],
     "forecast_trust": [
      "Vertrauen in die Sonnenprognose",
      "Anteil der erwarteten PV-Leistung, auf den sich die Regelung beim Zurückhalten verlässt (100 % = volle Prognose, 0 % = nur die aktuelle PV-Leistung zählt)."
     ],
     "season_start_day": [
      "Heizperiode beginnt: Tag",
      "Ab diesem Datum darf geheizt werden (z. B. 1. Oktober)."
     ],
     "season_start_month": [
      "Heizperiode beginnt: Monat",
      ""
     ],
     "season_end_day": [
      "Heizperiode endet: Tag",
      "Letzter Tag der Heizperiode (z. B. 31. März); die Periode darf über den Jahreswechsel gehen."
     ],
     "season_end_month": [
      "Heizperiode endet: Monat",
      ""
     ]
    },
    "sections": {}
   },
   "config.heating_vacation": {
    "title": "Urlaub",
    "fields": {
     "vacation_entities": [
      "Urlaubs-Entitäten",
      "Ist eine dieser Entitäten 'an', gilt Urlaub (z. B. ein input_boolean oder ein Kalender)."
     ],
     "vacation_temperature": [
      "Urlaubstemperatur",
      "Sollwert für alle Räume im Urlaub."
     ],
     "return_entity": [
      "Rückkehr Datum/Uhrzeit",
      "Optional: input_datetime, Zeitstempel-Sensor oder datetime-Entität. Es wird so rechtzeitig vorgeheizt (gelernte Aufheizzeit), dass bei Rückkehr der normale Sollwert erreicht ist."
     ],
     "preheat_reserve": [
      "Vorheiz-Reserve",
      "Zusätzliche Zeit zur berechneten Vorheizzeit."
     ]
    },
    "sections": {}
   },
   "config.heating_decision": {
    "title": "Heiztag-Entscheidung",
    "fields": {
     "theta_start": [
      "Heizgrenze theta (Startwert)",
      "Geheizt wird, wenn die vorhergesagte Tageshöchsttemperatur darunter liegt (z. B. 16 °C). Wird danach gelernt."
     ]
    },
    "sections": {}
   },
   "config.heating_ai": {
    "title": "KI (Claude)",
    "fields": {
     "api_key": [
      "Anthropic API-Key",
      "Optional. Ohne Key läuft nur die lokale Regelung. Der Key wird nur in Home Assistant gespeichert und nie protokolliert."
     ],
     "nightly_time": [
      "Uhrzeit des Nachtlaufs",
      "Tägliche Entscheidung, ob heute geheizt wird (zugleich Beginn des ausgewerteten Tages). Läuft mit und ohne KI."
     ]
    },
    "sections": {}
   },
   "config.heating_ai_model": {
    "title": "KI-Modell und Budget",
    "fields": {
     "model": [
      "Claude-Modell",
      "Modell für alle KI-Abfragen. Die Preise sind Vorschläge für das gewählte Modell und änderbar."
     ],
     "monthly_budget": [
      "Monatsbudget",
      "In US-Dollar, wie Anthropic abrechnet. Keine KI-Abfragen mehr, sobald die Kosten des Monats diesen Wert erreichen (bis zum Monatswechsel)."
     ]
    },
    "sections": {}
   },
   "config.meter": {
    "title": "Zähler",
    "fields": {
     "ai_task_entity": [
      "KI-Aufgabe",
      "KI-Aufgaben-Entität, die die Bilder liest (z. B. Anthropic, OpenAI, Google oder Ollama mit Bildunterstützung). Ein Zähler kann eine eigene nutzen."
     ],
     "notify_rejected": [
      "Benachrichtigungen",
      "Hauptschalter für die Benachrichtigungen in Home Assistant. Ab wann sie bei welchem Zähler kommen, steht beim Zähler unter „Benachrichtigungen“."
     ]
    },
    "sections": {}
   },
   "config.shutter_summer": {
    "title": "Sommertag",
    "fields": {
     "summer_threshold": [
      "Sommertag ab Vorhersage-Höchsttemperatur",
      "Ohne Sommertag gibt es keinen Sonnenschutz. Tagsüber beginnt der Sommertag auch, wenn die Außentemperatur über diesen Wert steigt (siehe Nacht)."
     ],
     "night_threshold": [
      "Später Sommertag nur bei Nacht ab",
      "Wird der Tag erst durch die Außentemperatur zum Sommertag, zählt das nur, wenn der Vorhersage-Tiefstwert der kommenden Nacht mindestens so hoch ist. Kühlt es nachts ab (Frühling, Herbst), bleibt die Wärme im Haus. Ohne Tiefstwert in der Vorhersage gilt der Sommertag wie bisher."
     ],
     "heating_entity": [
      "Heizbedarf",
      "Optional, z. B. ein input_boolean „Heizperiode“ oder der Heiztag einer Heizungssteuerung. Solange sie an ist, ist Sonnenwärme erwünscht: Sonnenschutz nur, wenn der Raum eines Fensters trotzdem zu warm ist. Fenster ohne Raumtemperatur werden dann nicht abgesenkt."
     ],
     "use_heating_day": [
      "Heiztag der Heizung",
      "Ohne eigenen Heizbedarf: der Heiztag des Heizungsmoduls, aber nur in der Heizperiode. Gilt nur, solange das Heizungsmodul eingeschaltet ist."
     ],
     "day_change_time": [
      "Tageswechsel",
      "Prüfung der Vorhersage und Zurücksetzen der Tagesmarker für Sonnenschutz und Benachrichtigungen."
     ],
     "forecast_type": [
      "Vorhersage-Art",
      "Automatisch nimmt die erste Art, die die Wetter-Entität kann (täglich, zweimal täglich, stündlich). Aus stündlichen Werten werden Tageshöchst- und Nachttiefstwert berechnet."
     ]
    },
    "sections": {}
   },
   "config.shutter_evening": {
    "title": "Abendmodus",
    "fields": {
     "evening_earliest": [
      "Abendmodus frühestens",
      "Vor dieser Uhrzeit beginnt der Abendmodus nie."
     ],
     "evening_elevation": [
      "Sonnenhöhe",
      "Der Abendmodus beginnt, wenn die Sonne unter diese Höhe sinkt (z. B. -4 °)."
     ],
     "evening_latest": [
      "Abendmodus spätestens",
      "Zeit-Fallback: spätestens um diese Uhrzeit beginnt der Abendmodus."
     ],
     "night_end": [
      "Ende der Nacht",
      "Abendmodus und Abend-Marker enden um diese Uhrzeit (oder bei Sonnenaufgang, falls früher)."
     ],
     "follow_up_earliest": [
      "Nachziehen ab",
      "Ein am Abend geschlossenes Fenster fährt das Rollo erst ab dieser Uhrzeit zu."
     ]
    },
    "sections": {}
   },
   "config.reconfigure": {
    "title": "API-Key ändern",
    "fields": {
     "api_key": [
      "Anthropic API-Key",
      "Optional. Ohne Key läuft nur die lokale Regelung. Der Key wird nur in Home Assistant gespeichert und nie protokolliert."
     ]
    },
    "sections": {}
   },
   "config.reauth_confirm": {
    "title": "API-Key abgelehnt",
    "fields": {
     "api_key": [
      "Anthropic API-Key",
      "Wird vor dem Speichern bei Anthropic geprüft. Der Key wird nur in Home Assistant gespeichert und nie protokolliert."
     ]
    },
    "sections": {}
   },
   "options.init": {
    "title": "Einstellungen",
    "fields": {},
    "sections": {}
   },
   "options.modules": {
    "title": "Module",
    "fields": {
     "modules": [
      "Module",
      "Die Teile des Hauses, die House Assistant steuern soll. Ein abgeschaltetes Modul behält seine Einstellungen."
     ],
     "show_panel": [
      "Dashboard in der Seitenleiste",
      "Aus: Das Dashboard verschwindet aus der Seitenleiste, bleibt aber über „Einstellungen“ bei der Integration erreichbar."
     ]
    },
    "sections": {}
   },
   "options.house": {
    "title": "Haus",
    "fields": {
     "outdoor_temperature": [
      "Außentemperatursensor",
      "Für Heizung und Rollos (z. B. ein Helfer, der mehrere Sensoren zusammenfasst). Ohne ihn gilt die aktuelle Temperatur der Wetter-Entität."
     ],
     "outdoor_humidity": [
      "Außenfeuchtesensor",
      "Optional. Für die Lüftungsempfehlung der Heizung; ohne Sensor wird die Luftfeuchte der Wetter-Entität genutzt."
     ],
     "weather": [
      "Wetter-Entität",
      "Empfohlen. Ihre Vorhersage nutzen die Heiztag-Entscheidung, die Sonnenprognose der Heizung und der Sommertag der Rollos. Ohne Außensensor gilt ihre aktuelle Temperatur."
     ],
     "language": [
      "Sprache der Meldungen",
      "Logbuch, letzter Grund, Push-Nachrichten und Benachrichtigungen aller Module. Automatisch = die Sprache von Home Assistant."
     ],
     "notify_services": [
      "Benachrichtigungsdienste",
      "Erhalten die Meldungen des Hauses, z. B. wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
     ],
     "workday_entity": [
      "Werktag-Sensor",
      "Optional, z. B. die Workday-Integration (berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
     ],
     "weekend_days": [
      "Wochenendtage",
      "Nur ohne Werktag-Sensor: an diesen Tagen gilt z. B. die Wochenend-Uhrzeit der Morgenöffnung."
     ],
     "house_azimuth": [
      "Vorderseite zeigt nach",
      "Himmelsrichtung, in die die Vorderseite schaut (90° = Ost, 180° = Süd, 270° = West), z. B. auf einer Karte abgelesen. Für das Haus im Sonnenkompass der Rollos."
     ],
     "house_width": [
      "Länge der Vorderseite",
      "Gilt auch für die Rückseite. Mit der Tiefe erscheint das Haus im Sonnenkompass, und der Luftzug durch Räume zwischen zwei offenen Fenstern wird erkannt."
     ],
     "house_depth": [
      "Tiefe",
      "Länge der beiden Seitenwände."
     ],
     "draft_reach": [
      "Luftzug-Reichweite",
      "Wie weit ein Raum von der Linie zwischen zwei offenen Fenstern anderer Räume entfernt sein darf, um ihren Luftzug abzubekommen (Standard 2 m)."
     ]
    },
    "sections": {}
   },
   "options.vacation": {
    "title": "Urlaub",
    "fields": {
     "vacation_entities": [
      "Externe Urlaubs-Entitäten",
      "Ist eine davon an, gilt ebenfalls Urlaub (z. B. ein input_boolean oder ein Kalender). Gilt für Heizung und Rollos; ohne Eintrag hier gelten die Entitäten in deren Einstellungen."
     ],
     "return_entity": [
      "Externe Rückkehr",
      "Optional: input_datetime, datetime- oder Zeitstempel-Entität. Die Heizung heizt darauf vor; eine eigene Rückkehr des Schalters hat Vorrang."
     ],
     "vacation_window_alert": [
      "Offene Fenster melden",
      "Zu Beginn des Urlaubs eine Meldung mit allen offenen, gekippten oder unbekannten Fenstern, im Urlaub sofort eine Meldung, wenn ein Fenster geöffnet oder gekippt wird. An die Benachrichtigungsdienste des Hauses, ohne sie als Benachrichtigung in Home Assistant."
     ]
    },
    "sections": {}
   },
   "options.meter": {
    "title": "Zähler",
    "fields": {
     "ai_task_entity": [
      "KI-Aufgabe",
      "KI-Aufgaben-Entität, die die Bilder liest (z. B. Anthropic, OpenAI, Google oder Ollama mit Bildunterstützung). Ein Zähler kann eine eigene nutzen."
     ],
     "notify_rejected": [
      "Benachrichtigungen",
      "Hauptschalter für die Benachrichtigungen in Home Assistant. Ab wann sie bei welchem Zähler kommen, steht beim Zähler unter „Benachrichtigungen“."
     ]
    },
    "sections": {}
   },
   "options.shutter": {
    "title": "Rollos",
    "fields": {},
    "sections": {}
   },
   "options.shutter_general": {
    "title": "Allgemein",
    "fields": {
     "outdoor_temperature": [
      "Außentemperatur-Sensor",
      "Für den Sommertag und die Temperaturbedingung jedes Fensters. Ohne Sensor wird die aktuelle Temperatur der Wetter-Entität verwendet (mindestens eins von beiden). Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "weather": [
      "Wetter-Entität",
      "Ihre Tagesvorhersage entscheidet beim Tageswechsel, ob heute ein Sommertag ist. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "language": [
      "Sprache der Meldungen",
      "Logbuch, letzter Grund und Push-Nachrichten. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "notify_services": [
      "Benachrichtigungsdienste",
      "Erhalten eine Nachricht, wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy). Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "workday_entity": [
      "Werktag-Sensor",
      "Optional, für die Morgenöffnung nach Uhrzeit (z. B. Workday-Integration, berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "weekend_days": [
      "Wochenendtage",
      "Nur ohne Werktag-Sensor: an diesen Tagen gilt die Wochenend-Uhrzeit der Morgenöffnung. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ]
    },
    "sections": {}
   },
   "options.shutter_override": {
    "title": "Manuelle Übersteuerung",
    "fields": {
     "override_trigger": [
      "Übersteuerung beginnt",
      "Nur bei echter Fahrt: Ein Befehl an ein Rollo, das schon in der Zielposition steht (z. B. „alle Rollos auf“, während es offen ist), startet keine Übersteuerung. Jeder Befehl: auch ohne Fahrt, wie bisher."
     ]
    },
    "sections": {}
   },
   "options.shutter_summer": {
    "title": "Sommertag",
    "fields": {
     "summer_threshold": [
      "Sommertag ab Vorhersage-Höchsttemperatur",
      "Ohne Sommertag gibt es keinen Sonnenschutz. Tagsüber beginnt der Sommertag auch, wenn die Außentemperatur über diesen Wert steigt (siehe Nacht)."
     ],
     "night_threshold": [
      "Später Sommertag nur bei Nacht ab",
      "Wird der Tag erst durch die Außentemperatur zum Sommertag, zählt das nur, wenn der Vorhersage-Tiefstwert der kommenden Nacht mindestens so hoch ist. Kühlt es nachts ab (Frühling, Herbst), bleibt die Wärme im Haus. Ohne Tiefstwert in der Vorhersage gilt der Sommertag wie bisher."
     ],
     "heating_entity": [
      "Heizbedarf",
      "Optional, z. B. ein input_boolean „Heizperiode“ oder der Heiztag einer Heizungssteuerung. Solange sie an ist, ist Sonnenwärme erwünscht: Sonnenschutz nur, wenn der Raum eines Fensters trotzdem zu warm ist. Fenster ohne Raumtemperatur werden dann nicht abgesenkt."
     ],
     "use_heating_day": [
      "Heiztag der Heizung",
      "Ohne eigenen Heizbedarf: der Heiztag des Heizungsmoduls, aber nur in der Heizperiode. Gilt nur, solange das Heizungsmodul eingeschaltet ist."
     ],
     "day_change_time": [
      "Tageswechsel",
      "Prüfung der Vorhersage und Zurücksetzen der Tagesmarker für Sonnenschutz und Benachrichtigungen."
     ],
     "forecast_type": [
      "Vorhersage-Art",
      "Automatisch nimmt die erste Art, die die Wetter-Entität kann (täglich, zweimal täglich, stündlich). Aus stündlichen Werten werden Tageshöchst- und Nachttiefstwert berechnet."
     ]
    },
    "sections": {}
   },
   "options.shutter_evening": {
    "title": "Abendmodus",
    "fields": {
     "evening_earliest": [
      "Abendmodus frühestens",
      "Vor dieser Uhrzeit beginnt der Abendmodus nie."
     ],
     "evening_elevation": [
      "Sonnenhöhe",
      "Der Abendmodus beginnt, wenn die Sonne unter diese Höhe sinkt (z. B. -4 °)."
     ],
     "evening_latest": [
      "Abendmodus spätestens",
      "Zeit-Fallback: spätestens um diese Uhrzeit beginnt der Abendmodus."
     ],
     "night_end": [
      "Ende der Nacht",
      "Abendmodus und Abend-Marker enden um diese Uhrzeit (oder bei Sonnenaufgang, falls früher)."
     ],
     "follow_up_earliest": [
      "Nachziehen ab",
      "Ein am Abend geschlossenes Fenster fährt das Rollo erst ab dieser Uhrzeit zu."
     ]
    },
    "sections": {}
   },
   "options.shutter_vacation": {
    "title": "Urlaubssimulation",
    "fields": {
     "vacation_entities": [
      "Urlaubs-Entitäten",
      "Urlaub ist aktiv, solange eine davon an ist (z. B. ein input_boolean „Urlaub“ oder ein Kalender). Gilt nur, solange unter Einstellungen > Urlaub nichts eingetragen ist. Der Schalter „Urlaub“ des Hauses gilt immer."
     ],
     "vacation_morning_start": [
      "Urlaub morgens ab",
      "Geschlossene Rollos der Fenster in der Simulation öffnen danach zu einer zufälligen Zeit."
     ],
     "vacation_morning_window": [
      "Zufallszeitraum morgens",
      "Jedes Fenster öffnet zu einer zufälligen Zeit in diesem Zeitraum."
     ],
     "vacation_position_min": [
      "Öffnungsposition von",
      "Zufällige Position zwischen beiden Werten."
     ],
     "vacation_position_max": [
      "Öffnungsposition bis",
      "Zufällige Position zwischen beiden Werten."
     ],
     "vacation_evening_start": [
      "Urlaub abends ab",
      "Beginnt den Abend für die Fenster der Simulation und schließt sie zu zufälligen Zeiten. Der normale Abendlauf ruht im Urlaub."
     ],
     "vacation_evening_window": [
      "Zufallszeitraum abends",
      "Jedes Fenster schließt zu einer zufälligen Zeit in diesem Zeitraum."
     ],
     "vacation_heat_protection": [
      "Hitzeschutz im Urlaub",
      "Der Sonnenschutz senkt im Urlaub ab, ohne auf Raumtemperatur, Klimaanlage oder Heizbedarf zu warten. Sommertag, Außentemperatur, Sonnensensoren, Haltezeiten und der Sonnenschalter des Fensters gelten weiter."
     ]
    },
    "sections": {}
   },
   "options.shutter_protection": {
    "title": "Wetterschutz",
    "fields": {
     "wind_entity": [
      "Windsensor",
      "Windgeschwindigkeit oder Böen, z. B. von einer Wetterstation."
     ],
     "wind_threshold": [
      "Windschutz ab",
      "In der Einheit des Windsensors (z. B. km/h oder m/s)."
     ],
     "rain_entity": [
      "Regensensor",
      "Ein Regensensor, der einschaltet, oder eine Regenmenge (z. B. mm/h)."
     ],
     "rain_threshold": [
      "Regenschutz über",
      "Nur bei einem Zahlenwert: Regen zählt über diesem Wert."
     ],
     "frost_threshold": [
      "Frost ab (höchstens)",
      "Außentemperatur. Nur Fenster mit einer Frostposition machen mit."
     ],
     "protection_release": [
      "Freigabe nach",
      "Ein Schutz endet erst, wenn der Wert so lange wieder im sicheren Bereich war. Ein nicht verfügbarer Sensor beendet nie einen Schutz."
     ]
    },
    "sections": {}
   },
   "options.shutter_startup": {
    "title": "Neustart-Schutz",
    "fields": {
     "startup_delay": [
      "Neustart-Schutz",
      "Nach dem Start von Home Assistant so lange keine Fahrt (Sensoren und Rollos melden sich noch an)."
     ],
     "catch_up_after": [
      "Abendlauf nachholen ab",
      "Nach dem Neustart-Schutz wird der Abendlauf für noch nicht geschlossene Fenster nachgeholt, aber erst ab dieser Uhrzeit."
     ]
    },
    "sections": {}
   },
   "options.shutter_advanced": {
    "title": "Erweitert",
    "fields": {
     "window_closed_delay": [
      "Fenster gilt als geschlossen nach",
      "Ein Fensterkontakt muss so lange „zu“ melden, bevor Nachziehen, Sonnenschutz oder Schließ-Auslöser greifen (gegen Prellen beim Schließen)."
     ],
     "command_interval": [
      "Abstand zwischen Fahrbefehlen",
      "Mehrere Rollos fahren nacheinander mit diesem Abstand (gegen Funkkollisionen). 0 = alle gleichzeitig."
     ],
     "verify_after": [
      "Position prüfen nach",
      "Hat ein Rollo sein Ziel bis dahin nicht erreicht, wird der Befehl einmal wiederholt, danach kommt eine Meldung. 0 = aus."
     ]
    },
    "sections": {}
   },
   "options.heating": {
    "title": "Heizung",
    "fields": {},
    "sections": {}
   },
   "options.heating_general": {
    "title": "Allgemein",
    "fields": {
     "outdoor_temperature": [
      "Außentemperatursensor",
      "Sensor für die Außentemperatur (z. B. ein Helfer, der mehrere Sensoren zusammenfasst). Ohne ihn gilt die aktuelle Temperatur der Wetter-Entität. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "outdoor_humidity": [
      "Außenfeuchtesensor",
      "Optional. Für die Lüftungsempfehlung; ohne Sensor wird die Luftfeuchte der Wetter-Entität genutzt. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "weather": [
      "Wetter-Entität",
      "Optional, aber empfohlen. Die Vorhersage wird für die nächtliche Heiztag-Entscheidung und die Sonnenprognose genutzt. Ohne Außensensor gilt ihre aktuelle Temperatur als Außentemperatur. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
     ],
     "pv_power": [
      "PV-Leistungssensor",
      "Optional. PV-Leistung (W oder kW) als Indikator für Sonne. Daraus wird der Sonneneinfluss je Bereich gelernt."
     ],
     "pv_forecast": [
      "PV-Prognosesensor",
      "Optional, nur zusammen mit dem PV-Leistungssensor. Erwartete PV-Energie der nächsten Stunde (Wh oder kWh, z. B. Forecast.Solar) oder erwartete Leistung in einer Stunde (W oder kW). Ohne diesen Sensor wird die Sonne aus der stündlichen Wettervorhersage und dem Sonnenstand geschätzt."
     ],
     "heat_meter": [
      "Wärmezähler",
      "Optional. Zählerstand des Wärmezählers der hier geregelten Heizkreise (Wh, kWh, MWh, MJ oder GJ, z. B. total_increasing). Die KI sieht dann die gemessene Wärme, außerdem steht sie im Panel. Seltene und grobe Werte sind kein Problem."
     ],
     "season_start": [
      "Beginn der Heizperiode (TT.MM.)",
      "Außerhalb der Heizperiode bleiben alle Kreise aus (nur Frostschutz) und die KI wird nicht gefragt."
     ],
     "season_end": [
      "Ende der Heizperiode (TT.MM.)",
      "Letzter Tag der Heizperiode, darf im Folgejahr liegen (z. B. 31.03.)."
     ],
     "frost_temperature": [
      "Frostschutz-Mindesttemperatur",
      "Gilt immer, auch außerhalb der Heizperiode und bei ausgeschaltetem Thermostat."
     ],
     "forecast_trust": [
      "Vertrauen in die Sonnenprognose",
      "Anteil der erwarteten PV-Leistung, auf den sich die Regelung beim Zurückhalten verlässt (100 % = volle Prognose, 0 % = nur die aktuelle PV-Leistung zählt)."
     ],
     "season_start_day": [
      "Heizperiode beginnt: Tag",
      "Ab diesem Datum darf geheizt werden (z. B. 1. Oktober)."
     ],
     "season_start_month": [
      "Heizperiode beginnt: Monat",
      ""
     ],
     "season_end_day": [
      "Heizperiode endet: Tag",
      "Letzter Tag der Heizperiode (z. B. 31. März); die Periode darf über den Jahreswechsel gehen."
     ],
     "season_end_month": [
      "Heizperiode endet: Monat",
      ""
     ]
    },
    "sections": {}
   },
   "options.heating_vacation": {
    "title": "Urlaub",
    "fields": {
     "vacation_entities": [
      "Urlaubs-Entitäten",
      "Ist eine dieser Entitäten 'an', gilt Urlaub (z. B. ein input_boolean oder ein Kalender). Gilt nur, solange unter Einstellungen > Urlaub nichts eingetragen ist. Der Schalter „Urlaub“ des Hauses gilt immer."
     ],
     "vacation_temperature": [
      "Urlaubstemperatur",
      "Sollwert für alle Räume im Urlaub (z. B. 17 °C)."
     ],
     "return_entity": [
      "Rückkehr Datum/Uhrzeit",
      "Optional: input_datetime, Zeitstempel-Sensor oder datetime-Entität. Es wird so rechtzeitig vorgeheizt (gelernte Aufheizzeit), dass bei Rückkehr der normale Sollwert erreicht ist. Die Rückkehr des Schalters „Urlaub“ hat Vorrang; ohne sie gilt eine unter Einstellungen > Urlaub eingetragene."
     ],
     "preheat_reserve": [
      "Vorheiz-Reserve",
      "Zusätzliche Zeit zur berechneten Vorheizzeit (z. B. 30 min)."
     ],
     "vacation_ventilation_pause": [
      "Lüftungsempfehlung ruht",
      "Im Urlaub zeigt die Lüftungsempfehlung „Urlaub“, „Lüften empfohlen“ ist aus. Urlaubsminuten zählen nicht für die KI-Lüftungsprüfung und gehen nicht ins Feuchteprofil ein."
     ]
    },
    "sections": {}
   },
   "options.heating_rules": {
    "title": "Notfallregel",
    "fields": {
     "emergency_enabled": [
      "Notfallregel",
      "An Tagen ohne Heizbetrieb darf ein Raum trotzdem heizen, wenn die nach der Vorlaufzeit erwartete Temperatur lange und deutlich unter dem Sollwert liegt, ohne dass gelüftet wurde."
     ],
     "emergency_delta": [
      "Notfall: unter Sollwert um",
      "Wie weit die nach der Vorlaufzeit erwartete Temperatur unter dem Sollwert liegen muss (mindestens die Einschalthysterese)."
     ],
     "emergency_duration": [
      "Notfall: Dauer",
      "Wie lange die erwartete Temperatur so tief bleiben muss (z. B. 45 min)."
     ],
     "emergency_window_quiet": [
      "Notfall: keine Fensteränderung seit",
      "Lüften zählt nicht: die Fenster dürfen sich so lange nicht verändert haben."
     ],
     "force_on_below": [
      "Immer heizen unter Sollwert um",
      "So weit unter dem Sollwert heizt der Kreis unabhängig von jeder Vorhersage und der erwarteten Sonne."
     ]
    },
    "sections": {}
   },
   "options.heating_ventilation": {
    "title": "Lüftung",
    "fields": {
     "ventilation_min_ah_advantage": [
      "Mindestvorteil absolute Feuchte",
      "Absolute Feuchte ist der Wassergehalt der Luft in g/m³, unabhängig von der Temperatur. Die Außenluft muss mindestens so viel weniger Wasser enthalten für 'Jetzt lüften' (z. B. 0,8 g/m³)."
     ],
     "ventilation_max_reference_excess": [
      "Außen höchstens wärmer um",
      "Trocknen wird nicht empfohlen, wenn es außen um mehr als diesen Wert wärmer ist als innen."
     ],
     "ventilation_energy_rh_per_k": [
      "Energiespar-Zuschlag",
      "Energiesparen: In der Heizperiode kostet Lüften Wärme, umso mehr, je kälter es draußen ist. Die Feuchte muss die Schwelle dann um so viel je Kelvin übersteigen, wie es draußen kälter ist als im Raum (z. B. 0,25 %/K: bei 21 °C innen und 1 °C außen 5 % mehr), höchstens bis 70 %; darüber wird gegen Schimmel immer gelüftet. 0 = aus. Startwert, die KI passt ihn je Raum an."
     ],
     "ventilation_mould_rh": [
      "Schimmelgrenze",
      "Ab dieser relativen Feuchte wird immer zum Lüften geraten, auch bei Frost und direkt nach einer Lüftung; der Energiespar-Zuschlag geht nie darüber. Für Räume mit kalten Außenwänden niedriger setzen. Startwert, die KI passt ihn je Raum an."
     ],
     "ventilation_airing_target_below": [
      "Lüftziel unter der Schwelle",
      "Die vorgeschlagene Lüftdauer zielt so weit unter die Feuchte-Schwelle. Startwert für die KI."
     ],
     "ventilation_airing_time_factor": [
      "Lüftdauer-Faktor",
      "Skaliert die vorgeschlagene Lüftdauer. Sobald zwei Lüftungen ausgewertet sind, wird sie aus dem gelernten Luftaustausch des Raums und dem Temperaturunterschied berechnet, vorher aus der Außentemperatur (5 Minuten bei Frost bis 20 Minuten bei Wärme). Startwert für die KI."
     ],
     "ventilation_airing_min_minutes": [
      "Kürzeste Lüftdauer",
      "Startwert für die KI."
     ],
     "ventilation_airing_max_minutes": [
      "Längste Lüftdauer",
      "Startwert für die KI."
     ],
     "ventilation_airing_pause": [
      "Pause nach dem Lüften",
      "Nach dem Lüften kommt Feuchte aus Wänden und Möbeln zurück. Erst nach dieser Pause wird wieder zum Trocknen geraten (unter der Schimmelgrenze); das spart Wärme und Nerven. Startwert für die KI."
     ],
     "ventilation_min_cooling_advantage": [
      "Mindest-Kühlvorteil",
      "'Lüften sinnvoll', wenn es innen mindestens so viel wärmer ist als außen (nicht während Heizbetrieb)."
     ],
     "ventilation_cooling_margin": [
      "Mindestabstand über Sollwert für Kühlen",
      "In der Heizperiode wird 'Lüften sinnvoll' (Kühlen) nur empfohlen, wenn der Raum mindestens so viel wärmer ist als sein Sollwert. Außerhalb der Heizperiode gilt das nicht. Räume ohne Heizkreis nutzen ihren Start-Sollwert."
     ],
     "ventilation_cooling_min_temp": [
      "Kühlen erst ab Raumtemperatur",
      "'Lüften sinnvoll' (Kühlen) erst ab dieser Raumtemperatur, ganzjährig. 0 = aus. Zusätzlich wird Kühlen nie empfohlen, wenn die Außenluft die relative Feuchte des Raums über seine Feuchte-Schwelle bringen würde."
     ],
     "night_start_hour": [
      "Nacht beginnt um",
      "Bei einem anderen Raum als Referenz zählt der Kühlvorteil nur nachts."
     ],
     "night_end_hour": [
      "Nacht endet um",
      "Ende der Nacht (Uhrzeit, z. B. 08:00)."
     ],
     "ventilation_ai_enabled": [
      "KI passt Lüftung je Raum an",
      "Ganzjährig prüft die KI die Lüftungsschwellen jedes Raums mit Feuchtesensor: Sie lernt, was in jedem Raum üblich ist, wie tief die Feuchte überhaupt sinken kann und was Lüften wirklich bringt. Nutzt das gemeinsame KI-Monatsbudget."
     ],
     "ventilation_check_interval": [
      "Grundintervall Lüftungsprüfung",
      "Erstes Intervall; es verdoppelt sich mit jeder Prüfung ohne relevante Änderung und beginnt von vorn, wenn ein Raum lange feucht bleibt oder sich ein Wert ändert."
     ],
     "ventilation_check_max_interval": [
      "Höchstintervall Lüftungsprüfung",
      "Länger wird das Intervall nie."
     ]
    },
    "sections": {}
   },
   "options.heating_ai": {
    "title": "KI",
    "fields": {
     "model": [
      "Claude-Modell",
      "Modell für alle KI-Abfragen. Die Preise sind Vorschläge für das gewählte Modell und änderbar."
     ],
     "effort": [
      "Denkaufwand",
      "Claude denkt vor der Antwort nach. Mehr Aufwand kann bessere Antworten geben, braucht aber mehr Tokens, die als Ausgabe abgerechnet werden. 'auto' überlässt es dem Modell."
     ],
     "nightly_time": [
      "Uhrzeit des Nachtlaufs",
      "Tägliche Entscheidung, ob heute geheizt wird (zugleich Beginn des bewerteten Tages)."
     ],
     "check_interval": [
      "Prüfintervall",
      "Grundintervall der periodischen KI-Prüfung an Heiztagen (z. B. 4 h). Es verdoppelt sich nach jeder Prüfung ohne relevante Änderung."
     ],
     "check_max_interval": [
      "Maximales Prüfintervall",
      "Obergrenze für das verdoppelte Intervall (z. B. 48 h)."
     ],
     "monthly_budget": [
      "Monatsbudget",
      "In US-Dollar, wie Anthropic abrechnet. Keine KI-Abfragen mehr, sobald die Kosten des Monats diesen Wert erreichen (bis zum Monatswechsel). Eine Prüfung kostet meist wenige Cent, 5 USD reichen also für etwa 100 bis 200 Abfragen."
     ],
     "price_input": [
      "Preis Eingabe-Tokens",
      "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
     ],
     "price_output": [
      "Preis Ausgabe-Tokens",
      "US-Dollar pro Million Tokens, wie Anthropic abrechnet (Denken zählt als Ausgabe)."
     ],
     "price_cache_write": [
      "Preis Cache schreiben",
      "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
     ],
     "price_cache_read": [
      "Preis Cache lesen",
      "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
     ],
     "max_output_tokens": [
      "Maximale Ausgabe-Tokens",
      "Obergrenze je Antwort, Denken eingeschlossen (zu niedrig schneidet Antworten ab; sie sind bezahlt, werden aber verworfen). Auch Obergrenze der Kostenschätzung vor einer Abfrage."
     ]
    },
    "sections": {}
   },
   "options.heating_decision": {
    "title": "Heiztag-Entscheidung (Experten)",
    "fields": {
     "theta": [
      "Heizgrenze theta (gelernt)",
      "Aktuelle Schwelle der Heiztag-Regel: liegt die Prognose-Höchsttemperatur darunter, wird geheizt. Eine Änderung ersetzt den gelernten Wert; danach wird von hier aus weiter gelernt."
     ],
     "too_cold_margin": [
      "Zu kalt unter Sollwert um",
      "Bewertung: ein Raum gilt als zu kalt unter Sollwert minus diesem Wert (Lüften ausgenommen)."
     ],
     "too_cold_minutes": [
      "Minuten zu kalt für Heizbedarf",
      "Bewertung: so viele Minuten zu kalt bedeuten Heizbedarf."
     ]
    },
    "sections": {
     "learning_steps": {
      "name": "Lernschritte",
      "description": "Wie stark sich Heizgrenze und Reserve nach einem bewerteten Fehler ändern.",
      "fields": {
       "theta_step_up": [
        "Heizgrenze: Schritt nach oben",
        "Nach Fehler A, also wenn es an einem Tag ohne Heizen zu kalt wurde (z. B. 1,0 K)."
       ],
       "theta_step_down": [
        "Heizgrenze: Schritt nach unten",
        "Nach Fehler B, also wenn geheizt wurde, obwohl es nicht nötig war (z. B. 1,0 K)."
       ],
       "puffer_step_up": [
        "Reserve über Sollwert: Schritt nach oben",
        "Nach Fehler A für den kalten Raum."
       ],
       "puffer_step_down": [
        "Reserve über Sollwert: Schritt nach unten",
        "Nach Fehler B."
       ]
      }
     },
     "phases": {
      "name": "Entscheidungsphasen",
      "description": "Wann die Heiztag-Entscheidung zwischen KI führt, gemeinsam und Regel führt wechselt.",
      "fields": {
       "phase_shared_min_days": [
        "Tage bis gemeinsame Entscheidung",
        "Wer über den Heiztag entscheidet: zuerst führt die KI, dann entscheiden KI und Regel gemeinsam, zuletzt führt die Regel. 'KI führt' -> 'gemeinsam' nach so vielen bewerteten Tagen (z. B. 14)."
       ],
       "phase_shared_min_agreement": [
        "Übereinstimmung für gemeinsam",
        "Mindest-Übereinstimmung von Regel und KI."
       ],
       "phase_rule_min_days": [
        "Tage bis Regel führt",
        "Phase 'gemeinsam' -> 'Regel führt' nach so vielen Tagen in 'gemeinsam'."
       ],
       "phase_rule_min_agreement": [
        "Übereinstimmung für Regel führt",
        "Mindest-Übereinstimmung von Regel und KI."
       ],
       "phase_max_rule_errors": [
        "Erlaubte Regelfehler",
        "Höchstens so viele Regelfehler im Zeitraum für einen Phasenwechsel."
       ],
       "phase_fallback_errors_7d": [
        "Regelfehler in 7 Tagen für Rückfall",
        "So viele Regelfehler in 7 Tagen führen eine Phase zurück."
       ],
       "phase_ai_check_every_days": [
        "KI-Kontrolle alle",
        "Wenn die Regel führt und sicher ist, wird die KI trotzdem alle so viele Tage gefragt."
       ]
      }
     }
    }
   },
   "options.heating_ai_limits": {
    "title": "KI-Grenzen",
    "fields": {},
    "sections": {
     "hysteresis_on": {
      "name": "Einschalt-Hysterese",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "hysteresis_off": {
      "name": "Ausschalt-Hysterese",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "overshoot_factor": {
      "name": "Faktor Überschwingen",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "lead_factor": {
      "name": "Faktor Vorlauf",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "sun_factor": {
      "name": "Sonnenfaktor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "window_delay_min": {
      "name": "Fensterverzögerung",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "recovery_bias_min": {
      "name": "Korrektur Erholungszeit",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "puffer": {
      "name": "Reserve über Sollwert (puffer)",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "theta": {
      "name": "Heizgrenze (theta)",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "rh_threshold": {
      "name": "Feuchte-Schwelle",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "rh_hysteresis": {
      "name": "Feuchte-Hysterese",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "min_ah_advantage": {
      "name": "Mindest-Trocknungsvorteil",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "max_reference_excess": {
      "name": "Draußen höchstens wärmer um",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "min_rh_drop": {
      "name": "Mindest-Feuchteabfall durch Lüften",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "min_cooling_advantage": {
      "name": "Mindest-Kühlvorteil",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "cooling_margin": {
      "name": "Kühl-Abstand über Sollwert",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "cooling_min_temp": {
      "name": "Kühlen erst ab Raumtemperatur",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "energy_rh_per_k": {
      "name": "Energiespar-Zuschlag",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "mould_rh": {
      "name": "Schimmelgrenze",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "airing_target_below": {
      "name": "Lüftziel unter der Schwelle",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "airing_time_factor": {
      "name": "Lüftdauer-Faktor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "airing_min_minutes": {
      "name": "Kürzeste Lüftdauer",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "airing_max_minutes": {
      "name": "Längste Lüftdauer",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     },
     "airing_pause_min": {
      "name": "Pause nach dem Lüften",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. Änderung je Prüfung",
        ""
       ]
      }
     }
    }
   },
   "room.user": {
    "title": "Raum",
    "fields": {
     "name": [
      "Name",
      "Name des Raums, auch für das Gerät und seine Entitäten."
     ],
     "area": [
      "Bereich (Home Assistant)",
      "Optional. Das Gerät des Raums kommt in diesen Bereich; seine Etage zählt für das Querlüften."
     ]
    },
    "sections": {
     "sensors": {
      "name": "Sensoren",
      "description": "",
      "fields": {
       "temperature_sensor": [
        "Temperatursensor",
        "Raumtemperatur. Ohne Sensor hat der Raum keine Heizung und keine Lüftungsempfehlung (z. B. ein Raum nur für Rollos)."
       ],
       "humidity_sensor": [
        "Feuchtesensor",
        "Relative Luftfeuchte, nötig für die Lüftungsempfehlung."
       ]
      }
     },
     "heating": {
      "name": "Heizkreis",
      "description": "",
      "fields": {
       "heater_switch": [
        "Heizkreis-Schalter",
        "Schalter des Stellantriebs (z. B. ein Relais). Leer lassen für einen Raum nur mit Lüftungsempfehlung."
       ],
       "default_target": [
        "Start-Sollwert",
        "Sollwert, bis du ihn an der Thermostatkarte änderst."
       ],
       "min_target": [
        "Kleinster Sollwert",
        "Kleinster Wert der Thermostatkarte."
       ],
       "max_target": [
        "Größter Sollwert",
        "Größter Wert der Thermostatkarte."
       ],
       "min_on_time": [
        "Mindest-Einschaltzeit",
        "Wird immer eingehalten (schont den Stellantrieb). Wird nicht gelernt."
       ],
       "min_off_time": [
        "Mindest-Ausschaltzeit",
        "Wird immer eingehalten. Wird nicht gelernt."
       ],
       "heating_type": [
        "Heizungsart",
        "Wie der Kreis heizt. Ein Fußboden speichert Wärme über Stunden, Heizkörper reagieren in Minuten; die KI beurteilt die gelernten Werte entsprechend."
       ]
      }
     },
     "start_values": {
      "name": "Startwerte (werden gelernt)",
      "description": "Nur beim Anlegen des Raums. Danach werden die gelernten Werte bearbeitet.",
      "fields": {
       "window_delay": [
        "Fensterverzögerung (Startwert)",
        "So lange offen pausiert die Heizung. Die KI darf den Wert anpassen."
       ],
       "recovery_time": [
        "Erholungszeit nach Lüften (Startwert)",
        "Nach dem Schließen wird so lange gewartet, weil Estrich und Wände den Raum oft selbst aufheizen. Wird danach gelernt."
       ],
       "dead_time": [
        "Totzeit bis der Raum wärmer wird (Startwert)",
        "Zeit vom Einschalten, bis der Raum wärmer wird; bei Fußbodenheizung oft 30-90 min, bei Heizkörpern 5-20 min. Wird danach gelernt."
       ],
       "puffer": [
        "Reserve über Sollwert (Startwert)",
        "Heiztag-Regel: wie weit ein Raum beim Nachtlauf über dem Sollwert liegen muss, um einen Tag ohne Heizen zu überstehen (z. B. 0,7 K). Wird danach gelernt."
       ]
      }
     },
     "ventilation": {
      "name": "Lüftung",
      "description": "",
      "fields": {
       "ventilation_rh_threshold": [
        "Feuchte-Schwelle",
        "Startwert der relativen Feuchte, ab der Lüften empfohlen wird (z. B. 65 % für Bäder); die KI-Lüftungsprüfung passt ihn an den Raum an."
       ],
       "reference_temperature": [
        "Referenz-Temperatur statt außen",
        "Optional, für Räume, die über einen anderen Raum gelüftet werden."
       ],
       "reference_humidity": [
        "Referenz-Feuchte statt außen",
        "Zusammen mit der Referenz-Temperatur nötig."
       ],
       "ventilation_block_entity": [
        "Lüftungs-Sperr-Entität",
        "Optional. Solange sie sperrt, wird kein Lüften empfohlen: eine Abdeckung (cover), solange sie geschlossen ist (z. B. Beschattung unten), eine Klima-Entität oder ein Warmwasserbereiter, solange nicht aus (z. B. Klimaanlage läuft), ein Schalter, Binärsensor, Ventilator o. Ä., solange an."
       ]
      }
     },
     "draft": {
      "name": "Luftzug aus anderen Räumen",
      "description": "Fenster anderer Räume, deren gemeinsames Öffnen auch diesen Raum auskühlt (Querlüftung). Je Kombination die Fenster wählen, die zusammen offen sein müssen. Sobald alle Fenster einer Kombination offen sind, verhält sich der Raum wie bei einem eigenen offenen Fenster: Die Heizung pausiert nach der Fensterverzögerung und wartet danach die Erholungszeit ab. Eine Kombination mit nur einem Fenster löst schon allein aus.",
      "fields": {
       "draft_group_1": [
        "Kombination 1",
        "z. B. Kinderzimmer + Bad; eine zweite Kombination z. B. Kinderzimmer + Schlafzimmer."
       ],
       "draft_group_2": [
        "Kombination 2",
        ""
       ],
       "draft_group_3": [
        "Kombination 3",
        ""
       ],
       "draft_group_4": [
        "Kombination 4",
        ""
       ]
      }
     },
     "sun_protection": {
      "name": "Sonnenschutz",
      "description": "Vorgaben für die Rollos der Fenster dieses Raums. Raumtemperatur und Sollwert kommen vom Temperatursensor und vom Thermostat des Raums, solange ein Fenster keine eigene Raumtemperatur hat.",
      "fields": {
       "cooling_entity": [
        "Klimaanlage",
        "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage. Gilt für alle Fenster des Raums ohne eigene Klimaanlage."
       ]
      }
     }
    }
   },
   "room.reconfigure": {
    "title": "Raum",
    "fields": {
     "name": [
      "Name",
      "Name des Raums, auch für das Gerät und seine Entitäten."
     ],
     "area": [
      "Bereich (Home Assistant)",
      "Optional. Das Gerät des Raums kommt in diesen Bereich; seine Etage zählt für das Querlüften."
     ]
    },
    "sections": {
     "sensors": {
      "name": "Sensoren",
      "description": "",
      "fields": {
       "temperature_sensor": [
        "Temperatursensor",
        "Raumtemperatur. Ohne Sensor hat der Raum keine Heizung und keine Lüftungsempfehlung (z. B. ein Raum nur für Rollos)."
       ],
       "humidity_sensor": [
        "Feuchtesensor",
        "Relative Luftfeuchte, nötig für die Lüftungsempfehlung."
       ]
      }
     },
     "heating": {
      "name": "Heizkreis",
      "description": "",
      "fields": {
       "heater_switch": [
        "Heizkreis-Schalter",
        "Schalter des Stellantriebs (z. B. ein Relais). Leer lassen für einen Raum nur mit Lüftungsempfehlung."
       ],
       "default_target": [
        "Start-Sollwert",
        "Sollwert, bis du ihn an der Thermostatkarte änderst."
       ],
       "min_target": [
        "Kleinster Sollwert",
        "Kleinster Wert der Thermostatkarte."
       ],
       "max_target": [
        "Größter Sollwert",
        "Größter Wert der Thermostatkarte."
       ],
       "min_on_time": [
        "Mindest-Einschaltzeit",
        "Wird immer eingehalten (schont den Stellantrieb). Wird nicht gelernt."
       ],
       "min_off_time": [
        "Mindest-Ausschaltzeit",
        "Wird immer eingehalten. Wird nicht gelernt."
       ],
       "heating_type": [
        "Heizungsart",
        "Wie der Kreis heizt. Ein Fußboden speichert Wärme über Stunden, Heizkörper reagieren in Minuten; die KI beurteilt die gelernten Werte entsprechend."
       ]
      }
     },
     "learned_values": {
      "name": "Gelernte Werte",
      "description": "Werte, mit denen gerade geregelt wird. Eine Änderung ersetzt den gelernten bzw. von der KI angepassten Wert; danach wird von hier aus weiter gelernt.",
      "fields": {
       "window_delay": [
        "Fensterverzögerung",
        "So lange offen pausiert die Heizung. Die KI darf den Wert anpassen."
       ],
       "recovery_time": [
        "Erholungszeit nach Lüften",
        "Gelernte Wartezeit nach dem Schließen der Fenster."
       ],
       "dead_time": [
        "Totzeit bis der Raum wärmer wird",
        "Gelernte Zeit, bis der Raum nach dem Einschalten wärmer wird."
       ],
       "puffer": [
        "Reserve über Sollwert",
        "Heiztag-Regel: nötiger Abstand über dem Sollwert beim Nachtlauf (gelernt)."
       ]
      }
     },
     "ventilation": {
      "name": "Lüftung",
      "description": "",
      "fields": {
       "ventilation_rh_threshold": [
        "Feuchte-Schwelle",
        "Startwert der relativen Feuchte, ab der Lüften empfohlen wird (z. B. 65 % für Bäder); die KI-Lüftungsprüfung passt ihn an den Raum an."
       ],
       "reference_temperature": [
        "Referenz-Temperatur statt außen",
        "Optional, für Räume, die über einen anderen Raum gelüftet werden."
       ],
       "reference_humidity": [
        "Referenz-Feuchte statt außen",
        "Zusammen mit der Referenz-Temperatur nötig."
       ],
       "ventilation_block_entity": [
        "Lüftungs-Sperr-Entität",
        "Optional. Solange sie sperrt, wird kein Lüften empfohlen: eine Abdeckung (cover), solange sie geschlossen ist (z. B. Beschattung unten), eine Klima-Entität oder ein Warmwasserbereiter, solange nicht aus (z. B. Klimaanlage läuft), ein Schalter, Binärsensor, Ventilator o. Ä., solange an."
       ]
      }
     },
     "draft": {
      "name": "Luftzug aus anderen Räumen",
      "description": "Fenster anderer Räume, deren gemeinsames Öffnen auch diesen Raum auskühlt (Querlüftung). Je Kombination die Fenster wählen, die zusammen offen sein müssen. Sobald alle Fenster einer Kombination offen sind, verhält sich der Raum wie bei einem eigenen offenen Fenster: Die Heizung pausiert nach der Fensterverzögerung und wartet danach die Erholungszeit ab. Eine Kombination mit nur einem Fenster löst schon allein aus.",
      "fields": {
       "draft_group_1": [
        "Kombination 1",
        "z. B. Kinderzimmer + Bad; eine zweite Kombination z. B. Kinderzimmer + Schlafzimmer."
       ],
       "draft_group_2": [
        "Kombination 2",
        ""
       ],
       "draft_group_3": [
        "Kombination 3",
        ""
       ],
       "draft_group_4": [
        "Kombination 4",
        ""
       ]
      }
     },
     "sun_protection": {
      "name": "Sonnenschutz",
      "description": "Vorgaben für die Rollos der Fenster dieses Raums. Raumtemperatur und Sollwert kommen vom Temperatursensor und vom Thermostat des Raums, solange ein Fenster keine eigene Raumtemperatur hat.",
      "fields": {
       "cooling_entity": [
        "Klimaanlage",
        "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage. Gilt für alle Fenster des Raums ohne eigene Klimaanlage."
       ]
      }
     }
    }
   },
   "group.user": {
    "title": "Gruppe",
    "fields": {
     "name": [
      "Name",
      "Wird auch für das Gerät und seine Entitäten verwendet."
     ],
     "azimuth_from": [
      "Azimut von",
      "Sonnenrichtung, ab der die Sonne auf die Fenster scheint (90 ° = Ost, 180 ° = Süd, 270 ° = West). Die Grenzen selbst zählen nicht."
     ],
     "azimuth_to": [
      "Azimut bis",
      "Erreicht die Sonne diese Richtung, öffnen geschützte Rollos wieder (Auto-Hoch)."
     ],
     "radiation_sensors": [
      "Strahlungssensoren",
      "Sonnenstrahlung in W/m², z. B. von einem Wetterdienst oder einer Wetterstation."
     ],
     "pv_sensors": [
      "PV-Leistungssensoren",
      "Leistung einer PV-Anlage oder eines Moduls in diese Richtung (W)."
     ],
     "lux_sensors": [
      "Helligkeitssensoren",
      "Lux-Sensoren an den Fenstern. Jeder Sensor der Gruppe muss die Schwelle des Fensters erreichen."
     ]
    },
    "sections": {}
   },
   "group.reconfigure": {
    "title": "Gruppe",
    "fields": {
     "name": [
      "Name",
      "Wird auch für das Gerät und seine Entitäten verwendet."
     ],
     "azimuth_from": [
      "Azimut von",
      "Sonnenrichtung, ab der die Sonne auf die Fenster scheint (90 ° = Ost, 180 ° = Süd, 270 ° = West). Die Grenzen selbst zählen nicht."
     ],
     "azimuth_to": [
      "Azimut bis",
      "Erreicht die Sonne diese Richtung, öffnen geschützte Rollos wieder (Auto-Hoch)."
     ],
     "radiation_sensors": [
      "Strahlungssensoren",
      "Sonnenstrahlung in W/m², z. B. von einem Wetterdienst oder einer Wetterstation."
     ],
     "pv_sensors": [
      "PV-Leistungssensoren",
      "Leistung einer PV-Anlage oder eines Moduls in diese Richtung (W)."
     ],
     "lux_sensors": [
      "Helligkeitssensoren",
      "Lux-Sensoren an den Fenstern. Jeder Sensor der Gruppe muss die Schwelle des Fensters erreichen."
     ]
    },
    "sections": {}
   },
   "window.basics": {
    "title": "Fenster",
    "fields": {
     "name": [
      "Name",
      "Wird auch für das Gerät und seine Entitäten verwendet."
     ],
     "room": [
      "Raum",
      "Optional. Die Heizung des Raums nutzt die Kontakte des Fensters; das Rollo nimmt Raumtemperatur und Klimaanlage des Raums."
     ],
     "size": [
      "Größe",
      "Wie schnell Lüften die Luft austauscht: Die vorgeschlagene Lüftdauer richtet sich danach, und zum Lüften wird die größte Öffnung vorgeschlagen. Die Größe gilt für jeden Kontakt des Fensters."
     ],
     "cover": [
      "Rollo",
      "Optional. 100 % = offen, 0 % = zu. Ohne Rollo dient das Fenster nur der Heizung."
     ],
     "window_sensors": [
      "Fensterkontakte",
      "'on' = offen. Fenstergriffe mit den Zuständen open, tilted und closed gehen auch. Unbekannt oder nicht verfügbar zählt als offen. Ein Kontakt gehört zu genau einem Fenster."
     ],
     "tilt_sensors": [
      "Kipp-Kontakte",
      "'on' = gekippt. Solange das Fenster nur gekippt ist, schließen die Rollos höchstens bis zur Lüftungsposition."
     ],
     "group": [
      "Gruppe",
      "Himmelsrichtung. Ohne Gruppe hat das Fenster keinen Sonnenschutz."
     ]
    },
    "sections": {}
   },
   "window.sun": {
    "title": "Sonnenschutz",
    "fields": {
     "radiation_threshold": [
      "Strahlungsschwelle",
      "Jeder Strahlungssensor der Gruppe muss diesen Wert erreichen."
     ],
     "pv_threshold": [
      "PV-Schwelle",
      "Jeder PV-Sensor der Gruppe muss diesen Wert erreichen."
     ],
     "lux_threshold": [
      "Helligkeitsschwelle",
      "Jeder Helligkeitssensor der Gruppe muss diesen Wert erreichen."
     ],
     "temperature_threshold": [
      "Außentemperatur mindestens",
      "Sonnenschutz erst ab dieser Außentemperatur."
     ],
     "temperature_hold": [
      "Haltezeit Temperatur",
      "So lange muss die Außentemperatur darüber liegen. Darunter endet die Bedingung sofort."
     ],
     "room_entity": [
      "Raumtemperatur",
      "Optional: Thermostat (climate) oder Temperatursensor des Raums. Dann wird nur abgesenkt, wenn der Raum zu warm ist. Ohne Wert gilt die Bedingung als erfüllt (außer am Heiztag)."
     ],
     "room_margin": [
      "Zu warm ab Sollwert plus",
      "Bei einem Thermostat: zu warm ab dessen Sollwert plus diesem Abstand."
     ],
     "room_threshold": [
      "Zu warm ab",
      "Bei einem Temperatursensor (oder einem Thermostat ohne Sollwert): zu warm ab dieser Temperatur."
     ],
     "cooling_entity": [
      "Klimaanlage",
      "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage."
     ],
     "sun_hold": [
      "Haltezeit Sonne",
      "So lange müssen Sommertag, Temperatur, Raum und alle Sonnensensoren erfüllt sein. Die Bedingung endet sofort."
     ],
     "sun_position": [
      "Sonnenschutz-Position",
      "Einmal am Tag auf diese Position. Ein schon weiter geschlossenes Rollo bleibt, wie es ist."
     ],
     "position_tolerance": [
      "Toleranz für Auto-Hoch",
      "Auto-Hoch öffnet nur Rollos, die auf der Sonnenschutz-Position bis so viel darüber stehen. Von Hand anders gestellte Rollos bleiben."
     ],
     "auto_up": [
      "Auto-Hoch",
      "Wieder öffnen, wenn die Sonne den Bereich verlässt (nicht im Abendmodus)."
     ],
     "notify_open_window": [
      "Bei offenem Fenster benachrichtigen",
      "Einmal am Tag, wenn ein offenes Fenster den Sonnenschutz verhindert hat."
     ],
     "manual_max_position": [
      "Manueller Sonnenschutz bis",
      "Ein bei Sonne von Hand höchstens auf diese Position gefahrenes Rollo gilt heute als Sonnenschutz (keine Automatikfahrt)."
     ],
     "manual_detection_window": [
      "Erkennungszeitraum",
      "Die manuelle Bewegung darf höchstens so lange her sein."
     ],
     "manual_follow_up": [
      "Nachlauf der Sonnenbedingung",
      "Für diese Erkennung zählt die Sonnenbedingung (ohne Temperatur) noch so lange nach ihrem Ende."
     ],
     "manual_at_sun_position": [
      "Fahrt auf Sonnenschutz-Position zählt",
      "Ein bei Sonne von irgendwem auf die Sonnenschutz-Position (bis zur Toleranz) gefahrenes Rollo gilt wie automatischer Sonnenschutz und öffnet wieder mit Auto-Hoch."
     ]
    },
    "sections": {}
   },
   "window.behavior": {
    "title": "Verhalten",
    "fields": {},
    "sections": {
     "override": {
      "name": "Manuelle Übersteuerung",
      "description": "",
      "fields": {
       "override_duration": [
        "Dauer",
        "Nach einer manuellen Bewegung pausiert die Automatik so lange für das Fenster. Jede weitere Bewegung startet sie neu. 0 = bis Sonnenaufgang."
       ],
       "override_sunrise_reset": [
        "Auch bei Sonnenaufgang beenden",
        "Die Übersteuerung endet zusätzlich beim nächsten Sonnenaufgang, auch wenn die Dauer noch läuft."
       ],
       "override_ignore_evening": [
        "Abend- und Urlaubsfahrten trotz Übersteuerung",
        "z. B. Schlafräume, die abends immer schließen sollen."
       ]
      }
     },
     "conditions": {
      "name": "Zusatzbedingungen",
      "description": "",
      "fields": {
       "open_block_entity": [
        "Öffnungssperre",
        "Kein automatisches Öffnen (Auto-Hoch, Lüften, Urlaub morgens, Morgenöffnung), außer die Entität hat einen der Freigabe-Zustände (z. B. ein Fernseher)."
       ],
       "open_block_free_states": [
        "Freigabe-Zustände",
        "Zustände der Öffnungssperre, in denen trotzdem geöffnet wird (z. B. off, standby)."
       ],
       "close_trigger_entities": [
        "Schließ-Auslöser",
        "Wird eine dieser Entitäten aktiv, schließt das Rollo einmal pro Aktiv-Zyklus, nur bei geschlossenem Fenster (sonst sobald es zu ist). Der Zyklus endet, wenn alle inaktiv sind."
       ],
       "close_trigger_active_states": [
        "Aktiv-Zustände",
        "Zustände, in denen ein Schließ-Auslöser als aktiv gilt (z. B. on, playing beim Fernseher)."
       ],
       "close_trigger_on_delay": [
        "Aktiv nach",
        "So lange muss ein Auslöser aktiv sein, bevor das Rollo schließt (kurzes Einschalten zählt nicht)."
       ],
       "close_trigger_off_delay": [
        "Inaktiv nach",
        "So lange müssen alle Auslöser inaktiv sein, bis der Zyklus endet und ein neues Einschalten wieder schließt."
       ],
       "close_trigger_min_position": [
        "Nur wenn weiter offen als",
        "Schließt nur, wenn das Rollo weiter offen steht als diese Position."
       ],
       "close_trigger_max_lock": [
        "Zyklus höchstens",
        "Spätestens nach dieser Zeit beginnt ein neuer Zyklus, auch wenn die Auslöser die ganze Zeit aktiv waren."
       ],
       "window_exception_entity": [
        "Fenster-Ausnahme",
        "Solange diese Entität verfügbar ist, verhindert ein offenes Fenster keine Schließfahrten und es gibt keine Nachricht (z. B. Klimaanlage mit Schlauch durch die Balkontür). Gilt nicht für den Urlaubsabend."
       ]
      }
     },
     "evening": {
      "name": "Abend",
      "description": "",
      "fields": {
       "evening_close": [
        "Abendlauf",
        "Zu Beginn des Abendmodus schließen, einmal pro Abend und nur bei geschlossenem Fenster."
       ],
       "evening_position": [
        "Abendposition",
        "Ziel des Abendlaufs und des Nachziehens. 0 % = zu; z. B. 20 % lässt in warmen Nächten einen Spalt."
       ],
       "follow_up_close": [
        "Nachziehen",
        "Wird das Fenster am Abend geschlossen, fährt das Rollo zu (auch bei Übersteuerung)."
       ],
       "evening_custom": [
        "Eigene Abendzeiten",
        "Die folgenden Werte statt der globalen verwenden."
       ],
       "evening_earliest": [
        "Abendmodus frühestens",
        "Vor dieser Uhrzeit beginnt der Abendmodus nie."
       ],
       "evening_elevation": [
        "Sonnenhöhe",
        "Der Abendmodus beginnt, wenn die Sonne unter diese Höhe sinkt (z. B. -4 °)."
       ],
       "evening_latest": [
        "Abendmodus spätestens",
        "Zeit-Fallback: spätestens um diese Uhrzeit beginnt der Abendmodus."
       ]
      }
     },
     "ventilation_settings": {
      "name": "Lüften und Urlaub",
      "description": "",
      "fields": {
       "ventilation": [
        "Lüften beim Öffnen des Fensters",
        "Beim Öffnen des Fensters fährt ein geschlossenes Rollo auf die Lüftungsposition (abends nach der kurzen, tagsüber nach der langen Verzögerung)."
       ],
       "ventilation_position": [
        "Lüftungsposition",
        "Position beim Lüften (100 % = offen)."
       ],
       "closed_position": [
        "Gilt als geschlossen bis",
        "Für Lüften und Urlaub morgens."
       ],
       "ventilation_delay_evening": [
        "Verzögerung abends",
        "Im Abendmodus fährt das Rollo nach dieser kurzen Zeit auf die Lüftungsposition."
       ],
       "ventilation_delay_day": [
        "Verzögerung tagsüber",
        "Das Fenster muss danach noch offen sein."
       ],
       "vacation": [
        "Urlaubssimulation",
        "An der zufälligen Öffnung und Schließung im Urlaub teilnehmen."
       ]
      }
     },
     "protection": {
      "name": "Wetterschutz & Tür",
      "description": "",
      "fields": {
       "weather_protection": [
        "Wetterschutz für dieses Fenster",
        "Aus = Wind, Regen und Frost fahren oder begrenzen dieses Rollo nie, egal was unten eingetragen ist. Für jedes Fenster einschalten, das mitmachen soll. Mit ausgeschalteter Automatik (global oder für dieses Fenster) gibt es auch keinen Wetterschutz."
       ],
       "wind_position": [
        "Position bei Wind",
        "Leer = nicht betroffen. Z. B. 100 % fährt Raffstores hoch. Nur mit eingeschaltetem Wetterschutz des Fensters."
       ],
       "window_wind_threshold": [
        "Eigene Windschwelle",
        "Leer = Windschutz ab der Schwelle der Grundeinstellungen. Sonst schützt dieses Fenster schon oder erst ab diesem Wert (Einheit des Windsensors)."
       ],
       "rain_position": [
        "Position bei Regen",
        "Leer = nicht betroffen. Z. B. 0 % für ein Dachfenster."
       ],
       "frost_position": [
        "Tiefste Position bei Frost",
        "Leer = aus. Bei Frost stoppt das Schließen hier, damit das Rollo nicht anfriert, z. B. 5 %."
       ],
       "protection_keep_closed": [
        "Weiter geschlossen gilt als geschützt",
        "Ein Rollo, das schon weiter zu ist als seine Position bei Wind oder Regen, wird nicht dorthin hochgefahren (z. B. zu auf 0 % bei Wind-Position 20 %). Nicht bei 100 %: Raffstores einfahren läuft immer."
       ],
       "lockout_protection": [
        "Aussperrschutz (Tür)",
        "Solange der Kontakt offen meldet, fährt nichts unter die Lüftungsposition, auch nicht mit Fenster-Ausnahme oder Wetterschutz."
       ]
      }
     }
    }
   },
   "window.morning": {
    "title": "Morgenöffnung",
    "fields": {
     "morning_enabled": [
      "Morgenöffnung",
      "Das Rollo morgens automatisch öffnen."
     ],
     "morning_mode": [
      "Modus",
      "Wodurch die Morgenöffnung ausgelöst wird; die Einstellungen dazu folgen im nächsten Schritt."
     ],
     "morning_earliest": [
      "Frühestens",
      "Vorher öffnet das Rollo nie, auch wenn der Auslöser früher kommt."
     ],
     "morning_latest": [
      "Spätestens",
      "Hat bis dahin nichts ausgelöst, öffnet das Rollo zu dieser Zeit."
     ],
     "morning_position": [
      "Zielposition",
      "100 = offen, weniger = Teilöffnung."
     ],
     "morning_sun_position": [
      "Direkt auf Sonnenschutz, falls nötig",
      "Gilt die Sonnenbedingung, nur bis zur Sonnenschutz-Position öffnen."
     ]
    },
    "sections": {}
   },
   "window.morning_time": {
    "title": "Morgenöffnung nach Uhrzeit",
    "fields": {
     "morning_time_workday": [
      "Werktags",
      "Uhrzeit an Werktagen (Werktag-Sensor oder Wochenendtage)."
     ],
     "morning_time_weekend": [
      "Wochenende und Feiertage",
      "Uhrzeit am Wochenende und an Feiertagen (Feiertage nur mit Werktag-Sensor)."
     ]
    },
    "sections": {}
   },
   "window.morning_sun": {
    "title": "Morgenöffnung nach Sonnenstand",
    "fields": {
     "morning_sun_event": [
      "Ereignis",
      "Sonnenaufgang oder das Erreichen einer Sonnenhöhe."
     ],
     "morning_sun_elevation": [
      "Sonnenhöhe",
      "Nur für Sonnenhöhe: öffnet, wenn die aufgehende Sonne diese Höhe erreicht."
     ],
     "morning_sun_offset": [
      "Versatz",
      "Minuten vor (negativ) oder nach dem Ereignis."
     ]
    },
    "sections": {}
   },
   "window.morning_brightness": {
    "title": "Morgenöffnung nach Helligkeit",
    "fields": {
     "morning_lux_threshold": [
      "Helligkeit",
      "Jeder Helligkeitssensor der Gruppe muss diesen Wert erreichen."
     ],
     "morning_lux_hold": [
      "Haltezeit",
      "So lange muss es hell genug sein, bevor das Rollo öffnet."
     ]
    },
    "sections": {}
   },
   "window.morning_trigger": {
    "title": "Morgenöffnung nach Auslöser",
    "fields": {
     "morning_trigger_entity": [
      "Auslöser-Entität",
      "Ein Zeitstempel (z. B. nächster Wecker des Handys) öffnet zu dieser Zeit plus Versatz. Jede andere Entität öffnet, wenn sie angeht (Bewegung, Schalter)."
     ],
     "morning_trigger_offset": [
      "Versatz",
      "Nur für Zeitstempel."
     ]
    },
    "sections": {}
   },
   "window.reconfigure": {
    "title": "Fenster ändern",
    "fields": {},
    "sections": {}
   },
   "meter.user": {
    "title": "Neuer Zähler",
    "fields": {
     "name": [
      "Name",
      ""
     ],
     "meter_type": [
      "Zählerart",
      ""
     ]
    },
    "sections": {}
   },
   "meter.details": {
    "title": "{name}",
    "fields": {},
    "sections": {
     "camera_section": {
      "name": "Kamera und Licht",
      "description": "Kamera am Zähler und das Licht, das für das Bild eingeschaltet wird.",
      "fields": {
       "camera": [
        "Kamera",
        "Kamera-Entität, die auf die Anzeige zeigt (z. B. ESP32-CAM mit ESPHome)."
       ],
       "light": [
        "Licht",
        "Optional. Wird für das Bild ein- und danach wieder ausgeschaltet (z. B. die Blitz-LED)."
       ],
       "light_brightness": [
        "Helligkeit",
        "Helligkeit des Lichts für das Bild. Am besten mit einem Testbild ausprobieren: Spiegelungen machen die Anzeige unlesbar."
       ],
       "light_brightness_2": [
        "Helligkeit 2. Bild",
        "Optional (0 = aus): Pro Versuch wird ein zweites Bild mit dieser Helligkeit aufgenommen, und die KI bekommt beide. Hilft, wenn bei einer Helligkeit ein Lichtfleck Ziffern überstrahlt und bei der anderen Ziffern zu dunkel sind. Ein Versuch dauert dadurch länger."
       ],
       "warmup": [
        "Vorlaufzeit",
        "Wartezeit nach dem Einschalten des Lichts, damit die Kamera die Belichtung anpasst."
       ],
       "discard_frames": [
        "Verworfene Bilder",
        "Bilder, die vor dem eigentlichen Bild weggeworfen werden. Kameras mit Puffer (ESP32-CAM) liefern sonst ein altes Bild ohne Licht."
       ]
      }
     },
     "external_light_section": {
      "name": "Externe Beleuchtung",
      "description": "Optional zusätzliches Licht (light- oder switch-Entität) neben dem Licht der Kamera, z. B. LED-Module. Ist es nicht erreichbar, wird ohne es abgelesen und eine Warnung ins Log geschrieben.",
      "fields": {
       "external_light": [
        "Externe Beleuchtung",
        "Optional. light- oder switch-Entität, die die Anzeige zusätzlich ausleuchtet. Leer lassen, wenn es keine gibt."
       ],
       "external_light_mode": [
        "Modus",
        "Nur während der Aufnahme: wird vor den Bildern ein- und danach wieder ausgeschaltet. Dauerlicht: wird nur eingeschaltet, falls es aus ist, und bleibt an."
       ],
       "external_light_brightness": [
        "Helligkeit",
        "Nur bei einer dimmbaren light-Entität; ein Schalter wird nur ein- und ausgeschaltet."
       ],
       "external_light_lead_time": [
        "Vorlaufzeit",
        "Wartezeit nach dem Einschalten der externen Beleuchtung, bevor das Licht der Kamera eingeschaltet wird und die Bilder aufgenommen werden."
       ],
       "external_light_turn_off": [
        "Danach ausschalten",
        "Nur im Modus „Nur während der Aufnahme“: schaltet das Licht nach den Bildern wieder aus, auch wenn Aufnahme oder Auswertung fehlschlagen."
       ]
      }
     },
     "image_section": {
      "name": "Bildausschnitt",
      "description": "Nur dieser Teil des Bildes geht an die KI. Bei Weitwinkel-Kameras auf die Anzeige zuschneiden; im Dashboard lässt sich der Ausschnitt mit der Maus aufziehen.",
      "fields": {
       "crop_left": [
        "Links",
        "Linker Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
       ],
       "crop_top": [
        "Oben",
        "Oberer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
       ],
       "crop_right": [
        "Rechts",
        "Rechter Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
       ],
       "crop_bottom": [
        "Unten",
        "Unterer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
       ],
       "rotate": [
        "Drehen",
        "Dreht das Bild im Uhrzeigersinn um diesen Winkel (negativ: gegen den Uhrzeigersinn), z. B. 90 für eine seitlich montierte Kamera oder ein paar Grad für eine schief sitzende Anzeige. Gedreht wird vor dem Zuschneiden, der Ausschnitt bezieht sich auf das gedrehte Bild."
       ],
       "exposure": [
        "Belichtung",
        "Helligkeit des Bildes für die KI: 100 % lässt es unverändert, darunter dunkler (gegen Spiegelungen und Überbelichtung), darüber heller."
       ],
       "enhance": [
        "Bild aufbereiten",
        "Macht das Bild grau, gleicht die Ausleuchtung aus und hebt den Kontrast an, bevor die KI es liest. Hilft, wenn das Licht einen hellen Fleck auf dem Displayglas und dunkle Ecken hinterlässt, oder bei blassen LCD-Segmenten. Im Live-Bild nicht zu sehen, dafür ein Testbild machen."
       ]
      }
     },
     "display_section": {
      "name": "Anzeige",
      "description": "Was die Anzeige zeigt. Die Hinweise bekommt die KI mit.",
      "fields": {
       "unit": [
        "Einheit",
        "Einheit auf der Anzeige (z. B. MWh, kWh oder m³)."
       ],
       "decimals": [
        "Nachkommastellen",
        "Anzahl der Nachkommastellen auf der Anzeige."
       ],
       "hints": [
        "Hinweise für die KI",
        "Optional. Was an dieser Anzeige besonders ist, z. B. Linien, die zu keiner Ziffer gehören, oder welche Ziffern nicht mitgelesen werden."
       ],
       "prompt": [
        "Eigene Anweisung an die KI",
        "Ersetzt die ganze automatisch erzeugte Anweisung (leer lassen für den Standard). Einheit, Nachkommastellen und Hinweise werden dann nicht mehr eingesetzt. Die KI soll weiterhin nur die Zahl oder „unlesbar“ antworten."
       ]
      }
     },
     "schedule_section": {
      "name": "Zeitplan",
      "description": "Wie oft der Zähler automatisch abgelesen wird.",
      "fields": {
       "interval": [
        "Intervall",
        "Zeit zwischen zwei automatischen Ablesungen."
       ],
       "condition_entity": [
        "Bedingung",
        "Optional. Solange diese Entität 'aus' ist, gilt das zweite Intervall (z. B. ein Heiztag-Sensor)."
       ],
       "condition_heating_day": [
        "Tage ohne Heizen wie Bedingung aus",
        "Das zweite Intervall gilt auch an Tagen ohne Heizen (Heiztag des Heizungsmoduls, nur in der Heizperiode). Ist die Heizung aus oder der Heiztag unbekannt, gilt das normale Intervall."
       ],
       "interval_off": [
        "Intervall, wenn die Bedingung aus ist",
        "Nur zusammen mit einer Bedingung oder den Tagen ohne Heizen."
       ]
      }
     },
     "checks_section": {
      "name": "Prüfungen",
      "description": "Mehrheitsentscheid und Plausibilitätsprüfung einer Ablesung.",
      "fields": {
       "max_rate": [
        "Größter Anstieg pro Stunde",
        "In der Einheit des Zählers. Ein größerer Anstieg seit der letzten gültigen Ablesung wird verworfen (z. B. 0,05 MWh = 50 kW)."
       ],
       "max_correction": [
        "Größte Korrektur",
        "In der Einheit des Zählers. Ein kleinerer Wert als zuvor wird nur übernommen, wenn er höchstens so viel kleiner ist und von weiteren Bildern bestätigt wird."
       ],
       "max_attempts": [
        "Bilder pro Ablesung",
        "Höchstens so viele Bilder, bis ein Wert zweimal gelesen wurde."
       ],
       "confirmations": [
        "Bestätigungsbilder",
        "Weitere Bilder, die alle den kleineren Wert zeigen müssen, bevor er als Korrektur übernommen wird."
       ],
       "history_hint": [
        "Letzte Stände an die KI",
        "Die KI bekommt die letzten 3 gültigen Zählerstände als Hinweis, um eine unklare Ziffer plausibel zu entscheiden. Sie soll trotzdem nur ablesen, was im Bild steht; die Prüfungen hier bleiben bestehen. Kann dazu verleiten, einen erwarteten Wert zu nennen, daher vor allem bei schwer lesbaren Anzeigen nutzen."
       ],
       "meter_ai_task_entity": [
        "Eigene KI-Aufgabe",
        "Optional. Statt der KI-Aufgabe der Integration."
       ]
      }
     },
     "notify_section": {
      "name": "Benachrichtigungen",
      "description": "Ab dem wievielten Mal in Folge eine Benachrichtigung in Home Assistant erscheint (0 = nie, 1 = sofort). Eine gültige Ablesung setzt die Zählung zurück. Gilt nur, solange in den Einstellungen der Integration Benachrichtigungen eingeschaltet sind.",
      "fields": {
       "notify_smaller": [
        "Kleiner als zuvor",
        "Wert kleiner als der letzte gültige und nicht als Korrektur bestätigt (verworfen)."
       ],
       "notify_too_large": [
        "Anstieg zu groß",
        "Wert stärker gestiegen als der größte Anstieg pro Stunde erlaubt (verworfen)."
       ],
       "notify_corrected": [
        "Korrigiert",
        "Kleinerer Wert von weiteren Bildern bestätigt und übernommen."
       ],
       "notify_failed": [
        "Unlesbar oder Fehler",
        "KI liest nichts Eindeutiges, oder Kamera bzw. KI nicht erreichbar. Unlesbare Ablesungen unterbrechen die Zählung der anderen Fälle nicht."
       ]
      }
     },
     "vacation_section": {
      "name": "Urlaub",
      "description": "Warnt, wenn im Urlaub etwas läuft: eine Meldung, ein Logbuch-Eintrag und das Ereignis house_assistant_vacation_alert, einmal je Urlaub und Fall. Gezählt ab der letzten gültigen Ablesung vor dem Urlaub. Nicht für den Wärmezähler.",
      "fields": {
       "vacation_alert": [
        "Im Urlaub warnen",
        "Standard: an beim Wasserzähler, sonst aus."
       ],
       "vacation_amount": [
        "Menge",
        "Verbrauch seit Urlaubsbeginn in Litern (Wasser, Gas) bzw. kWh (Strom), ab dem gewarnt wird. 0 = aus. Standard Wasser: 20 L."
       ],
       "vacation_rate": [
        "Mittlerer Durchfluss bzw. Leistung",
        "Mittel seit Urlaubsbeginn in L/h bzw. kW (frühestens nach einer Stunde), ab dem gewarnt wird. Bei Gas und Strom die Grundlast eintragen. 0 = aus. Standard Wasser: 5 L/h."
       ]
      }
     }
    }
   },
   "meter.reconfigure": {
    "title": "Zähler ändern",
    "fields": {
     "name": [
      "Name",
      ""
     ],
     "meter_type": [
      "Zählerart",
      ""
     ]
    },
    "sections": {
     "camera_section": {
      "name": "Kamera und Licht",
      "description": "Kamera am Zähler und das Licht, das für das Bild eingeschaltet wird.",
      "fields": {
       "camera": [
        "Kamera",
        "Kamera-Entität, die auf die Anzeige zeigt (z. B. ESP32-CAM mit ESPHome)."
       ],
       "light": [
        "Licht",
        "Optional. Wird für das Bild ein- und danach wieder ausgeschaltet (z. B. die Blitz-LED)."
       ],
       "light_brightness": [
        "Helligkeit",
        "Helligkeit des Lichts für das Bild. Am besten mit einem Testbild ausprobieren: Spiegelungen machen die Anzeige unlesbar."
       ],
       "light_brightness_2": [
        "Helligkeit 2. Bild",
        "Optional (0 = aus): Pro Versuch wird ein zweites Bild mit dieser Helligkeit aufgenommen, und die KI bekommt beide. Hilft, wenn bei einer Helligkeit ein Lichtfleck Ziffern überstrahlt und bei der anderen Ziffern zu dunkel sind. Ein Versuch dauert dadurch länger."
       ],
       "warmup": [
        "Vorlaufzeit",
        "Wartezeit nach dem Einschalten des Lichts, damit die Kamera die Belichtung anpasst."
       ],
       "discard_frames": [
        "Verworfene Bilder",
        "Bilder, die vor dem eigentlichen Bild weggeworfen werden. Kameras mit Puffer (ESP32-CAM) liefern sonst ein altes Bild ohne Licht."
       ]
      }
     },
     "external_light_section": {
      "name": "Externe Beleuchtung",
      "description": "Optional zusätzliches Licht (light- oder switch-Entität) neben dem Licht der Kamera, z. B. LED-Module. Ist es nicht erreichbar, wird ohne es abgelesen und eine Warnung ins Log geschrieben.",
      "fields": {
       "external_light": [
        "Externe Beleuchtung",
        "Optional. light- oder switch-Entität, die die Anzeige zusätzlich ausleuchtet. Leer lassen, wenn es keine gibt."
       ],
       "external_light_mode": [
        "Modus",
        "Nur während der Aufnahme: wird vor den Bildern ein- und danach wieder ausgeschaltet. Dauerlicht: wird nur eingeschaltet, falls es aus ist, und bleibt an."
       ],
       "external_light_brightness": [
        "Helligkeit",
        "Nur bei einer dimmbaren light-Entität; ein Schalter wird nur ein- und ausgeschaltet."
       ],
       "external_light_lead_time": [
        "Vorlaufzeit",
        "Wartezeit nach dem Einschalten der externen Beleuchtung, bevor das Licht der Kamera eingeschaltet wird und die Bilder aufgenommen werden."
       ],
       "external_light_turn_off": [
        "Danach ausschalten",
        "Nur im Modus „Nur während der Aufnahme“: schaltet das Licht nach den Bildern wieder aus, auch wenn Aufnahme oder Auswertung fehlschlagen."
       ]
      }
     },
     "image_section": {
      "name": "Bildausschnitt",
      "description": "Nur dieser Teil des Bildes geht an die KI. Bei Weitwinkel-Kameras auf die Anzeige zuschneiden; im Dashboard lässt sich der Ausschnitt mit der Maus aufziehen.",
      "fields": {
       "crop_left": [
        "Links",
        "Linker Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
       ],
       "crop_top": [
        "Oben",
        "Oberer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
       ],
       "crop_right": [
        "Rechts",
        "Rechter Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
       ],
       "crop_bottom": [
        "Unten",
        "Unterer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
       ],
       "rotate": [
        "Drehen",
        "Dreht das Bild im Uhrzeigersinn um diesen Winkel (negativ: gegen den Uhrzeigersinn), z. B. 90 für eine seitlich montierte Kamera oder ein paar Grad für eine schief sitzende Anzeige. Gedreht wird vor dem Zuschneiden, der Ausschnitt bezieht sich auf das gedrehte Bild."
       ],
       "exposure": [
        "Belichtung",
        "Helligkeit des Bildes für die KI: 100 % lässt es unverändert, darunter dunkler (gegen Spiegelungen und Überbelichtung), darüber heller."
       ],
       "enhance": [
        "Bild aufbereiten",
        "Macht das Bild grau, gleicht die Ausleuchtung aus und hebt den Kontrast an, bevor die KI es liest. Hilft, wenn das Licht einen hellen Fleck auf dem Displayglas und dunkle Ecken hinterlässt, oder bei blassen LCD-Segmenten. Im Live-Bild nicht zu sehen, dafür ein Testbild machen."
       ]
      }
     },
     "display_section": {
      "name": "Anzeige",
      "description": "Was die Anzeige zeigt. Die Hinweise bekommt die KI mit.",
      "fields": {
       "unit": [
        "Einheit",
        "Einheit auf der Anzeige (z. B. MWh, kWh oder m³)."
       ],
       "decimals": [
        "Nachkommastellen",
        "Anzahl der Nachkommastellen auf der Anzeige."
       ],
       "hints": [
        "Hinweise für die KI",
        "Optional. Was an dieser Anzeige besonders ist, z. B. Linien, die zu keiner Ziffer gehören, oder welche Ziffern nicht mitgelesen werden."
       ],
       "prompt": [
        "Eigene Anweisung an die KI",
        "Ersetzt die ganze automatisch erzeugte Anweisung (leer lassen für den Standard). Einheit, Nachkommastellen und Hinweise werden dann nicht mehr eingesetzt. Die KI soll weiterhin nur die Zahl oder „unlesbar“ antworten."
       ]
      }
     },
     "schedule_section": {
      "name": "Zeitplan",
      "description": "Wie oft der Zähler automatisch abgelesen wird.",
      "fields": {
       "interval": [
        "Intervall",
        "Zeit zwischen zwei automatischen Ablesungen."
       ],
       "condition_entity": [
        "Bedingung",
        "Optional. Solange diese Entität 'aus' ist, gilt das zweite Intervall (z. B. ein Heiztag-Sensor)."
       ],
       "interval_off": [
        "Intervall, wenn die Bedingung aus ist",
        "Nur zusammen mit einer Bedingung."
       ]
      }
     },
     "checks_section": {
      "name": "Prüfungen",
      "description": "Mehrheitsentscheid und Plausibilitätsprüfung einer Ablesung.",
      "fields": {
       "max_rate": [
        "Größter Anstieg pro Stunde",
        "In der Einheit des Zählers. Ein größerer Anstieg seit der letzten gültigen Ablesung wird verworfen (z. B. 0,05 MWh = 50 kW)."
       ],
       "max_correction": [
        "Größte Korrektur",
        "In der Einheit des Zählers. Ein kleinerer Wert als zuvor wird nur übernommen, wenn er höchstens so viel kleiner ist und von weiteren Bildern bestätigt wird."
       ],
       "max_attempts": [
        "Bilder pro Ablesung",
        "Höchstens so viele Bilder, bis ein Wert zweimal gelesen wurde."
       ],
       "confirmations": [
        "Bestätigungsbilder",
        "Weitere Bilder, die alle den kleineren Wert zeigen müssen, bevor er als Korrektur übernommen wird."
       ],
       "history_hint": [
        "Letzte Stände an die KI",
        "Die KI bekommt die letzten 3 gültigen Zählerstände als Hinweis, um eine unklare Ziffer plausibel zu entscheiden. Sie soll trotzdem nur ablesen, was im Bild steht; die Prüfungen hier bleiben bestehen. Kann dazu verleiten, einen erwarteten Wert zu nennen, daher vor allem bei schwer lesbaren Anzeigen nutzen."
       ],
       "meter_ai_task_entity": [
        "Eigene KI-Aufgabe",
        "Optional. Statt der KI-Aufgabe der Integration."
       ]
      }
     },
     "notify_section": {
      "name": "Benachrichtigungen",
      "description": "Ab dem wievielten Mal in Folge eine Benachrichtigung in Home Assistant erscheint (0 = nie, 1 = sofort). Eine gültige Ablesung setzt die Zählung zurück. Gilt nur, solange in den Einstellungen der Integration Benachrichtigungen eingeschaltet sind.",
      "fields": {
       "notify_smaller": [
        "Kleiner als zuvor",
        "Wert kleiner als der letzte gültige und nicht als Korrektur bestätigt (verworfen)."
       ],
       "notify_too_large": [
        "Anstieg zu groß",
        "Wert stärker gestiegen als der größte Anstieg pro Stunde erlaubt (verworfen)."
       ],
       "notify_corrected": [
        "Korrigiert",
        "Kleinerer Wert von weiteren Bildern bestätigt und übernommen."
       ],
       "notify_failed": [
        "Unlesbar oder Fehler",
        "KI liest nichts Eindeutiges, oder Kamera bzw. KI nicht erreichbar. Unlesbare Ablesungen unterbrechen die Zählung der anderen Fälle nicht."
       ]
      }
     },
     "vacation_section": {
      "name": "Urlaub",
      "description": "Warnt, wenn im Urlaub etwas läuft: eine Meldung, ein Logbuch-Eintrag und das Ereignis house_assistant_vacation_alert, einmal je Urlaub und Fall. Gezählt ab der letzten gültigen Ablesung vor dem Urlaub. Nicht für den Wärmezähler.",
      "fields": {
       "vacation_alert": [
        "Im Urlaub warnen",
        "Standard: an beim Wasserzähler, sonst aus."
       ],
       "vacation_amount": [
        "Menge",
        "Verbrauch seit Urlaubsbeginn in Litern (Wasser, Gas) bzw. kWh (Strom), ab dem gewarnt wird. 0 = aus. Standard Wasser: 20 L."
       ],
       "vacation_rate": [
        "Mittlerer Durchfluss bzw. Leistung",
        "Mittel seit Urlaubsbeginn in L/h bzw. kW (frühestens nach einer Stunde), ab dem gewarnt wird. Bei Gas und Strom die Grundlast eintragen. 0 = aus. Standard Wasser: 5 L/h."
       ]
      }
     }
    }
   }
  },
  "errors": {
   "config": {
    "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
    "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
    "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
    "name_required": "Bitte einen Namen eingeben.",
    "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
    "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
    "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
    "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
    "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
    "invalid_day_month": "Bitte ein gültiges Datum angeben (TT.MM., z. B. 01.10.); einen Tag wie den 31.02. gibt es nicht.",
    "invalid_auth": "Anthropic hat den API-Key abgelehnt. Prüfe ihn unter console.anthropic.com > API Keys und füge ihn ohne Leerzeichen ein. Ohne Key läuft die lokale Regelung weiter.",
    "cannot_connect": "Anthropic ist nicht erreichbar. Prüfe Internetverbindung, Proxy und Firewall. Der Key wurde nicht gespeichert.",
    "max_below_base": "Das maximale Intervall muss mindestens so groß sein wie das Prüfintervall (z. B. alle 4 h prüfen, höchstens alle 48 h).",
    "outdoor_required": "Bitte einen Außentemperatursensor oder eine Wetter-Entität wählen."
   },
   "options": {
    "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
    "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
    "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
    "name_required": "Bitte einen Namen eingeben.",
    "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
    "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
    "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
    "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
    "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
    "invalid_day_month": "Bitte ein gültiges Datum angeben (TT.MM., z. B. 01.10.); einen Tag wie den 31.02. gibt es nicht.",
    "invalid_auth": "Anthropic hat den API-Key abgelehnt. Prüfe ihn unter console.anthropic.com > API Keys und füge ihn ohne Leerzeichen ein. Ohne Key läuft die lokale Regelung weiter.",
    "cannot_connect": "Anthropic ist nicht erreichbar. Prüfe Internetverbindung, Proxy und Firewall. Der Key wurde nicht gespeichert.",
    "max_below_base": "Das maximale Intervall muss mindestens so groß sein wie das Prüfintervall (z. B. alle 4 h prüfen, höchstens alle 48 h).",
    "outdoor_required": "Bitte einen Außentemperatursensor oder eine Wetter-Entität wählen."
   },
   "room": {
    "name_required": "Bitte einen Namen angeben.",
    "name_in_use": "Ein anderer Raum heißt schon so. Bitte einen eindeutigen Namen wählen (Export und Import finden Räume über den Namen).",
    "switch_in_use": "Dieser Schalter steuert bereits einen anderen Raum. Jeder Heizkreis gehört zu genau einem Raum: wähle einen anderen Schalter oder entferne ihn zuerst aus dem anderen Raum.",
    "min_above_max": "Der kleinste Sollwert muss kleiner sein als der größte. Bitte einen der beiden Werte ändern (beide in °C).",
    "target_out_of_range": "Der Start-Sollwert muss zwischen dem kleinsten und dem größten Sollwert liegen. Bitte ihn oder die Grenzen anpassen.",
    "reference_incomplete": "Referenztemperatur und Referenzfeuchte gehen nur zusammen: beide Sensoren wählen oder keinen.",
    "temperature_required": "Für Heizkreis und Lüftungsempfehlung braucht der Raum einen Temperatursensor."
   },
   "group": {
    "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
    "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
    "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
    "name_required": "Bitte einen Namen eingeben.",
    "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
    "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
    "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
    "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
    "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern."
   },
   "window": {
    "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
    "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
    "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
    "name_required": "Bitte einen Namen eingeben.",
    "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
    "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
    "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
    "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
    "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
    "contact_in_use": "Dieser Kontakt gehört schon zu einem anderen Fenster. Jeder Kontakt gehört zu genau einem Fenster, sonst zählte eine Öffnung doppelt.",
    "contact_or_cover_required": "Bitte einen Fensterkontakt oder ein Rollo wählen; ohne beides tut das Fenster nichts.",
    "unknown_room": "Diesen Raum gibt es nicht mehr. Bitte einen anderen wählen."
   },
   "meter": {
    "name_required": "Bitte einen Namen eingeben.",
    "camera_required": "Bitte eine Kamera auswählen."
   }
  },
  "choices": {
   "effort": {
    "auto": "Auto (Modell-Standard)",
    "low": "Niedrig",
    "medium": "Mittel",
    "high": "Hoch"
   },
   "external_light_mode": {
    "capture": "Nur während der Aufnahme",
    "permanent": "Dauerlicht"
   },
   "forecast_type": {
    "auto": "Automatisch",
    "daily": "Täglich",
    "twice_daily": "Zweimal täglich",
    "hourly": "Stündlich"
   },
   "heating_type": {
    "underfloor": "Fußbodenheizung",
    "radiator": "Heizkörper",
    "other": "Andere (z. B. Wandheizung)"
   },
   "language": {
    "auto": "Wie Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "meter_type": {
    "heat": "Wärmezähler",
    "water": "Wasserzähler",
    "gas": "Gaszähler",
    "electricity": "Stromzähler",
    "other": "Anderer Zähler"
   },
   "modules": {
    "heating": "Heizung",
    "shutter": "Rollos",
    "meter": "Zähler"
   },
   "month": {
    "1": "Januar",
    "2": "Februar",
    "3": "März",
    "4": "April",
    "5": "Mai",
    "6": "Juni",
    "7": "Juli",
    "8": "August",
    "9": "September",
    "10": "Oktober",
    "11": "November",
    "12": "Dezember"
   },
   "morning_mode": {
    "time": "Feste Uhrzeit (Werktag / Wochenende)",
    "sun": "Sonnenstand (Aufgang oder Höhe)",
    "brightness": "Helligkeit der Gruppe",
    "trigger": "Auslöser-Entität (Wecker, Bewegung, Schalter)"
   },
   "morning_sun_event": {
    "sunrise": "Sonnenaufgang",
    "elevation": "Sonnenhöhe"
   },
   "override_trigger": {
    "movement": "Nur wenn das Rollo wirklich fährt",
    "command": "Bei jedem Befehl von Hand, auch ohne Fahrt"
   },
   "service_action": {
    "open": "Öffnen",
    "close": "Schließen",
    "evening": "Abendposition",
    "sun_protection": "Sonnenschutz-Position",
    "ventilation": "Lüftungsposition",
    "position": "Position"
   },
   "weekday": {
    "mon": "Montag",
    "tue": "Dienstag",
    "wed": "Mittwoch",
    "thu": "Donnerstag",
    "fri": "Freitag",
    "sat": "Samstag",
    "sun": "Sonntag"
   },
   "window_size": {
    "small": "Klein (z. B. Dachfenster)",
    "medium": "Mittel",
    "large": "Groß (z. B. zweiflügelig)",
    "door": "Tür (z. B. Balkontür)"
   }
  },
  "states": {
   "select.heating_day_override": {
    "auto": "Automatik",
    "heat_today": "Heute heizen",
    "off_today": "Heute nicht heizen"
   },
   "sensor.meter_status": {
    "ok": "Gültig",
    "corrected": "Korrigiert",
    "unreadable": "Unlesbar",
    "error": "Kamera- oder KI-Fehler",
    "smaller": "Kleiner als zuvor",
    "too_large": "Anstieg zu groß",
    "manual": "Von Hand gesetzt"
   },
   "sensor.next_action.action": {
    "evening": "Abendlauf",
    "morning": "Morgenöffnung",
    "override_end": "Ende der Übersteuerung",
    "sun_enter": "Sonne kommt in den Bereich",
    "sun_leave": "Sonne verlässt den Bereich",
    "protection_end": "Wetterschutz kann enden"
   },
   "sensor.window_status": {
    "off": "Automatik aus",
    "startup": "Neustart-Schutz",
    "override": "Manuelle Übersteuerung",
    "evening": "Abends geschlossen",
    "sun_protection": "Sonnenschutz",
    "vacation": "Urlaubssimulation",
    "ready": "Bereit",
    "protection": "Wetterschutz"
   },
   "sensor.ventilation": {
    "unknown": "Unbekannt",
    "close_window": "Fenster schließen",
    "ventilate_now": "Jetzt lüften",
    "ventilation_useful": "Lüften sinnvoll",
    "do_not_ventilate": "Nicht lüften",
    "blocked": "Lüften blockiert",
    "optimal": "Alles optimal",
    "vacation": "Urlaub"
   },
   "sensor.decision_phase": {
    "ai_leads": "KI führt",
    "shared": "Gemeinsam",
    "rule_leads": "Regel führt"
   },
   "sensor.room_status": {
    "off": "Aus",
    "out_of_season": "Außerhalb Heizperiode",
    "no_heating_day": "Kein Heiztag",
    "idle": "Bereit",
    "heating": "Heizt",
    "window_open": "Fenster offen",
    "recovery": "Erholung nach Lüften",
    "frost_protection": "Frostschutz",
    "vacation": "Urlaub",
    "preheat": "Vorheizen zur Rückkehr",
    "emergency": "Notfallregel",
    "sensor_error": "Sensorfehler",
    "actuator_unavailable": "Aktor nicht erreichbar",
    "no_circuit": "Kein Heizkreis"
   }
  }
 },
 "en": {
  "steps": {
   "config.user": {
    "title": "House Assistant",
    "fields": {
     "modules": [
      "Modules",
      "The parts of the house House Assistant takes care of. Can be changed later under Settings > Modules."
     ]
    },
    "sections": {}
   },
   "config.house": {
    "title": "House",
    "fields": {
     "outdoor_temperature": [
      "Outdoor temperature sensor",
      "For heating and covers (e.g. a helper combining several sensors). Without it the current temperature of the weather entity is used."
     ],
     "outdoor_humidity": [
      "Outdoor humidity sensor",
      "Optional. For the ventilation advice of the heating; without it the humidity of the weather entity is used."
     ],
     "weather": [
      "Weather entity",
      "Recommended. Its forecast is used by the heating day decision, the expected sun of the heating and the summer day of the covers. Without an outdoor sensor its current temperature applies."
     ],
     "language": [
      "Language of messages",
      "Logbook, last reason, push messages and notifications of every module. Automatic = the language of Home Assistant."
     ],
     "notify_services": [
      "Notification services",
      "Get the messages of the house, e.g. when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
     ],
     "workday_entity": [
      "Workday sensor",
      "Optional, e.g. the Workday integration (knows public holidays). Without a sensor the weekend days decide."
     ],
     "weekend_days": [
      "Weekend days",
      "Only without a workday sensor: on these days e.g. the weekend time of the morning opening applies."
     ],
     "house_azimuth": [
      "Front faces",
      "Direction the front looks to (90° = east, 180° = south, 270° = west), e.g. read from a map. For the house in the sun compass of the covers."
     ],
     "house_width": [
      "Length of the front",
      "Also the back. With the depth the house appears in the sun compass, and the draft through rooms between two open windows is recognised."
     ],
     "house_depth": [
      "Depth",
      "Length of the two side walls."
     ],
     "draft_reach": [
      "Draft reach",
      "How far a room may be from the line between two open windows of other rooms to still get their draft (default 2 m)."
     ]
    },
    "sections": {}
   },
   "config.heating": {
    "title": "Heating",
    "fields": {
     "pv_power": [
      "PV power sensor",
      "Optional. PV power (W or kW) as an indicator for sunshine. The solar gain per room is learned from it."
     ],
     "pv_forecast": [
      "PV forecast sensor",
      "Optional, only together with the PV power sensor. Expected PV energy of the next hour (Wh or kWh, e.g. Forecast.Solar) or expected power in one hour (W or kW). Without it the sun is estimated from the hourly weather forecast and the sun position."
     ],
     "heat_meter": [
      "Heat meter",
      "Optional. Meter reading of the heat meter of the circuits controlled here (Wh, kWh, MWh, MJ or GJ, e.g. total_increasing). The AI then sees the measured heat; it is also shown in the panel. Seldom and coarse readings are fine."
     ],
     "season_start": [
      "Heating period start (DD.MM.)",
      "Outside the heating period all circuits stay off (frost protection only) and the AI is not asked."
     ],
     "season_end": [
      "Heating period end (DD.MM.)",
      "Last day of the heating period, may be in the next year (e.g. 31.03.)."
     ],
     "frost_temperature": [
      "Frost protection temperature",
      "Always applies, also outside the heating period and with a switched-off thermostat."
     ],
     "forecast_trust": [
      "Trust in the sun forecast",
      "Share of the expected PV power the control relies on when it holds back heating (100 % = full forecast, 0 % = only the current PV power counts)."
     ],
     "season_start_day": [
      "Heating period starts: day",
      "Heating is possible from this date (e.g. 1 October)."
     ],
     "season_start_month": [
      "Heating period starts: month",
      ""
     ],
     "season_end_day": [
      "Heating period ends: day",
      "Last day of the heating period (e.g. 31 March); the period may span the turn of the year."
     ],
     "season_end_month": [
      "Heating period ends: month",
      ""
     ]
    },
    "sections": {}
   },
   "config.heating_vacation": {
    "title": "Vacation",
    "fields": {
     "vacation_entities": [
      "Vacation entities",
      "Any of these entities being 'on' means vacation (e.g. an input_boolean or a calendar)."
     ],
     "vacation_temperature": [
      "Vacation temperature",
      "Target for all rooms during vacation."
     ],
     "return_entity": [
      "Return date/time",
      "Optional input_datetime, timestamp sensor or datetime entity. Heating starts early enough (learned heat-up time) to reach the normal target on return."
     ],
     "preheat_reserve": [
      "Preheat reserve",
      "Additional time added to the calculated preheating time."
     ]
    },
    "sections": {}
   },
   "config.heating_decision": {
    "title": "Heating day decision",
    "fields": {
     "theta_start": [
      "Heating threshold theta (start value)",
      "Heating is needed when the forecast maximum of the day is below this value (e.g. 16 °C). Learned afterwards."
     ]
    },
    "sections": {}
   },
   "config.heating_ai": {
    "title": "AI (Claude)",
    "fields": {
     "api_key": [
      "Anthropic API key",
      "Optional. Without a key the local control runs alone. The key is only stored in Home Assistant and never logged."
     ],
     "nightly_time": [
      "Time of the nightly run",
      "Daily decision whether heating is needed today (also the start of the evaluated day). Runs with and without the AI."
     ]
    },
    "sections": {}
   },
   "config.heating_ai_model": {
    "title": "AI model and budget",
    "fields": {
     "model": [
      "Claude model",
      "Model for all AI calls. Prices below are suggestions for the selected model and can be changed."
     ],
     "monthly_budget": [
      "Monthly budget",
      "In US dollars, as Anthropic bills. No AI calls once the costs of the month reach this value (until the month changes)."
     ]
    },
    "sections": {}
   },
   "config.meter": {
    "title": "Meters",
    "fields": {
     "ai_task_entity": [
      "AI task",
      "AI task entity that reads the pictures (e.g. Anthropic, OpenAI, Google or Ollama with image support). A meter can use its own one."
     ],
     "notify_rejected": [
      "Notifications",
      "Main switch for the notifications in Home Assistant. When they come for which meter is set at the meter under \"Notifications\"."
     ]
    },
    "sections": {}
   },
   "config.shutter_summer": {
    "title": "Summer day",
    "fields": {
     "summer_threshold": [
      "Summer day from forecast high",
      "Without a summer day there is no sun protection. During the day the summer day also starts when the outdoor temperature rises above this value (see night)."
     ],
     "night_threshold": [
      "Late summer day only with a night from",
      "A summer day only by the outdoor temperature counts only when the forecast low of the coming night is at least this value. When the night cools down (spring, autumn), the warmth stays in the house. Without a low in the forecast the summer day counts as before."
     ],
     "heating_entity": [
      "Heating wanted",
      "Optional, e.g. an input_boolean \"heating season\" or the heating day of a heating control. While it is on, the warmth of the sun is welcome: sun protection only when the room of a window is too warm anyway. Windows without a room temperature are then not lowered."
     ],
     "use_heating_day": [
      "Heating day of the heating",
      "Without an own heat need entity: the heating day of the heating module, but only within the heating period. Only while the heating module is switched on."
     ],
     "day_change_time": [
      "Day change",
      "Forecast check and reset of the daily sun protection markers and notifications."
     ],
     "forecast_type": [
      "Kind of forecast",
      "Automatic takes the first kind the weather entity supports (daily, twice daily, hourly). From hourly values the high of the day and the low of the night are calculated."
     ]
    },
    "sections": {}
   },
   "config.shutter_evening": {
    "title": "Evening mode",
    "fields": {
     "evening_earliest": [
      "Evening mode at the earliest",
      "The evening mode never starts before this time."
     ],
     "evening_elevation": [
      "Sun elevation",
      "The evening mode starts when the sun drops below this elevation (e.g. -4 °)."
     ],
     "evening_latest": [
      "Evening mode at the latest",
      "Time fallback: the evening mode starts at this time at the latest."
     ],
     "night_end": [
      "End of the night",
      "Evening mode and evening markers end at this time (or at sunrise if that is earlier)."
     ],
     "follow_up_earliest": [
      "Close after window closed, from",
      "A window closed in the evening closes the cover only after this time."
     ]
    },
    "sections": {}
   },
   "config.reconfigure": {
    "title": "Change API key",
    "fields": {
     "api_key": [
      "Anthropic API key",
      "Optional. Without a key the local control runs alone. The key is only stored in Home Assistant and never logged."
     ]
    },
    "sections": {}
   },
   "config.reauth_confirm": {
    "title": "API key rejected",
    "fields": {
     "api_key": [
      "Anthropic API key",
      "Checked with Anthropic before it is saved. The key is only stored in Home Assistant and never logged."
     ]
    },
    "sections": {}
   },
   "options.init": {
    "title": "Settings",
    "fields": {},
    "sections": {}
   },
   "options.modules": {
    "title": "Modules",
    "fields": {
     "modules": [
      "Modules",
      "The parts of the house House Assistant takes care of. A module switched off keeps its settings."
     ],
     "show_panel": [
      "Dashboard in the sidebar",
      "Off: the dashboard disappears from the sidebar but stays reachable with \"Configure\" at the integration."
     ]
    },
    "sections": {}
   },
   "options.house": {
    "title": "House",
    "fields": {
     "outdoor_temperature": [
      "Outdoor temperature sensor",
      "For heating and covers (e.g. a helper combining several sensors). Without it the current temperature of the weather entity is used."
     ],
     "outdoor_humidity": [
      "Outdoor humidity sensor",
      "Optional. For the ventilation advice of the heating; without it the humidity of the weather entity is used."
     ],
     "weather": [
      "Weather entity",
      "Recommended. Its forecast is used by the heating day decision, the expected sun of the heating and the summer day of the covers. Without an outdoor sensor its current temperature applies."
     ],
     "language": [
      "Language of messages",
      "Logbook, last reason, push messages and notifications of every module. Automatic = the language of Home Assistant."
     ],
     "notify_services": [
      "Notification services",
      "Get the messages of the house, e.g. when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
     ],
     "workday_entity": [
      "Workday sensor",
      "Optional, e.g. the Workday integration (knows public holidays). Without a sensor the weekend days decide."
     ],
     "weekend_days": [
      "Weekend days",
      "Only without a workday sensor: on these days e.g. the weekend time of the morning opening applies."
     ],
     "house_azimuth": [
      "Front faces",
      "Direction the front looks to (90° = east, 180° = south, 270° = west), e.g. read from a map. For the house in the sun compass of the covers."
     ],
     "house_width": [
      "Length of the front",
      "Also the back. With the depth the house appears in the sun compass, and the draft through rooms between two open windows is recognised."
     ],
     "house_depth": [
      "Depth",
      "Length of the two side walls."
     ],
     "draft_reach": [
      "Draft reach",
      "How far a room may be from the line between two open windows of other rooms to still get their draft (default 2 m)."
     ]
    },
    "sections": {}
   },
   "options.vacation": {
    "title": "Vacation",
    "fields": {
     "vacation_entities": [
      "External vacation entities",
      "While one of them is on it is vacation as well (e.g. an input_boolean or a calendar). For heating and covers; without an entry here the entities in their settings apply."
     ],
     "return_entity": [
      "External return",
      "Optional: input_datetime, datetime or timestamp entity. The heating preheats for it; an own return of the switch comes first."
     ],
     "vacation_window_alert": [
      "Report open windows",
      "When the vacation starts a message with every open, tilted or unknown window; on vacation a message right away when a window is opened or tilted. To the notification services of the house, without any as a notification in Home Assistant."
     ]
    },
    "sections": {}
   },
   "options.meter": {
    "title": "Meters",
    "fields": {
     "ai_task_entity": [
      "AI task",
      "AI task entity that reads the pictures (e.g. Anthropic, OpenAI, Google or Ollama with image support). A meter can use its own one."
     ],
     "notify_rejected": [
      "Notifications",
      "Main switch for the notifications in Home Assistant. When they come for which meter is set at the meter under \"Notifications\"."
     ]
    },
    "sections": {}
   },
   "options.shutter": {
    "title": "Covers",
    "fields": {},
    "sections": {}
   },
   "options.shutter_general": {
    "title": "General",
    "fields": {
     "outdoor_temperature": [
      "Outdoor temperature sensor",
      "For the summer day and the temperature condition of every window. Without a sensor the current temperature of the weather entity is used (at least one of both). Only while nothing is set under Settings > House."
     ],
     "weather": [
      "Weather entity",
      "Its daily forecast decides at the day change whether today is a summer day. Only while nothing is set under Settings > House."
     ],
     "language": [
      "Language of messages",
      "Logbook, last reason and push messages. Only while nothing is set under Settings > House."
     ],
     "notify_services": [
      "Notification services",
      "Get a message when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone). Only while nothing is set under Settings > House."
     ],
     "workday_entity": [
      "Workday sensor",
      "Optional, for the morning opening by time (e.g. Workday integration, knows public holidays). Without a sensor the weekend days decide. Only while nothing is set under Settings > House."
     ],
     "weekend_days": [
      "Weekend days",
      "Only without a workday sensor: on these days the weekend time of the morning opening applies. Only while nothing is set under Settings > House."
     ]
    },
    "sections": {}
   },
   "options.shutter_override": {
    "title": "Manual override",
    "fields": {
     "override_trigger": [
      "Override starts",
      "Only with a real movement: a command to a cover already at its target (e.g. \"open all\" while it is open) does not start an override. Every command: also without movement, as before."
     ]
    },
    "sections": {}
   },
   "options.shutter_summer": {
    "title": "Summer day",
    "fields": {
     "summer_threshold": [
      "Summer day from forecast high",
      "Without a summer day there is no sun protection. During the day the summer day also starts when the outdoor temperature rises above this value (see night)."
     ],
     "night_threshold": [
      "Late summer day only with a night from",
      "A summer day only by the outdoor temperature counts only when the forecast low of the coming night is at least this value. When the night cools down (spring, autumn), the warmth stays in the house. Without a low in the forecast the summer day counts as before."
     ],
     "heating_entity": [
      "Heating wanted",
      "Optional, e.g. an input_boolean \"heating season\" or the heating day of a heating control. While it is on, the warmth of the sun is welcome: sun protection only when the room of a window is too warm anyway. Windows without a room temperature are then not lowered."
     ],
     "use_heating_day": [
      "Heating day of the heating",
      "Without an own heat need entity: the heating day of the heating module, but only within the heating period. Only while the heating module is switched on."
     ],
     "day_change_time": [
      "Day change",
      "Forecast check and reset of the daily sun protection markers and notifications."
     ],
     "forecast_type": [
      "Kind of forecast",
      "Automatic takes the first kind the weather entity supports (daily, twice daily, hourly). From hourly values the high of the day and the low of the night are calculated."
     ]
    },
    "sections": {}
   },
   "options.shutter_evening": {
    "title": "Evening mode",
    "fields": {
     "evening_earliest": [
      "Evening mode at the earliest",
      "The evening mode never starts before this time."
     ],
     "evening_elevation": [
      "Sun elevation",
      "The evening mode starts when the sun drops below this elevation (e.g. -4 °)."
     ],
     "evening_latest": [
      "Evening mode at the latest",
      "Time fallback: the evening mode starts at this time at the latest."
     ],
     "night_end": [
      "End of the night",
      "Evening mode and evening markers end at this time (or at sunrise if that is earlier)."
     ],
     "follow_up_earliest": [
      "Close after window closed, from",
      "A window closed in the evening closes the cover only after this time."
     ]
    },
    "sections": {}
   },
   "options.shutter_vacation": {
    "title": "Vacation simulation",
    "fields": {
     "vacation_entities": [
      "Vacation entities",
      "Vacation is active while one of them is on (e.g. an input_boolean \"vacation\" or a calendar). Only while nothing is set under Settings > Vacation. The switch “Vacation” of the house always counts."
     ],
     "vacation_morning_start": [
      "Vacation morning from",
      "Closed covers of the windows in the simulation open at a random time after this."
     ],
     "vacation_morning_window": [
      "Random period in the morning",
      "Each window opens at a random time within this period."
     ],
     "vacation_position_min": [
      "Opening position from",
      "Random position between both values."
     ],
     "vacation_position_max": [
      "Opening position to",
      "Random position between both values."
     ],
     "vacation_evening_start": [
      "Vacation evening from",
      "Starts the evening for the windows in the simulation and closes them at random times. The normal evening run rests during vacation."
     ],
     "vacation_evening_window": [
      "Random period in the evening",
      "Each window closes at a random time within this period."
     ],
     "vacation_heat_protection": [
      "Heat protection on vacation",
      "On vacation the sun protection lowers without waiting for room temperature, air conditioner or heat need. Summer day, outdoor temperature, sun sensors, hold times and the sun switch of the window still apply."
     ]
    },
    "sections": {}
   },
   "options.shutter_protection": {
    "title": "Weather protection",
    "fields": {
     "wind_entity": [
      "Wind sensor",
      "Wind speed or gusts, e.g. from a weather station."
     ],
     "wind_threshold": [
      "Wind protection from",
      "In the unit of the wind sensor (e.g. km/h or m/s)."
     ],
     "rain_entity": [
      "Rain sensor",
      "A rain sensor that turns on, or an amount of rain (e.g. mm/h)."
     ],
     "rain_threshold": [
      "Rain protection above",
      "Only for a numeric rain sensor: rain counts above this value."
     ],
     "frost_threshold": [
      "Frost at or below",
      "Outdoor temperature. Only windows with a frost position take part."
     ],
     "protection_release": [
      "Release after",
      "A protection ends only after the value stayed on the safe side this long. An unavailable sensor never ends a protection."
     ]
    },
    "sections": {}
   },
   "options.shutter_startup": {
    "title": "Restart protection",
    "fields": {
     "startup_delay": [
      "Restart protection",
      "No movement for this time after Home Assistant started (sensors and covers are still coming online)."
     ],
     "catch_up_after": [
      "Catch up the evening run from",
      "After the restart protection the evening run is caught up for windows not yet closed this evening, but only after this time."
     ]
    },
    "sections": {}
   },
   "options.shutter_advanced": {
    "title": "Advanced",
    "fields": {
     "window_closed_delay": [
      "Window counts as closed after",
      "A window contact must report closed this long before closing after the window, sun protection or the close trigger act (against bouncing contacts)."
     ],
     "command_interval": [
      "Spacing between cover commands",
      "Several covers move one after the other with this spacing (against radio collisions). 0 = all at once."
     ],
     "verify_after": [
      "Check the position after",
      "If a cover has not reached its target by then, the command is repeated once; then a notification is sent. 0 = off."
     ]
    },
    "sections": {}
   },
   "options.heating": {
    "title": "Heating",
    "fields": {},
    "sections": {}
   },
   "options.heating_general": {
    "title": "General",
    "fields": {
     "outdoor_temperature": [
      "Outdoor temperature sensor",
      "Sensor for the outdoor temperature (e.g. a helper combining several sensors). Without it the current temperature of the weather entity is used. Only while nothing is set under Settings > House."
     ],
     "outdoor_humidity": [
      "Outdoor humidity sensor",
      "Optional. Needed for the ventilation recommendation; without it the humidity of the weather entity is used. Only while nothing is set under Settings > House."
     ],
     "weather": [
      "Weather entity",
      "Optional but recommended. Its forecast is used for the nightly heating day decision and the expected sun. Without an outdoor sensor its current temperature is the outdoor temperature. Only while nothing is set under Settings > House."
     ],
     "pv_power": [
      "PV power sensor",
      "Optional. PV power (W or kW) as an indicator for sunshine. The solar gain per room is learned from it."
     ],
     "pv_forecast": [
      "PV forecast sensor",
      "Optional, only together with the PV power sensor. Expected PV energy of the next hour (Wh or kWh, e.g. Forecast.Solar) or expected power in one hour (W or kW). Without it the sun is estimated from the hourly weather forecast and the sun position."
     ],
     "heat_meter": [
      "Heat meter",
      "Optional. Meter reading of the heat meter of the circuits controlled here (Wh, kWh, MWh, MJ or GJ, e.g. total_increasing). The AI then sees the measured heat; it is also shown in the panel. Seldom and coarse readings are fine."
     ],
     "season_start": [
      "Heating period start (DD.MM.)",
      "Outside the heating period all circuits stay off (frost protection only) and the AI is not asked."
     ],
     "season_end": [
      "Heating period end (DD.MM.)",
      "Last day of the heating period, may be in the next year (e.g. 31.03.)."
     ],
     "frost_temperature": [
      "Frost protection temperature",
      "Always applies, also outside the heating period and with a switched-off thermostat."
     ],
     "forecast_trust": [
      "Trust in the sun forecast",
      "Share of the expected PV power the control relies on when it holds back heating (100 % = full forecast, 0 % = only the current PV power counts)."
     ],
     "season_start_day": [
      "Heating period starts: day",
      "Heating is possible from this date (e.g. 1 October)."
     ],
     "season_start_month": [
      "Heating period starts: month",
      ""
     ],
     "season_end_day": [
      "Heating period ends: day",
      "Last day of the heating period (e.g. 31 March); the period may span the turn of the year."
     ],
     "season_end_month": [
      "Heating period ends: month",
      ""
     ]
    },
    "sections": {}
   },
   "options.heating_vacation": {
    "title": "Vacation",
    "fields": {
     "vacation_entities": [
      "Vacation entities",
      "Any of these entities being 'on' means vacation (e.g. an input_boolean or a calendar). Only while nothing is set under Settings > Vacation. The switch “Vacation” of the house always counts."
     ],
     "vacation_temperature": [
      "Vacation temperature",
      "Target for all rooms during vacation (e.g. 17 °C)."
     ],
     "return_entity": [
      "Return date/time",
      "Optional input_datetime, timestamp sensor or datetime entity. Heating starts early enough (learned heat-up time) to reach the normal target on return. The return of the switch “Vacation” comes first; without it one set under Settings > Vacation."
     ],
     "preheat_reserve": [
      "Preheat reserve",
      "Additional time added to the calculated preheating time (e.g. 30 min)."
     ],
     "vacation_ventilation_pause": [
      "Ventilation advice rests",
      "On vacation the ventilation advice shows “Vacation”, “ventilation recommended” is off. Vacation minutes do not count for the AI ventilation check and stay out of the humidity profile."
     ]
    },
    "sections": {}
   },
   "options.heating_rules": {
    "title": "Emergency rule",
    "fields": {
     "emergency_enabled": [
      "Emergency rule",
      "On days without heating, a room may still heat if the temperature expected after the lead time is long and clearly below its target, without airing."
     ],
     "emergency_delta": [
      "Emergency: below target by",
      "How far below the target the temperature expected after the lead time has to be (at least the switch-on hysteresis)."
     ],
     "emergency_duration": [
      "Emergency: duration",
      "How long the expected temperature has to stay that low (e.g. 45 min)."
     ],
     "emergency_window_quiet": [
      "Emergency: no window change for",
      "Airing does not count: windows must not have changed for this time."
     ],
     "force_on_below": [
      "Always heat below target by",
      "Below target by this much the circuit heats regardless of every prediction and the expected sun."
     ]
    },
    "sections": {}
   },
   "options.heating_ventilation": {
    "title": "Ventilation",
    "fields": {
     "ventilation_min_ah_advantage": [
      "Minimum drying advantage",
      "Absolute humidity is the water content of the air in g/m³, independent of temperature. Outside air must contain at least this much less water for 'ventilate now' (e.g. 0.8 g/m³)."
     ],
     "ventilation_max_reference_excess": [
      "Maximum outside warmer by",
      "Drying is not recommended if outside is warmer than inside by more than this."
     ],
     "ventilation_energy_rh_per_k": [
      "Energy saving surcharge",
      "Energy saving: within the heating period airing costs heat, the more the colder it is outside. The humidity must then exceed the threshold by this much per Kelvin outside is colder than the room (e.g. 0.25 %/K: at 21 °C inside and 1 °C outside 5 % more), at most up to 70 %, above which airing is always recommended against mould. 0 = off. Start value, the AI adjusts it per room."
     ],
     "ventilation_mould_rh": [
      "Mould limit",
      "From this relative humidity airing is always recommended, even in frost and right after an airing; the energy saving surcharge never goes beyond it. Lower it for rooms with cold exterior walls. Start value, the AI adjusts it per room."
     ],
     "ventilation_airing_target_below": [
      "Airing target below threshold",
      "The suggested airing time aims at this far below the humidity threshold. Start value for the AI."
     ],
     "ventilation_airing_time_factor": [
      "Airing time factor",
      "Scales the suggested airing time. Once two airings are evaluated it is computed from the learned air exchange of the room and the temperature difference, before that from the outside temperature (5 min in frost up to 20 min when warm). Start value for the AI."
     ],
     "ventilation_airing_min_minutes": [
      "Shortest airing time",
      "Start value for the AI."
     ],
     "ventilation_airing_max_minutes": [
      "Longest airing time",
      "Start value for the AI."
     ],
     "ventilation_airing_pause": [
      "Pause after airing",
      "After an airing moisture comes back from walls and furniture. Drying is recommended again only after this pause (below the mould limit), which saves heat and nagging. Start value for the AI."
     ],
     "ventilation_min_cooling_advantage": [
      "Minimum cooling advantage",
      "'Ventilation useful' if inside is warmer than outside by at least this (not while heating)."
     ],
     "ventilation_cooling_margin": [
      "Minimum distance above target for cooling",
      "Within the heating period 'ventilation useful' (cooling) is only recommended if the room is at least this much warmer than its target. Not used outside the heating period. Rooms without a heating circuit use their initial target."
     ],
     "ventilation_cooling_min_temp": [
      "Cool only from room temperature",
      "'Ventilation useful' (cooling) only from this room temperature on, all year. 0 = off. In addition cooling is never recommended if the outside air would raise the relative humidity of the room above its humidity threshold."
     ],
     "night_start_hour": [
      "Night starts at",
      "Used when the reference is another room: cooling advantage only counts at night."
     ],
     "night_end_hour": [
      "Night ends at",
      "End of the night (time, e.g. 08:00)."
     ],
     "ventilation_ai_enabled": [
      "AI adjusts ventilation per room",
      "All year the AI reviews the ventilation thresholds of every room with a humidity sensor: it learns what is usual in each room, how low the humidity can get and what airing really achieves. Shares the monthly AI budget."
     ],
     "ventilation_check_interval": [
      "Ventilation check base interval",
      "First interval; it doubles with every check that changed nothing relevant and starts over when a room stays humid or a value changes."
     ],
     "ventilation_check_max_interval": [
      "Ventilation check maximum interval",
      "The interval never grows beyond this."
     ]
    },
    "sections": {}
   },
   "options.heating_ai": {
    "title": "AI",
    "fields": {
     "model": [
      "Claude model",
      "Model for all AI calls. Prices below are suggestions for the selected model and can be changed."
     ],
     "effort": [
      "Thinking effort",
      "Claude thinks before it answers. More effort can give better answers but uses more tokens, which are billed as output. 'auto' leaves it to the model."
     ],
     "nightly_time": [
      "Time of the nightly run",
      "Daily decision whether heating is needed today (also the start of the evaluated day)."
     ],
     "check_interval": [
      "Check interval",
      "Base interval of the periodic AI check on heating days (e.g. 4 h). It doubles after every check without relevant change."
     ],
     "check_max_interval": [
      "Maximum check interval",
      "Upper limit for the doubled interval (e.g. 48 h)."
     ],
     "monthly_budget": [
      "Monthly budget",
      "In US dollars, as Anthropic bills. No AI calls once the costs of the month reach this value (until the month changes). A check usually costs a few cents, so 5 USD allow about 100 to 200 calls."
     ],
     "price_input": [
      "Price input tokens",
      "US dollars per million tokens, as Anthropic bills."
     ],
     "price_output": [
      "Price output tokens",
      "US dollars per million tokens, as Anthropic bills (thinking counts as output)."
     ],
     "price_cache_write": [
      "Price cache write",
      "US dollars per million tokens, as Anthropic bills."
     ],
     "price_cache_read": [
      "Price cache read",
      "US dollars per million tokens, as Anthropic bills."
     ],
     "max_output_tokens": [
      "Maximum output tokens",
      "Upper limit per answer, thinking included (too low cuts answers off, they are paid but discarded). Also the upper bound of the cost estimate before a call."
     ]
    },
    "sections": {}
   },
   "options.heating_decision": {
    "title": "Heating day decision (experts)",
    "fields": {
     "theta": [
      "Heating threshold theta (learned)",
      "Current threshold of the heating day rule: if the forecast maximum is below it, heating is needed. A change replaces the learned value; learning continues from there."
     ],
     "too_cold_margin": [
      "Too cold below target by",
      "Evaluation: a room counts as too cold below target minus this (airing excluded)."
     ],
     "too_cold_minutes": [
      "Too cold minutes for heating need",
      "Evaluation: this many minutes too cold mean heating was needed."
     ]
    },
    "sections": {
     "learning_steps": {
      "name": "Learning steps",
      "description": "How much theta and the margin change after an evaluated error.",
      "fields": {
       "theta_step_up": [
        "Heating threshold: step up",
        "After error A, i.e. it got too cold on a day without heating (e.g. 1.0 K)."
       ],
       "theta_step_down": [
        "Heating threshold: step down",
        "After error B, i.e. heating ran although it was not needed (e.g. 1.0 K)."
       ],
       "puffer_step_up": [
        "Margin above target: step up",
        "After error A for the cold room."
       ],
       "puffer_step_down": [
        "Margin above target: step down",
        "After error B."
       ]
      }
     },
     "phases": {
      "name": "Decision phases",
      "description": "When the heating day decision moves between AI leads, shared and rule leads.",
      "fields": {
       "phase_shared_min_days": [
        "Days until shared decision",
        "Who decides the heating day: first the AI leads, then AI and rule decide together, finally the rule leads. 'AI leads' -> 'shared' after this many evaluated days (e.g. 14)."
       ],
       "phase_shared_min_agreement": [
        "Agreement for shared decision",
        "Minimum agreement of rule and AI."
       ],
       "phase_rule_min_days": [
        "Days until rule leads",
        "Phase 'shared' -> 'rule leads' after this many days in phase 'shared'."
       ],
       "phase_rule_min_agreement": [
        "Agreement for rule leads",
        "Minimum agreement of rule and AI."
       ],
       "phase_max_rule_errors": [
        "Allowed rule errors",
        "Maximum rule errors within the period for a phase change."
       ],
       "phase_fallback_errors_7d": [
        "Rule errors in 7 days for fallback",
        "This many rule errors within 7 days move back one phase."
       ],
       "phase_ai_check_every_days": [
        "AI control check every",
        "When the rule leads and is sure, the AI is still asked every this many days."
       ]
      }
     }
    }
   },
   "options.heating_ai_limits": {
    "title": "AI limits",
    "fields": {},
    "sections": {
     "hysteresis_on": {
      "name": "Switch-on hysteresis",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "hysteresis_off": {
      "name": "Switch-off hysteresis",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "overshoot_factor": {
      "name": "Overshoot factor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "lead_factor": {
      "name": "Lead time factor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "sun_factor": {
      "name": "Sun factor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "window_delay_min": {
      "name": "Window delay",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "recovery_bias_min": {
      "name": "Recovery time correction",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "puffer": {
      "name": "Margin above target (puffer)",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "theta": {
      "name": "Heating threshold (theta)",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "rh_threshold": {
      "name": "Humidity threshold",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "rh_hysteresis": {
      "name": "Humidity hysteresis",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "min_ah_advantage": {
      "name": "Minimum drying advantage",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "max_reference_excess": {
      "name": "Maximum outside warmer by",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "min_rh_drop": {
      "name": "Minimum humidity drop by airing",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "min_cooling_advantage": {
      "name": "Minimum cooling advantage",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "cooling_margin": {
      "name": "Cooling distance above target",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "cooling_min_temp": {
      "name": "Cool only from room temperature",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "energy_rh_per_k": {
      "name": "Energy saving surcharge",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "mould_rh": {
      "name": "Mould limit",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "airing_target_below": {
      "name": "Airing target below threshold",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "airing_time_factor": {
      "name": "Airing time factor",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "airing_min_minutes": {
      "name": "Shortest airing time",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "airing_max_minutes": {
      "name": "Longest airing time",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     },
     "airing_pause_min": {
      "name": "Pause after airing",
      "description": "",
      "fields": {
       "min": [
        "Minimum",
        ""
       ],
       "max": [
        "Maximum",
        ""
       ],
       "step": [
        "Max. change per check",
        ""
       ]
      }
     }
    }
   },
   "room.user": {
    "title": "Room",
    "fields": {
     "name": [
      "Name",
      "Name of the room, also used for the device and its entities."
     ],
     "area": [
      "Area",
      "Optional. The device of the room is placed in this area; its floor counts for cross ventilation."
     ]
    },
    "sections": {
     "sensors": {
      "name": "Sensors",
      "description": "",
      "fields": {
       "temperature_sensor": [
        "Temperature sensor",
        "Room temperature. Without a sensor the room has no heating and no ventilation advice (e.g. a room only for covers)."
       ],
       "humidity_sensor": [
        "Humidity sensor",
        "Relative humidity, needed for the ventilation recommendation."
       ]
      }
     },
     "heating": {
      "name": "Heating circuit",
      "description": "",
      "fields": {
       "heater_switch": [
        "Heating circuit switch",
        "Switch of the actuator (e.g. a relay). Leave empty for a room with ventilation recommendation only."
       ],
       "default_target": [
        "Initial target temperature",
        "Target until you change it on the thermostat card."
       ],
       "min_target": [
        "Minimum target",
        "Lowest value of the thermostat card."
       ],
       "max_target": [
        "Maximum target",
        "Highest value of the thermostat card."
       ],
       "min_on_time": [
        "Minimum on time",
        "Always respected (protects the actuator). Not learned."
       ],
       "min_off_time": [
        "Minimum off time",
        "Always respected. Not learned."
       ],
       "heating_type": [
        "Heating type",
        "How the circuit heats. A floor stores heat for hours, radiators react within minutes; the AI judges the learned values with this in mind."
       ]
      }
     },
     "start_values": {
      "name": "Start values (learned later)",
      "description": "Only when the room is created. Afterwards the learned values are edited.",
      "fields": {
       "window_delay": [
        "Window delay (start value)",
        "Window open this long pauses heating. The AI may adjust it."
       ],
       "recovery_time": [
        "Recovery time after airing (start value)",
        "After closing, heating waits this long because floor and walls often reheat the room. Learned afterwards."
       ],
       "dead_time": [
        "Dead time until the room warms (start value)",
        "Time from switching on until the room gets warmer; underfloor heating often 30-90 min, radiators 5-20 min. Learned afterwards."
       ],
       "puffer": [
        "Margin above target (start value)",
        "Heating day rule: how far above the target a room must be at the nightly run to manage a day without heating (e.g. 0.7 K). Learned afterwards."
       ]
      }
     },
     "ventilation": {
      "name": "Ventilation",
      "description": "",
      "fields": {
       "ventilation_rh_threshold": [
        "Humidity threshold",
        "Start value of the relative humidity from which ventilating is recommended (e.g. 65 % for bathrooms); the AI ventilation check adjusts it to the room."
       ],
       "reference_temperature": [
        "Reference temperature instead of outdoor",
        "Optional, for rooms aired via another room."
       ],
       "reference_humidity": [
        "Reference humidity instead of outdoor",
        "Required together with the reference temperature."
       ],
       "ventilation_block_entity": [
        "Ventilation block entity",
        "Optional. While it blocks, no ventilation is recommended: a cover while closed (e.g. sun protection down), a climate entity or water heater while not off (e.g. air conditioner running), a switch, binary sensor, fan or similar while on."
       ]
      }
     },
     "draft": {
      "name": "Draft from other rooms",
      "description": "Windows of other rooms whose opening together also cools this room (cross ventilation). Per combination choose the windows that must be open together. As soon as every window of one combination is open, the room behaves as with its own window open: heating pauses after the window delay and waits the recovery time. A combination with a single window triggers on its own.",
      "fields": {
       "draft_group_1": [
        "Combination 1",
        "e.g. kids' room + bathroom; a second combination e.g. kids' room + bedroom."
       ],
       "draft_group_2": [
        "Combination 2",
        ""
       ],
       "draft_group_3": [
        "Combination 3",
        ""
       ],
       "draft_group_4": [
        "Combination 4",
        ""
       ]
      }
     },
     "sun_protection": {
      "name": "Sun protection",
      "description": "Defaults for the covers of the windows of this room. Room temperature and target come from the temperature sensor and the thermostat of the room unless a window has its own room temperature.",
      "fields": {
       "cooling_entity": [
        "Air conditioner",
        "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner. Applies to every window of the room without its own air conditioner."
       ]
      }
     }
    }
   },
   "room.reconfigure": {
    "title": "Room",
    "fields": {
     "name": [
      "Name",
      "Name of the room, also used for the device and its entities."
     ],
     "area": [
      "Area",
      "Optional. The device of the room is placed in this area; its floor counts for cross ventilation."
     ]
    },
    "sections": {
     "sensors": {
      "name": "Sensors",
      "description": "",
      "fields": {
       "temperature_sensor": [
        "Temperature sensor",
        "Room temperature. Without a sensor the room has no heating and no ventilation advice (e.g. a room only for covers)."
       ],
       "humidity_sensor": [
        "Humidity sensor",
        "Relative humidity, needed for the ventilation recommendation."
       ]
      }
     },
     "heating": {
      "name": "Heating circuit",
      "description": "",
      "fields": {
       "heater_switch": [
        "Heating circuit switch",
        "Switch of the actuator (e.g. a relay). Leave empty for a room with ventilation recommendation only."
       ],
       "default_target": [
        "Initial target temperature",
        "Target until you change it on the thermostat card."
       ],
       "min_target": [
        "Minimum target",
        "Lowest value of the thermostat card."
       ],
       "max_target": [
        "Maximum target",
        "Highest value of the thermostat card."
       ],
       "min_on_time": [
        "Minimum on time",
        "Always respected (protects the actuator). Not learned."
       ],
       "min_off_time": [
        "Minimum off time",
        "Always respected. Not learned."
       ],
       "heating_type": [
        "Heating type",
        "How the circuit heats. A floor stores heat for hours, radiators react within minutes; the AI judges the learned values with this in mind."
       ]
      }
     },
     "learned_values": {
      "name": "Learned values",
      "description": "Values the control currently uses. A change replaces the learned or AI-adjusted value; learning continues from there.",
      "fields": {
       "window_delay": [
        "Window delay",
        "Window open this long pauses heating. The AI may adjust it."
       ],
       "recovery_time": [
        "Recovery time after airing",
        "Learned wait after the windows are closed."
       ],
       "dead_time": [
        "Dead time until the room warms",
        "Learned time until the room warms up after switching on."
       ],
       "puffer": [
        "Margin above target",
        "Heating day rule: needed margin above the target at the nightly run (learned)."
       ]
      }
     },
     "ventilation": {
      "name": "Ventilation",
      "description": "",
      "fields": {
       "ventilation_rh_threshold": [
        "Humidity threshold",
        "Start value of the relative humidity from which ventilating is recommended (e.g. 65 % for bathrooms); the AI ventilation check adjusts it to the room."
       ],
       "reference_temperature": [
        "Reference temperature instead of outdoor",
        "Optional, for rooms aired via another room."
       ],
       "reference_humidity": [
        "Reference humidity instead of outdoor",
        "Required together with the reference temperature."
       ],
       "ventilation_block_entity": [
        "Ventilation block entity",
        "Optional. While it blocks, no ventilation is recommended: a cover while closed (e.g. sun protection down), a climate entity or water heater while not off (e.g. air conditioner running), a switch, binary sensor, fan or similar while on."
       ]
      }
     },
     "draft": {
      "name": "Draft from other rooms",
      "description": "Windows of other rooms whose opening together also cools this room (cross ventilation). Per combination choose the windows that must be open together. As soon as every window of one combination is open, the room behaves as with its own window open: heating pauses after the window delay and waits the recovery time. A combination with a single window triggers on its own.",
      "fields": {
       "draft_group_1": [
        "Combination 1",
        "e.g. kids' room + bathroom; a second combination e.g. kids' room + bedroom."
       ],
       "draft_group_2": [
        "Combination 2",
        ""
       ],
       "draft_group_3": [
        "Combination 3",
        ""
       ],
       "draft_group_4": [
        "Combination 4",
        ""
       ]
      }
     },
     "sun_protection": {
      "name": "Sun protection",
      "description": "Defaults for the covers of the windows of this room. Room temperature and target come from the temperature sensor and the thermostat of the room unless a window has its own room temperature.",
      "fields": {
       "cooling_entity": [
        "Air conditioner",
        "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner. Applies to every window of the room without its own air conditioner."
       ]
      }
     }
    }
   },
   "group.user": {
    "title": "Group",
    "fields": {
     "name": [
      "Name",
      "Also used for the device and its entities."
     ],
     "azimuth_from": [
      "Azimuth from",
      "Sun direction from which the sun shines on the windows (90 ° = east, 180 ° = south, 270 ° = west). The bounds themselves do not count."
     ],
     "azimuth_to": [
      "Azimuth to",
      "When the sun reaches this direction, protected covers open again (auto up)."
     ],
     "radiation_sensors": [
      "Radiation sensors",
      "Solar radiation in W/m², e.g. from a weather service or a weather station."
     ],
     "pv_sensors": [
      "PV power sensors",
      "Power of a solar system or panel facing this direction (W)."
     ],
     "lux_sensors": [
      "Brightness sensors",
      "Lux sensors at the windows. Every sensor of the group must reach the threshold of the window."
     ]
    },
    "sections": {}
   },
   "group.reconfigure": {
    "title": "Group",
    "fields": {
     "name": [
      "Name",
      "Also used for the device and its entities."
     ],
     "azimuth_from": [
      "Azimuth from",
      "Sun direction from which the sun shines on the windows (90 ° = east, 180 ° = south, 270 ° = west). The bounds themselves do not count."
     ],
     "azimuth_to": [
      "Azimuth to",
      "When the sun reaches this direction, protected covers open again (auto up)."
     ],
     "radiation_sensors": [
      "Radiation sensors",
      "Solar radiation in W/m², e.g. from a weather service or a weather station."
     ],
     "pv_sensors": [
      "PV power sensors",
      "Power of a solar system or panel facing this direction (W)."
     ],
     "lux_sensors": [
      "Brightness sensors",
      "Lux sensors at the windows. Every sensor of the group must reach the threshold of the window."
     ]
    },
    "sections": {}
   },
   "window.basics": {
    "title": "Window",
    "fields": {
     "name": [
      "Name",
      "Also used for the device and its entities."
     ],
     "room": [
      "Room",
      "Optional. The heating of the room uses the contacts of the window; the cover takes room temperature and air conditioner of the room."
     ],
     "size": [
      "Size",
      "How fast airing exchanges the air: the suggested airing time follows it, and the largest opening is suggested for airing. The size applies to every contact of the window."
     ],
     "cover": [
      "Cover",
      "Optional. 100 % = open, 0 % = closed. Without a cover the window only serves the heating."
     ],
     "window_sensors": [
      "Window contacts",
      "'on' = open. Window handles with the states open, tilted and closed work as well. Unknown or unavailable counts as open. A contact belongs to one window only."
     ],
     "tilt_sensors": [
      "Tilt contacts",
      "'on' = tilted. While the window is only tilted, covers close no further than the ventilation position."
     ],
     "group": [
      "Group",
      "Direction of the sun. Without a group the window has no sun protection."
     ]
    },
    "sections": {}
   },
   "window.sun": {
    "title": "Sun protection",
    "fields": {
     "radiation_threshold": [
      "Radiation threshold",
      "Every radiation sensor of the group must reach this value."
     ],
     "pv_threshold": [
      "PV threshold",
      "Every PV sensor of the group must reach this value."
     ],
     "lux_threshold": [
      "Brightness threshold",
      "Every brightness sensor of the group must reach this value."
     ],
     "temperature_threshold": [
      "Outdoor temperature at least",
      "Sun protection only from this outdoor temperature on."
     ],
     "temperature_hold": [
      "Temperature hold time",
      "The outdoor temperature must stay above the value this long. Below it the condition ends immediately."
     ],
     "room_entity": [
      "Room temperature",
      "Optional: thermostat (climate) or temperature sensor of the room. Then the cover is only lowered when the room is too warm. Without a value the condition counts as met (except on a heating day)."
     ],
     "room_margin": [
      "Too warm from setpoint plus",
      "With a thermostat: too warm from its setpoint plus this margin."
     ],
     "room_threshold": [
      "Too warm from",
      "With a temperature sensor (or a thermostat without a setpoint): too warm from this temperature."
     ],
     "cooling_entity": [
      "Air conditioner",
      "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner."
     ],
     "sun_hold": [
      "Sun hold time",
      "Summer day, temperature, room and all sun sensors must be met this long. The condition ends immediately."
     ],
     "sun_position": [
      "Sun protection position",
      "Lowered once a day to this position. A cover already further closed is left alone."
     ],
     "position_tolerance": [
      "Tolerance for auto up",
      "Auto up only opens covers standing at the sun protection position up to this much above it. Covers moved elsewhere by hand stay."
     ],
     "auto_up": [
      "Auto up",
      "Open again when the sun leaves the sector (not in the evening)."
     ],
     "notify_open_window": [
      "Notify about an open window",
      "Once a day, if an open window prevented the sun protection."
     ],
     "manual_max_position": [
      "Manual sun protection up to",
      "A cover lowered by hand to at most this position while the sun shines counts as sun protection for today (no automatic movement)."
     ],
     "manual_detection_window": [
      "Detection period",
      "The manual movement must not be longer ago than this."
     ],
     "manual_follow_up": [
      "Follow-up of the sun condition",
      "For this detection the sun condition (without temperature) still counts this long after it ended."
     ],
     "manual_at_sun_position": [
      "Moving onto the sun protection position counts",
      "A cover moved by anyone onto the sun protection position (up to the tolerance) while the sun shines is treated like automatic sun protection and opens again with auto up."
     ]
    },
    "sections": {}
   },
   "window.behavior": {
    "title": "Behaviour",
    "fields": {},
    "sections": {
     "override": {
      "name": "Manual override",
      "description": "",
      "fields": {
       "override_duration": [
        "Duration",
        "After a manual movement the automatic pauses this long for the window. Every further movement starts it again. 0 = until sunrise."
       ],
       "override_sunrise_reset": [
        "Also end at sunrise",
        "The override also ends at the next sunrise, even if the duration is still running."
       ],
       "override_ignore_evening": [
        "Evening and vacation runs despite override",
        "e.g. bedrooms that should always close in the evening."
       ]
      }
     },
     "conditions": {
      "name": "Additional conditions",
      "description": "",
      "fields": {
       "open_block_entity": [
        "Opening block",
        "No automatic opening (auto up, ventilation, vacation morning, morning opening) unless this entity has one of the free states (e.g. a TV)."
       ],
       "open_block_free_states": [
        "Free states",
        "States of the opening block in which opening is still allowed (e.g. off, standby)."
       ],
       "close_trigger_entities": [
        "Close trigger",
        "When one of these entities becomes active, the cover closes once per active cycle, only with a closed window (otherwise as soon as it is closed). The cycle ends when all are inactive."
       ],
       "close_trigger_active_states": [
        "Active states",
        "States in which a close trigger counts as active (e.g. on, playing for a TV)."
       ],
       "close_trigger_on_delay": [
        "Active after",
        "A trigger must be active this long before the cover closes (switching on briefly does not count)."
       ],
       "close_trigger_off_delay": [
        "Inactive after",
        "All triggers must be inactive this long before the cycle ends and switching on closes again."
       ],
       "close_trigger_min_position": [
        "Only if open more than",
        "Only closes when the cover is open further than this position."
       ],
       "close_trigger_max_lock": [
        "Cycle at most",
        "After this time at the latest a new cycle starts, even if the triggers were active all the time."
       ],
       "window_exception_entity": [
        "Window exception",
        "While this entity is available, an open window does not prevent closing movements and no message is sent (e.g. an air conditioner with its hose through the balcony door). Not used for the vacation evening."
       ]
      }
     },
     "evening": {
      "name": "Evening",
      "description": "",
      "fields": {
       "evening_close": [
        "Evening run",
        "Close at the start of the evening mode, once per evening and only with a closed window."
       ],
       "evening_position": [
        "Evening position",
        "Target of the evening run and of closing after the window was closed. 0 % = closed; e.g. 20 % leaves a gap on warm nights."
       ],
       "follow_up_close": [
        "Close after window closed",
        "If the window is closed in the evening, the cover closes (also during an override)."
       ],
       "evening_custom": [
        "Own evening times",
        "Use the following values instead of the global ones."
       ],
       "evening_earliest": [
        "Evening mode at the earliest",
        "The evening mode never starts before this time."
       ],
       "evening_elevation": [
        "Sun elevation",
        "The evening mode starts when the sun drops below this elevation (e.g. -4 °)."
       ],
       "evening_latest": [
        "Evening mode at the latest",
        "Time fallback: the evening mode starts at this time at the latest."
       ]
      }
     },
     "ventilation_settings": {
      "name": "Ventilation and vacation",
      "description": "",
      "fields": {
       "ventilation": [
        "Ventilate when the window opens",
        "Opening the window moves a closed cover to the ventilation position (in the evening after the short delay, during the day after the long one)."
       ],
       "ventilation_position": [
        "Ventilation position",
        "Position for ventilation (100 % = open)."
       ],
       "closed_position": [
        "Counts as closed up to",
        "Used for ventilation and the vacation morning."
       ],
       "ventilation_delay_evening": [
        "Delay in the evening",
        "In the evening mode the cover moves to the ventilation position after this short time."
       ],
       "ventilation_delay_day": [
        "Delay during the day",
        "The window must still be open afterwards."
       ],
       "vacation": [
        "Vacation simulation",
        "Take part in the random opening and closing during vacation."
       ]
      }
     },
     "protection": {
      "name": "Weather protection & door",
      "description": "",
      "fields": {
       "weather_protection": [
        "Weather protection for this window",
        "Off = wind, rain and frost never move or limit this cover, whatever the positions below say. Turn it on for every window that should take part. With the automatic off (globally or for this window) there is no weather protection either."
       ],
       "wind_position": [
        "Position with wind",
        "Empty = not affected. E.g. 100 % retracts external venetian blinds. Only with the weather protection of the window on."
       ],
       "window_wind_threshold": [
        "Own wind threshold",
        "Empty = wind protection from the threshold of the basic settings. Otherwise this window is protected already or only from this value (unit of the wind sensor)."
       ],
       "rain_position": [
        "Position with rain",
        "Empty = not affected. E.g. 0 % for a roof window shutter."
       ],
       "frost_position": [
        "Lowest position with frost",
        "Empty = off. With frost, closing stops at this position so the cover cannot freeze on, e.g. 5 %."
       ],
       "protection_keep_closed": [
        "Further closed counts as protected",
        "A cover already further closed than its position with wind or rain is not opened to it (e.g. closed at 0 % with a wind position of 20 %). Not for a position of 100 %: retracting external venetian blinds always runs."
       ],
       "lockout_protection": [
        "Lockout protection (door)",
        "While the contact reports open, nothing closes below the ventilation position, also not with the window exception or the weather protection."
       ]
      }
     }
    }
   },
   "window.morning": {
    "title": "Morning opening",
    "fields": {
     "morning_enabled": [
      "Morning opening",
      "Open the cover automatically in the morning."
     ],
     "morning_mode": [
      "Mode",
      "What starts the morning opening; its settings follow in the next step."
     ],
     "morning_earliest": [
      "At the earliest",
      "The cover never opens before this time, even if the trigger comes earlier."
     ],
     "morning_latest": [
      "At the latest",
      "If nothing triggered until then, the cover opens at this time."
     ],
     "morning_position": [
      "Target position",
      "100 = open, less = partial opening."
     ],
     "morning_sun_position": [
      "Directly to sun protection if needed",
      "If the sun condition applies, open only to the sun protection position."
     ]
    },
    "sections": {}
   },
   "window.morning_time": {
    "title": "Morning opening by time",
    "fields": {
     "morning_time_workday": [
      "Workdays",
      "Time on workdays (workday sensor or weekend days)."
     ],
     "morning_time_weekend": [
      "Weekend and holidays",
      "Time on weekends and public holidays (holidays only with a workday sensor)."
     ]
    },
    "sections": {}
   },
   "window.morning_sun": {
    "title": "Morning opening by sun",
    "fields": {
     "morning_sun_event": [
      "Event",
      "Sunrise or the sun reaching an elevation."
     ],
     "morning_sun_elevation": [
      "Sun elevation",
      "Only for sun elevation: opens when the rising sun passes this elevation."
     ],
     "morning_sun_offset": [
      "Offset",
      "Minutes before (negative) or after the event."
     ]
    },
    "sections": {}
   },
   "window.morning_brightness": {
    "title": "Morning opening by brightness",
    "fields": {
     "morning_lux_threshold": [
      "Brightness",
      "Every brightness sensor of the group must reach this value."
     ],
     "morning_lux_hold": [
      "Hold time",
      "It must be bright enough this long before the cover opens."
     ]
    },
    "sections": {}
   },
   "window.morning_trigger": {
    "title": "Morning opening by trigger",
    "fields": {
     "morning_trigger_entity": [
      "Trigger entity",
      "A timestamp (e.g. the next alarm of a phone) opens at that time plus offset. Any other entity opens when it turns on (motion, switch)."
     ],
     "morning_trigger_offset": [
      "Offset",
      "Only for timestamps."
     ]
    },
    "sections": {}
   },
   "window.reconfigure": {
    "title": "Change window",
    "fields": {},
    "sections": {}
   },
   "meter.user": {
    "title": "New meter",
    "fields": {
     "name": [
      "Name",
      ""
     ],
     "meter_type": [
      "Meter type",
      ""
     ]
    },
    "sections": {}
   },
   "meter.details": {
    "title": "{name}",
    "fields": {},
    "sections": {
     "camera_section": {
      "name": "Camera and light",
      "description": "Camera of the meter and the light that is switched on for the picture.",
      "fields": {
       "camera": [
        "Camera",
        "Camera entity pointed at the display (e.g. an ESP32-CAM with ESPHome)."
       ],
       "light": [
        "Light",
        "Optional. Switched on for the picture and off again afterwards (e.g. the flash LED)."
       ],
       "light_brightness": [
        "Light brightness",
        "Brightness of the light for the picture. Try it with a test picture: reflections make the display unreadable."
       ],
       "light_brightness_2": [
        "Brightness 2nd picture",
        "Optional (0 = off): each attempt also takes a second picture with this brightness, and the AI gets both. Helps when at one brightness a light spot outshines digits and at the other digits are too dark. An attempt takes longer."
       ],
       "warmup": [
        "Warm-up time",
        "Wait after switching the light on, so the camera adjusts its exposure."
       ],
       "discard_frames": [
        "Discarded pictures",
        "Pictures thrown away before the real one. Cameras with a buffer (ESP32-CAM) otherwise deliver an old picture without light."
       ]
      }
     },
     "external_light_section": {
      "name": "External light",
      "description": "Optional extra light (light or switch entity) besides the light of the camera, e.g. LED modules. When it cannot be reached, the meter is read without it and a warning is logged.",
      "fields": {
       "external_light": [
        "External light",
        "Optional. Light or switch entity that lights the display in addition. Leave empty when there is none."
       ],
       "external_light_mode": [
        "Mode",
        "Only while taking pictures: switched on before the pictures and off afterwards. Always on: only switched on when it is off, and left on."
       ],
       "external_light_brightness": [
        "Brightness",
        "Only for a light entity that can be dimmed; a switch is just switched on and off."
       ],
       "external_light_lead_time": [
        "Lead time",
        "Wait after switching the external light on, before the light of the camera is switched on and the pictures are taken."
       ],
       "external_light_turn_off": [
        "Switch off afterwards",
        "Only in the mode \"Only while taking pictures\": switches the light off after the pictures, also when taking or reading them fails."
       ]
      }
     },
     "image_section": {
      "name": "Picture crop",
      "description": "Only this part of the picture is sent to the AI. Crop wide-angle cameras to the display; in the dashboard the crop can be drawn with the mouse.",
      "fields": {
       "crop_left": [
        "Left",
        "Left edge of the crop in percent of the width of the turned picture."
       ],
       "crop_top": [
        "Top",
        "Top edge of the crop in percent of the height of the turned picture."
       ],
       "crop_right": [
        "Right",
        "Right edge of the crop in percent of the width of the turned picture."
       ],
       "crop_bottom": [
        "Bottom",
        "Bottom edge of the crop in percent of the height of the turned picture."
       ],
       "rotate": [
        "Rotate",
        "Turns the picture clockwise by this angle (negative: counterclockwise), e.g. 90 for a camera mounted sideways or a few degrees for a display that sits askew. Turned before cropping, the crop refers to the turned picture."
       ],
       "exposure": [
        "Exposure",
        "Brightness of the picture for the AI: 100 % leaves it unchanged, below is darker (against reflections and overexposure), above is brighter."
       ],
       "enhance": [
        "Enhance picture",
        "Turns the picture grey, evens out the lighting and stretches the contrast before the AI reads it. Helps when the light leaves a bright spot on the display glass and dark corners, or with pale LCD segments. Not shown in the live picture; take a test picture to see it."
       ]
      }
     },
     "display_section": {
      "name": "Display",
      "description": "What the display shows. The hints are passed on to the AI.",
      "fields": {
       "unit": [
        "Unit",
        "Unit shown on the display (e.g. MWh, kWh or m³)."
       ],
       "decimals": [
        "Decimals",
        "Number of decimals shown on the display."
       ],
       "hints": [
        "Hints for the AI",
        "Optional. What is special about this display, e.g. lines that are not part of a digit, or which digits to ignore."
       ],
       "prompt": [
        "Own instructions for the AI",
        "Replace the whole generated instructions (leave empty for the standard). Unit, decimals and hints are then no longer inserted. The AI should still answer only with the number or “unreadable”."
       ]
      }
     },
     "schedule_section": {
      "name": "Schedule",
      "description": "How often the meter is read automatically.",
      "fields": {
       "interval": [
        "Interval",
        "Time between two automatic readings."
       ],
       "condition_entity": [
        "Condition",
        "Optional. While this entity is 'off', the second interval applies (e.g. a heating day sensor)."
       ],
       "condition_heating_day": [
        "Days without heating like condition off",
        "The second interval also applies on days without heating (heating day of the heating module, only within the heating period). With the heating off or an unknown heating day the normal interval applies."
       ],
       "interval_off": [
        "Interval while the condition is off",
        "Only together with a condition or the days without heating."
       ]
      }
     },
     "checks_section": {
      "name": "Checks",
      "description": "Majority vote and plausibility check of a reading.",
      "fields": {
       "max_rate": [
        "Largest increase per hour",
        "In the meter unit. A larger increase since the last valid reading is rejected (e.g. 0.05 MWh = 50 kW)."
       ],
       "max_correction": [
        "Largest correction",
        "In the meter unit. A smaller value than before is only taken when it is at most this much lower and confirmed by further pictures."
       ],
       "max_attempts": [
        "Pictures per reading",
        "Most pictures until a value has been read twice."
       ],
       "confirmations": [
        "Confirmation pictures",
        "Further pictures that must all show a smaller value before it is taken as a correction."
       ],
       "history_hint": [
        "Last readings to the AI",
        "The AI gets the last 3 valid readings as a hint, to decide an unclear digit plausibly. It should still read only what the picture shows; the checks here stay in place. Can tempt the AI to name an expected value, so use it mainly for displays that are hard to read."
       ],
       "meter_ai_task_entity": [
        "Own AI task",
        "Optional. Instead of the AI task of the integration."
       ]
      }
     },
     "notify_section": {
      "name": "Notifications",
      "description": "From the how-many-th time in a row a notification appears in Home Assistant (0 = never, 1 = at once). A valid reading starts the count again. Only while notifications are switched on in the settings of the integration.",
      "fields": {
       "notify_smaller": [
        "Smaller than before",
        "Value below the last valid one and not confirmed as a correction (rejected)."
       ],
       "notify_too_large": [
        "Increase too large",
        "Value rose more than the largest increase per hour allows (rejected)."
       ],
       "notify_corrected": [
        "Corrected",
        "Smaller value confirmed by more pictures and taken."
       ],
       "notify_failed": [
        "Unreadable or error",
        "The AI reads nothing clear, or the camera or AI is not reachable. Unreadable readings do not interrupt the count of the other cases."
       ]
      }
     },
     "vacation_section": {
      "name": "Vacation",
      "description": "Warns when something runs on vacation: a message, a logbook entry and the event house_assistant_vacation_alert, once per vacation and case. Counted from the last valid reading before the vacation. Not for the heat meter.",
      "fields": {
       "vacation_alert": [
        "Warn on vacation",
        "Default: on for a water meter, else off."
       ],
       "vacation_amount": [
        "Amount",
        "Used since the vacation started, in litres (water, gas) or kWh (electricity), from which it warns. 0 = off. Default water: 20 L."
       ],
       "vacation_rate": [
        "Mean flow or power",
        "Mean since the vacation started in L/h or kW (after an hour at the earliest) from which it warns. For gas and electricity enter the base load. 0 = off. Default water: 5 L/h."
       ]
      }
     }
    }
   },
   "meter.reconfigure": {
    "title": "Change meter",
    "fields": {
     "name": [
      "Name",
      ""
     ],
     "meter_type": [
      "Meter type",
      ""
     ]
    },
    "sections": {
     "camera_section": {
      "name": "Camera and light",
      "description": "Camera of the meter and the light that is switched on for the picture.",
      "fields": {
       "camera": [
        "Camera",
        "Camera entity pointed at the display (e.g. an ESP32-CAM with ESPHome)."
       ],
       "light": [
        "Light",
        "Optional. Switched on for the picture and off again afterwards (e.g. the flash LED)."
       ],
       "light_brightness": [
        "Light brightness",
        "Brightness of the light for the picture. Try it with a test picture: reflections make the display unreadable."
       ],
       "light_brightness_2": [
        "Brightness 2nd picture",
        "Optional (0 = off): each attempt also takes a second picture with this brightness, and the AI gets both. Helps when at one brightness a light spot outshines digits and at the other digits are too dark. An attempt takes longer."
       ],
       "warmup": [
        "Warm-up time",
        "Wait after switching the light on, so the camera adjusts its exposure."
       ],
       "discard_frames": [
        "Discarded pictures",
        "Pictures thrown away before the real one. Cameras with a buffer (ESP32-CAM) otherwise deliver an old picture without light."
       ]
      }
     },
     "external_light_section": {
      "name": "External light",
      "description": "Optional extra light (light or switch entity) besides the light of the camera, e.g. LED modules. When it cannot be reached, the meter is read without it and a warning is logged.",
      "fields": {
       "external_light": [
        "External light",
        "Optional. Light or switch entity that lights the display in addition. Leave empty when there is none."
       ],
       "external_light_mode": [
        "Mode",
        "Only while taking pictures: switched on before the pictures and off afterwards. Always on: only switched on when it is off, and left on."
       ],
       "external_light_brightness": [
        "Brightness",
        "Only for a light entity that can be dimmed; a switch is just switched on and off."
       ],
       "external_light_lead_time": [
        "Lead time",
        "Wait after switching the external light on, before the light of the camera is switched on and the pictures are taken."
       ],
       "external_light_turn_off": [
        "Switch off afterwards",
        "Only in the mode \"Only while taking pictures\": switches the light off after the pictures, also when taking or reading them fails."
       ]
      }
     },
     "image_section": {
      "name": "Picture crop",
      "description": "Only this part of the picture is sent to the AI. Crop wide-angle cameras to the display; in the dashboard the crop can be drawn with the mouse.",
      "fields": {
       "crop_left": [
        "Left",
        "Left edge of the crop in percent of the width of the turned picture."
       ],
       "crop_top": [
        "Top",
        "Top edge of the crop in percent of the height of the turned picture."
       ],
       "crop_right": [
        "Right",
        "Right edge of the crop in percent of the width of the turned picture."
       ],
       "crop_bottom": [
        "Bottom",
        "Bottom edge of the crop in percent of the height of the turned picture."
       ],
       "rotate": [
        "Rotate",
        "Turns the picture clockwise by this angle (negative: counterclockwise), e.g. 90 for a camera mounted sideways or a few degrees for a display that sits askew. Turned before cropping, the crop refers to the turned picture."
       ],
       "exposure": [
        "Exposure",
        "Brightness of the picture for the AI: 100 % leaves it unchanged, below is darker (against reflections and overexposure), above is brighter."
       ],
       "enhance": [
        "Enhance picture",
        "Turns the picture grey, evens out the lighting and stretches the contrast before the AI reads it. Helps when the light leaves a bright spot on the display glass and dark corners, or with pale LCD segments. Not shown in the live picture; take a test picture to see it."
       ]
      }
     },
     "display_section": {
      "name": "Display",
      "description": "What the display shows. The hints are passed on to the AI.",
      "fields": {
       "unit": [
        "Unit",
        "Unit shown on the display (e.g. MWh, kWh or m³)."
       ],
       "decimals": [
        "Decimals",
        "Number of decimals shown on the display."
       ],
       "hints": [
        "Hints for the AI",
        "Optional. What is special about this display, e.g. lines that are not part of a digit, or which digits to ignore."
       ],
       "prompt": [
        "Own instructions for the AI",
        "Replace the whole generated instructions (leave empty for the standard). Unit, decimals and hints are then no longer inserted. The AI should still answer only with the number or “unreadable”."
       ]
      }
     },
     "schedule_section": {
      "name": "Schedule",
      "description": "How often the meter is read automatically.",
      "fields": {
       "interval": [
        "Interval",
        "Time between two automatic readings."
       ],
       "condition_entity": [
        "Condition",
        "Optional. While this entity is 'off', the second interval applies (e.g. a heating day sensor)."
       ],
       "interval_off": [
        "Interval while the condition is off",
        "Only used together with a condition."
       ]
      }
     },
     "checks_section": {
      "name": "Checks",
      "description": "Majority vote and plausibility check of a reading.",
      "fields": {
       "max_rate": [
        "Largest increase per hour",
        "In the meter unit. A larger increase since the last valid reading is rejected (e.g. 0.05 MWh = 50 kW)."
       ],
       "max_correction": [
        "Largest correction",
        "In the meter unit. A smaller value than before is only taken when it is at most this much lower and confirmed by further pictures."
       ],
       "max_attempts": [
        "Pictures per reading",
        "Most pictures until a value has been read twice."
       ],
       "confirmations": [
        "Confirmation pictures",
        "Further pictures that must all show a smaller value before it is taken as a correction."
       ],
       "history_hint": [
        "Last readings to the AI",
        "The AI gets the last 3 valid readings as a hint, to decide an unclear digit plausibly. It should still read only what the picture shows; the checks here stay in place. Can tempt the AI to name an expected value, so use it mainly for displays that are hard to read."
       ],
       "meter_ai_task_entity": [
        "Own AI task",
        "Optional. Instead of the AI task of the integration."
       ]
      }
     },
     "notify_section": {
      "name": "Notifications",
      "description": "From the how-many-th time in a row a notification appears in Home Assistant (0 = never, 1 = at once). A valid reading starts the count again. Only while notifications are switched on in the settings of the integration.",
      "fields": {
       "notify_smaller": [
        "Smaller than before",
        "Value below the last valid one and not confirmed as a correction (rejected)."
       ],
       "notify_too_large": [
        "Increase too large",
        "Value rose more than the largest increase per hour allows (rejected)."
       ],
       "notify_corrected": [
        "Corrected",
        "Smaller value confirmed by more pictures and taken."
       ],
       "notify_failed": [
        "Unreadable or error",
        "The AI reads nothing clear, or the camera or AI is not reachable. Unreadable readings do not interrupt the count of the other cases."
       ]
      }
     },
     "vacation_section": {
      "name": "Vacation",
      "description": "Warns when something runs on vacation: a message, a logbook entry and the event house_assistant_vacation_alert, once per vacation and case. Counted from the last valid reading before the vacation. Not for the heat meter.",
      "fields": {
       "vacation_alert": [
        "Warn on vacation",
        "Default: on for a water meter, else off."
       ],
       "vacation_amount": [
        "Amount",
        "Used since the vacation started, in litres (water, gas) or kWh (electricity), from which it warns. 0 = off. Default water: 20 L."
       ],
       "vacation_rate": [
        "Mean flow or power",
        "Mean since the vacation started in L/h or kW (after an hour at the earliest) from which it warns. For gas and electricity enter the base load. 0 = off. Default water: 5 L/h."
       ]
      }
     }
    }
   }
  },
  "errors": {
   "config": {
    "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
    "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
    "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
    "name_required": "Please enter a name.",
    "azimuth_equal": "Azimuth from and to must differ.",
    "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
    "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
    "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
    "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
    "invalid_day_month": "Please enter a valid date (DD.MM., e.g. 01.10.); a day like 31.02. does not exist.",
    "invalid_auth": "Anthropic rejected the API key. Check it at console.anthropic.com under API keys and paste it without spaces. Without a key the local control keeps running.",
    "cannot_connect": "Anthropic cannot be reached. Check the internet connection, proxy and firewall. The key was not saved.",
    "max_below_base": "The maximum interval must be at least the check interval (e.g. check every 4 h, at most every 48 h).",
    "outdoor_required": "Choose an outdoor temperature sensor or a weather entity."
   },
   "options": {
    "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
    "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
    "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
    "name_required": "Please enter a name.",
    "azimuth_equal": "Azimuth from and to must differ.",
    "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
    "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
    "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
    "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
    "invalid_day_month": "Please enter a valid date (DD.MM., e.g. 01.10.); a day like 31.02. does not exist.",
    "invalid_auth": "Anthropic rejected the API key. Check it at console.anthropic.com under API keys and paste it without spaces. Without a key the local control keeps running.",
    "cannot_connect": "Anthropic cannot be reached. Check the internet connection, proxy and firewall. The key was not saved.",
    "max_below_base": "The maximum interval must be at least the check interval (e.g. check every 4 h, at most every 48 h).",
    "outdoor_required": "Choose an outdoor temperature sensor or a weather entity."
   },
   "room": {
    "name_required": "Please enter a name.",
    "name_in_use": "Another room already has this name. Please choose a unique name (export and import find rooms by name).",
    "switch_in_use": "This switch already controls another room. Each circuit can belong to one room only: choose another switch, or remove it from the other room first.",
    "min_above_max": "The smallest target must be below the largest target. Please change one of the two values (both in °C).",
    "target_out_of_range": "The start target must lie between the smallest and the largest target. Please adjust it or the limits.",
    "reference_incomplete": "Reference temperature and reference humidity only work together: choose both sensors or neither.",
    "temperature_required": "A heating circuit and the ventilation advice need a temperature sensor of the room."
   },
   "group": {
    "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
    "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
    "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
    "name_required": "Please enter a name.",
    "azimuth_equal": "Azimuth from and to must differ.",
    "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
    "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
    "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
    "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window."
   },
   "window": {
    "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
    "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
    "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
    "name_required": "Please enter a name.",
    "azimuth_equal": "Azimuth from and to must differ.",
    "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
    "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
    "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
    "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
    "contact_in_use": "This contact already belongs to another window. A contact belongs to one window only, otherwise one opening would count twice.",
    "contact_or_cover_required": "Choose a window contact or a cover; without either the window does nothing.",
    "unknown_room": "This room does not exist any more. Choose another one."
   },
   "meter": {
    "name_required": "Please enter a name.",
    "camera_required": "Please select a camera."
   }
  },
  "choices": {
   "effort": {
    "auto": "Auto (model default)",
    "low": "Low",
    "medium": "Medium",
    "high": "High"
   },
   "external_light_mode": {
    "capture": "Only while taking pictures",
    "permanent": "Always on"
   },
   "forecast_type": {
    "auto": "Automatic",
    "daily": "Daily",
    "twice_daily": "Twice daily",
    "hourly": "Hourly"
   },
   "heating_type": {
    "underfloor": "Underfloor heating",
    "radiator": "Radiators",
    "other": "Other (e.g. wall heating)"
   },
   "language": {
    "auto": "Like Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "meter_type": {
    "heat": "Heat meter",
    "water": "Water meter",
    "gas": "Gas meter",
    "electricity": "Electricity meter",
    "other": "Other meter"
   },
   "modules": {
    "heating": "Heating",
    "shutter": "Covers",
    "meter": "Meters"
   },
   "month": {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
   },
   "morning_mode": {
    "time": "Fixed time (workday / weekend)",
    "sun": "Sun (sunrise or elevation)",
    "brightness": "Brightness of the group",
    "trigger": "Trigger entity (alarm, motion, switch)"
   },
   "morning_sun_event": {
    "sunrise": "Sunrise",
    "elevation": "Sun elevation"
   },
   "override_trigger": {
    "movement": "Only when the cover really moves",
    "command": "With every command by hand, also without movement"
   },
   "service_action": {
    "open": "Open",
    "close": "Close",
    "evening": "Evening position",
    "sun_protection": "Sun protection position",
    "ventilation": "Ventilation position",
    "position": "Position"
   },
   "weekday": {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
    "sun": "Sunday"
   },
   "window_size": {
    "small": "Small (e.g. skylight)",
    "medium": "Medium",
    "large": "Large (e.g. double casement)",
    "door": "Door (e.g. balcony door)"
   }
  },
  "states": {
   "select.heating_day_override": {
    "auto": "Automatic",
    "heat_today": "Heat today",
    "off_today": "No heating today"
   },
   "sensor.meter_status": {
    "ok": "Valid",
    "corrected": "Corrected",
    "unreadable": "Unreadable",
    "error": "Camera or AI error",
    "smaller": "Smaller than before",
    "too_large": "Increase too large",
    "manual": "Set by hand"
   },
   "sensor.next_action.action": {
    "evening": "Evening run",
    "morning": "Morning opening",
    "override_end": "End of the override",
    "sun_enter": "Sun enters the sector",
    "sun_leave": "Sun leaves the sector",
    "protection_end": "Weather protection may end"
   },
   "sensor.window_status": {
    "off": "Automatic off",
    "startup": "Restart protection",
    "override": "Manual override",
    "evening": "Closed for the evening",
    "sun_protection": "Sun protection",
    "vacation": "Vacation simulation",
    "ready": "Ready",
    "protection": "Weather protection"
   },
   "sensor.ventilation": {
    "unknown": "Unknown",
    "close_window": "Close window",
    "ventilate_now": "Ventilate now",
    "ventilation_useful": "Ventilation useful",
    "do_not_ventilate": "Do not ventilate",
    "blocked": "Ventilation blocked",
    "optimal": "All fine",
    "vacation": "Vacation"
   },
   "sensor.decision_phase": {
    "ai_leads": "AI leads",
    "shared": "Shared",
    "rule_leads": "Rule leads"
   },
   "sensor.room_status": {
    "off": "Off",
    "out_of_season": "Outside heating period",
    "no_heating_day": "No heating day",
    "idle": "Ready",
    "heating": "Heating",
    "window_open": "Window open",
    "recovery": "Recovery after airing",
    "frost_protection": "Frost protection",
    "vacation": "Vacation",
    "preheat": "Preheating for return",
    "emergency": "Emergency rule",
    "sensor_error": "Sensor error",
    "actuator_unavailable": "Actuator unavailable",
    "no_circuit": "No heating circuit"
   }
  }
 }
};
export const HOUSE = {
 "de": {
  "fields": {
   "room": {
    "name": [
     "Name",
     "Name des Raums, auch für das Gerät und seine Entitäten."
    ],
    "area": [
     "Bereich (Home Assistant)",
     "Optional. Das Gerät des Raums kommt in diesen Bereich; seine Etage zählt für das Querlüften."
    ],
    "temperature_sensor": [
     "Temperatursensor",
     "Raumtemperatur. Ohne Sensor hat der Raum keine Heizung und keine Lüftungsempfehlung (z. B. ein Raum nur für Rollos)."
    ],
    "humidity_sensor": [
     "Feuchtesensor",
     "Relative Luftfeuchte, nötig für die Lüftungsempfehlung."
    ],
    "heater_switch": [
     "Heizkreis-Schalter",
     "Schalter des Stellantriebs (z. B. ein Relais). Leer lassen für einen Raum nur mit Lüftungsempfehlung."
    ],
    "default_target": [
     "Start-Sollwert",
     "Sollwert, bis du ihn an der Thermostatkarte änderst."
    ],
    "min_target": [
     "Kleinster Sollwert",
     "Kleinster Wert der Thermostatkarte."
    ],
    "max_target": [
     "Größter Sollwert",
     "Größter Wert der Thermostatkarte."
    ],
    "min_on_time": [
     "Mindest-Einschaltzeit",
     "Wird immer eingehalten (schont den Stellantrieb). Wird nicht gelernt."
    ],
    "min_off_time": [
     "Mindest-Ausschaltzeit",
     "Wird immer eingehalten. Wird nicht gelernt."
    ],
    "heating_type": [
     "Heizungsart",
     "Wie der Kreis heizt. Ein Fußboden speichert Wärme über Stunden, Heizkörper reagieren in Minuten; die KI beurteilt die gelernten Werte entsprechend."
    ],
    "window_delay": [
     "Fensterverzögerung (Startwert)",
     "So lange offen pausiert die Heizung. Die KI darf den Wert anpassen."
    ],
    "recovery_time": [
     "Erholungszeit nach Lüften (Startwert)",
     "Nach dem Schließen wird so lange gewartet, weil Estrich und Wände den Raum oft selbst aufheizen. Wird danach gelernt."
    ],
    "dead_time": [
     "Totzeit bis der Raum wärmer wird (Startwert)",
     "Zeit vom Einschalten, bis der Raum wärmer wird; bei Fußbodenheizung oft 30-90 min, bei Heizkörpern 5-20 min. Wird danach gelernt."
    ],
    "puffer": [
     "Reserve über Sollwert (Startwert)",
     "Heiztag-Regel: wie weit ein Raum beim Nachtlauf über dem Sollwert liegen muss, um einen Tag ohne Heizen zu überstehen (z. B. 0,7 K). Wird danach gelernt."
    ],
    "ventilation_rh_threshold": [
     "Feuchte-Schwelle",
     "Startwert der relativen Feuchte, ab der Lüften empfohlen wird (z. B. 65 % für Bäder); die KI-Lüftungsprüfung passt ihn an den Raum an."
    ],
    "reference_temperature": [
     "Referenz-Temperatur statt außen",
     "Optional, für Räume, die über einen anderen Raum gelüftet werden."
    ],
    "reference_humidity": [
     "Referenz-Feuchte statt außen",
     "Zusammen mit der Referenz-Temperatur nötig."
    ],
    "ventilation_block_entity": [
     "Lüftungs-Sperr-Entität",
     "Optional. Solange sie sperrt, wird kein Lüften empfohlen: eine Abdeckung (cover), solange sie geschlossen ist (z. B. Beschattung unten), eine Klima-Entität oder ein Warmwasserbereiter, solange nicht aus (z. B. Klimaanlage läuft), ein Schalter, Binärsensor, Ventilator o. Ä., solange an."
    ],
    "draft_group_1": [
     "Kombination 1",
     "z. B. Kinderzimmer + Bad; eine zweite Kombination z. B. Kinderzimmer + Schlafzimmer."
    ],
    "draft_group_2": [
     "Kombination 2",
     ""
    ],
    "draft_group_3": [
     "Kombination 3",
     ""
    ],
    "draft_group_4": [
     "Kombination 4",
     ""
    ],
    "cooling_entity": [
     "Klimaanlage",
     "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage. Gilt für alle Fenster des Raums ohne eigene Klimaanlage."
    ]
   },
   "window": {
    "name": [
     "Name",
     "Wird auch für das Gerät und seine Entitäten verwendet."
    ],
    "room": [
     "Raum",
     "Optional. Die Heizung des Raums nutzt die Kontakte des Fensters; das Rollo nimmt Raumtemperatur und Klimaanlage des Raums."
    ],
    "size": [
     "Größe",
     "Wie schnell Lüften die Luft austauscht: Die vorgeschlagene Lüftdauer richtet sich danach, und zum Lüften wird die größte Öffnung vorgeschlagen. Die Größe gilt für jeden Kontakt des Fensters."
    ],
    "cover": [
     "Rollo",
     "Optional. 100 % = offen, 0 % = zu. Ohne Rollo dient das Fenster nur der Heizung."
    ],
    "window_sensors": [
     "Fensterkontakte",
     "'on' = offen. Fenstergriffe mit den Zuständen open, tilted und closed gehen auch. Unbekannt oder nicht verfügbar zählt als offen. Ein Kontakt gehört zu genau einem Fenster."
    ],
    "tilt_sensors": [
     "Kipp-Kontakte",
     "'on' = gekippt. Solange das Fenster nur gekippt ist, schließen die Rollos höchstens bis zur Lüftungsposition."
    ],
    "group": [
     "Gruppe",
     "Himmelsrichtung. Ohne Gruppe hat das Fenster keinen Sonnenschutz."
    ]
   },
   "settings": {
    "outdoor_temperature": [
     "Außentemperatursensor",
     "Für Heizung und Rollos (z. B. ein Helfer, der mehrere Sensoren zusammenfasst). Ohne ihn gilt die aktuelle Temperatur der Wetter-Entität."
    ],
    "outdoor_humidity": [
     "Außenfeuchtesensor",
     "Optional. Für die Lüftungsempfehlung der Heizung; ohne Sensor wird die Luftfeuchte der Wetter-Entität genutzt."
    ],
    "weather": [
     "Wetter-Entität",
     "Empfohlen. Ihre Vorhersage nutzen die Heiztag-Entscheidung, die Sonnenprognose der Heizung und der Sommertag der Rollos. Ohne Außensensor gilt ihre aktuelle Temperatur."
    ],
    "language": [
     "Sprache der Meldungen",
     "Logbuch, letzter Grund, Push-Nachrichten und Benachrichtigungen aller Module. Automatisch = die Sprache von Home Assistant."
    ],
    "notify_services": [
     "Benachrichtigungsdienste",
     "Erhalten die Meldungen des Hauses, z. B. wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
    ],
    "workday_entity": [
     "Werktag-Sensor",
     "Optional, z. B. die Workday-Integration (berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
    ],
    "weekend_days": [
     "Wochenendtage",
     "Nur ohne Werktag-Sensor: an diesen Tagen gilt z. B. die Wochenend-Uhrzeit der Morgenöffnung."
    ],
    "house_azimuth": [
     "Vorderseite zeigt nach",
     "Himmelsrichtung, in die die Vorderseite schaut (90° = Ost, 180° = Süd, 270° = West), z. B. auf einer Karte abgelesen. Für das Haus im Sonnenkompass der Rollos."
    ],
    "house_width": [
     "Länge der Vorderseite",
     "Gilt auch für die Rückseite. Mit der Tiefe erscheint das Haus im Sonnenkompass, und der Luftzug durch Räume zwischen zwei offenen Fenstern wird erkannt."
    ],
    "house_depth": [
     "Tiefe",
     "Länge der beiden Seitenwände."
    ],
    "draft_reach": [
     "Luftzug-Reichweite",
     "Wie weit ein Raum von der Linie zwischen zwei offenen Fenstern anderer Räume entfernt sein darf, um ihren Luftzug abzubekommen (Standard 2 m)."
    ],
    "modules": [
     "Module",
     "Die Teile des Hauses, die House Assistant steuern soll. Ein abgeschaltetes Modul behält seine Einstellungen."
    ],
    "show_panel": [
     "Dashboard in der Seitenleiste",
     "Aus: Das Dashboard verschwindet aus der Seitenleiste, bleibt aber über „Einstellungen“ bei der Integration erreichbar."
    ]
   },
   "vacation": {
    "vacation_entities": [
     "Externe Urlaubs-Entitäten",
     "Ist eine davon an, gilt ebenfalls Urlaub (z. B. ein input_boolean oder ein Kalender). Gilt für Heizung und Rollos; ohne Eintrag hier gelten die Entitäten in deren Einstellungen."
    ],
    "return_entity": [
     "Externe Rückkehr",
     "Optional: input_datetime, datetime- oder Zeitstempel-Entität. Die Heizung heizt darauf vor; eine eigene Rückkehr des Schalters hat Vorrang."
    ],
    "vacation_window_alert": [
     "Offene Fenster melden",
     "Zu Beginn des Urlaubs eine Meldung mit allen offenen, gekippten oder unbekannten Fenstern, im Urlaub sofort eine Meldung, wenn ein Fenster geöffnet oder gekippt wird. An die Benachrichtigungsdienste des Hauses, ohne sie als Benachrichtigung in Home Assistant."
    ],
    "vacation_ventilation_pause": [
     "Lüftungsempfehlung ruht",
     "Im Urlaub zeigt die Lüftungsempfehlung „Urlaub“, „Lüften empfohlen“ ist aus. Urlaubsminuten zählen nicht für die KI-Lüftungsprüfung und gehen nicht ins Feuchteprofil ein."
    ],
    "vacation_heat_protection": [
     "Hitzeschutz im Urlaub",
     "Der Sonnenschutz senkt im Urlaub ab, ohne auf Raumtemperatur, Klimaanlage oder Heizbedarf zu warten. Sommertag, Außentemperatur, Sonnensensoren, Haltezeiten und der Sonnenschalter des Fensters gelten weiter."
    ]
   }
  },
  "choices": {
   "language": {
    "auto": "Wie Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "weekday": {
    "mon": "Montag",
    "tue": "Dienstag",
    "wed": "Mittwoch",
    "thu": "Donnerstag",
    "fri": "Freitag",
    "sat": "Samstag",
    "sun": "Sonntag"
   },
   "modules": {
    "heating": "Heizung",
    "shutter": "Rollos",
    "meter": "Zähler"
   }
  },
  "errors": {
   "name_required": "Bitte einen Namen eingeben.",
   "name_in_use": "Ein anderer Raum heißt schon so. Bitte einen eindeutigen Namen wählen (Export und Import finden Räume über den Namen).",
   "switch_in_use": "Dieser Schalter steuert bereits einen anderen Raum. Jeder Heizkreis gehört zu genau einem Raum: wähle einen anderen Schalter oder entferne ihn zuerst aus dem anderen Raum.",
   "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
   "target_out_of_range": "Der Start-Sollwert muss zwischen dem kleinsten und dem größten Sollwert liegen. Bitte ihn oder die Grenzen anpassen.",
   "reference_incomplete": "Referenztemperatur und Referenzfeuchte gehen nur zusammen: beide Sensoren wählen oder keinen.",
   "temperature_required": "Für Heizkreis und Lüftungsempfehlung braucht der Raum einen Temperatursensor.",
   "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
   "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
   "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
   "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
   "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
   "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
   "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
   "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
   "contact_in_use": "Dieser Kontakt gehört schon zu einem anderen Fenster. Jeder Kontakt gehört zu genau einem Fenster, sonst zählte eine Öffnung doppelt.",
   "contact_or_cover_required": "Bitte einen Fensterkontakt oder ein Rollo wählen; ohne beides tut das Fenster nichts.",
   "unknown_room": "Diesen Raum gibt es nicht mehr. Bitte einen anderen wählen.",
   "departure_after_return": "Die Abreise muss vor der Rückkehr liegen.",
   "return_in_past": "Die Rückkehr liegt in der Vergangenheit."
  },
  "sizes": {
   "small": "Klein (z. B. Dachfenster)",
   "medium": "Mittel",
   "large": "Groß (z. B. zweiflügelig)",
   "door": "Tür (z. B. Balkontür)"
  }
 },
 "en": {
  "fields": {
   "room": {
    "name": [
     "Name",
     "Name of the room, also used for the device and its entities."
    ],
    "area": [
     "Area",
     "Optional. The device of the room is placed in this area; its floor counts for cross ventilation."
    ],
    "temperature_sensor": [
     "Temperature sensor",
     "Room temperature. Without a sensor the room has no heating and no ventilation advice (e.g. a room only for covers)."
    ],
    "humidity_sensor": [
     "Humidity sensor",
     "Relative humidity, needed for the ventilation recommendation."
    ],
    "heater_switch": [
     "Heating circuit switch",
     "Switch of the actuator (e.g. a relay). Leave empty for a room with ventilation recommendation only."
    ],
    "default_target": [
     "Initial target temperature",
     "Target until you change it on the thermostat card."
    ],
    "min_target": [
     "Minimum target",
     "Lowest value of the thermostat card."
    ],
    "max_target": [
     "Maximum target",
     "Highest value of the thermostat card."
    ],
    "min_on_time": [
     "Minimum on time",
     "Always respected (protects the actuator). Not learned."
    ],
    "min_off_time": [
     "Minimum off time",
     "Always respected. Not learned."
    ],
    "heating_type": [
     "Heating type",
     "How the circuit heats. A floor stores heat for hours, radiators react within minutes; the AI judges the learned values with this in mind."
    ],
    "window_delay": [
     "Window delay (start value)",
     "Window open this long pauses heating. The AI may adjust it."
    ],
    "recovery_time": [
     "Recovery time after airing (start value)",
     "After closing, heating waits this long because floor and walls often reheat the room. Learned afterwards."
    ],
    "dead_time": [
     "Dead time until the room warms (start value)",
     "Time from switching on until the room gets warmer; underfloor heating often 30-90 min, radiators 5-20 min. Learned afterwards."
    ],
    "puffer": [
     "Margin above target (start value)",
     "Heating day rule: how far above the target a room must be at the nightly run to manage a day without heating (e.g. 0.7 K). Learned afterwards."
    ],
    "ventilation_rh_threshold": [
     "Humidity threshold",
     "Start value of the relative humidity from which ventilating is recommended (e.g. 65 % for bathrooms); the AI ventilation check adjusts it to the room."
    ],
    "reference_temperature": [
     "Reference temperature instead of outdoor",
     "Optional, for rooms aired via another room."
    ],
    "reference_humidity": [
     "Reference humidity instead of outdoor",
     "Required together with the reference temperature."
    ],
    "ventilation_block_entity": [
     "Ventilation block entity",
     "Optional. While it blocks, no ventilation is recommended: a cover while closed (e.g. sun protection down), a climate entity or water heater while not off (e.g. air conditioner running), a switch, binary sensor, fan or similar while on."
    ],
    "draft_group_1": [
     "Combination 1",
     "e.g. kids' room + bathroom; a second combination e.g. kids' room + bedroom."
    ],
    "draft_group_2": [
     "Combination 2",
     ""
    ],
    "draft_group_3": [
     "Combination 3",
     ""
    ],
    "draft_group_4": [
     "Combination 4",
     ""
    ],
    "cooling_entity": [
     "Air conditioner",
     "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner. Applies to every window of the room without its own air conditioner."
    ]
   },
   "window": {
    "name": [
     "Name",
     "Also used for the device and its entities."
    ],
    "room": [
     "Room",
     "Optional. The heating of the room uses the contacts of the window; the cover takes room temperature and air conditioner of the room."
    ],
    "size": [
     "Size",
     "How fast airing exchanges the air: the suggested airing time follows it, and the largest opening is suggested for airing. The size applies to every contact of the window."
    ],
    "cover": [
     "Cover",
     "Optional. 100 % = open, 0 % = closed. Without a cover the window only serves the heating."
    ],
    "window_sensors": [
     "Window contacts",
     "'on' = open. Window handles with the states open, tilted and closed work as well. Unknown or unavailable counts as open. A contact belongs to one window only."
    ],
    "tilt_sensors": [
     "Tilt contacts",
     "'on' = tilted. While the window is only tilted, covers close no further than the ventilation position."
    ],
    "group": [
     "Group",
     "Direction of the sun. Without a group the window has no sun protection."
    ]
   },
   "settings": {
    "outdoor_temperature": [
     "Outdoor temperature sensor",
     "For heating and covers (e.g. a helper combining several sensors). Without it the current temperature of the weather entity is used."
    ],
    "outdoor_humidity": [
     "Outdoor humidity sensor",
     "Optional. For the ventilation advice of the heating; without it the humidity of the weather entity is used."
    ],
    "weather": [
     "Weather entity",
     "Recommended. Its forecast is used by the heating day decision, the expected sun of the heating and the summer day of the covers. Without an outdoor sensor its current temperature applies."
    ],
    "language": [
     "Language of messages",
     "Logbook, last reason, push messages and notifications of every module. Automatic = the language of Home Assistant."
    ],
    "notify_services": [
     "Notification services",
     "Get the messages of the house, e.g. when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
    ],
    "workday_entity": [
     "Workday sensor",
     "Optional, e.g. the Workday integration (knows public holidays). Without a sensor the weekend days decide."
    ],
    "weekend_days": [
     "Weekend days",
     "Only without a workday sensor: on these days e.g. the weekend time of the morning opening applies."
    ],
    "house_azimuth": [
     "Front faces",
     "Direction the front looks to (90° = east, 180° = south, 270° = west), e.g. read from a map. For the house in the sun compass of the covers."
    ],
    "house_width": [
     "Length of the front",
     "Also the back. With the depth the house appears in the sun compass, and the draft through rooms between two open windows is recognised."
    ],
    "house_depth": [
     "Depth",
     "Length of the two side walls."
    ],
    "draft_reach": [
     "Draft reach",
     "How far a room may be from the line between two open windows of other rooms to still get their draft (default 2 m)."
    ],
    "modules": [
     "Modules",
     "The parts of the house House Assistant takes care of. A module switched off keeps its settings."
    ],
    "show_panel": [
     "Dashboard in the sidebar",
     "Off: the dashboard disappears from the sidebar but stays reachable with \"Configure\" at the integration."
    ]
   },
   "vacation": {
    "vacation_entities": [
     "External vacation entities",
     "While one of them is on it is vacation as well (e.g. an input_boolean or a calendar). For heating and covers; without an entry here the entities in their settings apply."
    ],
    "return_entity": [
     "External return",
     "Optional: input_datetime, datetime or timestamp entity. The heating preheats for it; an own return of the switch comes first."
    ],
    "vacation_window_alert": [
     "Report open windows",
     "When the vacation starts a message with every open, tilted or unknown window; on vacation a message right away when a window is opened or tilted. To the notification services of the house, without any as a notification in Home Assistant."
    ],
    "vacation_ventilation_pause": [
     "Ventilation advice rests",
     "On vacation the ventilation advice shows “Vacation”, “ventilation recommended” is off. Vacation minutes do not count for the AI ventilation check and stay out of the humidity profile."
    ],
    "vacation_heat_protection": [
     "Heat protection on vacation",
     "On vacation the sun protection lowers without waiting for room temperature, air conditioner or heat need. Summer day, outdoor temperature, sun sensors, hold times and the sun switch of the window still apply."
    ]
   }
  },
  "choices": {
   "language": {
    "auto": "Like Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "weekday": {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
    "sun": "Sunday"
   },
   "modules": {
    "heating": "Heating",
    "shutter": "Covers",
    "meter": "Meters"
   }
  },
  "errors": {
   "name_required": "Please enter a name.",
   "name_in_use": "Another room already has this name. Please choose a unique name (export and import find rooms by name).",
   "switch_in_use": "This switch already controls another room. Each circuit can belong to one room only: choose another switch, or remove it from the other room first.",
   "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
   "target_out_of_range": "The start target must lie between the smallest and the largest target. Please adjust it or the limits.",
   "reference_incomplete": "Reference temperature and reference humidity only work together: choose both sensors or neither.",
   "temperature_required": "A heating circuit and the ventilation advice need a temperature sensor of the room.",
   "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
   "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
   "azimuth_equal": "Azimuth from and to must differ.",
   "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
   "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
   "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
   "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
   "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
   "contact_in_use": "This contact already belongs to another window. A contact belongs to one window only, otherwise one opening would count twice.",
   "contact_or_cover_required": "Choose a window contact or a cover; without either the window does nothing.",
   "unknown_room": "This room does not exist any more. Choose another one.",
   "departure_after_return": "The departure must be before the return.",
   "return_in_past": "The return is in the past."
  },
  "sizes": {
   "small": "Small (e.g. skylight)",
   "medium": "Medium",
   "large": "Large (e.g. double casement)",
   "door": "Door (e.g. balcony door)"
  }
 }
};
export const HEATING = {
 "de": {
  "fields": {
   "outdoor_temperature": [
    "Außentemperatursensor",
    "Sensor für die Außentemperatur (z. B. ein Helfer, der mehrere Sensoren zusammenfasst). Ohne ihn gilt die aktuelle Temperatur der Wetter-Entität. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "outdoor_humidity": [
    "Außenfeuchtesensor",
    "Optional. Für die Lüftungsempfehlung; ohne Sensor wird die Luftfeuchte der Wetter-Entität genutzt. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "weather": [
    "Wetter-Entität",
    "Optional, aber empfohlen. Die Vorhersage wird für die nächtliche Heiztag-Entscheidung und die Sonnenprognose genutzt. Ohne Außensensor gilt ihre aktuelle Temperatur als Außentemperatur. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "pv_power": [
    "PV-Leistungssensor",
    "Optional. PV-Leistung (W oder kW) als Indikator für Sonne. Daraus wird der Sonneneinfluss je Bereich gelernt."
   ],
   "pv_forecast": [
    "PV-Prognosesensor",
    "Optional, nur zusammen mit dem PV-Leistungssensor. Erwartete PV-Energie der nächsten Stunde (Wh oder kWh, z. B. Forecast.Solar) oder erwartete Leistung in einer Stunde (W oder kW). Ohne diesen Sensor wird die Sonne aus der stündlichen Wettervorhersage und dem Sonnenstand geschätzt."
   ],
   "heat_meter": [
    "Wärmezähler",
    "Optional. Zählerstand des Wärmezählers der hier geregelten Heizkreise (Wh, kWh, MWh, MJ oder GJ, z. B. total_increasing). Die KI sieht dann die gemessene Wärme, außerdem steht sie im Panel. Seltene und grobe Werte sind kein Problem."
   ],
   "season_start": [
    "Beginn der Heizperiode (TT.MM.)",
    "Außerhalb der Heizperiode bleiben alle Kreise aus (nur Frostschutz) und die KI wird nicht gefragt."
   ],
   "season_end": [
    "Ende der Heizperiode (TT.MM.)",
    "Letzter Tag der Heizperiode, darf im Folgejahr liegen (z. B. 31.03.)."
   ],
   "frost_temperature": [
    "Frostschutz-Mindesttemperatur",
    "Gilt immer, auch außerhalb der Heizperiode und bei ausgeschaltetem Thermostat."
   ],
   "forecast_trust": [
    "Vertrauen in die Sonnenprognose",
    "Anteil der erwarteten PV-Leistung, auf den sich die Regelung beim Zurückhalten verlässt (100 % = volle Prognose, 0 % = nur die aktuelle PV-Leistung zählt)."
   ],
   "season_start_day": [
    "Heizperiode beginnt: Tag",
    "Ab diesem Datum darf geheizt werden (z. B. 1. Oktober)."
   ],
   "season_start_month": [
    "Heizperiode beginnt: Monat",
    ""
   ],
   "season_end_day": [
    "Heizperiode endet: Tag",
    "Letzter Tag der Heizperiode (z. B. 31. März); die Periode darf über den Jahreswechsel gehen."
   ],
   "season_end_month": [
    "Heizperiode endet: Monat",
    ""
   ],
   "vacation_entities": [
    "Urlaubs-Entitäten",
    "Ist eine dieser Entitäten 'an', gilt Urlaub (z. B. ein input_boolean oder ein Kalender). Gilt nur, solange unter Einstellungen > Urlaub nichts eingetragen ist. Der Schalter „Urlaub“ des Hauses gilt immer."
   ],
   "vacation_temperature": [
    "Urlaubstemperatur",
    "Sollwert für alle Räume im Urlaub (z. B. 17 °C)."
   ],
   "return_entity": [
    "Rückkehr Datum/Uhrzeit",
    "Optional: input_datetime, Zeitstempel-Sensor oder datetime-Entität. Es wird so rechtzeitig vorgeheizt (gelernte Aufheizzeit), dass bei Rückkehr der normale Sollwert erreicht ist. Die Rückkehr des Schalters „Urlaub“ hat Vorrang; ohne sie gilt eine unter Einstellungen > Urlaub eingetragene."
   ],
   "preheat_reserve": [
    "Vorheiz-Reserve",
    "Zusätzliche Zeit zur berechneten Vorheizzeit (z. B. 30 min)."
   ],
   "vacation_ventilation_pause": [
    "Lüftungsempfehlung ruht",
    "Im Urlaub zeigt die Lüftungsempfehlung „Urlaub“, „Lüften empfohlen“ ist aus. Urlaubsminuten zählen nicht für die KI-Lüftungsprüfung und gehen nicht ins Feuchteprofil ein."
   ],
   "emergency_enabled": [
    "Notfallregel",
    "An Tagen ohne Heizbetrieb darf ein Raum trotzdem heizen, wenn die nach der Vorlaufzeit erwartete Temperatur lange und deutlich unter dem Sollwert liegt, ohne dass gelüftet wurde."
   ],
   "emergency_delta": [
    "Notfall: unter Sollwert um",
    "Wie weit die nach der Vorlaufzeit erwartete Temperatur unter dem Sollwert liegen muss (mindestens die Einschalthysterese)."
   ],
   "emergency_duration": [
    "Notfall: Dauer",
    "Wie lange die erwartete Temperatur so tief bleiben muss (z. B. 45 min)."
   ],
   "emergency_window_quiet": [
    "Notfall: keine Fensteränderung seit",
    "Lüften zählt nicht: die Fenster dürfen sich so lange nicht verändert haben."
   ],
   "force_on_below": [
    "Immer heizen unter Sollwert um",
    "So weit unter dem Sollwert heizt der Kreis unabhängig von jeder Vorhersage und der erwarteten Sonne."
   ],
   "ventilation_min_ah_advantage": [
    "Mindestvorteil absolute Feuchte",
    "Absolute Feuchte ist der Wassergehalt der Luft in g/m³, unabhängig von der Temperatur. Die Außenluft muss mindestens so viel weniger Wasser enthalten für 'Jetzt lüften' (z. B. 0,8 g/m³)."
   ],
   "ventilation_max_reference_excess": [
    "Außen höchstens wärmer um",
    "Trocknen wird nicht empfohlen, wenn es außen um mehr als diesen Wert wärmer ist als innen."
   ],
   "ventilation_energy_rh_per_k": [
    "Energiespar-Zuschlag",
    "Energiesparen: In der Heizperiode kostet Lüften Wärme, umso mehr, je kälter es draußen ist. Die Feuchte muss die Schwelle dann um so viel je Kelvin übersteigen, wie es draußen kälter ist als im Raum (z. B. 0,25 %/K: bei 21 °C innen und 1 °C außen 5 % mehr), höchstens bis 70 %; darüber wird gegen Schimmel immer gelüftet. 0 = aus. Startwert, die KI passt ihn je Raum an."
   ],
   "ventilation_mould_rh": [
    "Schimmelgrenze",
    "Ab dieser relativen Feuchte wird immer zum Lüften geraten, auch bei Frost und direkt nach einer Lüftung; der Energiespar-Zuschlag geht nie darüber. Für Räume mit kalten Außenwänden niedriger setzen. Startwert, die KI passt ihn je Raum an."
   ],
   "ventilation_airing_target_below": [
    "Lüftziel unter der Schwelle",
    "Die vorgeschlagene Lüftdauer zielt so weit unter die Feuchte-Schwelle. Startwert für die KI."
   ],
   "ventilation_airing_time_factor": [
    "Lüftdauer-Faktor",
    "Skaliert die vorgeschlagene Lüftdauer. Sobald zwei Lüftungen ausgewertet sind, wird sie aus dem gelernten Luftaustausch des Raums und dem Temperaturunterschied berechnet, vorher aus der Außentemperatur (5 Minuten bei Frost bis 20 Minuten bei Wärme). Startwert für die KI."
   ],
   "ventilation_airing_min_minutes": [
    "Kürzeste Lüftdauer",
    "Startwert für die KI."
   ],
   "ventilation_airing_max_minutes": [
    "Längste Lüftdauer",
    "Startwert für die KI."
   ],
   "ventilation_airing_pause": [
    "Pause nach dem Lüften",
    "Nach dem Lüften kommt Feuchte aus Wänden und Möbeln zurück. Erst nach dieser Pause wird wieder zum Trocknen geraten (unter der Schimmelgrenze); das spart Wärme und Nerven. Startwert für die KI."
   ],
   "ventilation_min_cooling_advantage": [
    "Mindest-Kühlvorteil",
    "'Lüften sinnvoll', wenn es innen mindestens so viel wärmer ist als außen (nicht während Heizbetrieb)."
   ],
   "ventilation_cooling_margin": [
    "Mindestabstand über Sollwert für Kühlen",
    "In der Heizperiode wird 'Lüften sinnvoll' (Kühlen) nur empfohlen, wenn der Raum mindestens so viel wärmer ist als sein Sollwert. Außerhalb der Heizperiode gilt das nicht. Räume ohne Heizkreis nutzen ihren Start-Sollwert."
   ],
   "ventilation_cooling_min_temp": [
    "Kühlen erst ab Raumtemperatur",
    "'Lüften sinnvoll' (Kühlen) erst ab dieser Raumtemperatur, ganzjährig. 0 = aus. Zusätzlich wird Kühlen nie empfohlen, wenn die Außenluft die relative Feuchte des Raums über seine Feuchte-Schwelle bringen würde."
   ],
   "night_start_hour": [
    "Nacht beginnt um",
    "Bei einem anderen Raum als Referenz zählt der Kühlvorteil nur nachts."
   ],
   "night_end_hour": [
    "Nacht endet um",
    "Ende der Nacht (Uhrzeit, z. B. 08:00)."
   ],
   "ventilation_ai_enabled": [
    "KI passt Lüftung je Raum an",
    "Ganzjährig prüft die KI die Lüftungsschwellen jedes Raums mit Feuchtesensor: Sie lernt, was in jedem Raum üblich ist, wie tief die Feuchte überhaupt sinken kann und was Lüften wirklich bringt. Nutzt das gemeinsame KI-Monatsbudget."
   ],
   "ventilation_check_interval": [
    "Grundintervall Lüftungsprüfung",
    "Erstes Intervall; es verdoppelt sich mit jeder Prüfung ohne relevante Änderung und beginnt von vorn, wenn ein Raum lange feucht bleibt oder sich ein Wert ändert."
   ],
   "ventilation_check_max_interval": [
    "Höchstintervall Lüftungsprüfung",
    "Länger wird das Intervall nie."
   ],
   "model": [
    "Claude-Modell",
    "Modell für alle KI-Abfragen. Die Preise sind Vorschläge für das gewählte Modell und änderbar."
   ],
   "effort": [
    "Denkaufwand",
    "Claude denkt vor der Antwort nach. Mehr Aufwand kann bessere Antworten geben, braucht aber mehr Tokens, die als Ausgabe abgerechnet werden. 'auto' überlässt es dem Modell."
   ],
   "nightly_time": [
    "Uhrzeit des Nachtlaufs",
    "Tägliche Entscheidung, ob heute geheizt wird (zugleich Beginn des bewerteten Tages)."
   ],
   "check_interval": [
    "Prüfintervall",
    "Grundintervall der periodischen KI-Prüfung an Heiztagen (z. B. 4 h). Es verdoppelt sich nach jeder Prüfung ohne relevante Änderung."
   ],
   "check_max_interval": [
    "Maximales Prüfintervall",
    "Obergrenze für das verdoppelte Intervall (z. B. 48 h)."
   ],
   "monthly_budget": [
    "Monatsbudget",
    "In US-Dollar, wie Anthropic abrechnet. Keine KI-Abfragen mehr, sobald die Kosten des Monats diesen Wert erreichen (bis zum Monatswechsel). Eine Prüfung kostet meist wenige Cent, 5 USD reichen also für etwa 100 bis 200 Abfragen."
   ],
   "price_input": [
    "Preis Eingabe-Tokens",
    "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
   ],
   "price_output": [
    "Preis Ausgabe-Tokens",
    "US-Dollar pro Million Tokens, wie Anthropic abrechnet (Denken zählt als Ausgabe)."
   ],
   "price_cache_write": [
    "Preis Cache schreiben",
    "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
   ],
   "price_cache_read": [
    "Preis Cache lesen",
    "US-Dollar pro Million Tokens, wie Anthropic abrechnet."
   ],
   "max_output_tokens": [
    "Maximale Ausgabe-Tokens",
    "Obergrenze je Antwort, Denken eingeschlossen (zu niedrig schneidet Antworten ab; sie sind bezahlt, werden aber verworfen). Auch Obergrenze der Kostenschätzung vor einer Abfrage."
   ],
   "theta": [
    "Heizgrenze theta (gelernt)",
    "Aktuelle Schwelle der Heiztag-Regel: liegt die Prognose-Höchsttemperatur darunter, wird geheizt. Eine Änderung ersetzt den gelernten Wert; danach wird von hier aus weiter gelernt."
   ],
   "too_cold_margin": [
    "Zu kalt unter Sollwert um",
    "Bewertung: ein Raum gilt als zu kalt unter Sollwert minus diesem Wert (Lüften ausgenommen)."
   ],
   "too_cold_minutes": [
    "Minuten zu kalt für Heizbedarf",
    "Bewertung: so viele Minuten zu kalt bedeuten Heizbedarf."
   ],
   "theta_step_up": [
    "Heizgrenze: Schritt nach oben",
    "Nach Fehler A, also wenn es an einem Tag ohne Heizen zu kalt wurde (z. B. 1,0 K)."
   ],
   "theta_step_down": [
    "Heizgrenze: Schritt nach unten",
    "Nach Fehler B, also wenn geheizt wurde, obwohl es nicht nötig war (z. B. 1,0 K)."
   ],
   "puffer_step_up": [
    "Reserve über Sollwert: Schritt nach oben",
    "Nach Fehler A für den kalten Raum."
   ],
   "puffer_step_down": [
    "Reserve über Sollwert: Schritt nach unten",
    "Nach Fehler B."
   ],
   "phase_shared_min_days": [
    "Tage bis gemeinsame Entscheidung",
    "Wer über den Heiztag entscheidet: zuerst führt die KI, dann entscheiden KI und Regel gemeinsam, zuletzt führt die Regel. 'KI führt' -> 'gemeinsam' nach so vielen bewerteten Tagen (z. B. 14)."
   ],
   "phase_shared_min_agreement": [
    "Übereinstimmung für gemeinsam",
    "Mindest-Übereinstimmung von Regel und KI."
   ],
   "phase_rule_min_days": [
    "Tage bis Regel führt",
    "Phase 'gemeinsam' -> 'Regel führt' nach so vielen Tagen in 'gemeinsam'."
   ],
   "phase_rule_min_agreement": [
    "Übereinstimmung für Regel führt",
    "Mindest-Übereinstimmung von Regel und KI."
   ],
   "phase_max_rule_errors": [
    "Erlaubte Regelfehler",
    "Höchstens so viele Regelfehler im Zeitraum für einen Phasenwechsel."
   ],
   "phase_fallback_errors_7d": [
    "Regelfehler in 7 Tagen für Rückfall",
    "So viele Regelfehler in 7 Tagen führen eine Phase zurück."
   ],
   "phase_ai_check_every_days": [
    "KI-Kontrolle alle",
    "Wenn die Regel führt und sicher ist, wird die KI trotzdem alle so viele Tage gefragt."
   ],
   "api_key": [
    "Anthropic API-Key",
    "Optional. Ohne Key läuft nur die lokale Regelung. Der Key wird nur in Home Assistant gespeichert und nie protokolliert."
   ],
   "name": [
    "Name",
    "Name des Raums, auch für das Gerät und seine Entitäten."
   ],
   "area": [
    "Bereich (Home Assistant)",
    "Optional. Das Gerät des Raums kommt in diesen Bereich; seine Etage zählt für das Querlüften."
   ],
   "temperature_sensor": [
    "Temperatursensor",
    "Raumtemperatur. Ohne Sensor hat der Raum keine Heizung und keine Lüftungsempfehlung (z. B. ein Raum nur für Rollos)."
   ],
   "humidity_sensor": [
    "Feuchtesensor",
    "Relative Luftfeuchte, nötig für die Lüftungsempfehlung."
   ],
   "heater_switch": [
    "Heizkreis-Schalter",
    "Schalter des Stellantriebs (z. B. ein Relais). Leer lassen für einen Raum nur mit Lüftungsempfehlung."
   ],
   "default_target": [
    "Start-Sollwert",
    "Sollwert, bis du ihn an der Thermostatkarte änderst."
   ],
   "min_target": [
    "Kleinster Sollwert",
    "Kleinster Wert der Thermostatkarte."
   ],
   "max_target": [
    "Größter Sollwert",
    "Größter Wert der Thermostatkarte."
   ],
   "min_on_time": [
    "Mindest-Einschaltzeit",
    "Wird immer eingehalten (schont den Stellantrieb). Wird nicht gelernt."
   ],
   "min_off_time": [
    "Mindest-Ausschaltzeit",
    "Wird immer eingehalten. Wird nicht gelernt."
   ],
   "heating_type": [
    "Heizungsart",
    "Wie der Kreis heizt. Ein Fußboden speichert Wärme über Stunden, Heizkörper reagieren in Minuten; die KI beurteilt die gelernten Werte entsprechend."
   ],
   "window_delay": [
    "Fensterverzögerung (Startwert)",
    "So lange offen pausiert die Heizung. Die KI darf den Wert anpassen."
   ],
   "recovery_time": [
    "Erholungszeit nach Lüften (Startwert)",
    "Nach dem Schließen wird so lange gewartet, weil Estrich und Wände den Raum oft selbst aufheizen. Wird danach gelernt."
   ],
   "dead_time": [
    "Totzeit bis der Raum wärmer wird (Startwert)",
    "Zeit vom Einschalten, bis der Raum wärmer wird; bei Fußbodenheizung oft 30-90 min, bei Heizkörpern 5-20 min. Wird danach gelernt."
   ],
   "puffer": [
    "Reserve über Sollwert (Startwert)",
    "Heiztag-Regel: wie weit ein Raum beim Nachtlauf über dem Sollwert liegen muss, um einen Tag ohne Heizen zu überstehen (z. B. 0,7 K). Wird danach gelernt."
   ],
   "ventilation_rh_threshold": [
    "Feuchte-Schwelle",
    "Startwert der relativen Feuchte, ab der Lüften empfohlen wird (z. B. 65 % für Bäder); die KI-Lüftungsprüfung passt ihn an den Raum an."
   ],
   "reference_temperature": [
    "Referenz-Temperatur statt außen",
    "Optional, für Räume, die über einen anderen Raum gelüftet werden."
   ],
   "reference_humidity": [
    "Referenz-Feuchte statt außen",
    "Zusammen mit der Referenz-Temperatur nötig."
   ],
   "ventilation_block_entity": [
    "Lüftungs-Sperr-Entität",
    "Optional. Solange sie sperrt, wird kein Lüften empfohlen: eine Abdeckung (cover), solange sie geschlossen ist (z. B. Beschattung unten), eine Klima-Entität oder ein Warmwasserbereiter, solange nicht aus (z. B. Klimaanlage läuft), ein Schalter, Binärsensor, Ventilator o. Ä., solange an."
   ],
   "draft_group_1": [
    "Kombination 1",
    "z. B. Kinderzimmer + Bad; eine zweite Kombination z. B. Kinderzimmer + Schlafzimmer."
   ],
   "draft_group_2": [
    "Kombination 2",
    ""
   ],
   "draft_group_3": [
    "Kombination 3",
    ""
   ],
   "draft_group_4": [
    "Kombination 4",
    ""
   ],
   "cooling_entity": [
    "Klimaanlage",
    "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage. Gilt für alle Fenster des Raums ohne eigene Klimaanlage."
   ]
  },
  "learned": {
   "window_delay": [
    "Fensterverzögerung",
    "So lange offen pausiert die Heizung. Die KI darf den Wert anpassen."
   ],
   "recovery_time": [
    "Erholungszeit nach Lüften",
    "Gelernte Wartezeit nach dem Schließen der Fenster."
   ],
   "dead_time": [
    "Totzeit bis der Raum wärmer wird",
    "Gelernte Zeit, bis der Raum nach dem Einschalten wärmer wird."
   ],
   "puffer": [
    "Reserve über Sollwert",
    "Heiztag-Regel: nötiger Abstand über dem Sollwert beim Nachtlauf (gelernt)."
   ]
  },
  "sections": {
   "sensors": [
    "Sensoren",
    ""
   ],
   "heating": [
    "Heizkreis",
    ""
   ],
   "start_values": [
    "Startwerte (werden gelernt)",
    "Nur beim Anlegen des Raums. Danach werden die gelernten Werte bearbeitet."
   ],
   "ventilation": [
    "Lüftung",
    ""
   ],
   "draft": [
    "Luftzug aus anderen Räumen",
    "Fenster anderer Räume, deren gemeinsames Öffnen auch diesen Raum auskühlt (Querlüftung). Je Kombination die Fenster wählen, die zusammen offen sein müssen. Sobald alle Fenster einer Kombination offen sind, verhält sich der Raum wie bei einem eigenen offenen Fenster: Die Heizung pausiert nach der Fensterverzögerung und wartet danach die Erholungszeit ab. Eine Kombination mit nur einem Fenster löst schon allein aus."
   ],
   "sun_protection": [
    "Sonnenschutz",
    "Vorgaben für die Rollos der Fenster dieses Raums. Raumtemperatur und Sollwert kommen vom Temperatursensor und vom Thermostat des Raums, solange ein Fenster keine eigene Raumtemperatur hat."
   ],
   "learned_values": [
    "Gelernte Werte",
    "Werte, mit denen gerade geregelt wird. Eine Änderung ersetzt den gelernten bzw. von der KI angepassten Wert; danach wird von hier aus weiter gelernt."
   ]
  },
  "limits": {
   "hysteresis_on": "Einschalt-Hysterese",
   "hysteresis_off": "Ausschalt-Hysterese",
   "overshoot_factor": "Faktor Überschwingen",
   "lead_factor": "Faktor Vorlauf",
   "sun_factor": "Sonnenfaktor",
   "window_delay_min": "Fensterverzögerung",
   "recovery_bias_min": "Korrektur Erholungszeit",
   "puffer": "Reserve über Sollwert (puffer)",
   "theta": "Heizgrenze (theta)",
   "rh_threshold": "Feuchte-Schwelle",
   "rh_hysteresis": "Feuchte-Hysterese",
   "min_ah_advantage": "Mindest-Trocknungsvorteil",
   "max_reference_excess": "Draußen höchstens wärmer um",
   "min_rh_drop": "Mindest-Feuchteabfall durch Lüften",
   "min_cooling_advantage": "Mindest-Kühlvorteil",
   "cooling_margin": "Kühl-Abstand über Sollwert",
   "cooling_min_temp": "Kühlen erst ab Raumtemperatur",
   "energy_rh_per_k": "Energiespar-Zuschlag",
   "mould_rh": "Schimmelgrenze",
   "airing_target_below": "Lüftziel unter der Schwelle",
   "airing_time_factor": "Lüftdauer-Faktor",
   "airing_min_minutes": "Kürzeste Lüftdauer",
   "airing_max_minutes": "Längste Lüftdauer",
   "airing_pause_min": "Pause nach dem Lüften"
  },
  "limit_columns": {
   "min": "Minimum",
   "max": "Maximum",
   "step": "Max. Änderung je Prüfung"
  },
  "errors": {
   "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
   "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
   "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
   "name_required": "Bitte einen Namen eingeben.",
   "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
   "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
   "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
   "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
   "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
   "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
   "invalid_day_month": "Bitte ein gültiges Datum angeben (TT.MM., z. B. 01.10.); einen Tag wie den 31.02. gibt es nicht.",
   "invalid_auth": "Anthropic hat den API-Key abgelehnt. Prüfe ihn unter console.anthropic.com > API Keys und füge ihn ohne Leerzeichen ein. Ohne Key läuft die lokale Regelung weiter.",
   "cannot_connect": "Anthropic ist nicht erreichbar. Prüfe Internetverbindung, Proxy und Firewall. Der Key wurde nicht gespeichert.",
   "max_below_base": "Das maximale Intervall muss mindestens so groß sein wie das Prüfintervall (z. B. alle 4 h prüfen, höchstens alle 48 h).",
   "outdoor_required": "Bitte einen Außentemperatursensor oder eine Wetter-Entität wählen."
  },
  "area_errors": {
   "name_required": "Bitte einen Namen angeben.",
   "name_in_use": "Ein anderer Raum heißt schon so. Bitte einen eindeutigen Namen wählen (Export und Import finden Räume über den Namen).",
   "switch_in_use": "Dieser Schalter steuert bereits einen anderen Raum. Jeder Heizkreis gehört zu genau einem Raum: wähle einen anderen Schalter oder entferne ihn zuerst aus dem anderen Raum.",
   "min_above_max": "Der kleinste Sollwert muss kleiner sein als der größte. Bitte einen der beiden Werte ändern (beide in °C).",
   "target_out_of_range": "Der Start-Sollwert muss zwischen dem kleinsten und dem größten Sollwert liegen. Bitte ihn oder die Grenzen anpassen.",
   "reference_incomplete": "Referenztemperatur und Referenzfeuchte gehen nur zusammen: beide Sensoren wählen oder keinen.",
   "temperature_required": "Für Heizkreis und Lüftungsempfehlung braucht der Raum einen Temperatursensor."
  },
  "states": {
   "status": {
    "off": "Aus",
    "out_of_season": "Außerhalb Heizperiode",
    "no_heating_day": "Kein Heiztag",
    "idle": "Bereit",
    "heating": "Heizt",
    "window_open": "Fenster offen",
    "recovery": "Erholung nach Lüften",
    "frost_protection": "Frostschutz",
    "vacation": "Urlaub",
    "preheat": "Vorheizen zur Rückkehr",
    "emergency": "Notfallregel",
    "sensor_error": "Sensorfehler",
    "actuator_unavailable": "Aktor nicht erreichbar",
    "no_circuit": "Kein Heizkreis"
   },
   "ventilation": {
    "unknown": "Unbekannt",
    "close_window": "Fenster schließen",
    "ventilate_now": "Jetzt lüften",
    "ventilation_useful": "Lüften sinnvoll",
    "do_not_ventilate": "Nicht lüften",
    "blocked": "Lüften blockiert",
    "optimal": "Alles optimal",
    "vacation": "Urlaub"
   },
   "phase": {
    "ai_leads": "KI führt",
    "shared": "Gemeinsam",
    "rule_leads": "Regel führt"
   },
   "override": {
    "auto": "Automatik",
    "heat_today": "Heute heizen",
    "off_today": "Heute nicht heizen"
   }
  },
  "effort": {
   "auto": "Auto (Modell-Standard)",
   "low": "Niedrig",
   "medium": "Mittel",
   "high": "Hoch"
  },
  "heating_type": {
   "underfloor": "Fußbodenheizung",
   "radiator": "Heizkörper",
   "other": "Andere (z. B. Wandheizung)"
  }
 },
 "en": {
  "fields": {
   "outdoor_temperature": [
    "Outdoor temperature sensor",
    "Sensor for the outdoor temperature (e.g. a helper combining several sensors). Without it the current temperature of the weather entity is used. Only while nothing is set under Settings > House."
   ],
   "outdoor_humidity": [
    "Outdoor humidity sensor",
    "Optional. Needed for the ventilation recommendation; without it the humidity of the weather entity is used. Only while nothing is set under Settings > House."
   ],
   "weather": [
    "Weather entity",
    "Optional but recommended. Its forecast is used for the nightly heating day decision and the expected sun. Without an outdoor sensor its current temperature is the outdoor temperature. Only while nothing is set under Settings > House."
   ],
   "pv_power": [
    "PV power sensor",
    "Optional. PV power (W or kW) as an indicator for sunshine. The solar gain per room is learned from it."
   ],
   "pv_forecast": [
    "PV forecast sensor",
    "Optional, only together with the PV power sensor. Expected PV energy of the next hour (Wh or kWh, e.g. Forecast.Solar) or expected power in one hour (W or kW). Without it the sun is estimated from the hourly weather forecast and the sun position."
   ],
   "heat_meter": [
    "Heat meter",
    "Optional. Meter reading of the heat meter of the circuits controlled here (Wh, kWh, MWh, MJ or GJ, e.g. total_increasing). The AI then sees the measured heat; it is also shown in the panel. Seldom and coarse readings are fine."
   ],
   "season_start": [
    "Heating period start (DD.MM.)",
    "Outside the heating period all circuits stay off (frost protection only) and the AI is not asked."
   ],
   "season_end": [
    "Heating period end (DD.MM.)",
    "Last day of the heating period, may be in the next year (e.g. 31.03.)."
   ],
   "frost_temperature": [
    "Frost protection temperature",
    "Always applies, also outside the heating period and with a switched-off thermostat."
   ],
   "forecast_trust": [
    "Trust in the sun forecast",
    "Share of the expected PV power the control relies on when it holds back heating (100 % = full forecast, 0 % = only the current PV power counts)."
   ],
   "season_start_day": [
    "Heating period starts: day",
    "Heating is possible from this date (e.g. 1 October)."
   ],
   "season_start_month": [
    "Heating period starts: month",
    ""
   ],
   "season_end_day": [
    "Heating period ends: day",
    "Last day of the heating period (e.g. 31 March); the period may span the turn of the year."
   ],
   "season_end_month": [
    "Heating period ends: month",
    ""
   ],
   "vacation_entities": [
    "Vacation entities",
    "Any of these entities being 'on' means vacation (e.g. an input_boolean or a calendar). Only while nothing is set under Settings > Vacation. The switch “Vacation” of the house always counts."
   ],
   "vacation_temperature": [
    "Vacation temperature",
    "Target for all rooms during vacation (e.g. 17 °C)."
   ],
   "return_entity": [
    "Return date/time",
    "Optional input_datetime, timestamp sensor or datetime entity. Heating starts early enough (learned heat-up time) to reach the normal target on return. The return of the switch “Vacation” comes first; without it one set under Settings > Vacation."
   ],
   "preheat_reserve": [
    "Preheat reserve",
    "Additional time added to the calculated preheating time (e.g. 30 min)."
   ],
   "vacation_ventilation_pause": [
    "Ventilation advice rests",
    "On vacation the ventilation advice shows “Vacation”, “ventilation recommended” is off. Vacation minutes do not count for the AI ventilation check and stay out of the humidity profile."
   ],
   "emergency_enabled": [
    "Emergency rule",
    "On days without heating, a room may still heat if the temperature expected after the lead time is long and clearly below its target, without airing."
   ],
   "emergency_delta": [
    "Emergency: below target by",
    "How far below the target the temperature expected after the lead time has to be (at least the switch-on hysteresis)."
   ],
   "emergency_duration": [
    "Emergency: duration",
    "How long the expected temperature has to stay that low (e.g. 45 min)."
   ],
   "emergency_window_quiet": [
    "Emergency: no window change for",
    "Airing does not count: windows must not have changed for this time."
   ],
   "force_on_below": [
    "Always heat below target by",
    "Below target by this much the circuit heats regardless of every prediction and the expected sun."
   ],
   "ventilation_min_ah_advantage": [
    "Minimum drying advantage",
    "Absolute humidity is the water content of the air in g/m³, independent of temperature. Outside air must contain at least this much less water for 'ventilate now' (e.g. 0.8 g/m³)."
   ],
   "ventilation_max_reference_excess": [
    "Maximum outside warmer by",
    "Drying is not recommended if outside is warmer than inside by more than this."
   ],
   "ventilation_energy_rh_per_k": [
    "Energy saving surcharge",
    "Energy saving: within the heating period airing costs heat, the more the colder it is outside. The humidity must then exceed the threshold by this much per Kelvin outside is colder than the room (e.g. 0.25 %/K: at 21 °C inside and 1 °C outside 5 % more), at most up to 70 %, above which airing is always recommended against mould. 0 = off. Start value, the AI adjusts it per room."
   ],
   "ventilation_mould_rh": [
    "Mould limit",
    "From this relative humidity airing is always recommended, even in frost and right after an airing; the energy saving surcharge never goes beyond it. Lower it for rooms with cold exterior walls. Start value, the AI adjusts it per room."
   ],
   "ventilation_airing_target_below": [
    "Airing target below threshold",
    "The suggested airing time aims at this far below the humidity threshold. Start value for the AI."
   ],
   "ventilation_airing_time_factor": [
    "Airing time factor",
    "Scales the suggested airing time. Once two airings are evaluated it is computed from the learned air exchange of the room and the temperature difference, before that from the outside temperature (5 min in frost up to 20 min when warm). Start value for the AI."
   ],
   "ventilation_airing_min_minutes": [
    "Shortest airing time",
    "Start value for the AI."
   ],
   "ventilation_airing_max_minutes": [
    "Longest airing time",
    "Start value for the AI."
   ],
   "ventilation_airing_pause": [
    "Pause after airing",
    "After an airing moisture comes back from walls and furniture. Drying is recommended again only after this pause (below the mould limit), which saves heat and nagging. Start value for the AI."
   ],
   "ventilation_min_cooling_advantage": [
    "Minimum cooling advantage",
    "'Ventilation useful' if inside is warmer than outside by at least this (not while heating)."
   ],
   "ventilation_cooling_margin": [
    "Minimum distance above target for cooling",
    "Within the heating period 'ventilation useful' (cooling) is only recommended if the room is at least this much warmer than its target. Not used outside the heating period. Rooms without a heating circuit use their initial target."
   ],
   "ventilation_cooling_min_temp": [
    "Cool only from room temperature",
    "'Ventilation useful' (cooling) only from this room temperature on, all year. 0 = off. In addition cooling is never recommended if the outside air would raise the relative humidity of the room above its humidity threshold."
   ],
   "night_start_hour": [
    "Night starts at",
    "Used when the reference is another room: cooling advantage only counts at night."
   ],
   "night_end_hour": [
    "Night ends at",
    "End of the night (time, e.g. 08:00)."
   ],
   "ventilation_ai_enabled": [
    "AI adjusts ventilation per room",
    "All year the AI reviews the ventilation thresholds of every room with a humidity sensor: it learns what is usual in each room, how low the humidity can get and what airing really achieves. Shares the monthly AI budget."
   ],
   "ventilation_check_interval": [
    "Ventilation check base interval",
    "First interval; it doubles with every check that changed nothing relevant and starts over when a room stays humid or a value changes."
   ],
   "ventilation_check_max_interval": [
    "Ventilation check maximum interval",
    "The interval never grows beyond this."
   ],
   "model": [
    "Claude model",
    "Model for all AI calls. Prices below are suggestions for the selected model and can be changed."
   ],
   "effort": [
    "Thinking effort",
    "Claude thinks before it answers. More effort can give better answers but uses more tokens, which are billed as output. 'auto' leaves it to the model."
   ],
   "nightly_time": [
    "Time of the nightly run",
    "Daily decision whether heating is needed today (also the start of the evaluated day)."
   ],
   "check_interval": [
    "Check interval",
    "Base interval of the periodic AI check on heating days (e.g. 4 h). It doubles after every check without relevant change."
   ],
   "check_max_interval": [
    "Maximum check interval",
    "Upper limit for the doubled interval (e.g. 48 h)."
   ],
   "monthly_budget": [
    "Monthly budget",
    "In US dollars, as Anthropic bills. No AI calls once the costs of the month reach this value (until the month changes). A check usually costs a few cents, so 5 USD allow about 100 to 200 calls."
   ],
   "price_input": [
    "Price input tokens",
    "US dollars per million tokens, as Anthropic bills."
   ],
   "price_output": [
    "Price output tokens",
    "US dollars per million tokens, as Anthropic bills (thinking counts as output)."
   ],
   "price_cache_write": [
    "Price cache write",
    "US dollars per million tokens, as Anthropic bills."
   ],
   "price_cache_read": [
    "Price cache read",
    "US dollars per million tokens, as Anthropic bills."
   ],
   "max_output_tokens": [
    "Maximum output tokens",
    "Upper limit per answer, thinking included (too low cuts answers off, they are paid but discarded). Also the upper bound of the cost estimate before a call."
   ],
   "theta": [
    "Heating threshold theta (learned)",
    "Current threshold of the heating day rule: if the forecast maximum is below it, heating is needed. A change replaces the learned value; learning continues from there."
   ],
   "too_cold_margin": [
    "Too cold below target by",
    "Evaluation: a room counts as too cold below target minus this (airing excluded)."
   ],
   "too_cold_minutes": [
    "Too cold minutes for heating need",
    "Evaluation: this many minutes too cold mean heating was needed."
   ],
   "theta_step_up": [
    "Heating threshold: step up",
    "After error A, i.e. it got too cold on a day without heating (e.g. 1.0 K)."
   ],
   "theta_step_down": [
    "Heating threshold: step down",
    "After error B, i.e. heating ran although it was not needed (e.g. 1.0 K)."
   ],
   "puffer_step_up": [
    "Margin above target: step up",
    "After error A for the cold room."
   ],
   "puffer_step_down": [
    "Margin above target: step down",
    "After error B."
   ],
   "phase_shared_min_days": [
    "Days until shared decision",
    "Who decides the heating day: first the AI leads, then AI and rule decide together, finally the rule leads. 'AI leads' -> 'shared' after this many evaluated days (e.g. 14)."
   ],
   "phase_shared_min_agreement": [
    "Agreement for shared decision",
    "Minimum agreement of rule and AI."
   ],
   "phase_rule_min_days": [
    "Days until rule leads",
    "Phase 'shared' -> 'rule leads' after this many days in phase 'shared'."
   ],
   "phase_rule_min_agreement": [
    "Agreement for rule leads",
    "Minimum agreement of rule and AI."
   ],
   "phase_max_rule_errors": [
    "Allowed rule errors",
    "Maximum rule errors within the period for a phase change."
   ],
   "phase_fallback_errors_7d": [
    "Rule errors in 7 days for fallback",
    "This many rule errors within 7 days move back one phase."
   ],
   "phase_ai_check_every_days": [
    "AI control check every",
    "When the rule leads and is sure, the AI is still asked every this many days."
   ],
   "api_key": [
    "Anthropic API key",
    "Optional. Without a key the local control runs alone. The key is only stored in Home Assistant and never logged."
   ],
   "name": [
    "Name",
    "Name of the room, also used for the device and its entities."
   ],
   "area": [
    "Area",
    "Optional. The device of the room is placed in this area; its floor counts for cross ventilation."
   ],
   "temperature_sensor": [
    "Temperature sensor",
    "Room temperature. Without a sensor the room has no heating and no ventilation advice (e.g. a room only for covers)."
   ],
   "humidity_sensor": [
    "Humidity sensor",
    "Relative humidity, needed for the ventilation recommendation."
   ],
   "heater_switch": [
    "Heating circuit switch",
    "Switch of the actuator (e.g. a relay). Leave empty for a room with ventilation recommendation only."
   ],
   "default_target": [
    "Initial target temperature",
    "Target until you change it on the thermostat card."
   ],
   "min_target": [
    "Minimum target",
    "Lowest value of the thermostat card."
   ],
   "max_target": [
    "Maximum target",
    "Highest value of the thermostat card."
   ],
   "min_on_time": [
    "Minimum on time",
    "Always respected (protects the actuator). Not learned."
   ],
   "min_off_time": [
    "Minimum off time",
    "Always respected. Not learned."
   ],
   "heating_type": [
    "Heating type",
    "How the circuit heats. A floor stores heat for hours, radiators react within minutes; the AI judges the learned values with this in mind."
   ],
   "window_delay": [
    "Window delay (start value)",
    "Window open this long pauses heating. The AI may adjust it."
   ],
   "recovery_time": [
    "Recovery time after airing (start value)",
    "After closing, heating waits this long because floor and walls often reheat the room. Learned afterwards."
   ],
   "dead_time": [
    "Dead time until the room warms (start value)",
    "Time from switching on until the room gets warmer; underfloor heating often 30-90 min, radiators 5-20 min. Learned afterwards."
   ],
   "puffer": [
    "Margin above target (start value)",
    "Heating day rule: how far above the target a room must be at the nightly run to manage a day without heating (e.g. 0.7 K). Learned afterwards."
   ],
   "ventilation_rh_threshold": [
    "Humidity threshold",
    "Start value of the relative humidity from which ventilating is recommended (e.g. 65 % for bathrooms); the AI ventilation check adjusts it to the room."
   ],
   "reference_temperature": [
    "Reference temperature instead of outdoor",
    "Optional, for rooms aired via another room."
   ],
   "reference_humidity": [
    "Reference humidity instead of outdoor",
    "Required together with the reference temperature."
   ],
   "ventilation_block_entity": [
    "Ventilation block entity",
    "Optional. While it blocks, no ventilation is recommended: a cover while closed (e.g. sun protection down), a climate entity or water heater while not off (e.g. air conditioner running), a switch, binary sensor, fan or similar while on."
   ],
   "draft_group_1": [
    "Combination 1",
    "e.g. kids' room + bathroom; a second combination e.g. kids' room + bedroom."
   ],
   "draft_group_2": [
    "Combination 2",
    ""
   ],
   "draft_group_3": [
    "Combination 3",
    ""
   ],
   "draft_group_4": [
    "Combination 4",
    ""
   ],
   "cooling_entity": [
    "Air conditioner",
    "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner. Applies to every window of the room without its own air conditioner."
   ]
  },
  "learned": {
   "window_delay": [
    "Window delay",
    "Window open this long pauses heating. The AI may adjust it."
   ],
   "recovery_time": [
    "Recovery time after airing",
    "Learned wait after the windows are closed."
   ],
   "dead_time": [
    "Dead time until the room warms",
    "Learned time until the room warms up after switching on."
   ],
   "puffer": [
    "Margin above target",
    "Heating day rule: needed margin above the target at the nightly run (learned)."
   ]
  },
  "sections": {
   "sensors": [
    "Sensors",
    ""
   ],
   "heating": [
    "Heating circuit",
    ""
   ],
   "start_values": [
    "Start values (learned later)",
    "Only when the room is created. Afterwards the learned values are edited."
   ],
   "ventilation": [
    "Ventilation",
    ""
   ],
   "draft": [
    "Draft from other rooms",
    "Windows of other rooms whose opening together also cools this room (cross ventilation). Per combination choose the windows that must be open together. As soon as every window of one combination is open, the room behaves as with its own window open: heating pauses after the window delay and waits the recovery time. A combination with a single window triggers on its own."
   ],
   "sun_protection": [
    "Sun protection",
    "Defaults for the covers of the windows of this room. Room temperature and target come from the temperature sensor and the thermostat of the room unless a window has its own room temperature."
   ],
   "learned_values": [
    "Learned values",
    "Values the control currently uses. A change replaces the learned or AI-adjusted value; learning continues from there."
   ]
  },
  "limits": {
   "hysteresis_on": "Switch-on hysteresis",
   "hysteresis_off": "Switch-off hysteresis",
   "overshoot_factor": "Overshoot factor",
   "lead_factor": "Lead time factor",
   "sun_factor": "Sun factor",
   "window_delay_min": "Window delay",
   "recovery_bias_min": "Recovery time correction",
   "puffer": "Margin above target (puffer)",
   "theta": "Heating threshold (theta)",
   "rh_threshold": "Humidity threshold",
   "rh_hysteresis": "Humidity hysteresis",
   "min_ah_advantage": "Minimum drying advantage",
   "max_reference_excess": "Maximum outside warmer by",
   "min_rh_drop": "Minimum humidity drop by airing",
   "min_cooling_advantage": "Minimum cooling advantage",
   "cooling_margin": "Cooling distance above target",
   "cooling_min_temp": "Cool only from room temperature",
   "energy_rh_per_k": "Energy saving surcharge",
   "mould_rh": "Mould limit",
   "airing_target_below": "Airing target below threshold",
   "airing_time_factor": "Airing time factor",
   "airing_min_minutes": "Shortest airing time",
   "airing_max_minutes": "Longest airing time",
   "airing_pause_min": "Pause after airing"
  },
  "limit_columns": {
   "min": "Minimum",
   "max": "Maximum",
   "step": "Max. change per check"
  },
  "errors": {
   "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
   "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
   "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
   "name_required": "Please enter a name.",
   "azimuth_equal": "Azimuth from and to must differ.",
   "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
   "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
   "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
   "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
   "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
   "invalid_day_month": "Please enter a valid date (DD.MM., e.g. 01.10.); a day like 31.02. does not exist.",
   "invalid_auth": "Anthropic rejected the API key. Check it at console.anthropic.com under API keys and paste it without spaces. Without a key the local control keeps running.",
   "cannot_connect": "Anthropic cannot be reached. Check the internet connection, proxy and firewall. The key was not saved.",
   "max_below_base": "The maximum interval must be at least the check interval (e.g. check every 4 h, at most every 48 h).",
   "outdoor_required": "Choose an outdoor temperature sensor or a weather entity."
  },
  "area_errors": {
   "name_required": "Please enter a name.",
   "name_in_use": "Another room already has this name. Please choose a unique name (export and import find rooms by name).",
   "switch_in_use": "This switch already controls another room. Each circuit can belong to one room only: choose another switch, or remove it from the other room first.",
   "min_above_max": "The smallest target must be below the largest target. Please change one of the two values (both in °C).",
   "target_out_of_range": "The start target must lie between the smallest and the largest target. Please adjust it or the limits.",
   "reference_incomplete": "Reference temperature and reference humidity only work together: choose both sensors or neither.",
   "temperature_required": "A heating circuit and the ventilation advice need a temperature sensor of the room."
  },
  "states": {
   "status": {
    "off": "Off",
    "out_of_season": "Outside heating period",
    "no_heating_day": "No heating day",
    "idle": "Ready",
    "heating": "Heating",
    "window_open": "Window open",
    "recovery": "Recovery after airing",
    "frost_protection": "Frost protection",
    "vacation": "Vacation",
    "preheat": "Preheating for return",
    "emergency": "Emergency rule",
    "sensor_error": "Sensor error",
    "actuator_unavailable": "Actuator unavailable",
    "no_circuit": "No heating circuit"
   },
   "ventilation": {
    "unknown": "Unknown",
    "close_window": "Close window",
    "ventilate_now": "Ventilate now",
    "ventilation_useful": "Ventilation useful",
    "do_not_ventilate": "Do not ventilate",
    "blocked": "Ventilation blocked",
    "optimal": "All fine",
    "vacation": "Vacation"
   },
   "phase": {
    "ai_leads": "AI leads",
    "shared": "Shared",
    "rule_leads": "Rule leads"
   },
   "override": {
    "auto": "Automatic",
    "heat_today": "Heat today",
    "off_today": "No heating today"
   }
  },
  "effort": {
   "auto": "Auto (model default)",
   "low": "Low",
   "medium": "Medium",
   "high": "High"
  },
  "heating_type": {
   "underfloor": "Underfloor heating",
   "radiator": "Radiators",
   "other": "Other (e.g. wall heating)"
  }
 }
};
export const SHUTTER = {
 "LABELS": {
  "de": {
   "auto_up": [
    "Auto-Hoch",
    "Wieder öffnen, wenn die Sonne den Bereich verlässt (nicht im Abendmodus)."
   ],
   "azimuth_from": [
    "Azimut von",
    "Sonnenrichtung, ab der die Sonne auf die Fenster scheint (90 ° = Ost, 180 ° = Süd, 270 ° = West). Die Grenzen selbst zählen nicht."
   ],
   "azimuth_to": [
    "Azimut bis",
    "Erreicht die Sonne diese Richtung, öffnen geschützte Rollos wieder (Auto-Hoch)."
   ],
   "catch_up_after": [
    "Abendlauf nachholen ab",
    "Nach dem Neustart-Schutz wird der Abendlauf für noch nicht geschlossene Fenster nachgeholt, aber erst ab dieser Uhrzeit."
   ],
   "close_trigger_active_states": [
    "Aktiv-Zustände",
    "Zustände, in denen ein Schließ-Auslöser als aktiv gilt (z. B. on, playing beim Fernseher)."
   ],
   "close_trigger_entities": [
    "Schließ-Auslöser",
    "Wird eine dieser Entitäten aktiv, schließt das Rollo einmal pro Aktiv-Zyklus, nur bei geschlossenem Fenster (sonst sobald es zu ist). Der Zyklus endet, wenn alle inaktiv sind."
   ],
   "close_trigger_max_lock": [
    "Zyklus höchstens",
    "Spätestens nach dieser Zeit beginnt ein neuer Zyklus, auch wenn die Auslöser die ganze Zeit aktiv waren."
   ],
   "close_trigger_min_position": [
    "Nur wenn weiter offen als",
    "Schließt nur, wenn das Rollo weiter offen steht als diese Position."
   ],
   "close_trigger_off_delay": [
    "Inaktiv nach",
    "So lange müssen alle Auslöser inaktiv sein, bis der Zyklus endet und ein neues Einschalten wieder schließt."
   ],
   "close_trigger_on_delay": [
    "Aktiv nach",
    "So lange muss ein Auslöser aktiv sein, bevor das Rollo schließt (kurzes Einschalten zählt nicht)."
   ],
   "closed_position": [
    "Gilt als geschlossen bis",
    "Für Lüften und Urlaub morgens."
   ],
   "command_interval": [
    "Abstand zwischen Fahrbefehlen",
    "Mehrere Rollos fahren nacheinander mit diesem Abstand (gegen Funkkollisionen). 0 = alle gleichzeitig."
   ],
   "cooling_entity": [
    "Klimaanlage",
    "Optional: Solange diese Klimaanlage kühlt, gilt der Raum als zu warm. Der Sonnenschutz entlastet dann die Klimaanlage."
   ],
   "cover": [
    "Rollo",
    "Optional. 100 % = offen, 0 % = zu. Ohne Rollo dient das Fenster nur der Heizung."
   ],
   "day_change_time": [
    "Tageswechsel",
    "Prüfung der Vorhersage und Zurücksetzen der Tagesmarker für Sonnenschutz und Benachrichtigungen."
   ],
   "evening_close": [
    "Abendlauf",
    "Zu Beginn des Abendmodus schließen, einmal pro Abend und nur bei geschlossenem Fenster."
   ],
   "evening_custom": [
    "Eigene Abendzeiten",
    "Die folgenden Werte statt der globalen verwenden."
   ],
   "evening_earliest": [
    "Abendmodus frühestens",
    "Vor dieser Uhrzeit beginnt der Abendmodus nie."
   ],
   "evening_elevation": [
    "Sonnenhöhe",
    "Der Abendmodus beginnt, wenn die Sonne unter diese Höhe sinkt (z. B. -4 °)."
   ],
   "evening_latest": [
    "Abendmodus spätestens",
    "Zeit-Fallback: spätestens um diese Uhrzeit beginnt der Abendmodus."
   ],
   "evening_position": [
    "Abendposition",
    "Ziel des Abendlaufs und des Nachziehens. 0 % = zu; z. B. 20 % lässt in warmen Nächten einen Spalt."
   ],
   "follow_up_close": [
    "Nachziehen",
    "Wird das Fenster am Abend geschlossen, fährt das Rollo zu (auch bei Übersteuerung)."
   ],
   "follow_up_earliest": [
    "Nachziehen ab",
    "Ein am Abend geschlossenes Fenster fährt das Rollo erst ab dieser Uhrzeit zu."
   ],
   "forecast_type": [
    "Vorhersage-Art",
    "Automatisch nimmt die erste Art, die die Wetter-Entität kann (täglich, zweimal täglich, stündlich). Aus stündlichen Werten werden Tageshöchst- und Nachttiefstwert berechnet."
   ],
   "frost_position": [
    "Tiefste Position bei Frost",
    "Leer = aus. Bei Frost stoppt das Schließen hier, damit das Rollo nicht anfriert, z. B. 5 %."
   ],
   "frost_threshold": [
    "Frost ab (höchstens)",
    "Außentemperatur. Nur Fenster mit einer Frostposition machen mit."
   ],
   "group": [
    "Gruppe",
    "Himmelsrichtung. Ohne Gruppe hat das Fenster keinen Sonnenschutz."
   ],
   "heating_entity": [
    "Heizbedarf",
    "Optional, z. B. ein input_boolean „Heizperiode“ oder der Heiztag einer Heizungssteuerung. Solange sie an ist, ist Sonnenwärme erwünscht: Sonnenschutz nur, wenn der Raum eines Fensters trotzdem zu warm ist. Fenster ohne Raumtemperatur werden dann nicht abgesenkt."
   ],
   "language": [
    "Sprache der Meldungen",
    "Logbuch, letzter Grund und Push-Nachrichten. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "lockout_protection": [
    "Aussperrschutz (Tür)",
    "Solange der Kontakt offen meldet, fährt nichts unter die Lüftungsposition, auch nicht mit Fenster-Ausnahme oder Wetterschutz."
   ],
   "lux_sensors": [
    "Helligkeitssensoren",
    "Lux-Sensoren an den Fenstern. Jeder Sensor der Gruppe muss die Schwelle des Fensters erreichen."
   ],
   "lux_threshold": [
    "Helligkeitsschwelle",
    "Jeder Helligkeitssensor der Gruppe muss diesen Wert erreichen."
   ],
   "manual_at_sun_position": [
    "Fahrt auf Sonnenschutz-Position zählt",
    "Ein bei Sonne von irgendwem auf die Sonnenschutz-Position (bis zur Toleranz) gefahrenes Rollo gilt wie automatischer Sonnenschutz und öffnet wieder mit Auto-Hoch."
   ],
   "manual_detection_window": [
    "Erkennungszeitraum",
    "Die manuelle Bewegung darf höchstens so lange her sein."
   ],
   "manual_follow_up": [
    "Nachlauf der Sonnenbedingung",
    "Für diese Erkennung zählt die Sonnenbedingung (ohne Temperatur) noch so lange nach ihrem Ende."
   ],
   "manual_max_position": [
    "Manueller Sonnenschutz bis",
    "Ein bei Sonne von Hand höchstens auf diese Position gefahrenes Rollo gilt heute als Sonnenschutz (keine Automatikfahrt)."
   ],
   "morning_earliest": [
    "Frühestens",
    "Vorher öffnet das Rollo nie, auch wenn der Auslöser früher kommt."
   ],
   "morning_enabled": [
    "Morgenöffnung",
    "Das Rollo morgens automatisch öffnen."
   ],
   "morning_latest": [
    "Spätestens",
    "Hat bis dahin nichts ausgelöst, öffnet das Rollo zu dieser Zeit."
   ],
   "morning_lux_hold": [
    "Haltezeit",
    "So lange muss es hell genug sein, bevor das Rollo öffnet."
   ],
   "morning_lux_threshold": [
    "Helligkeit",
    "Jeder Helligkeitssensor der Gruppe muss diesen Wert erreichen."
   ],
   "morning_mode": [
    "Modus",
    "Wodurch die Morgenöffnung ausgelöst wird; die Einstellungen dazu folgen im nächsten Schritt."
   ],
   "morning_position": [
    "Zielposition",
    "100 = offen, weniger = Teilöffnung."
   ],
   "morning_sun_elevation": [
    "Sonnenhöhe",
    "Nur für Sonnenhöhe: öffnet, wenn die aufgehende Sonne diese Höhe erreicht."
   ],
   "morning_sun_event": [
    "Ereignis",
    "Sonnenaufgang oder das Erreichen einer Sonnenhöhe."
   ],
   "morning_sun_offset": [
    "Versatz",
    "Minuten vor (negativ) oder nach dem Ereignis."
   ],
   "morning_sun_position": [
    "Direkt auf Sonnenschutz, falls nötig",
    "Gilt die Sonnenbedingung, nur bis zur Sonnenschutz-Position öffnen."
   ],
   "morning_time_weekend": [
    "Wochenende und Feiertage",
    "Uhrzeit am Wochenende und an Feiertagen (Feiertage nur mit Werktag-Sensor)."
   ],
   "morning_time_workday": [
    "Werktags",
    "Uhrzeit an Werktagen (Werktag-Sensor oder Wochenendtage)."
   ],
   "morning_trigger_entity": [
    "Auslöser-Entität",
    "Ein Zeitstempel (z. B. nächster Wecker des Handys) öffnet zu dieser Zeit plus Versatz. Jede andere Entität öffnet, wenn sie angeht (Bewegung, Schalter)."
   ],
   "morning_trigger_offset": [
    "Versatz",
    "Nur für Zeitstempel."
   ],
   "name": [
    "Name",
    "Wird auch für das Gerät und seine Entitäten verwendet."
   ],
   "night_end": [
    "Ende der Nacht",
    "Abendmodus und Abend-Marker enden um diese Uhrzeit (oder bei Sonnenaufgang, falls früher)."
   ],
   "night_threshold": [
    "Später Sommertag nur bei Nacht ab",
    "Wird der Tag erst durch die Außentemperatur zum Sommertag, zählt das nur, wenn der Vorhersage-Tiefstwert der kommenden Nacht mindestens so hoch ist. Kühlt es nachts ab (Frühling, Herbst), bleibt die Wärme im Haus. Ohne Tiefstwert in der Vorhersage gilt der Sommertag wie bisher."
   ],
   "notify_open_window": [
    "Bei offenem Fenster benachrichtigen",
    "Einmal am Tag, wenn ein offenes Fenster den Sonnenschutz verhindert hat."
   ],
   "notify_services": [
    "Benachrichtigungsdienste",
    "Erhalten eine Nachricht, wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy). Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "open_block_entity": [
    "Öffnungssperre",
    "Kein automatisches Öffnen (Auto-Hoch, Lüften, Urlaub morgens, Morgenöffnung), außer die Entität hat einen der Freigabe-Zustände (z. B. ein Fernseher)."
   ],
   "open_block_free_states": [
    "Freigabe-Zustände",
    "Zustände der Öffnungssperre, in denen trotzdem geöffnet wird (z. B. off, standby)."
   ],
   "outdoor_temperature": [
    "Außentemperatur-Sensor",
    "Für den Sommertag und die Temperaturbedingung jedes Fensters. Ohne Sensor wird die aktuelle Temperatur der Wetter-Entität verwendet (mindestens eins von beiden). Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "override_duration": [
    "Dauer",
    "Nach einer manuellen Bewegung pausiert die Automatik so lange für das Fenster. Jede weitere Bewegung startet sie neu. 0 = bis Sonnenaufgang."
   ],
   "override_ignore_evening": [
    "Abend- und Urlaubsfahrten trotz Übersteuerung",
    "z. B. Schlafräume, die abends immer schließen sollen."
   ],
   "override_sunrise_reset": [
    "Auch bei Sonnenaufgang beenden",
    "Die Übersteuerung endet zusätzlich beim nächsten Sonnenaufgang, auch wenn die Dauer noch läuft."
   ],
   "override_trigger": [
    "Übersteuerung beginnt",
    "Nur bei echter Fahrt: Ein Befehl an ein Rollo, das schon in der Zielposition steht (z. B. „alle Rollos auf“, während es offen ist), startet keine Übersteuerung. Jeder Befehl: auch ohne Fahrt, wie bisher."
   ],
   "position_tolerance": [
    "Toleranz für Auto-Hoch",
    "Auto-Hoch öffnet nur Rollos, die auf der Sonnenschutz-Position bis so viel darüber stehen. Von Hand anders gestellte Rollos bleiben."
   ],
   "protection_keep_closed": [
    "Weiter geschlossen gilt als geschützt",
    "Ein Rollo, das schon weiter zu ist als seine Position bei Wind oder Regen, wird nicht dorthin hochgefahren (z. B. zu auf 0 % bei Wind-Position 20 %). Nicht bei 100 %: Raffstores einfahren läuft immer."
   ],
   "protection_release": [
    "Freigabe nach",
    "Ein Schutz endet erst, wenn der Wert so lange wieder im sicheren Bereich war. Ein nicht verfügbarer Sensor beendet nie einen Schutz."
   ],
   "pv_sensors": [
    "PV-Leistungssensoren",
    "Leistung einer PV-Anlage oder eines Moduls in diese Richtung (W)."
   ],
   "pv_threshold": [
    "PV-Schwelle",
    "Jeder PV-Sensor der Gruppe muss diesen Wert erreichen."
   ],
   "radiation_sensors": [
    "Strahlungssensoren",
    "Sonnenstrahlung in W/m², z. B. von einem Wetterdienst oder einer Wetterstation."
   ],
   "radiation_threshold": [
    "Strahlungsschwelle",
    "Jeder Strahlungssensor der Gruppe muss diesen Wert erreichen."
   ],
   "rain_entity": [
    "Regensensor",
    "Ein Regensensor, der einschaltet, oder eine Regenmenge (z. B. mm/h)."
   ],
   "rain_position": [
    "Position bei Regen",
    "Leer = nicht betroffen. Z. B. 0 % für ein Dachfenster."
   ],
   "rain_threshold": [
    "Regenschutz über",
    "Nur bei einem Zahlenwert: Regen zählt über diesem Wert."
   ],
   "room": [
    "Raum",
    "Optional. Die Heizung des Raums nutzt die Kontakte des Fensters; das Rollo nimmt Raumtemperatur und Klimaanlage des Raums."
   ],
   "room_entity": [
    "Raumtemperatur",
    "Optional: Thermostat (climate) oder Temperatursensor des Raums. Dann wird nur abgesenkt, wenn der Raum zu warm ist. Ohne Wert gilt die Bedingung als erfüllt (außer am Heiztag)."
   ],
   "room_margin": [
    "Zu warm ab Sollwert plus",
    "Bei einem Thermostat: zu warm ab dessen Sollwert plus diesem Abstand."
   ],
   "room_threshold": [
    "Zu warm ab",
    "Bei einem Temperatursensor (oder einem Thermostat ohne Sollwert): zu warm ab dieser Temperatur."
   ],
   "size": [
    "Größe",
    "Wie schnell Lüften die Luft austauscht: Die vorgeschlagene Lüftdauer richtet sich danach, und zum Lüften wird die größte Öffnung vorgeschlagen. Die Größe gilt für jeden Kontakt des Fensters."
   ],
   "startup_delay": [
    "Neustart-Schutz",
    "Nach dem Start von Home Assistant so lange keine Fahrt (Sensoren und Rollos melden sich noch an)."
   ],
   "summer_threshold": [
    "Sommertag ab Vorhersage-Höchsttemperatur",
    "Ohne Sommertag gibt es keinen Sonnenschutz. Tagsüber beginnt der Sommertag auch, wenn die Außentemperatur über diesen Wert steigt (siehe Nacht)."
   ],
   "sun_hold": [
    "Haltezeit Sonne",
    "So lange müssen Sommertag, Temperatur, Raum und alle Sonnensensoren erfüllt sein. Die Bedingung endet sofort."
   ],
   "sun_position": [
    "Sonnenschutz-Position",
    "Einmal am Tag auf diese Position. Ein schon weiter geschlossenes Rollo bleibt, wie es ist."
   ],
   "temperature_hold": [
    "Haltezeit Temperatur",
    "So lange muss die Außentemperatur darüber liegen. Darunter endet die Bedingung sofort."
   ],
   "temperature_threshold": [
    "Außentemperatur mindestens",
    "Sonnenschutz erst ab dieser Außentemperatur."
   ],
   "tilt_sensors": [
    "Kipp-Kontakte",
    "'on' = gekippt. Solange das Fenster nur gekippt ist, schließen die Rollos höchstens bis zur Lüftungsposition."
   ],
   "use_heating_day": [
    "Heiztag der Heizung",
    "Ohne eigenen Heizbedarf: der Heiztag des Heizungsmoduls, aber nur in der Heizperiode. Gilt nur, solange das Heizungsmodul eingeschaltet ist."
   ],
   "vacation": [
    "Urlaubssimulation",
    "An der zufälligen Öffnung und Schließung im Urlaub teilnehmen."
   ],
   "vacation_entities": [
    "Urlaubs-Entitäten",
    "Urlaub ist aktiv, solange eine davon an ist (z. B. ein input_boolean „Urlaub“ oder ein Kalender). Gilt nur, solange unter Einstellungen > Urlaub nichts eingetragen ist. Der Schalter „Urlaub“ des Hauses gilt immer."
   ],
   "vacation_evening_start": [
    "Urlaub abends ab",
    "Beginnt den Abend für die Fenster der Simulation und schließt sie zu zufälligen Zeiten. Der normale Abendlauf ruht im Urlaub."
   ],
   "vacation_evening_window": [
    "Zufallszeitraum abends",
    "Jedes Fenster schließt zu einer zufälligen Zeit in diesem Zeitraum."
   ],
   "vacation_heat_protection": [
    "Hitzeschutz im Urlaub",
    "Der Sonnenschutz senkt im Urlaub ab, ohne auf Raumtemperatur, Klimaanlage oder Heizbedarf zu warten. Sommertag, Außentemperatur, Sonnensensoren, Haltezeiten und der Sonnenschalter des Fensters gelten weiter."
   ],
   "vacation_morning_start": [
    "Urlaub morgens ab",
    "Geschlossene Rollos der Fenster in der Simulation öffnen danach zu einer zufälligen Zeit."
   ],
   "vacation_morning_window": [
    "Zufallszeitraum morgens",
    "Jedes Fenster öffnet zu einer zufälligen Zeit in diesem Zeitraum."
   ],
   "vacation_position_max": [
    "Öffnungsposition bis",
    "Zufällige Position zwischen beiden Werten."
   ],
   "vacation_position_min": [
    "Öffnungsposition von",
    "Zufällige Position zwischen beiden Werten."
   ],
   "ventilation": [
    "Lüften beim Öffnen des Fensters",
    "Beim Öffnen des Fensters fährt ein geschlossenes Rollo auf die Lüftungsposition (abends nach der kurzen, tagsüber nach der langen Verzögerung)."
   ],
   "ventilation_delay_day": [
    "Verzögerung tagsüber",
    "Das Fenster muss danach noch offen sein."
   ],
   "ventilation_delay_evening": [
    "Verzögerung abends",
    "Im Abendmodus fährt das Rollo nach dieser kurzen Zeit auf die Lüftungsposition."
   ],
   "ventilation_position": [
    "Lüftungsposition",
    "Position beim Lüften (100 % = offen)."
   ],
   "verify_after": [
    "Position prüfen nach",
    "Hat ein Rollo sein Ziel bis dahin nicht erreicht, wird der Befehl einmal wiederholt, danach kommt eine Meldung. 0 = aus."
   ],
   "weather": [
    "Wetter-Entität",
    "Ihre Tagesvorhersage entscheidet beim Tageswechsel, ob heute ein Sommertag ist. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "weather_protection": [
    "Wetterschutz für dieses Fenster",
    "Aus = Wind, Regen und Frost fahren oder begrenzen dieses Rollo nie, egal was unten eingetragen ist. Für jedes Fenster einschalten, das mitmachen soll. Mit ausgeschalteter Automatik (global oder für dieses Fenster) gibt es auch keinen Wetterschutz."
   ],
   "weekend_days": [
    "Wochenendtage",
    "Nur ohne Werktag-Sensor: an diesen Tagen gilt die Wochenend-Uhrzeit der Morgenöffnung. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ],
   "wind_entity": [
    "Windsensor",
    "Windgeschwindigkeit oder Böen, z. B. von einer Wetterstation."
   ],
   "wind_position": [
    "Position bei Wind",
    "Leer = nicht betroffen. Z. B. 100 % fährt Raffstores hoch. Nur mit eingeschaltetem Wetterschutz des Fensters."
   ],
   "wind_threshold": [
    "Windschutz ab",
    "In der Einheit des Windsensors (z. B. km/h oder m/s)."
   ],
   "window_closed_delay": [
    "Fenster gilt als geschlossen nach",
    "Ein Fensterkontakt muss so lange „zu“ melden, bevor Nachziehen, Sonnenschutz oder Schließ-Auslöser greifen (gegen Prellen beim Schließen)."
   ],
   "window_exception_entity": [
    "Fenster-Ausnahme",
    "Solange diese Entität verfügbar ist, verhindert ein offenes Fenster keine Schließfahrten und es gibt keine Nachricht (z. B. Klimaanlage mit Schlauch durch die Balkontür). Gilt nicht für den Urlaubsabend."
   ],
   "window_sensors": [
    "Fensterkontakte",
    "'on' = offen. Fenstergriffe mit den Zuständen open, tilted und closed gehen auch. Unbekannt oder nicht verfügbar zählt als offen. Ein Kontakt gehört zu genau einem Fenster."
   ],
   "window_wind_threshold": [
    "Eigene Windschwelle",
    "Leer = Windschutz ab der Schwelle der Grundeinstellungen. Sonst schützt dieses Fenster schon oder erst ab diesem Wert (Einheit des Windsensors)."
   ],
   "workday_entity": [
    "Werktag-Sensor",
    "Optional, für die Morgenöffnung nach Uhrzeit (z. B. Workday-Integration, berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage. Gilt nur, solange unter Einstellungen > Haus nichts eingetragen ist."
   ]
  },
  "en": {
   "auto_up": [
    "Auto up",
    "Open again when the sun leaves the sector (not in the evening)."
   ],
   "azimuth_from": [
    "Azimuth from",
    "Sun direction from which the sun shines on the windows (90 ° = east, 180 ° = south, 270 ° = west). The bounds themselves do not count."
   ],
   "azimuth_to": [
    "Azimuth to",
    "When the sun reaches this direction, protected covers open again (auto up)."
   ],
   "catch_up_after": [
    "Catch up the evening run from",
    "After the restart protection the evening run is caught up for windows not yet closed this evening, but only after this time."
   ],
   "close_trigger_active_states": [
    "Active states",
    "States in which a close trigger counts as active (e.g. on, playing for a TV)."
   ],
   "close_trigger_entities": [
    "Close trigger",
    "When one of these entities becomes active, the cover closes once per active cycle, only with a closed window (otherwise as soon as it is closed). The cycle ends when all are inactive."
   ],
   "close_trigger_max_lock": [
    "Cycle at most",
    "After this time at the latest a new cycle starts, even if the triggers were active all the time."
   ],
   "close_trigger_min_position": [
    "Only if open more than",
    "Only closes when the cover is open further than this position."
   ],
   "close_trigger_off_delay": [
    "Inactive after",
    "All triggers must be inactive this long before the cycle ends and switching on closes again."
   ],
   "close_trigger_on_delay": [
    "Active after",
    "A trigger must be active this long before the cover closes (switching on briefly does not count)."
   ],
   "closed_position": [
    "Counts as closed up to",
    "Used for ventilation and the vacation morning."
   ],
   "command_interval": [
    "Spacing between cover commands",
    "Several covers move one after the other with this spacing (against radio collisions). 0 = all at once."
   ],
   "cooling_entity": [
    "Air conditioner",
    "Optional: while this air conditioner cools, the room counts as too warm. Sun protection then takes load off the air conditioner."
   ],
   "cover": [
    "Cover",
    "Optional. 100 % = open, 0 % = closed. Without a cover the window only serves the heating."
   ],
   "day_change_time": [
    "Day change",
    "Forecast check and reset of the daily sun protection markers and notifications."
   ],
   "evening_close": [
    "Evening run",
    "Close at the start of the evening mode, once per evening and only with a closed window."
   ],
   "evening_custom": [
    "Own evening times",
    "Use the following values instead of the global ones."
   ],
   "evening_earliest": [
    "Evening mode at the earliest",
    "The evening mode never starts before this time."
   ],
   "evening_elevation": [
    "Sun elevation",
    "The evening mode starts when the sun drops below this elevation (e.g. -4 °)."
   ],
   "evening_latest": [
    "Evening mode at the latest",
    "Time fallback: the evening mode starts at this time at the latest."
   ],
   "evening_position": [
    "Evening position",
    "Target of the evening run and of closing after the window was closed. 0 % = closed; e.g. 20 % leaves a gap on warm nights."
   ],
   "follow_up_close": [
    "Close after window closed",
    "If the window is closed in the evening, the cover closes (also during an override)."
   ],
   "follow_up_earliest": [
    "Close after window closed, from",
    "A window closed in the evening closes the cover only after this time."
   ],
   "forecast_type": [
    "Kind of forecast",
    "Automatic takes the first kind the weather entity supports (daily, twice daily, hourly). From hourly values the high of the day and the low of the night are calculated."
   ],
   "frost_position": [
    "Lowest position with frost",
    "Empty = off. With frost, closing stops at this position so the cover cannot freeze on, e.g. 5 %."
   ],
   "frost_threshold": [
    "Frost at or below",
    "Outdoor temperature. Only windows with a frost position take part."
   ],
   "group": [
    "Group",
    "Direction of the sun. Without a group the window has no sun protection."
   ],
   "heating_entity": [
    "Heating wanted",
    "Optional, e.g. an input_boolean \"heating season\" or the heating day of a heating control. While it is on, the warmth of the sun is welcome: sun protection only when the room of a window is too warm anyway. Windows without a room temperature are then not lowered."
   ],
   "language": [
    "Language of messages",
    "Logbook, last reason and push messages. Only while nothing is set under Settings > House."
   ],
   "lockout_protection": [
    "Lockout protection (door)",
    "While the contact reports open, nothing closes below the ventilation position, also not with the window exception or the weather protection."
   ],
   "lux_sensors": [
    "Brightness sensors",
    "Lux sensors at the windows. Every sensor of the group must reach the threshold of the window."
   ],
   "lux_threshold": [
    "Brightness threshold",
    "Every brightness sensor of the group must reach this value."
   ],
   "manual_at_sun_position": [
    "Moving onto the sun protection position counts",
    "A cover moved by anyone onto the sun protection position (up to the tolerance) while the sun shines is treated like automatic sun protection and opens again with auto up."
   ],
   "manual_detection_window": [
    "Detection period",
    "The manual movement must not be longer ago than this."
   ],
   "manual_follow_up": [
    "Follow-up of the sun condition",
    "For this detection the sun condition (without temperature) still counts this long after it ended."
   ],
   "manual_max_position": [
    "Manual sun protection up to",
    "A cover lowered by hand to at most this position while the sun shines counts as sun protection for today (no automatic movement)."
   ],
   "morning_earliest": [
    "At the earliest",
    "The cover never opens before this time, even if the trigger comes earlier."
   ],
   "morning_enabled": [
    "Morning opening",
    "Open the cover automatically in the morning."
   ],
   "morning_latest": [
    "At the latest",
    "If nothing triggered until then, the cover opens at this time."
   ],
   "morning_lux_hold": [
    "Hold time",
    "It must be bright enough this long before the cover opens."
   ],
   "morning_lux_threshold": [
    "Brightness",
    "Every brightness sensor of the group must reach this value."
   ],
   "morning_mode": [
    "Mode",
    "What starts the morning opening; its settings follow in the next step."
   ],
   "morning_position": [
    "Target position",
    "100 = open, less = partial opening."
   ],
   "morning_sun_elevation": [
    "Sun elevation",
    "Only for sun elevation: opens when the rising sun passes this elevation."
   ],
   "morning_sun_event": [
    "Event",
    "Sunrise or the sun reaching an elevation."
   ],
   "morning_sun_offset": [
    "Offset",
    "Minutes before (negative) or after the event."
   ],
   "morning_sun_position": [
    "Directly to sun protection if needed",
    "If the sun condition applies, open only to the sun protection position."
   ],
   "morning_time_weekend": [
    "Weekend and holidays",
    "Time on weekends and public holidays (holidays only with a workday sensor)."
   ],
   "morning_time_workday": [
    "Workdays",
    "Time on workdays (workday sensor or weekend days)."
   ],
   "morning_trigger_entity": [
    "Trigger entity",
    "A timestamp (e.g. the next alarm of a phone) opens at that time plus offset. Any other entity opens when it turns on (motion, switch)."
   ],
   "morning_trigger_offset": [
    "Offset",
    "Only for timestamps."
   ],
   "name": [
    "Name",
    "Also used for the device and its entities."
   ],
   "night_end": [
    "End of the night",
    "Evening mode and evening markers end at this time (or at sunrise if that is earlier)."
   ],
   "night_threshold": [
    "Late summer day only with a night from",
    "A summer day only by the outdoor temperature counts only when the forecast low of the coming night is at least this value. When the night cools down (spring, autumn), the warmth stays in the house. Without a low in the forecast the summer day counts as before."
   ],
   "notify_open_window": [
    "Notify about an open window",
    "Once a day, if an open window prevented the sun protection."
   ],
   "notify_services": [
    "Notification services",
    "Get a message when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone). Only while nothing is set under Settings > House."
   ],
   "open_block_entity": [
    "Opening block",
    "No automatic opening (auto up, ventilation, vacation morning, morning opening) unless this entity has one of the free states (e.g. a TV)."
   ],
   "open_block_free_states": [
    "Free states",
    "States of the opening block in which opening is still allowed (e.g. off, standby)."
   ],
   "outdoor_temperature": [
    "Outdoor temperature sensor",
    "For the summer day and the temperature condition of every window. Without a sensor the current temperature of the weather entity is used (at least one of both). Only while nothing is set under Settings > House."
   ],
   "override_duration": [
    "Duration",
    "After a manual movement the automatic pauses this long for the window. Every further movement starts it again. 0 = until sunrise."
   ],
   "override_ignore_evening": [
    "Evening and vacation runs despite override",
    "e.g. bedrooms that should always close in the evening."
   ],
   "override_sunrise_reset": [
    "Also end at sunrise",
    "The override also ends at the next sunrise, even if the duration is still running."
   ],
   "override_trigger": [
    "Override starts",
    "Only with a real movement: a command to a cover already at its target (e.g. \"open all\" while it is open) does not start an override. Every command: also without movement, as before."
   ],
   "position_tolerance": [
    "Tolerance for auto up",
    "Auto up only opens covers standing at the sun protection position up to this much above it. Covers moved elsewhere by hand stay."
   ],
   "protection_keep_closed": [
    "Further closed counts as protected",
    "A cover already further closed than its position with wind or rain is not opened to it (e.g. closed at 0 % with a wind position of 20 %). Not for a position of 100 %: retracting external venetian blinds always runs."
   ],
   "protection_release": [
    "Release after",
    "A protection ends only after the value stayed on the safe side this long. An unavailable sensor never ends a protection."
   ],
   "pv_sensors": [
    "PV power sensors",
    "Power of a solar system or panel facing this direction (W)."
   ],
   "pv_threshold": [
    "PV threshold",
    "Every PV sensor of the group must reach this value."
   ],
   "radiation_sensors": [
    "Radiation sensors",
    "Solar radiation in W/m², e.g. from a weather service or a weather station."
   ],
   "radiation_threshold": [
    "Radiation threshold",
    "Every radiation sensor of the group must reach this value."
   ],
   "rain_entity": [
    "Rain sensor",
    "A rain sensor that turns on, or an amount of rain (e.g. mm/h)."
   ],
   "rain_position": [
    "Position with rain",
    "Empty = not affected. E.g. 0 % for a roof window shutter."
   ],
   "rain_threshold": [
    "Rain protection above",
    "Only for a numeric rain sensor: rain counts above this value."
   ],
   "room": [
    "Room",
    "Optional. The heating of the room uses the contacts of the window; the cover takes room temperature and air conditioner of the room."
   ],
   "room_entity": [
    "Room temperature",
    "Optional: thermostat (climate) or temperature sensor of the room. Then the cover is only lowered when the room is too warm. Without a value the condition counts as met (except on a heating day)."
   ],
   "room_margin": [
    "Too warm from setpoint plus",
    "With a thermostat: too warm from its setpoint plus this margin."
   ],
   "room_threshold": [
    "Too warm from",
    "With a temperature sensor (or a thermostat without a setpoint): too warm from this temperature."
   ],
   "size": [
    "Size",
    "How fast airing exchanges the air: the suggested airing time follows it, and the largest opening is suggested for airing. The size applies to every contact of the window."
   ],
   "startup_delay": [
    "Restart protection",
    "No movement for this time after Home Assistant started (sensors and covers are still coming online)."
   ],
   "summer_threshold": [
    "Summer day from forecast high",
    "Without a summer day there is no sun protection. During the day the summer day also starts when the outdoor temperature rises above this value (see night)."
   ],
   "sun_hold": [
    "Sun hold time",
    "Summer day, temperature, room and all sun sensors must be met this long. The condition ends immediately."
   ],
   "sun_position": [
    "Sun protection position",
    "Lowered once a day to this position. A cover already further closed is left alone."
   ],
   "temperature_hold": [
    "Temperature hold time",
    "The outdoor temperature must stay above the value this long. Below it the condition ends immediately."
   ],
   "temperature_threshold": [
    "Outdoor temperature at least",
    "Sun protection only from this outdoor temperature on."
   ],
   "tilt_sensors": [
    "Tilt contacts",
    "'on' = tilted. While the window is only tilted, covers close no further than the ventilation position."
   ],
   "use_heating_day": [
    "Heating day of the heating",
    "Without an own heat need entity: the heating day of the heating module, but only within the heating period. Only while the heating module is switched on."
   ],
   "vacation": [
    "Vacation simulation",
    "Take part in the random opening and closing during vacation."
   ],
   "vacation_entities": [
    "Vacation entities",
    "Vacation is active while one of them is on (e.g. an input_boolean \"vacation\" or a calendar). Only while nothing is set under Settings > Vacation. The switch “Vacation” of the house always counts."
   ],
   "vacation_evening_start": [
    "Vacation evening from",
    "Starts the evening for the windows in the simulation and closes them at random times. The normal evening run rests during vacation."
   ],
   "vacation_evening_window": [
    "Random period in the evening",
    "Each window closes at a random time within this period."
   ],
   "vacation_heat_protection": [
    "Heat protection on vacation",
    "On vacation the sun protection lowers without waiting for room temperature, air conditioner or heat need. Summer day, outdoor temperature, sun sensors, hold times and the sun switch of the window still apply."
   ],
   "vacation_morning_start": [
    "Vacation morning from",
    "Closed covers of the windows in the simulation open at a random time after this."
   ],
   "vacation_morning_window": [
    "Random period in the morning",
    "Each window opens at a random time within this period."
   ],
   "vacation_position_max": [
    "Opening position to",
    "Random position between both values."
   ],
   "vacation_position_min": [
    "Opening position from",
    "Random position between both values."
   ],
   "ventilation": [
    "Ventilate when the window opens",
    "Opening the window moves a closed cover to the ventilation position (in the evening after the short delay, during the day after the long one)."
   ],
   "ventilation_delay_day": [
    "Delay during the day",
    "The window must still be open afterwards."
   ],
   "ventilation_delay_evening": [
    "Delay in the evening",
    "In the evening mode the cover moves to the ventilation position after this short time."
   ],
   "ventilation_position": [
    "Ventilation position",
    "Position for ventilation (100 % = open)."
   ],
   "verify_after": [
    "Check the position after",
    "If a cover has not reached its target by then, the command is repeated once; then a notification is sent. 0 = off."
   ],
   "weather": [
    "Weather entity",
    "Its daily forecast decides at the day change whether today is a summer day. Only while nothing is set under Settings > House."
   ],
   "weather_protection": [
    "Weather protection for this window",
    "Off = wind, rain and frost never move or limit this cover, whatever the positions below say. Turn it on for every window that should take part. With the automatic off (globally or for this window) there is no weather protection either."
   ],
   "weekend_days": [
    "Weekend days",
    "Only without a workday sensor: on these days the weekend time of the morning opening applies. Only while nothing is set under Settings > House."
   ],
   "wind_entity": [
    "Wind sensor",
    "Wind speed or gusts, e.g. from a weather station."
   ],
   "wind_position": [
    "Position with wind",
    "Empty = not affected. E.g. 100 % retracts external venetian blinds. Only with the weather protection of the window on."
   ],
   "wind_threshold": [
    "Wind protection from",
    "In the unit of the wind sensor (e.g. km/h or m/s)."
   ],
   "window_closed_delay": [
    "Window counts as closed after",
    "A window contact must report closed this long before closing after the window, sun protection or the close trigger act (against bouncing contacts)."
   ],
   "window_exception_entity": [
    "Window exception",
    "While this entity is available, an open window does not prevent closing movements and no message is sent (e.g. an air conditioner with its hose through the balcony door). Not used for the vacation evening."
   ],
   "window_sensors": [
    "Window contacts",
    "'on' = open. Window handles with the states open, tilted and closed work as well. Unknown or unavailable counts as open. A contact belongs to one window only."
   ],
   "window_wind_threshold": [
    "Own wind threshold",
    "Empty = wind protection from the threshold of the basic settings. Otherwise this window is protected already or only from this value (unit of the wind sensor)."
   ],
   "workday_entity": [
    "Workday sensor",
    "Optional, for the morning opening by time (e.g. Workday integration, knows public holidays). Without a sensor the weekend days decide. Only while nothing is set under Settings > House."
   ]
  }
 },
 "CHOICES": {
  "de": {
   "forecast_type": {
    "auto": "Automatisch",
    "daily": "Täglich",
    "twice_daily": "Zweimal täglich",
    "hourly": "Stündlich"
   },
   "language": {
    "auto": "Wie Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "morning_mode": {
    "time": "Feste Uhrzeit (Werktag / Wochenende)",
    "sun": "Sonnenstand (Aufgang oder Höhe)",
    "brightness": "Helligkeit der Gruppe",
    "trigger": "Auslöser-Entität (Wecker, Bewegung, Schalter)"
   },
   "morning_sun_event": {
    "sunrise": "Sonnenaufgang",
    "elevation": "Sonnenhöhe"
   },
   "override_trigger": {
    "movement": "Nur wenn das Rollo wirklich fährt",
    "command": "Bei jedem Befehl von Hand, auch ohne Fahrt"
   },
   "service_action": {
    "open": "Öffnen",
    "close": "Schließen",
    "evening": "Abendposition",
    "sun_protection": "Sonnenschutz-Position",
    "ventilation": "Lüftungsposition",
    "position": "Position"
   },
   "weekday": {
    "mon": "Montag",
    "tue": "Dienstag",
    "wed": "Mittwoch",
    "thu": "Donnerstag",
    "fri": "Freitag",
    "sat": "Samstag",
    "sun": "Sonntag"
   },
   "window_size": {
    "small": "Klein (z. B. Dachfenster)",
    "medium": "Mittel",
    "large": "Groß (z. B. zweiflügelig)",
    "door": "Tür (z. B. Balkontür)"
   }
  },
  "en": {
   "forecast_type": {
    "auto": "Automatic",
    "daily": "Daily",
    "twice_daily": "Twice daily",
    "hourly": "Hourly"
   },
   "language": {
    "auto": "Like Home Assistant",
    "de": "Deutsch",
    "en": "English"
   },
   "morning_mode": {
    "time": "Fixed time (workday / weekend)",
    "sun": "Sun (sunrise or elevation)",
    "brightness": "Brightness of the group",
    "trigger": "Trigger entity (alarm, motion, switch)"
   },
   "morning_sun_event": {
    "sunrise": "Sunrise",
    "elevation": "Sun elevation"
   },
   "override_trigger": {
    "movement": "Only when the cover really moves",
    "command": "With every command by hand, also without movement"
   },
   "service_action": {
    "open": "Open",
    "close": "Close",
    "evening": "Evening position",
    "sun_protection": "Sun protection position",
    "ventilation": "Ventilation position",
    "position": "Position"
   },
   "weekday": {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
    "sun": "Sunday"
   },
   "window_size": {
    "small": "Small (e.g. skylight)",
    "medium": "Medium",
    "large": "Large (e.g. double casement)",
    "door": "Door (e.g. balcony door)"
   }
  }
 },
 "ERRORS": {
  "de": {
   "latest_before_earliest": "Die späteste Zeit liegt vor der frühesten. Bitte die späteste Zeit nach hinten oder die früheste nach vorne verschieben.",
   "night_end_after_evening": "Das Ende der Nacht muss vor dem frühesten Abendbeginn liegen, z. B. 03:30 bei Abendbeginn ab 17:00.",
   "min_above_max": "Das Minimum ist größer als das Maximum. Bitte die Werte tauschen oder anpassen.",
   "name_required": "Bitte einen Namen eingeben.",
   "azimuth_equal": "Azimut von und bis müssen verschieden sein.",
   "no_lux_sensor": "Die Gruppe dieses Fensters hat keinen Helligkeitssensor. Füge der Gruppe einen Helligkeitssensor hinzu oder wähle einen anderen Modus.",
   "need_temperature_source": "Bitte einen Außentemperatur-Sensor oder eine Wetter-Entität wählen; ohne Temperatur gibt es keinen Sommertag.",
   "not_numeric": "Diese Entität meldet keinen Zahlenwert. Bitte einen Sensor mit Messwert wählen (z. B. °C, lx, W, W/m²).",
   "invalid_notify_service": "Nur Benachrichtigungsdienste (notify.…) sind erlaubt. Bitte einen Dienst aus der Liste wählen.",
   "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern.",
   "invalid_day_month": "Bitte ein gültiges Datum angeben (TT.MM., z. B. 01.10.); einen Tag wie den 31.02. gibt es nicht.",
   "invalid_auth": "Anthropic hat den API-Key abgelehnt. Prüfe ihn unter console.anthropic.com > API Keys und füge ihn ohne Leerzeichen ein. Ohne Key läuft die lokale Regelung weiter.",
   "cannot_connect": "Anthropic ist nicht erreichbar. Prüfe Internetverbindung, Proxy und Firewall. Der Key wurde nicht gespeichert.",
   "max_below_base": "Das maximale Intervall muss mindestens so groß sein wie das Prüfintervall (z. B. alle 4 h prüfen, höchstens alle 48 h).",
   "outdoor_required": "Bitte einen Außentemperatursensor oder eine Wetter-Entität wählen."
  },
  "en": {
   "latest_before_earliest": "The latest time is before the earliest one. Move the latest time later or the earliest earlier.",
   "night_end_after_evening": "The end of the night must be before the earliest evening start, e.g. 03:30 with an evening from 17:00.",
   "min_above_max": "The minimum is above the maximum. Swap or adjust the values.",
   "name_required": "Please enter a name.",
   "azimuth_equal": "Azimuth from and to must differ.",
   "no_lux_sensor": "The group of this window has no brightness sensor. Add a brightness sensor to the group or choose another mode.",
   "need_temperature_source": "Choose an outdoor temperature sensor or a weather entity; without a temperature there is no summer day.",
   "not_numeric": "This entity does not report a number. Choose a sensor with a measured value (e.g. °C, lx, W, W/m²).",
   "invalid_notify_service": "Only notification services (notify.…) are allowed. Choose a service from the list.",
   "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window.",
   "invalid_day_month": "Please enter a valid date (DD.MM., e.g. 01.10.); a day like 31.02. does not exist.",
   "invalid_auth": "Anthropic rejected the API key. Check it at console.anthropic.com under API keys and paste it without spaces. Without a key the local control keeps running.",
   "cannot_connect": "Anthropic cannot be reached. Check the internet connection, proxy and firewall. The key was not saved.",
   "max_below_base": "The maximum interval must be at least the check interval (e.g. check every 4 h, at most every 48 h).",
   "outdoor_required": "Choose an outdoor temperature sensor or a weather entity."
  }
 },
 "STATUS": {
  "de": {
   "off": "Automatik aus",
   "startup": "Neustart-Schutz",
   "override": "Manuelle Übersteuerung",
   "evening": "Abends geschlossen",
   "sun_protection": "Sonnenschutz",
   "vacation": "Urlaubssimulation",
   "ready": "Bereit",
   "protection": "Wetterschutz"
  },
  "en": {
   "off": "Automatic off",
   "startup": "Restart protection",
   "override": "Manual override",
   "evening": "Closed for the evening",
   "sun_protection": "Sun protection",
   "vacation": "Vacation simulation",
   "ready": "Ready",
   "protection": "Weather protection"
  }
 },
 "NEXT_ACTION": {
  "de": {
   "evening": "Abendlauf",
   "morning": "Morgenöffnung",
   "override_end": "Ende der Übersteuerung",
   "sun_enter": "Sonne kommt in den Bereich",
   "sun_leave": "Sonne verlässt den Bereich",
   "protection_end": "Wetterschutz kann enden"
  },
  "en": {
   "evening": "Evening run",
   "morning": "Morning opening",
   "override_end": "End of the override",
   "sun_enter": "Sun enters the sector",
   "sun_leave": "Sun leaves the sector",
   "protection_end": "Weather protection may end"
  }
 }
};
export const METER = {
 "de": {
  "external_light_mode": {
   "capture": "Nur während der Aufnahme",
   "permanent": "Dauerlicht"
  },
  "fields": {
   "ai_task_entity": [
    "KI-Aufgabe",
    "KI-Aufgaben-Entität, die die Bilder liest (z. B. Anthropic, OpenAI, Google oder Ollama mit Bildunterstützung). Ein Zähler kann eine eigene nutzen."
   ],
   "notify_rejected": [
    "Benachrichtigungen",
    "Hauptschalter für die Benachrichtigungen in Home Assistant. Ab wann sie bei welchem Zähler kommen, steht beim Zähler unter „Benachrichtigungen“."
   ],
   "name": [
    "Name",
    ""
   ],
   "meter_type": [
    "Zählerart",
    ""
   ],
   "camera": [
    "Kamera",
    "Kamera-Entität, die auf die Anzeige zeigt (z. B. ESP32-CAM mit ESPHome)."
   ],
   "light": [
    "Licht",
    "Optional. Wird für das Bild ein- und danach wieder ausgeschaltet (z. B. die Blitz-LED)."
   ],
   "light_brightness": [
    "Helligkeit",
    "Helligkeit des Lichts für das Bild. Am besten mit einem Testbild ausprobieren: Spiegelungen machen die Anzeige unlesbar."
   ],
   "light_brightness_2": [
    "Helligkeit 2. Bild",
    "Optional (0 = aus): Pro Versuch wird ein zweites Bild mit dieser Helligkeit aufgenommen, und die KI bekommt beide. Hilft, wenn bei einer Helligkeit ein Lichtfleck Ziffern überstrahlt und bei der anderen Ziffern zu dunkel sind. Ein Versuch dauert dadurch länger."
   ],
   "warmup": [
    "Vorlaufzeit",
    "Wartezeit nach dem Einschalten des Lichts, damit die Kamera die Belichtung anpasst."
   ],
   "discard_frames": [
    "Verworfene Bilder",
    "Bilder, die vor dem eigentlichen Bild weggeworfen werden. Kameras mit Puffer (ESP32-CAM) liefern sonst ein altes Bild ohne Licht."
   ],
   "external_light": [
    "Externe Beleuchtung",
    "Optional. light- oder switch-Entität, die die Anzeige zusätzlich ausleuchtet. Leer lassen, wenn es keine gibt."
   ],
   "external_light_mode": [
    "Modus",
    "Nur während der Aufnahme: wird vor den Bildern ein- und danach wieder ausgeschaltet. Dauerlicht: wird nur eingeschaltet, falls es aus ist, und bleibt an."
   ],
   "external_light_brightness": [
    "Helligkeit",
    "Nur bei einer dimmbaren light-Entität; ein Schalter wird nur ein- und ausgeschaltet."
   ],
   "external_light_lead_time": [
    "Vorlaufzeit",
    "Wartezeit nach dem Einschalten der externen Beleuchtung, bevor das Licht der Kamera eingeschaltet wird und die Bilder aufgenommen werden."
   ],
   "external_light_turn_off": [
    "Danach ausschalten",
    "Nur im Modus „Nur während der Aufnahme“: schaltet das Licht nach den Bildern wieder aus, auch wenn Aufnahme oder Auswertung fehlschlagen."
   ],
   "crop_left": [
    "Links",
    "Linker Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
   ],
   "crop_top": [
    "Oben",
    "Oberer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
   ],
   "crop_right": [
    "Rechts",
    "Rechter Rand des Ausschnitts in Prozent der Breite des gedrehten Bildes."
   ],
   "crop_bottom": [
    "Unten",
    "Unterer Rand des Ausschnitts in Prozent der Höhe des gedrehten Bildes."
   ],
   "rotate": [
    "Drehen",
    "Dreht das Bild im Uhrzeigersinn um diesen Winkel (negativ: gegen den Uhrzeigersinn), z. B. 90 für eine seitlich montierte Kamera oder ein paar Grad für eine schief sitzende Anzeige. Gedreht wird vor dem Zuschneiden, der Ausschnitt bezieht sich auf das gedrehte Bild."
   ],
   "exposure": [
    "Belichtung",
    "Helligkeit des Bildes für die KI: 100 % lässt es unverändert, darunter dunkler (gegen Spiegelungen und Überbelichtung), darüber heller."
   ],
   "enhance": [
    "Bild aufbereiten",
    "Macht das Bild grau, gleicht die Ausleuchtung aus und hebt den Kontrast an, bevor die KI es liest. Hilft, wenn das Licht einen hellen Fleck auf dem Displayglas und dunkle Ecken hinterlässt, oder bei blassen LCD-Segmenten. Im Live-Bild nicht zu sehen, dafür ein Testbild machen."
   ],
   "unit": [
    "Einheit",
    "Einheit auf der Anzeige (z. B. MWh, kWh oder m³)."
   ],
   "decimals": [
    "Nachkommastellen",
    "Anzahl der Nachkommastellen auf der Anzeige."
   ],
   "hints": [
    "Hinweise für die KI",
    "Optional. Was an dieser Anzeige besonders ist, z. B. Linien, die zu keiner Ziffer gehören, oder welche Ziffern nicht mitgelesen werden."
   ],
   "prompt": [
    "Eigene Anweisung an die KI",
    "Ersetzt die ganze automatisch erzeugte Anweisung (leer lassen für den Standard). Einheit, Nachkommastellen und Hinweise werden dann nicht mehr eingesetzt. Die KI soll weiterhin nur die Zahl oder „unlesbar“ antworten."
   ],
   "interval": [
    "Intervall",
    "Zeit zwischen zwei automatischen Ablesungen."
   ],
   "condition_entity": [
    "Bedingung",
    "Optional. Solange diese Entität 'aus' ist, gilt das zweite Intervall (z. B. ein Heiztag-Sensor)."
   ],
   "condition_heating_day": [
    "Tage ohne Heizen wie Bedingung aus",
    "Das zweite Intervall gilt auch an Tagen ohne Heizen (Heiztag des Heizungsmoduls, nur in der Heizperiode). Ist die Heizung aus oder der Heiztag unbekannt, gilt das normale Intervall."
   ],
   "interval_off": [
    "Intervall, wenn die Bedingung aus ist",
    "Nur zusammen mit einer Bedingung oder den Tagen ohne Heizen."
   ],
   "max_rate": [
    "Größter Anstieg pro Stunde",
    "In der Einheit des Zählers. Ein größerer Anstieg seit der letzten gültigen Ablesung wird verworfen (z. B. 0,05 MWh = 50 kW)."
   ],
   "max_correction": [
    "Größte Korrektur",
    "In der Einheit des Zählers. Ein kleinerer Wert als zuvor wird nur übernommen, wenn er höchstens so viel kleiner ist und von weiteren Bildern bestätigt wird."
   ],
   "max_attempts": [
    "Bilder pro Ablesung",
    "Höchstens so viele Bilder, bis ein Wert zweimal gelesen wurde."
   ],
   "confirmations": [
    "Bestätigungsbilder",
    "Weitere Bilder, die alle den kleineren Wert zeigen müssen, bevor er als Korrektur übernommen wird."
   ],
   "history_hint": [
    "Letzte Stände an die KI",
    "Die KI bekommt die letzten 3 gültigen Zählerstände als Hinweis, um eine unklare Ziffer plausibel zu entscheiden. Sie soll trotzdem nur ablesen, was im Bild steht; die Prüfungen hier bleiben bestehen. Kann dazu verleiten, einen erwarteten Wert zu nennen, daher vor allem bei schwer lesbaren Anzeigen nutzen."
   ],
   "meter_ai_task_entity": [
    "Eigene KI-Aufgabe",
    "Optional. Statt der KI-Aufgabe der Integration."
   ],
   "notify_smaller": [
    "Kleiner als zuvor",
    "Wert kleiner als der letzte gültige und nicht als Korrektur bestätigt (verworfen)."
   ],
   "notify_too_large": [
    "Anstieg zu groß",
    "Wert stärker gestiegen als der größte Anstieg pro Stunde erlaubt (verworfen)."
   ],
   "notify_corrected": [
    "Korrigiert",
    "Kleinerer Wert von weiteren Bildern bestätigt und übernommen."
   ],
   "notify_failed": [
    "Unlesbar oder Fehler",
    "KI liest nichts Eindeutiges, oder Kamera bzw. KI nicht erreichbar. Unlesbare Ablesungen unterbrechen die Zählung der anderen Fälle nicht."
   ],
   "vacation_alert": [
    "Im Urlaub warnen",
    "Standard: an beim Wasserzähler, sonst aus."
   ],
   "vacation_amount": [
    "Menge",
    "Verbrauch seit Urlaubsbeginn in Litern (Wasser, Gas) bzw. kWh (Strom), ab dem gewarnt wird. 0 = aus. Standard Wasser: 20 L."
   ],
   "vacation_rate": [
    "Mittlerer Durchfluss bzw. Leistung",
    "Mittel seit Urlaubsbeginn in L/h bzw. kW (frühestens nach einer Stunde), ab dem gewarnt wird. Bei Gas und Strom die Grundlast eintragen. 0 = aus. Standard Wasser: 5 L/h."
   ]
  },
  "sections": {
   "camera_section": [
    "Kamera und Licht",
    "Kamera am Zähler und das Licht, das für das Bild eingeschaltet wird."
   ],
   "external_light_section": [
    "Externe Beleuchtung",
    "Optional zusätzliches Licht (light- oder switch-Entität) neben dem Licht der Kamera, z. B. LED-Module. Ist es nicht erreichbar, wird ohne es abgelesen und eine Warnung ins Log geschrieben."
   ],
   "image_section": [
    "Bildausschnitt",
    "Nur dieser Teil des Bildes geht an die KI. Bei Weitwinkel-Kameras auf die Anzeige zuschneiden; im Dashboard lässt sich der Ausschnitt mit der Maus aufziehen."
   ],
   "display_section": [
    "Anzeige",
    "Was die Anzeige zeigt. Die Hinweise bekommt die KI mit."
   ],
   "schedule_section": [
    "Zeitplan",
    "Wie oft der Zähler automatisch abgelesen wird."
   ],
   "checks_section": [
    "Prüfungen",
    "Mehrheitsentscheid und Plausibilitätsprüfung einer Ablesung."
   ],
   "notify_section": [
    "Benachrichtigungen",
    "Ab dem wievielten Mal in Folge eine Benachrichtigung in Home Assistant erscheint (0 = nie, 1 = sofort). Eine gültige Ablesung setzt die Zählung zurück. Gilt nur, solange in den Einstellungen der Integration Benachrichtigungen eingeschaltet sind."
   ],
   "vacation_section": [
    "Urlaub",
    "Warnt, wenn im Urlaub etwas läuft: eine Meldung, ein Logbuch-Eintrag und das Ereignis house_assistant_vacation_alert, einmal je Urlaub und Fall. Gezählt ab der letzten gültigen Ablesung vor dem Urlaub. Nicht für den Wärmezähler."
   ]
  },
  "errors": {
   "name_required": "Bitte einen Namen eingeben.",
   "camera_required": "Bitte eine Kamera auswählen."
  },
  "status": {
   "ok": "Gültig",
   "corrected": "Korrigiert",
   "unreadable": "Unlesbar",
   "error": "Kamera- oder KI-Fehler",
   "smaller": "Kleiner als zuvor",
   "too_large": "Anstieg zu groß",
   "manual": "Von Hand gesetzt"
  },
  "types": {
   "heat": "Wärmezähler",
   "water": "Wasserzähler",
   "gas": "Gaszähler",
   "electricity": "Stromzähler",
   "other": "Anderer Zähler"
  }
 },
 "en": {
  "external_light_mode": {
   "capture": "Only while taking pictures",
   "permanent": "Always on"
  },
  "fields": {
   "ai_task_entity": [
    "AI task",
    "AI task entity that reads the pictures (e.g. Anthropic, OpenAI, Google or Ollama with image support). A meter can use its own one."
   ],
   "notify_rejected": [
    "Notifications",
    "Main switch for the notifications in Home Assistant. When they come for which meter is set at the meter under \"Notifications\"."
   ],
   "name": [
    "Name",
    ""
   ],
   "meter_type": [
    "Meter type",
    ""
   ],
   "camera": [
    "Camera",
    "Camera entity pointed at the display (e.g. an ESP32-CAM with ESPHome)."
   ],
   "light": [
    "Light",
    "Optional. Switched on for the picture and off again afterwards (e.g. the flash LED)."
   ],
   "light_brightness": [
    "Light brightness",
    "Brightness of the light for the picture. Try it with a test picture: reflections make the display unreadable."
   ],
   "light_brightness_2": [
    "Brightness 2nd picture",
    "Optional (0 = off): each attempt also takes a second picture with this brightness, and the AI gets both. Helps when at one brightness a light spot outshines digits and at the other digits are too dark. An attempt takes longer."
   ],
   "warmup": [
    "Warm-up time",
    "Wait after switching the light on, so the camera adjusts its exposure."
   ],
   "discard_frames": [
    "Discarded pictures",
    "Pictures thrown away before the real one. Cameras with a buffer (ESP32-CAM) otherwise deliver an old picture without light."
   ],
   "external_light": [
    "External light",
    "Optional. Light or switch entity that lights the display in addition. Leave empty when there is none."
   ],
   "external_light_mode": [
    "Mode",
    "Only while taking pictures: switched on before the pictures and off afterwards. Always on: only switched on when it is off, and left on."
   ],
   "external_light_brightness": [
    "Brightness",
    "Only for a light entity that can be dimmed; a switch is just switched on and off."
   ],
   "external_light_lead_time": [
    "Lead time",
    "Wait after switching the external light on, before the light of the camera is switched on and the pictures are taken."
   ],
   "external_light_turn_off": [
    "Switch off afterwards",
    "Only in the mode \"Only while taking pictures\": switches the light off after the pictures, also when taking or reading them fails."
   ],
   "crop_left": [
    "Left",
    "Left edge of the crop in percent of the width of the turned picture."
   ],
   "crop_top": [
    "Top",
    "Top edge of the crop in percent of the height of the turned picture."
   ],
   "crop_right": [
    "Right",
    "Right edge of the crop in percent of the width of the turned picture."
   ],
   "crop_bottom": [
    "Bottom",
    "Bottom edge of the crop in percent of the height of the turned picture."
   ],
   "rotate": [
    "Rotate",
    "Turns the picture clockwise by this angle (negative: counterclockwise), e.g. 90 for a camera mounted sideways or a few degrees for a display that sits askew. Turned before cropping, the crop refers to the turned picture."
   ],
   "exposure": [
    "Exposure",
    "Brightness of the picture for the AI: 100 % leaves it unchanged, below is darker (against reflections and overexposure), above is brighter."
   ],
   "enhance": [
    "Enhance picture",
    "Turns the picture grey, evens out the lighting and stretches the contrast before the AI reads it. Helps when the light leaves a bright spot on the display glass and dark corners, or with pale LCD segments. Not shown in the live picture; take a test picture to see it."
   ],
   "unit": [
    "Unit",
    "Unit shown on the display (e.g. MWh, kWh or m³)."
   ],
   "decimals": [
    "Decimals",
    "Number of decimals shown on the display."
   ],
   "hints": [
    "Hints for the AI",
    "Optional. What is special about this display, e.g. lines that are not part of a digit, or which digits to ignore."
   ],
   "prompt": [
    "Own instructions for the AI",
    "Replace the whole generated instructions (leave empty for the standard). Unit, decimals and hints are then no longer inserted. The AI should still answer only with the number or “unreadable”."
   ],
   "interval": [
    "Interval",
    "Time between two automatic readings."
   ],
   "condition_entity": [
    "Condition",
    "Optional. While this entity is 'off', the second interval applies (e.g. a heating day sensor)."
   ],
   "condition_heating_day": [
    "Days without heating like condition off",
    "The second interval also applies on days without heating (heating day of the heating module, only within the heating period). With the heating off or an unknown heating day the normal interval applies."
   ],
   "interval_off": [
    "Interval while the condition is off",
    "Only together with a condition or the days without heating."
   ],
   "max_rate": [
    "Largest increase per hour",
    "In the meter unit. A larger increase since the last valid reading is rejected (e.g. 0.05 MWh = 50 kW)."
   ],
   "max_correction": [
    "Largest correction",
    "In the meter unit. A smaller value than before is only taken when it is at most this much lower and confirmed by further pictures."
   ],
   "max_attempts": [
    "Pictures per reading",
    "Most pictures until a value has been read twice."
   ],
   "confirmations": [
    "Confirmation pictures",
    "Further pictures that must all show a smaller value before it is taken as a correction."
   ],
   "history_hint": [
    "Last readings to the AI",
    "The AI gets the last 3 valid readings as a hint, to decide an unclear digit plausibly. It should still read only what the picture shows; the checks here stay in place. Can tempt the AI to name an expected value, so use it mainly for displays that are hard to read."
   ],
   "meter_ai_task_entity": [
    "Own AI task",
    "Optional. Instead of the AI task of the integration."
   ],
   "notify_smaller": [
    "Smaller than before",
    "Value below the last valid one and not confirmed as a correction (rejected)."
   ],
   "notify_too_large": [
    "Increase too large",
    "Value rose more than the largest increase per hour allows (rejected)."
   ],
   "notify_corrected": [
    "Corrected",
    "Smaller value confirmed by more pictures and taken."
   ],
   "notify_failed": [
    "Unreadable or error",
    "The AI reads nothing clear, or the camera or AI is not reachable. Unreadable readings do not interrupt the count of the other cases."
   ],
   "vacation_alert": [
    "Warn on vacation",
    "Default: on for a water meter, else off."
   ],
   "vacation_amount": [
    "Amount",
    "Used since the vacation started, in litres (water, gas) or kWh (electricity), from which it warns. 0 = off. Default water: 20 L."
   ],
   "vacation_rate": [
    "Mean flow or power",
    "Mean since the vacation started in L/h or kW (after an hour at the earliest) from which it warns. For gas and electricity enter the base load. 0 = off. Default water: 5 L/h."
   ]
  },
  "sections": {
   "camera_section": [
    "Camera and light",
    "Camera of the meter and the light that is switched on for the picture."
   ],
   "external_light_section": [
    "External light",
    "Optional extra light (light or switch entity) besides the light of the camera, e.g. LED modules. When it cannot be reached, the meter is read without it and a warning is logged."
   ],
   "image_section": [
    "Picture crop",
    "Only this part of the picture is sent to the AI. Crop wide-angle cameras to the display; in the dashboard the crop can be drawn with the mouse."
   ],
   "display_section": [
    "Display",
    "What the display shows. The hints are passed on to the AI."
   ],
   "schedule_section": [
    "Schedule",
    "How often the meter is read automatically."
   ],
   "checks_section": [
    "Checks",
    "Majority vote and plausibility check of a reading."
   ],
   "notify_section": [
    "Notifications",
    "From the how-many-th time in a row a notification appears in Home Assistant (0 = never, 1 = at once). A valid reading starts the count again. Only while notifications are switched on in the settings of the integration."
   ],
   "vacation_section": [
    "Vacation",
    "Warns when something runs on vacation: a message, a logbook entry and the event house_assistant_vacation_alert, once per vacation and case. Counted from the last valid reading before the vacation. Not for the heat meter."
   ]
  },
  "errors": {
   "name_required": "Please enter a name.",
   "camera_required": "Please select a camera."
  },
  "status": {
   "ok": "Valid",
   "corrected": "Corrected",
   "unreadable": "Unreadable",
   "error": "Camera or AI error",
   "smaller": "Smaller than before",
   "too_large": "Increase too large",
   "manual": "Set by hand"
  },
  "types": {
   "heat": "Heat meter",
   "water": "Water meter",
   "gas": "Gas meter",
   "electricity": "Electricity meter",
   "other": "Other meter"
  }
 }
};
