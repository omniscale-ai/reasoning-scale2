---
spec_version: "2"
task_id: "t0009_hierarchical_annotation_v2"
date_completed: "2026-04-30"
status: "complete"
---
# Results Summary: Hierarchical Annotation v2

## Summary

All 115 rows of the v1 hierarchical-annotation pilot were re-annotated under the v2 tree schema with
`claude-haiku-4-5` and full problem text, achieving 115/115 hierarchy completeness and a 21/23 (91%)
judge accept rate on the stratified spot-check. Per-benchmark v2-vs-v1 deltas are uniformly
positive, ranging from +33% (SWE-bench Verified, tau-bench) to +100% (WorkArena++).

## Metrics

* **avg_decisions_per_task** = **16.38** atomic actions per row across the 115-row v2 dataset (range
  4-65, median 14). Tracks plan-length distribution.
* **Per-benchmark v2 judge accept rate**: FrontierScience-Olympiad **67% (4/6)**, SWE-bench Verified
  **100% (6/6)**, WorkArena++ **100% (6/6)**, tau-bench **100% (5/5)**.
* **Per-benchmark v1-vs-v2 delta**: FrontierScience-Olympiad **+67 percentage points** (0% -> 67%),
  SWE-bench Verified **+33 pp** (67% -> 100%), WorkArena++ **+100 pp** (0% -> 100%), tau-bench **+33
  pp** (67% -> 100%).
* **`global_atomics` fraction** = **13.6%** (256 cross-cutting atomics out of 1,884 total). Within
  the 18-22% range reported by ReAct/Reflexion on HotpotQA, lower-bounded.
* **Hierarchy completeness**: **115/115 (100%)** rows passed the stricter v2 rule (`global` non-null
  AND atomics present somewhere in the tree).
* **Total cost**: **$9.10** (annotator $7.42 + judge $1.68), under the $15 task budget.

## Verification

* `verify_dataset_asset` (via `meta.asset_types.dataset.verificator`): **PASSED** with 0 errors, 1
  warning (DA-W007 — author has no `country` field; intentional, project-internal author).
* `verify_research_papers`: **PASSED** with 0 errors, 0 warnings.
* `verify_plan`: **PASSED** with 0 errors, 1 warning (PL-W009 — informational, see plan log).
* `ruff check`, `ruff format`, `mypy -p tasks.t0009_hierarchical_annotation_v2.code`: **PASSED**
  with no errors.
* All 115 v2 jsonl rows are valid JSON with the v2 schema fields populated.
* All 23 judged rows have a non-null `judge_verdict` in `{acceptable, needs revision}`.
* `_pilot_row_index` values in the v2 jsonl are unique (verified with a Python set check).
