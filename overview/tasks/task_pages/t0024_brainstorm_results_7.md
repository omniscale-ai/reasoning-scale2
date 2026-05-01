# ✅ Brainstorm session 7: rescope around RQ answers after t0019 calibration finding

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0024_brainstorm_results_7` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T18:00:00Z |
| **Completed** | 2026-05-01T19:30:00Z |
| **Duration** | 1h 30m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md), [`t0018_brainstorm_results_6`](../../../overview/tasks/task_pages/t0018_brainstorm_results_6.md), [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md), [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0024_brainstorm_results_7/`](../../../tasks/t0024_brainstorm_results_7/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0024_brainstorm_results_7/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0024_brainstorm_results_7/task_description.md)*

# Brainstorm Session 7: Refresh Literature Before the Next Agent Iteration

## Motivation

Brainstorm Session 6 (t0018) scheduled the headline confirmatory experiment as t0023
(`phase2_abc_confirmatory_sonnet_swebench`, N=157, $40-45 estimated). Two facts moved between
t0018 and now:

1. **t0019 weakened the headline schema effect**. The schema-only accept-rate delta from t0014
   (+58 pp under haiku judge) shrinks to +24.6 pp under a substantive sonnet judge and +37.3
   pp under a model-rotated sonnet judge. Both numbers are below the +45 pp commit threshold
   the task pre-registered. Model-anchoring is the dominant judge-side effect.
2. **Budget**: $26.12 remaining of the $100 project budget. Tasks have run 3-4x estimates
   (t0014 $21.16, t0019 $19.30 against $5 plans). t0023 at $40-45 does not fit even with the
   minimum-viable cuts described in its `task_description.md` Risks & Fallbacks.

The brainstorm-6 slate intentionally separated infrastructure (t0021, t0022) from the headline
agent run. Both libraries are now shipped and verified. Before consuming them with another
expensive sonnet experiment, the researcher chose to refresh the project's literature
understanding of hierarchical / granularity-aware agents and judge methodology, so the next
experiment iteration is designed against the current state of the art rather than the t0002 /
t0017 surveys that predate the t0014, t0019, t0020 findings.

## Decisions

### Direction

The five project research questions in `project/description.md` have **zero confirmed
answers** across 22 completed tasks. The brainstorm-6 plan was to answer 4 of 5 RQs in one
rescoped sonnet experiment. After dialogue, the researcher decided that the cheapest correct
next move is a focused 2024-2026 literature survey covering hierarchical / granularity-aware
LLM agents, search and planning structure, reasoning-structure discovery, agent benchmarks,
and LLM-as-judge methodology, plus the foundational options-framework theory anchor (Sutton,
Precup & Singh 1999). The survey informs the design of the next agent-iteration experiment,
which is deferred to a post-survey brainstorm session.

RQ3 (low-level "can-execute-now" vs "must-request-information") remains deferred — it requires
a different instrumentation (τ-bench-style) regardless of which experiment comes next.

### New Tasks (1)

| ID | Slug | Covers | Cost cap | Depends |
| --- | --- | --- | --- | --- |
| t0025 | `lit_survey_hierarchical_agents_and_judges_2024_2026` | reading list of 10 papers; informs next agent-iteration design | ~$3 | none |

### Cancellations (1)

| ID | Action | Reason |
| --- | --- | --- |
| t0023 | `not_started` → `cancelled` | Original $40-45 estimate exceeds remaining budget. The phase 2 ABC sonnet experiment is deferred to a post-literature-survey brainstorm so the design can incorporate hierarchical-agent and judge-methodology findings from t0025. |

### Corrections (5)

| Suggestion | Action | Reason |
| --- | --- | --- |
| S-0014-03 | active → rejected | Covered by t0019 model-rotated judge run; data merged. |
| S-0019-01 | active → rejected | Confirmatory v3 schema iteration not on critical path within remaining budget. |
| S-0017-01 | active → rejected | Trust-or-Escalate selective-evaluation library setup cost exceeds RQ-level value; the Trust-or-Escalate paper itself is on the t0025 reading list. |
| S-0002-03 | priority high → low | ServiceNow + WorkArena harness out of scope; SWE-bench is the chosen benchmark for the deferred phase 2 experiment. |
| S-0010-01 | priority high → medium | C-adversarial dropped from the immediate slate; partial coverage by C-random remains in the planned phase 2 successor. |

