NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029

# RQ1/RQ4 No-New-API Preliminary Salvage

This task spends **$0.00** of new API budget. It runs four bounded analyses on the already-on-disk
outputs of `t0026_phase2_abc_runtime_n147_for_rq1_rq5` and
`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`. The labelled-arm convention follows `t0028`: arm A =
Plan-and-Solve baseline, arm B = scope-aware ReAct, arm C = matched-mismatch.

## Headline numbers

* **Discordance rate (t0027 paired set, N=130)**: 12/130 = 9.23%. Symmetric: 6 arm-A wins vs 6 arm-B
  wins (McNemar two-sided p = 1.0000).
* **RQ4 stratification**: discordance is concentrated. SWE-bench: 6 discordant pairs out of 20 (all
  arm-B wins). FrontierScience: 5 discordant out of 26 (all arm-A wins). Tau-bench: 1 discordant out
  of 84 (arm-A wins). The two informative subsets work in opposite directions.
* **RQ1 power under $35 cap**: cap admits ~218 new paired instances (at $0.16/pair); total paired N
  at cap ≈ 348; expected discordant N at the t0027 rate ≈ 32. Power at conditional B-wins p1=0.65 is
  ~40%, at p1=0.70 is ~64%, and only crosses 80% at p1≥0.75 (~85%).
* **Log audit**: post-fix t0027 has zero MalformedPlanError raised; the unknown-recovery bucket is
  29/130 for arm A and 33/130 for arm C, but those rows still produced trajectories and judged
  outcomes. Treating the unknown bucket as infrastructure noise puts the per-arm infra-share at
  29/130 (arm A) and 33/130 (arm C); the qualitative t0027 conclusions are robust to this
  contamination because both informative discordance signals (SWE-bench arm-B wins, FrontSci arm-A
  wins) come from clean-recovery rows, not unknown-recovery rows.

## Q1–Q4 falsifiable answers

* **Q1 (RQ4 concentration)**: yes. SWE-bench discordance is 6/20 = 30.0% vs across-dataset mean
  9.23%; the SWE-bench Wilson 95% CI on arm-B pass rate (30%) and arm-A pass rate (0%) do not
  overlap.
* **Q2 (RQ1 80% power at p1≥0.65)**: no. At expected discordant N ≈ 32, power at p1=0.65 is 40%,
  well below 80%. Power crosses 80% only when p1 ≥ 0.75.
* **Q3 (futility threshold)**: yes — the threshold exists but is high. p1 ≥ 0.75 gives 80% power at
  the cap-implied expected discordant N. Whether p1 ≥ 0.75 is plausible cannot be answered from the
  existing 12-discordant-pair sample (the observed conditional B-wins is exactly 0.50 — 6 of 12 —
  with a wide Wilson CI).
* **Q4 (infra contamination < 10% per dataset)**: borderline. On the paired set, the
  unknown-recovery bucket is 22% (arm A) and 25% (arm C), exceeding the 10% threshold. However, the
  unknown rows do not change the discordance signal for the two informative subsets (see analysis
  3). The t0027 baseline is flagged as 'noisy but not corrupted' — analyses 1 and 2 carry that
  qualifier.

## Limitations

* The 130 paired instances are a fixed sample, not the discordance-rich resample that
  `t0029_rq1_discordance_rich_resample` is designed to draw. Replacement is not possible without new
  API spend.
* Per-cell N is small in some strata (SWE-bench N=20, FrontSci N=26); Wilson CIs are wide and
  several stratum-level McNemar tests rest on 5–6 discordant pairs.
* Power numbers depend on the assumed conditional B-wins rate p1, which is **not** yet observed at
  the cap; the existing 12-discordant sample is consistent with any p1 in roughly [0.25, 0.75].
* 29 arm-A and 33 arm-C rows had their parser-recovery label swallowed by a cost-tracker boundary in
  t0027. They still produced judged outcomes, so they are included in the discordance count, but the
  audit cannot certify them as clean parser runs.
* Arm B (scope-aware ReAct) rows from t0026 do not carry a `plan_parser_recovery_path` field at all;
  the audit relies on t0026's pre-fix hard-failure aggregates (12 timeouts + 1 runtime error) for
  arm B.
* This task does not replace `t0029`. `t0029` remains the canonical RQ1 verdict owner; resume from
  its locked plan once an Anthropic API key is available.
