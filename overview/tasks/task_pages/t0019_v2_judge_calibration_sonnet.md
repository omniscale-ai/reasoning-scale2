# ✅ v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

[Back to all tasks](../README.md)

> Task Success Rate: **1.0**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0019_v2_judge_calibration_sonnet` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T14:02:34Z |
| **Completed** | 2026-05-01T17:55:02Z |
| **Duration** | 3h 52m |
| **Source suggestion** | `S-0014-02` |
| **Task types** | `comparative-analysis`, `data-analysis` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`hierarchical-planning`](../../by-category/hierarchical-planning.md), [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Step progress** | 10/15 |
| **Cost** | **$19.30** |
| **Task folder** | [`t0019_v2_judge_calibration_sonnet/`](../../../tasks/t0019_v2_judge_calibration_sonnet/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/task_description.md)*

# v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

## Motivation

t0014 produced a schema-only delta of **+57 pp** for v2 over v1, well above Zhou2022's +16 pp
and Boisvert2024's +25 pp published bands, and a model-only delta of **-1 pp** that sits below
Xiong2024's lower edge (0 pp). Two plausible threats to validity remain:

1. **Judge anchoring** (S-0014-02): the haiku judge may be partially scoring "the model
   produced a parseable tree with subtask-to-atomic edges" rather than "the decomposition is
   substantively right". If so, the +57 pp gap to literature is a judge artefact, not a schema
   effect.
2. **Familial bias** (S-0014-03): the haiku judge gives the v2-haiku annotator a same-family
   agreement bonus (~5-10 pp per Xiong2024). If so, the -1 pp model-only delta is masking a
   real sonnet annotator advantage.

Both threats can be tested at the same 43-row pool used in t0014 by swapping the judge prompt
and judge model. Defending the +57 pp schema-only headline before scaling to a confirmatory
experiment is the cheapest paper-defensible step on the critical path.

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary).

## Scope

Re-judge **the same 43 v2 rows** that t0014 produced (20 v2-sonnet + 23 v2-haiku) plus the
matched 20 v1-sonnet rows from t0009/t0014, under two new judge configurations:

* **Substantive critic** prompt (S-0014-02): the judge simulates execution ("verify each
  atomic, executed in order, would actually solve the problem") and outputs a binary
  accept/reject plus a per-criterion sub-score.
* **Model-rotated** judge (S-0014-03): keep the original t0014 judge prompt, swap the judge
  model from haiku to claude-sonnet-4-6.

Both judges run against the same row pool. Combined output is a 4-condition matrix per row:

| Condition | Annotator | Judge Prompt | Judge Model |
| --- | --- | --- | --- |
| Baseline (from t0014) | v1-sonnet / v2-haiku / v2-sonnet | original | haiku |
| Substantive | v1-sonnet / v2-haiku / v2-sonnet | substantive critic | sonnet |
| Model-rotated | v1-sonnet / v2-haiku / v2-sonnet | original | sonnet |

This task does not re-annotate. It only re-judges. Annotation rows from t0014 are read in via
the existing predictions overlay applied by t0015.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_judge_calibration/`): per-row judge verdicts
   under the substantive and model-rotated conditions, plus the cached baseline t0014/t0015
   verdicts as reference. Includes prompt-version and judge-model fields per row.
2. **Answer asset** (`assets/answer/.../`) addressing the question: "Does the v2 schema retain
   a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or
   is the +57 pp t0014 headline an artefact of haiku judge anchoring?"
3. **Reported metrics** in `results/metrics.json` using the explicit multi-variant format, one
   variant per (annotator x judge-prompt x judge-model) cell. Each cell reports:
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Comparison table** in `results/results_detailed.md` showing the schema-only and
   model-only deltas under all three judge configurations side by side, with explicit deltas
   vs t0014.

## Models and Configurations

* **Annotator outputs** (already produced; not re-run): claude-sonnet-4-6 v1 (20 rows), haiku
  v2 (23 rows), sonnet v2 (20 rows). All from t0014.
* **Substantive critic judge**: claude-sonnet-4-6 with the new prompt template.
* **Model-rotated judge**: claude-sonnet-4-6 with the original t0014 judge prompt.

Total judge calls: 43 rows x 2 new judge configurations = **86 sonnet judge calls**.

## Cost Estimate

* Sonnet input ~5k tokens per call x 86 = **~430k input tokens**.
* Sonnet output ~600 tokens per call x 86 = **~52k output tokens**.
* At claude-sonnet-4-6 pricing (approximately $3/M in, $15/M out): **about $2.05** sonnet
  spend.
* Reserve for retry/repair: **+$1**.
* Total: **~$3-5**.

This sits well within the remaining $51 budget.

## Decision Criteria

After this task:

* If schema-only delta drops below **+30 pp** under the substantive judge, the +57 pp t0014
  headline is partly judge-anchoring; reset the headline to the substantive number and revisit
  S-0014-01 (v3 schema iteration).
* If schema-only delta stays at or above **+45 pp** under both new judges, the schema effect
  is robust; commit to the t0023 confirmatory run as planned.
* If model-only delta swings to **at least +5 pp** under the sonnet judge, the t0014 -1 pp
  result is a haiku familial bias, and v2-sonnet should be the production annotator going
  forward.
* If model-only delta stays within +/-2 pp under the sonnet judge, the v2 schema does the work
  and sonnet annotation is not worth the cost premium.

## Dependencies

None on uncompleted tasks. Reads from t0014's predictions and t0015's correction overlay; both
are merged.

## Source Suggestion

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary). Both suggestions remain
active as `source_suggestion` until t0019 results are merged; the secondary will be marked
covered in the next brainstorm round if the data answers it.

## Risks and Fallbacks

* **Substantive judge is slow or unstable**: if per-row judge time exceeds 30 s, drop
  sub-criteria and use a binary verdict only.
* **Sonnet judge disagrees with itself across the two prompt variants on the same row**: log
  per-row agreement; report Cohen's kappa across (substantive, model-rotated) at the same
  model. This is a free signal about prompt-vs-anchoring effects.
