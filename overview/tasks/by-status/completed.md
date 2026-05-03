# ✅ Tasks: Completed

31 tasks. ✅ **31 completed**.

[Back to all tasks](../README.md)

---

## ✅ Completed

<details>
<summary>✅ 0034 — <strong>Cancel t0029 and t0030 under no-Anthropic
constraint</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0034_cancel_t0029_t0030_no_anthropic` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0032_no_anthropic_rq1_path_decision`](../../../overview/tasks/task_pages/t0032_no_anthropic_rq1_path_decision.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0032-01` |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-05-03T14:18:02Z |
| **End time** | 2026-05-03T14:27:30Z |
| **Step progress** | 7/15 |
| **Task page** | [Cancel t0029 and t0030 under no-Anthropic constraint](../../../overview/tasks/task_pages/t0034_cancel_t0029_t0030_no_anthropic.md) |
| **Task folder** | [`t0034_cancel_t0029_t0030_no_anthropic/`](../../../tasks/t0034_cancel_t0029_t0030_no_anthropic/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0034_cancel_t0029_t0030_no_anthropic/results/results_detailed.md) |

# Cancel t0029 and t0030 under no-Anthropic constraint

## Motivation

This task is a mechanical consequence of `t0032_no_anthropic_rq1_path_decision`'s option-(a)
verdict. It is **not** a re-evaluation of t0029 / t0030's original design.

* The auto-memory and the project's standing operating constraint both record that
  `ANTHROPIC_API_KEY` is permanently unavailable. This is the durable posture, not a temporary
  outage.
* `t0029_rq1_discordance_rich_resample` was paused with status `intervention_blocked` waiting
  on Anthropic provider access for a 218-pair Sonnet rerun (~$26.54 budget reserved).
* `t0030_rq4_info_asymmetry_stratification` has status `not_started` and a hard upstream
  dependency on t0029's outputs, so it cannot launch as long as t0029 stays blocked.
* `t0032_no_anthropic_rq1_path_decision` (merged in PR #50) locked in **option (a) —
  existing-results-only verdict** as the recommended RQ1 execution path, explicitly because no
  Anthropic-backed continuation is viable.

With option (a) on the books, t0029's Sonnet rerun and t0030's downstream RQ4 stratification
cannot be unblocked. Leaving them in `intervention_blocked` / `not_started` keeps surfacing
them in runnable / uncovered aggregator views and misrepresents the project's actual
no-Anthropic posture.

Cancelling them now:

1. Frees the ~$26.54 budget reserved for t0029.
2. Removes both tasks from `--uncovered` aggregator views and from the runnable next-action
   lists.
3. Makes the project's task ledger reflect the actual no-Anthropic posture — i.e., that the
   RQ1 path forward is the t0033-level realignment of existing results, not a paused Sonnet
   rerun.

This task implements the cancellation. It does not alter any of the original locked plans,
research, or results files for t0029 / t0030 — those remain on the historical record as
pre-registered and no-longer-executable under the no-Anthropic constraint.

## Scope

The work is mechanical and consists of mutating two task statuses plus a short rationale note:

1. **t0029 (intervention_blocked → cancelled).** Status is **not** `not_started`, so per the
   corrections-overlay rule the change must go through this task's `corrections/` folder, not
   a direct edit to `tasks/t0029_rq1_discordance_rich_resample/task.json`. Write a correction
   file following `arf/specifications/corrections_specification.md` with `action: "update"`
   and `changes: {"status": "cancelled"}`. The rationale field must explicitly cite t0032's
   option-(a) verdict and the no-Anthropic constraint as the trigger, and must clarify that
   the 218-pair Sonnet rerun plan is preserved as historical / pre-registered, **not**
   retracted.

2. **t0030 (not_started → cancelled).** Status is currently `not_started`, so the brainstorm
   rule allows direct editing of `tasks/t0030_rq4_info_asymmetry_stratification/task.json`.
   Either route is acceptable; prefer the **corrections overlay** for symmetry with t0029 and
   so both cancellations live in one place. Whichever route is used, the rationale must record
   that the trigger is t0032's verdict and the upstream dependency on t0029's outputs (which
   will never be produced).

3. **Rationale note.** Inside this task's `corrections/` folder, write a short markdown note
   (e.g., `corrections/rationale.md`) documenting that:

   * The cancellation is a downstream consequence of t0032's option-(a) verdict, not a failure
     of t0029 / t0030's original design.
   * The locked plans for both tasks are retained on the historical record under no-Anthropic
     conditions and should be cited verbatim in any future no-Anthropic literature comparison.
   * The cancellation is permanent for as long as the no-Anthropic constraint holds.

4. **Overview refresh.** After the PR merges, run `arf.scripts.overview.materialize` so the
   `runnable-actions`, `not_started`, and `intervention_blocked` views drop t0029 / t0030.

## Out of Scope (Explicit Non-Goals)

* **Do NOT launch new experiments.** No paid API calls, no remote compute, no Sonnet runs.
* **Do NOT resume the old `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` B-run loop** in any
  form. That loop was retired before t0028 / t0029 existed; reviving it is out of scope for
  this and any other no-Anthropic task.
* **Do NOT modify any of t0029's or t0030's plan / research / results / corrections / log
  files.** The immutability rule still applies. The only mutation is the `status` field,
  expressed via this task's corrections overlay (or, for t0030, optionally a direct task.json
  edit).
* **Do NOT propose replacement experiments here.** That belongs in S-0032-02 / S-0032-03
  follow-ups, not in this correction task.

## Approach

This is a pure correction task. The anticipated step list (canonical step IDs only — no
research, planning, setup-machines, teardown, creative-thinking, or compare-literature steps):

1. `create-branch` — preflight
2. `check-deps` — preflight (verifies t0032 is `completed`)
3. `init-folders` — preflight (creates the standard task folder skeleton)
4. `implementation` — write the two correction files plus `corrections/rationale.md`; if the
   t0030 change is implemented as a direct edit instead, also stage the edit to
   `tasks/t0030_rq4_info_asymmetry_stratification/task.json`. Run `verify_corrections` and
   `verify_task_file` for any direct-edited task.
5. `results` — write `results_summary.md` / `results_detailed.md` recording the two status
   flips and the rationale. `metrics.json` is `{}`. `costs.json` is zero.
   `remote_machines_used.json` is `[]`.
6. `suggestions` — none expected; record an empty `suggestions.json`.
7. `reporting` — final verificator sweep, PR, merge, post-merge
   `arf.scripts.overview.materialize` on `main`.

## Verification Criteria

* `verify_corrections` passes with **0 errors** on this task's `corrections/` folder.
* If t0030 is direct-edited, `verify_task_file` passes with 0 errors on
  `t0030_rq4_info_asymmetry_stratification`.
* After post-merge overview refresh:
  * `aggregate_tasks --status cancelled` includes both `t0029_rq1_discordance_rich_resample`
    and `t0030_rq4_info_asymmetry_stratification`.
  * `aggregate_tasks --status intervention_blocked` no longer lists t0029.
  * `aggregate_tasks --status not_started` no longer lists t0030.
  * `aggregate_suggestions --uncovered` no longer surfaces S-0032-01 as actionable (covered by
    this task via `source_suggestion`).
* `corrections/rationale.md` cites `t0032_no_anthropic_rq1_path_decision` as the trigger and
  the permanent no-Anthropic constraint as the reason cancellation is durable.

## Expected Assets

None. This task produces no new datasets, papers, libraries, models, predictions, or answers.
It only mutates the status field of two pre-existing tasks via the corrections overlay (and,
optionally, a direct task.json edit for the `not_started` t0030).

**Results summary:**

> **Results Summary: Cancel t0029 and t0030 under no-Anthropic constraint**
>
> **Summary**
>
> Flipped two task statuses to `cancelled` as the durable consequence of t0032's option-(a)
> existing-results-only verdict and the permanent absence of `ANTHROPIC_API_KEY`. t0029 moved
> from
> `intervention_blocked` and t0030 from `not_started`. The corrections overlay could not
> express
> either change because its target_kind set has no `task` entry, so both edits were direct
> task.json
> mutations (status + end_time only) authorized by the user. A rationale document captures the
> reasoning chain and the framework constraint.
>
> **Metrics**
>
> * **Tasks cancelled**: **2** (t0029, t0030)
> * **t0029 status flip**: `intervention_blocked` → **`cancelled`**, end_time set to
> **`2026-05-03T14:21:00Z`**
> * **t0030 status flip**: `not_started` → **`cancelled`**, end_time set to
>   **`2026-05-03T14:21:00Z`**
> * **Correction JSON files written**: **0** (overlay does not support `task` target_kind)
> * **Rationale documents written**: **1** (`corrections/rationale.md`)
> * **Budget freed by cancelling t0029**: **~$26.54** (Sonnet rerun reservation;
>   non-recoverable under

</details>

<details>
<summary>✅ 0033 — <strong>Realign t0031 suggestions and t0029 status under
no-Anthropic constraint</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0033_realign_t0031_t0029_no_anthropic` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-05-03T13:07:25Z |
| **End time** | 2026-05-03T13:15:30Z |
| **Step progress** | 7/13 |
| **Task page** | [Realign t0031 suggestions and t0029 status under no-Anthropic constraint](../../../overview/tasks/task_pages/t0033_realign_t0031_t0029_no_anthropic.md) |
| **Task folder** | [`t0033_realign_t0031_t0029_no_anthropic/`](../../../tasks/t0033_realign_t0031_t0029_no_anthropic/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0033_realign_t0031_t0029_no_anthropic/results/results_detailed.md) |

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

**Results summary:**

> **T0031/T0029 NO-ANTHROPIC REALIGNMENT — CORRECTIONS APPLIED**
>
> **Summary**
>
> This task realigned two t0031 follow-up suggestions and one upstream task's status under the
> permanent no-Anthropic constraint. It produced no metrics, no quantitative results, and no
> paid
> spend. Three artefacts changed state on disk:
>
> * `S-0031-01` ("Unblock t0029 by provisioning ANTHROPIC_API_KEY") was redirected via
>   correction
> `C-0033-01` to "Decide a no-Anthropic RQ1 execution path", pointing at
> `t0032_no_anthropic_rq1_path_decision` as the decision owner.
> * `S-0031-02` ("Reconsider $35 cap given preliminary futility") was reframed via correction
> `C-0033-02` so the cap-reconsideration is explicitly conditional on a future non-Anthropic
> paid
> execution path, with auto-rejection if t0032 picks option (a) or (d).
> * `S-0031-03` was intentionally untouched and remains valid.
> * `tasks/t0029_rq1_discordance_rich_resample/task.json` was edited to set
> `status: "intervention_blocked"` (cross-task direct edit, justified by absence of a `task`
> target
> kind in the corrections spec v3 and by t0029 being `in_progress`, not `completed`), and an
> intervention file naming Anthropic provider unavailability as the permanent block was added.
>

</details>

<details>
<summary>✅ 0032 — <strong>No-Anthropic RQ1 path decision</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0032_no_anthropic_rq1_path_decision` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md), [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-03T13:19:53Z |
| **End time** | 2026-05-03T14:05:06Z |
| **Step progress** | 11/15 |
| **Task page** | [No-Anthropic RQ1 path decision](../../../overview/tasks/task_pages/t0032_no_anthropic_rq1_path_decision.md) |
| **Task folder** | [`t0032_no_anthropic_rq1_path_decision/`](../../../tasks/t0032_no_anthropic_rq1_path_decision/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0032_no_anthropic_rq1_path_decision/results/results_detailed.md) |

# No-Anthropic RQ1 path decision

## Motivation

t0029_rq1_discordance_rich_resample is the canonical owner of the RQ1 verdict (paired A-vs-B
McNemar test on a discordance-rich resample under a $35 cap). It was architected around
Claude-policy execution. Anthropic API access is now confirmed unavailable **indefinitely** —
not "credentials pending", but a hard, durable constraint. t0029 therefore cannot proceed as
originally specified.

t0031_rq1_rq4_no_new_api_salvage produced no-new-API preliminary evidence on the existing
t0026/t0027 paired N=130 sample: discordance rate **12/130 = 9.23%**, symmetric overall
(McNemar two-sided p = 1.0000), but with a real benchmark-by-arm interaction (SWE-bench favors
arm B; FrontierScience favors arm A; Tau-bench is dominated by both-fail). Under the locked
t0029 cap, ~218 admittable new pairs would yield ≈ 32 expected discordant; that sample gives ≥
80% one-sided power only when the conditional B-wins rate p1 ≥ 0.75.

We need to decide, with explicit cost / validity / comparability accounting, what RQ1's
realistic execution path now is.

## Scope

This is an **analysis-and-decision** task, not an experiment task. It produces exactly one
`answer` asset that picks one path and records the reasoning. It does **not** spend any new
paid API budget or provision remote machines.

## Inputs

* `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/` — fixed-B, redesigned-C paired
  N=130 outputs; the labelled-arm convention (arm A = Plan-and-Solve baseline; arm B =
  scope-aware ReAct; arm C = matched-mismatch).
* `tasks/t0031_rq1_rq4_no_new_api_salvage/results/` — discordance rate, RQ4 stratification
  (`results/data/rq4_stratification.json`), RQ1 power grid
  (`results/data/rq1_power_grid.json`), and infrastructure audit
  (`results/data/log_audit.json`).
* `tasks/t0029_rq1_discordance_rich_resample/plan/plan.md` — the locked $35-cap plan that is
  currently provider-blocked (and t0029's `task.json`, currently `in_progress`).

## Constraints

* **No `ANTHROPIC_API_KEY` is or will be available.** Treat Anthropic access as permanently
  unavailable for the remainder of the project.
* No remote-machine spend may be assumed without an explicit budget check via the cost
  aggregator.
* The labelled-arm convention from t0026/t0027 must be preserved when reasoning about
  comparability. Anything that re-runs trajectories on a different provider must document the
  comparability gap explicitly.
* Do **not** launch t0030_rq4_info_asymmetry_stratification under current constraints; its
  preconditions (a fresh discordance-rich paired sample) are gated on whichever path this task
  picks.

## Options to evaluate

This task must explicitly compare these four paths:

1. **(a) Existing-results-only verdict.** Accept the t0027 paired N=130 plus the t0031
   re-derivations as the final RQ1 evidence. Document the verdict as "underpowered for any p1
   ≤ 0.65; consistent with no-overall-effect; benchmark-by-arm interaction documented".
2. **(b) Local / open-weight rerun.** Re-execute arms A and/or B on locally available weights
   (or a freely hosted provider with sufficient capacity). Quantify which models are
   realistically runnable on hardware accessible to this project, the wall-clock and cost
   implications, and how much comparability with the Claude-based t0027 baseline is preserved.
3. **(c) Cheaper / alternative paid provider.** Identify a non-Anthropic API provider whose
   offerings can stand in for the policy currently played by Claude on arms A/B (or both),
   under a tight budget. Quantify per-pair cost, total expected spend at the t0029 cap-or-
   reduced-cap, and the comparability risk of swapping policy mid-protocol.
4. **(d) Project-level stop.** Conclude RQ1 with an explicit "underpowered, provider- blocked"
   verdict and reallocate the unspent budget. Specify what subsequent project work this
   unblocks (e.g. RQ4 stratification on existing data, infrastructure cleanup from S-0031-03).

## Approach

1. **Research (existing-code only).** Inventory exactly what t0027 and t0031 produced. No new
   internet research is required for the decision itself, but a minimal scan for alternative
   providers' published per-token pricing is allowed if option (c) needs numbers.
2. **Planning.** Produce a short comparison table over the four options, with columns:
   estimated cost in USD, validity / statistical-power risk, comparability with t0027 /
   t0028's labelled-arm baseline, and time-to-result.
3. **Implementation (analysis-only).** Re-load the t0031 power grid and confirm that the
   recommendation's power claim is internally consistent with the existing tables; no new API
   calls.
4. **Creative thinking.** Before locking in, list at least one non-obvious cost-saver (e.g.
   discordance-only rerun on a small N rather than a discordance-rich resample, or a
   bootstrap-style re-resampling of the existing 130) and decide whether it changes the
   recommendation.
5. **Answer asset.** Produce one `answer` asset under `assets/answer/<answer_id>/` containing:
   * the recommended path (one of a/b/c/d) and a one-sentence rationale,
   * the comparison table,
   * cost in USD (point estimate, not range — if a point estimate is impossible, document
     why),
   * validity-risk discussion (statistical power, provider-swap confound, missing-data bias),
   * comparability statement vs. t0027 (formal, not hand-wave),
   * concrete next-task suggestions that flow from the chosen path.

## Expected output

* Exactly one `answer` asset with `answer_id` derived from the chosen path (e.g.
  `no-anthropic-rq1-path-<a|b|c|d>`).
* `results/results_summary.md` whose first line is the headline label of the chosen path (e.g.
  `RQ1 PATH DECISION — OPTION (D): UNDERPOWERED, PROVIDER-BLOCKED STOP`).
* `results/results_detailed.md` with the comparison table embedded.
* `results/suggestions.json` with at most three follow-up suggestions tied to the chosen path
  (e.g. if (d): a suggestion to formally close t0029 and t0030 with a corrections-task status
  update).
* `results/costs.json` with `total_cost_usd: 0.00` (this task is analysis-only).
* `results/remote_machines_used.json: []`.

## Cost estimation

This task itself spends **$0.00** on paid APIs and provisions no remote machines. The
*outputs* of this task may recommend future spend; that recommendation must be costed at
USD-point-estimate granularity inside the answer asset, not deferred to a downstream
brainstorm.

## Comparability principle

The task **must** state, for each non-(a) option, whether the proposed rerun preserves
arm-labelling comparability with t0027/t0028. Specifically:

* (b) Local rerun: if a different policy plays arm A or arm B, the rerun is a *new
  experiment*, not a continuation of t0027. Any verdict must be reported as a verdict on the
  new policy, not on the original arm definitions.
* (c) Alternative provider: identical concern. Document the swap explicitly.
* (a) and (d): comparability is trivially preserved because no rerun happens.

## Risks & fallbacks

* If option (b) hinges on a model the project cannot actually run, fall back to (a) or (d).
* If option (c) requires a budget the project does not have (see `aggregate_costs`), fall back
  to (a) or (d).
* The task must not recommend a path that depends on Anthropic becoming available.

## Dependencies

* `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` (completed) — supplies the paired N=130
  baseline.
* `t0031_rq1_rq4_no_new_api_salvage` (completed) — supplies the re-derived discordance rate,
  RQ4 stratification, RQ1 power grid, and audit.

t0029 is **not** listed as a dependency: this task is the upstream that decides what happens
to t0029.

## Verification criteria

* Recommendation is exactly one of {(a), (b), (c), (d)} — not a hybrid, not a hedge.
* Cost is reported as a USD point estimate.
* Comparability with t0027 is stated explicitly for the chosen path.
* `verify_task_results`, `verify_suggestions`, and the `answer` asset verificator all pass.
* The recommendation does not assume Anthropic access becomes available at any point.

**Results summary:**

> **RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT**
>
> **Summary**
>
> Locked in **option (a) — existing-results-only verdict** as the recommended RQ1 execution
> path under
> the permanent no-Anthropic constraint. The t0031 re-derivation already yields the formal RQ1
> conclusion at $0 with arm-labelling comparability against t0027 / t0028 trivially preserved:
> 12 /
> 130 discordant pairs, symmetric 6 / 6 split, two-sided exact-binomial McNemar p =
> **1.0000**, with a
> real SWE-bench arm-B advantage and a marginal FrontierScience arm-A advantage that cancel in
> aggregate. Options (b), (c), and (d) were each rejected on a documented comparability or
> foreclosure
> basis; creative-thinking surfaced no non-obvious cost-saver that flips the recommendation.
>
> **Metrics**
>
> * **Aggregate McNemar p (N=130, t0031)**: **1.0000** (12 discordant; 6 a_only; 6 b_only)
> * **SWE-bench per-stratum cell**: b_only = **6**, a_only = **0** (n = 20; two-sided p =
>   **0.0312**)
> * **FrontierScience per-stratum cell**: a_only = **5**, b_only = **0** (n = 26; two-sided p
>   =
> **0.0625**)
> * **Tau-bench per-stratum cell**: 1 discordant of n = 84 (83 / 84 both-fail; two-sided p =
> **1.0000**)

</details>

<details>
<summary>✅ 0031 — <strong>RQ1/RQ4 no-new-API preliminary salvage on existing
t0026/t0027 outputs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_rq1_rq4_no_new_api_salvage` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-05-03T11:14:49Z |
| **End time** | 2026-05-03T11:47:30Z |
| **Step progress** | 9/15 |
| **Task page** | [RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Task folder** | [`t0031_rq1_rq4_no_new_api_salvage/`](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_detailed.md) |

# RQ1/RQ4 no-new-API preliminary salvage on existing t0026/t0027 outputs

This task runs strictly **no-new-API** preliminary analyses on already-paid-for outputs from
`t0026_phase2_abc_runtime_n147_for_rq1_rq5` and `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`.
It spends **$0.00** of new API budget. It does **not** replace
`t0029_rq1_discordance_rich_resample`, which remains the canonical source for the planned
McNemar verdict and resumes from its locked plan once an Anthropic API key becomes available.

* * *

## Motivation

`t0029_rq1_discordance_rich_resample` is currently `intervention_blocked` because the project
does not have an `ANTHROPIC_API_KEY` available, so the planned ~$35 paired resample cannot
run. Until a key is provisioned, no new RQ1 / RQ4 evidence can be collected through paired
sampling. However, the `t0026` and `t0027` runs already produced paired outputs (130 paired
instances in `t0027` across frontsci, taubench, and SWE-bench) plus extensive logs. Useful
preliminary evidence can be extracted from these existing artifacts at zero cost. This task
does that extraction in a tightly scoped, clearly-labelled way so that the project does not
stall while waiting on credentials, and so that when (or if) `t0029` resumes, its analysis
pipeline can build on a verified, audited baseline.

The four analyses below are the maximum that can be done responsibly without new sampling.
Anything beyond them — re-running models, embedding new texts, recomputing per-instance
metrics under a new prompt — requires new API spend and belongs to `t0029` or to a future
task. This task explicitly forbids scope creep into a `t0029` redesign.

* * *

## Research questions addressed

* **RQ1 (preliminary)**: Given the observed `t0027` discordance rate, what is the expected
  paired- discordant yield and McNemar power under the locked `t0029` budget cap, and under
  what scenarios is the planned cap likely to be informative versus underpowered?
* **RQ4 (preliminary)**: How does the discordance/concordance pattern between arm A
  (Plan-and-Solve baseline) and arm B (scope-aware ReAct) stratify by dataset (frontsci,
  taubench, SWE-bench) on the existing `t0027` outputs?

Both findings are explicitly **preliminary**. They cannot replace the McNemar verdict planned
in `t0029` because they reuse a fixed sample (130 paired instances) rather than the
discordance-rich resample that `t0029` is designed to draw.

* * *

## Scope — exactly four analyses, in this order

### Analysis 1 — preliminary RQ4 stratification on existing t0027 outputs

* Compute the joint table dataset × (concordance | discordance) × (arm A outcome × arm B
  outcome) over the 130 paired instances in `t0027`.
* Datasets to stratify by: `frontsci`, `taubench`, `SWE-bench`.
* Variant labelling: arm A = Plan-and-Solve baseline, arm B = scope-aware ReAct. This matches
  the `t0028` task description naming convention. The `t0027` predictions assets use the
  inverted `variant_a` / `variant_b` labels — handle the inversion in **one** load helper
  inside this task's code only. Do not propagate the inversion elsewhere; do not introduce a
  new convention.
* Report cell counts, marginal totals (concordance vs. discordance per dataset, arm A correct
  vs. arm B correct per dataset), and Wilson 95% CIs per cell where N permits (N >= 5 in the
  cell).
* Cells with N < 5 must be reported with the count but flagged as having no usable CI.
* Label every result in this analysis as **PRELIMINARY** because per-dataset cell counts will
  be small.

### Analysis 2 — RQ1 power / futility analysis using t0027's observed discordance rate

* Read the exact paired-discordance numerator and denominator from `t0027`'s actual `results/`
  files (e.g., `results_summary.md`, `results_detailed.md`, or the underlying predictions). Do
  **not** hardcode a 4.6% discordance rate — that figure came from a different earlier summary
  and is not the rate this analysis must use. The relevant rate is approximately 12 / 130 ≈
  9.2%, but the exact numerator and denominator are to be re-derived from `t0027` files.
* Under the `t0029` plan assumptions:
  * Hard $35 cap.
  * Approximately $0.16 per new paired instance.
  * `BATCH_SIZE = 8`.
  * Sampling order frontsci → taubench → SWE-bench, seed `20260503`.
* Compute:
  * The total number of paired instances the cap can buy in expectation (≈ 35 / 0.16 = 218,
    but derive precisely from the locked plan).
  * The expected number of discordant pairs at the observed rate.
  * McNemar exact-binomial power at that expected discordant count for plausible conditional
    "B-wins-given-discordant" rates: 0.55, 0.60, 0.65, 0.70, 0.75, 0.80.
  * A futility table: for each conditional B-wins rate, the minimum number of discordant pairs
    needed to reach 80% power at α = 0.05.
* Produce a **futility statement**: under what scenarios does the planned $35 cap have a
  meaningful chance of delivering an RQ1 verdict, and under what scenarios is the project
  better served by a different design. Do **not** prescribe the redesign; that belongs to a
  later brainstorm.

### Analysis 3 — audit of t0026 / t0027 logs distinguishing infrastructure failures from genuine model failures

* Walk `t0026` and `t0027` logs (`logs/`, `intervention/`, and `results/`) and classify each
  recorded failure into one of:
  * **(a) Infrastructure failure**: harness crash, parser error, cost-tracker double-count,
    retry storm, rate-limit, network timeout, or any failure mode that would have been fixed
    in `t0029`'s revised harness.
  * **(b) Genuine model failure**: the model produced an answer that scored as wrong on the
    task's metric.
* Produce a small table: per task, per dataset, count of (a) versus (b), with brief
  representative examples (one or two short quotes per category) drawn directly from the logs.
* Goal: tell us whether the `t0027` verdicts have been corrupted by infrastructure issues that
  would have been fixed in `t0029`'s harness, and therefore whether the `t0027` baseline is
  trustworthy as a reference for analyses 1 and 2.
* If meaningful infrastructure-failure contamination is detected, flag it explicitly in the
  report and qualify analyses 1 and 2 accordingly.

### Analysis 4 — short report

* Two output files:
  * `results/results_summary.md` — concise overview, key tables, headline labels.
  * `results/results_detailed.md` — full analyses with all derivations, charts, and per-cell
    tables.
* Headline label on the first line of `results/results_summary.md`: `NO-NEW-API PRELIMINARY
  EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* Include a clearly delimited `## Limitations` section listing every assumption and reason the
  evidence is preliminary, including:
  * The 130 paired instances are not a discordance-rich resample.
  * Per-cell N counts are small.
  * Power numbers depend on assumed conditional B-wins rates that are not yet observed.
  * Any infrastructure-failure contamination found in analysis 3.

* * *

## Approach

1. Implement a single load helper in `code/load_paired_outputs.py` that:
   * Reads `t0027` predictions assets.
   * Maps `variant_a` → arm B (scope-aware ReAct) and `variant_b` → arm A (Plan-and-Solve
     baseline) iff the inversion is confirmed by inspecting `t0027`'s task description and
     predictions metadata. Otherwise apply the inverse mapping. **Do not guess** — verify
     against `t0027`'s own files before locking the mapping in the helper.
   * Emits a single, internally-consistent paired DataFrame in arm-A / arm-B terms for
     downstream use.
2. `code/analysis_rq4_stratification.py` — analysis 1 implementation.
3. `code/analysis_rq1_power.py` — analysis 2 implementation, including the McNemar
   exact-binomial power computation.
4. `code/analysis_log_audit.py` — analysis 3 log walk and classification.
5. `code/build_report.py` — emits both report files into `results/` and saves all charts to
   `results/images/`.
6. All scripts are wrapped via `uv run python -m arf.scripts.utils.run_with_logs` per project
   rule 1; each major step gets its own log entry under `logs/`.

* * *

## Constraints

* **Zero API spend.** No paid LLM calls. No embedding calls. No vast.ai. The plan's cost
  estimate must be `$0.00`. `costs.json` must reflect zero third-party costs.
* **Local CPU only.** No remote machines. The `setup-machines` and `destroy-machines` stages
  are not applicable.
* **Read-only consumption** of `t0026`, `t0027`, and `t0029` outputs. No writes outside this
  task folder. No edits to other task folders. Top-level tooling files (`pyproject.toml`,
  `uv.lock`, `ruff.toml`, `.gitignore`) may change only if a new local-only dependency is
  genuinely needed — this task should not require any.
* **Single variant-labelling convention.** Reuse the `t0028` task-description naming (arm A =
  baseline, arm B = scope-aware) throughout all task-internal code, charts, and report tables.
  The `t0027` `variant_a` / `variant_b` inversion is isolated in `code/load_paired_outputs.py`
  only.
* **No spawning of follow-up tasks** from within `t0031`. Any follow-up redesign ideas go in
  `results/suggestions.json` only and are picked up by a later brainstorm.
* **Bounded scope.** The four analyses defined above are the entire scope. Do not expand into
  a full re-analysis of `t0026` / `t0027` or a `t0029` redesign.
* **Urgent but bounded.** The task is urgent in that it is the next thing the project should
  do, but every analysis must finish in well under a working day of agent time.

* * *

## Dependencies

* `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — completed; provides earlier paired outputs and
  logs. Read-only.
* `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` — completed; provides the 130 paired instances
  and logs that anchor analyses 1, 2, and 3.

`t0029_rq1_discordance_rich_resample` is **not** a dependency: it is `intervention_blocked`
and not yet completed, and `t0031` does not require its output. `t0031` explicitly does not
replace `t0029`.

* * *

## Compute and budget

* **API budget**: $0.00. No new model calls of any kind.
* **Compute**: local CPU only. Estimated wall-clock time: well under one hour for all four
  analyses combined, dominated by file I/O and small-N statistical computations.
* **No GPU**, no remote machines, no long-running jobs.

* * *

## Expected assets

`expected_assets`: `{}`. This is a pure analysis task. It produces no new datasets, models,
papers, libraries, predictions, or answers — only the report files in `results/` and
supporting code in `code/`.

* * *

## Output specification

* `code/load_paired_outputs.py` — the single load helper that reconciles `t0027`'s `variant_a`
  / `variant_b` inversion into arm A / arm B.
* `code/analysis_rq4_stratification.py` — analysis 1.
* `code/analysis_rq1_power.py` — analysis 2 (includes McNemar exact-binomial power).
* `code/analysis_log_audit.py` — analysis 3.
* `code/build_report.py` — analysis 4, emits the report files.
* `results/results_summary.md` — concise overview. Headline first line: `NO-NEW-API
  PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`. Includes the per-dataset RQ4 joint
  table, the RQ1 power / futility headline, the log-audit headline, and the `## Limitations`
  section.
* `results/results_detailed.md` — full analyses with all derivations, per-cell tables with
  Wilson 95% CIs, the full power table across plausible conditional B-wins rates, and the full
  log-audit classification.
* `results/images/` — charts referenced by `results_detailed.md`. Required charts:
  1. `rq4_stratification_heatmap.png` — dataset × outcome combination heatmap with cell
     counts. Question answered: where do discordant pairs concentrate?
  2. `rq1_power_curve.png` — McNemar power as a function of expected discordant count, one
     curve per conditional B-wins rate. Question answered: at what discordant-pair count does
     the planned cap deliver 80% power?
  3. `log_audit_failure_breakdown.png` — stacked bars per task per dataset showing
     infrastructure-failure vs. genuine-model-failure counts. Question answered: are `t0027`'s
     verdicts contaminated by infrastructure issues?
* `results/metrics.json` — registered metrics (`task_success_rate`,
  `overconfident_error_rate`, `avg_decisions_per_task`) computed only where they can be
  derived without new API calls; if a metric is not derivable from existing outputs, set its
  value to `null` with an explanatory note.
* `results/costs.json` — total `0.00` USD across all services.
* `results/suggestions.json` — follow-up suggestions only (e.g., "redesign `t0029` cap given
  the futility analysis"). No work is spawned from `t0031`.
* `results/remote_machines_used.json` — empty (no remote machines used).

All charts must be embedded into `results_detailed.md` with markdown image links and short
captions that name the question they answer.

* * *

## Key questions (numbered, falsifiable)

1. **Q1 (RQ4)**: Does the per-dataset stratified joint table show discordance concentrated in
   any one of {frontsci, taubench, SWE-bench}, with at least one cell having a Wilson 95% CI
   that does not overlap the across-dataset average? **Falsifiable**: if every dataset's
   discordance fraction sits inside the across-dataset CI, the answer is no.
2. **Q2 (RQ1 power)**: At the observed `t0027` discordance rate and the locked $35 cap, is the
   expected discordant-pair count high enough to give 80% McNemar power at conditional B-wins
   rate ≥ 0.65? **Falsifiable**: if the expected discordant count falls below the 80%-power
   threshold for every conditional B-wins rate < 0.75, the answer is no, and the futility
   statement must say so explicitly.
3. **Q3 (RQ1 futility)**: Is there a conditional B-wins rate at or above which the planned cap
   can deliver 80% power, and is that rate plausible given `t0027`'s observed paired outcomes?
   **Falsifiable**: yes / no with a numeric threshold and a one-sentence justification
   grounded in the `t0027` joint table.
4. **Q4 (log audit)**: Do infrastructure failures account for less than 10% of `t0027`'s
   failed instances per dataset? **Falsifiable**: if any dataset has >= 10%
   infrastructure-failure share, the `t0027` baseline must be flagged as contaminated and
   analyses 1 and 2 must carry that qualification through to `results_summary.md`.

* * *

## Verification criteria

* `results/results_summary.md` exists and its first non-empty line is exactly `NO-NEW-API
  PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* `results/results_summary.md` contains a `## Limitations` section.
* `results/results_detailed.md` exists, embeds all three required charts, and contains the
  full per-cell tables with Wilson 95% CIs.
* `results/costs.json` shows `0.00` USD total cost across all services.
* `results/remote_machines_used.json` is empty.
* No files outside `tasks/t0031_rq1_rq4_no_new_api_salvage/` are modified.
* The variant-labelling helper in `code/load_paired_outputs.py` is the **only** place where
  the `t0027` `variant_a` / `variant_b` inversion is handled.
* All four analyses are present and clearly labelled in both report files.
* All charts are saved under `results/images/` and embedded in `results_detailed.md`.

* * *

## Risks and fallbacks

* **Risk**: the inversion of `variant_a` / `variant_b` between `t0027` predictions and `t0028`
  task description is not as expected. **Fallback**: confirm the mapping by reading both files
  before locking the helper; if ambiguity remains, write an `intervention/` file rather than
  guessing.
* **Risk**: per-cell counts in the RQ4 stratification are too small to compute meaningful CIs.
  **Fallback**: report counts only and flag the cell as N < 5; do not invent a CI.
* **Risk**: the McNemar exact-binomial power computation is sensitive to the assumed
  conditional B-wins rate. **Fallback**: report a full grid of conditional B-wins rates rather
  than a single point estimate, and let the futility statement quantify uncertainty.
* **Risk**: log audit reveals so much infrastructure contamination that analyses 1 and 2 are
  effectively unusable. **Fallback**: the report must say so explicitly in `## Limitations`
  and in the headline summary; this is itself a useful preliminary finding.

* * *

## Cross-references

* Prior tasks whose results this task consumes: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`,
  `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`.
* Locked plan this task references but does not run: `t0029_rq1_discordance_rich_resample`.
* Naming convention this task follows: `t0028_brainstorm_results_8` task description (arm A =
  baseline, arm B = scope-aware).
* Source suggestion: none. This task was created by direct user instruction during a session
  in which `t0029` was `intervention_blocked`. It is not derived from a brainstorm suggestion.

**Results summary:**

> NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029
>
> **RQ1/RQ4 No-New-API Preliminary Salvage**
>
> This task spends **$0.00** of new API budget. It runs four bounded analyses on the
> already-on-disk
> outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
> `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`. The labelled-arm convention follows `t0028`:
> arm A =
> Plan-and-Solve baseline, arm B = scope-aware ReAct, arm C = matched-mismatch.
>
> **Summary**
>
> Re-derived the t0027 paired discordance rate at **12/130 = 9.23%** (symmetric: 6 arm-A wins
> vs 6
> arm-B wins, McNemar two-sided p = 1.0000). Stratified RQ4 shows discordance is concentrated
> in
> opposite directions on SWE-bench (6/20 arm-B wins) and FrontierScience (5/26 arm-A wins).
> Under the
> locked t0029 plan ($35 cap, ~$0.16/pair → ~218 admittable new pairs, ≈ 32 expected
> discordant at the
> t0027 rate) RQ1 reaches **80% power only when the conditional B-wins rate p1 ≥ 0.75**. The
> infrastructure-vs-genuine-failure audit confirms zero MalformedPlanError post-fix in t0027
> but flags
> 22% (arm A) and 25% (arm C) of paired rows as parser-recovery `unknown` (cost-tracker
> boundary noise
> that does not affect the discordance signal). This task does not replace t0029; it only
> narrows the
> prior over likely outcomes.

</details>

<details>
<summary>✅ 0028 — <strong>Brainstorm 8: close RQ1/RQ4 via discordance-rich resample
under $35 cap</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0028_brainstorm_results_8` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md), [`t0018_brainstorm_results_6`](../../../overview/tasks/task_pages/t0018_brainstorm_results_6.md), [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md), [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md), [`t0024_brainstorm_results_7`](../../../overview/tasks/task_pages/t0024_brainstorm_results_7.md), [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md), [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-03T08:30:00Z |
| **End time** | 2026-05-03T09:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm 8: close RQ1/RQ4 via discordance-rich resample under $35 cap](../../../overview/tasks/task_pages/t0028_brainstorm_results_8.md) |
| **Task folder** | [`t0028_brainstorm_results_8/`](../../../tasks/t0028_brainstorm_results_8/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0028_brainstorm_results_8/results/results_detailed.md) |

# Brainstorm Session 8: Close RQ1/RQ4 with Discordance-Rich Resample

## Context

Following t0024 (brainstorm 7), three substantive tasks ran:

* **t0025** literature survey synthesized RQ1-RQ5 status from 10 papers; flagged that direct
  runtime ABC evidence was missing.
* **t0026** Phase 2 ABC at N=147 produced first runtime data but ran $38.61 (over budget) and
  surfaced fault-tolerance bugs in arm B and a structurally-weak C wrapper.
* **t0027** Phase 2.5 ABC re-ran on N=130 paired instances with a fault-tolerant B and revised
  C. Headline: A=B=6 successes (4.62%), C=7 (5.38%). McNemar 6 vs 6 discordant pairs p=1.0
  (RQ1); 4 vs 5 discordant pairs p=1.0 (RQ5). ECE B=0.336, C=0.374 (still floored by all-100
  confidence).

## RQ Status After t0027

* **RQ1** (granularity → success): underpowered. 12 discordant pairs total; need ≥30 for a
  verdict.
* **RQ2** (overconfident error rate): blocked by template floor; needs content-driven
  calibrator + A confidence emission.
* **RQ3** (execute-now vs request-info): not operationalized; no decision field in agent
  output.
* **RQ4** (info-asymmetric gain concentration): underpowered; analysis-only follow-up on
  TaskA.
* **RQ5** (scope-mismatched strict-worse): counter-direction (C ≥ B) on small N; C wrapper not
  structurally distinct enough.

Remaining budget: **$66.54**.

## Decisions

This session schedules a minimum viable wave to close RQ1 and RQ4.

### New tasks

1. **t0029 TaskA — Discordance-rich paired resample for RQ1**
   * Hard cap: **$35**.
   * Goal: ≥30 discordant pairs across A vs B for a McNemar verdict on RQ1.
   * Abort rule: if the cap is hit before reaching 30 discordant pairs, stop and report a
     partial verdict with a power caveat. Do not launch replacement tasks in this wave.
   * Source suggestion: S-0025-04. Covers: S-0027-05.

2. **t0030 TaskE — RQ4 info-asymmetry stratification analysis**
   * Zero API cost (analysis on TaskA outputs).
   * Goal: stratify TaskA paired sample by subset (swebench / taubench / frontsci) and by
     concordance to test whether granularity gains concentrate where information asymmetry is
     highest.
   * Dependency: t0029.

### Suggestion cleanup

* **Reject as duplicate**: S-0026-02 (duplicate of S-0027-02).
* **Reject as obsolete**: S-0025-01 (pre-Phase-2 sampling proposal superseded by t0029).
* **Demote HIGH → MEDIUM**: S-0027-01 (calibrator), S-0027-02 (C structural rebuild) —
  deferred to next wave but still load-bearing.
* **Demote HIGH → LOW**: S-0020-01, S-0021-02, S-0022-02, S-0022-05 — pre-Phase-2 hypotheses
  superseded by direct runtime evidence in t0026/t0027.
* **Mark covered**: S-0025-04 (t0029 source), S-0027-05 (t0029 covers).

### Tasks not in this wave

TaskB (calibrator), TaskC (C structural rebuild), TaskD (RQ3 instrumentation) were proposed
but deferred. The guardrail explicitly forbids launching them as replacements if t0029 hits
the cap before reaching 30 discordant pairs — preserve the budget for the next session.

## Expected Outputs

* Two new task scaffolds (t0029, t0030) at status `not_started`.
* Eight correction files in `corrections/` reflecting the suggestion cleanup above.
* Updated overview after merge.

No paid external services are used by this brainstorm task itself.

**Results summary:**

> **Brainstorm Session 8 — Results Summary**
>
> **Summary**
>
> Scheduled a minimum viable wave to close RQ1 and RQ4 within the $66.54 remaining budget
> after
> t0027's underpowered McNemar verdicts (12 discordant pairs, p=1.0). Created t0029
> (`rq1_discordance_rich_resample`, hard $35 cap, abort on cap with partial verdict) and t0030
> (`rq4_info_asymmetry_stratification`, zero-API analysis on t0029 outputs). Eight suggestions
> corrected (2 rejected, 6 demoted). No RQ answered in this session.
>
> **Headline Decisions**
>
> * Created **t0029** (`rq1_discordance_rich_resample`) with hard $35 cap. Goal: reach >=30
>   discordant
> A vs B pairs for an RQ1 McNemar verdict. Abort rule: if cap is hit before 30 discordant
> pairs,
> halt API calls and report partial RQ1 verdict with explicit power caveat. No in-wave
> replacement
> task launched on cap. Source suggestion: S-0025-04. Covers: S-0027-05.
> * Created **t0030** (`rq4_info_asymmetry_stratification`) as zero-API-cost stratification
>   analysis
> on t0029's predictions. Goal: test whether granularity gain rate concentrates in high
> info-asymmetry strata per subset. Dependency: t0029.
> * Deferred **TaskB** (RQ2 calibrator), **TaskC** (RQ5 C structural rebuild), **TaskD** (RQ3

</details>

<details>
<summary>✅ 0027 — <strong>Phase 2.5 A/B/C re-run with fault-tolerant B and
structurally-distinct C</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` |
| **Status** | completed |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Expected assets** | 2 library, 3 predictions |
| **Source suggestion** | `S-0026-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/), [`experiment-run`](../../../meta/task_types/experiment-run/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-05-02T17:07:16Z |
| **End time** | 2026-05-03T08:07:00Z |
| **Step progress** | 9/15 |
| **Key metrics** | Task Success Rate: **0.05384615384615385** |
| **Task page** | [Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Task folder** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c/`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md) |

# Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

## Motivation

t0026 ran A/B/C on 130 paired instances and surfaced two structural defects that prevented
clean RQ1 (A vs B) and RQ5 (C vs both) answers:

* **B's plan parser is brittle.** 16 of 130 paired runs (12%) collapsed to
  `MalformedPlanError`, and zero of 20 SWE-bench instances succeeded for B. The A vs B paired
  McNemar came out symmetric — but the symmetry is dominated by parser failures, not by a real
  null effect on task success. **RQ1 is therefore unanswered.**

* **C is structurally A-with-noise, not B-with-extra-degradation.** The matched-mismatch
  wrapper delegates to `scope_aware_react` with a perturbed strategy label rather than to
  `plan_and_solve_v2`. C beat B (paired McNemar p = 0.019), which mechanically rejects the RQ5
  hypothesis ("C strictly worse than both A and B") — but the rejection is an artefact of C
  inheriting A's scaffold. **RQ5 is therefore mechanically rejected for the wrong reason.**

This task fixes both defects and re-runs A/B/C on the same 130 paired instances so the McNemar
tests measure the intended hypotheses. Source suggestions: **S-0026-01** (parser fix) and
**S-0026-02** (wrapper redesign).

## Questions Re-asked

* **RQ1:** Does scope-aware ReAct (A) achieve a higher paired task-success rate than
  scope-unaware Plan-and-Solve (B), once B's parser no longer collapses on noisy plans?
* **RQ5:** Is the matched-mismatch variant (C) strictly worse than both A and B, once C's
  scaffold is `plan_and_solve_v2` rather than `scope_aware_react`?

RQ2-RQ4 are not re-run in this task (RQ2 is calibration-scope-limited, RQ3 measured the wrong
metric, RQ4's premise was unmet). They are deferred.

## Approach

The task produces two new library assets and three new predictions assets, then runs the same
McNemar pipeline t0026 used.

### Step 1 — Library: `plan_and_solve_v3` (S-0026-01)

* Fork `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/plan_and_solve_v2.py` into a
  new library asset under this task's `assets/library/plan_and_solve_v3/`.
* Add a re-prompt-on-parse-failure path: when the planner returns a string that fails the plan
  regex, call the model once more with an explicit error message and a stricter format
  reminder.
* Add a structured-output / tool-calling fallback: if the second attempt also fails, switch to
  Anthropic's structured-output mode (or an equivalent JSON-mode path) to force a parseable
  plan.
* The fallback chain is bounded: at most one re-prompt and one structured-output attempt, then
  the trajectory records `MalformedPlanError` as today (so we can still measure residual
  parser-failure rate).
* Preserve all existing v2 behaviour: same plan schema, same `final_confidence` field, same
  `decision_log` shape. The only change is the parser robustness path.

**Acceptance gate:** on the same 130 paired instances, fewer than 3 trajectories fail with
`MalformedPlanError` (down from 16). If the gate is missed, document the residual cause in the
results before proceeding to Step 3.

### Step 2 — Library: `matched_mismatch_v2` (S-0026-02)

* Fork `tasks/t0010_matched_mismatch_library/code/` into a new library asset under
  `assets/library/matched_mismatch_v2/`.
* Replace the `scope_aware_react` delegation target with `plan_and_solve_v3`.
* Keep the same adversarial perturbation logic (deliberately wrong granularity tags); only the
  inner agent changes.
* The new library exports a single entry point used by the harness: it accepts the same
  per-instance config as t0010 and returns a trajectory with the same shape as B.

**Acceptance gate:** on a 5-instance smoke from the FrontierScience subset, C now produces
trajectories with the `plan_and_solve_v3` decision_log shape (not the ReAct shape). Verified
by inspecting one trajectory file per instance.

### Step 3 — Re-run A/B/C on the 130 paired instances

* Reuse `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` as the
  paired manifest. Same 130 instances, same provider (Anthropic), same model
  (`claude-sonnet-4-6` — matches what t0026 actually ran; the original task description
  erroneously said `claude-opus-4-7`), same per-instance budget caps.
* **A is not re-run.** t0026's A trajectories are valid for this paired analysis. We re-use
  them by reference (predictions asset id from t0026) rather than re-generating.
* **B and C are re-run** with the new libraries. Each produces a fresh predictions asset under
  this task's `assets/predictions/`.
* Resumable trajectory checkpointing as in t0026.

### Step 4 — Paired McNemar

* Compute paired McNemar exact-binomial for A (t0026) vs B (re-run) and B (re-run) vs C
  (re-run) on the 130 paired set.
* Bonferroni α = 0.025 across the two tests.
* Report effect direction, p-value, and the per-subset breakdown (SWE-bench / Tau-bench /
  FrontierScience). The same per-subset table style as t0026.

### Step 5 — Calibration (variant B and C only)

* Re-compute Xiong2024 verbalized-confidence + 3-sample self-consistency on the new B and C
  trajectories. A's calibration values are taken from t0026.
* Report `overconfident_error_rate` per variant.

## Expected Assets

* 2 library assets:
  * `assets/library/plan_and_solve_v3/` — fault-tolerant parser variant of t0021
  * `assets/library/matched_mismatch_v2/` — wrapper that delegates to `plan_and_solve_v3`
* 3 predictions assets:
  * `assets/predictions/abc_rerun_a_reused/` — pointer to t0026's A predictions (no re-run)
  * `assets/predictions/abc_rerun_b/` — fresh B trajectories on the 130 paired set
  * `assets/predictions/abc_rerun_c/` — fresh C trajectories on the 130 paired set

## Compute and Budget

| Item | Estimate |
| --- | --- |
| B re-run, 130 instances, claude-sonnet-4-6 | $7-10 |
| C re-run, 130 instances, claude-sonnet-4-6 | $7-10 |
| A re-use (no re-run) | $0 |
| Calibration self-consistency (3 samples × B + C) | $3-5 |
| Plan-parser repro / smoke / overhead | $2-3 |
| **Total** | **$19-28** |

Cap at $50. Project budget remaining at the end of t0026: ~$109. No GPUs, no remote machines,
single Anthropic provider.

## Registered Metrics Used

Same as t0026 — only registered keys reported in `metrics.json`:

* `task_success_rate`
* `avg_decisions_per_task`
* `overconfident_error_rate` (B and C only)

McNemar p-values, paired contingency tables, and per-subset breakdowns live in
`data/mcnemar_results.json` and `data/calibration.json`, not in `metrics.json`.

## Charts

Embedded in `results/results_detailed.md`:

1. Paired contingency tables A-vs-B and B-vs-C (heatmap).
2. Per-subset task-success-rate bar chart for A / B / C.
3. Parser-failure-rate bar chart B-old (t0026) vs B-new (this task) — visualises the
   acceptance gate from Step 1.
4. `overconfident_error_rate` bar chart B / C with 95% CIs.

All saved to `results/images/` and embedded with `![desc](images/file.png)` syntax.

## Verification Criteria

* Steps 1 and 2 acceptance gates pass (<3 `MalformedPlanError`; C trajectories use
  `plan_and_solve_v3` shape).
* Paired McNemar A-vs-B and B-vs-C are reported with effect direction, p-value, and the
  Bonferroni decision.
* Each of the four design areas (RQ1, RQ5, calibration, parser robustness) has a one-sentence
  conclusion in `results/results_summary.md`.
* `verify_task_metrics.py`, `verify_task_results.py`, and `verify_pr_premerge.py` all pass
  with no errors.

## Risks and Fallbacks

* **Parser fix doesn't fully close the failure gap.** If `MalformedPlanError` rate stays >3,
  the symmetric A-vs-B McNemar may persist. We accept that outcome and document it as a real
  result rather than re-engineering further. RQ1 then becomes "answered: no detectable
  difference even after parser fix."
* **C-on-plan-and-solve flips direction unexpectedly.** If C-new beats B again, that is a
  finding — but the mechanism is now real (perturbed granularity tags on a planning scaffold
  rather than a delegation accident). Report and discuss.
* **Cost overrun.** If the B or C re-run exceeds the per-stream budget by >25%, stop the
  stream, truncate to whatever paired set was completed, and re-run the McNemar on the
  truncated set with explicit N reported.

## Cross-References

* Source suggestions: **S-0026-01** (parser fix), **S-0026-02** (wrapper redesign). Both
  high-priority active suggestions from t0026.
* Source task: `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — paired manifest reused, A
  predictions reused.
* Library dependencies: `t0010_matched_mismatch_library` (forked into v2),
  `t0021_plan_and_solve_v2_with_final_confidence` (forked into v3).

**Results summary:**

> **Results Summary — t0027 Phase 2.5 A/B/C re-run**
>
> **Summary**
>
> Forked t0021's plan-and-solve v2 into a fault-tolerant `plan_and_solve_v3` (bounded
> 3-attempt
> plan-parse recovery) and t0010's mismatch wrapper into `matched_mismatch_v2` (now delegating
> to v3),
> re-ran B and C on t0026's 130 paired instances under claude-sonnet-4-6, and recomputed
> paired
> McNemar (Bonferroni α=0.025) for RQ1 (A vs B) and RQ5 (B vs C) plus 10-bin ECE calibration.
> Both
> McNemar tests are **do_not_reject** under Bonferroni; parser-failure rate is **0.0** for
> both
> variants (down from t0026's B=12%). Total task spend was **$20.7631** (cap $50).
>
> **Metrics**
>
> * **Variant A (reused from t0026)** — task_success_rate = **0.0462** (6/130)
> * **Variant B (plan_and_solve_v3)** — task_success_rate = **0.0462** (6/130),
> overconfident_error_rate = **0.0588**, ECE = **0.336**
> * **Variant C (mismatch over v3)** — task_success_rate = **0.0538** (7/130),
> overconfident_error_rate = **0.143**, ECE = **0.374**
> * **RQ1 paired McNemar (A vs B)** — discordant 6/6, p = **1.0**, do_not_reject (α=0.025)
> * **RQ5 paired McNemar (B vs C)** — discordant 4/5, p = **1.0**, do_not_reject (α=0.025)

</details>

<details>
<summary>✅ 0026 — <strong>Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0026_phase2_abc_runtime_n147_for_rq1_rq5` |
| **Status** | completed |
| **Effective date** | 2026-05-02 |
| **Dependencies** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Expected assets** | 3 predictions |
| **Source suggestion** | — |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-05-02T06:34:50Z |
| **End time** | 2026-05-02T14:50:45Z |
| **Step progress** | 11/15 |
| **Key metrics** | Task Success Rate: **0.11564625850340136** |
| **Task page** | [Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Task folder** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5/`](../../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/results_detailed.md) |

# Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5

## Motivation

The t0025 synthesis answered RQ1-RQ5 using only external literature (the t0017 paper corpus).
It explicitly flagged that there is **zero project-internal runtime evidence** behind those
answers. The t0023 confirmatory ABC run (N>=157) was cancelled after t0019 surfaced a
haiku-judge calibration failure that would have invalidated outcomes.

This task closes that gap with a properly powered, paired A/B/C run on N=147 instances
spanning all three runnable benchmark subsets (SWE-bench Verified, Tau-bench,
FrontierScience). The design produces project-internal evidence for **RQ1, RQ2, RQ3, RQ4** and
a properly powered McNemar paired test for **RQ5**. Total budget envelope: ~$125, hard cap
$135.

## Research Questions Targeted

* **RQ1** — Does scope-aware ReAct (variant A) outperform a scope-unaware Plan-and-Solve
  baseline (variant B) on success rate? Tested by paired McNemar across the full N=147.
* **RQ2** — Does mismatched-scope (variant C) underperform A on the same instances? Tested by
  paired McNemar across N=147.
* **RQ3** — How well does a sonnet judge agree with programmatic ground truth on benchmark
  items that have one (SWE-bench tests, FrontierScience exact-match)?
* **RQ4** — What is the calibration (ECE) of the verbalized `final_confidence` field emitted
  by the v2 Plan-and-Solve harness?
* **RQ5** — Does the strict double inequality `success(A) > success(B) > success(C)` hold? At
  N=147 with paired binary outcomes, McNemar can detect ~10 percentage-point pairwise gaps
  with alpha=0.025 each (Bonferroni-corrected for the two pairwise tests). Both `success(A) >
  success(B)` and `success(B) > success(C)` must reach significance for RQ5 to be affirmed.

## Scope and Configurations

Three variants, one model under test, one judge per pass with an inter-judge slice.

* **Variant A (scope-aware ReAct)** — uses the library produced by
  `t0006_scope_aware_react_library`. Each step receives the explicit scope description from
  the benchmark item.

* **Variant B (scope-unaware Plan-and-Solve v2)** — uses the library produced by
  `t0021_plan_and_solve_v2_with_final_confidence`. Plans the full solution, executes, emits
  `final_confidence` at the end of every action.

* **Variant C (mismatched-scope ReAct)** — uses the library produced by
  `t0010_matched_mismatch_library` to deliberately feed the wrong scope description. Same step
  structure as A.

* **Model under test (all variants)**: `claude-sonnet-4-6`. No haiku model under test in this
  run — RQ4 calibration must be cleanly attributable to verbalized confidence, not to a
  model-skill confound.

* **Judge**: `claude-sonnet-4-6` for the primary pass on every instance. `claude-opus-4-7`
  runs the same pass on a 30-instance overlap slice (10 from each benchmark) for inter-judge
  agreement. Programmatic ground truth is used wherever the benchmark provides it (SWE-bench
  tests, FrontierScience exact-answer match). Tau-bench has weaker programmatic ground truth
  and relies on judge plus tool-trace heuristics. **No haiku judge** — this is the t0019
  finding, encoded as a constraint on this task.

* **Confidence elicitation**: every action emits a numeric `final_confidence in [0, 1]` via
  the v2 harness. Variants A and C also emit a per-step confidence using the same field
  convention.

## Benchmark Slice (N=147)

Composite of N=147 instances drawn from already-downloaded subsets registered in
`t0003_download_benchmark_subsets`. WorkArena++ is excluded (no enumerable instances; requires
gated ServiceNow + HuggingFace access).

* 20 from SWE-bench Verified subset (out of 60 available; programmatic judging via test
  execution)
* 87 from Tau-bench subset (full subset; tool-trace plus judge)
* 40 from FrontierScience olympiad subset (full subset; programmatic exact-answer match)

Instance selection is reproducible — the planning step records the seed, the source manifest,
and the per-source instance IDs in `data/instance_manifest.json`. The 20 SWE-bench instances
are sampled with stratification across the difficulty buckets in the upstream subset. Each
variant runs on the *same* 147 instances (paired design).

## Metrics (computed for every variant)

* `success_rate` — fraction passing the programmatic check (or judge for items without one)
* `progress_rate` — AgentBoard subgoal progress rate via t0022 (where applicable; tau-bench
  and FrontierScience are single-step so this metric is reported only on SWE-bench)
* `eai_error_breakdown` — counts per Embodied Agent Interface error category via t0022
* `final_confidence_ece` — Expected Calibration Error of `final_confidence` against
  per-instance outcomes
* `judge_agreement_with_program` — agreement rate between sonnet judge and programmatic ground
  truth on items that have both (SWE-bench, FrontierScience)
* `inter_judge_agreement` — sonnet vs opus on the 30-instance overlap slice
* `mcnemar_p_a_vs_b` — paired McNemar p-value for `success(A) > success(B)`
* `mcnemar_p_b_vs_c` — paired McNemar p-value for `success(B) > success(C)`
* Efficiency: `efficiency_inference_time_per_item_seconds`,
  `efficiency_inference_cost_per_item_usd`

All metric keys must be registered in `meta/metrics/` before reporting; check with `uv run
python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and add any missing keys
via `/add-metric` during planning.

## Data Handling

* Intermediate artifacts (per-instance traces, per-action JSON, raw judge prompts and
  responses) saved under `data/runs/{variant}/`.
* The fixed N=147 slice is saved as `data/instance_manifest.json` with explicit seed, source
  IDs, and source dataset hashes — required for reproducibility.
* Predictions assets (one per variant) created under `assets/predictions/{variant}/`
  containing the per-instance predictions, confidence values, success labels, and judge
  responses.

## Compute and Budget

Local-only — no remote machines. All runs hit the Anthropic API directly.

Per-variant cost estimate (sonnet 4.6 agent + sonnet 4.6 judge):

* SWE-bench (20 instances × ~$0.85/instance) ≈ $17 per variant
* Tau-bench (87 instances × ~$0.20/instance) ≈ $17.40 per variant
* FrontierScience (40 instances × ~$0.18/instance) ≈ $7.20 per variant
* Per-variant subtotal: ~$41.60
* Three variants subtotal: ~$125
* Inter-judge slice (opus 4.7 on 30 items): ~$5
* Buffer for retries: ~$5

Total: **about $135 estimated, $145 hard cap**. Current project budget is $200 with $74.08
already spent, leaving $125.92 — the hard cap fits with $0-20 of slack. The planning step must
re-estimate on real prompt-token measurements before launching the full run; if measurements
indicate the cap will be breached, the SWE-bench slice is the first thing to shrink.

## Key Questions and Falsifiability

1. Is `success(A) > success(B)` significantly at alpha=0.025 (Bonferroni)? Falsifiable: if the
   McNemar test fails to reject, RQ1's project answer becomes "not supported by N=147
   evidence."
2. Is `success(B) > success(C)` significantly at alpha=0.025? Falsifiable: if the test fails
   to reject, RQ2 (and RQ5) flip.
3. Does sonnet judge agree with programmatic ground truth at >=90%? Falsifiable: if agreement
   is under 80%, RQ3 reports "judge unreliable even at sonnet."
4. Is ECE on `final_confidence` under 0.15? Falsifiable: if ECE >= 0.20, RQ4 reports
   "verbalized confidence not calibrated at this scale."
5. Strict double inequality `success(A) > success(B) > success(C)`: affirmed only if both
   pairwise tests in (1) and (2) are significant; otherwise reported as direction-only or
   refuted.

## Outputs

* `assets/predictions/{a_scope_aware,b_plan_and_solve,c_mismatched}/` — three predictions
  assets
* `results/results_summary.md` — high-level findings against each RQ, with explicit pass/fail
  per falsifiability question
* `results/results_detailed.md` — per-variant tables, per-benchmark breakdowns, reliability
  diagram, EAI error taxonomy table, McNemar contingency tables
* `results/metrics.json` — flat or multi-variant metric record covering every metric listed
  above
* `results/images/` — at minimum: success_rate_by_variant.png, success_rate_by_benchmark.png,
  ece_reliability_diagram.png, judge_agreement.png, eai_error_breakdown.png

## Cross-References

* **Source motivation**: t0024 brainstorm session 7 (rescope after t0019 calibration finding)
  and t0025 synthesis flagging zero internal evidence for RQ1-RQ5.
* **Replaces (smaller-N)**: t0023_phase2_abc_confirmatory_sonnet_swebench (cancelled).
* **Calibration baseline**: t0019_v2_judge_calibration_sonnet — informs the "no haiku judge"
  constraint on this run.
* **Harness reliability**: t0020_v2_truncation_vs_schema_ablation — informs the prompt-schema
  and truncation choices used by the harness.

**Results summary:**

> **t0026 Phase 2 A/B/C Runtime — Results Summary**
>
> **Summary**
>
> The strict double inequality `success(A) > success(B) > success(C)` posited by RQ5 is **not
> supported**. On the paired N=130 set (the same 130 instances run by every variant), variants
> A and B
> are statistically tied, and the adversarial-mismatched variant C significantly outperforms
> B. The
> sweep ran the full A/B/C × {SWE-bench, Tau-bench, FrontierScience} grid against
> `claude-sonnet-4-6`
> with a paired McNemar test on each pair, an Expected Calibration Error on variant B's
> verbalized
> `final_confidence`, and a sonnet/opus inter-judge agreement check. RQ3 (judge ↔
> program-truth
> agreement) and RQ4 (B's calibration) are answered cleanly. RQ1, RQ2, RQ5 are rejected by the
> data.
>
> | Pair | discordant (1st-only) | discordant (2nd-only) | McNemar p | Bonferroni alpha |
> | --- | --- | --- | --- | --- |
> | A vs B | 6 | 6 | 1.000 | 0.025 |
> | B vs C | 4 | 15 | **0.019** | 0.025 |
>
> Both pairwise tests must reach significance for RQ5 to be affirmed. A vs B fails (p ≈ 1.0).
> B vs C
> is significant in the *opposite* direction from RQ5: C beats B.
>

</details>

<details>
<summary>✅ 0025 — <strong>Synthesize Best-Available Answers to Research Questions
(RQ1-RQ5)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Start time** | 2026-05-01T21:10:07Z |
| **End time** | 2026-05-01T21:46:00Z |
| **Step progress** | 8/15 |
| **Task page** | [Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Task folder** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/results/results_detailed.md) |

# Synthesize Best-Available Answers to Research Questions (RQ1-RQ5)

## Motivation

This task was originally planned as a 10-paper literature survey of 2024-2026 work on
hierarchical agents and LLM-as-judge methodology. During implementation prestep, an
`aggregate_papers` check found that **all 10 target papers were already added to the project
under `t0017_literature_hierarchical_agents_and_judges`**. The `add-paper` skill's
duplicate-stop rule forbids re-adding any of them.

The intervention file `intervention/duplicate_papers.md` documents the conflict and three
resolution options. The researcher chose to drop the asset-addition half of the task entirely
and pivot the remaining work to **answering the project's five Research Questions directly**,
using the existing 10 paper summaries plus prior project findings from t0014, t0019, and t0020
as the evidence base.

## Scope

Produce a synthesis structured around the project's RQ1-RQ5:

* **RQ1**. Does explicit granularity conditioning yield higher final task success than an
  otherwise identical scope-unaware agent on the composite benchmark?
* **RQ2**. Does explicit granularity conditioning reduce the overconfident error rate, i.e.
  the fraction of incorrect actions taken with high confidence?
* **RQ3**. On low-level tasks, does granularity conditioning improve accuracy in
  distinguishing "can execute now" from "must request information"?
* **RQ4**. Are gains concentrated in states where local execution requires information not
  needed for higher-level planning (sub-hypothesis 1)?
* **RQ5**. Do scope-mismatched agents perform strictly worse than both scope-aware and
  scope-unaware baselines (sub-hypothesis 2)?

For each RQ, the synthesis reports:
1. The current best answer the project can defend (verdict: **strong support**, **partial
   support**, **no direct evidence**, or **contradictory**), based on the union of the
   existing evidence base.
2. Specific evidence from the 10 t0017 papers, cited by `citation_key` and headline numbers.
3. Specific evidence from prior project tasks t0014, t0019, t0020 — paying particular
   attention that those tasks studied **annotation and judging** of hierarchical schemas, not
   the runtime A/B/C agent conditioning that RQ1-RQ5 directly target. Indirect signal is
   reported as such.
4. Residual uncertainty: which parts of the RQ remain open and what experimental evidence
   (Phase 2 A/B/C runs) would be needed to close them.

## Approach

1. Read all 10 paper summaries under
   `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md`.
2. Read prior task results:
   `tasks/t0014_v2_annotator_sonnet_rerun/results/results_summary.md`,
   `tasks/t0019_v2_judge_calibration_sonnet/results/results_summary.md`,
   `tasks/t0020_v2_truncation_vs_schema_ablation/results/results_summary.md`.
3. Cross-tabulate evidence by RQ.
4. Write `results/results_summary.md` with a one-paragraph verdict per RQ and a single
   comparison table at the end.
5. Write `results/results_detailed.md` with the full evidence per RQ: literature evidence
   section, prior-project-task evidence section, residual-uncertainty section, and a final
   "next-experiment design" subsection mapping uncertainty to candidate Phase 2 designs.

## Cost Estimation

Total: ~$0.50.

* No paper downloads, no `add-paper` invocations.
* One sub-agent reads 10 paper summaries and produces a structured evidence table (~$0.20).
* Synthesis writeup uses cached evidence; orchestrator-only (~$0.30).

## Expected Outputs

* `results/results_summary.md` — one paragraph per RQ, with a single end-of-document
  comparison table summarising verdicts and primary supporting citation keys.
* `results/results_detailed.md` — full per-RQ evidence sections plus next-experiment design
  candidates derived from the residual-uncertainty notes.
* No new asset folders.

## Dependencies

None. The synthesis reads only files in `tasks/t0017_*/`, `tasks/t0014_*/`, `tasks/t0019_*/`,
`tasks/t0020_*/`, and the project's `description.md`.

## Risks & Fallbacks

* Risk: the 10 t0017 paper summaries contain insufficient detail to ground a particular RQ
  verdict. Fallback: mark that RQ as **no direct evidence** and explicitly document what the
  closest analog from the literature does say.
* Risk: t0014/t0019/t0020 prior findings are conflated with RQ1-RQ5. Mitigation: those tasks
  studied annotation and judging, not the runtime agent under A/B/C conditioning. The
  synthesis must keep that distinction explicit.
* Risk: the synthesis produces an over-confident verdict where RQs require empirical Phase 2
  data the project has not yet collected. Mitigation: the **residual uncertainty** subsection
  per RQ is mandatory; verdicts are bounded by the evidence and explicitly downgraded where
  direct empirical measurements are missing.

## Time Estimation

~30-45 minutes of agent execution.

## Assets Needed

None.

## Expected Assets

None. The deliverable is the synthesis written to `results/`.

## Remote Machines

None.

## Verification Criteria

* `results/results_summary.md` contains a section for each of RQ1, RQ2, RQ3, RQ4, RQ5 with an
  explicit verdict label and primary supporting citations.
* `results/results_detailed.md` contains, for each RQ, both literature evidence and
  prior-project evidence sections, plus a residual-uncertainty subsection.
* `verify_task_results` passes with zero errors.
* `verify_logs` passes for all step folders.
* `verify_task_file` passes for the re-scoped `task.json`.
* `verify_pr_premerge` passes before merge.

## Categories

This task does not produce paper assets or other categorised assets, so no `meta/categories/`
membership is required.

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
> date_completed: "2026-05-01"
> status: "complete"
> ---
> **Results Summary: Best-Available Answers to RQ1-RQ5**
>
> **Summary**
>
> This task was re-scoped after the implementation prestep discovered that all 10 originally
> planned
> paper assets already exist under `t0017_literature_hierarchical_agents_and_judges`. Rather
> than
> duplicate them, the task now answers the project's five Research Questions (RQ1-RQ5)
> directly, using
> the existing t0017 paper summaries plus prior project findings from t0014, t0019, and t0020
> as
> evidence. The headline finding is that **RQ1 and RQ4 have strong external-literature
> support,
> RQ2/RQ3/RQ5 have only partial support**, and **none of the five RQs has yet been answered
> with
> direct empirical project data on the runtime A/B/C agent conditioning** because the
> project's Phase
> 2 experiment (the cancelled t0023 ABC sonnet run, $40-45 estimate) has not yet been
> executed. The
> most important Brainstorm-Session-8 input from this synthesis is the residual- uncertainty
> list at
> the end of `results/results_detailed.md`, which scopes a minimum-viable Phase 2 design
> within the

</details>

<details>
<summary>✅ 0024 — <strong>Brainstorm session 7: rescope around RQ answers after
t0019 calibration finding</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0024_brainstorm_results_7` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md), [`t0018_brainstorm_results_6`](../../../overview/tasks/task_pages/t0018_brainstorm_results_6.md), [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md), [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-01T18:00:00Z |
| **End time** | 2026-05-01T19:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 7: rescope around RQ answers after t0019 calibration finding](../../../overview/tasks/task_pages/t0024_brainstorm_results_7.md) |
| **Task folder** | [`t0024_brainstorm_results_7/`](../../../tasks/t0024_brainstorm_results_7/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0024_brainstorm_results_7/results/results_detailed.md) |

# Brainstorm Session 7: Refresh Literature Before the Next Agent Iteration

## Motivation

Brainstorm Session 6 (t0018) scheduled the headline confirmatory experiment as t0023
(`phase2_abc_confirmatory_sonnet_swebench`, N=157, $40-45 estimated). Two facts moved between
t0018 and now:

1. **t0019 weakened the headline schema effect**. The schema-only accept-rate delta from t0014
   (+58 pp under haiku judge) shrinks to +24.6 pp under a substantive sonnet judge and +37.3
   pp under a model-rotated sonnet judge. Both numbers are below the +45 pp commit threshold
   the task pre-registered. Model-anchoring is the dominant judge-side effect.
2. **Budget**: $26.12 remaining of the $100 project budget. Tasks have run 3-4x estimates
   (t0014 $21.16, t0019 $19.30 against $5 plans). t0023 at $40-45 does not fit even with the
   minimum-viable cuts described in its `task_description.md` Risks & Fallbacks.

The brainstorm-6 slate intentionally separated infrastructure (t0021, t0022) from the headline
agent run. Both libraries are now shipped and verified. Before consuming them with another
expensive sonnet experiment, the researcher chose to refresh the project's literature
understanding of hierarchical / granularity-aware agents and judge methodology, so the next
experiment iteration is designed against the current state of the art rather than the t0002 /
t0017 surveys that predate the t0014, t0019, t0020 findings.

## Decisions

### Direction

The five project research questions in `project/description.md` have **zero confirmed
answers** across 22 completed tasks. The brainstorm-6 plan was to answer 4 of 5 RQs in one
rescoped sonnet experiment. After dialogue, the researcher decided that the cheapest correct
next move is a focused 2024-2026 literature survey covering hierarchical / granularity-aware
LLM agents, search and planning structure, reasoning-structure discovery, agent benchmarks,
and LLM-as-judge methodology, plus the foundational options-framework theory anchor (Sutton,
Precup & Singh 1999). The survey informs the design of the next agent-iteration experiment,
which is deferred to a post-survey brainstorm session.

RQ3 (low-level "can-execute-now" vs "must-request-information") remains deferred — it requires
a different instrumentation (τ-bench-style) regardless of which experiment comes next.

### New Tasks (1)

| ID | Slug | Covers | Cost cap | Depends |
| --- | --- | --- | --- | --- |
| t0025 | `lit_survey_hierarchical_agents_and_judges_2024_2026` | reading list of 10 papers; informs next agent-iteration design | ~$3 | none |

### Cancellations (1)

| ID | Action | Reason |
| --- | --- | --- |
| t0023 | `not_started` → `cancelled` | Original $40-45 estimate exceeds remaining budget. The phase 2 ABC sonnet experiment is deferred to a post-literature-survey brainstorm so the design can incorporate hierarchical-agent and judge-methodology findings from t0025. |

### Corrections (5)

| Suggestion | Action | Reason |
| --- | --- | --- |
| S-0014-03 | active → rejected | Covered by t0019 model-rotated judge run; data merged. |
| S-0019-01 | active → rejected | Confirmatory v3 schema iteration not on critical path within remaining budget. |
| S-0017-01 | active → rejected | Trust-or-Escalate selective-evaluation library setup cost exceeds RQ-level value; the Trust-or-Escalate paper itself is on the t0025 reading list. |
| S-0002-03 | priority high → low | ServiceNow + WorkArena harness out of scope; SWE-bench is the chosen benchmark for the deferred phase 2 experiment. |
| S-0010-01 | priority high → medium | C-adversarial dropped from the immediate slate; partial coverage by C-random remains in the planned phase 2 successor. |

## t0025 Reading List

Ten papers organized by theme. Asset format: standard paper assets in
`tasks/t0025_*/assets/paper/<paper_id>/` per `meta/asset_types/paper/specification.md`.

* **Hierarchical / granularity-aware agents** (4):
  * "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
    Agents" (ICLR 2026)
  * ArCHer: "Training Language Model Agents via Hierarchical Multi-Turn RL" (ICML 2024)
  * "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024)
  * Sutton, Precup & Singh 1999: "Between MDPs and Semi-MDPs" (foundational options framework)
* **Search and planning structure** (2):
  * "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024)
  * LATS: "Language Agent Tree Search" (ICML 2024)
* **Reasoning structure discovery** (1):
  * SELF-DISCOVER (NeurIPS 2024)
* **Agent benchmarks** (2):
  * Embodied Agent Interface (NeurIPS 2024)
  * AgentBoard (NeurIPS 2024 Datasets and Benchmarks)
* **LLM-as-judge methodology** (1):
  * "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"

## Hard Kill Switches for t0025

A literature-survey task does not need experiment-style kill switches, but the cost cap is
enforced:

* **Hard cap**: ~$3 ceiling for the whole survey (PDF downloads are free; cost comes only from
  agent reading and summarization). Halt if the projection at 5 papers in exceeds $5.
* **Stop on paywall block**: if more than 2 of the 10 papers cannot be downloaded after
  exhausting arXiv, Semantic Scholar, OpenAlex, and conference proceedings, halt and produce a
  summary based on abstracts plus a triage note.

## Parallelism

t0025 is the only new task. The 10 paper-add invocations inside t0025 can run in parallel via
sub-agents (each `add-paper` invocation is independent).

## RQ Coverage After This Session

| RQ | Status After t0024 | Addressed by |
| --- | --- | --- |
| RQ1 (granularity → success) | open → still open | future post-survey experiment |
| RQ2 (overconfident error) | open → still open | future post-survey experiment |
| RQ3 (can-execute vs must-request) | open → deferred | future task |
| RQ4 (gains in info-asymmetric states) | open → still open | future post-survey experiment |
| RQ5 (mismatch penalty) | open → still open | future post-survey experiment |

The literature survey itself does not answer any RQ; it informs the design of the experiment
that will. If post-survey brainstorming concludes that no remaining-budget experiment can
credibly answer the RQs, the project pivots to a thesis headlined on the offline annotation +
judge calibration findings (t0014 + t0019 + t0020) plus the literature-survey synthesis.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — full brainstorm task folder.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold (status
  `not_started`).
* 5 correction files in `tasks/t0024_brainstorm_results_7/corrections/`.
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to
  `cancelled`.

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no
  compute, no empirical findings. Decisions are quality-controlled only by reviewer judgement.
* A literature survey does not directly answer any RQ. It is preparatory work for the next
  experiment design, which itself is not yet scheduled.
* The remaining $26 budget after t0025's ~$3 leaves only ~$23 for any post-survey experiment —
  which is below most realistic cost estimates for an above-floor sonnet ABC run with N>=80.
  The post-survey brainstorm may have to choose between a tightly minimal experiment and a
  thesis pivot.
* RQ3 is deferred without a scheduled successor task.

## Next Steps

* Execute t0025 next: download and summarize the 10 papers, then write a synthesis section in
  the results that explicitly maps findings to candidate next-experiment designs.
* After t0025 completes: open Brainstorm Session 8 to scope the next agent-iteration
  experiment given the survey synthesis and the ~$23 remaining budget.

**Results summary:**

> **Brainstorm Session 7 — Results Summary**
>
> **Summary**
>
> Cancelled t0023 ($40-45 estimated, exceeds the $26.12 remaining budget), replaced it with
> t0025 — a
> 10-paper literature survey on hierarchical agents and LLM-as-judge methodology — and
> deferred the
> phase 2 ABC sonnet experiment to a post-survey Brainstorm Session 8. Five suggestions
> corrected
> (three rejected, two demoted). No RQ answered.
>
> **Headline Decisions**
>
> * Cancelled t0023 (`phase2_abc_confirmatory_sonnet_swebench`, $40-45 estimated) because its
>   cost
> exceeds the $26.12 remaining project budget.
> * Created t0025 (`lit_survey_hierarchical_agents_and_judges_2024_2026`) — a focused 10-paper
> literature survey of 2024-2026 work on hierarchical agents, search and planning structure,
> reasoning-structure discovery, agent benchmarks, and LLM-as-judge methodology, plus the
> foundational Sutton-Precup-Singh 1999 options-framework paper. Cost cap ~$3.
> * Wrote 5 correction files: 3 suggestion rejections (S-0014-03, S-0019-01, S-0017-01) and 2
>   priority
> demotions (S-0002-03 → low; S-0010-01 → medium).
> * Deferred RQ3 (can-execute-now vs must-request-information) to a future task — different

</details>

<details>
<summary>✅ 0022 — <strong>ABC Harness with Progress Rate and EAI Error
Taxonomy</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0022_abc_harness_progress_rate_and_error_taxonomy` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0017-02` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-05-01T14:04:29Z |
| **End time** | 2026-05-01T20:40:00Z |
| **Step progress** | 9/15 |
| **Task page** | [ABC Harness with Progress Rate and EAI Error Taxonomy](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Task folder** | [`t0022_abc_harness_progress_rate_and_error_taxonomy/`](../../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/results_detailed.md) |

# ABC Harness with Progress Rate and EAI Error Taxonomy

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor across all
three ABC conditions (A: 2.5%, B: 0%, C: 0%). At the floor, **binary task success cannot
distinguish** scope-aware from scope-unaware behaviour, so RQ1, RQ2, and RQ5 are invisible no
matter how big the sample.

t0017 surfaced two literature instruments that fix this:

* **AgentBoard progress rate** (Ma2024, NeurIPS 2024 D&B): subgoal coverage scoring with
  Pearson rho \> 0.95 against humans across 1013 environments. A continuous metric in `[0, 1]`
  that gives signal even when no run reaches the terminal goal.
* **Embodied Agent Interface error taxonomy** (Li2024, NeurIPS 2024): a 6-class per-step
  taxonomy (hallucination, affordance violation, missing step, extra step, wrong-order step,
  precondition/effect error) that attributes failures to specific modes.

Both instruments must be in place **before** t0023's confirmatory N>=157 run, otherwise t0023
risks producing the same uninformative floor result that t0012 produced. This task is a
zero-API library task that builds the two instruments and validates them on the t0012 sample.

This task covers `S-0017-02`.

## Scope

Build a single library that the existing ABC harness can import and call, exposing two
functions:

1. `compute_progress_rate(trajectory, environment_subgoals) -> float`
   * Implements the Ma2024 protocol: a list of subgoals defined per environment, scored 0/1 by
     a judge model, averaged over the trajectory. Returns a float in `[0, 1]`.
2. `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel`
   * Implements the Li2024 protocol: a strict-output judge call that returns one of six labels
     (`hallucination`, `affordance`, `missing_step`, `extra_step`, `wrong_order`,
     `precondition_or_effect`) plus an "ok" sentinel for non-error steps.

Both functions delegate to a judge model (default: claude-haiku-4-5; configurable to sonnet).
Subgoal definitions for FrontierScience-Olympiad and SWE-bench Verified live in a JSON
side-file in the library asset's `files/` directory. SWE-bench coverage is the priority since
t0023 runs there.

The library exposes a single high-level entry point `score_trajectory(trajectory, environment)
-> TrajectoryScore` that returns:

* `task_success: bool`
* `progress_rate: float`
* `step_errors: list[ErrorTaxonomyLabel]`
* `error_distribution: dict[label, count]`

## Deliverables

1. **Library asset** (`assets/library/abc_harness_metrics/`) with `details.json`, canonical
   description document, source code under `files/`, and subgoal-definition JSON for at least
   FrontierScience-Olympiad and SWE-bench Verified Lite.
2. **Unit tests** in `tasks/t0022_*/code/test_*.py`:
   * Progress rate is `0.0` when no subgoal is hit and `1.0` when all subgoals are hit, on a
     synthetic trajectory.
   * Each error taxonomy label is producible on a hand-crafted trajectory step.
   * The high-level entry point composes the two without raising on a known-good t0012 row.
3. **Validation against t0012**: replay the t0012 smoke trajectories through the new library
   and report progress rate and error distribution per ABC condition. Save these as a
   side-by-side table in `results/results_detailed.md`.
4. **Subgoal-definition JSON** for SWE-bench Verified Lite covering at least 50 instances (the
   subset t0023 will use). Use the SWE-bench Verified hint annotations as the seed.

## Implementation Notes

* **Subgoal scoring is a judge call**, not a deterministic check. Cache results to disk keyed
  by (environment, trajectory hash, subgoal text) so re-runs in t0023 do not re-spend.
* **Judge prompt** for progress rate: copy the Ma2024 supplementary material §C.2 prompt
  verbatim where licensing allows; otherwise paraphrase with explicit attribution in the
  library description document.
* **Error taxonomy prompt** for `classify_error`: use Li2024's appendix A.4 schema. The
  classifier returns exactly one label; ties default to `precondition_or_effect`.
* **Subgoal coverage on SWE-bench**: a "subgoal hit" is operationalised as the agent producing
  an edit that touches the same file as the gold patch hunk; finer-grained subgoals (line
  ranges, AST nodes) are out of scope here and can land in a follow-up.

## Cost Estimate

* Validation pass on t0012 smoke trajectories (~40 rows x 3 conditions x ~5 steps each = 600
  step-classifications + 120 progress-rate scores): **~720 haiku judge calls**.
* Haiku ~2k tokens in, ~150 tokens out per call: **~1.4M in, ~110k out**.
* At haiku pricing: **~$1.50**.
* Reserve: **+$0.50**.
* Total: **~$2**.

## Decision Criteria

After this task:

* If progress rate on the t0012 sample produces a non-degenerate distribution (mean > 0.05 and
  stddev > 0.03), the metric is a viable Metric 1 candidate for t0023. Otherwise, document the
  calibration problem and propose a different subgoal granularity.
* If the error taxonomy correctly distinguishes condition C trajectories from condition A
  trajectories on at least **30% of paired steps**, the taxonomy is doing real work and t0023
  can rely on it. Otherwise, flag and recommend tightening the per-environment subgoal lists
  before t0023.

## Dependencies

None. Output is consumed by t0023.

## Source Suggestion

`S-0017-02`.

## Risks and Fallbacks

* **Judge cost on t0023 explodes**: t0023 with N=157 x 3 conditions x ~5 steps each = ~2400
  step-classifications. Plan haiku as the default judge; reserve sonnet for spot-check
  re-grading on a 20-row stratified sample only.
* **Subgoal definitions miscalibrate**: the SWE-bench JSON has to be reviewed by hand on a
  10-instance pilot before t0023 ships.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass.
* Subgoal-definition JSON contains entries for at least 50 SWE-bench Verified Lite instances.
* The t0012 replay produces a per-condition breakdown of progress rate and error distribution
  in `results/results_detailed.md`.
* Cost in `results/costs.json` is at or below **$2**.

**Results summary:**

> **Results Summary: ABC Harness Progress Rate and Error Taxonomy**
>
> **Summary**
>
> Built and validated the `abc_harness_metrics` library: Ma2024 AgentBoard discrete-subgoal
> progress
> rate plus Li2024 Embodied Agent Interface six-plus-one error taxonomy. The library exposes
> `compute_progress_rate`, `classify_error`, and the high-level `score_trajectory` entry
> point, with
> 26 unit tests passing and a t0012 replay confirming end-to-end correctness on
> production-shape
> trajectories.
>
> **Metrics**
>
> * **Progress-rate mean across 89 t0012 trajectories**: **0.103** (decision threshold > 0.05)
>   — the
> library detects intermediate progress on real agent traces, not zero or one.
> * **Progress-rate standard deviation**: **0.228** (decision threshold > 0.03) — distribution
>   is
> meaningfully spread across the 91 rows, with values from 0.0 to 1.0.
> * **A-vs-C error-distribution total-variation separation**: **0.771** (decision threshold >=
>   0.30) —
> single-step (A) and hierarchical (C) trajectories produce qualitatively different error
> mixtures,
> confirming the taxonomy can discriminate between conditions for t0023.
> * **FrontierScience-Olympiad subgoal coverage**: **26 environments**, mean 4.6 subgoals each
>   (3-5

</details>

<details>
<summary>✅ 0021 — <strong>Plan-and-Solve v2 with final_confidence Field</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0021_plan_and_solve_v2_with_final_confidence` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0012-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-05-01T14:03:02Z |
| **End time** | 2026-05-01T17:10:00Z |
| **Step progress** | 9/15 |
| **Key metrics** | Task Success Rate: **0.0** |
| **Task page** | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Task folder** | [`t0021_plan_and_solve_v2_with_final_confidence/`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/results/results_detailed.md) |

# Plan-and-Solve v2 with final_confidence Field

## Motivation

The t0007 `scope_unaware_planandsolve_v1` library does not emit a `final_confidence` field on
trajectory records. As a result, t0012's smoke run collapsed Metric 2
(overconfident_error_rate) to **0.0** for conditions B and C, making **RQ4 untestable** in any
confirmatory ABC experiment that reuses this library.

Before scaling to t0023 (sonnet on SWE-bench, N>=157), the library has to emit a verbalized
confidence label so Metric 2 is non-degenerate. This is a prerequisite library task with
**zero external API cost**.

This task covers `S-0012-01`.

## Scope

Extend the existing `tasks/t0007_*/code/` library (or the active fork of it) so that every
trajectory record produced by `scope_unaware_planandsolve_v1` carries a `final_confidence`
field in the range `[0.0, 1.0]`, populated by a verbalized confidence call following the
**Xiong2024 section 3.2 protocol**:

* After the model produces its final action / answer for the trajectory, issue **one
  additional prompt** asking the model to rate its confidence in the just-produced output on a
  0-1 scale, with explicit anchor-language ("0.0 = certain wrong, 0.5 = coin flip, 1.0 =
  certain right").
* Parse the numeric value with a strict regex; on parse failure, retry once with a clearer
  prompt; on second failure, write `null` and increment a `final_confidence_parse_failures`
  counter on the trajectory metadata.

The new `final_confidence` field must be emitted by **all three conditions** (A scope-aware, B
scope-unaware, C scope-mismatched) so paired analysis is well-defined.

## Deliverables

1. **Library asset** (`assets/library/scope_unaware_planandsolve_v2/`) with full
   `details.json`, canonical description document, and source code under `files/`. The library
   keeps backward compatibility: the v1 entry point still exists and still returns
   trajectories without `final_confidence`; the new v2 entry point returns trajectories that
   always carry the field.
2. **Unit tests** in `tasks/t0021_*/code/test_*.py`:
   * `final_confidence` is in `[0.0, 1.0]` whenever the parse succeeds.
   * `final_confidence` is `null` when the parse fails.
   * `final_confidence_parse_failures` count matches the number of `null` rows.
   * Trajectories from all three conditions (A, B, C) carry the field.
   * The v1 entry point continues to return the legacy schema.
3. **Smoke validation**: run the v2 library on a 5-row instance pool with claude-haiku-4-5 and
   confirm Metric 2 (overconfident_error_rate) returns a non-degenerate, non-zero value when
   at least one row is wrong with high confidence.
4. **Verbalized confidence prompt template** copied into `assets/library/.../files/prompts/`
   verbatim, with an inline citation to Xiong2024 §3.2 in the description document.

## Implementation Notes

* **Prompt protocol**: Xiong2024 section 3.2 says: "After answering, on a separate line,
  output a number between 0 and 1 representing your confidence that your answer is correct,
  where 0 means certain wrong and 1 means certain correct." Reuse this exact phrasing.
* **Two-call vs one-call**: prefer the two-call protocol (final answer first, confidence
  second) to avoid the model conditioning its answer on its own confidence claim. One-call is
  acceptable only if the cost difference matters at scale.
* **Caching**: confidence calls must reuse the same conversation prefix as the answer call to
  avoid double-charging for the prompt context. Use claude prompt caching where available.

## Cost Estimate

* Smoke validation: 5 rows x 3 conditions x 2 calls each (answer + confidence) with
  claude-haiku-4-5 = **30 calls**.
* Haiku input ~4k tokens per call x 30 = **~120k input tokens**.
* Haiku output ~300 tokens per call x 30 = **~9k output tokens**.
* At haiku pricing: **<$0.20**.
* Total: **<$1**.

## Decision Criteria

After this task:

* If unit tests and the smoke validation pass, the library is unblocked for t0023.
* If the confidence parse fails on more than **20%** of haiku rows, raise the parse failure
  rate in the description document and either tighten the prompt or move to JSON-mode output.
  Do not ship a library that is unreliable at parsing.

## Dependencies

None. The library will be reused by t0023.

## Source Suggestion

`S-0012-01`.

## Risks and Fallbacks

* **Sonnet-vs-haiku confidence drift**: haiku may produce flat confidence distributions
  (everything 0.7-0.9). If so, document this and flag it as an interpretability risk for
  t0023's Metric 2 analysis. The library does not need to fix the model's calibration; it only
  needs to emit the field.
* **Refusal rate increase**: adding a confidence call may push some models toward hedging the
  primary answer. Compare the smoke-run accuracy at A condition to the t0007/t0012 numbers; if
  accuracy drops by more than 5 pp, run an ablation with the confidence call moved to a
  separate trajectory.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass (`uv run pytest tasks/t0021_*/code/`).
* Smoke validation produces a non-zero, non-1 value for Metric 2 when ground truth shows at
  least one high-confidence error.
* `results/metrics.json` records the smoke run's Metric 2 value to confirm the field is wired
  end-to-end.
* Cost in `results/costs.json` is at or below **$1**.

**Results summary:**

> **Results Summary: Plan-and-Solve v2 with final_confidence**
>
> **Summary**
>
> The deliverable is the `scope_unaware_planandsolve_v2` library that wraps the v1
> Plan-and-Solve
> agent and emits a verbalized `final_confidence` field on every trajectory following the
> Xiong et al.
> 2024 section 3.2 protocol. The n=1 x 3 validation pass confirms the parser, two-call
> protocol, and
> confidence emission are wired end-to-end across all three conditions (A scope-aware, B
> scope-unaware, C scope-mismatched). The 0% task-success rate across all conditions on
> FrontierScience-Olympiad with claude-haiku-4-5 is consistent with the t0012 floor finding
> for the
> same benchmark and model and is the explicit motivation for the larger downstream
> confirmatory study
> in t0023.
>
> **Metrics**
>
> * **task_success_rate**: A=**0.0** (0/1), B=**0.0** (0/1), C=**0.0** (0/1) — at-floor on
>   this
> benchmark, as expected.
> * **overconfident_error_rate**: A=**1.0** (the single A row was wrong with high confidence),
> B=**0.0**, C=**0.0** — non-degenerate emission across conditions confirmed.
> * **avg_decisions_per_task**: A=**1.0**, B=**8.0**, C=**31.0** — flagged side-finding: C
>   used 31x

</details>

<details>
<summary>✅ 0020 — <strong>v2 Truncation vs Schema Ablation</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0020_v2_truncation_vs_schema_ablation` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0009-04` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-05-01T14:06:25Z |
| **End time** | 2026-05-01T14:53:30Z |
| **Step progress** | 9/15 |
| **Key metrics** | Task Success Rate: **0.95** |
| **Task page** | [v2 Truncation vs Schema Ablation](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Task folder** | [`t0020_v2_truncation_vs_schema_ablation/`](../../../tasks/t0020_v2_truncation_vs_schema_ablation/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0020_v2_truncation_vs_schema_ablation/results/results_detailed.md) |

# v2 Truncation vs Schema Ablation

## Motivation

The t0009 -> t0014 v2 upgrade changed two things at once:

1. **Schema**: flat list -> nested tree (global -> subtask -> atomic).
2. **Text completeness**: prompts moved from a 1500-char truncation to the full problem text.

On FrontierScience-Olympiad and WorkArena++, v2 saw +67% and +100% accept-rate deltas. Either
the truncation fix is doing the work (Xiong2024's prediction: longer context -> better
calibration), or the schema upgrade is doing the work, or both.

t0019 attacks the judge side of this question. **t0020 attacks the input side.** It runs a
third condition that holds the schema constant and reverts the truncation, so any drop
relative to v2-full isolates the truncation contribution.

This task covers `S-0009-04`.

## Scope

Run **one new annotation condition**: the v2 tree schema applied to the same instance pool as
t0014, but with the problem text truncated to **1500 characters** in both annotator and judge
prompts (matching the t0009 baseline exactly).

The result feeds a 3-way comparison with already-collected data:

| Condition | Schema | Text | Source |
| --- | --- | --- | --- |
| v1-flat-truncated | flat | 1500 chars | t0009 baseline |
| v2-tree-truncated | tree | 1500 chars | **this task** (new) |
| v2-tree-full | tree | full text | t0014 (existing) |

Effects decompose:

* `v2-tree-truncated - v1-flat-truncated` = pure schema effect (text held constant).
* `v2-tree-full - v2-tree-truncated` = pure text-length effect (schema held constant).
* The t0014 +57 pp delta = sum of the two.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_truncated_ablation/`): per-row annotator and
   judge outputs for the v2-tree-truncated condition. Same row pool as t0014 for paired
   comparison.
2. **Answer asset** addressing: "Of the t0014 +57 pp schema-only delta, how much is
   attributable to the schema upgrade vs the truncation fix, holding the other constant?"
3. **Reported metrics** with three explicit variants (one per row in the table above):
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Decomposition table** in `results/results_detailed.md` showing the two isolated deltas
   with 95% CIs.

## Models and Configurations

* **Annotator**: claude-haiku-4-5 (matching t0009/t0014 baseline; haiku is cheap and used for
  the schema-effect reading).
* **Judge**: claude-haiku-4-5 with the t0014 original judge prompt (held constant; t0019
  handles the judge-side calibration).
* Same instance pool as t0014 (subtract the 3 known sonnet-timeout rows so n is matched across
  conditions).

Total annotation calls: ~40 rows x 1 condition = **~40 haiku annotation calls**. Total judge
calls: ~40 rows = **~40 haiku judge calls**.

## Cost Estimate

* Haiku input ~3k tokens per call x 80 calls = **~240k input tokens**.
* Haiku output ~500 tokens per call x 80 calls = **~40k output tokens**.
* At claude-haiku-4-5 pricing (approximately $0.80/M in, $4/M out): **about $0.36** haiku
  spend.
* Reserve for retry: **+$1**.
* Total: **~$1-2**.

## Decision Criteria

After this task:

* If `v2-tree-truncated - v1-flat-truncated >= +40 pp`, the schema upgrade is the dominant
  cause; Xiong2024's truncation hypothesis is rejected at this scale and the v2 schema
  deserves the headline.
* If `v2-tree-full - v2-tree-truncated >= +40 pp`, the truncation fix is the dominant cause;
  the v2 schema wins per row roughly because v1 truncation was clipping the problem before the
  model could reason about it. The headline shifts from "tree schema helps" to "include the
  full problem".
* If both contributions are within +/-15 pp of each other, the two compose roughly additively
  and both must be retained for the schema-effect claim.

## Dependencies

None.

## Source Suggestion

`S-0009-04`.

## Risks and Fallbacks

* **Truncation alters which instances are answerable at all**: some FrontierScience-Olympiad
  problems may be unparseable when clipped to 1500 chars. Log per-row truncation impact (did
  the model receive a complete problem statement) and report n for each (truncated, full)
  split.
* **Haiku is too noisy at small n**: if accept-rate stderr exceeds +/-15 pp on the new
  condition, flag the result as inconclusive and mark the decomposition as "underpowered,
  needs n=80 to resolve". Do not over-claim from n=40.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has the three variants with stderr.
* `results/results_detailed.md` contains the decomposition table and a paired-row check that
  the same instance ids appear in all three conditions.
* Cost in `results/costs.json` is at or below **$2**.

**Results summary:**

> **Results Summary: v2 Truncation vs Schema Ablation**
>
> **Summary**
>
> Ran the third condition needed to decompose the +57 pp v2-tree-full vs v1-flat-truncated
> acceptance-rate gap from t0014. Held the v2 tree schema constant and re-truncated the
> problem text
> to 1500 chars in both the haiku annotator and haiku judge prompts. Result: the v2 tree
> schema
> explains essentially all of the gap. The pure-schema effect is **+57 pp** (CI excludes 0);
> the
> pure-text-length effect is **+5 pp** (CI straddles 0 and is not significant at n=20).
>
> **Metrics**
>
> * **v1-flat-truncated accept rate**: **33%** (4 / 12), Wilson 95% CI [13.8%, 60.9%]
> * **v2-tree-truncated accept rate**: **90%** (18 / 20), Wilson 95% CI [69.9%, 97.2%]
> * **v2-tree-full accept rate**: **95%** (19 / 20), Wilson 95% CI [76.4%, 99.1%]
> * **Pure-schema delta** (v2-tree-truncated − v1-flat-truncated): **+56.7 pp**,
>   Newcombe-Wilson 95%
> CI [+22.5 pp, +77.5 pp]
> * **Pure-text delta** (v2-tree-full − v2-tree-truncated): **+5.0 pp**, Newcombe-Wilson 95%
>   CI
> [-15.0 pp, +25.5 pp]
> * **Headline delta** (v2-tree-full − v1-flat-truncated): **+61.7 pp**, Newcombe-Wilson 95%
>   CI

</details>

<details>
<summary>✅ 0019 — <strong>v2 Judge Calibration with Sonnet (Substantive + Familial
Bias)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0019_v2_judge_calibration_sonnet` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`comparative-analysis`](../../../meta/task_types/comparative-analysis/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-05-01T14:02:34Z |
| **End time** | 2026-05-01T17:55:02Z |
| **Step progress** | 10/15 |
| **Key metrics** | Task Success Rate: **1.0** |
| **Task page** | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Task folder** | [`t0019_v2_judge_calibration_sonnet/`](../../../tasks/t0019_v2_judge_calibration_sonnet/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0019_v2_judge_calibration_sonnet/results/results_detailed.md) |

# v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

## Motivation

t0014 produced a schema-only delta of **+57 pp** for v2 over v1, well above Zhou2022's +16 pp
and Boisvert2024's +25 pp published bands, and a model-only delta of **-1 pp** that sits below
Xiong2024's lower edge (0 pp). Two plausible threats to validity remain:

1. **Judge anchoring** (S-0014-02): the haiku judge may be partially scoring "the model
   produced a parseable tree with subtask-to-atomic edges" rather than "the decomposition is
   substantively right". If so, the +57 pp gap to literature is a judge artefact, not a schema
   effect.
2. **Familial bias** (S-0014-03): the haiku judge gives the v2-haiku annotator a same-family
   agreement bonus (~5-10 pp per Xiong2024). If so, the -1 pp model-only delta is masking a
   real sonnet annotator advantage.

Both threats can be tested at the same 43-row pool used in t0014 by swapping the judge prompt
and judge model. Defending the +57 pp schema-only headline before scaling to a confirmatory
experiment is the cheapest paper-defensible step on the critical path.

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary).

## Scope

Re-judge **the same 43 v2 rows** that t0014 produced (20 v2-sonnet + 23 v2-haiku) plus the
matched 20 v1-sonnet rows from t0009/t0014, under two new judge configurations:

* **Substantive critic** prompt (S-0014-02): the judge simulates execution ("verify each
  atomic, executed in order, would actually solve the problem") and outputs a binary
  accept/reject plus a per-criterion sub-score.
* **Model-rotated** judge (S-0014-03): keep the original t0014 judge prompt, swap the judge
  model from haiku to claude-sonnet-4-6.

Both judges run against the same row pool. Combined output is a 4-condition matrix per row:

| Condition | Annotator | Judge Prompt | Judge Model |
| --- | --- | --- | --- |
| Baseline (from t0014) | v1-sonnet / v2-haiku / v2-sonnet | original | haiku |
| Substantive | v1-sonnet / v2-haiku / v2-sonnet | substantive critic | sonnet |
| Model-rotated | v1-sonnet / v2-haiku / v2-sonnet | original | sonnet |

This task does not re-annotate. It only re-judges. Annotation rows from t0014 are read in via
the existing predictions overlay applied by t0015.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_judge_calibration/`): per-row judge verdicts
   under the substantive and model-rotated conditions, plus the cached baseline t0014/t0015
   verdicts as reference. Includes prompt-version and judge-model fields per row.
2. **Answer asset** (`assets/answer/.../`) addressing the question: "Does the v2 schema retain
   a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or
   is the +57 pp t0014 headline an artefact of haiku judge anchoring?"
3. **Reported metrics** in `results/metrics.json` using the explicit multi-variant format, one
   variant per (annotator x judge-prompt x judge-model) cell. Each cell reports:
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Comparison table** in `results/results_detailed.md` showing the schema-only and
   model-only deltas under all three judge configurations side by side, with explicit deltas
   vs t0014.

## Models and Configurations

* **Annotator outputs** (already produced; not re-run): claude-sonnet-4-6 v1 (20 rows), haiku
  v2 (23 rows), sonnet v2 (20 rows). All from t0014.
* **Substantive critic judge**: claude-sonnet-4-6 with the new prompt template.
* **Model-rotated judge**: claude-sonnet-4-6 with the original t0014 judge prompt.

Total judge calls: 43 rows x 2 new judge configurations = **86 sonnet judge calls**.

## Cost Estimate

* Sonnet input ~5k tokens per call x 86 = **~430k input tokens**.
* Sonnet output ~600 tokens per call x 86 = **~52k output tokens**.
* At claude-sonnet-4-6 pricing (approximately $3/M in, $15/M out): **about $2.05** sonnet
  spend.
* Reserve for retry/repair: **+$1**.
* Total: **~$3-5**.

This sits well within the remaining $51 budget.

## Decision Criteria

After this task:

* If schema-only delta drops below **+30 pp** under the substantive judge, the +57 pp t0014
  headline is partly judge-anchoring; reset the headline to the substantive number and revisit
  S-0014-01 (v3 schema iteration).
* If schema-only delta stays at or above **+45 pp** under both new judges, the schema effect
  is robust; commit to the t0023 confirmatory run as planned.
* If model-only delta swings to **at least +5 pp** under the sonnet judge, the t0014 -1 pp
  result is a haiku familial bias, and v2-sonnet should be the production annotator going
  forward.
* If model-only delta stays within +/-2 pp under the sonnet judge, the v2 schema does the work
  and sonnet annotation is not worth the cost premium.

## Dependencies

None on uncompleted tasks. Reads from t0014's predictions and t0015's correction overlay; both
are merged.

## Source Suggestion

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary). Both suggestions remain
active as `source_suggestion` until t0019 results are merged; the secondary will be marked
covered in the next brainstorm round if the data answers it.

