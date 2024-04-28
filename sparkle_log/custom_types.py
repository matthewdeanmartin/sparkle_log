from typing import Callable, Literal, Optional, Union

NumberType = Union[int, float, None]
GraphStyle = Literal["bar", "faces", "jagged", "linear", "vertical", "ascii_art", "pie_chart"]
Metrics = Literal["cpu", "memory", "drive"]
CustomMetricsCallBacks = Optional[dict[str, Callable[[], NumberType]]]
