# Repository Guidelines

## Project Structure & Module Organization

Core code lives under `src/trading_strategy/`. Use `cli.py` and `__main__.py` for entry points, `backtest.py` and `metrics.py` for execution and scoring, and `strategies/` for strategy implementations grouped by family such as `trend/`, `mean_reversion/`, `breakout/`, `pattern/`, and `multi_indicator/`. Tests live in `tests/` and currently focus on engine behavior, plotting, and strategy registration. Research notes and strategy docs belong in `docs/`, experiment definitions in `configs/`, rolling datasets in `data/rolling/`, and generated outputs in `results/`.

## Build, Test, and Development Commands

Set up a local environment with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the CLI against a config:

```bash
python3 -m trading_strategy --data path/to/ohlcv.csv --config configs/experiment.example.json --output results/latest.json
```

Useful commands:

- `python3 -m trading_strategy --list-strategies`: show registered strategies.
- `python3 -m unittest discover -s tests`: run the full test suite.
- `python3 -m pytest`: acceptable if `pytest` is installed, but the repository tests are written with `unittest`.

## Coding Style & Naming Conventions

Target Python 3.10+ and follow PEP 8 with 4-space indentation. Prefer small, explicit functions and typed signatures, matching existing modules such as `data.py` and `models.py`. Use `snake_case` for files, functions, variables, and config names like `btcusdt_spot_1h.ema.json`. Strategy classes use `PascalCase` and should expose a stable `name` string used by the registry and CLI.

## Testing Guidelines

Add tests in `tests/test_<area>.py`. Keep them deterministic and use compact inline candle fixtures where possible. New strategies should have at least one registration test and one behavioral backtest covering entries, exits, or risk rules. Prefer assertions on metrics, trade timestamps, and execution parameters over broad snapshot-style checks.

## Commit & Pull Request Guidelines

This repository has no established commit history yet, so use short imperative commit subjects such as `Add EMA slope filter strategy`. Keep commits focused on one change. Pull requests should summarize the strategy or engine change, list config or docs updates, and include before/after results when behavior changes materially. Link the relevant experiment config or issue when available.

## Data & Output Hygiene

Do not commit secrets or exchange credentials. Treat `data/` and `results/` as reproducible artifacts: keep raw inputs clean, avoid overwriting reference datasets silently, and write new outputs to clearly named files under `results/`.

## Repo Scope

This repository is for strategy research only. Keep it focused on backtests, validation, configs, results, and research documentation. Do not add live trading infrastructure such as exchange clients, order execution, API key handling, or real-time trading services. See `docs/repo-boundaries.md` for the full boundary.
