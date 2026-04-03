import unittest
from unittest.mock import MagicMock, patch

from trading_strategy.cli import _build_backtest_tasks, _resolve_max_workers, _run_backtests
from trading_strategy.models import Candle
from trading_strategy.strategies.benchmark.buy_and_hold import BuyAndHoldStrategy
from trading_strategy.strategies.trend.sma_cross import SmaCrossStrategy


class CliTests(unittest.TestCase):
    def test_build_backtest_tasks_expands_strategy_and_risk_combinations(self) -> None:
        candles = [
            Candle("2024-01-01", 100, 101, 99, 100, 1_000),
            Candle("2024-01-02", 101, 102, 100, 101, 1_000),
        ]
        strategies = [
            BuyAndHoldStrategy(),
            SmaCrossStrategy(short_window=5, long_window=20),
        ]
        risk_profiles = [
            {},
            {
                "atr_period": 14,
                "stop_loss_atr_multiple": 1.5,
            },
        ]

        tasks = _build_backtest_tasks(
            candles=candles,
            strategies=strategies,
            risk_profiles=risk_profiles,
            initial_cash=10_000,
            commission_bps=10,
            slippage_bps=5,
            bars_per_year=252,
        )

        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0]["strategy"].name, "buy_and_hold")
        self.assertIsNone(tasks[0]["atr_period"])
        self.assertEqual(tasks[-1]["strategy"].name, "sma_cross")
        self.assertEqual(tasks[-1]["atr_period"], 14)
        self.assertEqual(tasks[-1]["stop_loss_atr_multiple"], 1.5)

    def test_resolve_max_workers_prefers_cli_value(self) -> None:
        self.assertEqual(_resolve_max_workers(5, 2), 5)
        self.assertEqual(_resolve_max_workers(None, 3), 3)
        self.assertEqual(_resolve_max_workers(None, None), 1)

    def test_resolve_max_workers_rejects_non_positive_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "max_workers must be positive"):
            _resolve_max_workers(0, None)

    @patch("trading_strategy.cli.ProcessPoolExecutor")
    def test_run_backtests_uses_process_pool_when_parallel_requested(self, executor_cls: MagicMock) -> None:
        executor = executor_cls.return_value.__enter__.return_value
        executor.map.return_value = ["result-a", "result-b"]

        results = _run_backtests([{"task": 1}, {"task": 2}], max_workers=5)

        self.assertEqual(results, ["result-a", "result-b"])
        executor_cls.assert_called_once_with(max_workers=5)
        executor.map.assert_called_once()

    @patch("trading_strategy.cli._run_single_backtest")
    def test_run_backtests_executes_serially_with_single_worker(self, run_single_backtest: MagicMock) -> None:
        run_single_backtest.side_effect = ["result-a", "result-b"]

        results = _run_backtests([{"task": 1}, {"task": 2}], max_workers=1)

        self.assertEqual(results, ["result-a", "result-b"])
        self.assertEqual(run_single_backtest.call_count, 2)


if __name__ == "__main__":
    unittest.main()
