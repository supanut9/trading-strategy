from __future__ import annotations

from dataclasses import dataclass, field

from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy


@dataclass(frozen=True)
class BuyAndHoldStrategy(Strategy):
    name: str = "buy_and_hold"
    parameters: dict = field(default_factory=dict)

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        return 1 if index >= 0 else 0
