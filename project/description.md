# Granularity-Aware Hierarchical Agents

## Goal

Investigate whether explicitly specifying an agent's current operating granularity — global
planning, subtask planning, or atomic execution — improves action quality, uncertainty calibration,
and final task success in hierarchical problem solving. The project measures the effect of scope
labelling on a composite multi-step benchmark and produces a paper-ready confirm/refute verdict on
the main hypothesis with effect sizes and stratified breakdowns.

## Scope

### In Scope

* Inference-time prompting strategies that condition an LLM agent on an explicit granularity label
  (global / subtask / atomic).
* Three experimental conditions: scope-aware (A), scope-unaware (B), scope-mismatched (C).
* Three evaluation metrics: normalized final task success, overconfident error rate, and
  can-execute-now vs. must-request-information accuracy.
* A composite benchmark drawn from FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, and
  τ-bench, restricted to multi-step tasks of 4-8 decisions per task.
* Manual + LLM-assisted hierarchical annotation of gold actions at three granularity levels.
* Statistical testing across at least 100 tasks per condition with stratification by difficulty and
  granularity.

### Out of Scope

* Non-English benchmarks.
* RL or any gradient-based agent training (inference-time prompting only).
* Production deployment, latency engineering, and cost optimisation of the agent itself.
* Custom benchmark construction beyond the four named sources.

## Research Questions

1. Does explicit granularity conditioning yield higher final task success than an otherwise
   identical scope-unaware agent on the composite benchmark?
2. Does explicit granularity conditioning reduce the overconfident error rate, i.e. the fraction of
   incorrect actions taken with high confidence?
3. On low-level tasks, does granularity conditioning improve accuracy in distinguishing "can execute
   now" from "must request information"?
4. Are gains concentrated in states where local execution requires information not needed for
   higher-level planning (sub-hypothesis 1)?
5. Do scope-mismatched agents perform strictly worse than both scope-aware and scope-unaware
   baselines (sub-hypothesis 2)?

## Success Criteria

* At least 100 tasks fully annotated with gold actions at each of the three granularity levels
  (Phase 1 deliverable).
* Statistically significant difference between scope-aware (A) and scope-unaware (B) on at least two
  of the three metrics at the chosen significance threshold (Phase 2 deliverable).
* Scope-mismatched (C) ranks worst on Metric 1 (task success) and Metric 2 (overconfident error
  rate) relative to A and B (Phase 3 deliverable).
* Clear confirm/refute verdict on the main hypothesis with reported effect sizes and a stratified
  breakdown by task family and difficulty (Phase 4 deliverable).

## Key References

* FrontierScience-Olympiad — composite reasoning benchmark used for top-of-hierarchy strategic
  planning tasks.
* WorkArena++ — web-task benchmark used for mid-level subtask planning.
* SWE-bench Verified — repository-grounded software engineering benchmark used for atomic execution
  cases.
* τ-bench — tool-use benchmark contributing fine-grained execution decisions and request-vs-act
  branching.

## Current Phase

Phase 1 (task decomposition and annotation) is in progress: hierarchical annotation schema is being
finalised and the pilot annotation set is being expanded. Phase 2 (baseline scope-aware vs.
scope-unaware experiment) is queued and depends on completion of Phase 1.

## Pre-Existing Data and Code

The following prior assets were imported from the source `reasoning-scale-` project tree on
2026-04-29:

* `code/scripts/` — experiment runners and analysis scripts including `collect_and_annotate.py`,
  `run_experiment.py`, `run_diploma_experiments.py`, `run_synthesis.py`, and `analyze_results.py`.
  These drive Phase 1 annotation and Phase 2-3 experiment execution.
* `code/src/` — Python package with `runner.py`, `pipeline/`, `benchmarks/`, `models/`, `analysis/`,
  and `storage/` modules backing the scripts. Provides the agent-execution pipeline, benchmark
  adapters, and result storage layer.
* `code/config/` — experiment YAML configurations (`experiment_exp1_instruction.yaml`,
  `experiment_exp2_depth.yaml`, `experiment_exp3_mismatch.yaml`, `experiment_full.yaml`,
  `experiment_mock.yaml`, plus prompt templates under `prompts/`). Define the scope-aware,
  scope-unaware, and scope-mismatched conditions referenced in the research questions.
* `data/annotation_pilot/` — pilot hierarchical annotations of benchmark tasks at three granularity
  levels. Seed material for the Phase 1 ≥100-task target.
* `data/scale_awareness/` — earlier scale-awareness experiment outputs and intermediate artefacts
  used as exploratory baseline material.
* `data/original_roadmap.md` — the source research roadmap that drove this project description.

These assets connect to research questions 1-5: the scripts and pipeline run the A/B/C conditions
and compute Metrics 1-3, the configs realise the scope conditioning variants, and the pilot
annotations bootstrap the gold-action set required by all three metrics.
