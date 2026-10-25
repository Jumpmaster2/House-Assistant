# Zähler

Deutsch | [English](meters.en.md)

Das Modul **Zähler** (bisher Zähler-Ablesung) liest Zähler (Wärme, Wasser, Gas, Strom) mit einer Kamera ab. Eine günstige ESP32-CAM mit ESPHome fotografiert die Anzeige, eine KI-Aufgabe von Home Assistant (`ai_task`, z. B. Anthropic Claude, OpenAI, Google oder ein lokales Modell mit Bildunterstützung) liest den Zählerstand. Ein Mehrheitsentscheid über mehrere Bilder und eine Plausibilitätsprüfung sorgen dafür, dass Fehllesungen nicht in der Statistik landen.

Alles wird im Panel **House Assistant**, Bereich **Zähler**, eingerichtet: Zähler anlegen, Kamera und Licht wählen, mit einem Testbild die Helligkeit ausprobieren, Intervall und Prüfungen einstellen. Automationen, Skripte und Helfer sind nicht nötig.

## Funktionsweise

### Ein Bild aufnehmen

1. Das Licht (z. B. die Blitz-LED der ESP32-CAM) wird mit der eingestellten Helligkeit eingeschaltet, einmal für alle Bilder einer Ablesung.
2. Nach der Vorlaufzeit werden einige Bilder verworfen. Die ESP32-CAM liefert nach einer Pause sonst noch ein altes Bild ohne Licht aus ihrem Puffer.
3. Die Bilder werden aufgenommen, danach geht das Licht aus. War es vorher schon an (z. B. für das Livebild), bleibt es an.
4. Optional wird das Bild um einen beliebigen Winkel (bis ±180°) gedreht, auf den **Bildausschnitt** zugeschnitten und in der **Belichtung** angepasst. Das ist bei Weitwinkel-Kameras wichtig, auf denen die Anzeige sonst nur ein kleiner Streifen ist. Im Panel dreht man das letzte Bild gerade und zieht den Ausschnitt mit Maus oder Finger darüber auf. Mit **Bild aufbereiten** wird das Bild außerdem grau, gleichmäßig ausgeleuchtet und kontrastreicher, was bei einem hellen Lichtfleck auf dem Displayglas oder blassen LCD-Ziffern hilft. Beim Einrichten der Kamera hilft das **Livebild** dort (auf Wunsch mit eingeschaltetem Licht), ohne jedes Mal ein Testbild aufzunehmen.
5. Das Bild, das die KI bekommt, liegt danach unter `/media/house_assistant/<Zähler-ID>/letztes.jpg` (das unbeschnittene als `original.jpg`) und ist als Kamera-Entität **Letztes Bild** sichtbar.

### Externe Beleuchtung

Reicht das Licht der Kamera nicht oder spiegelt es, kann pro Zähler zusätzlich eine **externe Beleuchtung** eingeschaltet werden, z. B. LED-Module. Das geht mit jeder `light`- oder `switch`-Entität, der Abschnitt steht im Zähler-Editor unter **Externe Beleuchtung**. Ohne Entität verhält sich alles wie bisher.

| Option | Key | Standard | Bedeutung |
| --- | --- | --- | --- |
| Externe Beleuchtung | `external_light` | leer | `light`- oder `switch`-Entität; leer = keine externe Beleuchtung |
| Modus | `external_light_mode` | Nur während der Aufnahme (`capture`) | `capture`: vor den Bildern ein, danach aus. Dauerlicht (`permanent`): wird nur eingeschaltet, falls es aus ist, und nie ausgeschaltet |
| Helligkeit | `external_light_brightness` | 100 % | Nur bei einer dimmbaren `light`-Entität; ein Schalter wird nur ein- und ausgeschaltet |
| Vorlaufzeit | `external_light_lead_time` | 2 s | Wartezeit (0 bis 30 s) nach dem Einschalten, bevor das Licht der Kamera eingeschaltet und aufgenommen wird |
| Danach ausschalten | `external_light_turn_off` | ja | Nur im Modus „Nur während der Aufnahme“ |

Ablauf einer Ablesung oder eines Testbilds im Modus „Nur während der Aufnahme“: externe Beleuchtung ein (bei `light` mit der eingestellten Helligkeit), Vorlaufzeit abwarten, dann wie oben Licht der Kamera, Bilder und Auswertung durch die KI, danach externe Beleuchtung aus. Das Ausschalten passiert auch, wenn Aufnahme oder Auswertung fehlschlagen. Ist die Entität nicht verfügbar oder schlägt das Schalten fehl, steht eine Warnung im Log und es wird trotzdem abgelesen.

### Ablesen mit Mehrheitsentscheid

