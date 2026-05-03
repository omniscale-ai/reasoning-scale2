# Predictions: `agent-evaluation`

10 predictions asset(s).

[Back to all predictions](../README.md)

---

<details>
<summary>📊 <strong>Phase 2 smoke condition A (scope-aware ReAct) on
FrontierScience-Olympiad</strong> (<code>phase2-smoke-a</code>) — 40
instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `phase2-smoke-a` |
| **Model ID** | — |
| **Model** | claude-haiku-4-5 (Anthropic) accessed via the local Claude Code CLI with a minimal system prompt. Agent library: scope_aware_react_v1 (t0006). Tool registry: minimal calculator + finish only. Granularity tag injected per phase per the v2 hierarchy from t0009. |
| **Datasets** | `hierarchical-annotation-v2` |
| **Format** | jsonl |
| **Instances** | 40 |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Created by** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Documentation** | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-a/description.md) |

**Metrics at creation:**

* **task_success_rate**: 0.025
* **overconfident_error_rate**: 0.6471
* **avg_decisions_per_task**: 1.2

# Phase 2 smoke condition A predictions

## Metadata

* **Name**: Phase 2 smoke condition A (scope-aware ReAct) on FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library scope_aware_react_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset,
  hierarchy-complete rows)
* **Format**: jsonl
* **Instances**: 40
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These predictions are condition A (scope-aware ReAct) of the Phase 2 A/B/C smoke harness on
FrontierScience-Olympiad. The agent runs the v2 hierarchy in phase order and emits one
trajectory record per turn with an explicit granularity tag (`global` / `subtask` / `atomic`)
injected into every Thought. The harness used a minimal tool registry (calculator + finish)
and the same model and tool budget as conditions B and C, so the only manipulated factor is
the granularity-conditioning prompt.

The smoke is intentionally narrow (single benchmark, single provider, N=40 row-runs paired
with B and partially with C). Its goal is a directional signal plus a sample-size calibration
for any follow-up confirmatory run.

## Model

`claude-haiku-4-5` accessed through the local Claude Code CLI with `--system-prompt`
overridden to a minimal scientific-reasoning preamble (see
`tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py`). The CLI is invoked with
`--tools ""` and `--setting-sources ""` to suppress the default Claude Code system prompt and
tool catalogue, which together cost roughly $0.10/call. With the override, per-call cost falls
to ~$0.005 with cache reuse, the 25× reduction the harness needs to fit the $20 cap. The
calibration judge that decides correctness uses `claude-haiku-4-5-20251001` for the same
reason.

## Data

The FrontierScience-Olympiad rows of `hierarchical-annotation-v2` (produced by t0009). Filter:
`benchmark == "FrontierScience-Olympiad" AND hierarchy_completeness == true`. The filter
yields 40 rows with 26 unique `task_id`s — `task_id` collisions in the upstream pilot file
persist into v2 and are flagged as suggestion S-0009-04 (deduplication remediation). The
harness processes all 40 rows; metrics are reported as per-row.

## Prediction Format

JSONL, one row per problem. Each line is a JSON object with these fields:

| Field | Type | Notes |
| --- | --- | --- |
| `condition` | string | "Condition A: scope-aware ReAct" for this asset |
| `task_id` | string | The v2 dataset row's `task_id` |
| `problem` | string | Full problem text passed to the agent |
| `gold_answer` | string | Concatenated gold global / subtask / atomic actions from v2 |
| `final_answer` | string\|null | The agent's `Finish` answer; `null` if the agent errored |
| `is_correct` | boolean | Judge verdict from `claude-haiku-4-5` against `gold_answer` |
| `decision_count` | int | Number of trajectory turns the agent produced |
| `final_confidence` | float\|null | Final-turn `confidence` extracted from the trajectory |
| `trajectory` | string | JSON-serialised list of turn records |
| `agent_refused` | boolean | True if the model returned a content-policy refusal |

A turn record carries the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007:
`{turn_index, granularity, thought, action, observation, confidence}`.

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `task_success_rate` | 0.025 | 1 / 40 (one chemistry row solved correctly) |
| `overconfident_error_rate` | 0.6471 | 11 of 17 incorrect runs reported high confidence |
| `avg_decisions_per_task` | 1.20 | ReAct converges in one or two turns, then `Finish` |

## Main Ideas

* On FrontierScience-Olympiad, condition A succeeds on only 1 of 40 problems. The benchmark is
  beyond the agent's no-tool capacity — most problems require multi-page derivations the agent
  emits as one large `Finish` answer that the judge rejects.
* Condition A's `final_confidence` is reliably populated (the ReAct prompt elicits it on every
  Thought) — but the calibration metric is dominated by the high failure rate, giving an
  overconfident-error-rate of 64.7%. With a higher base accuracy this metric would be more
  informative.
