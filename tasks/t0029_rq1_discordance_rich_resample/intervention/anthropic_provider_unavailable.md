# Intervention: Anthropic provider access unavailable indefinitely

**Status**: blocking — `intervention_blocked`

**Recorded by**: `t0033_realign_t0031_t0029_no_anthropic`

**Date**: 2026-05-03

## What is blocked

`t0029_rq1_discordance_rich_resample` cannot proceed as specified. The task's locked plan (paired
A-vs-B McNemar resample on a discordance-rich sample under a hard $35 cap, executed against
Claude-policy arms) requires Anthropic API access that is no longer available.

## Why

Anthropic API access (`ANTHROPIC_API_KEY` / Claude API for paid task execution) is unavailable
indefinitely on this project — not "credentials pending" but a permanent, durable constraint. The
locked t0029 plan and its $35 budget cap are therefore not executable in their pre-registered form.

## What is preserved as historical

The locked plan in `tasks/t0029_rq1_discordance_rich_resample/task_description.md` is preserved as
the original pre-registered design. It is **not** modified by this intervention. It remains on the
record so that future readers can audit the original RQ1 architecture (paired McNemar, $35 cap, arm
A = Plan-and-Solve baseline, arm B = scope-aware ReAct) regardless of whether any future
re-execution actually uses it.

## Replacement-path ownership

The decision about how RQ1 is now answered — without Anthropic — is owned by
`t0032_no_anthropic_rq1_path_decision`. That task picks one of:

* (a) accept the existing t0027 + t0031 evidence as the final RQ1 verdict
* (b) re-run on locally available open-weight models
* (c) substitute a non-Anthropic paid provider under a tight budget
* (d) close RQ1 with an explicit "underpowered, provider-blocked" stop

Whichever path t0032 selects, it must not assume Anthropic access becomes available later.

## What this intervention does NOT do

* Does not modify `task_description.md` of t0029 (locked plan stays intact).
* Does not start `t0030_rq4_info_asymmetry_stratification`; that task's preconditions are gated on
  whichever path t0032 chooses.
* Does not assume the block is temporary or that a key will arrive.

## Resolution criteria

The block is removed only if t0032 picks an execution path that t0029 itself can carry out. Under
options (a) and (d), t0029 stays `intervention_blocked` permanently and a follow-up correction task
may close it as `cancelled` or `permanently_failed`. Under options (b) or (c), a future task may
either re-execute t0029 itself (if the framework allows) or open a successor task that inherits the
locked design with the alternative provider documented.
