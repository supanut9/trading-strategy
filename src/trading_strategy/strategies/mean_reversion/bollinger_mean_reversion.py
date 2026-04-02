from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import population_standard_deviation, simple_average


@dataclass(frozen=True)
class BollingerMeanReversionStrategy(Strategy):
    period: int
    band_width: float
    name: str = "bollinger_mean_reversion"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "band_width": self.band_width,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.period <= 1:
            raise ValueError("period must be greater than 1")
        if self.band_width <= 0:
            raise ValueError("band_width must be positive")
        if index + 1 < self.period:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        window = closes[-self.period :]
        middle_band = simple_average(window)
        std_dev = population_standard_deviation(window)
        lower_band = middle_band - (std_dev * self.band_width)
        current_close = closes[-1]

        if current_close <= lower_band:
            return 1
        if current_close >= middle_band:
            return 0
        return -1
