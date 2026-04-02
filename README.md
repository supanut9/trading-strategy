# Trading Strategy Experiment Lab

This repository starts with one job: compare strategy ideas on historical data before wiring anything into a live auto-trading bot.

Current focus:

- market: `BTCUSDT`
- execution venue: `spot`
- timeframe: `1h`

The current scaffold gives you:

- a CSV-based backtesting workflow
- baseline strategies to compare against each other
- parameter grid expansion for repeatable experiments
- consistent metrics for ranking results

## Why Start This Way

The wrong first move is usually connecting a broker API and then testing ideas in production.

The better first move is:

1. define what "best" means
2. run the same historical data through multiple strategies
3. compare them using the same costs and metrics
4. only promote a strategy to paper trading after it survives backtests

## Project Layout

- `docs/experiment-plan.md`: experiment design and next-step workflow
- `docs/strategy-memory.md`: top-level memory and current leaders
- `docs/strategies/README.md`: structured strategy catalog
- `configs/btcusdt_spot_1h.baselines.json`: first BTC spot hourly baseline sweep
- `configs/experiment.example.json`: generic example experiment definition
- `src/trading_strategy/`: loader, backtest engine, CLI
- `src/trading_strategy/strategies/`: strategy families and registry
- `tests/`: lightweight verification

## Data Format

Input data must be CSV with these headers:

```text
timestamp,open,high,low,close,volume
```

Notes:

- `timestamp` is kept as text and echoed back into reports
- prices and volume must be numeric
- rows must be ordered oldest to newest

## Quick Start

Create a virtual environment if you want isolation:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run an experiment:

```bash
python3 -m trading_strategy \
  --data path/to/ohlcv.csv \
  --config configs/btcusdt_spot_1h.baselines.json \
  --output results/latest.json
```

The CLI prints a ranked table and optionally writes full JSON results.

To also render a chart image for the top-ranked strategy:

```bash
python3 -m trading_strategy \
  --data path/to/ohlcv.csv \
  --config configs/btcusdt_spot_1h.baselines.json \
  --output results/latest.json \
  --plot-output results/latest.svg
```

The SVG chart includes the price graph with entry and exit markers plus the equity curve.

You can also embed generated charts directly in markdown docs with normal Markdown image syntax, for example:

```md
![Backtest Chart](results/latest.svg)
```

To inspect the current strategy catalog:

```bash
python3 -m trading_strategy --list-strategies
```

## Initial Strategy Set

- `buy_and_hold`: benchmark only
- `sma_cross`: trend-following baseline
- `rsi_mean_reversion`: simple oversold/overbought reversal baseline
- `donchian_breakout`: breakout baseline

Each strategy now lives in its own module under `src/trading_strategy/strategies/` so we can evolve families independently as the test matrix grows.

Strategy research is also stored by family under `docs/strategies/` so each indicator family can keep its own variants, best candidates, and experiment history.
Mixed-indicator systems should go under `docs/strategies/multi_indicator/` and document each indicator's role explicitly.
If the same logic is tested on many timeframes, record each timeframe explicitly in the strategy doc. If the strategy mixes timeframes in one system, store it under `docs/strategies/multi_timeframe/`.

## What "Best" Should Mean

Do not optimize only for raw return. Start by comparing:

- total return
- annualized return
- max drawdown
- Sharpe-like score
- win rate
- trade count
- exposure

A strategy with slightly lower return and materially lower drawdown is often the better candidate for automation.

## Recommended Next Steps

1. Collect one clean `BTCUSDT spot 1h` dataset.
2. Run `configs/btcusdt_spot_1h.baselines.json` without touching parameters.
3. Narrow to one family that behaves sensibly on BTC hourly data.
4. Add out-of-sample testing and walk-forward validation.
5. Only then consider paper trading integration.
