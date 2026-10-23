# House Assistant

[Deutsche Version](README.md)

Custom integration for Home Assistant that brings three integrations together on one model of the house:

* **Heating** (formerly [AI Heating Assistant](https://github.com/Jumpmaster2/AI-Heating-Assistant)): local, learning control per room, heating day decision and parameter review by Claude, ventilation advice.
* **Covers** (formerly [Shutter Assistant](https://github.com/Jumpmaster2/Shutter-Assistant)): sun protection by direction, evening mode, ventilation position, weather protection, override, morning opening, vacation simulation.
* **Meters** (formerly [Zähler-Ablesung](https://github.com/Jumpmaster2/Zaehler-Ablesung)): read meters with a camera and an AI, with a majority vote and a plausibility check.

Rooms and windows are entered only once. Heating, covers and meters build on them: cross ventilation follows from the arrangement of the windows, the heating day drives covers and meters, and the heat meter is only read when the heating ran.

> Status: in development (version 0.1.0, only the skeleton). Until version 1.0.0 please keep using the three existing integrations.

The full plan of the rebuild is in [docs/PLAN.md](docs/PLAN.md) (German).

## Installation with HACS

1. Open HACS and choose **Custom repositories** in the menu at the top right.
2. Add the repository `https://github.com/Jumpmaster2/House-Assistant` with type **Integration**.
3. Download **House Assistant** and restart Home Assistant.
4. **Settings > Devices & services > Add integration > House Assistant**.

Requires Home Assistant 2026.10 or newer.

## Development

```bash
pip install -r requirements_test.txt ruff
ruff check custom_components tests scripts
ruff format --check custom_components tests scripts
python scripts/build_labels.py --check
pytest
```

The panel texts (`frontend/labels.js`) are generated from the translation files. After changing `translations/*.json`, run `python scripts/build_labels.py` once (a test checks it). Before publishing, `python scripts/check_privacy.py --patterns <file>` checks for private data.

## License

MIT, see [LICENSE](LICENSE).
