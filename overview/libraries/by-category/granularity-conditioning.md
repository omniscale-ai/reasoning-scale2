# Libraries: `granularity-conditioning`

3 librar(y/ies).

[Back to all libraries](../README.md)

---

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
