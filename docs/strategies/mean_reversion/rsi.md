# RSI Strategy Family

## Summary

- family: `RSI`
- category: `mean_reversion`
- status: current leading branch
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
- indicators used:
  - `RSI`
  - `EMA` in rejected mixed-filter tests

## Core Hypothesis

On `BTC 1h`, selective RSI mean reversion may capture profitable pullbacks with a higher hit rate than trend-following systems.

## Indicators

- primary indicators:
  - `RSI`
- optional filters tested:
  - long EMA regime filter
- entry logic variants:
  - plain oversold entry
  - confirmation entry after RSI recovers above oversold
- exit logic variants:
  - immediate overbought exit
  - cross-down from overbought exit
- indicator roles:
  - entry trigger: `RSI oversold or RSI oversold recovery`
  - regime filter: `none in the leading variant`
  - exit trigger: `RSI overbought or RSI cross-down from overbought`
  - risk control: `currently implicit through entry and exit selectivity`

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

### Variant: `plain_rsi_mean_reversion`

- logic: enter when RSI is at or below oversold, exit when RSI is at or above overbought
- status: primary branch
- notes: currently strongest by both return and win rate

### Variant: `rsi_confirmation_entry`

- logic: enter only when RSI was oversold and then recovers back above oversold
- status: active secondary branch
- notes: lower risk profile, but weaker than plain RSI on current sample

### Variant: `rsi_crossdown_exit`

- logic: same entry as plain RSI, but exit only when RSI crosses back down below overbought
- status: active secondary branch
- notes: kept win rate, but reduced return

### Variant: `rsi_with_ema_filter`

- logic: plain RSI entries allowed only when price is above a long EMA
- status: rejected
- notes: produced zero trades in tested form

## Active Best Candidates

## Latest Chart

Top plotted `1h` RSI result:

![BTCUSDT spot 1h RSI focus refine top result](../../../results/btcusdt_spot_1h_rsi_focus_refine_5000.svg)

### Candidate: `rsi_best_sharpe`

- variant: `rsi_crossdown_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- parameters:
  - `period = 24`
  - `oversold = 19`
  - `overbought = 64`
- config: `configs/btcusdt_spot_1h.rsi_focus_refine.json`
- result file: `results/btcusdt_spot_1h_rsi_focus_refine_5000.json`
- total return: `+30.33%`
- max drawdown: `9.80%`
- Sharpe: `2.33`
- trades: `11`
- win rate: `63.64%`
- exposure: `14.68%`
- why it matters: best risk-adjusted RSI candidate found so far on the current `1h` sample

### Candidate: `rsi_best_winrate`

- variant: `plain_rsi_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- parameters:
  - `period = 24`
  - `oversold = 20`
  - `overbought = 62`
- config: `configs/btcusdt_spot_1h.rsi_focus_refine.json`
- result file: `results/btcusdt_spot_1h_rsi_focus_refine_5000.json`
- total return: `+18.55%`
- max drawdown: `6.75%`
- Sharpe: `1.65`
- trades: `13`
- win rate: `84.62%`
- exposure: `13.98%`
- why it matters: highest profitable win-rate candidate found so far with at least `10` trades on the current `1h` sample

### Candidate: `rsi_lower_drawdown_alternative`

- variant: `rsi_confirmation_entry`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- parameters:
  - `period = 22`
  - `oversold = 21`
  - `overbought = 63`
- config: `configs/btcusdt_spot_1h.rsi_confirmation.json`
- result file: `results/btcusdt_spot_1h_rsi_confirmation_5000.json`
- total return: `+15.76%`
- max drawdown: `8.94%`
- Sharpe: `1.30`
- trades: `19`
- win rate: `57.89%`
- exposure: `15.60%`
- why it matters: best lower-drawdown alternative within the RSI family

## Timeframe Findings

- `1h`:
  - current leading timeframe for the RSI family
  - focused refinement improved the branch materially beyond the earlier `period 22` pocket
  - best Sharpe result is now `rsi_mean_reversion_crossdown_exit 24 / 19 / 64`
  - highest profitable win-rate result with at least `10` trades is now `rsi_mean_reversion 24 / 20 / 62`
  - both leaders stayed profitable on separate early and recent 2500-candle windows
  - overlapping rolling-window validation was also clean
  - `24 / 19 / 64` won all `4` tested rolling windows
  - all `4` rolling windows stayed profitable, with Sharpe from `1.53` to `2.60`
  - ATR execution testing did not improve the top cross-down leader
  - the base `24 / 19 / 64` cross-down result stayed best at `+30.33%`, `2.33` Sharpe
  - only ATR take-profit helped the high-win-rate plain RSI branch, lifting `24 / 20 / 62` to `+23.97%` and `2.12` Sharpe with a `4 ATR` target
  - cooldown / re-entry suppression also did nothing around the top cross-down leader
  - cooldown settings from `1` to `8` bars produced the exact same metrics as the base result, which implies this branch does not re-enter too quickly on the current sample
