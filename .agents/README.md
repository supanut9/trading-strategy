# Repository Agents

This repository keeps Codex-specific workflow skills under `.agents/skills/`.

## Current Skills

- `backtest-runner`: run configs against CSV datasets and summarize top results
- `strategy-scaffold`: add or update strategy modules, registry entries, tests, and related docs
- `experiment-review`: compare result files and judge whether a new run is a real improvement
- `strategy-doc-sync`: update `docs/strategy-memory.md` and family research docs after experiments
- `config-author`: create or refine experiment config JSON files
- `rolling-validation`: validate candidates across rolling-window datasets and results
- `result-audit`: inspect suspicious outputs, anomalies, and weak evidence

## Layout

Each skill uses this structure:

```text
.agents/skills/<skill-name>/
├── SKILL.md
└── agents/openai.yaml
```

Use `SKILL.md` for workflow instructions and `agents/openai.yaml` for Codex UI metadata and optional dependencies.

## Adding A New Skill

1. Create a new folder under `.agents/skills/`.
2. Add a `SKILL.md` file with `name` and `description` in YAML frontmatter.
3. Add `agents/openai.yaml` when you want display metadata or tool dependencies.
4. Keep each skill focused on one repeatable repository workflow.

## Recommended Next Additions

- add scripts only when a workflow becomes repetitive enough that instructions are no longer reliable
- add MCP dependencies only when a skill truly needs external systems or official documentation

## Project Agent Roles

Project-scoped role config now lives under `.codex/`.

- `.codex/config.toml`: enables multi-agent support for this repo and registers role descriptions
- `.codex/agents/researcher.toml`: higher-reasoning role for strategy ideas and experiment planning
- `.codex/agents/executor.toml`: execution-oriented role for running backtests and collecting outputs
- `.codex/agents/reviewer.toml`: review-focused role for regressions, weak evidence, and stale docs

## MCP Guidance

Most workflows in this repo are local and deterministic, so skills should stay instruction-first.
Only declare MCP dependencies in `agents/openai.yaml` when a skill truly needs external systems or official docs.
