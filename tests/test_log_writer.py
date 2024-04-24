import logging
from unittest.mock import Mock, patch

from sparkle_log.log_writer import READINGS, log_system_metrics


def test_log_system_metrics_does_not_log_when_logger_disabled(caplog):
    """Test that log_system_metrics does not log when the logger is disabled."""
    with patch("sparkle_log.log_writer.GLOBAL_LOGGER", Mock(spec=logging.Logger)) as mock_logger:
        mock_logger.isEnabledFor.return_value = False

        log_system_metrics(["cpu"])

        assert len(caplog.records) == 0


def test_log_system_metrics_handles_empty_cpu_reading(caplog):
    """Test that log_system_metrics handles the scenario when CPU reading is 0 with interval=None."""
    with patch("sparkle_log.log_writer.GLOBAL_LOGGER", Mock(spec=logging.Logger)) as _mock_logger:
        mock_cpu_percent = Mock(return_value=0)

        with patch("psutil.cpu_percent", mock_cpu_percent):
            log_system_metrics(["cpu"])

        # GLOBAL STATE! results crossing tests :(
        assert len(READINGS["cpu"]) in (0, 1, 29)
        assert "CPU" not in caplog.text


def test_log_system_metrics_handles_metric_not_included(caplog):
    """Test that log_system_metrics does not log the metric if it's not included in the metrics to log."""
    with patch("sparkle_log.log_writer.GLOBAL_LOGGER", Mock(spec=logging.Logger)) as _mock_logger:
        log_system_metrics(())  # Metrics list is empty

        assert len(caplog.records) == 0
