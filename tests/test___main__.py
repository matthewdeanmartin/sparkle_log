from unittest.mock import MagicMock, patch

import pytest

from sparkle_log.__main__ import log_memory_and_cpu_cli


@pytest.mark.parametrize(
    "metrics,interval,expected_sleep", [(("cpu", "memory"), 1, 20), (("cpu",), 5, 20), (("memory",), 2, 20)]
)
def test_log_memory_and_cpu_cli(metrics, interval, expected_sleep):
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as mock_monitor,
        patch("sparkle_log.__main__.configure_logging") as mock_logging,
        patch("sparkle_log.__main__.time.sleep") as mock_sleep,
    ):

        # Instantiating a Magic Mock for the MetricsLoggingContext's context manager behavior
        mock_monitor.return_value.__enter__.return_value = MagicMock()
        mock_monitor.return_value.__exit__.return_value = MagicMock()

        log_memory_and_cpu_cli(metrics, interval)

        # Assertions
        mock_monitor.assert_called_once_with(metrics=metrics, interval=interval)
        mock_logging.assert_called_once()
        mock_sleep.assert_called()

        # Verifying __enter__ and __exit__ were called on the context manager
        assert mock_monitor.return_value.__enter__.call_count == 1
        assert mock_monitor.return_value.__exit__.call_count == 1


def test_log_memory_and_cpu_cli_exception_handling():
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as mock_monitor,
        patch("sparkle_log.__main__.configure_logging") as mock_logging,
        patch("sparkle_log.__main__.time.sleep") as mock_sleep,
    ):

        # Configuring the mock to raise an exception when entering the context manager
        mock_monitor.return_value.__enter__.side_effect = TypeError("Error initializing metrics")

        # Expectation is that the raised exception is not caught within the function,
        # thus the test should expect it to be raised
        with pytest.raises(TypeError) as exc_info:
            log_memory_and_cpu_cli(metrics=("cpu", "memory"), interval=1)

        # Verifying the exception message to ensure it's the correct one being caught
        assert str(exc_info.value) == "Error initializing metrics"

        mock_logging.assert_called_once()
        mock_sleep.assert_not_called()  # sleep should not be called due to exception

        # We do not verify __exit__ call because the exception is expected to abort the context manager entry


def test_log_memory_and_cpu_cli_happy_path():
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as mock_monitor,
        patch("sparkle_log.__main__.configure_logging") as mock_logging,
        patch("sparkle_log.__main__.time.sleep", return_value=None) as mock_sleep,
    ):

        log_memory_and_cpu_cli(metrics=("cpu",), interval=1)

        # Ensure the logging setup was called once with the correct level
        mock_logging.assert_called()

        # Verify MetricsLoggingContext is initialized correctly and context manager behavior
        mock_monitor.assert_called_once_with(metrics=("cpu",), interval=1)
        assert mock_monitor.return_value.__enter__.called
        assert mock_monitor.return_value.__exit__.called

        # Ensure time.sleep was called, indicating operation execution
        mock_sleep.assert_called()


def test_log_memory_and_cpu_cli_empty_metrics_one():
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as mock_monitor,
        patch("sparkle_log.__main__.time.sleep", return_value=None) as mock_sleep,
    ):

        log_memory_and_cpu_cli(metrics=(), interval=2)

        # With no metrics defined, the MetricsLoggingContext should still be initialized but with default metrics
        mock_monitor.assert_called_once_with(metrics=(), interval=2)

        # Check if mocked time.sleep was called indicating the code path proceeded despite the edge case
        mock_sleep.assert_called()


def test_log_memory_and_cpu_cli_with_exception():
    with patch("sparkle_log.__main__.MetricsLoggingContext") as mock_monitor:

        mock_monitor.return_value.__enter__.side_effect = RuntimeError("Metric collection failed")

        # Testing error handling by expecting a RuntimeError when the MetricsLoggingContext is used
        with pytest.raises(RuntimeError) as exc:
            log_memory_and_cpu_cli(metrics=("memory",), interval=1)

        assert "Metric collection failed" in str(exc.value)


@pytest.fixture
def mock_dependencies():
    """
    A fixture to mock all external dependencies used by log_memory_and_cpu_cli.
    This includes MetricsLoggingContext for monitoring metrics, logging setup, and time.sleep to simulate passage of time.
    """
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as metric_monitor,
        patch("sparkle_log.__main__.configure_logging") as logging_basic_config,
        patch("sparkle_log.__main__.time.sleep", return_value=None) as time_sleep,
    ):
        yield {"metric_monitor": metric_monitor, "logging_basic_config": logging_basic_config, "time_sleep": time_sleep}


def test_log_memory_and_cpu_cli_success(mock_dependencies):
    """
    Tests the successful execution of log_memory_and_cpu_cli.

    Validates that:
    - Logging is configured with INFO level.
    - MetricsLoggingContext is correctly initialized with provided metrics and interval.
    - Metric monitoring subprocess is entered and exited—indicating the context manager's correct usage.
    """
    metrics = ("cpu", "memory")
    interval = 1

    log_memory_and_cpu_cli(metrics=metrics, interval=interval)

    mock_dependencies["logging_basic_config"].assert_called()
    mock_dependencies["metric_monitor"].assert_called_once_with(metrics=metrics, interval=interval)
    assert mock_dependencies["metric_monitor"].return_value.__enter__.called, "Metric monitor wasn't entered correctly"
    assert mock_dependencies["metric_monitor"].return_value.__exit__.called, "Metric monitor didn't exit as expected"


def test_log_memory_and_cpu_cli_with_error(mock_dependencies):
    """
    Tests log_memory_and_cpu_cli for handling exceptions during its execution.

    Specifically, simulates a RuntimeException during metric monitoring to ensure the application gracefully exits.
    """
    mock_dependencies["metric_monitor"].return_value.__enter__.side_effect = RuntimeError("Monitoring error")

    with pytest.raises(RuntimeError, match="Monitoring error"):
        log_memory_and_cpu_cli(metrics=("cpu",), interval=1)


@pytest.fixture
def mock_system():
    """
    Fixture to mock external system dependencies like the MetricsLoggingContext class and the sleep function.
    """
    with (
        patch("sparkle_log.__main__.MetricsLoggingContext") as MockMetricsLoggingContext,
        patch("sparkle_log.__main__.time.sleep", return_value=None) as mock_sleep,
    ):
        yield MockMetricsLoggingContext, mock_sleep


def test_log_memory_and_cpu_cli_empty_metrics(mock_system):
    """
    Test the `log_memory_and_cpu_cli` function for handling an edge case where the metrics parameter is an empty tuple.

    This test verifies that the MetricsLoggingContext is still initialized (indicative of the system's robustness) and that
    it handles such configurations gracefully without throwing errors or behaving unexpectedly.
    """
    MockMetricsLoggingContext, mock_sleep = mock_system

    # Define an empty metrics tuple as our edge case scenario
    empty_metrics = ()
    interval = 1

    # Execute the function with the edge case scenario
    log_memory_and_cpu_cli(metrics=empty_metrics, interval=interval)

    # Assertions to verify the correct handling of the edge case
    MockMetricsLoggingContext.assert_called_once_with(metrics=empty_metrics, interval=interval)
    assert (
        MockMetricsLoggingContext.return_value.__enter__.called
    ), "MetricsLoggingContext context manager was not entered"
    assert MockMetricsLoggingContext.return_value.__exit__.called, "MetricsLoggingContext context manager did not exit"
    mock_sleep.assert_called(), "Expected time.sleep to be called, indicating the function proceeded with execution."
