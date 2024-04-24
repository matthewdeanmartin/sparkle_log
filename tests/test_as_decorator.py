from unittest.mock import Mock, patch

import pytest

from sparkle_log.as_decorator import monitor_metrics_on_call


@pytest.fixture
def mock_global_logger_enabled():
    with patch("sparkle_log.as_decorator.GLOBAL_LOGGER.isEnabledFor") as mock_enabled:
        yield mock_enabled


@pytest.fixture
def mock_thread():
    with patch("sparkle_log.as_decorator.Thread") as mock_thread:
        yield mock_thread


@pytest.fixture
def mock_run_scheduler():
    with patch("sparkle_log.as_decorator.run_scheduler") as mock_scheduler:
        yield mock_scheduler


def test_monitor_metrics_disabled_logger(mock_global_logger_enabled, mock_thread, mock_run_scheduler):
    mock_global_logger_enabled.return_value = False
    mock_func = Mock()

    decorated_func = monitor_metrics_on_call()(mock_func)
    decorated_func()

    assert not mock_thread.called
    assert not mock_run_scheduler.called
    assert mock_func.called


def test_monitor_metrics_error_condition(mock_global_logger_enabled, mock_thread, mock_run_scheduler):
    mock_global_logger_enabled.side_effect = TypeError("Error")
    mock_func = Mock()

    decorated_func = monitor_metrics_on_call()(mock_func)
    with pytest.raises(TypeError):
        decorated_func()

    assert not mock_thread.called
    assert not mock_run_scheduler.called
    assert not mock_func.called


def test_monitor_metrics_skips_scheduler_when_logger_disabled(
    mock_global_logger_enabled, mock_thread, mock_run_scheduler
):
    """Test that monitor_metrics_on_call skips the scheduler when the global logger is disabled."""
    mock_global_logger_enabled.return_value = False
    mock_func = Mock()

    decorated_func = monitor_metrics_on_call()(mock_func)
    decorated_func()

    assert not mock_thread.called
    assert not mock_run_scheduler.called
    assert mock_func.called


def test_monitor_metrics_handles_exception_from_logger_enabled_check(
    mock_global_logger_enabled, mock_thread, mock_run_scheduler
):
    """Test that monitor_metrics_on_call handles an exception raised during logger enabled checking."""
    mock_global_logger_enabled.side_effect = TypeError("Error")
    mock_func = Mock()

    decorated_func = monitor_metrics_on_call()(mock_func)
    with pytest.raises(TypeError):
        decorated_func()

    assert not mock_thread.called
    assert not mock_run_scheduler.called
    assert not mock_func.called
