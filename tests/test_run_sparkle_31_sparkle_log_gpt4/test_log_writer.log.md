System: You are an excellent python pytest unit test engineer. We are writing pytest tests.

First, begin by looking for bugs. There might not be any bugs. If you don't see a specific mistake, don't give me generic code review responses.

Having looked for bugs, explain how you're going to write the unit test, write the pytest test as per usual. Don't 
forget to write test functions! Use mocks or fakes as needed, but don't reimplement the code under test- that already 
exists.

## Tooling
Use pytest style testing. Use unittest.mock for mocking. pytest, unittest.mock

Do not, under any circumstances, use unittest.TestCase.


## Coding preferences
- The target python version is 3.10
- Make sure code is cross-platform and does not use linux-only modules. 
- Prefer pathlib.Path whenever possible. 
- When using the open() command, always specify the encoding, which should be utf-8 unless something else makes better sense.

## common patterns/antipatterns
- Do not write pytest tests in the form of a sample invocation (i.e. not wrapped in a function), but do write in the 
  body of a `def test_...` function
- Do make use of the tmp_path fixture for writing files. Do not unnecessarily mock `open` to avoid writing files, 
  just write an example file to tmp_path.

```
from tests.env_util import temporary_env_var

with temporary_env_var("NAME", "mock_value", "NAME2", "mock_value2"):
	assert os.environ["NAME"] == "mock_value"
	assert os.environ["NAME2"] == "mock_value2"
```

Library is named sparkle_log.
User: 
Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py

Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py
Module Name: sparkle_log.log_writer
```python
import logging
import statistics

import psutil

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[int]] = {"cpu": [], "memory": []}


def log_system_metrics(metrics: tuple[str, ...]) -> None:
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = psutil.cpu_percent(interval=interval)
        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        average = round(statistics.mean(value), 1)
        minimum = min(value)
        maximum = max(value)
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {value[-1]}% | {sparkline(value)}, {value} | min, mean, max ({minimum}, {average}, {maximum})"
            )
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/ui.py
def sparkline(numbers: list[int]) -> str:
    """Generate a simple sparkline string for a list of integers."""
    ...
```


Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py

Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py
Module Name: sparkle_log.log_writer
```python
import logging
import statistics

import psutil

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[int]] = {"cpu": [], "memory": []}


def log_system_metrics(metrics: tuple[str, ...]) -> None:
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = psutil.cpu_percent(interval=interval)
        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        average = round(statistics.mean(value), 1)
        minimum = min(value)
        maximum = max(value)
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {value[-1]}% | {sparkline(value)}, {value} | min, mean, max ({minimum}, {average}, {maximum})"
            )
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/ui.py
def sparkline(numbers: list[int]) -> str:
    """Generate a simple sparkline string for a list of integers."""
    ...
```


Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py

Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py
Module Name: sparkle_log.log_writer
```python
import logging
import statistics

import psutil

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[int]] = {"cpu": [], "memory": []}


def log_system_metrics(metrics: tuple[str, ...]) -> None:
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = psutil.cpu_percent(interval=interval)
        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        average = round(statistics.mean(value), 1)
        minimum = min(value)
        maximum = max(value)
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {value[-1]}% | {sparkline(value)}, {value} | min, mean, max ({minimum}, {average}, {maximum})"
            )
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/ui.py
def sparkline(numbers: list[int]) -> str:
    """Generate a simple sparkline string for a list of integers."""
    ...
```



Please write a parameterized unit test using pytest pytest, unittest.mock. This test should check multiple inputs 
and their expected outputs for a single function. Utilize unittest.mock to simulate any external interactions and Path for handling file paths. This will help us ensure our function behaves correctly under various conditions.

Assistant: Given the information and requirements for the `log_system_metrics` function within the `sparkle_log.log_writer` module, we will focus on parameterizing a test for varying conditions, specifically different metric inputs ("cpu", "memory", and combinations thereof), and verify whether the logging happens as expected based on the `GLOBAL_LOGGER`'s configuration and the readings from the `psutil` library.

### Steps for Writing the Parameterized Unit Test

1. **Mock Dependencies**: 
    - Mock `GLOBAL_LOGGER` to control and assert logging behavior.
    - Mock `psutil.cpu_percent` and `psutil.virtual_memory` to simulate system readings.
    - We won't need to mock file paths or use `Path` as the function in question doesn't directly interact with the filesystem.

2. **Parameterize Inputs**: We will parameterize the test with different metric tuples (e.g., `("cpu",)`, `("memory",)`, and `("cpu", "memory")`) to test the function's behavior under these varying inputs. 

3. **Assert Correct Behavior**: Verify that:
    - The correct logging calls are made with expected messages based on mocked system readings.
    - System readings (CPU, memory) are correctly appended and trimmed in the `READINGS` dict.

### Writing Test Code

Here's how the pytest code could look:

