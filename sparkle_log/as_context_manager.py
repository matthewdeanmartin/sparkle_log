"""
Context manager of logger so you have more control over when it starts and stops.
"""

import logging
import time
from threading import Event, Thread
from typing import Any

from sparkle_log.custom_types import CustomMetricsCallBacks, GraphStyle
from sparkle_log.graphs import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricsLoggingContext:
    """
    Context manager to log system metrics.
    """

    def __init__(
        self,
        metrics=("cpu", "memory"),
        interval: int = 10,
        style: GraphStyle = "faces",
        custom_metrics: CustomMetricsCallBacks = None,
    ) -> None:
        """Initialize the context manager."""
        if not metrics:
            metrics = ("cpu", "memory")
        else:
            custom_metrics_names = custom_metrics.keys() if custom_metrics else []
            for metric in metrics:
                if metric not in ("cpu", "memory", "drive") and metric not in custom_metrics_names:
                    raise TypeError("Unexpected metric")
        self.metrics = metrics
        self.interval = interval
        self.style = style
        self.stop_event: Event | None = None
        self.scheduler_thread: Thread | None = None
        self.custom_metrics = custom_metrics

    def __enter__(self) -> "MetricsLoggingContext":
        """Start the context manager, if logging enabled."""
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(
                target=run_scheduler,
                args=(self.stop_event, self.metrics, self.interval, self.style, self.custom_metrics),
            )
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Stop the context manager."""
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            if self.stop_event:
                self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import random

    def dodgy_metric():
        return random.randint(0, 100)

    with MetricsLoggingContext(metrics=("dodgy",), interval=1, custom_metrics={"dodgy": dodgy_metric}):
        # Execute some operations
        print("Monitoring system metrics during operations...")
        time.sleep(20)
        # Operations are now being monitored
        # The thread will be stopped when exiting this block
