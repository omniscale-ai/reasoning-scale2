# Results Detailed: Brainstorm Session 6

## Methodology

* Date: 2026-05-01
* Type: planning session, no compute or API spend.
* Inputs: aggregator outputs from `aggregate_tasks`, `aggregate_suggestions`, `aggregate_costs`,
  `aggregate_answers`; results summaries from t0014, t0015, t0017; t0017 literature synthesis.

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
* **Agent runs**: sonnet. Literature consensus + t0012 showed haiku-no-tools is at floor on hard
  benchmarks.

### Parallelism

t0019, t0020, t0021, t0022 launch in parallel worktrees immediately. t0023 starts when t0021 and
t0022 are complete.

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

7 of 10 RQs receive direct evidence from this slate. RQ3, RQ8, RQ10 deferred to a future brainstorm
once the core RQ1/2/5/7 story holds at N>=157.

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

* If t0019 substantive judge sustains the +57 pp schema-only delta: proceed with t0023 and write the
  schema-validity section of the paper.
* If t0019 substantive judge invalidates or reduces the schema-only delta: re-scope t0023 to also
  include the substantive judge as the primary metric, and re-evaluate S-0014-01 (v3 schema
  iteration).
* If t0020 shows truncation explains a meaningful fraction of v2's gain: RQ7 conclusion shifts;
  paper claims must be qualified accordingly.
