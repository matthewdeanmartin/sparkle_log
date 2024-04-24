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
Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py

Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py
Module Name: sparkle_log.as_context_manager
```python
import logging
import time
from threading import Event, Thread
from typing import Any, Optional

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricMonitor:
    def __init__(self, metrics=("cpu", "memory"), interval: int = 10) -> None:
        self.metrics = metrics
        self.interval = interval
        self.stop_event: Optional[Event] = None
        self.scheduler_thread: Optional[Thread] = None

    def __enter__(self) -> "MetricMonitor":
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(
                target=run_scheduler,
                args=(self.stop_event, self.metrics, self.interval),
            )
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/scheduler.py
def run_scheduler(stop_event: Event, metrics: tuple[str, ...], seconds: int):
    """Run scheduled tasks until the stop_event is set."""
    ...
```


Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py

Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py
Module Name: sparkle_log.as_context_manager
```python
import logging
import time
from threading import Event, Thread
from typing import Any, Optional

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricMonitor:
    def __init__(self, metrics=("cpu", "memory"), interval: int = 10) -> None:
        self.metrics = metrics
        self.interval = interval
        self.stop_event: Optional[Event] = None
        self.scheduler_thread: Optional[Thread] = None

    def __enter__(self) -> "MetricMonitor":
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(
                target=run_scheduler,
                args=(self.stop_event, self.metrics, self.interval),
            )
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/scheduler.py
def run_scheduler(stop_event: Event, metrics: tuple[str, ...], seconds: int):
    """Run scheduled tasks until the stop_event is set."""
    ...
```


Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py

Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py
Module Name: sparkle_log.as_context_manager
```python
import logging
import time
from threading import Event, Thread
from typing import Any, Optional

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricMonitor:
    def __init__(self, metrics=("cpu", "memory"), interval: int = 10) -> None:
        self.metrics = metrics
        self.interval = interval
        self.stop_event: Optional[Event] = None
        self.scheduler_thread: Optional[Thread] = None

    def __enter__(self) -> "MetricMonitor":
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(
                target=run_scheduler,
                args=(self.stop_event, self.metrics, self.interval),
            )
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/scheduler.py
def run_scheduler(stop_event: Event, metrics: tuple[str, ...], seconds: int):
    """Run scheduled tasks until the stop_event is set."""
    ...
```



Please write a parameterized unit test using pytest pytest, unittest.mock. This test should check multiple inputs 
and their expected outputs for a single function. Utilize unittest.mock to simulate any external interactions and Path for handling file paths. This will help us ensure our function behaves correctly under various conditions.

Assistant: Given the code and instructions provided, I'll write a parameterized unit test for the `MetricMonitor` class `__enter__` and `__exit__` methods in the `sparkle_log.as_context_manager.py` module. Since the main external interaction to mock in these methods is the `GLOBAL_LOGGER` object (to check if it is enabled for logging at the `INFO` level) and the interactions with the thread that runs `run_scheduler`, mocking will be employed for these aspects. Using `pytest` along with `unittest.mock.patch`, we can effectively simulate different environments and conditions. There is no direct interaction with file paths within the given code, so `pathlib.Path` won't be used in these particular tests. Instead, we focus on the logging and threading aspects.

### Writing the Parametrized PyTest

First, we need to import necessary libraries and functions:

```python
import pytest
from unittest.mock import patch, Mock
from threading import Event
from sparkle_log.as_context_manager import MetricsLoggingContext
```

Then, we structure our parameterized test for both `__enter__` and `__exit__` methods:

```python
@pytest.mark.parametrize(
    "log_enabled, expected_thread_start",
    [
        (True, True),  # Test Case: Logger enabled, expect thread to start
        (False, False),  # Test Case: Logger not enabled, expect thread not to start
    ],
)
def test_MetricMonitor_context_management(log_enabled, expected_thread_start):
    with patch(
        "sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor"
    ) as mock_isEnabledFor:
        # Mock GLOBAL_LOGGER to control isEnabledFor behavior
        mock_isEnabledFor.return_value = log_enabled

        # Mock run_scheduler to observe if it's called
        with patch("sparkle_log.as_context_manager.Thread") as mock_thread:
            mock_thread_instance = Mock()
            mock_thread.return_value = mock_thread_instance

            # Using MetricMonitor as context manager to trigger __enter__
            with MetricMonitor(metrics=("cpu",), interval=5) as monitor:
                pass

            # Check that the thread's start method is called if log is enabled
            if expected_thread_start:
                mock_thread_instance.start.assert_called_once()
            else:
                mock_thread_instance.start.assert_not_called()

    # After the context block exits, __exit__ is called, testing it's behaviour
    mock_thread_instance.join.assert_called_with()
```

