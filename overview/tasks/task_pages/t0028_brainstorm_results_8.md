# ✅ Brainstorm 8: close RQ1/RQ4 via discordance-rich resample under $35 cap

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0028_brainstorm_results_8` |
| **Status** | ✅ completed |
| **Started** | 2026-05-03T08:30:00Z |
| **Completed** | 2026-05-03T09:30:00Z |
| **Duration** | 1h 0m |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md), [`t0018_brainstorm_results_6`](../../../overview/tasks/task_pages/t0018_brainstorm_results_6.md), [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md), [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md), [`t0024_brainstorm_results_7`](../../../overview/tasks/task_pages/t0024_brainstorm_results_7.md), [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md), [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0028_brainstorm_results_8/`](../../../tasks/t0028_brainstorm_results_8/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0028_brainstorm_results_8/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0028_brainstorm_results_8/task_description.md)*

# Brainstorm Session 8: Close RQ1/RQ4 with Discordance-Rich Resample

## Context

Following t0024 (brainstorm 7), three substantive tasks ran:

* **t0025** literature survey synthesized RQ1-RQ5 status from 10 papers; flagged that direct
  runtime ABC evidence was missing.
* **t0026** Phase 2 ABC at N=147 produced first runtime data but ran $38.61 (over budget) and
  surfaced fault-tolerance bugs in arm B and a structurally-weak C wrapper.
* **t0027** Phase 2.5 ABC re-ran on N=130 paired instances with a fault-tolerant B and revised
  C. Headline: A=B=6 successes (4.62%), C=7 (5.38%). McNemar 6 vs 6 discordant pairs p=1.0
  (RQ1); 4 vs 5 discordant pairs p=1.0 (RQ5). ECE B=0.336, C=0.374 (still floored by all-100
  confidence).

## RQ Status After t0027

* **RQ1** (granularity → success): underpowered. 12 discordant pairs total; need ≥30 for a
  verdict.
* **RQ2** (overconfident error rate): blocked by template floor; needs content-driven
  calibrator + A confidence emission.
* **RQ3** (execute-now vs request-info): not operationalized; no decision field in agent
  output.
* **RQ4** (info-asymmetric gain concentration): underpowered; analysis-only follow-up on
  TaskA.
* **RQ5** (scope-mismatched strict-worse): counter-direction (C ≥ B) on small N; C wrapper not
  structurally distinct enough.

Remaining budget: **$66.54**.

## Decisions

This session schedules a minimum viable wave to close RQ1 and RQ4.

### New tasks

1. **t0029 TaskA — Discordance-rich paired resample for RQ1**
   * Hard cap: **$35**.
   * Goal: ≥30 discordant pairs across A vs B for a McNemar verdict on RQ1.
   * Abort rule: if the cap is hit before reaching 30 discordant pairs, stop and report a
     partial verdict with a power caveat. Do not launch replacement tasks in this wave.
   * Source suggestion: S-0025-04. Covers: S-0027-05.

2. **t0030 TaskE — RQ4 info-asymmetry stratification analysis**
   * Zero API cost (analysis on TaskA outputs).
   * Goal: stratify TaskA paired sample by subset (swebench / taubench / frontsci) and by
     concordance to test whether granularity gains concentrate where information asymmetry is
     highest.
   * Dependency: t0029.

### Suggestion cleanup

* **Reject as duplicate**: S-0026-02 (duplicate of S-0027-02).
* **Reject as obsolete**: S-0025-01 (pre-Phase-2 sampling proposal superseded by t0029).
* **Demote HIGH → MEDIUM**: S-0027-01 (calibrator), S-0027-02 (C structural rebuild) —
  deferred to next wave but still load-bearing.
* **Demote HIGH → LOW**: S-0020-01, S-0021-02, S-0022-02, S-0022-05 — pre-Phase-2 hypotheses
  superseded by direct runtime evidence in t0026/t0027.
* **Mark covered**: S-0025-04 (t0029 source), S-0027-05 (t0029 covers).

### Tasks not in this wave

TaskB (calibrator), TaskC (C structural rebuild), TaskD (RQ3 instrumentation) were proposed
but deferred. The guardrail explicitly forbids launching them as replacements if t0029 hits
the cap before reaching 30 discordant pairs — preserve the budget for the next session.

