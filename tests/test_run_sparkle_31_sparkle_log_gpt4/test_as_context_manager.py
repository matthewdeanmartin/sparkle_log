from unittest.mock import MagicMock, Mock, patch

import pytest

from sparkle_log.as_context_manager import MetricsLoggingContext


@pytest.mark.parametrize(
    "log_enabled, expected_thread_start",
    [
        (True, True),  # Test Case: Logger enabled, expect thread to start
        (False, False),  # Test Case: Logger not enabled, expect thread not to start
    ],
)
def test_MetricsLoggingContext_context_management(log_enabled, expected_thread_start):
    with patch("sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor") as mock_isEnabledFor:
        # Mock GLOBAL_LOGGER to control isEnabledFor behavior
        mock_isEnabledFor.return_value = log_enabled

        # Mock run_scheduler to observe if it's called
        with patch("sparkle_log.as_context_manager.Thread") as mock_thread:
            mock_thread_instance = Mock()
            mock_thread.return_value = mock_thread_instance

            # Using MetricsLoggingContext as context manager to trigger __enter__
            with MetricsLoggingContext(metrics=("cpu",), interval=5) as _monitor:
                pass

            # Check that the thread's start method is called if log is enabled
            if expected_thread_start:
                mock_thread_instance.start.assert_called_once()
            else:
                mock_thread_instance.start.assert_not_called()

    # After the context block exits, __exit__ is called, testing it's behaviour
    # mock has to act like a thread to get joined.
    # mock_thread_instance.join.assert_called_with()


class SomeTestException(Exception):
    """Custom exception for testing purposes."""


def test_MetricsLoggingContext_exception_handling():
    with (
        patch("sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=True),
        patch("sparkle_log.as_context_manager.Thread") as mock_thread,
    ):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Simulate an exception within the with block
        try:
            with MetricsLoggingContext(metrics=("cpu",), interval=5) as _monitor:
                raise SomeTestException("Testing exception handling.")
        except SomeTestException:
            pass  # Exception is expected, continue to check if cleanup occurs

        # Verify that despite the exception, the cleanup process (thread join) is still attempted
        mock_thread_instance.join.assert_called_once()


def test_metric_monitor_happy_path():
    """Test the expected behavior when everything runs correctly."""
    with (
        patch("sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=True),
        patch("sparkle_log.as_context_manager.Thread") as mock_thread,
    ):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        with MetricsLoggingContext(metrics=("cpu", "memory"), interval=10) as _monitor:
            pass

        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        mock_thread_instance.join.assert_called_once()


def test_metric_monitor_logger_disabled():
    """Test behavior when logging is disabled for INFO level."""
    with patch("sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=False):
        with MetricsLoggingContext(metrics=("cpu",), interval=5) as monitor:
            pass

        # Expect that the scheduler thread was never started as logging is not enabled.
        assert monitor.scheduler_thread is None


def test_metric_monitor_usage_outside_context_manager():
    """Testing misuse of the context manager (e.g., not using the 'with' statement)."""
    # No mocking required as this tests misuse of the API directly
    monitor = MetricsLoggingContext(metrics=("cpu",), interval=5)
    # Assert the scheduler thread was not started as the context manager protocol was not entered.
    assert monitor.scheduler_thread is None