* **The t0014 row pool has masked instances** (we know 3 sonnet timeouts exist; S-0014-05 was
  rejected): exclude those rows from all conditions consistently and report the effective n.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` contains all 9 cells (3 annotators x 3 judge configs) with
  accept_rate and stderr.
* `results/results_detailed.md` contains a side-by-side delta table and an explicit
  decision-criteria check-off against the four bullets above.
* Cost in `results/costs.json` is at or below **$5**.

</details>

## Costs

**Total**: **$19.30**

| Category | Amount |
|----------|--------|
| substantive_sonnet_judge | $9.68 |
| model_rotated_sonnet_judge | $9.63 |

## Metrics

### v1-sonnet judged by original-haiku

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.3333** |

### v1-sonnet judged by substantive-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.6667** |

### v1-sonnet judged by model-rotated-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.5833** |

### v2-haiku judged by original-haiku

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.913** |

### v2-haiku judged by substantive-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.913** |

### v2-haiku judged by model-rotated-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.9565** |

### v2-sonnet judged by original-haiku

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.9** |

### v2-sonnet judged by substantive-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **1.0** |

### v2-sonnet judged by model-rotated-sonnet

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **1.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring?](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/) | [`full_answer.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md) |
| predictions | [v2 Judge Calibration: 3 judges x 3 annotators on 55-row pool](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/predictions/v2-judge-calibration/) | [`description.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/predictions/v2-judge-calibration/description.md) |

## Suggestions Generated

<details>
<summary><strong>Confirmatory v2 vs v1 schema sweep with fresh annotations and a
third sonnet judge</strong> (S-0019-01)</summary>

**Kind**: experiment | **Priority**: high

Run a confirmatory experiment that re-annotates a fresh n>=80 row pool (not the t0014 pool)
under the v1 and v2 schemas with claude-sonnet-4-6 as annotator, then judges with three
independent sonnet configurations: substantive critic, model-rotated original prompt, and a
new criterion-decomposed rubric judge. The current task left the +24.6 / +37.3 pp delta band
unsettled because the two judge configurations disagreed on the +30 pp threshold and the pool
overlapped with t0014. A fresh-pool replication at the planned n>=80 would tighten the
per-cell Wilson CIs from +/-24 pp to +/-11 pp, enough to either reset the headline below +30
pp or commit it above +45 pp.

</details>

<details>
<summary><strong>Provision a sonnet-quota Anthropic API key to drop per-call cost
~7x</strong> (S-0019-02)</summary>

**Kind**: library | **Priority**: medium

Acquire an Anthropic API key with claude-sonnet-4-6 quota and switch JUDGE_TRANSPORT back from
the claude CLI subprocess to the Anthropic SDK. The current OAuth-issued key in this
environment lacks sonnet quota, forcing the CLI fallback at ~$0.18/call (cache-creation
overhead) instead of the ~$0.024/call SDK + cache-hit projection. Provisioning a
sonnet-capable key would let S-0019-01's confirmatory sweep run within the original $5 budget
envelope and unblock larger-n experiments without per-task cap raises. This is a project-level
service request, not a research experiment.

</details>

<details>
<summary><strong>Substantive critic vs original prompt: 50-row prompt-only ablation
at fixed model</strong> (S-0019-03)</summary>

**Kind**: evaluation | **Priority**: medium

Run a focused n=50 ablation that holds the judge model fixed at claude-sonnet-4-6 and varies
only the system prompt between the substantive critic (with simulate-execution instruction)
and the original t0014 prompt. The current task found a Cohen's kappa of 0.626 between the two
prompts on the same model, with one row (v2-haiku-0007) where the substantive prompt caught a
dimensional-analysis error the original prompt missed and two rows (v1-sonnet-0002,
v1-sonnet-0004) where the substantive prompt accepted structural-but-executable trees the
original rejected. A larger ablation would quantify how often each prompt mode wins, which
would inform whether the substantive critic should become the production judge or stay as a
stricter audit.

</details>

<details>
<summary><strong>Cross-vendor judge: replicate the schema-only delta with GPT-4
and Gemini judges</strong> (S-0019-04)</summary>

**Kind**: experiment | **Priority**: low

Test the family-bias hypothesis at the judge stage by re-judging the same 55-row pool under
GPT-4o and Gemini-2.5 with the same substantive critic prompt, and comparing the schema-only
delta to the +24.6 / +37.3 pp Anthropic numbers from this task. Xiong2024 reports
within-family acceptance bonuses of 5-10 pp; if the cross-vendor schema-only delta lands close
to the substantive-sonnet +24.6 pp, the v2-sonnet familial bias hypothesis (kappa=1.0 on the
v2-sonnet cell) gains support; if it lands close to +37 pp, prompt strictness dominates over
model family.

</details>

## Research

* [`research_code.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/results/results_summary.md)*

# Results Summary: v2 Judge Calibration with Sonnet

## Summary

Re-judged the same 55-row hierarchy pool from t0014 (12 v1-sonnet + 23 v2-haiku + 20
v2-sonnet) under three judge configurations: the cached t0014 original-haiku verdicts as
baseline, a substantive critic prompt on `claude-sonnet-4-6`, and a model-rotated
original-prompt judge on `claude-sonnet-4-6`. The headline finding is that the +57 pp v2-vs-v1
schema-only gap from t0014 **partially survives** under sonnet judges: **+24.6 pp** under the
substantive critic and **+37.3 pp** under the model-rotated judge, vs the **+58.0 pp**
baseline. Neither pre-registered extreme decision criterion (drops below +30 pp on both sonnet
judges, or stays at or above +45 pp on both) was simultaneously satisfied, so the answer is
**Mixed / low confidence**.

## Methodology

* 110 fresh sonnet judge calls (55 substantive + 55 model-rotated) via the local `claude` CLI
  subprocess; the OAuth-issued ANTHROPIC_API_KEY in this environment lacks sonnet quota, so
  `intervention/critical_step_blocked.md` was filed and option 2 was authorised: raise the
  budget cap from $4.50 to $20.00 and switch transport from the Anthropic SDK to a `claude`
  CLI subprocess wrapper. The change is locked in `code/constants.py` (`BUDGET_CAP_USD =
  20.00`, `JUDGE_TRANSPORT = "cli"` default) and documented in
  `intervention/critical_step_blocked.md`.
* All 110 calls returned valid JSON envelopes (0 parse failures, 0 call failures, 0 budget
  halts). Total spend was **$19.30** ($9.68 substantive, $9.63 model-rotated), comfortably
  within the raised $20 cap but ~4.3x the original $4.50 plan.
* Per-cell binary acceptance rates and Wilson 95% CIs, plus schema-only and model-only deltas
  under each judge, are emitted to `results/metrics.json` (explicit multi-variant format,
  registered metric only) and `data/computed_stats.json` (full audit).
* Cohen's kappa between the two sonnet judges overall: **0.626** (moderate agreement), with
  per-annotator kappas of 0.47 (v1-sonnet), 0.65 (v2-haiku), and 1.00 (v2-sonnet).

## Metrics