## Expected Outputs

* Two new task scaffolds (t0029, t0030) at status `not_started`.
* Eight correction files in `corrections/` reflecting the suggestion cleanup above.
* Updated overview after merge.

No paid external services are used by this brainstorm task itself.

</details>

## Research

* [`research_code.md`](../../../tasks/t0028_brainstorm_results_8/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0028_brainstorm_results_8/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0028_brainstorm_results_8/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0028_brainstorm_results_8/results/results_summary.md)*

# Brainstorm Session 8 — Results Summary

## Summary

Scheduled a minimum viable wave to close RQ1 and RQ4 within the $66.54 remaining budget after
t0027's underpowered McNemar verdicts (12 discordant pairs, p=1.0). Created t0029
(`rq1_discordance_rich_resample`, hard $35 cap, abort on cap with partial verdict) and t0030
(`rq4_info_asymmetry_stratification`, zero-API analysis on t0029 outputs). Eight suggestions
corrected (2 rejected, 6 demoted). No RQ answered in this session.

## Headline Decisions

* Created **t0029** (`rq1_discordance_rich_resample`) with hard $35 cap. Goal: reach >=30
  discordant A vs B pairs for an RQ1 McNemar verdict. Abort rule: if cap is hit before 30
  discordant pairs, halt API calls and report partial RQ1 verdict with explicit power caveat.
  No in-wave replacement task launched on cap. Source suggestion: S-0025-04. Covers:
  S-0027-05.
* Created **t0030** (`rq4_info_asymmetry_stratification`) as zero-API-cost stratification
  analysis on t0029's predictions. Goal: test whether granularity gain rate concentrates in
  high info-asymmetry strata per subset. Dependency: t0029.
* Deferred **TaskB** (RQ2 calibrator), **TaskC** (RQ5 C structural rebuild), **TaskD** (RQ3
  instrumentation) to a later session to preserve budget and respect the cap-on-cap guardrail.
* Wrote 8 correction files: 2 rejections (S-0026-02 duplicate; S-0025-01 obsolete) and 6
  demotions (S-0027-01 HIGH→MEDIUM; S-0027-02 HIGH→MEDIUM; S-0020-01, S-0021-02, S-0022-02,
  S-0022-05 HIGH→LOW).
* Net backlog change: 64 active uncovered → 62 active.

## Methodology

This was a planning session. No metrics were computed, no compute was used, no remote machines
were provisioned. Decisions were derived from:

* Aggregator outputs (`aggregate_tasks`, `aggregate_suggestions`, `aggregate_answers`,
  `aggregate_costs`).
* Results summaries from the three tasks completed since Brainstorm Session 7: t0025, t0026,
  t0027.
* Direct researcher dialogue captured in the step logs.

## Metrics

No quantitative metrics were produced. `results/metrics.json` is `{}` by design.

Cross-task counts captured in this session:

* New tasks created: 2 (t0029, t0030).
* Tasks cancelled: 0.
* Suggestion corrections: 8 (2 rejections; 6 demotions).
* Follow-on suggestions: 0 (preserved for next session per guardrail).
* Compute cost: $0.00. Remote machines used: 0.

## Verification

* `verify_task_file t0028_brainstorm_results_8` — passed.
* `verify_corrections t0028_brainstorm_results_8` — passed (0 errors, 0 warnings).
* `verify_task_file t0029_rq1_discordance_rich_resample` — passed.
* `verify_task_file t0030_rq4_info_asymmetry_stratification` — passed.
* `verify_logs t0028_brainstorm_results_8` — passed.

## Files Created

* `tasks/t0028_brainstorm_results_8/` full brainstorm task folder.
* 8 correction files in `tasks/t0028_brainstorm_results_8/corrections/`.
* `tasks/t0029_rq1_discordance_rich_resample/{task.json,task_description.md}`.
* `tasks/t0030_rq4_info_asymmetry_stratification/{task.json,task_description.md}`.

## Next Steps

* Execute t0029 with the hard $35 cap and abort rule. Expect either a full RQ1 verdict at >=30
  discordant pairs, or a partial verdict with power caveat at the cap.
