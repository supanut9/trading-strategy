# EMA Strategy Family

## Summary

- family: `EMA`
- category: `trend`
- status: active, but no longer the leading branch
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
- indicators used:
  - `EMA`

## Core Hypothesis

EMA-based trend logic should react faster than SMA on `BTC 1h`, allowing earlier trend participation and better pullback entries.

## Indicators

- primary indicators:
  - `EMA`
- optional filters tested:
  - price above filter EMA
  - higher-level EMA trend filter
  - EMA slope filter
  - EMA spread filter
- exit logic components:
  - crossover exit
  - loss of fast EMA support
- indicator roles:
  - entry trigger: `EMA alignment or EMA crossover`
  - regime filter: `EMA filters when used`
  - exit trigger: `EMA crossover or loss of fast EMA support`
  - risk control: `not yet formalized inside this family`

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

### Variant: `ema_cross`

- logic: long when short EMA is above long EMA
- status: de-prioritized
- notes: simple crossover variants mostly lost money after costs

### Variant: `ema_triple_pullback_fast_exit`

- logic: require bullish triple-EMA stack, enter near middle EMA, exit on loss of fast EMA support
- status: best EMA-only branch
- notes: materially better than naive EMA crossovers

### Variant: `ema_triple_pullback_fast_exit_spread_filter`

- logic: same as fast-exit pullback branch, but requires minimum EMA separation
- status: de-prioritized
- notes: reduced trades too aggressively

### Variant: `ema_cross_trend_filter`

- logic: EMA crossover plus higher-level EMA trend filter
- status: de-prioritized
- notes: cleaner behavior, but not enough edge

### Variant: `ema_cross_price_slope_filter`

- logic: EMA crossover plus filter EMA slope and price above filter EMA
- status: de-prioritized
- notes: did not compete with the pullback branch

## Active Best Candidates

### Candidate: `ema_best_candidate`

- variant: `ema_triple_pullback_fast_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- parameters:
  - `fast_window = 12`
  - `middle_window = 20`
  - `slow_window = 43`
  - `pullback_pct = 0.00125`
- config: `configs/btcusdt_spot_1h.ema_best_candidate.json`
- result file: `results/btcusdt_spot_1h_ema_best_candidate_5000.json`
- total return: `+4.48%`
- max drawdown: `4.49%`
- Sharpe: `0.97`
- trades: `29`
- win rate: `34.48%`
- exposure: `4.82%`
- why it matters: best confirmed EMA-only result on the current sample

### Candidate: `ema_best_4h_candidate`

- variant: `ema_triple_pullback`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- parameters:
  - `fast_window = 10`
  - `middle_window = 22`
  - `slow_window = 55`
  - `pullback_pct = 0.0025`
- config: `configs/btcusdt_spot_4h.ema_refine.json`
- result file: `results/btcusdt_spot_4h_ema_refine_5000.json`
- total return: `+98.99%`
- max drawdown: `14.46%`
- Sharpe: `1.49`
- trades: `50`
- win rate: `36.00%`
- exposure: `25.45%`
- why it matters: strongest EMA result found so far on direct Binance `4h` candles after focused refinement

## Timeframe Findings

- `1h`:
  - best meaningful EMA branch remains the fast-exit pullback family
  - top meaningful EMA result in the matrix was still modest compared with RSI
  - best meaningful matrix result: `+3.19%`, Sharpe `0.98`, trades `11`
- `4h`:
  - EMA improved materially versus `1h`
  - direct `4h` data strongly favored the triple-pullback family
  - focused refinement improved the matrix winner further
  - best result: `ema_triple_pullback 10 / 22 / 55 @ 0.0025`
  - return: `+98.99%`, max drawdown `14.46%`, Sharpe `1.49`
  - early/recent window validation kept the refined leader ahead of the previous matrix winner in both halves
  - early 2500 candles: `+68.05%`, `1.87` Sharpe
  - recent 2500 candles: `+18.42%`, `1.00` Sharpe
  - overlapping rolling-window validation was also supportive
  - `10 / 22 / 55 @ 0.0025` ranked first in `3` of `4` rolling windows
  - the only exception was the oldest rolling window, where `10 / 21 / 55 @ 0.003` slightly led
  - ATR execution testing did not improve the refined leader
  - loose ATR stop-loss overlays stayed close, but still trailed the base result
  - ATR take-profit overlays degraded the branch materially by cutting the trend too early
  - trailing EMA exits also failed clearly
  - every tested trailing-window variant trailed the base system badly, confirming that this branch needs room to run rather than tighter EMA-based trailing exits

## Experiment History

### Experiment

- date: `2026-04-02`
- variant: `ema_triple_pullback` with ATR execution rules
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: ATR stop-loss or take-profit handling may further improve the validated direct-`4h` EMA pullback branch
- config: `configs/btcusdt_spot_4h.ema_atr_execution.json`
- result file: `results/btcusdt_spot_4h_ema_atr_execution_5000.json`
- conclusion: the base `10 / 22 / 55 @ 0.0025` system still ranked first; loose ATR stop-loss overlays came close but did not improve Sharpe or return, and ATR take-profit overlays hurt the trend branch significantly

### Experiment

- date: `2026-04-02`
- variant: `ema_triple_pullback` vs `ema_triple_pullback_trailing_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: a configurable trailing EMA exit may improve the validated direct-`4h` pullback branch without the heavier damage caused by ATR take-profit exits
- config: `configs/btcusdt_spot_4h.ema_trailing_refine.json`
- result file: `results/btcusdt_spot_4h_ema_trailing_refine_5000.json`
- conclusion: trailing EMA exits were clearly inferior; the base `10 / 22 / 55 @ 0.0025` result stayed dominant and the best trailing-window test only managed `+2.37%` with `0.14` Sharpe