* The harness end-to-end runs cleanly at $0.10-0.15 per row. A confirmatory FrontierScience
  run detecting a 5pp paired effect at α=0.05 needs N≈157, well above this smoke's N=40.

## Summary

These are the scope-aware (A) condition's outputs from the project's first end-to-end Phase 2
run. The harness drives the v2 hierarchy in phase order, the agent emits a granularity-tagged
trajectory per row, and the haiku judge marks each output correct or incorrect against the v2
gold actions.

The headline finding is that the FrontierScience-Olympiad subset of the v2 dataset is too hard
for a no-tool agent: condition A solves only 1 of 40 problems. Condition B (Plan-and-Solve)
solves 0 of 40 in the matched run; condition C ran 11 of 40 before the budget halt. Within
this near-zero-success regime, condition A's overconfident-error-rate of 64.7% means the agent
confidently asserts wrong answers most of the time, in line with Xiong2024's diagnosis of LLM
calibration on hard reasoning problems.

For the project, the predictions are useful for two purposes: (a) they validate the harness
end-to-end, including the cost model, the per-row checkpointing, and the trajectory schema
parity with B and C; (b) they bound how informative a low-N FrontierScience run can be —
follow-up runs should either widen the benchmark mix (SWE-bench Verified, tau-bench) or scale
to ~150 rows on FrontierScience to detect the predicted 5pp scope-conditioning effect.

</details>

<details>
<summary>📊 <strong>Phase 2 smoke condition B (scope-unaware Plan-and-Solve) on
FrontierScience-Olympiad</strong> (<code>phase2-smoke-b</code>) — 40
instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `phase2-smoke-b` |
| **Model ID** | — |
| **Model** | claude-haiku-4-5 (Anthropic) accessed via the local Claude Code CLI with a minimal system prompt. Agent library: scope_unaware_planandsolve_v1 (t0007). Tool registry: minimal calculator + finish only. No granularity tag (condition B by design). |
| **Datasets** | `hierarchical-annotation-v2` |
| **Format** | jsonl |
| **Instances** | 40 |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |
| **Created by** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Documentation** | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-b/description.md) |

**Metrics at creation:**

* **task_success_rate**: 0.0
* **overconfident_error_rate**: 0.0
* **avg_decisions_per_task**: 6.525

# Phase 2 smoke condition B predictions

## Metadata

* **Name**: Phase 2 smoke condition B (scope-unaware Plan-and-Solve) on
  FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library
  scope_unaware_planandsolve_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset,
  hierarchy-complete rows)
* **Format**: jsonl
* **Instances**: 40
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These predictions are condition B (scope-unaware Plan-and-Solve) of the Phase 2 A/B/C smoke
harness on FrontierScience-Olympiad. The agent generates a free-form numbered plan, then
executes each step sequentially through a Plan-and-Execute loop. Trajectory records carry the
literal `granularity = "unspecified"` to mark the B condition. Same model, same tool registry,
same minimal-system-prompt CLI invocation, and the same set of 40 rows as condition A — the
only manipulated factor here is the absence of explicit granularity conditioning in the
agent's prompt template.

## Model

Same `claude-haiku-4-5` model and minimal-system-prompt CLI invocation as condition A. Agent
library is `scope_unaware_planandsolve_v1` (t0007). The Plan-and-Solve prompt does not elicit
a per-step verbalised confidence — this is a documented limitation of the v1 library and the
reason `final_confidence` is `null` for nearly every B row, which collapses the
`overconfident_error_rate` metric for B (see Main Ideas).

## Data

The same 40 FrontierScience-Olympiad hierarchy-complete rows from `hierarchical-annotation-v2`
that condition A processed.

## Prediction Format

JSONL, one row per problem; same schema as `phase2-smoke-a`. The trajectory `granularity`
field is the literal string `"unspecified"` for every turn, marking condition B.
`final_confidence` is `null` for B rows (Plan-and-Solve does not natively emit a verbalised
confidence label) — the harness records this as a known gap and surfaces it as a follow-up
suggestion to extend the t0007 library.

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `task_success_rate` | 0.000 | 0 / 40 |
| `overconfident_error_rate` | 0.000 | Collapsed: no rows surface `final_confidence`, so the
  Xiong2024 aggregator records zero overconfident errors by default. **Not comparable to A.**
  |
| `avg_decisions_per_task` | 6.53 | Plan-and-Solve runs longer trajectories than ReAct |

## Main Ideas

* Condition B solves zero of 40 FrontierScience-Olympiad problems with no tool use. The
  benchmark is beyond a no-tool Plan-and-Solve agent's capacity.