* Die KI bekommt das Bild und eine Anweisung, die sich aus Zählerart, Einheit, Nachkommastellen und deinen **Hinweisen** zusammensetzt (im Editor unter "Anweisung an die KI" einsehbar). Sie antwortet nur mit der Zahl oder mit "unlesbar".
* Mit **Bearbeiten** lässt sich die ganze Anweisung frei ändern; die automatisch erzeugte dient als Vorlage. Eine eigene Anweisung ersetzt dann die erzeugte vollständig, Einheit, Nachkommastellen und Hinweise werden nicht mehr eingesetzt. **Standard wiederherstellen** kehrt zur erzeugten Anweisung zurück.
* Es werden so lange Bilder gelesen, bis ein Wert **zweimal gleich** gelesen wurde, höchstens die eingestellte Zahl an Bildern (Standard 4). Gibt es keinen solchen Wert, ist die Ablesung "unlesbar".
* Der allererste Wert eines Zählers wird zusätzlich durch weitere Bilder (Standard 2) bestätigt, weil es noch nichts gibt, womit er sich vergleichen ließe.
* Mit **Helligkeit 2. Bild** (0 = aus) wird pro Versuch ein zweites Bild mit anderer Lichthelligkeit aufgenommen (`letztes_2.jpg`), und die KI bekommt beide.
* Mit **Letzte Stände an die KI** bekommt die KI die letzten 3 gültigen Zählerstände als Hinweis, um eine unklare Ziffer plausibel zu entscheiden. Sie soll trotzdem nur ablesen, was im Bild steht; Mehrheitsentscheid und Plausibilitätsprüfung bleiben unverändert. Ein von Hand gesetzter Stand ersetzt die bisherigen.
* Steht in der Antwort der KI außer der Zahl nur eine Einheit oder eine Bezeichnung ("1234,5 m³", "Zählerstand: 1234.5"), zählt die Zahl.

### Plausibilitätsprüfung

* **Anstieg zu groß:** Steigt der Wert seit der letzten gültigen Ablesung um mehr als *größter Anstieg pro Stunde × Stunden* (mindestens eine halbe Stunde, ohne vorherigen Wert zwei Stunden), wird er verworfen.
* **Kleiner als zuvor:** Ein kleinerer Wert wird nur übernommen, wenn er höchstens um die *größte Korrektur* kleiner ist und weitere Bilder (Standard 2) ihn alle bestätigen. Dann gilt er als "korrigiert" (eine frühere Fehllesung wird damit berichtigt). Die Heizung wertet eine solche Korrektur nicht als Zählertausch.
* Im Panel lässt sich ein verworfener, aber richtig gelesener Wert mit einem Klick übernehmen. Das Bild wird unter `verworfen/` aufbewahrt (die letzten 20) und ist im Panel auf der Zählerkarte unter **Verworfene Bilder** zu sehen.
* Der Zählerstand-Sensor hat die Zustandsklasse `total` (nicht `total_increasing`), damit eine Korrektur nach unten in der Statistik nicht als Zählertausch zählt.

### Benachrichtigungen

Verworfene, korrigierte und fehlgeschlagene Ablesungen können eine Benachrichtigung in Home Assistant erzeugen. Für jeden Zähler lässt sich im Abschnitt **Benachrichtigungen** einstellen, ab dem wievielten Mal in Folge sie erscheint (0 = nie, 1 = sofort):

| Fall | Standard |
| --- | --- |
| Kleiner als zuvor | 1 |
| Anstieg zu groß | 1 |
| Korrigiert | 1 |
| Unlesbar oder Fehler (Kamera/KI nicht erreichbar) | 3 |

* Eine gültige Ablesung setzt die Zählung zurück und entfernt die Benachrichtigung.
* Ein anderer Fall beginnt die Zählung neu (z. B. "Anstieg zu groß" nach zweimal "kleiner als zuvor"). Unlesbare Ablesungen zeigen keinen Wert und unterbrechen die Zählung der anderen Fälle nicht; sie werden für sich gezählt.
* Der Schalter in den Einstellungen der Zähler schaltet alle diese Benachrichtigungen ab.

### Leckwarnung im Urlaub

