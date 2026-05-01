---
spec_version: "2"
predictions_id: "phase2-smoke-c"
documented_by_task: "t0012_phase2_abc_smoke_frontierscience"
date_documented: "2026-05-01"
---

# Phase 2 smoke condition C predictions (partial)

## Metadata

* **Name**: Phase 2 smoke condition C (scope-mismatched random) on FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library matched_mismatch_v1
  (t0010) wrapping scope_unaware_planandsolve_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset, hierarchy-complete
  rows; first 11 of 40)
* **Format**: jsonl
* **Instances**: 11 (partial; budget halt before remaining 29)
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These are the partial outputs of condition C (scope-mismatched, `random` strategy) of the Phase
2 A/B/C smoke harness on FrontierScience-Olympiad. The matched-mismatch wrapper from t0010
walks the v2 hierarchy in phase order, identifies the correct granularity at each step from the
annotation, and replaces it with a uniformly-random incorrect tag drawn from the two
non-correct choices. The wrapper delegates the actual model call to
`scope_unaware_planandsolve_v1` so condition C's prompt structure matches B's exactly except
for the (deliberately wrong) tag.

The run halted after row 11 of 40 when the harness hit the $18 budget cap. The 11 rows that
completed are paired with the corresponding rows in conditions A and B for the limited paired
analysis reported in the task results.

## Model

Same `claude-haiku-4-5` model, same minimal-system-prompt CLI invocation, same tool
registry, and same set of upstream rows. Agent: `matched_mismatch_v1` with
`mismatch_strategy="random"` and `delegate="scope_unaware_planandsolve"`.

## Data

The first 11 FrontierScience-Olympiad hierarchy-complete rows from
`hierarchical-annotation-v2`, processed in the same order conditions A and B used.

## Prediction Format

JSONL, one row per problem; same schema as conditions A and B. The trajectory `granularity`
field carries the *wrong* tag the wrapper injected; the correct tag for the same step is
recorded separately in trajectory record `extras._correct_granularity`.

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `task_success_rate` | 0.000 | 0 / 11 |
| `overconfident_error_rate` | 0.000 | Same Plan-and-Solve confidence gap as B; not informative |
| `avg_decisions_per_task` | 26.0 | C trajectories run *much* longer than B (6.5) — the wrong
  granularity tag triggers replanning loops |

## Main Ideas

* Condition C ran 11 of 40 rows before the harness budget halt at $18.37. The metrics reported
  in `metrics.json` for C are computed on those 11 rows only, with a paired analysis against
  the same 11-row subset of A and B.
* The most striking observation from the partial C trajectories is the **6× decision-count
  increase** versus B (26.0 vs 6.5). The wrong granularity tag pushes Plan-and-Solve into long
  re-planning loops without converging on a final answer — exactly the failure mode RQ5
  predicted, but in a form invisible to the registered Metric 1 because both B and C end at
  zero accuracy.
* The harness budget model needs revision before any future C run: at ~$0.40 per C row (vs
  ~$0.10 for A/B) the wrapper-induced replanning eats budget. Either (a) cap turns per row in
  the C delegate, (b) reserve a dedicated budget for C, or (c) batch C against an easier
  benchmark where the success-rate signal can be observed.

## Summary

These are the 11 partial outputs of condition C from the project's first end-to-end Phase 2
smoke. The run halted at the $18 budget cap before reaching the remaining 29 rows.
Within the 11 completed rows, condition C solved zero problems (in line with conditions A and
B on the same hard FrontierScience-Olympiad benchmark) but spent dramatically more decisions
per row (26 vs 6.5 for B). The all-zero success rate makes RQ5 (sub-hypothesis 2: "C ranks
worst on Metrics 1 and 2") untestable in this run — there is no spread between A, B, and C on
the success metric to rank them.

For the project, condition C's most useful contribution from the smoke is a budget-model
finding: the matched-mismatch wrapper triggers Plan-and-Solve re-planning loops that push the
per-row cost roughly 4× higher than the matched B condition. Any future A/B/C run on a hard
benchmark must either cap C's turn count or reserve a separate budget envelope for C.
