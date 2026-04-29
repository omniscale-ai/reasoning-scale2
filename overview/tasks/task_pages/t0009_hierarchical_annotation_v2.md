# ⏳ Hierarchical annotation v2: tree schema with subtask-to-atomic edges

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0009_hierarchical_annotation_v2` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-04-29T23:24:52Z |
| **Source suggestion** | `S-0005-02` |
| **Task types** | `hierarchical-annotation` |
| **Expected assets** | 1 dataset |
| **Task folder** | [`t0009_hierarchical_annotation_v2/`](../../../tasks/t0009_hierarchical_annotation_v2/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0009_hierarchical_annotation_v2/task_description.md)*

# Hierarchical Annotation v2 (Tree Schema)

## Motivation

The v1 annotation produced by `t0005_hierarchical_annotation_pilot_v1` uses a flat schema:
`subtask` is a `list[str]`, `atomic` is a `list[str]`, and there is no encoded edge mapping
atomics to their parent subtask. The v1 schema also truncates problem text to 1500 characters
in the `task_excerpt` field, which the v1 LLM-as-judge identified as the dominant failure mode
on FrontierScience-Olympiad rows (0/3 accept rate). This task fixes both issues: re-annotates
all 115 rows under a tree-shaped v2 schema with full problem text, and spot-checks at least
20% of rows with the LLM judge to estimate quality. Implements suggestion S-0005-02 and the
partial v2-schema portion of S-0005-01.

## v2 Schema

```json
{
  "task_id": "...",
  "benchmark": "...",
  "domain": "...",
  "difficulty": { ... },
  "problem": "...",
  "hierarchy": {
    "global": "<one-sentence top-level approach>",
    "subtasks": [
      {
        "subtask": "<subtask description>",
        "atomics": ["<atomic step>", "..."]
      },
      ...
    ],
    "global_atomics": ["<cross-cutting atomic step>", "..."]
  },
  "gold_actions": {
    "global": "<resolved global action>",
    "subtasks": [
      {
        "subtask": "<resolved subtask action>",
        "atomics": ["<resolved atomic action>", "..."]
      },
      ...
    ],
    "global_atomics": ["<resolved cross-cutting atomic action>", "..."]
  },
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "...",
  "hierarchy_completeness": true | false
}
```

`global_atomics` captures atomic steps that do not belong to any single subtask (typically
verification, sanity checks, or cross-cutting concerns surfaced in v1's flat `atomic` list).

## Scope

* Re-run the v1 annotator (`claude-sonnet-4-6`) with a new prompt that elicits the tree schema
  above. Pass the **full problem text** (no `task_excerpt` truncation).
* Apply the same task_id deduplication fix from v1 (the source pilot file has 14 rows with
  colliding `task_id`s; thread `_pilot_row_index` through the asset).
* Spot-check at least 23 rows (20%) with `claude-haiku-4-5-20251001` as judge. Sample is
  stratified across the four benchmarks (FrontierScience-Olympiad, SWE-bench Verified,
  HumanEval-proxy, Mind2Web-proxy).
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical-annotation-v2/`
  with the schema above and a `description.md` explaining the v2 → v1 migration.
* Compare v2 vs v1 judge accept rate per benchmark and flag any benchmark where v2 fails to
  improve.

Out of scope: scaling beyond 115 rows (S-0005-01 expansion), human review (full review pass
deferred to v3), proxy benchmark replacement (deferred to follow-up).

## Approach

1. Read the v1 dataset `assets/dataset/hierarchical-annotation-v1/files/*.jsonl` from t0005
   and load all 115 rows.
2. For each row, construct a v2 annotation prompt with the full problem text and the v2 schema
   in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree.
3. Stratified-sample 23 rows. For each, call the haiku judge with the row's full problem and
   the proposed v2 hierarchy; capture verdict + one-sentence justification.
4. Persist as a `dataset` asset with `details.json` (source = t0005's v1 dataset asset,
   version = "v2", license inherited per row, sample count = 115) and
   `files/hierarchical_annotation_v2.jsonl`.
5. Report per-benchmark v2-vs-v1 judge accept rate delta in `results/results_detailed.md`.

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2/{details.json, description.md, files/}`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate vs v1.
* `results/results_detailed.md` with the full audit table, the v2-vs-v1 comparison, and any
  rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (mean atomics per row).
* Follow-up suggestions for: row-count expansion to ≥200, human review pass, proxy benchmark
  remediation, and any benchmark where v2 fails to improve over v1.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$15** (115 sonnet annotations + 23 haiku
judges). Per-task cap: $20.

## Dependencies and Cross-References

* No task dependencies. Reads t0005's v1 dataset asset as input but does not depend on the
  t0005 task being incomplete.
* References `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows, original).
* Sister-task coordination: t0012 will consume the v2 dataset; this task must publish the v2
  dataset asset before t0012's implementation step runs.

## Source Suggestion

S-0005-02 — "Re-run LLM-as-judge with full problem text (no truncation)." Also partially
addresses S-0005-01 (annotation v2 schema) and the schema-gap finding from brainstorm 3.

## Key Questions

1. What is the per-benchmark judge accept rate under v2 vs v1?
2. How does the v2 schema's tree shape affect FrontierScience-Olympiad acceptance specifically
   (the worst-performing benchmark in v1)?
3. Are there rows where the v2 tree decomposition is well-defined but the v1 flat
   decomposition was empty (hierarchy_completeness: false in v1)?
4. What fraction of atomics fall under `global_atomics` vs assigned to a specific subtask?

</details>
