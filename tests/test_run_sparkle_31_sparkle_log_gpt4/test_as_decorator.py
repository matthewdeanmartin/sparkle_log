import logging
import time
from unittest.mock import MagicMock, patch

import pytest

from sparkle_log.as_decorator import monitor_metrics_on_call


# Sample function to be decorated
def test_func():
    return "Function has been run"


# Set up parameterization for different logging levels and expected outcomes
@pytest.mark.parametrize(
    "log_level, expected_start_thread",
    [
        (logging.INFO, True),  # Expect scheduler to start when logging level is INFO
        (logging.DEBUG, False),  # Expect scheduler not to start when logging level is DEBUG or lower than INFO
    ],
)
def test_monitor_metrics(log_level, expected_start_thread, tmp_path):
    with (
        patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor") as mock_isEnabledFor,
        patch("sparkle_log.as_decorator.run_scheduler") as _mock_run_scheduler,
        patch("threading.Thread.start") as mock_thread_start,
        patch("threading.Thread.join") as _mock_thread_join,
    ):

        # Mock the isEnabledFor to return True or False based on input log_level
        mock_isEnabledFor.return_value = log_level == logging.INFO

        # Decorate a test function with the monitor_metrics_on_call decorator
        @monitor_metrics_on_call(metrics=("cpu", "memory"), interval=1)
        def decorated_func():
            time.sleep(1)
            return "Decorated function called"

        # Call the decorated function
        result = decorated_func()

        # Assert the decorated function returns the correct value
        assert result == "Decorated function called"

        # Check if the thread start & scheduler functions were called or not based on expected behavior
        if expected_start_thread:
            mock_thread_start.assert_called_once()
            # start is mocked! It will never be called.
            # mock_run_scheduler.assert_called_once()
        else:
            mock_thread_start.assert_not_called()
            # vacuously true, we mocked start!
            # mock_run_scheduler.assert_not_called()


@pytest.fixture
def mock_run_scheduler(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("sparkle_log.as_decorator.run_scheduler", mock)
    return mock


@pytest.fixture
def mock_thread_start_stop(monkeypatch):
    start_mock = MagicMock()
    join_mock = MagicMock()
    monkeypatch.setattr("threading.Thread.start", start_mock)
    monkeypatch.setattr("threading.Thread.join", join_mock)
    return start_mock, join_mock


def raise_exception(*args, **kwargs):
    raise ValueError("Test exception")


def test_monitor_metrics_with_exception(mock_run_scheduler, mock_thread_start_stop):
    with patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor", return_value=True):

        @monitor_metrics_on_call(metrics=("cpu", "memory"), interval=10)
        def decorated_func():
            return raise_exception()

        # Check if the exception is raised and if the scheduler stops properly
        with pytest.raises(ValueError, match="Test exception"):
            decorated_func()

        # Check if the thread's start and join methods were called, indicating that cleanup was done
        start_mock, join_mock = mock_thread_start_stop
        start_mock.assert_called_once()
        join_mock.assert_called_once()


# Happy Path Test
def test_monitor_metrics_happy_path(mock_run_scheduler, mock_thread_start_stop):
    @monitor_metrics_on_call(metrics=("cpu", "memory"), interval=10)
    def sample_function(x, y):
        return x + y

    with patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor", return_value=True):
        assert sample_function(1, 2) == 3

    start_mock, join_mock = mock_thread_start_stop
    start_mock.assert_called_once()
    join_mock.assert_called_once()


# Edge Case: Logger disabled
def test_monitor_metrics_logger_disabled(mock_run_scheduler, mock_thread_start_stop):
    @monitor_metrics_on_call(metrics=("cpu", "memory"), interval=10)
    def sample_function():
        return "Logger not enabled"

    with patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor", return_value=False):
        assert sample_function() == "Logger not enabled"

    start_mock, join_mock = mock_thread_start_stop
    start_mock.assert_not_called()
    join_mock.assert_not_called()


# Edge Case: Function with args and kwargs
def test_monitor_metrics_with_args_kwargs(mock_run_scheduler, mock_thread_start_stop):
    @monitor_metrics_on_call(metrics=("cpu"), interval=5)
    def sample_function(a, b=0, **kwargs):
        return a + b + sum(kwargs.values())

    with patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor", return_value=True):
        assert sample_function(1, 2, c=3, d=4) == 10

    start_mock, join_mock = mock_thread_start_stop
    start_mock.assert_called_once()
    join_mock.assert_called_once()
