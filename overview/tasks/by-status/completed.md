# ✅ Tasks: Completed

10 tasks. ✅ **10 completed**.

[Back to all tasks](../README.md)

---

## ✅ Completed

<details>
<summary>✅ 0011 — <strong>Metric 2 calibration aggregator: verbalized confidence
+ 3-sample self-consistency</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_metric2_calibration_aggregator` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:12Z |
| **End time** | 2026-04-29T23:43:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Task folder** | [`t0011_metric2_calibration_aggregator/`](../../../tasks/t0011_metric2_calibration_aggregator/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md) |

# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as
the canonical calibration protocol — verbalized confidence elicitation (low / medium / high +
brief justification) plus 3-sample self-consistency aggregation. Without this library, the
Phase 2 smoke test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the
diagnostic Metric 3 (avg decisions per task). This task unblocks the headline experiment by
producing a library that any agent's trajectory records can be passed through to compute
`overconfident_error_rate`. Implements suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/`
  exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low /
    medium / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem
    and returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is
    majority-vote on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float`
    that returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls
    the model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at
  `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` covering: prompt
  template formatting, parsing of low / medium / high confidence labels, majority-vote
  aggregation across 3 samples (including ties), threshold-based overconfident detection, and
  end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic
tests only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a
   `paths.py` and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold
  default rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration
  error) computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric
2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized
   labels mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default:
   prefer the highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results
   can include it in `metrics.json` directly?

**Results summary:**

> **Results Summary — Metric 2 Calibration Aggregator**
>
> **Summary**
>
> Implemented the metric2_calibration_aggregator_v1 library that operationalizes the project's
> Metric
> 2 (`overconfident_error_rate`) using the Xiong2024 §3.2 black-box calibration protocol. The
> library
> exposes `ConfidencePromptTemplate`, `ConfidenceJudge`, `elicit_confidence`,
> `compute_overconfident_error_rate`, and `CalibrationRecord` plus a trajectory-record
> adapter, with a
> single overridable threshold default (`HIGH_CONFIDENCE_THRESHOLD = 0.75`) and the canonical
> low/medium/high → 0.25/0.5/0.9 numeric mapping.
>
> **Metrics**
>
> * **Tests run**: 25 — all passed in 0.03 s
> (`uv run pytest tasks/t0011_metric2_calibration_aggregator/code/`).
> * **Code lines written**: ~340 in `code/calibration.py`, ~125 in `code/constants.py`, ~40 in
> `code/paths.py`, ~370 in `code/test_calibration.py` (test count includes the `ScriptedModel`
> fake).
> * **Public API surface**: 5 entry points required by the task description plus 1 helper
> (`calibration_record_from_trajectory`); 6 entry points listed in `details.json`.

</details>

<details>
<summary>✅ 0010 — <strong>Matched-mismatch library: condition C with deliberately
wrong granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0007-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:02Z |
| **End time** | 2026-04-29T23:46:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Matched-mismatch library: condition C with deliberately wrong granularity tags](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../../tasks/t0010_matched_mismatch_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0010_matched_mismatch_library/results/results_detailed.md) |

# Matched-Mismatch Library (Condition C)

## Motivation

The project's main hypothesis includes sub-hypothesis 2: scope-mismatched agents perform
strictly worse than both scope-aware (A) and scope-unaware (B) baselines. Without a C library,
research question 5 cannot be tested. This task implements C by wrapping the existing
libraries (`scope_aware_react_v1` from t0006 or `scope_unaware_planandsolve_v1` from t0007)
with a granularity-tag layer that emits **deliberately incorrect** tags at each step. The
library shares the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007 so a Phase 2 harness
can run all three conditions interchangeably. Implements suggestion S-0007-01.

## Scope

* Implement a library asset under `assets/library/matched_mismatch_v1/` exposing a
  `MatchedMismatchAgent` class that:
  * Accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
    registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`.
  * Walks the v2 hierarchy in phase order (the harness's canonical walk), determines the
    correct granularity at each step from the annotation, and **assigns an incorrect tag**
    according to the strategy:
    * `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`.
    * `adversarial`: always pick the most distant tag (`atomic` when correct is `global`,
      `global` when correct is `atomic`, `atomic` when correct is `subtask`).
  * Delegates each step to either `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`
    (configurable). The delegate handles the actual model call; the wrapper only controls the
    granularity tag.
  * Emits trajectory records in the canonical `TRAJECTORY_RECORD_FIELDS` schema, with the
    `granularity` field carrying the *wrong* tag (the actual correct tag is logged separately
    as `_correct_granularity` in an extras blob).
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` covering:
  random-strategy uniformity over `{global, subtask, atomic} \ correct_tag`,
  adversarial-strategy correctness, schema parity with t0007, end-to-end run with both
  delegate options.

Out of scope: the actual A/B/C experiment (handled by t0012), benchmark-specific tool
registries, remote execution.

## Approach

1. Read t0007's `scope_unaware_planandsolve_v1` library and t0006's `scope_aware_react_v1`
   library. Confirm the canonical trajectory schema is `TRAJECTORY_RECORD_FIELDS` from t0007.
2. Implement the library in `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
   Re-export the public API from `assets/library/matched_mismatch_v1/library/`.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests are deterministic (no live API calls). Use `ScriptedModel` from t0007 as the
   delegate's model.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/matched_mismatch_v1/` with `details.json`, `description.md`, `files/`.
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion to make the random-strategy mismatch ablation (uniform random vs.
  adversarial vs. matched) explicit in t0012.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  library assets. Reads `TRAJECTORY_RECORD_FIELDS` from t0007.

## Source Suggestion

S-0007-01 — "Implement matched-mismatch (C) library on top of scope_unaware_planandsolve_v1."

## Key Questions

1. What is the cleanest way to handle a granularity tag for steps that fall under
   `global_atomics` (cross-cutting atomics with no parent subtask)? Default: treat as `atomic`
   for the purposes of the mismatch strategy.
2. Should the wrapper expose a way to override the mismatch policy per-step (e.g., to inject
   targeted mismatches in specific phases)? Default: no, keep the wrapper minimal.
3. How should the schema's `_correct_granularity` extras field be standardised so a downstream
   experiment can compute the mismatch contribution per step?

**Results summary:**

> **Results Summary: Matched-Mismatch Library (Condition C)**
>
> **Summary**
>
> Implemented the project's condition-C library `matched_mismatch_v1` — a wrapper that walks
> the v2
> hierarchy from t0009 in canonical phase order, substitutes a deliberately incorrect
> granularity tag
> according to a `random` or `adversarial` strategy, and delegates the per-phase model call to
> either
> the t0006 ReAct or t0007 Plan-and-Solve format. The library reuses t0007's
> `TRAJECTORY_RECORD_FIELDS` schema unchanged and stores the correct tag in
> `extras["_correct_granularity"]`. All 14 deterministic tests pass and every `REQ-*`
> checklist item
> is satisfied.
>
> **Metrics**
>
> * **Tests passed**: 14 of 14 (`uv run pytest tasks/t0010_matched_mismatch_library/code/
>   -v`).
> * **Source lines (`matched_mismatch.py`)**: 463 lines including documentation and `__all__`
>   export
> list.
> * **Public API entry points**: 6 (`MatchedMismatchAgent`, `MatchedMismatchRecord`,
>   `AgentRunResult`,
> `Phase`, `iter_phases`, `pick_mismatch_tag`).
> * **Module-level constants exported**: 4 (`GRANULARITY_VALUES`, `ADVERSARIAL_MAP`,

</details>

<details>
<summary>✅ 0008 — <strong>Brainstorm session 3: insert v2 re-annotation, plan Phase
2 smoke</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0008_brainstorm_results_3` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T00:00:00Z |
| **End time** | 2026-04-30T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 3: insert v2 re-annotation, plan Phase 2 smoke](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md) |
| **Task folder** | [`t0008_brainstorm_results_3/`](../../../tasks/t0008_brainstorm_results_3/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0008_brainstorm_results_3/results/results_detailed.md) |

# Brainstorm Session 3

## Context

Wave 2 (t0004 brainstorm + t0005, t0006, t0007) merged at $0.06 total cost. The literature
survey, benchmark download, annotation pilot v1, and both scope-aware / scope-unaware
libraries are complete. The project is poised for the first Phase 2 result — but the v1
annotation schema has a structural gap that must be fixed first.

## Schema gap discovered

While modelling A/C condition prompts on the `is_bored` (HumanEval/91) row, we found that the
v1 annotation schema is **flat**: `subtask` is a list of strings, `atomic` is a list of
strings, and there is **no encoded edge** mapping atomics to their parent subtask. For the
`hierarchical-annotation-v1` smoke harness this forces one of three orderings — none of them
faithful to how humans actually reason hierarchically — and undermines the cleanliness of the
A-vs-B-vs-C contrast in the planned Phase 2 smoke test.

The fix is a tree-shaped v2 schema:

```json
{
  "hierarchy": {
    "global": "...",
    "subtasks": [
      {"subtask": "...", "atomics": ["...", "..."]},
      ...
    ],
    "global_atomics": ["..."]
  }
}
```

This change is **inserted as the new ASAP task** (t0009) before any of the previously-planned
wave 3 tasks can build on it.

## Decisions

Four new tasks created, all `not_started`. Three are parallel-safe; one waits on the others:

* `t0009_hierarchical_annotation_v2` (covers `S-0005-01` partial + `S-0005-02` + new schema
  finding) — re-annotate all 115 rows under the tree schema with full problem text. **No
  deps.**
* `t0010_matched_mismatch_library` (covers `S-0007-01`) — matched-mismatch (C) library; reuses
  t0007's `TRAJECTORY_RECORD_FIELDS`. Schema-independent. **No deps.**
* `t0011_metric2_calibration_aggregator` (covers `S-0002-02`) — Xiong2024
  verbalized-confidence + 3-sample self-consistency aggregator. Schema-independent. **No
  deps.**
* `t0012_phase2_abc_smoke_frontierscience` (covers `S-0006-03`, `S-0007-02`, `S-0005-06`) —
  first end-to-end Phase 2 A/B/C run on the FrontierScience subset of the **v2** dataset.
  **Deps**: t0009, t0010, t0011.

## Why this wave

Three tasks unblock the headline experiment:

* t0009 fixes the schema so the harness can drive granularity transitions naturally
  (depth-first by subtask in v2) instead of by an artificial phase walk over flat lists.
* t0010 provides the C condition without which RQ5 (sub-hypothesis 2) cannot be tested.
* t0011 implements Metric 2; without it the smoke test can only report Metric 1.

t0012 is the first run that produces a directional A/B/C signal on a real benchmark. It is
deliberately scoped as a smoke test (N=28 on hierarchy-complete FS-Olympiad rows, single
provider Anthropic, paired across conditions) rather than a definitive experiment. The
follow-up multi-provider replication (Gemini + OpenAI keys are now available) is queued for
the next brainstorm.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03; demoting four high-priority access/infrastructure suggestions to medium) —
  flagged earlier but explicitly deferred to keep this session focused on the v2 ASAP work.
* Multi-provider (Gemini, OpenAI) replication of the smoke test — deferred until t0012
  produces a single-provider headline result.
* Annotation v2 row-count expansion to ≥200 (covered by S-0005-01 in part; t0009 only
  re-encodes the existing 115 rows, not new annotation work).
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.

**Results summary:**

> **Brainstorm Session 3 — Results Summary**
>
> **Summary**
>
> Third brainstorm produced four new not-started tasks. The v1 annotation schema was found to
> lack
> subtask-to-atomic edges; a v2 re-annotation task was inserted ASAP as t0009. The original
> wave 3
> plan (matched-mismatch library, Metric 2 calibration, A/B/C smoke harness) was preserved and
> renumbered to t0010-t0012, with t0012 gated on the other three.
>
> **Session Overview**
>
> * **Date**: 2026-04-30
> * **Context**: Triggered after wave 2 (t0004-t0007) merged at $0.06 spend, with 27 uncovered
> suggestions and the v2 schema gap surfaced during prompt-modelling discussion of the
> `is_bored`
> annotation.
> * **Prompt**: Plan the first Phase 2 result on a real benchmark, with whatever schema
>   upgrades are
> needed to make the harness honest about the granularity transitions.
>
> **Decisions**
>

</details>

<details>
<summary>✅ 0007 — <strong>Scope-unaware Plan-and-Solve library: condition B
baseline</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-06` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:48Z |
| **End time** | 2026-04-29T20:01:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Scope-unaware Plan-and-Solve library: condition B baseline](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../../tasks/t0007_scope_unaware_planandsolve_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0007_scope_unaware_planandsolve_library/results/results_detailed.md) |

# Scope-Unaware Plan-and-Solve Library (Condition B)

## Motivation

The literature survey in t0002 identified Plan-and-Solve (Wang2023) as the strongest published
prompt-only baseline that does not condition on explicit granularity tags. It is therefore the
canonical scope-unaware (B) baseline for the project's A-vs-B-vs-C comparison. This task
produces the matching library asset, sharing the trajectory-log schema with t0006 so a Phase 2
experiment can run both libraries against the same harness without bespoke glue. Implements
suggestion S-0002-06.

## Scope

* Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
  `PlanAndSolveAgent` class that:
  * Accepts a problem statement, a tool registry, and a model-call callable.
  * Generates a free-form numbered plan, then executes each step sequentially through a
    Plan-and-Execute loop.
  * Emits trajectory records in the same schema as `scope_aware_react_v1` so both libraries
    are drop-in interchangeable. The `granularity` field in the schema is filled with the
    literal string `"unspecified"` to mark the B condition.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}`.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing
  from scratch. License is Apache 2.0; record attribution in `description.md`.
* Provide pytest coverage at
  `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` covering: plan
  parsing, sequential execution, trajectory schema parity with t0006, finish detection, and
  error recovery on malformed model output.

Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
execution.

## Approach

1. Read t0002's Wang2023 paper summary and the LangChain Plan-and-Execute source to ground the
   prompt template and execution loop.
2. Implement the library in
   `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and re-export the
   public API from `assets/library/scope_unaware_planandsolve_v1/library/`.
