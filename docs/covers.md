# Rollos

Deutsch | [English](covers.en.md)

Das Modul **Rollos** (bisher Shutter Assistant) steuert Rollos und Raffstores automatisch (die Behanghöhe; Lamellen werden nicht gewendet): Sonnenschutz nach Himmelsrichtung, Abendmodus, Lüftungsposition, Wetterschutz (Wind, Regen, Frost), manuelle Übersteuerung, Morgenöffnung und Urlaubssimulation. Alles wird in der Oberfläche eingestellt, nichts ist fest im Code. Es gibt keine KI und kein Lernen, die Regeln sind nachvollziehbar und jede Fahrt steht mit Grund im Logbuch.

Das Modul ersetzt typischerweise ein Bündel von YAML-Automationen mit vielen Helfern (input_boolean, input_number, timer) für Sonnenschutz, Auto-Hoch, Abendlauf, Nachziehen, Lüften, Übersteuerung und Urlaub (siehe [Umstieg von YAML-Automationen](migration.md)).

## Funktionsweise

Das Modul arbeitet ereignisgesteuert: Es reagiert nur auf Zustandswechsel der eingestellten Entitäten und auf berechnete Zeitpunkte (Sonne betritt oder verlässt einen Bereich, Abendbeginn, Haltezeiten, Ende einer Übersteuerung, Tageswechsel). Es gibt kein Abfragen im Sekundentakt.

### Himmelsrichtungen und Fenster

* Eine **Himmelsrichtung** (Gruppe) hat Azimut von und bis sowie beliebig viele Sonnensensoren (PV-Leistung, Helligkeit in Lux, Strahlung z. B. von Open-Meteo). Eine Himmelsrichtung hat keine Schwellen.
* Ein **Fenster mit Rollo** ist ein Fenster des Hauses (*Haus > Fenster*) mit Rollo, Fensterkontakt(en) und einer Himmelsrichtung. Alle Schwellen, Positionen und Zeiten stehen am Fenster (*Rollos > Fenster*). Ein Fenster ohne Rollo dient nur der Heizung.
* Gehört das Fenster zu einem **Raum**, nimmt es dessen Werte: als Raumtemperatur den Temperatursensor des Raums und als Sollwert das Thermostat des Raums (Heizung), dazu die Klimaanlage des Raums. Ein am Fenster eingetragener Wert hat Vorrang.

### Sonnenschutz

* **Sommertag:** Sonnenschutz gibt es nur an Sommertagen. Beim Tageswechsel (Standard 01:00) wird die Höchsttemperatur der Tagesvorhersage geprüft. Steigt die Außentemperatur tagsüber über die Schwelle, wird es ebenfalls ein Sommertag, aber nur, wenn der Vorhersage-Tiefstwert der kommenden Nacht mindestens 14 °C beträgt (einstellbar). Ein warmer Nachmittag im Frühling oder Herbst mit kühler Nacht löst also keinen Sonnenschutz aus. Ohne Tiefstwert in der Vorhersage gilt der Sommertag wie bisher.
* **Sonnenbedingung je Fenster:** Sommertag UND Außentemperatur über der Schwelle des Fensters (mit Haltezeit) UND jeder Sonnensensor der Himmelsrichtung über seiner Schwelle. Das Ganze muss die Sonnen-Haltezeit lang erfüllt sein und endet sofort. Nach einem Neustart wird sofort ausgewertet, die Haltezeit läuft ab dem Start.
* **Wärmebedarf (optional):** Mit einer **Raumtemperatur** (vom Raum oder am Fenster) wird nur abgesenkt, wenn der Raum zu warm ist: bei einem Thermostat ab Sollwert + 2 K, bei einem Temperatursensor ab 24 °C. Kühlt die gewählte **Klimaanlage**, gilt der Raum als zu warm, der Sonnenschutz entlastet sie. Meldet sie keine Aktion (z. B. Midea), zählt der Modus „Kühlen“ und im Modus „Auto“ eine Raumtemperatur über ihrem Sollwert. Gilt **Heizbedarf**, ist Sonnenwärme erwünscht: Abgesenkt wird dann nur, wenn der Raum trotzdem zu warm ist; Fenster ohne Raumtemperatur bleiben oben. Heizbedarf ist eine eigene Entität (z. B. ein input_boolean „Heizperiode“) oder, ohne sie, der **Heiztag der Heizung** (Option, nur in der Heizperiode). Das Wiederöffnen ist davon unabhängig, es hängt weiter nur am Sonnenstand.
* **Hitzeschutz im Urlaub:** Im Urlaub des Hauses senkt der Sonnenschutz ab, ohne auf Raumtemperatur, Klimaanlage oder Heizbedarf zu warten. Sommertag, Außentemperatur, Sonnensensoren, Haltezeiten und der Sonnenschutz-Schalter des Fensters gelten weiter, im Winter wird also nicht abgesenkt (Option, Standard an).
* **Absenken:** Steht die Sonne im Bereich der Himmelsrichtung und gilt die Sonnenbedingung, fährt das Rollo einmal am Tag auf die Sonnenschutz-Position. Ist es schon weiter zu, wird es nur vorgemerkt und bleibt in Ruhe. Ein offenes Fenster verhindert die Fahrt; dann gibt es einmal am Tag eine Benachrichtigung (pro Fenster abschaltbar), aber nur wenn wirklich eine Fahrt verhindert wurde. Nach dem Schließen des Fensters wird nachgeholt.
* **Auto-Hoch:** Verlässt die Sonne den Bereich, öffnet das Rollo wieder, aber nur wenn es noch auf der Sonnenschutz-Position steht (bis zur Toleranz darüber). Von Hand anders gestellte Rollos bleiben, wie sie sind. Kein Auto-Hoch im Abendmodus, bei Übersteuerung oder Öffnungssperre. Pro Fenster abschaltbar.
* **Manuellen Sonnenschutz erkennen:** Fährt jemand bei Sonne ein Rollo von Hand weit genug herunter (Standard höchstens 25 %), gilt das als Sonnenschutz für heute. Optional zählt auch jede Fahrt genau auf die Sonnenschutz-Position.