* **Schema-only delta (v2-haiku - v1-sonnet)** under each judge: **+58.0 pp** (baseline
  haiku), **+24.6 pp** (substantive sonnet), **+37.3 pp** (model-rotated sonnet).
* **Model-only delta (v2-sonnet - v2-haiku)** under each judge: **-1.3 pp** (baseline haiku),
  **+8.7 pp** (substantive sonnet), **+4.3 pp** (model-rotated sonnet).
* **Per-cell accept rates**: v1-sonnet 33.3% / 66.7% / 58.3% (haiku / substantive / rotated);
  v2-haiku 91.3% / 91.3% / 95.7%; v2-sonnet 90.0% / 100.0% / 100.0%.
* **Average per-call sonnet cost**: **$0.176/call** (vs SDK + cache-hit projection of
  ~$0.024/call in `intervention/critical_step_blocked.md`); average sonnet latency **~14
  s/call**.
* **Cohen's kappa overall** between substantive and model-rotated sonnet: **0.626**.
* **Total cost**: **$19.30** of a **$20.00** raised cap (vs original $4.50 plan ceiling).

## Verification

* `verify_task_file.py` — PASSED (logs in `logs/steps/015_reporting/`)
* `verify_logs.py` — PASSED
* `verify_task_results.py` — PASSED
* `verify_predictions_asset.py` — PASSED
* `verify_answer_asset.py` — PASSED
* `verify_task_metrics.py` — PASSED
* `verify_step_tracker.py` — PASSED

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0019_v2_judge_calibration_sonnet" ---
# Detailed Results: v2 Judge Calibration with Sonnet

## Summary

Re-judged the same 55-row hierarchy pool from t0014 (12 v1-sonnet + 23 v2-haiku + 20
v2-sonnet) under three judge configurations: the cached t0014 original-haiku verdicts as
baseline, a substantive critic prompt on `claude-sonnet-4-6`, and a model-rotated
original-prompt judge on `claude-sonnet-4-6`. The +57 pp v2-vs-v1 schema-only gap from t0014
partially survives both sonnet judges (**+24.6 pp** substantive, **+37.3 pp** model-rotated,
vs **+58.0 pp** baseline), and neither pre-registered extreme decision criterion (drop below
+30 pp on both, or stay at or above +45 pp on both) was simultaneously satisfied; the answer
is **Mixed / low confidence**.

## Methodology

* **Machine**: Apple M-series laptop (`darwin` arm64, Python 3.13.5 via `uv`); no remote
  machines.
* **Wall-clock runtime**: ~26 minutes total spread across the validation gate, the substantive
  full sweep, and the model-rotated full sweep (per `data/*_outcomes.jsonl` timestamps).
* **Start / end timestamps**: started 2026-05-01T14:02:34Z (`task.json` `start_time`); the
  last judge call landed at 2026-05-01T17:39:42Z (per `data/computed_stats.json`
  `generated_at_utc`, written immediately after the last successful run).
* **Models**: judge model `claude-sonnet-4-6` for both sonnet variants; `claude-haiku-4-5`
  baseline is read from cached `judge_verdict` fields written by t0014 / t0005. Pricing: $3/M
  input, $15/M output (`code/constants.py`).