## Risks and Fallbacks

* **Substantive judge is slow or unstable**: if per-row judge time exceeds 30 s, drop
  sub-criteria and use a binary verdict only.
* **Sonnet judge disagrees with itself across the two prompt variants on the same row**: log
  per-row agreement; report Cohen's kappa across (substantive, model-rotated) at the same
  model. This is a free signal about prompt-vs-anchoring effects.
* **The t0014 row pool has masked instances** (we know 3 sonnet timeouts exist; S-0014-05 was
  rejected): exclude those rows from all conditions consistently and report the effective n.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` contains all 9 cells (3 annotators x 3 judge configs) with
  accept_rate and stderr.
* `results/results_detailed.md` contains a side-by-side delta table and an explicit
  decision-criteria check-off against the four bullets above.
* Cost in `results/costs.json` is at or below **$5**.

**Results summary:**

> **Results Summary: v2 Judge Calibration with Sonnet**
>
> **Summary**
>
> Re-judged the same 55-row hierarchy pool from t0014 (12 v1-sonnet + 23 v2-haiku + 20
> v2-sonnet)
> under three judge configurations: the cached t0014 original-haiku verdicts as baseline, a
> substantive critic prompt on `claude-sonnet-4-6`, and a model-rotated original-prompt judge
> on
> `claude-sonnet-4-6`. The headline finding is that the +57 pp v2-vs-v1 schema-only gap from
> t0014
> **partially survives** under sonnet judges: **+24.6 pp** under the substantive critic and
> **+37.3
> pp** under the model-rotated judge, vs the **+58.0 pp** baseline. Neither pre-registered
> extreme
> decision criterion (drops below +30 pp on both sonnet judges, or stays at or above +45 pp on
> both)
> was simultaneously satisfied, so the answer is **Mixed / low confidence**.
>
> **Methodology**
>
> * 110 fresh sonnet judge calls (55 substantive + 55 model-rotated) via the local `claude`
>   CLI
> subprocess; the OAuth-issued ANTHROPIC_API_KEY in this environment lacks sonnet quota, so
> `intervention/critical_step_blocked.md` was filed and option 2 was authorised: raise the
> budget
> cap from $4.50 to $20.00 and switch transport from the Anthropic SDK to a `claude` CLI
> subprocess
> wrapper. The change is locked in `code/constants.py` (`BUDGET_CAP_USD = 20.00`,

</details>

<details>
<summary>✅ 0018 — <strong>Brainstorm session 6: paper-driven slate after t0017
literature survey</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0018_brainstorm_results_6` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md), [`t0016_brainstorm_results_5`](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md), [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-05-01T12:00:00Z |
| **End time** | 2026-05-01T13:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 6: paper-driven slate after t0017 literature survey](../../../overview/tasks/task_pages/t0018_brainstorm_results_6.md) |
| **Task folder** | [`t0018_brainstorm_results_6/`](../../../tasks/t0018_brainstorm_results_6/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0018_brainstorm_results_6/results/results_detailed.md) |

