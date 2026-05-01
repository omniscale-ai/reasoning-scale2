---
spec_version: "2"
predictions_id: "phase2-smoke-a"
documented_by_task: "t0012_phase2_abc_smoke_frontierscience"
date_documented: "2026-05-01"
---

# Phase 2 smoke condition A predictions

## Metadata

* **Name**: Phase 2 smoke condition A (scope-aware ReAct) on FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library scope_aware_react_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset, hierarchy-complete
  rows)
* **Format**: jsonl
* **Instances**: 40
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These predictions are condition A (scope-aware ReAct) of the Phase 2 A/B/C smoke harness on
FrontierScience-Olympiad. The agent runs the v2 hierarchy in phase order and emits one
trajectory record per turn with an explicit granularity tag (`global` / `subtask` / `atomic`)
injected into every Thought. The harness used a minimal tool registry (calculator + finish) and
the same model and tool budget as conditions B and C, so the only manipulated factor is the
granularity-conditioning prompt.

The smoke is intentionally narrow (single benchmark, single provider, N=40 row-runs paired with
B and partially with C). Its goal is a directional signal plus a sample-size calibration for any
follow-up confirmatory run.

## Model

`claude-haiku-4-5` accessed through the local Claude Code CLI with `--system-prompt`
overridden to a minimal scientific-reasoning preamble (see
`tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py`). The CLI is invoked with
`--tools ""` and `--setting-sources ""` to suppress the default Claude Code system prompt and
tool catalogue, which together cost roughly $0.10/call. With the override, per-call cost falls
to ~$0.005 with cache reuse, the 25× reduction the harness needs to fit the $20 cap. The
calibration judge that decides correctness uses `claude-haiku-4-5-20251001` for the same reason.

## Data

The FrontierScience-Olympiad rows of `hierarchical-annotation-v2` (produced by t0009). Filter:
`benchmark == "FrontierScience-Olympiad" AND hierarchy_completeness == true`. The filter yields
40 rows with 26 unique `task_id`s — `task_id` collisions in the upstream pilot file persist into
v2 and are flagged as suggestion S-0009-04 (deduplication remediation). The harness processes
all 40 rows; metrics are reported as per-row.

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
* The harness end-to-end runs cleanly at $0.10-0.15 per row. A confirmatory FrontierScience run
  detecting a 5pp paired effect at α=0.05 needs N≈157, well above this smoke's N=40.

## Summary

These are the scope-aware (A) condition's outputs from the project's first end-to-end Phase 2
run. The harness drives the v2 hierarchy in phase order, the agent emits a granularity-tagged
trajectory per row, and the haiku judge marks each output correct or incorrect against the v2
gold actions.

The headline finding is that the FrontierScience-Olympiad subset of the v2 dataset is too hard
for a no-tool agent: condition A solves only 1 of 40 problems. Condition B (Plan-and-Solve)
solves 0 of 40 in the matched run; condition C ran 11 of 40 before the budget halt. Within this
near-zero-success regime, condition A's overconfident-error-rate of 64.7% means the agent
confidently asserts wrong answers most of the time, in line with Xiong2024's diagnosis of LLM
calibration on hard reasoning problems.

For the project, the predictions are useful for two purposes: (a) they validate the harness
end-to-end, including the cost model, the per-row checkpointing, and the trajectory schema
parity with B and C; (b) they bound how informative a low-N FrontierScience run can be —
follow-up runs should either widen the benchmark mix (SWE-bench Verified, tau-bench) or scale
to ~150 rows on FrontierScience to detect the predicted 5pp scope-conditioning effect.
