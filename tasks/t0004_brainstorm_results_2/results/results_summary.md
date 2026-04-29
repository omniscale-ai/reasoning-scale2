# Brainstorm Session 2 — Results Summary

## Summary

Second brainstorm produced three new not-started tasks for parallel execution: a v1 hierarchical
annotation pilot and two baseline libraries (ReAct+tags for the A condition, Plan-and-Solve for the
B condition). Round 2 suggestion cleanup deferred to a follow-up session.

## Session Overview

* **Date**: 2026-04-29
* **Context**: Triggered after t0001-t0003 wave completed at $0 spend, with 15 uncovered suggestions
  queued.
* **Prompt**: Plan Phase 1 annotation deliverable and the libraries Phase 2 baseline experiment will
  need.

## Decisions

1. **Create `t0005_hierarchical_annotation_pilot_v1`** (covers `S-0002-08`,
   `hierarchical-annotation`). Audit and conform the 115 existing pilot rows to the global / subtask
   / atomic schema with at least a 10% LLM-as-judge spot-check. Output one `dataset` asset.
2. **Create `t0006_scope_aware_react_library`** (covers `S-0002-07`, `write-library`). Implement the
   A condition as ReAct extended with `{global, subtask, atomic}` granularity tags. No external
   cost.
3. **Create `t0007_scope_unaware_planandsolve_library`** (covers `S-0002-06`, `write-library`).
   Adapt LangChain Plan-and-Execute as the canonical B baseline. No external cost.
4. **Defer Round 2 suggestion cleanup**. Duplicates identified (S-0003-01 ≈ S-0002-04 for
   FrontierMath, S-0003-02 ≈ S-0002-03 for ServiceNow) but rejection corrections were not authorised
   in this session.
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