* Execute t0030 immediately after t0029 finishes (zero API cost).
* Brainstorm session 9 will revisit the deferred suggestions (S-0027-01, S-0027-02, RQ3
  instrumentation) and decide whether the project continues based on the RQ1 / RQ4 verdicts.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0028_brainstorm_results_8/results/results_detailed.md)*

# Brainstorm Session 8 — Detailed Results

## Summary

Brainstorm session 8 chose a minimum viable wave (t0029 + t0030) to close RQ1 and RQ4 within
the $66.54 remaining project budget. Hard $35 cap on t0029 with an abort rule that produces a
partial verdict on cap. Eight suggestion corrections applied (2 rejections, 6 demotions).

## Methodology

Pure planning session. No API calls, no compute, no remote machines. Decisions captured in
step logs 001-004 and applied via correction files plus two child task scaffolds.

## Project State at Session Start

* Total spend: $133.46 / $200. Remaining: $66.54.
* Tasks: 27 (1 cancelled t0023, 26 completed).
* Uncovered suggestions: 64 (9 HIGH, 35 MEDIUM, 20 LOW).
* Answer assets: 2 (none directly answer RQ1-RQ5).
* Tasks completed since Brainstorm Session 7: t0025 (literature survey, $0.20), t0026 (Phase 2
  N=147, $38.61, over original $10 limit), t0027 (Phase 2.5 N=130, $20.76).

## Per-RQ Status After t0027

| RQ | Status | Direct evidence | Blocker | Cost to close |
| --- | --- | --- | --- | --- |
| RQ1 granularity → success | Underpowered | t0027 6 vs 6 disc., p=1.0 | Need >=30 disc. pairs | ~$21-32 |
| RQ2 overconfident error rate | Stuck at 100% confidence | t0027 ECE B=0.336 / C=0.374 | Plan-and-Solve floor; need content-driven calibrator + A patch | ~$10-22 |
| RQ3 execute-now vs request-info | Not operationalised | None | Need decision field in agent output | ~$5-18 |
| RQ4 info-asymmetric gain | Underpowered | t0027 per-subset rates suggestive | Stratification of >=30 disc. sample | ~$3-5 |
| RQ5 scope-mismatched strict-worse | Counter-direction | t0027 C=7 vs B=6 | C wrapper not structurally distinct enough | ~$12-32 |

## Independent Priority Reassessment of HIGH Suggestions

| Suggestion | Original priority | Reassessed | Action |
| --- | --- | --- | --- |
| S-0020-01 | high | low | Demote (HIGH→LOW). Pre-Phase-2 instruction-following hypothesis superseded by t0026/t0027 runtime data. |
| S-0021-02 | high | low | Demote (HIGH→LOW). Plan-and-Solve framing tweaks; floor confirmed content-driven by t0027. |
| S-0022-02 | high | low | Demote (HIGH→LOW). Progress-rate variant; binding constraint is power, not metric design. |
| S-0022-05 | high | low | Demote (HIGH→LOW). Error-taxonomy refinement; t0027 already produced first-order recovery distributions. |
| S-0025-01 | high | rejected | Reject obsolete. Pre-Phase-2 sampling proposal superseded by t0029. |
| S-0025-04 | high | covered | Source suggestion for t0029. |
| S-0026-02 | high | rejected | Reject duplicate of S-0027-02. |
| S-0027-01 | high | medium | Demote. Calibrator deferred to next wave. |
| S-0027-02 | high | medium | Demote. C structural rebuild deferred to next wave. |

Net: 9 HIGH → 0 HIGH (2 covered, 1 rejected duplicate, 1 rejected obsolete, 4 demoted to LOW,
2 demoted to MEDIUM).

## Decision Rationale

The minimum viable wave (t0029 + t0030) was chosen over the full five-RQ closure (TaskA-E,
~$48-104) for these reasons:

1. **Budget headroom for cap overruns**: t0026 already overran its $10 limit by 286%. A $35
   cap on t0029 with $66 remaining preserves $31 of headroom for unexpected overruns plus the
   next session's wave.
2. **RQ1 is the headline question**: a project-wide verdict on the main hypothesis is the
   Phase 4 deliverable in `project/description.md`. RQ1 closure has the highest information
   value per dollar.