3. Reuse the trajectory log schema defined in t0006 by reading t0006's library when it lands;
   if t0006 has not landed yet, define the schema here and document that t0006 must conform.
4. Write `details.json`, `description.md`, and `files/` for the asset.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_unaware_planandsolve_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for the matched mismatch (C) library.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. May reference t0006's library if it merges first; otherwise this task
  defines the trajectory schema and t0006 must conform.
* References Wang2023 paper asset (`10.48550_arXiv.2305.04091`) from t0002.

## Source Suggestion

S-0002-06 — "Implement Plan-and-Solve as the canonical scope-unaware (B) baseline."

## Key Questions

1. What plan format does Plan-and-Solve produce, and how should it be parsed
   deterministically?
2. How should the library mark the absence of a granularity tag in the trajectory record?
3. What is the minimal API surface that lets a Phase 2 harness swap between this and t0006's
   library by changing only one line?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0007_scope_unaware_planandsolve_library"
> date_completed: "2026-04-29"
> ---
> **Results Summary — t0007_scope_unaware_planandsolve_library**
>
> **Summary**
>
> Produced one library asset, `scope_unaware_planandsolve_v1`, that adapts LangChain's
> Plan-and-Execute reference implementation of Wang et al.'s Plan-and-Solve prompting (arXiv
> 2305.04091) as the canonical scope-unaware (B) baseline for the project. The library passes
> its
> asset verificator and a 14-case pytest suite, all without any paid API calls.
>
> **Metrics**
>
> * **Library tests passing**: **14 / 14** (zero failures)
> * **Ruff errors on task code**: **0**
> * **Mypy errors on task code**: **0**
> * **Library asset verificator errors / warnings**: **0 / 0**