### Experiment

- date: `2026-04-02`
- variant: `ema_triple_pullback 10 / 22 / 55 @ 0.0025` vs `ema_triple_pullback 10 / 21 / 55 @ 0.003` on overlapping rolling windows
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file:
  - `data/rolling/btcusdt_spot_4h_direct_window_1.csv`
  - `data/rolling/btcusdt_spot_4h_direct_window_2.csv`
  - `data/rolling/btcusdt_spot_4h_direct_window_3.csv`
  - `data/rolling/btcusdt_spot_4h_direct_window_4.csv`
- test window:
  - `4` overlapping windows of `2000` candles with `1000`-candle step
- hypothesis: the refined direct-`4h` leader should stay ahead of the previous nearby EMA variant on most rolling windows if the edge is robust
- config: `configs/btcusdt_spot_4h.ema_window_validation.json`
- result file:
  - `results/rolling/btcusdt_spot_4h_ema_window_1.json`
  - `results/rolling/btcusdt_spot_4h_ema_window_2.json`
  - `results/rolling/btcusdt_spot_4h_ema_window_3.json`
  - `results/rolling/btcusdt_spot_4h_ema_window_4.json`
- conclusion: `10 / 22 / 55 @ 0.0025` ranked first in `3` of `4` rolling windows and stayed profitable in all `4`; the older `10 / 21 / 55 @ 0.003` variant only won the oldest window, so the refined leader still looks like the better default candidate

### Experiment

- date: `2026-04-01`
- variant: `ema_cross`, `ema_price_trend`, `ema_triple_stack`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: basic EMA trend logic may be enough to build a profitable BTC `1h` branch
- config: `configs/btcusdt_spot_1h.ema.json`, `configs/btcusdt_spot_1h.ema_variations.json`, `configs/btcusdt_spot_1h.ema_popular.json`
- result file:
  - `results/btcusdt_spot_1h_ema_5000.json`
  - `results/btcusdt_spot_1h_ema_variations_5000.json`
  - `results/btcusdt_spot_1h_ema_popular_5000.json`
- conclusion: naive EMA variants and popular public EMA combinations were not profitable on this sample

### Experiment