# Brainstorm Session 6: Paper-Driven Slate After t0017 Literature Survey

## Objective

Translate t0017's literature findings (hierarchical / granularity-aware agents, LLM-as-judge
methodology) and t0014's schema-vs-model deconfound (+57 pp schema-only, -1 pp model-only)
into a concrete experimental slate that delivers paper-quality results on the project's
research questions as fast as possible.

## Decisions

This session reached agreement on:

* **5 new tasks** (t0019-t0023) covering RQ1, RQ2, RQ4, RQ5, RQ6, RQ7, and RQ9.
* **4 reprioritizations** to reflect t0014/t0017 findings.
* **2 rejections** (out-of-scope or infeasible).
* **Default model standardization**: haiku for annotation/judging unless the hypothesis
  demands sonnet; sonnet for actual agent runs (literature consensus + t0012 floor result).
* **Parallelism**: t0019, t0020, t0021, t0022 launch in parallel worktrees; t0023 starts when
  t0021 and t0022 are done.

## New Tasks

| ID | Slug | Covers | Cost | Depends |
| --- | --- | --- | --- | --- |
| t0019 | `v2_judge_calibration_sonnet` | S-0014-02, S-0014-03 | ~$5 | none |
| t0020 | `v2_truncation_vs_schema_ablation` | S-0009-04 | ~$2 | none |
| t0021 | `plan_and_solve_v2_with_final_confidence` | S-0012-01 | $0 | none |
| t0022 | `abc_harness_progress_rate_and_error_taxonomy` | S-0017-02 | ~$1 | none |
| t0023 | `phase2_abc_confirmatory_sonnet_swebench` | S-0012-02, S-0010-01 | ~$30 | t0021, t0022 |

