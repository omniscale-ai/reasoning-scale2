# Plan: Brainstorm Session 7

## Objective

Rescope the t0023 confirmatory experiment around the t0019 judge-calibration finding and the $26.12
remaining budget. The agreed outcome is to refresh the project's literature understanding of
hierarchical / granularity-aware agents and judge methodology before committing the remaining budget
to another sonnet experiment.

## Approach

1. Aggregate project state (tasks, suggestions, costs, answers).
2. Read results summaries for t0019, t0020, t0021, t0022 (the four tasks completed since t0018).
3. Form an independent priority reassessment for every active suggestion in light of t0019's
   judge-anchoring finding.
4. Present project state, surface the t0023-vs-budget conflict, propose candidate paths.
5. Discuss with the researcher; converge on a slate that informs the next agent-iteration design
   before committing further experiment spend.
6. Create the brainstorm-results task folder.
7. Apply decisions: cancel t0023, write 5 correction files, create t0025 (literature survey) via
   `/create-task`, and add the 10 reading-list papers as paper assets.
8. Finalize: write step logs, results files, run verificators, push, PR, merge.

## Cost Estimation

$0 — purely a planning session. No API or compute spend.

## Step by Step

* Step 1 (review-project-state): run aggregators, read t0019-t0022 results summaries, materialize
  overview.
* Step 2 (discuss-decisions): present candidate paths; converge on a literature-survey-first slate
  with the next agent-iteration experiment deferred to a post-survey brainstorm; defer RQ3.
* Step 3 (apply-decisions): cancel t0023; write 5 correction files; create t0025
  (`lit_survey_hierarchical_agents_and_judges_2024_2026`).
* Step 4 (finalize): step logs, results, verificators, push, PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None — brainstorm tasks produce no assets, only correction files and child task folders.

## Time Estimation

~1.5 hours of researcher dialogue + execution.

## Risks & Fallbacks

* Risk: child-task creation fails verification. Fallback: fix verification errors and re-run
  `/create-task` for t0025.
* Risk: pre-merge verificator fails. Fallback: address the specific error code surfaced and retry.
* Risk: cancelling t0023 leaves dangling references. Fallback: search for inbound references via the
  task aggregator and update any task-description prose that names t0023 directly.
* Risk: paper downloads fail for paywalled venues. Fallback: per `add-paper` skill, set
  `download_status: failed` and write the summary from the abstract + metadata.

## Verification Criteria

* All 5 correction files pass `verify_corrections t0024_brainstorm_results_7`.
* t0025 task folder passes `verify_task_file`.
* `verify_logs t0024_brainstorm_results_7` passes for all four step folders.
* Pre-merge verificator passes.