* The `overconfident_error_rate` metric is **not informative for condition B** in this version
  of the harness because Plan-and-Solve trajectories do not surface a `final_confidence`
  field. This gap is documented and queued for follow-up: either extend
  `scope_unaware_planandsolve_v1` to emit per-step confidence (Xiong2024 §3.2), or run a
  separate calibration pass that asks the model to rate its final answer in a follow-up call.
* Condition B uses ~5× more decisions per task than condition A (6.5 vs 1.2). The longer
  trajectories are not converting into higher accuracy on this benchmark — both stay near
  zero.

## Summary

These are condition B's outputs from the project's first end-to-end Phase 2 smoke. With no
granularity tag and a generic Plan-and-Solve prompt, the agent solves 0 of 40 FrontierScience
problems — slightly worse than condition A's 1 of 40 but within the noise floor of the smoke's
sample size (the paired McNemar test gives p = 1.0 because there are no discordant pairs at
N=40 across A and B). The results validate that the harness ran cleanly to completion on
condition B as well as condition A; the predictions file is well-formed; and the cost per row
is comparable to condition A (~$0.10-0.15).

For the project, the most actionable finding from these predictions is the
`overconfident_error_rate` collapse: the v1 t0007 library does not emit verbalised confidence
in trajectory records, so Metric 2 cannot be computed honestly for condition B without further
work. This is the single most important methodological finding from the smoke and gates any
future A-vs-B-vs-C run that wants to test RQ2.

</details>

<details>
<summary>📊 <strong>Phase 2 smoke condition C (scope-mismatched random) on
FrontierScience-Olympiad</strong> (<code>phase2-smoke-c</code>) — 11
instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `phase2-smoke-c` |
| **Model ID** | — |
| **Model** | claude-haiku-4-5 via local Claude Code CLI. Agent library: matched_mismatch_v1 (t0010), strategy='random', delegate=scope_unaware_planandsolve_v1. Each phase receives a deliberately incorrect granularity tag drawn uniformly from the two non-correct choices. |
| **Datasets** | `hierarchical-annotation-v2` |
| **Format** | jsonl |
| **Instances** | 11 |
| **Date created** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Created by** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Documentation** | [`description.md`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-c/description.md) |

**Metrics at creation:**

* **task_success_rate**: 0.0
* **overconfident_error_rate**: 0.0
* **avg_decisions_per_task**: 26.0

# Phase 2 smoke condition C predictions (partial)

## Metadata

* **Name**: Phase 2 smoke condition C (scope-mismatched random) on FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library matched_mismatch_v1
  (t0010) wrapping scope_unaware_planandsolve_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset,
  hierarchy-complete rows; first 11 of 40)
* **Format**: jsonl
* **Instances**: 11 (partial; budget halt before remaining 29)
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These are the partial outputs of condition C (scope-mismatched, `random` strategy) of the
Phase 2 A/B/C smoke harness on FrontierScience-Olympiad. The matched-mismatch wrapper from
t0010 walks the v2 hierarchy in phase order, identifies the correct granularity at each step
from the annotation, and replaces it with a uniformly-random incorrect tag drawn from the two
non-correct choices. The wrapper delegates the actual model call to
`scope_unaware_planandsolve_v1` so condition C's prompt structure matches B's exactly except
for the (deliberately wrong) tag.

The run halted after row 11 of 40 when the harness hit the $18 budget cap. The 11 rows that
completed are paired with the corresponding rows in conditions A and B for the limited paired
analysis reported in the task results.

## Model

Same `claude-haiku-4-5` model, same minimal-system-prompt CLI invocation, same tool registry,
and same set of upstream rows. Agent: `matched_mismatch_v1` with `mismatch_strategy="random"`
and `delegate="scope_unaware_planandsolve"`.

## Data

The first 11 FrontierScience-Olympiad hierarchy-complete rows from
`hierarchical-annotation-v2`, processed in the same order conditions A and B used.

## Prediction Format

JSONL, one row per problem; same schema as conditions A and B. The trajectory `granularity`
field carries the *wrong* tag the wrapper injected; the correct tag for the same step is
recorded separately in trajectory record `extras._correct_granularity`.

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `task_success_rate` | 0.000 | 0 / 11 |
| `overconfident_error_rate` | 0.000 | Same Plan-and-Solve confidence gap as B; not informative |
| `avg_decisions_per_task` | 26.0 | C trajectories run *much* longer than B (6.5) — the wrong
  granularity tag triggers replanning loops |

## Main Ideas

* Condition C ran 11 of 40 rows before the harness budget halt at $18.37. The metrics reported
  in `metrics.json` for C are computed on those 11 rows only, with a paired analysis against
  the same 11-row subset of A and B.
* The most striking observation from the partial C trajectories is the **6× decision-count
  increase** versus B (26.0 vs 6.5). The wrong granularity tag pushes Plan-and-Solve into long
  re-planning loops without converging on a final answer — exactly the failure mode RQ5
  predicted, but in a form invisible to the registered Metric 1 because both B and C end at
  zero accuracy.
