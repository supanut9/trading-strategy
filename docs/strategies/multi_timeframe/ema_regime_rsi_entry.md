# EMA Regime + RSI Entry

## Summary

- family: `EMA regime + RSI entry`
- category: `multi_timeframe`
- status: active scaffold, not tested yet
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h entry with 4h regime filter`
- indicators used:
  - `EMA`
  - `RSI`

## Core Hypothesis

A higher-timeframe `4h` EMA regime filter may remove the weakest `1h` RSI mean-reversion entries while preserving the strong hit rate of the base RSI branch.

## Indicators

- primary indicators:
  - `RSI` on `1h`
  - `EMA` on aggregated completed `4h` closes
- optional filters:
  - none yet beyond the `4h` regime gate
- exit logic components:
  - `1h` RSI cross-down from overbought
  - flat when the completed `4h` EMA regime turns bearish
- indicator roles:
  - entry trigger: `1h RSI oversold`
  - regime filter: `4h EMA fast above 4h EMA slow`
  - exit trigger: `1h RSI cross-down from overbought or loss of bullish 4h regime`
  - risk control: `currently implicit through regime filter and exit logic`

## Timeframe Context

- symbol: `BTCUSDT`
- market: `spot`
- tested timeframes:
  - `1h`
  - derived `4h`
- default execution timeframe: `1h`
- multi-timeframe: `yes`
- timeframe roles:
  - entry timeframe: `1h`
  - filter timeframe: `4h`
  - exit timeframe: `1h` plus `4h` regime invalidation
  - execution timeframe: `1h`

## Variants

### Variant: `ema_regime_rsi_entry`

- logic: enter on `1h` RSI oversold only when the latest completed `4h` fast EMA remains above the `4h` slow EMA
- status: active scaffold
- indicators used:
  - `1h RSI`
  - completed `4h` EMA regime
- notes: implemented as an aggregated higher-timeframe filter inside the strategy so the current single-timeframe backtest engine does not need architectural changes

## Active Best Candidates

- none yet

## Experiment History

- none yet

## Rejected Or De-Prioritized Ideas

- none yet

## Next Experiments

- next: run `configs/btcusdt_spot_1h.ema_regime_rsi_entry.json`
- reason: measure whether the `4h` trend gate improves drawdown or trade quality relative to the current leading `1h` RSI candidates
