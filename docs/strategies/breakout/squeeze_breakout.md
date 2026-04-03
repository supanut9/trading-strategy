# Squeeze Breakout Strategy Family

## Summary

- family: `bollinger_squeeze_breakout`
- category: `breakout`
- status: active exploration
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `4h` on direct Binance candles
- indicators used:
  - `Bollinger bandwidth`
  - `channel breakout`
  - `EMA trend filter`

## Core Hypothesis

When volatility compresses into a narrow Bollinger range, the next upside channel breakout may capture a stronger move than a plain breakout taken in any volatility state.

## Indicators

- primary indicators:
  - `Bollinger bandwidth`
  - `recent highest high`
  - `recent lowest low`
- optional filters:
  - `EMA trend filter`
- indicator roles:
  - entry trigger: `close above breakout channel after prior squeeze`
  - regime filter: `prior Bollinger bandwidth below threshold`
  - exit trigger: `close below short exit channel`
  - risk control: `squeeze threshold`, `exit lookback`, and optional `EMA trend filter`

## Variants

### Variant: `bollinger_squeeze_breakout`

- logic: require a low-volatility Bollinger squeeze on the prior window, then enter on an upside breakout above the recent channel high and exit on a break below a shorter channel low
- status: first implemented variant
- notes: this is a stricter breakout than plain Donchian because it only trades after compression

### Variant: `bollinger_squeeze_breakout_trend_filter`

- logic: same squeeze-plus-breakout trigger, but only when price is above a rising EMA trend filter
- status: tested, currently best variant in this family by Sharpe
- notes: the trend gate reduced trade count and exposure, but improved drawdown control and hit rate

## Active Best Candidates

### Candidate: `squeeze_breakout_trend_best_4h`

- variant: `bollinger_squeeze_breakout_trend_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- parameters:
  - `period = 30`
  - `band_width = 2.0`
  - `squeeze_threshold_pct = 3.5`
  - `breakout_lookback = 30`
  - `exit_lookback = 10`
  - `trend_ema_window = 200`
  - `trend_slope_window = 3`
- config: `configs/btcusdt_spot_4h.squeeze_breakout_trend_filter.json`
- result file: `results/btcusdt_spot_4h_squeeze_breakout_trend_focus_5000.json`
- total return: `+87.63%`
- max drawdown: `15.73%`
- Sharpe: `1.75`
- trades: `15`
- win rate: `60.00%`
- exposure: `12.32%`
- why it matters: the EMA gate made the branch materially cleaner on a risk-adjusted basis, even though it still trails the validated `4h` EMA pullback leader

### Candidate: `squeeze_breakout_trend_best_4h_atr_stop`

- variant: `bollinger_squeeze_breakout_trend_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- parameters:
  - `period = 30`
  - `band_width = 2.0`
  - `squeeze_threshold_pct = 3.5`
  - `breakout_lookback = 30`
  - `exit_lookback = 10`
  - `trend_ema_window = 200`
  - `trend_slope_window = 3`
- execution parameters:
  - `atr_period = 14`
  - `stop_loss_atr_multiple = 1.5`
- config: `configs/btcusdt_spot_4h.breakout_atr_execution.json`
- result file: `results/btcusdt_spot_4h_breakout_atr_execution_5000.json`
- total return: `+81.39%`
- max drawdown: `14.96%`
- Sharpe: `1.77`
- trades: `16`
- win rate: `50.00%`
- exposure: `9.94%`
- why it matters: this is now the best Sharpe version of the breakout branch, giving up some raw return to reduce drawdown slightly

## Experiment History

### Experiment

- date: `2026-04-02`
- variant: `bollinger_squeeze_breakout`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: adding a pre-breakout volatility compression filter can improve on plain breakout entries by suppressing noisy expansions that start from already-wide ranges
- config: `configs/btcusdt_spot_4h.squeeze_breakout.json`
- result file: `results/btcusdt_spot_4h_squeeze_breakout_5000.json`
- conclusion: the branch is worth keeping for further refinement because several settings were strongly profitable, but the best Sharpe only reached `0.48`, so it is still weaker than the leading direct `4h` EMA branch

### Experiment

