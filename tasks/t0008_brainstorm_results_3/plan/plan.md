# Plan: Brainstorm Session 3

## Objective

Insert v2 tree-schema re-annotation as the new ASAP task, preserve original wave 3 (matched-
mismatch library, Metric 2 calibration, A/B/C smoke harness), and renumber all four tasks under the
t0009-t0012 range.

## Approach

Inline brainstorm. Aggregate state, present 27 uncovered suggestions, identify the schema gap
exposed during prompt-modelling discussion, propose four parallel-capable tasks with the smoke
harness gated on the other three. Defer Round 2 suggestion cleanup to keep this session focused.

## Cost Estimation

USD 0. Pure planning task; no API or compute spend.

## Step by Step

1. Review project state (7 completed tasks, 27 uncovered suggestions, $0.06 / $100 spent).
2. Read full descriptions of high-priority suggestions; reassess priorities.
3. Propose three-task wave 3 (matched-mismatch + Metric 2 + smoke harness).
4. Discover v2 schema gap during prompt-modelling discussion of the `is_bored` row.
5. Insert t0009 (v2 re-annotation) ASAP; renumber the original three tasks to t0010-t0012.
6. Receive researcher confirmation: "confirm".
7. Create four child task folders.
8. Run verificators, commit, push, PR, merge.
9. After merge, fork three parallel `/execute-task` background agents for t0009/t0010/t0011.
10. t0012 stays not_started; spawn its agent only after t0009, t0010, t0011 all merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm tasks produce no assets.

## Time Estimation

Inline session under one hour of researcher time.

## Risks & Fallbacks

Risk: t0009 v2 re-annotation produces a lower judge accept rate than v1's 33%. Fallback: the smoke
harness can fall back to the v1 dataset with a documented schema-walk compromise; v2 quality
remediation becomes a follow-up task.

Risk: t0012's N=28 is too small to detect the predicted ~5pp A-vs-B effect. Fallback: report the
directional signal and effect-size confidence intervals; the multi-provider replication and
benchmark expansion are already queued as follow-up tasks for the next brainstorm.

## Verification Criteria

* `verify_task_file` passes for the brainstorm task and all four child tasks.
* `verify_logs` passes with at most the documented LG-W005 / LG-W007 / LG-W008 warnings.
* `verify_corrections` and `verify_suggestions` pass (both files are empty).
