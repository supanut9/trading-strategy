import json
import tempfile
import unittest
from pathlib import Path

from trading_strategy.portfolio import compare_portfolio_from_config


class PortfolioComparisonTests(unittest.TestCase):
    def test_compare_portfolio_combines_weighted_equity_curves(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            first_result = _write_result_file(
                base_path / "first.json",
                equity_curve=[1000.0, 1100.0, 1210.0],
                exposure_pct=20.0,
                strategy_name="strategy_a",
            )
            second_result = _write_result_file(
                base_path / "second.json",
                equity_curve=[1000.0, 1000.0, 1050.0],
                exposure_pct=40.0,
                strategy_name="strategy_b",
            )

            result = compare_portfolio_from_config(
                {
                    "initial_cash": 1000,
                    "bars_per_year": 252,
                    "components": [
                        {"result_file": first_result.name, "result_rank": 1, "weight": 0.6, "label": "alpha"},
                        {"result_file": second_result.name, "result_rank": 1, "weight": 0.4, "label": "beta"},
                    ],
                },
                base_path=base_path,
            )

            self.assertEqual(result.equity_curve, [1000.0, 1060.0, 1146.0])
            self.assertEqual(result.metrics.ending_equity, 1146.0)
            self.assertAlmostEqual(result.metrics.total_return_pct, 14.6)
            self.assertAlmostEqual(result.metrics.exposure_pct, 28.0)
            self.assertEqual([component.label for component in result.components], ["alpha", "beta"])

    def test_compare_portfolio_rejects_weights_that_do_not_sum_to_one(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            result_path = _write_result_file(base_path / "result.json", equity_curve=[1000.0, 1010.0], exposure_pct=10.0)

            with self.assertRaisesRegex(ValueError, "weights must sum to 1.0"):
                compare_portfolio_from_config(
                    {
                        "components": [
                            {"result_file": result_path.name, "weight": 0.7},
                            {"result_file": result_path.name, "weight": 0.2},
                        ]
                    },
                    base_path=base_path,
                )

    def test_compare_portfolio_rejects_mismatched_curve_lengths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            first_result = _write_result_file(base_path / "first.json", equity_curve=[1000.0, 1100.0], exposure_pct=10.0)
            second_result = _write_result_file(base_path / "second.json", equity_curve=[1000.0, 1050.0, 1100.0], exposure_pct=20.0)

            with self.assertRaisesRegex(ValueError, "matching equity curve lengths"):
                compare_portfolio_from_config(
                    {
                        "components": [
                            {"result_file": first_result.name, "weight": 0.5},
                            {"result_file": second_result.name, "weight": 0.5},
                        ]
                    },
                    base_path=base_path,
                )

    def test_compare_portfolio_supports_selecting_non_top_rank(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_path = Path(temp_dir)
            result_path = base_path / "ranked.json"
            payload = {
                "results": [
                    _result_payload(equity_curve=[1000.0, 1100.0], exposure_pct=15.0, strategy_name="top"),
                    _result_payload(equity_curve=[1000.0, 1200.0], exposure_pct=25.0, strategy_name="second"),
                ]
            }
            result_path.write_text(json.dumps(payload), encoding="utf-8")

            result = compare_portfolio_from_config(
                {
                    "components": [
                        {"result_file": result_path.name, "result_rank": 2, "weight": 1.0},
                    ]
                },
                base_path=base_path,
            )

            self.assertEqual(result.components[0].strategy_name, "second")
            self.assertEqual(result.equity_curve, [1000.0, 1200.0])


def _write_result_file(path: Path, *, equity_curve: list[float], exposure_pct: float, strategy_name: str = "strategy") -> Path:
    payload = {"results": [_result_payload(equity_curve=equity_curve, exposure_pct=exposure_pct, strategy_name=strategy_name)]}
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _result_payload(*, equity_curve: list[float], exposure_pct: float, strategy_name: str) -> dict:
    return {
        "strategy_name": strategy_name,
        "parameters": {"example": 1},
        "execution_parameters": {},
        "metrics": {
            "ending_equity": equity_curve[-1],
            "total_return_pct": 0.0,
            "annualized_return_pct": 0.0,
            "max_drawdown_pct": 0.0,
            "sharpe": 0.0,
            "trade_count": 0,
            "win_rate_pct": 0.0,
            "profit_factor": 0.0,
            "exposure_pct": exposure_pct,
        },
        "equity_curve": equity_curve,
        "trades": [],
    }


if __name__ == "__main__":
    unittest.main()
