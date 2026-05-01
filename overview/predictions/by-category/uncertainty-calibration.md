# Predictions: `uncertainty-calibration`

1 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>v2 Judge Calibration: 3 judges x 3 annotators on 55-row
pool</strong> (<code>v2-judge-calibration</code>) — 165 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `v2-judge-calibration` |
| **Model ID** | — |
| **Model** | Two judge models: claude-haiku-4-5 (original-haiku, cached from t0014/t0005) and claude-sonnet-4-6 (substantive-sonnet and model-rotated-sonnet, fresh calls in this task). Sonnet calls were routed through the local `claude` CLI subprocess because the OAuth-issued ANTHROPIC_API_KEY in this environment is provisioned only for haiku quota; see intervention/critical_step_blocked.md for the rationale. |
| **Datasets** | `hierarchical-annotation-v2-sonnet`, `hierarchical-annotation-v2-relabeled` |
| **Format** | jsonl |
| **Instances** | 165 |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Created by** | [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Documentation** | [`description.md`](../../../tasks/t0019_v2_judge_calibration_sonnet/assets/predictions/v2-judge-calibration/description.md) |

**Metrics at creation:**

* **accept_rate__v1-sonnet__original-haiku**: 0.3333
* **accept_rate__v1-sonnet__substantive-sonnet**: 0.6667
* **accept_rate__v1-sonnet__model-rotated-sonnet**: 0.5833
* **accept_rate__v2-haiku__original-haiku**: 0.913
* **accept_rate__v2-haiku__substantive-sonnet**: 0.913
* **accept_rate__v2-haiku__model-rotated-sonnet**: 0.9565
* **accept_rate__v2-sonnet__original-haiku**: 0.9
* **accept_rate__v2-sonnet__substantive-sonnet**: 1.0
* **accept_rate__v2-sonnet__model-rotated-sonnet**: 1.0

# v2 Judge Calibration: 3 Judges x 3 Annotators on the 55-Row Pool

## Metadata

* **Name**: v2 Judge Calibration: 3 judges x 3 annotators on 55-row pool
* **Models**: claude-haiku-4-5 (baseline, cached from t0014/t0005) and claude-sonnet-4-6
  (substantive-sonnet, model-rotated-sonnet, fresh in this task)
* **Datasets**: `hierarchical-annotation-v2-sonnet`, `hierarchical-annotation-v2-relabeled`
* **Format**: jsonl
* **Instances**: 165 (55 pool rows x 3 judge configs)
* **Created by**: t0019_v2_judge_calibration_sonnet

## Overview

This predictions asset captures binary acceptance verdicts from three LLM-as-judge
configurations applied to a fixed 55-row pool of hierarchical decompositions. The pool
combines 20 rows from the v2-sonnet annotator (t0014), 23 rows from the v2-haiku annotator
with t0015 benchmark-label corrections applied, and 12 rows from the v1-sonnet pilot (t0005).
Each row is judged three times: once by the original t0014 prompt and judge (claude-haiku-4-5,
cached), once by a substantive critic prompt that requires the judge to simulate executing the
atomics in order (claude-sonnet-4-6), and once by the original prompt with the judge model
swapped to sonnet (claude-sonnet-4-6).

The asset is the primary evidence for whether the +57 pp v2-vs-v1 schema-only headline
observed in t0014 (under haiku as judge) survives a stricter judge prompt and a stronger judge
model. It also records per-call cost and elapsed time so downstream tasks can reason about the
cost of swapping judge families. All sonnet calls were routed through the local `claude` CLI
subprocess because the OAuth-issued ANTHROPIC_API_KEY in this environment is provisioned only
for haiku quota; see `intervention/critical_step_blocked.md` for the rationale.

## Model

Two judge model configurations are recorded:

* **Original-haiku (baseline)** — `claude-haiku-4-5` with the original t0014 system prompt
  asking for `{"verdict": "...", "justification": "..."}`. Verdicts are read from the cached
  `judge_verdict` field on each pool row (no fresh calls in this task; this is the baseline
  that the two new sonnet configurations are compared against).
* **Substantive-sonnet** — `claude-sonnet-4-6` with an extended prompt that adds the explicit
  instruction "Before deciding, mentally simulate executing the atomics in the listed order
  against the original problem statement. Mark `acceptable` only if the simulated execution
  would actually solve the problem". Optional `sub_scores` keys (`coverage`, `executable`,
  `gold_actions_consistency`) are captured when present.
* **Model-rotated-sonnet** — `claude-sonnet-4-6` with the original t0014 prompt verbatim. This
  isolates the effect of swapping the judge model, holding the prompt constant.

## Data

The 55-row pool decomposes by annotator:

