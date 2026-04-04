from __future__ import annotations

from abc import ABC, abstractmethod

from trading_strategy.models import Candle


class Strategy(ABC):
    name: str
    parameters: dict
    supports_short_positions: bool = False

    @abstractmethod
    def desired_position(self, index: int, candles: list[Candle]) -> int:
        """
        Return the intended position state using data up to `index`.

        Default signal semantics:
        - `1`: be long
        - `0`: be flat
        - `-1`: keep the current position unchanged

        Short-capable strategies may set `supports_short_positions = True`
        and then use:
        - `1`: be long
        - `0`: be flat
        - `-1`: be short
        - `2`: keep the current position unchanged
        """