Explanation:
1. **Parameterization**: The test runs twice with different values for `log_enabled` and `expected_thread_start`, allowing us to check the behavior when the `GLOBAL_LOGGER` is enabled and when it is not.
2. **Mocks and Patches**: We mock `GLOBAL_LOGGER.isEnabledFor` to return our parameterized `log_enabled` value to simulate the logger being enabled or disabled. Then, we mock `Thread` to verify whether the `start` method is called based on the logger's state.
3. **Context Manager Test**: We use the `MetricMonitor` in a `with` block to test the `__enter__` and `__exit__` methods. The implementation details, such as threading and logging, are mocked out, focusing the test on the `MetricMonitor`'s behavior in response to our mock configurations.

This test adequately simulates the conditions and interactions within the `MetricMonitor`'s context manager functionality, verifying that threads are appropriately started and joined based on the logging configuration without the need for actual system logging or thread execution.
User: 
Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py

Source Path: E:\github\sparkle_log\sparkle_log\as_context_manager.py
Module Name: sparkle_log.as_context_manager
```python
import logging
import time
from threading import Event, Thread
from typing import Any, Optional

from sparkle_log.global_logger import GLOBAL_LOGGER
from sparkle_log.scheduler import run_scheduler


class MetricMonitor:
    def __init__(self, metrics=("cpu", "memory"), interval: int = 10) -> None:
        self.metrics = metrics
        self.interval = interval
        self.stop_event: Optional[Event] = None
        self.scheduler_thread: Optional[Thread] = None

    def __enter__(self) -> "MetricMonitor":
        if GLOBAL_LOGGER.isEnabledFor(logging.INFO):
            self.stop_event = Event()
            self.scheduler_thread = Thread(
                target=run_scheduler,
                args=(self.stop_event, self.metrics, self.interval),
            )
            self.scheduler_thread.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.stop_event.set()
            self.scheduler_thread.join()


# Usage example with the context manager
```

Here are function and method signatures of the dependencies

```python
# sparkle_log/scheduler.py
def run_scheduler(stop_event: Event, metrics: tuple[str, ...], seconds: int):
    """Run scheduled tasks until the stop_event is set."""
    ...
```


Next, let's focus on testing simulated exceptions. Write a unit test using pytest pytest, unittest.mock that the 
code does something sensible when exceptions are raised. 
Employ unittest.mock to mock out dependencies and use Path objects for file paths. Testing exceptions will help us ensure our error handling is robust.

If nothing can be written that fits that description, write "Nothing to do here."

Assistant: Given the context and constraints of the provided `MetricMonitor` class from the `sparkle_log.as_context_manager` module, there's a straightforward approach for handling exceptions: the class itself doesn't explicitly handle exceptions within its `__enter__` or `__exit__` methods beyond ensuring that the spawned thread is joined back if it was started. This is a basic resource management pattern that doesn't involve complex error handling logic.

However, for the sake of addressing the request and showcasing how one might test for sensible behavior in the face of exceptions (even if the original code does not explicitly manage exceptions), let's consider a hypothetical scenario where an exception is raised within the `with` block where the `MetricMonitor` is used. We'll ensure that the `__exit__` method behaves as expected, i.e., it still attempts to clean up by joining the thread.

Since the given requirement doesn't align perfectly with the code provided (i.e., there's no direct interaction with file paths and not much in the way of exceptions to handle), the outlined test will focus on a constructed example to demonstrate the testing of exception handling.

### Writing the Unit Test with Pytest and unittest.mock

```python
import pytest
from unittest.mock import patch, MagicMock
from threading import Event
from sparkle_log.as_context_manager import MetricsLoggingContext


class TestException(Exception):
    """Custom exception for testing purposes."""

    pass


def test_MetricMonitor_exception_handling():
    with patch(
        "sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("sparkle_log.as_context_manager.Thread") as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Simulate an exception within the with block
        try:
            with MetricsLoggingContext(metrics=("cpu",), interval=5) as monitor:
                raise TestException("Testing exception handling.")
        except TestException:
            pass  # Exception is expected, continue to check if cleanup occurs

        # Verify that despite the exception, the cleanup process (thread join) is still attempted
        mock_thread_instance.join.assert_called_once()
```

