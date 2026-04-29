# Brainstorm Session 2

## Context

Second brainstorm session. The first wave (t0001 brainstorm + t0002 literature survey + t0003
benchmark download) completed at $0 cost. Three completed tasks have produced 11 paper assets, 4
dataset assets, and 15 uncovered follow-up suggestions.

Key findings carried into this session:

* **Literature survey (t0002)** identified Plan-and-Solve [Wang2023] as the canonical scope-unaware
  (B) baseline, ReAct [Yao2022] as the foundation for the scope-aware (A) condition, and Xiong2024
  as the calibration protocol for Metric 2.
* **Benchmark download (t0003)** confirmed FrontierMath (gated by Epoch AI) and WorkArena++ (gated
  by ServiceNow + HF) cannot be unblocked by infrastructure work in the current session. Pilot
  proxies are frozen as fallback. SWE-bench Verified and tau-bench are accessible.
* The deferred T3 candidate from session 1 (`hierarchical_annotation_pilot`) is now appropriate to
  schedule, but in a smaller v1 form: audit and conform the existing 115 pilot rows rather than
  attempt a full re-annotation.

## Decisions

Three new tasks created, all `not_started`, no inter-task dependencies (parallel-safe):

* `t0005_hierarchical_annotation_pilot_v1` (covers `S-0002-08`) — audit & conform the existing pilot
  annotations to the global / subtask / atomic schema.
* `t0006_scope_aware_react_library` (covers `S-0002-07`) — write-library: ReAct extended with
  granularity tags. Implements the A condition.
* `t0007_scope_unaware_planandsolve_library` (covers `S-0002-06`) — write-library: Plan-and-Solve
  adapted from LangChain. Implements the B condition.

## Why this wave

t0005 unblocks Phase 1 (annotation deliverable). t0006 + t0007 are the two libraries the Phase 2
baseline experiment will consume. Once all three are merged, the Phase 2 smoke-test experiment
(deferred T4 from session 1) becomes practical to schedule.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03) is intentionally deferred to a follow-up session.
* SWE-bench Docker harness (S-0002-05) is deferred until experiment tasks need it.
* FrontierMath (S-0002-04 / S-0003-01) and ServiceNow (S-0002-03 / S-0003-02) access remain open
  high-priority blockers but not on the path to first Phase 2 results.
