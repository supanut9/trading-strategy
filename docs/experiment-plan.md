# Strategy Experiment Plan

## Goal

Find which strategy family is most robust for an auto-trading bot, not which one looks best on one lucky backtest.

## Active Scope

The active experiment track is currently:

- symbol: `BTCUSDT`
- market type: `spot`
- timeframe: `1h`

Do not widen scope until this track has a stable baseline.

## Phase 1 Scope

Start narrow:

- one market at a time
- one timeframe at a time
- long-only execution
- one position at a time
- fixed transaction cost assumptions

This is intentionally constrained so results stay interpretable.

## Baseline Hypotheses

Test three broad ideas before inventing complex models:

1. Trend following
   - Example: moving-average crossover
   - Hypothesis: works better in persistent directional markets
2. Mean reversion
   - Example: RSI oversold/overbought
   - Hypothesis: works better in range-bound markets
3. Breakout
   - Example: Donchian channel breakout
   - Hypothesis: captures expansion after consolidation

Always include buy-and-hold as a benchmark.

## Decision Rules

Treat a strategy as promising only if it satisfies most of these:

- positive return after costs
- max drawdown within acceptable risk
- enough trades to be statistically interesting
- performance does not depend on one exact parameter pair
- still behaves reasonably on out-of-sample data

## Minimum Experiment Loop

1. Choose one symbol and timeframe.
2. Backtest all baseline strategies with modest parameter grids.
3. Rank by risk-adjusted return, not just total return.
4. Inspect top candidates for trade count and drawdown.
5. Re-run top candidates on a different period.

## Common Failure Modes

- overfitting to one date range
- ignoring fees and slippage
- choosing strategies with too few trades
- optimizing only for return
- mixing markets and timeframes too early

## Promotion Path

Use this gate before live automation:

1. historical backtest passes
2. out-of-sample test passes
3. paper trading passes
4. risk limits are defined
5. live execution is enabled with small size

## First Dataset

Start with `BTCUSDT spot 1h` only.

Avoid mixing in other coins, futures, or other timeframes until the baseline families are separated cleanly and their behavior is understood.
