---
spec_version: "3"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-01T15:53:04Z"
completed_at: "2026-05-01T20:25:00Z"
---
## Summary

Wrote the four mandatory result artifacts for task t0022: `results_summary.md` (scannable summary
with 8 metric bullets and 5 verificator lines), `results_detailed.md` (spec_version 2 with full
methodology, per-condition error tables, REQ-1 through REQ-13 coverage table), `metrics.json` (empty
`{}` because no project-registered metric keys match this library task's outputs), and `costs.json`
(total $2.4172 with breakdown by judge type and a `note` documenting the $0.42 overshoot root cause
and mitigation). Added `remote_machines_used.json` (empty array). Both `verify_task_results.py` and
`verify_task_metrics.py` pass with zero errors and zero warnings.

## Actions Taken

1. Read `arf/specifications/task_results_specification.md` (v8) and the plan REQ-1..REQ-13 to anchor
   the Task Requirement Coverage section.
2. Created `results/metrics.json` as `{}` per the spec rule that empty is valid for tasks with no
   registered metrics matching their outputs.
3. Created `results/costs.json` with `total_cost_usd: 2.4172`, breakdown by progress-rate and
   error-taxonomy judge calls, `services.anthropic_api: 2.4172`, `budget_limit: 2.0`, and a `note`
   field that names the headroom misconfiguration as root cause and the headroom-bump-plus-prior-
   spend correction as the mitigation.
4. Created `results/results_summary.md` with `## Summary`, `## Metrics` (8 numbered bullets: PR mean
   0.103, PR stddev 0.228, A-vs-C separation 0.771, FrontierScience 26 envs, SWE-bench 60 envs,
   26/26 unit tests, $2.4172 total cost), and `## Verification` (5 verificator lines).
5. Created `results/results_detailed.md` (spec_version "2") with `## Summary`, `## Methodology`
   (machine, runtime, methods, subgoal coverage), `## Metrics Tables` (PR distribution, per-
   condition error distribution, library coverage), `## Verification`, `## Limitations` (5 numbered
   items), `## Files Created`, and `## Task Requirement Coverage` (final `##` section, 13 rows for
   REQ-1..REQ-13: 12 Done, 1 Partial).
6. Created `results/remote_machines_used.json` as `[]` (no remote machines used).
7. Ran `uv run flowmark --inplace --nobackup` on both result `.md` files; flowmark normalized table
   separators and reflowed long lines.
8. Ran `verify_task_results.py` and `verify_task_metrics.py` via `run_with_logs.py`; both pass with
   zero errors and zero warnings.

## Outputs

* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/results_summary.md`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/results_detailed.md`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/metrics.json`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/costs.json`
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/remote_machines_used.json`

## Issues

REQ-13 ($2 cost cap) is marked **Partial** rather than **Done** because total spend was $2.4172
(over by $0.42). Documented in detail in `costs.json` `note` and in the Limitations section of
`results_detailed.md`. Root cause and mitigation are recorded so t0023 inherits the fix.
