from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import (
    exponential_moving_average,
    population_standard_deviation,
    simple_average,
)


@dataclass(frozen=True)
class BollingerSqueezeBreakoutTrendFilterStrategy(Strategy):
    period: int
    band_width: float
    squeeze_threshold_pct: float
    breakout_lookback: int
    exit_lookback: int
    trend_ema_window: int
    trend_slope_window: int
    name: str = "bollinger_squeeze_breakout_trend_filter"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "band_width": self.band_width,
            "squeeze_threshold_pct": self.squeeze_threshold_pct,
            "breakout_lookback": self.breakout_lookback,
            "exit_lookback": self.exit_lookback,
            "trend_ema_window": self.trend_ema_window,
            "trend_slope_window": self.trend_slope_window,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.period <= 1:
            raise ValueError("period must be greater than 1")
        if self.band_width <= 0:
            raise ValueError("band_width must be positive")
        if self.squeeze_threshold_pct <= 0:
            raise ValueError("squeeze_threshold_pct must be positive")
        if self.exit_lookback <= 0 or self.breakout_lookback <= 0:
            raise ValueError("lookback windows must be positive")
        if self.exit_lookback > self.breakout_lookback:
            raise ValueError("exit_lookback must be smaller than or equal to breakout_lookback")
        if self.trend_ema_window <= 0 or self.trend_slope_window <= 0:
            raise ValueError("trend filter windows must be positive")

        required_bars = max(
            self.period,
            self.breakout_lookback,
            self.exit_lookback,
            self.trend_ema_window + self.trend_slope_window,
        )
        if index < required_bars:
            return 0

        prior_closes = [candle.close for candle in candles[index - self.period : index]]
        middle_band = simple_average(prior_closes)
        if middle_band == 0:
            return 0

        std_dev = population_standard_deviation(prior_closes)
        band_span = std_dev * self.band_width * 2
        band_span_pct = (band_span / middle_band) * 100

        closes = [candle.close for candle in candles[: index + 1]]
        current_close = closes[-1]
        current_trend_ema = exponential_moving_average(closes, self.trend_ema_window)
        prior_trend_ema = exponential_moving_average(closes[: -self.trend_slope_window], self.trend_ema_window)
        bullish_trend = current_close > current_trend_ema and current_trend_ema > prior_trend_ema

        breakout_window = candles[index - self.breakout_lookback : index]
        exit_window = candles[index - self.exit_lookback : index]
        breakout_high = max(candle.high for candle in breakout_window)
        exit_low = min(candle.low for candle in exit_window)

        if bullish_trend and band_span_pct <= self.squeeze_threshold_pct and current_close > breakout_high:
            return 1
        if current_close < exit_low or not bullish_trend:
            return 0
        return -1
