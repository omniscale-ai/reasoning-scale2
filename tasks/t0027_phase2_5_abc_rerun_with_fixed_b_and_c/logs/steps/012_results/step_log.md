---
spec_version: "3"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-03T07:52:39Z"
completed_at: "2026-05-03T08:03:05Z"
---
## Summary

Wrote the spec-version-2 results bundle for the t0027 Phase 2.5 A/B/C re-run: results_summary.md
with headline numbers, results_detailed.md with full methodology, metrics tables, 12 worked
examples, and the mandatory Task Requirement Coverage section, plus costs.json ($20.7631 / $50.00
cap) and remote_machines_used.json (empty — local-only task). Generated six PNG charts (success rate
overall and per-subset, McNemar discordant pairs, calibration reliability, plan-parser recovery
distribution, cost breakdown) via a new make_result_charts.py.

## Actions Taken

1. Wrote `results/costs.json` with the per-stream agent / judge / smoke-gate breakdown for B and C
   plus a note explaining why the model under test is claude-sonnet-4-6 rather than the originally
   specified claude-opus-4-7.
2. Wrote `results/remote_machines_used.json` as `[]` to record that no remote compute was used.
3. Wrote `code/make_result_charts.py` which loads `data/mcnemar_results.json`,
   `data/calibration.json`, `results/metrics.json`, and `results/costs.json` and emits six
   matplotlib PNGs into `results/images/`.
4. Ran the chart generator and verified all six PNGs were produced.
5. Wrote `results/results_summary.md` with the headline numbers (RQ1 do_not_reject p=1.0, RQ5
   do_not_reject p=1.0, parser failure rate 0/130 for B and C, ECE 0.336 / 0.374, total cost
   $20.7631) and a verification block listing every passing verificator.
6. Wrote `results/results_detailed.md` (spec_version "2") with Summary, Methodology, Verification,
   Limitations, Files Created, Metrics Tables, Comparison vs t0026, Visualizations, Analysis, 12
   worked examples (best/random/contrastive/worst/boundary/all_failed across B and C), and the final
   mandatory Task Requirement Coverage section (REQ-1 through REQ-11 plus RQ1 and RQ5).
7. Ran `flowmark` on both markdown deliverables and `ruff check --fix` plus `ruff format` on the new
   chart script.

## Outputs

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_summary.md`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/remote_machines_used.json`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/success_rate_overall.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/success_rate_by_subset.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/mcnemar_discordant_overall.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/calibration_reliability.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/recovery_path_distribution.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/cost_breakdown.png`
* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/make_result_charts.py`

## Issues

No issues encountered.
