# Strategy Memory

This file is now the top-level index for strategy tracking.

Use the catalog under `docs/strategies/` to store each strategy family, its variants, and the experiments run for each variant.

## Active Dataset

- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h`
- dataset file: `data/btcusdt_spot_1h_5000.csv`
- candle count: `5000`
- current test window: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`

## Fixed Backtest Assumptions

- initial cash: usually `1000 USD`
- commission: `10 bps`
- slippage: `5 bps`
- execution model: next-bar open
- position model: long-only, one position at a time
- sizing: full capital, fractional position sizing allowed

## Strategy Catalog

- catalog index: `docs/strategies/README.md`
- template for new strategy docs: `docs/strategies/_template.md`
- trend family:
  - `docs/strategies/trend/ema.md`
- breakout family:
  - `docs/strategies/breakout/squeeze_breakout.md`
- mean reversion family:
  - `docs/strategies/mean_reversion/rsi.md`
  - `docs/strategies/mean_reversion/bollinger.md`
- pattern family:
  - `docs/strategies/pattern/double_top_bottom.md`
- multi-indicator family:
  - `docs/strategies/multi_indicator/README.md`
  - `docs/strategies/multi_indicator/rsi_ema.md`
  - `docs/strategies/multi_indicator/rsi_ema_atr_price.md`
- multi-timeframe family:
  - `docs/strategies/multi_timeframe/README.md`
  - `docs/strategies/multi_timeframe/ema_regime_rsi_entry.md`

## Current Leaders

- best Sharpe on current `1h` sample:
  - `rsi_mean_reversion_crossdown_exit 24 / 19 / 64`
  - total return: `+30.33%`
  - max drawdown: `9.80%`
  - Sharpe: `2.33`
  - trades: `11`
  - win rate: `63.64%`
  - see: `docs/strategies/mean_reversion/rsi.md`
- best high-win-rate profitable `1h` candidate:
  - `rsi_mean_reversion 24 / 20 / 62`
  - total return: `+18.55%`
  - max drawdown: `6.75%`
  - Sharpe: `1.65`
  - trades: `13`
  - win rate: `84.62%`
  - see: `docs/strategies/mean_reversion/rsi.md`
- best EMA candidate on direct `4h` sample:
  - `ema_triple_pullback 10 / 22 / 55 @ 0.0025`
  - total return: `+98.99%`
  - max drawdown: `14.46%`
  - Sharpe: `1.49`
  - trades: `50`
  - win rate: `36.00%`
  - see: `docs/strategies/trend/ema.md`
- best lower-timeframe exploratory candidate outside `1h`:
  - `rsi_mean_reversion_confirmation 21 / 20 / 64` on `15m`
  - total return: `+8.16%`
  - max drawdown: `2.06%`
  - Sharpe: `3.90`
  - trades: `12`
  - win rate: `66.67%`
  - see: `docs/strategies/mean_reversion/rsi.md`
  - status: recent-slice only; this branch did not hold on the later `15000`-candle extension

## Latest Chart

Current top plotted result:

![BTCUSDT spot 1h RSI top result](../results/btcusdt_spot_1h_rsi_focus_refine_5000.svg)

## Validation Notes

- `1h RSI` leaders held up on both early and recent 2500-candle windows:
  - cross-down leader stayed profitable in both halves with Sharpe above `2.30`
  - high-win-rate plain RSI leader also stayed profitable in both halves
- direct `4h EMA` leader held up on both early and recent 2500-candle windows:
  - refined `10 / 22 / 55 @ 0.0025` stayed ahead of the previous matrix winner in both halves
  - recent-half result was still positive at `+18.42%` with `1.00` Sharpe
- ATR execution sweeps on the validated leaders did not create a new winner:
  - `1h` RSI best Sharpe stayed the base `24 / 19 / 64` cross-down system with no ATR overlay
  - direct `4h` EMA best Sharpe stayed the base `10 / 22 / 55 @ 0.0025` pullback system with no ATR overlay
  - the only useful secondary result was `1h` plain RSI `24 / 20 / 62` improving to `+23.97%` with a `4 ATR` take-profit
- the next two local refinements were also negative:
  - `1h` RSI cooldown settings from `1` to `8` bars had no effect at all on the top cross-down leader
  - direct `4h` EMA trailing exits were much worse than the base pullback system
- overlapping rolling-window validation was supportive:
  - `1h` RSI `24 / 19 / 64` ranked first in all `4` rolling windows
  - direct `4h` EMA `10 / 22 / 55 @ 0.0025` ranked first in `3` of `4` rolling windows
  - the only `4h` exception was the oldest window, where `10 / 21 / 55 @ 0.003` slightly led
- direct `4h RSI` refinement improved the family, but the top-Sharpe result used only `5` trades:
  - meaningful `10+` trade `4h` RSI candidates still carried roughly `30%` drawdown
  - direct `4h EMA` remains the cleaner leading branch on that timeframe