* The harness budget model needs revision before any future C run: at ~$0.40 per C row (vs
  ~$0.10 for A/B) the wrapper-induced replanning eats budget. Either (a) cap turns per row in
  the C delegate, (b) reserve a dedicated budget for C, or (c) batch C against an easier
  benchmark where the success-rate signal can be observed.

## Summary

These are the 11 partial outputs of condition C from the project's first end-to-end Phase 2
smoke. The run halted at the $18 budget cap before reaching the remaining 29 rows. Within the
11 completed rows, condition C solved zero problems (in line with conditions A and B on the
same hard FrontierScience-Olympiad benchmark) but spent dramatically more decisions per row
(26 vs 6.5 for B). The all-zero success rate makes RQ5 (sub-hypothesis 2: "C ranks worst on
Metrics 1 and 2") untestable in this run — there is no spread between A, B, and C on the
success metric to rank them.

For the project, condition C's most useful contribution from the smoke is a budget-model
finding: the matched-mismatch wrapper triggers Plan-and-Solve re-planning loops that push the
per-row cost roughly 4× higher than the matched B condition. Any future A/B/C run on a hard
benchmark must either cap C's turn count or reserve a separate budget envelope for C.

</details>

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

<details>
<summary>📊 <strong>Variant A (reused pointer to t0026 a-scope-aware
predictions)</strong> (<code>abc-rerun-a-reused</code>) — 147 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `abc-rerun-a-reused` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport), max_turns=10, max_tokens=4096. Inherited verbatim from t0026's a-scope-aware predictions; t0027 does not re-run variant A. B and C in t0027 also run on claude-sonnet-4-6, so all three variants share the same model and the A-vs-B and A-vs-C McNemar comparisons isolate scaffold/parser differences cleanly. The original t0027 task description erroneously stated claude-opus-4-7 for B/C; that was a transcription error caught during implementation by inspecting t0026's paths.py and corrected. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 147 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Documentation** | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/description.md) |

**Metrics at creation:**

* **success_rate_judge_sonnet**: 0.04081632653061224
* **n_success**: 6
* **n_instances_inherited_from_t0026**: 147
* **n_paired_used_in_t0027_analysis**: 130
* **total_cost_usd**: 0.0

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
contract (`predictions: 3`) while making explicit that variant A is not re-run in this task.
The t0027 task description directs that "A is not re-run; t0026's A trajectories are valid for
this paired analysis. We re-use them by reference rather than re-generating." The actual
per-instance predictions live unchanged in t0026's `a-scope-aware` predictions asset; this
folder contains only a pointer JSON file that names the source path. Consumers (the McNemar
analysis script, calibration script, plotting scripts) read the source JSONL path directly. No
prediction data is duplicated into this asset.

## Model

claude-sonnet-4-6, accessed via the Anthropic CLI transport with a 10-turn ReAct cap and 4096
max output tokens per call. The agent runs the scope-aware ReAct scaffold from t0010 with
atomic granularity. Configuration is inherited verbatim from t0026's `a-scope-aware` asset.
The t0027 re-run uses **claude-sonnet-4-6** for variants B and C as well, so all three
variants share the same model. The original t0027 task description erroneously stated
claude-opus-4-7 for B/C; that was a transcription error and was corrected after discovering
the mismatch via t0026's `paths.py` and trajectory error messages. The A-vs-B and A-vs-C
McNemar comparisons in t0027 are therefore clean same-model contrasts (different scaffolds,
same model).

## Data

The 147 inherited instances span SWE-bench Verified (20, stratified by difficulty bucket),
Tau-bench (87, deterministic by domain+task_index), and FrontierScience Olympiad (40,
deterministic by task_id). The exact instance IDs and source SHA-256 hashes are recorded in
t0026's `data/instance_manifest.json`. The t0027 paired analysis filters to the **130 paired
instances** — the intersection of all three t0026 variants' completed instances (instances
where every variant returned a non-null final answer or judge verdict).

## Prediction Format

JSON Lines — one JSON object per line. Each row carries: `instance_id` (str), `subset` (str),
`variant` (str), `final_answer` (str|null), `final_confidence` (float|null; null for variant A
because A does not elicit verbalised confidence), `cost_usd` (float), `trajectory_path`
(str|null), `judge_sonnet_success` (bool), `judge_sonnet_rationale` (str),
`judge_opus_success` (bool|null; non-null only on the inter-judge subset of 30 instances),
`judge_opus_rationale` (str|null). The schema is identical to the t0026 source asset.

This asset's `files/pointer.json` is a small JSON object pointing back to the t0026 source
path; it is not the prediction data. Consumers must read the t0026 source JSONL listed in the
Metadata section to access the actual records.

## Metrics