- date: `2026-04-02`
- variant: `bollinger_squeeze_breakout_trend_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: a light EMA trend qualifier may preserve the best squeeze breakouts while filtering weaker counter-trend expansions
- config: `configs/btcusdt_spot_4h.squeeze_breakout_trend_filter.json`
- result file: `results/btcusdt_spot_4h_squeeze_breakout_trend_filter_5000.json`
- conclusion: the trend filter improved Sharpe from `0.48` to `0.56`, reduced max drawdown from `19.07%` to `17.38%`, and lifted win rate from `42.86%` to `58.82%`, so it is the better version of this family so far

### Experiment

- date: `2026-04-02`
- variant: `bollinger_squeeze_breakout_trend_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: a tighter local search around the `30 / 4.0 / 30 / 10` region can improve the risk-adjusted breakout leader further
- config: `configs/btcusdt_spot_4h.squeeze_breakout_trend_focus.json`
- result file: `results/btcusdt_spot_4h_squeeze_breakout_trend_focus_5000.json`
- conclusion: the tighter focus improved the family again, reaching `+87.63%` return with `15.73%` drawdown and `1.75` Sharpe at `30 / 2.0 / 3.5 / 30 / 10 / 200 / 3`

### Experiment

- date: `2026-04-02`
- variant: focused breakout leader vs nearby direct-`4h` EMA pullback leaders on overlapping rolling windows
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
- hypothesis: if the refined breakout leader is robust, it should stay competitive with or ahead of the strongest `4h` EMA pullback baselines across rolling windows, not only on the full sample
- config: `configs/btcusdt_spot_4h.breakout_vs_ema_window_validation.json`
- result file:
  - `results/rolling/btcusdt_spot_4h_breakout_window_1.json`
  - `results/rolling/btcusdt_spot_4h_breakout_window_2.json`
  - `results/rolling/btcusdt_spot_4h_breakout_window_3.json`
  - `results/rolling/btcusdt_spot_4h_breakout_window_4.json`
- conclusion: the focused breakout leader ranked first by Sharpe in all `4` rolling windows against both EMA pullback baselines, which is a strong robustness signal even though EMA sometimes had slightly higher raw return in individual windows

### Experiment

- date: `2026-04-02`
- variant: focused breakout leader with ATR execution overlay
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: a small ATR stop may improve the refined breakout leader by trimming drawdown without killing the core edge
- config: `configs/btcusdt_spot_4h.breakout_atr_execution.json`
- result file: `results/btcusdt_spot_4h_breakout_atr_execution_5000.json`
- conclusion: a `1.5 ATR` stop improved Sharpe slightly from `1.75` to `1.77` and reduced max drawdown from `15.73%` to `14.96%`, but raw return fell from `+87.63%` to `+81.39%`, so the branch now has separate best-return and best-Sharpe versions

### Experiment

- date: `2026-04-02`
- variant: ATR-stop breakout leader on overlapping rolling windows
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
- hypothesis: if the ATR-stop version is a real improvement, it should stay profitable and maintain its risk control outside the full-sample test
- config: `configs/btcusdt_spot_4h.breakout_atr_window_validation.json`
- result file:
  - `results/rolling/btcusdt_spot_4h_breakout_atr_window_1.json`
  - `results/rolling/btcusdt_spot_4h_breakout_atr_window_2.json`
  - `results/rolling/btcusdt_spot_4h_breakout_atr_window_3.json`
  - `results/rolling/btcusdt_spot_4h_breakout_atr_window_4.json`
- conclusion: the ATR-stop breakout stayed profitable in all `4` windows with average rolling metrics of `+26.77%` return, `8.67%` drawdown, and `1.58` Sharpe; it looks slightly cleaner than the no-ATR version on average, but the evidence is still limited by only `5` to `8` trades per window

## Rejected Or De-Prioritized Ideas

- idea: treat the squeeze breakout family as a new overall leader
- why it was rejected: even the better trend-filtered variant still trails the existing direct `4h` EMA leader by a wide margin on Sharpe

## Next Experiments

- next: run a direct research comparison between the validated `4h` EMA pullback leader and the two `4h` breakout leaders, then decide whether the breakout branch is best treated as the return-seeking alternative or the risk-controlled secondary branch
- reason: the family now has enough evidence internally; the remaining question is ranking against the mature EMA benchmark, not further local tuning
