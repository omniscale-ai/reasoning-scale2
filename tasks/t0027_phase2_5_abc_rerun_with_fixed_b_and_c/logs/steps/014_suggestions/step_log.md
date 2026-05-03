---
spec_version: "3"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-03T08:04:37Z"
completed_at: "2026-05-03T08:06:06Z"
---
## Summary

Wrote `results/suggestions.json` with six follow-up suggestions for downstream tasks. The
suggestions focus on what t0027 itself surfaced rather than restating still-open t0026 ones: a
content-driven calibrator over v3 features (S-0027-01), a structurally distinct adversarial behavior
for matched_mismatch beyond mere v3 delegation (S-0027-02), an identity-plan ablation to isolate
planner contribution (S-0027-03), unconditional recovery_path telemetry (S-0027-04), a
discordance-rich paired sample to gain McNemar power (S-0027-05), and promotion of bounded recovery
into every other library scaffold (S-0027-06).

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` for the v2 schema.
2. Inspected `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/suggestions.json` to
   understand the prior open suggestion set (S-0026-01 through S-0026-06) and avoid duplication.
3. Listed `meta/categories/` to pick valid category slugs for each new suggestion.
4. Wrote six suggestions covering calibration (1 high), wrapper redesign (1 high), planner ablation
   (1 medium), telemetry instrumentation (1 medium), discordance-rich sampling (1 medium), and
   library refactor (1 low).
5. Ran `flowmark` on this step log.

## Outputs

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/suggestions.json`

## Issues

No issues encountered.
