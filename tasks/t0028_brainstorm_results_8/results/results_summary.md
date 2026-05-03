# Brainstorm Session 8 — Results Summary

## Summary

Scheduled a minimum viable wave to close RQ1 and RQ4 within the $66.54 remaining budget after
t0027's underpowered McNemar verdicts (12 discordant pairs, p=1.0). Created t0029
(`rq1_discordance_rich_resample`, hard $35 cap, abort on cap with partial verdict) and t0030
(`rq4_info_asymmetry_stratification`, zero-API analysis on t0029 outputs). Eight suggestions
corrected (2 rejected, 6 demoted). No RQ answered in this session.

## Headline Decisions

* Created **t0029** (`rq1_discordance_rich_resample`) with hard $35 cap. Goal: reach >=30 discordant
  A vs B pairs for an RQ1 McNemar verdict. Abort rule: if cap is hit before 30 discordant pairs,
  halt API calls and report partial RQ1 verdict with explicit power caveat. No in-wave replacement
  task launched on cap. Source suggestion: S-0025-04. Covers: S-0027-05.
* Created **t0030** (`rq4_info_asymmetry_stratification`) as zero-API-cost stratification analysis
  on t0029's predictions. Goal: test whether granularity gain rate concentrates in high
  info-asymmetry strata per subset. Dependency: t0029.
* Deferred **TaskB** (RQ2 calibrator), **TaskC** (RQ5 C structural rebuild), **TaskD** (RQ3
  instrumentation) to a later session to preserve budget and respect the cap-on-cap guardrail.
* Wrote 8 correction files: 2 rejections (S-0026-02 duplicate; S-0025-01 obsolete) and 6 demotions
  (S-0027-01 HIGH→MEDIUM; S-0027-02 HIGH→MEDIUM; S-0020-01, S-0021-02, S-0022-02, S-0022-05
  HIGH→LOW).
* Net backlog change: 64 active uncovered → 62 active.

## Methodology

This was a planning session. No metrics were computed, no compute was used, no remote machines were
provisioned. Decisions were derived from:

* Aggregator outputs (`aggregate_tasks`, `aggregate_suggestions`, `aggregate_answers`,
  `aggregate_costs`).
* Results summaries from the three tasks completed since Brainstorm Session 7: t0025, t0026, t0027.
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
