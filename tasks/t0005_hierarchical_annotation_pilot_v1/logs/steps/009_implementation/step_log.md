---
spec_version: "3"
task_id: "t0005_hierarchical_annotation_pilot_v1"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T19:51:23Z"
completed_at: "2026-04-29T20:05:00Z"
---
# Step 9: implementation

## Summary

Implemented all six plan steps end-to-end. Built the deterministic mapper, ran the LLM-as-judge
spot-check on a stratified sample of 12 rows using `claude-haiku-4-5-20251001` via the local
`claude` CLI (no separate `ANTHROPIC_API_KEY` needed), produced the `hierarchical-annotation-v1`
dataset asset (115 rows), and emitted summary statistics plus two charts. The dataset asset passes
`meta.asset_types.dataset.verificator` with zero errors and one warning (`DA-W007`: author has no
country field, which is acceptable for a project-internal asset).

## Actions Taken

1. Wrote `code/paths.py`, `code/constants.py`, `code/inspect_pilot.py`, `code/hierarchy_mapper.py`,
   `code/run_mapper.py`, `code/select_judge_sample.py`, `code/judge_runner.py`,
   `code/build_dataset_asset.py`, and `code/compute_stats.py`.
2. Added `matplotlib>=3.8` to `pyproject.toml` dependencies and ran `uv sync` (allowed top-level
   change per Critical Rule 1). REQ: needed for the per-benchmark and atomic-length charts.
3. Ran `inspect_pilot` to confirm the granularity-label state. Output: 115 rows, four benchmarks, no
   `hierarchy` key on input rows, node-type counts strategic=117 / conceptual=284 /
   computational=526 / verification=136. Satisfies REQ-1.
4. Ran `run_mapper` to produce `code/_outputs/mapped.jsonl` (115 rows). Satisfies REQ-2.
5. Ran `select_judge_sample` to pick 3 rows per benchmark = 12 rows total. Satisfies REQ-4.
6. Validation gate: ran the judge on the first sampled row alone first. Verified that the JSON
   verdict parsed correctly. Then ran the full 12-row judge over the sample.
7. Ran the judge runner (`judge_runner`) and merged verdicts into mapped rows by `_pilot_row_index`
   (task_ids are non-unique in the source pilot file — fixed during this step). Total cost:
   **$0.0598**. Result: 4 acceptable / 8 needs revision (33.3% accept rate overall; FrontierScience
   0/3, SWE-bench 2/3, tau-bench 2/3, WorkArena++ 0/3). Satisfies REQ-3.
8. Ran `build_dataset_asset` to produce
   `assets/dataset/hierarchical-annotation-v1/{details.json, description.md, files/hierarchical_annotation_v1.jsonl}`.
   115 rows confirmed; schema includes all required fields. Satisfies REQ-5.
9. Ran `meta.asset_types.dataset.verificator`: 0 errors, 1 warning (DA-W007 author country).
   Satisfies REQ-9.
10. Ran `compute_stats` to produce `code/_outputs/stats.json` and the two charts in
    `results/images/`. Computed `avg_decisions_per_task = 5.76` (mean of `len(atomic)` across all
    115 rows). Satisfies REQ-6 and REQ-7 (metric value is now ready for the orchestrator's results
    step to copy into `results/metrics.json`).
11. Verified ruff and mypy. mypy in package mode
    (`-p tasks.t0005_hierarchical_annotation_pilot_v1.code`) succeeds (the project's mypy config
    excludes `tasks/.*/code/`, so type-checking task code is a smoke import test rather than full
    type analysis).

## Outputs

* `code/paths.py`, `code/constants.py`
* `code/inspect_pilot.py`, `code/hierarchy_mapper.py`, `code/run_mapper.py`,
  `code/select_judge_sample.py`, `code/judge_runner.py`, `code/build_dataset_asset.py`,
  `code/compute_stats.py`
* `code/_outputs/mapped.jsonl` (115 rows, ~480 KB)
* `code/_outputs/judge_sample.jsonl` (12 rows)
* `code/_outputs/mapped_with_judge.jsonl` (115 rows)
* `code/_outputs/judge_costs.json`
* `code/_outputs/stats.json`
* `assets/dataset/hierarchical-annotation-v1/details.json`
* `assets/dataset/hierarchical-annotation-v1/description.md`
* `assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl` (115 rows)
* `results/images/per_benchmark_completeness.png`
* `results/images/atomic_lengths.png`
* `pyproject.toml` (matplotlib dependency added)

## Issues

* The source pilot file contains 14 rows whose `task_id` collides with at least one other row (115
  rows but only 101 unique `task_id` values). The first version of the judge runner merged verdicts
  back into mapped rows by `task_id`, which over-applied verdicts to duplicate rows. Fixed by
  carrying a `_pilot_row_index` field through the sample and merging by row index.
* DA-W007 (no author country) warning is acceptable for a project-internal asset whose author is the
  project itself.

## Requirement Completion Checklist

| Req | Status | Evidence |
| --- | --- | --- |
| REQ-1 (inspect & document) | done | `code/inspect_pilot.py` output captured in `logs/commands/`, summarised in this step log |
| REQ-2 (deterministic mapper) | done | `code/hierarchy_mapper.py`, `code/_outputs/mapped.jsonl` (115 rows) |
| REQ-3 (LLM-as-judge runner) | done | `code/judge_runner.py`, `code/_outputs/judge_costs.json` |
| REQ-4 (stratified >=12 rows) | done | 12 rows judged, exactly 3 per benchmark |
| REQ-5 (dataset asset, 115 rows) | done | `assets/dataset/hierarchical-annotation-v1/` |
| REQ-6 (stats reported) | done | `code/_outputs/stats.json` ready for `results_detailed.md` |
| REQ-7 (metrics) | done | `avg_decisions_per_task = 5.76` available for `results/metrics.json` |
| REQ-8 (cost cap $5) | done | Total cost $0.0598 — well under cap |
| REQ-9 (verify_dataset_asset) | done | `meta.asset_types.dataset.verificator` passed (1 warning) |