### Abend

* **Abendmodus:** beginnt, wenn die Sonne unter die eingestellte Höhe sinkt (Standard -4 °), frühestens um 17:00 und spätestens um 21:00. Er endet um 03:30 oder bei Sonnenaufgang. Werte global oder pro Fenster.
* **Abendlauf:** zu Beginn des Abendmodus schließt jedes Rollo einmal, wenn das Fenster zu ist und keine Übersteuerung aktiv ist (pro Fenster einstellbar: trotz Übersteuerung schließen, z. B. Schlafräume).
* **Abendposition:** pro Fenster das Ziel von Abendlauf, Nachziehen und Urlaub abends. Standard 0 % = zu; z. B. 20 % lässt in warmen Nächten einen Spalt.
* **Nachziehen:** wird am Abend ein Fenster geschlossen, fährt das Rollo zu (ab 16:00, auch bei Übersteuerung).
* **Lüftungsposition:** wird ein Fenster geöffnet und das Rollo ist (fast) zu, fährt es auf die Lüftungsposition (Standard 30 %). Abends nach 3 s, tagsüber nach 60 s, wenn das Fenster dann noch offen ist.

### Fensterkontakte, gekippt und Tür

* **Offen, gekippt, zu:** Fensterkontakte melden „an“ = offen. Fenstergriffe mit den Zuständen `open`, `tilted` und `closed` gehen ebenfalls, zusätzlich gibt es **Kipp-Kontakte** („an“ = gekippt). Für die Rollos zählt unbekannt oder nicht verfügbar als offen (bei Kipp-Kontakten als gekippt).
* **Gekippt:** ein nur gekipptes Fenster verhindert keine Schließfahrt, das Rollo fährt aber höchstens bis zur Lüftungsposition. Wird ein Fenster gekippt, gibt es wie beim Öffnen die Lüftungsposition. Ganz offen verhindert Schließfahrten.
* **Aussperrschutz (Tür):** solange der Kontakt offen meldet, fährt nichts unter die Lüftungsposition, auch nicht mit Fenster-Ausnahme, Nachziehen oder Wetterschutz.

### Wetterschutz

