# Bollinger Strategy Family

## Summary

- family: `Bollinger Bands`
- category: `mean_reversion`
- status: de-prioritized
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
- indicators used:
  - `SMA`
  - standard deviation
  - `Bollinger Bands`

## Core Hypothesis

Buying near the lower Bollinger Band and exiting near the middle band may create a high-win-rate mean-reversion system on BTC `1h`.

## Indicators

- primary indicators:
  - `SMA`
  - standard deviation
  - Bollinger Bands
- exit logic components:
  - exit at middle band
- indicator roles:
  - entry trigger: `price at or below lower band`
  - regime filter: `none`
  - exit trigger: `price at or above middle band`
  - risk control: `none in tested form`

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

### Variant: `bollinger_mean_reversion`

- logic: enter at or below the lower band, exit at or above the middle band
- status: de-prioritized
- notes: reached decent win rates but lost heavily after costs

## Active Best Candidates

### Candidate: `bollinger_best_tested`

- variant: `bollinger_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- parameters:
  - `period = 30`
  - `band_width = 1.2`
- config: `configs/btcusdt_spot_1h.high_winrate_search.json`
- result file: `results/btcusdt_spot_1h_high_winrate_search_5000.json`
- total return: `-44.01%`
- max drawdown: `46.95%`
- Sharpe: `-2.91`
- trades: `106`
- win rate: `62.26%`
- exposure: `38.09%`
- why it matters: highest-tested Bollinger hit rate, but still not acceptable because the branch lost too much money

## Timeframe Findings

- `1h`:
  - Bollinger hit rate looked decent, but every tested variant lost heavily
- `4h`:
  - Bollinger improved materially versus `1h`
  - best tested `4h` result was `period=30, band_width=2.0`
  - result: `-2.01%`, Sharpe `0.11`, win rate `71.21%`
  - conclusion: still not good enough, but much closer to viability than the `1h` branch

## Experiment History

### Experiment

- date: `2026-04-01`
- variant: `bollinger_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: Bollinger mean reversion may create a high-win-rate branch on BTC `1h`
- config: `configs/btcusdt_spot_1h.high_winrate_search.json`
- result file: `results/btcusdt_spot_1h_high_winrate_search_5000.json`
- conclusion: Bollinger produced `59-62%` win rate in several variants, but all tested combinations lost heavily after costs

### Experiment

- date: `2026-04-01`
- variant: broad Bollinger family matrix
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: Bollinger mean reversion may survive better on direct `4h` than on `1h`
- config:
  - `configs/btcusdt_spot_1h.family_matrix.json`
  - `configs/btcusdt_spot_4h.family_matrix.json`
- result file:
  - `results/btcusdt_spot_1h_family_matrix_5000.json`
  - `results/btcusdt_spot_4h_family_matrix_5000.json`
- conclusion: `4h` Bollinger was much better than `1h`, but still not attractive enough to prioritize

## Rejected Or De-Prioritized Ideas

- idea: prioritize Bollinger as a production candidate
- why it was rejected: high win rate did not translate into profitability
- evidence:
  - `results/btcusdt_spot_1h_high_winrate_search_5000.json`

## Next Experiments

- next: none unless there is a deliberate reason to revisit Bollinger with a different exit model or additional filters
- reason: current evidence does not justify more time on this branch
