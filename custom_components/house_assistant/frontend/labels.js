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
   "config.shutter": {
    "title": "Rollos",
    "fields": {
     "outdoor_temperature": [
      "Außentemperatur-Sensor",
      "Für den Sommertag und die Temperaturbedingung jedes Fensters. Ohne Sensor wird die aktuelle Temperatur der Wetter-Entität verwendet (mindestens eins von beiden)."
     ],
     "weather": [
      "Wetter-Entität",
      "Ihre Tagesvorhersage entscheidet beim Tageswechsel, ob heute ein Sommertag ist."
     ],
     "language": [
      "Sprache der Meldungen",
      "Logbuch, letzter Grund und Push-Nachrichten."
     ],
     "notify_services": [
      "Benachrichtigungsdienste",
      "Erhalten eine Nachricht, wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
     ],
     "workday_entity": [
      "Werktag-Sensor",
      "Optional, für die Morgenöffnung nach Uhrzeit (z. B. Workday-Integration, berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
     ],
     "weekend_days": [
      "Wochenendtage",
      "Nur ohne Werktag-Sensor: an diesen Tagen gilt die Wochenend-Uhrzeit der Morgenöffnung."
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
      "Für den Sommertag und die Temperaturbedingung jedes Fensters. Ohne Sensor wird die aktuelle Temperatur der Wetter-Entität verwendet (mindestens eins von beiden)."
     ],
     "weather": [
      "Wetter-Entität",
      "Ihre Tagesvorhersage entscheidet beim Tageswechsel, ob heute ein Sommertag ist."
     ],
     "language": [
      "Sprache der Meldungen",
      "Logbuch, letzter Grund und Push-Nachrichten."
     ],
     "notify_services": [
      "Benachrichtigungsdienste",
      "Erhalten eine Nachricht, wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
     ],
     "workday_entity": [
      "Werktag-Sensor",
      "Optional, für die Morgenöffnung nach Uhrzeit (z. B. Workday-Integration, berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
     ],
     "weekend_days": [
      "Wochenendtage",
      "Nur ohne Werktag-Sensor: an diesen Tagen gilt die Wochenend-Uhrzeit der Morgenöffnung."
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
      "Urlaub ist aktiv, solange eine davon an ist (z. B. ein input_boolean „Urlaub“ oder ein Kalender)."
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
     "cover": [
      "Rollo",
      "100 % = offen, 0 % = zu."
     ],
     "window_sensors": [
      "Fensterkontakte",
      "'on' = offen. Fenstergriffe mit den Zuständen open, tilted und closed gehen auch. Unbekannt oder nicht verfügbar zählt als offen."
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
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern."
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
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern."
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
    "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern."
   },
   "meter": {
    "name_required": "Bitte einen Namen eingeben.",
    "camera_required": "Bitte eine Kamera auswählen."
   }
  },
  "choices": {
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
    "shutter": "Rollos",
    "meter": "Zähler"
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
   }
  },
  "states": {
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
   "config.shutter": {
    "title": "Covers",
    "fields": {
     "outdoor_temperature": [
      "Outdoor temperature sensor",
      "For the summer day and the temperature condition of every window. Without a sensor the current temperature of the weather entity is used (at least one of both)."
     ],
     "weather": [
      "Weather entity",
      "Its daily forecast decides at the day change whether today is a summer day."
     ],
     "language": [
      "Language of messages",
      "Logbook, last reason and push messages."
     ],
     "notify_services": [
      "Notification services",
      "Get a message when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
     ],
     "workday_entity": [
      "Workday sensor",
      "Optional, for the morning opening by time (e.g. Workday integration, knows public holidays). Without a sensor the weekend days decide."
     ],
     "weekend_days": [
      "Weekend days",
      "Only without a workday sensor: on these days the weekend time of the morning opening applies."
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
      "For the summer day and the temperature condition of every window. Without a sensor the current temperature of the weather entity is used (at least one of both)."
     ],
     "weather": [
      "Weather entity",
      "Its daily forecast decides at the day change whether today is a summer day."
     ],
     "language": [
      "Language of messages",
      "Logbook, last reason and push messages."
     ],
     "notify_services": [
      "Notification services",
      "Get a message when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
     ],
     "workday_entity": [
      "Workday sensor",
      "Optional, for the morning opening by time (e.g. Workday integration, knows public holidays). Without a sensor the weekend days decide."
     ],
     "weekend_days": [
      "Weekend days",
      "Only without a workday sensor: on these days the weekend time of the morning opening applies."
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
      "Vacation is active while one of them is on (e.g. an input_boolean \"vacation\" or a calendar)."
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
     "cover": [
      "Cover",
      "100 % = open, 0 % = closed."
     ],
     "window_sensors": [
      "Window contacts",
      "'on' = open. Window handles with the states open, tilted and closed work as well. Unknown or unavailable counts as open."
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
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window."
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
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window."
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
    "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window."
   },
   "meter": {
    "name_required": "Please enter a name.",
    "camera_required": "Please select a camera."
   }
  },
  "choices": {
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
    "shutter": "Covers",
    "meter": "Meters"
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
   }
  },
  "states": {
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
   }
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
    "100 % = offen, 0 % = zu."
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
    "Logbuch, letzter Grund und Push-Nachrichten."
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
    "Erhalten eine Nachricht, wenn ein offenes Fenster den Sonnenschutz verhindert (nur notify-Dienste, z. B. notify.mobile_app_handy)."
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
    "Für den Sommertag und die Temperaturbedingung jedes Fensters. Ohne Sensor wird die aktuelle Temperatur der Wetter-Entität verwendet (mindestens eins von beiden)."
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
   "vacation": [
    "Urlaubssimulation",
    "An der zufälligen Öffnung und Schließung im Urlaub teilnehmen."
   ],
   "vacation_entities": [
    "Urlaubs-Entitäten",
    "Urlaub ist aktiv, solange eine davon an ist (z. B. ein input_boolean „Urlaub“ oder ein Kalender)."
   ],
   "vacation_evening_start": [
    "Urlaub abends ab",
    "Beginnt den Abend für die Fenster der Simulation und schließt sie zu zufälligen Zeiten. Der normale Abendlauf ruht im Urlaub."
   ],
   "vacation_evening_window": [
    "Zufallszeitraum abends",
    "Jedes Fenster schließt zu einer zufälligen Zeit in diesem Zeitraum."
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
    "Ihre Tagesvorhersage entscheidet beim Tageswechsel, ob heute ein Sommertag ist."
   ],
   "weather_protection": [
    "Wetterschutz für dieses Fenster",
    "Aus = Wind, Regen und Frost fahren oder begrenzen dieses Rollo nie, egal was unten eingetragen ist. Für jedes Fenster einschalten, das mitmachen soll. Mit ausgeschalteter Automatik (global oder für dieses Fenster) gibt es auch keinen Wetterschutz."
   ],
   "weekend_days": [
    "Wochenendtage",
    "Nur ohne Werktag-Sensor: an diesen Tagen gilt die Wochenend-Uhrzeit der Morgenöffnung."
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
    "'on' = offen. Fenstergriffe mit den Zuständen open, tilted und closed gehen auch. Unbekannt oder nicht verfügbar zählt als offen."
   ],
   "window_wind_threshold": [
    "Eigene Windschwelle",
    "Leer = Windschutz ab der Schwelle der Grundeinstellungen. Sonst schützt dieses Fenster schon oder erst ab diesem Wert (Einheit des Windsensors)."
   ],
   "workday_entity": [
    "Werktag-Sensor",
    "Optional, für die Morgenöffnung nach Uhrzeit (z. B. Workday-Integration, berücksichtigt Feiertage). Ohne Sensor entscheiden die Wochenendtage."
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
    "100 % = open, 0 % = closed."
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
    "Logbook, last reason and push messages."
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
    "Get a message when an open window prevents sun protection (notify services only, e.g. notify.mobile_app_phone)."
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
    "For the summer day and the temperature condition of every window. Without a sensor the current temperature of the weather entity is used (at least one of both)."
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
   "vacation": [
    "Vacation simulation",
    "Take part in the random opening and closing during vacation."
   ],
   "vacation_entities": [
    "Vacation entities",
    "Vacation is active while one of them is on (e.g. an input_boolean \"vacation\" or a calendar)."
   ],
   "vacation_evening_start": [
    "Vacation evening from",
    "Starts the evening for the windows in the simulation and closes them at random times. The normal evening run rests during vacation."
   ],
   "vacation_evening_window": [
    "Random period in the evening",
    "Each window closes at a random time within this period."
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
    "Its daily forecast decides at the day change whether today is a summer day."
   ],
   "weather_protection": [
    "Weather protection for this window",
    "Off = wind, rain and frost never move or limit this cover, whatever the positions below say. Turn it on for every window that should take part. With the automatic off (globally or for this window) there is no weather protection either."
   ],
   "weekend_days": [
    "Weekend days",
    "Only without a workday sensor: on these days the weekend time of the morning opening applies."
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
    "'on' = open. Window handles with the states open, tilted and closed work as well. Unknown or unavailable counts as open."
   ],
   "window_wind_threshold": [
    "Own wind threshold",
    "Empty = wind protection from the threshold of the basic settings. Otherwise this window is protected already or only from this value (unit of the wind sensor)."
   ],
   "workday_entity": [
    "Workday sensor",
    "Optional, for the morning opening by time (e.g. Workday integration, knows public holidays). Without a sensor the weekend days decide."
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
   "cover_in_use": "Dieses Rollo wird schon von einem anderen Fenster gesteuert. Bitte ein anderes Rollo wählen oder das andere Fenster ändern."
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
   "cover_in_use": "This cover is already controlled by another window. Choose another cover or change the other window."
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
   "interval_off": [
    "Intervall, wenn die Bedingung aus ist",
    "Nur zusammen mit einer Bedingung."
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
   "interval_off": [
    "Interval while the condition is off",
    "Only used together with a condition."
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
