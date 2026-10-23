# House Assistant

[English version](README.en.md)

Custom Integration für Home Assistant, die drei bisherige Integrationen auf einem gemeinsamen Modell des Hauses zusammenführt:

* **Heizung** (bisher [AI Heating Assistant](https://github.com/Jumpmaster2/AI-Heating-Assistant)): lokale, lernende Regelung je Raum, Heiztag-Entscheidung und Parameterprüfung durch Claude, Lüftungsempfehlung.
* **Rollos** (bisher [Shutter Assistant](https://github.com/Jumpmaster2/Shutter-Assistant)): Sonnenschutz nach Himmelsrichtung, Abendmodus, Lüftungsposition, Wetterschutz, Übersteuerung, Morgenöffnung, Urlaubssimulation.
* **Zähler** (bisher [Zähler-Ablesung](https://github.com/Jumpmaster2/Zaehler-Ablesung)): Zähler mit einer Kamera und einer KI ablesen, mit Mehrheitsentscheid und Plausibilitätsprüfung.

Räume und Fenster werden nur einmal erfasst. Heizung, Rollos und Zähler bauen darauf auf: Querlüften ergibt sich aus der Anordnung der Fenster, der Heiztag steuert Rollos und Zähler, der Wärmezähler wird nur abgelesen, wenn geheizt wurde.

> Status: in Entwicklung (Version 0.1.0, nur das Grundgerüst). Bis zur Version 1.0.0 bitte weiter die drei bisherigen Integrationen verwenden.

Der vollständige Plan des Umbaus steht in [docs/PLAN.md](docs/PLAN.md).

## Installation über HACS

1. HACS öffnen, oben rechts im Menü **Benutzerdefinierte Repositories** wählen.
2. Repository `https://github.com/Jumpmaster2/House-Assistant`, Typ **Integration**, hinzufügen.
3. **House Assistant** herunterladen und Home Assistant neu starten.
4. **Einstellungen > Geräte & Dienste > Integration hinzufügen > House Assistant**.

Voraussetzung: Home Assistant 2026.10 oder neuer.

## Entwicklung

```bash
pip install -r requirements_test.txt ruff
ruff check custom_components tests scripts
ruff format --check custom_components tests scripts
python scripts/build_labels.py --check
pytest
```

Die Texte des Dashboards (`frontend/labels.js`) werden aus den Übersetzungsdateien erzeugt. Nach einer Änderung an `translations/*.json` einmal `python scripts/build_labels.py` ausführen (ein Test prüft das). Vor dem Veröffentlichen prüft `python scripts/check_privacy.py --patterns <Datei>` auf private Daten.

## Lizenz

MIT, siehe [LICENSE](LICENSE).
