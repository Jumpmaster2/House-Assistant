"""Constants for House Assistant."""

from __future__ import annotations

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "house_assistant"
NAME: Final = "House Assistant"
LOGGER = logging.getLogger(__package__)

# Every platform is set up once; the modules add and remove their entities there.
PLATFORMS: Final = [Platform.BUTTON, Platform.CAMERA, Platform.SENSOR, Platform.SWITCH]

# Options are kept per section: the house (core) and one section per module, with the
# keys of the former integrations unchanged inside.
OPT_CORE: Final = "core"
CONF_MODULES: Final = "modules"

MODULE_METER: Final = "meter"
# order of the modules in dialogs and in the panel
MODULE_ORDER: Final = (MODULE_METER,)

SUBENTRY_METER: Final = "meter"

STORAGE_VERSION: Final = 1
