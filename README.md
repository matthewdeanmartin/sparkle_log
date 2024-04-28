# sparkle_log

Write a spark line graph of CPU, Memory, etc to the python log

```text
❯ sparkle_log
Demo of Sparkle Monitoring system metrics during operations...
INFO     CPU   :   % |                              ▄ | min, mean, max (4, 4, 4)
INFO     Memory:   % |                              ▄ | min, mean, max (46, 46, 46)
Maybe CPU intensive work done here...
INFO     CPU   :   % |                           ▆▁█▄ | min, mean, max (1, 3.2, 5)
INFO     Memory:   % |                           ▄▄▄▄ | min, mean, max (46, 46, 46)
Maybe Memory intensive work done here...
INFO     Memory:   % |                         ▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
INFO     CPU   :   % |                        ▆▁█▄▃▃▁ | min, mean, max (1, 2.6, 5)
INFO     Memory:   % |                        ▄▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
```

Tracking just one metric at a time looks better.

```text
INFO     Memory:   % |                              ▄ | min, mean, max (46, 46, 46)
INFO     Memory:   % |                           ▄▄▄▄ | min, mean, max (46, 46, 46)
INFO     Memory:   % |                         ▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
INFO     Memory:   % |                        ▄▄▄▄▄▄▄ | min, mean, max (46, 46, 46)
```

## Install

`pip install sparkle_log`

## Usage

This will write up to log entries to your AWS Lambda log, at a frequency you specify, e.g. every 60 seconds.
Light-weight, cheap, immediately correlates to your other print statements and log entries.

If logging is less than INFO, then no data is collected.

As a decorator

```python
import sparkle_log
import logging

logging.basicConfig(level=logging.INFO)


@sparkle_log.monitor_metrics_on_call(("cpu", "memory" "drive"), 60)
def handler_name(event, context) -> str:
    return "Hello world!"
```

As a context manager:

```python
import time
import sparkle_log
import logging

logging.basicConfig(level=logging.INFO)


def handler_name(event, context) -> str:
    with sparkle_log.MetricsLoggingContext(
        metrics=("cpu", "memory", "drive"), interval=5
    ):
        time.sleep(20)
        return "Hello world!"
```

```python
import time
import logging
import random
from sparkle_log import MetricsLoggingContext

logging.basicConfig(level=logging.INFO)


def dodgy_metric() -> int:
    return random.randint(0, 100)


with MetricsLoggingContext(
    metrics=("dodgy",), interval=1, custom_metrics={"dodgy": dodgy_metric}
):
    print("Monitoring system metrics during operations...")
    time.sleep(20)
```

## Supported Styles

Graph styles currently are all autoscaled. Linear, faces, vertical have only 3 levels. Bar has 8 levels.

```python
from typing import cast
from sparkle_log import sparkline, GraphStyle

for style in ["bar", "jagged", "vertical", "linear", "ascii_art", "pie_chart", "faces"]:
    print(
        f"{style}: {sparkline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], cast(GraphStyle, style))}"
    )
```

Results:

```text
bar: ▁▂▃▃▄▅▆▆▇█
jagged: ___--^^¯¯¯
vertical: ___|||‖‖‖‖
linear: ___---¯¯¯¯
ascii_art:  .:-=+*#%@
pie_chart: ○○◔◔◑◑◕◕●●
faces: 😞😞😞😐😐😊😊😁😁😁
```

## Prior art

You could also use container insights or htop. This tool should provide the most value when the server is headless and
you only have logging or no easy way to correlate log entries to graphs.

### Diagnostics as sparklines

- [memsparkline](https://pypi.org/project/memsparkline/) - CLI tool to show memory as sparkline.
- [densli](https://pypi.org/project/densli/)  (defunct?) server stats tool with terminal sparkline display
- [sparcli](https://pypi.org/project/sparcli/) Context manager for displaying arbitrary metrics as sparklines

### Sparkline functions

- [py-sparkblocks](https://pypi.org/project/py-sparkblocks/) function to create sparkline graph
- [sparklines](https://pypi.org/project/sparklines/) function to create sparkline graph
- [rich-sparklines](https://pypi.org/project/rich-sparklines/) function that works with rich UI library
- [yasl](https://pypi.org/project/yasl/) Yet Another Sparkline Library
- [Piltdown](https://pypi.org/project/Piltdown) Variety of ASCII/Unicode graphs including sparklines.
- [termgraph](https://pypi.org/project/termgraph/) - Various terminal graphs not including sparklines, but including bar
  graphs.
- [lehar](https://pypi.org/project/lehar/) - Another sparkline function

### CLI tools that display sparklines from arbitrary numbers

- [sparkl](https://pypi.org/project/sparkl/)
- [sparkback](https://github.com/mmichie/sparkback)
- [spark](http://github.com/holman/spark) Pure bash implementation that seems to have inspired many clones.
