# Predictions: `llm-as-judge`

3 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>Variant A: Scope-Aware ReAct (atomic granularity)</strong>
(<code>a-scope-aware</code>) — 147 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `a-scope-aware` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport). max_turns=10, max_tokens=4096. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 147 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Documentation** | [`description.md`](../../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/a-scope-aware/description.md) |

**Metrics at creation:**

* **success_rate_judge_sonnet**: 0.04081632653061224
* **n_success**: 6
* **n_instances**: 147
* **total_cost_usd**: 4.596921

# Variant A: Scope-Aware ReAct (atomic granularity)

## Metadata

* **Variant**: a
* **Model**: claude-sonnet-4-6
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 147
* **Created by**: t0026_phase2_abc_runtime_n147_for_rq1_rq5

## Overview

Scope-Aware ReAct agent operating at atomic granularity over a paired N=147 instance manifest
spanning SWE-bench Verified, Tau-bench, and FrontierScience Olympiad. Each prediction includes
the agent's final answer, the trajectory path, the per-instance cost, and primary sonnet judge
verdicts. A subset of 30 instances also carries an opus inter-judge verdict for inter-rater
agreement.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs use a 10-turn cap
with 4096 max output tokens per call.

## Data

The paired N=147 manifest spans 20 SWE-bench Verified instances (stratified by difficulty
bucket), 87 Tau-bench instances (deterministic by domain+task_index), and 40 FrontierScience
Olympiad instances (deterministic by task_id). The manifest `data/instance_manifest.json`
records the exact instance IDs and source SHA-256 hashes per subset.

## Prediction Format

JSON Lines. Each row has: instance_id, subset, variant, final_answer (nullable),
final_confidence (nullable; only populated for variant B), cost_usd, trajectory_path,
judge_sonnet_success, judge_sonnet_rationale, judge_opus_success (nullable; non-null only for
the inter-judge sample), judge_opus_rationale (nullable).

## Metrics

* Success rate (sonnet judge, all subsets): **0.0408**
* Cost per instance: **$0.0313**

Per-subset breakdown:

* swebench: n=20, n_success=6, success_rate=0.3000
* taubench: n=87, n_success=0, success_rate=0.0000
* frontsci: n=40, n_success=0, success_rate=0.0000

## Main Ideas

* These predictions provide the runtime evidence base for RQ1-RQ5 in t0026 — calibration
  (RQ1-RQ2), judge agreement (RQ3-RQ4), and strict A>B>C ordering (RQ5) are all computed from
  these JSONL files.
* Judge verdicts attached inline avoid recomputing judge calls across downstream tasks; opus
  inter-judge subset enables inter-rater agreement without a full opus pass.
* Empty or null final_answer entries are recorded honestly and judged as FAIL by the
  substantive prompt; downstream analyses can treat them as legitimate failures rather than
  missing data.

## Summary

This predictions asset captures variant a runs across the paired N=147 manifest under the
claude-sonnet-4-6 model. The trajectory files in `data/runs/a/` contain the full action
history; the JSONL here is the analysis-ready summary with judge verdicts joined inline.
Together with `assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}` for the other
two variants, this asset supplies the full dataset used in `results/metrics.json` and the
per-research-question comparisons reported in `results/results_detailed.md`.

</details>

<details>
<summary>📊 <strong>Variant B: Plan-and-Solve v2 with final_confidence</strong>
(<code>b-plan-and-solve</code>) — 147 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `b-plan-and-solve` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport). max_turns=10, max_tokens=4096. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 147 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Documentation** | [`description.md`](../../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/b-plan-and-solve/description.md) |

**Metrics at creation:**

* **success_rate_judge_sonnet**: 0.04081632653061224
* **n_success**: 6
* **n_instances**: 147
* **total_cost_usd**: 10.531533

# Variant B: Plan-and-Solve v2 with final_confidence

## Metadata

* **Variant**: b
* **Model**: claude-sonnet-4-6
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 147
* **Created by**: t0026_phase2_abc_runtime_n147_for_rq1_rq5

## Overview

Plan-and-Solve v2 agent emitting a final_confidence in [0,1] alongside final_answer, evaluated
on the same paired N=147 manifest. Each prediction includes the agent's final answer, the
trajectory path, the per-instance cost, and primary sonnet judge verdicts. A subset of 29
instances also carries an opus inter-judge verdict for inter-rater agreement.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs use a 10-turn cap
with 4096 max output tokens per call.

## Data

The paired N=147 manifest spans 20 SWE-bench Verified instances (stratified by difficulty
bucket), 87 Tau-bench instances (deterministic by domain+task_index), and 40 FrontierScience
Olympiad instances (deterministic by task_id). The manifest `data/instance_manifest.json`
records the exact instance IDs and source SHA-256 hashes per subset.

## Prediction Format

