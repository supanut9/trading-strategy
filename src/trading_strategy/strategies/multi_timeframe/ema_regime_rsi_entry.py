from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import exponential_moving_average, rsi


@dataclass(frozen=True)
class EmaRegimeRsiEntryStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    trend_fast_window: int
    trend_slow_window: int
    timeframe_multiple: int = 4
    name: str = "ema_regime_rsi_entry"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "trend_fast_window": self.trend_fast_window,
            "trend_slow_window": self.trend_slow_window,
            "timeframe_multiple": self.timeframe_multiple,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if self.trend_fast_window >= self.trend_slow_window:
            raise ValueError("trend_fast_window must be smaller than trend_slow_window")
        if self.timeframe_multiple <= 1:
            raise ValueError("timeframe_multiple must be greater than 1")
        if index + 1 < self.period + 2:
            return 0

        higher_timeframe_closes = _completed_higher_timeframe_closes(
            candles[: index + 1],
            self.timeframe_multiple,
        )
        if len(higher_timeframe_closes) < self.trend_slow_window:
            return 0

        trend_fast_ema = exponential_moving_average(higher_timeframe_closes, self.trend_fast_window)
        trend_slow_ema = exponential_moving_average(higher_timeframe_closes, self.trend_slow_window)
        if trend_fast_ema <= trend_slow_ema:
            return 0

        closes = [candle.close for candle in candles[: index + 1]]
        previous_rsi = rsi(closes[:-1], self.period)
        current_rsi = rsi(closes, self.period)

        if previous_rsi >= self.overbought and current_rsi < self.overbought:
            return 0
        if current_rsi <= self.oversold:
            return 1
        return -1


def _completed_higher_timeframe_closes(candles: list[Candle], timeframe_multiple: int) -> list[float]:
    completed_bar_count = len(candles) // timeframe_multiple
    return [
        candles[((bar_index + 1) * timeframe_multiple) - 1].close
        for bar_index in range(completed_bar_count)
    ]
