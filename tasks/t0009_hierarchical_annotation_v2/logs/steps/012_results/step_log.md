---
spec_version: "3"
task_id: "t0009_hierarchical_annotation_v2"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-30T00:43:34Z"
completed_at: "2026-04-30T00:55:00Z"
---
# Step 12: results

## Summary

Wrote all results documents (`results_summary.md`, `results_detailed.md`, `examples_full.md`,
`metrics.json`, `costs.json`, `remote_machines_used.json`) and generated the two required charts
(`v1_vs_v2_accept_rate.png`, `v2_atomics_distribution.png`). Both `verify_task_results` and
`verify_task_metrics` pass with no errors or warnings.

## Actions Taken

1. Wrote `results/metrics.json` with the registered `avg_decisions_per_task = 16.38` metric.
2. Wrote `results/costs.json` (total $9.10) and `results/remote_machines_used.json` (`[]`).
3. Wrote `code/make_charts.py` and generated the two PNG charts under `results/images/`.
4. Wrote `results_summary.md` with the three mandatory sections.
5. Wrote `results_detailed.md` with all mandatory sections (Summary, Methodology, Metrics Tables,
   Comparison vs Baselines, Visualizations, Examples, Analysis, Plan Assumption Check, Limitations,
   Verification, Files Created, Task Requirement Coverage).
6. Wrote `results/examples_full.md` with 10 verbatim annotation examples (full input prompts + full
   output JSON) covering 2-3 rows per benchmark plus the 2 needs-revision rows.
7. Ran `verify_task_results` and `verify_task_metrics`: both PASSED with no errors or warnings.

## Outputs

- `tasks/t0009_hierarchical_annotation_v2/results/results_summary.md`
- `tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md`
- `tasks/t0009_hierarchical_annotation_v2/results/examples_full.md`
- `tasks/t0009_hierarchical_annotation_v2/results/metrics.json`
- `tasks/t0009_hierarchical_annotation_v2/results/costs.json`
- `tasks/t0009_hierarchical_annotation_v2/results/remote_machines_used.json`
- `tasks/t0009_hierarchical_annotation_v2/results/images/v1_vs_v2_accept_rate.png`
- `tasks/t0009_hierarchical_annotation_v2/results/images/v2_atomics_distribution.png`
- `tasks/t0009_hierarchical_annotation_v2/code/make_charts.py`

## Issues

No issues encountered. The plan-vs-actual cost discrepancy ($2 estimate vs $9.10 actual) is
documented prominently in `results_detailed.md` `## Plan Assumption Check`.
