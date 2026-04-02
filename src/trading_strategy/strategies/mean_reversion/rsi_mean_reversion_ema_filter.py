from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average, rsi


@dataclass(frozen=True)
class RsiMeanReversionEmaFilterStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    filter_window: int
    name: str = "rsi_mean_reversion_ema_filter"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "filter_window": self.filter_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if self.filter_window <= 0:
            raise ValueError("filter_window must be positive")
        required_bars = max(self.period + 1, self.filter_window)
        if index + 1 < required_bars:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        current_close = closes[-1]
        filter_ema = exponential_moving_average(closes, self.filter_window)
        current_rsi = rsi(closes, self.period)

        if current_close <= filter_ema:
            return 0
        if current_rsi <= self.oversold:
            return 1
        if current_rsi >= self.overbought:
            return 0
        return -1
