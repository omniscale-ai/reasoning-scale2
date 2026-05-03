# Cancel t0029 and t0030 under no-Anthropic constraint

## Motivation

This task is a mechanical consequence of `t0032_no_anthropic_rq1_path_decision`'s option-(a)
verdict. It is **not** a re-evaluation of t0029 / t0030's original design.

* The auto-memory and the project's standing operating constraint both record that
  `ANTHROPIC_API_KEY` is permanently unavailable. This is the durable posture, not a temporary
  outage.
* `t0029_rq1_discordance_rich_resample` was paused with status `intervention_blocked` waiting on
  Anthropic provider access for a 218-pair Sonnet rerun (~$26.54 budget reserved).
* `t0030_rq4_info_asymmetry_stratification` has status `not_started` and a hard upstream dependency
  on t0029's outputs, so it cannot launch as long as t0029 stays blocked.
* `t0032_no_anthropic_rq1_path_decision` (merged in PR #50) locked in **option (a) —
  existing-results-only verdict** as the recommended RQ1 execution path, explicitly because no
  Anthropic-backed continuation is viable.

With option (a) on the books, t0029's Sonnet rerun and t0030's downstream RQ4 stratification cannot
be unblocked. Leaving them in `intervention_blocked` / `not_started` keeps surfacing them in
runnable / uncovered aggregator views and misrepresents the project's actual no-Anthropic posture.

Cancelling them now:

1. Frees the ~$26.54 budget reserved for t0029.
2. Removes both tasks from `--uncovered` aggregator views and from the runnable next-action lists.
3. Makes the project's task ledger reflect the actual no-Anthropic posture — i.e., that the RQ1 path
   forward is the t0033-level realignment of existing results, not a paused Sonnet rerun.

This task implements the cancellation. It does not alter any of the original locked plans, research,
or results files for t0029 / t0030 — those remain on the historical record as pre-registered and
no-longer-executable under the no-Anthropic constraint.

## Scope

The work is mechanical and consists of mutating two task statuses plus a short rationale note:

1. **t0029 (intervention_blocked → cancelled).** Status is **not** `not_started`, so per the
   corrections-overlay rule the change must go through this task's `corrections/` folder, not a
   direct edit to `tasks/t0029_rq1_discordance_rich_resample/task.json`. Write a correction file
   following `arf/specifications/corrections_specification.md` with `action: "update"` and
   `changes: {"status": "cancelled"}`. The rationale field must explicitly cite t0032's option-(a)
   verdict and the no-Anthropic constraint as the trigger, and must clarify that the 218-pair Sonnet
   rerun plan is preserved as historical / pre-registered, **not** retracted.

2. **t0030 (not_started → cancelled).** Status is currently `not_started`, so the brainstorm rule
   allows direct editing of `tasks/t0030_rq4_info_asymmetry_stratification/task.json`. Either route
   is acceptable; prefer the **corrections overlay** for symmetry with t0029 and so both
   cancellations live in one place. Whichever route is used, the rationale must record that the
   trigger is t0032's verdict and the upstream dependency on t0029's outputs (which will never be
   produced).

3. **Rationale note.** Inside this task's `corrections/` folder, write a short markdown note (e.g.,
   `corrections/rationale.md`) documenting that:

   * The cancellation is a downstream consequence of t0032's option-(a) verdict, not a failure of
     t0029 / t0030's original design.
   * The locked plans for both tasks are retained on the historical record under no-Anthropic
     conditions and should be cited verbatim in any future no-Anthropic literature comparison.
   * The cancellation is permanent for as long as the no-Anthropic constraint holds.

4. **Overview refresh.** After the PR merges, run `arf.scripts.overview.materialize` so the
   `runnable-actions`, `not_started`, and `intervention_blocked` views drop t0029 / t0030.

## Out of Scope (Explicit Non-Goals)

* **Do NOT launch new experiments.** No paid API calls, no remote compute, no Sonnet runs.
* **Do NOT resume the old `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` B-run loop** in any form.
  That loop was retired before t0028 / t0029 existed; reviving it is out of scope for this and any
  other no-Anthropic task.
* **Do NOT modify any of t0029's or t0030's plan / research / results / corrections / log files.**
  The immutability rule still applies. The only mutation is the `status` field, expressed via this
  task's corrections overlay (or, for t0030, optionally a direct task.json edit).
* **Do NOT propose replacement experiments here.** That belongs in S-0032-02 / S-0032-03 follow-ups,
  not in this correction task.

## Approach

This is a pure correction task. The anticipated step list (canonical step IDs only — no research,
planning, setup-machines, teardown, creative-thinking, or compare-literature steps):

1. `create-branch` — preflight
2. `check-deps` — preflight (verifies t0032 is `completed`)
3. `init-folders` — preflight (creates the standard task folder skeleton)
4. `implementation` — write the two correction files plus `corrections/rationale.md`; if the t0030
   change is implemented as a direct edit instead, also stage the edit to
   `tasks/t0030_rq4_info_asymmetry_stratification/task.json`. Run `verify_corrections` and
   `verify_task_file` for any direct-edited task.
5. `results` — write `results_summary.md` / `results_detailed.md` recording the two status flips and
   the rationale. `metrics.json` is `{}`. `costs.json` is zero. `remote_machines_used.json` is `[]`.
6. `suggestions` — none expected; record an empty `suggestions.json`.
7. `reporting` — final verificator sweep, PR, merge, post-merge `arf.scripts.overview.materialize`
   on `main`.

## Verification Criteria

* `verify_corrections` passes with **0 errors** on this task's `corrections/` folder.
* If t0030 is direct-edited, `verify_task_file` passes with 0 errors on
  `t0030_rq4_info_asymmetry_stratification`.
* After post-merge overview refresh:
  * `aggregate_tasks --status cancelled` includes both `t0029_rq1_discordance_rich_resample` and
    `t0030_rq4_info_asymmetry_stratification`.
  * `aggregate_tasks --status intervention_blocked` no longer lists t0029.
  * `aggregate_tasks --status not_started` no longer lists t0030.
  * `aggregate_suggestions --uncovered` no longer surfaces S-0032-01 as actionable (covered by this
    task via `source_suggestion`).
* `corrections/rationale.md` cites `t0032_no_anthropic_rq1_path_decision` as the trigger and the
  permanent no-Anthropic constraint as the reason cancellation is durable.

## Expected Assets

None. This task produces no new datasets, papers, libraries, models, predictions, or answers. It
only mutates the status field of two pre-existing tasks via the corrections overlay (and,
optionally, a direct task.json edit for the `not_started` t0030).
