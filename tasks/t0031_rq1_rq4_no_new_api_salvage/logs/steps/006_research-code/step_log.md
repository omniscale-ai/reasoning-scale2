---
spec_version: "3"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-03T11:20:13Z"
completed_at: "2026-05-03T11:21:30Z"
---
## Summary

Inventoried the existing local outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c` so that the four bounded no-new-API analyses can load
only from on-disk artifacts. Located the 130-row paired predictions JSONL files, the paired
manifest, the per-row `plan_parser_recovery_path` field used for the audit, and the t0026
hard-failure aggregates. Resolved the variant-labelling reconciliation between t0027's internal
convention and t0028's reporting convention.

## Actions Taken

1. Spawned an Explore subagent to walk t0026/t0027 output trees and report concrete file paths,
   schemas, and aggregate counts.
2. Verified the variant-labelling claim directly via `Grep` on `tasks/t0027_*/plan/plan.md` and
   `tasks/t0031_*/task_description.md` — confirmed t0027 internal `variant_a = scope-aware ReAct`
   vs. t0031 reporting `arm A = Plan-and-Solve baseline`, so the load helper must invert
   `variant_a → arm_b` and `variant_b → arm_a`.
3. Wrote `research/research_code.md` capturing canonical paths, schemas, audit signal sources, the
   load-helper recipe, and the t0029 power-analysis parameters ($35 cap, ~$0.16/pair, 30-discordant
   target, sampling order).

## Outputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/research/research_code.md`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered.
