# ⏹ v2 annotator Sonnet rerun: deconfound schema vs model

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0014_v2_annotator_sonnet_rerun` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source suggestion** | `S-0009-01` |
| **Task types** | `hierarchical-annotation`, `comparative-analysis` |
| **Expected assets** | 1 dataset |
| **Task folder** | [`t0014_v2_annotator_sonnet_rerun/`](../../../tasks/t0014_v2_annotator_sonnet_rerun/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0014_v2_annotator_sonnet_rerun/task_description.md)*

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
