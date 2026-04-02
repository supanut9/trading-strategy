---
name: experiment-review
description: Use when comparing backtest result files in this repository, reviewing whether a new config improved or regressed performance, or ranking candidates across result JSON outputs. Do not use for creating strategy code or editing docs only.
---

# Experiment Review

Use this skill to evaluate experiment outputs in `results/` and decide what changed materially.

## Scope

- Compare one or more result JSON files under `results/`
- Review the top-ranked strategy from a new run
- Check whether a candidate is more robust or only better on one metric
- Summarize likely winners, regressions, and weak evidence

## Workflow

1. Identify the relevant result files and related config files.
2. Read the ranking metric and top entries from each JSON payload.
3. Compare at minimum:
   total return
   max drawdown
   Sharpe-like score
   trade count
   win rate
4. Call out when an apparent improvement is not convincing because trades are too few, drawdown increased too much, or gains are too narrow.
5. Tie conclusions back to the repo’s experiment rules in `docs/experiment-plan.md`.

## Review heuristics

- Prefer candidates that stay competitive across return, drawdown, and trade count.
- Do not promote a result that wins only on total return while risk worsens materially.
- Treat very low trade counts as weak evidence.
- Mention whether the result beats the current leader recorded in `docs/strategy-memory.md`.

## Output expectations

- Name the winning candidate clearly.
- State whether the change is a meaningful improvement, neutral iteration, or regression.
- Recommend the next step: refine, validate on another window, document, or stop exploring that branch.
