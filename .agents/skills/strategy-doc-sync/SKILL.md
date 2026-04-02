---
name: strategy-doc-sync
description: Use when updating this repository’s strategy research documents after experiments or strategy changes, including docs/strategy-memory.md, docs/strategies/, and related result references. Do not use for pure code changes with no research or documentation impact.
---

# Strategy Doc Sync

Use this skill to keep research documents aligned with the latest experiments.

## Scope

- Update `docs/strategy-memory.md`
- Update family files under `docs/strategies/`
- Add config and result file references
- Refresh leader summaries, validation notes, and next experiments when the evidence changed

## Workflow

1. Read the relevant family doc under `docs/strategies/` and `docs/strategy-memory.md`.
2. Read the matching config and result files before editing claims.
3. Update only the sections affected by the new evidence:
   active best candidates
   experiment history
   rejected or de-prioritized ideas
   current leaders
   key result files
4. Keep timeframe, dataset file, and test window explicit.
5. Preserve the repo’s existing research tone: short factual bullets, not narrative prose.

## Documentation rules

- Every experiment entry should point to both the config file and result file.
- If a branch is ruled out, say so directly to avoid repeating dead-end work later.
- If the leader changes, update both the family doc and `docs/strategy-memory.md`.
- Do not claim robustness unless there is validation evidence.

## Output expectations

- Summarize what changed in the docs.
- Mention which files were updated.
- Flag any missing evidence that prevented a full documentation update.
