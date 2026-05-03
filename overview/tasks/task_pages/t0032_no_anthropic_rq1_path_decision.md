# ✅ No-Anthropic RQ1 path decision

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0032_no_anthropic_rq1_path_decision` |
| **Status** | ✅ completed |
| **Started** | 2026-05-03T13:19:53Z |
| **Completed** | 2026-05-03T14:05:06Z |
| **Duration** | 45m |
| **Dependencies** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md), [`t0031_rq1_rq4_no_new_api_salvage`](../../../overview/tasks/task_pages/t0031_rq1_rq4_no_new_api_salvage.md) |
| **Task types** | `answer-question` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 11/15 |
| **Task folder** | [`t0032_no_anthropic_rq1_path_decision/`](../../../tasks/t0032_no_anthropic_rq1_path_decision/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/results/results_detailed.md) |

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

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Which RQ1 execution path do we follow under the permanent no-Anthropic constraint: (a) existing-results-only verdict, (b) local / open-weight rerun, (c) alternative paid provider, or (d) project-level underpowered / provider-blocked stop?](../../../tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/) | [`full_answer.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Close t0029 / t0030 via correction as no-longer-actionable under
no-Anthropic constraint</strong> (S-0032-01)</summary>

**Kind**: evaluation | **Priority**: high

Now that t0032 locks in option (a) — existing-results-only verdict — as the recommended RQ1
execution path, t0029 (rerun B+C at the 218-pair cap) and t0030 (B-only matched-mismatch
follow-up) are no longer actionable. Both rely on Sonnet via the Anthropic API, which the
project memory marks as permanently unavailable. Emit a downstream correction task that flips
both task statuses to 'cancelled' with a rationale referencing t0032's verdict and the
no-Anthropic constraint, so aggregators stop surfacing them as outstanding work.

</details>

<details>
<summary><strong>Spend released RQ1 budget on cost-tracker fix, bootstrap CIs, and
RQ4 stratification follow-ups</strong> (S-0032-02)</summary>

**Kind**: experiment | **Priority**: medium

With option (a) locked in, the ~$26.54 reserved for the t0029 218-pair rerun is released.
Reinvest it in three cost-free or near-zero analyses directly motivated by t0032's
creative-thinking pass: (1) implement S-0031-03 to fix per-instance cost tracking so future
paired runs report Sonnet cost reliably; (2) compute 95% bootstrap confidence intervals around
the per-stratum McNemar cells from t0031 (SWE-bench 6/0, FrontierScience 0/5, tau-bench 1 of
84) to harden the conclusion that arms differ qualitatively by benchmark; (3) re-stratify the
existing 130-pair t0031 sample by trace length / tool-call count for the RQ4
efficiency-vs-accuracy story without any new paid API call.

</details>

<details>
<summary><strong>Qualitative trajectory typology of the 12 t0031 discordant
pairs</strong> (S-0032-03)</summary>

**Kind**: evaluation | **Priority**: low

Build a small qualitative typology of the 12 discordant paired instances from t0031 (6 a_only
+ 6 b_only) to characterise how plan-and-solve_v3 (arm A) and matched_mismatch_v2 (arm B)
diverge on the same instance. Tag each discordant pair by failure mode (planning error, tool
misuse, retrieval gap, formatting, etc.) and benchmark stratum. The output is one short
markdown asset; the task is zero-cost (reads existing trajectories from t0026/t0027) and feeds
back into RQ1 reporting and future agent-design suggestions.

</details>

## Research

* [`creative_thinking.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/research/creative_thinking.md)
* [`research_code.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/research/research_internet.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/results/results_summary.md)*

# RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT

## Summary

Locked in **option (a) — existing-results-only verdict** as the recommended RQ1 execution path
under the permanent no-Anthropic constraint. The t0031 re-derivation already yields the formal
RQ1 conclusion at $0 with arm-labelling comparability against t0027 / t0028 trivially
preserved: 12 / 130 discordant pairs, symmetric 6 / 6 split, two-sided exact-binomial McNemar
p = **1.0000**, with a real SWE-bench arm-B advantage and a marginal FrontierScience arm-A
advantage that cancel in aggregate. Options (b), (c), and (d) were each rejected on a
documented comparability or foreclosure basis; creative-thinking surfaced no non-obvious
cost-saver that flips the recommendation.

