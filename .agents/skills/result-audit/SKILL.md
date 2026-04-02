---
name: result-audit
description: Use when investigating suspicious or hard-to-trust backtest outputs in this repository, such as sharp metric jumps, very low trade counts, zero-trade runs, or mismatches between expected and observed behavior. Do not use for normal experiment ranking.
---

# Result Audit

Use this skill when experiment outputs look wrong, fragile, or misleading.

## Scope

- Unexpected metric jumps between similar configs
- Zero-trade or near-zero-trade outcomes
- Very high return with unconvincing sample size
- Suspected config, registry, or backtest-assumption mismatches

## Workflow

1. Identify the suspicious result file, config, and strategy branch.
2. Check whether the ranking metric hid an obvious weakness such as drawdown or trade count.
3. Compare against nearby runs with similar parameters.
4. Inspect whether the strategy name, parameter grid, or execution settings explain the anomaly.
5. Report whether the issue is:
   expected but weak evidence
   a documentation mismatch
   a config mistake
   a likely code bug worth deeper review

## Audit priorities

- Low trade counts are a reliability warning.
- Zero-trade runs should be explained, not ignored.
- Large performance jumps from tiny parameter changes deserve extra scrutiny.
- Never describe a suspicious result as a new leader without stating the caveats.