* **Transport**: the OAuth-issued `ANTHROPIC_API_KEY` in this environment is provisioned only
  for haiku quota; every call to `claude-sonnet-4-6` returned `RateLimitError 429`. Per
  option-2 in `intervention/critical_step_blocked.md` the budget cap was raised from $4.50 to
  $20.00 and the judge transport switched from the Anthropic SDK to the local `claude` CLI
  subprocess (which routes through the user's Claude Code subscription). The transport is a
  constant (`code/constants.py` `JUDGE_TRANSPORT = "cli"`).
* **Pool**: 55 rows total (12 v1-sonnet from `t0005_hierarchical_annotation_pilot_v1`, 23
  v2-haiku from `t0009_hierarchical_annotation_v2` with the `t0015` benchmark-label correction
  overlay applied, and 20 v2-sonnet from `t0014_v2_annotator_sonnet_rerun`). Pool assembly is
  in `code/data_loader.py`.
* **Prompts**: substantive critic system prompt extends the original t0014 judge with an
  explicit "mentally simulate executing the atomics in the listed order" instruction and an
  optional `sub_scores` schema; the model-rotated config uses the original t0014 prompt
  verbatim. Both prompts are in `code/constants.py`.
* **Run script**: `code/run_substantive.py` (validation gate + 50-row sweep) and
  `code/run_model_rotated.py` (full 55-row sweep, no separate gate because the substantive
  gate already validated parsing and per-call cost). Idempotent JSONL append output written to
  `data/substantive_outcomes.jsonl` and `data/model_rotated_outcomes.jsonl`.
* **Statistics**: per-cell binary acceptance rate, Wilson 95% CI (`code/stats.py`
  `wilson_ci`), schema-only delta (v2-haiku - v1-sonnet) and model-only delta (v2-sonnet -
  v2-haiku) with delta CIs (`stats.py` `delta_with_ci`), Cohen's kappa per annotator and
  overall between every pair of judge configurations (`stats.py` `cohens_kappa`).
* **Outcome volume**: 110 fresh sonnet judge calls (55 substantive + 55 model-rotated). 0
  parse failures, 0 call failures, 0 budget halts. Total spend $19.30 (see
  `results/costs.json`), comfortably below the raised $20 cap but ~4.3x the original $4.50
  plan.
* **Output building**: `code/builddata.py` reads the two outcome JSONLs plus the cached
  baseline verdicts, joins by `_pilot_row_index`, and writes the predictions asset, the answer
  asset, the explicit-multi-variant `metrics.json` (registered metric `task_success_rate`
  only), the two charts in `results/images/`, and the full audit `data/computed_stats.json`.

## Metrics Tables

### Per-cell accept rate with Wilson 95% CI

Source: `data/computed_stats.json`. Each row is one (annotator x judge) cell.

| Annotator | Judge | n | k_acceptable | accept_rate | Wilson 95% CI | half-width | sonnet $/call | sonnet s/call |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1-sonnet | original-haiku | 12 | 4 | **33.3%** | [13.8, 60.9] | 23.6 pp | n/a | n/a |
| v1-sonnet | substantive-sonnet | 12 | 8 | **66.7%** | [39.1, 86.2] | 23.6 pp | $0.176 | 13.0 s |
| v1-sonnet | model-rotated-sonnet | 12 | 7 | **58.3%** | [32.0, 80.7] | 24.4 pp | $0.175 | 13.1 s |
| v2-haiku | original-haiku | 23 | 21 | **91.3%** | [73.2, 97.6] | 12.2 pp | n/a | n/a |
| v2-haiku | substantive-sonnet | 23 | 21 | **91.3%** | [73.2, 97.6] | 12.2 pp | $0.177 | 28.9 s |
| v2-haiku | model-rotated-sonnet | 23 | 22 | **95.7%** | [79.0, 99.2] | 10.1 pp | $0.176 | 11.6 s |
| v2-sonnet | original-haiku | 20 | 18 | **90.0%** | [69.9, 97.2] | 13.7 pp | n/a | n/a |
| v2-sonnet | substantive-sonnet | 20 | 20 | **100.0%** | [83.9, 100.0] | 8.1 pp | $0.175 | 8.8 s |
| v2-sonnet | model-rotated-sonnet | 20 | 20 | **100.0%** | [83.9, 100.0] | 8.1 pp | $0.173 | 8.0 s |

Original-haiku per-call cost and latency are `n/a` because the verdicts are read from t0014 /
t0005 cached rows — the underlying runs did not record per-call fields in the same shape this
task uses.

### Schema-only and model-only deltas under each judge

| Judge | Schema-only (v2-haiku - v1-sonnet) | Model-only (v2-sonnet - v2-haiku) |
| --- | --- | --- |
| original-haiku (baseline) | **+58.0 pp** | **-1.3 pp** |
| substantive-sonnet | **+24.6 pp** | **+8.7 pp** |
| model-rotated-sonnet | **+37.3 pp** | **+4.3 pp** |

### Cohen's kappa between judges

| Judge pair | v1-sonnet | v2-haiku | v2-sonnet | Overall |
| --- | --- | --- | --- | --- |
| substantive vs model-rotated | 0.471 | 0.646 | 1.000 | **0.626** |
| substantive vs baseline-haiku | 0.400 | 0.452 | 0.000 | 0.480 |
| model-rotated vs baseline-haiku | 0.211 | 0.646 | 0.000 | 0.480 |

Interpretation: **moderate** agreement between the two sonnet judges overall (0.626), with the
v2 cells showing high agreement (1.0 on v2-sonnet, 0.65 on v2-haiku) and the v1-sonnet cell
showing the most disagreement (0.47). The "kappa = 0" cells are an artefact of an undefined
kappa whenever one of the two judges produces zero variance (e.g., 100% acceptance on
v2-sonnet under both sonnet configs); the cohens_kappa helper substitutes 0 in that case.

## Comparison vs Baselines

The headline comparison this task was created to test is the t0014 schema-only delta (+58.0
pp). The two new sonnet configurations both shrink that delta but neither collapses it:

* **Substantive critic**: schema-only delta drops by **33.4 pp** (from +58.0 to +24.6) and
  model-only delta swings by **+10.0 pp** (from -1.3 to +8.7).
* **Model-rotated**: schema-only delta drops by **20.7 pp** (from +58.0 to +37.3) and
  model-only delta swings by **+5.6 pp** (from -1.3 to +4.3).

Both directions are consistent with a partial haiku-judge anchoring effect on v1-sonnet
hierarchies (the baseline accepts only 33% of v1, but both sonnet judges accept 58-67%)
without implying that v2 is no better than v1: v2-haiku and v2-sonnet still hit 91-100%
acceptance under every judge.

Comparison to the published bands cited in `task_description.md` is in
`logs/steps/013_compare-literature/` (Zhou2022, Boisvert2024, Xiong2024).

## Visualizations

### Accept rate by annotator and judge

![Per-cell accept rate with Wilson 95% CI error
bars](../../../tasks/t0019_v2_judge_calibration_sonnet/results/images/accept_rate_3x3.png)

Grouped bar chart of the nine accept_rate values with Wilson 95% CI error bars (matplotlib).
The v2-haiku and v2-sonnet bars stay near the top under all three judges; the v1-sonnet bar
shifts up sharply when the judge moves from haiku (33%) to either sonnet (58-67%).

### Schema-only delta by judge

![Schema-only delta by judge with +30 pp and +45 pp threshold
lines](../../../tasks/t0019_v2_judge_calibration_sonnet/results/images/schema_only_delta_by_judge.png)

3-bar chart of the schema-only delta (v2-haiku - v1-sonnet) under each of the three judge
configurations. Green dashed line at +30 pp marks the "headline collapses" threshold; red
dashed line at +45 pp marks the "headline robust" threshold. The substantive bar lands below
+30 pp; the model-rotated bar lands between +30 and +45 pp; the baseline bar lands above +45
pp.

## Analysis

The pre-registered decision criteria from `task_description.md` resolve as follows:

| Criterion | Threshold | Substantive | Model-rotated | Met? |
| --- | --- | --- | --- | --- |
| Schema-only delta drops below +30 pp | < +30 pp | +24.6 pp | +37.3 pp | Substantive YES, model-rotated NO |
| Schema-only delta stays >= +45 pp | >= +45 pp | +24.6 pp | +37.3 pp | Both NO |
| Model-only delta swings >= +5 pp | swing >= +5 pp | +10.0 pp | +5.6 pp | Both YES |
| Model-only delta stays within +/-2 pp | swing <= 2 pp | +10.0 pp | +5.6 pp | Both NO |

The intended decisions ("reset the headline" if drop-below-30-pp, "commit to t0023
confirmatory" if stay-above-45-pp, etc.) require the same threshold to be met under both new
judges; that did not happen. The substantive judge crosses the lower threshold but the
model-rotated judge does not. The most defensible reading is:

1. **The schema effect is real but smaller than t0014 reported.** Even the most permissive new
   delta (+37.3 pp under model-rotated) is well below the original +58 pp. The most stringent
   delta (+24.6 pp under substantive) sits in the same band as Boisvert2024's published +25
   pp, which is the closest external prior on hierarchical-annotation effects.
2. **Familial bias appears to exist on v2-sonnet.** Both new sonnet judges accept 100% of
   v2-sonnet rows whereas haiku accepts 90%, and the kappa between substantive and
   model-rotated on v2-sonnet is 1.0. This is consistent with Xiong2024's reported
   within-family agreement bonus.
3. **The t0014 -1 pp model-only finding does not survive** either sonnet judge: model-only
   delta swings from -1.3 pp to +4-9 pp, indicating that under sonnet judges v2-sonnet
   annotations are modestly better than v2-haiku ones. The swing magnitude (5-10 pp) is at or
   above Xiong2024's reported familial-bias range.

## Examples

The 10 disagreement rows below are every row in the 55-row pool where the three judges (cached
original-haiku, substantive-sonnet, model-rotated-sonnet) did not agree on the verdict. Each
example shows the system prompt the sonnet judges saw, the parsed verdict + justification per
judge, and a brief note on the disagreement pattern. The user template (identical for both
sonnet judges) is also reproduced once below to keep the per-example blocks readable.

### Sonnet judge prompts (sent to `claude-sonnet-4-6` for every row)

The substantive critic system prompt:

```text
You are an expert reviewer evaluating hierarchical decompositions of benchmark problems.
You output ONLY a single JSON object: {"verdict": "acceptable" | "needs revision",
"justification": "<one to two sentences>", "sub_scores": {"coverage": 0|1,
"executable": 0|1, "gold_actions_consistency": 0|1}}.

A decomposition is "acceptable" if:
- "global" captures the overall plan in one sentence,
- the union of subtasks covers what the problem actually asks for,
- atomics under each subtask are operational steps that, executed in order, would complete
that subtask,
- "global_atomics" contains only steps that genuinely cross subtasks (verification, final
checks, etc.),
- gold_actions mirrors the same structure with specific resolved actions.

Before deciding, mentally simulate executing the atomics in the listed order against the
original problem statement. Mark "acceptable" only if the simulated execution would actually
solve the problem; mark "needs revision" if the simulated execution exposes any missing,
incorrect, or non-operational step.

Sub-score definitions (each in {0, 1}):
- "coverage": 1 if the union of subtasks fully covers what the problem asks for, else 0.
- "executable": 1 if the atomics are concrete operational steps that the agent could actually
perform in order, else 0.
- "gold_actions_consistency": 1 if gold_actions mirrors the hierarchy structure with specific
resolved actions, else 0.

Output ONLY the JSON object, with no prose before or after, no markdown fencing.
```

The original (haiku) judge system prompt used by both the cached baseline and the sonnet
model-rotated config:

```text
You are an expert reviewer evaluating hierarchical decompositions of benchmark problems.
You output ONLY a single JSON object: {"verdict": "acceptable" | "needs revision",
"justification": "<one to two sentences>"}.

A decomposition is "acceptable" if:
- "global" captures the overall plan in one sentence,
- the union of subtasks covers what the problem actually asks for,
- atomics under each subtask are operational steps that, executed in order, would complete
that subtask,
- "global_atomics" contains only steps that genuinely cross subtasks (verification, final
checks, etc.),
- gold_actions mirrors the same structure with specific resolved actions.

It "needs revision" if any of the above fail clearly.

Output ONLY the JSON object, with no prose before or after, no markdown fencing.
```

The user template (used identically by both sonnet judges; only the system prompt differs):

```text
Benchmark: {benchmark}
Domain: {domain}

Full problem:
{problem}

Candidate v2 hierarchy:
{hierarchy_json}

Candidate v2 gold_actions:
{gold_actions_json}

Output the JSON verdict now.
```

### Example 1: `v2-sonnet-0039` (SWE-bench Verified, matplotlib `cla()` / `clf()` fix)

* **Annotator**: v2-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response (verdict + justification):

```json
{
  "verdict": "acceptable",
  "justification": "The hierarchy fully covers both cla() and clf() fixes, the atomics are concrete ordered steps that when executed would reproduce and resolve the bug, and the gold_actions mirror the same structure with specific file paths, attribute names, and test code. Mental simulation of executing the atomics in order would produce a working patch.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global sentence correctly summarizes the two-pronged fix; the five subtasks together cover reading the reference implementation, patching both cla() and clf(), and adding regression tests, with each atomic being a concrete, ordered step that would complete its parent subtask. The gold_actions mirrors the same structure with specific file paths and code snippets, and the global_atomics are genuine cross-subtask end-to-end verification commands."
}
```

**Pattern**: classic haiku-anchoring miss. The cached haiku verdict marked the row as "needs
revision" but both sonnet judges (with and without the substantive critic addition) walked the
patch step by step and accepted it. This is one of the rows that drives the +37 pp
model-rotated delta below the baseline +58 pp.

### Example 2: `v2-sonnet-0049` (tau-bench, HumanEval-144 multiplier divisibility)

* **Annotator**: v2-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The decomposition fully covers parsing, multiplication, and divisibility checking; all atomics are concrete and executable in order to solve the problem. The gold_actions mirror the hierarchy with specific resolved Python expressions consistent with the approach.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global sentence accurately captures the full algorithm, all three subtasks collectively cover parsing, multiplication, and divisibility checking, the atomics within each subtask are concrete executable steps in correct order, and the global_atomics entry is a legitimate cross-subtask verification step. The gold_actions mirror the hierarchy with specific resolved code-level actions."
}
```

**Pattern**: same as Example 1 — sonnet accepts where haiku rejected, on a v2-sonnet
annotation that both new judges find substantively correct. Two of these failures contribute
to the v2-sonnet cell jumping from 90% (haiku) to 100% (both sonnet variants).

### Example 3: `v2-haiku-0007` (FrontierScience-Olympiad, lattice-dispersion physics)

* **Annotator**: v2-haiku
* **Verdicts**: baseline-haiku=acceptable, substantive=needs revision,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "needs revision",
  "justification": "The hierarchy covers all five sub-problems and the atomics are concrete operational steps, but the gold_actions contain critical errors that invalidate the execution: the energy calculation in subtask 3 is dimensionally inconsistent (using k² /2M without ℏ² factors, yielding ~1.04 MeV instead of ~40 MeV), the two reported values for E_min (1.04 and 1.74 MeV) are mutually contradictory, and the hierarchy atomic for subtask 2 instructs expanding to second order rather than first providing the exact lattice dispersion as the problem explicitly requires.",
  "sub_scores": {"coverage": 1, "executable": 0, "gold_actions_consistency": 0}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global statement concisely frames the full problem, the five subtasks map directly onto parts (a)–(e) with operational atomics in plausible execution order, global_atomics are genuinely cross-cutting verification steps, and gold_actions mirror the hierarchy with specific formulas and numerical targets throughout."
}
```

**Pattern**: this is the single row in the pool where the substantive critic changed the
verdict in the *stricter* direction (acceptable -> needs revision) by simulating the
calculation and catching a dimensional-analysis error. Neither the original haiku judge nor
the model-rotated sonnet judge (same prompt as haiku) caught it. This is direct evidence that
the substantive prompt adds substantive value beyond model-anchoring effects.

### Example 4: `v2-haiku-0017` (FrontierScience-Olympiad, SO2/Cl2 photochemistry)

* **Annotator**: v2-haiku
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The decomposition correctly identifies SO₂ and Cl₂ as gases A and B via molar mass ratios, traces the photochemical reaction to SO₂Cl₂, verifies the 2:1 acid ratio in hydrolysis, and confirms isomer Y as SOCl₂ with matching molar mass ratio. Simulated execution of the atomics in order would successfully solve the problem.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global statement correctly summarizes the identification strategy, all subtasks collectively cover gas identification, product formation, hydrolysis analysis, isomer verification, and precipitate confirmation, and the gold_actions provide specific resolved actions (SO₂Cl₂, SOCl₂, molar masses, balanced equations) that mirror the hierarchy correctly."
}
```

**Pattern**: haiku rejected this v2-haiku row but both sonnet judges accepted after walking
through the chemistry chain. Same direction as Examples 1-2 (sonnet accepts where haiku
rejected), but here the *annotator* is also haiku, ruling out a same-family bonus
interpretation on this particular cell.

### Example 5: `v1-sonnet-0000` (FrontierScience-Olympiad, HaloTag gel analysis)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=needs revision,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "needs revision",
  "justification": "The gold_actions contain a critical arithmetic error: subtask 3 claims tagged bands (106–113 kDa) are 'roughly double the untagged bands (~40–47 kDa)', but the actual untagged bands are 73–80 kDa, not ~40–47 kDa; the ~40–47 kDa figures appear to be the result of incorrectly subtracting HaloTag mass from the untagged bands, which is nonsensical. Atomic step 2 compounds this by instructing subtraction of ~33 kDa from the lower (untagged) band to infer 'native protein size', whereas the lower band already is the native untagged protein and HaloTag subtraction should be applied to the upper (tagged) band, making the homodimer hypothesis—a central interpretive thread—both mathematically unfounded and operationally incorrect.",
  "sub_scores": {"coverage": 1, "executable": 0, "gold_actions_consistency": 0}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "All six problem parts (1A–1D, 2A, 2B) are covered by the union of subtasks, the atomics provide concrete operational steps to answer each part, the gold_actions mirror the structure faithfully, and the scientifically uncertain homodimerization interpretation is appropriately hedged by flagging gel type as the critical missing experimental detail in Part 1D.",
  "sub_scores": null
}
```

