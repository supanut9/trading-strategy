from __future__ import annotations

import math


def simple_average(values: list[float]) -> float:
    return sum(values) / len(values)


def population_standard_deviation(values: list[float]) -> float:
    mean = simple_average(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def exponential_moving_average(values: list[float], period: int) -> float:
    if period <= 0:
        raise ValueError("period must be positive")
    if len(values) < period:
        raise ValueError("not enough values to compute EMA")

    multiplier = 2 / (period + 1)
    ema = simple_average(values[:period])
    for value in values[period:]:
        ema = ((value - ema) * multiplier) + ema
    return ema


def rsi(closes: list[float], period: int) -> float:
    window = closes[-(period + 1) :]
    gains = 0.0
    losses = 0.0
    for previous, current in zip(window, window[1:]):
        delta = current - previous
        if delta > 0:
            gains += delta
        else:
            losses += abs(delta)

    average_gain = gains / period
    average_loss = losses / period
    if average_loss == 0:
        return 100.0
    relative_strength = average_gain / average_loss
    return 100 - (100 / (1 + relative_strength))


def average_true_range(highs: list[float], lows: list[float], closes: list[float], period: int) -> float:
    if period <= 0:
        raise ValueError("period must be positive")
    if not (len(highs) == len(lows) == len(closes)):
        raise ValueError("highs, lows, and closes must have the same length")
    if len(closes) < period + 1:
        raise ValueError("not enough values to compute ATR")

    true_ranges: list[float] = []
    start = len(closes) - period
    for index in range(start, len(closes)):
        previous_close = closes[index - 1]
        high = highs[index]
        low = lows[index]
        true_ranges.append(max(high - low, abs(high - previous_close), abs(low - previous_close)))
    return simple_average(true_ranges)