Im Urlaub des Hauses (siehe [README](../README.md#urlaub)) warnt ein Zähler, wenn etwas läuft, obwohl niemand zu Hause ist. Abschnitt **Urlaub** im Zähler-Editor:

| Option | Standard | Bedeutung |
| --- | --- | --- |
| Im Urlaub warnen | an beim Wasserzähler, sonst aus | |
| Menge | Wasser 20 L, sonst 0 | Verbrauch seit Urlaubsbeginn in Litern (Wasser, Gas) bzw. kWh (Strom); 0 = aus |
| Mittlerer Durchfluss bzw. Leistung | Wasser 5 L/h, sonst 0 | Mittel seit Urlaubsbeginn in L/h bzw. kW, frühestens nach einer Stunde; bei Gas und Strom die Grundlast eintragen; 0 = aus |

Gezählt wird ab der letzten gültigen Ablesung vor dem Urlaub. Überschreitet ein Wert seine Grenze, gibt es eine Meldung an die Benachrichtigungsdienste des Hauses (ohne sie eine Benachrichtigung in Home Assistant), einen Logbuch-Eintrag, das Ereignis `house_assistant_vacation_alert` (mit `meter_id`, `meter`, `case`, `used`, `hours`, `limit`, `unit`) und das Attribut `vacation_alerts` am Zählerstand, einmal je Urlaub und Fall. Der Wärmezähler ist ausgenommen.

### Zeitplan

* Jeder Zähler wird automatisch im eingestellten **Intervall** abgelesen (Prüfung alle 5 Minuten). Nach einer unlesbaren oder fehlgeschlagenen Ablesung kommt der nächste Versuch schon nach 15 Minuten.
* Optional eine **Bedingung**: Solange diese Entität `off` ist, gilt ein zweites Intervall. Mit der Option **Tage ohne Heizen** gilt das zweite Intervall auch an Tagen, an denen das Modul Heizung nicht heizt (unbekannt zählt wie ein Heiztag). Beispiel: an Heiztagen alle 30 Minuten, sonst alle 6 Stunden.
* Der Schalter **Automatik** stoppt die automatischen Ablesungen, die Schaltfläche **Jetzt ablesen** liest sofort ab.

## Entitäten je Zähler

| Entität | Bedeutung |
| --- | --- |
| Zählerstand | Letzter gültiger Wert (Energie, Wasser oder Gas, für das Energie-Dashboard geeignet). Attribute `last_valid_reading` und im Urlaub `vacation_alerts`. |
| Mittlere Leistung / Mittlerer Durchfluss | Verbrauch seit der vorherigen gültigen Ablesung (kW bei Energie, L/h bei Volumen). Wird bei einer Korrektur zurückgesetzt. |
| Status | Ergebnis der letzten Ablesung: gültig, korrigiert, unlesbar, kleiner als zuvor, Anstieg zu groß, Kamera- oder KI-Fehler, von Hand gesetzt. Attribut `readings` mit allen Einzellesungen. |
| Letzte Ablesung / Nächste Ablesung | Zeitpunkte (Diagnose). |
| Letztes Bild | Kamera-Entität mit dem zuletzt aufgenommenen Bild. |
| Jetzt ablesen / Testbild | Schaltflächen. Das Testbild wird nur aufgenommen, nicht gelesen (zum Ausprobieren von Ausrichtung, Schärfe und Helligkeit). |
| Automatik | Automatische Ablesungen an oder aus. |

## Dienste und Ereignisse

* `house_assistant.read_meter`: Zähler der angegebenen Entitäten jetzt ablesen.
* `house_assistant.set_meter_reading`: Zählerstand von Hand setzen (z. B. nach einer Fehllesung oder beim Start). Die nächsten Ablesungen werden gegen diesen Wert geprüft. Auch im Panel unter "Zählerstand von Hand setzen".
* Ereignis `house_assistant_meter_reading` nach jeder Ablesung mit `meter_id`, `meter`, `valid`, `status`, `value`, `previous`, `readings`, `unit`.

## Einrichten

1. Das Modul **Zähler** einschalten (bei der Einrichtung oder unter *Einstellungen > Module*) und die KI-Aufgabe wählen.
2. Im Panel unter **Zähler** einen Zähler hinzufügen: Name, Zählerart, Kamera, Licht. Speichern, dann mit **Testbild** Ausrichtung und Helligkeit prüfen.
3. Einmal **Jetzt ablesen** und das Ergebnis prüfen. Stimmt etwas nicht, in den **Hinweisen** beschreiben, was die KI falsch liest (z. B. "Die Linie über den Ziffern ist der Rahmen, kein Segment").

Voraussetzungen: eine KI-Aufgaben-Entität mit Bildunterstützung (Anhänge), eine Kamera-Entität.

### Kamera: ESP32-CAM mit ESPHome

Ein Beispiel liegt in [esphome-esp32-cam.yaml](esphome-esp32-cam.yaml). Erfahrungen aus dem Betrieb:

* **Kameratakt 8 MHz** statt 20 MHz. Der höhere Takt stört die WLAN-Antenne der ESP32-CAM; Bilder dauern dann über 10 Sekunden oder brechen ab, OTA-Updates hängen.
* **Zwei Bildpuffer** und kein Dauer-Streaming (`idle_framerate: 0 fps`). Das Modul verwirft die ersten Bilder nach dem Einschalten des Lichts.
* **Blitz-LED** über `ledc` auf Kanal 2 (die Kamera belegt den Timer der Kanäle 0 und 1) und mit begrenzter Leistung, sonst spiegelt das Display. Meist reichen 10 bis 60 %.
* Bei LCD-Anzeigen den Winkel so wählen, dass die LED nicht direkt reflektiert.

### Kosten

Pro Bild eine KI-Abfrage, pro Ablesung meist 2 Bilder. Mit einem kleinen Modell (z. B. Claude Haiku) und 1024×768 Pixeln sind das Bruchteile eines Cents je Ablesung. Das Intervall bestimmt die Kosten: alle 30 Minuten sind rund 100 Bilder am Tag.

## Datenschutz

Die Bilder gehen an den Anbieter der gewählten KI-Aufgabe. Sie zeigen nur die Zähleranzeige, sofern die Kamera passend ausgerichtet ist.
