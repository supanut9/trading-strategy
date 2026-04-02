---
name: rolling-validation
description: Use when validating a candidate strategy across multiple rolling-window datasets or result files in this repository, especially under data/rolling/ and results/rolling/. Do not use for single-run experiment summaries.
---

# Rolling Validation

Use this skill to check whether a strategy stays credible across multiple windows instead of one favorable sample.

## Scope

- Run the same config across rolling datasets in `data/rolling/`
- Compare rolling result files in `results/rolling/`
- Summarize consistency, not just the best window

## Workflow

1. Identify the target strategy or config and the matching rolling datasets.
2. Keep output files grouped under `results/rolling/`.
3. Compare each window on:
   total return
   max drawdown
   Sharpe-like score
   trade count
   leader rank within the window
4. Call out whether the candidate wins broadly, degrades gracefully, or collapses outside one period.
5. Feed credible conclusions into `docs/strategy-memory.md` or the relevant family doc when requested.

## Validation rules

- One strong window is not enough.
- A candidate that stays near the top across windows is more useful than one that spikes once.
- Note any window where trade count becomes too small to trust.