3. **TaskE is free**: piggy-backing t0030 on t0029's predictions delivers RQ4 at zero API
   cost.
4. **Cap-on-cap guardrail**: the researcher explicitly forbade in-wave replacement tasks if
   t0029 hits the cap. This preserves budget and the suggestion backlog for an informed next
   session rather than spending blind on RQ2/RQ3/RQ5 before the RQ1 verdict.

## New Tasks

### t0029 RQ1 Discordance-Rich Paired Resample

* Status: `not_started`. Source suggestion: S-0025-04. Covers: S-0027-05.
* Hard $35 cap. Abort rule: if cap hit before 30 discordant pairs, partial verdict + power
  caveat, no in-wave replacements.
* Reuses t0021 Plan-and-Solve v2 (arm A) and t0027 fault-tolerant scope-aware ReAct (arm B).
* Saves predictions assets so t0030 can run with no additional API spend.
* Dependencies: t0010, t0021, t0027.

### t0030 RQ4 Info-Asymmetry Stratification

* Status: `not_started`. Source suggestion: none.
* Zero API cost. Stratifies t0029's paired sample by subset and info-asymmetry tertile.
* Tests whether granularity gain rate (success_rate(B) - success_rate(A)) concentrates in
  high-asymmetry strata via stratified McNemar / CMH with Bonferroni alpha=0.025.
* Dependencies: t0029.

## Suggestion Corrections

| Correction ID | Target | Action | Rationale (short) |
| --- | --- | --- | --- |
| C-0028-01 | S-0026-02 | reject | Duplicate of S-0027-02. |
| C-0028-02 | S-0025-01 | reject | Obsolete; t0029 supersedes. |
| C-0028-03 | S-0027-01 | priority MEDIUM | Calibrator deferred to next wave. |
| C-0028-04 | S-0027-02 | priority MEDIUM | C rebuild deferred to next wave. |
| C-0028-05 | S-0020-01 | priority LOW | Pre-Phase-2 hypothesis superseded. |
| C-0028-06 | S-0021-02 | priority LOW | Floor is content-driven, not template. |
| C-0028-07 | S-0022-02 | priority LOW | Power, not metric design, is binding. |
| C-0028-08 | S-0022-05 | priority LOW | Taxonomy already established. |

## Verification

* `verify_task_file t0028_brainstorm_results_8` — passed.
* `verify_corrections t0028_brainstorm_results_8` — passed (0 errors, 0 warnings).
* `verify_task_file t0029_rq1_discordance_rich_resample` — passed.
* `verify_task_file t0030_rq4_info_asymmetry_stratification` — passed.
* `verify_logs t0028_brainstorm_results_8` — passed.

## Files Created

* `tasks/t0028_brainstorm_results_8/task.json`
* `tasks/t0028_brainstorm_results_8/task_description.md`
* `tasks/t0028_brainstorm_results_8/step_tracker.json`
* `tasks/t0028_brainstorm_results_8/plan/plan.md`
* `tasks/t0028_brainstorm_results_8/research/{research_papers,research_internet,research_code}.md`
* `tasks/t0028_brainstorm_results_8/results/{results_summary,results_detailed}.md`
* `tasks/t0028_brainstorm_results_8/results/{metrics,suggestions,costs,remote_machines_used}.json`
* `tasks/t0028_brainstorm_results_8/logs/steps/00{1,2,3,4}_*/step_log.md`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0020-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0021-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0022-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0022-05.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0025-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0026-02.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0027-01.json`
* `tasks/t0028_brainstorm_results_8/corrections/suggestion_S-0027-02.json`
* `tasks/t0029_rq1_discordance_rich_resample/{task.json,task_description.md}`
* `tasks/t0030_rq4_info_asymmetry_stratification/{task.json,task_description.md}`

## Limitations

* No RQ answered in this session by design.
* If t0029 hits the cap, the wave produces only a partial RQ1 verdict and a partial RQ4
  stratification.
* RQ2, RQ3, RQ5 remain open and depend on a future brainstorm session deciding whether the
  project continues, based on the RQ1 / RQ4 outcomes.

## Next Steps

* Execute t0029 (hard $35 cap, abort on cap).
* Execute t0030 immediately after.
* Run brainstorm session 9 with t0029 / t0030 results in hand.

</details>