```python
import pytest
from unittest.mock import patch, MagicMock
from sparkle_log.log_writer import log_system_metrics

# Importing directly for mocking, even if not directly used in tests to enhance clarity
import psutil
from sparkle_log.global_logger import GLOBAL_LOGGER


@pytest.mark.parametrize(
    "metrics,expected_calls",
    [
        (("cpu",), 1),
        (("memory",), 1),
        (("cpu", "memory"), 2),
    ],
)
def test_log_system_metrics(metrics, expected_calls):
    with patch.object(
        GLOBAL_LOGGER, "isEnabledFor", return_value=True
    ) as mock_is_enabled, patch.object(GLOBAL_LOGGER, "info") as mock_info, patch(
        "psutil.cpu_percent", return_value=50
    ) as mock_cpu_percent, patch(
        "psutil.virtual_memory", return_value=MagicMock(percent=70)
    ) as mock_virtual_memory, patch(
        "sparkle_log.ui.sparkline", return_value="spark"
    ):
        log_system_metrics(metrics)

        assert mock_is_enabled.called
        # Ensure that based on input metrics, logging happens the expected number of times
        assert mock_info.call_count == expected_calls

        # Validate that the logging messages include specific text based on the metrics
        for metric in metrics:
            if metric == "cpu":
                mock_info.assert_any_call(
                    "CPU: 50% | spark | min, mean, max (50, 50.0, 50)"
                )
            elif metric == "memory":
                mock_info.assert_any_call(
                    "Memory: 70% | spark, [70] | min, mean, max (70, 70.0, 70)"
                )
```

Here's the breakdown:
- We use `@pytest.mark.parametrize` to run the test with different combinations of metrics, and based on those, a defined expected number of times the logging should occur.
- `patch.object` and `patch` are used to mock `GLOBAL_LOGGER` methods, `psutil`'s system readings, and the `sparkline` function, so no actual calls to system resources or logging occur. 
- We assert that the `mock_info` method of the mocked logger was called the expected number of times and that it was called with specific arguments that match the expected log output based on mocked system metrics.

This test approach ensures that `log_system_metrics` behaves correctly under various conditions and that both system metrics are logged appropriately based on the function's logic and parameters.
User: 
Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py

Source Path: E:\github\sparkle_log\sparkle_log\log_writer.py
Module Name: sparkle_log.log_writer
```python
import logging
import statistics

import psutil

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.ui import sparkline

READINGS: dict[str, list[int]] = {"cpu": [], "memory": []}


def log_system_metrics(metrics: tuple[str, ...]) -> None:
    if not GLOBAL_LOGGER.isEnabledFor(logging.INFO):
        return
    if "cpu" in metrics:
        # Interval non to prevent blocking.
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        interval = None
        reading = psutil.cpu_percent(interval=interval)
        if reading == 0 and interval is None:
            # First reading on interval None is trash, bail.
            return
        READINGS["cpu"].append(int(reading))
    if "memory" in metrics:
        READINGS["memory"].append(int(psutil.virtual_memory().percent))

    for _key, value in READINGS.items():
        if len(value) > 30:  # Keep the last 30 readings
            value.pop(0)

    for metric, value in READINGS.items():
        if metric not in metrics:
            continue
        average = round(statistics.mean(value), 1)
        minimum = min(value)
        maximum = max(value)
        if metric == "cpu":
            GLOBAL_LOGGER.info(
                f"CPU: {value[-1]}% | {sparkline(value)} | min, mean, max ({minimum}, {average}, {maximum})"
            )
        elif metric == "memory":
            GLOBAL_LOGGER.info(
                f"Memory: {value[-1]}% | {sparkline(value)}, {value} | min, mean, max ({minimum}, {average}, {maximum})"
            )
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/ui.py
def sparkline(numbers: list[int]) -> str:
    """Generate a simple sparkline string for a list of integers."""
    ...
```


Next, let's focus on testing simulated exceptions. Write a unit test using pytest pytest, unittest.mock that the 
code does something sensible when exceptions are raised. 
Employ unittest.mock to mock out dependencies and use Path objects for file paths. Testing exceptions will help us ensure our error handling is robust.

If nothing can be written that fits that description, write "Nothing to do here."

Assistant: In the provided `log_system_metrics` function from the `sparkle_log.log_writer` module, there's no explicit exception handling for errors that may be raised by its dependencies, notably `psutil.cpu_percent` and `psutil.virtual_memory().percent`. Thus, our focus for this test would be to ensure that if these dependencies raise exceptions, our function either continues gracefully (if that's the intended behavior) or fails in a predictable manner. However, based on the current code snippet, the function does not seem to catch exceptions or errors internally, which limits the scope for testing exception handling directly within this context.

That being said, for educational purposes, let's simulate testing exception handling by mocking these dependencies to raise exceptions, to demonstrate how one would typically write such a test. Note that this is more of a hypothetical exercise given the current function does not have built-in error handling.

### Hypothetical Test for Simulated Exceptions

