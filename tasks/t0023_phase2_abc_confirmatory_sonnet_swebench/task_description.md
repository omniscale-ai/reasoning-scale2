# Phase 2 Confirmatory ABC Run with Sonnet on SWE-bench

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor on all three ABC
conditions (A: 2.5%, B: 0%, C: 0%). It cannot answer RQ1 (does scope-aware A beat scope-unaware B),
RQ2 (do gains concentrate in scope-sensitive states), or RQ5 (do scope-mismatched C agents degrade
predictably) because the conditions are indistinguishable at the floor.

Per the t0017 literature survey, three changes lift the experiment out of the floor regime:

1. **Stronger model**: claude-sonnet-4-6 instead of haiku (the literature consensus is that
   scope-conditioning effects only become legible above ~30% baseline accuracy, see Wang2023 and
   Boisvert2024).
2. **Tractable benchmark**: SWE-bench Verified Lite at the per-instance level (haiku achieves
   roughly 12-18% on the public leaderboard for similar lite splits; sonnet should reach 30-50%).
3. **Continuous and diagnostic metrics**: progress rate (Ma2024) plus EAI error taxonomy (Li2024),
   wired in via t0022, replace the binary-success metric that collapsed t0012.

This is the **headline experiment** of the upcoming paper. Everything in Wave 1 (t0019, t0020)
defends the schema headline; everything in Wave 2 (t0021, t0022) builds the instruments; **Wave 3
(this task) produces the confirmatory N>=157 signal that the paper claims**.

This task covers `S-0012-02` (primary) and `S-0010-01` (secondary; the C-condition variants provide
partial coverage).

## Scope

Run a paired ABC experiment on **N>=157 SWE-bench Verified Lite instances** with claude-sonnet-4-6,
using the t0021 v2 Plan-and-Solve library (which emits `final_confidence`) and the t0022 metrics
library (progress rate + EAI error taxonomy).

Three conditions per instance, in randomized order to defuse position bias:

* **A scope-aware**: the agent receives the v2 hierarchical scope tag for each step.
* **B scope-unaware**: the agent receives no scope tag (matches the base Plan-and-Solve setting).
* **C scope-mismatched**: the agent receives a wrong scope tag.

C-condition variants (per S-0010-01):

* `C-random`: tag drawn uniformly from the wrong-tag set with seed=0.
* `C-adversarial`: tag chosen to be the most distant from the true scope (e.g., atomic on a global
  step).

If budget allows, also run a `C-phase-randomized` control where the hierarchy itself is shuffled
within the row but the tag is correct; this isolates step-order from scope-mismatch.

## Sample Size and Power

* **N>=157 paired rows** per condition (Phase 1 confirmatory power calculation from t0012's smoke
  output): detects a 10 pp success-rate delta at alpha=0.05 with power 0.8 under McNemar pairing.
* **Annotation pre-step**: SWE-bench Verified Lite needs hierarchical-decomposition annotations for
  the agent's scope-tag input. The current dataset has 23 SWE-bench rows from t0012; this task
  **must annotate ~150 fresh instances** before the agent runs. Annotation uses claude-haiku-4-5
  with the t0014 v2 schema.

## Deliverables

1. **Predictions asset** (`assets/predictions/phase2_abc_swebench_sonnet/`): per-row trajectories
   for all three conditions plus the C variants, with `final_confidence`, `progress_rate`, and error
   taxonomy distributions filled in.