## t0025 Reading List

Ten papers organized by theme. Asset format: standard paper assets in
`tasks/t0025_*/assets/paper/<paper_id>/` per `meta/asset_types/paper/specification.md`.

* **Hierarchical / granularity-aware agents** (4):
  * "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
    Agents" (ICLR 2026)
  * ArCHer: "Training Language Model Agents via Hierarchical Multi-Turn RL" (ICML 2024)
  * "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024)
  * Sutton, Precup & Singh 1999: "Between MDPs and Semi-MDPs" (foundational options framework)
* **Search and planning structure** (2):
  * "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024)
  * LATS: "Language Agent Tree Search" (ICML 2024)
* **Reasoning structure discovery** (1):
  * SELF-DISCOVER (NeurIPS 2024)
* **Agent benchmarks** (2):
  * Embodied Agent Interface (NeurIPS 2024)
  * AgentBoard (NeurIPS 2024 Datasets and Benchmarks)
* **LLM-as-judge methodology** (1):
  * "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"

## Hard Kill Switches for t0025

A literature-survey task does not need experiment-style kill switches, but the cost cap is
enforced:

* **Hard cap**: ~$3 ceiling for the whole survey (PDF downloads are free; cost comes only from
  agent reading and summarization). Halt if the projection at 5 papers in exceeds $5.
* **Stop on paywall block**: if more than 2 of the 10 papers cannot be downloaded after
  exhausting arXiv, Semantic Scholar, OpenAlex, and conference proceedings, halt and produce a
  summary based on abstracts plus a triage note.

## Parallelism

t0025 is the only new task. The 10 paper-add invocations inside t0025 can run in parallel via
sub-agents (each `add-paper` invocation is independent).

## RQ Coverage After This Session

| RQ | Status After t0024 | Addressed by |
| --- | --- | --- |
| RQ1 (granularity → success) | open → still open | future post-survey experiment |
| RQ2 (overconfident error) | open → still open | future post-survey experiment |
| RQ3 (can-execute vs must-request) | open → deferred | future task |
| RQ4 (gains in info-asymmetric states) | open → still open | future post-survey experiment |
| RQ5 (mismatch penalty) | open → still open | future post-survey experiment |

The literature survey itself does not answer any RQ; it informs the design of the experiment
that will. If post-survey brainstorming concludes that no remaining-budget experiment can
credibly answer the RQs, the project pivots to a thesis headlined on the offline annotation +
judge calibration findings (t0014 + t0019 + t0020) plus the literature-survey synthesis.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — full brainstorm task folder.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold (status
  `not_started`).
* 5 correction files in `tasks/t0024_brainstorm_results_7/corrections/`.
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to
  `cancelled`.

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no
  compute, no empirical findings. Decisions are quality-controlled only by reviewer judgement.
* A literature survey does not directly answer any RQ. It is preparatory work for the next
  experiment design, which itself is not yet scheduled.
* The remaining $26 budget after t0025's ~$3 leaves only ~$23 for any post-survey experiment —
  which is below most realistic cost estimates for an above-floor sonnet ABC run with N>=80.
  The post-survey brainstorm may have to choose between a tightly minimal experiment and a
  thesis pivot.
* RQ3 is deferred without a scheduled successor task.

## Next Steps

* Execute t0025 next: download and summarize the 10 papers, then write a synthesis section in
  the results that explicitly maps findings to candidate next-experiment designs.
* After t0025 completes: open Brainstorm Session 8 to scope the next agent-iteration
  experiment given the survey synthesis and the ~$23 remaining budget.

</details>

## Research