* **Pro Fenster einschalten:** Der Wetterschutz wirkt nur auf Fenster, bei denen **Wetterschutz für dieses Fenster** eingeschaltet ist (Standard aus). Ohne den Schalter fahren oder begrenzen Wind, Regen und Frost das Rollo nie, auch wenn Positionen eingetragen sind (sie bleiben erhalten).
* **Automatik aus = kein Wetterschutz:** Ist die Automatik aus (global oder für das Fenster), fährt auch der Wetterschutz nicht; ein laufender Schutz endet für diese Fenster ohne Fahrt. Wird die Automatik wieder eingeschaltet, während der Schutz noch läuft, fahren die Rollos auf ihre Schutzposition.
* **Wind und Regen:** global ein Windsensor mit Schwelle (in der Einheit des Sensors) und ein Regensensor (an/aus oder eine Menge über einer Schwelle). Pro Fenster eine **Position bei Wind** und **bei Regen**, leer = nicht betroffen (z. B. Raffstores bei Wind auf 100 %, ein Dachfenster bei Regen auf 0 %). Eine **eigene Windschwelle** am Fenster ersetzt für dieses Fenster die globale Schwelle (z. B. ein Balkonrollo schon ab 50 km/h, die übrigen erst ab 75 km/h); sie hat eine eigene Freigabezeit, und der Binärsensor Windschutz ist an, solange irgendein Fenster geschützt wird (Attribut `windows`). Der Schutz beginnt sofort und fährt die betroffenen Rollos einmal auf ihre Position, **auch bei Übersteuerung** (nicht im Neustart-Schutz, danach nachgeholt). Wer ein Rollo während des Schutzes von Hand verfährt, behält diese Position: Ein Neustart des Moduls fährt bereits geschützte Rollos nicht erneut. Ein Rollo, das schon **weiter zu** ist als seine Schutzposition, gilt als geschützt und wird nicht hochgefahren (Option **Weiter geschlossen gilt als geschützt**, Standard an; nicht bei 100 %, Raffstores einfahren läuft immer). Wind geht vor Regen. Ein offenes Fenster verhindert nur Schließfahrten; sie werden nachgeholt, sobald es zu ist.
* **Solange der Schutz läuft,** ruhen alle anderen Regeln für das Fenster (Status „Wetterschutz“). Er endet erst, wenn der Wert die **Freigabezeit** (Standard 15 min) lang wieder im sicheren Bereich war. Ein nicht verfügbarer Sensor beendet nie einen Schutz. Danach entscheidet die Automatik neu (Sonnenschutz, Abendlauf); die alte Position wird nicht wiederhergestellt.
* **Frost:** Fenster mit einer **tiefsten Position bei Frost** (z. B. 5 %) schließen bei einer Außentemperatur bis zur Frostschwelle (Standard 1 °C) nur bis dorthin, damit das Rollo nicht anfriert. Das gilt für alle automatischen Fahrten und Dienste, nicht für den Wind- und Regenschutz.
* **Anzeige:** Solange Wind- oder Regenschutz läuft, zeigen die Übersicht im Panel und die Karte den aktuellen Wert des auslösenden Sensors (z. B. „Windschutz 62 km/h“). Die Binärsensoren Wind- und Regenschutz nennen den Sensor im Attribut `sensor`.
* Beginn und Ende stehen im Logbuch, dazu das Ereignis `house_assistant_protection` mit `kind` (wind, rain, frost) und `active`.

### Zuverlässigkeit

* **Abstand zwischen Fahrbefehlen** (Erweitert, Standard 0 = alle gleichzeitig): mehrere Rollos fahren nacheinander, z. B. alle 2 s, gegen Funkkollisionen.
* **Position prüfen** (Erweitert, Standard nach 90 s): hat ein Rollo sein Ziel bis dahin nicht erreicht (± 5 %), wird der Befehl einmal wiederholt. Klappt das auch nicht, gibt es eine Benachrichtigung, einen Logbuch-Eintrag und das Ereignis `house_assistant_cover_failed`. Fährt das Rollo bei der Prüfung noch, wird einmal später nachgesehen. Eine Bewegung von Hand beendet die Prüfung.

### Übersteuerung

Jede manuelle Bewegung (am Taster, in der App, nicht durch House Assistant und nicht durch andere Automationen oder Skripte) startet eine Übersteuerung für das Fenster, Standard 60 min. Jede weitere Bewegung startet sie neu. Optional endet sie zusätzlich bei Sonnenaufgang, mit Dauer 0 nur bei Sonnenaufgang. Das Modul merkt sich seine eigenen Fahrten, späte Positionsmeldungen werden deshalb nicht fälschlich als manuell gewertet.

