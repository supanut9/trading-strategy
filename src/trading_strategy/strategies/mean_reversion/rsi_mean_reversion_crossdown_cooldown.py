from __future__ import annotations

from dataclasses import dataclass, field

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.indicators import rsi


@dataclass
class RsiMeanReversionCrossdownCooldownStrategy(Strategy):
    period: int
    oversold: float
    overbought: float
    cooldown_bars: int
    name: str = "rsi_mean_reversion_crossdown_cooldown"
    _cache_key: tuple[int, int] | None = field(default=None, init=False, repr=False)
    _positions: list[int] = field(default_factory=list, init=False, repr=False)

    @property
    def parameters(self) -> dict:
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought,
            "cooldown_bars": self.cooldown_bars,
        }

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if self.oversold >= self.overbought:
            raise ValueError("oversold must be smaller than overbought")
        if self.cooldown_bars < 0:
            raise ValueError("cooldown_bars must be non-negative")
        if index + 1 < self.period + 2:
            return 0
        cache_key = (id(candles), len(candles))
        if self._cache_key != cache_key:
            self._cache_key = cache_key
            self._positions = self._build_positions(candles)
        return self._positions[index]

    def _build_positions(self, candles: list[Candle]) -> list[int]:
        positions = [0] * len(candles)
        in_position = False
        cooldown_remaining = 0

        closes: list[float] = []
        for current_index, candle in enumerate(candles):
            closes.append(candle.close)
            if current_index + 1 < self.period + 2:
                positions[current_index] = 0
                continue

            previous_rsi = rsi(closes[:-1], self.period)
            current_rsi = rsi(closes, self.period)

            if in_position:
                if previous_rsi >= self.overbought and current_rsi < self.overbought:
                    in_position = False
                    cooldown_remaining = self.cooldown_bars
                    positions[current_index] = 0
                    continue

                positions[current_index] = -1
                continue

            if cooldown_remaining > 0:
                cooldown_remaining -= 1
                positions[current_index] = 0
                continue

            if current_rsi <= self.oversold:
                in_position = True
                positions[current_index] = 1
                continue

            positions[current_index] = -1

        return positions
