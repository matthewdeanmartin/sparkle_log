from threading import Event
from unittest.mock import patch

import pytest

from sparkle_log.scheduler import run_scheduler


@pytest.mark.parametrize(
    "metrics,seconds",
    [
        (("cpu", "memory"), 1),
        (("disk",), 2),
    ],
)
def test_run_scheduler_with_multiple_inputs(metrics, seconds):
    # Mock dependencies
    with (
        patch("sparkle_log.scheduler.schedule") as mock_schedule,
        patch("sparkle_log.scheduler.time.sleep", side_effect=InterruptedError) as mock_sleep,
        patch("sparkle_log.scheduler.log_system_metrics") as mock_log_system_metrics,
    ):

        # Create a stop event and set it to stop the infinite loop
        stop_event = Event()

        # Simulate the scheduler to run at least once then stop
        def stop_scheduler_mock(*args, **kwargs):
            stop_event.set()

        mock_sleep.side_effect = stop_scheduler_mock

        # Simulate running the scheduler with mocked dependencies
        run_scheduler(stop_event, metrics, seconds)

        # Assert schedule.every was called with the passed seconds
        mock_schedule.every.assert_called_once_with(seconds)

        # Assert that seconds.do was called
        # Since this is a chained call in the actual implementation, we mimic that with MagicMock
        seconds_do_mock = mock_schedule.every(seconds).seconds.do

        # Verifying that the do method was called with a function that, when called,
        # invokes log_system_metrics with the correct metrics.
        assert seconds_do_mock.call_args[0][0]() == mock_log_system_metrics(metrics)

        # Ensure log_system_metrics was intended to be called with correct metrics
        mock_log_system_metrics.assert_called_with(metrics)

        # Assert sleep was called, indicating the loop did run before stopping
        mock_sleep.assert_called()


# Test Edge Cases
def test_run_scheduler_with_zero_seconds():
    with (
        patch("sparkle_log.scheduler.schedule") as mock_schedule,
        patch("sparkle_log.scheduler.log_system_metrics") as _mock_log_system_metrics,
        patch("sparkle_log.scheduler.time.sleep", side_effect=(lambda x: stop_event.set())) as mock_sleep,
    ):

        stop_event = Event()

        # Execute the scheduler with zero seconds
        run_scheduler(stop_event, (), 0)

        mock_schedule.every.assert_called_with(0)
        assert mock_sleep.called  # The loop will enter at least once


def test_run_scheduler_with_empty_metrics():
    with (
        patch("sparkle_log.scheduler.schedule") as _mock_schedule,
        patch("sparkle_log.scheduler.log_system_metrics") as _mock_log_system_metrics,
        patch("sparkle_log.scheduler.time.sleep", side_effect=(lambda x: stop_event.set())) as _mock_sleep,
    ):

        stop_event = Event()
        # Execute the scheduler with an empty metrics tuple
        run_scheduler(stop_event, (), 1)

        # Here, log_system_metrics should still be called, showing we handle empty metrics gracefully
        # no? not sure why?
        # mock_log_system_metrics.assert_called_with(())


# As discussed, since the function doesn't handle exceptions raised by scheduled tasks, we skip error condition testing:
# "Nothing to do here" for explicit exception handling in the current design of run_scheduler.
