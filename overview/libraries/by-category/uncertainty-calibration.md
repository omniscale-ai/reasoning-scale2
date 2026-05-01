# Libraries: `uncertainty-calibration`

3 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>Metric 2 Calibration Aggregator</strong>
(<code>metric2_calibration_aggregator_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `metric2_calibration_aggregator_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0011_metric2_calibration_aggregator/code/calibration.py`, `tasks/t0011_metric2_calibration_aggregator/code/constants.py`, `tasks/t0011_metric2_calibration_aggregator/code/paths.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Documentation** | [`description.md`](../../../tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md) |

**Entry points:**

* `ConfidencePromptTemplate` (class) — Frozen dataclass wrapping the Xiong2024 §3.2
  human-inspired prompt with {problem} and {action} placeholders.
* `ConfidenceJudge` (class) — Self-consistency aggregator that majority-votes on predicted
  action labels and returns the mean confidence within the majority cohort, falling back to
  the highest-confidence sample on a 3-way tie.
* `compute_overconfident_error_rate` (function) — Returns the fraction of CalibrationRecord
  values that are incorrect with predicted_confidence >= HIGH_CONFIDENCE_THRESHOLD (default
  0.75); 0.0 for empty input.
* `elicit_confidence` (function) — Formats the confidence prompt, invokes a model_call, parses
  the verbalized label (low/medium/high), and returns (label, numeric_confidence).
* `CalibrationRecord` (class) — Frozen dataclass holding (problem_id, predicted_label,
  predicted_confidence, is_correct); the canonical input shape for
  compute_overconfident_error_rate.
* `calibration_record_from_trajectory` (function) — Adapter that converts a t0006/t0007/t0010
  trajectory record (canonical TRAJECTORY_RECORD_FIELDS schema) into a CalibrationRecord.

Verbalized-confidence + 3-sample self-consistency aggregator that computes
overconfident_error_rate per the Xiong2024 protocol.

</details>

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

<details>
<summary>📦 <strong>Scope-Unaware Plan-and-Solve v2 (with final_confidence)</strong>
(<code>scope_unaware_planandsolve_v2</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `scope_unaware_planandsolve_v2` |
| **Version** | 1 |
| **Modules** | `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py`, `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/constants.py`, `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/paths.py` |
| **Dependencies** | — |
| **Date created** | 2026-05-01 |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Created by** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Documentation** | [`description.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/description.md) |

**Entry points:**

* `PlanAndSolveAgentV2` (class) — Plan-and-Solve v2 agent. Composes the v1 agent and emits a
  verbalized final_confidence on every AgentResultV2 result.
* `AgentResultV2` (class) — Aggregate output: final_answer, trajectory, plan, final_confidence
  (0..1 or None), final_confidence_parse_failures (0/1/2).
* `TrajectoryRecordV2` (class) — Trajectory record with the canonical six v1 fields plus
  final_confidence (populated only on the finishing record).
* `elicit_final_confidence` (function) — Issue the Xiong2024 verbalized-confidence prompt once
  with one retry on parse failure; returns (value_in_[0,1] or None,
  parse_failures_in_{0,1,2}).
* `parse_final_confidence` (function) — Strict regex parser: match
  \b(0(?:\.\d+)?|1(?:\.0+)?)\b, take last match, clamp to [0.0, 1.0]; return None when no
  match.

Wraps the v1 scope-unaware Plan-and-Solve agent and adds a verbalized final_confidence field
on every trajectory, following the Xiong et al. 2024 section 3.2 protocol.

</details>
