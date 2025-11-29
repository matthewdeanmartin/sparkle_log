import asyncio
import logging
import types
from concurrent.futures import ThreadPoolExecutor

import pytest

from sparkle_log import log_writer as LW
from sparkle_log import ui
from sparkle_log.as_context_manager import MetricsLoggingContext
from sparkle_log.as_decorator import monitor_metrics_on_call
from sparkle_log.graphs import GLOBAL_LOGGER

# ---------- Fixtures ----------


@pytest.fixture(autouse=True)
def _reset_readings_and_logger():
    # Save & restore logger level
    prev_level = GLOBAL_LOGGER.level
    # Enable INFO so logging path is active by default
    GLOBAL_LOGGER.setLevel(logging.INFO)
    # Reset global buffers
    LW.READINGS.clear()
    yield
    LW.READINGS.clear()
    GLOBAL_LOGGER.setLevel(prev_level)


# ---------- Tests ----------


@pytest.mark.asyncio
async def test_async_decorator_no_logging():
    """
    Ensure the async decorator awaits the coroutine and returns its value
    when INFO logging is disabled (regression test for missing 'await').
    """
    GLOBAL_LOGGER.setLevel(logging.WARNING)  # disables INFO

    @monitor_metrics_on_call(metrics=("cpu",), interval=1)
    async def work(x: int) -> int:
        await asyncio.sleep(0)
        return x * 2

    assert await work(21) == 42


def test_sparkline_bar_all_none(monkeypatch):
    """
    'bar' style must tolerate None values (pre-filled buffers).
    We mock sparklines.sparklines to avoid external dependency variability.
    """
    fake_module = types.SimpleNamespace(sparklines=lambda nums: ["OK"])  # return a single rendered line
    monkeypatch.setattr(ui, "sparklines", fake_module, raising=True)

    result = ui.sparkline([None, None, None, None, None], style="bar")
    assert isinstance(result, str) and result == "OK"


def test_first_cpu_none_allows_other_metrics(monkeypatch):
    """
    When psutil.cpu_percent(interval=None) returns 0 on the first tick,
    CPU should be skipped but memory/drive/custom should still append.
    """
    # psutil.cpu_percent -> 0 (simulate initial unreliable read)
    monkeypatch.setattr(LW.psutil, "cpu_percent", lambda interval=None: 0)

    # psutil.virtual_memory().percent -> 55
    class _VM:
        percent = 55

    monkeypatch.setattr(LW.psutil, "virtual_memory", lambda: _VM())

    # drive free percent -> 66
    monkeypatch.setattr(LW, "get_free_percent_for_all_drives", lambda: 66)

    # Ensure buffers created: 29 Nones each initially
    LW.log_system_metrics(metrics=("cpu", "memory", "drive"), style="bar", custom_metrics=None)

    # CPU should have skipped append (len 29), memory/drive should have appended (len 30)
    assert len(LW.READINGS["cpu"]) == 29
    assert len(LW.READINGS["memory"]) == 30 and LW.READINGS["memory"][-1] == 55
    assert len(LW.READINGS["drive"]) == 30 and LW.READINGS["drive"][-1] == 66


def test_concurrent_calls_lock(monkeypatch):
    """
    Concurrent invocations should not race or raise KeyError;
    memory window must cap at 30 samples.
    """

    class _VM:
        percent = 42

    monkeypatch.setattr(LW.psutil, "virtual_memory", lambda: _VM())

    def call():
        LW.log_system_metrics(metrics=("memory",), style="bar", custom_metrics=None)

    with ThreadPoolExecutor(max_workers=8) as ex:
        for _ in range(20):
            ex.submit(call)

    assert "memory" in LW.READINGS
    assert 1 <= len(LW.READINGS["memory"]) <= 30
    # All entries should be ints (no None) after first append
    assert all(isinstance(v, int) for v in LW.READINGS["memory"] if v is not None)


def test_metric_validation_message():
    """
    Supplying an unknown metric without providing a matching custom metric
    should raise a clear, actionable TypeError.
    """
    with pytest.raises(TypeError) as ei:
        MetricsLoggingContext(metrics=("bogus",), interval=1, style="bar", custom_metrics=None)
    msg = str(ei.value)
    assert "Unexpected metric" in msg
