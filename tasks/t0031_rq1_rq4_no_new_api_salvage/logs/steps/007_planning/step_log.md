---
spec_version: "3"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
step_number: 7
step_name: "planning"
status: "completed"
started_at: "2026-05-03T11:25:15Z"
completed_at: "2026-05-03T11:26:30Z"
---
## Summary

Wrote `plan/plan.md` describing the four bounded no-new-API analyses (RQ4 stratification, RQ1
power/futility, infrastructure-vs-genuine-failure audit, short report), the load helper that owns
the single `variant → arm` inversion, the seven code files that implement everything, the local-CPU
runtime ($0.00 budget, no remote machines), and the explicit verification criteria (headline label,
three PNG charts, re-derived discordance count).

## Actions Taken

1. Ran `prestep` for `planning` to mark the step in_progress.
2. Drafted `plan/plan.md` with all 11 mandatory sections (Objective, Approach, Cost Estimation, Step
   by Step, Remote Machines, Assets Needed, Expected Assets, Time Estimation, Risks & Fallbacks,
   Verification Criteria) tied to concrete files and the t0029 power-analysis parameters.

## Outputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/plan/plan.md`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/logs/steps/007_planning/step_log.md`

## Issues

No issues encountered. The plan declares `expected_assets: {}`, which will produce one TF-W005
warning at the task-level verification stage; this is expected for an analysis-only task.
