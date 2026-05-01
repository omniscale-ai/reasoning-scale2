# ✅ Brainstorm session 6: paper-driven slate after t0017 literature survey

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0018_brainstorm_results_6` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T12:00:00Z |
| **Completed** | 2026-05-01T13:30:00Z |
| **Duration** | 1h 30m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0018_brainstorm_results_6/`](../../../tasks/t0018_brainstorm_results_6/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0018_brainstorm_results_6/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0018_brainstorm_results_6/task_description.md)*

# Brainstorm Session 6: Paper-Driven Slate After t0017 Literature Survey

## Objective

Translate t0017's literature findings (hierarchical / granularity-aware agents, LLM-as-judge
methodology) and t0014's schema-vs-model deconfound (+57 pp schema-only, -1 pp model-only)
into a concrete experimental slate that delivers paper-quality results on the project's
research questions as fast as possible.

## Decisions

This session reached agreement on:

* **5 new tasks** (t0019-t0023) covering RQ1, RQ2, RQ4, RQ5, RQ6, RQ7, and RQ9.
* **4 reprioritizations** to reflect t0014/t0017 findings.
* **2 rejections** (out-of-scope or infeasible).
* **Default model standardization**: haiku for annotation/judging unless the hypothesis
  demands sonnet; sonnet for actual agent runs (literature consensus + t0012 floor result).
* **Parallelism**: t0019, t0020, t0021, t0022 launch in parallel worktrees; t0023 starts when
  t0021 and t0022 are done.

## New Tasks

| ID | Slug | Covers | Cost | Depends |
| --- | --- | --- | --- | --- |
| t0019 | `v2_judge_calibration_sonnet` | S-0014-02, S-0014-03 | ~$5 | none |
| t0020 | `v2_truncation_vs_schema_ablation` | S-0009-04 | ~$2 | none |
| t0021 | `plan_and_solve_v2_with_final_confidence` | S-0012-01 | $0 | none |
| t0022 | `abc_harness_progress_rate_and_error_taxonomy` | S-0017-02 | ~$1 | none |
| t0023 | `phase2_abc_confirmatory_sonnet_swebench` | S-0012-02, S-0010-01 | ~$30 | t0021, t0022 |

Total budget commitment ~$38, leaving ~$13 of the $100 project budget after this round.

## Reprioritizations

* **S-0009-03** (human-review kappa): high → medium. LLM-only stress tests in t0019 run first.
* **S-0003-01** (FrontierMath access): high → medium. SWE-bench is the chosen path;
  FrontierMath doesn't address the floor problem.
* **S-0012-03** (FSO smoke with tools): medium → low. Abandoning FSO route in favour of
  SWE-bench sonnet.
* **S-0014-01** (v3 schema iteration): kept medium, but explicitly conditioned on t0019
  substantive judge upholding the +57 pp schema-only delta.

## Rejections

* **S-0014-05** (re-run 3 sonnet timeouts): cost-of-recovery exceeds value; t0019 doesn't need
  those rows.
