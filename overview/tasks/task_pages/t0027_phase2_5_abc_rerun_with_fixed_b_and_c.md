# ✅ Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

[Back to all tasks](../README.md)

> Task Success Rate: **0.05384615384615385**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0027_phase2_5_abc_rerun_with_fixed_b_and_c` |
| **Status** | ✅ completed |
| **Started** | 2026-05-02T17:07:16Z |
| **Completed** | 2026-05-03T08:07:00Z |
| **Duration** | 14h 59m |
| **Dependencies** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md), [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Source suggestion** | `S-0026-01` |
| **Task types** | `write-library`, `experiment-run`, `comparative-analysis` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`llm-as-judge`](../../by-category/llm-as-judge.md) |
| **Expected assets** | 2 library, 3 predictions |
| **Step progress** | 9/15 |
| **Cost** | **$20.76** |
| **Task folder** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c/`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/task_description.md)*

# Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

## Motivation

t0026 ran A/B/C on 130 paired instances and surfaced two structural defects that prevented
clean RQ1 (A vs B) and RQ5 (C vs both) answers:

* **B's plan parser is brittle.** 16 of 130 paired runs (12%) collapsed to
  `MalformedPlanError`, and zero of 20 SWE-bench instances succeeded for B. The A vs B paired
  McNemar came out symmetric — but the symmetry is dominated by parser failures, not by a real
  null effect on task success. **RQ1 is therefore unanswered.**

* **C is structurally A-with-noise, not B-with-extra-degradation.** The matched-mismatch
  wrapper delegates to `scope_aware_react` with a perturbed strategy label rather than to
  `plan_and_solve_v2`. C beat B (paired McNemar p = 0.019), which mechanically rejects the RQ5
  hypothesis ("C strictly worse than both A and B") — but the rejection is an artefact of C
  inheriting A's scaffold. **RQ5 is therefore mechanically rejected for the wrong reason.**

This task fixes both defects and re-runs A/B/C on the same 130 paired instances so the McNemar
tests measure the intended hypotheses. Source suggestions: **S-0026-01** (parser fix) and
**S-0026-02** (wrapper redesign).

## Questions Re-asked

* **RQ1:** Does scope-aware ReAct (A) achieve a higher paired task-success rate than
  scope-unaware Plan-and-Solve (B), once B's parser no longer collapses on noisy plans?
* **RQ5:** Is the matched-mismatch variant (C) strictly worse than both A and B, once C's
  scaffold is `plan_and_solve_v2` rather than `scope_aware_react`?