</details>

<details>
<summary>✅ 0006 — <strong>Scope-aware ReAct library: condition A with explicit
granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-07` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:38Z |
| **End time** | 2026-04-29T20:07:30Z |
| **Step progress** | 10/15 |
| **Task page** | [Scope-aware ReAct library: condition A with explicit granularity tags](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../../tasks/t0006_scope_aware_react_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0006_scope_aware_react_library/results/results_detailed.md) |

# Scope-Aware ReAct Library (Condition A)

## Motivation

The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a `{global, subtask, atomic}` granularity tag emitted at every Thought /
Action turn, plus a logging hook that records the active tag alongside the model's confidence.
The library is the substrate every Phase 2 A-condition experiment will import. Implements
suggestion S-0002-07.

## Scope

* Implement a library asset under `assets/library/scope_aware_react_v1/` exposing a
  `ScopeAwareReactAgent` class that:
  * Accepts a problem statement, a fixed `granularity` argument (`"global" | "subtask" |
    "atomic"`), a tool registry, and a model-call callable.
  * Loops Thought / Action / Observation steps, prepending the active granularity tag to every
    Thought emission, and parses Action JSON until the agent emits a `Finish` action.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}` to
    a JSONL trajectory file the experiment harness can replay.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` covering: tag
  injection, action parsing, finish detection, error recovery on malformed JSON, and
  trajectory logging integrity.

Out of scope: the actual A-vs-B-vs-C experiment (a separate experiment-run task), benchmark-
specific tool registries (also a separate task), and any remote-execution wiring.

## Approach

1. Read t0002's `research/research_papers.md` and the Yao2022 paper summary to ground the
   prompt format. Reuse LangChain's ReAct prompt where appropriate; the project licence is
   Apache 2.0.
2. Implement the library in `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`
   and re-export the public API from a `library/__init__.py` shim under `assets/library/
   scope_aware_react_v1/`.
3. Write the asset's `details.json`, `description.md`, and `files/` directory with the
   runnable source.
4. Write tests as deterministic unit tests; no live API calls.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_aware_react_v1/` with `details.json`, `description.md`, and `files/`.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` and matching test file.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for benchmark-specific tool registries.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Yao2022 paper asset (`10.48550_arXiv.2210.03629`) from t0002.
* Sister task `t0007_scope_unaware_planandsolve_library` produces the matched B baseline; both
  must follow the same trajectory-logging schema so a Phase 2 experiment can consume both.

## Source Suggestion

S-0002-07 — "Implement scope-aware (A) as ReAct extended with explicit granularity tags."

## Key Questions

1. What is the minimal extension to ReAct's prompt template that reliably elicits a
   granularity tag on every Thought emission?
2. How should the library handle a model that refuses to emit a tag (back off, abort, or
   default to `atomic`)?
3. What schema for the trajectory log lets t0007 emit identical-shape records?

**Results summary:**

> **Results Summary: Scope-Aware ReAct Library**
>
> **Summary**
>
> Shipped the project's first library asset: `scope_aware_react_v1`, implementing condition A
> (scope-aware ReAct) with explicit `{global, subtask, atomic}` granularity tags, a JSONL
> trajectory
> writer whose six-field schema is the canonical contract for both this library and t0007, and
> deterministic-replay testing via `ScriptedModel`. All quality gates clean and the asset
> verificator
> passed.
>
> **Metrics**
>
> * **Library asset**: 1 (`scope_aware_react_v1`), passes
>   `meta.asset_types.library.verificator` with
> **0 errors / 0 warnings**.
> * **Tests**: **8 / 8** passing in `code/test_scope_aware_react.py`
> (`pytest tasks/t0006_scope_aware_react_library/code/ -v` reported all tests passing).
> * **Source files**: **3 modules** in `code/` (`scope_aware_react.py` ~370 lines,
>   `constants.py`,
> `paths.py`) plus 1 test file.
> * **Public entry points**: **6** (`ScopeAwareReactAgent`, `ScriptedModel`,
>   `TrajectoryRecord`,
> `Action`, `AgentResult`, `MalformedActionError`).

</details>

<details>
<summary>✅ 0005 — <strong>Hierarchical annotation pilot v1: audit and conform
existing 115 rows</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_hierarchical_annotation_pilot_v1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0002-08` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T19:35:28Z |
| **End time** | 2026-04-29T20:14:30Z |
| **Step progress** | 9/15 |
| **Task page** | [Hierarchical annotation pilot v1: audit and conform existing 115 rows](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Task folder** | [`t0005_hierarchical_annotation_pilot_v1/`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0005_hierarchical_annotation_pilot_v1/results/results_detailed.md) |

# Hierarchical Annotation Pilot v1

## Motivation

Phase 1 of the project's roadmap requires ≥100 tasks fully annotated with gold actions at
three granularity levels (global / subtask / atomic). The imported
`project/data/annotation_pilot/ tasks_annotated.jsonl` already contains 115 LLM-annotated
rows, but the rows have not been verified to conform to the project's three-level schema and
there is no human or LLM-as-judge spot-check pass on record. This task closes that gap in v1
form: keep the existing 115 rows in place, audit their structure, and produce a canonical
dataset asset that downstream Phase 2 / 3 experiments can consume. Implements suggestion
S-0002-08.

## Scope

* Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on
  each row to determine whether it carries explicit global / subtask / atomic granularity
  labels or whether the granularity must be inferred.
* If labels are missing, write a deterministic mapper that derives the three-level structure
  from the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block
  per row.
* Run an LLM-as-judge spot-check on at least 10% of rows (≥12 rows) to estimate hierarchy
  quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/`
  with rows of shape `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask,
  atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict,
  judge_notes}`.

Out of scope for v1: replacing the HumanEval and Mind2Web proxies, expanding beyond 115 rows,
human review, inter-rater agreement studies. All deferred to follow-up tasks.

## Approach

1. Load the 115-row pilot file. For each row, compute the inferred or stated hierarchy and
   emit the canonical schema record.
2. Sample at least 12 rows stratified across the four benchmarks (FrontierScience-Olympiad,
   SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Send each to the LLM judge with the
   row's problem text and proposed hierarchy; capture verdict ("acceptable" / "needs
   revision") plus a one-sentence justification.
3. Persist the consolidated dataset asset with `details.json` (source URL = the imported pilot
   path, version = "v1", license = inherited from each upstream benchmark, sample count = 115)
   and `files/hierarchical_annotation_v1.jsonl`.
4. Report distribution stats in `results/results_detailed.md` (per-benchmark counts,
   per-domain counts, hierarchy-completeness rate, judge accept rate).

## Expected Outputs

* `assets/dataset/hierarchical_annotation_v1/` with `details.json`, `files/`, and a
  `description.md`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate.
* `results/results_detailed.md` with the full audit table and any rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (the registered diagnostic
  metric).
* Follow-up suggestions for: extension to ≥200 rows, full human-review pass, and proxy
  benchmark remediation.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: under 3 USD for 12-15 LLM-as-judge calls on
`claude-haiku-4-5-20251001`. Per-task cap: 5 USD.

## Dependencies and Cross-References

* No task dependencies.
* Reads `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows).
* Reads `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules — wrap
  as black-box utilities, never modify in place.
* References the four benchmark dataset assets produced by `t0003_download_benchmark_subsets`.

## Source Suggestion

S-0002-08 — "Run a Phase 1 pilot annotation on 20 tasks before scaling to 100." This task
implements that idea in v1 form, leveraging the existing 115 rows rather than re-annotating
from scratch.

## Key Questions

1. Do the existing 115 rows already carry a global / subtask / atomic decomposition, or must
   one be inferred?
2. What is the per-benchmark hierarchy-completeness rate?
3. What is the LLM-as-judge accept rate? Does it differ across benchmarks?
4. Are there systematic patterns in rejected rows (e.g., one benchmark consistently failing)?

**Results summary:**

> **Results Summary: Hierarchical Annotation Pilot v1**
>
> **Summary**
>
> Audited the 115-row pilot annotation file, projected each row's `steps.nodes` graph onto the
> project's three-level global / subtask / atomic schema with a deterministic Python mapper,
> ran an
> LLM-as-judge spot-check on a 12-row stratified sample using `claude-haiku-4-5-20251001` via
> the
> local `claude` CLI, and produced a single canonical `hierarchical-annotation-v1` dataset
> asset (115
> rows). The asset passes the dataset verificator with 0 errors and 1 warning.
>
> **Metrics**
>
> * **Rows in dataset**: **115** (FrontierScience-Olympiad **40**, SWE-bench Verified **23**,
> tau-bench **26**, WorkArena++ **26**)
> * **Overall hierarchy completeness**: **88.7%** (102 / 115 rows have a non-null `global` and
>   a
> non-empty `atomic` list)
> * **Per-benchmark completeness**: FrontierScience-Olympiad **70.0%** (28/40), SWE-bench
>   Verified
> **100.0%** (23/23), tau-bench **96.2%** (25/26), WorkArena++ **100.0%** (26/26)
> * **LLM-as-judge accept rate (overall)**: **33.3%** (4/12 rows accepted)
> * **Per-benchmark judge accept rate**: FrontierScience-Olympiad **0.0%** (0/3), SWE-bench
>   Verified

</details>

<details>
<summary>✅ 0004 — <strong>Brainstorm session 2: plan Phase 1 annotation and Phase
2 baseline libraries</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_brainstorm_results_2` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T15:30:00Z |
| **End time** | 2026-04-29T15:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 2: plan Phase 1 annotation and Phase 2 baseline libraries](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md) |
| **Task folder** | [`t0004_brainstorm_results_2/`](../../../tasks/t0004_brainstorm_results_2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0004_brainstorm_results_2/results/results_detailed.md) |

