---
spec_version: "2"
task_id: "t0032_no_anthropic_rq1_path_decision"
---
# Results Detailed: No-Anthropic RQ1 Path Decision

## Summary

This analysis-only task chose **option (a) — existing-results-only verdict** as the RQ1 execution
path under the permanent no-Anthropic constraint. The decision is driven by the t0031 re-derivation
on the existing N = 130 paired sample (12 discordant, 6 / 6 split, McNemar p = 1.0000) plus the
t0031 power grid (cap-sized rerun is structurally underpowered for any plausible true p1 short of
0.75) and the realized t0026 / t0027 per-instance cost totals. The task produced one `answer` asset,
a 4-row × 5-column comparison table, a creative-thinking memo confirming no cost-saver flips the
recommendation, and this results bundle. No paid API call, no remote compute, no Anthropic
credentials required at any point.

## Methodology

* **Machine**: macOS 25.4.0 (Darwin), arm64; analysis ran inside the Glite ARF worktree at
  `/Users/lysaniuk/Documents/reasoning-scale2-worktrees/t0032_no_anthropic_rq1_path_decision`. No
  remote compute was provisioned.
* **Total runtime**: ≈ 60 minutes wall-clock (start 2026-05-03T13:20:00Z; end ≈ 2026-05-03T14:25Z),
  dominated by reading and synthesising the 5 upstream JSON sidecars and writing the answer asset.
* **Method**: pure Python (`json.load`, `pathlib.Path`, arithmetic only — no statistical libraries).
  Four scripts under `code/` (`paths.py`, `build_decision_inputs.py`, `build_comparison_table.py`,
  `cross_check.py`) load the t0031 power-grid / RQ4-stratification / log-audit sidecars and the
  t0026 / t0027 cost totals, derive the four-option comparison cells, emit
  `code/decision_inputs.json` and `code/comparison_table.md`, and confirm the discordance numbers
  match `tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md` verbatim.
* **Inputs (5 JSON sidecars)**:
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq1_power_grid.json`
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/rq4_stratification.json`
  * `tasks/t0031_rq1_rq4_no_new_api_salvage/results/data/log_audit.json`
  * `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json`
  * `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/results/costs.json`
* **Internet research**: scoped narrowly to non-Anthropic 2026 list pricing (GPT-5 and Gemini 2.5
  Pro at $1.25 / $10.00 per MTok) — see `research/research_internet.md`. No paper research was
  needed.

## Comparison Table

The four-option comparison drives the decision. Cells are derived in `code/build_decision_inputs.py`
and rendered by `code/build_comparison_table.py`; the table below is the canonical version copied
into `assets/answer/no-anthropic-rq1-path-a/full_answer.md`.

| Option | USD point estimate | Validity / power risk | Comparability with t0027 / t0028 | Time-to-result |
| --- | ---: | --- | --- | --- |
| (a) existing-results-only verdict | $0.00 | Aggregate McNemar p=1.0000 on N=130 (12 discordant); verdict is null aggregate with documented per-stratum interaction. No new sampling. | Trivially preserved; no rerun, t0027 fixed-arm convention untouched. | Hours (analysis-only; no compute). |
| (b) local / open-weight rerun | $0.00 (hardware-bound) | Same structural underpowering as (c) at the t0029 cap; open-weight policy quality is unbounded variance vs Sonnet baseline. | Lost: replaces the policy under arm A or arm B; verdict is on a different model, not on the t0027 arms. | Days to weeks (engineering + GPU provisioning). |
| (c) alternative paid provider (GPT-5 / Gemini 2.5 Pro) | $0.07 / pair x 218 = $15.26 (band $15-$25) | Power < 0.80 unless true p1 >= 0.75 (per t0031 power grid); cap-sized rerun still likely null. | Lost: GPT-5 or Gemini 2.5 Pro plays arm B in place of Claude Sonnet 4.6; arm label preserved, policy under label changed. | About 1-2 days (provider onboarding + 218-pair sweep). |
| (d) project-level underpowered / provider-blocked stop | $0.00 | No verdict produced; forecloses analysis that (a) can already deliver. | Trivially preserved (no rerun); but the comparability is moot without a verdict. | Immediate (hard stop). |

## Headline Findings

* **The aggregate signal is null and the per-stratum interaction is real**. McNemar p = 1.0000 on
  N=130 obscures a SWE-bench arm-B advantage (b_only = 6, a_only = 0; one-sided p = 0.0312) and a
  FrontierScience arm-A advantage in the opposite direction (a_only = 5, b_only = 0; one-sided p =
  0.0625). The cancellation **is** the finding; downstream readers must not treat the aggregate as
  evidence against benchmark-by-arm interaction.
