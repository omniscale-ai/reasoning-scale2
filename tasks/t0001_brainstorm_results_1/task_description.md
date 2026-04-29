# Brainstorm Session 1

## Context

This is the first brainstorm session for the granularity-aware hierarchical agents project, executed
inline as part of `/setup-project` immediately after `meta/` was populated. The project has no
completed tasks, no suggestions, and no answer assets, so the session focused on Round 1 (propose
first tasks). Rounds 2 (suggestion cleanup) and 3 (confirmation) had nothing to clean up and
proceeded straight to confirmation.

## Decisions

The researcher accepted two child tasks for immediate creation:

* `t0002_literature_survey_granularity_conditioning` — survey papers on granularity / scope / scale
  conditioning in LLM agents, hierarchical task decomposition, and uncertainty calibration metrics.
* `t0003_download_benchmark_subsets` — wire up access to subsets of the four roadmap benchmarks
  (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench) at difficulty 4-8 decisions
  per task.

Two further candidate tasks (`hierarchical_annotation_pilot` and
`baseline_scope_experiment_smoke_test`) were discussed in detail but deferred — the researcher will
review T1 and T2 outputs before committing.

## Why these tasks first

T1 and T2 are independent and low-cost. T1 anchors later planning decisions in the literature; T2
unblocks every Phase 1 annotation extension and every Phase 2/3 experiment. Running them in parallel
keeps the project moving while preserving the option to redirect after the literature survey.

## Out-of-band notes

* `project/data/annotation_pilot/tasks_annotated.jsonl` already contains 115 LLM-annotated rows, but
  tau-bench and WorkArena++ rows use HumanEval and Mind2Web proxies because the real benchmarks were
  "unavailable on HF" at original-annotation time. T2 must address this directly.
* The `available_services` list dropped `openai_api` during setup because no API key was provided;
  `anthropic_api` remains. T1 and T2 should plan their LLM use accordingly.
