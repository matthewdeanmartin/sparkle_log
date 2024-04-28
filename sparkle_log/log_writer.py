"""
Log writer module, stateful and does not require a decorator or context manager.
"""

import logging
import statistics
from typing import cast

import psutil

from sparkle_log.custom_types import CustomMetricsCallBacks, GraphStyle, Metrics, NumberType
from sparkle_log.drive_space import get_free_percent_for_all_drives
from sparkle_log.graphs import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[NumberType]] = {}


def log_system_metrics(
    metrics: tuple[Metrics, ...], style: GraphStyle = "bar", custom_metrics: CustomMetricsCallBacks = None
) -> None:
    """
    Log system metrics.

    Args:
        metrics: A tuple of metrics to log.
        style: The style of the sparkline.
        custom_metrics: A dictionary of custom metrics to log.
    """
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if not READINGS:
        for initial_metric in metrics:
            READINGS[initial_metric] = [None] * 29

    if custom_metrics:
        for custom_metric in custom_metrics:
            reading = custom_metrics[custom_metric]()
            try:
                if reading is None:
                    READINGS[custom_metric].append(None)
                else:
                    READINGS[custom_metric].append(int(reading))
            except KeyError:
                READINGS[custom_metric] = [None] * 29
                if reading is None:
                    READINGS[custom_metric].append(None)
                else:
                    READINGS[custom_metric].append(int(reading))

    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = cast(NumberType, psutil.cpu_percent(interval=interval))

        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        if reading is None:
            READINGS["cpu"].append(0)
        else:
            READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    if "drive" in metrics:
        READINGS["drive"].append(int(get_free_percent_for_all_drives()))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        if all(_ is None for _ in value):
            continue
        values_for_stats = [_ for _ in value if _ is not None]
        average = int(round(statistics.mean(values_for_stats), 0))

        def pad(value: NumberType) -> str:
            """Pad the value with spaces."""
            if value is None:
                return "  "
            return str(int(value)).rjust(2)

        minimum = pad(min(values_for_stats))
        maximum = pad(max(values_for_stats))
        metric_formatted = pad(value[-1])[-2:]
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU   : {metric_formatted}% "
                f"| min, mean, max ({minimum}, {average}, {maximum}) "
                f"| {sparkline(value, style)}"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {metric_formatted}% "
                f"| min, mean, max ({minimum}, {average}, {maximum}) "
                f"| {sparkline(value, style)}"
            )
        elif metric == "drive":
            GLOBAL_LOGGER.info(
                f"Drive: {metric_formatted}% "
                f"| min, mean, max ({minimum}, {average}, {maximum}) "
                f"| {sparkline(value, style)}"
            )
        else:
            GLOBAL_LOGGER.info(
                f"{metric}: {metric_formatted}% "
                f"| min, mean, max ({minimum}, {average}, {maximum}) "
                f"| {sparkline(value, style)}"
            )