- `4h`:
  - direct Binance `4h` candles support the RSI branch
  - the broader matrix slightly favored the cross-down exit variant over plain RSI
  - focused direct-`4h` refinement improved the family further, but the top-Sharpe result used only `5` trades
  - best top-Sharpe result: `rsi_mean_reversion_crossdown_exit 25 / 19 / 65`
  - result: `+52.54%`, max drawdown `12.45%`, Sharpe `1.63`, trades `5`, win rate `100.00%`
  - best meaningful `10+` trade result by Sharpe: `rsi_mean_reversion_crossdown_exit 21 / 18 / 64`
  - result: `+39.37%`, max drawdown `30.84%`, Sharpe `0.87`, trades `10`, win rate `80.00%`
  - conclusion: `4h` RSI remains interesting, but direct `4h` EMA is currently the cleaner branch on robustness and drawdown

## Experiment History

### Experiment

- date: `2026-04-02`
- variant: `rsi_crossdown_exit` and `plain_rsi_mean_reversion` with ATR execution rules
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: ATR belongs in execution, not entry, and may improve the leading `1h` RSI systems through stop-loss and take-profit handling
- config: `configs/btcusdt_spot_1h.rsi_atr_execution.json`
- result file: `results/btcusdt_spot_1h_rsi_atr_execution_5000.json`
- conclusion: ATR stops mostly hurt both RSI leaders, while a `4 ATR` take-profit improved the plain high-win-rate branch; the top Sharpe leader still remained the base `24 / 19 / 64` cross-down system with no ATR exit overlay

### Experiment

- date: `2026-04-02`
- variant: `rsi_crossdown_exit` vs `rsi_crossdown_cooldown`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: a short cooldown after exit may reduce clustered re-entries and improve the top `1h` RSI branch
- config: `configs/btcusdt_spot_1h.rsi_cooldown_refine.json`
- result file: `results/btcusdt_spot_1h_rsi_cooldown_refine_5000.json`
- conclusion: cooldown values from `1` to `8` bars produced the exact same result as the base `24 / 19 / 64` cross-down system, so re-entry suppression is not a meaningful lever for this branch on the current sample

### Experiment

- date: `2026-04-02`
- variant: `rsi_crossdown_exit` vs `plain_rsi_mean_reversion` on overlapping rolling windows
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file:
  - `data/rolling/btcusdt_spot_1h_window_1.csv`
  - `data/rolling/btcusdt_spot_1h_window_2.csv`
  - `data/rolling/btcusdt_spot_1h_window_3.csv`
  - `data/rolling/btcusdt_spot_1h_window_4.csv`
- test window:
  - `4` overlapping windows of `2000` candles with `1000`-candle step
- hypothesis: the leading `1h` RSI cross-down branch should continue to beat the high-win-rate plain RSI alternative across overlapping rolling windows, not only on the full 5000-candle sample
- config: `configs/btcusdt_spot_1h.rsi_window_validation.json`
- result file:
  - `results/rolling/btcusdt_spot_1h_rsi_window_1.json`
  - `results/rolling/btcusdt_spot_1h_rsi_window_2.json`
  - `results/rolling/btcusdt_spot_1h_rsi_window_3.json`
  - `results/rolling/btcusdt_spot_1h_rsi_window_4.json`
- conclusion: `rsi_mean_reversion_crossdown_exit 24 / 19 / 64` ranked first in all `4` rolling windows and stayed profitable in every one, which is a strong robustness signal even though the first two windows used only `2` trades each

### Experiment

- date: `2026-04-01`
- variant: `plain_rsi_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: a simple RSI oversold/overbought reversal may outperform EMA trend logic on BTC `1h`
- config: `configs/btcusdt_spot_1h.rsi_sweep.json`
- result file: `results/btcusdt_spot_1h_rsi_sweep_5000.json`
- conclusion: RSI beat the EMA branch on raw return and opened a profitable pocket near longer RSI periods

### Experiment

- date: `2026-04-01`
- variant: `plain_rsi_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: the initial profitable RSI pocket can be improved by local threshold refinement
- config: `configs/btcusdt_spot_1h.rsi_micro_refine.json`
- result file: `results/btcusdt_spot_1h_rsi_micro_refine_5000.json`
- conclusion: the branch improved materially, with the leading zone moving to `period 22`, `oversold 18-21`, `overbought 63-64`

### Experiment

