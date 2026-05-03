# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0033 — <strong>Realign t0031 suggestions and t0029 status under
no-Anthropic constraint</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0033_realign_t0031_t0029_no_anthropic` |
| **Status** | not_started |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`correction`](../../../meta/task_types/correction/) |
| **Task page** | [Realign t0031 suggestions and t0029 status under no-Anthropic constraint](../../../overview/tasks/task_pages/t0033_realign_t0031_t0029_no_anthropic.md) |
| **Task folder** | [`t0033_realign_t0031_t0029_no_anthropic/`](../../../tasks/t0033_realign_t0031_t0029_no_anthropic/) |

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

<details>
<summary>⏹ 0032 — <strong>No-Anthropic RQ1 path decision</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0032_no_anthropic_rq1_path_decision` |
| **Status** | not_started |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md), [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [No-Anthropic RQ1 path decision](../../../overview/tasks/task_pages/t0032_no_anthropic_rq1_path_decision.md) |
| **Task folder** | [`t0032_no_anthropic_rq1_path_decision/`](../../../tasks/t0032_no_anthropic_rq1_path_decision/) |

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

</details>

<details>
<summary>⏹ 0030 — <strong>RQ4 info-asymmetry stratification analysis on t0029
outputs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0030_rq4_info_asymmetry_stratification` |
| **Status** | not_started |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0029_rq1_discordance_rich_resample`](../../../overview/tasks/task_pages/t0029_rq1_discordance_rich_resample.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [RQ4 info-asymmetry stratification analysis on t0029 outputs](../../../overview/tasks/task_pages/t0030_rq4_info_asymmetry_stratification.md) |
| **Task folder** | [`t0030_rq4_info_asymmetry_stratification/`](../../../tasks/t0030_rq4_info_asymmetry_stratification/) |

# RQ4 Info-Asymmetry Stratification Analysis

## Motivation

RQ4 asks: **does the gain from granularity-aware scope conditioning concentrate in instances
where information asymmetry between the agent and the task is highest?**

t0027 produced suggestive but underpowered evidence: per-subset success rates were
A=0/B=0.012/C=0.036 on taubench and A=0/B=0.192/C=0.154 on frontsci, hinting that gains might
concentrate in frontsci (where the agent has the largest information gap to close). The total
sample of 12 discordant pairs in t0027 makes any subset-level claim premature.

This task piggy-backs on t0029's discordance-rich resample to deliver an RQ4 verdict at zero
additional API cost: it consumes t0029's predictions and runs a stratified analysis only.

## Scope

In scope:

* Read t0029's predictions assets for arm A and arm B.
* Define "information asymmetry" operationally per subset using existing metadata in
  `t0010_matched_mismatch_library` (e.g., gold-context length, hidden-state count,
  human-judgement disagreement scores).
* Compute per-stratum (subset × asymmetry-tertile) discordant counts and granularity-gain
  rates (B success - A success).
* Run stratified McNemar / proportion tests with Bonferroni correction across the strata.
* Produce a stratification table and at least one figure (subset × asymmetry tertile).
* Write an answer asset for RQ4 with confidence assessment and the explicit caveat if the
  t0029 sample fell short of the >= 30 discordant-pair target.

Out of scope:

* Any new API calls or remote compute.
* RQ1 verdict (delivered by t0029).
* RQ5 verdict (deferred to a later wave).
* Building a new info-asymmetry metric — reuse only what is already in
  `t0010_matched_mismatch_library` and t0027's harness logs.

## Method

1. Load t0029 predictions for arm A and arm B keyed by paired instance ID.
2. Join against `t0010_matched_mismatch_library` to recover per-instance metadata (subset,
   asymmetry signals).
3. Define info-asymmetry tertiles per subset (low / mid / high) using the chosen signal.
4. Compute granularity-gain rate per stratum: `success_rate(B) - success_rate(A)`.
5. Test the joint hypothesis "gain rate is higher in high-asymmetry strata than low-asymmetry
   strata" via stratified McNemar (per subset) plus a Cochran-Mantel-Haenszel-style overall
   test, with Bonferroni-adjusted alpha = 0.025.
6. Write the answer asset following `meta/asset_types/answer/specification.md`.

## Deliverables

* `assets/answer/rq4-info-asymmetry-stratification/` answer asset with a confidence rating and
  the verdict (full / partial / inconclusive).
* `results/results_summary.md` and `results/results_detailed.md` with the stratification table
  and figure embedded.
* `results/metrics.json` with per-stratum granularity-gain rates and the joint test p value.
* `results/images/rq4_stratification.png` (subset × asymmetry tertile heatmap or grouped bar).

## Cross-references

* Source: t0028 brainstorm session 8.
* Depends on: t0029.
* Builds on: t0010_matched_mismatch_library (subset metadata).
* Source suggestion: none (analysis-only follow-up).

</details>
