"""Compatibility facade for the split scheduling, selection, packing and batch modules."""

from .batches import *  # noqa: F401,F403
from .curriculum import *  # noqa: F401,F403
from .packing import *  # noqa: F401,F403
from .selection import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("_")]
