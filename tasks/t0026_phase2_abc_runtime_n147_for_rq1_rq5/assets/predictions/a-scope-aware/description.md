---
spec_version: "2"
predictions_id: "a-scope-aware"
documented_by_task: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
date_documented: "2026-05-02"
---

# Variant A: Scope-Aware ReAct (atomic granularity)

## Metadata

* **Variant**: a
* **Model**: claude-sonnet-4-6
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 147
* **Created by**: t0026_phase2_abc_runtime_n147_for_rq1_rq5

## Overview

Scope-Aware ReAct agent operating at atomic granularity over a paired N=147 instance manifest spanning SWE-bench Verified, Tau-bench, and FrontierScience Olympiad. Each prediction includes the agent's final answer, the trajectory path, the per-instance cost, and primary sonnet judge verdicts. A subset of 30 instances also carries an opus inter-judge verdict for inter-rater agreement.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs use a 10-turn cap with 4096 max output tokens per call.

## Data

The paired N=147 manifest spans 20 SWE-bench Verified instances (stratified by difficulty bucket), 87 Tau-bench instances (deterministic by domain+task_index), and 40 FrontierScience Olympiad instances (deterministic by task_id). The manifest `data/instance_manifest.json` records the exact instance IDs and source SHA-256 hashes per subset.

## Prediction Format

JSON Lines. Each row has: instance_id, subset, variant, final_answer (nullable), final_confidence (nullable; only populated for variant B), cost_usd, trajectory_path, judge_sonnet_success, judge_sonnet_rationale, judge_opus_success (nullable; non-null only for the inter-judge sample), judge_opus_rationale (nullable).

## Metrics

* Success rate (sonnet judge, all subsets): **0.0408**
* Cost per instance: **$0.0313**

Per-subset breakdown:

* swebench: n=20, n_success=6, success_rate=0.3000
* taubench: n=87, n_success=0, success_rate=0.0000
* frontsci: n=40, n_success=0, success_rate=0.0000

## Main Ideas

* These predictions provide the runtime evidence base for RQ1-RQ5 in t0026 — calibration (RQ1-RQ2), judge agreement (RQ3-RQ4), and strict A>B>C ordering (RQ5) are all computed from these JSONL files.
* Judge verdicts attached inline avoid recomputing judge calls across downstream tasks; opus inter-judge subset enables inter-rater agreement without a full opus pass.
* Empty or null final_answer entries are recorded honestly and judged as FAIL by the substantive prompt; downstream analyses can treat them as legitimate failures rather than missing data.

## Summary

This predictions asset captures variant a runs across the paired N=147 manifest under the claude-sonnet-4-6 model. The trajectory files in `data/runs/a/` contain the full action history; the JSONL here is the analysis-ready summary with judge verdicts joined inline. Together with `assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}` for the other two variants, this asset supplies the full dataset used in `results/metrics.json` and the per-research-question comparisons reported in `results/results_detailed.md`.
