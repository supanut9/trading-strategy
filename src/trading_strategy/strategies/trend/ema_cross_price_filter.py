from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average


@dataclass(frozen=True)
class EmaCrossPriceFilterStrategy(Strategy):
    short_window: int
    long_window: int
    filter_window: int
    name: str = "ema_cross_price_filter"

    @property
    def parameters(self) -> dict:
        return {
            "short_window": self.short_window,
            "long_window": self.long_window,
            "filter_window": self.filter_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.short_window >= self.long_window:
            raise ValueError("short_window must be smaller than long_window")
        if self.long_window >= self.filter_window:
            raise ValueError("long_window must be smaller than filter_window")
        if index + 1 < self.filter_window:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        short_ema = exponential_moving_average(closes, self.short_window)
        long_ema = exponential_moving_average(closes, self.long_window)
        filter_ema = exponential_moving_average(closes, self.filter_window)
        current_close = closes[-1]
        return 1 if short_ema > long_ema and current_close > filter_ema else 0
