# ✅ Brainstorm session 3: insert v2 re-annotation, plan Phase 2 smoke

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0008_brainstorm_results_3` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T00:00:00Z |
| **Completed** | 2026-04-30T00:00:00Z |
| **Duration** | 0s |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0008_brainstorm_results_3/`](../../../tasks/t0008_brainstorm_results_3/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0008_brainstorm_results_3/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0008_brainstorm_results_3/task_description.md)*

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

</details>

## Research

* [`research_code.md`](../../../tasks/t0008_brainstorm_results_3/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0008_brainstorm_results_3/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0008_brainstorm_results_3/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0008_brainstorm_results_3/results/results_summary.md)*

# Brainstorm Session 3 — Results Summary

## Summary

Third brainstorm produced four new not-started tasks. The v1 annotation schema was found to
lack subtask-to-atomic edges; a v2 re-annotation task was inserted ASAP as t0009. The original
wave 3 plan (matched-mismatch library, Metric 2 calibration, A/B/C smoke harness) was
preserved and renumbered to t0010-t0012, with t0012 gated on the other three.

## Session Overview

* **Date**: 2026-04-30
* **Context**: Triggered after wave 2 (t0004-t0007) merged at $0.06 spend, with 27 uncovered
  suggestions and the v2 schema gap surfaced during prompt-modelling discussion of the
  `is_bored` annotation.
* **Prompt**: Plan the first Phase 2 result on a real benchmark, with whatever schema upgrades
  are needed to make the harness honest about the granularity transitions.

## Decisions

1. **Create `t0009_hierarchical_annotation_v2`** (covers `S-0005-01` partial + `S-0005-02` +
   new schema finding). Re-annotate all 115 rows under the tree schema with full problem text;
   spot- check at least 20% with the LLM judge. Cost ~$15. No deps. ASAP.
2. **Create `t0010_matched_mismatch_library`** (covers `S-0007-01`). Implements the C
   condition on top of `scope_unaware_planandsolve_v1`, reusing t0007's
   `TRAJECTORY_RECORD_FIELDS`. No external cost. No deps.
3. **Create `t0011_metric2_calibration_aggregator`** (covers `S-0002-02`). Implements the
   Xiong2024 verbalized-confidence + 3-sample self-consistency protocol. No external cost. No
   deps.
4. **Create `t0012_phase2_abc_smoke_frontierscience`** (covers `S-0006-03`, `S-0007-02`,
   `S-0005-06`). First end-to-end Phase 2 A/B/C smoke run on the FrontierScience subset of the
   v2 dataset. N=28 paired across conditions. Single provider (Anthropic). Budget $20. Deps:
   t0009, t0010, t0011.
5. **Defer Round 2 suggestion cleanup** (rejecting S-0003-01 / S-0003-02 as duplicates;
   reprioritizing four high-priority access/infrastructure suggestions to medium). Will be
   addressed in the next brainstorm.
6. **Defer multi-provider replication** of the smoke test until t0012 produces a
   single-provider headline result.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 4 |
| Suggestions covered by new tasks | 8 |
| Suggestions rejected | 0 |
| Suggestions reprioritized | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file` — t0008, t0009, t0010, t0011, t0012 PASSED.
* `verify_corrections` — t0008 PASSED (no corrections).
* `verify_suggestions` — t0008 PASSED.
* `verify_logs` — t0008 PASSED (LG-W005, LG-W007, LG-W008 acceptable for a planning task).

## Next Steps

After this PR merges, fork three parallel `/execute-task` background agents for t0009, t0010,
t0011. t0012 stays `not_started`; spawn its agent only after all three deps complete. Plan a
brainstorm 4 once t0012 lands to address Round 2 cleanup, schedule multi-provider replication,
and decide whether to expand the v2 dataset or move to a tool-using benchmark next.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0008_brainstorm_results_3/results/results_detailed.md)*

# Brainstorm Session 3 — Detailed Results

## Summary

Four new not-started tasks created (t0009-t0012). The v2 re-annotation task was inserted ASAP
based on a schema gap discovered during prompt-modelling discussion. Round 2 cleanup and
multi-provider replication were explicitly deferred.

## Methodology

1. Aggregated tasks, suggestions, and costs. 7 completed tasks, 27 uncovered suggestions,
   $0.06 spent.
2. Read full descriptions of high-priority suggestions. Identified consolidation opportunities
   (S-0006-03 + S-0007-02 + S-0005-06 = same headline experiment).
3. Proposed three-task wave 3 (matched-mismatch + Metric 2 + smoke harness on v1 dataset).
4. Researcher requested concrete prompt models for A/B/C conditions on a random row from the
   pilot dataset.
5. Modelled prompts on `he_HumanEval_91` (`is_bored` problem). Discovered the v1 hierarchy
   schema is flat (`subtask: list[str]`, `atomic: list[str]`) with no subtask-to-atomic edges.
6. Researcher decided to redo annotation under a tree schema ASAP, then return to wave 3.
7. Inserted t0009 (v2 re-annotation) as the new ASAP task; renumbered the original three tasks
   to t0010-t0012.
8. Researcher confirmation: "confirm".
9. Created the brainstorm task folder and four child task folders.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 4 |
| Suggestions covered by new tasks | 8 |
| Suggestions rejected | 0 |
| Suggestions reprioritized | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Limitations

Planning task; no experiments run. Round 2 cleanup deferred — uncovered suggestion count of 27
remains after this session.

## Files Created

* `tasks/t0008_brainstorm_results_3/` — full brainstorm-results task folder.
* `tasks/t0009_hierarchical_annotation_v2/{task.json,task_description.md}`.
* `tasks/t0010_matched_mismatch_library/{task.json,task_description.md}`.
* `tasks/t0011_metric2_calibration_aggregator/{task.json,task_description.md}`.
* `tasks/t0012_phase2_abc_smoke_frontierscience/{task.json,task_description.md}`.

## Verification

* `verify_task_file` — t0008, t0009, t0010, t0011, t0012: PASSED.
* `verify_corrections` — t0008: PASSED (no corrections).
* `verify_suggestions` — t0008: PASSED.
* `verify_logs` — t0008: PASSED.

</details>
