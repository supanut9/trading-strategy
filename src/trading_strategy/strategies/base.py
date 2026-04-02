from __future__ import annotations

from abc import ABC, abstractmethod

from trading_strategy.models import Candle


class Strategy(ABC):
    name: str
    parameters: dict

    @abstractmethod
    def desired_position(self, index: int, candles: list[Candle]) -> int:
        """
        Return the intended position state using data up to `index`.

        Signal semantics:
        - `1`: be long
        - `0`: be flat
        - `-1`: keep the current position unchanged
        """
