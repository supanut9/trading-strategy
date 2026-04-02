# Strategy Catalog

This catalog stores strategy research in a structured way.

Use this when a strategy can have:

- one indicator
- multiple indicators
- many variants of entry, exit, or filters
- one timeframe
- many tested timeframes
- multiple timeframes inside one strategy

The goal is to keep each strategy family readable over time instead of mixing all experiments into one long log.

## How To Classify A Strategy

Use the strategy logic first, not just the indicator name.

- `trend`: follows strength or continuation
- `mean_reversion`: buys weakness or fades extension back toward normal
- `breakout`: trades expansion outside a prior range
- `multi_indicator`: mixes indicators that come from different logic families or assigns clearly different jobs to different indicators
- `multi_timeframe`: uses more than one timeframe inside the same strategy logic

Examples:

- `EMA crossover` -> `trend`
- `RSI oversold bounce` -> `mean_reversion`
- `Donchian breakout` -> `breakout`
- `RSI pullback with EMA regime filter` -> `multi_indicator`
- `4h trend filter with 1h entry` -> `multi_timeframe`

## Indicator Roles

When multiple indicators are used, document each indicator by role:

- `entry trigger`: what causes the trade to open
- `regime filter`: what market condition must be true first
- `exit trigger`: what causes the trade to close
- `risk control`: stop, volatility gate, sizing rule, cooldown, or trade suppression

This matters because the same indicator can be used in different ways.

Examples:

- `RSI` can be a mean-reversion entry trigger or a trend-strength filter
- `EMA` can be a trend signal, a mean-reversion anchor, or a regime filter
- `Bollinger` can be a mean-reversion entry or a breakout confirmation

## Timeframe Rules

Treat timeframe as part of the tested context, not a minor note.

This means:

- `RSI 22 / 21 / 63 on 1h` and `RSI 22 / 21 / 63 on 4h` should be recorded as different tested contexts
- a strategy tested on many timeframes should keep those results in the same family file, but each candidate and experiment entry must record the timeframe explicitly
- a strategy that uses more than one timeframe in the same logic should go under `multi_timeframe/`

Examples:

- same strategy, different tested contexts:
  - `RSI mean reversion on 15m`
  - `RSI mean reversion on 1h`
  - `RSI mean reversion on 4h`
- true multi-timeframe strategy:
  - `4h EMA regime filter + 1h RSI entry`

## Timeframe Roles

When more than one timeframe is involved, record the role of each timeframe:

- `entry timeframe`
- `filter timeframe`
- `exit timeframe`
- `execution timeframe`

## Structure

Each strategy family should get its own document under a category folder:

- `docs/strategies/trend/`
- `docs/strategies/mean_reversion/`
- `docs/strategies/breakout/`
- `docs/strategies/pattern/`
- `docs/strategies/multi_indicator/`
- `docs/strategies/multi_timeframe/`

Recommended rule:

- one family per file
- multiple variants inside the file
- every experiment entry linked to a config and result file

## Current Catalog

- trend
  - `docs/strategies/trend/ema.md`
- mean reversion
  - `docs/strategies/mean_reversion/rsi.md`
  - `docs/strategies/mean_reversion/bollinger.md`
- pattern
  - `docs/strategies/pattern/double_top_bottom.md`
- multi indicator
  - `docs/strategies/multi_indicator/README.md`
  - `docs/strategies/multi_indicator/rsi_ema.md`
  - `docs/strategies/multi_indicator/rsi_ema_atr_price.md`
- multi timeframe
  - `docs/strategies/multi_timeframe/README.md`

## Standard Sections Per Strategy File

Each strategy file should contain:

1. strategy family summary
2. core hypothesis
3. indicator building blocks
4. variant list
5. active best candidates
6. experiment history
7. rejected or de-prioritized ideas
8. next experiments

## Variant Naming Guidance

Use explicit names that describe the logic, not just the parameters.

Examples:

- `plain_rsi_mean_reversion`
- `rsi_confirmation_entry`
- `rsi_crossdown_exit`
- `ema_triple_pullback_fast_exit`
- `ema_spread_filter`
- `ema_with_rsi_filter`

## Experiment Entry Rule

Every experiment entry should include:

- date
- variant name
- symbol
- market
- timeframe
- dataset file
- test window
- hypothesis
- config file
- result file
- key parameters
- return
- drawdown
- Sharpe
- trade count
- win rate
- conclusion

Use `docs/strategies/_template.md` as the base when adding a new family.
