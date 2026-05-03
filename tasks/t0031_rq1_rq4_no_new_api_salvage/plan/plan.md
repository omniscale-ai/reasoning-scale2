---
spec_version: "1"
task_id: "t0031_rq1_rq4_no_new_api_salvage"
status: "complete"
date_completed: "2026-05-03"
---
# Plan — t0031_rq1_rq4_no_new_api_salvage

## Objective

Run four bounded no-new-API analyses on the existing t0026 / t0027 outputs to deliver salvage
evidence while t0029 is `intervention_blocked`. Concretely: (1) preliminary RQ4 stratification on
t0027's 130 paired instances, (2) RQ1 power/futility analysis under t0029's $35 cap, (3)
infrastructure-vs-genuine-failure audit of t0026/t0027 logs, (4) short report assembling the three
analyses with the required headline label.

## Approach

* Read all inputs from local disk only — no API calls, no remote compute.
* Implement one load helper (`load_paired_outputs.py`) that owns the single `variant → arm`
  inversion (t0027 `variant_a` → arm B scope-aware ReAct, `variant_b` → arm A Plan-and-Solve
  baseline, `variant_c` → arm C matched-mismatch).
* Implement three analysis scripts that each consume the post-inversion frame, plus a fourth
  `build_report.py` that assembles the headline-labelled summary and detailed report.
* Compute Wilson 95% CIs (closed form) and McNemar exact-binomial p-values (scipy.stats.binomtest)
  with no MC sampling.
* Produce three PNG charts in `results/images/` and embed them in `results_detailed.md`.
* Re-derive every count (especially discordance) from the loaded DataFrame — never hardcode.

## Cost Estimation

| Item | Cost (USD) |
| --- | --- |
| OpenAI / Anthropic API calls | 0.00 |
| Vast.ai compute | 0.00 |
| Local CPU only | 0.00 |
| **Total** | **0.00** |

This task carries `task_types: ["data-analysis"]` with `has_external_costs: false`. The project
budget gate is skipped per spec.

## Step by Step

1. **`code/paths.py`** — centralized `pathlib.Path` constants for the three t0027 prediction JSONL
   files, the paired manifest, the t0026 / t0027 `results/results_detailed.md` paths, the t0029 task
   description path, and the t0031 results / images output paths.

2. **`code/constants.py`** — typed constants for column names (`INSTANCE_ID`, `SUBSET`, `VARIANT`,
   `JUDGE_SUCCESS`, `RECOVERY_PATH`, `COST_USD`), arm enum (`ArmKind` = `arm_a | arm_b | arm_c`),
   subset enum (`SubsetKind` = `swebench | frontsci | taubench`), recovery-path enum (`RecoveryPath`
   = `clean | reprompt | json_fallback | all_failed | unknown`), and the t0029 plan parameters
   (`HARD_CAP_USD = 35.00`, `COST_PER_PAIR_USD = 0.16`, `DISCORDANCE_TARGET = 30`,
   `B_WINS_GRID = (0.55, 0.60, 0.65, 0.70, 0.75, 0.80)`).

