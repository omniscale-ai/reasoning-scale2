# Brainstorm Session 6: Paper-Driven Slate After t0017 Literature Survey

## Objective

Translate t0017's literature findings (hierarchical / granularity-aware agents, LLM-as-judge
methodology) and t0014's schema-vs-model deconfound (+57 pp schema-only, -1 pp model-only) into a
concrete experimental slate that delivers paper-quality results on the project's research questions
as fast as possible.

## Decisions

This session reached agreement on:

* **5 new tasks** (t0019-t0023) covering RQ1, RQ2, RQ4, RQ5, RQ6, RQ7, and RQ9.
* **4 reprioritizations** to reflect t0014/t0017 findings.
* **2 rejections** (out-of-scope or infeasible).
* **Default model standardization**: haiku for annotation/judging unless the hypothesis demands
  sonnet; sonnet for actual agent runs (literature consensus + t0012 floor result).
* **Parallelism**: t0019, t0020, t0021, t0022 launch in parallel worktrees; t0023 starts when t0021
  and t0022 are done.

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
* **S-0003-01** (FrontierMath access): high → medium. SWE-bench is the chosen path; FrontierMath
  doesn't address the floor problem.
* **S-0012-03** (FSO smoke with tools): medium → low. Abandoning FSO route in favour of SWE-bench
  sonnet.
* **S-0014-01** (v3 schema iteration): kept medium, but explicitly conditioned on t0019 substantive
  judge upholding the +57 pp schema-only delta.

## Rejections

* **S-0014-05** (re-run 3 sonnet timeouts): cost-of-recovery exceeds value; t0019 doesn't need those
  rows.
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
2. **Answering RQ7** (semantic scope vs prompt length) with an additional cheap ablation (t0020).
3. **Building the two missing instruments** for the confirmatory experiment in parallel (t0021,
   t0022), so Wave 2 is unblocked the moment Wave 1 finishes.
4. **Running the confirmatory N>=157 experiment** with sonnet on SWE-bench (t0023) to get the
   non-floor A/B/C signal that t0012 could not produce.

The 4-task parallel Wave 1 + library Wave 2 + big experiment Wave 3 structure compresses the
critical path to roughly 1-2 weeks of execution rather than serial-running everything.
