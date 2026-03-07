# sparkle_log/custom_types.py
from __future__ import annotations

from typing import Callable, Literal, Union

NumberType = Union[int, float, None]
GraphStyle = Literal[
    "bar",
    "faces",
    "jagged",
    "linear",
    "vertical",
    "ascii_art",
    "pie_chart",
    "braille",
    "arrows",
    "weather",
    "hearts",
    "stars",
    "circles",
    "triangles",
    "blocks",
    "dna",
    "morse",
    "digits",
    "binary",
    "hex",
    "chess",
    "cards",
    "bullets",
    "math",
    "zodiac",
    "traffic",
    "battery",
    "temperature",
    "music",
    "checkmarks",
    "trees",
]
Metrics = Literal["cpu", "memory", "drive"]
CustomMetricsCallBacks = dict[str, Callable[[], NumberType]] | None
