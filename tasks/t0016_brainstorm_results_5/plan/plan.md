# Plan: Brainstorm Session 5

## Objective

Pure backlog cleanup after `t0014_v2_annotator_sonnet_rerun` and
`t0015_correct_proxy_benchmark_labels` merged: prune 3 redundant suggestions, reprioritize 5, and
record the haiku-default annotation policy as a decision rather than a task. No new tasks created.

## Approach

1. Aggregate tasks, suggestions, costs, and answer assets to produce a project-state snapshot.
2. Reread `t0014` results and `compare_literature.md` to extract the load-bearing science update
   (the +57 pp schema-only delta likely bundles a truncation fix; haiku-judge familial bias is
   unresolved).
3. Reassess priorities of all 35 active suggestions independently of their stored values.
4. Present state and proposals to the researcher; iterate.
5. Write 8 correction files in `corrections/` (3 status updates to "rejected", 5 priority changes).
6. Run all verificators, materialize the overview, push, PR, merge.

## Cost Estimation

Zero API spend. Pure planning task.

## Step by Step

1. Phase 1: aggregate tasks/suggestions/costs/answers; read t0014 + t0015 result summaries; read
   t0014 `compare_literature.md`; reassess priorities.
2. Phase 1.5: clarify session focus and budget envelope with researcher.
3. Phase 2 (Round 2 only): present 3 reject + 5 reprioritize proposals; iterate.
4. Phase 2 (Round 3): summarize and lock in the decision list.
5. Phase 3: determine next task index (16); confirm session number (5).
6. Phase 4: create branch `task/t0016_brainstorm_results_5`; create folder structure.
7. Phase 5: write 8 correction files in `corrections/`.
8. Phase 6: results docs, step logs, session log, capture; verificators; overview; commit; PR;
   merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. This is a planning-only task.

## Time Estimation

~30 minutes wall-clock for the full session including merge.

## Risks & Fallbacks

* **t0012 perturbed.** Mitigation: this branch touches no t0012 files and modifies no t0009 dataset
  files; t0012 reads the t0009 dataset through the aggregator and is unaffected.
* **Merge conflicts on overview/.** Mitigation: re-run materializer just before commit so the
  overview reflects post-merge state; the materializer is deterministic on the same input.
* **Pre-merge verificator failures.** Mitigation: PR body uses the four mandatory sections from the
  start.

## Verification Criteria

* `verify_task_file t0016_brainstorm_results_5` passes 0 errors.
* `verify_corrections t0016_brainstorm_results_5` passes 0 errors.
* `verify_suggestions t0016_brainstorm_results_5` passes 0 errors (empty suggestions array).
* `verify_logs t0016_brainstorm_results_5` passes 0 errors (warnings LG-W005, LG-W007, LG-W008
  acceptable per skill spec).
* `verify_pr_premerge` passes 0 errors before merge.
* Aggregator output post-merge shows: S-0005-04, S-0005-05, S-0014-04 with status "rejected";
  S-0009-04 priority "high"; S-0002-09, S-0006-02, S-0011-02, S-0014-05 priority "low".