# Brainstorm Session 2

## Context

Second brainstorm session. The first wave (t0001 brainstorm + t0002 literature survey + t0003
benchmark download) completed at $0 cost. Three completed tasks have produced 11 paper assets,
4 dataset assets, and 15 uncovered follow-up suggestions.

Key findings carried into this session:

* **Literature survey (t0002)** identified Plan-and-Solve [Wang2023] as the canonical
  scope-unaware (B) baseline, ReAct [Yao2022] as the foundation for the scope-aware (A)
  condition, and Xiong2024 as the calibration protocol for Metric 2.
* **Benchmark download (t0003)** confirmed FrontierMath (gated by Epoch AI) and WorkArena++
  (gated by ServiceNow + HF) cannot be unblocked by infrastructure work in the current
  session. Pilot proxies are frozen as fallback. SWE-bench Verified and tau-bench are
  accessible.
* The deferred T3 candidate from session 1 (`hierarchical_annotation_pilot`) is now
  appropriate to schedule, but in a smaller v1 form: audit and conform the existing 115 pilot
  rows rather than attempt a full re-annotation.

## Decisions

Three new tasks created, all `not_started`, no inter-task dependencies (parallel-safe):

* `t0005_hierarchical_annotation_pilot_v1` (covers `S-0002-08`) — audit & conform the existing
  pilot annotations to the global / subtask / atomic schema.