Total budget commitment ~$38, leaving ~$13 of the $100 project budget after this round.

## Reprioritizations

* **S-0009-03** (human-review kappa): high → medium. LLM-only stress tests in t0019 run first.
* **S-0003-01** (FrontierMath access): high → medium. SWE-bench is the chosen path;
  FrontierMath doesn't address the floor problem.
* **S-0012-03** (FSO smoke with tools): medium → low. Abandoning FSO route in favour of
  SWE-bench sonnet.
* **S-0014-01** (v3 schema iteration): kept medium, but explicitly conditioned on t0019
  substantive judge upholding the +57 pp schema-only delta.

## Rejections

* **S-0014-05** (re-run 3 sonnet timeouts): cost-of-recovery exceeds value; t0019 doesn't need
  those rows.
* **S-0002-09** (re-fetch papers with LFS): public-fork LFS upload is denied; ghostscript
  compression is the working pattern (see t0017 PR #29).

## RQs Addressed by This Slate

| RQ | Addressed by | Mechanism |
| --- | --- | --- |
| RQ1 | t0023 | A vs B task-success deltas with sonnet on SWE-bench |
| RQ2 | t0022, t0023 | Progress-rate per scope-sensitive state |
| RQ4 | t0021 (prereq) + t0023 | Metric 2 with non-zero `final_confidence` |
| RQ5 | t0023 (C and C-adversarial conditions) | Mismatch-penalty deltas |
| RQ6 | t0022 + t0023 | EAI error taxonomy on global/subtask/atomic alignment |
| RQ7 | t0019 + t0020 | Substantive judge + truncation ablation isolate semantic-scope from anchor and length |
| RQ9 | t0023 | Hard/easy SWE-bench split by hunk count |

RQ3, RQ8, RQ10 are deferred to a future round once the core RQ1/2/5/7 story holds at N>=157.

## Why This Slate, Now

The fastest paper-defensible path requires:

1. **Defending the +57 pp schema-only headline** before claiming it (t0019). Cheap (~$5) and
   decisive.
2. **Answering RQ7** (semantic scope vs prompt length) with an additional cheap ablation
   (t0020).
3. **Building the two missing instruments** for the confirmatory experiment in parallel
   (t0021, t0022), so Wave 2 is unblocked the moment Wave 1 finishes.
4. **Running the confirmatory N>=157 experiment** with sonnet on SWE-bench (t0023) to get the
   non-floor A/B/C signal that t0012 could not produce.

The 4-task parallel Wave 1 + library Wave 2 + big experiment Wave 3 structure compresses the
critical path to roughly 1-2 weeks of execution rather than serial-running everything.

**Results summary:**

> **Results Summary: Brainstorm Session 6**
>
> **Summary**
>
> Translated t0017 literature findings and t0014 deconfound results into a paper-driven
> experimental
> slate. Created 5 new tasks (t0019-t0023) covering RQ1, RQ2, RQ4, RQ5, RQ6, RQ7, and RQ9;
> applied 5
> correction files (3 reprioritizations + 2 rejections); standardized model defaults (haiku
> for
> annotation/judging, sonnet for agent runs).
>
> **Metrics**
>
> * **5 new tasks created**: t0019, t0020, t0021, t0022, t0023.
> * **5 corrections applied**: 3 reprioritizations (S-0009-03, S-0003-01, S-0012-03), 2
>   rejections
> (S-0014-05, S-0002-09).
> * **7 suggestions covered by new tasks** (linked via `source_suggestion`): S-0014-02,
>   S-0014-03,
> S-0009-04, S-0012-01, S-0017-02, S-0012-02, S-0010-01.
> * **Budget commitment for the wave**: ~$38 of $51.31 remaining; targeted leftover after
>   wave: ~$13.
> * **Suggestions actively uncovered after this round**: 35 (down from 40 before this session;
>   -5
> covered by new tasks net of 0 new suggestions).
>

</details>

<details>
<summary>✅ 0017 — <strong>Literature: Hierarchical Agents and LLM-as-Judge</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0017_literature_hierarchical_agents_and_judges` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 10 paper |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-05-01T00:00:00Z |
| **End time** | 2026-05-01T01:40:00Z |
| **Step progress** | 3/3 |
| **Task page** | [Literature: Hierarchical Agents and LLM-as-Judge](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Task folder** | [`t0017_literature_hierarchical_agents_and_judges/`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0017_literature_hierarchical_agents_and_judges/results/results_detailed.md) |

# Literature: Hierarchical Agents and LLM-as-Judge

## Motivation

The post-t0014 state of this project leaves several open questions that the existing
literature likely speaks to directly:

* The v2 schema win demonstrated that *annotation granularity* matters far more than the
  annotator model swap. Recent work on hierarchical / granularity-aware agents in RL and
  preference learning is the closest external analogue.
* Open suggestions about multi-judge agreement studies (S-0009-03) and calibration of LLM
  judges call for a direct read of the "Trust or Escalate" line of work on judges with
  provable agreement guarantees.
* Several agent-evaluation suggestions in the backlog target benchmarks we have not yet
  adopted; AgentBoard and Embodied Agent Interface are the canonical references to compare
  against.
* A short theory anchor in the options framework (Sutton, Precup & Singh 1999) is useful as
  the foundational reference for any hierarchical-action discussion in our own writing.

This task is a focused, single-pass literature survey: download, read, and summarize a curated
set of ten papers as paper assets, then stop. It is *not* an experiment, baseline, or
brainstorm — its only deliverable is the ten paper assets and a brief synthesis in
`results_detailed.md`.

## Scope

Add the following ten papers as paper assets under `assets/paper/<paper_id>/`, each with
`details.json`, the canonical summary document, and the downloaded file (or a documented
download failure):

### Hierarchical / granularity-aware agents

* P1: *Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
  Agents* — ICLR 2026.
* P2: *ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL* — ICML 2024.
* P3: *Reinforcing LLM Agents via Policy Optimization with Action Decomposition* — NeurIPS
  2024.
* P10: *Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement
  Learning* — Sutton, Precup & Singh, Artificial Intelligence 1999. Theory anchor for the
  options framework; a brief summary is sufficient.

### Search and planning structure

* P4: *Can Graph Learning Improve Planning in LLM-based Agents?* — NeurIPS 2024.
* P5: *LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language
  Models* — ICML 2024.

### Reasoning structure discovery

* P6: *SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures* — NeurIPS 2024.

### Agent benchmarks

* P7: *Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making* — NeurIPS
  2024.
* P8: *AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents* — NeurIPS 2024
  Datasets and Benchmarks.

### LLM-as-judge methodology

* P9: *Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement*.

## Approach

The task uses the standard `/add-paper` skill once per paper. For each paper:

* Resolve identity (DOI or arXiv ID), check no duplicate already exists in the project, gather
  full metadata (CrossRef + Semantic Scholar + OpenAlex), download the PDF, write
  `details.json`, read the paper, and write the canonical summary document with all nine
  mandatory sections.
* When download fails (paywall, no public version), still produce metadata and an
  abstract-based summary, with `download_status: "failed"` and a populated
  `download_failure_reason`.
* Run the paper-asset verificator after each addition.

After all ten papers are added, write a brief synthesis (`results_detailed.md`) grouping
findings by the five themes above and identifying which suggestions in our backlog the survey
strengthens or weakens. The synthesis should be at most one page; this task is not a
meta-review.

## Expected Outputs

* `assets/paper/<paper_id>/` for each of the ten papers, passing `verify_paper_asset.py` with
  zero errors.
* `results/results_summary.md` and `results/results_detailed.md` — a short synthesis grouped
  by theme, with explicit pointers to the suggestions and prior tasks each paper informs.
* `results/suggestions.json` containing any new suggestions that emerge from the reading
  (likely experiment ideas connecting hierarchical-RL findings to our annotation/calibration
  agenda).

## Compute and Budget

No GPU compute. Costs are limited to API calls during paper download (CrossRef, Semantic
Scholar, OpenAlex are free) and any LLM-assisted summarization that runs through the standard
agent context — well under \$5 total.

## Dependencies

None. Literature surveys are independent and should run in isolation. The task does not block
on any in-flight work.

## Risks and Fallbacks

* *Paper unavailable for download* — proceed with abstract-based summary per the paper-asset
  specification. This is acceptable for at most two of the ten; if more fail, escalate to the
  researcher rather than producing many low-quality summaries.
* *DOI mismatch or duplicate detection* — if a paper is already in the project, skip it and
  note the existing `paper_id` in the synthesis.

## Verification Criteria

* `assets/paper/` contains exactly ten subfolders, each passing `verify_paper_asset.py`.
* Every paper asset has `summary_path` populated and the canonical summary document contains
  all nine mandatory sections.
* `results/results_detailed.md` references each of the ten papers by `citation_key` at least
  once.
* `results/suggestions.json` is valid even if empty (`{"suggestions": []}`).

## Cross-References

* **Source suggestion** — none. This task originates from the t0016 brainstorm follow-up,
  where the researcher requested a focused read on this slice of the literature.
* **Prior tasks whose findings this informs** — t0009 (hierarchical annotation v2), t0014 (v2
  annotator sonnet rerun), t0012 (phase-2 ABC smoke), and the open suggestions S-0009-03
  (multi- judge agreement) and S-0009-04 (truncation/schema deconfound).

**Results summary:**

> **Results Summary: Literature Survey on Hierarchical Agents and LLM-as-Judge**
>
> **Summary**
>
> Completed a literature survey of ten papers covering hierarchical / granularity-aware LLM
> agents,
> search-and-planning structure, reasoning-structure discovery, agent benchmarks, and
> LLM-as-judge
> methodology — plus the foundational options-framework paper (Sutton 1999) as a brief theory
> anchor.
> All ten paper assets pass the v3 paper-asset verificator with zero errors and zero warnings.
> The
> synthesis below groups findings by the five themes defined in `task_description.md` and
> identifies
> which backlog suggestions and prior tasks the survey strengthens or weakens.
>
> **Metrics**
>
> * **10 paper assets created** out of a 10-paper target — meets `expected_assets.paper = 10`
>   exactly.
> * **5 of 5 themes covered** with at least 1 paper each: hierarchical / granularity-aware
>   agents (4
> papers — Gao2026, Zhou2024, Wen2024, Sutton1999), search and planning structure (2 papers —
> Wu2024, Zhou2024a), reasoning-structure discovery (1 paper — Zhou2024b), agent benchmarks (2
> papers — Li2024, Ma2024), LLM-as-judge methodology (1 paper — Jung2024).
> * **0 errors and 0 warnings** across 10 verifier runs after the initial PA-W005 cleanup on
> `Zhou2024b` invented category slugs.

</details>

<details>
<summary>✅ 0016 — <strong>Brainstorm session 5: prune backlog after t0014
deconfound</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0016_brainstorm_results_5` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0013_brainstorm_results_4`](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T22:00:00Z |
| **End time** | 2026-04-30T22:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 5: prune backlog after t0014 deconfound](../../../overview/tasks/task_pages/t0016_brainstorm_results_5.md) |
| **Task folder** | [`t0016_brainstorm_results_5/`](../../../tasks/t0016_brainstorm_results_5/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0016_brainstorm_results_5/results/results_detailed.md) |

# Brainstorm Session 5: Prune Backlog After t0014 Deconfound

## Context

Session 5 ran on 2026-04-30 immediately after `t0014_v2_annotator_sonnet_rerun` and
`t0015_correct_proxy_benchmark_labels` merged. `t0012_phase2_abc_smoke_frontierscience` is in
progress; this session deliberately does not perturb it.

## Headline Inputs

`t0014` decomposed t0009's published +58 pp v2-vs-v1 judge-accept-rate gain into a **+57 pp
schema-only** delta and a **−1 pp model-only** delta. The annotator-model swap from haiku to
sonnet contributes essentially zero of the gain; the v2 tree schema accounts for nearly all of
it. The +57 pp schema-only delta also bundles a truncation fix (v1 had a 1500-character
`task_excerpt` truncation that v2 removed), which `compare_literature.md` flags as a real
confound.

`t0015` wrote a single corrections-overlay file relabelling 52 of 115 v2 rows: 26 `m2w_*` rows
from `WorkArena++` to `Mind2Web`, and 26 `he_*` rows from `tau-bench` to `HumanEval`.

## Decisions

This session is pure backlog cleanup. No new tasks. No task cancellations. No task updates.
Only suggestion-status corrections.

### Reject (3)

* **S-0005-04** — superseded by t0015 (proxy benchmark naming corrected) and by the inline
  task_id de-duplication fix in t0009.
* **S-0005-05** — duplicate of S-0009-03 (single-blind human review with Cohen's kappa serves
  the same role).
* **S-0014-04** — this is a project-level decision, not a task. The +57 pp schema / −1 pp
  model split already establishes haiku-default as the right policy; recorded as project
  policy rather than executed as a task.

### Reprioritize (5)

* **S-0009-04** medium → **high** — the per-benchmark pattern in t0014 (+100 pp on long-input
  benchmarks vs +13–17 pp on short ones) is exactly what the truncation hypothesis predicts.
  Splitting the schema-only +57 pp into "tree shape" vs "no truncation" is now load-bearing
  for the science.
* **S-0002-09** medium → low — infrastructure chore (re-fetch 11 PDFs with git LFS); low
  signal for the science.
* **S-0006-02** medium → low — async ScopeAwareReactAgent is performance optimization, not
  science; Phase 2 does not need it.
* **S-0011-02** medium → low — provider-specific calibration prompt variants; Phase 2
  currently uses Anthropic only, so variant work is premature.
* **S-0014-05** medium → low — re-running 3 FrontierScience-Olympiad sonnet timeouts only
  recovers 3 rows; n=20 → 23 does not materially change Wilson CIs on the existing
  decomposition.

## Out of Scope

* Creating new tasks (deferred to session 6 once t0012 lands).
* Modifying t0012's in-progress state.
* Replacing the proxy rows with native WorkArena++ / tau-bench data (S-0015-01 remains active
  at medium priority for a future session).

## Outputs

* 8 correction files in `corrections/` against six prior tasks.
* No new suggestions.
* No new assets.
* Updated effective suggestion view: 3 fewer active, 5 with revised priority.

**Results summary:**

> **Results Summary: t0016_brainstorm_results_5**
>
> **Summary**
>
> Brainstorm session 5 was a pure backlog cleanup pass after t0014 (v2 sonnet rerun
> deconfound) and
> t0015 (proxy benchmark relabel) merged. Eight corrections were issued: three rejections,
> five
> priority changes. No new tasks were created and no existing tasks were modified.
>
> **Session Overview**
>
> * **Session number**: 5
> * **Date**: 2026-04-30
> * **Duration**: ~30 minutes
> * **Mode**: Pure cleanup (no new tasks, no task updates)
> * **Researcher budget envelope**: < $5 total (no API spend; planning only)
>
> **Decisions**
>
> **Rejections (3)**
>

</details>

<details>
<summary>✅ 0015 — <strong>Correct proxy-benchmark labels in t0009 v2
dataset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_correct_proxy_benchmark_labels` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0009-06` |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Start time** | 2026-04-30T19:08:28Z |
| **End time** | 2026-04-30T19:32:45Z |
| **Step progress** | 9/15 |
| **Task page** | [Correct proxy-benchmark labels in t0009 v2 dataset](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Task folder** | [`t0015_correct_proxy_benchmark_labels/`](../../../tasks/t0015_correct_proxy_benchmark_labels/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0015_correct_proxy_benchmark_labels/results/results_detailed.md) |

# Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Motivation

The `t0009_hierarchical_annotation_v2` dataset asset labels its four benchmarks as
`FrontierScience-Olympiad`, `SWE-bench Verified`, `WorkArena++`, and `tau-bench`. The first
two are accurate. The latter two are mislabelled — the underlying rows are `Mind2Web` and
`HumanEval` rows used as proxies for browser-using and tool-using agent benchmarks, not actual
`WorkArena++` or `tau-bench` rows. Once t0012 (Phase 2 A/B/C smoke) reports per-benchmark
numbers, naïve consumers would attribute results to benchmarks the project does not actually
evaluate on.

This task fixes the labels via the corrections-overlay mechanism — no re-annotation, no API
spend, no change to the t0009 task folder. Implements `S-0009-06` variant b (label correction;
variant a would have replaced the proxy rows with actual WorkArena++/tau-bench data, which is
out of scope for this wave).

## Scope

* Write one correction file per affected benchmark (or one combined correction, depending on
  the aggregator's per-row update support):
  * `WorkArena++` → `Mind2Web`.
  * `tau-bench` → `HumanEval`.
* Action: `update`. The correction overlays `details.json` `description_path` (and any per-row
  `benchmark` fields exposed by the dataset aggregator) so downstream consumers see the
  corrected labels.
* Provide a one-paragraph rationale per correction file referencing the original proxy
  decision taken in t0003 (benchmark download) and t0005 (v1 annotation pilot).
* Run `verify_corrections` against the new files.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data (a separate dataset
task, deferred); editing t0009's task folder (immutable); changing per-row IDs (only the
benchmark label).

## Approach

1. Read t0009's `assets/dataset/hierarchical-annotation-v2/details.json` and the dataset
   aggregator schema to confirm where benchmark labels are exposed (top-level `benchmarks`
   list, per-row `benchmark` field, or both).
2. Confirm the dataset aggregator's correction-overlay support — if `file_changes` is
   required, author a replacement description document and (if applicable) replacement JSONL
   with corrected per-row labels.
3. Write the correction file(s) under `corrections/dataset_<dataset_id>.json` per
   `corrections_specification.md` v3.
4. Re-run the dataset aggregator with the correction overlay applied; confirm the corrected
   labels are visible in the materialized output.

## Expected Outputs

* `corrections/dataset_<t0009_dataset_id>.json` (one or more correction files).
* If `file_changes` is needed: a replacement description document and/or replacement JSONL
  under this task's `assets/dataset/...-relabeled/` folder.
* `results/results_summary.md` reporting how many rows had their benchmark label corrected and
  the before/after distribution.
* `results/results_detailed.md` with the rationale, the correction-file structure, and any
  follow-up suggestion to actually replace the proxy rows with native WorkArena++/tau-bench
  data.

## Compute and Budget

No GPU. No API spend. Estimated cost: **$0**. Per-task cap: $1.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the dataset asset whose labels are being
  corrected.
* Independent of `t0014_v2_annotator_sonnet_rerun`. Order does not matter; if both land before
  t0012 finishes, t0012's per-benchmark reporting will pick up both overlays through the
  aggregator.
* `t0012` (in_progress) reads the t0009 dataset through the aggregator, so the corrected
  labels flow through automatically once t0015 merges. The FrontierScience filter t0012 uses
  is unaffected.

## Source Suggestion

`S-0009-06` variant b — "Relabel the proxy benchmarks WorkArena++→Mind2Web and
tau-bench→HumanEval in the v2 dataset via a correction file."

## Key Questions

1. How many rows are affected by each label correction?
2. Does the t0009 dataset aggregator support per-row label overlays via `changes`, or is a
   `file_changes` overlay needed?
3. Are there any downstream consumers (other than t0012) that already cache the original
   labels and would need re-aggregation?

**Results summary:**

> **Results Summary: Correct Proxy-Benchmark Labels in t0009 v2 Dataset**
>
> **Summary**
>
> Wrote a single corrections-overlay file
> (`corrections/dataset_hierarchical-annotation-v2.json`) that
> relabels the **52** rows in the t0009 v2 hierarchical-annotation dataset whose `benchmark`
> field
> referred to a gated proxy-target benchmark instead of the actual data source: **26** `m2w_*`
> rows
> move from `WorkArena++` to `Mind2Web`, and **26** `he_*` rows move from `tau-bench` to
> `HumanEval`.
> The `aggregate_datasets` overlay applies cleanly: the effective JSONL now carries the
> corrected
> labels and the dataset metadata prose no longer mentions the wrong benchmark names.
>
> **Metrics**
>
> * **Rows relabeled, total**: **52** of 115 (45.2%)
> * **`WorkArena++` -> `Mind2Web`**: **26** rows (all rows whose `task_id` starts with `m2w_`)
> * **`tau-bench` -> `HumanEval`**: **26** rows (all rows whose `task_id` starts with `he_`)
> * **Rows unchanged**: **63** (40 `FrontierScience-Olympiad` + 23 `SWE-bench Verified`)
> * **Effective JSONL distribution after overlay**: 40 / 23 / 26 / 26
>   (FrontierScience-Olympiad /
> SWE-bench Verified / Mind2Web / HumanEval)
> * **Non-`benchmark` field diffs vs source**: **0**

</details>

<details>
<summary>✅ 0014 — <strong>v2 annotator Sonnet rerun: deconfound schema vs
model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0014_v2_annotator_sonnet_rerun` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0009-01` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-04-30T19:07:28Z |
| **End time** | 2026-04-30T23:59:00Z |
| **Step progress** | 12/15 |
| **Task page** | [v2 annotator Sonnet rerun: deconfound schema vs model](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Task folder** | [`t0014_v2_annotator_sonnet_rerun/`](../../../tasks/t0014_v2_annotator_sonnet_rerun/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0014_v2_annotator_sonnet_rerun/results/results_detailed.md) |

# v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)

## Motivation

`t0009_hierarchical_annotation_v2` reports a v2-vs-v1 judge accept-rate delta of approximately
+58 pp on the stratified haiku-judged sample. The v1 annotator was `claude-sonnet-4-6`; the v2
annotator was switched to `claude-haiku-4-5-20251001` mid-task to fit the cost budget. The
judge model was constant (`claude-haiku-4-5-20251001`). The +58 pp number therefore conflates
two effects:

* schema effect: tree decomposition with subtask-to-atomic edges and full problem text;
* model effect: switching annotator from Sonnet to Haiku.

Without isolating the schema component, the headline claim that "v2 unblocks Phase 2" rests on
a load-bearing-but-unverified assumption. `t0012` (Phase 2 A/B/C smoke on FrontierScience) is
already in flight against the v2 dataset, so this deconfound is needed before any
per-benchmark numbers from t0012 can be reported. Implements `S-0009-01`.

## Scope

* Re-annotate the **same 115 rows** under the same v2 tree schema using `claude-sonnet-4-6` as
  the annotator.
* Use the **same prompt** as t0009 (full problem text, tree-schema system instructions).
* Judge with **the same `claude-haiku-4-5-20251001`** judge on the **same 23-row stratified
  sample** used in t0009 (same row IDs, same seed=42).
* Report per-benchmark and aggregate judge accept rate. Compare against v2-haiku and v1-sonnet
  to decompose the +58 pp delta into a schema component and a model component.
* Persist as a new `dataset` asset under `assets/dataset/hierarchical-annotation-v2-sonnet/`
  with `details.json`, `description.md`, and `files/hierarchical_annotation_v2_sonnet.jsonl`.

Out of scope: re-judging on a different sample, re-running v1 (already in t0005), changing the
schema, expanding row count, fixing the proxy-benchmark labels (handled by `t0015`).

## Approach

1. Read t0009's v2 dataset asset and the original 115 v1 rows from t0005's dataset asset.
2. Construct a v2 annotation prompt (identical to t0009's) with the full problem text and the
   v2 tree schema in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree
   per row.
3. Apply the same task_id deduplication fix used in t0009.
4. Recover the same stratified sample IDs from t0009's results (seed=42, stratified across
   FrontierScience-Olympiad, SWE-bench Verified, and the two proxy benchmarks). Run the haiku
   judge on the v2-sonnet hierarchies for those rows.
5. Persist the dataset asset with `annotation_model: "claude-sonnet-4-6"`. Annotate the
   `description.md` with the deconfound experimental design and the comparison protocol.
6. Compute the three accept-rate deltas:
   * v2-sonnet vs v1-sonnet → schema component (annotator constant).
   * v2-sonnet vs v2-haiku → annotator-model component (schema constant).
   * v2-haiku vs v1-sonnet → original t0009 headline (for sanity check).

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2-sonnet/{details.json, description.md, files/}`.
* `results/results_summary.md` reporting the three deltas with confidence intervals.
* `results/results_detailed.md` with per-row judge verdicts and per-benchmark breakdowns.
* `results/metrics.json` reporting `judge_accept_rate_v2_sonnet` (aggregate) plus
  per-benchmark variants if the metrics registry supports them.
* Follow-up suggestions if the schema component turns out to be small (motivating a v3 schema
  iteration) or the model swap dominates (motivating a Sonnet-default annotation policy).

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$5** (115 sonnet annotations at the same prompt
length as t0009's haiku run + 23 haiku judge calls reusing the same protocol). Per-task cap:
$10.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the v2 schema, the prompt, the stratified
  sample IDs, and the v2-haiku baseline accept rates.
* Independent of `t0015_correct_proxy_benchmark_labels`. Either order is fine, but if t0015
  lands first, this task should consume the corrected labels in its per-benchmark breakdown
  via the aggregator's correction overlay.
* `t0012` (in_progress) is unaffected — its FrontierScience filter and pre-locked v2 inputs do
  not change retroactively when this task lands.

## Source Suggestion

`S-0009-01` — "Re-run v2 annotation with claude-sonnet-4-6 to isolate the schema effect from
the annotator-model swap."

## Key Questions

1. What is the per-benchmark accept-rate delta of v2-sonnet vs v2-haiku (annotator-model
   component)?
2. What is the per-benchmark accept-rate delta of v2-sonnet vs v1-sonnet (schema component)?
3. Does the FrontierScience-Olympiad benchmark — the worst performer in v1 — improve under
   v2-sonnet? By how much vs the t0009 v2-haiku improvement?
4. If the schema component is small, is there a v3 schema change worth scoping, and should
   t0012's smoke be paused until that lands?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0014_v2_annotator_sonnet_rerun"
> date_completed: "2026-04-30"
> status: "complete"
> ---
> **Results Summary: v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)**
>
> **Summary**
>
> Re-annotated the same 115-row v1 pilot under the v2 tree schema with `claude-sonnet-4-6`,
> re-judged
> with the t0009 `claude-haiku-4-5` judge on the same seed-42 stratified sample (intersected
> to 20
> rows after 3 FrontierScience-Olympiad sonnet timeouts), and decomposed the t0009 +58 pp
> headline
> into a **+57 pp schema-only** delta and a **-1 pp model-only** delta. The annotator-model
> swap
> (haiku -> sonnet) contributes essentially zero of the t0009 gain; the v2 tree schema
> accounts for
> nearly all of it. Total cost $21.16 (annotator $19.77 + judge $1.40), within the
> user-authorised $25
> cumulative cap.
>
> **Metrics**
>

</details>

<details>
<summary>✅ 0013 — <strong>Brainstorm session 4: v2 schema-vs-model confound and
proxy-benchmark labels</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0013_brainstorm_results_4` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T18:00:00Z |
| **End time** | 2026-04-30T18:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 4: v2 schema-vs-model confound and proxy-benchmark labels](../../../overview/tasks/task_pages/t0013_brainstorm_results_4.md) |
| **Task folder** | [`t0013_brainstorm_results_4/`](../../../tasks/t0013_brainstorm_results_4/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0013_brainstorm_results_4/results/results_detailed.md) |

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

**Results summary:**

> **Brainstorm Session 4 — Results Summary**
>
> **Summary**
>
> Fourth brainstorm produced two new not-started tasks (t0014 and t0015) and applied eight
> correction
> files for the Round 2 cleanup deferred from brainstorm 3. The two tasks address the
> schema-vs-model
> confound and proxy-benchmark provenance issues surfaced by t0009. Wave budget cap: $10. Both
> new
> tasks are parallel-safe; t0012 stays in_progress and unaffected.
>
> **Session Overview**
>
> * **Date**: 2026-04-30
> * **Context**: Triggered after t0009-t0011 merged with $9.16 / $100 spent. t0012 is
>   in_progress.
> t0009 reported a +58 pp v2-vs-v1 judge accept rate but the annotation provider was swapped
> from
> Sonnet (v1) to Haiku (v2), so the headline delta is confounded with the model swap. The v2
> dataset
> also labels two proxy benchmarks under their proxy targets' names instead of the true source
> corpora.
> * **Prompt**: Resolve both pre-Phase-2 issues so t0012's headline experiment can rest on a
>   clean v2
> foundation, and prune the 17-suggestion high-priority backlog.
>

</details>

<details>
<summary>✅ 0012 — <strong>Phase 2 A/B/C smoke harness on FrontierScience
subset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_phase2_abc_smoke_frontierscience` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Expected assets** | 3 predictions, 1 library |
| **Source suggestion** | `S-0006-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **Start time** | 2026-04-30T00:55:11Z |
| **End time** | 2026-05-01T04:43:00Z |
| **Step progress** | 11/15 |
| **Key metrics** | Task Success Rate: **0.025** |
| **Task page** | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Task folder** | [`t0012_phase2_abc_smoke_frontierscience/`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0012_phase2_abc_smoke_frontierscience/results/results_detailed.md) |

# Phase 2 A/B/C Smoke Harness on FrontierScience Subset

## Motivation

This is the project's **first end-to-end Phase 2 result**. It tests the headline hypothesis on
a real benchmark for the first time: scope-aware (A) > scope-unaware (B) > scope-mismatched
(C). The smoke test is intentionally narrow — single benchmark (FrontierScience-Olympiad),
single provider (Anthropic Claude), N=28 hierarchy-complete rows from the v2 dataset, paired
across conditions. The goal is a directional signal plus a sample-size calibration for
follow-up confirmatory runs. Implements suggestions S-0006-03, S-0007-02, and S-0005-06.

## Hypotheses tested

| RQ | Predicted direction | Detection threshold at N=28 |
| --- | --- | --- |
| RQ1 — A success rate > B success rate | A − B ≥ +5pp | ~15pp paired (McNemar/sign test, α=0.05) |
| RQ2 — A overconfident error rate < B | A − B ≤ −2pp | ~5-8pp paired |
| RQ5 — C worst on Metrics 1 and 2 | C < min(A, B) on both | clear ranking when A > B + 5pp |

Excluded by design (handled in separate experiments on the right benchmarks):

* RQ3 (request-vs-act accuracy on low-level tasks) — needs tau-bench, not FrontierScience.
* RQ4 (gains concentrated in info-asymmetric states) — needs WorkArena++ or tool-using
  benchmark.

## Scope

* Build a small `phase2_smoke_harness_v1` library under `assets/library/` that:
  * Loads the v2 dataset asset from t0009 and filters to FrontierScience-Olympiad rows with
    `hierarchy_completeness == true`.
  * Runs a phase-order walk over each row's `hierarchy` (global → all subtasks → all
    `global_atomics`); for each step in the walk, dispatches to one of the three libraries (A:
    t0006, B: t0007, C: t0010).
  * Captures every step's trajectory record into one JSONL per condition under
    `assets/predictions/`.
  * Calls t0011's `compute_overconfident_error_rate` on each trajectory file.
  * Computes `task_success_rate` by parsing each trajectory's final `Finish` answer and
    comparing to the row's gold final answer (FrontierScience problems end with `FINAL ANSWER:
    ...`).
  * Reports `avg_decisions_per_task` per condition.
* Produce three `predictions` assets (one per condition: A, B, C).
* Produce one `library` asset for the harness itself.
* Run on the **28 hierarchy-complete FrontierScience-Olympiad rows** from the v2 dataset (this
  matches the v1 hierarchy-complete count; refine after t0009 lands if v2 row count differs).

Out of scope: multi-provider replication (deferred), benchmark-specific tool registries beyond
a minimal `python_exec` for FrontierScience math problems, scaling N beyond ~28.

## Approach

1. Read the v2 dataset asset from t0009 once t0009 has merged. Filter to FrontierScience-
   Olympiad and `hierarchy_completeness == true`.
2. Implement the harness library that drives the phase-order walk and dispatches
   per-condition. Reuse t0006, t0007, t0010 libraries; reuse t0011's calibration aggregator.
3. For each row, run all three conditions against the same model (`claude-sonnet-4-6-20251001`
   recommended) with paired execution (same seed where applicable, same problem text, same
   tool registry).
4. Tool registry is minimal: a single `python_exec` tool for arithmetic and one
   `Finish(answer)` tool. FrontierScience-Olympiad rows are mostly verbal reasoning; tools
   exist for explicit computation only.
5. Persist trajectory JSONLs under `assets/predictions/<condition>/files/`. Compute and
   persist metrics.
6. Write `results/results_summary.md` with the 3×3 condition × metric table and the predicted-
   versus-observed effect sizes. Write `results/results_detailed.md` with per-row trajectories
   summarised, the McNemar p-value for A-vs-B and B-vs-C, and the implied sample size for
   follow-up confirmatory runs.
7. Generate at least 2 charts: condition × metric bar chart with confidence intervals; per-row
   success matrix heatmap (rows=problems, columns=conditions).

## Expected Outputs

* `assets/library/phase2_smoke_harness_v1/` — the harness library.
* `assets/predictions/phase2_smoke_a/`, `assets/predictions/phase2_smoke_b/`,
  `assets/predictions/phase2_smoke_c/` — three predictions assets, one per condition.
* `results/metrics.json` in explicit-variant format (3 variants: A, B, C; metrics:
  `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`).
* `results/results_summary.md` and `results/results_detailed.md` with hypothesis-test results,
  effect sizes, sample-size calibration, and clear acknowledgement of the excluded RQs.
* `results/images/` with at least 2 charts.
* Follow-up suggestions for: multi-provider replication (Gemini, OpenAI), expansion to
  tool-using benchmarks (SWE-bench, tau-bench), confirmatory N expansion based on observed
  variance.

## Compute and Budget

No GPU. Anthropic API only. **Budget cap: USD 20** (per-task default cap is $10; this task
exceeds the default and explicitly opts up). Estimated breakdown: 28 rows × 3 conditions × ~3
self-consistency calls per step × ~6 steps per row × ~$0.005 per call = $7.5 baseline; budget
$20 leaves headroom for retries and the calibration prompt.

## Dependencies and Cross-References

* **Hard dependencies (must be `completed`)**:
  * `t0009_hierarchical_annotation_v2` — produces the v2 dataset asset this task consumes.
  * `t0010_matched_mismatch_library` — produces the C-condition library.
  * `t0011_metric2_calibration_aggregator` — produces the Metric 2 implementation.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  libraries.
* References Yao2022 ReAct, Wang2023 Plan-and-Solve, and Xiong2024 calibration paper assets
  from t0002.

## Source Suggestion

S-0006-03 — "Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience subset." Also
covers S-0007-02 and S-0005-06 by consolidation.

## Key Questions

1. Does A − B reach the +5pp threshold on `task_success_rate`?
2. Does A − B reach the −2pp threshold on `overconfident_error_rate`?
3. Does C rank strictly worst on both metrics relative to A and B?
4. What is the within-condition variance, and what N does the FrontierScience confirmatory run
   need to detect a 5pp effect at α=0.05 with paired test?
5. Are there per-domain (physics / chemistry / biology) effect-size differences worth
   surfacing to the next brainstorm?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0012_phase2_abc_smoke_frontierscience"
> ---
> **Results Summary — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)**
>
> **Summary**
>
> All three agent conditions (scope-aware ReAct A, scope-unaware Plan-and-Solve B,
> scope-mismatched
> Plan-and-Solve C) solved near-zero FrontierScience-Olympiad problems with claude-haiku-4-5
> and no
> tools: A solved 1/40 (2.5%), B solved 0/40, C solved 0/11 (budget halted at 11 rows). The
> paired
> McNemar test across the 6 fully overlapping rows yields p=1.0 for all pairs — the null is
> not
> rejected, and the smoke confirms that FrontierScience-Olympiad is beyond haiku capacity
> without tool
> use.
>
> **Metrics**
>
> * **task_success_rate**: A=0.025 (1/40), B=0.000 (0/40), C=0.000 (0/11)
> * **overconfident_error_rate**: A=0.647, B=0.000\*, C=0.000\* (\*collapsed — no
>   final_confidence in
> Plan-and-Solve trajectories; not comparable to A)

</details>

<details>
<summary>✅ 0011 — <strong>Metric 2 calibration aggregator: verbalized confidence
+ 3-sample self-consistency</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_metric2_calibration_aggregator` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:12Z |
| **End time** | 2026-04-29T23:43:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Task folder** | [`t0011_metric2_calibration_aggregator/`](../../../tasks/t0011_metric2_calibration_aggregator/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md) |

# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as
the canonical calibration protocol — verbalized confidence elicitation (low / medium / high +
brief justification) plus 3-sample self-consistency aggregation. Without this library, the
Phase 2 smoke test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the
diagnostic Metric 3 (avg decisions per task). This task unblocks the headline experiment by
producing a library that any agent's trajectory records can be passed through to compute
`overconfident_error_rate`. Implements suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/`
  exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low /
    medium / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem
    and returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is
    majority-vote on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float`
    that returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls
    the model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at
  `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` covering: prompt
  template formatting, parsing of low / medium / high confidence labels, majority-vote
  aggregation across 3 samples (including ties), threshold-based overconfident detection, and
  end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic
tests only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a
   `paths.py` and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold
  default rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration
  error) computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric
