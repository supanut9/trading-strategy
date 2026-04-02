from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import simple_average


@dataclass(frozen=True)
class SmaTriplePullbackFastExitStrategy(Strategy):
    fast_window: int
    middle_window: int
    slow_window: int
    pullback_pct: float
    name: str = "sma_triple_pullback_fast_exit"

    @property
    def parameters(self) -> dict:
        return {
            "fast_window": self.fast_window,
            "middle_window": self.middle_window,
            "slow_window": self.slow_window,
            "pullback_pct": self.pullback_pct,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if not (self.fast_window < self.middle_window < self.slow_window):
            raise ValueError("fast_window must be smaller than middle_window and middle_window smaller than slow_window")
        if self.pullback_pct < 0:
            raise ValueError("pullback_pct must be non-negative")
        if index + 1 < self.slow_window:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        fast_sma = simple_average(closes[-self.fast_window :])
        middle_sma = simple_average(closes[-self.middle_window :])
        slow_sma = simple_average(closes[-self.slow_window :])
        current_close = closes[-1]

        if not (fast_sma > middle_sma > slow_sma):
            return 0
        if current_close < fast_sma:
            return 0

        distance_from_middle = abs(current_close - middle_sma) / middle_sma
        if distance_from_middle <= self.pullback_pct:
            return 1
        return -1