* **The cap-sized rerun is structurally underpowered**. From `rq1_power_grid.json`: power crosses
  0.80 only at p1 ≥ 0.75 (power = 0.846 at p1 = 0.75; 0.959 at p1 = 0.80) and is below 0.10 at p1 ≤
  0.55. Even an option-(c) rerun on GPT-5 / Gemini 2.5 Pro at the t0029 cap still likely returns
  null for any plausible true p1.
* **Comparability with t0027 / t0028 is the binding criterion, not cost**. t0027's fixed-arm
  convention pinned A = `plan_and_solve_v3`, B = scope-aware ReAct, C = `matched_mismatch_v2` to
  Claude Sonnet 4.6. Replacing the model under any arm label preserves the label but changes the
  policy under the label, so any (b) / (c) verdict is a verdict on a new policy — not a continuation
  of t0027. Cheaper providers do not rescue this; the comparability gap is policy-substitution-
  shaped, not dollar-shaped.
* **Tau-bench is dominated by both-fail (83 / 84 pairs)**. No amount of additional Tau-bench paired
  data will move RQ1; the conditional-event rate is too low. This is an upstream sampling problem,
  not an analysis problem.
* **Creative thinking surfaced six candidates (C1-C6) and none flips the recommendation**. The
  strongest a-priori candidate (C1, discordance-only rerun on a non-Anthropic provider at ≈ $0.84)
  fails on the same comparability gap as option (c) plus a selection-bias confound that t0028
  explicitly avoided. C2 (bootstrap CIs on the existing N=130 sample) and C4 (qualitative trajectory
  typology of the 12 discordant pairs) are recorded as candidate follow-up suggestions for the
  released budget. See `research/creative_thinking.md`.

## Verification

* `meta.asset_types.answer.verificator` on `assets/answer/no-anthropic-rq1-path-a/` — PASSED (0
  errors, 0 warnings).
* `verify_plan` on `plan/plan.md` — PASSED (0 errors, 0 warnings) after replacing literal
  orchestrator-managed filenames in Step by Step with semantic references.
* `verify_task_dependencies` on (t0027, t0031) — PASSED (0 errors, 0 warnings); both dependencies
  are completed and their assets are uncorrected.
* `cross_check.py` confirms the discordance and per-stratum cells in `code/decision_inputs.json`
  match `tasks/t0031_rq1_rq4_no_new_api_salvage/results/results_summary.md` verbatim.
* `ruff check --fix .` and `ruff format .` — clean.
  `mypy -p tasks.t0032_no_anthropic_rq1_path_decision.code` — clean.
* `flowmark --inplace --nobackup` was run on every newly written `.md` file (plan, research,
  creative-thinking, results_summary, results_detailed, answer assets, step logs).

## Limitations

* The t0031 power grid uses a single conditional-B-wins-rate (p1) sweep with fixed cap arithmetic
  ($0.16 / pair, 218 new pairs, 32 expected discordant). Real reruns deviate slightly from the
  modelled p1 grid; the qualitative conclusion (underpowering at p1 < 0.75) is robust but the exact
  power numbers are not.
* Per-stratum n's are small (SWE-bench n = 20, FrontierScience n = 26). Both p-values are reported
  as one-sided in t0031; the two-sided values are 0.0312 and 0.0625 respectively. These should be
  reported with Wilson 95% CIs (already in `rq4_stratification.json`) rather than as headline
  p-values, and the interpretation should reflect "marginal" rather than "definitive" arm-A
  advantage on FrontierScience.
* The arm-labelling comparability argument relies on the t0027 convention being the binding
  artefact. If a downstream task explicitly redefines the arm labels (for instance, "arm B is now
  any scope-aware ReAct policy on any provider"), then option (c) or (b) becomes admissible under
  that redefinition. This task does not perform that redefinition.
* The option (c) per-pair cost ($0.07) is an output-token-dominated point estimate at 2026 list
  pricing. Batch (50%) and cached-input (≈ 90%) discounts could lower it further but were excluded
  from the headline because t0027 ran online and the comparability claim is already lost.
* No bootstrap confidence band was computed on the symmetric 6 / 6 cell. C2 in
  `research/creative_thinking.md` records this as a candidate follow-up suggestion (S-0032-02);
  including it strengthens the per-stratum interpretation but does not change the headline.

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
