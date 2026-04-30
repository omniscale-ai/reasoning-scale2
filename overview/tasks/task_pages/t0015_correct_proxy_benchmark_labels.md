# ✅ Correct proxy-benchmark labels in t0009 v2 dataset

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0015_correct_proxy_benchmark_labels` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T19:08:28Z |
| **Completed** | 2026-04-30T19:32:45Z |
| **Duration** | 24m |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source suggestion** | `S-0009-06` |
| **Task types** | `correction` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`benchmark-annotation`](../../by-category/benchmark-annotation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`hierarchical-planning`](../../by-category/hierarchical-planning.md) |
| **Step progress** | 9/15 |
| **Task folder** | [`t0015_correct_proxy_benchmark_labels/`](../../../tasks/t0015_correct_proxy_benchmark_labels/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/task_description.md)*

# Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Motivation

The `t0009_hierarchical_annotation_v2` dataset asset labels its four benchmarks as
`FrontierScience-Olympiad`, `SWE-bench Verified`, `WorkArena++`, and `tau-bench`. The first
two are accurate. The latter two are mislabelled — the underlying rows are `Mind2Web` and
`HumanEval` rows used as proxies for browser-using and tool-using agent benchmarks, not actual
`WorkArena++` or `tau-bench` rows. Once t0012 (Phase 2 A/B/C smoke) reports per-benchmark
numbers, naïve consumers would attribute results to benchmarks the project does not actually
evaluate on.

This task fixes the labels via the corrections-overlay mechanism — no re-annotation, no API
spend, no change to the t0009 task folder. Implements `S-0009-06` variant b (label correction;
variant a would have replaced the proxy rows with actual WorkArena++/tau-bench data, which is
out of scope for this wave).

## Scope

* Write one correction file per affected benchmark (or one combined correction, depending on
  the aggregator's per-row update support):
  * `WorkArena++` → `Mind2Web`.
  * `tau-bench` → `HumanEval`.
* Action: `update`. The correction overlays `details.json` `description_path` (and any per-row
  `benchmark` fields exposed by the dataset aggregator) so downstream consumers see the
  corrected labels.
* Provide a one-paragraph rationale per correction file referencing the original proxy
  decision taken in t0003 (benchmark download) and t0005 (v1 annotation pilot).
* Run `verify_corrections` against the new files.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data (a separate dataset
task, deferred); editing t0009's task folder (immutable); changing per-row IDs (only the
benchmark label).

## Approach

1. Read t0009's `assets/dataset/hierarchical-annotation-v2/details.json` and the dataset
   aggregator schema to confirm where benchmark labels are exposed (top-level `benchmarks`
   list, per-row `benchmark` field, or both).
2. Confirm the dataset aggregator's correction-overlay support — if `file_changes` is
   required, author a replacement description document and (if applicable) replacement JSONL
   with corrected per-row labels.
3. Write the correction file(s) under `corrections/dataset_<dataset_id>.json` per
   `corrections_specification.md` v3.
4. Re-run the dataset aggregator with the correction overlay applied; confirm the corrected
   labels are visible in the materialized output.

## Expected Outputs

* `corrections/dataset_<t0009_dataset_id>.json` (one or more correction files).
* If `file_changes` is needed: a replacement description document and/or replacement JSONL
  under this task's `assets/dataset/...-relabeled/` folder.
* `results/results_summary.md` reporting how many rows had their benchmark label corrected and
  the before/after distribution.
* `results/results_detailed.md` with the rationale, the correction-file structure, and any
  follow-up suggestion to actually replace the proxy rows with native WorkArena++/tau-bench
  data.

## Compute and Budget

No GPU. No API spend. Estimated cost: **$0**. Per-task cap: $1.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the dataset asset whose labels are being
  corrected.
* Independent of `t0014_v2_annotator_sonnet_rerun`. Order does not matter; if both land before
  t0012 finishes, t0012's per-benchmark reporting will pick up both overlays through the
  aggregator.
* `t0012` (in_progress) reads the t0009 dataset through the aggregator, so the corrected
  labels flow through automatically once t0015 merges. The FrontierScience filter t0012 uses
  is unaffected.

## Source Suggestion

`S-0009-06` variant b — "Relabel the proxy benchmarks WorkArena++→Mind2Web and
tau-bench→HumanEval in the v2 dataset via a correction file."

## Key Questions

1. How many rows are affected by each label correction?
2. Does the t0009 dataset aggregator support per-row label overlays via `changes`, or is a
   `file_changes` overlay needed?
3. Are there any downstream consumers (other than t0012) that already cache the original
   labels and would need re-aggregation?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| dataset | [Hierarchical Annotation v2 (115-row pilot, tree schema, relabeled)](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/) | [`description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md) |

