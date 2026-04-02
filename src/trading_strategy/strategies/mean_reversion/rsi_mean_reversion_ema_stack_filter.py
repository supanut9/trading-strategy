from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average, rsi


@dataclass(frozen=True)
class RsiMeanReversionEmaStackFilterStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    fast_filter_window: int
    slow_filter_window: int
    name: str = "rsi_mean_reversion_ema_stack_filter"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "fast_filter_window": self.fast_filter_window,
            "slow_filter_window": self.slow_filter_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if self.fast_filter_window >= self.slow_filter_window:
            raise ValueError("fast_filter_window must be smaller than slow_filter_window")
        required_bars = max(self.period + 1, self.slow_filter_window)
        if index + 1 < required_bars:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        current_rsi = rsi(closes, self.period)
        fast_filter_ema = exponential_moving_average(closes, self.fast_filter_window)
        slow_filter_ema = exponential_moving_average(closes, self.slow_filter_window)

        if fast_filter_ema <= slow_filter_ema:
            return 0
        if current_rsi <= self.oversold:
            return 1
        if current_rsi >= self.overbought:
            return 0
        return -1
