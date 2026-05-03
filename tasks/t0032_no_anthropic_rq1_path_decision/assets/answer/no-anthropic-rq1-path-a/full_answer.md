---
spec_version: "2"
answer_id: "no-anthropic-rq1-path-a"
answered_by_task: "t0032_no_anthropic_rq1_path_decision"
date_answered: "2026-05-03"
confidence: "high"
---
# No-Anthropic RQ1 path: option (a) existing-results-only verdict

## Question

Which RQ1 execution path do we follow under the permanent no-Anthropic constraint: (a)
existing-results-only verdict, (b) local / open-weight rerun, (c) alternative paid provider, or (d)
project-level underpowered / provider-blocked stop?

## Short Answer

Option (a), the existing-results-only verdict, is the right path. The t0031 re-derivation already
yields the formal RQ1 conclusion at $0 with arm-labelling comparability with t0027 / t0028 preserved
by construction: 12 / 130 = 9.23% discordance, 6 arm-A wins and 6 arm-B wins, two-sided
exact-binomial McNemar p = 1.0000, with a SWE-bench arm-B advantage and a FrontierScience arm-A
advantage that cancel in aggregate. Options (b) and (c) replace the policy under each arm label and
turn any rerun into a verdict on a new experiment, while option (d) forecloses the verdict that (a)
can deliver immediately.

## Research Process

This is an analysis-only task. The decision was driven by re-reading three JSON sidecars produced by
t0031 (`rq1_power_grid.json`, `rq4_stratification.json`, `log_audit.json`) plus the realized
agent-call cost totals from t0026 and t0027. A small Python script under `code/` (see
`build_decision_inputs.py` and `cross_check.py`) loads those files, asserts that the headline
discordance numbers match the values reported in `t0031/results/results_summary.md` verbatim, and
emits `code/decision_inputs.json` plus `code/comparison_table.md`. Internet research was scoped
narrowly to non-Anthropic 2026 list prices for option (c) (GPT-5 and Gemini 2.5 Pro at $1.25 /
$10.00 per MTok). No new agent code was run, no remote machine was created, and no paid API call was
made. Conflicting evidence was handled by halting on disagreement (`build_decision_inputs.py` raises
`RuntimeError` if `rq4_stratification.json` overall counts disagree with the ALL stratum or if the
log audit's paired N disagrees with the stratification N).

## Evidence from Papers

The `papers` method was not used; this decision turns on the project's own measurements (t0027
paired N=130, t0031 power grid and stratification, t0026 / t0027 realized costs) and on provider
list prices. No published-paper evidence is required to choose between (a), (b), (c), and (d) on
this specific data.

## Evidence from Internet Sources

Provider pricing pages (see `research/research_internet.md` and the source URLs below) establish the
cheapest credible non-Anthropic option in the Sonnet-4.6 tier at $1.25 input / $10.00 output per
MTok (GPT-5, Gemini 2.5 Pro). Output token list price is roughly 33% cheaper than Claude Sonnet 4.6
at $3.00 / $15.00. Output dominates the per-pair cost shape, so option (c) per-pair cost is anchored
at about $0.07 — about 67% of the realized $0.107 paired-instance cost on Sonnet. Multiplied by the
t0029 admission cap of 218 new pairs, option (c) totals $0.07 x 218 = $15.26, in the $15-$25 band
reported in `research_internet.md`. Batch and cached-input discounts (50% and ~90% respectively)
could halve this further but would also further erode comparability with t0027, which ran online.
They are deferred to creative thinking and are not credited in the headline point estimate.

## Evidence from Code or Experiments

The decisive evidence is project-internal and re-derived in `code/decision_inputs.json`:

* **Discordance and McNemar (ALL stratum, t0031)**: paired N = 130, n_discordant = 12, a_only = 6,
  b_only = 6, two-sided exact-binomial McNemar p = **1.0000**. The aggregate signal is null. The
  re-derivation in `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq4_stratification.json` is
  the authoritative source; `cross_check.py` confirms our `decision_inputs.json` matches the t0031
  numbers verbatim.
* **Per-stratum cells (t0031)**: SWE-bench (n = 20) shows b_only = 6 and a_only = 0 with two-sided
  McNemar p = 0.0312 — a real arm-B advantage on SWE-bench. FrontierScience (n = 26) shows a_only =
  5 and b_only = 0 with two-sided p = 0.0625 — a marginal arm-A advantage on FrontierScience that is
  in the opposite direction. Tau-bench (n = 84) has 1 discordant pair out of 84 (83 / 84 are
  both-fail). These per-stratum directions cancel in the ALL row.
* **Power at the t0029 cap (t0031)**: `rq1_power_grid.json` enumerates RQ1 power as a function of
  the conditional B-wins rate p1, holding the cap arithmetic fixed. Power crosses 0.80 only at p1 >=
  0.75 (power = 0.846 at p1 = 0.75, 0.959 at p1 = 0.80) and is below 0.10 at p1 = 0.55. Even a fresh
  cap-sized rerun therefore yields a null verdict for any plausible "true" p1 short of 0.75 — the
  test is structurally underpowered against a realistic alternative. This is the same constraint
  that any (b) or (c) rerun would inherit.
