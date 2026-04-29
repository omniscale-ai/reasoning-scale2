# Plan: Brainstorm Session 2

## Objective

Translate completed-task results into the next wave of tasks. Specifically: schedule the deferred T3
annotation pilot in v1 form, plus the two baseline libraries that Phase 2 needs.

## Approach

Inline brainstorm. Aggregate state from `aggregate_tasks`, `aggregate_suggestions`,
`aggregate_costs`. Reassess priorities against actual t0002 / t0003 findings. Propose three
parallel-safe tasks. Skip Round 2 suggestion cleanup; defer to a follow-up session.

## Cost Estimation

USD 0. Pure planning task; no API or compute spend.

## Step by Step

1. Review project state (3 completed tasks, 15 uncovered suggestions, $0 / $100 spent).
2. Reassess suggestion priorities; identify duplicates (S-0003-01 ≈ S-0002-04, S-0003-02 ≈
   S-0002-03) but defer cleanup.
3. Propose t0005 / t0006 / t0007 with rationale.
4. Receive researcher confirmation: "run round 1 using fork as you did earlier".
5. Create child task folders with `task.json` and `task_description.md`.
6. Run verificators, commit, push, PR, merge.
7. After merge, fork three parallel `/execute-task` background agents.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm tasks produce no assets.

## Time Estimation

Inline session, under one hour of researcher time.

## Risks & Fallbacks

Risk: t0005 / t0006 / t0007 turn out to be misaligned after deeper inspection. Fallback: future
brainstorm sessions can cancel `not_started` tasks via `task.json` edits or correction files.

## Verification Criteria

* `verify_task_file` passes for the brainstorm task and three child tasks.
* `verify_logs` passes with at most the documented LG-W005 / LG-W007 / LG-W008 warnings.
* `verify_corrections` and `verify_suggestions` pass (both files are empty).
