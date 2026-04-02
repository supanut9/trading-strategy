from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import average_true_range, exponential_moving_average, rsi


@dataclass(frozen=True)
class RsiEmaAtrVolatilityFilterStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    ema_window: int
    ema_slope_window: int
    atr_period: int
    min_atr_pct: float
    max_atr_pct: float
    name: str = "rsi_ema_atr_volatility_filter"

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "ema_window": self.ema_window,
            "ema_slope_window": self.ema_slope_window,
            "atr_period": self.atr_period,
            "min_atr_pct": self.min_atr_pct,
            "max_atr_pct": self.max_atr_pct,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if self.ema_window <= 0 or self.ema_slope_window <= 0 or self.atr_period <= 0:
            raise ValueError("window parameters must be positive")
        if self.min_atr_pct < 0 or self.max_atr_pct <= self.min_atr_pct:
            raise ValueError("ATR thresholds must be non-negative and max_atr_pct must exceed min_atr_pct")

        required_bars = max(self.period + 2, self.ema_window + self.ema_slope_window, self.atr_period + 1)
        if index + 1 < required_bars:
            return 0

        window = candles[: index + 1]
        closes = [candle.close for candle in window]
        highs = [candle.high for candle in window]
        lows = [candle.low for candle in window]

        previous_rsi = rsi(closes[:-1], self.period)
        current_rsi = rsi(closes, self.period)
        current_close = closes[-1]

        current_ema = exponential_moving_average(closes, self.ema_window)
        prior_ema = exponential_moving_average(closes[: -self.ema_slope_window], self.ema_window)
        atr = average_true_range(highs, lows, closes, self.atr_period)
        atr_pct = (atr / current_close) * 100

        bullish_regime = current_close > current_ema and current_ema > prior_ema
        healthy_volatility = self.min_atr_pct <= atr_pct <= self.max_atr_pct

        if bullish_regime and healthy_volatility and current_rsi <= self.oversold:
            return 1
        if previous_rsi >= self.overbought and current_rsi < self.overbought:
            return 0
        if not bullish_regime:
            return 0
        return -1
