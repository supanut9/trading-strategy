# Repo Boundaries

This repository is a strategy research lab.

Its purpose is to support:

- strategy development
- backtesting
- parameter sweeps
- rolling validation
- result comparison
- research documentation

## Keep In This Repo

- strategy classes under `src/trading_strategy/strategies/`
- indicator helpers
- backtest engine and metrics
- experiment CLI
- experiment configs under `configs/`
- historical datasets under `data/`
- generated result files under `results/`
- rolling-window validation workflows
- research notes and strategy docs under `docs/`
- backtest-only portfolio simulation, if added later for research

## Do Not Add To This Repo

- exchange API integrations
- REST or WebSocket broker clients
- API key or secret management
- live order execution
- live position syncing
- account balance tracking
- real-time schedulers or background trade services
- production alerting, monitoring, or incident handling
- production portfolio routing across accounts
- paper trading tied to live market feeds

## Allowed If Research-Only

- more realistic fee, slippage, and execution assumptions
- multi-timeframe backtest logic
- multi-strategy portfolio simulation
- walk-forward validation
- result auditing and experiment review tools

These are allowed only if they remain:

- offline
- reproducible
- based on historical data
- runnable from the repository CLI or tests

## Decision Rule

If a feature needs any of the following, it belongs in a separate live-trading repository instead:

- API keys
- live market connectivity
- broker state
- account state
- persistent trading services
- real order placement

## Recommended Split

- `trading-strategy`: research, backtests, validation, docs
- separate bot repo: live data, portfolio orchestration, execution, monitoring