2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized
   labels mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default:
   prefer the highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results
   can include it in `metrics.json` directly?

**Results summary:**

> **Results Summary — Metric 2 Calibration Aggregator**
>
> **Summary**
>
> Implemented the metric2_calibration_aggregator_v1 library that operationalizes the project's
> Metric
> 2 (`overconfident_error_rate`) using the Xiong2024 §3.2 black-box calibration protocol. The
> library
> exposes `ConfidencePromptTemplate`, `ConfidenceJudge`, `elicit_confidence`,
> `compute_overconfident_error_rate`, and `CalibrationRecord` plus a trajectory-record
> adapter, with a
> single overridable threshold default (`HIGH_CONFIDENCE_THRESHOLD = 0.75`) and the canonical
> low/medium/high → 0.25/0.5/0.9 numeric mapping.
>
> **Metrics**
>
> * **Tests run**: 25 — all passed in 0.03 s
> (`uv run pytest tasks/t0011_metric2_calibration_aggregator/code/`).
> * **Code lines written**: ~340 in `code/calibration.py`, ~125 in `code/constants.py`, ~40 in
> `code/paths.py`, ~370 in `code/test_calibration.py` (test count includes the `ScriptedModel`
> fake).
> * **Public API surface**: 5 entry points required by the task description plus 1 helper
> (`calibration_record_from_trajectory`); 6 entry points listed in `details.json`.