## Metrics

* **Aggregate McNemar p (N=130, t0031)**: **1.0000** (12 discordant; 6 a_only; 6 b_only)
* **SWE-bench per-stratum cell**: b_only = **6**, a_only = **0** (n = 20; two-sided p =
  **0.0312**)
* **FrontierScience per-stratum cell**: a_only = **5**, b_only = **0** (n = 26; two-sided p =
  **0.0625**)
* **Tau-bench per-stratum cell**: 1 discordant of n = 84 (83 / 84 both-fail; two-sided p =
  **1.0000**)
* **Power at the t0029 cap**: crosses 0.80 only at p1 ≥ 0.75 (power = **0.846** at p1 = 0.75;
  below **0.10** at p1 = 0.55)
* **Per-paired-instance cost on Sonnet (t0026 + t0027)**: ≈ **$0.107** ($0.0344 arm A +
  $0.0727 arm B)
* **Option (c) USD point estimate**: $0.07 / pair × 218 = **$15.26** (band $15-$25)
* **This task's total cost**: **$0.00** (no paid API call, no remote compute)

## Verification

* `meta.asset_types.answer.verificator` (answer asset) — PASSED (0 errors, 0 warnings)
* `verify_plan` (plan/plan.md) — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies` (t0027, t0031) — PASSED (0 errors, 0 warnings)
* `cross_check.py` (t0031 numbers re-derived in `code/decision_inputs.json`) — PASSED
  (verbatim match)
* `ruff check --fix . && ruff format .` and `mypy -p
  tasks.t0032_no_anthropic_rq1_path_decision.code` — clean

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0032_no_anthropic_rq1_path_decision/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0032_no_anthropic_rq1_path_decision" ---
# Results Detailed: No-Anthropic RQ1 Path Decision

## Summary

This analysis-only task chose **option (a) — existing-results-only verdict** as the RQ1
execution path under the permanent no-Anthropic constraint. The decision is driven by the
t0031 re-derivation on the existing N = 130 paired sample (12 discordant, 6 / 6 split, McNemar
p = 1.0000) plus the t0031 power grid (cap-sized rerun is structurally underpowered for any
plausible true p1 short of 0.75) and the realized t0026 / t0027 per-instance cost totals. The
task produced one `answer` asset, a 4-row × 5-column comparison table, a creative-thinking
memo confirming no cost-saver flips the recommendation, and this results bundle. No paid API
call, no remote compute, no Anthropic credentials required at any point.

## Methodology

* **Machine**: macOS 25.4.0 (Darwin), arm64; analysis ran inside the Glite ARF worktree at
  `/Users/lysaniuk/Documents/reasoning-scale2-worktrees/t0032_no_anthropic_rq1_path_decision`.
  No remote compute was provisioned.
* **Total runtime**: ≈ 60 minutes wall-clock (start 2026-05-03T13:20:00Z; end ≈
  2026-05-03T14:25Z), dominated by reading and synthesising the 5 upstream JSON sidecars and
  writing the answer asset.
* **Method**: pure Python (`json.load`, `pathlib.Path`, arithmetic only — no statistical
  libraries). Four scripts under `code/` (`paths.py`, `build_decision_inputs.py`,
  `build_comparison_table.py`, `cross_check.py`) load the t0031 power-grid /
  RQ4-stratification / log-audit sidecars and the t0026 / t0027 cost totals, derive the
  four-option comparison cells, emit `code/decision_inputs.json` and
  `code/comparison_table.md`, and confirm the discordance numbers match
  `tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md` verbatim.
* **Inputs (5 JSON sidecars)**:
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq1_power_grid.json`
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq4_stratification.json`
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/log_audit.json`
  * `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json`
  * `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json`
* **Internet research**: scoped narrowly to non-Anthropic 2026 list pricing (GPT-5 and Gemini
  2.5 Pro at $1.25 / $10.00 per MTok) — see `research/research_internet.md`. No paper research
  was needed.