In this test:
- **Custom Exception Handling**: We define a custom `TestException` to raise within the `with` block to simulate an error occurring during the lifetime of the context manager.
- **Mocks and Assertions**: `GLOBAL_LOGGER.isEnabledFor` is mocked to ensure the logger is considered enabled (triggering the thread start), and `Thread` is mocked to verify behavior without executing real threading logic.
- **Exception Handling Verification**: After simulating an exception within the `with` block, the focus is on whether the `__exit__` method correctly attempts to clean up by joining the thread, despite the occurrence of the exception. This ensures that our context manager is robust against interruptions.

This test aligns with the goal of ensuring sensible behavior when exceptions arise, specifically focusing on resource cleanup, which is relevant to the `MetricMonitor` class's context management pattern.
User: 
Write a comprehensive unit test using pytest pytest, unittest.mock that covers happy path scenarios, edge cases, and error conditions. Make use of unittest.mock for mocking dependencies and Path over str for file paths.

Assistant: To create a comprehensive unit test covering happy paths, edge cases, and error conditions for the `MetricMonitor` class, we'll incorporate `pytest` and `unittest.mock`, as well as mock dependencies and utilize `Path` objects when relevant. Given the provided source, there are no file path operations directly in `MetricMonitor`, so the emphasis on `Path` objects will be hypothetical, primarily focusing on mocking and testing behavior.

## Happy Path Scenario

A happy path scenario tests the expected use case. For `MetricMonitor`, this involves creating an instance, using it within a context manager, and ensuring it starts and stops the scheduler thread as expected.

## Edge Cases

Edge cases could involve what happens when:
- `GLOBAL_LOGGER.isEnabledFor(logging.INFO)` returns `False`, meaning logging is not enabled at the INFO level, and hence the scheduler should not start.
- The monitor is used outside of a context manager, or misuse of the API.

## Error Conditions

Error conditions simulate what happens when unexpected exceptions occur within the provided code block. However, the primary source of error handling would be ensuring that the thread is joined even if an exception is raised within the `with` block of the context manager, which was covered in a previous answer. Here, we'll also consider mocking exceptions thrown by the thread itself as an error condition to test.

### Test Implementation

```python
import pytest
from unittest.mock import patch, MagicMock
import logging
from threading import Event
from sparkle_log.as_context_manager import MetricsLoggingContext


def test_metric_monitor_happy_path():
    """Test the expected behavior when everything runs correctly."""
    with patch(
        "sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("sparkle_log.as_context_manager.Thread") as mock_thread:
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        with MetricsLoggingContext(metrics=("cpu", "memory"), interval=10) as monitor:
            pass

        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        mock_thread_instance.join.assert_called_once()


def test_metric_monitor_logger_disabled():
    """Test behavior when logging is disabled for INFO level."""
    with patch(
        "sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=False
    ):
        with MetricsLoggingContext(metrics=("cpu",), interval=5) as monitor:
            pass

        # Expect that the scheduler thread was never started as logging is not enabled.
        monitor.scheduler_thread is None


def test_metric_monitor_usage_outside_context_manager():
    """Testing misuse of the context manager (e.g., not using the 'with' statement)."""
    # No mocking required as this tests misuse of the API directly
    monitor = MetricsLoggingContext(metrics=("cpu",), interval=5)
    # Assert the scheduler thread was not started as the context manager protocol was not entered.
    assert monitor.scheduler_thread is None


def test_metric_monitor_exception_in_thread():
    """Test handling of exceptions thrown by the scheduler thread."""
    with patch(
        "sparkle_log.as_context_manager.GLOBAL_LOGGER.isEnabledFor", return_value=True
    ), patch("sparkle_log.as_context_manager.Thread") as mock_thread, patch(
        "sparkle_log.scheduler.run_scheduler",
        side_effect=Exception("Mock scheduler exception"),
    ):
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        with pytest.raises(Exception) as execinfo:
            with MetricsLoggingContext(metrics=("cpu",), interval=5) as monitor:
                # Directly call the thread's target to simulate exception within the with block
                monitor.scheduler_thread._target(*monitor.scheduler_thread._args)

        assert "Mock scheduler exception" in str(execinfo.value)
        mock_thread_instance.join.assert_called_once()
```

These tests ensure that the `MetricMonitor` class behaves correctly under varying conditions, offering a comprehensive test suite that covers proper usage and potential misuse or error conditions. The tests demonstrate the use of `unittest.mock` for mocking dependent functionalities and methods, focusing on behavior rather than implementation.