* [`research_code.md`](../../../tasks/t0024_brainstorm_results_7/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0024_brainstorm_results_7/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0024_brainstorm_results_7/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0024_brainstorm_results_7/results/results_summary.md)*

# Brainstorm Session 7 — Results Summary

## Summary

Cancelled t0023 ($40-45 estimated, exceeds the $26.12 remaining budget), replaced it with
t0025 — a 10-paper literature survey on hierarchical agents and LLM-as-judge methodology — and
deferred the phase 2 ABC sonnet experiment to a post-survey Brainstorm Session 8. Five
suggestions corrected (three rejected, two demoted). No RQ answered.

## Headline Decisions

* Cancelled t0023 (`phase2_abc_confirmatory_sonnet_swebench`, $40-45 estimated) because its
  cost exceeds the $26.12 remaining project budget.
* Created t0025 (`lit_survey_hierarchical_agents_and_judges_2024_2026`) — a focused 10-paper
  literature survey of 2024-2026 work on hierarchical agents, search and planning structure,
  reasoning-structure discovery, agent benchmarks, and LLM-as-judge methodology, plus the
  foundational Sutton-Precup-Singh 1999 options-framework paper. Cost cap ~$3.
* Wrote 5 correction files: 3 suggestion rejections (S-0014-03, S-0019-01, S-0017-01) and 2
  priority demotions (S-0002-03 → low; S-0010-01 → medium).
* Deferred RQ3 (can-execute-now vs must-request-information) to a future task — different
  instrumentation requirements regardless of the next experiment.
* Deferred the phase 2 ABC sonnet experiment to a post-survey Brainstorm Session 8 so the
  design can incorporate hierarchical-agent and judge-methodology findings from t0025.

## Methodology

This was a planning session. No metrics were computed, no compute was used, no remote machines
were provisioned. The decisions were derived from:

* Aggregator outputs (`aggregate_tasks`, `aggregate_suggestions`, `aggregate_answers`,
  `aggregate_costs`).
* The four results summaries produced since Brainstorm Session 6: t0019, t0020, t0021, t0022.
* Direct researcher dialogue, captured in the step logs.

## Metrics

No quantitative metrics were produced. This is a planning task; `results/metrics.json` is `{}`
by design. Cross-task counts captured in this session:

* Tasks cancelled: 1 (t0023).
* New tasks created: 1 (t0025).
* Suggestion corrections: 5 (3 rejections — S-0014-03, S-0019-01, S-0017-01; 2 priority
  demotions — S-0002-03 → low, S-0010-01 → medium).
* Follow-on suggestions: 0.
* Compute cost: $0.00. Remote machines used: 0.

## Verification

* `verify_task_file t0024_brainstorm_results_7` — passed (1 expected `TF-W005` warning for
  empty `expected_assets`).
* `verify_task_results t0024_brainstorm_results_7` — passed after this section was added.
* `verify_logs t0024_brainstorm_results_7` — passed (3 acceptable warnings: no command logs,
  no session capture, no capture report; expected for a planning-only task).
* `verify_corrections t0024_brainstorm_results_7` — passed (5 correction files, 0 errors, 0
  warnings).
* `verify_task_file t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` — passed (0
  errors, 0 warnings).

## RQ Coverage After This Session

| RQ | Status | Addressed by |
| --- | --- | --- |
| RQ1 (granularity → success) | open | future post-survey experiment |
| RQ2 (overconfident error) | open | future post-survey experiment |
| RQ3 (can-execute vs must-request) | deferred | future task |
| RQ4 (gains in info-asymmetric states) | open | future post-survey experiment |
| RQ5 (mismatch penalty) | open | future post-survey experiment |

The literature survey itself does not answer any RQ; it informs the design of the experiment
that will. If post-survey brainstorming concludes that no remaining-budget experiment can
credibly answer the RQs, the project pivots to a thesis headlined on the offline annotation +
judge calibration findings (t0014 + t0019 + t0020) plus the literature-survey synthesis.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — full brainstorm task folder.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold (status
  `not_started`).
