import unittest

from trading_strategy.backtest import run_backtest
from trading_strategy.models import Candle
from trading_strategy.strategies.base import Strategy
from trading_strategy.strategies.benchmark.buy_and_hold import BuyAndHoldStrategy
from trading_strategy.strategies.breakout.bollinger_squeeze_breakout import BollingerSqueezeBreakoutStrategy
from trading_strategy.strategies.breakout.bollinger_squeeze_breakout_trend_filter import (
    BollingerSqueezeBreakoutTrendFilterStrategy,
)
from trading_strategy.strategies.breakout.donchian_breakout import DonchianBreakoutStrategy


class OneShotLongStrategy(Strategy):
    name = "one_shot_long"
    parameters = {}

    def desired_position(self, index: int, candles: list[Candle]) -> int:
        if index <= 1:
            return 1
        if index == 2:
            return -1
        return 0


class BacktestTests(unittest.TestCase):
    def test_buy_and_hold_generates_positive_return_in_uptrend(self) -> None:
        candles = [
            Candle("2024-01-01", 100, 101, 99, 100, 1_000),
            Candle("2024-01-02", 101, 103, 100, 102, 1_000),
            Candle("2024-01-03", 102, 106, 101, 105, 1_000),
            Candle("2024-01-04", 105, 109, 104, 108, 1_000),
        ]

        result = run_backtest(
            candles,
            BuyAndHoldStrategy(),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
        )

        self.assertGreater(result.metrics.total_return_pct, 0)
        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].entry_time, "2024-01-02")
        self.assertEqual(result.trades[0].exit_time, "2024-01-04")

    def test_donchian_breakout_waits_for_breakout_before_entering(self) -> None:
        candles = [
            Candle("2024-01-01", 10, 10, 9, 9.5, 1_000),
            Candle("2024-01-02", 9.5, 10, 9, 9.8, 1_000),
            Candle("2024-01-03", 9.8, 10, 9.7, 9.9, 1_000),
            Candle("2024-01-04", 10.2, 10.8, 10.1, 10.7, 1_000),
            Candle("2024-01-05", 10.8, 11.0, 10.7, 10.9, 1_000),
        ]

        result = run_backtest(
            candles,
            DonchianBreakoutStrategy(lookback=3, exit_lookback=2),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
        )

        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].entry_time, "2024-01-05")

    def test_bollinger_squeeze_breakout_enters_after_compression_and_exits_on_channel_loss(self) -> None:
        candles = [
            Candle("2024-01-01", 100.0, 100.2, 99.9, 100.0, 1_000),
            Candle("2024-01-02", 100.0, 100.2, 99.95, 100.1, 1_000),
            Candle("2024-01-03", 100.1, 100.15, 100.0, 100.05, 1_000),
            Candle("2024-01-04", 100.05, 101.5, 100.0, 101.3, 1_000),
            Candle("2024-01-05", 101.4, 101.6, 99.0, 99.2, 1_000),
            Candle("2024-01-06", 99.0, 99.2, 98.8, 99.1, 1_000),
        ]

        result = run_backtest(
            candles,
            BollingerSqueezeBreakoutStrategy(
                period=3,
                band_width=2.0,
                squeeze_threshold_pct=1.0,
                breakout_lookback=3,
                exit_lookback=2,
            ),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
        )

        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].entry_time, "2024-01-05")
        self.assertEqual(result.trades[0].exit_time, "2024-01-06")

    def test_bollinger_squeeze_breakout_trend_filter_requires_bullish_ema_regime(self) -> None:
        candles = [
            Candle("2024-01-01", 100.0, 101.0, 99.0, 100.0, 1_000),
            Candle("2024-01-02", 99.5, 100.0, 98.5, 99.0, 1_000),
            Candle("2024-01-03", 99.0, 99.5, 98.5, 99.4, 1_000),
            Candle("2024-01-04", 99.4, 99.6, 99.2, 99.5, 1_000),
            Candle("2024-01-05", 99.5, 99.7, 99.4, 99.6, 1_000),
            Candle("2024-01-06", 99.6, 102.5, 99.5, 102.2, 1_000),
            Candle("2024-01-07", 102.0, 102.1, 97.5, 98.0, 1_000),
            Candle("2024-01-08", 98.0, 98.2, 97.8, 98.1, 1_000),
        ]

        result = run_backtest(
            candles,
            BollingerSqueezeBreakoutTrendFilterStrategy(
                period=3,
                band_width=2.0,
                squeeze_threshold_pct=1.0,
                breakout_lookback=3,
                exit_lookback=2,
                trend_ema_window=3,
                trend_slope_window=2,
            ),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
        )

        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].entry_time, "2024-01-07")
        self.assertEqual(result.trades[0].exit_time, "2024-01-08")

    def test_atr_take_profit_exits_trade_intrabar(self) -> None:
        candles = [
            Candle("2024-01-01", 100, 102, 99, 100, 1_000),
            Candle("2024-01-02", 101, 103, 100, 102, 1_000),
            Candle("2024-01-03", 103, 110, 102, 109, 1_000),
            Candle("2024-01-04", 109, 111, 108, 110, 1_000),
        ]

        result = run_backtest(
            candles,
            OneShotLongStrategy(),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
            atr_period=1,
            take_profit_atr_multiple=2.0,
        )

        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].entry_time, "2024-01-03")
        self.assertEqual(result.trades[0].exit_time, "2024-01-03")
        self.assertAlmostEqual(result.trades[0].exit_price, 109.0)
        self.assertEqual(
            result.execution_parameters,
            {"atr_period": 1, "take_profit_atr_multiple": 2.0},
        )

    def test_atr_stop_loss_takes_priority_when_stop_and_target_hit_same_bar(self) -> None:
        candles = [
            Candle("2024-01-01", 100, 102, 99, 100, 1_000),
            Candle("2024-01-02", 101, 103, 100, 102, 1_000),
            Candle("2024-01-03", 103, 110, 99, 108, 1_000),
            Candle("2024-01-04", 108, 110, 107, 109, 1_000),
        ]

        result = run_backtest(
            candles,
            OneShotLongStrategy(),
            initial_cash=10_000,
            commission_bps=0,
            slippage_bps=0,
            bars_per_year=252,
            atr_period=1,
            stop_loss_atr_multiple=1.0,
            take_profit_atr_multiple=2.0,
        )

        self.assertEqual(result.metrics.trade_count, 1)
        self.assertEqual(result.trades[0].exit_time, "2024-01-03")
        self.assertAlmostEqual(result.trades[0].exit_price, 100.0)
        self.assertLess(result.trades[0].pnl, 0)


if __name__ == "__main__":
    unittest.main()
