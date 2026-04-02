from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy


Pivot = tuple[int, float]


@dataclass(frozen=True)
class DoublePatternMatch:
    kind: str
    first_pivot_index: int
    first_pivot_price: float
    second_pivot_index: int
    second_pivot_price: float
    neckline: float
    trigger_index: int
    trigger_price: float
    pivot_distance_pct: float
    neckline_move_pct: float


def _pivot_highs(candles: list[Candle], swing_window: int) -> list[Pivot]:
    pivots: list[Pivot] = []
    for index in range(swing_window, len(candles) - swing_window):
        current_high = candles[index].high
        left = candles[index - swing_window : index]
        right = candles[index + 1 : index + swing_window + 1]
        if all(current_high > candle.high for candle in left) and all(current_high >= candle.high for candle in right):
            pivots.append((index, current_high))
    return pivots


def _pivot_lows(candles: list[Candle], swing_window: int) -> list[Pivot]:
    pivots: list[Pivot] = []
    for index in range(swing_window, len(candles) - swing_window):
        current_low = candles[index].low
        left = candles[index - swing_window : index]
        right = candles[index + 1 : index + swing_window + 1]
        if all(current_low < candle.low for candle in left) and all(current_low <= candle.low for candle in right):
            pivots.append((index, current_low))
    return pivots


def _find_latest_double_bottom_breakout(
    candles: list[Candle],
    swing_window: int,
    min_separation_bars: int,
    max_separation_bars: int,
    peak_tolerance_pct: float,
    neckline_buffer_pct: float,
    breakout_pct: float,
) -> DoublePatternMatch | None:
    lows = _pivot_lows(candles, swing_window)
    highs = _pivot_highs(candles, swing_window)
    latest_breakout: DoublePatternMatch | None = None

    for first_index, first_price in lows:
        for second_index, second_price in lows:
            if second_index <= first_index:
                continue

            separation = second_index - first_index
            if separation < min_separation_bars or separation > max_separation_bars:
                continue

            average_bottom = (first_price + second_price) / 2
            if average_bottom <= 0:
                continue
            bottom_distance = abs(first_price - second_price) / average_bottom
            if bottom_distance > peak_tolerance_pct:
                continue

            neckline_candidates = [price for pivot_index, price in highs if first_index < pivot_index < second_index]
            if not neckline_candidates:
                continue

            neckline = max(neckline_candidates)
            rebound_pct = (neckline - average_bottom) / average_bottom
            if rebound_pct < neckline_buffer_pct:
                continue

            breakout_level = neckline * (1 + breakout_pct)
            for breakout_index in range(second_index + 1, len(candles)):
                if candles[breakout_index].close >= breakout_level:
                    latest_breakout = DoublePatternMatch(
                        kind="double_bottom",
                        first_pivot_index=first_index,
                        first_pivot_price=first_price,
                        second_pivot_index=second_index,
                        second_pivot_price=second_price,
                        neckline=neckline,
                        trigger_index=breakout_index,
                        trigger_price=candles[breakout_index].close,
                        pivot_distance_pct=bottom_distance * 100,
                        neckline_move_pct=rebound_pct * 100,
                    )
                    break

    return latest_breakout


def _find_latest_double_top_breakdown(
    candles: list[Candle],
    swing_window: int,
    min_separation_bars: int,
    max_separation_bars: int,
    peak_tolerance_pct: float,
    neckline_buffer_pct: float,
    breakout_pct: float,
) -> DoublePatternMatch | None:
    highs = _pivot_highs(candles, swing_window)
    lows = _pivot_lows(candles, swing_window)
    latest_breakdown: DoublePatternMatch | None = None

    for first_index, first_price in highs:
        for second_index, second_price in highs:
            if second_index <= first_index:
                continue

            separation = second_index - first_index
            if separation < min_separation_bars or separation > max_separation_bars:
                continue

            average_top = (first_price + second_price) / 2
            if average_top <= 0:
                continue
            top_distance = abs(first_price - second_price) / average_top
            if top_distance > peak_tolerance_pct:
                continue

            neckline_candidates = [price for pivot_index, price in lows if first_index < pivot_index < second_index]
            if not neckline_candidates:
                continue

            neckline = min(neckline_candidates)
            pullback_pct = (average_top - neckline) / average_top
            if pullback_pct < neckline_buffer_pct:
                continue

            breakdown_level = neckline * (1 - breakout_pct)
            for breakdown_index in range(second_index + 1, len(candles)):
                if candles[breakdown_index].close <= breakdown_level:
                    latest_breakdown = DoublePatternMatch(
                        kind="double_top",
                        first_pivot_index=first_index,
                        first_pivot_price=first_price,
                        second_pivot_index=second_index,
                        second_pivot_price=second_price,
                        neckline=neckline,
                        trigger_index=breakdown_index,
                        trigger_price=candles[breakdown_index].close,
                        pivot_distance_pct=top_distance * 100,
                        neckline_move_pct=pullback_pct * 100,
                    )
                    break

    return latest_breakdown


def find_latest_pattern_matches(candles: list[Candle], params: dict) -> tuple[DoublePatternMatch | None, DoublePatternMatch | None]:
    return (
        _find_latest_double_bottom_breakout(
            candles,
            params["swing_window"],
            params["min_separation_bars"],
            params["max_separation_bars"],
            params["peak_tolerance_pct"],
            params["neckline_buffer_pct"],
            params["breakout_pct"],
        ),
        _find_latest_double_top_breakdown(
            candles,
            params["swing_window"],
            params["min_separation_bars"],
            params["max_separation_bars"],
            params["peak_tolerance_pct"],
            params["neckline_buffer_pct"],
            params["breakout_pct"],
        ),
    )


@dataclass(frozen=True)
class DoubleTopBottomReversalStrategy(Strategy):
    swing_window: int
    min_separation_bars: int
    max_separation_bars: int
    peak_tolerance_pct: float
    neckline_buffer_pct: float
    breakout_pct: float
    lookback_bars: int
    name: str = "double_top_bottom_reversal"

    @property
    def parameters(self) -> dict:
        return {
            "swing_window": self.swing_window,
            "min_separation_bars": self.min_separation_bars,
            "max_separation_bars": self.max_separation_bars,
            "peak_tolerance_pct": self.peak_tolerance_pct,
            "neckline_buffer_pct": self.neckline_buffer_pct,
            "breakout_pct": self.breakout_pct,
            "lookback_bars": self.lookback_bars,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.swing_window < 1:
            raise ValueError("swing_window must be positive")
        if self.min_separation_bars < 1:
            raise ValueError("min_separation_bars must be positive")
        if self.max_separation_bars <= self.min_separation_bars:
            raise ValueError("max_separation_bars must be greater than min_separation_bars")
        if self.peak_tolerance_pct < 0 or self.neckline_buffer_pct < 0 or self.breakout_pct < 0:
            raise ValueError("percentage thresholds must be non-negative")
        if self.lookback_bars <= self.max_separation_bars + (self.swing_window * 2):
            raise ValueError("lookback_bars must be large enough to contain the pattern search")

        start_index = max(0, index + 1 - self.lookback_bars)
        window = candles[start_index : index + 1]
        minimum_window = (self.swing_window * 2) + self.max_separation_bars + 3
        if len(window) < minimum_window:
            return 0

        bullish_breakout, bearish_breakdown = find_latest_pattern_matches(window, self.parameters)

        if bullish_breakout is None:
            return 0
        if bearish_breakdown is None:
            return 1
        return 1 if bullish_breakout.trigger_index > bearish_breakdown.trigger_index else 0
