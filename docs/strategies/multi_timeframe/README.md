# Multi-Timeframe Strategies

Use this category when one strategy uses more than one timeframe inside the same logic.

Examples:

- `4h trend filter + 1h entry`
- `1d regime + 4h setup + 1h execution`
- `15m entry + 1h exit`

## When To Put A Strategy Here

Put a strategy in `multi_timeframe/` when at least one of these is true:

- one timeframe is used for entry and another timeframe is used for filtering
- one timeframe is used for execution and another is used for exit confirmation
- the strategy logic cannot be described honestly as a single-timeframe system

Do not use this category just because the same strategy was tested on many timeframes.

Examples:

- `RSI tested on 15m, 1h, and 4h` is still one family file with multiple tested contexts
- `4h EMA trend filter + 1h RSI entry` is a true `multi_timeframe` strategy

## Required Documentation Fields

Every multi-timeframe strategy file should explicitly list:

- entry timeframe
- filter timeframe
- exit timeframe
- execution timeframe
- indicators used on each timeframe
- how data from the higher timeframe is aligned to the lower timeframe

## Suggested Files

Create one file per multi-timeframe family, for example:

- `docs/strategies/multi_timeframe/rsi_4h_1h.md`
- `docs/strategies/multi_timeframe/ema_regime_rsi_entry.md`
- `docs/strategies/multi_timeframe/breakout_1d_4h.md`
