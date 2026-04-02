# Double Top / Bottom Pattern Family

## Summary

- family: `double_top_bottom`
- category: `pattern`
- status: active exploration
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
  - `4h`
- indicators used:
  - `swing highs`
  - `swing lows`
  - `neckline breakout`

## Core Hypothesis

Repeated price rejection around a similar low can identify a bullish double-bottom reversal, while repeated rejection around a similar high can identify a bearish double-top exit.

## Indicators

- primary indicators:
  - local pivot highs
  - local pivot lows
- optional filters:
  - none yet
- exit logic components:
  - bearish double-top neckline breakdown
- indicator roles:
  - entry trigger: `double-bottom neckline breakout`
  - regime filter: `none yet`
  - exit trigger: `double-top neckline breakdown`
  - risk control: `pattern spacing and tolerance constraints`

## Timeframe Context

- symbol: `BTCUSDT`
- market: `spot`
- tested timeframes:
  - `1h`
  - `4h`
- default execution timeframe: `1h`
- multi-timeframe: `no`
- timeframe roles:
  - entry timeframe: `same as execution`
  - filter timeframe: `none`
  - exit timeframe: `same as execution`
  - execution timeframe: `1h` or `4h`

## Variants

### Variant: `double_top_bottom_reversal`

- logic: enter on bullish double-bottom breakout and exit on bearish double-top breakdown
- status: first implemented variant
- indicators used:
  - pivot highs
  - pivot lows
  - neckline breakout
- notes: pattern detection is heuristic and sensitive to swing-point choices

## Charts

### `1h` Top Result

![BTCUSDT spot 1h double top bottom top result](../../../results/btcusdt_spot_1h_pattern_double_top_bottom_5000.svg)

### `1h` Zoomed Trade Example

This is a local zoom around one representative trade with the detector annotations drawn directly on the chart:
- `Bottom 1`
- `Bottom 2`
- `Neckline`
- `Breakout`

![BTCUSDT spot 1h double top bottom zoomed trade example](../../../results/btcusdt_spot_1h_pattern_double_top_bottom_zoom.svg)

### Direct `4h` Top Result

![BTCUSDT spot 4h double top bottom top result](../../../results/btcusdt_spot_4h_pattern_double_top_bottom_5000.svg)

### Direct `4h` Zoomed Trade Example

This zoom uses the same explicit detector annotations.

![BTCUSDT spot 4h double top bottom zoomed trade example](../../../results/btcusdt_spot_4h_pattern_double_top_bottom_zoom.svg)

## Active Best Candidates

### Candidate: `double_top_bottom_best_4h`

- variant: `double_top_bottom_reversal`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `4h`
- dataset file: `data/btcusdt_spot_4h_5000_direct.csv`
- test window: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- parameters:
  - `swing_window = 2`
  - `min_separation_bars = 4`
  - `max_separation_bars = 18`
  - `peak_tolerance_pct = 0.01`
  - `neckline_buffer_pct = 0.015`
  - `breakout_pct = 0.0`
  - `lookback_bars = 90`
- config: `configs/btcusdt_spot_4h.pattern_double_top_bottom.json`
- result file: `results/btcusdt_spot_4h_pattern_double_top_bottom_5000.json`
- total return: `+12.10%`
- max drawdown: `43.02%`
- Sharpe: `0.32`
- trades: `68`
- win rate: `35.29%`
- exposure: `46.05%`
- why it matters: best first-pass pattern result, but still materially weaker than the leading indicator branches

## Experiment History

### Experiment

- date: `2026-04-01`
- variant: `double_top_bottom_reversal`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: simple double-bottom entry and double-top exit logic may capture cleaner reversal structures than indicator-based triggers
- config:
  - `configs/btcusdt_spot_1h.pattern_double_top_bottom.json`
  - `configs/btcusdt_spot_4h.pattern_double_top_bottom.json`
- result file:
  - `results/btcusdt_spot_1h_pattern_double_top_bottom_5000.json`
  - `results/btcusdt_spot_4h_pattern_double_top_bottom_5000.json`
- conclusion: the first detector underperformed badly on `1h` and only reached a weak `+12.10%` with `43.02%` drawdown on direct `4h`, so this exact setup is not competitive yet

## Rejected Or De-Prioritized Ideas

- idea: start with head and shoulders immediately
- why it was rejected: too subjective for the first price-pattern detector

- idea: use the current raw double-top/bottom detector as a leading branch
- why it was rejected: first-pass results were weak versus RSI and EMA, especially on `1h`
- evidence:
  - `results/btcusdt_spot_1h_pattern_double_top_bottom_5000.json`
  - `results/btcusdt_spot_4h_pattern_double_top_bottom_5000.json`

## Next Experiments

- next: only revisit price patterns with additional filters such as trend or volatility context
- reason: the raw geometry detector alone is not strong enough to compete with validated RSI and EMA branches