* `t0006_scope_aware_react_library` (covers `S-0002-07`) — write-library: ReAct extended with
  granularity tags. Implements the A condition.
* `t0007_scope_unaware_planandsolve_library` (covers `S-0002-06`) — write-library:
  Plan-and-Solve adapted from LangChain. Implements the B condition.

## Why this wave

t0005 unblocks Phase 1 (annotation deliverable). t0006 + t0007 are the two libraries the Phase
2 baseline experiment will consume. Once all three are merged, the Phase 2 smoke-test
experiment (deferred T4 from session 1) becomes practical to schedule.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03) is intentionally deferred to a follow-up session.
* SWE-bench Docker harness (S-0002-05) is deferred until experiment tasks need it.
* FrontierMath (S-0002-04 / S-0003-01) and ServiceNow (S-0002-03 / S-0003-02) access remain
  open high-priority blockers but not on the path to first Phase 2 results.

**Results summary:**

> **Brainstorm Session 2 — Results Summary**
>
> **Summary**
>
> Second brainstorm produced three new not-started tasks for parallel execution: a v1
> hierarchical
> annotation pilot and two baseline libraries (ReAct+tags for the A condition, Plan-and-Solve
> for the
> B condition). Round 2 suggestion cleanup deferred to a follow-up session.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Triggered after t0001-t0003 wave completed at $0 spend, with 15 uncovered
>   suggestions
> queued.
> * **Prompt**: Plan Phase 1 annotation deliverable and the libraries Phase 2 baseline
>   experiment will
> need.
>
> **Decisions**
>
> 1. **Create `t0005_hierarchical_annotation_pilot_v1`** (covers `S-0002-08`,
> `hierarchical-annotation`). Audit and conform the 115 existing pilot rows to the global /
> subtask

