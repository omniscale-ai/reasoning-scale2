---
spec_version: "1"
task_id: "t0015_correct_proxy_benchmark_labels"
research_stage: "code"
tasks_reviewed: 12
tasks_cited: 4
libraries_found: 4
libraries_relevant: 0
date_completed: "2026-04-30"
status: "complete"
---

# Research Code — t0015_correct_proxy_benchmark_labels

## Task Objective

This task corrects mislabeled benchmark names in the `hierarchical-annotation-v2` dataset asset
produced by [t0009]. Two sets of rows carry the wrong `benchmark` field: 26 Mind2Web rows are
labeled `WorkArena++` and 26 HumanEval rows are labeled `tau-bench`. The fix must be delivered via
the corrections-overlay mechanism, leaving [t0009]'s task folder untouched, and must update both the
JSONL data file and the description metadata mentioning those benchmark names.

## Library Landscape

The library aggregator returns four registered libraries: `scope_aware_react_v1`,
`scope_unaware_planandsolve_v1`, `matched_mismatch_v1`, and `metric2_calibration_aggregator_v1`.
None of them is relevant to this task — they are agent strategy and metric-aggregation libraries for
downstream evaluation experiments, not data-correction utilities. No correction is recorded against
any of them. This task is a pure data-overlay correction with no executable code, so no library
import path is needed.

## Key Findings

### Origin of the proxy decision (t0003 → t0005 → t0009)

The proxy benchmark substitution was decided during dataset acquisition in [t0003]. WorkArena++ and
tau-bench were inaccessible at download time (gated registration, no public split with task
descriptions) so the project picked Mind2Web and HumanEval as drop-in stand-ins covering the same
"web-agent" and "code-agent" axes. The substitution was documented in [t0003]'s
`results/results_summary.md` but the row-level `benchmark` field in the downloaded slices was never
rewritten to reflect the swap. Pilot annotation in [t0005] reused those slices verbatim; v2
re-annotation in [t0009] reused [t0005]'s row IDs verbatim. The mislabel is therefore preserved
through three tasks because each downstream task treats `benchmark` as immutable provenance.

### Evidence from row-level task IDs in v2

The 115-row v2 JSONL at
`tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
makes the mislabel auditable from the data alone. Splitting `task_id` by underscore prefix gives
`fs` (40 rows, all labeled `FrontierScience-Olympiad` — correct), `swe` (23 rows, all labeled
`SWE-bench Verified` — correct), `m2w` (26 rows, all labeled `WorkArena++` — these are Mind2Web
rows; mislabel), and `he` (26 rows, all labeled `tau-bench` — these are HumanEval rows; mislabel).
The prefix-to-source mapping is consistent with the row IDs used in [t0005]'s v1 JSONL, confirming
the mislabel originated upstream and was preserved.

### Dataset overlay mechanics

The dataset aggregator at `meta/asset_types/dataset/aggregator.py` calls
`_load_effective_dataset_records`, which walks every task's `corrections/` folder and applies
`update` actions to the target dataset. The `changes` block of an `update` correction merges into
the metadata returned by the aggregator (so overriding `short_description` and `size_description`
takes effect at read time), and the `file_changes` block lets a correction redirect specific logical
paths to replacement files in the correcting task's own assets. For datasets the logical paths
exposed are the `description_path` field (currently `description.md`) plus every entry in `files[]`
(currently `files/hierarchical_annotation_v2.jsonl`). Both must be replaced for the overlay to be
complete.

### Schema preservation across v1 and v2

[t0009]'s v2 schema redefines the per-row hierarchy (global / subtasks-with-atomics / global_atomics
\+ parallel gold_actions tree) but copies the `benchmark`, `task_id`, and source context fields from
[t0005]'s v1 rows without modification. Re-annotation focused on the planning hierarchy, not on
benchmark provenance, which is why the v1 mislabel survived intact. This is relevant for the
planning step of t0015: only the `benchmark` field needs to change in the relabeled JSONL — every
other field can be carried over unchanged from the v2 source file.

## Reusable Code and Assets

There is no code or library to import or copy for this task — it is a pure data correction delivered
through the corrections-overlay mechanism. The reusable artifacts are data and specifications, not
code:

* **Source dataset asset** —
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/` from [t0009].
  * What it provides: `details.json`, `description.md`, and `files/hierarchical_annotation_v2.jsonl`
    (115 rows, one JSON object per line).
  * Reuse method: **read-only input** — the relabeled JSONL is produced by streaming this file and
    rewriting only the `benchmark` field for rows whose `task_id` starts with `m2w_` or `he_`.
  * Adaptation needed: rewrite `benchmark` in 52 rows; leave the remaining 63 rows byte-identical.
  * Approximate size: 115 lines of JSONL.

