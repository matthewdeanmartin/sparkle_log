"""
Sparkline graph code goes here.
"""

from typing import cast

import sparklines

from sparkle_log.custom_types import GraphStyle, NumberType


def sparkline(numbers: list[NumberType], style: GraphStyle = "bar") -> str:
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


def faces_sparkline(data: list[NumberType]):
    """Generate a sparkline with face emojis."""
    symbols = ["😞", "😐", "😊", "😁"]
    return sparkline_it(data, symbols)


def sparkline_it(data: list[NumberType], symbols: list[str]):
    """Generate a sparkline with the given symbols."""
    noneless_data = [_ for _ in data if _ is not None]
    max_val = max(noneless_data)
    min_val = min(noneless_data)
    range_val = max_val - min_val
    if range_val == 0:  # Avoid division by zero
        return "".join(" " for _ in data)
    if range_val * len(symbols) == 0:
        return " "
    return "".join(
        symbols[min(len(symbols) - 1, int((val - min_val) / range_val * len(symbols)))] if val is not None else " "
        for val in data
    )


def pie_chart_sparkline(data: list[NumberType]):
    """Using different geometric shapes or other symbols"""
    symbols = ["○", "◔", "◑", "◕", "●"]
    return sparkline_it(data, symbols)


def ascii_sparkline(data: list[NumberType]):
    """Using different ASCII characters."""
    symbols = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    return sparkline_it(data, symbols)


def linear_ascii_sparkline(data: list[NumberType]):
    """Ascii for Low, medium, and high levels"""
    levels = ["_", "-", "¯"]
    return sparkline_it(data, levels)


def jagged_ascii_sparkline(data: list[NumberType]):
    """Ascii incorporating a peak character"""
    symbols = ["_", "-", "^", "¯"]
    return sparkline_it(data, symbols)


def vertical_ascii_sparkline(data: list[NumberType]):
    """Ascii Using single and double vertical lines"""
    symbols = ["_", "|", "‖"]
    return sparkline_it(data, symbols)


if __name__ == "__main__":

    def run():
        for style in ["bar", "jagged", "vertical", "linear", "ascii_art", "pie_chart", "faces"]:
            print(f"{style}: {sparkline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], cast(GraphStyle, style))}")

    run()
