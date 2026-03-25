"""Tests that demonstrate bugs found in the sparkle_log codebase."""

import threading
import time
from unittest.mock import patch

import pytest
import schedule as schedule_mod

from sparkle_log.log_writer import _log_metric_series, _pad
from sparkle_log.scheduler import run_scheduler
from sparkle_log.ui import sparkline, sparkline_it


# ---------------------------------------------------------------------------
# Bug 1: sparkline_it crashes with ValueError on all-None data
# File: sparkle_log/ui.py, lines 43-44
# When all values are None, noneless_data is empty and max()/min() raise
# ValueError: max() arg is an empty sequence
# ---------------------------------------------------------------------------
class TestBug1AllNoneData:
    def test_sparkline_it_all_none_raises_valueerror(self):
        """sparkline_it crashes when given all-None data."""
        symbols = ["_", "-", "^"]
        with pytest.raises(ValueError, match="max.*iterable argument is empty"):
            sparkline_it([None, None, None], symbols)

    def test_sparkline_all_none_faces_style_crashes(self):
        """Sparkline with faces style crashes on all-None data."""
        with pytest.raises(ValueError, match="max.*iterable argument is empty"):
            sparkline([None, None, None], "faces")

    def test_sparkline_it_empty_list(self):
        """sparkline_it crashes on empty list too."""
        symbols = ["_", "-", "^"]
        with pytest.raises(ValueError):
            sparkline_it([], symbols)


# ---------------------------------------------------------------------------
# Bug 2: sparkline_it returns all spaces when all values are identical
# File: sparkle_log/ui.py, lines 47-48
# When range_val == 0 (all values are the same), the function returns spaces
# instead of a meaningful representation. If you're monitoring memory at a
# steady 46%, you'd expect to see actual graph characters, not blanks.
# ---------------------------------------------------------------------------
class TestBug2AllSameValues:
    def test_sparkline_it_all_same_returns_spaces(self):
        """When all values are equal, sparkline_it returns only spaces."""
        symbols = ["_", "-", "^", "~"]
        result = sparkline_it([5, 5, 5, 5], symbols)
        # Bug: returns "    " (4 spaces) instead of something visible
        assert result == "    ", "Demonstrating the bug: all spaces returned"

    def test_sparkline_faces_all_same_returns_spaces(self):
        """Faces sparkline with constant data returns invisible output."""
        result = sparkline([46, 46, 46, 46], "faces")
        # Bug: returns "    " — the user sees nothing in their log
        assert result.strip() == "", "Demonstrating the bug: no visible output"


# ---------------------------------------------------------------------------
# Bug 3: sparkline() bar style has fragile for/return pattern
# File: sparkle_log/ui.py, lines 17-19
# The `for line in sparklines.sparklines(numbers): return line` pattern
# means if the iterable is empty, the function falls through the if/elif
# chain without hitting `return ""` — it implicitly returns None.
# ---------------------------------------------------------------------------
class TestBug3BarStyleFallthrough:
    def test_sparkline_bar_empty_iterable_falls_through(self):
        """When sparklines lib returns empty iterable, the 'bar' branch
        doesn't return anything — execution falls through to `return ""`.
        This means bar style silently returns empty string instead of
        raising an error or returning a meaningful fallback. The `for/return`
        pattern is misleading and fragile.
        """
        with patch("sparkle_log.ui.sparklines.sparklines", return_value=iter([])):
            result = sparkline([1, 2, 3], "bar")
            # Bug: the for-loop doesn't execute, so bar branch produces ""
            # via fallthrough — not an explicit return from the bar branch.
            # If someone adds an else clause or reorders, this breaks silently.
            assert result == ""

    def test_sparkline_bar_none_in_data_may_crash(self):
        """Passing None values to sparklines lib (bar style) may cause issues
        depending on the sparklines library version.
        """
        # This exercises the bar path with None values — the sparklines lib
        # receives raw None values with no filtering, unlike sparkline_it.
        try:
            result = sparkline([None, None, 5, None], "bar")
            # If it doesn't crash, we at least confirm it ran
            assert isinstance(result, str)
        except (TypeError, ValueError):
            # Bug: None values are passed unfiltered to sparklines library
            pass


