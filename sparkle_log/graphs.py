# sparkle_log/graphs.py
"""
Global logger to avoid cyclical imports
"""

from __future__ import annotations

import logging

GLOBAL_LOGGER = logging.getLogger(__name__)
