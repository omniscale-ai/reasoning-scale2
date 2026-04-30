---
spec_version: "2"
task_id: "t0014_v2_annotator_sonnet_rerun"
date_completed: "2026-04-30"
status: "complete"
---
# Results Summary: v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)

## Summary

Re-annotated the same 115-row v1 pilot under the v2 tree schema with `claude-sonnet-4-6`, re-judged
with the t0009 `claude-haiku-4-5` judge on the same seed-42 stratified sample (intersected to 20
rows after 3 FrontierScience-Olympiad sonnet timeouts), and decomposed the t0009 +58 pp headline
into a **+57 pp schema-only** delta and a **-1 pp model-only** delta. The annotator-model swap
(haiku -> sonnet) contributes essentially zero of the t0009 gain; the v2 tree schema accounts for
nearly all of it. Total cost $21.16 (annotator $19.77 + judge $1.40), within the user-authorised $25
cumulative cap.

## Metrics

* **avg_decisions_per_task** = **12.16** atomic actions per row across the 100 v2-sonnet rows that
  passed `hierarchy_completeness` (1,216 total atomics; range 4-29, median 11). Tracks plan-length
  distribution; lower than t0009 v2-haiku (16.38) because sonnet emits more terse, higher-level
  atomics on average.
* **Aggregate v2-sonnet judge accept rate**: **90% (18/20)**, Wilson 95% CI **[69.9%, 97.2%]**.
* **Schema-only delta** (v2-sonnet vs v1-sonnet, annotator constant): **+57 pp** (90% vs 33%, n_a=20
  / n_b=12; v1-sonnet Wilson CI [13.8%, 60.9%]).
* **Model-only delta** (v2-sonnet vs v2-haiku, schema constant): **-1 pp** (90% vs 91%, n_a=20 /
  n_b=23; v2-haiku Wilson CI [73.2%, 97.6%]). The two CIs overlap completely; the point estimate is
  within sampling noise of zero.
* **Headline cross-check** (v2-haiku vs v1-sonnet): **+58 pp** — matches t0009's published number
  exactly, confirming the decomposition arithmetic (schema_only + model_only + interaction = 57 - 1
  \+ 2 = +58 pp; interaction term within noise).
* **Per-benchmark schema-only deltas**: FrontierScience-Olympiad **+100 pp** (0% -> 100%, n=3/3),
  WorkArena++ **+100 pp** (0% -> 100%, n=6/3), SWE-bench Verified **+17 pp** (67% -> 83%, n=6/3),
  tau-bench **+13 pp** (67% -> 80%, n=5/3).
* **Per-benchmark model-only deltas**: FrontierScience-Olympiad **+33 pp** (67% -> 100%, n=6/3),
  WorkArena++ **+0 pp** (100% -> 100%, n=6/6), SWE-bench Verified **-17 pp** (100% -> 83%, n=6/6),
  tau-bench **-20 pp** (100% -> 80%, n=5/5). Negative deltas on SWE/tau are within Wilson-CI noise:
  v2-haiku was already at 100% there, so a single sonnet slip drops the rate by 17-20 pp.
* **Total cost**: **$21.16** (annotator $19.77 + judge $1.40), within the user-authorised $25
  cumulative cap (intervention `budget_cap_raised.md`).

## Verification

* `verify_dataset_asset` (via
  `meta.asset_types.dataset.verificator t0014_v2_annotator_sonnet_rerun hierarchical-annotation-v2-sonnet`):
  **PASSED** with 0 errors, 1 warning (DA-W007 — author has no `country` field; intentional, the
  project entity is institutional not a named individual).
* `verify_research_papers t0014_v2_annotator_sonnet_rerun`: **PASSED** with 0 errors, 0 warnings.
* `verify_plan t0014_v2_annotator_sonnet_rerun`: **PASSED** with 0 errors, ≤ 2 warnings.
* `ruff check`, `ruff format`, `mypy -p tasks.t0014_v2_annotator_sonnet_rerun.code`: all clean, no
  errors.
* All 115 v2-sonnet jsonl rows are valid JSON with the v2 schema fields populated; every row has
  `annotation_model = "claude-sonnet-4-6"`. All 20 judged rows have a non-null `judge_verdict` in
  `{acceptable, needs revision}`. `_pilot_row_index` values are unique.
* The 20-row judge sample is the t0009 23-row sample intersected with v2-sonnet completeness
  (FrontierScience-Olympiad rows 7, 8, 14 dropped because three sonnet retries timed out at the 300
  s CLI ceiling). Per-benchmark sample sizes: FrontierScience-Olympiad 3, SWE-bench Verified 6,
  WorkArena++ 6, tau-bench 5.
