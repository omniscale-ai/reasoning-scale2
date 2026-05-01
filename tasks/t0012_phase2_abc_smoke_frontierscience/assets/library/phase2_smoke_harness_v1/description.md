---
spec_version: "2"
library_id: "phase2_smoke_harness_v1"
documented_by_task: "t0012_phase2_abc_smoke_frontierscience"
date_documented: "2026-05-01"
---

# Phase 2 A/B/C Smoke Harness (v1)

## Metadata

* **Name**: Phase 2 A/B/C Smoke Harness
* **Version**: 0.1.0
* **Task**: `t0012_phase2_abc_smoke_frontierscience`
* **Dependencies**: matplotlib, numpy
* **Modules**: `code/run_smoke.py`, `code/harness.py`, `code/model_call.py`, `code/stats.py`,
  `code/charts.py`, `code/tools.py`, `code/constants.py`, `code/paths.py`

## Overview

This is the experiment harness for the project's first end-to-end Phase 2 result. It loads the
v2 hierarchical-annotation dataset (t0009), filters to FrontierScience-Olympiad rows with a
complete tree-shaped hierarchy, and runs three agent libraries — `scope_aware_react_v1` (A),
`scope_unaware_planandsolve_v1` (B), and `matched_mismatch_v1` (C) — against the same model on
the same rows, paired by `task_id`. Per-row trajectories are persisted to JSONL on every step
so a crash mid-run can resume from the last checkpoint. After the runs finish, the harness
computes the registered project metrics in the explicit-variant format, runs paired McNemar
tests, computes a confirmatory-N estimate, and renders two charts. All model calls go through
the local Claude Code CLI with `--tools ""` and `--setting-sources ""` to suppress the default
system prompt and tool catalogue, dropping per-call cost from ~$0.10 to ~$0.005 with cache
reuse — a 25× reduction the harness needs to fit the $20 budget cap.

## API Reference

### `run_smoke.main()` (script)

CLI entry point. Flags:

```
--limit N                Cap N rows to process.
--budget-cap-usd USD     Hard cap on cumulative spend (default: 18.0).
--skip-condition {a,b,c} Skip a single condition (debug only).
--resume                 Reuse existing _intermediate_*.json files when present.
```

### `harness.run_condition_a / run_condition_b / run_condition_c` (functions)

Each takes `row` (one v2 dataset row), `model_call` (a closure produced by
`make_model_call`), and a tool registry. Returns a tuple `(final_answer, trajectory)` where
`trajectory` is a list of trajectory records with the canonical
`TRAJECTORY_RECORD_FIELDS` schema from t0007.

### `harness.compute_metrics(outcomes: list[RowOutcome]) -> Metrics`

Aggregates row outcomes into the three registered project metrics.

### `harness.judge_correctness(*, task_id, problem, gold, candidate, judge_call) -> bool`

Compares a candidate final answer against the row's gold actions using the haiku judge with
short-circuit normalisation (whitespace, case, equivalent expressions). Returns `False` for
`None` candidates and content-policy refusals.

### `model_call.make_model_call(*, model, cost_tracker, note) -> Callable[[str], str]`

Returns a closure that invokes the local Claude Code CLI and records cost on every call. The
returned callable raises `RuntimeError` on persistent CLI failures after exponential backoff.

### `stats.mcnemar_paired(*, a_correct, b_correct) -> McNemarResult`

Paired McNemar test on binary correctness vectors. Falls back to an exact binomial when
discordant pairs are sparse (n_discordant < 10).

### `stats.confirmatory_n_for_paired_difference(*, discordant_rate_estimate, target_effect_pp) -> int`

Estimate of the N required to detect a target paired-difference effect at α=0.05, power=0.8
given an observed discordant rate.

## Usage Examples

```bash
# Full smoke run (default budget cap $18.0)
uv run python -u -m arf.scripts.utils.run_with_logs \
    --task-id t0012_phase2_abc_smoke_frontierscience -- \
    uv run python -u -m tasks.t0012_phase2_abc_smoke_frontierscience.code.run_smoke

# Quick 2-row validation
uv run python -u -m tasks.t0012_phase2_abc_smoke_frontierscience.code.run_smoke \
    --limit 2 --budget-cap-usd 5.0

# Resume after a crash
uv run python -u -m tasks.t0012_phase2_abc_smoke_frontierscience.code.run_smoke --resume
```

Programmatic use of `compute_metrics`:

```python
from tasks.t0012_phase2_abc_smoke_frontierscience.code.harness import (
    compute_metrics, jsonable_to_outcomes,
)
import json

outcomes = jsonable_to_outcomes(
    json.load(open("tasks/.../_intermediate_a.json"))
)
metrics = compute_metrics(outcomes=outcomes)
print(metrics.task_success_rate, metrics.overconfident_error_rate)
```

## Dependencies

* `matplotlib` — for the two result charts (`condition_metric_bar.png`,
  `per_row_success_heatmap.png`).
* `numpy` — used in `stats.py` for the McNemar exact-binomial fallback and Wilson interval.

## Testing

```bash
uv run pytest tasks/t0012_phase2_abc_smoke_frontierscience/code/test_harness.py
```

The test suite (14 tests) covers: outcome serialisation round-trip, metric computation
(including the 0-success edge case), gold-answer extraction, judge short-circuits on common
normalisation cases, McNemar exact-binomial fallback, Wilson interval, and confirmatory-N
calculation. All tests run deterministically with no live API calls.

## Main Ideas

* **Per-row checkpointing is mandatory** for any experiment harness with non-trivial wall-clock
  cost. The first two attempts to run this harness through a spawned `/execute-task` agent
  crashed mid-run; checkpointing meant the third attempt resumed without losing prior rows.
* **System-prompt override is the single biggest cost lever** when using the local Claude
  Code CLI — the default system prompt is ~50k tokens. With `--tools ""` and
  `--setting-sources ""` the harness fits 84 row-runs under $18 instead of ~$200.
* **Trajectory schema parity with t0006/t0007/t0010 is enforced by re-export**: the harness
  reads `TRAJECTORY_RECORD_FIELDS` from t0007 and asserts every emitted record matches. This
  caught two mismatches during early development.
* **The `final_confidence` gap in t0007/t0010** is exposed by the harness rather than papered
  over: B/C trajectories carry `null` confidence and Metric 2 collapses to zero for those
  conditions. The harness reports the metric honestly and surfaces the gap as a follow-up
  suggestion rather than synthesising a fake confidence score.

## Summary

The harness is the substrate for every Phase 2 A/B/C run on the project's hierarchical-
annotation data. It pairs three agent libraries against the same problem set and the same
model, computes the three registered project metrics in the explicit-variant format, runs
paired hypothesis tests, and produces an asset-compliant predictions JSONL per condition plus
two charts. Cost control is built into the run loop, and per-row checkpointing makes the
harness robust to mid-run crashes.

In the project, this library is consumed by the t0012 task itself and is the natural starting
point for any follow-up confirmatory run, multi-provider replication, or extension to
additional benchmarks (SWE-bench Verified, tau-bench). Its known limitations — the Metric 2
collapse for B/C, the `task_id` collision in the upstream pilot file, the lack of a pluggable
provider beyond the local Claude Code CLI — are documented in this task's results and queued
as follow-up suggestions.