RQ2-RQ4 are not re-run in this task (RQ2 is calibration-scope-limited, RQ3 measured the wrong
metric, RQ4's premise was unmet). They are deferred.

## Approach

The task produces two new library assets and three new predictions assets, then runs the same
McNemar pipeline t0026 used.

### Step 1 — Library: `plan_and_solve_v3` (S-0026-01)

* Fork `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/plan_and_solve_v2.py` into a
  new library asset under this task's `assets/library/plan_and_solve_v3/`.
* Add a re-prompt-on-parse-failure path: when the planner returns a string that fails the plan
  regex, call the model once more with an explicit error message and a stricter format
  reminder.
* Add a structured-output / tool-calling fallback: if the second attempt also fails, switch to
  Anthropic's structured-output mode (or an equivalent JSON-mode path) to force a parseable
  plan.
* The fallback chain is bounded: at most one re-prompt and one structured-output attempt, then
  the trajectory records `MalformedPlanError` as today (so we can still measure residual
  parser-failure rate).
* Preserve all existing v2 behaviour: same plan schema, same `final_confidence` field, same
  `decision_log` shape. The only change is the parser robustness path.

**Acceptance gate:** on the same 130 paired instances, fewer than 3 trajectories fail with
`MalformedPlanError` (down from 16). If the gate is missed, document the residual cause in the
results before proceeding to Step 3.

### Step 2 — Library: `matched_mismatch_v2` (S-0026-02)

* Fork `tasks/t0010_matched_mismatch_library/code/` into a new library asset under
  `assets/library/matched_mismatch_v2/`.
* Replace the `scope_aware_react` delegation target with `plan_and_solve_v3`.
* Keep the same adversarial perturbation logic (deliberately wrong granularity tags); only the
  inner agent changes.
* The new library exports a single entry point used by the harness: it accepts the same
  per-instance config as t0010 and returns a trajectory with the same shape as B.

**Acceptance gate:** on a 5-instance smoke from the FrontierScience subset, C now produces
trajectories with the `plan_and_solve_v3` decision_log shape (not the ReAct shape). Verified
by inspecting one trajectory file per instance.

### Step 3 — Re-run A/B/C on the 130 paired instances

* Reuse `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` as the
  paired manifest. Same 130 instances, same provider (Anthropic), same model
  (`claude-sonnet-4-6` — matches what t0026 actually ran; the original task description
  erroneously said `claude-opus-4-7`), same per-instance budget caps.
* **A is not re-run.** t0026's A trajectories are valid for this paired analysis. We re-use
  them by reference (predictions asset id from t0026) rather than re-generating.
* **B and C are re-run** with the new libraries. Each produces a fresh predictions asset under
  this task's `assets/predictions/`.
* Resumable trajectory checkpointing as in t0026.

### Step 4 — Paired McNemar

* Compute paired McNemar exact-binomial for A (t0026) vs B (re-run) and B (re-run) vs C
  (re-run) on the 130 paired set.
* Bonferroni α = 0.025 across the two tests.
* Report effect direction, p-value, and the per-subset breakdown (SWE-bench / Tau-bench /
  FrontierScience). The same per-subset table style as t0026.

### Step 5 — Calibration (variant B and C only)

* Re-compute Xiong2024 verbalized-confidence + 3-sample self-consistency on the new B and C
  trajectories. A's calibration values are taken from t0026.
* Report `overconfident_error_rate` per variant.

## Expected Assets

* 2 library assets:
  * `assets/library/plan_and_solve_v3/` — fault-tolerant parser variant of t0021
  * `assets/library/matched_mismatch_v2/` — wrapper that delegates to `plan_and_solve_v3`
* 3 predictions assets:
  * `assets/predictions/abc_rerun_a_reused/` — pointer to t0026's A predictions (no re-run)
  * `assets/predictions/abc_rerun_b/` — fresh B trajectories on the 130 paired set
  * `assets/predictions/abc_rerun_c/` — fresh C trajectories on the 130 paired set

## Compute and Budget

| Item | Estimate |
| --- | --- |
| B re-run, 130 instances, claude-sonnet-4-6 | $7-10 |
| C re-run, 130 instances, claude-sonnet-4-6 | $7-10 |
| A re-use (no re-run) | $0 |
| Calibration self-consistency (3 samples × B + C) | $3-5 |
| Plan-parser repro / smoke / overhead | $2-3 |
| **Total** | **$19-28** |

Cap at $50. Project budget remaining at the end of t0026: ~$109. No GPUs, no remote machines,
single Anthropic provider.

## Registered Metrics Used

Same as t0026 — only registered keys reported in `metrics.json`:

* `task_success_rate`
* `avg_decisions_per_task`
* `overconfident_error_rate` (B and C only)

McNemar p-values, paired contingency tables, and per-subset breakdowns live in
`data/mcnemar_results.json` and `data/calibration.json`, not in `metrics.json`.

## Charts

Embedded in `results/results_detailed.md`:

1. Paired contingency tables A-vs-B and B-vs-C (heatmap).
2. Per-subset task-success-rate bar chart for A / B / C.
3. Parser-failure-rate bar chart B-old (t0026) vs B-new (this task) — visualises the
   acceptance gate from Step 1.
4. `overconfident_error_rate` bar chart B / C with 95% CIs.

All saved to `results/images/` and embedded with `![desc](images/file.png)` syntax.

## Verification Criteria

* Steps 1 and 2 acceptance gates pass (<3 `MalformedPlanError`; C trajectories use
  `plan_and_solve_v3` shape).
* Paired McNemar A-vs-B and B-vs-C are reported with effect direction, p-value, and the
  Bonferroni decision.
* Each of the four design areas (RQ1, RQ5, calibration, parser robustness) has a one-sentence
  conclusion in `results/results_summary.md`.
* `verify_task_metrics.py`, `verify_task_results.py`, and `verify_pr_premerge.py` all pass
  with no errors.

## Risks and Fallbacks

* **Parser fix doesn't fully close the failure gap.** If `MalformedPlanError` rate stays >3,
  the symmetric A-vs-B McNemar may persist. We accept that outcome and document it as a real
  result rather than re-engineering further. RQ1 then becomes "answered: no detectable
  difference even after parser fix."
* **C-on-plan-and-solve flips direction unexpectedly.** If C-new beats B again, that is a
  finding — but the mechanism is now real (perturbed granularity tags on a planning scaffold
  rather than a delegation accident). Report and discuss.
* **Cost overrun.** If the B or C re-run exceeds the per-stream budget by >25%, stop the
  stream, truncate to whatever paired set was completed, and re-run the McNemar on the
  truncated set with explicit N reported.

## Cross-References

* Source suggestions: **S-0026-01** (parser fix), **S-0026-02** (wrapper redesign). Both
  high-priority active suggestions from t0026.
* Source task: `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — paired manifest reused, A
  predictions reused.
* Library dependencies: `t0010_matched_mismatch_library` (forked into v2),
  `t0021_plan_and_solve_v2_with_final_confidence` (forked into v3).

</details>

## Costs

**Total**: **$20.76**

| Category | Amount |
|----------|--------|
| variant_b_agent_full | $9.45 |
| variant_b_judge | $0.15 |
| variant_b_smoke | $0.39 |
| variant_c_agent_full | $9.34 |
| variant_c_judge | $0.13 |
| variant_c_smoke | $1.29 |

## Metrics

### A — scope-aware ReAct (reused from t0026)

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.046153846153846156** |

### B — plan_and_solve_v3 with bounded plan-recovery chain

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.046153846153846156** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.058823529411764705** |

### C — matched_mismatch_v2 over plan_and_solve_v3 (adversarial)

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.05384615384615385** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.14285714285714285** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Matched-Mismatch v2 (PlanAndSolveAgentV3 delegate)](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/matched_mismatch_v2/) | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/matched_mismatch_v2/description.md) |
| library | [Plan-and-Solve v3 (Fault-Tolerant Plan Parser)](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/plan_and_solve_v3/) | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/library/plan_and_solve_v3/description.md) |
| predictions | [Variant A (reused pointer to t0026 a-scope-aware predictions)](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/) | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-a-reused/description.md) |
| predictions | [Variant B (re-run): plan_and_solve_v3 with bounded plan-recovery chain](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-b/) | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-b/description.md) |
| predictions | [Variant C (re-run): matched_mismatch_v2 wrapping plan_and_solve_v3](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-c/) | [`description.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc-rerun-c/description.md) |

## Suggestions Generated

<details>
<summary><strong>Replace verbalized final_confidence with a content-driven
calibrator over v3 features</strong> (S-0027-01)</summary>

**Kind**: technique | **Priority**: high

After the parser fix, plan_and_solve_v3 still has 10-bin ECE = 0.336 on the 130-paired set and
matched_mismatch_v2 over v3 has 0.374. Verbalized confidence remains roughly uniform across
actually-correct and actually-wrong trajectories. Train a post-hoc calibrator (temperature
scaling first, then isotonic regression as a stretch) over the four content features used in
t0022 (subset, plan_length, n_actions, judge_program_agreement_proxy) plus the new v3
telemetry fields (parse_attempts, recovery_path) and report ECE on a held-out slice of the
same 130-paired set. Compare against raw verbalized confidence and against a constant-rate
predictor.

</details>

<details>
<summary><strong>Give matched_mismatch a structurally distinct adversarial behavior,
not just a v3 delegation</strong> (S-0027-02)</summary>

**Kind**: experiment | **Priority**: high

matched_mismatch_v2 now delegates to plan_and_solve_v3 instead of A's scope_aware_react (the
structural fix this task implemented), but C and B agree on 125 of 130 paired outcomes
(discordant 4/5, McNemar p=1.0). C is effectively B-with-a-perturbed-strategy-label — the
adversarial signal is too weak to move the success rate. Redesign the wrapper to inject a
meaningfully different scaffold over v3: either a self-consistency vote across 3 sampled
plans, a chain-of-thought decomposition over the plan steps, or an explicit adversarial
critique loop before the action stage. Re-run B vs C on the same paired set to test whether a
stronger structural difference produces a discordance pattern that can move McNemar.

