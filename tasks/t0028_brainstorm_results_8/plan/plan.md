# Plan: Brainstorm Session 8

## Objective

Schedule a minimum viable wave to close RQ1 and RQ4 within the $66.54 remaining budget, following
t0027's underpowered McNemar verdict (p=1.0 on 12 discordant pairs). Defer RQ2, RQ3, and RQ5 closure
tasks to a later session to preserve budget for an unexpected overrun.

## Approach

1. Aggregate project state (tasks, suggestions, costs, answers).
2. Read results summaries for t0025, t0026, t0027 (the three tasks completed since t0024).
3. Form an independent priority reassessment for every active HIGH suggestion in light of t0027's
   runtime ABC findings.
4. Present project state with per-RQ blocker and cost analysis.
5. Discuss with the researcher; converge on the minimum viable wave (TaskA + TaskE) that closes RQ1
   (with caveat) and RQ4 within a hard $35 cap.
6. Create the brainstorm-results task folder.
7. Apply decisions: write 8 correction files (2 rejections, 6 reprioritizations), create t0029
   (TaskA) and t0030 (TaskE) via `/create-task`.
8. Finalize: write step logs, results files, run verificators, push, PR, merge.

## Cost Estimation

$0 — purely a planning session. No API or compute spend.

## Step by Step

* Step 1 (review-project-state): run aggregators, read t0025-t0027 results summaries, materialize
  overview.
* Step 2 (discuss-decisions): present candidate task wave A-E with per-RQ cost mapping; converge on
  TaskA + TaskE only with hard $35 cap and explicit guardrail against in-wave replacements.
* Step 3 (apply-decisions): write 8 correction files; create t0029 and t0030 task scaffolds.
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

* Risk: t0029 hits the $35 cap before reaching 30 discordant pairs. Mitigation: explicit abort rule
  documented in t0029's task description; partial verdict reported with power caveat; no in-wave
  replacement tasks.
* Risk: child-task creation fails verification. Fallback: fix verification errors and re-run
  `/create-task` for the failing task.
* Risk: pre-merge verificator fails. Fallback: address the specific error code surfaced and retry.

## Verification Criteria

* All 8 correction files pass `verify_corrections t0028_brainstorm_results_8`.
* t0029 and t0030 task folders pass `verify_task_file`.
* `verify_logs t0028_brainstorm_results_8` passes for all four step folders.
* Pre-merge verificator passes.
