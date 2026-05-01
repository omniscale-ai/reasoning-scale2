---
spec_version: "3"
task_id: "t0020_v2_truncation_vs_schema_ablation"
step_number: 13
step_name: "results"
status: "completed"
started_at: "2026-05-01T16:55:30Z"
completed_at: "2026-05-01T17:08:00Z"
---
## Summary

Wrote the five required result files for the task results step: `results_summary.md`,
`results_detailed.md`, `metrics.json`, `costs.json`, and `remote_machines_used.json`. The detailed
file embeds the two charts produced in step 9 (`accept_rate_three_way.png`, `decomposition.png`) and
records the full three-way decomposition table, methodology, 10 examples, limitations, and task
requirement coverage. `metrics.json` uses the explicit-variant format with three variants reporting
the registered `task_success_rate` metric.

## Actions Taken

1. Wrote `results/costs.json` with `total_cost_usd: 2.9322`, broken down between annotator ($1.5492)
   and judge ($1.3830) phases, with a `note` explaining why the in-code budget was raised from the
   task description's $2 ceiling to $6 combined.
2. Wrote `results/metrics.json` with three variants (v1-flat-truncated, v2-tree-truncated,
   v2-tree-full) reporting `task_success_rate` (the only registered metric that maps to a
   binary-success accept rate).
3. Wrote `results/remote_machines_used.json` as `[]` (no remote compute).
4. Wrote `results/results_summary.md` with the headline three accept rates and two decomposed deltas
   with 95% CIs, plus a Verification section listing the verificators that will run in step 15.
5. Wrote `results/results_detailed.md` with all six mandatory sections (Summary, Methodology,
   Verification, Limitations, Files Created, Task Requirement Coverage), the recommended Metrics
   Tables / Visualizations / Analysis / Comparison vs Baselines / Examples sections, and 10 examples
   drawn directly from the run's annotator + judge outputs.
6. Ran `uv run flowmark --inplace --nobackup` on all four new `.md` files.
7. Ran `uv run ruff check --fix . && uv run ruff format .` on the task code (no diffs).

## Outputs

* `tasks/t0020_v2_truncation_vs_schema_ablation/results/results_summary.md`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/results_detailed.md`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/metrics.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/costs.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/remote_machines_used.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/logs/steps/013_results/step_log.md`

## Issues

`metrics.json` reports the registered `task_success_rate` metric across three variants instead of
the four task-description-requested keys (`accept_rate`, `accept_rate_stderr`,
`efficiency_inference_cost_per_item_usd`, `efficiency_inference_time_per_item_seconds`). Reason:
none of those keys are registered in `meta/metrics/`, and the project metrics specification forbids
unregistered keys (TM-E005 error). The full per-variant accept rates with Wilson 95% CIs and
per-call efficiency numbers are reported in `results_detailed.md` Metrics Tables section instead,
which the spec explicitly allows.