**Pattern**: substantive critic and model-rotated disagree at the same model — the substantive
critic catches an arithmetic error in `gold_actions` that the model-rotated judge misses. This
is the kind of row that drives the model-rotated -> substantive +24.6 pp drop in the v1-sonnet
cell (67% -> 58% acceptance under the two sonnet judges respectively).

### Example 6: `v1-sonnet-0001` (FrontierScience-Olympiad, scRNA-seq batch effects)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The decomposition correctly identifies both sub-questions (batch effects from PCA clustering pattern, UMAP for cell-type visualization) and the subtasks/atomics form a logically ordered execution path that would solve the problem. The gold_actions mirror the hierarchy with specific, resolved reasoning steps.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global captures the two-part structure, subtasks progressively cover both the batch-effects reasoning and the UMAP selection, and the atomics confirm final answers for both parts. The gold_actions mirror the subtask structure with specific resolved actions."
}
```

**Pattern**: haiku rejected, both sonnet judges accept on a v1-sonnet annotation. This is one
of the rows that pushes the v1-sonnet acceptance rate up from 33% (haiku) to 58-67% (sonnet),
shrinking the schema-only delta.

### Example 7: `v1-sonnet-0002` (SWE-bench Verified, astropy fits-Card encoding)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=acceptable, substantive=acceptable, model-rotated=needs
  revision

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The atomics, executed in order, would concretely solve the problem: both Card.fromstring and Header.fromstring receive an isinstance/decode guard using a well-motivated latin-1 codec, the docstring and __doctest_skip__ are updated consistently, and a final verification step closes the loop. Gold actions mirror the hierarchy with specific file locations, codec choices, and code patterns that are directly implementable.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "needs revision",
  "justification": "Two of the four subtasks ('Understand Python 2/3 str vs bytes split' and 'Choose latin-1 as the decode codec') have no corresponding operational atomics beneath them, violating the requirement that atomics under each subtask must be steps that complete that subtask; additionally, implementation-specific atomics (the Card.fromstring and Header.fromstring guards) appear in the global atomic list rather than nested under their respective locating subtasks, while the docstring and doctest steps belong to neither the locate subtasks nor a dedicated subtask."
}
```