* **Corrections specification** — `arf/specifications/corrections_specification.md` v3.
  * What it provides: schema for `correction_id` (`C-XXXX-NN` derived from the correcting task ID),
    `target_task`, `target_kind: dataset`, `target_id`, `action: update`, `changes` (metadata
    overrides), and `file_changes` (per-logical-path replacement). Includes the rule that
    `file_changes` `replacement_task` must equal the correcting task ID.
  * Reuse method: **format reference**, no code to copy.

* **Dataset aggregator** — `meta/asset_types/dataset/aggregator.py` and
  `arf/scripts/common/corrections.py`.
  * What it provides: the materialization logic that resolves overlays. Used as a black box —
    `aggregate_datasets --ids hierarchical-annotation-v2 --include-full-description` is the
    verification command.
  * Reuse method: **invoke as a CLI**; no Python import required.

## Lessons Learned

The single most important lesson from prior tasks is that data provenance fields are not
self-correcting: [t0003] documented the proxy substitution in prose but did not rewrite the
row-level `benchmark` field, and every downstream task ([t0005], [t0009]) preserved the original
field rather than the prose. The corrections-overlay mechanism exists exactly for this case — it
lets a downstream task override both metadata and underlying files without touching the producing
task's folder, which would violate the immutability rule. Another lesson is that `update`
corrections combine `changes` and `file_changes` cleanly: when description prose mentions the
mislabeled values, both must be overridden so that aggregator output is internally consistent.

## Recommendations for This Task

1. **Use a single `update` correction** with both `changes` and `file_changes`. Override
   `short_description` and `size_description` in `changes` so any aggregator-rendered prose stops
   mentioning the wrong benchmark names. Use `file_changes` to swap `description.md` and
   `files/hierarchical_annotation_v2.jsonl` to relabeled copies.
2. **Author the replacement files inside this task's own `assets/dataset/<replacement_id>/`
   folder.** The correction spec requires `replacement_task` to equal the correcting task ID. Pick
   `hierarchical-annotation-v2-relabeled` as the replacement asset slug to keep the relationship
   obvious.
3. **Rewrite only the `benchmark` field**, in exactly 52 rows. Map `WorkArena++ → Mind2Web` for the
   26 `m2w_*` rows and `tau-bench → HumanEval` for the 26 `he_*` rows. Leave the 63 remaining rows
   (40 `fs_*` and 23 `swe_*`) byte-identical to preserve diff readability.
4. **Verify with `aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json`**
   after writing the correction. The materialized record must reflect the new descriptions and the
   file overlay must point at this task's replacement files. Also run `verify_corrections` to
   enforce schema compliance.
5. **Do not modify any file under `tasks/t0009_hierarchical_annotation_v2/`.** All edits live in
   `tasks/t0015_correct_proxy_benchmark_labels/`.

## Task Index

### [t0003]

* **Task ID**: `t0003_download_benchmark_subsets`
* **Name**: Download benchmark subsets
* **Status**: completed
* **Relevance**: Origin of the proxy substitution: this task is where Mind2Web was selected as a
  drop-in stand-in for the gated WorkArena++ split and HumanEval as a stand-in for tau-bench.

### [t0005]

* **Task ID**: `t0005_hierarchical_annotation_pilot_v1`
* **Name**: Hierarchical annotation pilot v1
* **Status**: completed
* **Relevance**: First task to consume the proxy slices for hierarchical annotation. Preserved the
  mislabeled `benchmark` field row-for-row, propagating the issue downstream.

### [t0009]

* **Task ID**: `t0009_hierarchical_annotation_v2`
* **Name**: Hierarchical annotation v2
* **Status**: completed
* **Relevance**: Producer of the dataset asset this task corrects. Re-annotated v1 rows under a v2
  tree schema but carried the mislabel through unchanged.

### [t0013]

* **Task ID**: `t0013_brainstorm_results_4`
* **Name**: Brainstorm results 4
* **Status**: completed
* **Relevance**: Source of the suggestion `S-0009-06` that this task implements (variant b — fix
  labels in the existing rows).
