# Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

## Motivation

t0026 ran A/B/C on 130 paired instances and surfaced two structural defects that prevented clean RQ1
(A vs B) and RQ5 (C vs both) answers:

* **B's plan parser is brittle.** 16 of 130 paired runs (12%) collapsed to `MalformedPlanError`, and
  zero of 20 SWE-bench instances succeeded for B. The A vs B paired McNemar came out symmetric — but
  the symmetry is dominated by parser failures, not by a real null effect on task success. **RQ1 is
  therefore unanswered.**

* **C is structurally A-with-noise, not B-with-extra-degradation.** The matched-mismatch wrapper
  delegates to `scope_aware_react` with a perturbed strategy label rather than to
  `plan_and_solve_v2`. C beat B (paired McNemar p = 0.019), which mechanically rejects the RQ5
  hypothesis ("C strictly worse than both A and B") — but the rejection is an artefact of C
  inheriting A's scaffold. **RQ5 is therefore mechanically rejected for the wrong reason.**

This task fixes both defects and re-runs A/B/C on the same 130 paired instances so the McNemar tests
measure the intended hypotheses. Source suggestions: **S-0026-01** (parser fix) and **S-0026-02**
(wrapper redesign).

## Questions Re-asked

* **RQ1:** Does scope-aware ReAct (A) achieve a higher paired task-success rate than scope-unaware
  Plan-and-Solve (B), once B's parser no longer collapses on noisy plans?
* **RQ5:** Is the matched-mismatch variant (C) strictly worse than both A and B, once C's scaffold
  is `plan_and_solve_v2` rather than `scope_aware_react`?

RQ2-RQ4 are not re-run in this task (RQ2 is calibration-scope-limited, RQ3 measured the wrong
metric, RQ4's premise was unmet). They are deferred.

## Approach

The task produces two new library assets and three new predictions assets, then runs the same
McNemar pipeline t0026 used.

### Step 1 — Library: `plan_and_solve_v3` (S-0026-01)

* Fork `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/plan_and_solve_v2.py` into a new
  library asset under this task's `assets/library/plan_and_solve_v3/`.
* Add a re-prompt-on-parse-failure path: when the planner returns a string that fails the plan
  regex, call the model once more with an explicit error message and a stricter format reminder.
* Add a structured-output / tool-calling fallback: if the second attempt also fails, switch to
  Anthropic's structured-output mode (or an equivalent JSON-mode path) to force a parseable plan.
* The fallback chain is bounded: at most one re-prompt and one structured-output attempt, then the
  trajectory records `MalformedPlanError` as today (so we can still measure residual parser-failure
  rate).
* Preserve all existing v2 behaviour: same plan schema, same `final_confidence` field, same
  `decision_log` shape. The only change is the parser robustness path.

**Acceptance gate:** on the same 130 paired instances, fewer than 3 trajectories fail with
`MalformedPlanError` (down from 16). If the gate is missed, document the residual cause in the
results before proceeding to Step 3.

### Step 2 — Library: `matched_mismatch_v2` (S-0026-02)

* Fork `tasks/t0010_matched_mismatch_library/code/` into a new library asset under
  `assets/library/matched_mismatch_v2/`.
* Replace the `scope_aware_react` delegation target with `plan_and_solve_v3`.
* Keep the same adversarial perturbation logic (deliberately wrong granularity tags); only the inner
  agent changes.
* The new library exports a single entry point used by the harness: it accepts the same per-instance
  config as t0010 and returns a trajectory with the same shape as B.

**Acceptance gate:** on a 5-instance smoke from the FrontierScience subset, C now produces
trajectories with the `plan_and_solve_v3` decision_log shape (not the ReAct shape). Verified by
inspecting one trajectory file per instance.

### Step 3 — Re-run A/B/C on the 130 paired instances

* Reuse `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` as the paired
  manifest. Same 130 instances, same provider (Anthropic), same model (`claude-sonnet-4-6` — matches
  what t0026 actually ran; the original task description erroneously said `claude-opus-4-7`), same
  per-instance budget caps.
* **A is not re-run.** t0026's A trajectories are valid for this paired analysis. We re-use them by
  reference (predictions asset id from t0026) rather than re-generating.
* **B and C are re-run** with the new libraries. Each produces a fresh predictions asset under this
  task's `assets/predictions/`.
* Resumable trajectory checkpointing as in t0026.

### Step 4 — Paired McNemar

* Compute paired McNemar exact-binomial for A (t0026) vs B (re-run) and B (re-run) vs C (re-run) on
  the 130 paired set.
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

Cap at $50. Project budget remaining at the end of t0026: ~$109. No GPUs, no remote machines, single
Anthropic provider.

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
3. Parser-failure-rate bar chart B-old (t0026) vs B-new (this task) — visualises the acceptance gate
   from Step 1.
4. `overconfident_error_rate` bar chart B / C with 95% CIs.

All saved to `results/images/` and embedded with `![desc](images/file.png)` syntax.

## Verification Criteria

* Steps 1 and 2 acceptance gates pass (<3 `MalformedPlanError`; C trajectories use
  `plan_and_solve_v3` shape).
* Paired McNemar A-vs-B and B-vs-C are reported with effect direction, p-value, and the Bonferroni
  decision.
* Each of the four design areas (RQ1, RQ5, calibration, parser robustness) has a one-sentence
  conclusion in `results/results_summary.md`.
* `verify_task_metrics.py`, `verify_task_results.py`, and `verify_pr_premerge.py` all pass with no
  errors.

## Risks and Fallbacks

* **Parser fix doesn't fully close the failure gap.** If `MalformedPlanError` rate stays >3, the
  symmetric A-vs-B McNemar may persist. We accept that outcome and document it as a real result
  rather than re-engineering further. RQ1 then becomes "answered: no detectable difference even
  after parser fix."
* **C-on-plan-and-solve flips direction unexpectedly.** If C-new beats B again, that is a finding —
  but the mechanism is now real (perturbed granularity tags on a planning scaffold rather than a
  delegation accident). Report and discuss.
* **Cost overrun.** If the B or C re-run exceeds the per-stream budget by >25%, stop the stream,
  truncate to whatever paired set was completed, and re-run the McNemar on the truncated set with
  explicit N reported.

## Cross-References

* Source suggestions: **S-0026-01** (parser fix), **S-0026-02** (wrapper redesign). Both
  high-priority active suggestions from t0026.
* Source task: `t0026_phase2_abc_runtime_n147_for_rq1_rq5` — paired manifest reused, A predictions
  reused.
* Library dependencies: `t0010_matched_mismatch_library` (forked into v2),
  `t0021_plan_and_solve_v2_with_final_confidence` (forked into v3).