- first-pass raw price-pattern detection is not competitive yet:
  - `1h` double-top/bottom was clearly negative
  - direct `4h` double-top/bottom was only weakly positive and carried `43.02%` max drawdown
- the first fully combined `RSI + EMA + ATR + structure` branch was too restrictive:
  - it produced zero trades on both the tested `1h` and direct `4h` grids
- the softer `RSI + EMA + ATR volatility` follow-up also failed:
  - it still produced zero trades on both the tested `1h` and direct `4h` grids
- refined `4h` squeeze breakout with a light EMA trend filter improved the family:
  - focused refinement improved it further to `+87.63%` with `15.73%` drawdown and `1.75` Sharpe
  - the trend gate and tighter local search now make this a serious secondary `4h` branch
  - the breakout leader then ranked first by Sharpe in all `4` direct-`4h` rolling windows against the top EMA pullback baselines
  - that makes it more robust than it first appeared on the single full-sample comparison
  - a `1.5 ATR` stop then produced the best-Sharpe breakout variant at `+81.39%`, `14.96%` drawdown, and `1.77` Sharpe
  - rolling validation for that ATR-stop version stayed positive in all `4` windows, averaging `+26.77%` return, `8.67%` drawdown, and `1.58` Sharpe
  - the trade-count caution still applies because each ATR-stop rolling window used only `5` to `8` trades
- new lower-timeframe sweep results were mixed:
  - `15m` RSI confirmation became a viable secondary branch after refinement
  - direct head-to-head still favored `15m` RSI confirmation `21 / 20 / 64` on Sharpe and drawdown over `24 / 20 / 65`
  - rolling validation for `15m` was supportive, but each window used only `3` to `6` trades, so confidence should stay moderate
  - the later `15000`-candle extension weakened the case materially:
  - all four tested `15m` candidates were negative on the full extended sample
  - only `3` of `6` larger rolling windows were profitable
  - current conclusion: keep `15m` as exploratory only, not as a validated branch
  - `5m` was effectively noise in the first pass
  - `30m` did not produce a profitable leader in the first pass

## Update Rules

Update the catalog when:

1. a new strategy family is introduced
2. a new variant is introduced
3. the best candidate changes
4. the dataset window changes
5. backtest cost assumptions change
6. a branch is ruled out and should not be retried blindly

## Key Result Files