2. **Answer asset** addressing RQ1 ("Does explicit operating-granularity conditioning improve final
   task success?") with explicit numerical answers for:
   * `success_rate(A) - success_rate(B)` with 95% CI from McNemar paired test
   * `progress_rate(A) - progress_rate(B)` with 95% CI from paired t-test
   * `success_rate(A) - success_rate(C-random)` and `... - success_rate(C-adversarial)`
   * `overconfident_error_rate` per condition (using `final_confidence` from t0021)
3. **Reported metrics** in `results/metrics.json` (explicit multi-variant) covering:
   * Per condition: `task_success_rate`, `progress_rate_mean`, `overconfident_error_rate`, plus
     per-error-taxonomy-label counts.
   * Paired-difference statistics: McNemar p-values, paired t-test p-values, effect sizes.
   * Efficiency: `efficiency_inference_time_per_item_seconds`,
     `efficiency_inference_cost_per_item_usd` (per condition).
4. **Hard/easy split analysis** by SWE-bench Verified hunk count (RQ9): does scope-conditioning
   value increase with task complexity? Reported in `results/results_detailed.md` with per-bucket
   deltas and 95% CIs.
5. **Compare-literature step**: side-by-side table of A-vs-B deltas with Wang2023 and Boisvert2024's
   scope-conditioning numbers.

## Models and Configurations

* **Annotator** (pre-step): claude-haiku-4-5 with v2 tree schema (matching t0014).
* **Agent**: claude-sonnet-4-6 via the t0021 v2 Plan-and-Solve library.
* **Judge / metric scorer**: claude-haiku-4-5 (default; per t0022 cost analysis), with a sonnet
  spot-check on a 20-row stratified sample to bound judge bias.

## Cost Estimate

* **Annotation pre-step** (about 150 fresh SWE-bench rows with haiku at v2 schema): about 150 calls,
  around 6k tokens in / 1k tokens out per call. **About $11**.
* **Agent run** (N=157 x 3 conditions + 1 C variant on a 50-row subset = 521 trajectories, about 10
  calls per trajectory averaging 8k tokens in / 1k tokens out at sonnet pricing): about 5.2M input
  tokens, about 520k output tokens. **About $23-25**.
* **Metric scoring** (per t0022 cost analysis): **about $3**.
* **Sonnet spot-check** (20 rows x 3 conditions x about 5 steps = 300 calls, about 3k in, 200 out at
  sonnet pricing): **about $3**.
* **Reserve for retries / extra rows**: **+$3**.
* **Total**: **about $40-45**. The per-task limit may need to be raised; pre-flag as a budget
  intervention. If it does not get raised, drop the C-adversarial variant or the sonnet spot-check.

## Decision Criteria (Headline)

* If `success_rate(A) - success_rate(B) >= +5 pp` with McNemar p<0.05, the paper's central claim
  (RQ1) holds and the v2 schema produces a **legible**, **non-floor**, **paired** signal.
* If `progress_rate(A) - progress_rate(B) >= +0.05` with paired-t p<0.05 even when binary success is
  closer, the granularity-conditioning effect manifests in subgoal coverage rather than terminal
  success. Both interpretations support the headline.
* If both deltas are within +/-2 pp / +/-0.02 of zero with tight CIs, the v2 schema does not
  transfer from offline annotation accept-rate to online agent task success on this benchmark; the
  paper pivots to "schema helps annotation, not online agents" and the brainstorm round after this
  task scopes the next experiment.
* The C-adversarial penalty must be at least as large as C-random for RQ5 to hold.

## Dependencies

* `t0021_plan_and_solve_v2_with_final_confidence` (library that emits `final_confidence`).
* `t0022_abc_harness_progress_rate_and_error_taxonomy` (progress rate + EAI taxonomy).

Both are in flight as of this task's creation. Sequential dependency: t0023 cannot start
implementation until both libraries pass their own verification.

## Source Suggestion

`S-0012-02` (primary). `S-0010-01` is partially covered by the C-random and C-adversarial variants;
the phase-randomized control is in scope only if budget permits.

## Risks and Fallbacks

* **Budget overrun**: if the run-cost exceeds $40, drop the C-adversarial variant first (saves about
  $5), then the sonnet spot-check (about $3). The paired A/B/C-random comparison is the minimum
  viable headline.
* **Sonnet hits a different floor on SWE-bench**: if A-condition success rate at N=20 pilot is below
  10%, abort the full run and recompute the power requirement at the new effect size.
* **Annotation cost dominates**: if the v2 annotation pre-step exceeds $15, switch to a three-shot
  prompt instead of the full v2 schema for the SWE-bench corpus only and document the schema
  simplification.
* **Judge bias on SWE-bench**: SWE-bench has a deterministic test-suite ground truth, so
  task_success is judge-free. Progress rate is judge-dependent; the sonnet spot-check exists to
  bound this bias.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has explicit variants for A, B, C-random, and (if run) C-adversarial, each
  with task_success_rate, progress_rate_mean, overconfident_error_rate, and efficiency metrics.
* Paired-difference statistics for at least RQ1 and RQ5 are reported with explicit p-values.
* `results/results_detailed.md` contains the hard/easy split analysis (RQ9) and the
  literature-comparison table.
* Cost in `results/costs.json` is documented with the per-stage breakdown above and is at or below
  the agreed limit (currently ~$45).
