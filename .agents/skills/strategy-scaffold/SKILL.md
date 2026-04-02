---
name: strategy-scaffold
description: Use when adding or updating a trading strategy in this repository, including creating a new strategy module, wiring it into the registry, adding tests, and updating strategy documentation. Do not use for simple experiment execution only.
---

# Strategy Scaffold

Use this skill when the task is to add or evolve strategy code in `src/trading_strategy/strategies/`.

## Scope

- New strategy modules under the correct family directory
- Registry imports and `STRATEGY_REGISTRY` entries
- Family `__init__.py` updates only if needed by current repo patterns
- Tests in `tests/test_registry.py` or a focused `tests/test_<area>.py`
- Docs under `docs/strategies/` and memory updates when the strategy is part of ongoing research

## Workflow

1. Find the closest existing strategy in the same family and copy its structure, not its exact logic.
2. Name files in `snake_case`, for example `ema_cross_price_filter.py`.
3. Name classes in `PascalCase` and expose a stable `name` string matching the registry key.
4. Add the import and `StrategyDefinition` entry in `src/trading_strategy/strategies/registry.py`.
5. Add at least:
   one registry-oriented test proving the strategy can be built
   one behavior test covering entry, exit, or risk-management logic
6. Update strategy docs if the change introduces a new documented variant or materially changes research conclusions.

## Checks

- Use `python3 -m unittest discover -s tests` after edits.
- Use `python3 -m trading_strategy --list-strategies` to confirm the strategy is visible.

## Notes

- Keep logic deterministic and self-contained.
- Prefer concise inline candle fixtures in tests.
- Reuse existing indicator helpers from `src/trading_strategy/strategies/indicators.py` when possible.
- Do not add live trading, broker integration, or secrets.
