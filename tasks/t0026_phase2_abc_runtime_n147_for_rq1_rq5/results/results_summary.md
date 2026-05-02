# t0026 Phase 2 A/B/C Runtime — Results Summary

## Summary

The strict double inequality `success(A) > success(B) > success(C)` posited by RQ5 is **not
supported**. On the paired N=130 set (the same 130 instances run by every variant), variants A and B
are statistically tied, and the adversarial-mismatched variant C significantly outperforms B. The
sweep ran the full A/B/C × {SWE-bench, Tau-bench, FrontierScience} grid against `claude-sonnet-4-6`
with a paired McNemar test on each pair, an Expected Calibration Error on variant B's verbalized
`final_confidence`, and a sonnet/opus inter-judge agreement check. RQ3 (judge ↔ program-truth
agreement) and RQ4 (B's calibration) are answered cleanly. RQ1, RQ2, RQ5 are rejected by the data.

| Pair | discordant (1st-only) | discordant (2nd-only) | McNemar p | Bonferroni alpha |
| --- | --- | --- | --- | --- |
| A vs B | 6 | 6 | 1.000 | 0.025 |
| B vs C | 4 | 15 | **0.019** | 0.025 |

Both pairwise tests must reach significance for RQ5 to be affirmed. A vs B fails (p ≈ 1.0). B vs C
is significant in the *opposite* direction from RQ5: C beats B.

## Per-RQ Outcomes

* **RQ1 (A > B?)** — **Not supported.** Paired McNemar A vs B is symmetric (6/6 discordant pairs, p
  ≈ 1.0). The two variants are indistinguishable on success rate at this sample size.
* **RQ2 (C < A?)** — **Not supported.** C beats A on the headline rate (11.6% vs 4.1%); the
  primary-test pair targeted in this task is B vs C, which is significant in the wrong direction for
  the original RQ.
* **RQ3 (judge ↔ program agreement)** — **Strong agreement.** Sonnet judge agrees with programmatic
  ground truth on **91.7%** of items (n=120) and with the opus judge on **97.7%** of the inter-judge
  slice (n=89).
* **RQ4 (final_confidence calibration)** — **Mis-calibrated.** Variant B's 10-bin Expected
  Calibration Error is **0.43** (n=49). Bins around 0.6-1.0 confidence have empirical success rates
  ≤ 0.25.
* **RQ5 (strict A > B > C)** — **Rejected.** `rq5_strict_inequality_supported = false`.

## Overall Success Rates (denominator = 147 target instances)

| Variant | overall | SWE-bench | Tau-bench | FrontierScience |
| --- | --- | --- | --- | --- |
| A scope-aware ReAct | 4.1% | 30.0% | 0.0% | 0.0% |
| B Plan-and-Solve v2 | 4.1% | 0.0% | 2.3% | 10.0% |
| C mismatched-adversarial | 11.6% | 5.0% | 10.3% | 17.5% |

The subset-level pattern is the most striking finding: A wins decisively on SWE-bench, C wins on
Tau-bench and FrontierScience, B wins nowhere.

## What Drives the Inversion

Variant B accumulates **16 `MalformedPlanError` failures** (12% of B's 130 runs) — its
Plan-and-Solve schema is brittle to noisy plans. Variant C delegates to scope-aware ReAct under an
"adversarial" wrapper, so it never trips the plan parser. The "adversarial" label turns out to be
partly cosmetic in this implementation: C is structurally a noisier variant of A, not a weaker
variant of B. See `logs/steps/011_creative-thinking/step_log.md` for the full set of candidate
explanations.

Variant-level failure breakdown (errors recorded as non-success):

* A: 12 timeouts, 1 runtime error → 13 of 130 runs failed
* B: 22 timeouts, 2 runtime errors, 16 MalformedPlanError → 40 of 130 runs failed
* C: 43 timeouts, 1 runtime error → 44 of 130 runs failed

C's higher timeout count is the cost of its longer reasoning chains, but the ones that *do* finish
land more often on the judge-friendly short answer.

## Cost and Compute

* Inference cost (runs only): **$26.07** across 390 trajectories (130 × 3 variants).
* Cost per item (runs): **$0.066**. Judges plus inter-judge slice add to the project total but are
  not in the per-item efficiency metric.
* Wall-clock for the full sweep (run + judge phases): ~6.1 hours, executed in parallel via
  `ThreadPoolExecutor(max_workers=8)` for both runs and judges.
* Hard cap was $135; we are well under.

## Caveats

* Paired set is N=130, not the planned N=147. 17 instances per variant were filtered out by the
  resumable-checkpoint path because pre-existing trajectory files from a corrupted earlier run were
  still on disk. The same 17 ids are missing across A, B, and C, so the *paired* tests remain valid;
  the *absolute* success rates are biased to the extent the skipped set is non-random.
* Tau-bench was run without a real tool registry (stub `python_exec` only), so all three variants
  collapse to "describe what you would do." Tau-bench numbers in this report should be read as a
  harness-bound floor, not a real Tau-bench score.
* Variant B is the only variant with a `final_confidence` head; ECE = 0.43 is the calibration of B
  alone. RQ4 is answered for B but is not a cross-variant comparison.

## Outputs

* Metrics: `results/metrics.json`
* Per-pair McNemar: `data/mcnemar_results.json`
* Calibration: `data/calibration.json`
* Judge agreement: `data/judge_agreement.json`
* Trajectories: `data/runs/{a,b,c}/trajectory_*.json` (390 files)
* Predictions assets: `assets/predictions/{a-scope-aware,b-plan-and-solve,c-mismatched}/`
* Charts:
  `results/images/{success_rate_by_subset,success_rate_overall,calibration_reliability,mcnemar_discordants}.png`

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| `success_rate_a` | 0.0408 | 6 / 147 |
| `success_rate_b` | 0.0408 | 6 / 147 |
| `success_rate_c` | 0.1156 | 17 / 147 |
| `mcnemar_p_a_vs_b` | 1.000 | exact binomial, paired N=130 |
| `mcnemar_p_b_vs_c` | 0.019 | exact binomial, paired N=130 (Bonferroni α = 0.025) |
| `rq5_strict_inequality_supported` | false | both pairwise tests must clear α; only B vs C does, in the wrong direction |
| `final_confidence_ece` | 0.4302 | n = 49, 10-bin equal-width ECE on variant B |
| `judge_agreement_with_program` | 0.9167 | n = 120; sonnet judge vs programmatic ground truth |
| `inter_judge_agreement` | 0.9775 | n = 89; sonnet vs opus on the inter-judge slice |
| `efficiency_inference_cost_per_item_usd` | 0.066 | runs only, averaged across A+B+C |

Full machine-readable payload: `results/metrics.json`.

## Verification

* `rq5_strict_inequality_supported` is present in `results/metrics.json` and equals `false`.
* `mcnemar_p_a_vs_b` ≈ 1.000 and `mcnemar_p_b_vs_c` < 0.025 (Bonferroni-adjusted alpha for two
  pairwise tests).
* `final_confidence_ece` is reported with `n_total > 0` (n = 49).
* `judge_agreement_with_program` and `inter_judge_agreement` are reported with sample sizes (n = 120
  and n = 89 respectively).
* All four headline charts present in `results/images/`: `success_rate_overall.png`,
  `success_rate_by_subset.png`, `calibration_reliability.png`, `mcnemar_discordants.png`.
* Paired N=130 set is documented in the Caveats section above (17 instances filtered by the
  resumable-checkpoint path; same ids missing across A, B, C, so paired tests remain valid).