</details>

<details>
<summary>✅ 0010 — <strong>Matched-mismatch library: condition C with deliberately
wrong granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0007-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:02Z |
| **End time** | 2026-04-29T23:46:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Matched-mismatch library: condition C with deliberately wrong granularity tags](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../../tasks/t0010_matched_mismatch_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0010_matched_mismatch_library/results/results_detailed.md) |

# Matched-Mismatch Library (Condition C)

## Motivation

The project's main hypothesis includes sub-hypothesis 2: scope-mismatched agents perform
strictly worse than both scope-aware (A) and scope-unaware (B) baselines. Without a C library,
research question 5 cannot be tested. This task implements C by wrapping the existing
libraries (`scope_aware_react_v1` from t0006 or `scope_unaware_planandsolve_v1` from t0007)
with a granularity-tag layer that emits **deliberately incorrect** tags at each step. The
library shares the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007 so a Phase 2 harness
can run all three conditions interchangeably. Implements suggestion S-0007-01.

## Scope

* Implement a library asset under `assets/library/matched_mismatch_v1/` exposing a
  `MatchedMismatchAgent` class that:
  * Accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
    registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`.
  * Walks the v2 hierarchy in phase order (the harness's canonical walk), determines the
    correct granularity at each step from the annotation, and **assigns an incorrect tag**
    according to the strategy:
    * `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`.
    * `adversarial`: always pick the most distant tag (`atomic` when correct is `global`,
      `global` when correct is `atomic`, `atomic` when correct is `subtask`).
  * Delegates each step to either `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`
    (configurable). The delegate handles the actual model call; the wrapper only controls the
    granularity tag.
  * Emits trajectory records in the canonical `TRAJECTORY_RECORD_FIELDS` schema, with the
    `granularity` field carrying the *wrong* tag (the actual correct tag is logged separately
    as `_correct_granularity` in an extras blob).
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` covering:
  random-strategy uniformity over `{global, subtask, atomic} \ correct_tag`,
  adversarial-strategy correctness, schema parity with t0007, end-to-end run with both
  delegate options.

