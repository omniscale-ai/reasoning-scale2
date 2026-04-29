# Brainstorm Session 3 — Results Summary

## Summary

Third brainstorm produced four new not-started tasks. The v1 annotation schema was found to lack
subtask-to-atomic edges; a v2 re-annotation task was inserted ASAP as t0009. The original wave 3
plan (matched-mismatch library, Metric 2 calibration, A/B/C smoke harness) was preserved and
renumbered to t0010-t0012, with t0012 gated on the other three.

## Session Overview

* **Date**: 2026-04-30
* **Context**: Triggered after wave 2 (t0004-t0007) merged at $0.06 spend, with 27 uncovered
  suggestions and the v2 schema gap surfaced during prompt-modelling discussion of the `is_bored`
  annotation.
* **Prompt**: Plan the first Phase 2 result on a real benchmark, with whatever schema upgrades are
  needed to make the harness honest about the granularity transitions.

## Decisions

1. **Create `t0009_hierarchical_annotation_v2`** (covers `S-0005-01` partial + `S-0005-02` + new
   schema finding). Re-annotate all 115 rows under the tree schema with full problem text; spot-
   check at least 20% with the LLM judge. Cost ~$15. No deps. ASAP.
2. **Create `t0010_matched_mismatch_library`** (covers `S-0007-01`). Implements the C condition on
   top of `scope_unaware_planandsolve_v1`, reusing t0007's `TRAJECTORY_RECORD_FIELDS`. No external
   cost. No deps.
3. **Create `t0011_metric2_calibration_aggregator`** (covers `S-0002-02`). Implements the Xiong2024
   verbalized-confidence + 3-sample self-consistency protocol. No external cost. No deps.
4. **Create `t0012_phase2_abc_smoke_frontierscience`** (covers `S-0006-03`, `S-0007-02`,
   `S-0005-06`). First end-to-end Phase 2 A/B/C smoke run on the FrontierScience subset of the v2
   dataset. N=28 paired across conditions. Single provider (Anthropic). Budget $20. Deps: t0009,
   t0010, t0011.
5. **Defer Round 2 suggestion cleanup** (rejecting S-0003-01 / S-0003-02 as duplicates;
   reprioritizing four high-priority access/infrastructure suggestions to medium). Will be addressed
   in the next brainstorm.
6. **Defer multi-provider replication** of the smoke test until t0012 produces a single-provider
   headline result.

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

After this PR merges, fork three parallel `/execute-task` background agents for t0009, t0010, t0011.
t0012 stays `not_started`; spawn its agent only after all three deps complete. Plan a brainstorm 4
once t0012 lands to address Round 2 cleanup, schedule multi-provider replication, and decide whether
to expand the v2 dataset or move to a tool-using benchmark next.