## Suggestions Generated

<details>
<summary><strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++ and
tau-bench data</strong> (S-0015-01)</summary>

**Kind**: dataset | **Priority**: medium

Variant a of S-0009-06 (now folded into this follow-up). The 26 m2w_* rows in the v2
hierarchical-annotation dataset are Mind2Web data used as a proxy for the gated WorkArena++
split, and the 26 he_* rows are HumanEval data used as a proxy for the gated tau-bench split.
t0015 corrected the labels but did not replace the underlying data. This task should (1)
obtain access to a real WorkArena++ split and a real tau-bench split (both currently gated;
expect a registration / agreement step that must be tracked as an intervention), (2)
re-annotate 26 + 26 rows under the v2 tree schema using the same haiku annotator and judge as
t0009 to keep variant b apples-to-apples, and (3) issue a corrections-overlay against
hierarchical-annotation-v2 that swaps the proxy rows for the native rows. Out of scope: any
change to the FrontierScience-Olympiad or SWE-bench Verified rows.

</details>

<details>
<summary><strong>Add a row-level original_benchmark provenance field to future
relabel corrections</strong> (S-0015-02)</summary>

**Kind**: evaluation | **Priority**: low

The t0015 overlay rewrites the per-row benchmark string but does not preserve the original
proxy label inside the row. A reader inspecting only the effective JSONL cannot tell that the
row was previously labeled differently — provenance lives only in the corrections overlay's
description.md. For future relabel corrections, the framework would benefit from a soft
convention where the corrected row carries an original_benchmark field (or, more generally,
original_<field> for any field rewritten by a corrections overlay). This makes per-row
provenance auditable without round-tripping through the corrections file. The task should: (1)
propose the convention as a small extension to the corrections specification, (2) update the
dataset-asset verificator to surface a warning when an overlay rewrites a per-row field
without preserving the original, and (3) backfill the convention into the t0015 overlay.

</details>

## Research

