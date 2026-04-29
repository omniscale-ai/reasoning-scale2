# ✅ Brainstorm session 2: plan Phase 1 annotation and Phase 2 baseline libraries

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0004_brainstorm_results_2` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T15:30:00Z |
| **Completed** | 2026-04-29T15:30:00Z |
| **Duration** | 0s |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0004_brainstorm_results_2/`](../../../tasks/t0004_brainstorm_results_2/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0004_brainstorm_results_2/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0004_brainstorm_results_2/task_description.md)*

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

</details>

## Research

* [`research_code.md`](../../../tasks/t0004_brainstorm_results_2/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0004_brainstorm_results_2/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0004_brainstorm_results_2/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0004_brainstorm_results_2/results/results_summary.md)*

# Brainstorm Session 2 — Results Summary

## Summary

Second brainstorm produced three new not-started tasks for parallel execution: a v1
hierarchical annotation pilot and two baseline libraries (ReAct+tags for the A condition,
Plan-and-Solve for the B condition). Round 2 suggestion cleanup deferred to a follow-up
session.

## Session Overview

* **Date**: 2026-04-29
* **Context**: Triggered after t0001-t0003 wave completed at $0 spend, with 15 uncovered
  suggestions queued.
* **Prompt**: Plan Phase 1 annotation deliverable and the libraries Phase 2 baseline
  experiment will need.

## Decisions

1. **Create `t0005_hierarchical_annotation_pilot_v1`** (covers `S-0002-08`,
   `hierarchical-annotation`). Audit and conform the 115 existing pilot rows to the global /
   subtask / atomic schema with at least a 10% LLM-as-judge spot-check. Output one `dataset`
   asset.
2. **Create `t0006_scope_aware_react_library`** (covers `S-0002-07`, `write-library`).
   Implement the A condition as ReAct extended with `{global, subtask, atomic}` granularity
   tags. No external cost.
3. **Create `t0007_scope_unaware_planandsolve_library`** (covers `S-0002-06`,
   `write-library`). Adapt LangChain Plan-and-Execute as the canonical B baseline. No external
   cost.
4. **Defer Round 2 suggestion cleanup**. Duplicates identified (S-0003-01 ≈ S-0002-04 for
   FrontierMath, S-0003-02 ≈ S-0002-03 for ServiceNow) but rejection corrections were not
   authorised in this session.
5. **Defer SWE-bench Docker harness (S-0002-05)** until experiment tasks need it.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 3 |
| Suggestions covered by new tasks | 3 |
| Suggestions rejected | 0 |
| Suggestions reprioritized | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file` — t0004, t0005, t0006, t0007 PASSED.
* `verify_corrections` — t0004 PASSED (no corrections).
* `verify_suggestions` — t0004 PASSED.
* `verify_logs` — t0004 PASSED (LG-W005, LG-W007, LG-W008 acceptable for a planning task).

## Next Steps

t0005, t0006, t0007 are independent and parallel-safe. Spawn three parallel `/execute-task`
background agents immediately after this PR merges. After all three land, hold a Round-2-only
brainstorm to clean up duplicate suggestions and propose the Phase 2 smoke-test experiment.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0004_brainstorm_results_2/results/results_detailed.md)*

# Brainstorm Session 2 — Detailed Results

## Summary

Second brainstorm produced three new not-started tasks (t0005, t0006, t0007) and explicitly
deferred Round 2 suggestion cleanup, the SWE-bench Docker harness, and the FrontierMath /
WorkArena++ access blockers.

## Methodology

1. Ran `aggregate_tasks`, `aggregate_suggestions --uncovered`, and `aggregate_costs` to load
   project state. Read full descriptions of all 9 high-priority suggestions.
2. Reassessed priorities against completed-task results: identified S-0003-01 ≈ S-0002-04 and
   S-0003-02 ≈ S-0002-03 as duplicates (FrontierMath and ServiceNow respectively).
3. Proposed three parallel-safe tasks aligned to Phase 1 deliverable and Phase 2 baseline
   needs.
4. Researcher confirmation: "run round 1 using fork as you did earlier" — authorised task
   creation only, deferred Round 2 cleanup.
5. Created the brainstorm task folder and three child task folders.
6. Ran verificators, committed, opened PR, merged.
7. After merge, three parallel `/execute-task` background agents spawned for t0005, t0006,
   t0007.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 3 |
| Suggestions covered by new tasks | 3 |
| Suggestions rejected | 0 |
| Suggestions reprioritized | 0 |
| Corrections written | 0 |
| Answer assets produced | 0 |

## Limitations

Planning task; no experiments run. Round 2 cleanup deferred — uncovered suggestion count
remains high after this session.

## Files Created

* `tasks/t0004_brainstorm_results_2/` — full brainstorm-results task folder.
* `tasks/t0005_hierarchical_annotation_pilot_v1/{task.json,task_description.md}`.
* `tasks/t0006_scope_aware_react_library/{task.json,task_description.md}`.
* `tasks/t0007_scope_unaware_planandsolve_library/{task.json,task_description.md}`.

## Verification

* `verify_task_file` — t0004, t0005, t0006, t0007: PASSED.
* `verify_corrections` — t0004: PASSED (no corrections).
* `verify_suggestions` — t0004: PASSED.
* `verify_logs` — t0004: PASSED.

</details>
