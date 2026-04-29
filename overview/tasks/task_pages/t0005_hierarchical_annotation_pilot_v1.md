# ⏹ Hierarchical annotation pilot v1: audit and conform existing 115 rows

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0005_hierarchical_annotation_pilot_v1` |
| **Status** | ⏹ not_started |
| **Source suggestion** | `S-0002-08` |
| **Task types** | `hierarchical-annotation` |
| **Expected assets** | 1 dataset |
| **Task folder** | [`t0005_hierarchical_annotation_pilot_v1/`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/task_description.md)*

# Hierarchical Annotation Pilot v1

## Motivation

Phase 1 of the project's roadmap requires ≥100 tasks fully annotated with gold actions at
three granularity levels (global / subtask / atomic). The imported
`project/data/annotation_pilot/ tasks_annotated.jsonl` already contains 115 LLM-annotated
rows, but the rows have not been verified to conform to the project's three-level schema and
there is no human or LLM-as-judge spot-check pass on record. This task closes that gap in v1
form: keep the existing 115 rows in place, audit their structure, and produce a canonical
dataset asset that downstream Phase 2 / 3 experiments can consume. Implements suggestion
S-0002-08.

## Scope

* Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on
  each row to determine whether it carries explicit global / subtask / atomic granularity
  labels or whether the granularity must be inferred.
* If labels are missing, write a deterministic mapper that derives the three-level structure
  from the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block
  per row.
* Run an LLM-as-judge spot-check on at least 10% of rows (≥12 rows) to estimate hierarchy
  quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/`
  with rows of shape `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask,
  atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict,
  judge_notes}`.

Out of scope for v1: replacing the HumanEval and Mind2Web proxies, expanding beyond 115 rows,
human review, inter-rater agreement studies. All deferred to follow-up tasks.

## Approach

1. Load the 115-row pilot file. For each row, compute the inferred or stated hierarchy and
   emit the canonical schema record.
2. Sample at least 12 rows stratified across the four benchmarks (FrontierScience-Olympiad,
   SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Send each to the LLM judge with the
   row's problem text and proposed hierarchy; capture verdict ("acceptable" / "needs
   revision") plus a one-sentence justification.
3. Persist the consolidated dataset asset with `details.json` (source URL = the imported pilot
   path, version = "v1", license = inherited from each upstream benchmark, sample count = 115)
   and `files/hierarchical_annotation_v1.jsonl`.
4. Report distribution stats in `results/results_detailed.md` (per-benchmark counts,
   per-domain counts, hierarchy-completeness rate, judge accept rate).

## Expected Outputs

* `assets/dataset/hierarchical_annotation_v1/` with `details.json`, `files/`, and a
  `description.md`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate.
* `results/results_detailed.md` with the full audit table and any rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (the registered diagnostic
  metric).
* Follow-up suggestions for: extension to ≥200 rows, full human-review pass, and proxy
  benchmark remediation.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: under 3 USD for 12-15 LLM-as-judge calls on
`claude-haiku-4-5-20251001`. Per-task cap: 5 USD.

## Dependencies and Cross-References

* No task dependencies.
* Reads `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows).
* Reads `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules — wrap
  as black-box utilities, never modify in place.
* References the four benchmark dataset assets produced by `t0003_download_benchmark_subsets`.

## Source Suggestion

S-0002-08 — "Run a Phase 1 pilot annotation on 20 tasks before scaling to 100." This task
implements that idea in v1 form, leveraging the existing 115 rows rather than re-annotating
from scratch.

## Key Questions

1. Do the existing 115 rows already carry a global / subtask / atomic decomposition, or must
   one be inferred?
2. What is the per-benchmark hierarchy-completeness rate?
3. What is the LLM-as-judge accept rate? Does it differ across benchmarks?
4. Are there systematic patterns in rejected rows (e.g., one benchmark consistently failing)?

</details>