* 5 correction files in `tasks/t0024_brainstorm_results_7/corrections/`.
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to
  `cancelled`.

## Next Steps

* Execute t0025 next: download and summarize the 10 papers, then write a synthesis section
  that explicitly maps findings to candidate next-experiment designs.
* After t0025 completes: open Brainstorm Session 8 to scope the next agent-iteration
  experiment given the survey synthesis and the ~$23 remaining budget.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0024_brainstorm_results_7/results/results_detailed.md)*

# Brainstorm Session 7 — Detailed Results

## Summary

Brainstorm Session 7 cancelled t0023 (phase 2 ABC confirmatory sonnet experiment) because its
$40-45 cost estimate exceeds the $26.12 remaining project budget after t0019's weakened
headline, and replaced it with t0025 — a focused 10-paper literature survey of 2024-2026
hierarchical-agent and LLM-as-judge work, plus the 1999 options-framework paper as a theory
anchor. The phase 2 ABC sonnet experiment is deferred to a post-survey Brainstorm Session 8 so
the design can incorporate hierarchical-agent and judge-methodology findings. No RQ was
answered; all five remain open or deferred.

## Methodology

This was a planning session — no compute, no remote machines, no metric runs. Inputs and
procedure:

* Aggregated project state via `aggregate_tasks`, `aggregate_suggestions --uncovered`,
  `aggregate_answers`, `aggregate_costs` (all with `--format json`).
* Read the four results summaries produced since Brainstorm Session 6 (t0019, t0020, t0021,
  t0022) and the t0019 model-rotated judge finding in detail.
* Independently reassessed every active high-priority suggestion against current task results
  before presenting to the researcher.
* Iterated through three candidate paths (rescope-and-answer-RQ, thesis-pivot,
  literature-refresh-first) with the researcher, who pivoted mid-session to the
  literature-refresh path and provided the 10-paper reading list.
* Applied the agreed slate by editing `tasks/t0023_*/task.json` to `cancelled`, writing 5
  correction files in `tasks/t0024_brainstorm_results_7/corrections/`, and creating the t0025
  task scaffold via the `/create-task` skill.

## Context

Brainstorm Session 6 (t0018) had scheduled t0023 (`phase2_abc_confirmatory_sonnet_swebench`,
N>=157, $40-45 estimated) as the headline confirmatory ABC experiment. Two facts moved between
t0018 and the start of this session:

1. **t0019 weakened the headline schema effect**. The schema-only accept-rate delta from t0014
   (+58 pp under haiku judge) shrinks to **+24.6 pp** under a substantive sonnet judge and
   **+37.3 pp** under a model-rotated sonnet judge. Both numbers are below the +45 pp commit
   threshold the task pre-registered. Model-anchoring is the dominant judge-side effect.
2. **Budget**: $26.12 remaining of the $100 project budget after t0019 ($19.30) and t0014
   ($21.16) cost overruns. t0023 at $40-45 does not fit even with the minimum-viable cuts.

## Project State Going In

| Aspect | Status |
| --- | --- |
| Completed tasks | 22 |
| In progress / not-started | t0023 only |
| RQs answered | 0 of 5 |
| Suggestions: high-priority active | several across t0010, t0014, t0017, t0019 |
| Budget remaining | $26.12 |
| Latest libraries shipped | t0021 (plan-and-solve v2), t0022 (ABC harness + progress rate + error taxonomy) |

## Discussion Summary

The session opened with the researcher reviewing the project state and noting that no RQ has a
confirmed answer despite 22 tasks. Three candidate paths were surfaced:

* **Path A — rescope-and-answer-RQ**: trim t0023 to N=80, drop C-adversarial, drop sonnet
  judge spot-check, hard-cap at $25. Estimated to fit in budget but with no margin and
  per-task overruns of 3-4x as the historical norm.
* **Path B — thesis-pivot**: stop new experiment work and write the thesis around the offline
  annotation findings (t0014 + t0019 + t0020). Defensible body of work but leaves all 5 RQs
  unanswered.
