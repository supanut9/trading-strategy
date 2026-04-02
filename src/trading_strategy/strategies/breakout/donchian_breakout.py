from __future__ import annotations

from dataclasses import dataclass

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy


@dataclass(frozen=True)
class DonchianBreakoutStrategy(Strategy):
    lookback: int
    exit_lookback: int
    name: str = "donchian_breakout"

    @property
    def parameters(self) -> dict:
        return {
            "lookback": self.lookback,
            "exit_lookback": self.exit_lookback,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.exit_lookback > self.lookback:
            raise ValueError("exit_lookback must be smaller than or equal to lookback")
        if index < self.lookback:
            return 0

        current_close = candles[index].close
        breakout_window = candles[index - self.lookback : index]
        exit_window = candles[index - self.exit_lookback : index]
        breakout_high = max(candle.high for candle in breakout_window)
        exit_low = min(candle.low for candle in exit_window)

        if current_close > breakout_high:
            return 1
        if current_close < exit_low:
            return 0
        return -1