```python
import pytest
from unittest.mock import patch, MagicMock
import psutil
from sparkle_log.log_writer import log_system_metrics
from logging import INFO

# Considering there's no explicit exception handling in the provided function,
# this is hypothetical and assumes we want to check if the function can skip
# over exceptions raised by psutil functions without breaking.


def test_log_system_metrics_with_exceptions():
    with patch.object(
        GLOBAL_LOGGER, "isEnabledFor", return_value=True
    ) as mock_is_enabled_for, patch.object(GLOBAL_LOGGER, "info") as mock_info:
        # Simulate `cpu_percent` raising an exception
        with patch("psutil.cpu_percent", side_effect=Exception("CPU reading failed")):
            log_system_metrics(("cpu",))

        # Simulate `virtual_memory().percent` raising an exception
        with patch(
            "psutil.virtual_memory", side_effect=Exception("Memory reading failed")
        ):
            log_system_metrics(("memory",))

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
```

**Conclusion:**

Given the implementation of `log_system_metrics` as provided, there's no direct way to write a meaningful test focusing on exception handling since the function itself does not handle exceptions. Therefore, the proper response here is "Nothing to do here," unless the code under test is modified to include explicit exception handling.

This hypothetical test demonstrates the approach but won't yield useful results without modifications to the function being tested to gracefully handle exceptions.
User: 
Write a comprehensive unit test using pytest pytest, unittest.mock that covers happy path scenarios, edge cases, and error conditions. Make use of unittest.mock for mocking dependencies and Path over str for file paths.

Assistant: To write a comprehensive unit test for the `log_system_metrics` function within the `sparkle_log.log_writer` module, we'll cover the following scenarios:
1. **Happy path scenario** for both "cpu" and "memory" metrics logging, ensuring that logging happens correctly when `GLOBAL_LOGGER` is enabled for `logging.INFO`.
2. **Edge case** where `psutil.cpu_percent` could potentially give a zero value on the first call with `interval=None` and ensure that no logging occurs in this specific case.
3. **Error conditions** are somewhat limited by the nature of the provided code, as there's no explicit error handling within the function. However, we can still mock a situation where dependencies might behave unexpectedly (e.g., return non-integer values) but keeping in mind that the real function doesn't handle exceptions.

We'll use `unittest.mock.patch` to mock the dependencies like `GLOBAL_LOGGER`, `psutil.cpu_percent`, and `psutil.virtual_memory`. Note that since the function doesn't interact with the filesystem directly, we won't need to use `Path` objects here.

### Unit Test Code

```python
import pytest
from unittest.mock import patch, MagicMock
import psutil
from sparkle_log.log_writer import log_system_metrics, READINGS


@pytest.fixture(autouse=True)
def clear_readings():
    """Fixture to clear the READINGS dictionary before each test case."""
    READINGS["cpu"] = []
    READINGS["memory"] = []


def test_log_cpu_metrics_happy_path():
    with patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("sparkle_log.log_writer.sparkline", return_value="[sparkline]"), patch(
        "psutil.cpu_percent", return_value=20
    ), patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.info"
    ) as mock_info:
        log_system_metrics(("cpu",))

        assert READINGS["cpu"][-1] == 20
        mock_info.assert_called_once_with(
            "CPU: 20% | [sparkline] | min, mean, max (20, 20.0, 20)"
        )


def test_log_memory_metrics_happy_path():
    with patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("sparkle_log.log_writer.sparkline", return_value="[sparkline]"), patch(
        "psutil.virtual_memory", MagicMock(percent=50)
    ), patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.info"
    ) as mock_info:
        log_system_metrics(("memory",))

        assert READINGS["memory"][-1] == 50
        mock_info.assert_called_once_with(
            "Memory: 50% | [sparkline], [50] | min, mean, max (50, 50.0, 50)"
        )


def test_no_logging_if_not_enabled():
    with patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=False
    ), patch("sparkle_log.log_writer.GLOBAL_LOGGER.info") as mock_info:
        log_system_metrics(("cpu", "memory"))

        mock_info.assert_not_called()


def test_cpu_metrics_first_call_zero_value():
    with patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("psutil.cpu_percent", return_value=0), patch(
        "sparkle_log.log_writer.GLOBAL_LOGGER.info"
    ) as mock_info:
        log_system_metrics(("cpu",))

        # No logging should occur for the first zero value with interval=None
        mock_info.assert_not_called()


# Error condition tests are omitted due to the nature of provided function which lacks explicit exception handling.
```

This test suite covers the defined scenarios thoroughly. It checks that:
- Metrics are logged correctly when the logger is enabled and metrics are provided.
- Reads for `cpu` are not logged when the initial call returns a first-time zero value, simulating the interval=None behavior.
- When the logger is not enabled, no logging occurs, covering an implicit edge case.

Error condition testing as commonly defined is impractical here given the function's current structure, but this suite serves to ensure the main functionality reacts as expected under normal and some boundary conditions.