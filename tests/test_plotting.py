import tempfile
import unittest
from pathlib import Path

from trading_strategy.backtest import run_backtest
from trading_strategy.models import Candle
from trading_strategy.plotting import write_backtest_svg
from trading_strategy.strategies.benchmark.buy_and_hold import BuyAndHoldStrategy


class PlottingTests(unittest.TestCase):
    def test_write_backtest_svg_creates_svg_file(self) -> None:
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

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "chart.svg"
            write_backtest_svg(candles, result, output, title="Test Chart")
            content = output.read_text(encoding="utf-8")

        self.assertIn("<svg", content)
        self.assertIn("Test Chart", content)
        self.assertIn("Equity", content)

    def test_write_backtest_svg_renders_annotations(self) -> None:
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

        annotations = [
            {"kind": "point", "index": 1, "value": 102, "label": "Bottom 1", "color": "#7c3aed"},
            {"kind": "horizontal_line", "start_index": 0, "end_index": 3, "value": 105, "label": "Neckline", "color": "#ea580c"},
            {"kind": "box_text", "lines": ["Pivot diff 0.8%", "Neck move 2.1%"], "color": "#2563eb"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "annotated.svg"
            write_backtest_svg(candles, result, output, title="Annotated", annotations=annotations)
            content = output.read_text(encoding="utf-8")

        self.assertIn("Bottom 1", content)
        self.assertIn("Neckline", content)
        self.assertIn("Pivot diff 0.8%", content)


if __name__ == "__main__":
    unittest.main()
