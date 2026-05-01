---
spec_version: "1"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 6
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: t0021_plan_and_solve_v2_with_final_confidence

## Task Objective

Identify the existing assets, libraries, and data shapes that the v2 Plan-and-Solve library must
extend, the trajectory schema callers depend on, the smoke harness wiring that consumed the v1
library, and the registered metric that will be used to validate the new `final_confidence` field
end-to-end. The deliverable is a v2 library that elicits a verbalized confidence (Xiong2024 §3.2) on
top of the existing Plan-and-Solve agent and is validated by a 5-row × 3-condition smoke run on
FrontierScience-Olympiad with `claude-haiku-4-5`.

## Library Landscape

Two libraries are registered in the project and relevant to this task. Both must remain importable
without modification — the v2 work introduces a new library alongside them rather than mutating
either one.

* **`scope_unaware_planandsolve_v1`** — created by [t0007]; lives at
  `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`. Provides the
  `PlanAndSolveAgent` used by Conditions B and C in the t0012 smoke. Aggregator output reflects the
  original asset (no corrections). **Relevant**: this is the direct base for the v2 entry point.
  Import path: `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve`.

* **`matched_mismatch_v1`** — created by [t0010]; lives at
  `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`. Implements Condition C by reusing
  `PLAN_PROMPT_TEMPLATE`, `EXECUTE_PROMPT_TEMPLATE`, and `_parse_executor_output` from [t0007].
  **Relevant**: the v2 design must keep the v1 module's public symbols intact so this library still
  works after t0021 ships. Import path:
  `tasks.t0010_matched_mismatch_library.code.matched_mismatch`.

No other registered libraries surfaced via the aggregator. The v2 library will be registered as
`scope_unaware_planandsolve_v2` under `assets/library/` in this task.

## Key Findings

### v1 Plan-and-Solve agent shape and trajectory schema

The v1 library [t0007] exposes `PlanAndSolveAgent.run(problem: str) -> AgentResult`. The result
carries `final_answer: str | None`, `trajectory: list[TrajectoryRecord]`, and `plan: list[str]`.
Each `TrajectoryRecord` has six fields —
`(turn_index, granularity, thought, action, observation, confidence)` — and `confidence` is always
`None` in v1. The `granularity` slot is always `"unspecified"`. The model-call shape is
`Callable[[str], str]` with no conversation memory; turn context is reconstructed by the agent in
each prompt. `parse_plan` extracts numbered steps via the regex `^\s*\d+[\.\)]\s+(.+)$` and raises
`MalformedPlanError` on empty plans. The executor parser handles three patterns: `FINAL_ANSWER:`,
`Action: <tool> | Args: <args>`, and `THOUGHT_ONLY:`. Termination triggers when an executor response
yields `FINAL_ANSWER:` — the loop appends a finish record (`action="finish"`,
`observation=final_answer`) and breaks.

### t0012 smoke harness already has a `final_confidence` slot for B and C

The harness from [t0012] (`tasks/t0012_phase2_abc_smoke_frontierscience/code/harness.py`) writes
per-row JSONL records that include `final_confidence: float | None` at the **top level** of each
record. For Condition A (chain-of-thought) the field is populated; for Conditions B and C it is
always `null` because v1 never elicits a verbalized confidence. The harness includes
`extract_final_confidence(trajectory) -> float | None` that walks the trajectory in reverse and
returns the last numeric per-step `confidence` — but since v1 never sets per-step confidence, this
fallback always returns `None`. The v2 library should populate `final_confidence` at the **result
level** so downstream consumers can read it directly without relying on the per-step fallback.

### Metric 2 collapses to 0.0 for B and C in t0012

The registered metric `overconfident_error_rate` from [t0011]
(`tasks/t0011_metric2_calibration_aggregator/code/calibration.py`) is the fraction of records that
are wrong with `predicted_confidence >= HIGH_CONFIDENCE_THRESHOLD` (0.75). Empty input returns 0.0.
The metric uses `CalibrationRecord(problem_id, predicted_label, predicted_confidence, is_correct)`.
In the [t0012] N=40 smoke, B and C each had `overconfident_error_rate = 0.0` because every record
had `predicted_confidence is None`. This collapses Metric 2 and makes RQ4 untestable until v2 fills
in the field.

### Model-call shape and CLI wrapping

The [t0012] `model_call.py` wraps the local `claude` CLI with `--system-prompt`, `--tools ""`,
`--setting-sources ""` to strip the default Claude Code system prompt and tools. It records cost and
usage via a `CostTracker` and reports `total_cost_usd` per call from the CLI envelope. It is
designed for `claude-haiku-4-5`. The agent module is **not a registered library**, so the v2 task
must **copy** it into `code/model_call.py` to honor the cross-task import rule.

### Dataset path

