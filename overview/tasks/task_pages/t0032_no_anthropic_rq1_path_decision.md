# ⏹ No-Anthropic RQ1 path decision

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0032_no_anthropic_rq1_path_decision` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md), [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Task types** | `answer-question` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0032_no_anthropic_rq1_path_decision/`](../../../tasks/t0032_no_anthropic_rq1_path_decision/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/task_description.md)*

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
