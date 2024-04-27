"""
Global logger to avoid cyclical imports
"""

import logging

GLOBAL_LOGGER = logging.getLogger(__name__)