JSON Lines. Each row has: instance_id, subset, variant, final_answer (nullable),
final_confidence (nullable; only populated for variant B), cost_usd, trajectory_path,
judge_sonnet_success, judge_sonnet_rationale, judge_opus_success (nullable; non-null only for
the inter-judge sample), judge_opus_rationale (nullable).

## Metrics

* Success rate (sonnet judge, all subsets): **0.0408**
* Cost per instance: **$0.0716**

Per-subset breakdown:

* swebench: n=20, n_success=0, success_rate=0.0000
* taubench: n=87, n_success=2, success_rate=0.0230
* frontsci: n=40, n_success=4, success_rate=0.1000

## Main Ideas

* These predictions provide the runtime evidence base for RQ1-RQ5 in t0026 — calibration
  (RQ1-RQ2), judge agreement (RQ3-RQ4), and strict A>B>C ordering (RQ5) are all computed from
  these JSONL files.
* Judge verdicts attached inline avoid recomputing judge calls across downstream tasks; opus
  inter-judge subset enables inter-rater agreement without a full opus pass.
* Empty or null final_answer entries are recorded honestly and judged as FAIL by the
  substantive prompt; downstream analyses can treat them as legitimate failures rather than
  missing data.

## Summary

This predictions asset captures variant b runs across the paired N=147 manifest under the
claude-sonnet-4-6 model. The trajectory files in `data/runs/b/` contain the full action
history; the JSONL here is the analysis-ready summary with judge verdicts joined inline.
Together with `assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}` for the other
two variants, this asset supplies the full dataset used in `results/metrics.json` and the
per-research-question comparisons reported in `results/results_detailed.md`.

</details>

<details>
<summary>📊 <strong>Variant C: Mismatched (atomic granularity, adversarial
annotation)</strong> (<code>c-mismatched</code>) — 147 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `c-mismatched` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport). max_turns=10, max_tokens=4096. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 147 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Documentation** | [`description.md`](../../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/c-mismatched/description.md) |

**Metrics at creation:**

* **success_rate_judge_sonnet**: 0.11564625850340136
* **n_success**: 17
* **n_instances**: 147
* **total_cost_usd**: 13.947051

# Variant C: Mismatched (atomic granularity, adversarial annotation)

## Metadata

* **Variant**: c
* **Model**: claude-sonnet-4-6
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 147
* **Created by**: t0026_phase2_abc_runtime_n147_for_rq1_rq5

## Overview

Matched-Mismatch agent fed an intentionally adversarial synthetic annotation, evaluated on the
same paired N=147 manifest as the negative control for RQ5 strict ordering. Each prediction
includes the agent's final answer, the trajectory path, the per-instance cost, and primary
sonnet judge verdicts. A subset of 30 instances also carries an opus inter-judge verdict for
inter-rater agreement.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs use a 10-turn cap
with 4096 max output tokens per call.

## Data

The paired N=147 manifest spans 20 SWE-bench Verified instances (stratified by difficulty
bucket), 87 Tau-bench instances (deterministic by domain+task_index), and 40 FrontierScience
Olympiad instances (deterministic by task_id). The manifest `data/instance_manifest.json`
records the exact instance IDs and source SHA-256 hashes per subset.

## Prediction Format

JSON Lines. Each row has: instance_id, subset, variant, final_answer (nullable),
final_confidence (nullable; only populated for variant B), cost_usd, trajectory_path,
judge_sonnet_success, judge_sonnet_rationale, judge_opus_success (nullable; non-null only for
the inter-judge sample), judge_opus_rationale (nullable).

## Metrics

* Success rate (sonnet judge, all subsets): **0.1156**
* Cost per instance: **$0.0949**

Per-subset breakdown:

* swebench: n=20, n_success=1, success_rate=0.0500
* taubench: n=87, n_success=9, success_rate=0.1034
* frontsci: n=40, n_success=7, success_rate=0.1750

## Main Ideas

* These predictions provide the runtime evidence base for RQ1-RQ5 in t0026 — calibration
  (RQ1-RQ2), judge agreement (RQ3-RQ4), and strict A>B>C ordering (RQ5) are all computed from
  these JSONL files.
* Judge verdicts attached inline avoid recomputing judge calls across downstream tasks; opus
  inter-judge subset enables inter-rater agreement without a full opus pass.
* Empty or null final_answer entries are recorded honestly and judged as FAIL by the
  substantive prompt; downstream analyses can treat them as legitimate failures rather than
  missing data.

## Summary

This predictions asset captures variant c runs across the paired N=147 manifest under the
claude-sonnet-4-6 model. The trajectory files in `data/runs/c/` contain the full action
history; the JSONL here is the analysis-ready summary with judge verdicts joined inline.
Together with `assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}` for the other
two variants, this asset supplies the full dataset used in `results/metrics.json` and the
per-research-question comparisons reported in `results/results_detailed.md`.

</details>
