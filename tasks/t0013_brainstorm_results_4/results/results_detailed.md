# Brainstorm Session 4 — Detailed Results

## Summary

Two new not-started tasks created (t0014, t0015). Eight correction files written: five suggestion
rejections, three suggestion reprioritizations. t0012 stays in_progress and is not modified by this
session.

## Methodology

1. Aggregated tasks, suggestions, answers, and costs through the standard four-aggregator triplet.
   11 completed tasks, 1 in_progress (t0012), 17 high-priority uncovered suggestions, $9.16 / $100
   spent.
2. Read `results_summary.md` for t0009, t0010, t0011 to ground reassessed priorities.
3. Identified the schema-vs-model confound in t0009 (Sonnet→Haiku provider swap conflated with the
   v1→v2 schema upgrade in the +58 pp delta) and the proxy-benchmark label drift (`WorkArena++`
   labels Mind2Web rows; `tau-bench` labels HumanEval rows).
4. Round 1: proposed two parallel pre-Phase-2 tasks (Sonnet rerun, proxy benchmark relabel
   correction). Researcher confirmed with budget cap $10 and "запускаем параллельно но t0012 позже".
5. Round 2: proposed 5 rejections + 3 reprioritizations. Researcher delegated decision authority
   ("отклоняй чо хочешь").
6. Round 3: confirmation. Researcher: "go".
7. Created the brainstorm task folder and two child task folders.
8. Wrote eight correction files in `corrections/`.
9. Ran verificators, materialized overview, formatted markdown via flowmark.

## Confound and Proxy-Benchmark Issues

### Schema-vs-model confound (t0014 motivation)

t0009 reports a v2-vs-v1 judge accept rate delta of approximately +58 pp on the stratified sample.
However, the v1 annotator was `claude-sonnet-4-6` while the v2 annotator was switched to
`claude-haiku-4-5-20251001` mid-task to fit the cost budget. The judge model was constant
(`claude-haiku-4-5-20251001`). Two effects therefore overlap:

* schema effect: tree decomposition with subtask-to-atomic edges and full problem text;
* model effect: switching annotator from Sonnet to Haiku (potentially in the *opposite* direction).

t0014 disentangles the two by re-running the v2 annotator with Sonnet and judging with the same
haiku judge on the same stratified sample. The accept-rate delta against v2-haiku isolates the
annotator-model component; the residual against v1-sonnet isolates the schema component.

### Proxy-benchmark provenance (t0015 motivation)

t0009's `details.json` lists four benchmarks: `FrontierScience-Olympiad`, `SWE-bench Verified`,
`WorkArena++`, `tau-bench`. The first two are accurate. The latter two are mislabelled — the rows
under those labels are `Mind2Web` and `HumanEval` rows used as proxies. Once the t0012 smoke result
is reported, the per-benchmark numbers would otherwise be attributed to benchmarks the project does
not actually evaluate on. t0015 fixes the labels via a `correction` file (no re-annotation, no API
spend) so downstream consumers and reports see the corrected source corpora.

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

Verified counts cross-checked against the on-disk correction-file table: rejections = 5 (verified),
reprioritizations = 3 (verified), new tasks = 2 (verified), corrections = 8 (verified).

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

Planning task; no experiments run. Multi-provider replication and v2 row-count expansion remain on
the backlog. The schema component of the v2 delta is asserted only after t0014 lands; until then,
the +58 pp number stays publicly attributable to the schema.

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
