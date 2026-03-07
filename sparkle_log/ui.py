# sparkle_log/ui.py
"""
Sparkline graph code goes here.
"""

from __future__ import annotations

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
    elif style == "braille":
        return braille_sparkline(numbers)
    elif style == "arrows":
        return arrows_sparkline(numbers)
    elif style == "weather":
        return weather_sparkline(numbers)
    elif style == "hearts":
        return hearts_sparkline(numbers)
    elif style == "stars":
        return stars_sparkline(numbers)
    elif style == "circles":
        return circles_sparkline(numbers)
    elif style == "triangles":
        return triangles_sparkline(numbers)
    elif style == "blocks":
        return blocks_sparkline(numbers)
    elif style == "dna":
        return dna_sparkline(numbers)
    elif style == "morse":
        return morse_sparkline(numbers)
    elif style == "digits":
        return digits_sparkline(numbers)
    elif style == "binary":
        return binary_sparkline(numbers)
    elif style == "hex":
        return hex_sparkline(numbers)
    elif style == "chess":
        return chess_sparkline(numbers)
    elif style == "cards":
        return cards_sparkline(numbers)
    elif style == "bullets":
        return bullets_sparkline(numbers)
    elif style == "math":
        return math_sparkline(numbers)
    elif style == "zodiac":
        return zodiac_sparkline(numbers)
    elif style == "traffic":
        return traffic_sparkline(numbers)
    elif style == "battery":
        return battery_sparkline(numbers)
    elif style == "temperature":
        return temperature_sparkline(numbers)
    elif style == "music":
        return music_sparkline(numbers)
    elif style == "checkmarks":
        return checkmarks_sparkline(numbers)
    elif style == "trees":
        return trees_sparkline(numbers)
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


def braille_sparkline(data: list[NumberType]):
    """Generate a sparkline with Unicode Braille patterns."""
    symbols = ["⠁", "⠂", "⠃", "⠄", "⠅", "⠆", "⠇", "⠈", "⠉", "⠊"]
    return sparkline_it(data, symbols)


def arrows_sparkline(data: list[NumberType]):
    """Generate a sparkline with directional arrows."""
    symbols = ["←", "↔", "→"]
    return sparkline_it(data, symbols)


def weather_sparkline(data: list[NumberType]):
    """Generate a sparkline with weather condition symbols."""
    symbols = ["☁️", "🌤️", "⛅", "🌧️", "⛈️"]
    return sparkline_it(data, symbols)


def hearts_sparkline(data: list[NumberType]):
    """Generate a sparkline with heart symbols."""
    symbols = ["💔", "❤️", "💕", "💖", "💗"]
    return sparkline_it(data, symbols)


def stars_sparkline(data: list[NumberType]):
    """Generate a sparkline with star symbols."""
    symbols = ["☆", "★"]
    return sparkline_it(data, symbols)


def circles_sparkline(data: list[NumberType]):
    """Generate a sparkline with geometric circle symbols."""
    symbols = ["◌", "◍", "◎", "◉", "◐"]
    return sparkline_it(data, symbols)


def triangles_sparkline(data: list[NumberType]):
    """Generate a sparkline with triangular shapes."""
    symbols = ["▽", "△", "▲"]
    return sparkline_it(data, symbols)


def blocks_sparkline(data: list[NumberType]):
    """Generate a sparkline with block elements."""
    symbols = ["▢", "▣", "▤", "▥", "▦", "▧", "▨", "▩", "■"]
    return sparkline_it(data, symbols)


def dna_sparkline(data: list[NumberType]):
    """Generate a sparkline with helix-style characters."""
    symbols = ["╱", "╲", "╳"]
    return sparkline_it(data, symbols)


def morse_sparkline(data: list[NumberType]):
    """Generate a sparkline with dots and dashes."""
    symbols = ["·", "–"]
    return sparkline_it(data, symbols)


def digits_sparkline(data: list[NumberType]):
    """Generate a sparkline with digit characters."""
    symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return sparkline_it(data, symbols)


def binary_sparkline(data: list[NumberType]):
    """Generate a sparkline with binary representation."""
    symbols = ["0", "1"]
    return sparkline_it(data, symbols)


def hex_sparkline(data: list[NumberType]):
    """Generate a sparkline with hexadecimal characters."""
    symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    return sparkline_it(data, symbols)


def chess_sparkline(data: list[NumberType]):
    """Generate a sparkline with chess piece symbols."""
    symbols = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]
    return sparkline_it(data, symbols)


def cards_sparkline(data: list[NumberType]):
    """Generate a sparkline with playing card suit symbols."""
    symbols = ["♠", "♥", "♦", "♣"]
    return sparkline_it(data, symbols)


def bullets_sparkline(data: list[NumberType]):
    """Generate a sparkline with bullet point symbols."""
    symbols = ["▫", "▪"]
    return sparkline_it(data, symbols)


def math_sparkline(data: list[NumberType]):
    """Generate a sparkline with mathematical symbols."""
    symbols = ["∾", "∿", "∇", "△", "□", "○", "◷"]
    return sparkline_it(data, symbols)


def zodiac_sparkline(data: list[NumberType]):
    """Generate a sparkline with astrological symbols."""
    symbols = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]
    return sparkline_it(data, symbols)


def traffic_sparkline(data: list[NumberType]):
    """Generate a sparkline with traffic light colors."""
    symbols = ["🔴", "🟡", "🟢"]
    return sparkline_it(data, symbols)


def battery_sparkline(data: list[NumberType]):
    """Generate a sparkline with battery level symbols."""
    symbols = ["🪫", "🔋"]
    return sparkline_it(data, symbols)


def temperature_sparkline(data: list[NumberType]):
    """Generate a sparkline with thermometer-style symbols."""
    symbols = ["💧", "🧊", "🌡️"]
    return sparkline_it(data, symbols)


def music_sparkline(data: list[NumberType]):
    """Generate a sparkline with musical note symbols."""
    symbols = ["♩", "♪", "♫", "♬"]
    return sparkline_it(data, symbols)


def checkmarks_sparkline(data: list[NumberType]):
    """Generate a sparkline with success/failure symbols."""
    symbols = ["✗", "✓"]
    return sparkline_it(data, symbols)


def trees_sparkline(data: list[NumberType]):
    """Generate a sparkline with forest/environment symbols."""
    symbols = ["🌱", "🌲", "🌳", "🌴"]
    return sparkline_it(data, symbols)


if __name__ == "__main__":

    def run():
        for style in [
            "bar", "jagged", "vertical", "linear", "ascii_art", "pie_chart", "faces",
            "braille", "arrows", "weather", "hearts", "stars", "circles", "triangles",
            "blocks", "dna", "morse", "digits", "binary", "hex", "chess", "cards",
            "bullets", "math", "zodiac", "traffic", "battery", "temperature", "music",
            "checkmarks", "trees",
        ]:
            print(f"{style}: {sparkline([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], cast(GraphStyle, style))}")

    run()
