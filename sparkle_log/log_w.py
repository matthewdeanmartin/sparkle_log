"""
Log writer module, stateful and does not require a decorator or context manager.
"""

from __future__ import annotations

import logging
import statistics
from threading import Lock
from typing import cast

import psutil

from sparkle_log.custom_types import CustomMetricsCallBacks, GraphStyle, Metrics, NumberType
from sparkle_log.drive_space import get_free_percent_for_all_drives
from sparkle_log.graphs import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

# Global readings buffer. Each metric stores a rolling window of up to 30 samples.
READINGS: dict[str, list[NumberType]] = {}

# Protect READINGS from concurrent access (decorator + context manager can run in parallel threads).
_READINGS_LOCK = Lock()


def _ensure_metric_buffers(metrics: tuple[Metrics, ...], custom_metrics: CustomMetricsCallBacks) -> None:
    """Ensure all requested metric keys (including custom) exist in READINGS."""
    with _READINGS_LOCK:
        for m in metrics:
            READINGS.setdefault(m, [None] * 29)
        if custom_metrics:
            for name in custom_metrics.keys():
                READINGS.setdefault(name, [None] * 29)


def _append_metric_sample(name: str, value: NumberType) -> None:
    """Append a single sample to a metric window, trimming to last 30."""
    with _READINGS_LOCK:
        READINGS.setdefault(name, [None] * 29).append(value)
        if len(READINGS[name]) > 30:
            READINGS[name].pop(0)


def _gather_builtin_metrics(metrics: tuple[Metrics, ...]) -> None:
    """Sample built-in metrics (cpu/memory/drive) and append to buffers."""
    if "cpu" in metrics:
        # Interval None to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = cast(NumberType, psutil.cpu_percent(interval=interval))

        # First reading with interval=None can be unreliable (often 0).
        # Do not append that initial 0, but do not bail out either; let other metrics record.
        if not (reading == 0 and interval is None):
            _append_metric_sample("cpu", 0 if reading is None else int(reading))

    if "memory" in metrics:
        _append_metric_sample("memory", int(psutil.virtual_memory().percent))

    if "drive" in metrics:
        _append_metric_sample("drive", int(get_free_percent_for_all_drives()))


def _gather_custom_metrics(custom_metrics: CustomMetricsCallBacks) -> None:
    """Sample custom metric callables and append to buffers."""
    if not custom_metrics:
        return
    for name, fn in custom_metrics.items():
        try:
            reading = fn()
        except Exception:  # nosec - user-provided callback may fail; we insulate the logger
            reading = None
        _append_metric_sample(name, None if reading is None else int(reading))


def _pad(value: NumberType) -> str:
    """Pad the value with spaces."""
    if value is None:
        return "  "
    return str(int(value)).rjust(2)


def _log_metric_series(metric: str, series: list[NumberType], style: GraphStyle) -> None:
    """Compute stats and emit a single log line for one metric."""
    if all(v is None for v in series):
        return
    values_for_stats = [int(v) for v in series if v is not None]
    if not values_for_stats:
        return

    average = int(round(statistics.mean(values_for_stats), 0))
    minimum = _pad(min(values_for_stats))
    maximum = _pad(max(values_for_stats))
    current = _pad(series[-1])[-2:]

    # Keep the original human-readable format and sparkline.
    if metric == "cpu":
        GLOBAL_LOGGER.info(
            f"CPU   : {current}% "
            f"| min, mean, max ({minimum}, {average}, {maximum}) "
            f"| {sparkline(series, style)}"
        )
    elif metric == "memory":
        GLOBAL_LOGGER.info(
            f"Memory: {current}% "
            f"| min, mean, max ({minimum}, {average}, {maximum}) "
            f"| {sparkline(series, style)}"
        )
    elif metric == "drive":
        GLOBAL_LOGGER.info(
            f"Drive: {current}% " f"| min, mean, max ({minimum}, {average}, {maximum}) " f"| {sparkline(series, style)}"
        )
    else:
        GLOBAL_LOGGER.info(
            f"{metric}: {current}% "
            f"| min, mean, max ({minimum}, {average}, {maximum}) "
            f"| {sparkline(series, style)}"
        )


def log_system_metrics(
    metrics: tuple[Metrics, ...],
    style: GraphStyle = "bar",
    custom_metrics: CustomMetricsCallBacks = None,
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

    # Ensure buffers exist for all requested metrics before sampling.
    _ensure_metric_buffers(metrics, custom_metrics)

    # Gather samples.
    _gather_custom_metrics(custom_metrics)
    _gather_builtin_metrics(metrics)

    # Trim windows once after sampling (defensive; individual appends already trim).
    with _READINGS_LOCK:
        for values in READINGS.values():
            if len(values) > 30:
                values.pop(0)

        # Emit logs only for requested metrics (built-ins or custom names that were requested).
        for metric, series in READINGS.items():
            if metric not in metrics and (not custom_metrics or metric not in custom_metrics):
                continue
            _log_metric_series(metric, series, style)
