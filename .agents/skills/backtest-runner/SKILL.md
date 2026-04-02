---
name: backtest-runner
description: Use when working in this repository to run a backtest or experiment, compare result files, or summarize strategy performance from config JSON and OHLCV CSV inputs. Do not use for creating new strategy modules.
---

# Backtest Runner

Use this skill for repeatable experiment execution in `trading-strategy`.

## When to use

- Running `python3 -m trading_strategy` with a config and dataset
- Listing available strategies before choosing a config
- Writing JSON or SVG outputs under `results/`
- Comparing ranked metrics across runs

## Workflow

1. Confirm the input files exist.
   Typical inputs are `configs/*.json` and `data/rolling/*.csv`.
2. Inspect the config when the request depends on ranking metric, strategy grid, or risk settings.
3. Run the CLI from the repository root.
4. If requested, write outputs to a dated or descriptive file in `results/`.
5. Summarize the top result using the printed ranking table and any saved JSON payload.

## Commands

List strategies:

```bash
python3 -m trading_strategy --list-strategies
```

Run an experiment:

```bash
python3 -m trading_strategy \
  --data data/rolling/btcusdt_spot_1h_window_1.csv \
  --config configs/btcusdt_spot_1h.baselines.json \
  --output results/baselines.window_1.json
```

Render a chart for the top-ranked strategy:

```bash
python3 -m trading_strategy \
  --data data/rolling/btcusdt_spot_1h_window_1.csv \
  --config configs/btcusdt_spot_1h.baselines.json \
  --output results/baselines.window_1.json \
  --plot-output results/baselines.window_1.svg
```

## Output expectations

- Report the ranking metric and top strategy name.
- Mention return, drawdown, Sharpe-like score, trade count, and win rate when available.
- Flag missing input files, empty results, or invalid config keys directly.