The smoke validation should pull rows from
`tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
filtered by `benchmark == "FrontierScience-Olympiad"` and `hierarchy_completeness == True`, matching
the [t0012] selection.

### Two-call protocol must reconstruct conversation in the prompt

Because v1's model-call shape is `Callable[[str], str]` with no conversation memory, the "two-call
protocol with shared conversation prefix" rule must be honored by reconstructing the prefix in the
prompt itself: the confidence call's prompt must include the original question, the final answer the
agent already produced, and only then ask for the 0-1 confidence. This honors the no-double-prime
intent (the model sees its own answer before rating it but cannot revise it) without requiring a
stateful chat API.

### Haiku confidence distribution risk

Empirically [t0012] reports `task_success_rate = 0.0` for Condition B at N=40 with Haiku, and Haiku
is known to verbalize 0.7-0.9 confidence even on wrong answers. At N=5 this means 5/5 rows are
likely wrong, and at least one will likely report confidence ≥ 0.75 — so Metric 2 should be
non-degenerate (>0) for B in the smoke. If the Haiku flat distribution risk holds across all 5 rows,
Metric 2 may even reach 1.0; either outcome validates the wiring.

## Reusable Code and Assets

* **Source**: `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`
  * **What it does**: `PlanAndSolveAgent.run`, `parse_plan`, `_parse_executor_output`,
    `MalformedPlanError`, `TrajectoryRecord`, `AgentResult`, `ScriptedModel`,
    `PLAN_PROMPT_TEMPLATE`, `EXECUTE_PROMPT_TEMPLATE`, `TRAJECTORY_RECORD_FIELDS`.
  * **Reuse method**: **import via library** (registered as `scope_unaware_planandsolve_v1`).
  * **Function signatures**:
    `PlanAndSolveAgent(model_call: Callable[[str], str], max_turns: int = 12)`;
    `run(problem: str) -> AgentResult`.
  * **Adaptation needed**: none for v1; v2 will compose this agent and add a confidence post-call.
  * **Line count**: ~280 lines.

* **Source**: `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`
  * **What it does**: Condition C agent that hierarchically expands plan steps.
  * **Reuse method**: **import via library** (registered as `matched_mismatch_v1`).
  * **Function signatures**: `MatchedMismatchAgent(model_call, ...)`; `run(problem) -> AgentResult`.
  * **Adaptation needed**: in the smoke harness, wrap calls to its result through a v2 confidence
    post-call (using the same prompt as v2 Condition B) so Condition C also carries
    `final_confidence`.
  * **Line count**: ~200 lines.

* **Source**: `tasks/t0011_metric2_calibration_aggregator/code/calibration.py`
  * **What it does**: `compute_overconfident_error_rate(records, threshold=0.75) -> float`,
    `CalibrationRecord`, `HIGH_CONFIDENCE_THRESHOLD = 0.75`.
  * **Reuse method**: **copy into task** (not registered as a library; needed for smoke metric
    computation in `code/run_smoke.py`).
  * **Function signatures**:
    `compute_overconfident_error_rate(records: Iterable[CalibrationRecord], threshold: float = 0.75) -> float`.
  * **Adaptation needed**: none.
  * **Line count**: ~80 lines.

* **Source**: `tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py`
  * **What it does**: Wraps the local `claude` CLI with `--tools ""` and `--system-prompt`/
    `--setting-sources` flags; tracks per-call cost via `CostTracker`.
  * **Reuse method**: **copy into task** (not a library).
  * **Function signatures**:
    `make_model_call(model: str, cost_tracker: CostTracker, note: str) -> Callable[[str], str]`;
    `CostTracker.is_budget_ok(headroom_usd: float) -> bool`.
  * **Adaptation needed**: keep as-is; only required for the smoke validation script.
  * **Line count**: ~150 lines.

* **Source**: `tasks/t0012_phase2_abc_smoke_frontierscience/code/harness.py`
  * **What it does**: Loads the FrontierScience-Olympiad dataset slice, runs all three conditions,
    runs the haiku judge, writes JSONL predictions with the per-row schema (including the unfilled
    top-level `final_confidence` slot).
  * **Reuse method**: **copy** specific helpers into `code/run_smoke.py` (judge prompt, dataset
    loader, RowOutcome dataclass). Do not copy the full harness — the task only needs a 5-row smoke
    runner.
  * **Function signatures**: `JUDGE_PROMPT_TEMPLATE`, `RowOutcome`, helpers around dataset
    filtering.
  * **Adaptation needed**: shrink to N=5; replace v1 Condition B agent with v2; add a v2 confidence
    post-call wrapper for Conditions A and C so all three carry `final_confidence`.
  * **Line count**: ~400 lines (only ~150 lines of helpers will be copied).

* **Source**:
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
  * **What it does**: dataset of FrontierScience-Olympiad rows with hierarchy annotations.
  * **Reuse method**: **read-only** asset path; no copying needed.
  * **Adaptation needed**: filter to `benchmark == "FrontierScience-Olympiad"` and
    `hierarchy_completeness == True`, then take the first 5 rows.

## Lessons Learned

* **The per-step `confidence` slot was over-engineered for v1.** [t0007] introduced it but never
  filled it. Adding `final_confidence` at the **result level** for v2 (and a parallel
  `TrajectoryRecordV2` with the field for spec literalism) keeps the design clean instead of
  overloading per-step confidence.
* **The v1 module is a stable foundation.** [t0007]'s tests use `ScriptedModel` (deterministic fake)
  — no live API. The v2 module should keep the same testing convention so unit tests run offline.
* **Cost tracking matters at smoke scale.** [t0012] consumed budget through inadvertently-included
  default Claude Code system prompts; the fix in `model_call.py` (`--system-prompt`, `--tools ""`)
  must be preserved verbatim.
* **Verbalized confidence on a stateless API requires prompt-level conversation reconstruction.**
  Earlier tasks did not need this because they ran chain-of-thought in a single call; the two-call
  protocol forces the design.
* **Metric 2 needs at least one wrong-and-confident row to be non-degenerate.** A 5-row smoke is
  small enough to fail this test if Haiku happens to verbalize low confidence on every wrong row,
  but [t0012]'s observed 0.7-0.9 Haiku confidence distribution makes this unlikely.

## Recommendations for This Task

1. **Write `code/planandsolve_v2.py`** that imports the v1 agent and parsers from [t0007] and adds
   `PlanAndSolveAgentV2`, `TrajectoryRecordV2`, `AgentResultV2`, `parse_final_confidence`, and
   `CONFIDENCE_PROMPT_TEMPLATE`. Run the v1 algorithm to get the final answer, then issue **one**
   confidence call whose prompt includes the question and the produced answer. On parse failure,
   retry once with a stricter prompt; on second failure set `final_confidence=None` and increment a
   `final_confidence_parse_failures` counter.
2. **Register the new library at `assets/library/scope_unaware_planandsolve_v2/`** with
   `details.json`, `description.md`, and `files/prompts/confidence_prompt.txt` containing the
   verbatim Xiong2024 §3.2 phrasing. Cite the paper in the description.
3. **Copy** `model_call.py` from [t0012] into `code/model_call.py` and the calibration module from
   [t0011] into `code/calibration.py`. Both are not libraries, so they cannot be imported across
   tasks.
4. **Build `code/run_smoke.py`** that loads 5 FrontierScience-Olympiad rows, runs A/B/C with
   per-condition `final_confidence` (B uses the v2 agent directly; C wraps the [t0010]
   matched-mismatch agent in the same v2 confidence post-call; A reuses chain-of-thought from
   [t0006] but routes through the v2 confidence post-call to keep the field present in all three
   conditions). Use the [t0012] judge prompt verbatim for `is_correct`.
5. **Compute Metric 2 per condition** using `compute_overconfident_error_rate` from the copied
   calibration module; report values in `results/metrics.json`.
6. **Keep v1 imports intact.** Do not edit `tasks/t0007_*/code/planandsolve.py` or
   `tasks/t0010_*/code/matched_mismatch.py`; they remain the canonical v1 source.

## Task Index

### [t0006]

* **Task ID**: `t0006_scope_aware_react_library`
* **Name**: Scope-aware ReAct library (Condition A)
* **Status**: completed
* **Relevance**: Provides Condition A in the smoke (scope-aware ReAct with granularity tags). The v2
  confidence post-call must wrap A's output so all three conditions carry `final_confidence`.

### [t0007]

* **Task ID**: `t0007_scope_unaware_planandsolve_library`
* **Name**: scope_unaware_planandsolve_v1
* **Status**: completed
* **Relevance**: This is the v1 Plan-and-Solve library. v2 imports its prompts, parsers, and core
  agent and adds a verbalized confidence post-call.

### [t0009]

* **Task ID**: `t0009_hierarchical_annotation_v2`
* **Name**: Hierarchical annotation v2 dataset
* **Status**: completed
* **Relevance**: Source of FrontierScience-Olympiad rows used by the smoke validation (5 rows × 3
  conditions).

### [t0010]

* **Task ID**: `t0010_matched_mismatch_library`
* **Name**: matched_mismatch_v1
* **Status**: completed
* **Relevance**: Condition C agent that imports symbols from the v1 Plan-and-Solve module. v2 must
  preserve those symbols so this library remains importable; the smoke wraps Condition C with the v2
  confidence post-call.

### [t0011]

* **Task ID**: `t0011_metric2_calibration_aggregator`
* **Name**: Metric 2 calibration aggregator
* **Status**: completed
* **Relevance**: Defines `compute_overconfident_error_rate` and `HIGH_CONFIDENCE_THRESHOLD = 0.75`.
  v2 smoke validation copies this module to compute Metric 2 per condition.

### [t0012]

* **Task ID**: `t0012_phase2_abc_smoke_frontierscience`
* **Name**: Phase 2 A/B/C smoke on FrontierScience-Olympiad
* **Status**: in_progress
* **Relevance**: Source of the smoke harness pattern, judge prompt, model-call wrapper, and dataset
  filter. Demonstrated that B/C `overconfident_error_rate = 0.0` because v1 never sets
  `final_confidence` — the failure mode that motivates this task.