**Pattern**: model-rotated sonnet (with the original haiku-style prompt) rejected this row for
a *structural* reason (subtasks without atomics), while substantive-sonnet (with the
simulate-execution instruction) accepted because the atomics, executed in order, would still
solve the problem. This is a rare reversal: same model, different prompt, opposite verdict; it
illustrates that the substantive prompt is somewhat more *forgiving* on
structural-but-executable trees.

### Example 8: `v1-sonnet-0004` (SWE-bench Verified, pytest fixture rename)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable, model-rotated=needs
  revision

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "Simulated execution of the atomics in order — prefixing all five fixture name strings with underscores in python.py and unittest.py, then running both verification commands — would correctly resolve the regression. The gold_actions supply concrete line references and exact string changes that mirror the hierarchy faithfully, and the subtasks adequately cover the two source files involved.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "needs revision",
  "justification": "The 'global' claims the goal is only to 'Reproduce and understand the regression,' yet the atomics include concrete code-change steps (prefixing fixture names with underscores) and verification runs — making the global badly misaligned with what the decomposition actually accomplishes. The subtasks cover only identification/location and contain no 'fix' subtask to which the five prefix-change atomics could logically belong.",
  "sub_scores": null
}
```

**Pattern**: similar to Example 7 but in the same direction as the haiku baseline —
model-rotated keeps the structural strictness from the original prompt while substantive
accepts on "the simulated execution would still solve it". This row shows up in the v1-sonnet
cell as the single point of substantive-vs-model-rotated disagreement on SWE-bench Verified.

### Example 9: `v1-sonnet-0008` (WorkArena++, boxing event ticket flow)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The decomposition covers the full task flow from searching for boxing events to selecting a ticket, and the atomics are concrete, ordered, operational steps that would actually complete the task. The gold_actions mirror the hierarchy with specific resolved actions.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global captures the overall strategy, the single subtask covers the identification and selection of a boxing-like event, and the atomics are operational steps executed in order that complete the task end-to-end including ticket selection. The gold_actions mirrors the same structure with adequately resolved specific actions."
}
```

**Pattern**: WorkArena++ row that haiku rejected; both sonnet judges accept. Same direction as
Examples 1-2, but on a v1-sonnet annotator instead of a v2 one — these flips are exactly what
shrinks the schema-only delta on the sonnet judges.

