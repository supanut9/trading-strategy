from __future__ import annotations

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy


class MirrorShortStrategy(Strategy):
    supports_short_positions = True

    def __init__(self, base_strategy: Strategy) -> None:
        self.base_strategy = base_strategy
        self.name = f"{base_strategy.name}_mirror_short"
        self.parameters = dict(base_strategy.parameters)
        self._mirrored_candles: list[Candle] | None = None

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        mirrored_candles = self._get_mirrored_candles(candles)
        base_signal = self.base_strategy.desired_position(index, mirrored_candles)
        if base_signal == 1:
            return -1
        if base_signal == 0:
            return 0
        return 2

    def _get_mirrored_candles(self, candles: list[Candle]) -> list[Candle]:
        if self._mirrored_candles is not None and len(self._mirrored_candles) == len(candles):
            return self._mirrored_candles

        mirrored: list[Candle] = []
        for candle in candles:
            mirrored.append(
                Candle(
                    timestamp=candle.timestamp,
                    open=1 / candle.open,
                    high=1 / candle.low,
                    low=1 / candle.high,
                    close=1 / candle.close,
                    volume=candle.volume,
                )
            )

        self._mirrored_candles = mirrored
        return mirrored