- date: `2026-04-01`
- variant: `ema_triple_pullback_fast_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: tighter pullback entries and earlier exits may improve the EMA branch
- config: `configs/btcusdt_spot_1h.ema_next.json`, `configs/btcusdt_spot_1h.ema_best_candidate.json`
- result file:
  - `results/btcusdt_spot_1h_ema_next_5000.json`
  - `results/btcusdt_spot_1h_ema_best_candidate_5000.json`
- conclusion: this created the best EMA-only branch, but it still trailed the later RSI branch

### Experiment

- date: `2026-04-01`
- variant: `ema_triple_pullback_fast_exit_spread_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: minimum EMA separation may remove weak trend setups
- config: `configs/btcusdt_spot_1h.ema_spread_filter_micro.json`
- result file: `results/btcusdt_spot_1h_ema_spread_filter_micro_5000.json`
- conclusion: spread gating improved smoothness, but reduced trades too much and did not beat the baseline EMA candidate

### Experiment

- date: `2026-04-01`
- variant: `ema_triple_pullback_fast_exit` vs `sma_triple_pullback_fast_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: the edge may come from the pullback structure rather than EMA specifically
- config: `configs/btcusdt_spot_1h.ma_vs_ema.json`
- result file: `results/btcusdt_spot_1h_ma_vs_ema_5000.json`
- conclusion: SMA was clearly worse than EMA on the same structure

### Experiment

- date: `2026-04-01`
- variant: broad EMA family matrix
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: the broader EMA family may behave very differently on `1h` versus native `4h` candles
- config:
  - `configs/btcusdt_spot_1h.family_matrix.json`
  - `configs/btcusdt_spot_4h.family_matrix.json`
- result file:
  - `results/btcusdt_spot_1h_family_matrix_5000.json`
  - `results/btcusdt_spot_4h_family_matrix_5000.json`
- conclusion: EMA was mediocre on `1h` but strong on direct `4h`, especially in the triple-pullback family

### Experiment

- date: `2026-04-01`
- variant: `ema_triple_pullback`, `ema_triple_pullback_fast_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: the direct-`4h` EMA winner from the family matrix can likely be improved with a tighter pullback band and a slightly adjusted middle EMA
- config: `configs/btcusdt_spot_4h.ema_refine.json`
- result file: `results/btcusdt_spot_4h_ema_refine_5000.json`
- conclusion: refinement improved the leader from `10 / 21 / 55 @ 0.003` to `10 / 22 / 55 @ 0.0025`, lifting return to `+98.99%` and Sharpe to `1.49`

### Experiment

- date: `2026-04-01`
- variant: `ema_triple_pullback`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file:
  - `data/btcusdt_spot_4h_2500_direct_early.csv`
  - `data/btcusdt_spot_4h_2500_direct_recent.csv`
- test window:
  - early half: `2023-12-20 08:00 UTC` to `2025-02-08 20:00 UTC`
  - recent half: `2025-02-09 00:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: the refined direct-`4h` EMA leader should stay ahead of the previous matrix winner on separate market windows, not only on the full 5000-candle sample
- config: `configs/btcusdt_spot_4h.ema_window_validation.json`
- result file:
  - `results/btcusdt_spot_4h_ema_window_validation_early_2500.json`
  - `results/btcusdt_spot_4h_ema_window_validation_recent_2500.json`
- conclusion: the refined `10 / 22 / 55 @ 0.0025` candidate stayed ahead of the older `10 / 21 / 55 @ 0.003` candidate in both halves, which is a useful robustness signal

## Rejected Or De-Prioritized Ideas

- idea: simple EMA crossovers
- why it was rejected: repeated losses after costs and low win rate
- evidence:
  - `results/btcusdt_spot_1h_ema_5000.json`
  - `results/btcusdt_spot_1h_ema_popular_5000.json`

- idea: EMA spread filter as main lever
- why it was rejected: cut trades too aggressively and did not improve return
- evidence:
  - `results/btcusdt_spot_1h_ema_spread_filter_micro_5000.json`

## Next Experiments

- next: combine EMA with a different secondary signal only if needed for comparison or regime classification
- reason: the plain EMA family appears mature enough for now and is no longer the leading branch