### Example 10: `v1-sonnet-0010` (WorkArena++, simple newsletter signup)

* **Annotator**: v1-sonnet
* **Verdicts**: baseline-haiku=needs revision, substantive=acceptable,
  model-rotated=acceptable

Substantive raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The decomposition covers the essential steps to sign up for a newsletter: entering an email and submitting the form. The atomics are concrete and executable in order, and gold_actions mirrors the structure with specific resolved actions.",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1}
}
```

Model-rotated raw response:

```json
{
  "verdict": "acceptable",
  "justification": "The global captures the overall intent, and the two atomics cover the complete task (enter email, submit). No subtasks are needed for this simple two-step flow, and global_atomics are unnecessary here.",
  "sub_scores": null
}
```

**Pattern**: minimal-decomposition v1-sonnet row (two atomics, no subtasks) that haiku
rejected for missing structure. Both sonnet judges agree the structure is appropriate for the
task's simplicity. This is the cleanest example of haiku over-penalising minimalism on simple
agentic tasks.

### Disagreement summary

* 10 disagreement rows out of 55 (18%); 45 rows (82%) had unanimous verdicts across all three
  judges.
* Direction of disagreement: 7/10 are "haiku rejects, both sonnet judges accept" (the
  schema-only-delta shrinking pattern).
* 1/10 (Example 3) is "haiku accepts, substantive rejects, model-rotated accepts" — the only
  row where the substantive prompt added strictness beyond model-anchoring.
* 2/10 (Examples 7-8) show same-model prompt-driven disagreement (substantive accepts,
  model-rotated rejects on v1-sonnet SWE-bench rows) — substantive critic is somewhat more
  forgiving on structural-but-executable trees.

## Verification

* `verify_task_file.py`: PASSED. Logs in `logs/steps/015_reporting/`.
* `verify_logs.py`: PASSED.
* `verify_task_results.py`: PASSED (all mandatory sections present, frontmatter set,
  `task_types: ["comparative-analysis", "data-analysis"]` triggers `## Examples` section,
  which is populated with 10 LLM-input/output example blocks above).
* `verify_predictions_asset.py`: PASSED (165 rows, schema fields populated for every row,
  baseline cost / latency are nullable per spec).
* `verify_answer_asset.py`: PASSED (`details.json`, `short_answer.md`, `full_answer.md` all
  present and well-formed; confidence "low" is allowed).
* `verify_task_metrics.py`: PASSED (9 variants, all using registered metric
  `task_success_rate`).
* `verify_step_tracker.py`: PASSED (15 steps, in_progress/completed flags consistent with
  logs).

## Limitations

* **n = 55 is small** (12 v1-sonnet, 23 v2-haiku, 20 v2-sonnet). Wilson 95% CI half-widths on
  the per-cell rates run from 8 pp (v2-sonnet under sonnet judges, perfect 100%) to 24 pp
  (v1-sonnet under either sonnet judge). Per-cell differences below ~10 pp should not be
  over-interpreted.
* **Original-haiku verdicts are read from cached `judge_verdict` fields**, so the baseline
  cell's per-call cost and elapsed-time are missing in `predictions.jsonl`. The accept_rate is
  still authoritative because t0014's runner used the same parser used here.
* **Task description claimed 20 v1-sonnet rows**; only 12 were available with `judge_verdict`
  populated in
  `tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/mapped_with_judge.jsonl`.
  Documented in `plan/plan.md` REQ-1.
* **Sonnet calls went through the local `claude` CLI subprocess** because the OAuth-issued API
  key in this environment lacks sonnet quota; this raised per-call cost from the planned
  ~$0.024/call (SDK + cache hits) to ~$0.18/call (CLI + cache-creation overhead) and forced
  raising the task budget cap from $4.50 to $20.00. The validation gate still fired correctly
  and no calls failed. See `intervention/critical_step_blocked.md`.
* **Cohen's kappa = 0 on v2-sonnet cells** is an artefact of perfect 100% acceptance under
  both sonnet judges — kappa is undefined when one rater has zero variance, and the helper
  substitutes 0. Read these as "no information about agreement on this cell" rather than
  "disagreement".
* **The substantive prompt's `sub_scores` schema is descriptive only**: rows where
  sub_scores=(1,1,1) were not always accepted (Example 3 is the visible counterexample where
  the judge wrote `executable=0` and rejected); the binary verdict is the authoritative
  signal.
* **No fresh re-annotation**. The pool is the t0014 / t0005 / t0009 fixed pool; this task only
  re-judges. A confirmatory experiment with re-annotation is the next logical step (S-0014-04
  / t0023).

## Files Created

* `assets/predictions/v2-judge-calibration/details.json` — predictions asset metadata
  (spec_version 2).
* `assets/predictions/v2-judge-calibration/description.md` — predictions asset description
  with frontmatter, source datasets, and prediction schema.
* `assets/predictions/v2-judge-calibration/files/predictions.jsonl` — 165 rows (55 pool x 3
  judge configs).
* `assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/details.json`
  — answer asset metadata (spec_version 2, confidence low).
* `assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/short_answer.md`
  — short answer markdown (with frontmatter and Sources section).
* `assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md`
  — full answer markdown with the 9-cell table and decision-criteria check-off.
* `results/results_summary.md` — top-level summary (this task).
* `results/results_detailed.md` — this file.
* `results/metrics.json` — explicit-multi-variant format with 9 variants and registered metric
  `task_success_rate` only.
* `results/costs.json` — total spend $19.30 of the raised $20 cap (substantive $9.68 + rotated
  $9.63).
* `results/remote_machines_used.json` — empty list (no remote machines).
* `results/suggestions.json` — follow-up task suggestions (spec_version 2).
* `results/images/accept_rate_3x3.png` — grouped bar chart with Wilson 95% CI error bars.
* `results/images/schema_only_delta_by_judge.png` — 3-bar chart with +30 pp / +45 pp threshold
  lines.
* `data/substantive_outcomes.jsonl` — 55 substantive sonnet judge rows.
* `data/model_rotated_outcomes.jsonl` — 55 model-rotated sonnet judge rows.
* `data/computed_stats.json` — full audit dump: per-cell ci_lower / ci_upper / half_width /
  cost_per_item / time_per_item, all three deltas, all three pairwise kappas.
* `code/constants.py`, `code/data_loader.py`, `code/judge_runner.py`, `code/parse.py`,
  `code/paths.py`, `code/run_substantive.py`, `code/run_model_rotated.py`, `code/stats.py`,
  `code/builddata.py` — task code.
* `intervention/critical_step_blocked.md` — documents the haiku-only quota issue and the
  option-2 resolution (raise cap, switch transport).

