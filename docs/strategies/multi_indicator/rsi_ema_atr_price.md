# RSI + EMA + ATR + Price Structure Strategy Family

## Summary

- family: `RSI + EMA + ATR + price structure`
- category: `multi_indicator`
- status: rejected for now
- primary market: `BTCUSDT spot`
- tested timeframes:
  - `1h`
  - `4h`
- indicators used:
  - `RSI`
  - `EMA`
  - `ATR`
  - recent range structure

## Core Hypothesis

RSI can time pullback entries, EMA can keep the strategy aligned with regime, ATR can avoid dead or chaotic volatility conditions, and recent range structure can prevent longs when price is still sitting in the weak half of the local range.

## Indicators

- primary indicators:
  - `RSI`
  - `EMA`
  - `ATR`
  - recent high/low range midpoint
- optional filters:
  - none yet beyond the current combined logic
- exit logic components:
  - RSI cross-down from overbought
  - regime failure exit when price loses the EMA regime condition
- indicator roles:
  - entry trigger: `RSI oversold`
  - regime filter: `price above EMA and EMA rising`
  - exit trigger: `RSI cross-down or regime failure`
  - risk control: `ATR % gate and recent range midpoint filter`

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
  - filter timeframe: `same as execution`
  - exit timeframe: `same as execution`
  - execution timeframe: `1h` or `4h`

## Variants

### Variant: `rsi_ema_atr_price_structure`

- logic: long only when RSI is oversold, price is above a rising EMA, ATR percent is inside a target band, and price is in the upper half of the recent range
- status: first implemented variant
- indicators used:
  - `RSI` for entry and exit
  - `EMA` for regime
  - `ATR` for volatility
  - recent range midpoint for price structure
- notes: this is the first real “all of the above” combined system in the repo

### Variant: `rsi_ema_atr_volatility_filter`

- logic: long only when RSI is oversold, price is above a rising EMA, and ATR percent is inside a target band
- status: second implemented variant
- indicators used:
  - `RSI` for entry and exit
  - `EMA` for regime
  - `ATR` for volatility suppression only
- notes: this removed the range-midpoint structure gate to test whether ATR alone could work as the supporting filter

## Active Best Candidates

No confirmed leader yet.

Both implemented versions produced zero trades across the tested `1h` and `4h` grids, so there is no active candidate to promote.

## Experiment History

### Experiment

- date: `2026-04-02`
- variant: `rsi_ema_atr_price_structure`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: a combined system with clear indicator roles may outperform the weaker `RSI + EMA` mixed variants and produce a cleaner branch than raw pattern logic
- config:
  - `configs/btcusdt_spot_1h.rsi_ema_atr_price.json`
  - `configs/btcusdt_spot_4h.rsi_ema_atr_price.json`
- result file:
  - `results/btcusdt_spot_1h_rsi_ema_atr_price_5000.json`
  - `results/btcusdt_spot_4h_rsi_ema_atr_price_5000.json`
- conclusion: the first combined version was too restrictive and produced zero trades on both `1h` and direct `4h`

### Experiment

- date: `2026-04-02`
- variant: `rsi_ema_atr_volatility_filter`
- symbol: `BTCUSDT`
- market: `spot`
- timeframe: `1h` and `4h`
- dataset file:
  - `data/btcusdt_spot_1h_5000.csv`
  - `data/btcusdt_spot_4h_5000_direct.csv`
- test window:
  - `1h`: `2025-09-05 03:00 UTC` to `2026-04-01 10:00 UTC`
  - `4h`: `2023-12-20 08:00 UTC` to `2026-04-01 12:00 UTC`
- hypothesis: removing the price-structure gate and keeping only ATR as a softer supporting filter may restore trade frequency while preserving cleaner mixed-signal quality
- config:
  - `configs/btcusdt_spot_1h.rsi_ema_atr_vol.json`
  - `configs/btcusdt_spot_4h.rsi_ema_atr_vol.json`
- result file:
  - `results/btcusdt_spot_1h_rsi_ema_atr_vol_5000.json`
  - `results/btcusdt_spot_4h_rsi_ema_atr_vol_5000.json`
- conclusion: the softer ATR-only support design still produced zero trades on both `1h` and direct `4h`

## Rejected Or De-Prioritized Ideas

- idea: use the full `RSI + EMA + ATR + structure` stack as a hard entry gate in version one
- why it was rejected: even after loosening the structure filter, the combined conditions still removed the branch entirely on the tested grids
- evidence:
  - `results/btcusdt_spot_1h_rsi_ema_atr_price_5000.json`
  - `results/btcusdt_spot_4h_rsi_ema_atr_price_5000.json`
  - `results/btcusdt_spot_1h_rsi_ema_atr_vol_5000.json`
  - `results/btcusdt_spot_4h_rsi_ema_atr_vol_5000.json`

## Next Experiments

- next: stop gating entry with all three indicators at once
- reason: even the softer ATR-only support version still killed the branch completely

- next: if this family is revived later, use `ATR` for stop sizing or position sizing in the execution layer instead of as a pre-entry filter
- reason: `ATR` seems more suitable for risk handling than entry qualification in this repo's current long-only setup
