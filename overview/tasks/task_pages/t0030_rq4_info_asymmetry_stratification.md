# ⏹ RQ4 info-asymmetry stratification analysis on t0029 outputs

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0030_rq4_info_asymmetry_stratification` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0029_rq1_discordance_rich_resample`](../../../overview/tasks/task_pages/t0029_rq1_discordance_rich_resample.md) |
| **Task types** | `data-analysis`, `answer-question` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0030_rq4_info_asymmetry_stratification/`](../../../tasks/t0030_rq4_info_asymmetry_stratification/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0030_rq4_info_asymmetry_stratification/task_description.md)*

# RQ4 Info-Asymmetry Stratification Analysis

## Motivation

RQ4 asks: **does the gain from granularity-aware scope conditioning concentrate in instances
where information asymmetry between the agent and the task is highest?**

t0027 produced suggestive but underpowered evidence: per-subset success rates were
A=0/B=0.012/C=0.036 on taubench and A=0/B=0.192/C=0.154 on frontsci, hinting that gains might
concentrate in frontsci (where the agent has the largest information gap to close). The total
sample of 12 discordant pairs in t0027 makes any subset-level claim premature.

This task piggy-backs on t0029's discordance-rich resample to deliver an RQ4 verdict at zero
additional API cost: it consumes t0029's predictions and runs a stratified analysis only.

## Scope

In scope:

* Read t0029's predictions assets for arm A and arm B.
* Define "information asymmetry" operationally per subset using existing metadata in
  `t0010_matched_mismatch_library` (e.g., gold-context length, hidden-state count,
  human-judgement disagreement scores).
* Compute per-stratum (subset × asymmetry-tertile) discordant counts and granularity-gain
  rates (B success - A success).
* Run stratified McNemar / proportion tests with Bonferroni correction across the strata.
* Produce a stratification table and at least one figure (subset × asymmetry tertile).
* Write an answer asset for RQ4 with confidence assessment and the explicit caveat if the
  t0029 sample fell short of the >= 30 discordant-pair target.

Out of scope:

* Any new API calls or remote compute.
* RQ1 verdict (delivered by t0029).
* RQ5 verdict (deferred to a later wave).
* Building a new info-asymmetry metric — reuse only what is already in
  `t0010_matched_mismatch_library` and t0027's harness logs.

## Method

1. Load t0029 predictions for arm A and arm B keyed by paired instance ID.
2. Join against `t0010_matched_mismatch_library` to recover per-instance metadata (subset,
   asymmetry signals).
3. Define info-asymmetry tertiles per subset (low / mid / high) using the chosen signal.
4. Compute granularity-gain rate per stratum: `success_rate(B) - success_rate(A)`.
5. Test the joint hypothesis "gain rate is higher in high-asymmetry strata than low-asymmetry
   strata" via stratified McNemar (per subset) plus a Cochran-Mantel-Haenszel-style overall
   test, with Bonferroni-adjusted alpha = 0.025.
6. Write the answer asset following `meta/asset_types/answer/specification.md`.

## Deliverables

* `assets/answer/rq4-info-asymmetry-stratification/` answer asset with a confidence rating and
  the verdict (full / partial / inconclusive).
* `results/results_summary.md` and `results/results_detailed.md` with the stratification table
  and figure embedded.
* `results/metrics.json` with per-stratum granularity-gain rates and the joint test p value.
* `results/images/rq4_stratification.png` (subset × asymmetry tertile heatmap or grouped bar).

## Cross-references

* Source: t0028 brainstorm session 8.
* Depends on: t0029.
* Builds on: t0010_matched_mismatch_library (subset metadata).
* Source suggestion: none (analysis-only follow-up).

</details>
