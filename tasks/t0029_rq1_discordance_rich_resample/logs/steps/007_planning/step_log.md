---
spec_version: "3"
task_id: "t0029_rq1_discordance_rich_resample"
step_number: 7
step_name: "planning"
status: "completed"
started_at: "2026-05-03T10:14:19Z"
completed_at: "2026-05-03T10:21:00Z"
---
## Summary

Pre-registered the t0029 paired resample plan in `plan/plan.md`: a discordance-rich McNemar
exact-binomial test of arm A (Plan-and-Solve baseline) vs arm B (scope-aware ReAct) on
claude-sonnet-4-6, with a hard cumulative-cost cap of $35.00, a stratified frontsci → taubench →
SWE-bench sampling order seeded at 20260503, and an explicit partial-verdict escape hatch when the
cap binds before 30 discordant pairs accumulate. The plan resolves the t0027 ↔ t0028
variant-labeling inversion by adopting the task description's naming (arm_a = baseline, arm_b =
scope-aware) throughout new code and isolating the inversion to a single `load_t0027_paired.py`
shim.

## Actions Taken

1. Ran prestep to mark planning in_progress and create the step folder.
2. Read `arf/specifications/plan_specification.md` to confirm required frontmatter and section
   layout.
3. Wrote `plan/plan.md` with all 11 mandatory sections (Objective, Task Requirement Checklist,
   Approach, Cost Estimation, Step by Step, Remote Machines, Assets Needed, Expected Assets, Time
   Estimation, Risks & Fallbacks, Verification Criteria) plus a pinned Variant-Label Inversion note.
4. Encoded 12 REQ items (REQ-1..REQ-12) traceable to numbered Step by Step entries; marked steps 1,
   5, 8, 9 as `[CRITICAL]`.
5. Documented the cumulative-cost guardrail (`CUMULATIVE_TASK_CAP_USD = 35.00`, `BATCH_SIZE = 8`,
   `DISCORDANCE_TARGET = 30`, `T0029_SEED = 20260503`) and the worst-case ~$1.28 cap-overshoot bound
   from between-batch checking.
6. Ran flowmark on `plan/plan.md` and re-ran `verify_plan.py`; the plan passes with one expected
   PL-W009 warning (`costs.json` is referenced because the partial-verdict path requires the harness
   to live-update it, not just the orchestrator).
7. Recorded the variant-labeling decision: use t0028 task-description naming in all new outputs and
   confine the t0027 inversion to `load_t0027_paired.py`.

## Outputs

* `tasks/t0029_rq1_discordance_rich_resample/plan/plan.md`
* `tasks/t0029_rq1_discordance_rich_resample/logs/steps/007_planning/step_log.md`
* `tasks/t0029_rq1_discordance_rich_resample/logs/commands/004_20260503T101717Z_uv-run-flowmark.*`

## Issues

PL-W009 warning is accepted as non-blocking. `results/costs.json` is referenced in Step by Step
because the live cumulative-cost guardrail and the partial-verdict abort rule require the harness
itself to write to that file between batches; the orchestrator-managed final write is layered on
top. No errors.
