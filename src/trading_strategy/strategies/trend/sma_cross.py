from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import simple_average


@dataclass(frozen=True)
class SmaCrossStrategy(Strategy):
    short_window: int
    long_window: int
    name: str = "sma_cross"

    @property
    def parameters(self) -> dict:
        return {
            "short_window": self.short_window,
            "long_window": self.long_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be smaller than long_window")
        if index + 1 < self.long_window:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        short_sma = simple_average(closes[-self.short_window :])
        long_sma = simple_average(closes[-self.long_window :])
        return 1 if short_sma > long_sma else 0