In den Einstellungen (Panel *Rollos > Allgemein*, Karte **Manuelle Übersteuerung**) lässt sich wählen, wann sie beginnt: **nur wenn das Rollo wirklich fährt** (Standard; die Position ändert sich um mehr als 2 %, bei Rollos ohne Position steht es danach anders) oder **bei jedem Befehl von Hand, auch ohne Fahrt**. Mit dem Standard startet z. B. „Alexa, alle Rollos auf“ keine Übersteuerung bei Rollos, die schon offen sind.

### Zusatzbedingungen statt Sonderregeln

* **Öffnungssperre:** solange eine Entität nicht in einem der Freigabe-Zustände ist, wird nicht automatisch geöffnet (Auto-Hoch, Lüften, Urlaub morgens, Morgenöffnung). Beispiel: Fernseher an.
* **Schließ-Auslöser:** wird eine der Entitäten aktiv (Ein-Verzögerung), schließt das Rollo einmal pro Aktiv-Zyklus, wenn es weiter offen ist als die Mindestposition und das Fenster zu ist. Ist das Fenster offen, wird geschlossen, sobald es zu ist. Der Zyklus endet, wenn alle Entitäten inaktiv sind (Aus-Verzögerung). Beispiel: Fernseher einschalten schließt das Wohnzimmer-Rollo.
* **Fenster-Ausnahme:** solange eine Entität verfügbar ist, verhindert ein offenes Fenster keine Schließfahrt und es gibt keine Benachrichtigung. Beispiel: Klimaanlage mit Schlauch durch die Balkontür.

### Morgenöffnung (pro Fenster, Standard aus)

Modi: feste Uhrzeit (Werktag sowie Wochenende und Feiertag über den Werktag-Sensor des Hauses), Sonnenaufgang oder Sonnenhöhe mit Versatz, Helligkeit der Himmelsrichtung über einer Schwelle mit Haltezeit, Auslöser-Entität (Zeitstempel wie der nächste Wecker des Handys, oder eine Entität, die angeht). Dazu ein Zeitfenster frühestens und spätestens, eine Zielposition (offen oder Teilöffnung) und optional direkt die Sonnenschutz-Position, wenn die Sonnenbedingung gilt. Nicht bei Übersteuerung, Öffnungssperre oder einem seit dem Abend von Hand verstellten Rollo.

### Urlaubssimulation