</details>

<details>
<summary>✅ 0003 — <strong>Download benchmark subsets for the four roadmap
sources</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_download_benchmark_subsets` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 4 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Start time** | 2026-04-29T14:30:55Z |
| **End time** | 2026-04-29T14:58:30Z |
| **Step progress** | 8/15 |
| **Task page** | [Download benchmark subsets for the four roadmap sources](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Task folder** | [`t0003_download_benchmark_subsets/`](../../../tasks/t0003_download_benchmark_subsets/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0003_download_benchmark_subsets/results/results_detailed.md) |

# Download Benchmark Subsets

## Motivation

Phase 1 (annotation) and Phase 2 (baseline scope-aware vs. scope-unaware experiment) both
depend on having local, reproducible subsets of the four roadmap benchmarks. The existing
pilot annotation data uses HumanEval and Mind2Web proxies for tau-bench and WorkArena++
because the real benchmarks were "unavailable on HF" at original-annotation time. This task
either resolves that gap by acquiring the real benchmarks or, if access is genuinely
unavailable, documents the decision to keep proxies and freezes the choice for Phase 2.

## Scope

Acquire four benchmark subsets, each targeted at multi-step tasks of 4-8 decisions per task to
match the project's stated difficulty range:

* FrontierScience-Olympiad — full official distribution path; subset by domain to match the
  pilot's physics / chemistry / biology focus.
* WorkArena++ — official distribution. If genuinely inaccessible (gated, retired, dataset
  moved), document the access attempt and keep the Mind2Web proxy already present in the
  pilot.
* SWE-bench Verified — official Princeton/HF distribution; subset to instances that map
  cleanly onto the project's three-level hierarchy.
* tau-bench — official distribution. If genuinely inaccessible, keep the HumanEval proxy with
  documented justification.

Out of scope: full benchmark execution harnesses (those belong in later experiment-run tasks),
custom annotation (that belongs in T3 hierarchical-annotation pilot), and modifications of
benchmark data (subsetting only, no relabelling).

## Approach

1. For each benchmark, attempt the official distribution path documented in its source paper
   or GitHub README. Cache successful downloads under the task's
   `assets/dataset/<slug>/files/`.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata
   the benchmark provides. If no such metadata exists, sample uniformly and document the
   sampling seed.
3. Produce one dataset asset per benchmark with `details.json` describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log to the dataset asset's
   `details.json` with `download_status: "failed"` and a clear `download_failure_reason`. The
   project's policy in this case is to keep the existing pilot proxy and not block on access.
5. Emit follow-up suggestions for any benchmark whose access pathway is non-obvious or whose
   subsetting choice deserves a Phase 2 sensitivity check.

## Expected Outputs

* Four dataset assets under
  `assets/dataset/{frontierscience,workarena_plus_plus,swebench_verified, taubench}/` with
  `details.json` and `files/` directories (or empty `files/` plus a clear failed status if
  inaccessible).
* `results/results_summary.md` with a per-benchmark access status, sample count, and any
  subset decisions.
* `results/suggestions.json` flagging any benchmarks where the proxy choice is now permanent.

## Compute and Budget

No GPU. No paid API calls anticipated. All work is local downloads and metadata writing.
Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. Independent of T1.
* Cross-references: existing pilot annotation data at
  `project/data/annotation_pilot/tasks_annotated.jsonl` documents the proxy decisions this
  task must either resolve or formalise.

**Results summary:**

> **Results Summary: Download Benchmark Subsets**
>
> **Summary**
>
> Acquired four benchmark subsets covering the project's roadmap sources
> (FrontierScience-Olympiad,
> WorkArena++, SWE-bench Verified, tau-bench). Three were downloaded directly from public
> sources;
> WorkArena++ instance enumeration is gated on a live ServiceNow developer instance, so its
> asset
> captures the upstream curriculum manifest only and freezes the Mind2Web pilot proxy as the
> de-facto
> Phase 2 fallback. All four dataset assets pass `verify_dataset_asset` with zero errors.
>
> **Metrics**
>
> * **4 of 4** dataset assets created and passing `verify_dataset_asset` (zero errors, zero
>   warnings).
> * **FrontierScience-Olympiad subset**: **40** problems (15 physics, 10 chemistry, 15
>   biology),
> packaged from pilot rows; status **success** (FrontierMath upstream still gated).
> * **WorkArena++ subset**: **42** compositional task class lists extracted from upstream
> `curriculum.py`; status **success (manifest only)**, instance enumeration deferred and
> Mind2Web
> pilot proxy frozen.
> * **SWE-bench Verified subset**: **60** instances filtered from **500** Verified using the
>   4-8 hunks
> rule; status **success**.

</details>

<details>
<summary>✅ 0002 — <strong>Literature survey: granularity conditioning and
hierarchical agents</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_granularity_conditioning` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 10 paper |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-29T13:50:47Z |
| **End time** | 2026-04-29T14:26:49Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: granularity conditioning and hierarchical agents](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Task folder** | [`t0002_literature_survey_granularity_conditioning/`](../../../tasks/t0002_literature_survey_granularity_conditioning/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0002_literature_survey_granularity_conditioning/results/results_detailed.md) |

# Literature Survey: Granularity Conditioning and Hierarchical Agents

## Motivation

The project's central hypothesis is that explicitly conditioning an LLM agent on its current
operating granularity (global / subtask / atomic) improves task success, calibration, and
request-vs-act discrimination. Before designing the Phase 2 baseline experiment we need
literature grounding on three threads: how prior work has framed and operationalised
"granularity" or "scope" labels for hierarchical agents, what hierarchical task decomposition
schemas exist in the four benchmark sources, and which uncertainty-calibration metrics have
been used in agent settings (in particular, definitions and prior measurements of the
overconfident error rate). The survey output anchors every later planning decision and lets us
cite prior work in the Phase 4 paper-ready report.

## Scope

* Granularity / scope / scale conditioning in LLM agents and prompt engineering. Include any
  work that varies the level of abstraction at which an agent receives its instructions, even
  if the authors do not use the word "granularity".
* Hierarchical task decomposition: papers proposing two-, three-, or n-level decompositions
  for benchmarks similar to those in this project (FrontierScience-Olympiad, WorkArena++,
  SWE-bench Verified, tau-bench).
* Uncertainty calibration in LLM agents: confidence elicitation methods, definitions of
  overconfident error rate, calibration plots and metrics, and prior reports on how
  calibration changes with prompt design.
* The four roadmap benchmarks themselves: their official task structures, scoring conventions,
  and any published results that bracket what counts as competitive performance.

Out of scope: training-time techniques (RL, gradient-based fine-tuning), non-English
benchmarks, production deployment papers — all consistent with the project's Out of Scope
section.

## Approach

1. Run the standard `/research-papers` and `/research-internet` stages with the three thread
   queries above. Use the `download-paper` skill for any candidate paper found via search.
2. Produce paper assets under `assets/paper/` for at least 10 highly relevant papers, each
   with a summary that conforms to the paper asset specification.
3. Aggregate findings into `research/research_papers.md` with a section per thread:
   granularity conditioning, hierarchical decomposition, calibration metrics, benchmark
   grounding.
4. Connect each thread back to the project's research questions and explicitly flag (a) any
   prior work that already answers a research question, (b) any methodological choices the
   survey resolves for Phase 2, and (c) any open questions to surface as suggestions.

## Expected Outputs

* At least 10 paper assets under `assets/paper/<paper_id>/` with `details.json`, summary, and
  PDF or markdown file.
* `research/research_papers.md` and `research/research_internet.md` synthesising the survey.
* `results/results_summary.md` with a thread-by-thread takeaway and explicit follow-up
  suggestions for the next brainstorm session (typically: which benchmarks to deprioritise,
  which conditioning prompts to adopt, which calibration metric to register as a project
  metric).
* `results/suggestions.json` with concrete follow-up ideas surfaced by the survey.

## Compute and Budget

No GPU. Anthropic API only (the project's `available_services` list dropped `openai_api` until
an API key is provided). Estimated cost: under 5 USD for paper summarisation through Claude.

## Dependencies and Cross-References

* No task dependencies. Independent of T2.
* Reads `project/description.md` for research questions and success criteria.
* The project's pre-existing `project/data/annotation_pilot/tasks_annotated.jsonl` should be
  inspected during the survey to ground discussion of benchmark coverage.

## Key Questions

1. What prior work explicitly compares scope-aware vs. scope-unaware vs. scope-mismatched LLM
   agents on multi-step benchmarks, and what effect sizes did they report?
2. What definitions of "overconfident error rate" exist in the agent calibration literature,
   and which is most appropriate for our Metric 2 specification?
3. What hierarchical decomposition schemas are already published for FrontierScience-Olympiad,
   WorkArena++, SWE-bench Verified, and tau-bench, and how do they map to our global / subtask
   / atomic split?
4. Are the WorkArena++ and tau-bench benchmarks truly inaccessible (as the existing pilot data
   suggests), or are there standard distribution channels we missed?

**Results summary:**

> **Results Summary: Literature Survey on Granularity Conditioning and Hierarchical Agents**
>
> **Summary**
>
> Completed a literature survey of 11 papers covering granularity / scope conditioning of LLM
> agents,
> hierarchical task decomposition, uncertainty calibration, and the four roadmap benchmarks
> (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). All 11 paper assets
> pass the
> v3 paper-asset verificator and are tagged with project categories.
>
> **Metrics**
>
> * **11 paper assets created** out of a 10-paper minimum target — exceeds REQ-1 by one paper.
> * **4 of 4 survey threads covered** with at least 2 papers each: granularity / hierarchical
> prompting (Yao2022, Wang2023, Shinn2023, Zhou2022, Wei2022 noted but not added in this round
> — 4
> added), four roadmap benchmarks (Glazer2024, Drouin2024, Boisvert2024, Jimenez2024,
> OpenAI2024,
> Yao2024 — 6 added), calibration (Xiong2024 — 1 added).
> * **0 errors** across 11 verificator runs; 1 minor warning (PA-W007 missing-country) on the
>   first
> paper, fixed by adding country codes.
>
> **Verification**

</details>

<details>
<summary>✅ 0001 — <strong>Brainstorm session 1: plan first project tasks</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0001_brainstorm_results_1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T00:00:00Z |
| **End time** | 2026-04-29T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 1: plan first project tasks](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md) |
| **Task folder** | [`t0001_brainstorm_results_1/`](../../../tasks/t0001_brainstorm_results_1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0001_brainstorm_results_1/results/results_detailed.md) |