Out of scope: the actual A/B/C experiment (handled by t0012), benchmark-specific tool
registries, remote execution.

## Approach

1. Read t0007's `scope_unaware_planandsolve_v1` library and t0006's `scope_aware_react_v1`
   library. Confirm the canonical trajectory schema is `TRAJECTORY_RECORD_FIELDS` from t0007.
2. Implement the library in `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
   Re-export the public API from `assets/library/matched_mismatch_v1/library/`.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests are deterministic (no live API calls). Use `ScriptedModel` from t0007 as the
   delegate's model.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/matched_mismatch_v1/` with `details.json`, `description.md`, `files/`.
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion to make the random-strategy mismatch ablation (uniform random vs.
  adversarial vs. matched) explicit in t0012.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  library assets. Reads `TRAJECTORY_RECORD_FIELDS` from t0007.

## Source Suggestion

S-0007-01 — "Implement matched-mismatch (C) library on top of scope_unaware_planandsolve_v1."

## Key Questions

1. What is the cleanest way to handle a granularity tag for steps that fall under
   `global_atomics` (cross-cutting atomics with no parent subtask)? Default: treat as `atomic`
   for the purposes of the mismatch strategy.
2. Should the wrapper expose a way to override the mismatch policy per-step (e.g., to inject
   targeted mismatches in specific phases)? Default: no, keep the wrapper minimal.
3. How should the schema's `_correct_granularity` extras field be standardised so a downstream
   experiment can compute the mismatch contribution per step?

**Results summary:**

> **Results Summary: Matched-Mismatch Library (Condition C)**
>
> **Summary**
>
> Implemented the project's condition-C library `matched_mismatch_v1` — a wrapper that walks
> the v2
> hierarchy from t0009 in canonical phase order, substitutes a deliberately incorrect
> granularity tag
> according to a `random` or `adversarial` strategy, and delegates the per-phase model call to
> either
> the t0006 ReAct or t0007 Plan-and-Solve format. The library reuses t0007's
> `TRAJECTORY_RECORD_FIELDS` schema unchanged and stores the correct tag in
> `extras["_correct_granularity"]`. All 14 deterministic tests pass and every `REQ-*`
> checklist item
> is satisfied.
>
> **Metrics**
>
> * **Tests passed**: 14 of 14 (`uv run pytest tasks/t0010_matched_mismatch_library/code/
>   -v`).
> * **Source lines (`matched_mismatch.py`)**: 463 lines including documentation and `__all__`
>   export
> list.
> * **Public API entry points**: 6 (`MatchedMismatchAgent`, `MatchedMismatchRecord`,
>   `AgentRunResult`,
> `Phase`, `iter_phases`, `pick_mismatch_tag`).
> * **Module-level constants exported**: 4 (`GRANULARITY_VALUES`, `ADVERSARIAL_MAP`,

</details>

<details>
<summary>✅ 0009 — <strong>Hierarchical annotation v2: tree schema with
subtask-to-atomic edges</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_hierarchical_annotation_v2` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T23:24:52Z |
| **End time** | 2026-04-30T00:53:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Hierarchical annotation v2: tree schema with subtask-to-atomic edges](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Task folder** | [`t0009_hierarchical_annotation_v2/`](../../../tasks/t0009_hierarchical_annotation_v2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md) |

# Hierarchical Annotation v2 (Tree Schema)

## Motivation

The v1 annotation produced by `t0005_hierarchical_annotation_pilot_v1` uses a flat schema:
`subtask` is a `list[str]`, `atomic` is a `list[str]`, and there is no encoded edge mapping
atomics to their parent subtask. The v1 schema also truncates problem text to 1500 characters
in the `task_excerpt` field, which the v1 LLM-as-judge identified as the dominant failure mode
on FrontierScience-Olympiad rows (0/3 accept rate). This task fixes both issues: re-annotates
all 115 rows under a tree-shaped v2 schema with full problem text, and spot-checks at least
20% of rows with the LLM judge to estimate quality. Implements suggestion S-0005-02 and the
partial v2-schema portion of S-0005-01.

## v2 Schema

```json
{
  "task_id": "...",
  "benchmark": "...",
  "domain": "...",
  "difficulty": { ... },
  "problem": "...",
  "hierarchy": {
    "global": "<one-sentence top-level approach>",
    "subtasks": [
      {
        "subtask": "<subtask description>",
        "atomics": ["<atomic step>", "..."]
      },
      ...
    ],
    "global_atomics": ["<cross-cutting atomic step>", "..."]
  },
  "gold_actions": {
    "global": "<resolved global action>",
    "subtasks": [
      {
        "subtask": "<resolved subtask action>",
        "atomics": ["<resolved atomic action>", "..."]
      },
      ...
    ],
    "global_atomics": ["<resolved cross-cutting atomic action>", "..."]
  },
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "...",
  "hierarchy_completeness": true | false
}
```

`global_atomics` captures atomic steps that do not belong to any single subtask (typically
verification, sanity checks, or cross-cutting concerns surfaced in v1's flat `atomic` list).

## Scope

* Re-run the v1 annotator (`claude-sonnet-4-6`) with a new prompt that elicits the tree schema
  above. Pass the **full problem text** (no `task_excerpt` truncation).
* Apply the same task_id deduplication fix from v1 (the source pilot file has 14 rows with
  colliding `task_id`s; thread `_pilot_row_index` through the asset).
* Spot-check at least 23 rows (20%) with `claude-haiku-4-5-20251001` as judge. Sample is
  stratified across the four benchmarks (FrontierScience-Olympiad, SWE-bench Verified,
  HumanEval-proxy, Mind2Web-proxy).
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical-annotation-v2/`
  with the schema above and a `description.md` explaining the v2 → v1 migration.
* Compare v2 vs v1 judge accept rate per benchmark and flag any benchmark where v2 fails to
  improve.

Out of scope: scaling beyond 115 rows (S-0005-01 expansion), human review (full review pass
deferred to v3), proxy benchmark replacement (deferred to follow-up).

## Approach

1. Read the v1 dataset `assets/dataset/hierarchical-annotation-v1/files/*.jsonl` from t0005
   and load all 115 rows.
2. For each row, construct a v2 annotation prompt with the full problem text and the v2 schema
   in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree.
3. Stratified-sample 23 rows. For each, call the haiku judge with the row's full problem and
   the proposed v2 hierarchy; capture verdict + one-sentence justification.
4. Persist as a `dataset` asset with `details.json` (source = t0005's v1 dataset asset,
   version = "v2", license inherited per row, sample count = 115) and
   `files/hierarchical_annotation_v2.jsonl`.
5. Report per-benchmark v2-vs-v1 judge accept rate delta in `results/results_detailed.md`.

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2/{details.json, description.md, files/}`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate vs v1.
* `results/results_detailed.md` with the full audit table, the v2-vs-v1 comparison, and any
  rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (mean atomics per row).
* Follow-up suggestions for: row-count expansion to ≥200, human review pass, proxy benchmark
  remediation, and any benchmark where v2 fails to improve over v1.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$15** (115 sonnet annotations + 23 haiku
judges). Per-task cap: $20.

## Dependencies and Cross-References

* No task dependencies. Reads t0005's v1 dataset asset as input but does not depend on the
  t0005 task being incomplete.
* References `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows, original).
* Sister-task coordination: t0012 will consume the v2 dataset; this task must publish the v2
  dataset asset before t0012's implementation step runs.

## Source Suggestion

S-0005-02 — "Re-run LLM-as-judge with full problem text (no truncation)." Also partially
addresses S-0005-01 (annotation v2 schema) and the schema-gap finding from brainstorm 3.

## Key Questions

1. What is the per-benchmark judge accept rate under v2 vs v1?
2. How does the v2 schema's tree shape affect FrontierScience-Olympiad acceptance specifically
   (the worst-performing benchmark in v1)?
3. Are there rows where the v2 tree decomposition is well-defined but the v1 flat
   decomposition was empty (hierarchy_completeness: false in v1)?
4. What fraction of atomics fall under `global_atomics` vs assigned to a specific subtask?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0009_hierarchical_annotation_v2"
> date_completed: "2026-04-30"
> status: "complete"
> ---
> **Results Summary: Hierarchical Annotation v2**
>
> **Summary**
>
> All 115 rows of the v1 hierarchical-annotation pilot were re-annotated under the v2 tree
> schema with
> `claude-haiku-4-5` and full problem text, achieving 115/115 hierarchy completeness and a
> 21/23 (91%)
> judge accept rate on the stratified spot-check. Per-benchmark v2-vs-v1 deltas are uniformly
> positive, ranging from +33% (SWE-bench Verified, tau-bench) to +100% (WorkArena++).
>
> **Metrics**
>
> * **avg_decisions_per_task** = **16.38** atomic actions per row across the 115-row v2
>   dataset (range
> 4-65, median 14). Tracks plan-length distribution.
> * **Per-benchmark v2 judge accept rate**: FrontierScience-Olympiad **67% (4/6)**, SWE-bench
>   Verified

</details>

<details>
<summary>✅ 0008 — <strong>Brainstorm session 3: insert v2 re-annotation, plan Phase
2 smoke</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0008_brainstorm_results_3` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T00:00:00Z |
| **End time** | 2026-04-30T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 3: insert v2 re-annotation, plan Phase 2 smoke](../../../overview/tasks/task_pages/t0008_brainstorm_results_3.md) |
| **Task folder** | [`t0008_brainstorm_results_3/`](../../../tasks/t0008_brainstorm_results_3/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0008_brainstorm_results_3/results/results_detailed.md) |

# Brainstorm Session 3

## Context

Wave 2 (t0004 brainstorm + t0005, t0006, t0007) merged at $0.06 total cost. The literature
survey, benchmark download, annotation pilot v1, and both scope-aware / scope-unaware
libraries are complete. The project is poised for the first Phase 2 result — but the v1
annotation schema has a structural gap that must be fixed first.

## Schema gap discovered

While modelling A/C condition prompts on the `is_bored` (HumanEval/91) row, we found that the
v1 annotation schema is **flat**: `subtask` is a list of strings, `atomic` is a list of
strings, and there is **no encoded edge** mapping atomics to their parent subtask. For the
`hierarchical-annotation-v1` smoke harness this forces one of three orderings — none of them
faithful to how humans actually reason hierarchically — and undermines the cleanliness of the
A-vs-B-vs-C contrast in the planned Phase 2 smoke test.

The fix is a tree-shaped v2 schema:

```json
{
  "hierarchy": {
    "global": "...",
    "subtasks": [
      {"subtask": "...", "atomics": ["...", "..."]},
      ...
    ],
    "global_atomics": ["..."]
  }
}
```

This change is **inserted as the new ASAP task** (t0009) before any of the previously-planned
wave 3 tasks can build on it.

## Decisions

Four new tasks created, all `not_started`. Three are parallel-safe; one waits on the others:

* `t0009_hierarchical_annotation_v2` (covers `S-0005-01` partial + `S-0005-02` + new schema
  finding) — re-annotate all 115 rows under the tree schema with full problem text. **No
  deps.**
* `t0010_matched_mismatch_library` (covers `S-0007-01`) — matched-mismatch (C) library; reuses
  t0007's `TRAJECTORY_RECORD_FIELDS`. Schema-independent. **No deps.**
* `t0011_metric2_calibration_aggregator` (covers `S-0002-02`) — Xiong2024
  verbalized-confidence + 3-sample self-consistency aggregator. Schema-independent. **No
  deps.**
* `t0012_phase2_abc_smoke_frontierscience` (covers `S-0006-03`, `S-0007-02`, `S-0005-06`) —
  first end-to-end Phase 2 A/B/C run on the FrontierScience subset of the **v2** dataset.
  **Deps**: t0009, t0010, t0011.

## Why this wave

Three tasks unblock the headline experiment:

* t0009 fixes the schema so the harness can drive granularity transitions naturally
  (depth-first by subtask in v2) instead of by an artificial phase walk over flat lists.
* t0010 provides the C condition without which RQ5 (sub-hypothesis 2) cannot be tested.
* t0011 implements Metric 2; without it the smoke test can only report Metric 1.

t0012 is the first run that produces a directional A/B/C signal on a real benchmark. It is
deliberately scoped as a smoke test (N=28 on hierarchy-complete FS-Olympiad rows, single
provider Anthropic, paired across conditions) rather than a definitive experiment. The
follow-up multi-provider replication (Gemini + OpenAI keys are now available) is queued for
the next brainstorm.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03; demoting four high-priority access/infrastructure suggestions to medium) —
  flagged earlier but explicitly deferred to keep this session focused on the v2 ASAP work.
* Multi-provider (Gemini, OpenAI) replication of the smoke test — deferred until t0012
  produces a single-provider headline result.
* Annotation v2 row-count expansion to ≥200 (covered by S-0005-01 in part; t0009 only
  re-encodes the existing 115 rows, not new annotation work).
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.

**Results summary:**

> **Brainstorm Session 3 — Results Summary**
>
> **Summary**
>
> Third brainstorm produced four new not-started tasks. The v1 annotation schema was found to
> lack
> subtask-to-atomic edges; a v2 re-annotation task was inserted ASAP as t0009. The original
> wave 3
> plan (matched-mismatch library, Metric 2 calibration, A/B/C smoke harness) was preserved and
> renumbered to t0010-t0012, with t0012 gated on the other three.
>
> **Session Overview**
>
> * **Date**: 2026-04-30
> * **Context**: Triggered after wave 2 (t0004-t0007) merged at $0.06 spend, with 27 uncovered
> suggestions and the v2 schema gap surfaced during prompt-modelling discussion of the
> `is_bored`
> annotation.
> * **Prompt**: Plan the first Phase 2 result on a real benchmark, with whatever schema
>   upgrades are
> needed to make the harness honest about the granularity transitions.
>
> **Decisions**
>

</details>

<details>
<summary>✅ 0007 — <strong>Scope-unaware Plan-and-Solve library: condition B
baseline</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-06` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:48Z |
| **End time** | 2026-04-29T20:01:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Scope-unaware Plan-and-Solve library: condition B baseline](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../../tasks/t0007_scope_unaware_planandsolve_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0007_scope_unaware_planandsolve_library/results/results_detailed.md) |

# Scope-Unaware Plan-and-Solve Library (Condition B)

## Motivation

The literature survey in t0002 identified Plan-and-Solve (Wang2023) as the strongest published
prompt-only baseline that does not condition on explicit granularity tags. It is therefore the
canonical scope-unaware (B) baseline for the project's A-vs-B-vs-C comparison. This task
produces the matching library asset, sharing the trajectory-log schema with t0006 so a Phase 2
experiment can run both libraries against the same harness without bespoke glue. Implements
suggestion S-0002-06.

## Scope

* Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
  `PlanAndSolveAgent` class that:
  * Accepts a problem statement, a tool registry, and a model-call callable.
  * Generates a free-form numbered plan, then executes each step sequentially through a
    Plan-and-Execute loop.
  * Emits trajectory records in the same schema as `scope_aware_react_v1` so both libraries
    are drop-in interchangeable. The `granularity` field in the schema is filled with the
    literal string `"unspecified"` to mark the B condition.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}`.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing
  from scratch. License is Apache 2.0; record attribution in `description.md`.
* Provide pytest coverage at
  `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` covering: plan
  parsing, sequential execution, trajectory schema parity with t0006, finish detection, and
  error recovery on malformed model output.

Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
execution.

## Approach

1. Read t0002's Wang2023 paper summary and the LangChain Plan-and-Execute source to ground the
   prompt template and execution loop.
2. Implement the library in
   `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and re-export the
   public API from `assets/library/scope_unaware_planandsolve_v1/library/`.
3. Reuse the trajectory log schema defined in t0006 by reading t0006's library when it lands;
   if t0006 has not landed yet, define the schema here and document that t0006 must conform.
4. Write `details.json`, `description.md`, and `files/` for the asset.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_unaware_planandsolve_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for the matched mismatch (C) library.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. May reference t0006's library if it merges first; otherwise this task
  defines the trajectory schema and t0006 must conform.
* References Wang2023 paper asset (`10.48550_arXiv.2305.04091`) from t0002.

## Source Suggestion

S-0002-06 — "Implement Plan-and-Solve as the canonical scope-unaware (B) baseline."

## Key Questions

1. What plan format does Plan-and-Solve produce, and how should it be parsed
   deterministically?
2. How should the library mark the absence of a granularity tag in the trajectory record?
3. What is the minimal API surface that lets a Phase 2 harness swap between this and t0006's
   library by changing only one line?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0007_scope_unaware_planandsolve_library"
> date_completed: "2026-04-29"
> ---
> **Results Summary — t0007_scope_unaware_planandsolve_library**
>
> **Summary**
>
> Produced one library asset, `scope_unaware_planandsolve_v1`, that adapts LangChain's
> Plan-and-Execute reference implementation of Wang et al.'s Plan-and-Solve prompting (arXiv
> 2305.04091) as the canonical scope-unaware (B) baseline for the project. The library passes
> its
> asset verificator and a 14-case pytest suite, all without any paid API calls.
>
> **Metrics**
>
> * **Library tests passing**: **14 / 14** (zero failures)
> * **Ruff errors on task code**: **0**
> * **Mypy errors on task code**: **0**
> * **Library asset verificator errors / warnings**: **0 / 0**

</details>

