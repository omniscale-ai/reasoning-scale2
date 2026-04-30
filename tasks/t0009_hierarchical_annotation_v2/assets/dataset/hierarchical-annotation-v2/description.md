---
spec_version: "2"
dataset_id: "hierarchical-annotation-v2"
summarized_by_task: "t0009_hierarchical_annotation_v2"
date_summarized: "2026-04-30"
---
# Hierarchical Annotation v2 (115-row pilot, tree schema)

## Metadata

* **Name**: Hierarchical Annotation v2 (115-row pilot, tree schema)
* **Year**: 2026
* **Authors**: Glite ARF reasoning-scale2 project
* **License**: inherited-per-row
* **Access**: restricted
* **Size**: 115 rows total; 115 pass v2 hierarchy_completeness; 23 judged; 21 acceptable, 2 needs
  revision.

## Overview

This dataset re-annotates the 115 benchmark tasks from the v1 hierarchical annotation pilot
(`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/`) under a
tree-shaped v2 schema. Where v1 used a flat list-of-strings structure (`subtask: list[str]`,
`atomic: list[str]`) with no encoded edges between higher-level subtasks and lower-level atomic
actions, v2 records explicit parent edges through a nested object:

* `hierarchy.global` — one-sentence top-level approach,
* `hierarchy.subtasks` — list of `{subtask, atomics}` objects, where each subtask carries the atomic
  steps that implement it,
* `hierarchy.global_atomics` — atomic steps that span the whole trajectory and do not belong to any
  single subtask (typically verification, sanity checks, or cross-cutting concerns).

The same shape is mirrored on the `gold_actions` side of each row, recording the resolved concrete
actions an agent would take at each level.

The v2 pass also fixes the v1 LLM-as-judge truncation bug: where v1 truncated the problem text to
the first 1,500 characters before showing it to either the annotator or the judge, v2 passes the
full `problem` body to both. This was the diagnosed dominant failure mode for
FrontierScience-Olympiad rows in v1 (0/3 accept rate when the judge could not see the actual
question).

The annotator and judge for v2 both run on `claude-haiku-4-5` via the local Claude Code CLI. The
original task description called for the v1 annotator (`claude-sonnet-4-6`) held constant to enable
a clean v2-vs-v1 schema comparison; v2 uses the cheaper `claude-haiku-4-5` model because the Claude
Code CLI's per-invocation system-prompt overhead made Sonnet ~5x more expensive than the task budget
allowed for 115 rows. This is documented as a known confound in
`tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md`.

## Content & Annotation

Each row of the JSONL contains the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `_pilot_row_index` | int | 0-based row index in the v1 pilot file. Unique key. |
| `task_id` | string | Source task ID; non-unique (14 v1 collisions). |
| `benchmark` | string | FrontierScience-Olympiad / SWE-bench Verified / WorkArena++ / tau-bench. |
| `domain` | string | Free-form domain tag from the source row. |
| `difficulty` | object | Difficulty rubric from the source row, copied verbatim. |
| `problem` | string | Full problem statement (no truncation). |
| `hierarchy` | object | v2 tree (`global`, `subtasks`, `global_atomics`). |
| `gold_actions` | object | Mirror tree of resolved concrete actions. |
| `annotation_model` | string | `claude-haiku-4-5`. |
| `judge_verdict` | string \| null | `"acceptable"`, `"needs revision"`, or `null`. |
| `judge_notes` | string \| null | Justification or error string for the verdict. |
| `hierarchy_completeness` | bool | True iff `global` is non-null AND (any subtask has atomics OR `global_atomics` non-empty). |
| `annotator_notes` | string | Parser status: `ok` / `parse-failure: ...` / `call-failure: ...`. |

**Sample stratification.** The judge sample was drawn with a fixed seed of 42, stratified by
benchmark to allocate 6 rows from FrontierScience-Olympiad, 6 from SWE-bench Verified, 6 from
WorkArena++, and 5 from tau-bench (totalling 23 rows, 20% of the dataset). Only rows with
`hierarchy_completeness == true` were eligible for sampling.