* **S-0002-09** (re-fetch papers with LFS): public-fork LFS upload is denied; ghostscript
  compression is the working pattern (see t0017 PR #29).

## RQs Addressed by This Slate

| RQ | Addressed by | Mechanism |
| --- | --- | --- |
| RQ1 | t0023 | A vs B task-success deltas with sonnet on SWE-bench |
| RQ2 | t0022, t0023 | Progress-rate per scope-sensitive state |
| RQ4 | t0021 (prereq) + t0023 | Metric 2 with non-zero `final_confidence` |
| RQ5 | t0023 (C and C-adversarial conditions) | Mismatch-penalty deltas |
| RQ6 | t0022 + t0023 | EAI error taxonomy on global/subtask/atomic alignment |
| RQ7 | t0019 + t0020 | Substantive judge + truncation ablation isolate semantic-scope from anchor and length |
| RQ9 | t0023 | Hard/easy SWE-bench split by hunk count |

RQ3, RQ8, RQ10 are deferred to a future round once the core RQ1/2/5/7 story holds at N>=157.

## Why This Slate, Now

The fastest paper-defensible path requires:

1. **Defending the +57 pp schema-only headline** before claiming it (t0019). Cheap (~$5) and
   decisive.
2. **Answering RQ7** (semantic scope vs prompt length) with an additional cheap ablation
   (t0020).
3. **Building the two missing instruments** for the confirmatory experiment in parallel
   (t0021, t0022), so Wave 2 is unblocked the moment Wave 1 finishes.
4. **Running the confirmatory N>=157 experiment** with sonnet on SWE-bench (t0023) to get the
   non-floor A/B/C signal that t0012 could not produce.

The 4-task parallel Wave 1 + library Wave 2 + big experiment Wave 3 structure compresses the
critical path to roughly 1-2 weeks of execution rather than serial-running everything.

</details>

## Research

* [`research_code.md`](../../../tasks/t0018_brainstorm_results_6/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0018_brainstorm_results_6/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0018_brainstorm_results_6/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0018_brainstorm_results_6/results/results_summary.md)*

# Results Summary: Brainstorm Session 6

## Summary

Translated t0017 literature findings and t0014 deconfound results into a paper-driven
experimental slate. Created 5 new tasks (t0019-t0023) covering RQ1, RQ2, RQ4, RQ5, RQ6, RQ7,
and RQ9; applied 5 correction files (3 reprioritizations + 2 rejections); standardized model
defaults (haiku for annotation/judging, sonnet for agent runs).

## Metrics

* **5 new tasks created**: t0019, t0020, t0021, t0022, t0023.
* **5 corrections applied**: 3 reprioritizations (S-0009-03, S-0003-01, S-0012-03), 2
  rejections (S-0014-05, S-0002-09).
* **7 suggestions covered by new tasks** (linked via `source_suggestion`): S-0014-02,
  S-0014-03, S-0009-04, S-0012-01, S-0017-02, S-0012-02, S-0010-01.
* **Budget commitment for the wave**: ~$38 of $51.31 remaining; targeted leftover after wave:
  ~$13.
* **Suggestions actively uncovered after this round**: 35 (down from 40 before this session;
  -5 covered by new tasks net of 0 new suggestions).

## Verification

* `verify_corrections t0018_brainstorm_results_6`: see PR pre-merge report.
* `verify_logs t0018_brainstorm_results_6`: see PR pre-merge report.
* `verify_task_file` on each new task t0019-t0023: see PR pre-merge report.
* Pre-merge verificator: see PR pre-merge report.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0018_brainstorm_results_6/results/results_detailed.md)*

# Results Detailed: Brainstorm Session 6

## Summary

Brainstorm Session 6 produced a 5-task experimental slate (t0019-t0023) covering 7 of 10
research questions, plus 5 suggestion corrections (3 priority demotions, 2 rejections). Total
budget commitment ~$38, fitting within the remaining $51 project budget.

## Methodology

* Date: 2026-05-01
* Type: planning session, no compute or API spend.
* Inputs: aggregator outputs from `aggregate_tasks`, `aggregate_suggestions`,
  `aggregate_costs`, `aggregate_answers`; results summaries from t0014, t0015, t0017; t0017
  literature synthesis.

## Project State At Session Start

* **17 completed tasks** (t0001-t0017), 0 in-progress, 0 not-started.
* **Budget**: $48.6924 of $100 spent (48.7%); $51.3076 remaining.
* Two prior tasks over per-task limit: t0012 ($18.37), t0014 ($21.16).
* **Active suggestions**: 40 uncovered (10 high-priority, 18 medium, 12 low).
* **Answers**: 0 answer assets in the project.

## Decisions

### New Tasks (5)

| ID | Slug | Covers | Cost | Depends |
| --- | --- | --- | --- | --- |
| t0019 | `v2_judge_calibration_sonnet` | S-0014-02 (primary), S-0014-03 | ~$5 | none |
| t0020 | `v2_truncation_vs_schema_ablation` | S-0009-04 | ~$2 | none |
| t0021 | `plan_and_solve_v2_with_final_confidence` | S-0012-01 | $0 | none |
| t0022 | `abc_harness_progress_rate_and_error_taxonomy` | S-0017-02 | ~$1 | none |
| t0023 | `phase2_abc_confirmatory_sonnet_swebench` | S-0012-02 (primary), S-0010-01 | ~$30 | t0021, t0022 |

### Corrections (5)

