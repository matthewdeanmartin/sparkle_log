from unittest.mock import MagicMock, patch

import pytest

from sparkle_log.graphs import GLOBAL_LOGGER
from sparkle_log.log_writer import READINGS, log_system_metrics

# Importing directly for mocking, even if not directly used in tests to enhance clarity


@pytest.mark.parametrize(
    "metrics,expected_calls",
    [
        (("cpu",), 1),
        (("memory",), 1),
        (("cpu", "memory"), 2),
    ],
)
def test_log_system_metrics(metrics, expected_calls):
    with (
        patch.object(GLOBAL_LOGGER, "isEnabledFor", return_value=True) as mock_is_enabled,
        patch.object(GLOBAL_LOGGER, "info") as mock_info,
        patch("psutil.cpu_percent", return_value=50) as _mock_cpu_percent,
        patch("psutil.virtual_memory", return_value=MagicMock(percent=70)) as _mock_virtual_memory,
        patch("sparkle_log.ui.sparkline", return_value="spark"),
    ):
        for _key, value in READINGS.items():
            value.clear()
        log_system_metrics(metrics)

        assert mock_is_enabled.called
        # Ensure that based on input metrics, logging happens the expected number of times
        assert mock_info.call_count == expected_calls

        # Validate that the logging messages include specific text based on the metrics
        for metric in metrics:
            if metric == "cpu":
                mock_info.assert_any_call("CPU   :   50% | ▄ | min, mean, max (50, 50, 50)")
            elif metric == "memory":
                mock_info.assert_any_call("Memory:   70% | ▄ | min, mean, max (70, 70, 70)")


# Considering there's no explicit exception handling in the provided function,
# this is hypothetical and assumes we want to check if the function can skip
# over exceptions raised by psutil functions without breaking.

# def test_log_system_metrics_with_exceptions():
#     with patch.object(GLOBAL_LOGGER, 'isEnabledFor', return_value=True) as mock_is_enabled_for, \
#          patch.object(GLOBAL_LOGGER, 'info') as mock_info:
#         # Simulate `cpu_percent` raising an exception
#         with patch('psutil.cpu_percent', side_effect=Exception("CPU reading failed")):
#             log_system_metrics(("cpu",))
#
#         # Simulate `virtual_memory().percent` raising an exception
#         with patch('psutil.virtual_memory', side_effect=Exception("Memory reading failed")):
#             log_system_metrics(("memory",))

# In a real-world application, you would check here if the function
# handles the exception (e.g., by logging an error) without interrupting
# the flow of the program. However, based on the provided code, we cannot
# assert on exception handling behavior.

# Hypothetical assertion: If there were a try-except block inside
# `log_system_metrics` that catches exceptions and logs an error message,
# we could assert if `mock_info` was called with an appropriate error message.
# Example (this won't work with the current function as it does not catch exceptions):
# mock_info.assert_called_with("An error occurred while reading system metrics.")

# This test will not work as expected with the current implementation of `log_system_metrics`
# since it does not handle exceptions. Adjusting the actual function to handle exceptions
# would make this approach valid.


@pytest.fixture(autouse=True)
def clear_readings():
    """Fixture to clear the READINGS dictionary before each test case."""
    READINGS["cpu"] = []
    READINGS["memory"] = []


def test_log_cpu_metrics_happy_path():
    with (
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True),
        patch("sparkle_log.log_writer.sparkline", return_value="[sparkline]"),
        patch("psutil.cpu_percent", return_value=20),
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.info") as mock_info,
    ):

        log_system_metrics(("cpu",))

        assert READINGS["cpu"][-1] == 20
        mock_info.assert_called_once_with("CPU   :   20% | [sparkline] | min, mean, max (20, 20, 20)")


def test_log_memory_metrics_happy_path():
    for key, _value in READINGS.items():
        READINGS[key].clear()
    with (
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True),
        patch("sparkle_log.log_writer.sparkline", return_value="[sparkline]"),
        patch("sparkle_log.log_writer.psutil.virtual_memory", return_value=MagicMock(percent=50)),
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.info") as mock_info,
    ):

        log_system_metrics(("memory",))

        assert READINGS["memory"][-1] == 50
        mock_info.assert_called_once_with("Memory:   50% | [sparkline] | min, mean, max (50, 50, 50)")


def test_no_logging_if_not_enabled():
    with (
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=False),
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.info") as mock_info,
    ):

        log_system_metrics(("cpu", "memory"))

        mock_info.assert_not_called()


def test_cpu_metrics_first_call_zero_value():
    with (
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True),
        patch("psutil.cpu_percent", return_value=0),
        patch("sparkle_log.log_writer.GLOBAL_LOGGER.info") as mock_info,
    ):

        log_system_metrics(("cpu",))

        # No logging should occur for the first zero value with interval=None
        mock_info.assert_not_called()


# Error condition tests are omitted due to the nature of provided function which lacks explicit exception handling.
