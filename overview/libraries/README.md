# Libraries (9)

9 librar(y/ies).

**Browse by view**: By category: [`agent-evaluation`](by-category/agent-evaluation.md),
[`benchmark-frontierscience`](by-category/benchmark-frontierscience.md),
[`granularity-conditioning`](by-category/granularity-conditioning.md),
[`hierarchical-planning`](by-category/hierarchical-planning.md),
[`uncertainty-calibration`](by-category/uncertainty-calibration.md); [By date
added](by-date-added/README.md)

---

<details>
<summary>📦 <strong>ABC Harness Metrics</strong> (<code>abc_harness_metrics</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `abc_harness_metrics` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/types.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/constants.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/paths.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/judge_cache.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/model_call.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/progress_rate.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/error_taxonomy.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/score_trajectory.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/replay_t0012.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/build_subgoals_frontierscience.py`, `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/build_subgoals_swebench.py` |
| **Dependencies** | datasets |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Created by** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Documentation** | [`description.md`](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/description.md) |

**Entry points:**

* `compute_progress_rate` (function) — Ma2024 AgentBoard discrete-subgoal-coverage progress
  rate for one trajectory.
* `classify_error` (function) — Li2024 Embodied Agent Interface error-taxonomy classifier;
  returns one of seven labels (six error labels plus an ok sentinel).
* `score_trajectory` (function) — High-level entry point that composes progress rate and
  per-step error classification into a TrajectoryScore.
* `TrajectoryScore` (class) — Frozen dataclass with task_success, progress_rate, step_errors
  tuple, and error_distribution Counter.
* `ErrorTaxonomyLabel` (class) — StrEnum of the seven error-taxonomy labels (hallucination,
  affordance, missing_step, extra_step, wrong_order, precondition_or_effect, ok).
* `make_judge_call` (function) — Construct a judge callable backed by the local Claude Code
  CLI with cost-tracking and budget cap.
* `CostTracker` (class) — Process-wide cumulative-spend tracker with cap enforcement.

Adds Ma2024 AgentBoard discrete-subgoal progress rate and Li2024 Embodied Agent Interface
six-plus-one error taxonomy to the ABC harness used by t0023.

</details>

<details>
<summary>📦 <strong>Matched-Mismatch Agent (v1)</strong>
(<code>matched_mismatch_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `matched_mismatch_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Documentation** | [`description.md`](../../tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/description.md) |

**Entry points:**

* `MatchedMismatchAgent` (class) — Condition-C agent that walks a v2 hierarchy and emits
  trajectory records carrying a deliberately wrong granularity tag.
* `MatchedMismatchRecord` (class) — Frozen dataclass whose first six fields are exactly
  TRAJECTORY_RECORD_FIELDS; an extras mapping carries the correct tag under
  _correct_granularity.
* `AgentRunResult` (class) — Aggregate output of one MatchedMismatchAgent.run call:
  final_answer, trajectory, phases.
* `Phase` (class) — One step of the canonical phase-ordered walk over a v2 annotation tree
  (kind, correct_tag, payload).
* `iter_phases` (function) — Yield Phase objects in canonical order: global, then per-subtask
  (subtask, atomics), then global_atomics.
* `pick_mismatch_tag` (function) — Return a granularity tag distinct from the correct tag,
  picked uniformly at random or per ADVERSARIAL_MAP.

Condition-C wrapper that walks the v2 hierarchy in phase order and substitutes deliberately
incorrect granularity tags around either the t0006 ReAct delegate or the t0007 Plan-and-Solve
delegate.

</details>

<details>
<summary>📦 <strong>Matched-Mismatch v2 (PlanAndSolveAgentV3 delegate)</strong>
(<code>matched_mismatch_v2</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `matched_mismatch_v2` |
| **Version** | 0.2.0 |
| **Modules** | `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/matched_mismatch_v2.py` |
| **Dependencies** | — |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Created by** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Documentation** | [`description.md`](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/matched_mismatch_v2/description.md) |

**Entry points:**

* `MatchedMismatchV2Agent` (class) — Variant-C agent: runs PlanAndSolveAgentV3 once on the
  problem, then post-processes the v3 trajectory to overwrite each record's granularity with
  an adversarially-perturbed label drawn from the v2 hierarchy phase walk.
* `AgentRunResultV2` (class) — Aggregate result with the PnS-v3 trajectory shape
  (TrajectoryRecordV2 records) plus the un-perturbed phase walk and the literal delegate id
  used for logging.
* `DELEGATE_PLAN_AND_SOLVE_V3` (function) — String constant 'scope_unaware_planandsolve_v3' —
  the single supported delegate id for the v2 wrapper, used in the t0027 harness for symmetry
  with t0010 logging.

Forks t0010's matched-mismatch wrapper to delegate to PlanAndSolveAgentV3 instead of
scope_aware_react, addressing S-0026-02 so variant C is B-with-extra-degradation rather than
A-with-noise.

</details>

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
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Documentation** | [`description.md`](../../tasks/t0011_metric2_calibration_aggregator/assets/library/metric2_calibration_aggregator_v1/description.md) |

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
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Documentation** | [`description.md`](../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/library/phase2_smoke_harness_v1/description.md) |

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
<summary>📦 <strong>Plan-and-Solve v3 (Fault-Tolerant Plan Parser)</strong>
(<code>plan_and_solve_v3</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `plan_and_solve_v3` |
| **Version** | 0.3.0 |
| **Modules** | `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/planandsolve_v3.py` |
| **Dependencies** | — |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Created by** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Documentation** | [`description.md`](../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/plan_and_solve_v3/description.md) |

**Entry points:**

* `PlanAndSolveAgentV3` (class) — Plan-and-Solve v3 agent: v2 with a fault-tolerant
  plan-parsing prefix and the same verbalized-confidence postlude.
* `AgentResultV3` (class) — Aggregate result with the v2 fields plus plan_parser_recovery_path
  and plan_parser_attempts diagnostics.
* `_robust_parse_plan` (function) — Standalone planner helper that drives the three-attempt
  fallback chain (clean / re-prompt / JSON-fallback).
* `REPROMPT_PLAN_PROMPT_TEMPLATE` (function) — Template used for the second planner call when
  the first response fails to parse.
* `JSON_PLAN_PROMPT_TEMPLATE` (function) — Template used for the third planner call requesting
  a JSON object with a 'steps' array.

Forks Plan-and-Solve v2 (t0021) by adding a re-prompt and JSON-mode fallback chain when the
planner emits an unparseable numbered list, addressing S-0026-01.

</details>

<details>
<summary>📦 <strong>Scope-Aware ReAct Agent</strong>
(<code>scope_aware_react_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `scope_aware_react_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`, `tasks/t0006_scope_aware_react_library/code/constants.py`, `tasks/t0006_scope_aware_react_library/code/paths.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Documentation** | [`description.md`](../../tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/description.md) |

**Entry points:**

* `ScopeAwareReactAgent` (class) — Run the scope-aware ReAct loop with a fixed granularity for
  all turns; writes a JSONL trajectory log.
* `ScriptedModel` (class) — Deterministic helper that replays a fixed list of model
  completions for unit tests.
* `TrajectoryRecord` (class) — Frozen dataclass describing one JSONL record with the canonical
  six-field schema.
* `Action` (class) — Frozen dataclass holding a parsed Action: name (tool or 'Finish') plus
  args dict.
* `AgentResult` (class) — Frozen dataclass returned by ScopeAwareReactAgent.run() with answer,
  finished flag, turn count, and full trajectory.
* `MalformedActionError` (class) — Raised internally when the model emits a malformed Action
  JSON line; surfaced as <parse_error> in the trajectory log.

ReAct agent extended with explicit {global, subtask, atomic} granularity tags and a JSONL
trajectory writer.

</details>

<details>
<summary>📦 <strong>Scope-Unaware Plan-and-Solve Agent (v1)</strong>
(<code>scope_unaware_planandsolve_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `scope_unaware_planandsolve_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Documentation** | [`description.md`](../../tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md) |

**Entry points:**

* `PlanAndSolveAgent` (class) — Plan-then-execute agent that produces trajectory records with
  granularity='unspecified'.
* `ScriptedModel` (class) — Deterministic-test fake model returning pre-recorded responses in
  order.
* `TrajectoryRecord` (class) — Frozen dataclass for one step of a trajectory; schema shared
  with t0006's scope_aware_react_v1.
* `AgentResult` (class) — Aggregate output of one PlanAndSolveAgent.run call: final_answer,
  trajectory, plan.
* `MalformedPlanError` (class) — Raised when the planner output yields zero numbered steps.
* `parse_plan` (function) — Parse a free-form numbered plan into an ordered list of step
  strings.

Scope-unaware Plan-and-Solve agent adapting LangChain Plan-and-Execute as the canonical
condition-B baseline for the project's A-vs-B-vs-C comparison.

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
| **Categories** | [`uncertainty-calibration`](../../meta/categories/uncertainty-calibration/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Created by** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Documentation** | [`description.md`](../../tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/description.md) |

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
