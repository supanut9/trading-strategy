---
name: config-author
description: Use when creating or refining experiment config JSON files in this repository, including parameter grids, ranking metrics, and risk-management sweeps under configs/. Do not use for running backtests or editing strategy code.
---

# Config Author

Use this skill when the task is to create or adjust experiment definitions under `configs/`.

## Scope

- New config files under `configs/`
- Refining parameter grids for an existing strategy family
- Updating ranking metrics or risk-management sweeps
- Making config names consistent with existing repository patterns

## Workflow

1. Find the closest existing config for the same family, symbol, market, and timeframe.
2. Keep naming aligned with the repo pattern, for example `btcusdt_spot_1h.rsi_focus_refine.json`.
3. Keep the config explicit about:
   experiment metadata
   strategies and parameter grids
   ranking metric
   transaction-cost assumptions
   optional ATR execution parameters
4. Prefer narrow, interpretable sweeps over wide brute-force grids unless the user asks otherwise.
5. When creating a follow-up config, state the hypothesis in the `experiment` label or surrounding docs.

## Checks

- Re-open the JSON after editing to confirm valid syntax.
- Make sure every referenced strategy name exists in `src/trading_strategy/strategies/registry.py`.
- Keep the config easy to compare with nearby experiments.