| Suggestion | Action | Reason |
| --- | --- | --- |
| S-0009-03 | priority high → medium | Cheap LLM stress tests in t0019 run before $200-300 human kappa pass. |
| S-0003-01 | priority high → medium | SWE-bench is chosen path; FrontierMath access does not fix floor problem. |
| S-0012-03 | priority medium → low | Abandoning FSO route in favour of SWE-bench sonnet. |
| S-0014-05 | status active → rejected | Cost-of-recovery exceeds value; t0019 does not need those rows. |
| S-0002-09 | status active → rejected | Public-fork LFS upload denied; ghostscript compression is the working pattern. |

### Default Model Standardization

* **Annotation/judging**: haiku unless the hypothesis demands sonnet (e.g., t0019 substantive
  judge). t0014 showed sonnet adds nothing as annotator on the v2 schema.
* **Agent runs**: sonnet. Literature consensus + t0012 showed haiku-no-tools is at floor on
  hard benchmarks.

### Parallelism

t0019, t0020, t0021, t0022 launch in parallel worktrees immediately. t0023 starts when t0021
and t0022 are complete.

## RQ Coverage After This Session

| RQ | Status | Addressed by |
| --- | --- | --- |
| RQ1 (granularity → success) | open → addressed | t0023 |
| RQ2 (gains in scope-sensitive states) | open → addressed | t0022 + t0023 |
| RQ3 (info sufficiency) | open | deferred to a future round |
| RQ4 (calibration) | open → addressed | t0021 (prereq) + t0023 |
| RQ5 (mismatch penalty) | open → addressed | t0023 |
| RQ6 (hierarchical consistency) | open → addressed | t0022 + t0023 |
| RQ7 (semantic scope vs prompt length) | open → addressed | t0019 + t0020 |
| RQ8 (agent-inferred granularity) | open | deferred |
| RQ9 (depth, branching, info dependencies) | open → partially addressed | t0023 hard/easy split |
| RQ10 (recovery / replanning) | open | deferred |

7 of 10 RQs receive direct evidence from this slate. RQ3, RQ8, RQ10 deferred to a future
brainstorm once the core RQ1/2/5/7 story holds at N>=157.

## Verification

* All 5 child task files (t0019-t0023) pass `verify_task_file` with 0 errors and 0 warnings.
* All 5 correction files pass `verify_corrections` with 0 errors.
* Brainstorm task structure (4 phases, step logs) follows `human-brainstorm` skill
  conventions.
* `verify_task_results` and `verify_logs` pass on this task folder.
* Task index ordering invariant satisfied: brainstorm task t0018 has lower index than child
  tasks t0019-t0023 (per Phase 3 step 19 of the human-brainstorm skill).

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no compute
  spend, no empirical findings. Decisions are quality-controlled only by reviewer judgement.
* The slate's expected-value reasoning depends on t0017's literature claims (Wang2023,
  Boisvert2024, Xiong2024 effect-size predictions); if those numbers do not transfer, t0023
  may still hit the floor and force a paper-pivot.
* Source-suggestion coverage is single-valued in `task.json`: secondary suggestions covered by
  t0019 (S-0014-03) and t0023 (S-0010-01) are recorded only in the task descriptions.
* RQ3, RQ8, RQ10 remain unaddressed; the next brainstorm after t0023 results land must scope
  them.

## Files Created

* `tasks/t0018_brainstorm_results_6/` — full brainstorm task folder.
* `tasks/t0019_v2_judge_calibration_sonnet/` — task scaffold (status `not_started`).
* `tasks/t0020_v2_truncation_vs_schema_ablation/` — task scaffold.
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/` — task scaffold.
* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/` — task scaffold.
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/` — task scaffold.
* 5 correction files in `tasks/t0018_brainstorm_results_6/corrections/`.

## Next Steps and Suggestions

No new suggestions emitted by this session — all forward motion is encoded in the 5 new task
folders.

After t0019/t0020 results return:

* If t0019 substantive judge sustains the +57 pp schema-only delta: proceed with t0023 and
  write the schema-validity section of the paper.
* If t0019 substantive judge invalidates or reduces the schema-only delta: re-scope t0023 to
  also include the substantive judge as the primary metric, and re-evaluate S-0014-01 (v3
  schema iteration).
* If t0020 shows truncation explains a meaningful fraction of v2's gain: RQ7 conclusion
  shifts; paper claims must be qualified accordingly.

</details>
