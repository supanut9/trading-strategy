# RSI + EMA Strategy Family

## Summary

- family: `RSI + EMA`
- category: `multi_indicator`
- status: exploratory
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
- indicators used:
  - `RSI`
  - `EMA`

## Core Hypothesis

RSI can identify pullback entries, while EMA can decide whether the broader market regime is supportive enough to take those entries.

This combined family is meant to answer a specific question:

- does RSI become better when it is only allowed to trade inside an EMA-defined regime?

## Indicators

- primary indicators:
  - `RSI`
  - `EMA`
- optional filters:
  - long EMA regime filter
  - EMA slope filter
  - EMA stack filter
- exit logic components:
  - RSI overbought exit
  - RSI cross-down exit
  - confirmation-based exit
- indicator roles:
  - entry trigger: `RSI`
  - regime filter: `EMA`
  - exit trigger: usually `RSI`
  - risk control: can later include cooldown, ATR stop, or trade suppression

## Timeframe Context

- symbol: `BTCUSDT`
- market: `spot`
- tested timeframes:
  - `1h`
  - `4h` on direct Binance candles
- default execution timeframe: `1h`
- multi-timeframe: `no`
- timeframe roles:
  - entry timeframe: `1h`
  - filter timeframe: `1h`
  - exit timeframe: `1h`
  - execution timeframe: `1h`

## Variants

### Variant: `rsi_entry_with_long_ema_filter`

- logic: enter on RSI oversold only when price is above a long EMA
- status: tested, rejected in current form
- indicators used:
  - `RSI` for entry and exit
  - `EMA` for regime filter
- notes: the tested `150/200 EMA` filters removed all trades on the current sample

### Variant: `rsi_confirmation_with_ema_filter`

- logic: confirmation-entry RSI combined with EMA regime filter
- status: not tested yet
- indicators used:
  - `RSI` for entry and exit
  - `EMA` for regime filter
- notes: candidate future branch if we revisit filtered RSI with a less restrictive EMA condition

### Variant: `rsi_with_ema_slope_filter`

- logic: RSI entry allowed only when a long EMA is rising
- status: not tested yet
- indicators used:
  - `RSI` for entry and exit
  - `EMA` for regime filter
- notes: this may be more flexible than requiring price strictly above a long EMA

### Variant: `rsi_with_ema_stack_filter`

- logic: RSI entry allowed only when a faster EMA is above a slower EMA
- status: not tested yet
- indicators used:
  - `RSI` for entry and exit
  - `EMA` pair for regime filter
- notes: candidate for a softer regime definition than `price > 200 EMA`

## Active Best Candidates

No active mixed `RSI + EMA` candidate yet.

No mixed `RSI + EMA` variant has produced a meaningful edge yet.

The broad matrix still failed to produce a strong mixed candidate on either `1h` or `4h`.

## Timeframe Findings

- `1h`:
  - tested mixed variants produced zero trades across the current grids
- `4h`:
  - some slope and stack variants finally produced trades
  - best meaningful result was still weak:
    - `rsi_mean_reversion_ema_stack_filter 22 / 18 / 63 with 50/200 EMA stack`
    - `+1.59%`, Sharpe `0.17`, trades `3`
  - conclusion: mixed `RSI + EMA` remains exploratory and clearly trails plain RSI

## Experiment History

### Experiment

- date: `2026-04-01`
- variant: `rsi_entry_with_long_ema_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: filtering RSI entries with a long EMA may remove weak counter-trend trades
- config: `configs/btcusdt_spot_1h.rsi_ema_filter.json`
- result file: `results/btcusdt_spot_1h_rsi_ema_filter_5000.json`
- parameters:
  - tested around `period=22`
  - `oversold=18-21`
  - `overbought=63-64`
  - `filter_window=150, 200`
- total return: `0.00%`
- max drawdown: `0.00%`
- Sharpe: `0.00`
- trades: `0`
- win rate: `0.00%`
- exposure: `0.00%`
- conclusion: this filter definition was too restrictive and removed the branch entirely

### Experiment

- date: `2026-04-01`
- variant: `rsi_entry_with_long_ema_filter`, `rsi_with_ema_slope_filter`, `rsi_with_ema_stack_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: softer EMA regime definitions may allow RSI+EMA to work where the hard long-EMA filter failed
- config:
  - `configs/btcusdt_spot_1h.family_matrix.json`
  - `configs/btcusdt_spot_4h.family_matrix.json`
- result file:
  - `results/btcusdt_spot_1h_family_matrix_5000.json`
  - `results/btcusdt_spot_4h_family_matrix_5000.json`
- conclusion: `1h` mixed variants still failed, while `4h` mixed variants finally traded but remained too weak to compete with plain RSI

## Rejected Or De-Prioritized Ideas

- idea: `price > 150 EMA` or `price > 200 EMA` as the first mixed RSI+EMA regime gate
- why it was rejected: it produced zero trades on the profitable RSI region
- evidence:
  - `results/btcusdt_spot_1h_rsi_ema_filter_5000.json`

## Next Experiments

- next: test `RSI + EMA slope` instead of `RSI + price-above-long-EMA`
- reason: it may preserve more trades while still filtering weak regimes

- next: test `RSI + EMA stack filter`
- reason: a softer EMA regime rule may work better than a hard `price > 150/200 EMA` requirement
