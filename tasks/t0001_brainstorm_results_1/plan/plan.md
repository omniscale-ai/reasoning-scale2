# Plan: Brainstorm Session 1

## Objective

Translate the project description and four-phase research roadmap into the first concrete tasks.
Produce no experimental output; only task plans.

## Approach

Follow the `/human-brainstorm` skill in lightweight mode for an empty project. Skip aggregator
review (all aggregators return zero rows on a fresh fork). Propose four candidate tasks that
together unblock Phase 1 annotation work and Phase 2 baseline experiments. Confirm researcher
choices and create matching not-started task folders.

## Cost Estimation

USD 0. Pure planning task; no API or compute spend.

## Step by Step

1. Review project state (empty for a fresh fork).
2. Propose four candidate first tasks with rationale, cost, and dependencies.
3. Receive researcher decision: T1 and T2 accepted, T3 and T4 deferred.
4. Create child task folders for T1 and T2.
5. Run verificators, commit, push, PR, merge.

## Remote Machines

None.

## Assets Needed

None.

## Expected Assets

None. Brainstorm tasks produce no assets.

## Time Estimation

Inline session, under one hour of researcher time.

## Risks & Fallbacks

Risk: chosen tasks turn out to be misaligned after literature review. Fallback: future brainstorm
sessions can cancel `not_started` tasks via `task.json` edits or the corrections mechanism.

## Verification Criteria

* `verify_task_file` passes for the brainstorm task and both child tasks.
* `verify_logs` passes with at most the documented LG-W005 / LG-W007 / LG-W008 warnings.
* `verify_corrections` and `verify_suggestions` pass (both files are empty).
