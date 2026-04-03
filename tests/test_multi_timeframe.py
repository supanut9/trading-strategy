import unittest

from trading_strategy.models import Candle
from trading_strategy.strategies.multi_timeframe.ema_regime_rsi_entry import EmaRegimeRsiEntryStrategy


class EmaRegimeRsiEntryStrategyTests(unittest.TestCase):
    def test_returns_flat_until_enough_completed_higher_timeframe_bars_exist(self) -> None:
        candles = [
            Candle(f"2024-01-01 {hour:02d}:00", 100 + hour, 101 + hour, 99 + hour, 100 + hour, 1_000)
            for hour in range(12)
        ]
        strategy = EmaRegimeRsiEntryStrategy(
            period=2,
            oversold=40,
            overbought=60,
            trend_fast_window=2,
            trend_slow_window=3,
            timeframe_multiple=4,
        )

        self.assertEqual(strategy.desired_position(10, candles), 0)

    def test_enters_only_when_higher_timeframe_regime_is_bullish(self) -> None:
        candles = [
            Candle("2024-01-01 00:00", 100, 101, 99, 100, 1_000),
            Candle("2024-01-01 01:00", 100, 101, 98, 99, 1_000),
            Candle("2024-01-01 02:00", 99, 100, 97, 98, 1_000),
            Candle("2024-01-01 03:00", 98, 99, 97, 100, 1_000),
            Candle("2024-01-01 04:00", 100, 104, 99, 103, 1_000),
            Candle("2024-01-01 05:00", 103, 106, 102, 105, 1_000),
            Candle("2024-01-01 06:00", 105, 108, 104, 107, 1_000),
            Candle("2024-01-01 07:00", 107, 111, 106, 110, 1_000),
            Candle("2024-01-01 08:00", 110, 113, 109, 112, 1_000),
            Candle("2024-01-01 09:00", 112, 115, 111, 114, 1_000),
            Candle("2024-01-01 10:00", 114, 115, 112, 113, 1_000),
            Candle("2024-01-01 11:00", 113, 114, 111, 112, 1_000),
            Candle("2024-01-01 12:00", 112, 113, 110, 111, 1_000),
            Candle("2024-01-01 13:00", 111, 112, 98, 100, 1_000),
            Candle("2024-01-01 14:00", 100, 101, 95, 96, 1_000),
        ]
        strategy = EmaRegimeRsiEntryStrategy(
            period=2,
            oversold=35,
            overbought=70,
            trend_fast_window=2,
            trend_slow_window=3,
            timeframe_multiple=4,
        )

        self.assertEqual(strategy.desired_position(14, candles), 1)

    def test_exits_when_rsi_crosses_back_down_from_overbought(self) -> None:
        candles = [
            Candle("2024-01-01 00:00", 100, 101, 99, 100, 1_000),
            Candle("2024-01-01 01:00", 100, 101, 98, 99, 1_000),
            Candle("2024-01-01 02:00", 99, 100, 97, 98, 1_000),
            Candle("2024-01-01 03:00", 98, 99, 97, 100, 1_000),
            Candle("2024-01-01 04:00", 100, 104, 99, 103, 1_000),
            Candle("2024-01-01 05:00", 103, 106, 102, 105, 1_000),
            Candle("2024-01-01 06:00", 105, 108, 104, 107, 1_000),
            Candle("2024-01-01 07:00", 107, 111, 106, 110, 1_000),
            Candle("2024-01-01 08:00", 110, 113, 109, 112, 1_000),
            Candle("2024-01-01 09:00", 112, 115, 111, 114, 1_000),
            Candle("2024-01-01 10:00", 114, 117, 113, 116, 1_000),
            Candle("2024-01-01 11:00", 116, 118, 115, 117, 1_000),
            Candle("2024-01-01 12:00", 117, 117, 115, 116, 1_000),
            Candle("2024-01-01 13:00", 116, 120, 115, 119, 1_000),
            Candle("2024-01-01 14:00", 119, 120, 107, 108, 1_000),
        ]
        strategy = EmaRegimeRsiEntryStrategy(
            period=2,
            oversold=25,
            overbought=70,
            trend_fast_window=2,
            trend_slow_window=3,
            timeframe_multiple=4,
        )

        self.assertEqual(strategy.desired_position(14, candles), 0)


if __name__ == "__main__":
    unittest.main()
