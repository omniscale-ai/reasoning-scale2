---
spec_version: "3"
task_id: "t0014_v2_annotator_sonnet_rerun"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-04-30T23:32:00Z"
completed_at: "2026-04-30T23:40:00Z"
---
# Step 12: results

## Summary

Wrote the five mandatory results files: `results_summary.md`, `results_detailed.md`, `metrics.json`,
`costs.json`, and `remote_machines_used.json`. Embedded the three charts produced in step 9
(`three_way_accept_rate.png`, `aggregate_decomposition.png`, `v2_sonnet_atomics_distribution.png`)
into `results_detailed.md`. Reported the three-way decomposition (+57 pp schema-only, -1 pp
model-only, +58 pp headline) with Wilson 95% CIs on every cell.

## Actions Taken

1. Wrote `results/metrics.json` with a single registered metric (`avg_decisions_per_task = 12.16`),
   matching `meta/metrics/avg_decisions_per_task/description.json` (unit "count", value_type
   "float"). The same metric was reported by t0009 at 16.38; v2-sonnet drops to 12.16 because sonnet
   emits noticeably terser hierarchies.
2. Wrote `results/costs.json` with `total_cost_usd = 21.1632` (annotator $19.7667 + judge $1.3965)
   and an explanatory note crediting the user-authorised cap raise from $10 to $25 (intervention
   `budget_cap_raised.md`). The note also flags that 96 of 115 sonnet calls succeeded; 14
   call-failures (3 unique FS row indices retried) and 1 parse-failure were logged. This closes the
   intervention's "costs.json final total recorded" precondition.
3. Wrote `results/remote_machines_used.json` as `[]` — no remote compute was used.
4. Wrote `results/results_summary.md` (spec_version "2") with sections Summary / Metrics /
   Verification. Headline metrics: aggregate v2-sonnet accept rate 90% (18/20) [69.9%, 97.2%];
   schema-only +57 pp; model-only -1 pp; headline +58 pp matches t0009 exactly.
5. Wrote `results/results_detailed.md` (spec_version "2") with all mandatory sections plus the final
   `## Task Requirement Coverage` mirroring `plan/plan.md` REQ-1..REQ-11. Embedded the three step-9
   PNGs via `![desc](images/file.png)` syntax. Answered the four key questions from
   `task_description.md` in the requirement-coverage section.
6. Will run `flowmark --inplace --nobackup` on the new markdown files in the next quality gate.

## Outputs

* `tasks/t0014_v2_annotator_sonnet_rerun/results/results_summary.md`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/results_detailed.md`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/metrics.json`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/costs.json`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/remote_machines_used.json`

## Issues

None. Charts already produced in step 9; results writeup just embeds them.