- date: `2026-04-01`
- variant: `rsi_with_ema_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: filtering RSI trades by a long EMA may remove counter-trend entries
- config: `configs/btcusdt_spot_1h.rsi_ema_filter.json`
- result file: `results/btcusdt_spot_1h_rsi_ema_filter_5000.json`
- conclusion: long-EMA filters at `150` and `200` eliminated the branch entirely and produced zero trades

### Experiment

- date: `2026-04-01`
- variant: `rsi_confirmation_entry`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: waiting for RSI to recover above oversold may improve trade quality
- config: `configs/btcusdt_spot_1h.rsi_confirmation.json`
- result file: `results/btcusdt_spot_1h_rsi_confirmation_5000.json`
- conclusion: confirmation reduced drawdown on the aggressive profile, but did not beat plain RSI on return or Sharpe

### Experiment

- date: `2026-04-01`
- variant: `rsi_crossdown_exit`, `rsi_confirmation_entry`, `plain_rsi_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: exit and confirmation variants may produce a better high-win-rate strategy than plain RSI
- config: `configs/btcusdt_spot_1h.high_winrate_search.json`
- result file: `results/btcusdt_spot_1h_high_winrate_search_5000.json`
- conclusion: plain RSI still won when combining win rate and positive return; confirmation remained the best lower-risk alternative

### Experiment

- date: `2026-04-01`
- variant: `plain_rsi_mean_reversion`, `rsi_confirmation_entry`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: the strongest `1h` RSI candidates may retain or improve their edge on native exchange `4h` candles
- config: `configs/btcusdt_spot_4h.rsi_candidates_direct.json`
- result file: `results/btcusdt_spot_4h_rsi_candidates_direct_5000.json`
- conclusion: the aggressive plain RSI candidate `22 / 21 / 63` worked well on direct `4h` candles and reached `+26.63%` return with `76.92%` win rate

### Experiment

- date: `2026-04-01`
- variant: broad RSI family matrix
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: RSI entry and exit variants may produce different leaders on `1h` versus direct `4h`
- config:
  - `configs/btcusdt_spot_1h.family_matrix.json`
  - `configs/btcusdt_spot_4h.family_matrix.json`
- result file:
  - `results/btcusdt_spot_1h_family_matrix_5000.json`
  - `results/btcusdt_spot_4h_family_matrix_5000.json`
- conclusion: plain RSI remained best on `1h`, while `4h` favored the cross-down exit variant in the broader matrix

### Experiment

- date: `2026-04-01`
- variant: `plain_rsi_mean_reversion`, `rsi_crossdown_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: the strongest `1h` RSI pocket can likely be improved by pushing the period slightly longer and comparing plain exits against cross-down exits directly
- config: `configs/btcusdt_spot_1h.rsi_focus_refine.json`
- result file: `results/btcusdt_spot_1h_rsi_focus_refine_5000.json`
- conclusion: the best Sharpe leader moved to `rsi_mean_reversion_crossdown_exit 24 / 19 / 64`, while the highest profitable win-rate leader moved to `rsi_mean_reversion 24 / 20 / 62`

### Experiment

- date: `2026-04-01`
- variant: `rsi_crossdown_exit`, `plain_rsi_mean_reversion`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file:
  - `data/btcusdt_spot_1h_2500_early.csv`
  - `data/btcusdt_spot_1h_2500_recent.csv`
- test window:
  - early half: `2025-09-05 03:00 UTC` to `2026-01-17 06:00 UTC`
  - recent half: `2026-01-17 07:00 UTC` to `2026-04-01 10:00 UTC`
- hypothesis: the new `1h` RSI leaders should remain profitable on separate halves of the current sample rather than depending on one concentrated regime
- config: `configs/btcusdt_spot_1h.rsi_window_validation.json`
- result file:
  - `results/btcusdt_spot_1h_rsi_window_validation_early_2500.json`
  - `results/btcusdt_spot_1h_rsi_window_validation_recent_2500.json`
- conclusion: both leaders stayed profitable in both halves, and the cross-down exit leader remained the better Sharpe profile in each half

### Experiment

- date: `2026-04-01`
- variant: `plain_rsi_mean_reversion`, `rsi_crossdown_exit`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: the direct-`4h` RSI branch can likely be improved by testing slightly longer RSI periods and comparing plain exits against cross-down exits directly
- config: `configs/btcusdt_spot_4h.rsi_focus_refine.json`
- result file: `results/btcusdt_spot_4h_rsi_focus_refine_5000.json`
- conclusion: refinement improved the direct-`4h` RSI branch, but the highest-Sharpe results depended on very few trades; the more meaningful `10+` trade candidates still showed large drawdown

## Rejected Or De-Prioritized Ideas

- idea: simple long-EMA regime filter
- why it was rejected: removed all trades for the tested profitable RSI variants
- evidence:
  - `results/btcusdt_spot_1h_rsi_ema_filter_5000.json`

## Next Experiments

- next: add cooldown or re-entry suppression to the plain RSI branch
- reason: this is the cleanest remaining lever for improving win rate and trade quality without destroying the existing edge

- next: test exit refinements around the leading plain RSI candidates
- reason: the main edge already exists; exit tuning is more promising than adding another top-level filter
