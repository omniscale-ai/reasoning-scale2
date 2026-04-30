---
spec_version: "2"
dataset_id: "hierarchical-annotation-v2-sonnet"
summarized_by_task: "t0014_v2_annotator_sonnet_rerun"
date_summarized: "2026-04-30"
---

# Hierarchical Annotation v2-sonnet (115-row pilot, tree schema, sonnet annotator)

## Metadata

* **Name**: Hierarchical Annotation v2-sonnet (115-row pilot, tree schema, sonnet annotator)
* **Year**: 2026
* **Authors**: Glite ARF reasoning-scale2 project
* **License**: inherited-per-row
* **Access**: restricted
* **Size**: 115 rows total; 100 pass v2 hierarchy_completeness; 20 judged; 18 acceptable, 2 needs revision.

## Overview

This dataset is a controlled re-annotation of the v1 hierarchical annotation pilot
(`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/`) under
the same v2 tree schema as
`tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/`, but with
`claude-sonnet-4-6` (sonnet) as the annotator instead of haiku. The judge stays on
`claude-haiku-4-5` (haiku), held constant across all variants.

The purpose of this asset is to deconfound the t0009 headline result. t0009 reported a +58 pp
aggregate accept-rate gain over v1, but it changed two things at once: schema (flat -> tree) and
annotator (sonnet -> haiku). This asset isolates the model component by reusing the v2 schema with
the original v1 annotator model.

The v2 tree schema records:

* `hierarchy.global` — one-sentence top-level approach,
* `hierarchy.subtasks` — list of `{subtask, atomics}` objects, where each subtask carries the
  atomic steps that implement it,
* `hierarchy.global_atomics` — atomic steps that span the whole trajectory and do not belong to
  any single subtask (typically verification, sanity checks, or cross-cutting concerns).

The same shape is mirrored on the `gold_actions` side of each row, recording the resolved concrete
actions an agent would take at each level.

The v2 pass also fixes the v1 LLM-as-judge truncation bug: where v1 truncated the problem text to
the first 1,500 characters before showing it to either the annotator or the judge, v2 passes the
full `problem` body to both.

## Content & Annotation

Each row of the JSONL contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `_pilot_row_index` | int | 0-based row index in the v1 pilot file. Unique key. |
| `task_id` | string | Source task ID; non-unique (14 v1 collisions). |
| `benchmark` | string | FrontierScience-Olympiad / SWE-bench Verified / WorkArena++ / tau-bench. |
| `domain` | string | Free-form domain tag from the source row. |
| `difficulty` | object | Difficulty rubric from the source row, copied verbatim. |
| `problem` | string | Full problem statement (no truncation). |
| `hierarchy` | object | v2 tree (`global`, `subtasks`, `global_atomics`). |
| `gold_actions` | object | Mirror tree of resolved concrete actions. |
| `annotation_model` | string | `claude-sonnet-4-6`. |
| `judge_verdict` | string \| null | `"acceptable"`, `"needs revision"`, or `null`. |
| `judge_notes` | string \| null | Justification or error string for the verdict. |
| `hierarchy_completeness` | bool | True iff `global` is non-null AND (any subtask has atomics OR `global_atomics` non-empty). |
| `annotator_notes` | string | Parser status: `ok` / `parse-failure: ...` / `call-failure: ...`. |

**Sample stratification.** The judge sample was drawn with a fixed seed of 42, stratified by
benchmark to allocate 6 rows from FrontierScience-Olympiad, 6 from SWE-bench Verified, 6 from
WorkArena++, and 5 from tau-bench (totalling 23 rows, 20% of the dataset). Only rows with
`hierarchy_completeness == true` were eligible for sampling. The same seed is used by t0009, so
the resulting sample composition is directly comparable when both runs hit
`hierarchy_completeness == true` on the same `_pilot_row_index` set.

## Statistics

| Benchmark | Total rows | Complete | Judged | Acceptable | Needs revision |
|-----------|------------|----------|--------|------------|----------------|
| FrontierScience-Olympiad | 40 | 26 | 3 | 3 | 0 |
| SWE-bench Verified | 23 | 22 | 6 | 5 | 1 |
| WorkArena++ | 26 | 26 | 6 | 6 | 0 |
| tau-bench | 26 | 26 | 5 | 4 | 1 |

* Total rows: 115
* Rows with v2 `hierarchy_completeness == true`: 100
* Rows judged: 20
* Acceptable: 18
* Needs revision: 2

## Usage Notes

* Load the JSONL with one row per line; each line is a JSON object with the schema described
  above. Use `_pilot_row_index` rather than `task_id` as the primary key — `task_id` is not
  unique across the source pilot.
* Compare against
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/`
  (haiku annotator, same schema, same prompt) to isolate the annotator-model effect; compare
  against
  `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/`
  (sonnet annotator, flat schema) to isolate the schema effect.
* Rows where `hierarchy_completeness == false` should be excluded from any downstream agent
  evaluation — their tree was not parseable at annotation time.
* Rows where `judge_verdict == "needs revision"` are still usable for downstream experiments,
  but their gold_actions should be inspected manually before being trusted as ground truth.
* The judge is a single LLM rater; treat verdicts as advisory, not as inter-rater agreement.

## Main Ideas

* **Deconfound design**: this asset and t0009's `hierarchical-annotation-v2` differ only in the
  annotator model. The v2-sonnet vs v2-haiku accept-rate delta therefore measures the
  annotator-model effect under a fixed schema and fixed judge. The v2-sonnet vs v1-sonnet delta
  measures the schema effect under a fixed annotator model.
* **Sonnet > haiku within the v2 schema** is the empirically expected outcome based on
  Boisvert2024 (Sonnet beats Haiku by ~25 pp on WorkArena++) and Zhou2022 (decomposition prompts
  +16 pp), which together suggest both axes contribute.
* **Same prompt, same temperature, same judge**: keeping every other element constant means any
  observed delta is attributable to the annotator-model swap.
* **Same 23-row sample** (seed=42, stratified): row-matched comparison enables Wilson 95% CI on
  per-benchmark deltas with n=5-6 per cell.

## Summary

Hierarchical Annotation v2-sonnet is the controlled-rerun companion to t0009's v2 dataset. It
re-annotates the same 115 benchmark rows under the same tree schema and the
same prompt, but with claude-sonnet-4-6 instead of claude-haiku-4-5. The judge is held constant on
claude-haiku-4-5 and operates on the same 23-row stratified sample, so the resulting accept-rate
delta is a clean read on the annotator-model component of t0009's +58 pp headline.

For this project, this asset is the missing arm of the {schema, model} 2x2: t0005 = (flat,
sonnet), t0009 = (tree, haiku), this asset = (tree, sonnet). The fourth cell (flat, haiku) is not
needed because no downstream experiment plans to use a flat schema with haiku.

Compared to alternatives — there is no published hierarchical annotation of these specific
benchmark composites; v1, v2-haiku, and v2-sonnet are bespoke project assets. WorkArena++'s
upstream paper (Boisvert2024) provides a tree-shaped annotation schema for its own subset that
v2's design echoes.
