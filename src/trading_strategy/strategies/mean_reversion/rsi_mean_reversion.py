from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import rsi


@dataclass(frozen=True)
class RsiMeanReversionStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    name: str = "rsi_mean_reversion"

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
        if index + 1 < self.period + 1:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        current_rsi = rsi(closes, self.period)
        return 1 if current_rsi <= self.oversold else 0 if current_rsi >= self.overbought else -1