<details>
<summary>✅ 0006 — <strong>Scope-aware ReAct library: condition A with explicit
granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-07` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:38Z |
| **End time** | 2026-04-29T20:07:30Z |
| **Step progress** | 10/15 |
| **Task page** | [Scope-aware ReAct library: condition A with explicit granularity tags](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../../tasks/t0006_scope_aware_react_library/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0006_scope_aware_react_library/results/results_detailed.md) |

# Scope-Aware ReAct Library (Condition A)

## Motivation

The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a `{global, subtask, atomic}` granularity tag emitted at every Thought /
Action turn, plus a logging hook that records the active tag alongside the model's confidence.
The library is the substrate every Phase 2 A-condition experiment will import. Implements
suggestion S-0002-07.

## Scope

* Implement a library asset under `assets/library/scope_aware_react_v1/` exposing a
  `ScopeAwareReactAgent` class that:
  * Accepts a problem statement, a fixed `granularity` argument (`"global" | "subtask" |
    "atomic"`), a tool registry, and a model-call callable.
  * Loops Thought / Action / Observation steps, prepending the active granularity tag to every
    Thought emission, and parses Action JSON until the agent emits a `Finish` action.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}` to
    a JSONL trajectory file the experiment harness can replay.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` covering: tag
  injection, action parsing, finish detection, error recovery on malformed JSON, and
  trajectory logging integrity.

Out of scope: the actual A-vs-B-vs-C experiment (a separate experiment-run task), benchmark-
specific tool registries (also a separate task), and any remote-execution wiring.

## Approach

1. Read t0002's `research/research_papers.md` and the Yao2022 paper summary to ground the
   prompt format. Reuse LangChain's ReAct prompt where appropriate; the project licence is
   Apache 2.0.
2. Implement the library in `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`
   and re-export the public API from a `library/__init__.py` shim under `assets/library/
   scope_aware_react_v1/`.
3. Write the asset's `details.json`, `description.md`, and `files/` directory with the
   runnable source.
4. Write tests as deterministic unit tests; no live API calls.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_aware_react_v1/` with `details.json`, `description.md`, and `files/`.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` and matching test file.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for benchmark-specific tool registries.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Yao2022 paper asset (`10.48550_arXiv.2210.03629`) from t0002.
* Sister task `t0007_scope_unaware_planandsolve_library` produces the matched B baseline; both
  must follow the same trajectory-logging schema so a Phase 2 experiment can consume both.

## Source Suggestion

S-0002-07 — "Implement scope-aware (A) as ReAct extended with explicit granularity tags."

## Key Questions

1. What is the minimal extension to ReAct's prompt template that reliably elicits a
   granularity tag on every Thought emission?
2. How should the library handle a model that refuses to emit a tag (back off, abort, or
   default to `atomic`)?
3. What schema for the trajectory log lets t0007 emit identical-shape records?

**Results summary:**

> **Results Summary: Scope-Aware ReAct Library**
>
> **Summary**
>
> Shipped the project's first library asset: `scope_aware_react_v1`, implementing condition A
> (scope-aware ReAct) with explicit `{global, subtask, atomic}` granularity tags, a JSONL
> trajectory
> writer whose six-field schema is the canonical contract for both this library and t0007, and
> deterministic-replay testing via `ScriptedModel`. All quality gates clean and the asset
> verificator
> passed.
>
> **Metrics**
>
> * **Library asset**: 1 (`scope_aware_react_v1`), passes
>   `meta.asset_types.library.verificator` with
> **0 errors / 0 warnings**.
> * **Tests**: **8 / 8** passing in `code/test_scope_aware_react.py`
> (`pytest tasks/t0006_scope_aware_react_library/code/ -v` reported all tests passing).
> * **Source files**: **3 modules** in `code/` (`scope_aware_react.py` ~370 lines,
>   `constants.py`,
> `paths.py`) plus 1 test file.
> * **Public entry points**: **6** (`ScopeAwareReactAgent`, `ScriptedModel`,
>   `TrajectoryRecord`,
> `Action`, `AgentResult`, `MalformedActionError`).

</details>

<details>
<summary>✅ 0005 — <strong>Hierarchical annotation pilot v1: audit and conform
existing 115 rows</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_hierarchical_annotation_pilot_v1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0002-08` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T19:35:28Z |
| **End time** | 2026-04-29T20:14:30Z |
| **Step progress** | 9/15 |
| **Task page** | [Hierarchical annotation pilot v1: audit and conform existing 115 rows](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Task folder** | [`t0005_hierarchical_annotation_pilot_v1/`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0005_hierarchical_annotation_pilot_v1/results/results_detailed.md) |

# Hierarchical Annotation Pilot v1

## Motivation

Phase 1 of the project's roadmap requires ≥100 tasks fully annotated with gold actions at
three granularity levels (global / subtask / atomic). The imported
`project/data/annotation_pilot/ tasks_annotated.jsonl` already contains 115 LLM-annotated
rows, but the rows have not been verified to conform to the project's three-level schema and
there is no human or LLM-as-judge spot-check pass on record. This task closes that gap in v1
form: keep the existing 115 rows in place, audit their structure, and produce a canonical
dataset asset that downstream Phase 2 / 3 experiments can consume. Implements suggestion
S-0002-08.

## Scope

* Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on
  each row to determine whether it carries explicit global / subtask / atomic granularity
  labels or whether the granularity must be inferred.
* If labels are missing, write a deterministic mapper that derives the three-level structure
  from the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block
  per row.
* Run an LLM-as-judge spot-check on at least 10% of rows (≥12 rows) to estimate hierarchy
  quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/`
  with rows of shape `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask,
  atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict,
  judge_notes}`.

Out of scope for v1: replacing the HumanEval and Mind2Web proxies, expanding beyond 115 rows,
human review, inter-rater agreement studies. All deferred to follow-up tasks.

## Approach

1. Load the 115-row pilot file. For each row, compute the inferred or stated hierarchy and
   emit the canonical schema record.
2. Sample at least 12 rows stratified across the four benchmarks (FrontierScience-Olympiad,
   SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Send each to the LLM judge with the
   row's problem text and proposed hierarchy; capture verdict ("acceptable" / "needs
   revision") plus a one-sentence justification.
3. Persist the consolidated dataset asset with `details.json` (source URL = the imported pilot
   path, version = "v1", license = inherited from each upstream benchmark, sample count = 115)
   and `files/hierarchical_annotation_v1.jsonl`.
4. Report distribution stats in `results/results_detailed.md` (per-benchmark counts,
   per-domain counts, hierarchy-completeness rate, judge accept rate).

## Expected Outputs

* `assets/dataset/hierarchical_annotation_v1/` with `details.json`, `files/`, and a
  `description.md`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate.
* `results/results_detailed.md` with the full audit table and any rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (the registered diagnostic
  metric).
* Follow-up suggestions for: extension to ≥200 rows, full human-review pass, and proxy
  benchmark remediation.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: under 3 USD for 12-15 LLM-as-judge calls on
`claude-haiku-4-5-20251001`. Per-task cap: 5 USD.

## Dependencies and Cross-References

* No task dependencies.
* Reads `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows).
* Reads `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules — wrap
  as black-box utilities, never modify in place.
* References the four benchmark dataset assets produced by `t0003_download_benchmark_subsets`.

## Source Suggestion

S-0002-08 — "Run a Phase 1 pilot annotation on 20 tasks before scaling to 100." This task
implements that idea in v1 form, leveraging the existing 115 rows rather than re-annotating
from scratch.

## Key Questions

1. Do the existing 115 rows already carry a global / subtask / atomic decomposition, or must
   one be inferred?
2. What is the per-benchmark hierarchy-completeness rate?
3. What is the LLM-as-judge accept rate? Does it differ across benchmarks?
4. Are there systematic patterns in rejected rows (e.g., one benchmark consistently failing)?

**Results summary:**

> **Results Summary: Hierarchical Annotation Pilot v1**
>
> **Summary**
>
> Audited the 115-row pilot annotation file, projected each row's `steps.nodes` graph onto the
> project's three-level global / subtask / atomic schema with a deterministic Python mapper,
> ran an
> LLM-as-judge spot-check on a 12-row stratified sample using `claude-haiku-4-5-20251001` via
> the
> local `claude` CLI, and produced a single canonical `hierarchical-annotation-v1` dataset
> asset (115
> rows). The asset passes the dataset verificator with 0 errors and 1 warning.
>
> **Metrics**
>
> * **Rows in dataset**: **115** (FrontierScience-Olympiad **40**, SWE-bench Verified **23**,
> tau-bench **26**, WorkArena++ **26**)
> * **Overall hierarchy completeness**: **88.7%** (102 / 115 rows have a non-null `global` and
>   a
> non-empty `atomic` list)
> * **Per-benchmark completeness**: FrontierScience-Olympiad **70.0%** (28/40), SWE-bench
>   Verified
> **100.0%** (23/23), tau-bench **96.2%** (25/26), WorkArena++ **100.0%** (26/26)
> * **LLM-as-judge accept rate (overall)**: **33.3%** (4/12 rows accepted)
> * **Per-benchmark judge accept rate**: FrontierScience-Olympiad **0.0%** (0/3), SWE-bench
>   Verified

</details>

<details>
<summary>✅ 0004 — <strong>Brainstorm session 2: plan Phase 1 annotation and Phase
2 baseline libraries</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_brainstorm_results_2` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T15:30:00Z |
| **End time** | 2026-04-29T15:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 2: plan Phase 1 annotation and Phase 2 baseline libraries](../../../overview/tasks/task_pages/t0004_brainstorm_results_2.md) |
| **Task folder** | [`t0004_brainstorm_results_2/`](../../../tasks/t0004_brainstorm_results_2/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0004_brainstorm_results_2/results/results_detailed.md) |

# Brainstorm Session 2

## Context

Second brainstorm session. The first wave (t0001 brainstorm + t0002 literature survey + t0003
benchmark download) completed at $0 cost. Three completed tasks have produced 11 paper assets,
4 dataset assets, and 15 uncovered follow-up suggestions.

Key findings carried into this session:

* **Literature survey (t0002)** identified Plan-and-Solve [Wang2023] as the canonical
  scope-unaware (B) baseline, ReAct [Yao2022] as the foundation for the scope-aware (A)
  condition, and Xiong2024 as the calibration protocol for Metric 2.
* **Benchmark download (t0003)** confirmed FrontierMath (gated by Epoch AI) and WorkArena++
  (gated by ServiceNow + HF) cannot be unblocked by infrastructure work in the current
  session. Pilot proxies are frozen as fallback. SWE-bench Verified and tau-bench are
  accessible.
* The deferred T3 candidate from session 1 (`hierarchical_annotation_pilot`) is now
  appropriate to schedule, but in a smaller v1 form: audit and conform the existing 115 pilot
  rows rather than attempt a full re-annotation.

## Decisions

Three new tasks created, all `not_started`, no inter-task dependencies (parallel-safe):

* `t0005_hierarchical_annotation_pilot_v1` (covers `S-0002-08`) — audit & conform the existing
  pilot annotations to the global / subtask / atomic schema.
* `t0006_scope_aware_react_library` (covers `S-0002-07`) — write-library: ReAct extended with
  granularity tags. Implements the A condition.
* `t0007_scope_unaware_planandsolve_library` (covers `S-0002-06`) — write-library:
  Plan-and-Solve adapted from LangChain. Implements the B condition.

## Why this wave

t0005 unblocks Phase 1 (annotation deliverable). t0006 + t0007 are the two libraries the Phase
2 baseline experiment will consume. Once all three are merged, the Phase 2 smoke-test
experiment (deferred T4 from session 1) becomes practical to schedule.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03) is intentionally deferred to a follow-up session.
* SWE-bench Docker harness (S-0002-05) is deferred until experiment tasks need it.
* FrontierMath (S-0002-04 / S-0003-01) and ServiceNow (S-0002-03 / S-0003-02) access remain
  open high-priority blockers but not on the path to first Phase 2 results.

**Results summary:**

> **Brainstorm Session 2 — Results Summary**
>
> **Summary**
>
> Second brainstorm produced three new not-started tasks for parallel execution: a v1
> hierarchical
> annotation pilot and two baseline libraries (ReAct+tags for the A condition, Plan-and-Solve
> for the
> B condition). Round 2 suggestion cleanup deferred to a follow-up session.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Triggered after t0001-t0003 wave completed at $0 spend, with 15 uncovered
>   suggestions
> queued.
> * **Prompt**: Plan Phase 1 annotation deliverable and the libraries Phase 2 baseline
>   experiment will
> need.
>
> **Decisions**
>
> 1. **Create `t0005_hierarchical_annotation_pilot_v1`** (covers `S-0002-08`,
> `hierarchical-annotation`). Audit and conform the 115 existing pilot rows to the global /
> subtask

</details>

<details>
<summary>✅ 0003 — <strong>Download benchmark subsets for the four roadmap
sources</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_download_benchmark_subsets` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 4 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../../meta/task_types/download-dataset/) |
| **Start time** | 2026-04-29T14:30:55Z |
| **End time** | 2026-04-29T14:58:30Z |
| **Step progress** | 8/15 |
| **Task page** | [Download benchmark subsets for the four roadmap sources](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Task folder** | [`t0003_download_benchmark_subsets/`](../../../tasks/t0003_download_benchmark_subsets/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0003_download_benchmark_subsets/results/results_detailed.md) |

# Download Benchmark Subsets

## Motivation

Phase 1 (annotation) and Phase 2 (baseline scope-aware vs. scope-unaware experiment) both
depend on having local, reproducible subsets of the four roadmap benchmarks. The existing
pilot annotation data uses HumanEval and Mind2Web proxies for tau-bench and WorkArena++
because the real benchmarks were "unavailable on HF" at original-annotation time. This task
either resolves that gap by acquiring the real benchmarks or, if access is genuinely
unavailable, documents the decision to keep proxies and freezes the choice for Phase 2.

## Scope

Acquire four benchmark subsets, each targeted at multi-step tasks of 4-8 decisions per task to
match the project's stated difficulty range:

* FrontierScience-Olympiad — full official distribution path; subset by domain to match the
  pilot's physics / chemistry / biology focus.
* WorkArena++ — official distribution. If genuinely inaccessible (gated, retired, dataset
  moved), document the access attempt and keep the Mind2Web proxy already present in the
  pilot.
* SWE-bench Verified — official Princeton/HF distribution; subset to instances that map
  cleanly onto the project's three-level hierarchy.
* tau-bench — official distribution. If genuinely inaccessible, keep the HumanEval proxy with
  documented justification.

Out of scope: full benchmark execution harnesses (those belong in later experiment-run tasks),
custom annotation (that belongs in T3 hierarchical-annotation pilot), and modifications of
benchmark data (subsetting only, no relabelling).

## Approach

1. For each benchmark, attempt the official distribution path documented in its source paper
   or GitHub README. Cache successful downloads under the task's
   `assets/dataset/<slug>/files/`.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata
   the benchmark provides. If no such metadata exists, sample uniformly and document the
   sampling seed.
3. Produce one dataset asset per benchmark with `details.json` describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log to the dataset asset's
   `details.json` with `download_status: "failed"` and a clear `download_failure_reason`. The
   project's policy in this case is to keep the existing pilot proxy and not block on access.
5. Emit follow-up suggestions for any benchmark whose access pathway is non-obvious or whose
   subsetting choice deserves a Phase 2 sensitivity check.

## Expected Outputs

* Four dataset assets under
  `assets/dataset/{frontierscience,workarena_plus_plus,swebench_verified, taubench}/` with
  `details.json` and `files/` directories (or empty `files/` plus a clear failed status if
  inaccessible).
* `results/results_summary.md` with a per-benchmark access status, sample count, and any
  subset decisions.
* `results/suggestions.json` flagging any benchmarks where the proxy choice is now permanent.

## Compute and Budget

No GPU. No paid API calls anticipated. All work is local downloads and metadata writing.
Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. Independent of T1.
* Cross-references: existing pilot annotation data at
  `project/data/annotation_pilot/tasks_annotated.jsonl` documents the proxy decisions this
  task must either resolve or formalise.

**Results summary:**

> **Results Summary: Download Benchmark Subsets**
>
> **Summary**
>
> Acquired four benchmark subsets covering the project's roadmap sources
> (FrontierScience-Olympiad,
> WorkArena++, SWE-bench Verified, tau-bench). Three were downloaded directly from public
> sources;
> WorkArena++ instance enumeration is gated on a live ServiceNow developer instance, so its
> asset
> captures the upstream curriculum manifest only and freezes the Mind2Web pilot proxy as the
> de-facto
> Phase 2 fallback. All four dataset assets pass `verify_dataset_asset` with zero errors.
>
> **Metrics**
>
> * **4 of 4** dataset assets created and passing `verify_dataset_asset` (zero errors, zero
>   warnings).
> * **FrontierScience-Olympiad subset**: **40** problems (15 physics, 10 chemistry, 15
>   biology),
> packaged from pilot rows; status **success** (FrontierMath upstream still gated).
> * **WorkArena++ subset**: **42** compositional task class lists extracted from upstream
> `curriculum.py`; status **success (manifest only)**, instance enumeration deferred and
> Mind2Web
> pilot proxy frozen.
> * **SWE-bench Verified subset**: **60** instances filtered from **500** Verified using the
>   4-8 hunks
> rule; status **success**.

</details>

<details>
<summary>✅ 0002 — <strong>Literature survey: granularity conditioning and
hierarchical agents</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_granularity_conditioning` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 10 paper |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-29T13:50:47Z |
| **End time** | 2026-04-29T14:26:49Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: granularity conditioning and hierarchical agents](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Task folder** | [`t0002_literature_survey_granularity_conditioning/`](../../../tasks/t0002_literature_survey_granularity_conditioning/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0002_literature_survey_granularity_conditioning/results/results_detailed.md) |

# Literature Survey: Granularity Conditioning and Hierarchical Agents

## Motivation

The project's central hypothesis is that explicitly conditioning an LLM agent on its current
operating granularity (global / subtask / atomic) improves task success, calibration, and
request-vs-act discrimination. Before designing the Phase 2 baseline experiment we need
literature grounding on three threads: how prior work has framed and operationalised
"granularity" or "scope" labels for hierarchical agents, what hierarchical task decomposition
schemas exist in the four benchmark sources, and which uncertainty-calibration metrics have
been used in agent settings (in particular, definitions and prior measurements of the
overconfident error rate). The survey output anchors every later planning decision and lets us
cite prior work in the Phase 4 paper-ready report.

## Scope

* Granularity / scope / scale conditioning in LLM agents and prompt engineering. Include any
  work that varies the level of abstraction at which an agent receives its instructions, even
  if the authors do not use the word "granularity".
* Hierarchical task decomposition: papers proposing two-, three-, or n-level decompositions
  for benchmarks similar to those in this project (FrontierScience-Olympiad, WorkArena++,
  SWE-bench Verified, tau-bench).
* Uncertainty calibration in LLM agents: confidence elicitation methods, definitions of
  overconfident error rate, calibration plots and metrics, and prior reports on how
  calibration changes with prompt design.
* The four roadmap benchmarks themselves: their official task structures, scoring conventions,
  and any published results that bracket what counts as competitive performance.

Out of scope: training-time techniques (RL, gradient-based fine-tuning), non-English
benchmarks, production deployment papers — all consistent with the project's Out of Scope
section.

## Approach

1. Run the standard `/research-papers` and `/research-internet` stages with the three thread
   queries above. Use the `download-paper` skill for any candidate paper found via search.
2. Produce paper assets under `assets/paper/` for at least 10 highly relevant papers, each
   with a summary that conforms to the paper asset specification.
3. Aggregate findings into `research/research_papers.md` with a section per thread:
   granularity conditioning, hierarchical decomposition, calibration metrics, benchmark
   grounding.
4. Connect each thread back to the project's research questions and explicitly flag (a) any
   prior work that already answers a research question, (b) any methodological choices the
   survey resolves for Phase 2, and (c) any open questions to surface as suggestions.

## Expected Outputs

* At least 10 paper assets under `assets/paper/<paper_id>/` with `details.json`, summary, and
  PDF or markdown file.
* `research/research_papers.md` and `research/research_internet.md` synthesising the survey.
* `results/results_summary.md` with a thread-by-thread takeaway and explicit follow-up
  suggestions for the next brainstorm session (typically: which benchmarks to deprioritise,
  which conditioning prompts to adopt, which calibration metric to register as a project
  metric).
* `results/suggestions.json` with concrete follow-up ideas surfaced by the survey.

## Compute and Budget

No GPU. Anthropic API only (the project's `available_services` list dropped `openai_api` until
an API key is provided). Estimated cost: under 5 USD for paper summarisation through Claude.

## Dependencies and Cross-References

* No task dependencies. Independent of T2.
* Reads `project/description.md` for research questions and success criteria.
* The project's pre-existing `project/data/annotation_pilot/tasks_annotated.jsonl` should be
  inspected during the survey to ground discussion of benchmark coverage.

## Key Questions

1. What prior work explicitly compares scope-aware vs. scope-unaware vs. scope-mismatched LLM
   agents on multi-step benchmarks, and what effect sizes did they report?
2. What definitions of "overconfident error rate" exist in the agent calibration literature,
   and which is most appropriate for our Metric 2 specification?
3. What hierarchical decomposition schemas are already published for FrontierScience-Olympiad,
   WorkArena++, SWE-bench Verified, and tau-bench, and how do they map to our global / subtask
   / atomic split?
4. Are the WorkArena++ and tau-bench benchmarks truly inaccessible (as the existing pilot data
   suggests), or are there standard distribution channels we missed?

**Results summary:**

> **Results Summary: Literature Survey on Granularity Conditioning and Hierarchical Agents**
>
> **Summary**
>
> Completed a literature survey of 11 papers covering granularity / scope conditioning of LLM
> agents,
> hierarchical task decomposition, uncertainty calibration, and the four roadmap benchmarks
> (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). All 11 paper assets
> pass the
> v3 paper-asset verificator and are tagged with project categories.
>
> **Metrics**
>
> * **11 paper assets created** out of a 10-paper minimum target — exceeds REQ-1 by one paper.
> * **4 of 4 survey threads covered** with at least 2 papers each: granularity / hierarchical
> prompting (Yao2022, Wang2023, Shinn2023, Zhou2022, Wei2022 noted but not added in this round
> — 4
> added), four roadmap benchmarks (Glazer2024, Drouin2024, Boisvert2024, Jimenez2024,
> OpenAI2024,
> Yao2024 — 6 added), calibration (Xiong2024 — 1 added).
> * **0 errors** across 11 verificator runs; 1 minor warning (PA-W007 missing-country) on the
>   first
> paper, fixed by adding country codes.
>
> **Verification**

</details>

<details>
<summary>✅ 0001 — <strong>Brainstorm session 1: plan first project tasks</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0001_brainstorm_results_1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T00:00:00Z |
| **End time** | 2026-04-29T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 1: plan first project tasks](../../../overview/tasks/task_pages/t0001_brainstorm_results_1.md) |
| **Task folder** | [`t0001_brainstorm_results_1/`](../../../tasks/t0001_brainstorm_results_1/) |
| **Detailed report** | [results_detailed.md](../../../tasks/t0001_brainstorm_results_1/results/results_detailed.md) |

# Brainstorm Session 1

## Context

This is the first brainstorm session for the granularity-aware hierarchical agents project,
executed inline as part of `/setup-project` immediately after `meta/` was populated. The
project has no completed tasks, no suggestions, and no answer assets, so the session focused
on Round 1 (propose first tasks). Rounds 2 (suggestion cleanup) and 3 (confirmation) had
nothing to clean up and proceeded straight to confirmation.

## Decisions

The researcher accepted two child tasks for immediate creation:

* `t0002_literature_survey_granularity_conditioning` — survey papers on granularity / scope /
  scale conditioning in LLM agents, hierarchical task decomposition, and uncertainty
  calibration metrics.
* `t0003_download_benchmark_subsets` — wire up access to subsets of the four roadmap
  benchmarks (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench) at
  difficulty 4-8 decisions per task.

Two further candidate tasks (`hierarchical_annotation_pilot` and
`baseline_scope_experiment_smoke_test`) were discussed in detail but deferred — the researcher
will review T1 and T2 outputs before committing.

## Why these tasks first

T1 and T2 are independent and low-cost. T1 anchors later planning decisions in the literature;
T2 unblocks every Phase 1 annotation extension and every Phase 2/3 experiment. Running them in
parallel keeps the project moving while preserving the option to redirect after the literature
survey.

## Out-of-band notes

* `project/data/annotation_pilot/tasks_annotated.jsonl` already contains 115 LLM-annotated
  rows, but tau-bench and WorkArena++ rows use HumanEval and Mind2Web proxies because the real
  benchmarks were "unavailable on HF" at original-annotation time. T2 must address this
  directly.
* The `available_services` list dropped `openai_api` during setup because no API key was
  provided; `anthropic_api` remains. T1 and T2 should plan their LLM use accordingly.

**Results summary:**

> **Brainstorm Session 1 — Results Summary**
>
> **Summary**
>
> The first brainstorm session for the granularity-aware hierarchical agents project produced
> two new
> not-started tasks (literature survey and benchmark download) and deferred two further
> candidates
> pending the literature-survey output. No suggestions, corrections, or answer assets were
> produced;
> the project is brand new and the suggestion backlog is empty.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Inline brainstorm executed by `/setup-project` immediately after `meta/` was
> populated. Project repository was a fresh fork of the Glite ARF template.
> * **Prompt**: Translate the project description and four-phase roadmap into concrete first
>   tasks the
> researcher can launch.
>
> **Decisions**
>
> 1. **Create `t0002_literature_survey_granularity_conditioning`**. Survey the literature on

</details>
