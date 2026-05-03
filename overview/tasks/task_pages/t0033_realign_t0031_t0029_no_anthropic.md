# ⏹ Realign t0031 suggestions and t0029 status under no-Anthropic constraint

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0033_realign_t0031_t0029_no_anthropic` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Task types** | `correction` |
| **Task folder** | [`t0033_realign_t0031_t0029_no_anthropic/`](../../../tasks/t0033_realign_t0031_t0029_no_anthropic/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0033_realign_t0031_t0029_no_anthropic/task_description.md)*

# Realign t0031 suggestions and t0029 status under no-Anthropic constraint

## Motivation

Anthropic API access is now confirmed unavailable indefinitely (not "credentials pending").
Two artifacts produced before this constraint was clear are now misaligned with reality and
must be corrected:

1. `t0031_rq1_rq4_no_new_api_salvage` (completed, immutable) emitted suggestion `S-0031-01`
   ("Unblock t0029 by provisioning ANTHROPIC_API_KEY") and `S-0031-02` (which assumes the
   locked t0029 path under Anthropic execution). Neither suggestion is actionable any more.
2. `t0029_rq1_discordance_rich_resample` is on disk with `status: "in_progress"` and
   `start_time: "2026-05-03T09:55:36Z"` despite never having executed. Its true state is
   "blocked on unavailable provider access", which the framework expresses as
   `intervention_blocked` plus an intervention file.

Note: the corrections specification (v3) does not define a `task` target kind, so t0029's
status flip is implemented as a direct edit of its `task.json` from this task's branch (t0029
is not completed; rule 5 does not apply). The two suggestion realignments use standard
`suggestion` correction files.

## Scope

**Strictly limited to:**

* Realigning `S-0031-01` and `S-0031-02` via correction files.
* Flipping `t0029_rq1_discordance_rich_resample` to `intervention_blocked` and writing one
  intervention file naming the block as permanent provider unavailability.
* Preserving t0029's `task_description.md` exactly as-is (the locked, pre-registered plan
  stays on the record as historical).

**Out of scope:**

* Modifying `t0032_no_anthropic_rq1_path_decision` in any way.
* Launching `t0030_rq4_info_asymmetry_stratification`.
* Touching `S-0031-03` (cost-tracker boundary fix). It remains valid and unchanged.
* Spending any new paid-API budget or provisioning remote machines.
* Any reasoning that assumes Anthropic access becomes available later.

## Inputs

* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/suggestions.json` — the two targets
  (`S-0031-01`, `S-0031-02`).
* `tasks/t0029_rq1_discordance_rich_resample/task.json` — the status to flip.
* `tasks/t0032_no_anthropic_rq1_path_decision/task.json` — the upstream that will own the
  no-Anthropic RQ1 decision; referenced in the new S-0031-01 description but not modified
  here.

## Constraints

* **No `ANTHROPIC_API_KEY` is or will be available.** Treat Anthropic access as permanently
  unavailable.
* No remote-machine spend.
* Do not edit anything inside `tasks/t0031_*/` (it is a completed, immutable task).
* Do not edit anything inside `tasks/t0032_*/`.
* The two correction files must follow the v3 corrections spec
  (`arf/specifications/corrections_specification.md`); both use `action: "update"` and supply
  a `rationale` that names the no-Anthropic constraint as the reason.

## Output

1. `tasks/t0033_realign_t0031_t0029_no_anthropic/corrections/suggestion_S-0031-01.json` —
   `action: "update"`, replacing `title` and `description` with the no-Anthropic
   alternative-path framing (decide an RQ1 execution/verdict path that does not require
   Anthropic API access; pointer to `t0032_no_anthropic_rq1_path_decision` as the task that
   owns the decision); priority stays `high`; `kind` stays `experiment`.
2. `tasks/t0033_realign_t0031_t0029_no_anthropic/corrections/suggestion_S-0031-02.json` —
   `action: "update"`, rewriting `description` so the cap-reconsideration is conditional on
   any future *non-Anthropic* paid execution path; priority stays `high`; `kind` stays
   `evaluation`.
3. Direct edit of `tasks/t0029_rq1_discordance_rich_resample/task.json`: set `status` →
   `"intervention_blocked"`. Leave `start_time` as-is; `end_time` stays `null`.
   `task_description.md` is **not** modified.
4. New file
   `tasks/t0029_rq1_discordance_rich_resample/intervention/anthropic_provider_unavailable.md`
   stating: provider access (Claude / Anthropic) is unavailable indefinitely; the locked plan
   and $35 cap are preserved as a pre-registered design but are not executable;
   replacement-path decision is owned by `t0032_no_anthropic_rq1_path_decision`.
5. Standard task results: `results_summary.md` (with the headline label `T0031/T0029
   NO-ANTHROPIC REALIGNMENT — CORRECTIONS APPLIED`), `results_detailed.md`, `metrics.json`
   (registered keys only, all `null`), `costs.json` (`total_cost_usd: 0.00`),
   `remote_machines_used.json: []`, `suggestions.json` (no follow-up suggestions; t0032
   already owns the next decision — emit an empty `suggestions: []` if the spec allows, else
   one explicit `kind: "evaluation"` pointer to t0032).

## Approach

This is a `correction` task. Skip research and planning steps — the targets and fixes are
fully explicit in this description. Step list:

1. `create-branch`
2. `check-deps`
3. `init-folders`
4. `implementation` — write the two correction JSON files; edit t0029 `task.json`; write the
   intervention file.
5. `results` — write the standard results files; run `verify_corrections`,
   `verify_task_results`, and `verify_task_dependencies`.
6. `suggestions` — confirm no follow-ups (or one t0032 pointer); run `verify_suggestions`.
7. `reporting` — close out, run final verificators, push, PR, merge.

## Verification criteria

* `verify_corrections` passes for both correction files (correct `correction_id` format
  `C-0033-01`/`C-0033-02`, target tasks/IDs resolve, action/changes/rationale all present).
* `verify_task_dependencies` continues to pass (only listed dependency is `t0031`).
* `verify_task_file` passes.
* `verify_task_results` passes (0 errors).
* `verify_suggestions` passes.
* After merge, the `aggregate_suggestions` aggregator returns the corrected effective view of
  S-0031-01 and S-0031-02.
* `tasks/t0029_*/task.json` reads `status: "intervention_blocked"` on `main`, with
  `tasks/t0029_*/intervention/anthropic_provider_unavailable.md` present.
* `tasks/t0030_*/` is untouched.
* `tasks/t0032_*/` is untouched.

## Risks & fallbacks

* If `verify_pr_premerge` rejects the cross-task edit of t0029, fall back to: (i) keep the two
  suggestion corrections, (ii) document the t0029-status discrepancy as a known issue in
  `results_summary.md`, and (iii) escalate to the user before opening the PR. Do **not**
  silently revert or work around the verificator.
* If the corrections verificator rejects an `update` that changes only `description`/`title`,
  re-read `arf/specifications/corrections_specification.md` and adjust; never invent fields.

</details>
