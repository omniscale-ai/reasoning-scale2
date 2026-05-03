---
spec_version: "3"
task_id: "t0032_no_anthropic_rq1_path_decision"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-03T13:28:29Z"
completed_at: "2026-05-03T13:55:00Z"
---
## Summary

Inventoried existing on-disk outputs from `t0026`, `t0027`, and `t0031` that the four-option
decision rests on. Confirmed via `aggregate_libraries.py` that all 9 project libraries are
agent-side and **zero** are relevant to this analysis-only task. Catalogued the three reusable JSON
sidecars in `t0031/results/data/` (`rq1_power_grid.json`, `rq4_stratification.json`,
`log_audit.json`) plus the two `costs.json` files in `t0026` and `t0027` as the canonical numeric
inputs to the option (a)/(b)/(c)/(d) comparison table.

## Actions Taken

1. Read `tasks/t0027/results/results_summary.md`, `tasks/t0031/results/results_summary.md`, and the
   three `tasks/t0031/results/data/*.json` sidecars to recover the discordance numbers (12/130 =
   9.23%, symmetric 6/6 split, McNemar p=1.0000), the RQ1 power grid (power crosses 80% only at p1 ≥
   0.75), and the per-stratum cells (SWE-bench p=0.0312, FrontierScience p=0.0625, Tau-bench
   dominated by both-fail).
2. Read `tasks/t0026/results/costs.json` and `tasks/t0027/results/costs.json` to confirm the
   per-instance cost shape on Claude Sonnet 4.6 (about $0.0344 / $0.0727 / $0.0718 per instance for
   arms A / B / C respectively).
3. Wrote `tasks/t0032.../research/research_code.md` with all six required sections (Task Objective,
   Library Landscape, Key Findings, Reusable Code and Assets, Lessons Learned, Recommendations, Task
   Index covering t0026, t0027, t0028, t0029, t0031).
4. Corrected the t0026 / t0028 / t0029 task-folder slugs after an initial verificator run flagged
   three RC-W002 warnings against folder names that did not exist on disk (the actual slugs are
   `t0026_phase2_abc_runtime_n147_for_rq1_rq5`, `t0028_brainstorm_results_8`, and
   `t0029_rq1_discordance_rich_resample`). Reattributed the arm-labelling anchor from t0028 (which
   is the brainstorm-results task) to t0027 (which actually fixed the convention via
   `plan_and_solve_v3` and `matched_mismatch_v2`).
5. Ran flowmark on the file and re-ran `verify_research_code`; final result is **PASSED with 0
   errors and 0 warnings**.

## Outputs

* `tasks/t0032_no_anthropic_rq1_path_decision/research/research_code.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/logs/steps/006_research-code/step_log.md`

## Issues

The first verificator pass returned 0 errors but 3 RC-W002 warnings because the Task Index entries
referenced task-folder names that did not exist on disk. The folders actually exist under different
slugs (t0026 was `t0026_phase2_abc_runtime_n147_for_rq1_rq5`, not `..._paired_real_runs_full`; t0028
is `t0028_brainstorm_results_8`, not `..._phase2_75_abc_runtime_n147_rq1_rq5`; t0029 is
`t0029_rq1_discordance_rich_resample`, not `..._phase2_6_abc_more_pairs`). Fixed by editing the Task
Index entries and the inline path reference in the Reusable Code and Assets section, plus correcting
the upstream Lessons Learned and Recommendations bullets that incorrectly attributed the
arm-labelling fix to t0028 (the brainstorm task) rather than t0027 (where the policy under each arm
label was actually pinned).