Im Urlaub des Hauses (siehe [README](../README.md#urlaub)) ruht der normale Abendlauf. Stattdessen öffnen die teilnehmenden Fenster morgens zu einer zufälligen Zeit (Standard 07:00 bis 08:00) auf eine zufällige Position (60 bis 100 %) und schließen abends zufällig (19:00 bis 20:30). Sonnenschutz (mit Hitzeschutz) und Lüften laufen weiter.

### Neustart-Schutz

Nach dem Start von Home Assistant gibt es einige Minuten (Standard 5) keine Fahrten. Danach wird ausgewertet und der Abendlauf für noch nicht geschlossene Fenster nachgeholt (nur ab 12:00). Übersteuerungen, Tagesmarker, ein laufender Wetterschutz und die Automatik-Schalter bleiben über Neustarts erhalten.

### Temperatur-Einheiten

Alle Temperaturen der Rollos (Schwellen, Vorhersage, Raum) gelten in der Einheit des Einheitensystems von Home Assistant. Bei °F werden die Standardwerte umgerechnet (Sommertag ab 73 °F, Nacht ab 57 °F, Außentemperatur ab 66 °F, Raum ab 75 °F, Sollwert plus 4 °F). Wird das Einheitensystem später umgestellt, die Schwellen bitte von Hand anpassen. Der Sollwert eines Thermostats der Heizung wird umgerechnet.

## Panel

Im Panel **House Assistant**, Bereich **Rollos** (nur für Administratoren):

* **Übersicht:** Automatik an/aus, Sommertag (Vorhersage und Schwelle), Beginn des Abendmodus, Urlaub, Wetterschutz und Neustart-Schutz. Dazu der **Sonnenkompass** mit dem aktuellen Sonnenstand und den Bereichen der Himmelsrichtungen, Hinweise (z. B. eingestellte Entitäten, die es nicht gibt, oder eine gelöschte Himmelsrichtung) und alle Fenster mit Status, Position, Fensterkontakt (offen, gekippt, zu), nächster Aktion und letztem Grund. Eine laufende Übersteuerung lässt sich direkt **beenden**. Der **Sonnenbedingung-Check** zeigt je Fenster jede Teilbedingung mit aktuellem Wert und Schwelle: Sommertag (mit Nacht-Tiefstwert, wenn die Außentemperatur ihn ausgelöst hat), Außentemperatur, jeder Sonnensensor, Raum, Klimaanlage, Heizbedarf, Hitzeschutz im Urlaub, Haltezeit (mit Uhrzeit, ab wann sie erfüllt ist) und ob die Sonne im Bereich steht.
* **Fenster:** alle Fenster mit Rollo als Tabelle, anklicken zum Bearbeiten. Der Editor zeigt die Einstellungen nach Themen in Karten (Fenster, Sonnenschutz, Manuellen Sonnenschutz erkennen, Abend, Übersteuerung, Lüften & Urlaub, Morgenöffnung, Zusatzbedingungen, Wetterschutz & Tür). Es erscheinen nur die Felder, die gerade gelten: Schwellen nur für die Sensortypen der Himmelsrichtung, eigene Abendzeiten nur wenn eingeschaltet, bei der Morgenöffnung nur die Felder des gewählten Modus. **Duplizieren** legt ein neues Fenster mit denselben Einstellungen an, nur Rollo und Fensterkontakte werden neu gewählt.
* **Gruppen:** Himmelsrichtungen mit den aktuellen Werten ihrer Sensoren und den Fenstern, die sie verwenden. Beim Bearbeiten zeigt der Kompass den Bereich sofort an.
* **Haus im Kompass:** Sind Länge der Vorderseite, Tiefe und Ausrichtung des Hauses eingetragen (*Haus > Allgemein*), erscheint das Haus maßstabsgetreu gedreht in der Mitte des Kompasses. Einer Himmelsrichtung lässt sich dann eine **Wand** zuordnen: der Azimut-Bereich wird auf die Ausrichtung der Wand ± 90° gesetzt (danach frei änderbar) und die Wand erscheint in ihrer Farbe. **Fenster** erscheinen als Markierung an ihrer Wand (eigene Wand oder die der Himmelsrichtung), live eingefärbt nach Sonnenschutz, Übersteuerung und Abend, hohl bei offenem Fenster; ein Klick öffnet das Fenster. Mit **Position an der Wand** (1, 2, 3 …) lässt sich die Reihenfolge der Fenster einer Wand festlegen: 1 ist ganz links, von innen durch die Wand nach draußen geschaut; Fenster ohne Zahl kommen danach. Wand und Position nutzt auch die Heizung für Querlüften und Luftzug.
* **Allgemein** und **Abend & Urlaub:** die Einstellungen in Karten, jede Karte wird für sich gespeichert.

Die Werte werden genauso geprüft wie in den Dialogen (gleiche Bereiche, Einheiten und Regeln).

## Einstellungen

Außentemperatur, Wetter, Sprache der Meldungen, Benachrichtigungsdienste, Werktag-Sensor und Wochenendtage stehen in den **Einstellungen des Hauses** (siehe [README](../README.md#einstellungen-des-hauses)); die gleichnamigen Felder der Rollos gelten nur, solange dort nichts eingetragen ist.

| Option (*Einstellungen > Rollos*) | Standard | Bedeutung |
|---|---|---|
| Sommertag ab | 23 °C | Höchsttemperatur der Vorhersage |
| Später Sommertag nur bei Nacht ab | 14 °C | Tiefstwert der kommenden Nacht, wenn erst die Außentemperatur den Sommertag auslöst |
| Heizbedarf | | optional, z. B. ein `input_boolean` „Heizperiode“; an = Sonnenwärme erwünscht |
| Heiztag der Heizung | an | ohne eigenen Heizbedarf der Heiztag des Heizungsmoduls (nur in der Heizperiode) |
| Tageswechsel | 01:00 | Vorhersage prüfen, Tagesmarker zurücksetzen |
| Vorhersage-Art | automatisch | täglich, zweimal täglich oder stündlich; automatisch nimmt die erste, die die Wetter-Entität kann |
| Abendmodus frühestens, Sonnenhöhe, spätestens | 17:00, -4 °, 21:00 | |
| Ende der Nacht | 03:30 | |
| Nachziehen ab | 16:00 | |
| Urlaub morgens ab, Zufallszeitraum | 07:00, 60 min | |
| Öffnungsposition von, bis | 60 %, 100 % | |
| Urlaub abends ab, Zufallszeitraum | 19:00, 90 min | |
| Hitzeschutz im Urlaub | an | Sonnenschutz ohne Raum, Klimaanlage und Heizbedarf |
| Übersteuerung beginnt | nur bei echter Fahrt | oder bei jedem Befehl von Hand, auch ohne Fahrt |
| Windsensor, Windschutz ab | , 50 | Einheit des Sensors (z. B. km/h) |
| Regensensor, Regenschutz über | , 0 | an/aus oder eine Menge (z. B. mm/h) |
| Frost ab (höchstens) | 1 °C | Außentemperatur, nur für Fenster mit Frostposition |
| Freigabe nach | 15 min | Wetterschutz endet erst nach dieser Zeit im sicheren Bereich |
| Neustart-Schutz | 5 min | |
| Abendlauf nachholen ab | 12:00 | |
| Fenster gilt als geschlossen nach (Erweitert) | 5 s | Entprellung der Fensterkontakte |
| Abstand zwischen Fahrbefehlen (Erweitert) | 0 s | 0 = alle gleichzeitig |
| Position prüfen nach (Erweitert) | 90 s | einmal wiederholen, dann melden; 0 = aus |

### Himmelsrichtungen

**Gruppe hinzufügen**: Name, Azimut von und bis (90 ° = Ost, 180 ° = Süd, 270 ° = West; die Grenzen selbst zählen nicht), Strahlungs-, PV- und Helligkeitssensoren, Wand.

### Fenster

**Fenster hinzufügen** (im Panel unter *Haus > Fenster* oder *Rollos > Fenster*, oder unter der Integration):

1. **Fenster:** Name, Raum, Größe, Rollo, Fensterkontakte (auch Fenstergriffe), Kipp-Kontakte, Himmelsrichtung (ohne sie kein Sonnenschutz), Wand und Position an der Wand. Ohne Rollo endet der Dialog hier.
2. **Sonnenschutz:** Schwellen für die Sensortypen der Himmelsrichtung, Außentemperatur mindestens (19 °C), Haltezeiten Temperatur (10 min) und Sonne (5 min), Raumtemperatur (leer = die des Raums; Thermostat: zu warm ab Sollwert + 2 K, Sensor: ab 24 °C), Klimaanlage (leer = die des Raums), Sonnenschutz-Position (10 %), Toleranz für Auto-Hoch (5 %), Auto-Hoch, Benachrichtigung bei offenem Fenster, manueller Sonnenschutz bis (25 %), Erkennungszeitraum (5 min), Nachlauf (5 min), Fahrt auf Sonnenschutz-Position zählt.
3. **Verhalten:** Übersteuerung (60 min, Sonnenaufgang, Abend- und Urlaubsfahrten trotz Übersteuerung), Zusatzbedingungen, Abend (Abendlauf, Abendposition 0 %, Nachziehen, eigene Abendzeiten), Lüften (30 %, gilt als geschlossen bis 5 %, 3 s abends, 60 s tagsüber), Urlaubssimulation, Wetterschutz & Tür (Wetterschutz für dieses Fenster, Position bei Wind, eigene Windschwelle, Position bei Regen, tiefste Position bei Frost, weiter geschlossen gilt als geschützt, Aussperrschutz).
4. **Morgenöffnung:** an oder aus, Modus und Zeitfenster, danach die Einstellungen des Modus.

Positionen: 100 % = offen, 0 % = zu. Ein Rollo und ein Kontakt gehören zu genau einem Fenster.

## Entitäten

Gerät „Rollos“:

* Schalter **Automatik** (aus = keine automatische Fahrt; bleibt über Neustarts erhalten)
* Binärsensoren **Sommertag** und **Abendmodus**
* Binärsensoren **Windschutz**, **Regenschutz** und **Frostschutz** (nur wenn eingerichtet, mit dem Ende der Freigabezeit)
* Sensor **Vorhersage Höchsttemperatur**

Je Fenster mit Rollo (eigenes Gerät):

* Sensor **Status** (Wetterschutz, Automatik aus, Neustart-Schutz, Manuelle Übersteuerung, Abends geschlossen, Sonnenschutz, Urlaubssimulation, Bereit)
* Sensor **Letzter Grund** (Text, Code, Position, Zeit)
* Sensor **Nächste Aktion** (Zeitpunkt, Attribut `action`: Abendlauf, Morgenöffnung, Ende der Übersteuerung, Sonne kommt in oder verlässt den Bereich, Wetterschutz kann enden)
* Schalter **Automatik** (nur dieses Fenster; aus = auch kein Wetterschutz) und **Sonnenschutz** (aus = bei Sonne nicht absenken; schon abgesenkte Rollos öffnen wieder wie gewohnt), beide bleiben über Neustarts erhalten
* Binärsensoren **Manuelle Übersteuerung** (mit Ende), **Sonnenbedingung** (mit Teilbedingungen), **Sonnenschutz heute**, **Abends geschlossen**

Für Kontroll-Karten im Dashboard liefern **Sonnenbedingung** (Schwellen, Sensoren, Azimut-Bereich, Haltezeiten und wann sie ablaufen) und **Status** (Rollo, Fensterkontakte, Abendbeginn, Übersteuerung bis) alle Werte als Attribute. **Abendmodus** hat Beginn und Ende des aktuellen oder nächsten Abends, **Automatik** das Ende eines laufenden Neustart-Schutzes. „Sonnenbedingung“, „Letzter Grund“ und „Vorhersage Höchsttemperatur“ sind Diagnose-Entitäten; die Attribute von „Sonnenbedingung“ und „Status“ werden nicht im Verlauf gespeichert (sie ändern sich oft).

Jede Fahrt und jede Übersteuerung steht mit Grund im **Logbuch**.

## Dienste und Ereignisse

Alle Dienste wirken auf die Rollos konfigurierter Fenster (`entity_id`, auch eine Entität des Fensters); ohne `entity_id` auf alle Fenster. Sie starten keine Übersteuerung.

| Dienst | Wirkung |
|---|---|
| `house_assistant.move_cover` | `action`: `open`, `close`, `evening` (Abendposition, als „abends geschlossen“ vorgemerkt), `sun_protection` (Sonnenschutz-Position, als Sonnenschutz vorgemerkt, öffnet später per Auto-Hoch), `ventilation` oder `position` mit `position`. Frost- und Aussperrschutz gelten weiter. |
| `house_assistant.start_cover_override` | Übersteuerung wie eine Fahrt von Hand; `duration` in Minuten (leer = Dauer des Fensters, 0 = bis Sonnenaufgang) |
| `house_assistant.end_cover_override` | laufende Übersteuerung beenden |
| `house_assistant.resume_cover` | Übersteuerung beenden und sofort entscheiden lassen (Sonnenschutz, Abendlauf) |

```yaml
# Beispiel: bei Gewitterwarnung alle Rollos im Erdgeschoss auf die Abendposition
action: house_assistant.move_cover
data:
  entity_id: [cover.wohnzimmer, cover.kueche]
  action: evening
```

Ereignisse für eigene Automationen:

* `house_assistant_cover_moved`: jeder Fahrbefehl mit `window`, `window_id`, `entity_id`, `position` und `reason` (z. B. `sun_lower`, `evening_close`, `protection_wind`, `service`)
* `house_assistant_cover_failed`: Ziel auch nach der Wiederholung nicht erreicht, mit `position` und `current_position`
* `house_assistant_protection`: Wetterschutz beginnt oder endet, mit `kind` und `active`

## Dashboard-Karten

Für alle Nutzer (auch ohne Admin-Rechte); die Karten werden automatisch geladen (siehe [README](../README.md#dashboard-karten)).

**Rollo-Karte** (`custom:house-assistant-cover-card`): alle Fenster mit Status, Position, Fensterkontakt, nächster Aktion und laufender Übersteuerung (mit „Automatik fortsetzen“), Knöpfe für Auf, Stopp und Ab (wirken wie ein Taster, starten also eine Übersteuerung), aktiver Wetterschutz und ein kleiner Sonnenkompass. Einstellen lässt sich über die Karte nichts.

```yaml
type: custom:house-assistant-cover-card
title: Rollos            # optional
windows: [Wohnzimmer]    # optional: Namen oder IDs, Standard alle
compass: true            # optional: Sonnenkompass anzeigen
```

**Kachel** (`custom:house-assistant-tile`, 3 × 1): ein Rollo oder ein Fensterkontakt. Oben steht der Name, darunter Symbol und Zustand (Öffnungsgrad bzw. offen, gekippt, zu). Der Rollo fährt als Lamellen von oben in die Kachel. Ein offenes oder gekipptes Fenster färbt die Kachel. Antippen öffnet den Info-Dialog.

```yaml
type: custom:house-assistant-tile
entity: cover.wohnzimmer   # Rollo, binary_sensor (an = offen) oder Fenstergriff (open/tilted/closed)
name: Wohnzimmer           # optional
icon: mdi:blinds           # optional
```

**Fensterkachel** (`custom:house-assistant-window-tile`, 6 × 1): Fenster und Rollo zusammen: oben der Name, darunter links das Fenster (offen, gekippt, zu) und rechts der Rollo mit Öffnungsgrad. Ohne Fensterkontakt nur der Rollo. Antippen des Fensters öffnet den Fensterkontakt (ohne Kontakt den Status des Fensters), Antippen des Rollos den Rollo, der Rest der Kachel ebenfalls den Rollo.

```yaml
type: custom:house-assistant-window-tile
window: Wohnzimmer         # Fenster des Hauses (Name oder ID), oder selbst:
cover: cover.wohnzimmer
contact: binary_sensor.wohnzimmerfenster
tilt: binary_sensor.wohnzimmerfenster_gekippt   # optional, an = gekippt
```

Farben (beide Kacheln, optional): `color_cover`, `color_closed`, `color_open` und `color_tilted`, jeweils ein Farbname des Themes (`purple`, `orange`, `teal`, …) oder eine CSS-Farbe (`"#00897b"`). Alles lässt sich auch im Karten-Editor einstellen.

### Eigene Dashboard-Karten

Die Attribute der Entitäten lassen sich in eigenen Karten verwenden, zum Beispiel:

```yaml
type: entities
title: Wohnzimmer
entities:
  - entity: sensor.wohnzimmer_status
  - entity: binary_sensor.wohnzimmer_sonnenbedingung
    secondary_info: last-changed
  - type: attribute
    entity: sensor.wohnzimmer_status
    attribute: evening_start
    name: Abend ab
  - type: attribute
    entity: binary_sensor.wohnzimmer_sonnenbedingung
    attribute: condition_on_at
    name: Sonnenbedingung erfüllt ab
```

## Fehlerbehebung

* **Kein Sonnenschutz:** im Panel den **Sonnenbedingung-Check** des Fensters öffnen. Jede Teilbedingung zeigt Wert und Schwelle. Häufige Gründe: kein Sommertag (Vorhersage unter der Schwelle), keine Himmelsrichtung, ein Sonnensensor unter der Schwelle, die Haltezeit läuft noch, offenes Fenster, aktive Übersteuerung.
* **Übersteuerung startet ungewollt:** „Nur wenn das Rollo wirklich fährt“ wählen (Panel *Rollos > Allgemein*, Karte **Manuelle Übersteuerung**). Fahrten anderer Automationen und Skripte zählen nie.
* **Keine Vorhersage:** Panel und Reparaturen zeigen einen Hinweis, wenn die Wetter-Entität keine Vorhersage liefert. Vorhersage-Art oder eine andere Wetter-Entität wählen.
* **Rollo fährt nicht auf eine Position:** Rollos ohne Positionsunterstützung können nur auf und zu (im Log steht eine Warnung).
* **Meldung „Rollo hat … % nicht erreicht“:** das Rollo meldet seine Position nicht oder ungenau. „Position prüfen nach“ (Erweitert) verlängern oder auf 0 stellen.
* **Rollo bleibt oben bzw. auf der Lüftungsposition:** Wetterschutz aktiv (Status „Wetterschutz“), Fenster gekippt, Aussperrschutz einer offenen Tür oder Frost. Der letzte Grund und die Übersicht zeigen, was gilt.