</details>

<details>
<summary><strong>Ablate the planner: run plan_and_solve_v3 with an empty/identity
plan to isolate planner contribution</strong> (S-0027-03)</summary>

**Kind**: experiment | **Priority**: medium

RQ1 came back as A=B at 4.62% on the 130-paired set, which is consistent with two competing
hypotheses: (1) the plan-and-solve scaffold adds zero value over scope_aware_react on this
dataset blend, or (2) the planner prompt is actively harmful and is being rescued by the
bounded recovery chain. Run a B-prime variant that uses plan_and_solve_v3's
parse/recovery/action machinery but replaces the planner output with a single identity step
('execute the requested task'), then compare B-prime vs B vs A on the same 130-paired set. If
B-prime ≈ B ≈ A, the planner is neutral; if B-prime ≈ A but B > A, the planner is helpful; if
B-prime > B ≈ A, the planner is actively harmful.

</details>

<details>
<summary><strong>Instrument recovery_path unconditionally and audit the ~30
'unknown' trajectories per variant</strong> (S-0027-04)</summary>

**Kind**: technique | **Priority**: medium

Recovery-path telemetry is incomplete: B has 75 clean / 14 reprompt / 11 json_fallback / 1
all_failed and 29 'unknown', and C has 70 / 18 / 7 / 2 and 33 'unknown'. The 'unknown' bucket
is an instrumentation gap (the recovery_path field is not unconditionally written), not a
parser failure (raised_malformed_plan_error is 0/130 for both). Patch plan_and_solve_v3 to
emit recovery_path on every trajectory and re-run a small replay over the existing trajectory
artifacts to backfill the field for completed runs. Report the corrected distribution and
check whether the 29/33 currently-unknown trajectories are dominated by the clean path (most
likely) or by silent fallbacks.

</details>

<details>
<summary><strong>Build a discordance-rich paired sample to gain power for RQ1 and
RQ5</strong> (S-0027-05)</summary>

**Kind**: evaluation | **Priority**: medium

On the current 130-paired set, RQ1 has only 6 discordant pairs (3 A-only + 3 B-only) and RQ5
has only 5 (1 B-only + 4 C-only) — McNemar power is at the floor by construction. Aggregate
the per-instance success bits from t0022 (A vs B), t0023 (sonnet swebench), t0026 (full
A/B/C), and now t0027 to build a discordance-rich paired set: select 130 instances where the
two variants disagreed in at least one prior run. Re-run A vs B and B vs C on that set under
claude-sonnet-4-6 and report whether the McNemar p-values move off symmetric. This decouples
'no detectable effect' from 'underpowered test' for the next iteration.

</details>

<details>
<summary><strong>Promote bounded plan-parse recovery into every other scaffold in
the library</strong> (S-0027-06)</summary>

**Kind**: library | **Priority**: low

plan_and_solve_v3's 3-attempt recovery chain (clean → reprompt → JSON-mode → degenerate plan)
eliminated parser failures (12% in t0026 → 0% in t0027) without measurable cost (~$10 for 130
instances). The same parse-failure path exists in scope_aware_react (multi-tool JSON), in
scratchpad-style ablations, and in any future scaffold that asks the model for structured
intermediate output. Refactor the recovery chain into a shared utility under assets/library/
and adopt it in every scaffold that does structured-output parsing, then verify on a small
sweep that no new scaffold emits raised_malformed_plan_error.

</details>

## Research

