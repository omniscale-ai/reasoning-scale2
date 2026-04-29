# Brainstorm Session 3 — Full Transcript

## Project State Presented

* Tasks: 7 completed (t0001-t0007). 0 in progress, 0 not-started.
* Cost: $0.0598 / $100 (0.06%).
* Suggestions: 27 uncovered (14 high, 8 medium, 5 low).

Key findings carried in:

* t0005 annotation pilot v1 reported a **33%** judge accept rate; FrontierScience-Olympiad rows hit
  0/3 due to 1500-char excerpt truncation. 12 of 40 FS rows had `hierarchy_completeness: false` (no
  decomposition at all). 14 task_id collisions in the source pilot file.
* t0006 + t0007 libraries shipped at $0; both converged on the same `TRAJECTORY_RECORD_FIELDS`
  schema (lucky parity, not contracted). 22 tests pass between them.
* Metric 2 (`overconfident_error_rate`) has no implementation; the Xiong2024 protocol is
  pre-registered but not yet code.

## Clarification Questions

Skipped — researcher's intent was clear from earlier context (continue toward Phase 2 result).

## Discussion — Round 1: New Tasks

AI proposed three tasks: matched-mismatch (C) library, Metric 2 aggregator, A/B/C smoke harness on
FS-Olympiad rows from the v1 dataset.

Researcher: "let's model prompts for scope-aware and scope-mismatched cases. pick random problem
from dataset"

AI sampled `he_HumanEval_91` (`is_bored`) from the v1 dataset and modelled the A and C condition
prompts. While walking through the granularity sequence (global → subtask → ... → atomic) for the A
condition, AI realised the v1 schema is flat (`subtask: list[str]`, `atomic: list[str]`) with no
encoded edge mapping atomics to their parent subtask.

Researcher: "once task has this annotations [...] what is correct order of injecting these
granularities? i.e., starting from global it can go subtaskA -> subtaskB -> atomicA -> atomicB ->
atomicC, or can go subtaskA -> atomicA -> atomicB -> subtaskB -> atomicC..."

AI explained three plausible orderings (phase, tree, agent-chosen) and recommended phase order as a
smoke-test compromise on the existing v1 schema, with a v2 tree schema flagged as a follow-up.

Researcher: "no, I need to redo labelling according v2 tree schema ASAP. then return to what we
planned for wave3"

AI revised the plan: insert t0009 (v2 tree-schema re-annotation) as the new ASAP task; preserve the
original three tasks as t0010-t0012; gate t0012 on all three.

## Discussion — Round 2: Suggestion Cleanup

AI proposed (carried over from earlier discussion): reject S-0003-01 ≈ S-0002-04 (FrontierMath
duplicate) and S-0003-02 ≈ S-0002-03 (ServiceNow duplicate); demote S-0002-04, S-0002-03, S-0002-05,
S-0005-01 from high to medium.

Researcher: did not address Round 2 in the "confirm" instruction. AI deferred cleanup to brainstorm
4 to keep this session focused on the v2 ASAP work.

## Discussion — Round 3: Confirmation

AI summarised: 4 new tasks (t0009 v2 annotation, t0010 matched-mismatch, t0011 Metric 2, t0012 smoke
harness), 0 rejections, 0 reprioritizations, 0 cancellations.

Researcher: "confirm"

## Decisions Summary

1. Create `t0009_hierarchical_annotation_v2`. ASAP. Re-annotate 115 rows under tree schema with full
   text. Cost ~$15. No deps.
2. Create `t0010_matched_mismatch_library`. Cost $0. No deps.
3. Create `t0011_metric2_calibration_aggregator`. Cost $0. No deps.
4. Create `t0012_phase2_abc_smoke_frontierscience`. Cost ~$20. Deps: t0009, t0010, t0011.
5. Defer Round 2 suggestion cleanup to brainstorm 4.
6. Defer multi-provider replication until t0012 produces a single-provider headline.
7. After PR merge, fork three parallel `/execute-task` agents for t0009, t0010, t0011. t0012 waits.
