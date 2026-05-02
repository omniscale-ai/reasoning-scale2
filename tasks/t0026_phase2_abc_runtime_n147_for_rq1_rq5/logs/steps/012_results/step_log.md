---
spec_version: "3"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-02T14:34:26Z"
completed_at: "2026-05-02T14:48:00Z"
---
## Summary

Wrote the canonical results documents (`results_summary.md`, `results_detailed.md`), generated the
four headline charts under `results/images/`, populated `results/costs.json` with the exact run cost
($26.07) plus an Anthropic-rate-based judge cost estimate, and seeded `results/suggestions.json` and
`results/remote_machines_used.json` so downstream steps can finalize them. The headline finding —
RQ5 strict A>B>C inequality is rejected because A and B are tied (p ≈ 1.0) and C significantly beats
B (p = 0.019, paired N=130) — is documented with the contributing per-subset patterns and the
`MalformedPlanError` failure mode in B.

## Actions Taken

1. Loaded `results/metrics.json`, `data/mcnemar_results.json`, `data/calibration.json`,
   `data/judge_agreement.json`, and per-trajectory cost fields to compute per-variant subtotals (A:
   $4.47, B: $9.07, C: $12.54; runs total $26.07 across 390 trajectories).
2. Wrote `code/plot_results.py` and generated four PNGs into `results/images/`:
   `success_rate_overall.png`, `success_rate_by_subset.png`, `calibration_reliability.png`,
   `mcnemar_discordants.png`.
3. Wrote `results/results_summary.md` (per-RQ outcomes, per-subset rates, drivers of inversion,
   cost, caveats) and `results/results_detailed.md` (methodology, per-variant breakdown, statistical
   tests, calibration table, judge agreement, reproducibility section).
4. Wrote `results/costs.json` with the run-cost subtotals plus an estimated judge cost (390 sonnet
   + 89 opus calls at Anthropic published rates → ~$12.53). Wrote
     `results/remote_machines_used.json` as `[]` (local-only sweep).
5. Seeded `results/suggestions.json` with `spec_version=2` and an empty list to be filled by step
   14\.

## Outputs

* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/results_summary.md`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/results_detailed.md`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/remote_machines_used.json`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/suggestions.json` (placeholder)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/images/{success_rate_overall,success_rate_by_subset,calibration_reliability,mcnemar_discordants}.png`
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/plot_results.py`

## Issues

No issues encountered. The run-vs-judge cost split is partly estimated because the in-memory
`CostTracker` snapshots were not persisted to disk during the sweep; the run subtotal is exact (sum
of per-trajectory `cost_usd`) and the judge subtotal is computed from call counts at published
rates.