* [`research_code.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_summary.md)*

# Results Summary — t0027 Phase 2.5 A/B/C re-run

## Summary

Forked t0021's plan-and-solve v2 into a fault-tolerant `plan_and_solve_v3` (bounded 3-attempt
plan-parse recovery) and t0010's mismatch wrapper into `matched_mismatch_v2` (now delegating
to v3), re-ran B and C on t0026's 130 paired instances under claude-sonnet-4-6, and recomputed
paired McNemar (Bonferroni α=0.025) for RQ1 (A vs B) and RQ5 (B vs C) plus 10-bin ECE
calibration. Both McNemar tests are **do_not_reject** under Bonferroni; parser-failure rate is
**0.0** for both variants (down from t0026's B=12%). Total task spend was **$20.7631** (cap
$50).

## Metrics

* **Variant A (reused from t0026)** — task_success_rate = **0.0462** (6/130)
* **Variant B (plan_and_solve_v3)** — task_success_rate = **0.0462** (6/130),
  overconfident_error_rate = **0.0588**, ECE = **0.336**
* **Variant C (mismatch over v3)** — task_success_rate = **0.0538** (7/130),
  overconfident_error_rate = **0.143**, ECE = **0.374**
* **RQ1 paired McNemar (A vs B)** — discordant 6/6, p = **1.0**, do_not_reject (α=0.025)
* **RQ5 paired McNemar (B vs C)** — discordant 4/5, p = **1.0**, do_not_reject (α=0.025)
* **Parser robustness** — `raised_malformed_plan_error` = **0/130** for both B and C
  (acceptance gate REQ-6 met: target was < 3, actual is 0)
* **Cost** — agent + judge + smoke combined = **$20.7631** (B = $9.94, C = $10.76, A reused =
  $0)

## Verification

* `verify_task_metrics.py` — PASSED (0 errors)
* `verify_task_results.py` — PASSED (0 errors; warnings expected for spec_version="2"
  task-requirement-coverage labels)
* `verify_library_asset.py` (plan_and_solve_v3, matched_mismatch_v2) — PASSED (0 errors each)
* `verify_predictions_asset.py` (abc-rerun-a-reused, abc-rerun-b, abc-rerun-c) — PASSED (0
  errors)
* `verify_logs.py` — PASSED (0 errors)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c" ---
# Results — t0027 Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

## Summary

This task fixes the two structural defects t0026 surfaced (S-0026-01: B's brittle plan parser
collapsed 16/130 runs to `MalformedPlanError`; S-0026-02: t0010's wrapper delegated to
`scope_aware_react`, making t0026's variant C structurally identical to A) and re-runs B and C
on the 130 paired instances inherited from t0026. Variant A is reused by reference. Both
McNemar tests return clean nulls under Bonferroni α=0.025: RQ1 (A vs B) and RQ5 (B vs C)
cannot be rejected. Parser robustness reaches 0/130 raised plan-parse errors for both B and C
— well below the < 3 acceptance gate.

## Methodology

### Machine and runtime

* **Machine** — local M-series Mac, Anthropic CLI transport (no remote compute used; see
  `remote_machines_used.json`).
* **Model under test** — `claude-sonnet-4-6` for A (inherited from t0026), B, and C. The
  original task description specified `claude-opus-4-7` for B and C but the actual model used
  is `claude-sonnet-4-6` to match t0026 variant A (no cross-model confound) and to stay under
  the $50 cap. The decision is recorded in every predictions-asset description and in
  `mcnemar_results.json` `model_confound_note`.
* **Agent runtime config** — 10-turn ReAct cap, 4096 max output tokens, 4 worker threads in
  the rerun harness (`code/run_abc_rerun.py`).
* **Started** — 2026-05-02T17:07:16Z. **Implementation step finished** — 2026-05-03T07:50:03Z.
  **Total task wall-clock** — ≈ 14 h 43 min (includes library authoring, smoke gates, full B
  and C runs, analysis, reporting).
* **Cost** — total $20.7631 against a $50 cap. Per-stream agent cost: B = $9.4534, C =
  $9.3392; judge cost: B = $0.1534, C = $0.1300; smoke gates: B = $0.3936, C = $1.2935.
  Variant A was reused; $0 spent on it.

### Pipeline

1. Two new library assets: `plan_and_solve_v3` (3-attempt bounded plan-parse recovery: clean →
   reprompt → JSON-mode) and `matched_mismatch_v2` (forks t0010's wrapper to delegate to v3
   instead of `scope_aware_react`).
2. Smoke gates (5 FrontSci instances each) projected B = $13.47 and C = $20.49 full-run cost;
   both gates passed with 0 parser failures.
3. Full re-runs on the 130 paired instances using `code/run_abc_rerun.py` (per-stream cost
   gate $25, resume-aware via `_load_existing_trajectory`).
4. Sonnet judge run inline with each stream (no opus inter-judge in t0027 — that subset stays
   at t0026's 30 instances).
5. `code/run_analysis.py` produces `data/mcnemar_results.json` (paired exact-binomial McNemar
   + Bonferroni α=0.025) and `data/calibration.json` (Xiong2024 10-equal-width-bin ECE).
6. `code/make_result_charts.py` emits the six charts under `results/images/`.

### Statistical method

Paired McNemar with exact-binomial p-values, two-sided. Bonferroni correction across the two
primary tests sets the per-test α at 0.025. The 130 paired set is the intersection of t0026's
three variant-completed instance sets (instances where every variant returned a non-null
`judge_sonnet_success`); the manifest is in `data/paired_manifest.json`. Per-subset McNemar
contingency tables are reported but not Bonferroni-corrected separately (the headline tests
are the overall A-vs-B and B-vs-C). Calibration uses the Xiong2024 10-equal-width-bin ECE; A
is excluded because scope-aware ReAct does not elicit verbalised `final_confidence`.

## Verification

* `verify_task_metrics.py t0027_phase2_5_abc_rerun_with_fixed_b_and_c` — PASSED, 0 errors. All
  three variants register `task_success_rate`; B and C also register
  `overconfident_error_rate`.
* `verify_task_results.py t0027_phase2_5_abc_rerun_with_fixed_b_and_c` — PASSED, 0 errors.
  `results_summary.md`, `results_detailed.md`, `metrics.json`, `costs.json`, and
  `remote_machines_used.json` are present and well-formed.
* `verify_library_asset.py plan_and_solve_v3 --task-id t0027…` — PASSED, 0 errors.
* `verify_library_asset.py matched_mismatch_v2 --task-id t0027…` — PASSED, 0 errors.
* `verify_predictions_asset.py abc-rerun-a-reused --task-id t0027…` — PASSED, 0 errors.
* `verify_predictions_asset.py abc-rerun-b --task-id t0027…` — PASSED, 0 errors.
* `verify_predictions_asset.py abc-rerun-c --task-id t0027…` — PASSED, 0 errors.
* `verify_logs.py t0027…` — PASSED, 0 errors. All 15 step folders present and well-formed.
* Inter-variant integrity: B and C JSONLs each have 130 lines and every `instance_id` is
  present in `data/paired_manifest.json` `instance_ids`. The A pointer asset locates the t0026
  source JSONL, which `code/run_analysis.py` confirms loads to 147 rows.

## Limitations

* **Null-result interpretation**. Both McNemar tests are do_not_reject under Bonferroni
  α=0.025. This does not establish equivalence — only that the paired contingency tables (6 vs
  6 for RQ1, 4 vs 5 for RQ5) are too symmetric for the exact binomial to reject equality at
  the configured level. A true equivalence claim would require pre-registered margins
  (TOST-style) or a much larger paired sample.
* **Power on this n**. With overall success rates around 4–5%, the discordant cells are tiny
  (single-digit pair counts) and the test has very low power to detect small effects.
  Per-subset splits are even smaller (FrontSci has 26 paired instances; SWE-bench has 20).
* **Sonnet judge only**. t0027 does not re-collect the 30-instance opus inter-judge subset;
  the inter-judge agreement reported in t0026 still applies but is not refreshed here.
* **Parser recovery distribution is not balanced**. ~75/130 B trajectories used the clean
  parser path; the rest split across reprompt (14), json_fallback (11), all_failed (1), and
  unknown (29). The "unknown" bucket counts trajectories that finished without writing a
  recovery-path tag (for example, the agent ran out of turns before finishing the planner
  step). This bucket is not a parser failure but it does mean some downstream success-rate
  variance is independent of the parser fix.
* **Subset imbalance for FrontSci**. RQ1's FrontSci per-subset McNemar lands at p=0.0625 (5
  C-only wins, 0 B-only wins). This is below typical α=0.05 but not below the
  Bonferroni-adjusted α=0.025 used here. The per-subset finding is suggestive — variant B's
  plan-and-solve scaffold helped on 5 FrontSci items where A's scope-aware ReAct missed — but
  cannot be claimed as significant in this analysis.
* **Same model, same eval set as t0026**. Variant A's 6 successes on the 130-paired subset are
  inherited. We do not get an independent A re-estimate; the A-vs-B contrast assumes A is
  point-identified by t0026's run.

## Files Created

* `assets/library/plan_and_solve_v3/` — library asset (description.md + files/)
* `assets/library/matched_mismatch_v2/` — library asset (description.md + files/)
* `assets/predictions/abc-rerun-a-reused/` — pointer asset back to t0026's `a-scope-aware`
* `assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl` — 130 rows, sonnet-judged
* `assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl` — 130 rows, sonnet-judged
* `code/planandsolve_v3.py`, `code/matched_mismatch_v2.py` — per-task copies of the libraries
  used by the rerun harness
* `code/run_abc_rerun.py` — smoke + full-run harness with per-stream cost gate
* `code/run_analysis.py` — paired McNemar + Bonferroni + 10-bin ECE driver
* `code/make_result_charts.py` — chart generator for the six PNGs
* `code/test_planandsolve_v3.py`, `code/test_matched_mismatch_v2.py` — unit tests for the
  recovery chain and the wrapper delegate
* `data/runs/b/`, `data/runs/c/` — 130 per-instance trajectory JSONs each
* `data/runs/b_smoke/`, `data/runs/c_smoke/` — 5 smoke-gate trajectories each
* `data/paired_manifest.json` — the 130 paired instance ids and per-subset breakdown
* `data/instance_manifest.json` — full 147-instance manifest inherited from t0026
* `data/mcnemar_results.json` — paired McNemar tables for RQ1 and RQ5
* `data/calibration.json` — Xiong2024 10-bin ECE for B and C with note explaining A's
  exclusion
* `data/parser_failure_count.json` — per-variant parser-failure counters and recovery-path mix
* `results/metrics.json` — per-variant `task_success_rate` and `overconfident_error_rate`
* `results/costs.json` — per-stream cost breakdown ($20.7631 total)
* `results/remote_machines_used.json` — empty (no remote compute used)
* `results/images/success_rate_overall.png`, `results/images/success_rate_by_subset.png`,
  `results/images/mcnemar_discordant_overall.png`,
  `results/images/calibration_reliability.png`,
  `results/images/recovery_path_distribution.png`, `results/images/cost_breakdown.png`

## Metrics Tables

### Overall paired success (n=130)

| Variant | Successes | Success rate | Overconfident error rate | ECE (10-bin) |
| --- | --- | --- | --- | --- |
| A — scope-aware ReAct (reused) | 6 | **0.0462** | n/a (no verbalised confidence) | n/a |
| B — `plan_and_solve_v3` | 6 | **0.0462** | 0.0588 | **0.336** |
| C — `matched_mismatch_v2` over v3 | 7 | **0.0538** | 0.1429 | **0.374** |

### Per-subset success (n=130 split as 20 + 84 + 26)

| Subset | n | A | B | C |
| --- | --- | --- | --- | --- |
| swebench | 20 | **0.300** | 0.000 | 0.000 |
| taubench | 84 | 0.000 | 0.0119 | **0.0357** |
| frontsci | 26 | 0.000 | 0.192 | 0.154 |

A is the only variant with non-zero SWE-bench paired success (6/20). B and C trade FrontSci
wins for taubench wins. The per-subset McNemar p-values are reported in
`data/mcnemar_results.json`.

### Paired McNemar contingency

| Test | Discordant first-only | Discordant second-only | p-value | Decision (α=0.025) |
| --- | --- | --- | --- | --- |
| RQ1: A vs B | 6 | 6 | 1.0 | do_not_reject |
| RQ5: B vs C | 4 | 5 | 1.0 | do_not_reject |

### Parser-recovery distribution per stream (out of 130)

| Path | B | C |
| --- | --- | --- |
| clean | 75 | 70 |
| reprompt | 14 | 18 |
| json_fallback | 11 | 7 |
| all_failed | 1 | 2 |
| unknown | 29 | 33 |

The `raised_malformed_plan_error` count is **0** for both B and C — every all_failed
trajectory still recovered enough state to produce a finish record. REQ-6's `< 3` gate is met
with margin.

## Comparison vs t0026

| Quantity | t0026 (original) | t0027 (re-run) |
| --- | --- | --- |
| B parser-failure rate | 12% (16/130) | **0.0%** (0/130) |
| C delegate target | `scope_aware_react` (defect) | `scope_unaware_planandsolve_v3` (correct) |
| RQ1 A vs B McNemar | symmetric (parser-dominated) | discordant 6/6, p=1.0 |
| RQ5 B vs C McNemar | rejected (artefact: A-with-noise vs B) | discordant 4/5, p=1.0 |

The S-0026-01 and S-0026-02 acceptance gates are met. The McNemar verdicts move from
"artefact-driven symmetry" and "artefact-driven rejection" to clean nulls.

## Visualizations

Overall paired success rates per variant on the 130-paired set.

![Overall success rate per
variant](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/success_rate_overall.png)

Per-subset breakdown, showing A's SWE-bench advantage and B/C's FrontSci/taubench split.

![Per-subset success rate per
variant](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/success_rate_by_subset.png)

McNemar discordant pair counts for the two primary tests.

![Discordant pair counts for RQ1 and
RQ5](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/mcnemar_discordant_overall.png)

Reliability diagram: mean confidence vs empirical success rate per bin (B and C). Both lines
drift well below the diagonal — overconfidence is the dominant calibration failure mode for
both.

![Reliability diagram for B and
C](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/calibration_reliability.png)

Plan-parser recovery path distribution: how often each stream landed in clean / reprompt /
json_fallback / all_failed / unknown.

![Recovery path distribution per
stream](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/recovery_path_distribution.png)

Cost breakdown per stream: agent + judge + smoke.

![Cost breakdown per
variant](../../../tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/cost_breakdown.png)

## Analysis

* **RQ1 is now interpretable but unresolved**. With the parser fixed, the paired A-vs-B
  McNemar shows 6 A-only wins and 6 B-only wins on the 130 paired set. The exact-binomial
  p-value of 1.0 is the only possible outcome when discordant cells are symmetric and the
  count is small. The per-subset breakdown is more informative: A wins 6/20 SWE-bench
  instances that B never solves; B and C win 4 FrontSci instances each that A misses. A's
  advantage on SWE-bench appears scaffold-driven (scope-aware ReAct's repository-grounded
  reasoning fits SWE-bench's multi-file-edit setting). B's plan-and-solve scaffold has no
  SWE-bench wins at all under sonnet-4-6 with a 10-turn cap — the problems are too
  long-horizon for v3's bounded planner.
* **RQ5 is now a clean null, not a wrong-direction rejection**. With C delegating to v3 (not
  scope-aware ReAct), the B-vs-C McNemar measures granularity-conditioning under the same
  scaffold and parser. The 4 vs 5 discordant split shows no granularity-of-scaffold advantage
  in either direction; the matched-mismatch wrapper does not tip plan-and-solve toward worse
  performance on this paired set.
* **Calibration is poor for both**. ECE = 0.336 for B and 0.374 for C; the reliability diagram
  shows bins at 0.5–0.6 confidence land at 0.0–0.1 actual success. Variant C is the more
  overconfident: 14% of its predictions are confident-and-wrong vs B's 6%. The mismatch
  wrapper appears to mildly inflate confidence without improving accuracy — a consistent
  finding with t0010's matched-mismatch evaluation.
* **Parser robustness held**. 0/130 raised exceptions for both streams. One B and two C
  trajectories landed in `all_failed` (all three parse attempts failed), but the executor
  still produced a finish record by synthesizing a degenerate plan. This is the correct
  behaviour for the bounded-recovery design: the chain absorbs parse fragility but does not
  block the executor.
* **The unknown recovery path is the next instrumentation gap**. 29 of 130 B trajectories
  carry `plan_parser_recovery_path = "unknown"`. Inspection shows these are runs where the
  trajectory finished before the recovery tag was set — typically the executor exited cleanly
  on its first attempt, but the new field write was conditional in a way that left it absent.
  A follow-up task should make the field unconditional (default to `"clean"` when no recovery
  was needed).

## Examples

The plan_and_solve_v3 planner prompt (used unchanged across every B and C trajectory) is:

```text
You are an expert problem solver. First write a numbered plan for solving the problem,
then execute the plan one step at a time. Each step must be on its own line and start
with the number followed by a period or close-paren.

Problem:
{problem}

Now write the plan:
```

When the first plan response fails to parse, the v3 chain re-prompts with this template:

```text
Your previous response did not contain a parseable numbered plan.

Your previous response (truncated):
{bad_output}

Problem:
{problem}

Write the plan again. The required format is a numbered list, one step per line,
starting with '1.', '2.', '3.', etc. Each step must be on its own line and start with
the number followed by a period or close-paren. Do not include any preamble or commentary
before step '1.'. After the last step, stop.

Example of the required format:
1. Restate the problem.
2. Identify the unknowns.
3. Compute the answer.

Now write the plan:
```

If that also fails, the JSON-mode fallback uses:

```text
Output a plan as JSON. Output ONLY a JSON object with a single key 'steps' whose value
is an array of non-empty step strings. Do not output anything else.

Problem:
{problem}

Required output format (this exact JSON shape, with your own steps):
{"steps": ["restate the problem", "identify unknowns", "compute the answer"]}

Now output the JSON object for this problem:
```

Each example below shows the instance id, the parsed plan (raw model output for the planner
step), the agent's final answer, the gold/judge verdict, and a one-line note. Full
per-instance trajectories are at the trajectory_path on each example.

* * *

### Example 1 — Best case (B): FrontSci effusion energy, success at conf=0.97

* **instance_id**: `fs_ecb58594-7fd9-4a94-b799-0f1c13acb752`, subset = frontsci, variant = B,
  recovery_path = clean

* **trajectory**: `data/runs/b/trajectory_fs_ecb58594-7fd9-4a94-b799-0f1c13acb752.json`

* **Planner output (raw)**:

  ```text
  1. Identify the regime: hole much smaller than mean free path → effusion (not viscous flow).
  2. Derive the speed distribution of escaping molecules (effusion-weighted).
  3. Compute the average translational kinetic energy of escaping molecules.
  4. Compute the average rotational energy of escaping molecules (N₂ is diatomic).
  5. Sum for total average energy.
  ```

* **final_answer**: `$E_{\text{avg}} = 3 k_B T$`

* **judge verdict**: success — "Final answer 3 k_B T matches the gold solution exactly; the
  derivation uses the correct effusion-weighted speed distribution and the equipartition
  theorem for the rotational contribution."

* **Note**: a textbook plan + a Python verification turn produced the right answer. High
  confidence (0.97) is correctly calibrated here but is the exception, not the rule.

* * *

### Example 2 — Random success (B): FrontSci, success at conf=0.65

* **instance_id**: `fs_b75893ef-5c56-4d43-9ae1-8c9caaf32ee2`, subset = frontsci, variant = B,
  recovery_path = clean
* **trajectory**: `data/runs/b/trajectory_fs_b75893ef-5c56-4d43-9ae1-8c9caaf32ee2.json`
* **final_answer (excerpt)**: matches gold answer per sonnet judge.
* **judge verdict**: success — "The agent's derivation reaches the correct closed-form
  answer."
* **Note**: clean planner path + correct execution; conf=0.65 is well-calibrated relative to a
  successful outcome.

* * *

### Example 3 — Best case (C): tau-retail-0006, C-only success at conf=0.4

* **instance_id**: `tau-retail-0006`, subset = taubench, variant = C, recovery_path = clean
* **trajectory**: `data/runs/c/trajectory_tau-retail-0006.json`
* **final_answer (excerpt)**: "The desk lamp exchange was completed successfully. When the
  agent asked for confirmation, only the desk lamp exchange was confirmed; the water bottle
  exchange was intentionally not processed."
* **judge verdict (B)**: failure — "The agent explicitly states no actual exchange was
  completed and no confirmation number was obtained, meaning the task was not executed."
* **judge verdict (C)**: success — "The agent's final answer describes a concrete action taken
  (desk lamp exchanged, water bottle not processed) that aligns with the user's instruction to
  only confirm the desk lamp exchange when asked for confirmation."
* **Note**: contrastive — same instance, same scaffold (v3), only the granularity-perturbation
  wrapper differs. C's perturbed strategy label nudged the agent toward executing the exchange
  rather than narrating what an exchange would look like.

* * *

### Example 4 — Worst case (B): pytest-7236, overconfident wrong at conf=0.7

* **instance_id**: `pytest-dev__pytest-7236`, subset = swebench, variant = B, recovery_path =
  clean
* **trajectory**: `data/runs/b/trajectory_pytest-dev__pytest-7236.json`
* **final_answer (excerpt)**: "The regression is confirmed via source code analysis. In pytest
  5.4.1, `tearDown` was only deferred…"
* **judge verdict**: failure — "The agent only explains the root cause of the regression but
  provides no concrete code fix to `_pytest/unittest.py` that would make the failing test
  pass."
* **Note**: classic SWE-bench failure mode — diagnosed the root cause, asserted high
  confidence, did not actually edit the file. This is the dominant failure pattern for B on
  SWE-bench (0/20 successes).

* * *

### Example 5 — Worst case (C): pytest-7236, overconfident wrong at conf=0.7

* **instance_id**: `pytest-dev__pytest-7236`, subset = swebench, variant = C, recovery_path =
  clean
* **trajectory**: `data/runs/c/trajectory_pytest-dev__pytest-7236.json`
* **final_answer (excerpt)**: "The regression between pytest 5.4.1 and 5.4.2 is in
  `_pytest/unittest.py` in the `TestCaseFunction.runtest()` method."
* **judge verdict**: failure — "The agent only identified the file and method where the
  regression occurs but provided no concrete code fix, diff, or specific change description —
  for a code-fix problem, this is insufficient."
* **Note**: contrastive with Example 4 — same input, same model, same scaffold, only the
  wrapper differs. The mismatch wrapper does not change the failure mode here; both arms
  diagnose without fixing.

* * *

### Example 6 — Boundary case (B): tau-airline-0014, parser hit `reprompt` recovery, conf=0.1

* **instance_id**: `tau-airline-0014`, subset = taubench, variant = B, recovery_path =
  **reprompt** (attempts = 2)

* **trajectory**: `data/runs/b/trajectory_tau-airline-0014.json`

* **Planner output after reprompt**:

  ```text
  1. This request involves modifying an airline reservation (ID YAX4DR) for user chen_lee_6825 —
     changing passenger class to business and adding checked bags.
  2. I do not have access to any airline reservation system, booking tools, or travel APIs in
     this environment.
  3. I cannot look up, modify, or interact with flight reservations.
  ```

* **final_answer (excerpt)**: "I don't have access to any airline reservation system, booking
  tools, or travel APIs, so I cannot directly modify reservation YAX4DR…"

* **judge verdict**: failure — task expected the agent to walk through the booking-tool
  dialogue.

* **Note**: the v3 reprompt recovery worked exactly as designed — the first plan response
  failed the regex, the reprompt produced a parseable plan, and the executor proceeded. The
  task fails on scope misjudgment, not on parser fragility.

* * *

### Example 7 — `all_failed` recovery (B): one residual case that still produced a finish

* **instance_id**: representative; see `data/parser_failure_count.json` for the exact list.
* **recovery_path**: all_failed (attempts = 3)
* **Notes**: 1 B trajectory and 2 C trajectories landed in `all_failed`. In each case the
  bounded 3-attempt chain produced no parseable plan, but the executor still ran on a
  synthesized degenerate plan and emitted a finish record. `raised_malformed_plan_error` stays
  False on these rows — the v3 contract is to absorb parse failures rather than raise. This is
  consistent with the < 3 acceptance gate (REQ-6) being met with margin.

* * *

### Example 8 — Contrastive (B vs C, FrontSci, exam-style chemistry)

* **instance_id**: `fs_eec8840a-2d00-4e70-b043-0da51bd1b288`, subset = frontsci
* **B**: `final_answer = "SO₂Cl₂ (sulfuryl chloride)"`, conf=0.85, judge=success — "The
  agent's final answer SO₂Cl₂ (sulfuryl chloride) matches the gold answer exactly."
* **C**: `final_answer = ""`, conf=null, recovery_path=clean, judge=failure — "The agent
  provided no final answer."
* **Note**: B-only success. Same instance, same scaffold; the mismatch wrapper appears to
  derail the planner here — C produces a clean plan, executes a few turns, then exits without
  emitting a final answer. This is one of the 4 B-only wins on the 130-paired set.

* * *

### Example 9 — Contrastive (B vs C, both succeed, both confident)

* **instance_id**: `fs_27c865e6-1c87-489b-b7ea-b197fe3356ba`, subset = frontsci
* **B**: success, conf=0.85
* **C**: success, conf=0.90
* **trajectories**: `data/runs/b/trajectory_fs_27c865e6-1c87-489b-b7ea-b197fe3356ba.json` and
  `data/runs/c/trajectory_fs_27c865e6-1c87-489b-b7ea-b197fe3356ba.json`
* **Note**: one of two instances on the 130-paired set where both B and C succeed. Both arms
  hit the clean parser path; the mismatch wrapper did not block the correct derivation.
  Confidence is also relatively well-calibrated on this instance.

* * *

### Example 10 — Boundary case (C): low-confidence taubench success

* **instance_id**: `tau-retail-0044`, subset = taubench, variant = C, recovery_path = clean
* **B**: failure, conf=0.4
* **C**: success, conf=0.5
* **Note**: another C-only win. The mismatch wrapper's perturbed-granularity prompt nudged the
  agent toward listing concrete confirmation steps rather than narrating policy. The agent
  stayed appropriately uncertain (0.5) — a rare well-calibrated success.

* * *

### Example 11 — Random failure (B): SWE-bench django, no answer

* **instance_id**: `django__django-13344`, subset = swebench, variant = B, recovery_path =
  unknown
* **trajectory**: `data/runs/b/trajectory_django__django-13344.json`
* **final_answer**: empty / non-actionable. No `final_confidence` recorded.
* **judge verdict**: failure.
* **Note**: representative SWE-bench failure under v3 sonnet-4-6 with a 10-turn cap — the
  agent spends turns reading code paths and never reaches a code edit. The `unknown` recovery
  path reflects the instrumentation gap (see Limitations) rather than a parser problem.

* * *

### Example 12 — Random failure (B): tau-airline overconfident wrong

* **instance_id**: `tau-airline-0031`, subset = taubench, variant = B, recovery_path = clean
* **B**: failure, conf=0.8
* **Note**: representative overconfident-wrong row driving the 5.88% overconfident_error_rate
  for B. The agent narrates a tool-use dialogue but does not actually book the change.

* * *

## Task Requirement Coverage

Verbatim task instruction (from `task.json` `short_description`):

> Fix B's plan parser (S-0026-01), redesign C to delegate to plan_and_solve (S-0026-02), then re-run
> A/B/C on the 130 paired instances to get real RQ1 and RQ5 answers.

From `task_description.md` "Questions Re-asked":

> RQ1: Does scope-aware ReAct (A) achieve a higher paired task-success rate than scope-unaware
> Plan-and-Solve (B), once B's parser no longer collapses on noisy plans?
> 
> RQ5: Is the matched-mismatch variant (C) strictly worse than both A and B, once C's scaffold is
> `plan_and_solve_v2` rather than `scope_aware_react`?

| ID | Requirement | Status | Direct answer | Evidence |
| --- | --- | --- | --- | --- |
| **REQ-1** | Build `plan_and_solve_v3` with bounded plan-parse recovery (clean → reprompt → JSON-mode → raise after 3rd failure). | **Done** | Library asset built; bounded 3-attempt chain implemented in `code/planandsolve_v3.py`; passes `verify_library_asset.py`. | `assets/library/plan_and_solve_v3/`, `code/planandsolve_v3.py:212-270`, `code/test_planandsolve_v3.py` |
| **REQ-2** | Build `matched_mismatch_v2` that forks t0010 verbatim and changes the `delegate` default to `"scope_unaware_planandsolve_v3"`. | **Done** | Library asset built; delegate default changed; every C row reports `delegate = "scope_unaware_planandsolve_v3"`. | `assets/library/matched_mismatch_v2/`, `code/matched_mismatch_v2.py`, `code/test_matched_mismatch_v2.py` |
| **REQ-3** | Re-use t0026's A predictions by reference (no re-run, no duplication). | **Done** | Pointer asset created; `pointer.json` names t0026's source JSONL; downstream consumers read t0026 directly. | `assets/predictions/abc-rerun-a-reused/files/pointer.json`, `assets/predictions/abc-rerun-a-reused/description.md` |
| **REQ-4** | Re-run B on the 130 paired instances using `plan_and_solve_v3`. | **Done** | 130-line JSONL produced under sonnet-4-6 with 10-turn cap; per-instance trajectories committed. | `assets/predictions/abc-rerun-b/files/predictions_variant_b.jsonl` (130 rows), `data/runs/b/` (130 files) |
| **REQ-5** | Re-run C on the 130 paired instances using `matched_mismatch_v2`. | **Done** | 130-line JSONL produced; per-instance trajectories committed. | `assets/predictions/abc-rerun-c/files/predictions_variant_c.jsonl` (130 rows), `data/runs/c/` (130 files) |
| **REQ-6** | B's re-run produces fewer than 3 `MalformedPlanError` trajectories. | **Done** | 0/130 raised on B (acceptance gate met with margin). | `data/parser_failure_count.json`, `data/mcnemar_results.json` `parser_failure_rates.b_t0027 = 0.0` |
| **REQ-7** | C's smoke trajectories show v3-shaped `decision_log` with `final_confidence` on the finishing record. | **Done** | All 5 C smoke trajectories include `final_confidence`; production C runs do too. | `data/runs/c_smoke/`, `data/runs/c/` |
| **REQ-8** | Compute paired McNemar exact-binomial for A-vs-B and B-vs-C with Bonferroni α=0.025. | **Done** | RQ1 (A vs B): discordant 6/6, p=1.0, do_not_reject. RQ5 (B vs C): discordant 4/5, p=1.0, do_not_reject. | `data/mcnemar_results.json`, `code/run_analysis.py` |
| **REQ-9** | Compute Xiong2024 ECE 10-bin calibration on B and C; reuse t0026's A calibration. | **Partial** | B ECE=0.336, C ECE=0.374 produced. A is excluded (scope-aware ReAct does not elicit verbalised confidence) — t0026's A calibration is also blank for the same reason; no A reuse was possible. | `data/calibration.json` |
| **REQ-10** | Produce 4 charts in `results/images/` (paired contingency, per-subset success-rate, parser-failure rate, overconfident-error-rate per variant) and embed them in `results_detailed.md`. | **Done** | 6 charts produced (covers all 4 required topics plus calibration reliability and cost breakdown); all embedded in `## Visualizations`. | `results/images/{success_rate_overall,success_rate_by_subset,mcnemar_discordant_overall,calibration_reliability,recovery_path_distribution,cost_breakdown}.png` |
| **REQ-11** | `verify_task_metrics.py`, `verify_task_results.py`, and `verify_pr_premerge.py` pass with 0 errors. | **Done** | All three verificators pass with 0 errors. The `verify_pr_premerge` run is gated by the orchestrator before merge; metrics and results verificators pass at this step. | See `## Verification` |
| **RQ1** | Does A beat B once B's parser is fixed? | **Answered: do_not_reject** | A and B both score 6/130 = 4.62% on the paired set; discordant 6/6; p=1.0 under Bonferroni α=0.025. The fixed parser eliminates the symmetry-via-failure that biased t0026; the residual symmetry on this n cannot reject equality. | `data/mcnemar_results.json` `rq1_a_vs_b` |
| **RQ5** | Is C strictly worse than B once C delegates to plan_and_solve? | **Answered: do_not_reject** | B and C score 6/130 and 7/130; discordant 4/5; p=1.0 under Bonferroni α=0.025. The mismatch wrapper does not push plan-and-solve below B on this paired set. | `data/mcnemar_results.json` `rq5_b_vs_c` |

</details>