3. **`code/load_paired_outputs.py`** — the single inversion point. Reads the manifest, reads the
   three JSONL prediction files, filters to the 130 paired IDs, applies
   `variant_a → arm_b, variant_b → arm_a, variant_c → arm_c`, pivots to a wide DataFrame keyed on
   `(instance_id, subset)` with columns `arm_a_judge_success`, `arm_b_judge_success`,
   `arm_a_recovery_path` (from t0027 variant B's parser path), `arm_a_cost_usd`, `arm_b_cost_usd`,
   etc. Returns a frozen `PairedFrame` dataclass with the DataFrame plus precomputed `n_total`,
   `n_per_subset`, `n_discordant`.

4. **`code/analysis_rq4_stratification.py`** — group the wide DataFrame by `subset`, cross-tabulate
   `arm_a_judge_success × arm_b_judge_success` (the standard 2x2), report cell counts, marginals,
   and Wilson 95% CIs per cell where N ≥ 5. Save the joint table to
   `results/data/rq4_stratification.json` and produce the heatmap chart
   `results/images/rq4_stratification_heatmap.png`.

5. **`code/analysis_rq1_power.py`** — given the discordance rate ρ̂ derived from the loaded
   DataFrame, simulate the t0029 plan over the `B_WINS_GRID`. For each (cap-pair-budget,
   conditional-B-wins) combination, compute the expected number of discordant pairs at cap, the
   probability that the McNemar exact-binomial p-value would reject H0 (one-sided B > A) at α =
   0.05, and the futility frontier — the conditional-B-wins floor at which the planned cap has < 80
   % power. Save the power grid to `results/data/rq1_power_grid.json` and produce
   `results/images/rq1_power_curve.png`.

6. **`code/analysis_log_audit.py`** — combine t0026 hard-failure aggregates (parsed from
   `tasks/t0026_*/results/results_detailed.md` lines 65-96 via a small regex parser) with t0027
   per-row `plan_parser_recovery_path` from the loaded DataFrame. Produce the failure breakdown
   table:

| Layer | Category | t0026 (pre-fix) | t0027 (post-fix) |
| --- | --- | --- | --- |
| infra | timeouts |  |  |
| infra | RuntimeErrors |  |  |
| infra | parser unknown |  |  |
| infra | cost-tracker errors |  |  |
| genuine | judged-fail with clean / reprompt / json_fallback path |  |  |
| genuine | parser all_failed |  |  |

   Save to `results/data/log_audit.json` and produce
   `results/images/log_audit_failure_breakdown.png`.

7. **`code/build_report.py`** — assemble `results/results_summary.md` (first line:
   `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`), `results/results_detailed.md`
   with all three charts embedded via `![desc](images/...)`, and the four mandatory JSON files
   (`metrics.json`, `costs.json`, `remote_machines_used.json`, `suggestions.json`).

8. **Run** the four analyses sequentially via `arf.scripts.utils.run_with_logs`. Total expected
   wall-time < 30 s on local CPU.

## Remote Machines

None. All analyses run on local CPU.

## Assets Needed

* `tasks/t0027_*/assets/predictions/abc-rerun-{a-reused,b,c}/files/predictions_variant_{a,b,c}.jsonl`
* `tasks/t0027_*/data/paired_manifest.json`
* `tasks/t0026_*/results/results_detailed.md`
* `tasks/t0027_*/results/results_detailed.md`
* `tasks/t0029_*/task_description.md`

All five sources are already on disk in the main repo at
`/Users/lysaniuk/Documents/reasoning-scale2/`.

## Expected Assets

None. `task.json` declares `expected_assets: {}`. The verificator emits TF-W005 (warning); this is
expected and accepted for an analysis-only task.

## Time Estimation

| Step | Effort |
| --- | --- |
| paths.py + constants.py | 5 min |
| load_paired_outputs.py | 25 min |
| analysis_rq4_stratification.py | 15 min |
| analysis_rq1_power.py | 25 min |
| analysis_log_audit.py | 20 min |
| build_report.py | 25 min |
| Run + format + verify | 15 min |
| **Total** | **≈ 2 hours** |

## Risks & Fallbacks

* **Risk: `variant_a` JSONL is the pointer asset, not actual rows.** Fallback: if the JSONL is empty
  or contains a single pointer record, read t0026's `variant_a` predictions directly from
  `tasks/t0026_*/assets/predictions/variant_a/files/predictions_variant_a.jsonl`.
* **Risk: per-row schema differs slightly between B and A (A lacks `plan_parser_recovery_path`).**
  Fallback: load helper inserts `arm_b_recovery_path = "n/a"` for the scope-aware ReAct rows; the
  audit script counts only B's recovery paths.
* **Risk: discordance rate from t0027 differs from the documented ~9.2%.** Fallback: report the
  re-derived value verbatim and flag any discrepancy in `results_detailed.md`.
* **Risk: McNemar exact-binomial floor on small discordant N.** Mitigation: power analysis reports
  both the expected discordant N at cap and the achievable p-value floor; if the floor exceeds 0.05
  even at 30 discordant pairs, the futility verdict is reported clearly.

## Verification Criteria

* `verify_plan` passes (one orchestrator-managed warning PL-W009 expected).
* `verify_logs` passes for all step folders.
* `results_summary.md` first line equals exactly
  `NO-NEW-API PRELIMINARY EVIDENCE — NOT A REPLACEMENT FOR t0029`.
* `results/images/` contains exactly three PNG charts: `rq4_stratification_heatmap.png`,
  `rq1_power_curve.png`, `log_audit_failure_breakdown.png`.
* `costs.json` reports `total_cost_usd: 0.00`.
* `remote_machines_used.json` is `[]`.
* The discordance count cited in `results_summary.md` matches the value computed by
  `load_paired_outputs.py` from the loaded DataFrame.
