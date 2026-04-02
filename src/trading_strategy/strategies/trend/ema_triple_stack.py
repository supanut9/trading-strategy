from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average


@dataclass(frozen=True)
class EmaTripleStackStrategy(Strategy):
    fast_window: int
    middle_window: int
    slow_window: int
    name: str = "ema_triple_stack"

    @property
    def parameters(self) -> dict:
        return {
            "fast_window": self.fast_window,
            "middle_window": self.middle_window,
            "slow_window": self.slow_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if not (self.fast_window < self.middle_window < self.slow_window):
            raise ValueError("fast_window must be smaller than middle_window and middle_window smaller than slow_window")
        if index + 1 < self.slow_window:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        fast_ema = exponential_moving_average(closes, self.fast_window)
        middle_ema = exponential_moving_average(closes, self.middle_window)
        slow_ema = exponential_moving_average(closes, self.slow_window)
        return 1 if fast_ema > middle_ema > slow_ema else 0
