from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average


@dataclass(frozen=True)
class EmaTriplePullbackTrailingExitStrategy(Strategy):
    fast_window: int
    middle_window: int
    slow_window: int
    pullback_pct: float
    trailing_window: int
    name: str = "ema_triple_pullback_trailing_exit"

    @property
    def parameters(self) -> dict:
        return {
            "fast_window": self.fast_window,
            "middle_window": self.middle_window,
            "slow_window": self.slow_window,
            "pullback_pct": self.pullback_pct,
            "trailing_window": self.trailing_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if not (self.fast_window < self.middle_window < self.slow_window):
            raise ValueError("fast_window must be smaller than middle_window and middle_window smaller than slow_window")
        if self.pullback_pct < 0:
            raise ValueError("pullback_pct must be non-negative")
        if self.trailing_window <= 0:
            raise ValueError("trailing_window must be positive")
        required_bars = max(self.slow_window, self.trailing_window)
        if index + 1 < required_bars:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        fast_ema = exponential_moving_average(closes, self.fast_window)
        middle_ema = exponential_moving_average(closes, self.middle_window)
        slow_ema = exponential_moving_average(closes, self.slow_window)
        trailing_ema = exponential_moving_average(closes, self.trailing_window)
        current_close = closes[-1]

        if not (fast_ema > middle_ema > slow_ema):
            return 0
        if current_close < trailing_ema:
            return 0

        distance_from_middle = abs(current_close - middle_ema) / middle_ema
        if distance_from_middle <= self.pullback_pct:
            return 1
        return -1
