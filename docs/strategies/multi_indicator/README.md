# Multi-Indicator Strategies

Use this category when a strategy mixes indicators that have different jobs.

Examples:

- `RSI + EMA`
- `EMA + ATR`
- `Bollinger + RSI`
- `breakout + volume`

## When To Put A Strategy Here

Put a strategy in `multi_indicator/` when at least one of these is true:

- the strategy uses indicators from different logic families
- the strategy is easier to understand as a combined system than as a variant of one indicator family
- one indicator is clearly the entry trigger and another is clearly the regime or risk filter

Do not force everything here.

Use single-family docs when the strategy is still mostly one indicator family with small adjustments.

Examples:

- `RSI with confirmation entry` still belongs under `mean_reversion/rsi.md`
- `EMA with spread filter` still belongs under `trend/ema.md`
- `RSI entry + EMA regime filter` should usually live under `multi_indicator/`

## Required Documentation Fields

Every multi-indicator strategy file should explicitly list:

- indicators used
- entry trigger
- regime filter
- exit trigger
- risk control
- which part of the logic each indicator is responsible for

## Suggested Files

Create one file per combined family, for example:

- `docs/strategies/multi_indicator/rsi_ema.md`
- `docs/strategies/multi_indicator/ema_atr.md`
- `docs/strategies/multi_indicator/breakout_volume.md`