# ---------------------------------------------------------------------------
# Bug 4: scheduler uses global schedule — concurrent instances interfere
# File: sparkle_log/scheduler.py, line 23
# schedule.every() uses the module-level default scheduler. Multiple
# concurrent context managers/decorators share it, causing job leakage.
# Jobs are also never cleared when the stop event is set.
# ---------------------------------------------------------------------------
class TestBug4GlobalScheduler:
    def test_scheduler_uses_global_schedule(self):
        """Jobs accumulate in the global scheduler and are never cleaned up."""
        # Clear any pre-existing jobs
        schedule_mod.clear()
        initial_jobs = len(schedule_mod.jobs)

        stop_event = threading.Event()

        # Start scheduler in a thread
        t = threading.Thread(
            target=run_scheduler,
            args=(stop_event, ("cpu",), 60, "bar", None),
        )
        t.start()

        # Let it register the job
        time.sleep(0.1)

        # Job was registered globally
        jobs_after_start = len(schedule_mod.jobs)
        assert jobs_after_start > initial_jobs, "Job should be registered"

        # Stop the scheduler
        stop_event.set()
        t.join(timeout=5)

        # Bug: job is NEVER removed from the global scheduler
        jobs_after_stop = len(schedule_mod.jobs)
        assert jobs_after_stop > initial_jobs, (
            "Demonstrating the bug: job remains in global scheduler after stop"
        )

        # Clean up for other tests
        schedule_mod.clear()

    def test_two_schedulers_share_global_state(self):
        """Two concurrent schedulers interfere via the shared global scheduler."""
        schedule_mod.clear()

        stop1 = threading.Event()
        stop2 = threading.Event()

        t1 = threading.Thread(
            target=run_scheduler,
            args=(stop1, ("cpu",), 60, "bar", None),
        )
        t2 = threading.Thread(
            target=run_scheduler,
            args=(stop2, ("memory",), 60, "bar", None),
        )

        t1.start()
        t2.start()

        time.sleep(0.1)

        # Bug: both jobs are in the same global scheduler
        assert len(schedule_mod.jobs) == 2, (
            "Demonstrating the bug: both schedulers share the global job list"
        )

        stop1.set()
        stop2.set()
        t1.join(timeout=5)
        t2.join(timeout=5)

        # Bug: both jobs still linger
        assert len(schedule_mod.jobs) == 2, (
            "Demonstrating the bug: jobs are never cleaned up"
        )

        schedule_mod.clear()


# ---------------------------------------------------------------------------
# Bug 5: _pad truncates values >= 100 and current display is wrong
# File: sparkle_log/log_writer.py, lines 81, 95
# _pad uses rjust(2) — fine for 0-99, but 100 becomes "100" (3 chars).
# Then line 95 does _pad(series[-1])[-2:] which slices "100" to "00".
# CPU/memory are percentages (0-100) so 100% is a valid value.
# ---------------------------------------------------------------------------
class TestBug5PadTruncation:
    def test_pad_value_100(self):
        """_pad(100) returns '100' which is 3 chars, not 2."""
        result = _pad(100)
        # rjust(2) on "100" is still "100" (no padding needed, already wider)
        assert result == "100"
        assert len(result) == 3, "3 chars, but display expects 2-char field"

    def test_current_display_truncates_100(self):
        """The current value display slices '100' to '00'."""
        series = [None] * 29 + [100]
        # Reproducing what _log_metric_series does at line 95:
        current = _pad(series[-1])[-2:]
        assert current == "00", "Demonstrating the bug: 100% displays as 00%"

    def test_log_metric_series_shows_truncated_100(self):
        """Full integration: 100% CPU shows as '00%' in the log line."""
        series = [100] * 30
        with patch("sparkle_log.log_writer.GLOBAL_LOGGER") as mock_logger:
            mock_logger.isEnabledFor.return_value = True
            _log_metric_series("cpu", series, "bar")

            call_args = mock_logger.info.call_args[0][0]
            # Bug: the log line contains "00%" instead of "100%"
            assert "00%" in call_args, f"Demonstrating the bug: {call_args!r}"
            assert "100%" not in call_args, f"100%% should NOT appear: {call_args!r}"
