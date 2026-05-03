---
spec_version: "3"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-03T11:28:37Z"
completed_at: "2026-05-03T11:43:00Z"
---
## Summary

Implemented eight Python modules in `code/` (paths, constants, stats_helpers, load_paired_outputs,
analysis_rq4_stratification, analysis_rq1_power, analysis_log_audit, build_report). Ran the four
analyses on local CPU with no API calls and produced three JSON tables in `results/data/`, three PNG
charts in `results/images/`, and the six standard `results/` deliverables. Re-derived the
discordance rate (12/130 = 0.0923) from the loaded paired DataFrame; computed expected discordant N
at the t0029 \$35 cap (32) and the McNemar power grid over conditional B-wins ∈ {0.55..0.80}.

## Actions Taken

1. Spawned an Implementation subagent with the full plan + research context, instructing it to write
   the eight modules, run them via `run_with_logs.py`, run ruff/mypy, and verify outputs.
2. Subagent loaded the three JSONL prediction files, applied the single
   `variant_a → arm_b, variant_b → arm_a, variant_c → arm_c` inversion in `load_paired_outputs.py`,
   and asserted `n_total == 130` and the documented per-subset counts (swebench=20, frontsci=26,
   taubench=84).
3. RQ4 stratification: built per-subset and ALL 2x2 contingency tables (`both_pass`, `a_only`,
   `b_only`, `both_fail`) with Wilson 95% CIs and McNemar exact-binomial p-values. Saved to
   `results/data/rq4_stratification.json` and rendered
   `results/images/rq4_stratification_heatmap.png`.
4. RQ1 power: computed `new_pairs_at_cap = floor(35.00/0.16) = 218`, total N at cap = 348, expected
   discordant at cap = 32, and the power grid (0.55→0.082, 0.60→0.205, 0.65→0.405, 0.70→0.644,
   0.75→0.846, 0.80→0.959). Saved to `results/data/rq1_power_grid.json` and rendered
   `results/images/rq1_power_curve.png`.
5. Log audit: parsed t0026 hard-failure aggregates (A=13, B=40 incl. 16 MalformedPlanError, C=44),
   counted t0027 parser-recovery paths post-inversion, and split rows into infrastructure vs genuine
   model-failure layers. Saved to `results/data/log_audit.json` and rendered
   `results/images/log_audit_failure_breakdown.png`.
6. Built the report: `results/results_summary.md` (first line exactly
   `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`), `results/results_detailed.md`
   with all three charts embedded, and the four standard JSON deliverables.
7. Quality gates: `ruff check --fix`, `ruff format`, and
   `mypy -p tasks.t0031_rq1_rq4_no_new_api_salvage.code` all clean. Markdown formatted with
   `flowmark`.

## Outputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/code/{paths,constants,stats_helpers,load_paired_outputs, analysis_rq4_stratification,analysis_rq1_power,analysis_log_audit,build_report}.py`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/{rq4_stratification,rq1_power_grid, log_audit}.json`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/images/{rq4_stratification_heatmap, rq1_power_curve,log_audit_failure_breakdown}.png`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/{results_summary,results_detailed}.md`
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/{metrics,costs,remote_machines_used, suggestions}.json`

## Issues

Three minor issues were resolved during implementation:

1. variant_a JSONL from t0026 has 147 rows but only 130 unique `instance_id`s; the load helper
   asserts duplicate rows have identical `judge_sonnet_success` before keeping the first occurrence.
2. scipy is not in the project dependency set; Wilson CI and binomial pmf/sf were implemented in
   closed form using `math.comb` rather than adding a new dependency.
3. arm_b (from variant_a / t0026) lacks `plan_parser_recovery_path` by construction (scope-aware
   ReAct has no plan parser); the audit reports arm_b infra=0, genuine=124, and documents this
   constraint in the Limitations section of `results_detailed.md`.
