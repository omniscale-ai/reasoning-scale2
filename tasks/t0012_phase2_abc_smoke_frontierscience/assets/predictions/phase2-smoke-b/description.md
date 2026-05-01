---
spec_version: "2"
predictions_id: "phase2-smoke-b"
documented_by_task: "t0012_phase2_abc_smoke_frontierscience"
date_documented: "2026-05-01"
---

# Phase 2 smoke condition B predictions

## Metadata

* **Name**: Phase 2 smoke condition B (scope-unaware Plan-and-Solve) on FrontierScience-Olympiad
* **Model**: claude-haiku-4-5 via local Claude Code CLI; agent library
  scope_unaware_planandsolve_v1
* **Datasets**: hierarchical-annotation-v2 (FrontierScience-Olympiad subset, hierarchy-complete
  rows)
* **Format**: jsonl
* **Instances**: 40
* **Created by**: t0012_phase2_abc_smoke_frontierscience

## Overview

These predictions are condition B (scope-unaware Plan-and-Solve) of the Phase 2 A/B/C smoke
harness on FrontierScience-Olympiad. The agent generates a free-form numbered plan, then
executes each step sequentially through a Plan-and-Execute loop. Trajectory records carry the
literal `granularity = "unspecified"` to mark the B condition. Same model, same tool registry, same minimal-system-prompt CLI invocation, and the same set of
40 rows as condition A — the only manipulated factor here is the absence of explicit
granularity conditioning in the agent's prompt template.

## Model

Same `claude-haiku-4-5` model and minimal-system-prompt CLI invocation as condition
A. Agent library is `scope_unaware_planandsolve_v1` (t0007). The Plan-and-Solve prompt does not
elicit a per-step verbalised confidence — this is a documented limitation of the v1 library and
the reason `final_confidence` is `null` for nearly every B row, which collapses the
`overconfident_error_rate` metric for B (see Main Ideas).

## Data

The same 40 FrontierScience-Olympiad hierarchy-complete rows from `hierarchical-annotation-v2`
that condition A processed.

## Prediction Format

JSONL, one row per problem; same schema as `phase2-smoke-a`. The
trajectory `granularity` field is the literal string `"unspecified"` for every turn, marking
condition B. `final_confidence` is `null` for B rows (Plan-and-Solve does not natively emit a
verbalised confidence label) — the harness records this as a known gap and surfaces it as a
follow-up suggestion to extend the t0007 library.

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `task_success_rate` | 0.000 | 0 / 40 |
| `overconfident_error_rate` | 0.000 | Collapsed: no rows surface `final_confidence`, so the
  Xiong2024 aggregator records zero overconfident errors by default. **Not comparable to A.** |
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
  trajectories are not converting into higher accuracy on this benchmark — both stay near zero.

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