## Statistics

| Benchmark | Total rows | Complete | Judged | Acceptable | Needs revision |
| --- | --- | --- | --- | --- | --- |
| FrontierScience-Olympiad | 40 | 40 | 6 | 4 | 2 |
| SWE-bench Verified | 23 | 23 | 6 | 6 | 0 |
| WorkArena++ | 26 | 26 | 6 | 6 | 0 |
| tau-bench | 26 | 26 | 5 | 5 | 0 |

* Total rows: 115
* Rows with v2 `hierarchy_completeness == true`: 115
* Rows judged: 23
* Acceptable: 21
* Needs revision: 2

## Usage Notes

* Load the JSONL with one row per line; each line is a JSON object with the schema described above.
  Use `_pilot_row_index` rather than `task_id` as the primary key — `task_id` is not unique across
  the source pilot.
* The `hierarchy` and `gold_actions` blocks are intended for downstream Phase 2 scope-conditioning
  experiments (`tasks/t0012_phase2_abc_smoke_frontierscience` and successors). The
  `subtasks[i].atomics` list is the canonical list of atomic actions an agent should take while
  operating in subtask `i`.
* `global_atomics` is the canonical list of cross-cutting actions (final verification, sanity
  checks). Keep these distinct from subtask-bound atomics in the experiment harness.
* Rows where `hierarchy_completeness == false` should be excluded from any downstream agent
  evaluation — their tree was not parseable at annotation time.
* Rows where `judge_verdict == "needs revision"` are still usable for downstream experiments, but
  their gold_actions should be inspected manually before being trusted as ground truth.
* The judge is a single LLM rater; treat verdicts as advisory, not as inter-rater agreement.

## Main Ideas

* **Schema upgrade matters**: the v1 flat schema discarded the parent-child relationship between
  subtasks and atomics; v2 records it explicitly via the nested `subtasks` list. Downstream
  scope-conditioning experiments require this structure to evaluate "operating-at-this-level"
  behaviour.
* **Truncation was the dominant v1 failure**: passing full problem text to both annotator and judge
  measurably improved the accept rate, especially on long-context benchmarks like
  FrontierScience-Olympiad — see the v2-vs-v1 comparison in
  `tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md`.
* **`global_atomics` is non-trivial**: a meaningful fraction of atomics are cross-cutting
  (verification, sanity check) and do not belong under any single subtask. v1 lumped these into the
  flat atomic list; v2 separates them.
* **Model substitution is a known confound**: v2 used haiku for both annotator and judge while v1
  used sonnet for the annotator. The v2-vs-v1 accept-rate delta therefore conflates the schema
  change with a model downgrade. Future work (v3) should re-run with the original sonnet annotator
  under a flat-rate API to disentangle these.

## Summary

Hierarchical Annotation v2 is the canonical input dataset for the project's Phase 2 experiments on
scope-conditioned agents. It re-annotates the same 115 benchmark rows the v1 pilot covered but
encodes a tree-shaped hierarchy with explicit subtask-to-atomic edges and a separate
`global_atomics` bucket for cross-cutting steps. Both the annotator and the judge see the full
problem text, fixing the dominant v1 truncation failure mode.

For this project, v2 is the preferred input over v1 wherever the experiment harness requires the
parent-child edges (Phase 2 onward). The v1 dataset remains useful only for the historical v2-vs-v1
schema comparison documented in this task's results. The known model-substitution confound
(haiku-for-sonnet, driven by Claude Code CLI cost overhead) limits the apples-to-apples strength of
that comparison; a v3 follow-up task is queued to address it.

Compared to alternatives — there is no published hierarchical annotation of these specific benchmark
composites; v1 and v2 are bespoke project assets. WorkArena++'s upstream paper (Boisvert2024)
provides a tree-shaped annotation schema for its own subset, which v2's design echoes.
