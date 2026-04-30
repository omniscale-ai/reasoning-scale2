# Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Motivation

The `t0009_hierarchical_annotation_v2` dataset asset labels its four benchmarks as
`FrontierScience-Olympiad`, `SWE-bench Verified`, `WorkArena++`, and `tau-bench`. The first two are
accurate. The latter two are mislabelled — the underlying rows are `Mind2Web` and `HumanEval` rows
used as proxies for browser-using and tool-using agent benchmarks, not actual `WorkArena++` or
`tau-bench` rows. Once t0012 (Phase 2 A/B/C smoke) reports per-benchmark numbers, naïve consumers
would attribute results to benchmarks the project does not actually evaluate on.

This task fixes the labels via the corrections-overlay mechanism — no re-annotation, no API spend,
no change to the t0009 task folder. Implements `S-0009-06` variant b (label correction; variant a
would have replaced the proxy rows with actual WorkArena++/tau-bench data, which is out of scope for
this wave).

## Scope

* Write one correction file per affected benchmark (or one combined correction, depending on the
  aggregator's per-row update support):
  * `WorkArena++` → `Mind2Web`.
  * `tau-bench` → `HumanEval`.
* Action: `update`. The correction overlays `details.json` `description_path` (and any per-row
  `benchmark` fields exposed by the dataset aggregator) so downstream consumers see the corrected
  labels.
* Provide a one-paragraph rationale per correction file referencing the original proxy decision
  taken in t0003 (benchmark download) and t0005 (v1 annotation pilot).
* Run `verify_corrections` against the new files.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data (a separate dataset task,
deferred); editing t0009's task folder (immutable); changing per-row IDs (only the benchmark label).

## Approach

1. Read t0009's `assets/dataset/hierarchical-annotation-v2/details.json` and the dataset aggregator
   schema to confirm where benchmark labels are exposed (top-level `benchmarks` list, per-row
   `benchmark` field, or both).
2. Confirm the dataset aggregator's correction-overlay support — if `file_changes` is required,
   author a replacement description document and (if applicable) replacement JSONL with corrected
   per-row labels.
3. Write the correction file(s) under `corrections/dataset_<dataset_id>.json` per
   `corrections_specification.md` v3.
4. Re-run the dataset aggregator with the correction overlay applied; confirm the corrected labels
   are visible in the materialized output.

## Expected Outputs

* `corrections/dataset_<t0009_dataset_id>.json` (one or more correction files).
* If `file_changes` is needed: a replacement description document and/or replacement JSONL under
  this task's `assets/dataset/...-relabeled/` folder.
* `results/results_summary.md` reporting how many rows had their benchmark label corrected and the
  before/after distribution.
* `results/results_detailed.md` with the rationale, the correction-file structure, and any follow-up
  suggestion to actually replace the proxy rows with native WorkArena++/tau-bench data.

## Compute and Budget

No GPU. No API spend. Estimated cost: **$0**. Per-task cap: $1.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the dataset asset whose labels are being
  corrected.
* Independent of `t0014_v2_annotator_sonnet_rerun`. Order does not matter; if both land before t0012
  finishes, t0012's per-benchmark reporting will pick up both overlays through the aggregator.
* `t0012` (in_progress) reads the t0009 dataset through the aggregator, so the corrected labels flow
  through automatically once t0015 merges. The FrontierScience filter t0012 uses is unaffected.

## Source Suggestion

`S-0009-06` variant b — "Relabel the proxy benchmarks WorkArena++→Mind2Web and tau-bench→HumanEval
in the v2 dataset via a correction file."

## Key Questions

1. How many rows are affected by each label correction?
2. Does the t0009 dataset aggregator support per-row label overlays via `changes`, or is a
   `file_changes` overlay needed?
3. Are there any downstream consumers (other than t0012) that already cache the original labels and
   would need re-aggregation?
