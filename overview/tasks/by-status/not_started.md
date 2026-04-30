# ⏹ Tasks: Not Started

2 tasks. ⏹ **2 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0015 — <strong>Correct proxy-benchmark labels in t0009 v2
dataset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_correct_proxy_benchmark_labels` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0009-06` |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Task page** | [Correct proxy-benchmark labels in t0009 v2 dataset](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Task folder** | [`t0015_correct_proxy_benchmark_labels/`](../../../tasks/t0015_correct_proxy_benchmark_labels/) |

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

<details>
<summary>⏹ 0014 — <strong>v2 annotator Sonnet rerun: deconfound schema vs
model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0014_v2_annotator_sonnet_rerun` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0009-01` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Task page** | [v2 annotator Sonnet rerun: deconfound schema vs model](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Task folder** | [`t0014_v2_annotator_sonnet_rerun/`](../../../tasks/t0014_v2_annotator_sonnet_rerun/) |

# v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)

## Motivation

`t0009_hierarchical_annotation_v2` reports a v2-vs-v1 judge accept-rate delta of approximately
+58 pp on the stratified haiku-judged sample. The v1 annotator was `claude-sonnet-4-6`; the v2
annotator was switched to `claude-haiku-4-5-20251001` mid-task to fit the cost budget. The
judge model was constant (`claude-haiku-4-5-20251001`). The +58 pp number therefore conflates
two effects:

* schema effect: tree decomposition with subtask-to-atomic edges and full problem text;
* model effect: switching annotator from Sonnet to Haiku.

Without isolating the schema component, the headline claim that "v2 unblocks Phase 2" rests on
a load-bearing-but-unverified assumption. `t0012` (Phase 2 A/B/C smoke on FrontierScience) is
already in flight against the v2 dataset, so this deconfound is needed before any
per-benchmark numbers from t0012 can be reported. Implements `S-0009-01`.

## Scope

* Re-annotate the **same 115 rows** under the same v2 tree schema using `claude-sonnet-4-6` as
  the annotator.
* Use the **same prompt** as t0009 (full problem text, tree-schema system instructions).
* Judge with **the same `claude-haiku-4-5-20251001`** judge on the **same 23-row stratified
  sample** used in t0009 (same row IDs, same seed=42).
* Report per-benchmark and aggregate judge accept rate. Compare against v2-haiku and v1-sonnet
  to decompose the +58 pp delta into a schema component and a model component.
* Persist as a new `dataset` asset under `assets/dataset/hierarchical-annotation-v2-sonnet/`
  with `details.json`, `description.md`, and `files/hierarchical_annotation_v2_sonnet.jsonl`.

Out of scope: re-judging on a different sample, re-running v1 (already in t0005), changing the
schema, expanding row count, fixing the proxy-benchmark labels (handled by `t0015`).

## Approach

1. Read t0009's v2 dataset asset and the original 115 v1 rows from t0005's dataset asset.
2. Construct a v2 annotation prompt (identical to t0009's) with the full problem text and the
   v2 tree schema in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree
   per row.
3. Apply the same task_id deduplication fix used in t0009.
4. Recover the same stratified sample IDs from t0009's results (seed=42, stratified across
   FrontierScience-Olympiad, SWE-bench Verified, and the two proxy benchmarks). Run the haiku
   judge on the v2-sonnet hierarchies for those rows.
5. Persist the dataset asset with `annotation_model: "claude-sonnet-4-6"`. Annotate the
   `description.md` with the deconfound experimental design and the comparison protocol.
6. Compute the three accept-rate deltas:
   * v2-sonnet vs v1-sonnet → schema component (annotator constant).
   * v2-sonnet vs v2-haiku → annotator-model component (schema constant).
   * v2-haiku vs v1-sonnet → original t0009 headline (for sanity check).

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2-sonnet/{details.json, description.md, files/}`.
* `results/results_summary.md` reporting the three deltas with confidence intervals.
* `results/results_detailed.md` with per-row judge verdicts and per-benchmark breakdowns.
* `results/metrics.json` reporting `judge_accept_rate_v2_sonnet` (aggregate) plus
  per-benchmark variants if the metrics registry supports them.
* Follow-up suggestions if the schema component turns out to be small (motivating a v3 schema
  iteration) or the model swap dominates (motivating a Sonnet-default annotation policy).

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$5** (115 sonnet annotations at the same prompt
length as t0009's haiku run + 23 haiku judge calls reusing the same protocol). Per-task cap:
$10.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the v2 schema, the prompt, the stratified
  sample IDs, and the v2-haiku baseline accept rates.
* Independent of `t0015_correct_proxy_benchmark_labels`. Either order is fine, but if t0015
  lands first, this task should consume the corrected labels in its per-benchmark breakdown
  via the aggregator's correction overlay.
* `t0012` (in_progress) is unaffected — its FrontierScience filter and pre-locked v2 inputs do
  not change retroactively when this task lands.

## Source Suggestion

`S-0009-01` — "Re-run v2 annotation with claude-sonnet-4-6 to isolate the schema effect from
the annotator-model swap."

## Key Questions

1. What is the per-benchmark accept-rate delta of v2-sonnet vs v2-haiku (annotator-model
   component)?
2. What is the per-benchmark accept-rate delta of v2-sonnet vs v1-sonnet (schema component)?
3. Does the FrontierScience-Olympiad benchmark — the worst performer in v1 — improve under
   v2-sonnet? By how much vs the t0009 v2-haiku improvement?
4. If the schema component is small, is there a v3 schema change worth scoping, and should
   t0012's smoke be paused until that lands?

</details>
