"""
Write sparkline graphs of CPU and memory usage to your logs.
"""

__all__ = [
    "monitor_metrics_on_call",
    "log_system_metrics",
    "MetricsLoggingContext",
    "__version__",
    "sparkline",
    "GraphStyle",
    "Metrics",
]

from sparkle_log.__about__ import __version__
from sparkle_log.as_context_manager import MetricsLoggingContext
from sparkle_log.as_decorator import monitor_metrics_on_call
from sparkle_log.custom_types import GraphStyle, Metrics
from sparkle_log.log_writer import log_system_metrics
from sparkle_log.ui import sparkline
