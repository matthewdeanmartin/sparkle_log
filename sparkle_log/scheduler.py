"""Trigger logging on a schedule."""

import time
from threading import Event

import schedule

from sparkle_log.custom_types import CustomMetricsCallBacks, GraphStyle, Metrics
from sparkle_log.log_writer import log_system_metrics


def run_scheduler(
    stop_event: Event,
    metrics: tuple[Metrics, ...],
    seconds: int,
    style: GraphStyle = "bar",
    custom_metrics: CustomMetricsCallBacks = None,
):
    """Run scheduled tasks until the stop_event is set."""
    schedule.every(seconds).seconds.do(lambda: log_system_metrics(metrics, style, custom_metrics))

    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)
