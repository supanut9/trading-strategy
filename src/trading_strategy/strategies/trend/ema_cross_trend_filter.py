from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average


@dataclass(frozen=True)
class EmaCrossTrendFilterStrategy(Strategy):
    short_window: int
    long_window: int
    trend_fast_window: int
    trend_slow_window: int
    name: str = "ema_cross_trend_filter"

    @property
    def parameters(self) -> dict:
        return {
            "short_window": self.short_window,
            "long_window": self.long_window,
            "trend_fast_window": self.trend_fast_window,
            "trend_slow_window": self.trend_slow_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be smaller than long_window")
        if self.trend_fast_window >= self.trend_slow_window:
            raise ValueError("trend_fast_window must be smaller than trend_slow_window")
        minimum_window = max(self.long_window, self.trend_slow_window)
        if index + 1 < minimum_window:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        short_ema = exponential_moving_average(closes, self.short_window)
        long_ema = exponential_moving_average(closes, self.long_window)
        trend_fast_ema = exponential_moving_average(closes, self.trend_fast_window)
        trend_slow_ema = exponential_moving_average(closes, self.trend_slow_window)
        return 1 if short_ema > long_ema and trend_fast_ema > trend_slow_ema else 0