* **Per-paired-instance cost on Claude Sonnet 4.6 (t0026 + t0027)**: arm A from t0026
  (`runs_variant_a_usd = $4.4659 / 130 = ~$0.0344` per instance) plus arm B from t0027
  (`variant_b_agent_full = $9.4534 / 130 = ~$0.0727` per instance) sums to a paired cost of **about
  $0.107 per paired instance**. Arm C from t0027 (`variant_c_agent_full = $9.3392 / 130 = ~$0.0718`
  per instance) is included for completeness but is not in the RQ1 paired denominator.
* **Arm-labelling anchor (t0027)**: `tasks/t0027/results/results_summary.md` fixes the convention A
  = Plan-and-Solve (`plan_and_solve_v3`), B = scope-aware ReAct, C = matched-mismatch
  (`matched_mismatch_v2`) on Claude Sonnet 4.6. Replacing the model under any arm label is a policy
  swap, not a continuation of the t0027 experiment.

## Synthesis

### Comparison table

| Option | USD point estimate | Validity / power risk | Comparability with t0027 / t0028 | Time-to-result |
| --- | ---: | --- | --- | --- |
| (a) existing-results-only verdict | $0.00 | Aggregate McNemar p=1.0000 on N=130 (12 discordant); verdict is null aggregate with documented per-stratum interaction. No new sampling. | Trivially preserved; no rerun, t0027 fixed-arm convention untouched. | Hours (analysis-only; no compute). |
| (b) local / open-weight rerun | $0.00 (hardware-bound) | Same structural underpowering as (c) at the t0029 cap; open-weight policy quality is unbounded variance vs Sonnet baseline. | Lost: replaces the policy under arm A or arm B; verdict is on a different model, not on the t0027 arms. | Days to weeks (engineering + GPU provisioning). |
| (c) alternative paid provider (GPT-5 / Gemini 2.5 Pro) | $0.07 / pair x 218 = $15.26 (band $15-$25) | Power < 0.80 unless true p1 >= 0.75 (per t0031 power grid); cap-sized rerun still likely null. | Lost: GPT-5 or Gemini 2.5 Pro plays arm B in place of Claude Sonnet 4.6; arm label preserved, policy under label changed. | About 1-2 days (provider onboarding + 218-pair sweep). |
| (d) project-level underpowered / provider-blocked stop | $0.00 | No verdict produced; forecloses analysis that (a) can already deliver. | Trivially preserved (no rerun); but the comparability is moot without a verdict. | Immediate (hard stop). |

### Comparability with t0027 / t0028 fixed-arm convention

The decisive criterion is the t0027 fixed-arm convention. t0027 anchored the labels A =
Plan-and-Solve, B = scope-aware ReAct, C = matched-mismatch by binding each arm to specific
project-internal libraries (`plan_and_solve_v3`, `matched_mismatch_v2`) running on Claude Sonnet
4.6. t0028 then scheduled the discordance-rich resample under exactly that convention. Any rerun
that swaps the model preserves the arm **label** but changes the **policy under the label**, so a
McNemar test on the new sample answers a different question — namely, does the new model's
arm-B-style policy beat the new model's arm-A-style policy on the same instance pool?

* **Option (a)** preserves comparability trivially: there is no rerun, so the t0027 fixed-arm
  convention is untouched and the verdict is a verdict on the t0027 arms by construction.
* **Option (b)** replaces the policy under arm A or arm B with whatever open-weight model is used.
  Arm label preserved; policy under label changed. The resulting verdict is a verdict on the
  open-weight model, not on the t0027 arms.
* **Option (c)** is structurally identical to (b) in this dimension: GPT-5 or Gemini 2.5 Pro plays
  arm B in place of Claude Sonnet 4.6. Arm label preserved; policy under label changed. The
  resulting verdict is a verdict on GPT-5 or Gemini 2.5 Pro, not on the t0027 arms. The $0.07 / pair
  cost number is honest, but the comparability claim is what fails — and it fails before the cost
  calculation matters.
* **Option (d)** preserves comparability trivially in the same sense as (a) (no rerun), but it
  forecloses the verdict that (a) can deliver. The comparability is moot without a verdict.

### Why option (b) is rejected

Option (b) uses an open-weight policy (Llama-class, Qwen-class, or similar) hosted locally or on
project GPU. The headline cost is hardware-bound rather than token-bound, so the dollar number looks
attractive. Two reasons rule it out: first, the comparability gap is the same as option (c) —
replacing Claude Sonnet 4.6 under arm A or arm B turns any RQ1 verdict into a verdict on a new
model, not a continuation of t0027 / t0028. Second, the structural underpowering at the t0029 cap
applies regardless of provider. Even if the open-weight policy matches Sonnet quality exactly, the
t0031 power grid says the cap-sized rerun is below 0.80 power for any plausible true p1 short of
0.75. Spending engineering time on (b) buys neither comparability nor power.

### Why option (c) is rejected