* Success rate (sonnet judge, all 147 t0026 instances): **0.0408** (6/147)
* Success rate restricted to the 130 paired instances used in t0027's analysis: computed on
  the fly by the t0027 analysis script (`code/run_analysis.py`); see
  `data/mcnemar_results.json` for the exact paired contingency tables and per-subset
  success-rate breakdowns
* Cost per instance (t0026 inherited): **$0.0313**
* Re-run cost in t0027: **$0** (no API calls; predictions are reused by reference)

## Main Ideas

* **No re-run, no duplication.** The t0027 task description directs that A be reused by
  reference; the actual JSONL is not copied into this asset. The pointer file records the
  source path so downstream consumers can locate it without ambiguity.
* **No mixed-model confound.** All three variants (A, B, C) use claude-sonnet-4-6. The
  original t0027 task description stated claude-opus-4-7 for B/C, but that was a transcription
  error caught during implementation by inspecting t0026's `paths.py` and trajectory error
  messages. With the corrected model, the A-vs-B and A-vs-C McNemar comparisons isolate
  scaffold/parser differences cleanly. Re-running A was unnecessary because t0026's A
  trajectories were already on the correct model.
* **Filtering to the 130 paired set is performed at analysis time.** The pointer asset itself
  reports the inherited count (147) for traceability with t0026; the McNemar test runs on the
  paired intersection of 130. The exact paired set is computed by `code/run_analysis.py` from
  the three variants' JSONL files at run time.

## Summary

This is a pointer-only predictions asset. Variant A's per-instance predictions, trajectories,
and judge verdicts are inherited verbatim from t0026's `a-scope-aware` asset; nothing is
re-generated in t0027. The `files/pointer.json` file names the source predictions directory
and the source JSONL so the McNemar analysis script and calibration script can locate the
underlying records by reading the canonical t0026 path directly. The t0027 paired analysis
filters the inherited 147 instances to the 130 paired set defined as the intersection of all
three t0026 variants' completed instances.

The asset exists to make explicit, in the t0027 expected_assets contract, that variant A is
part of the analysis but is not produced by this task. All three variants share
claude-sonnet-4-6, so the A-vs-B McNemar in t0027 is a clean "same model, different scaffold"
comparison and the A-vs-C McNemar is a "same model, different scaffold + granularity-mismatch
wrapper" comparison.

</details>

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
<summary>📊 <strong>Variant B (re-run): plan_and_solve_v3 with bounded plan-recovery
chain</strong> (<code>abc-rerun-b</code>) — 130 instances (jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `abc-rerun-b` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport). max_turns=10, max_tokens=4096. The agent is plan_and_solve_v3 (built in this task as an upgrade to t0021's plan_and_solve_v2) which introduces a bounded 3-attempt plan-parse recovery chain: attempt 1 is the standard PS+ template; attempt 2 re-prompts with a corrective preamble; attempt 3 forces JSON-mode parsing as a structural fallback. The agent only re-raises MalformedPlanError if all three attempts fail. The first/second/third attempt outcome is recorded in the per-instance plan_parser_recovery_path field. Note: model is claude-sonnet-4-6 to match what t0026 actually ran; the original t0027 task description erroneously stated claude-opus-4-7 and was corrected after discovering the mismatch via t0026's paths.py. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 130 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Documentation** | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-b/description.md) |

# Variant B (re-run): plan_and_solve_v3 with bounded plan-recovery chain

## Metadata

* **Variant**: b
* **Model**: claude-sonnet-4-6 (Anthropic CLI transport, 10-turn cap, 4096 max output tokens)
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 130 (paired set; intersection of t0026 a/b/c completed runs)
* **Per-subset**: 20 swebench + 84 taubench + 26 frontsci
* **Created by**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c

## Overview

This predictions asset is the t0027 re-run of variant B on the 130 paired instances inherited
from t0026, produced to address suggestion S-0026-01 (B's parser fragility under the v2 plan
parser). In t0026, 16 of 130 paired runs of variant B (12.3%) collapsed to MalformedPlanError
because the single-shot plan parser could not recover from common model formatting drift
(numbered lists with non-canonical separators, prose preambles, bracketed step labels). Those
failures contaminated the A-vs-B paired McNemar comparison since they appeared as agent-level
failures rather than capability ceilings.

The t0027 re-run replaces the v2 agent with a new plan_and_solve_v3 library
(`assets/library/plan_and_solve_v3/`) that wraps the same v2 plan/solve loop with a bounded
3-attempt plan-parse recovery chain:

1. **Clean** — the standard PS+ template; if `parse_plan` succeeds, return immediately.
2. **Reprompt** — on first parse failure, re-issue the planner call with a short corrective
   preamble asking the model to format the plan as a clean numbered list.
