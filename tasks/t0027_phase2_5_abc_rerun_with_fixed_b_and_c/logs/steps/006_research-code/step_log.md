---
spec_version: "3"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-02T17:11:02Z"
completed_at: "2026-05-02T17:13:30Z"
---
## Summary

Surveyed the three dependency tasks (t0007 v1, t0010 matched-mismatch, t0021 v2 confidence layer,
and t0026 A/B/C harness) to identify the exact entry points, file/line locations, dispatch sites,
and trajectory shapes that t0027 must preserve. The most important finding: `MalformedPlanError`
lives in t0007's `parse_plan` (called from `PlanAndSolveAgent.run` at `planandsolve.py:281-282`),
not in t0021's confidence layer — so the v3 fork must override the planning step in t0007 logic, not
in t0021.

## Actions Taken

1. Spawned an Explore subagent with a 600-word cap to survey
   `tasks/t0010_matched_mismatch_library/`, `tasks/t0021_plan_and_solve_v2_with_final_confidence/`,
   and `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/`, asking for entry points, dispatch sites,
   trajectory shapes, McNemar and calibration entry points, and the 130-paired filter.
2. Read `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py:160-292` to confirm
   `MalformedPlanError` lives in v1 and the planner has no retry path.
3. Wrote `research/research_code.md` covering Objective, Background, Methodology Review (per task),
   Key Findings, Recommended Approach (4-step fork plan with cost estimate), and a References list
   of all relevant file/line anchors.

## Outputs

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/research/research_code.md`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered.
