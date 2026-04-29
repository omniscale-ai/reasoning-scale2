# Granularity-Aware Hierarchical Agents

## Goal

Investigate whether explicitly specifying an agent's current operating granularity — global
planning, subtask planning, or atomic execution — improves action quality, uncertainty calibration,
and final task success in hierarchical problem solving. The project measures the effect of scope
labelling on a composite multi-step benchmark and produces a paper-ready confirm/refute verdict on
the main hypothesis with effect sizes and stratified breakdowns.

## Research Questions

1. Does explicit granularity conditioning yield higher final task success than an otherwise
   identical scope-unaware agent on the composite benchmark?
2. Does explicit granularity conditioning reduce the overconfident error rate, i.e. the fraction of
   incorrect actions taken with high confidence?
3. On low-level tasks, does granularity conditioning improve accuracy in distinguishing "can execute
   now" from "must request information"?
4. Are gains concentrated in states where local execution requires information not needed for
   higher-level planning (sub-hypothesis 1)?
5. Do scope-mismatched agents perform strictly worse than both scope-aware and scope-unaware
   baselines (sub-hypothesis 2)?

## Success Criteria

* At least 100 tasks fully annotated with gold actions at each of the three granularity levels
  (Phase 1 deliverable).
* Statistically significant difference between scope-aware (A) and scope-unaware (B) on at least two
  of the three metrics at the chosen significance threshold (Phase 2 deliverable).
* Scope-mismatched (C) ranks worst on Metric 1 (task success) and Metric 2 (overconfident error
  rate) relative to A and B (Phase 3 deliverable).
* Clear confirm/refute verdict on the main hypothesis with reported effect sizes and a stratified
  breakdown by task family and difficulty (Phase 4 deliverable).

## Current Phase

Phase 1 (task decomposition and annotation) is in progress: the hierarchical annotation schema is
being finalised and the pilot annotation set is being expanded. Phase 2 (baseline scope-aware vs.
scope-unaware experiment) is queued and depends on completion of Phase 1.

## Results Dashboard

See [`overview/README.md`](overview/README.md) for aggregated results, metrics, and task status
across all completed tasks.

## Getting Started

```bash
git clone <this-repo-url>
cd reasoning-scale2
uv sync
uv run pre-commit install
python3 doctor.py
```

Do not re-run `/setup-project` unless you intend to re-initialise a fresh fork — it overwrites
`project/` and `meta/` content.

## Daily Workflow

* `/create-task` — scaffold a new task folder from a suggestion or idea.
* `/execute-task <task_id>` — drive a task through research → planning → implementation → analysis →
  reporting.
* `/human-brainstorm` — turn `suggestions.json` from completed tasks into the next task plan.
* Regenerate the dashboard with `uv run python -m arf.scripts.overview.materialize` and review
  `overview/README.md` after each task lands.

## Key Rules

* Every CLI call is wrapped in `uv run python -m arf.scripts.utils.run_with_logs <cmd>` so logs are
  captured.
* Tasks only modify files inside their own folder; the only top-level files a task may touch are
  `pyproject.toml`, `uv.lock`, `ruff.toml`, and `.gitignore`.
* Every task stage and every action is a separate, well-described commit.
* Completed task folders are immutable. Fix mistakes via correction files in a new task, never by
  editing past folders.
* Read through aggregators, never walk task folders directly. Raw globs miss the corrections
  overlay.
* Metrics must be registered in `meta/metrics/` before a task reports them; unregistered metrics
  fail verification.

## Project Structure

```text
arf/            Framework code: scripts, skills, specifications, styleguide, docs, tests
meta/           Project metadata: asset_types/, categories/, metrics/, task_types/
tasks/          One folder per research task (created by the create-task skill)
overview/       Materialized aggregator dashboard (regenerated, committed)
project/        Project-level files: description.md, budget.json, code/, data/
.claude/        Claude Code config (settings.json, rules/, skills/ symlinks)
.codex/         Codex CLI config (agents/, skills/ symlinks)
CLAUDE.md       Project overview loaded at Claude Code session start
pyproject.toml  Python deps and tooling config
doctor.py       Environment validation script
ruff.toml       Lint config
```

## Categories

* `agent-evaluation` — Agent Evaluation
* `benchmark-annotation` — Benchmark Annotation
* `benchmark-frontierscience` — FrontierScience-Olympiad
* `benchmark-swebench` — SWE-bench Verified
* `benchmark-taubench` — tau-bench
* `benchmark-workarena` — WorkArena++
* `granularity-conditioning` — Granularity Conditioning
* `hierarchical-planning` — Hierarchical Planning
* `uncertainty-calibration` — Uncertainty Calibration

## Metrics

* `task_success_rate` — Task Success Rate (`accuracy`, key)
* `overconfident_error_rate` — Overconfident Error Rate (`ratio`)
* `avg_decisions_per_task` — Average Decisions per Task (`count`)

## Task Types

Project-specific:

* `hierarchical-annotation` — Hierarchical Annotation

Generic (shipped with the template, reusable as-is):

* `answer-question`, `baseline-evaluation`, `brainstorming`, `build-model`, `code-reproduction`,
  `comparative-analysis`, `correction`, `data-analysis`, `deduplication`, `download-dataset`,
  `download-paper`, `experiment-run`, `feature-engineering`, `infrastructure-setup`,
  `internet-research`, `literature-survey`, `write-library`.

## Budget and Services

Total budget: **100.00 USD**. Available paid services: `anthropic_api`. Per-task default limit:
**10.00 USD**. (`openai_api` is declared in the project plan but disabled in `available_services`
until the API key is added; see `project/budget.json`.)

## Documentation

* [Autonomy and Safety](arf/docs/explanation/safety.md) — read first.
* [Tutorial](arf/docs/tutorial/) — five-page walkthrough from empty fork to first results.
* [Reference](arf/docs/reference/) — aggregators, glossary, specifications, skills.
* Style guides: [Python](arf/styleguide/python_styleguide.md),
  [Markdown](arf/styleguide/markdown_styleguide.md),
  [Agent Instructions](arf/styleguide/agent_instructions_styleguide.md).

## License

Released under the [Apache License 2.0](LICENSE).
