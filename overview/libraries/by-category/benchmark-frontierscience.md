# Libraries: `benchmark-frontierscience`

1 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>Phase 2 A/B/C Smoke Harness (v1)</strong>
(<code>phase2_smoke_harness_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `phase2_smoke_harness_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0012_phase2_abc_smoke_frontierscience/code/charts.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/constants.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/harness.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/paths.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/run_smoke.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/stats.py`, `tasks/t0012_phase2_abc_smoke_frontierscience/code/tools.py` |
| **Dependencies** | matplotlib, numpy |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Documentation** | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/library/phase2_smoke_harness_v1/description.md) |

**Entry points:**

* `main` (script) — CLI entry point. Loads the v2 dataset, runs A/B/C with paired execution,
  persists predictions JSONL per condition, computes metrics in explicit-variant format, runs
  paired McNemar tests, computes confirmatory N, renders charts, and writes intermediate
  stats.
* `run_condition_a` (function) — Drive scope_aware_react_v1 over the v2 hierarchy of one row
  in phase order; return final answer plus trajectory.
* `run_condition_b` (function) — Drive scope_unaware_planandsolve_v1 over one row; return
  final answer plus trajectory.
* `run_condition_c` (function) — Drive matched_mismatch_v1 (random strategy) wrapping
  scope_unaware_planandsolve_v1 over one row; return final answer plus trajectory carrying
  wrong granularity tags.
* `compute_metrics` (function) — Compute task_success_rate, overconfident_error_rate, and
  avg_decisions_per_task from a list of RowOutcome records.
* `judge_correctness` (function) — Compare a candidate final answer against gold actions using
  the local Claude Code CLI judge (haiku) with retry and short-circuit normalisation.
* `load_smoke_rows` (function) — Load and filter the v2 dataset to FrontierScience-Olympiad
  hierarchy-complete rows.
* `make_model_call` (function) — Return a closure that invokes the local Claude Code CLI with
  --tools '' and --setting-sources '' to suppress the default system prompt and tool
  catalogue, dropping per-call cost from ~$0.10 to ~$0.005 with cache reuse.
* `CostTracker` (class) — Process-wide cumulative-spend tracker with budget enforcement;
  thread-safe, supports per-model breakdown.
* `mcnemar_paired` (function) — Paired McNemar test on binary correctness vectors with exact
  binomial fallback when discordant pairs are sparse.
* `wilson_interval` (function) — Wilson 95% confidence interval for a binomial proportion.
* `confirmatory_n_for_paired_difference` (function) — Estimate the N required to detect a
  target paired effect at alpha=0.05 / power=0.8 given an observed discordant rate.
* `build_react_tool_registry` (function) — Build the minimal calculator + finish tool registry
  used by condition A.
* `build_planandsolve_tool_registry` (function) — Build the minimal calculator + finish tool
  registry used by conditions B and C.

Experiment harness that runs scope-aware (A), scope-unaware (B), and scope-mismatched (C)
agents on FrontierScience-Olympiad rows of hierarchical-annotation-v2, paired by task_id, with
budget enforcement, per-row checkpointing, and pre-registered RQ1/RQ2/RQ5 hypothesis tests.

</details>
