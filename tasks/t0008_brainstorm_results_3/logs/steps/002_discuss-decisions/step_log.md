---
spec_version: "3"
task_id: "t0008_brainstorm_results_3"
step_number: 2
step_name: "discuss-decisions"
status: "completed"
started_at: "2026-04-30T00:00:00Z"
completed_at: "2026-04-30T00:00:00Z"
---
## Summary

Initial Round 1 proposal was three tasks (matched-mismatch, Metric 2, smoke harness on v1 data).
While modelling A/C prompts on the `is_bored` row, the v1 schema gap (no subtask-to-atomic edge) was
discovered, prompting the researcher to insert t0009 v2 re-annotation as the new ASAP task.

## Actions Taken

1. Drafted the original three-task wave 3 proposal (matched-mismatch + Metric 2 + smoke harness)
   with cost, dependencies, and source-suggestion mapping.
2. Modelled the A and C condition prompts on `he_HumanEval_91` to demonstrate the granularity-
   tagging approach concretely.
3. Identified the schema gap when explaining the granularity-injection ordering to the researcher.
4. Inserted t0009 (v2 tree-schema re-annotation) as the new ASAP task; renumbered the original three
   tasks to t0010-t0012; gated t0012 on all three.
5. Recorded researcher confirmation ("confirm") and the explicit deferral of Round 2 cleanup.

## Outputs

None. Discussion step; outputs land in step 003 (apply-decisions).

## Issues

No issues encountered.
