# Libraries: `hierarchical-planning`

3 librar(y/ies).

[Back to all libraries](../README.md)

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
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |
| **Created by** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Documentation** | [`description.md`](../../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/assets/library/abc_harness_metrics/description.md) |

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
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Documentation** | [`description.md`](../../../tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/description.md) |

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
<summary>📦 <strong>Scope-Unaware Plan-and-Solve Agent (v1)</strong>
(<code>scope_unaware_planandsolve_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `scope_unaware_planandsolve_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Documentation** | [`description.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md) |

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
