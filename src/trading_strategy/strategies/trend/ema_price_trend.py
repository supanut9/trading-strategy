from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average


@dataclass(frozen=True)
class EmaPriceTrendStrategy(Strategy):
    ema_window: int
    slope_window: int
    name: str = "ema_price_trend"

    @property
    def parameters(self) -> dict:
        return {
            "ema_window": self.ema_window,
            "slope_window": self.slope_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.slope_window <= 0:
            raise ValueError("slope_window must be positive")
        minimum_bars = self.ema_window + self.slope_window
        if index + 1 < minimum_bars:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        current_ema = exponential_moving_average(closes, self.ema_window)
        previous_ema = exponential_moving_average(closes[: -self.slope_window], self.ema_window)
        current_close = closes[-1]
        return 1 if current_close > current_ema and current_ema > previous_ema else 0
