---
spec_version: "3"
task_id: "t0014_v2_annotator_sonnet_rerun"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-30T19:28:54Z"
completed_at: "2026-04-30T23:30:00Z"
---
# Step 9: implementation

## Summary

Completed the controlled-rerun pipeline for t0014: re-annotated all 115 v1-pilot rows with
`claude-sonnet-4-6` under the v2 tree schema (running across two budget-cap-raised sessions),
recovered the 23-row judge sample (intersected to 20 rows because three FrontierScience-Olympiad
rows hit `claude` CLI timeouts on sonnet), ran the haiku judge on those 20 rows, and assembled the
`hierarchical-annotation-v2-sonnet` dataset asset with judge verdicts merged. Computed the three-way
comparison and emitted the three required charts.

Aggregate result: schema-only delta = **+57 pp** (90% v2-sonnet vs 33% v1-sonnet, n_a=20 / n_b=12),
model-only delta = **−1 pp** (90% v2-sonnet vs 91% v2-haiku, n_a=20 / n_b=23), headline delta =
**+58 pp** (matches t0009's reported number within sampling noise). The schema swap accounts for
nearly the entire t0009 gain; the annotator-model swap contributes essentially nothing.

## Actions Taken

1. Annotation phase (already partly executed before this final session):
   * Ran `v2_annotator.py` across two sessions; the first session halted at row 52 with
     `total_cost_usd=$10.92` over the original $10 cap; user authorised raising the cap to $25
     cumulative (`intervention/budget_cap_raised.md`). The second session resumed via the idempotent
     JSONL append and finished the remaining rows. Final state: 115 unique `_pilot_row_index` values
     in `code/_outputs/v2_sonnet_annotated.jsonl`, `total_cost_usd=$19.7667` across 96 successful
     sonnet calls plus 14 call-failures (all on three FrontierScience-Olympiad row indices that
     consistently timed out at the 300 s CLI ceiling) and 1 parse-failure that the safe-parser
     absorbed.
2. Sample selection: rewrote `select_judge_sample.py` to load t0009's persisted sample directly and
   intersect with v2-sonnet rows that have `hierarchy_completeness == true`, instead of redrawing
   the random sample from the local bucket. The seed-and-bucket approach diverges when the
   FrontierScience-Olympiad bucket loses rows: `random.sample` over a different population gives a
   different draw on the same seed. Loading the persisted t0009 sample and filtering by completeness
   guarantees the model-only delta is computed on the maximum apples-to-apples intersection. Result:
   20 rows kept (FrontierScience-Olympiad=3, SWE-bench Verified=6, WorkArena++=6, tau-bench=5); 3
   dropped (FrontierScience-Olympiad rows 7, 8, 14 — sonnet timed out three retries).
3. Judge: ran `v2_judge.py --workers 4`. 20/20 judged, 18 acceptable, 2 needs revision, 0 parse
   failures, 0 call failures. Cost: $1.3965, well under the $2 judge cap.
4. Asset assembly: ran `build_v2_asset.py` to merge judge verdicts into the annotated rows, and
   wrote `details.json` and `description.md`. Verified via
   `python -m meta.asset_types.dataset.verificator --task-id t0014_v2_annotator_sonnet_rerun hierarchical-annotation-v2-sonnet`:
   PASSED, 0 errors, 1 warning (DA-W007 author has no country — intentional, the project entity is
   institutional not personal).
5. Three-way statistics: ran `compute_stats.py`. Wrote `code/_outputs/three_way_comparison.json` and
   `code/_outputs/three_way_table.md`. Aggregate schema-only +57 pp, model-only −1 pp, headline +58
   pp.
6. Charts: ran `make_charts.py`. Three PNGs in `results/images/`: `three_way_accept_rate.png`,
   `aggregate_decomposition.png`, `v2_sonnet_atomics_distribution.png`.
7. Quality gate: `ruff check --fix` and `ruff format` pass clean;
   `mypy -p tasks.t0014_v2_annotator_sonnet_rerun.code` reports zero errors.

## Outputs

* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_annotated.jsonl` (115 rows)
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_annotator_costs.json`
  (`total_cost_usd=$19.7667`)
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl` (20 rows)
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_outcomes.jsonl` (20 rows)
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_costs.json`
  (`total_cost_usd=$1.3965`)
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/three_way_comparison.json`
* `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/three_way_table.md`
* `tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/`
  (details.json + description.md + files/hierarchical_annotation_v2_sonnet.jsonl)
* `tasks/t0014_v2_annotator_sonnet_rerun/results/images/three_way_accept_rate.png`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/images/aggregate_decomposition.png`
* `tasks/t0014_v2_annotator_sonnet_rerun/results/images/v2_sonnet_atomics_distribution.png`

## Issues

* **3-row sample shrinkage on FrontierScience-Olympiad** (call-failures on idx 7, 8, 14). All three
  are `claude` CLI timeouts at 300 s on long-context Olympiad problems. The plan's risk fallback
  ("compute model-only delta on the intersection set and report sample size") is in effect; the
  remaining 20-of-23 sample still preserves the per-benchmark bucket structure for the other three
  benchmarks at full size.
* DA-W007 warning on the dataset asset (author has no country) is intentional; the project entity is
  institutional, not a named individual.
* Annotator cost ($19.77) ran ~4× the original $5 estimate due to CLI cache-creation overhead on the
  long v2 system prompt; the $25 cumulative cap (per `intervention/budget_cap_raised.md`) absorbed
  this overrun cleanly.