* **Path C — literature-refresh-first**: spend ~$3 on a focused 2024-2026 literature survey
  before committing the bulk of the remaining budget to another sonnet experiment, so the
  next-experiment design is informed by current state-of-the-art on hierarchical agents and
  LLM-as-judge methodology.

After dialogue, the researcher chose Path C and provided a 10-paper reading list. The
reasoning was that the existing project surveys (t0002, t0017) predate the t0014, t0019, t0020
findings and may have under-weighted hierarchical-RL, options-framework, and judge-anchoring
literature that bears directly on what the next experiment should look like.

The phase 2 ABC sonnet experiment (formerly t0023, considered as t0025 in earlier session
drafts) is deferred to a post-survey Brainstorm Session 8.

## Decisions Applied in Step 3

### Cancellation

* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — `status: not_started` →
  `status: cancelled`. No other fields changed.

### New task

| ID | Slug | Type | Cost cap | Expected assets |
| --- | --- | --- | --- | --- |
| t0025 | `lit_survey_hierarchical_agents_and_judges_2024_2026` | `literature-survey` | ~$3 | `paper: 10` |

### Suggestion corrections (5)

| Suggestion | Action | Rationale |
| --- | --- | --- |
| S-0014-03 | reject | Covered by t0019 model-rotated judge run; data merged. |
| S-0019-01 | reject | Confirmatory v3 schema iteration not on critical path within remaining budget. |
| S-0017-01 | reject | Trust-or-Escalate library setup cost exceeds RQ-level value; the paper is on the t0025 reading list. |
| S-0002-03 | demote (high → low) | ServiceNow + WorkArena out of scope; SWE-bench is the chosen benchmark for the deferred phase 2. |
| S-0010-01 | demote (high → medium) | C-adversarial dropped from immediate slate; partial coverage by C-random remains in the planned phase 2 successor. |

## t0025 Reading List

* Hierarchical / granularity-aware agents (4):
  * "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
    Agents" (ICLR 2026)
  * ArCHer: "Training Language Model Agents via Hierarchical Multi-Turn RL" (ICML 2024)
  * "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024)
  * Sutton, Precup & Singh 1999: "Between MDPs and Semi-MDPs" (foundational options framework)
* Search and planning structure (2):
  * "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024)
  * LATS: "Language Agent Tree Search" (ICML 2024)
* Reasoning structure discovery (1):
  * SELF-DISCOVER (NeurIPS 2024)
* Agent benchmarks (2):
  * Embodied Agent Interface (NeurIPS 2024)
  * AgentBoard (NeurIPS 2024 Datasets and Benchmarks)
* LLM-as-judge methodology (1):
  * "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no
  compute, no empirical findings. Decisions are quality-controlled only by reviewer judgement.
* The remaining $26 budget after t0025's ~$3 leaves only ~$23 for any post-survey experiment —
  below most realistic cost estimates for an above-floor sonnet ABC run with N>=80. The
  post-survey brainstorm may have to choose between a tightly minimal experiment and a thesis
  pivot.
* RQ3 is deferred without a scheduled successor task.

## Verification

* `verify_task_file t0024_brainstorm_results_7` — pass (expected).
* `verify_task_file t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` — pass.
* `verify_task_results t0024_brainstorm_results_7` — to be run during finalize step.
* `verify_logs t0024_brainstorm_results_7` — to be run during finalize step.
* `verify_corrections t0024_brainstorm_results_7` — to be run during finalize step.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — brainstorm task folder with `task.json`,
  `task_description.md`, `step_tracker.json`, plan, research placeholders, results files, step
  logs, and 5 correction files.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold
  (`task.json`, `task_description.md`, status `not_started`).
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to
  `cancelled`.

## Next Steps / Suggestions

This brainstorm produces no follow-on suggestions of its own — the immediate next executable
task is t0025, and the post-survey Brainstorm Session 8 will produce the next round of
suggestions and tasks. Any suggestions written in `results/suggestions.json` would prejudge
that session.

</details>
