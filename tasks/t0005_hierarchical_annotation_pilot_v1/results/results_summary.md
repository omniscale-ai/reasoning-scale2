# Results Summary: Hierarchical Annotation Pilot v1

## Summary

Audited the 115-row pilot annotation file, projected each row's `steps.nodes` graph onto the
project's three-level global / subtask / atomic schema with a deterministic Python mapper, ran an
LLM-as-judge spot-check on a 12-row stratified sample using `claude-haiku-4-5-20251001` via the
local `claude` CLI, and produced a single canonical `hierarchical-annotation-v1` dataset asset (115
rows). The asset passes the dataset verificator with 0 errors and 1 warning.

## Metrics

* **Rows in dataset**: **115** (FrontierScience-Olympiad **40**, SWE-bench Verified **23**,
  tau-bench **26**, WorkArena++ **26**)
* **Overall hierarchy completeness**: **88.7%** (102 / 115 rows have a non-null `global` and a
  non-empty `atomic` list)
* **Per-benchmark completeness**: FrontierScience-Olympiad **70.0%** (28/40), SWE-bench Verified
  **100.0%** (23/23), tau-bench **96.2%** (25/26), WorkArena++ **100.0%** (26/26)
* **LLM-as-judge accept rate (overall)**: **33.3%** (4/12 rows accepted)
* **Per-benchmark judge accept rate**: FrontierScience-Olympiad **0.0%** (0/3), SWE-bench Verified
  **66.7%** (2/3), tau-bench **66.7%** (2/3), WorkArena++ **0.0%** (0/3)
* **`avg_decisions_per_task`** (registered metric): **5.76** atomic actions per task
* **Total LLM cost**: **$0.06** (well under the $5 per-task cap)

## Verification

* `meta.asset_types.dataset.verificator` — **PASSED** (0 errors, 1 warning DA-W007 — author has no
  country field, acceptable for project-internal asset)
* `verify_research_papers` — **PASSED** (0 errors, 0 warnings)
* `verify_plan` — **PASSED** (0 errors, 1 warning PL-W009 about descriptive references to
  orchestrator-managed files in the REQ checklist)
* `verify_task_dependencies` — **PASSED** (no dependencies)
* `verify_task_metrics` and the rest of the reporting-step verificators run during the next step;
  see Step 15 for their final outcome.
