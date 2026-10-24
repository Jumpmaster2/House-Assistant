"""Import every module so it registers itself with the runtime."""

from __future__ import annotations

from . import heating, meter, shutter  # noqa: F401
from .core import vacation  # noqa: F401  (the house)