## Comparison Table

The four-option comparison drives the decision. Cells are derived in
`code/build_decision_inputs.py` and rendered by `code/build_comparison_table.py`; the table
below is the canonical version copied into
`assets/answer/no-anthropic-rq1-path-a/full_answer.md`.

| Option | USD point estimate | Validity / power risk | Comparability with t0027 / t0028 | Time-to-result |
| --- | ---: | --- | --- | --- |
| (a) existing-results-only verdict | $0.00 | Aggregate McNemar p=1.0000 on N=130 (12 discordant); verdict is null aggregate with documented per-stratum interaction. No new sampling. | Trivially preserved; no rerun, t0027 fixed-arm convention untouched. | Hours (analysis-only; no compute). |
| (b) local / open-weight rerun | $0.00 (hardware-bound) | Same structural underpowering as (c) at the t0029 cap; open-weight policy quality is unbounded variance vs Sonnet baseline. | Lost: replaces the policy under arm A or arm B; verdict is on a different model, not on the t0027 arms. | Days to weeks (engineering + GPU provisioning). |
| (c) alternative paid provider (GPT-5 / Gemini 2.5 Pro) | $0.07 / pair x 218 = $15.26 (band $15-$25) | Power < 0.80 unless true p1 >= 0.75 (per t0031 power grid); cap-sized rerun still likely null. | Lost: GPT-5 or Gemini 2.5 Pro plays arm B in place of Claude Sonnet 4.6; arm label preserved, policy under label changed. | About 1-2 days (provider onboarding + 218-pair sweep). |
| (d) project-level underpowered / provider-blocked stop | $0.00 | No verdict produced; forecloses analysis that (a) can already deliver. | Trivially preserved (no rerun); but the comparability is moot without a verdict. | Immediate (hard stop). |

## Headline Findings

* **The aggregate signal is null and the per-stratum interaction is real**. McNemar p = 1.0000
  on N=130 obscures a SWE-bench arm-B advantage (b_only = 6, a_only = 0; one-sided p = 0.0312)
  and a FrontierScience arm-A advantage in the opposite direction (a_only = 5, b_only = 0;
  one-sided p = 0.0625). The cancellation **is** the finding; downstream readers must not
  treat the aggregate as evidence against benchmark-by-arm interaction.
* **The cap-sized rerun is structurally underpowered**. From `rq1_power_grid.json`: power
  crosses 0.80 only at p1 ≥ 0.75 (power = 0.846 at p1 = 0.75; 0.959 at p1 = 0.80) and is below
  0.10 at p1 ≤ 0.55. Even an option-(c) rerun on GPT-5 / Gemini 2.5 Pro at the t0029 cap still
  likely returns null for any plausible true p1.
* **Comparability with t0027 / t0028 is the binding criterion, not cost**. t0027's fixed-arm
  convention pinned A = `plan_and_solve_v3`, B = scope-aware ReAct, C = `matched_mismatch_v2`
  to Claude Sonnet 4.6. Replacing the model under any arm label preserves the label but
  changes the policy under the label, so any (b) / (c) verdict is a verdict on a new policy —
  not a continuation of t0027. Cheaper providers do not rescue this; the comparability gap is
  policy-substitution- shaped, not dollar-shaped.
* **Tau-bench is dominated by both-fail (83 / 84 pairs)**. No amount of additional Tau-bench
  paired data will move RQ1; the conditional-event rate is too low. This is an upstream
  sampling problem, not an analysis problem.
* **Creative thinking surfaced six candidates (C1-C6) and none flips the recommendation**. The
  strongest a-priori candidate (C1, discordance-only rerun on a non-Anthropic provider at ≈
  $0.84) fails on the same comparability gap as option (c) plus a selection-bias confound that
  t0028 explicitly avoided. C2 (bootstrap CIs on the existing N=130 sample) and C4
  (qualitative trajectory typology of the 12 discordant pairs) are recorded as candidate
  follow-up suggestions for the released budget. See `research/creative_thinking.md`.

## Verification

