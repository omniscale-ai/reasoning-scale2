# ✅ Brainstorm session 4: v2 schema-vs-model confound and proxy-benchmark labels

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0013_brainstorm_results_4` |
| **Status** | ✅ completed |
| **Started** | 2026-04-30T18:00:00Z |
| **Completed** | 2026-04-30T18:00:00Z |
| **Duration** | 0s |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Task types** | `brainstorming` |
| **Step progress** | 4/4 |
| **Task folder** | [`t0013_brainstorm_results_4/`](../../../tasks/t0013_brainstorm_results_4/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0013_brainstorm_results_4/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0013_brainstorm_results_4/task_description.md)*

# Brainstorm Session 4

## Context

Three of the four wave 3 tasks completed: t0009 (v2 tree-schema annotation), t0010 (matched-
mismatch library), t0011 (Metric 2 calibration aggregator). t0012 (Phase 2 A/B/C smoke on
FrontierScience) is `in_progress`. Total spend stands at roughly $9.16 of the $100 project
budget.

Two issues surfaced in t0009 that the headline experiment cannot rest on cleanly:

1. **Schema-vs-model confound.** t0009 reports a +58 pp judge-acceptance delta over v1, but
   the annotation provider was swapped from Claude Sonnet (v1) to Claude Haiku (v2) midway.
   The +58 pp number conflates the tree-schema upgrade with the model swap. Without a Sonnet
   rerun on the v2 schema, we cannot say whether the schema actually moved acceptance — and
   the "v2 unblocks Phase 2" story has a load-bearing dependency on that being a real schema
   effect.
2. **Proxy-benchmark provenance.** The v2 dataset labels two of its four benchmarks
   "WorkArena++" and "tau-bench". The underlying rows are actually Mind2Web and HumanEval rows
   used as proxies. Downstream consumers (and the t0012 in-flight smoke) read the labels at
   face value, which would misrepresent results once the headline numbers are reported.

Suggestion backlog also accumulated: 17 high-priority suggestions across S-0001-* through
S-0011-*, several with overlap and a few that the t0012 in-flight task already covers.

## Decisions

Two new tasks created, both `not_started`, parallel-safe, no dependencies on each other:

* `t0014_v2_annotator_sonnet_rerun` (covers `S-0009-01`) — re-run the v2 annotator on the same
  115 rows using `claude-sonnet-4-6`, judge with the same haiku judge on the same stratified
  sample. Compare per-benchmark accept rate against v2-haiku to isolate the schema component
  of the +58 pp delta. Budget: ~$5.
* `t0015_correct_proxy_benchmark_labels` (covers `S-0009-06` variant b) — write a correction
  file against the t0009 dataset asset that renames the `WorkArena++` benchmark label to
  `Mind2Web` and the `tau-bench` benchmark label to `HumanEval`, with a one-paragraph
  rationale. No new annotation, no API spend. Budget: $0.

Wave budget cap: **$10** combined for both tasks (t0014 ~$5; t0015 ~$0; ~$5 of headroom).

Parallelism: t0014 and t0015 launch in parallel. t0012 stays in_progress and is not modified
by this session — its FrontierScience filter is unaffected by the proxy-benchmark relabel.

## Suggestion cleanup

Five rejections (duplicates or already covered by an in-flight task):

* `S-0002-04` — duplicate of `S-0003-01` (FrontierMath access negotiation).
* `S-0003-02` — duplicate of `S-0002-03` (ServiceNow lab provisioning).
* `S-0005-06` — covered by t0012 (Phase 2 A/B/C smoke FrontierScience scope).
* `S-0007-02` — covered by t0012 (matched-mismatch C condition is exercised inside t0012).
* `S-0005-01` — superseded by `S-0009-03` + `S-0009-05` (the v2 follow-ups are now the
  canonical scaling and human-review track, not the v1-era "row-count expansion" framing).

Three reprioritizations (high → medium):

* `S-0002-01` — pass^k metric (replication infrastructure; not on the headline path until
  after the smoke).
* `S-0002-05` — SWE-bench Docker harness (compute infrastructure; not on the headline path).
* `S-0006-01` — tool registries (registry instrumentation; not on the headline path).

Two follow-ups intentionally **not** corrected:

* `S-0010-01` — kept active as a Phase-2 follow-up to land after t0012's first headline
  result.
* `S-0009-01` — covered by `t0014`, so it stays active and the new task references it through
  `source_suggestion`.

## Out of scope this session

* Multi-provider replication of t0012 (Gemini, OpenAI). Deferred until t0012 produces a
  single- provider headline result.
* v2 row-count expansion beyond 115 rows. Tracked under `S-0009-03`/`S-0009-05`.
* Human review pass over v2 annotations.
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.
* Any change to t0012 itself (in_progress; immutable for this session).

</details>

## Research

* [`research_code.md`](../../../tasks/t0013_brainstorm_results_4/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0013_brainstorm_results_4/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0013_brainstorm_results_4/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0013_brainstorm_results_4/results/results_summary.md)*

# Brainstorm Session 4 — Results Summary

## Summary

Fourth brainstorm produced two new not-started tasks (t0014 and t0015) and applied eight
correction files for the Round 2 cleanup deferred from brainstorm 3. The two tasks address the
schema-vs-model confound and proxy-benchmark provenance issues surfaced by t0009. Wave budget
cap: $10. Both new tasks are parallel-safe; t0012 stays in_progress and unaffected.

## Session Overview

* **Date**: 2026-04-30
* **Context**: Triggered after t0009-t0011 merged with $9.16 / $100 spent. t0012 is
  in_progress. t0009 reported a +58 pp v2-vs-v1 judge accept rate but the annotation provider
  was swapped from Sonnet (v1) to Haiku (v2), so the headline delta is confounded with the
  model swap. The v2 dataset also labels two proxy benchmarks under their proxy targets' names
  instead of the true source corpora.
* **Prompt**: Resolve both pre-Phase-2 issues so t0012's headline experiment can rest on a
  clean v2 foundation, and prune the 17-suggestion high-priority backlog.

## Decisions

1. **Create `t0014_v2_annotator_sonnet_rerun`** (covers `S-0009-01`). Re-run the v2 annotator
   on the same 115 rows with `claude-sonnet-4-6`; judge with the same haiku judge on the same
   stratified sample. Compare per-benchmark accept rate against v2-haiku. Budget ~$5. No deps.
2. **Create `t0015_correct_proxy_benchmark_labels`** (covers `S-0009-06` variant b). Write a
   correction file against the t0009 dataset asset that renames `WorkArena++` to `Mind2Web`
   and `tau-bench` to `HumanEval` with a one-paragraph rationale. No API spend. No deps.
3. **Reject 5 suggestions** as duplicates or already-covered:
   * `S-0002-04` ↔ `S-0003-01` duplicate (FrontierMath access).
   * `S-0003-02` ↔ `S-0002-03` duplicate (ServiceNow lab provisioning).
   * `S-0005-06` covered by t0012 (Phase 2 A/B/C smoke FrontierScience).
   * `S-0007-02` covered by t0012 (matched-mismatch C condition).
   * `S-0005-01` superseded by `S-0009-03` + `S-0009-05` (v2 follow-ups now own the scaling
     track).
4. **Reprioritize 3 suggestions** from high to medium (off the headline path):
   * `S-0002-01` (pass^k metric).
   * `S-0002-05` (SWE-bench Docker harness).
   * `S-0006-01` (tool registries).
5. **Keep `S-0010-01`** active as a Phase-2 follow-up to land after t0012's first headline
   result.
6. **Defer multi-provider replication** (Gemini + OpenAI) until t0012 produces a
   single-provider headline.
7. **Wave budget cap**: $10. Parallelism: t0014 and t0015 launch in parallel. t0012 stays
   in_progress and is not modified.

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 2 |
| Suggestions covered by new tasks | 2 |
| Suggestions rejected | 5 |
| Suggestions reprioritized | 3 |
| Corrections written | 8 |
| Answer assets produced | 0 |

## Verification

* `verify_task_file` — t0013, t0014, t0015 PASSED.
* `verify_corrections` — t0013 PASSED (8 correction files).
* `verify_suggestions` — t0013 PASSED (no new suggestions).
* `verify_logs` — t0013 PASSED (LG-W001/W005/W007/W008 acceptable for a planning task).

## Next Steps

After this PR merges, fork two parallel `/execute-task` background agents for `t0014` and
`t0015`. `t0012` continues independently. Plan brainstorm 5 once t0012 lands plus at least one
of t0014 / t0015 — to address multi-provider replication, v2 row-count expansion, and any v3
schema iteration the deconfound result motivates.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0013_brainstorm_results_4/results/results_detailed.md)*

# Brainstorm Session 4 — Detailed Results

## Summary

Two new not-started tasks created (t0014, t0015). Eight correction files written: five
suggestion rejections, three suggestion reprioritizations. t0012 stays in_progress and is not
modified by this session.

## Methodology

1. Aggregated tasks, suggestions, answers, and costs through the standard four-aggregator
   triplet. 11 completed tasks, 1 in_progress (t0012), 17 high-priority uncovered suggestions,
   $9.16 / $100 spent.
2. Read `results_summary.md` for t0009, t0010, t0011 to ground reassessed priorities.
3. Identified the schema-vs-model confound in t0009 (Sonnet→Haiku provider swap conflated with
   the v1→v2 schema upgrade in the +58 pp delta) and the proxy-benchmark label drift
   (`WorkArena++` labels Mind2Web rows; `tau-bench` labels HumanEval rows).
4. Round 1: proposed two parallel pre-Phase-2 tasks (Sonnet rerun, proxy benchmark relabel
   correction). Researcher confirmed with budget cap $10 and "запускаем параллельно но t0012
   позже".
5. Round 2: proposed 5 rejections + 3 reprioritizations. Researcher delegated decision
   authority ("отклоняй чо хочешь").
6. Round 3: confirmation. Researcher: "go".
7. Created the brainstorm task folder and two child task folders.
8. Wrote eight correction files in `corrections/`.
9. Ran verificators, materialized overview, formatted markdown via flowmark.

## Confound and Proxy-Benchmark Issues

### Schema-vs-model confound (t0014 motivation)

t0009 reports a v2-vs-v1 judge accept rate delta of approximately +58 pp on the stratified
sample. However, the v1 annotator was `claude-sonnet-4-6` while the v2 annotator was switched
to `claude-haiku-4-5-20251001` mid-task to fit the cost budget. The judge model was constant
(`claude-haiku-4-5-20251001`). Two effects therefore overlap:

* schema effect: tree decomposition with subtask-to-atomic edges and full problem text;
* model effect: switching annotator from Sonnet to Haiku (potentially in the *opposite*
  direction).

t0014 disentangles the two by re-running the v2 annotator with Sonnet and judging with the
same haiku judge on the same stratified sample. The accept-rate delta against v2-haiku
isolates the annotator-model component; the residual against v1-sonnet isolates the schema
component.

### Proxy-benchmark provenance (t0015 motivation)

t0009's `details.json` lists four benchmarks: `FrontierScience-Olympiad`, `SWE-bench
Verified`, `WorkArena++`, `tau-bench`. The first two are accurate. The latter two are
mislabelled — the rows under those labels are `Mind2Web` and `HumanEval` rows used as proxies.
Once the t0012 smoke result is reported, the per-benchmark numbers would otherwise be
attributed to benchmarks the project does not actually evaluate on. t0015 fixes the labels via
a `correction` file (no re-annotation, no API spend) so downstream consumers and reports see
the corrected source corpora.

## Decisions

| Decision | Action | Source |
| --- | --- | --- |
| Create `t0014_v2_annotator_sonnet_rerun` | new task, no deps, ~$5 | covers `S-0009-01` |
| Create `t0015_correct_proxy_benchmark_labels` | new task, no deps, $0 | covers `S-0009-06` (b) |
| Reject `S-0002-04` | correction `update`, status → rejected | duplicate of `S-0003-01` |
| Reject `S-0003-02` | correction `update`, status → rejected | duplicate of `S-0002-03` |
| Reject `S-0005-06` | correction `update`, status → rejected | covered by t0012 |
| Reject `S-0007-02` | correction `update`, status → rejected | covered by t0012 |
| Reject `S-0005-01` | correction `update`, status → rejected | superseded by S-0009-03 + S-0009-05 |
| Demote `S-0002-01` | correction `update`, priority → medium | pass^k off headline path |
| Demote `S-0002-05` | correction `update`, priority → medium | SWE-bench harness off path |
| Demote `S-0006-01` | correction `update`, priority → medium | tool registries off path |

Verified counts cross-checked against the on-disk correction-file table: rejections = 5
(verified), reprioritizations = 3 (verified), new tasks = 2 (verified), corrections = 8
(verified).

## Metrics

| Item | Count |
| --- | --- |
| New tasks created | 2 |
| Suggestions covered by new tasks | 2 |
| Suggestions rejected | 5 |
| Suggestions reprioritized | 3 |
| Corrections written | 8 |
| Answer assets produced | 0 |

## Limitations

Planning task; no experiments run. Multi-provider replication and v2 row-count expansion
remain on the backlog. The schema component of the v2 delta is asserted only after t0014
lands; until then, the +58 pp number stays publicly attributable to the schema.

## Files Created

* `tasks/t0013_brainstorm_results_4/` — full brainstorm-results task folder.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0002-01.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0002-04.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0002-05.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0003-02.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0005-01.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0005-06.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0006-01.json`.
* `tasks/t0013_brainstorm_results_4/corrections/suggestion_S-0007-02.json`.
* `tasks/t0014_v2_annotator_sonnet_rerun/{task.json, task_description.md}`.
* `tasks/t0015_correct_proxy_benchmark_labels/{task.json, task_description.md}`.

## Verification

* `verify_task_file` — t0013, t0014, t0015: PASSED.
* `verify_corrections` — t0013: PASSED (8 correction files).
* `verify_suggestions` — t0013: PASSED.
* `verify_logs` — t0013: PASSED.

</details>
