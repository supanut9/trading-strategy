from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import rsi


@dataclass(frozen=True)
class RsiMeanReversionConfirmationStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    name: str = "rsi_mean_reversion_confirmation"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if index + 1 < self.period + 2:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        previous_rsi = rsi(closes[:-1], self.period)
        current_rsi = rsi(closes, self.period)

        if previous_rsi <= self.oversold and current_rsi > self.oversold:
            return 1
        if current_rsi >= self.overbought:
            return 0
        return -1