3. **JSON-mode** — on second parse failure, issue a third call that forces JSON-mode output
   and parses the steps from a structured payload.
4. **all_failed** — if all three attempts fail, the agent re-raises MalformedPlanError exactly
   as v2 did, so the failure is still observable but is now bounded by the chain rather than
   by a single fragile pass.

Each per-instance prediction records which path was taken (`plan_parser_recovery_path` ∈
{clean, reprompt, json_mode, all_failed, unknown}) and the number of attempts used
(`plan_parser_attempts` ∈ {1, 2, 3}). The `raised_malformed_plan_error` boolean is True iff
all three attempts failed.

The asset shares the schema and judge wiring with t0026's `b-plan-and-solve` so paired McNemar
analyses (A vs B in this task; B-old vs B-new across t0026 and t0027 by joining on
instance_id) can re-use the same instance manifest and the same primary sonnet judge.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The agent runs the
plan_and_solve_v3 scaffold with `max_turns=10` and `max_tokens=4096` per call. Tool registry
is the canonical `build_planandsolve_tool_registry` from t0012 (text-only generic tools — no
scope-aware tools, no filesystem, no shell). Cost is tracked in-memory via the project
CostTracker; per-instance cost is written to the JSONL `cost_usd` field. Inter-judge agreement
subset (30 instances on opus) is *not* re-collected in t0027 — only the primary sonnet judge
runs in this task.

## Data

The 130 paired instances are the intersection of all three t0026 variants' completed instances
— i.e., instances where every variant returned a non-null judge_sonnet_success. The exact
instance ids and subset breakdown live in `data/paired_manifest.json`. The full 147-instance
manifest is also persisted in `data/instance_manifest.json` for traceability with t0026 even
though t0027 only re-runs the 130-paired subset.

## Prediction Format

JSON Lines — one JSON object per line, identical schema to t0026's `b-plan-and-solve` plus
three new diagnostic fields. Each row carries:

* `instance_id` (str), `subset` (str ∈ {swebench, taubench, frontsci}), `variant` ("b")
* `final_answer` (str | null), `final_confidence` (float | null; 0..1 verbalised confidence)
* `cost_usd` (float; per-instance cost from CostTracker)
* `trajectory_path` (str | null; absolute path to the per-instance trajectory JSON in
  `data/runs/b/`)
* `judge_sonnet_success` (bool), `judge_sonnet_rationale` (str)
* `plan_parser_recovery_path` (str ∈ {clean, reprompt, json_mode, all_failed, unknown})
* `plan_parser_attempts` (int ∈ {1, 2, 3})
* `raised_malformed_plan_error` (bool; True iff all three plan-parse attempts failed)

The opus inter-judge fields (`judge_opus_success`, `judge_opus_rationale`) are not produced in
this re-run; downstream consumers comparing to t0026 should treat them as absent.

## Metrics

The full set of headline metrics is computed by `code/run_analysis.py` and written to
`results/metrics.json`. The most relevant ones to register at the project level are:

* `success_rate_b_paired` — McNemar success rate for variant B on the 130-paired set
* `parser_failure_rate_b` — fraction of B runs with `raised_malformed_plan_error=True`
  (target: significantly below the 12.3% observed in t0026)
* `total_cost_usd_b` — wall-clock cost from CostTracker

Per-subset success-rate breakdowns and the recovery-path distribution table are persisted in
`data/mcnemar_results.json` and the calibration ECE in `data/calibration.json`.

## Main Ideas

* The v3 fallback chain restores B as a viable agent under model formatting drift. The
  recovery path distribution itself is a useful diagnostic: instances landing on `reprompt` or
  `json_mode` identify families of problems where the model's natural plan format diverges
  from PS+ template expectations.
