# Plan: Brainstorm Session 6

## Objective

Run an interactive brainstorming session to translate t0017 findings and t0014 deconfound into a
concrete experimental slate that delivers paper-quality results on the project research questions as
quickly as possible.

## Approach

1. Aggregate project state (tasks, suggestions, costs, answers).
2. Form an independent priority reassessment for every active suggestion.
3. Present project state to the researcher.
4. Discuss new tasks, suggestion cleanup, and confirm.
5. Create the brainstorm-results task folder.
6. Apply decisions: write correction files for reprioritizations and rejections, then create new
   task folders via `/create-task`.
7. Finalize: write step logs, results files, run verificators, PR, merge.

## Cost Estimation

$0 — purely a planning session. No API or compute spend.

## Step by Step

* Step 1 (review-project-state): run aggregators, read recent results summaries, materialize
  overview.
* Step 2 (discuss-decisions): three rounds with the researcher (new tasks, cleanup, confirm).
* Step 3 (apply-decisions): write 6 correction files; create t0019-t0023 task folders.
* Step 4 (finalize): step logs, results, verificators, push, PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None — brainstorm tasks produce no assets, only correction files and child task folders.

## Time Estimation

~1.5 hours of researcher dialogue + execution.

## Risks & Fallbacks

* Risk: child-task creation fails verification. Fallback: fix verification errors and re-run
  `/create-task` for the affected task.
* Risk: pre-merge verificator fails. Fallback: address the specific error code surfaced and retry
  the merge.

## Verification Criteria

* All 6 correction files pass `verify_corrections t0018_brainstorm_results_6`.
* Each new task folder passes `verify_task_file`.
* `verify_logs t0018_brainstorm_results_6` passes for all four step folders.
* Pre-merge verificator passes.
