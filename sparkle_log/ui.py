"""
Sparkline graph code goes here.
"""

from typing import Literal

import sparklines

GraphStyle = Literal["bar", "faces", "jagged", "linear", "vertical", "ascii_art", "pie_chart"]


def sparkline(numbers: list[int], style: GraphStyle = "bar") -> str:
    """Generate a simple sparkline string for a list of integers."""
    if style == "bar":
        for line in sparklines.sparklines(numbers):
            return line
    elif style == "jagged":
        return jagged_ascii_sparkline(numbers)
    elif style == "vertical":
        return vertical_ascii_sparkline(numbers)
    elif style == "linear":
        return linear_ascii_sparkline(numbers)
    elif style == "ascii_art":
        return ascii_sparkline(numbers)
    elif style == "pie_chart":
        return pie_chart_sparkline(numbers)
    elif style == "faces":
        return faces_sparkline(numbers)
    return ""


def faces_sparkline(data):
    """Generate a sparkline with face emojis."""
    symbols = ["😞", "😐", "😊", "😁"]
    return sparkline_it(data, symbols)


def sparkline_it(data: list[int], symbols: list[str]):
    """Generate a sparkline with the given symbols."""
    noneless_data = [_ for _ in data if _ is not None]
    max_val = max(noneless_data)
    min_val = min(noneless_data)
    range_val = max_val - min_val
    if range_val == 0:  # Avoid division by zero
        return "".join(symbols[0] for _ in data)
    if range_val * len(symbols) == 0:
        return " "
    return "".join(
        symbols[min(len(symbols) - 1, int((val - min_val) / range_val * len(symbols)))] if val is not None else " "
        for val in data
    )


def pie_chart_sparkline(data):
    """Using different geometric shapes or other symbols"""
    symbols = ["○", "◔", "◑", "◕", "●"]
    return sparkline_it(data, symbols)


def ascii_sparkline(data):
    """Using different ASCII characters."""
    symbols = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    return sparkline_it(data, symbols)


def linear_ascii_sparkline(data):
    """Ascii for Low, medium, and high levels"""
    levels = ["_", "-", "¯"]
    return sparkline_it(data, levels)


def jagged_ascii_sparkline(data):
    """Ascii incorporating a peak character"""
    symbols = ["_", "-", "^", "¯"]
    return sparkline_it(data, symbols)


def vertical_ascii_sparkline(data):
    """Ascii Using single and double vertical lines"""
    symbols = ["_", "|", "‖"]
    return sparkline_it(data, symbols)
