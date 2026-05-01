---
spec_version: "2"
answer_id: "does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges"
answered_by_task: "t0019_v2_judge_calibration_sonnet"
date_answered: "2026-05-01"
confidence: "low"
---
# Does v2 keep a 30+ pp delta under substantive and sonnet judges?

## Question

Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under a
sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring?

## Short Answer

The evidence is mixed. Under substantive-sonnet the schema-only delta is +24.6 pp and under
model-rotated-sonnet it is +37.3 pp, vs the t0014 baseline of +58.0 pp. The +57 pp headline does not
cleanly survive a stronger judge, but neither does it collapse below +30 pp on both configurations;
the answer depends on which sonnet judge configuration is treated as canonical.

## Research Process

We re-judged a fixed 55-row pool (12 v1-sonnet rows from t0005, 23 v2-haiku rows from t0009 with
t0015 benchmark-label corrections applied, and 20 v2-sonnet rows from t0014) under three judge
configurations: the cached original-haiku verdicts from t0014/t0005 (baseline), a substantive critic
prompt that asks claude-sonnet-4-6 to simulate executing the atomics in order, and a model-rotated
configuration that keeps the original prompt verbatim and only swaps the judge model from
claude-haiku-4-5 to claude-sonnet-4-6. We did not re-annotate; only the judge stage changes. The two
sonnet configurations were run via the local `claude` CLI subprocess because the OAuth-issued API
key in this environment lacks sonnet quota (see `intervention/critical_step_blocked.md`).

For each (annotator x judge_config) cell we computed the binary acceptance rate, the Wilson 95%
confidence interval, and the schema-only delta (v2-haiku minus v1-sonnet) and model-only delta
(v2-sonnet minus v2-haiku) within each judge configuration. We also computed Cohen's kappa between
the three judge configurations on the per-row binary verdict.

## Evidence from Papers

The papers method was not used directly in this task. The literature priors that motivate the
question (Zhou2022 on judge anchoring, Boisvert2024 on hierarchical-annotation effect sizes,
Xiong2024 on within-family judge bias) were already surveyed in the t0017 literature task and are
referenced for comparison only; no new paper download or summarization was performed here.

## Evidence from Internet Sources

The internet method was not used in this task. The data sources are entirely internal: t0014's
v2-sonnet annotations, t0009 v2-haiku annotations with t0015 corrections applied, t0005 v1-sonnet
judgments, and the 110 fresh sonnet judge calls produced by this task's runners.

## Evidence from Code or Experiments

The 9-cell evidence table from `assets/predictions/v2-judge-calibration/files/predictions.jsonl`:

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

Schema-only delta (v2-haiku minus v1-sonnet) and model-only delta (v2-sonnet minus v2-haiku) under
each judge configuration:

| Judge | Schema-only delta | Model-only delta |
| --- | --- | --- |
| original-haiku (baseline, t0014/t0005) | +58.0 pp | -1.3 pp |
| substantive-sonnet | +24.6 pp | +8.7 pp |
| model-rotated-sonnet | +37.3 pp | +4.3 pp |

Decision-criteria check-off (each criterion was pre-registered in `task_description.md`):

* **Schema-only delta drops below +30 pp under substantive-sonnet**: Yes (+24.6 pp)
* **Schema-only delta drops below +30 pp under model-rotated-sonnet**: No (+37.3 pp)
* **Schema-only delta stays at or above +45 pp under substantive-sonnet**: No (+24.6 pp)
* **Schema-only delta stays at or above +45 pp under model-rotated-sonnet**: No (+37.3 pp)
* **Model-only delta swings by 5+ pp under substantive-sonnet vs baseline**: Yes (delta-of-deltas
  +10.0 pp)
* **Model-only delta swings by 5+ pp under model-rotated-sonnet vs baseline**: Yes (delta-of-deltas
  +5.7 pp)
* **Model-only delta stays within +/- 2 pp under substantive-sonnet vs baseline**: No
* **Model-only delta stays within +/- 2 pp under model-rotated-sonnet vs baseline**: No

## Synthesis

The +57 pp v2-vs-v1 schema-only headline observed in t0014 (under haiku as judge) shifts
substantially under the stronger judges (substantive +24.6 pp, model-rotated +37.3 pp vs baseline
+58.0 pp). Under both sonnet configurations the schema-only delta is much smaller, and the
model-only delta shifts in lock-step. This supports the interpretation that the t0014 headline is
partially an artefact of haiku judge anchoring on v1-sonnet hierarchies rather than a clean signal
that the v2 schema by itself produces dramatically more correct decompositions; both prompt-swap and
model-swap shrink the gap to a similar magnitude, suggesting model anchoring dominates prompt
anchoring on this pool.

## Limitations

* **n = 55 is small** (12 v1, 23 v2-haiku, 20 v2-sonnet); Wilson 95% CI half-widths on the per-cell
  rates are 12-30 pp, so per-cell rate differences below ~10 pp should not be over-interpreted.
* **The original-haiku verdicts are read from cached fields** (`judge_verdict` on each row), which
  means the baseline cell's per-call cost and elapsed-time fields are missing in the predictions
  JSONL. The accept_rate is still authoritative because t0014's runner emitted it via the same
  parser used here.
* **Two of the v1-sonnet rows are FrontierScience-Olympiad rows that t0014 already analysed**; the
  model-only delta is therefore not entirely independent of t0014's scope. Future replications on a
  fresh-pool task (S-0014-04) will give the cleaner test.
* **All sonnet calls went through the `claude` CLI subprocess** because the OAuth-issued API key in
  this environment lacks sonnet quota; this raised the per-call cost from the planned ~$0.024/call
  (SDK + cache hits) to ~$0.18/call (CLI + cache-creation overhead) and required raising the task
  budget cap from $4.50 to $20.00. See `intervention/critical_step_blocked.md`.

## Sources

* Predictions asset: `assets/predictions/v2-judge-calibration/files/predictions.jsonl`
* Task: `t0005_hierarchical_annotation_pilot_v1`
* Task: `t0009_hierarchical_annotation_v2`
* Task: `t0014_v2_annotator_sonnet_rerun`
* Task: `t0015_correct_proxy_benchmark_labels`