* All three variants (A, B, C) use the same model — claude-sonnet-4-6. The original t0027 task
  description erroneously stated claude-opus-4-7, but t0026 actually ran on Sonnet (verified
  via t0026's `paths.py:60` and trajectory error messages). t0027 was corrected to match. The
  A-vs-B McNemar is therefore a clean comparison: same model, different scaffold (scope-aware
  ReAct vs plan-and-solve with v3 fault-tolerant parser).
* The 130-paired filter ensures the McNemar test in `data/mcnemar_results.json` is a true
  paired-difference test on the same instances across variants, with Bonferroni-corrected α =
  0.025.

## Summary

This asset re-runs variant B on the 130 paired t0026 instances using the new plan_and_solve_v3
library that we developed in this task to fix the MalformedPlanError defect that contaminated
12.3% of t0026's variant-B runs. The new agent retains the v2 plan/solve loop but adds a
bounded three-attempt plan-parse recovery chain (clean -> re-prompt -> JSON-mode), records the
recovery path taken on each instance, and only re-raises MalformedPlanError when all three
attempts fail.

The headline finding for this asset will be the new variant-B parser-failure rate (target:
substantially below 12.3%) and the recovery-path distribution that diagnoses *which* recovery
strategy was needed for each instance. The McNemar A-vs-B analysis in `code/run_analysis.py`
re-evaluates RQ1 ("does the scope-aware ReAct scaffold beat plan-and-solve under a fair
parser?") under the fixed parser. Since A and B share claude-sonnet-4-6, the McNemar isolates
the scaffold/parser difference. The B-vs-C McNemar addresses RQ5 ("does scaffold-granularity
matter when the agent is plan-and-solve, holding parser fixed?") and is now meaningful for the
first time because t0027's variant C delegates to plan_and_solve_v3 as well, eliminating the
C-vs-A delegate-conflation defect (S-0026-02) that made t0026's RQ5 uninterpretable.

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
<summary>📊 <strong>Variant C (re-run): matched_mismatch_v2 wrapping
plan_and_solve_v3</strong> (<code>abc-rerun-c</code>) — 130 instances
(jsonl)</summary>

| Field | Value |
|---|---|
| **ID** | `abc-rerun-c` |
| **Model ID** | — |
| **Model** | claude-sonnet-4-6 via Anthropic API (CLI transport). max_turns=10, max_tokens=4096. The agent is matched_mismatch_v2 (built in this task) which forks t0010's mismatch wrapper to delegate to PlanAndSolveAgentV3 instead of the original scope_aware_react. The wrapper still applies the adversarial granularity perturbation map (global -> atomic, subtask -> atomic, atomic -> global) to the t0010-style synthetic v2 hierarchy before running the underlying agent, producing the same shape of mismatched conditioning as t0010 but now over a plan_and_solve scaffold. The plan-parse 3-attempt recovery chain from plan_and_solve_v3 is inherited unchanged. Note: model is claude-sonnet-4-6 to match what t0026 actually ran; the original t0027 task description erroneously stated claude-opus-4-7 and was corrected after discovering the mismatch via t0026's paths.py. |
| **Datasets** | `swebench-verified-subset`, `taubench-subset`, `frontierscience-olympiad-subset` |
| **Format** | jsonl |
| **Instances** | 130 |
| **Date created** | 2026-05-02 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`llm-as-judge`](../../../meta/categories/llm-as-judge/) |
| **Created by** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Documentation** | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-c/description.md) |

# Variant C (re-run): matched_mismatch_v2 wrapping plan_and_solve_v3

## Metadata

* **Variant**: c
* **Model**: claude-sonnet-4-6 (Anthropic CLI transport, 10-turn cap, 4096 max output tokens)
* **Datasets**: swebench-verified-subset, taubench-subset, frontierscience-olympiad-subset
* **Format**: jsonl
* **Instances**: 130 (paired set; intersection of t0026 a/b/c completed runs)
* **Per-subset**: 20 swebench + 84 taubench + 26 frontsci
* **Created by**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c

## Overview

This predictions asset is the t0027 re-run of variant C on the 130 paired instances inherited
from t0026, produced to address suggestion S-0026-02 (the wrong-delegate defect). In t0026,
variant C delegated to the t0010 `scope_aware_react` agent rather than to a plan-and-solve
scaffold, which made C structurally identical to variant A (scope-aware ReAct) plus
mismatched-granularity noise. Under that delegate, RQ5 ("does scaffold-granularity matter when
the agent is plan-and-solve, holding parser fixed?") was uninterpretable because variant B
(plan-and-solve) and variant C (ReAct + noise) tested different scaffolds, not the same
scaffold under matched/mismatched granularity.

The t0027 re-run uses a new `matched_mismatch_v2` library
(`assets/library/matched_mismatch_v2/`) that forks t0010's mismatch wrapper to delegate to
`PlanAndSolveAgentV3` instead of `scope_aware_react`. The wrapper continues to apply the
adversarial granularity perturbation map (`global -> atomic`, `subtask -> atomic`, `atomic ->
global`) to a t0010-style synthetic v2 hierarchy before running the agent, producing the same
shape of mismatched conditioning as t0010 but now over the plan-and-solve scaffold.
Concretely, every row in this asset reports `delegate = "scope_unaware_planandsolve_v3"` —
never `scope_aware_react`.

Because the underlying agent is plan_and_solve_v3, the bounded 3-attempt plan-parse recovery
chain (clean -> reprompt -> JSON-mode) and its per-instance diagnostics
(`plan_parser_recovery_path`, `plan_parser_attempts`, `raised_malformed_plan_error`) are
inherited unchanged. This means the C-vs-B McNemar comparison in `code/run_analysis.py` is now
a clean "same agent, matched vs mismatched granularity" contrast, with parser fragility
neutralized in both arms.

## Model

claude-sonnet-4-6 accessed via the Anthropic CLI transport. The wrapper drives
plan_and_solve_v3 once per instance with `max_turns=10` and `max_tokens=4096`. Tool registry
is the canonical `build_planandsolve_tool_registry` from t0012 (text-only generic tools).
Synthetic v2 hierarchies are constructed from each problem's `problem_text` using the same
4-phase construction as t0026's runner.py (verbatim copy in
`code/run_abc_rerun.py::_synthetic_annotation`): one global phase followed by three atomic
phases that label sub-portions of the problem text. The adversarial perturbation map is
applied unchanged from t0010.

Cost is tracked via the project CostTracker; per-instance cost is written to the JSONL
`cost_usd` field. Inter-judge agreement subset (30 instances on opus) is *not* re-collected in
t0027 — only the primary sonnet judge runs in this task.

## Data

The 130 paired instances are the intersection of all three t0026 variants' completed instances
— i.e., instances where every variant returned a non-null `judge_sonnet_success`. The exact
instance ids and per-subset breakdown live in `data/paired_manifest.json`. The full
147-instance manifest is also persisted in `data/instance_manifest.json` for traceability with
t0026 even though t0027 only re-runs the 130-paired subset.

## Prediction Format

JSON Lines — one JSON object per line, identical schema to variant B in this task plus an
explicit `delegate` field. Each row carries:

* `instance_id` (str), `subset` (str ∈ {swebench, taubench, frontsci}), `variant` ("c")
* `final_answer` (str | null), `final_confidence` (float | null; 0..1 verbalised confidence)
* `cost_usd` (float), `trajectory_path` (str | null; per-instance trajectory in
  `data/runs/c/`)
* `judge_sonnet_success` (bool), `judge_sonnet_rationale` (str)
* `plan_parser_recovery_path` (str ∈ {clean, reprompt, json_mode, all_failed, unknown})
* `plan_parser_attempts` (int ∈ {1, 2, 3})
* `raised_malformed_plan_error` (bool; True iff all three plan-parse attempts failed)
* `delegate` (str = "scope_unaware_planandsolve_v3" on every row in this asset)

The opus inter-judge fields (`judge_opus_success`, `judge_opus_rationale`) are not produced in
this re-run; downstream consumers comparing to t0026 should treat them as absent.

## Metrics

The full set of headline metrics is computed by `code/run_analysis.py` and written to
`results/metrics.json`. The metrics relevant to register at the project level are:

* `success_rate_c_paired` — McNemar success rate for variant C on the 130-paired set
* `parser_failure_rate_c` — fraction of C runs with `raised_malformed_plan_error=True`
* `total_cost_usd_c` — wall-clock cost from CostTracker

Per-subset success-rate breakdowns and the recovery-path distribution table are persisted in
`data/mcnemar_results.json` and the calibration ECE in `data/calibration.json`.

## Main Ideas

* The matched_mismatch_v2 library fixes the structural defect that made t0026's variant C
  meaningless for RQ5: C now delegates to plan_and_solve_v3, so B and C share the same
  scaffold and parser, isolating the granularity-conditioning effect as the only systematic
  difference.
* The adversarial granularity perturbation policy is preserved verbatim from t0010 (`global ->
  atomic`, `subtask -> atomic`, `atomic -> global`), so this task's C results compose cleanly
  with the t0010 matched-mismatch evaluation that established the wrapper's behaviour on a
  different model and scaffold combination.
* All three variants (A, B, C) use the same model — claude-sonnet-4-6. The original t0027 task
  description erroneously stated claude-opus-4-7 for B/C, but t0026 actually ran on Sonnet
  (verified via t0026's `paths.py:60` and trajectory error messages). t0027 was corrected to
  match. The B-vs-C McNemar therefore isolates the granularity-conditioning effect cleanly:
  same model, same scaffold, same parser, only the wrapper differs.

## Summary

This asset re-runs variant C on the 130 paired t0026 instances using the new
matched_mismatch_v2 library, which retargets the t0010 mismatch wrapper at plan_and_solve_v3
instead of `scope_aware_react`. This eliminates the wrong-delegate defect (S-0026-02) that
made t0026's variant C structurally identical to A and rendered RQ5 uninterpretable. Because B
and C now share the same scaffold and parser, the B-vs-C McNemar in `code/run_analysis.py` is
a clean test of granularity-conditioning under the plan-and-solve agent.

The headline finding for this asset will be the difference in success rate between variant B
(matched plan-and-solve) and variant C (mismatched plan-and-solve). If the gap is significant
after Bonferroni correction (α = 0.025), it confirms that scaffold-granularity affects
plan-and-solve performance even when the underlying scaffold and parser are held fixed; if the
gap is not significant, it suggests the granularity-conditioning effect observed in t0010 was
scaffold- or model-specific and does not generalize to plan-and-solve under claude-sonnet-4-6.

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