Option (c) substitutes GPT-5 or Gemini 2.5 Pro for Claude Sonnet 4.6 under one of the arm labels and
pays the 218-pair sweep at the cheaper output-token list price. The total cost lands at $0.07 x 218
= $15.26, in the $15-$25 band — well inside the project's pre-warn budget headroom. The cost is not
the disqualifier. The disqualifier is the same comparability failure as (b): the arm label is
preserved by construction, but the policy under the label is not. The McNemar test on the new sample
becomes a McNemar test on GPT-5 / Gemini 2.5 Pro, which is interesting but is not RQ1 as posed
against the t0027 / t0028 fixed-arm convention. The cap-sized run is also still underpowered against
any plausible true p1 short of 0.75, so even a "successful" option (c) run likely returns null.
Paying $16 for a likely-null verdict on a different policy is the worst kind of expensive null.

### Why option (d) is rejected

Option (d) declares RQ1 underpowered and provider-blocked and stops the analysis. It costs $0 and
preserves arm-labelling comparability trivially (because no rerun happens). But option (a) costs the
same $0, preserves the same comparability, and additionally delivers the formal verdict — McNemar p
= 1.0000 on the existing N = 130 plus the documented per-stratum interaction (SWE-bench arm-B
advantage; FrontierScience arm-A advantage; Tau-bench dominated by both-fail). Option (d) forecloses
analysis that (a) can already deliver, with no offsetting benefit. There is no scenario where (d)
dominates (a).

### Why option (a) is recommended

Option (a) is the unique option that delivers a defensible RQ1 verdict at $0 cost while keeping the
t0027 / t0028 fixed-arm convention intact. The verdict is **null aggregate with a documented
per-stratum interaction**: aggregate McNemar p = 1.0000, but SWE-bench shows a real arm-B advantage
(b_only = 6, a_only = 0; one-sided p = 0.0312) and FrontierScience shows a marginal arm-A advantage
in the opposite direction (a_only = 5, b_only = 0; one-sided p = 0.0625). The cancellation is the
finding: any single-aggregate RQ1 statement obscures a real benchmark-by-arm interaction that should
be reported. Option (a) lets us publish that finding without spinning up a new experiment, without
breaking comparability with t0027 / t0028, and without spending paid-API budget that downstream
tasks (RQ4 stratification on existing data, S-0031-03 cost-tracker fix) can use instead. The
recommendation is exactly option (a). It does not assume Anthropic access becomes available at any
point — and it does not need to.

## Limitations

* The t0031 power grid uses a single conditional-B-wins-rate (p1) sweep with a fixed cap-arithmetic
  assumption ($0.16 / pair, 218 new pairs, 32 expected discordant). Real reruns would deviate
  slightly from the modelled p1 grid; the qualitative conclusion (underpowering at p1 < 0.75) is
  robust but the exact power numbers are not.
* The per-stratum interaction is real but the per-stratum n's are small: SWE-bench n = 20,
  FrontierScience n = 26. Both p-values are one-sided in the per-stratum reporting; the two-sided
  values are 0.0312 and 0.0625 respectively. These should be reported with Wilson 95% CIs (already
  in `rq4_stratification.json`) rather than as headline p-values.
* Tau-bench is dominated by both-fail (83 / 84 pairs). No amount of additional Tau-bench paired data
  will move RQ1; the conditional-event rate is too low. This is an upstream sampling problem, not an
  analysis problem.
* The arm-labelling comparability argument relies on the t0027 convention being the binding
  artefact. If a downstream task explicitly redefines the arm labels (for instance, "arm B is now
  any scope-aware ReAct policy on any provider"), then option (c) or (b) becomes admissible under
  that redefinition. This task does not perform that redefinition.
* The option (c) per-pair cost ($0.07) is an output-token-dominated point estimate. Batch (50%) and
  cached-input (~90%) discounts could lower it further, but they were excluded from the headline
  because t0027 ran online and the comparability claim is already lost — discounts cannot rescue
  what is structurally not a continuation.

## Sources

* Task: `t0026_phase2_abc_runtime_n147_for_rq1_rq5`
* Task: `t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
* Task: `t0028_brainstorm_results_8`
* Task: `t0029_rq1_discordance_rich_resample`
* Task: `t0031_rq1_rq4_no_new_api_salvage`
* URL: https://openai.com/api/pricing/
* URL: https://ai.google.dev/gemini-api/docs/pricing
* URL: https://www.anthropic.com/pricing

[t0026]: ../../../../t0026_phase2_abc_runtime_n147_for_rq1_rq5/
[t0027]: ../../../../t0027_phase2_5_abc_rerun_with_fixed_b_and_c/
[t0028]: ../../../../t0028_brainstorm_results_8/
[t0029]: ../../../../t0029_rq1_discordance_rich_resample/
[t0031]: ../../../../t0031_rq1_rq4_no_new_api_salvage/
[openai-pricing-2026]: https://openai.com/api/pricing/
[google-gemini-pricing-2026]: https://ai.google.dev/gemini-api/docs/pricing
[anthropic-pricing-2026]: https://www.anthropic.com/pricing
