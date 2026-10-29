# Heizung

Deutsch | [English](heating.en.md)

Das Modul **Heizung** (bisher AI Heating Assistant) regelt eine Fußbodenheizung (oder Heizkörper je Raum, siehe Heizungsart) mit einem Schaltaktor je Heizkreis (z. B. ein Relais, das den Stellantrieb schaltet) lokal, lernt das Verhalten jedes Raums und lässt die Parameter regelmäßig von Claude (Anthropic) prüfen. Home Assistant trifft alle Schaltentscheidungen selbst. Die KI schaltet nie, sie passt nur Parameter innerhalb einstellbarer Grenzen an und wird mit wachsender Sicherheit seltener gefragt.

Das Modul ersetzt typischerweise: Thermostat-Helfer (Generic Thermostat), Better Thermostat, Automationen für Sollwert, Wetter, Kälte und Urlaub sowie eine Lüftungsempfehlung auf Basis der Luftfeuchte.

Räume und Fenster kommen aus dem **Haus** (Panel *House Assistant > Haus*): Ein Raum mit Temperatursensor bekommt Heizung und Lüftungsempfehlung, mit Heizkreis-Schalter auch ein Thermostat. Die Fensterkontakte sind die Kontakte der Fenster des Raums, die Größe des Fensters ergibt die Öffnungsfläche.

## Lokale Regelung je Raum

* **Sollwert** über die normale Thermostatkarte. Er bleibt dauerhaft gespeichert, bis du ihn änderst. Keine Zeitpläne, keine Nachtabsenkung (bei Fußbodenheizung meist kontraproduktiv).
* **Vorausschauend einschalten:** Der Kreis geht an, wenn die Temperatur nach der gelernten Totzeit (unter Berücksichtigung von Abkühlrate, Außentemperatur und Sonne) unter Sollwert minus Einschalthysterese fallen würde.
* **Sonne vorausschauend:** Für die Abkühlung über die Vorlaufzeit zählt nicht nur die aktuelle PV-Leistung, sondern die in dieser Zeit erwartete. Ist absehbar, dass die Sonne den Raum ohnehin aufheizt, schaltet der Kreis morgens nicht erst ein; abends rechnet die Regelung nicht mehr mit Sonne, die gleich verschwindet. Quelle ist ein optionaler PV-Prognosesensor (z. B. Forecast.Solar) oder, ohne ihn, die stündliche Wettervorhersage (Bewölkung) zusammen mit dem Sonnenstand. Dafür lernt das Modul an fast wolkenlosen Tagen, wie viel PV-Leistung bei klarem Himmel zu erwarten ist. Die Prognose fließt nur zu 70 % ein (Option „Vertrauen in die Sonnenprognose“), und 1 K unter Sollwert wird unabhängig von jeder Vorhersage geheizt (Option „Immer heizen unter Sollwert um“, 0,3 bis 3 K). Ohne PV-Leistungssensor bleibt alles wie bisher. Liefert der Sensor tagsüber keinen Wert, gilt die PV-Leistung als unbekannt: Es wird dann nichts kalibriert und nichts ins Modell übernommen, gerechnet wird mit der erwarteten Leistung (PV-Prognosesensor oder Sonnenstand und Bewölkung, sobald die Skala gelernt ist, sonst 0); bei tief stehender Sonne oder wenn ohnehin kaum Leistung zu erwarten ist, gilt 0. Fehlt der Wert länger als eine Stunde bei Tag, steht eine Warnung im Protokoll.
* **Vorausschauend abschalten:** Der Kreis geht aus, wenn die aktuelle Temperatur plus das erwartete Überschwingen den Sollwert plus Ausschalthysterese erreicht. Das Überschwingen der trägen Fußbodenheizung wird gelernt (abhängig von der Laufzeit). Nach dem Abschalten wird die noch im Boden steckende Wärme beim Wiedereinschalten berücksichtigt, bis die Temperatur wieder fällt; sonst liefe der Kreis nach der Mindestpause sofort wieder an.
* **Fenster:** Ist ein Fenster des Raums länger als die Fensterverzögerung offen, pausiert die Heizanforderung. Nach dem Schließen wird die gelernte Erholungszeit abgewartet, weil Estrich und Wände den Raum oft selbst wieder aufheizen. Ist die Temperatur vor dem Lüften wieder erreicht, endet die Erholung sofort (nach kurzem Lüften nicht, siehe *Kurzlüften*). Die Erholungszeit richtet sich nach der Lüftung selbst (siehe *Lernen je Raum*): Nach kurzem Stoßlüften wartet die Heizung kürzer als nach langem Lüften bei Frost oder Querlüften. **Gekippt** zählt wie offen, aber nur mit 25 % der Öffnungsfläche: über einen Fenstergriff (offen, gekippt, zu) oder einen Kipp-Kontakt des Fensters. Ein nicht verfügbarer Kontakt zählt wie bisher als zu.
* **Querlüften und Luftzug, automatisch:** Aus der Lage der Fenster am Haus (Wand und Position, Etage aus dem Home-Assistant-Bereich des Raums) erkennt das Modul zwei Fälle:
  * *Querlüften:* ein eigenes Fenster ist offen, zusammen mit einem Fenster eines anderen Raums derselben Etage an einer gegenüberliegenden oder angrenzenden Wand.
  * *Luftzug:* Zwei Fenster anderer Räume derselben Etage (gegenüber oder über Eck) sind offen, und der Raum liegt höchstens die *Luftzug-Reichweite* (Standard 2 m) von der Linie zwischen ihnen entfernt. Dann verhält sich der Raum wie bei einem eigenen offenen Fenster: Pause nach der Fensterverzögerung, danach Erholungszeit, kein Lernen und keine Zählung als „zu kalt“. Dafür braucht das Haus Länge und Tiefe (*Haus > Allgemein*); ohne sie gibt es nur Querlüften.

  Im Raum-Editor (*Haus > Räume*) zeigt ein Plan des Hauses die Kombinationen als Linien, jede lässt sich einzeln abschalten. Gibt es in Home Assistant keine Etagen, liegen alle Räume auf einer Etage; ein Raum, dessen Etage sich nicht bestimmen lässt, nimmt nicht teil. Ein Fenster ohne Wand (eigene oder die seiner Himmelsrichtung) nimmt ebenfalls nicht teil.