* [`research_code.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/results/results_summary.md)*

# Results Summary: Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Summary

Wrote a single corrections-overlay file
(`corrections/dataset_hierarchical-annotation-v2.json`) that relabels the **52** rows in the
t0009 v2 hierarchical-annotation dataset whose `benchmark` field referred to a gated
proxy-target benchmark instead of the actual data source: **26** `m2w_*` rows move from
`WorkArena++` to `Mind2Web`, and **26** `he_*` rows move from `tau-bench` to `HumanEval`. The
`aggregate_datasets` overlay applies cleanly: the effective JSONL now carries the corrected
labels and the dataset metadata prose no longer mentions the wrong benchmark names.

## Metrics

* **Rows relabeled, total**: **52** of 115 (45.2%)
* **`WorkArena++` -> `Mind2Web`**: **26** rows (all rows whose `task_id` starts with `m2w_`)
* **`tau-bench` -> `HumanEval`**: **26** rows (all rows whose `task_id` starts with `he_`)
* **Rows unchanged**: **63** (40 `FrontierScience-Olympiad` + 23 `SWE-bench Verified`)
* **Effective JSONL distribution after overlay**: 40 / 23 / 26 / 26 (FrontierScience-Olympiad
  / SWE-bench Verified / Mind2Web / HumanEval)
* **Non-`benchmark` field diffs vs source**: **0**
* **Cost**: **$0** (local file authoring; no API or compute spend)

## Verification

* `verify_corrections t0015_correct_proxy_benchmark_labels` -> **PASSED** (0 errors, 0
  warnings)
* `aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json` -> overlay
  applies; `description_path` resolves to t0015's relabeled `description.md`; `files[0].path`
  resolves to the relabeled JSONL; `short_description` and `size_description` no longer
  mention `WorkArena++` or `tau-bench`.
* Dataset asset verificator on `hierarchical-annotation-v2-relabeled` -> **PASSED** (0 errors,
  2 warnings inherited from the source schema: missing author country and 4-paragraph Summary
  shape).
* `verify_research_code` -> **PASSED** (0 errors, 0 warnings).
* `verify_plan` -> **PASSED** (0 errors, 0 warnings).
* `verify_task_folder` -> **PASSED** (0 errors, expected warnings about empty `logs/searches/`
  and `corrections/` populated mid-execution).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0015_correct_proxy_benchmark_labels" ---

# Results Detailed: Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Summary

The t0009 v2 hierarchical-annotation dataset inherited a row-level mislabel from the upstream
pipeline. During [t0003] the project chose Mind2Web as a drop-in proxy for the gated
`WorkArena++` split and HumanEval as a drop-in proxy for the gated `tau-bench` split, but the
row-level `benchmark` field was never rewritten to reflect the actual data source. [t0005]'s
v1 pilot reused the slices verbatim, and [t0009]'s v2 re-annotation copied v1's `benchmark`
field unchanged, propagating the mislabel through three tasks. This task overlays the dataset
description and the JSONL via a single `update` correction; **52** of 115 rows now carry the
corrected `benchmark` string, and the dataset aggregator surfaces the corrected labels to all
downstream consumers.

## Methodology

* **Machine**: Local development laptop (Darwin 25.4.0, arm64). No remote machines were used.
* **Runtime**: Total task wall-clock between `task.json` `start_time` and end of step 12 is
  approximately 22 minutes, of which step 9 (implementation) took roughly 5 minutes and the
  remaining time was spent on research, planning, verification, and logging steps.
* **Start timestamp**: `2026-04-30T19:08:28Z` (task start)
* **End timestamp (this step)**: `2026-04-30T19:30:00Z` (results step, approximate)
* **Method**: Authored a single corrections-overlay file targeting the t0009 dataset asset
  `hierarchical-annotation-v2`. The correction uses `action: update` with two effects:
  * `changes` overrides the dataset asset's `short_description` and `size_description` strings
    so the metadata prose no longer references the wrong benchmark names.
  * `file_changes` swaps `description.md` and `files/hierarchical_annotation_v2.jsonl` for
    relabeled copies stored in this task's
    `assets/dataset/hierarchical-annotation-v2-relabeled/` folder. The relabeled JSONL was
    generated by streaming the source JSONL row-by-row, rewriting the `benchmark` field when
    `task_id` started with `m2w_` (`WorkArena++` -> `Mind2Web`) or `he_` (`tau-bench` ->
    `HumanEval`), and leaving the other 63 rows byte-identical. Serialization used
    `json.dumps(row, ensure_ascii=False)` to match the source byte-for-byte.

## Before / After Distribution

| Benchmark label | Before (source `hierarchical_annotation_v2.jsonl`) | After (effective JSONL via overlay) | Delta |
| --- | --- | --- | --- |
| `FrontierScience-Olympiad` | 40 | 40 | 0 |
| `SWE-bench Verified` | 23 | 23 | 0 |
| `WorkArena++` | 26 | 0 | -26 |
| `tau-bench` | 26 | 0 | -26 |
| `Mind2Web` | 0 | 26 | +26 |
| `HumanEval` | 0 | 26 | +26 |
| **Total rows** | **115** | **115** | **0** |

The total row count is preserved exactly. Only the `benchmark` field changes; every other
field (`_pilot_row_index`, `task_id`, `domain`, `difficulty`, `problem`, `hierarchy`,
`gold_actions`, `annotation_model`, `judge_verdict`, `judge_notes`, `hierarchy_completeness`,
`annotator_notes`) is byte-identical to the source on every row.

## Correction-File Structure

The overlay file `corrections/dataset_hierarchical-annotation-v2.json` follows the v3
corrections spec:

* `correction_id`: `C-0015-01`
* `correcting_task`: `t0015_correct_proxy_benchmark_labels`
* `target_task`: `t0009_hierarchical_annotation_v2`
* `target_kind`: `dataset`
* `target_id`: `hierarchical-annotation-v2`
* `action`: `update`
* `changes`: overrides `short_description` and `size_description` with the corrected benchmark
  names (`Mind2Web (proxy for WorkArena++)`, `HumanEval (proxy for tau-bench)`).
* `file_changes`:
  * `description.md` -> replace with this task's
    `assets/dataset/hierarchical-annotation-v2-relabeled/description.md`
  * `files/hierarchical_annotation_v2.jsonl` -> replace with this task's
    `assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
* `rationale`: one paragraph citing [t0003] (proxy decision) and [t0005] (v1 propagation).

The choice of `action: update` over `delete` + `replace` was deliberate: [t0012] (Phase 2 ABC
smoke) and any future Phase 2 task already references the dataset by `dataset_id`
`hierarchical-annotation-v2`, so the overlay must keep that ID stable while swapping its
content.

## Effective Aggregator Output

`aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json` produces the
overlay-merged view. Highlights:

* `description_path`:
  `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md`
* `files[0].path`:
  `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
* `short_description` mentions `Mind2Web (proxy for WorkArena++)` and `HumanEval (proxy for
  tau-bench)`. No mention of `WorkArena++` or `tau-bench` as standalone benchmark names.
* `size_description` lists per-row counts as `40 FrontierScience-Olympiad, 23 SWE-bench
  Verified, 26 Mind2Web (proxy for WorkArena++), 26 HumanEval (proxy for tau-bench)`.

The source dataset folder under [t0009] is untouched; its raw `details.json`, raw
`description.md`, and raw `files/hierarchical_annotation_v2.jsonl` continue to carry the proxy
labels. Downstream consumers that read through the aggregator (the only sanctioned read path)
see the corrected labels; consumers that walk the filesystem directly would still see the
proxy labels, but the framework rule (CLAUDE.md rule 9) forbids that path.

## Verification

* `verify_corrections t0015_correct_proxy_benchmark_labels` -> PASSED (0 errors, 0 warnings).
* `aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json` -> overlay
  applies; corrected metadata and effective files resolve through the overlay.
* Dataset asset verificator on `hierarchical-annotation-v2-relabeled` -> PASSED (0 errors, 2
  warnings inherited from the source schema: missing author country, and 4-paragraph Summary
  shape).
* `verify_research_code` -> PASSED (0 errors, 0 warnings).
* `verify_plan` -> PASSED (0 errors, 0 warnings).
* `verify_task_folder` -> PASSED (0 errors, expected warnings about empty `logs/searches/` and
  `corrections/` populated before the task is marked completed).
* Effective JSONL benchmark distribution: `40 / 23 / 26 / 26` (FrontierScience-Olympiad /
  SWE-bench Verified / Mind2Web / HumanEval).
* Diff vs source: exactly **52** rows changed; only the `benchmark` field differs in any of
  the changed rows.
* `git diff main..HEAD --name-only` confirms zero files outside this task folder were
  modified.

## Limitations

* **Variant b only**: This correction implements suggestion S-0009-06 variant b (label-only
  correction). Variant a (replace the proxy rows with native `WorkArena++` and `tau-bench`
  data) remains an open follow-up — see `results/suggestions.json`. Downstream readers should
  continue to treat per-benchmark numbers for `Mind2Web` and `HumanEval` as approximations of
  the agent-evaluation axes that `WorkArena++` and `tau-bench` cover, rather than as actual
  numbers for those gated benchmarks.
* **No row-level provenance trail**: The relabeled JSONL does not include a separate
  `original_benchmark` field; the row-level provenance is documented only in the overlay's
  `description.md` and `rationale`. A reader who inspects only the effective JSONL will not
  see evidence that the row was previously labeled differently.
* **Aggregator-only correction**: Consumers that read the source JSONL directly (bypassing the
  aggregator) will still see the proxy labels. CLAUDE.md rule 9 forbids that read path, but it
  is not technically blocked.
* **No quantitative experiment results**: This task does not produce predictions, F1 scores,
  or any registered metrics; `metrics.json` is `{}`.

## Files Created

* `tasks/t0015_correct_proxy_benchmark_labels/corrections/dataset_hierarchical-annotation-v2.json`
* `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/details.json`
* `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md`
* `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
* `tasks/t0015_correct_proxy_benchmark_labels/research/research_code.md`
* `tasks/t0015_correct_proxy_benchmark_labels/plan/plan.md`
* `tasks/t0015_correct_proxy_benchmark_labels/results/results_summary.md`
* `tasks/t0015_correct_proxy_benchmark_labels/results/results_detailed.md`
* `tasks/t0015_correct_proxy_benchmark_labels/results/metrics.json`
* `tasks/t0015_correct_proxy_benchmark_labels/results/costs.json`
* `tasks/t0015_correct_proxy_benchmark_labels/results/remote_machines_used.json`
* `tasks/t0015_correct_proxy_benchmark_labels/results/suggestions.json` (written in step 14)
* Step logs under `tasks/t0015_correct_proxy_benchmark_labels/logs/steps/`.

## Task Requirement Coverage

The operative request from `task.json` and `task_description.md`:

```text
Name: Correct proxy-benchmark labels in t0009 v2 dataset

Short description: Write a correction file against the t0009 v2 dataset asset that relabels the
WorkArena++ benchmark to Mind2Web and tau-bench to HumanEval, reflecting the actual proxy sources.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data; editing t0009's task
folder; changing per-row IDs.

Expected Outputs:
* corrections/dataset_<t0009_dataset_id>.json (one or more correction files).
* If file_changes is needed: a replacement description document and/or replacement JSONL under this
  task's assets/dataset/...-relabeled/ folder.
* results/results_summary.md reporting how many rows had their benchmark label corrected and the
  before/after distribution.
* results/results_detailed.md with the rationale, the correction-file structure, and any follow-up
  suggestion to actually replace the proxy rows with native WorkArena++/tau-bench data.

Key questions:
1. How many rows are affected by each label correction?
2. Does the aggregator support per-row label overlays via changes, or is file_changes needed?
3. Are there any downstream consumers (other than t0012) that already cache the original labels?
```

| ID | Requirement | Status | Direct answer | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Relabel `WorkArena++` rows to `Mind2Web` | Done | All **26** rows whose `task_id` starts with `m2w_` carry `benchmark == "Mind2Web"` in the relabeled JSONL. | `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl` (26 of 115 rows) |
| REQ-2 | Relabel `tau-bench` rows to `HumanEval` | Done | All **26** rows whose `task_id` starts with `he_` carry `benchmark == "HumanEval"` in the relabeled JSONL. | Same file (26 of 115 rows) |
| REQ-3 | Use action `update` in the correction file | Done | The single correction file uses `"action": "update"`. | `corrections/dataset_hierarchical-annotation-v2.json` field `action` |
| REQ-4 | Overlay `description_path` and any prose mentioning the wrong labels | Done | `file_changes` replaces `description.md` and the JSONL; `changes` overrides `short_description` and `size_description`. | `corrections/dataset_hierarchical-annotation-v2.json` fields `changes` and `file_changes` |
| REQ-5 | One-paragraph rationale referencing the t0003 / t0005 proxy decision | Done | Single paragraph in the `rationale` field cites [t0003] (proxy decision) and [t0005] (v1 propagation). | `corrections/dataset_hierarchical-annotation-v2.json` field `rationale` |
| REQ-6 | `verify_corrections` passes against the new files | Done | Verificator output: PASSED (0 errors, 0 warnings). | step log `009_implementation/step_log.md` and `logs/commands/` |
| REQ-7 | Confirm corrected labels visible in materialized aggregator output | Done | `aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json` shows the overlay-merged metadata and resolves to t0015's relabeled files. | step log `009_implementation/step_log.md` |
| REQ-8 | Out of scope: do not edit t0009's folder, do not change per-row IDs, do not replace proxy rows with native data | Done | `git diff main..HEAD --name-only` shows zero files outside this task folder; diff of relabeled JSONL vs source shows only the `benchmark` field changes — `_pilot_row_index` and `task_id` are unchanged on every row; no proxy rows were replaced with native data. | `git diff main..HEAD --name-only` output and JSONL diff |
| REQ-9 | Report row counts and before/after distribution | Done | `results/results_summary.md` and the Before/After Distribution table above report the **52** total relabeled rows (26 + 26) and the per-benchmark before/after counts. | `results/results_summary.md` and this file's Before/After Distribution section |
| REQ-10 | Provide a follow-up suggestion to replace proxy rows with native WorkArena++ / tau-bench data | Done | `results/suggestions.json` carries the variant-a follow-up. | `results/suggestions.json` (written in step 14) |

### Direct answers to the three Key Questions

1. **How many rows are affected by each label correction?**
   * `WorkArena++` -> `Mind2Web`: **26** rows.
   * `tau-bench` -> `HumanEval`: **26** rows.
   * Total: **52** of 115 rows.
2. **Does the aggregator support per-row label overlays via `changes`, or is `file_changes`
   needed?** The aggregator's `changes` field overlays only top-level dataset metadata (e.g.,
   `short_description`, `size_description`) — it cannot patch fields inside row records of a
   referenced JSONL file. To rewrite per-row `benchmark` strings the overlay must replace the
   JSONL itself via `file_changes`. This task therefore uses both: `changes` for the prose
   metadata and `file_changes` for `description.md` plus the JSONL.
3. **Are there any downstream consumers (other than t0012) that already cache the original
   labels?** No. As of 2026-04-30, `aggregate_tasks --has-dependency
   t0009_hierarchical_annotation_v2` returns only `t0012_phase2_abc_smoke_frontierscience`
   (in_progress). No other completed task reads the t0009 dataset asset, and no library in the
   project caches the labels separately.

</details>
