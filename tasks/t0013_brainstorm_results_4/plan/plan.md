# Plan: Brainstorm Session 4

## Objective

Resolve the two issues surfaced in t0009 — the schema-vs-model confound and the proxy-benchmark
label drift — by inserting two parallel-safe pre-Phase-2 tasks (`t0014` Sonnet rerun and `t0015`
proxy-benchmark relabel correction). Apply Round 2 suggestion cleanup deferred from brainstorm 3:
five rejections and three reprioritizations.

## Approach

Inline brainstorm. Aggregate state through the standard four-aggregator triplet (tasks, suggestions,
answers, costs), reassess high-priority suggestions against the t0009-t0011 results, present an
independent priority list to the researcher, and iterate on the wave 4 task list. Apply all
suggestion cleanup as correction files in `corrections/`. Create the two child task folders under
`/create-task` semantics (`task.json` + `task_description.md` only; full task lifecycle created by
`/execute-task`).

## Cost Estimation

USD 0. Pure planning task; no API or compute spend.

## Step by Step

1. Run aggregators (tasks, suggestions, answers, costs); read recent `results_summary.md` files for
   t0009-t0011 to ground reassessed priorities.
2. Re-materialize overview to refresh GitHub-readable views.
3. Round 1: propose two parallel pre-Phase-2 tasks — `t0014` (Sonnet rerun) and `t0015` (proxy
   benchmark relabel correction). Researcher confirms with budget cap $10.
4. Round 2: propose 5 rejections and 3 reprioritizations. Researcher delegates "отклоняй чо хочешь".
5. Round 3: confirmation. Researcher: "go".
6. Create the brainstorm task folder.
7. Apply 5 rejection corrections + 3 reprioritization corrections in `corrections/`.
8. Create child task folders for `t0014` and `t0015`.
9. Run `verify_task_file`, `verify_corrections`, `verify_suggestions`, `verify_logs`.
10. Re-materialize overview, run flowmark on edited markdown, commit, push, PR, pre-merge verify,
    merge.
11. After merge, fork two parallel `/execute-task` background agents for `t0014` and `t0015`.
    `t0012` stays in_progress and is unaffected.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm tasks produce no assets.

## Time Estimation

Inline session under one hour of researcher time.

## Risks & Fallbacks

Risk: t0014's Sonnet rerun shows that the v2 schema delta is mostly the model swap, not the schema
upgrade. Fallback: report the deconfound result honestly; if the schema component is small,
re-evaluate whether the v2 dataset is the correct foundation for t0012's headline experiment, and
queue a v3 schema iteration in brainstorm 5.

Risk: t0015's correction file is rejected by `verify_corrections` because the t0009 dataset
aggregator does not yet support per-row label updates. Fallback: extend the correction to the
dataset asset's `details.json` `description_path` overlay and document the limitation as a follow-up
suggestion.

Risk: a suggestion rejected here turns out to be the right line of work after t0012 lands. Fallback:
any later task can write a correction with `action: "update"` and `changes: {"status": "active"}` to
revive a rejected suggestion. Rejections in this session are reversible.

## Verification Criteria

* `verify_task_file` passes for `t0013`, `t0014`, and `t0015`.
* `verify_corrections` passes for all eight correction files.
* `verify_suggestions` passes for `t0013` (`suggestions.json` is empty).
* `verify_logs` passes (LG-W001/W005/W007/W008 acceptable for a planning task).