* **Luftzug von Hand:** Zusätzlich gibt es je Raum unter *Luftzug aus anderen Räumen* bis zu vier Kombinationen von Fensterkontakten anderer Räume (auch über Etagen, z. B. ein Treppenhaus). Sobald alle Fenster einer Kombination offen sind, wirkt das wie Luftzug. Eine Kombination mit nur einem Fenster löst schon allein aus. Die Lüftungsempfehlung des Raums richtet sich weiter nur nach seinen eigenen Fenstern. Die Attribute `draft` und `draft_windows` des Thermostats zeigen, ob gerade Luftzug erkannt wird und durch welche Fenster.
* **Kurzlüften:** Solange ein Fenster offen ist, schaltet ein ausgeschalteter Kreis nicht ein, auch vor Ablauf der Fensterverzögerung. Ein laufender Kreis wird dabei nicht unterbrochen. War das Fenster mindestens *Kurz lüften ab* (Standard 1 Minute, je Raum) offen, aber kürzer als die Fensterverzögerung, wartet die Heizung danach eine feste Zeit: die gelernte Erholungszeit mal *Wartezeit nach kurzem Lüften* (Standard 50 %, also bei 30 Minuten gelernter Erholungszeit 15 Minuten). Diese Wartezeit endet nur durch Zeitablauf, nicht durch eine wieder erreichte Temperatur, und wird nicht nach der Länge des Lüftens skaliert. 0 % heißt keine Wartezeit. Das Logbuch zeigt „Kurz gelüftet: Wartezeit bis ...“ und „Wartezeit nach kurzem Lüften beendet.“; bei zu kurzem Lüften oder ohne Wartezeit steht nichts darin. Das Lernen der Erholungszeit bleibt davon unberührt: gemessen wird weiter, bis der Raum wieder seine Temperatur erreicht. Beide Werte sind Einstellungen des Raums im Abschnitt *Lüften* (Dialog und Panel), jederzeit änderbar, nicht von der KI verstellt.
* **Mindest-Ein- und -Ausschaltzeit** werden immer eingehalten.
* **Frostschutz** gilt immer, auch außerhalb der Heizperiode und bei ausgeschaltetem Thermostat.
* **Ausfälle:** Liefert der Temperatursensor keinen oder einen unmöglichen Wert (außerhalb −50 bis 80 °C, `nan`), bleibt der Kreis aus (Status *Sensorfehler*), auch der Frostschutz kann dann nicht greifen. Ist der Schalter nicht erreichbar, zeigt der Status *Aktor nicht erreichbar*. Dauert ein solcher Ausfall (oder der des Außentemperatursensors) länger als 15 Minuten, erscheint eine Reparaturmeldung unter Einstellungen > System > Reparaturen; sie verschwindet von selbst, sobald der Wert zurück ist. Eine ignorierte Meldung bleibt auch nach einem Neustart ignoriert, solange der Ausfall andauert. Folgt ein Schalter den Befehlen nicht, wird er nach 1, 2, 4, 8 und dann alle 15 Minuten erneut geschaltet statt jede Minute; nach drei Versuchen erscheint ebenfalls eine Meldung.
* **Unveränderter Sensor:** Ändert sich der Wert eines Raumtemperatursensors mit Heizkreis länger nicht, erscheint eine Reparaturmeldung. Die Einstellung *Sensor unverändert melden nach* in den Notfallregeln beträgt standardmäßig 12 Stunden; 0 schaltet die Prüfung aus. Die Regelung läuft unverändert weiter. Bei grober Sensorauflösung in sehr stabilen Räumen die Frist erhöhen oder 0 setzen.
* **Heizperiode:** Außerhalb (z. B. 01.04. bis 30.09.) bleiben alle Kreise aus, es gibt keine KI-Abfragen.
* **Urlaub:** Im Urlaub des Hauses (Schalter *Urlaub* mit Abreise und Rückkehr, oder eine externe Quelle wie ein Kalender; siehe [README](../README.md#urlaub)) gilt die Urlaubstemperatur für alle Räume. Anhand der gelernten Aufheizrate wird so rechtzeitig vorgeheizt, dass zur Rückkehr der normale Sollwert erreicht ist; die eigene Rückkehr des Schalters hat Vorrang vor einer Rückkehr-Entität. Liegt die Rückkehr in der Vergangenheit, wird sie ignoriert und die Urlaubstemperatur gilt. Die Lüftungsempfehlung ruht im Urlaub (Option *Lüftungsempfehlung ruht*, Standard an).

## Heiztag-Entscheidung (Nachtlauf)

Einmal pro Nacht (Uhrzeit einstellbar) wird entschieden, ob heute überhaupt geheizt wird.

1. Eine **lokale Regel** schlägt vor: heizen, wenn die Prognose-Höchsttemperatur unter `theta` liegt oder ein Raum unter Sollwert plus `puffer` liegt.
2. Die **KI** bekommt Wettervorhersage, Raumwerte, Lernwerte und die bewerteten letzten Tage (mit Heizminuten und Überheizen je Tag) und antwortet strukturiert (JSON mit Schema). Komfort hat Vorrang, unnötige Heiztage soll sie aber vermeiden.
3. Ein **Phasenmodell** entscheidet, wer führt: *KI führt* (Start), *Gemeinsam* (bei Einigkeit diese, sonst die Regel, wenn sie sich sicher ist), *Regel führt* (die KI wird nur gefragt, wenn die Regel unsicher ist, plus einmal pro Woche zur Kontrolle). Ein Wechsel erfolgt nach genügend Tagen mit hoher Übereinstimmung und wenigen Regelfehlern, bei Fehlern geht es eine Phase zurück.
4. Jeder Tag wird nachträglich **bewertet**. Solange nichts geheizt hat, zählt die echte Raumtemperatur (Minuten zu kalt außerhalb von Lüftungsphasen). Sobald ein Kreis lief, hat die Entscheidung den Raum selbst warm gehalten; dann zählt ein virtueller Raum, der mit der gelernten Abkühlrate ohne Heizung weiterläuft. Fehler A (nicht geheizt, obwohl nötig) und Fehler B (geheizt ohne Bedarf) passen `theta` und `puffer` an. Tage mit manuellem Override und Urlaubstage werden nicht gelernt.

Bei "kein Heiztag" bleiben alle Kreise aus, außer Frostschutz und der optionalen **Notfallregel** (Raum unter dem Sollwert und Temperatur voraussichtlich nach der Vorlaufzeit lange und deutlich darunter, ohne dass gelüftet wurde). Über die Auswahl "Heiztag manuell" lässt sich der Tag übersteuern, das gilt bis zur nächsten Entscheidung. "Heute heizen" wirkt auch außerhalb der Heizperiode (etwa an einem kalten Frühlingstag); die KI bleibt dort aus.

Der Heiztag steht auch den anderen Modulen zur Verfügung: als Heizbedarf der Rollos (Option *Heiztag der Heizung*) und als Bedingung der Zähler (Option *Tage ohne Heizen*).

## Lernen je Raum

* **Thermisches Modell** (rekursive kleinste Quadrate): `dT/dt = a · Ventil − k · (T_innen − T_außen) + s · PV`. Daraus folgen Aufheizrate, Abkühlrate, Einfluss der Außentemperatur (`k`) und Einfluss der Sonne (`s`, PV-Leistung als Sonnenindikator).
* **Ereignisse:** Totzeit nach dem Einschalten, Überschwingen nach dem Abschalten, Erholungszeit nach dem Lüften. Die Totzeit zählt erst, wenn der Anstieg bestätigt ist (ein zweiter Sensorschritt oder ein Schritt, der fünf Minuten anhält), damit ein einzelnes Zittern des Sensors sie nicht verfälscht. Die Erholungszeit wird auch gelernt, wenn die Heizung die Wartezeit abbricht, sofern der Raum am Ende der Wartezeit gerade von selbst wärmer wurde; das thermische Modell vergisst langsam (etwa drei Wochen).
* **Erholung je Lüftung:** Wie lange ein Raum zum Erholen braucht, hängt davon ab, wie stark er beim Lüften ausgekühlt ist. Jede Lüftung wird deshalb verfolgt: wie weit die Temperatur bis zum Schließen gefallen ist (K) und wie lange und wie tief sie unter dem Wert vor dem Lüften lag (Kelvinstunden; langes Lüften, Querlüften und Frost kühlen auch Wände und Boden aus). Ein zweites Modell (kleinste Quadrate) lernt daraus `Erholung = Grundwert + Minuten je K Abfall + Minuten je Kelvinstunde`. Ab vier ausgewerteten Lüftungen wartet die Heizung nach jeder Lüftung die dafür erwartete Zeit, höchstens das Dreifache und mindestens ein Viertel der mittleren Erholungszeit. Davor gilt die mittlere Erholungszeit. Das Modell vergisst langsam (etwa 30 Lüftungen); die Koeffizienten stehen als Attribute am Sensor *Erholungszeit nach Lüften* und werden mit exportiert.
* Alle Werte werden dauerhaft gespeichert, als Sensoren angezeigt und lassen sich exportieren, importieren und zurücksetzen. Export und Import finden Räume über den Namen, deshalb muss jeder Raum anders heißen. Werden die KI-Grenzen enger gestellt, werden Werte außerhalb beim nächsten Laden auf die Grenze gesetzt (mit Logbuch-Eintrag).

## KI-Prüfung (Claude)

* Nur an Heiztagen und in der Heizperiode. Sie erhält eine kompakte Zusammenfassung je Raum (Ist, Soll, Lernwerte, Kennzahlen seit der letzten Prüfung) und liefert Parameteranpassungen als JSON. Begründungen schreibt sie in der Sprache der Meldungen (Einstellungen des Hauses, sonst die Sprache von Home Assistant, auch regionale Varianten wie de-CH).
* **Ziel:** so wenig Wärme wie möglich, ohne dass ein Raum unter den Sollwert fällt. Komfort ist eine feste Grenze, kein Tauschobjekt. Dafür bekommt die KI neben den Minuten zu kalt auch:
  * **Überheizen** (`over_kh`): Kelvinstunden mehr als 0,2 K über dem Sollwert, während der Kreis läuft und bis 4 Stunden nach dem Abschalten (also Wärme, die die Heizung zu viel geliefert hat). Wärme nur von der Sonne an einem Tag ohne Heizen zählt nicht. Der Anteil bei Sonne (`sun_over_kh`, PV ab 0,3 kW bzw. ab 10 % der gelernten Leistung bei klarem Himmel) zeigt, ob der Sonnenfaktor zu niedrig ist.
  * **Heizaufwand je Bedarf** (`on_per_kh`): Heizminuten je Kelvinstunde Unterschied zwischen Sollwert und Außentemperatur. So sind Prüfungen bei unterschiedlichem Wetter vergleichbar.
  * **Mittlere Laufzeit** je Einschalten.
  * **Lüften und Erholung:** Minuten mit offenem Fenster, davon nur Luftzug aus anderen Räumen (`draft_min`) und Querlüften mit eigenem Fenster (`cross_min`), Zahl der Lüftungen, Minuten in der Erholung und davon zu kalt (`rec_cold_min`, zählt nicht zu den Minuten zu kalt). Dazu die letzten 8 Lüftungen einzeln: Uhrzeit, Dauer, Art (eigenes Fenster, Querlüften, nur Luftzug), Öffnungsfläche, Außentemperatur, Temperatur vorher, Abfall, Kelvinstunden, erwartete und tatsächliche Erholung und wie sie endete. Damit kann die KI die Korrektur der Erholungszeit und die Fensterverzögerung gezielt anpassen.
  * **Verlauf der letzten 6 Prüfungen** mit ihren Kennzahlen und den dabei gemachten Änderungen. Die KI kann damit beurteilen, ob eine Änderung etwas gebracht hat, und sie sonst zurücknehmen. Wird ein Raum zurückgesetzt oder ein gelernter Wert von Hand geändert, wird sein Verlauf gelöscht.
* Anpassbare Parameter: Einschalt- und Ausschalthysterese, Faktor Überschwingen, Faktor Vorlauf, Sonnenfaktor, Fensterverzögerung, Korrektur der Erholungszeit, `puffer` und `theta`. Jeder Wert wird auf Minimum, Maximum und eine maximale Änderung je Prüfung begrenzt (alles einstellbar).
* **KI-Anweisungen anpassen:** Im Panel unter *Heizung > KI > KI-Anweisungen* sind die Anweisungen an die KI für beide Aufrufe (Nachtentscheidung und Parameterprüfung) in Bausteine zerlegt. Jeder Standard-Baustein lässt sich abschalten oder umformulieren (*Standard wiederherstellen* setzt ihn zurück). Eigene Bausteine (bis zu 10 je Aufruf, je höchstens 2000 Zeichen, in jeder Sprache) ergänzen das Wissen über das Haus, z. B. „Im Wohnbereich brennt abends meist der Kaminofen“. Aufgabe und Antwortformat bleiben fest, damit die Antwort gültig bleibt. Eine Vorschau zeigt die fertige Anweisung. Längere Anweisungen kosten etwas mehr je Abfrage.
* **Seltener fragen:** Das Prüfintervall verdoppelt sich nach jeder Prüfung ohne relevante Änderung und ohne Komfortfehler (bis zum Maximalintervall). Es fällt auf das Grundintervall zurück, wenn es zu kalt war, ein Raum deutlich überheizt wurde (mehr als 0,5 Kelvinstunden je Tag, anteilig), die KI deutlich geändert hat oder du Einstellungen bzw. einen Sollwert um mindestens 0,5 K änderst (kleinere Schritte, etwa aus Automationen, setzen das Intervall nicht zurück). Eine bereits geplante Prüfung bleibt über den Nachtlauf hinweg bestehen; nach einem Nicht-Heiztag folgt die nächste Prüfung nach dem Grundintervall, und war ein Raum seit der letzten Prüfung zu kalt, wird die nächste Prüfung vorgezogen.
* **Kosten:** aus der Token-Nutzung mal den eingetragenen Preisen (in USD). Antwortet nach einem serverseitigen Fallback ein anderes Modell, gilt dessen Listenpreis. Vor jeder Abfrage wird geschätzt (Ausgabe: doppelter Mittelwert der bisherigen Antworten im Monat, höchstens die maximalen Ausgabe-Tokens, Standard 16000 inklusive Denken); ist das Monatsbudget erreicht, gibt es bis zum Monatswechsel keine Abfragen.
* **Ausfall:** Bei Fehlern, Zeitüberschreitung oder ungültiger Antwort läuft die Regelung mit den zuletzt gelernten Werten weiter. Der API-Key erscheint nie im Log und wird in der Diagnose geschwärzt.
* **Abgelehnter API-Key:** Lehnt Anthropic den Key ab (z. B. widerrufen), fragt Home Assistant unter Einstellungen > Geräte & Dienste nach einem neuen Key (erneute Authentifizierung). Bis dahin läuft die lokale Regelung ohne KI weiter; ein leeres Feld schaltet die KI ab.
* **Wetterdienst antwortet nicht:** Die Wetterprognose wird höchstens 10 Sekunden lang abgewartet; danach entscheidet die Heiztag-Regel ohne Prognose, und die Regelung läuft weiter. Schlägt die Heiztag-Entscheidung fehl, wird sie nach 15 Minuten erneut versucht (Fehler im Log).

## Wärmezähler

Optional. Mit einem Wärmezähler sieht die KI die tatsächlich verbrauchte Wärme statt nur der Laufzeit der Kreise. Am besten ist ein Zähler des Moduls **Zähler**: Die Heizung bekommt dann den echten Zeitpunkt der Ablesung, und eine bestätigte Korrektur nach unten ist kein Zählertausch. Ein beliebiger Energie-Sensor geht weiterhin.

* Verbrauch wird immer **zwischen zwei Zählerwerten** gerechnet, nicht zwischen beliebigen Zeitpunkten. Zusammen mit jedem Zählerwert merkt sich das Modul den bis dahin aufgelaufenen Heizbedarf (Kelvinstunden Sollwert minus Außentemperatur, Mittel über die Räume). Verbrauch und Bedarf decken so genau denselben Zeitraum ab, auch wenn der Zähler nur alle paar Stunden und in groben Schritten meldet.
* **KI-Prüfung:** `heat` mit kWh, Stunden und `kwh_per_kh` (kWh je Kelvinstunde Bedarf, das beste Maß für die Effizienz) seit der letzten Prüfung; Zeiträume unter einer Stunde werden nicht gemeldet. `kwh_per_kh` steht auch im Prüfverlauf.
* **Nachtlauf:** kWh je vergangenem Heiztag in der Historie.
* **Panel:** Karte **Wärme** mit heute, gestern, diesem Monat und dem Zeitpunkt des letzten Zählerwerts. Ein Tag zählt vom letzten Zählerwert vor Mitternacht bis zum letzten vor der nächsten Mitternacht, „gestern“ fehlt nach einem ausgelassenen Tag.
* Sinkt der Zählerstand (Zählertausch, keine bestätigte Korrektur) oder wird ein anderer Zähler gewählt, beginnt die Zählung neu.

### Wärme je Raum

Mit einer Wohnfläche je Raum (Feld **Wohnfläche**, m², 1 bis 200) verteilt das Modul jeden Zählerwert auf die Räume. Eine Heizphase ist die Zeit zwischen zwei geänderten Zählerwerten. Jeder Raum, der darin geheizt hat, bekommt einen Anteil: Laufzeit mal Wohnfläche mal Heizbedarf (Sollwert minus Außentemperatur) mal eine Leistung je m² und K, die das Modul aus den Phasen lernt. Die Anteile ergeben zusammen immer den Zählerwert. Was kein Raum geheizt hat (Warmwasser, Leitungen), steht unter **Nicht zugeordnet**. Räume ohne Wohnfläche nehmen nicht teil.

* **Sensoren:** je Raum **Wärmeverbrauch** (kWh gesamt, für das Energie-Dashboard), **Wärmeverbrauch heute** und **Heizleistung geschätzt** (kW bei Sollwert und Außentemperatur von jetzt; Attribute `confidence`, `kwh_since_last_reading_estimate`, `minutes_heated_today`). Im Haus **Nicht zugeordnet**. Die Summen ändern sich nur mit den Ablesungen und fallen nie.
* **Sicherheit:** `confidence` steigt mit den Heizphasen des Raums. Phasen, in denen nur dieser Raum heizte, lernen am schnellsten. Der Zähler liefert nur ganze kWh; kurze Phasen werden mit der nächsten zusammengelegt. Am Anfang sind die Anteile grob.
* **Ablesung:** Solange ein Raum heizt, wird der Wärmezähler alle 15 Minuten gelesen, sonst nur einmal am Tag (Optionen des Zählers „Intervall, solange ein Raum heizt“ und „Intervall sonst“). Das Ein- und Ausschalten der Heizung (der erste Heizkreis an, der letzte aus) fordert eine Ablesung an, mindestens 5 Minuten nach der letzten. Nach dem Ende bleibt das kurze Intervall noch höchstens 30 Minuten, damit die letzte Wärme der Phase ihr zugeordnet wird; ohne laufenden Heizkreis wird danach nichts mehr verbraucht. Das gilt für Wärmezähler und Zähler mit der Bedingung „Heiztag“.

## Lüftungsempfehlung

Je Raum mit Temperatursensor (auch ohne Heizkreis) aus absoluter Feuchte innen und außen (oder eines Referenzraums):
*Jetzt lüften* (Feuchte über Schwelle, Außenluft trockener und Lüften senkt die Feuchte spürbar), *Lüften sinnvoll* (kühlt, wenn nicht geheizt wird; in der Heizperiode nur, wenn der Raum deutlich über dem Sollwert liegt; nie unter der optionalen Mindesttemperatur und nie, wenn die Außenluft die relative Feuchte des Raums über seine Feuchte-Schwelle bringen würde), *Nicht lüften*, *Fenster schließen* (offen, bringt aber nichts), *Lüften blockiert* (Sperr-Entität aktiv, z. B. Klimaanlage), *Alles optimal* und *Urlaub* (die Empfehlung ruht im Urlaub).

**Gelerntes Feuchteprofil je Raum:** Für jeden Raum mit Feuchtesensor lernt das Modul, was im Raum üblich ist (Tagesminimum, -mittel, -maximum, tags und nachts, getrennt für Heizperiode und Rest des Jahres), die tiefste Feuchte der letzten 14 Tage, wie schnell die Feuchte bei geschlossenem Fenster steigt und was Lüften wirklich bringt: welcher Teil des Unterschieds zur Außenluft beim Lüften verschwindet und wie viel davon innerhalb von 30 Minuten aus Wänden und Möbeln zurückkommt. Sobald zwei Lüftungsvorgänge ausgewertet sind, rechnet die Empfehlung mit der Feuchte, die Lüften tatsächlich erreicht: Sinkt sie dadurch nicht mindestens um den Mindest-Feuchteabfall, lautet die Empfehlung *Nicht lüften* statt *Jetzt lüften* (manchmal geht es eben nicht tiefer). Eine Hysterese verhindert ein Hin und Her um die Schwelle. Urlaubstage gehen nicht ins Profil ein.

**Energiesparend lüften:** In der Heizperiode kostet Lüften Wärme, umso mehr, je kälter die Außenluft ist. Ein nur leicht zu feuchter Raum wartet deshalb: Die Feuchte muss die Schwelle um den *Energiespar-Zuschlag* je Kelvin Temperaturunterschied übersteigen (Standard 0,25 %/K, bei 21 °C innen und 1 °C außen also 5 % mehr). Bis dahin lautet die Empfehlung *Nicht lüften*, ein offenes Fenster ergibt *Fenster schließen*. Hat das Lüften begonnen, läuft es bis zur Hysterese unter der nötigen Feuchte weiter. Der Zuschlag reicht nie über die *Schimmelgrenze* (Standard 70 %, je Raum einstellbar, z. B. niedriger bei kalten Außenwänden); ab dort wird gegen Schimmel immer gelüftet. Nach einer Lüftung bekommt der Raum eine *Pause* (Standard 30 Minuten), in der Feuchte aus Wänden zurückkommt, bevor erneut zum Trocknen geraten wird.

**Gelernte Lüftdauer:** Jeder Raum lernt aus seinen Lüftungen, wie schnell seine Fenster die Luft austauschen (umgerechnet auf den Temperaturunterschied, denn kalte Luft zieht schneller). Daraus schlägt das Attribut `airing_minutes` die Minuten vor, die bis zum *Lüftziel* (Standard 5 % unter der Schwelle) nötig sind, mal *Lüftdauer-Faktor*, begrenzt auf *kürzeste* und *längste Lüftdauer* (3 bis 20 Minuten). Bis zwei Lüftungen ausgewertet sind, gilt eine Tabelle nach Außentemperatur (5 Minuten bei Frost, 10 bis 10 °C, 15 bis 15 °C, sonst 20). Die Größe der Fenster zählt mit: Ein kleines Fenster hat die halbe Öffnung eines mittleren, ein großes das 1,6-fache, eine Tür das 2,5-fache, ein gekipptes Fenster ein Viertel seiner Größe. Gelernt wird der Luftaustausch je Öffnungsfläche, deshalb stimmt die Lüftdauer für jedes Fenster des Raums. Vorgeschlagen wird die größte Öffnung (Attribut `airing_window`) mit der Dauer dafür; ist schon ein Fenster offen, gilt die Dauer für die offenen Fenster. **Querlüften** (ein eigenes Fenster zusammen mit einem Fenster eines anderen Raums, automatisch oder von Hand) tauscht die Luft viel schneller aus; dafür lernt der Raum einen eigenen Luftaustausch. Bis zwei Querlüftungen ausgewertet sind, gilt der normale (längere) Wert. Die KI sieht bei jeder Lüftung vorgeschlagene und tatsächliche Dauer, ob quergelüftet wurde, Feuchte vorher, am tiefsten und 30 Minuten danach und passt alle diese Werte je Raum an.

**KI-Lüftungsprüfung:** Ganzjährig prüft die KI die Lüftungsschwellen jedes Raums mit Feuchtesensor, aufgebaut wie die Parameterprüfung der Heizkreise: Sie bekommt das Feuchteprofil, die Statistik seit der letzten Prüfung (Minuten feucht, ab 70 %, empfohlen, Fenster offen, unnötig offen, offen beim Heizen, Wechsel der Empfehlung; Urlaubsminuten zählen nicht) und den Verlauf früherer Prüfungen und darf je Raum Feuchte-Schwelle, Hysterese, Mindest-Trocknungsvorteil, Übertemperatur der Referenz, Mindest-Feuchteabfall, Energiespar-Zuschlag, Schimmelgrenze, Lüftziel, Lüftdauer-Faktor, kürzeste und längste Lüftdauer, Pause nach dem Lüften, Mindest-Kühlvorteil, Kühl-Abstand und Kühlen-ab-Temperatur innerhalb der KI-Grenzen anpassen. Die konfigurierten Werte sind Startwerte; ändert man sie, ersetzen sie den Wert der KI. Das Intervall beginnt beim Grundintervall (6 h) und verdoppelt sich mit jeder Prüfung ohne relevante Änderung bis zum Höchstintervall (72 h); bleibt ein Raum lange feucht oder ändert sich etwas, beginnt es von vorn. Die Prüfung nutzt das gemeinsame Monatsbudget; ihre Anweisungen lassen sich unter *KI-Anweisungen* (Lüftungsprüfung) anpassen. Die gelernten Werte zeigt der Reiter **Lernwerte**.

## Panel

Im Panel **House Assistant**, Bereich **Heizung** (nur für Administratoren):

* **Übersicht:** Heiztag mit Phase und Begründung, Heiztag manuell (Automatik, Heute heizen, Heute nicht heizen), alle Räume mit Temperatur, Sollwert, Status und Lüftungsempfehlung (anklicken öffnet das Thermostat), Schalter KI aktiv, letzte und nächste KI-Prüfung, nächster Nachtlauf, letzte Heiztag-Entscheidung mit Quelle (KI, Regel, beide einig), KI-Kosten im Monat, Hinweise (fehlende Entitäten, letzter KI-Fehler, Budget erreicht) und eine Zusammenfassung der Einstellungen.
* **Räume:** die Heizung je Raum (Heizkreis, Sollwerte, Mindestlaufzeiten, Heizungsart, Lüftung, Luftzug von Hand); Name, Bereich, Sensoren und Fenster stehen im Bereich **Haus**.
* **Lernwerte:** je Raum mit Heizkreis eine kompakte Kachel mit Lernstand, Aufheiz- und Abkühlrate, Totzeit, Überschwingen, Erholung nach Lüften, Einfluss Außentemperatur und Sonne; aufklappbar die von der KI anpassbaren Regelparameter. Dazu die Heiztag-Regel (`theta`, bewertete Tage). Der Stift führt zum Bearbeiten der gelernten Werte.
* **Allgemein, Notfall & Lüftung, KI, Heiztag-Entscheidung:** alle Einstellungen nach Themen in Karten, jede Karte wird für sich gespeichert. Unter **KI** auch der API-Key (wird vor dem Speichern geprüft, der gespeicherte Key wird nie angezeigt) und die KI-Grenzen.

## Dashboard-Karten

Die Karten werden für alle Benutzer und Dashboards automatisch geladen (siehe [README](../README.md#dashboard-karten)).

**Thermostat** (`custom:house-assistant-thermostat-card`): sieht aus wie die Thermostat-Karte von Home Assistant und zeigt zusätzlich die **Luftfeuchte** des Raums, in derselben Zeile wie die zweite Temperatur. Den Sollwert stellst du durch Ziehen am Punkt auf dem Ring oder mit den Pfeiltasten ein (eine Berührung woanders auf dem Ring scrollt nur die Seite), die drei Punkte öffnen das Thermostat. Mit fester Höhe (`grid_options` mit `rows` als Zahl) wird der Ring so verkleinert, dass er in die Kachel passt.

```yaml
type: custom:house-assistant-thermostat-card
entity: climate.wohnbereich
show_current_as_primary: true   # Ist-Temperatur groß, Sollwert klein (Standard: false)
show_humidity: true             # Standard: true
name: Wohnbereich               # optional
```

**Thermostat kompakt** (`custom:house-assistant-thermostat-compact-card`): ohne Bogen, halb so hoch (Standard 6 × 2): oben der Name, groß die Ist-Temperatur und die Luftfeuchte, klein der Sollwert und der Status. Die Leiste links ist orange, solange geheizt wird, sonst grau. Ein Tipp öffnet das Thermostat zum Einstellen.

```yaml
type: custom:house-assistant-thermostat-compact-card
entity: climate.wohnbereich
show_humidity: true   # Standard: true
name: Wohnbereich     # optional
```

**Raumklima-Kachel** (`custom:house-assistant-climate-tile-card`): Standard 6 × 1 wie die Kachel-Karte: oben der Name, darunter Temperatur und Luftfeuchte nebeneinander. Die Werte kommen vom Thermostat des Raums oder von beliebigen Sensoren (auch für Räume ohne Heizkreis); ein angegebener Sensor hat Vorrang. Ein Tipp auf einen Wert öffnet die zugehörige Entität.

```yaml
type: custom:house-assistant-climate-tile-card
entity: climate.wohnbereich            # oder/und:
temperature_entity: sensor.temperatur_schlafzimmer
humidity_entity: sensor.luftfeuchtigkeit_schlafzimmer
name: Schlafzimmer                     # optional
```

## Einstellungen

Temperatursensoren dürfen in °C, °F oder K melden; ohne Einheit gilt das Einheitensystem von Home Assistant. Gerechnet wird intern in °C, und alle Temperaturen in den Einstellungen der Heizung (Sollwerte, Frostschutz, `theta`) werden in °C eingegeben. Die Thermostate zeigen Werte im Einheitensystem von Home Assistant.

Außentemperatur, Außenfeuchte, Wetter und Urlaub stehen in den **Einstellungen des Hauses** (siehe [README](../README.md#einstellungen-des-hauses)). Es gibt keine eigenen Quellen im Heizungsmodul.

| Option | Standard | Bedeutung |
|---|---|---|
| PV-Leistungssensor | | optional, Sonnenindikator (W oder kW; ohne Einheit gilt W, eine andere Einheit wird mit Warnung ignoriert) |
| PV-Prognosesensor | | optional, nur mit PV-Leistungssensor: Energie der nächsten Stunde (Wh oder kWh) oder Leistung in einer Stunde (W oder kW); ohne ihn wird die Wettervorhersage genutzt |
| Wärmezähler | | optional, Zählerstand der hier geregelten Heizkreise (ein Zähler des Moduls Zähler oder ein Energie-Sensor in Wh, kWh, MWh, MJ oder GJ); seltene und grobe Werte sind kein Problem |
| Heizperiode | 01.10. bis 31.03. (Südhalbkugel: 01.05. bis 30.09.) | im Dialog als Tag und Monat, im Panel im Format TT.MM.; der Vorschlag richtet sich bei der Einrichtung nach dem Breitengrad von Home Assistant |
| Frostschutz | 7 °C | gilt immer |
| Urlaubstemperatur | 18 °C | für alle Räume |
| Vorheiz-Reserve | 30 min | |
| Lüftungsempfehlung ruht (Haus > Urlaub) | an | im Urlaub |
| Startwert `theta` | 16 °C | Heiztag-Regel; nur bei der Einrichtung, danach wird der gelernte Wert bearbeitet |
| API-Key, Modell | Claude Opus 5.5 | änderbar, eigener Modellname möglich |
| Nachtlauf | 03:00 | |
| Monatsbudget | 5 USD | |

Reihenfolge im Optionsmenü (*Einstellungen > Heizung*): Allgemein, Urlaub, Notfallregel, Lüftung, KI, Heiztag-Entscheidung (Experten), KI-Grenzen (Experten). Lernschritte und Entscheidungsphasen liegen in einklappbaren Abschnitten.

* **Notfallregel:** an, 1 K unter Sollwert (voraussichtlich nach der Vorlaufzeit, mindestens die Einschalthysterese), 45 min, Fenster 30 min unverändert.
* **Lüftung:** Mindestvorteil absolute Feuchte 0,8 g/m³, außen höchstens 4 K wärmer, Mindest-Kühlvorteil 1 K, Kühlen in der Heizperiode erst ab 1 K über Sollwert, optional Kühlen erst ab einer festen Raumtemperatur (z. B. 23,5 °C, ganzjährig, Standard aus), Nacht 20:00 bis 08:00 Uhr (Uhrzeiten, minutengenau). Alle Schwellen sind Startwerte für die KI-Lüftungsprüfung (an, Grundintervall 6 h, Höchstintervall 72 h).
* **KI:** Modell, Effort (Standard niedrig), Nachtlauf, Prüfintervall 4 h, Maximalintervall 48 h, Budget, Preise in USD je Million Tokens (Anthropic rechnet in US-Dollar ab; es wird nicht umgerechnet) (Eingabe, Ausgabe, Cache schreiben, Cache lesen; vorbelegt mit dem Listenpreis des Modells), maximale Ausgabe-Tokens.
* **KI-Grenzen:** Minimum, Maximum, größte Änderung je Prüfung für jeden Parameter. Neue Eingaben müssen innerhalb des festen Parameterbereichs liegen; der Schritt darf von 0 bis zur Spanne dieses Bereichs reichen. Schritt 0 friert den Parameter ein. Bestehende brauchbare Grenzen außerhalb des festen Bereichs bleiben gültig und können unverändert gespeichert werden; erst beim Ändern gelten die festen Grenzen. Beim Start werden nur unbrauchbare Grenzen repariert, nicht bestehende Bereiche verengt.
* **Heiztag-Entscheidung:** gelerntes `theta` (änderbar), Bewertungsschwellen, Lernschritte, Bedingungen der Phasenwechsel.

Den API-Key änderst du im Panel unter **Heizung > KI** oder über **Neu konfigurieren**.

## Heizung je Raum

Im Panel unter **Heizung > Räume** (oder im Raum-Dialog unter der Integration). Je Raum:

| Option | Standard |
|---|---|
| Heizkreis-Schalter | z. B. `switch.heating_circuit_1`; leer = nur Lüftungsempfehlung (verlangt einen Temperatursensor) |
| Start-Sollwert, kleinster und größter Sollwert | 21 / 16 / 24 °C |
| Mindest-Ein- und -Ausschaltzeit | 10 / 10 min (fest) |
| Heizungsart | Fußbodenheizung (Standard), Heizkörper oder Andere; die KI beurteilt Trägheit und gelernte Werte danach. Die Regelung selbst lernt das Verhalten jedes Raums ohnehin. |
| Startwerte Fensterverzögerung, Erholungszeit, Totzeit, puffer | 5 min, 30 min, 30 min, 0,7 K; nur beim Anlegen |
| Abschnitt *Lüften*: Kurz lüften ab, Wartezeit nach kurzem Lüften | 1 min, 50 %; jederzeit änderbar |
| Feuchte-Schwelle | 60 % |
| Wohnfläche | optional, 1 bis 200 m²; für die Verteilung des Wärmezählers auf die Räume (siehe Wärmezähler) |
| Referenz-Temperatur und -Feuchte | optional, statt außen (Raum ohne eigenes Fenster) |
| Lüftungs-Sperr-Entität | optional |
| Luftzug aus anderen Räumen | optional: bis zu 4 Kombinationen von Fensterkontakten anderer Räume, die zusammen offen sein müssen |

Startwerte (auch `theta`) werden nur beim Einrichten bzw. Anlegen gesetzt und gelten, bis etwas gelernt wurde. Danach zeigt der Raum unter **Gelernte Werte** die Werte, mit denen gerade geregelt wird (Fensterverzögerung, Erholungszeit, Totzeit, puffer; die Werte zum kurzen Lüften stehen im Abschnitt *Lüften*), und das gelernte `theta` steht unter **Heiztag-Entscheidung**. Eine Änderung dort ersetzt den gelernten bzw. von der KI angepassten Wert, das Lernen geht von dort aus weiter, und das Logbuch vermerkt es.

## Entitäten

Entitäten, die nach einer Änderung nicht mehr entstehen (z. B. „Wärme heute“ nach dem Entfernen des Wärmezählers), werden beim nächsten Start des Moduls aus der Entitätsregistrierung entfernt. Schnell wechselnde Prognosewerte (`predicted_temperature`, `expected_peak`, `expected_pv_kw`) und große Attribute (Parameterliste, letzte Tage, Regel, KI-Zusammenfassung) zeichnet der Recorder nicht auf; die Werte sind auf die angezeigte Genauigkeit gerundet, damit nicht jede Minute ein neuer Zustand entsteht.

Bei neuen Installationen sind die Diagnose-Sensoren der Lernwerte (Aufheiz- und Abkühlrate, Überschwingen, Totzeit, Erholungszeit, Einfluss Außen und Sonne) zunächst deaktiviert; das Panel zeigt die Werte trotzdem an. KI-Zeitstempel, KI-Kosten und Entscheidungsphase sind Diagnose-Entitäten. Das Gerät eines Raums kommt in seinen Home-Assistant-Bereich.

Gerät „Heizung“:

* Binärsensor **Heiztag** (mit Quelle, Begründung, Konfidenz, Phase, Zeitpunkt der Entscheidung `decided_at` und nächstem Nachtlauf `next_decision`)
* Sensoren **Entscheidungsphase**, **Letzte KI-Prüfung** (mit Zusammenfassung und letztem Fehler), **Nächste KI-Prüfung**, **Letzte und nächste KI-Lüftungsprüfung**, **KI-Kosten im Monat**
* Sensor **Wärme heute** (nur mit Wärmezähler, kWh; Attribute `yesterday`, `month`, `last_month`, `meter_reading_at`)
* je Raum mit Wohnfläche und Wärmezähler: **Wärmeverbrauch**, **Wärmeverbrauch heute**, **Heizleistung geschätzt**; im Haus **Nicht zugeordnet**
* Schalter **KI aktiv**
* Auswahl **Heiztag manuell** (Automatik, Heute heizen, Heute nicht heizen)

Je Raum mit Temperatursensor (eigenes Gerät):

* **Thermostat** (climate, nur mit Heizkreis), Attribute u. a. `predicted_temperature`, `expected_peak`, `expected_pv_kw` (über die Vorlaufzeit erwartete PV-Leistung), `draft` und `draft_windows`
* Sensoren **Status**, **Aufheizrate**, **Abkühlrate**, **Überschwingen nach Abschalten**, **Totzeit**, **Erholungszeit nach Lüften**, **Einfluss Außentemperatur**, **Einfluss Sonne**, **Lernstand**
* Sensor **Lüftungsempfehlung** und Binärsensor **Lüften empfohlen** (auch für Räume ohne Heizkreis)

Alle wichtigen Entscheidungen und jede KI-Anpassung mit Begründung stehen im **Logbuch**.

## Dienste

`import_parameters`, `reset_learned`, `decide_heating_day`, `run_ai_check` und `run_ai_ventilation_check` (die drei letzten können KI-Kosten verursachen) dürfen nur Administratoren aufrufen; Automationen und Skripte ohne Benutzer dürfen sie weiter nutzen.

| Dienst | Zweck |
|---|---|
| `house_assistant.export_parameters` | Lernwerte und Parameter als JSON (Antwort des Dienstes) |
| `house_assistant.import_parameters` | Lernwerte und Parameter aus JSON setzen (z. B. Startwerte) |
| `house_assistant.reset_learned` | Lernwerte einzelner Räume auf die Startwerte zurücksetzen, optional auch die Parameter |
| `house_assistant.run_ai_check` | KI-Prüfung sofort starten |
| `house_assistant.run_ai_ventilation_check` | KI-Lüftungsprüfung sofort starten |
| `house_assistant.decide_heating_day` | Heiztag-Entscheidung sofort ausführen, optional ohne KI |

Beispiel Import:

```yaml
action: house_assistant.import_parameters
data:
  data:
    areas:
      Wohnzimmer:
        learned:
          dead_time_min: 45
          recovery_min: 40
          loss_per_h: 0.004
        params:
          hysteresis_on: 0.2
```

## Fehlerbehebung

* **Status *Sensorfehler*:** Der Temperatursensor liefert keinen, einen unmöglichen Wert oder eine Einheit, die keine Temperatur ist (Warnung im Protokoll). Der Kreis bleibt aus; nach 15 Minuten erscheint eine Reparaturmeldung.
* **Status *Aktor nicht erreichbar*:** Der Schalter ist `unavailable`. Folgt er Befehlen nicht, wird mit wachsendem Abstand erneut geschaltet; nach drei Versuchen erscheint eine Reparaturmeldung.
* **KI fragt nicht mehr:** Budget erreicht (Hinweis im Panel, Sensor *KI-Kosten im Monat* mit `budget_reached`) oder der API-Key wurde abgelehnt (erneute Authentifizierung unter Einstellungen > Geräte & Dienste).

## Datenschutz

Ohne API-Key verlässt nichts das Haus. Mit Key gehen an Anthropic: die Raumnamen, Temperaturen, Soll- und Lernwerte, Kennzahlen seit der letzten Prüfung, Außentemperatur, PV-Leistung, eine kompakte Wettervorhersage, Wärmezählerwerte und der Verlauf der Heiztag-Entscheidungen. Entitäts-IDs, Standort und der API-Key selbst sind nicht Teil der Anfragen.

## Bekannte Einschränkungen

* Alle Temperaturen in den Einstellungen der Heizung werden in °C eingegeben (Sensoren und Thermostate dürfen °F nutzen).
* Nur Schaltaktoren (an/aus) je Heizkreis, keine stetigen Ventile.
* Querlüften und Luftzug sind eine Näherung aus Wand und Reihenfolge der Fenster, ohne Innentüren. Falsche Kombinationen schaltest du im Raum ab; Kombinationen von Hand bleiben möglich.
* Die Verteilung des Wärmezählers auf die Räume ist gelernt, nicht gemessen. Ein Raum ohne Wohnfläche bekommt keinen Anteil; seine Wärme geht auf die übrigen Räume derselben Phase, bzw. auf „Nicht zugeordnet“, wenn sonst niemand geheizt hat.

## Beispiel für eine Automation

An einem Brückentag nicht heizen. Die Auswahl gilt für den Tag, an dem sie gesetzt wird; nach Mitternacht und vor dem Nachtlauf gesetzt, gilt sie für den neuen Tag:

```yaml
automation:
  - alias: "Kein Heizen am Brückentag"
    triggers:
      - trigger: time
        at: "00:30:00"
    conditions:
      - condition: state
        entity_id: calendar.brueckentage
        state: "on"
    actions:
      - action: select.select_option
        target:
          # die ID steht unter Einstellungen > Entitäten
          entity_id: select.heizung_heiztag_manuell
        data:
          option: off_today
```

## Ausschalten

Wird das Modul Heizung ausgeschaltet, die Integration deaktiviert oder entfernt, schaltet sie alle eingeschalteten Heizkreise aus; sonst würde ein gerade laufender Kreis ohne Grenze weiterheizen. Dasselbe gilt für den Schalter eines Raums ohne Heizkreis mehr und für einen Schalter, der in einem Raum durch einen anderen ersetzt wurde. Ein Neustart des Moduls (z. B. nach einer Änderung der Einstellungen) oder von Home Assistant lässt die Kreise unverändert.