- baseline EMA sweep: `results/btcusdt_spot_1h_ema_5000.json`
- EMA family sweep: `results/btcusdt_spot_1h_ema_variations_5000.json`
- popular EMA combos: `results/btcusdt_spot_1h_ema_popular_5000.json`
- EMA filtered variants: `results/btcusdt_spot_1h_ema_filtered_5000.json`
- EMA next refinements: `results/btcusdt_spot_1h_ema_next_5000.json`
- EMA best candidate: `results/btcusdt_spot_1h_ema_best_candidate_5000.json`
- EMA vs SMA comparison: `results/btcusdt_spot_1h_ma_vs_ema_5000.json`
- EMA spread filter micro check: `results/btcusdt_spot_1h_ema_spread_filter_micro_5000.json`
- RSI sweep: `results/btcusdt_spot_1h_rsi_sweep_5000.json`
- RSI micro refinement: `results/btcusdt_spot_1h_rsi_micro_refine_5000.json`
- RSI EMA filter check: `results/btcusdt_spot_1h_rsi_ema_filter_5000.json`
- RSI confirmation check: `results/btcusdt_spot_1h_rsi_confirmation_5000.json`
- high-win-rate search: `results/btcusdt_spot_1h_high_winrate_search_5000.json`
- focused `1h` RSI refinement: `results/btcusdt_spot_1h_rsi_focus_refine_5000.json`
- `1h` RSI window validation early half: `results/btcusdt_spot_1h_rsi_window_validation_early_2500.json`
- `1h` RSI window validation recent half: `results/btcusdt_spot_1h_rsi_window_validation_recent_2500.json`
- direct 4h RSI candidate check: `results/btcusdt_spot_4h_rsi_candidates_direct_5000.json`
- 1h family matrix: `results/btcusdt_spot_1h_family_matrix_5000.json`
- 4h family matrix: `results/btcusdt_spot_4h_family_matrix_5000.json`
- focused direct `4h` EMA refinement: `results/btcusdt_spot_4h_ema_refine_5000.json`
- direct `4h` EMA window validation early half: `results/btcusdt_spot_4h_ema_window_validation_early_2500.json`
- direct `4h` EMA window validation recent half: `results/btcusdt_spot_4h_ema_window_validation_recent_2500.json`
- focused direct `4h` RSI refinement: `results/btcusdt_spot_4h_rsi_focus_refine_5000.json`
- first-pass `1h` double top/bottom sweep: `results/btcusdt_spot_1h_pattern_double_top_bottom_5000.json`
- first-pass direct `4h` double top/bottom sweep: `results/btcusdt_spot_4h_pattern_double_top_bottom_5000.json`
- first-pass `1h` RSI + EMA + ATR + structure sweep: `results/btcusdt_spot_1h_rsi_ema_atr_price_5000.json`
- first-pass direct `4h` RSI + EMA + ATR + structure sweep: `results/btcusdt_spot_4h_rsi_ema_atr_price_5000.json`
- softer `1h` RSI + EMA + ATR volatility sweep: `results/btcusdt_spot_1h_rsi_ema_atr_vol_5000.json`
- softer direct `4h` RSI + EMA + ATR volatility sweep: `results/btcusdt_spot_4h_rsi_ema_atr_vol_5000.json`
- first-pass direct `4h` squeeze breakout sweep: `results/btcusdt_spot_4h_squeeze_breakout_5000.json`
- trend-filtered direct `4h` squeeze breakout sweep: `results/btcusdt_spot_4h_squeeze_breakout_trend_filter_5000.json`
- focused trend-filtered direct `4h` squeeze breakout sweep: `results/btcusdt_spot_4h_squeeze_breakout_trend_focus_5000.json`
- focused `15m` RSI confirmation refinement: `results/btcusdt_spot_15m_rsi_confirmation_refine_5000.json`
- focused `15m` RSI confirmation head-to-head: `results/btcusdt_spot_15m_rsi_confirmation_head_to_head_5000.json`
- extended `15m` RSI confidence check: `results/btcusdt_spot_15m_rsi_confidence_extension_15000.json`
- focused `1h` RSI next refinement: `results/btcusdt_spot_1h_rsi_refine_next_5000.json`
- rolling `15m` RSI window 1: `results/rolling/btcusdt_spot_15m_rsi_window_1.json`
- rolling `15m` RSI window 2: `results/rolling/btcusdt_spot_15m_rsi_window_2.json`
- rolling `15m` RSI window 3: `results/rolling/btcusdt_spot_15m_rsi_window_3.json`
- rolling `15m` RSI window 4: `results/rolling/btcusdt_spot_15m_rsi_window_4.json`
- rolling direct `4h` breakout window 1: `results/rolling/btcusdt_spot_4h_breakout_window_1.json`
- rolling direct `4h` breakout window 2: `results/rolling/btcusdt_spot_4h_breakout_window_2.json`
- rolling direct `4h` breakout window 3: `results/rolling/btcusdt_spot_4h_breakout_window_3.json`
- rolling direct `4h` breakout window 4: `results/rolling/btcusdt_spot_4h_breakout_window_4.json`
- focused direct `4h` breakout ATR execution sweep: `results/btcusdt_spot_4h_breakout_atr_execution_5000.json`
- rolling direct `4h` breakout ATR window 1: `results/rolling/btcusdt_spot_4h_breakout_atr_window_1.json`
- rolling direct `4h` breakout ATR window 2: `results/rolling/btcusdt_spot_4h_breakout_atr_window_2.json`
- rolling direct `4h` breakout ATR window 3: `results/rolling/btcusdt_spot_4h_breakout_atr_window_3.json`
- rolling direct `4h` breakout ATR window 4: `results/rolling/btcusdt_spot_4h_breakout_atr_window_4.json`
- focused `1h` RSI ATR execution sweep: `results/btcusdt_spot_1h_rsi_atr_execution_5000.json`
- focused direct `4h` EMA ATR execution sweep: `results/btcusdt_spot_4h_ema_atr_execution_5000.json`
- focused `1h` RSI cooldown refinement: `results/btcusdt_spot_1h_rsi_cooldown_refine_5000.json`
- focused direct `4h` EMA trailing refinement: `results/btcusdt_spot_4h_ema_trailing_refine_5000.json`
- rolling `1h` RSI window 1: `results/rolling/btcusdt_spot_1h_rsi_window_1.json`
- rolling `1h` RSI window 2: `results/rolling/btcusdt_spot_1h_rsi_window_2.json`
- rolling `1h` RSI window 3: `results/rolling/btcusdt_spot_1h_rsi_window_3.json`
- rolling `1h` RSI window 4: `results/rolling/btcusdt_spot_1h_rsi_window_4.json`
- rolling direct `4h` EMA window 1: `results/rolling/btcusdt_spot_4h_ema_window_1.json`
- rolling direct `4h` EMA window 2: `results/rolling/btcusdt_spot_4h_ema_window_2.json`
- rolling direct `4h` EMA window 3: `results/rolling/btcusdt_spot_4h_ema_window_3.json`
- rolling direct `4h` EMA window 4: `results/rolling/btcusdt_spot_4h_ema_window_4.json`