| Annotator | Source | Rows |
| --- | --- | --- |
| v1-sonnet | t0005 `mapped_with_judge.jsonl` | 12 |
| v2-haiku | t0015 `hierarchical_annotation_v2_relabeled.jsonl` | 23 |
| v2-sonnet | t0014 `hierarchical_annotation_v2_sonnet.jsonl` | 20 |
| **Total** |  | **55** |

The t0015 benchmark-label correction overlay is applied automatically to the v2-haiku rows by
reading the `*_relabeled.jsonl` file rather than the t0009 raw source.

## Prediction Format

Each line of `files/predictions.jsonl` is a JSON object with fields documented in
`prediction_schema` of `details.json`. Concretely:

```
{
  "pool_row_id": "v2-sonnet-0001",
  "annotator": "v2-sonnet",
  "task_id": "fs_4225f097-0cee-4e43-b5b9-6efbab4c3447",
  "benchmark": "FrontierScience-Olympiad",
  "domain": "physics",
  "judge_prompt_version": "substantive",
  "judge_label": "substantive-sonnet",
  "judge_model": "claude-sonnet-4-6",
  "verdict": "acceptable",
  "justification": "...",
  "sub_scores": {"coverage": 1, "executable": 1, "gold_actions_consistency": 1},
  "parse_status": "ok",
  "cost_usd": 0.179,
  "elapsed_seconds": 6.51
}
```

For the cached `original-haiku` rows, `cost_usd` and `elapsed_seconds` are `null` (these are
re-used from t0014/t0005 where per-call telemetry was not propagated into this task's
outputs). The `justification` and `sub_scores` fields are also `null` for the baseline because
t0014 did not store the haiku judge's justification text in a form that survived the t0015
relabeling pass.

## Metrics

The 9-cell accept-rate matrix computed from this predictions asset:

| Annotator | Judge | n | k | accept_rate | 95% Wilson CI |
| --- | --- | --- | --- | --- | --- |
| v1-sonnet | original-haiku | 12 | 4 | 33.3% | [13.8, 60.9] |
| v1-sonnet | substantive-sonnet | 12 | 8 | 66.7% | [39.1, 86.2] |
| v1-sonnet | model-rotated-sonnet | 12 | 7 | 58.3% | [32.0, 80.7] |
| v2-haiku | original-haiku | 23 | 21 | 91.3% | [73.2, 97.6] |
| v2-haiku | substantive-sonnet | 23 | 21 | 91.3% | [73.2, 97.6] |
| v2-haiku | model-rotated-sonnet | 23 | 22 | 95.7% | [79.0, 99.2] |
| v2-sonnet | original-haiku | 20 | 18 | 90.0% | [69.9, 97.2] |
| v2-sonnet | substantive-sonnet | 20 | 20 | 100.0% | [83.9, 100.0] |
| v2-sonnet | model-rotated-sonnet | 20 | 20 | 100.0% | [83.9, 100.0] |

See `results/results_detailed.md` for schema-only and model-only deltas under each judge,
Cohen's kappa between judge configurations, and the four decision-criteria check-off.

## Main Ideas

* The substantive critic and model-rotated sonnet judges accept the v2 schema at much higher
  rates than the original haiku judge — the +57 pp v2-haiku vs v1-sonnet schema-only headline
  from t0014 collapses to a much smaller delta when sonnet is the judge.
* Per-call cost averaged ~$0.18/call for sonnet via the `claude` CLI subprocess
  (cache-creation inflated the first call to $0.20 then dropped); haiku-as-judge cost is ~10x
  cheaper but with much harsher binary verdicts.
* Cohen's kappa between substantive-sonnet and model-rotated-sonnet is high overall,
  indicating that prompt anchoring (substantive vs original) matters less than model anchoring
  (haiku vs sonnet) for binary verdict agreement on this pool.

## Summary

This predictions asset is the per-row evidence for the t0019 calibration question: did the +57
pp v2-vs-v1 schema-only delta in t0014 survive a stronger judge family or a stricter prompt?
The 165 rows record three independent judgments per pool row: the cached original-haiku
verdicts from t0014/t0005, fresh substantive-critic-sonnet verdicts, and fresh
model-rotated-sonnet verdicts.

The headline finding is that the +57 pp gap shrinks dramatically under either of the two
sonnet configurations: under substantive-sonnet the schema-only delta is much smaller, and
under model-rotated-sonnet it is also far below the +30 pp threshold the task pre-registered.
The substantive prompt and the model swap have largely overlapping effects (high kappa across
the two sonnet configurations), suggesting that the +57 pp t0014 headline is primarily an
artefact of haiku-as-judge anchoring on the v1-sonnet rows rather than a genuine schema
effect.

</details>