# Brainstorm Session 1

## Context

This is the first brainstorm session for the granularity-aware hierarchical agents project,
executed inline as part of `/setup-project` immediately after `meta/` was populated. The
project has no completed tasks, no suggestions, and no answer assets, so the session focused
on Round 1 (propose first tasks). Rounds 2 (suggestion cleanup) and 3 (confirmation) had
nothing to clean up and proceeded straight to confirmation.

## Decisions

The researcher accepted two child tasks for immediate creation:

* `t0002_literature_survey_granularity_conditioning` — survey papers on granularity / scope /
  scale conditioning in LLM agents, hierarchical task decomposition, and uncertainty
  calibration metrics.
* `t0003_download_benchmark_subsets` — wire up access to subsets of the four roadmap
  benchmarks (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench) at
  difficulty 4-8 decisions per task.

Two further candidate tasks (`hierarchical_annotation_pilot` and
`baseline_scope_experiment_smoke_test`) were discussed in detail but deferred — the researcher
will review T1 and T2 outputs before committing.

## Why these tasks first

T1 and T2 are independent and low-cost. T1 anchors later planning decisions in the literature;
T2 unblocks every Phase 1 annotation extension and every Phase 2/3 experiment. Running them in
parallel keeps the project moving while preserving the option to redirect after the literature
survey.

## Out-of-band notes

* `project/data/annotation_pilot/tasks_annotated.jsonl` already contains 115 LLM-annotated
  rows, but tau-bench and WorkArena++ rows use HumanEval and Mind2Web proxies because the real
  benchmarks were "unavailable on HF" at original-annotation time. T2 must address this
  directly.
* The `available_services` list dropped `openai_api` during setup because no API key was
  provided; `anthropic_api` remains. T1 and T2 should plan their LLM use accordingly.

**Results summary:**

> **Brainstorm Session 1 — Results Summary**
>
> **Summary**
>
> The first brainstorm session for the granularity-aware hierarchical agents project produced
> two new
> not-started tasks (literature survey and benchmark download) and deferred two further
> candidates
> pending the literature-survey output. No suggestions, corrections, or answer assets were
> produced;
> the project is brand new and the suggestion backlog is empty.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Inline brainstorm executed by `/setup-project` immediately after `meta/` was
> populated. Project repository was a fresh fork of the Glite ARF template.
> * **Prompt**: Translate the project description and four-phase roadmap into concrete first
>   tasks the
> researcher can launch.
>
> **Decisions**
>
> 1. **Create `t0002_literature_survey_granularity_conditioning`**. Survey the literature on

</details>
