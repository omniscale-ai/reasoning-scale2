# ⏳ Phase 2 A/B/C smoke harness on FrontierScience subset

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0012_phase2_abc_smoke_frontierscience` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-04-30T00:55:11Z |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source suggestion** | `S-0006-03` |
| **Task types** | `experiment-run`, `baseline-evaluation` |
| **Expected assets** | 3 predictions, 1 library |
| **Task folder** | [`t0012_phase2_abc_smoke_frontierscience/`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/task_description.md)*

# Phase 2 A/B/C Smoke Harness on FrontierScience Subset

## Motivation

This is the project's **first end-to-end Phase 2 result**. It tests the headline hypothesis on
a real benchmark for the first time: scope-aware (A) > scope-unaware (B) > scope-mismatched
(C). The smoke test is intentionally narrow — single benchmark (FrontierScience-Olympiad),
single provider (Anthropic Claude), N=28 hierarchy-complete rows from the v2 dataset, paired
across conditions. The goal is a directional signal plus a sample-size calibration for
follow-up confirmatory runs. Implements suggestions S-0006-03, S-0007-02, and S-0005-06.

## Hypotheses tested

| RQ | Predicted direction | Detection threshold at N=28 |
| --- | --- | --- |
| RQ1 — A success rate > B success rate | A − B ≥ +5pp | ~15pp paired (McNemar/sign test, α=0.05) |
| RQ2 — A overconfident error rate < B | A − B ≤ −2pp | ~5-8pp paired |
| RQ5 — C worst on Metrics 1 and 2 | C < min(A, B) on both | clear ranking when A > B + 5pp |

Excluded by design (handled in separate experiments on the right benchmarks):

* RQ3 (request-vs-act accuracy on low-level tasks) — needs tau-bench, not FrontierScience.
* RQ4 (gains concentrated in info-asymmetric states) — needs WorkArena++ or tool-using
  benchmark.

## Scope

* Build a small `phase2_smoke_harness_v1` library under `assets/library/` that:
  * Loads the v2 dataset asset from t0009 and filters to FrontierScience-Olympiad rows with
    `hierarchy_completeness == true`.
  * Runs a phase-order walk over each row's `hierarchy` (global → all subtasks → all
    `global_atomics`); for each step in the walk, dispatches to one of the three libraries (A:
    t0006, B: t0007, C: t0010).
  * Captures every step's trajectory record into one JSONL per condition under
    `assets/predictions/`.
  * Calls t0011's `compute_overconfident_error_rate` on each trajectory file.
  * Computes `task_success_rate` by parsing each trajectory's final `Finish` answer and
    comparing to the row's gold final answer (FrontierScience problems end with `FINAL ANSWER:
    ...`).
  * Reports `avg_decisions_per_task` per condition.
* Produce three `predictions` assets (one per condition: A, B, C).
* Produce one `library` asset for the harness itself.
* Run on the **28 hierarchy-complete FrontierScience-Olympiad rows** from the v2 dataset (this
  matches the v1 hierarchy-complete count; refine after t0009 lands if v2 row count differs).

Out of scope: multi-provider replication (deferred), benchmark-specific tool registries beyond
a minimal `python_exec` for FrontierScience math problems, scaling N beyond ~28.

## Approach

1. Read the v2 dataset asset from t0009 once t0009 has merged. Filter to FrontierScience-
   Olympiad and `hierarchy_completeness == true`.
2. Implement the harness library that drives the phase-order walk and dispatches
   per-condition. Reuse t0006, t0007, t0010 libraries; reuse t0011's calibration aggregator.
3. For each row, run all three conditions against the same model (`claude-sonnet-4-6-20251001`
   recommended) with paired execution (same seed where applicable, same problem text, same
   tool registry).
4. Tool registry is minimal: a single `python_exec` tool for arithmetic and one
   `Finish(answer)` tool. FrontierScience-Olympiad rows are mostly verbal reasoning; tools
   exist for explicit computation only.
5. Persist trajectory JSONLs under `assets/predictions/<condition>/files/`. Compute and
   persist metrics.
6. Write `results/results_summary.md` with the 3×3 condition × metric table and the predicted-
   versus-observed effect sizes. Write `results/results_detailed.md` with per-row trajectories
   summarised, the McNemar p-value for A-vs-B and B-vs-C, and the implied sample size for
   follow-up confirmatory runs.
7. Generate at least 2 charts: condition × metric bar chart with confidence intervals; per-row
   success matrix heatmap (rows=problems, columns=conditions).

## Expected Outputs

* `assets/library/phase2_smoke_harness_v1/` — the harness library.
* `assets/predictions/phase2_smoke_a/`, `assets/predictions/phase2_smoke_b/`,
  `assets/predictions/phase2_smoke_c/` — three predictions assets, one per condition.
* `results/metrics.json` in explicit-variant format (3 variants: A, B, C; metrics:
  `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`).
* `results/results_summary.md` and `results/results_detailed.md` with hypothesis-test results,
  effect sizes, sample-size calibration, and clear acknowledgement of the excluded RQs.
* `results/images/` with at least 2 charts.
* Follow-up suggestions for: multi-provider replication (Gemini, OpenAI), expansion to
  tool-using benchmarks (SWE-bench, tau-bench), confirmatory N expansion based on observed
  variance.

## Compute and Budget

No GPU. Anthropic API only. **Budget cap: USD 20** (per-task default cap is $10; this task
exceeds the default and explicitly opts up). Estimated breakdown: 28 rows × 3 conditions × ~3
self-consistency calls per step × ~6 steps per row × ~$0.005 per call = $7.5 baseline; budget
$20 leaves headroom for retries and the calibration prompt.

## Dependencies and Cross-References

* **Hard dependencies (must be `completed`)**:
  * `t0009_hierarchical_annotation_v2` — produces the v2 dataset asset this task consumes.
  * `t0010_matched_mismatch_library` — produces the C-condition library.
  * `t0011_metric2_calibration_aggregator` — produces the Metric 2 implementation.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  libraries.
* References Yao2022 ReAct, Wang2023 Plan-and-Solve, and Xiong2024 calibration paper assets
  from t0002.

## Source Suggestion

S-0006-03 — "Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience subset." Also
covers S-0007-02 and S-0005-06 by consolidation.

## Key Questions

1. Does A − B reach the +5pp threshold on `task_success_rate`?
2. Does A − B reach the −2pp threshold on `overconfident_error_rate`?
3. Does C rank strictly worst on both metrics relative to A and B?
4. What is the within-condition variance, and what N does the FrontierScience confirmatory run
   need to detect a 5pp effect at α=0.05 with paired test?
5. Are there per-domain (physics / chemistry / biology) effect-size differences worth
   surfacing to the next brainstorm?

</details>
