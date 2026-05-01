---
spec_version: "3"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-01T14:07:07Z"
completed_at: "2026-05-01T14:38:10Z"
---
## Summary

Surveyed prior task code and registered libraries to identify the assets the v2 Plan-and-Solve
library must extend, the trajectory schema callers depend on, and the smoke harness wiring that
consumed the v1 library. Six tasks were reviewed and cited: t0006 (ReAct, Condition A), t0007
(Plan-and-Solve v1, Condition B base), t0009 (FrontierScience-Olympiad dataset), t0010
(matched-mismatch v1, Condition C), t0011 (Metric 2 calibration), and t0012 (ABC smoke harness on
FrontierScience-Olympiad). Two registered libraries were identified as relevant: scope-unaware
Plan-and-Solve v1 and matched-mismatch v1. Confirmed that the v1 trajectory has a per-step
`confidence` slot that v1 never fills, that the t0012 harness already has a top-level
`final_confidence: null` slot ready to receive v2 output, and that t0012's Metric 2 collapsed to 0.0
for B and C because of the missing field. Recorded recommendations for the v2 design (compose v1,
add a single post-call confidence elicitation, register a new library, copy non-library helpers into
the task).

## Actions Taken

1. Read `task.json`, `task_description.md`, and the canonical research-code specification.
2. Read v1 source `tasks/t0007_*/code/planandsolve.py`, the t0012 harness and model-call wrapper,
   the t0011 calibration module, and the t0010 matched-mismatch library.
3. Examined a t0012 prediction JSONL row to confirm the `final_confidence: null` gap.
4. Wrote `research/research_code.md` with YAML frontmatter and the seven canonical sections (Task
   Objective, Library Landscape, Key Findings, Reusable Code and Assets, Lessons Learned,
   Recommendations for This Task, Task Index).
5. Ran `flowmark` and `verify_research_code` until both reported zero errors and zero warnings.

## Outputs

* `tasks/t0021_plan_and_solve_v2_with_final_confidence/research/research_code.md`
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/logs/steps/006_research-code/step_log.md`

## Issues

Initial draft was missing the YAML frontmatter and used non-canonical section names; fixed by
rewriting the file to the canonical structure. One transient `RC-W002` warning about a wrong t0006
task ID (`t0006_chain_of_thought_baseline` vs the actual `t0006_scope_aware_react_library`) was
fixed by looking up the correct ID via `aggregate_tasks --format ids`.