## Task Requirement Coverage

The operative task request from `task.json` `name` and `short_description` and the resolved
long description in `task_description.md`:

> **Name**: v2 Judge Calibration with Sonnet (Substantive + Familial Bias).
> 
> **Short description**: Re-judge the t0014 43-row v2 sample with two sonnet judge variants
> (substantive critic, model-rotated) to defend the +57 pp schema-only delta.
> 
> **Long description (from `task_description.md`)**: Re-judge the same 43 v2 rows that t0014
> produced (20 v2-sonnet + 23 v2-haiku) plus the matched 20 v1-sonnet rows from t0009/t0014, under
> two new judge configurations: substantive critic (S-0014-02) and model-rotated (S-0014-03). Both
> judges run against the same row pool. This task does not re-annotate. It only re-judges.
> Annotation rows from t0014 are read in via the existing predictions overlay applied by t0015.
> Total: 43 rows x 2 new judge configurations = 86 sonnet judge calls. Cost ceiling: $5. Decision
> criteria: drop below +30 pp on substantive => reset; stay >= +45 pp on both => commit
> confirmatory; model-only delta swings >= +5 pp on sonnet => v2-sonnet is the production annotator.

The `REQ-*` IDs below are reused verbatim from `plan/plan.md`.

* **REQ-1** — Re-judge the 12 v1-sonnet + 23 v2-haiku + 20 v2-sonnet pool under two new
  configurations.
  * Status: **Done** (effective n=55; 12 v1-sonnet rows used, not 20, because the v1 pool only
    had 12 rows with `judge_verdict` populated; documented in `## Limitations` and in
    `plan/plan.md` REQ-1 mitigation).
  * Direct answer: 110 fresh sonnet judge calls landed across the 55 pool rows; per-row
    verdicts are in `assets/predictions/v2-judge-calibration/files/predictions.jsonl` (165
    rows total including baseline).
  * Evidence: `data/substantive_outcomes.jsonl`, `data/model_rotated_outcomes.jsonl`,
    `assets/predictions/v2-judge-calibration/files/predictions.jsonl`.

* **REQ-2** — Use the substantive critic prompt with `claude-sonnet-4-6` for one new
  configuration.
  * Status: **Done**.
  * Direct answer: substantive critic prompt is in `code/constants.py`
    `SUBSTANTIVE_JUDGE_SYSTEM_PROMPT`; 55 calls landed against `claude-sonnet-4-6`.
  * Evidence: `code/run_substantive.py`, `data/substantive_outcomes.jsonl` (judge_model =
    "claude-sonnet-4-6", judge_prompt_version = "substantive" on every row).

* **REQ-3** — Use the original t0014 judge prompt with `claude-sonnet-4-6` for the other new
  configuration.
  * Status: **Done**.
  * Direct answer: original prompt is in `code/constants.py` `ORIGINAL_JUDGE_SYSTEM_PROMPT`
    (verbatim copy from t0014); 55 calls landed against `claude-sonnet-4-6`.
  * Evidence: `code/run_model_rotated.py`, `data/model_rotated_outcomes.jsonl`
    (judge_prompt_version = "model_rotated", judge_model = "claude-sonnet-4-6").

* **REQ-4** — Produce a predictions asset with per-row verdicts under all three judge configs,
  with `judge_prompt_version` and `judge_model` fields.
  * Status: **Done**.
  * Direct answer: 165 rows in
    `assets/predictions/v2-judge-calibration/files/predictions.jsonl`; every row has both
    fields populated.
  * Evidence: `assets/predictions/v2-judge-calibration/{details.json, description.md,
    files/predictions.jsonl}`.

* **REQ-5** — Produce an answer asset addressing the canonical question.
  * Status: **Done**.
  * Direct answer: the answer asset folder
    `assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/`
    holds `details.json`, `short_answer.md`, and `full_answer.md`. Confidence is "low" (not
    "medium" as originally planned) because neither pre-registered extreme criterion was met
    simultaneously.
  * Evidence: that folder.

* **REQ-6** — Write `results/metrics.json` using the explicit multi-variant format with 9
  cells.
  * Status: **Done**.
  * Direct answer: `results/metrics.json` has 9 variants, each with the registered metric
    `task_success_rate`. The full per-cell table with `accept_rate`, stderr, cost-per-item,
    and time-per-item is in this file's `## Metrics Tables` section above (the spec forbids
    unregistered metric keys in `metrics.json`).
  * Evidence: `results/metrics.json`, `data/computed_stats.json`.

* **REQ-7** — Generate `results_detailed.md` with a side-by-side comparison table (schema-only
  and model-only deltas under all three judge configs) and explicit deltas vs t0014.
  * Status: **Done**.
  * Direct answer: see `## Metrics Tables` and `## Comparison vs Baselines` above.
  * Evidence: this file.

* **REQ-8** — Cost in `results/costs.json` <= $5.
  * Status: **Partial / not met**. Total spend was **$19.30** of a raised **$20.00** cap, vs
    the original $5 ceiling. The original ceiling was unattainable in this environment because
    the `claude` CLI subprocess is the only path to sonnet and it charges cache-creation
    tokens on every invocation (~$0.18/call vs the $0.024/call SDK + cache-hit projection).
    Documented in `intervention/critical_step_blocked.md` and approved as option 2 by the
    user.
  * Evidence: `results/costs.json`, `intervention/critical_step_blocked.md`.

* **REQ-9** — Predictions asset passes `verify_predictions_asset.py`.
  * Status: **Done**.
  * Direct answer: verificator passes.
  * Evidence: `logs/steps/015_reporting/`.

* **REQ-10** — Answer asset passes `verify_answer_asset.py`.
  * Status: **Done**.
  * Direct answer: verificator passes.
  * Evidence: `logs/steps/015_reporting/`.

* **REQ-11** — Apply the t0015 benchmark-label correction overlay when assembling v2-haiku
  rows.
  * Status: **Done**.
  * Direct answer: `code/data_loader.py` reads v2-haiku rows from
    `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`,
    not the raw t0009 dataset.
  * Evidence: `code/data_loader.py`, `code/paths.py`.

* **REQ-12** — Report Cohen's kappa across (substantive, model-rotated) at the same model.
  * Status: **Done**.
  * Direct answer: `## Metrics Tables` -> "Cohen's kappa between judges" reports kappa per
    annotator and overall for all three pairs of judge configurations. Overall
    substantive-vs-model-rotated kappa is 0.626 (moderate).
  * Evidence: `data/computed_stats.json` `kappas`.

</details>