* `meta.asset_types.answer.verificator` on `assets/answer/no-anthropic-rq1-path-a/` — PASSED
  (0 errors, 0 warnings).
* `verify_plan` on `plan/plan.md` — PASSED (0 errors, 0 warnings) after replacing literal
  orchestrator-managed filenames in Step by Step with semantic references.
* `verify_task_dependencies` on (t0027, t0031) — PASSED (0 errors, 0 warnings); both
  dependencies are completed and their assets are uncorrected.
* `cross_check.py` confirms the discordance and per-stratum cells in
  `code/decision_inputs.json` match
  `tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md` verbatim.
* `ruff check --fix .` and `ruff format .` — clean. `mypy -p
  tasks.t0032_no_anthropic_rq1_path_decision.code` — clean.
* `flowmark --inplace --nobackup` was run on every newly written `.md` file (plan, research,
  creative-thinking, results_summary, results_detailed, answer assets, step logs).

## Limitations

* The t0031 power grid uses a single conditional-B-wins-rate (p1) sweep with fixed cap
  arithmetic ($0.16 / pair, 218 new pairs, 32 expected discordant). Real reruns deviate
  slightly from the modelled p1 grid; the qualitative conclusion (underpowering at p1 < 0.75)
  is robust but the exact power numbers are not.
* Per-stratum n's are small (SWE-bench n = 20, FrontierScience n = 26). Both p-values are
  reported as one-sided in t0031; the two-sided values are 0.0312 and 0.0625 respectively.
  These should be reported with Wilson 95% CIs (already in `rq4_stratification.json`) rather
  than as headline p-values, and the interpretation should reflect "marginal" rather than
  "definitive" arm-A advantage on FrontierScience.
