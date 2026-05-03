# Rationale: Cancellation of t0029 and t0030 under no-Anthropic constraint

## What this task does

Two task statuses were flipped to `cancelled`:

* `t0029_rq1_discordance_rich_resample`: `intervention_blocked` → `cancelled`
* `t0030_rq4_info_asymmetry_stratification`: `not_started` → `cancelled`

Both edits were made directly to the respective `task.json` files. No `corrections/*.json` files
were written, because — see "Why direct edit" below — the corrections overlay does not support
task-status mutations.

This task does not modify any other field on those tasks: their plans, research, locked
hyperparameters, results, code, and assets are preserved unchanged on the historical record.

## Why cancellation is correct

The cancellation follows directly from `t0032_no_anthropic_rq1_path_decision` (merged in PR #50),
which locked in **option (a) — existing-results-only verdict** as the recommended RQ1 execution
path. The full chain:

1. The standing operating constraint of this project is that `ANTHROPIC_API_KEY` is permanently
   unavailable — not a temporary outage. Auto-memory and `project/description.md` both treat this as
   a durable posture.
2. t0029's locked plan called for a 218-pair Sonnet rerun (~$26.54 reserved) to reach >=30
   discordant pairs and obtain an RQ1 McNemar verdict. The Sonnet rerun cannot run without Anthropic
   access.
3. t0029 was paused with status `intervention_blocked` waiting on that provider access. Under the
   no-Anthropic constraint, the intervention can never be resolved, so the task is permanently
   stuck.
4. t0030's `data-analysis` / `answer-question` plan explicitly stratifies t0029's paired sample
   outputs. Without t0029 producing those outputs, t0030 cannot launch.
5. t0032's option-(a) verdict ratified that no Anthropic-backed continuation of the RQ1 plan is
   viable, and that the RQ1 path forward is the existing-results-only realignment already executed
   by `t0033_realign_t0031_t0029_no_anthropic`.

Leaving t0029 in `intervention_blocked` and t0030 in `not_started` would keep both tasks visible in
runnable / uncovered aggregator views and misrepresent the project's actual posture. Cancellation
makes the task ledger reflect reality.

The cancellation is a downstream consequence of t0032's verdict — not a failure of t0029's or
t0030's original design. Both plans remain on the historical record as pre-registered and
no-longer-executable under no-Anthropic conditions, and should be cited verbatim in any future
no-Anthropic literature comparison.

## Why direct edit (not a `corrections/*.json` file)

The original scaffold for this task assumed both flips would go through the corrections overlay.
That turned out to be mechanically impossible:

* The corrections framework (`arf/scripts/common/artifacts.py`) defines `ALL_TARGET_KINDS` as
  exactly `{suggestion, paper, answer, dataset, library, model, predictions}`. There is no `task`
  target kind.
* `arf/specifications/corrections_specification.md` confirms the same target_kind set in its
  authoritative table.
* `arf/scripts/aggregators/aggregate_tasks.py` does not consult any corrections overlay when
  computing task status — there is no aggregator-side mechanism to honor a task-status correction
  even if one were written.
* No correction file in the repo (52 in total at the time of this task) targets a task; every one
  targets a `suggestion` or a `dataset`. There is no precedent for a task-status correction because
  the framework does not support one.

The brainstorm-skill rule says only `not_started` tasks can have `task.json` directly edited and
that completed or in-progress tasks must never be modified. `intervention_blocked` is neither
`not_started` nor `completed` / `in_progress`; the rule does not formally cover it.

Given that:

* the corrections overlay cannot express the change,
* extending the corrections framework with a `task` target_kind is explicitly out of scope per
  CLAUDE.md rule 0 (framework changes are not task work) and was not requested,
* t0029 has no paid execution outputs, no committed predictions, and no results files — its status
  is the only field the cancellation needs to mutate,
* the immutability rule's purpose is to protect completed research / results / code / assets, and
  this edit changes none of those,

the user explicitly authorized direct-editing both `task.json` files in this session. The edits add
an `end_time` timestamp matching the cancellation moment and flip `status` to `cancelled`. No other
fields are touched.

For t0030, direct edit was already permitted by the brainstorm-skill rule (status was
`not_started`), so its treatment is straightforward.

## Permanence

The cancellation is durable for as long as the no-Anthropic constraint holds. If Anthropic access
ever became available again, restarting the original t0029 plan would require a fresh task with its
own task ID — the `cancelled` state on t0029 / t0030 should not be reverted. Their plans are the
historical record of what was pre-registered under no-Anthropic conditions; they are not a queue of
pending work.

## Files in this task's `corrections/` folder

This document is the only file in `corrections/`. There are no `*.json` correction files because no
aggregated artifact (suggestion, paper, answer, dataset, library, model, predictions) needed
correcting — only two task statuses, which the overlay cannot express.
