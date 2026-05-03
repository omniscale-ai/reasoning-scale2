# ❌ Tasks: Cancelled

3 tasks. ❌ **3 cancelled**.

[Back to all tasks](../README.md)

---

## ❌ Cancelled

<details>
<summary>❌ 0023 — <strong>Phase 2 Confirmatory ABC Run with Sonnet on
SWE-bench</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0023_phase2_abc_confirmatory_sonnet_swebench` |
| **Status** | cancelled |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0012-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Task page** | [Phase 2 Confirmatory ABC Run with Sonnet on SWE-bench](../../../overview/tasks/task_pages/t0023_phase2_abc_confirmatory_sonnet_swebench.md) |
| **Task folder** | [`t0023_phase2_abc_confirmatory_sonnet_swebench/`](../../../tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/) |

# Phase 2 Confirmatory ABC Run with Sonnet on SWE-bench

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor on all three
ABC conditions (A: 2.5%, B: 0%, C: 0%). It cannot answer RQ1 (does scope-aware A beat
scope-unaware B), RQ2 (do gains concentrate in scope-sensitive states), or RQ5 (do
scope-mismatched C agents degrade predictably) because the conditions are indistinguishable at
the floor.

Per the t0017 literature survey, three changes lift the experiment out of the floor regime:

1. **Stronger model**: claude-sonnet-4-6 instead of haiku (the literature consensus is that
   scope-conditioning effects only become legible above ~30% baseline accuracy, see Wang2023
   and Boisvert2024).
2. **Tractable benchmark**: SWE-bench Verified Lite at the per-instance level (haiku achieves
   roughly 12-18% on the public leaderboard for similar lite splits; sonnet should reach
   30-50%).
3. **Continuous and diagnostic metrics**: progress rate (Ma2024) plus EAI error taxonomy
   (Li2024), wired in via t0022, replace the binary-success metric that collapsed t0012.

This is the **headline experiment** of the upcoming paper. Everything in Wave 1 (t0019, t0020)
defends the schema headline; everything in Wave 2 (t0021, t0022) builds the instruments;
**Wave 3 (this task) produces the confirmatory N>=157 signal that the paper claims**.

This task covers `S-0012-02` (primary) and `S-0010-01` (secondary; the C-condition variants
provide partial coverage).

## Scope

Run a paired ABC experiment on **N>=157 SWE-bench Verified Lite instances** with
claude-sonnet-4-6, using the t0021 v2 Plan-and-Solve library (which emits `final_confidence`)
and the t0022 metrics library (progress rate + EAI error taxonomy).

Three conditions per instance, in randomized order to defuse position bias:

* **A scope-aware**: the agent receives the v2 hierarchical scope tag for each step.
* **B scope-unaware**: the agent receives no scope tag (matches the base Plan-and-Solve
  setting).
* **C scope-mismatched**: the agent receives a wrong scope tag.

C-condition variants (per S-0010-01):

* `C-random`: tag drawn uniformly from the wrong-tag set with seed=0.
* `C-adversarial`: tag chosen to be the most distant from the true scope (e.g., atomic on a
  global step).

If budget allows, also run a `C-phase-randomized` control where the hierarchy itself is
shuffled within the row but the tag is correct; this isolates step-order from scope-mismatch.

## Sample Size and Power

* **N>=157 paired rows** per condition (Phase 1 confirmatory power calculation from t0012's
  smoke output): detects a 10 pp success-rate delta at alpha=0.05 with power 0.8 under McNemar
  pairing.
* **Annotation pre-step**: SWE-bench Verified Lite needs hierarchical-decomposition
  annotations for the agent's scope-tag input. The current dataset has 23 SWE-bench rows from
  t0012; this task **must annotate ~150 fresh instances** before the agent runs. Annotation
  uses claude-haiku-4-5 with the t0014 v2 schema.

## Deliverables

1. **Predictions asset** (`assets/predictions/phase2_abc_swebench_sonnet/`): per-row
   trajectories for all three conditions plus the C variants, with `final_confidence`,
   `progress_rate`, and error taxonomy distributions filled in.
2. **Answer asset** addressing RQ1 ("Does explicit operating-granularity conditioning improve
   final task success?") with explicit numerical answers for:
   * `success_rate(A) - success_rate(B)` with 95% CI from McNemar paired test
   * `progress_rate(A) - progress_rate(B)` with 95% CI from paired t-test
   * `success_rate(A) - success_rate(C-random)` and `... - success_rate(C-adversarial)`
   * `overconfident_error_rate` per condition (using `final_confidence` from t0021)
3. **Reported metrics** in `results/metrics.json` (explicit multi-variant) covering:
   * Per condition: `task_success_rate`, `progress_rate_mean`, `overconfident_error_rate`,
     plus per-error-taxonomy-label counts.
   * Paired-difference statistics: McNemar p-values, paired t-test p-values, effect sizes.
   * Efficiency: `efficiency_inference_time_per_item_seconds`,
     `efficiency_inference_cost_per_item_usd` (per condition).
4. **Hard/easy split analysis** by SWE-bench Verified hunk count (RQ9): does
   scope-conditioning value increase with task complexity? Reported in
   `results/results_detailed.md` with per-bucket deltas and 95% CIs.
5. **Compare-literature step**: side-by-side table of A-vs-B deltas with Wang2023 and
   Boisvert2024's scope-conditioning numbers.

## Models and Configurations

* **Annotator** (pre-step): claude-haiku-4-5 with v2 tree schema (matching t0014).
* **Agent**: claude-sonnet-4-6 via the t0021 v2 Plan-and-Solve library.
* **Judge / metric scorer**: claude-haiku-4-5 (default; per t0022 cost analysis), with a
  sonnet spot-check on a 20-row stratified sample to bound judge bias.

## Cost Estimate

* **Annotation pre-step** (about 150 fresh SWE-bench rows with haiku at v2 schema): about 150
  calls, around 6k tokens in / 1k tokens out per call. **About $11**.
* **Agent run** (N=157 x 3 conditions + 1 C variant on a 50-row subset = 521 trajectories,
  about 10 calls per trajectory averaging 8k tokens in / 1k tokens out at sonnet pricing):
  about 5.2M input tokens, about 520k output tokens. **About $23-25**.
* **Metric scoring** (per t0022 cost analysis): **about $3**.
* **Sonnet spot-check** (20 rows x 3 conditions x about 5 steps = 300 calls, about 3k in, 200
  out at sonnet pricing): **about $3**.
* **Reserve for retries / extra rows**: **+$3**.
* **Total**: **about $40-45**. The per-task limit may need to be raised; pre-flag as a budget
  intervention. If it does not get raised, drop the C-adversarial variant or the sonnet
  spot-check.

## Decision Criteria (Headline)

* If `success_rate(A) - success_rate(B) >= +5 pp` with McNemar p<0.05, the paper's central
  claim (RQ1) holds and the v2 schema produces a **legible**, **non-floor**, **paired**
  signal.
* If `progress_rate(A) - progress_rate(B) >= +0.05` with paired-t p<0.05 even when binary
  success is closer, the granularity-conditioning effect manifests in subgoal coverage rather
  than terminal success. Both interpretations support the headline.
* If both deltas are within +/-2 pp / +/-0.02 of zero with tight CIs, the v2 schema does not
  transfer from offline annotation accept-rate to online agent task success on this benchmark;
  the paper pivots to "schema helps annotation, not online agents" and the brainstorm round
  after this task scopes the next experiment.
* The C-adversarial penalty must be at least as large as C-random for RQ5 to hold.

## Dependencies

* `t0021_plan_and_solve_v2_with_final_confidence` (library that emits `final_confidence`).
* `t0022_abc_harness_progress_rate_and_error_taxonomy` (progress rate + EAI taxonomy).

Both are in flight as of this task's creation. Sequential dependency: t0023 cannot start
implementation until both libraries pass their own verification.

## Source Suggestion

`S-0012-02` (primary). `S-0010-01` is partially covered by the C-random and C-adversarial
variants; the phase-randomized control is in scope only if budget permits.

## Risks and Fallbacks

* **Budget overrun**: if the run-cost exceeds $40, drop the C-adversarial variant first (saves
  about $5), then the sonnet spot-check (about $3). The paired A/B/C-random comparison is the
  minimum viable headline.
* **Sonnet hits a different floor on SWE-bench**: if A-condition success rate at N=20 pilot is
  below 10%, abort the full run and recompute the power requirement at the new effect size.
* **Annotation cost dominates**: if the v2 annotation pre-step exceeds $15, switch to a
  three-shot prompt instead of the full v2 schema for the SWE-bench corpus only and document
  the schema simplification.
* **Judge bias on SWE-bench**: SWE-bench has a deterministic test-suite ground truth, so
  task_success is judge-free. Progress rate is judge-dependent; the sonnet spot-check exists
  to bound this bias.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has explicit variants for A, B, C-random, and (if run) C-adversarial,
  each with task_success_rate, progress_rate_mean, overconfident_error_rate, and efficiency
  metrics.
* Paired-difference statistics for at least RQ1 and RQ5 are reported with explicit p-values.
* `results/results_detailed.md` contains the hard/easy split analysis (RQ9) and the
  literature-comparison table.
* Cost in `results/costs.json` is documented with the per-stage breakdown above and is at or
  below the agreed limit (currently ~$45).

</details>

<details>
<summary>❌ 0029 — <strong>RQ1 discordance-rich paired resample with hard $35
cap</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0029_rq1_discordance_rich_resample` |
| **Status** | cancelled |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Expected assets** | 2 predictions |
| **Source suggestion** | `S-0025-04` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`comparative-analysis`](../../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-05-03T09:55:36Z |
| **End time** | 2026-05-03T14:21:00Z |
| **Task page** | [RQ1 discordance-rich paired resample with hard $35 cap](../../../overview/tasks/task_pages/t0029_rq1_discordance_rich_resample.md) |
| **Task folder** | [`t0029_rq1_discordance_rich_resample/`](../../../tasks/t0029_rq1_discordance_rich_resample/) |

# RQ1 Discordance-Rich Paired Resample (Hard $35 Cap)

## Motivation

t0027's Phase 2.5 A/B/C re-run on 130 paired instances produced an underpowered RQ1 verdict:

* A=B=6 successes (4.62%); C=7 (5.38%).
* McNemar discordant pairs A vs B: **6 vs 6**, exact-binomial p=1.0.
* McNemar discordant pairs A vs C (RQ5): **4 vs 5**, p=1.0.

With only 12 discordant pairs, no realistic effect size could have produced a significant
verdict. RQ1 ("does adding granularity-aware scope conditioning improve task success vs the
scope-unaware baseline?") cannot be answered from t0027 alone.

This task closes the power gap with a discordance-rich resample of A vs B and reports an RQ1
verdict (or a partial verdict with explicit power caveat if the budget cap is hit first).

This task covers source suggestion **S-0025-04** and follow-up suggestion **S-0027-05**.

## Scope

In scope:

* Run **arm A** (Plan-and-Solve baseline) and **arm B** (scope-aware ReAct) on a paired sample
  of instances drawn from the project's three subsets (SWE-bench Verified, taubench,
  frontsci), prioritising selection criteria that increase the expected number of discordant
  pairs.
* Reuse the t0027 fault-tolerant arm-B harness and the t0021 Plan-and-Solve v2 implementation
  as the canonical libraries.
* Compute McNemar paired exact-binomial test on the resulting discordant counts; report effect
  size, 95% CI, and the per-subset breakdown.
* Save full predictions assets for both arms so t0030 (RQ4 stratification) can run without any
  additional API spend.

Out of scope:

* Arm C (deferred to a later wave).
* Calibrator work / RQ2 (deferred — see S-0027-01 demoted to MEDIUM in t0028).
* RQ3 instrumentation (deferred).
* Any C-arm rebuild (S-0027-02 demoted to MEDIUM in t0028).

## Hard Cost Cap and Abort Rule

**Cap**: $35.00 USD. Track spend live in `results/costs.json` after each batch of API calls
and in the harness. The budget verificator must show this task does not exceed $35 in
`effective_budget_limit_usd`.

**Abort rule**: if the cap is hit (>= $35.00 cumulative) and the running discordant-pair count
is **< 30**, halt all further API calls and proceed directly to the analysis step. Report a
**partial RQ1 verdict** with:

* Observed discordant counts (b, c).
* McNemar exact-binomial p value at the partial sample.
* Explicit power caveat: "with N_discordant = X, this analysis has power Y to detect an
  odds-ratio of Z; failure to reject H0 does not establish equivalence."
* No replacement task launched in the same wave (preserved budget and suggestion backlog for
  the next brainstorm session).

The guardrail must be implemented in the harness, not just documented — the experiment runner
must check `cumulative_cost_usd >= 35.00` after every batch and exit cleanly if true.

## Sampling Strategy

Goal: reach **>= 30 discordant pairs** between A and B.

Approach (pre-registered, in priority order):

1. **Stratified resample from t0027's 130 paired instances**: prioritise re-running on the 12
   discordant pairs from t0027 plus instances flagged by t0027's recovery distribution as
   "unknown" (B=29, C=33) where one arm's outcome is uncertain.
2. **Expand within-subset coverage**: draw additional paired instances from
   `t0010_matched_mismatch_library` first from frontsci (where t0027 showed the largest
   per-subset gap: B=0.192 vs A=0.000), then taubench, then SWE-bench Verified.
3. **Concentrate on harder difficulty bands**: t0027's per-subset table suggests A=0 outside
   SWE-bench, so RQ1 discordance is entirely driven by B≠0 outcomes; sample with bias toward
   instances where B is more likely to succeed and A more likely to fail.

Pre-register the sampling rule in `plan/plan.md` before any API call. The experiment must
record how each instance was selected.

## Method

* Use the **same Plan-and-Solve v2 (t0021)** library as arm A.
* Use the **same fault-tolerant scope-aware ReAct (t0027 final)** library as arm B.
* Use **claude-sonnet-4-6** with the fixed temperature and decoding settings from t0027.
* Re-run a paired instance only if it does not already have a usable A and B prediction in the
  t0027 predictions assets — if both arms succeeded cleanly in t0027, reuse those predictions.
* Persist every API call and per-instance cost in `results/costs.json`.

## Deliverables

* `results/results_summary.md` and `results/results_detailed.md` with the McNemar verdict
  (full or partial).
* `results/metrics.json` with `mcnemar_b_count`, `mcnemar_c_count`, `mcnemar_p_value`,
  `mcnemar_effect_size`, `mcnemar_ci_lower`, `mcnemar_ci_upper`, `discordant_pairs_total`,
  `paired_n_total`, plus per-subset breakdowns.
* `results/predictions/arm_a/` and `results/predictions/arm_b/` predictions assets covering
  all paired instances actually run.
* `results/suggestions.json` describing follow-up tasks for whatever RQ remains open (RQ2
  calibrator, RQ3 instrumentation, RQ5 C rebuild) — no replacement task launched in this wave.
* Per-subset stratification table (also reused by t0030).

## Cross-references

* Source: t0028 brainstorm session 8.
* Source suggestion: S-0025-04.
* Covers: S-0027-05.
* Builds on: t0021 (Plan-and-Solve v2), t0027 (fault-tolerant arm B and harness).
* Feeds: t0030 (RQ4 info-asymmetry stratification).

</details>

<details>
<summary>❌ 0030 — <strong>RQ4 info-asymmetry stratification analysis on t0029
outputs</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0030_rq4_info_asymmetry_stratification` |
| **Status** | cancelled |
| **Effective date** | 2026-05-03 |
| **Dependencies** | [`t0029_rq1_discordance_rich_resample`](../../../overview/tasks/task_pages/t0029_rq1_discordance_rich_resample.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | — |
| **Task types** | [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **End time** | 2026-05-03T14:21:00Z |
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