* The arm-labelling comparability argument relies on the t0027 convention being the binding
  artefact. If a downstream task explicitly redefines the arm labels (for instance, "arm B is
  now any scope-aware ReAct policy on any provider"), then option (c) or (b) becomes
  admissible under that redefinition. This task does not perform that redefinition.
* The option (c) per-pair cost ($0.07) is an output-token-dominated point estimate at 2026
  list pricing. Batch (50%) and cached-input (≈ 90%) discounts could lower it further but were
  excluded from the headline because t0027 ran online and the comparability claim is already
  lost.
* No bootstrap confidence band was computed on the symmetric 6 / 6 cell. C2 in
  `research/creative_thinking.md` records this as a candidate follow-up suggestion
  (S-0032-02); including it strengthens the per-stratum interpretation but does not change the
  headline.

## Files Created

* `tasks/t0032_no_anthropic_rq1_path_decision/code/paths.py`
* `tasks/t0032_no_anthropic_rq1_path_decision/code/build_decision_inputs.py`
* `tasks/t0032_no_anthropic_rq1_path_decision/code/build_comparison_table.py`
* `tasks/t0032_no_anthropic_rq1_path_decision/code/cross_check.py`
* `tasks/t0032_no_anthropic_rq1_path_decision/code/decision_inputs.json`
* `tasks/t0032_no_anthropic_rq1_path_decision/code/comparison_table.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/details.json`
* `tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/short_answer.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/assets/answer/no-anthropic-rq1-path-a/full_answer.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/research/research_internet.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/research/research_code.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/research/creative_thinking.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/plan/plan.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/results/results_summary.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/results/results_detailed.md`
* `tasks/t0032_no_anthropic_rq1_path_decision/results/metrics.json`
* `tasks/t0032_no_anthropic_rq1_path_decision/results/costs.json`
* `tasks/t0032_no_anthropic_rq1_path_decision/results/remote_machines_used.json`

## Task Requirement Coverage

The operative request from `tasks/t0032_no_anthropic_rq1_path_decision/task_description.md`:

> Choose one RQ1 execution path under permanent no-Anthropic constraint: existing-only verdict,
> local rerun, alternate provider, or stop. Produce exactly one `answer` asset that picks one path
> and records the reasoning. Compare cost in USD (point estimate), validity / statistical-power
> risk, comparability with t0027 / t0028's labelled-arm baseline, and time-to-result. Recommendation
> is exactly one of {(a), (b), (c), (d)} — not a hybrid, not a hedge. The recommendation does not
> assume Anthropic access becomes available at any point.

| ID | Status | Direct answer | Evidence |
| --- | --- | --- | --- |
| **REQ-1** Evaluate option (a) | Done | Recommended; t0031 re-derivation gives McNemar p = 1.0000 on N=130 (12 discordant; 6 / 6); per-stratum cells SWE-bench (b_only=6, a_only=0, p=0.0312), FrontierScience (a_only=5, b_only=0, p=0.0625), Tau-bench (1 / 84). Power at the t0029 cap: 0.846 at p1 = 0.75. | `code/decision_inputs.json`; `code/comparison_table.md` row 1; `assets/answer/no-anthropic-rq1-path-a/full_answer.md` "Why option (a) is recommended". |
| **REQ-2** Evaluate option (b) | Done | Rejected. Open-weight rerun cost is hardware-bound ($0); the comparability gap is the same as option (c) — replacing Claude Sonnet 4.6 under arm A or arm B turns any RQ1 verdict into a verdict on a new model. Same structural underpowering at the t0029 cap. | `code/comparison_table.md` row 2; `full_answer.md` "Why option (b) is rejected"; `research/research_code.md` for the labelling anchor. |
| **REQ-3** Evaluate option (c) | Done | Rejected. Per-pair point estimate $0.07 (output-token-dominated, GPT-5 / Gemini 2.5 Pro list); total $15.26 over 218 pairs (band $15-$25). Comparability gap is the disqualifier, not cost. Cap-sized run is also still underpowered (p1 < 0.75 → power < 0.80). | `code/decision_inputs.json` `option_costs.c_total_usd = 15.26`; `code/comparison_table.md` row 3; `full_answer.md` "Why option (c) is rejected"; `research/research_internet.md`. |
| **REQ-4** Evaluate option (d) | Done | Rejected. $0 hard stop preserves comparability trivially but forecloses the verdict that option (a) already delivers for the same $0. The unspent budget is recoverable under (a); (d) offers no offsetting benefit. | `code/comparison_table.md` row 4; `full_answer.md` "Why option (d) is rejected"; cross-references in suggestions step (S-0032-01). |
| **REQ-5** Comparability statement vs t0027 / t0028 | Done | Section "Comparability with t0027 / t0028 fixed-arm convention" in `full_answer.md` states explicitly that (a) and (d) preserve comparability trivially (no rerun); (b) and (c) preserve the arm label but change the policy under the label. | `assets/answer/no-anthropic-rq1-path-a/full_answer.md` H3 section under Synthesis; verificator passed at H3 because spec-mandated H2 set does not include "Comparability". |
| **REQ-6** Produce one `answer` asset | Done | `assets/answer/no-anthropic-rq1-path-a/{details.json, short_answer.md, full_answer.md}`. `details.json` `spec_version: "2"`, `confidence: "high"`, `answer_methods: ["code-experiment", "internet"]`, `categories: ["agent-evaluation", "uncertainty-calibration"]`. | Answer-asset verificator: 0 errors, 0 warnings. |
| **REQ-7** Results bundle with headline label | Done | `results/results_summary.md` first non-frontmatter line is exactly `# RQ1 PATH DECISION — OPTION (A): EXISTING-RESULTS-ONLY VERDICT`; `results/results_detailed.md` embeds the comparison table verbatim. | This file (`results_detailed.md`) and `results/results_summary.md`. |
| **REQ-8** At most 3 follow-up suggestions | Done in step 14 | Suggestions: S-0032-01 (close t0029 / t0030 via correction), S-0032-02 (apply released budget to S-0031-03 cost-tracker fix + bootstrap CIs from C2 + RQ4 stratification analysis), S-0032-03 (qualitative trajectory typology of the 12 discordant pairs from C4 — optional). | `results/suggestions.json` (written in step 14). |
| **REQ-9** Cost / machines bookkeeping | Done | `results/costs.json` reports `total_cost_usd: 0.00`; `results/remote_machines_used.json` is `[]`. | `results/costs.json`; `results/remote_machines_used.json`. |

</details>
