---
spec_version: "2"
predictions_id: "abc-rerun-a-reused"
documented_by_task: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_documented: "2026-05-02"
---
# Variant A (Reused Pointer to t0026 a-scope-aware Predictions)

## Metadata

* **Variant**: a (reused; not re-run)
* **Source predictions asset**: `t0026_phase2_abc_runtime_n147_for_rq1_rq5/a-scope-aware`
* **Source JSONL**:
  `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/a-scope-aware/files/predictions_variant_a.jsonl`
* **Model**: claude-sonnet-4-6 (Anthropic CLI transport, 10-turn cap, 4096 max output tokens)
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances inherited**: 147 (from t0026); the t0027 paired analysis filters to 130
* **Created by**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c

## Overview

This predictions asset is a *pointer*. It exists to satisfy the t0027 task's expected_assets
contract (`predictions: 3`) while making explicit that variant A is not re-run in this task. The
t0027 task description directs that "A is not re-run; t0026's A trajectories are valid for this
paired analysis. We re-use them by reference rather than re-generating." The actual per-instance
predictions live unchanged in t0026's `a-scope-aware` predictions asset; this folder contains only a
pointer JSON file that names the source path. Consumers (the McNemar analysis script, calibration
script, plotting scripts) read the source JSONL path directly. No prediction data is duplicated into
this asset.

## Model

claude-sonnet-4-6, accessed via the Anthropic CLI transport with a 10-turn ReAct cap and 4096 max
output tokens per call. The agent runs the scope-aware ReAct scaffold from t0010 with atomic
granularity. Configuration is inherited verbatim from t0026's `a-scope-aware` asset. The t0027
re-run uses **claude-sonnet-4-6** for variants B and C as well, so all three variants share the same
model. The original t0027 task description erroneously stated claude-opus-4-7 for B/C; that was a
transcription error and was corrected after discovering the mismatch via t0026's `paths.py` and
trajectory error messages. The A-vs-B and A-vs-C McNemar comparisons in t0027 are therefore clean
same-model contrasts (different scaffolds, same model).

## Data

The 147 inherited instances span SWE-bench Verified (20, stratified by difficulty bucket), Tau-bench
(87, deterministic by domain+task_index), and FrontierScience Olympiad (40, deterministic by
task_id). The exact instance IDs and source SHA-256 hashes are recorded in t0026's
`data/instance_manifest.json`. The t0027 paired analysis filters to the **130 paired instances** —
the intersection of all three t0026 variants' completed instances (instances where every variant
returned a non-null final answer or judge verdict).

## Prediction Format

JSON Lines — one JSON object per line. Each row carries: `instance_id` (str), `subset` (str),
`variant` (str), `final_answer` (str|null), `final_confidence` (float|null; null for variant A
because A does not elicit verbalised confidence), `cost_usd` (float), `trajectory_path` (str|null),
`judge_sonnet_success` (bool), `judge_sonnet_rationale` (str), `judge_opus_success` (bool|null;
non-null only on the inter-judge subset of 30 instances), `judge_opus_rationale` (str|null). The
schema is identical to the t0026 source asset.

This asset's `files/pointer.json` is a small JSON object pointing back to the t0026 source path; it
is not the prediction data. Consumers must read the t0026 source JSONL listed in the Metadata
section to access the actual records.

## Metrics

* Success rate (sonnet judge, all 147 t0026 instances): **0.0408** (6/147)
* Success rate restricted to the 130 paired instances used in t0027's analysis: computed on the fly
  by the t0027 analysis script (`code/run_analysis.py`); see `data/mcnemar_results.json` for the
  exact paired contingency tables and per-subset success-rate breakdowns
* Cost per instance (t0026 inherited): **$0.0313**
* Re-run cost in t0027: **$0** (no API calls; predictions are reused by reference)

## Main Ideas

* **No re-run, no duplication.** The t0027 task description directs that A be reused by reference;
  the actual JSONL is not copied into this asset. The pointer file records the source path so
  downstream consumers can locate it without ambiguity.
* **No mixed-model confound.** All three variants (A, B, C) use claude-sonnet-4-6. The original
  t0027 task description stated claude-opus-4-7 for B/C, but that was a transcription error caught
  during implementation by inspecting t0026's `paths.py` and trajectory error messages. With the
  corrected model, the A-vs-B and A-vs-C McNemar comparisons isolate scaffold/parser differences
  cleanly. Re-running A was unnecessary because t0026's A trajectories were already on the correct
  model.
* **Filtering to the 130 paired set is performed at analysis time.** The pointer asset itself
  reports the inherited count (147) for traceability with t0026; the McNemar test runs on the paired
  intersection of 130. The exact paired set is computed by `code/run_analysis.py` from the three
  variants' JSONL files at run time.

## Summary

This is a pointer-only predictions asset. Variant A's per-instance predictions, trajectories, and
judge verdicts are inherited verbatim from t0026's `a-scope-aware` asset; nothing is re-generated in
t0027. The `files/pointer.json` file names the source predictions directory and the source JSONL so
the McNemar analysis script and calibration script can locate the underlying records by reading the
canonical t0026 path directly. The t0027 paired analysis filters the inherited 147 instances to the
130 paired set defined as the intersection of all three t0026 variants' completed instances.

The asset exists to make explicit, in the t0027 expected_assets contract, that variant A is part of
the analysis but is not produced by this task. All three variants share claude-sonnet-4-6, so the
A-vs-B McNemar in t0027 is a clean "same model, different scaffold" comparison and the A-vs-C
McNemar is a "same model, different scaffold + granularity-mismatch wrapper" comparison.
