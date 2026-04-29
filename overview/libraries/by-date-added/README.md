# Libraries by Date Added

3 librar(y/ies) grouped by creation date.

[Back to all libraries](../README.md)

---

## 2026-04-29 (3)

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
<summary>📦 <strong>Scope-Aware ReAct Agent</strong>
(<code>scope_aware_react_v1</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `scope_aware_react_v1` |
| **Version** | 0.1.0 |
| **Modules** | `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`, `tasks/t0006_scope_aware_react_library/code/constants.py`, `tasks/t0006_scope_aware_react_library/code/paths.py` |
| **Dependencies** | — |
| **Date created** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Created by** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Documentation** | [`description.md`](../../../tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/description.md) |

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
