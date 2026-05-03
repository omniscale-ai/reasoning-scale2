---
spec_version: "3"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
step_number: 13
step_name: "results"
status: "completed"
started_at: "2026-05-03T11:44:17Z"
completed_at: "2026-05-03T11:45:30Z"
---
## Summary

Finalized the result deliverables emitted by `code/build_report.py` and brought them into compliance
with `arf/specifications/task_results_specification.md`. Restructured `results_summary.md` to
include the three mandatory `## Summary`, `## Metrics`, `## Verification` sections while preserving
the mandatory first-line headline label. Cleaned `metrics.json` to scalar-only snake_case keys. The
task-results verificator now passes with zero errors.

## Actions Taken

1. Ran `verify_task_results.py`; received four errors (3× missing mandatory section in
   `results_summary.md`, 1× non-scalar `_derived` value in `metrics.json`) plus three warnings
   (snake_case + experiment-type Examples).
2. Rewrote `results_summary.md` so that line 1 is exactly the mandated headline label, then a `#`
   document title, then the three mandatory sections (`## Summary`, `## Metrics`, `## Verification`)
   plus a `## Limitations` section. Re-derived numbers (discordance, power grid, audit) are listed
   as bold quantitative bullet points in `## Metrics`.
3. Rewrote `metrics.json` to keep only the registered metric keys (`task_success_rate`,
   `overconfident_error_rate`, `avg_decisions_per_task`, all null) plus snake_case scalar
   derived-quantity keys (`discordance_rate_t0027`, `expected_discordant_n_at_cap`,
   `new_pairs_admitted_at_cap`, `power_at_p1_0_55` … `power_at_p1_0_80`).
4. Re-ran `flowmark` and `verify_task_results.py` — verificator now reports 0 errors and 1
   non-blocking warning (TR-W013, experiment-type `## Examples` section is missing; this is a
   data-analysis task and produces no per-instance examples beyond the embedded charts).

## Outputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md` (rewritten)
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/metrics.json` (rewritten)

## Issues

One non-blocking warning remains:
`TR-W013 results_detailed.md is missing ## Examples section (mandatory for experiment-type tasks)`.
This task is `data-analysis`, not `experiment`; the verificator emits this warning unconditionally.
The required experiment-style content (charts, contingency tables, power grid) is already embedded
in `results_detailed.md` via the three PNGs and inline tables. No further action.
