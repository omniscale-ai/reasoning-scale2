# RQ1 Discordance-Rich Paired Resample (Hard $35 Cap)

## Motivation

t0027's Phase 2.5 A/B/C re-run on 130 paired instances produced an underpowered RQ1 verdict:

* A=B=6 successes (4.62%); C=7 (5.38%).
* McNemar discordant pairs A vs B: **6 vs 6**, exact-binomial p=1.0.
* McNemar discordant pairs A vs C (RQ5): **4 vs 5**, p=1.0.

With only 12 discordant pairs, no realistic effect size could have produced a significant verdict.
RQ1 ("does adding granularity-aware scope conditioning improve task success vs the scope-unaware
baseline?") cannot be answered from t0027 alone.

This task closes the power gap with a discordance-rich resample of A vs B and reports an RQ1 verdict
(or a partial verdict with explicit power caveat if the budget cap is hit first).

This task covers source suggestion **S-0025-04** and follow-up suggestion **S-0027-05**.

## Scope

In scope:

* Run **arm A** (Plan-and-Solve baseline) and **arm B** (scope-aware ReAct) on a paired sample of
  instances drawn from the project's three subsets (SWE-bench Verified, taubench, frontsci),
  prioritising selection criteria that increase the expected number of discordant pairs.
* Reuse the t0027 fault-tolerant arm-B harness and the t0021 Plan-and-Solve v2 implementation as the
  canonical libraries.
* Compute McNemar paired exact-binomial test on the resulting discordant counts; report effect size,
  95% CI, and the per-subset breakdown.
* Save full predictions assets for both arms so t0030 (RQ4 stratification) can run without any
  additional API spend.

Out of scope:

* Arm C (deferred to a later wave).
* Calibrator work / RQ2 (deferred — see S-0027-01 demoted to MEDIUM in t0028).
* RQ3 instrumentation (deferred).
* Any C-arm rebuild (S-0027-02 demoted to MEDIUM in t0028).

## Hard Cost Cap and Abort Rule

**Cap**: $35.00 USD. Track spend live in `results/costs.json` after each batch of API calls and in
the harness. The budget verificator must show this task does not exceed $35 in
`effective_budget_limit_usd`.

**Abort rule**: if the cap is hit (>= $35.00 cumulative) and the running discordant-pair count is
**< 30**, halt all further API calls and proceed directly to the analysis step. Report a **partial
RQ1 verdict** with:

* Observed discordant counts (b, c).
* McNemar exact-binomial p value at the partial sample.
* Explicit power caveat: "with N_discordant = X, this analysis has power Y to detect an odds-ratio
  of Z; failure to reject H0 does not establish equivalence."
* No replacement task launched in the same wave (preserved budget and suggestion backlog for the
  next brainstorm session).

The guardrail must be implemented in the harness, not just documented — the experiment runner must
check `cumulative_cost_usd >= 35.00` after every batch and exit cleanly if true.

## Sampling Strategy

Goal: reach **>= 30 discordant pairs** between A and B.

Approach (pre-registered, in priority order):

1. **Stratified resample from t0027's 130 paired instances**: prioritise re-running on the 12
   discordant pairs from t0027 plus instances flagged by t0027's recovery distribution as "unknown"
   (B=29, C=33) where one arm's outcome is uncertain.
2. **Expand within-subset coverage**: draw additional paired instances from
   `t0010_matched_mismatch_library` first from frontsci (where t0027 showed the largest per-subset
   gap: B=0.192 vs A=0.000), then taubench, then SWE-bench Verified.
3. **Concentrate on harder difficulty bands**: t0027's per-subset table suggests A=0 outside
   SWE-bench, so RQ1 discordance is entirely driven by B≠0 outcomes; sample with bias toward
   instances where B is more likely to succeed and A more likely to fail.

Pre-register the sampling rule in `plan/plan.md` before any API call. The experiment must record how
each instance was selected.

## Method

* Use the **same Plan-and-Solve v2 (t0021)** library as arm A.
* Use the **same fault-tolerant scope-aware ReAct (t0027 final)** library as arm B.
* Use **claude-sonnet-4-6** with the fixed temperature and decoding settings from t0027.
* Re-run a paired instance only if it does not already have a usable A and B prediction in the t0027
  predictions assets — if both arms succeeded cleanly in t0027, reuse those predictions.
* Persist every API call and per-instance cost in `results/costs.json`.

## Deliverables

* `results/results_summary.md` and `results/results_detailed.md` with the McNemar verdict (full or
  partial).
* `results/metrics.json` with `mcnemar_b_count`, `mcnemar_c_count`, `mcnemar_p_value`,
  `mcnemar_effect_size`, `mcnemar_ci_lower`, `mcnemar_ci_upper`, `discordant_pairs_total`,
  `paired_n_total`, plus per-subset breakdowns.
* `results/predictions/arm_a/` and `results/predictions/arm_b/` predictions assets covering all
  paired instances actually run.
* `results/suggestions.json` describing follow-up tasks for whatever RQ remains open (RQ2
  calibrator, RQ3 instrumentation, RQ5 C rebuild) — no replacement task launched in this wave.
* Per-subset stratification table (also reused by t0030).

## Cross-references

* Source: t0028 brainstorm session 8.
* Source suggestion: S-0025-04.
* Covers: S-0027-05.
* Builds on: t0021 (Plan-and-Solve v2), t0027 (fault-tolerant arm B and harness).
* Feeds: t0030 (RQ4 info-asymmetry stratification).
