---
spec_version: "2"
dataset_id: "hierarchical-annotation-v1"
summarized_by_task: "t0005_hierarchical_annotation_pilot_v1"
date_summarized: "2026-04-29"
---
# Hierarchical Annotation v1 (115-row pilot audit)

## Metadata

* **Name**: Hierarchical Annotation v1 (115-row pilot audit)
* **Year**: 2026
* **Authors**: Glite ARF reasoning-scale project
* **License**: inherited-per-row
* **Access**: restricted
* **Size**: 115 rows; one row per benchmark task

## Overview

This dataset is the v1 hierarchical-annotation pilot of the Glite ARF reasoning-scale project. It
takes the 115 LLM-annotated rows produced by `project/code/scripts/collect_and_annotate.py` and
projects each row's `steps.nodes` graph onto the project's three-level global / subtask / atomic
schema using a deterministic mapper. A 12-row LLM-as-judge spot-check (3 rows per benchmark) using
`claude-haiku-4-5-20251001` provides an external quality estimate.

The dataset feeds Phase 2 and Phase 3 scope-conditioning experiments. It is the canonical
gold-action source until a larger v2 (>=200 rows with full human review) is produced.

## Content & Annotation

Each row follows the canonical schema:

```json
{
  "task_id": "<benchmark prefix + uuid>",
  "benchmark": "FrontierScience-Olympiad" | "SWE-bench Verified" | "tau-bench" | "WorkArena++",
  "domain": "<benchmark-specific category, e.g. physics or sales>",
  "difficulty": {...},
  "problem": "<full problem statement>",
  "hierarchy": {
    "global": "<short label of the high-level plan move> | null",
    "subtask": ["<conceptual subtask labels in id order>", ...],
    "atomic":  ["<computational + verification action labels in id order>", ...]
  },
  "gold_actions": { ... mirrors hierarchy but uses the longer 'detail' field ... },
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "<one-sentence justification or null>",
  "hierarchy_completeness": true | false
}
```

Mapper rules:

* **`global`**: text from the lowest-id `strategic` node, falling back to the first node by id when
  none exists, and `null` when the input row's `steps` is `null` (LLM annotation failure).
* **`subtask`**: list of `conceptual` node labels in id order; falls back to `strategic` nodes
  beyond the first when no conceptual nodes are present.
* **`atomic`**: `computational` and `verification` nodes in id order.

`hierarchy_completeness` is `true` iff `global is not None` and `len(atomic) > 0`.

## Statistics

| Benchmark | Row count | Hierarchy completeness | Judge accept rate |
| --- | --- | --- | --- |
| FrontierScience-Olympiad | 40 | 70.0% | 0.0% (0/3) |
| SWE-bench Verified | 23 | 100.0% | 66.7% (2/3) |
| WorkArena++ | 26 | 100.0% | 0.0% (0/3) |
| tau-bench | 26 | 96.2% | 66.7% (2/3) |

* **Mean atomic actions per task**: 5.76
* **Total rows**: 115

## Usage Notes

Load with `jsonlines` or pandas (`pd.read_json(..., lines=True)`). Filter by
`hierarchy_completeness == true` if downstream consumers need only fully-decomposed rows. The judge
verdict is populated only on the stratified sample (12 rows total); for all other rows
`judge_verdict` is `null` — this is by design.

Known quirks:

* FrontierScience-Olympiad has 11 rows with `steps == null` due to upstream LLM annotation failures.
  These rows are preserved with `hierarchy_completeness == false` and a `null` global label so
  downstream tasks can re-annotate without re-running the original pipeline.
* The pilot file's "agentic proxies" are tau-bench and WorkArena++ (not HumanEval-proxy and
  Mind2Web-proxy as one earlier draft of the task description named them).

## Main Ideas

* The deterministic mapper exploits the existing `type` field (`strategic`, `conceptual`,
  `computational`, `verification`) so no extra LLM cost is needed for the mapping itself; the
  external judge check is what guards quality.
* A small (12-row) stratified judge sample is sufficient to surface schema bugs because hierarchy
  errors tend to be systematic across rows of the same benchmark.
* Empty `subtask` lists are valid v1 output: when the upstream annotator produced a flat list of
  computational nodes without conceptual abstractions, the mapper preserves that flatness rather
  than inventing subtask boundaries.

## Summary

The hierarchical-annotation-v1 dataset converts 115 LLM-annotated benchmark tasks into a uniform
global / subtask / atomic schema using a deterministic Python mapper, and supplements that with a
12-row LLM-as-judge audit. It is the input to all Phase 2 / Phase 3 scope-conditioning experiments
in the project.

For the project, this asset is the first concrete instantiation of the project's hierarchical
schema. Its main limitations — the small sample size, the reliance on a single annotator
(`claude-sonnet-4-6`), and the absence of human-rater agreement — are deferred to a v2 task that
will scale to >=200 rows and add human review.
