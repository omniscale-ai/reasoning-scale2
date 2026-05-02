---
spec_version: "1"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
research_stage: "code"
tasks_reviewed: 4
tasks_cited: 4
libraries_found: 7
libraries_relevant: 3
date_completed: "2026-05-02"
status: "complete"
---
# research_code.md — t0027 prior-task code review

## Task Objective

t0027 fixes two structural defects from t0026's A/B/C run on the 130-paired manifest: (1) B's
`MalformedPlanError` collapse on 16/130 instances, and (2) C delegating to `scope_aware_react`
instead of `scope_unaware_planandsolve`, which made it structurally A-with-noise rather than
B-with-extra-degradation. The deliverables are two new libraries (`plan_and_solve_v3` with re-prompt
and JSON-tool-call fallback, and `matched_mismatch_v2` re-targeted to v3) plus a re-run of B and C
on the same 130 paired ids, reusing A trajectories from t0026 verbatim and re-running McNemar
(Bonferroni α = 0.025) and ECE calibration on the new B and C predictions.

## Library Landscape

The library aggregator returned 7 libraries; 3 are directly relevant to t0027:

* `scope_unaware_planandsolve_v1` [t0007] — base v1 implementation containing `MalformedPlanError`
  and the un-retried plan-parse path. Imported as the inheritance target for v3.
* `scope_unaware_planandsolve_v2` [t0021] — v2 wrapper that adds `final_confidence` elicitation on
  top of v1. v3 must preserve v2's confidence layer unchanged. Imported.
* `matched_mismatch_v1` [t0010] — condition-C wrapper that walks phases and dispatches to one of two
  delegate strings (`scope_aware_react` or `scope_unaware_planandsolve`). Forked into
  `matched_mismatch_v2` with the delegate default flipped.

Non-relevant libraries: `scope_aware_react_v1` (from t0006) is A's agent and is not modified.
`metric2_calibration_aggregator_v1` (t0011), `phase2_smoke_harness_v1` (t0012), and
`abc_harness_metrics` (t0022) are not consumed; t0027 reuses the t0026 in-task copies of the
McNemar, ECE, and metrics modules instead. None of the three relevant libraries show a correction
overlay in the aggregator output, so the v1/v2 sources are authoritative.

## Key Findings

### Plan-parser failure mode lives in v1, not v2

`MalformedPlanError` is defined and raised inside [t0007]'s `planandsolve.py` (class definition at
`planandsolve.py:90`; raise site at `planandsolve.py:189-192` inside `parse_plan`). The agent runner
at `planandsolve.py:280-282` calls `parse_plan(plan_text)` immediately after the model returns —
there is no retry, no JSON fallback, and no schema enforcement. [t0021]'s v2 wrapper adds
`final_confidence` elicitation but does **not** parse plans, so v3 must override the v1 plan-parsing
step rather than touching v2's confidence layer. This is the single most important implementation
finding: the natural fork point is a new `_robust_parse_plan` helper that wraps `parse_plan`, not a
change inside `planandsolve_v2.py`.

### C's t0026 delegate was structurally wrong

[t0010]'s `MatchedMismatchAgent` accepts a `delegate` string literal and dispatches to one of two
parsers (`_parse_react_output` at `matched_mismatch.py:42` or `_parse_planandsolve_output` at
`matched_mismatch.py:50`). The adversarial mapping
`ADVERSARIAL_MAP = {"global": "atomic", "atomic": "global", "subtask": "atomic"}` at
`matched_mismatch.py:66-70` is delegate-agnostic — only the inner agent has to change. [t0026]'s
runner passed `"scope_aware_react"` as the delegate, so C inherited A's behavior plus tag
perturbation rather than B's behavior plus tag perturbation. The fix is a one-line default-flip in
`matched_mismatch_v2`.

### t0026 trajectory and harness shapes are reusable

[t0026]'s `runner.py:166-214` defines three helpers `_run_variant_a/b/c` and persists outcomes via
`_persist_outcome()` to `trajectory_<instance_id>.json` files using the `_InstanceOutcome` dataclass
at `runner.py:98-104`
(`instance_id, subset, variant, final_answer, final_confidence, cost_usd, trajectory`). The McNemar
pipeline at `mcnemar.py:75-94` and the `compute_ece_10bin` aggregator at `calibration.py:28-78`
consume this shape directly, so v3 must emit the same dataclass field set. The 130-paired set is
derived inside `metrics.py:130-147` by intersecting completed instance ids across variants — t0027
reuses this intersection logic verbatim.

### A trajectories can be reused without re-running

Because A is unaffected by either defect, t0027 does not re-run A. Instead, the t0026 A trajectories
are copied (or symlinked) into `assets/predictions/abc_rerun_a_reused/` and the calibration values
are taken from `t0026/data/calibration.json`. This saves roughly $9-10 of inference cost and removes
a major source of run-to-run variance from the A-vs-B McNemar test.

## Reusable Code and Assets

* **`scope_unaware_planandsolve_v1`** — Source:
  `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`. **Reuse method: import via
  library.** Re-uses `parse_plan`, `_PLAN_LINE_RE`, `MalformedPlanError`, `PLAN_PROMPT_TEMPLATE`,
  the `TrajectoryRecord` dataclass at `planandsolve.py:99-114`, and the executor logic from
  `PlanAndSolveAgent.run` (`planandsolve.py:280-…`). Adaptation: subclass or re-implement only the
  plan-parse step; insert a
  `_robust_parse_plan(model_call, problem, plan_text, *, max_attempts=2, json_fallback=True)`
  helper. ~30 LOC of new code.
* **`scope_unaware_planandsolve_v2`** — Source:
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py`. **Reuse method:
  import via library.** Re-uses `elicit_final_confidence` at `planandsolve_v2.py:182-207`,
  `parse_final_confidence` at `planandsolve_v2.py:152-174`, `CONFIDENCE_PROMPT_TEMPLATE` /
  `CONFIDENCE_RETRY_PROMPT_TEMPLATE` at `planandsolve_v2.py:61-83`, and `TrajectoryRecordV2` at
  `planandsolve_v2.py:111-127`. Adaptation: none — v3 wraps v3-with-robust-plan in the same
  confidence shell. ~5 LOC of new wiring.
* **`matched_mismatch_v1`** — Source:
  `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`. **Reuse method: import via
  library.** Re-uses `MatchedMismatchAgent` dataclass at `matched_mismatch.py:54-66`,
  `pick_mismatch_tag` at `matched_mismatch.py:136-146`, and `ADVERSARIAL_MAP` at
  `matched_mismatch.py:66-70`. Adaptation: change the `_parse_planandsolve_output` import target to
  v3's library and update the default `delegate` string literal to
  `"scope_unaware_planandsolve_v3"`. ~10 LOC of new code.
* **t0026 harness modules** — Source: `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/`
  (`runner.py`, `mcnemar.py`, `calibration.py`, `metrics.py`, `instance_loader.py`, `paths.py`,
  `anthropic_shim.py`, `judge.py`). **Reuse method: copy into task** (cross-task code-import rule
  forbids importing another task's `code/`). Re-uses `runner.run_variant`, `_InstanceOutcome`,
  `pairwise_mcnemar(success_first, success_second)` at `mcnemar.py:75-94`,
  `compute_ece_10bin(confidences, outcomes)` at `calibration.py:28-78`, and the 130-paired
  intersection at `metrics.py:130-147`. Adaptation: redirect `_run_variant_b` to v3 and
  `_run_variant_c` to v2. ~50 LOC of glue.
* **t0026 manifest and A trajectories** — Source:
  `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` and
  `assets/predictions/variant_a/`. **Reuse method: copy into task assets.** Manifest is reused
  unchanged; A trajectories are copied into `assets/predictions/abc_rerun_a_reused/` with a pointer
  in `details.json`.

## Lessons Learned

* **Don't catch `MalformedPlanError` silently** — t0026 logged the failures correctly but had no
  retry path, which inflated B's parser-failure rate from a recoverable per-prompt issue (probably
  ~2-3% with one re-prompt) into a 12.3% structural collapse (16/130). v3 must retry but also
  preserve the residual error count so the McNemar test can still attribute B's tail behavior
  honestly.
* **Wrapper-default delegate is a sharp edge** — the `MatchedMismatchAgent` API made it easy to
  silently mis-target the C condition by passing the wrong delegate string. v2 should default to v3
  explicitly and document the choice in the library `description.md`.
* **Reuse paired A trajectories whenever the variant under test is the only one fixed** — running A
  again would have added cost and variance without changing the question being answered. The
  130-paired manifest plus a fixed seed makes A-vs-B-new and B-new-vs-C-new the only paired
  comparisons that need re-running.

## Recommendations for This Task

1. **`plan_and_solve_v3` library** — Fork `planandsolve.py` [t0007] and `planandsolve_v2.py` [t0021]
   into a single module under `assets/library/plan_and_solve_v3/`. Add
   `_robust_parse_plan(model_call, problem, plan_text, *, max_attempts=2, json_fallback=True)` that
   (a) tries `parse_plan(plan_text)`, (b) on `MalformedPlanError`, re-prompts with a stricter format
   reminder and tries `parse_plan` again, (c) on a second failure, falls back to the Anthropic JSON
   tool-call path with a `{steps: list[string]}` schema, (d) on a third failure, re-raises
   `MalformedPlanError` so the residual rate is recorded honestly.
2. **`matched_mismatch_v2` library** — Fork [t0010] verbatim, swap the `_parse_planandsolve_output`
   import target to v3, and change the default `delegate` literal to
   `"scope_unaware_planandsolve_v3"`. No other logic changes.
3. **Re-run harness** — Write `code/run_abc_rerun.py` that loads the t0026 manifest, restricts to
   the 130 paired ids (intersection of t0026's three completed runs), copies t0026's A trajectories
   into the reused predictions asset, then calls `runner.run_variant` for B (v3) and C (v2) with
   checkpointing. Use the same Anthropic shim, judge, and `_persist_outcome` from [t0026].
4. **Analysis** — Re-use [t0026]'s `mcnemar.pairwise_mcnemar`, `calibration.compute_ece_10bin`, and
   `metrics.compute_overconfident_error_rate` against the new B/C trajectories and the reused A
   trajectories. Apply Bonferroni α = 0.025 across {A-vs-B, B-vs-C}. No new analysis code beyond a
   thin glue script.
5. **Acceptance gates** — Verify (a) B's re-run produces fewer than 3 `MalformedPlanError`
   trajectories, and (b) C's smoke trajectories show v3-shaped `decision_log` (i.e., the
   `final_confidence` field is present on the finishing record). Both are checkable from the
   resulting predictions assets without running any new analysis.

## Task Index

### [t0007]

* **Task ID**: t0007_scope_unaware_planandsolve_library
* **Name**: Scope-unaware Plan-and-Solve baseline library
* **Status**: completed
* **Relevance**: Defines `parse_plan` and `MalformedPlanError`. v3's plan-parsing fix overrides this
  module's un-retried parse step.

### [t0010]

* **Task ID**: t0010_matched_mismatch_library
* **Name**: Matched-Mismatch wrapper library
* **Status**: completed
* **Relevance**: Defines the condition-C wrapper. matched_mismatch_v2 forks this with the inner
  agent flipped to v3.

### [t0021]

* **Task ID**: t0021_plan_and_solve_v2_with_final_confidence
* **Name**: Plan-and-Solve v2 with final-confidence elicitation
* **Status**: completed
* **Relevance**: Adds verbalized confidence to v1. v3 inherits this confidence layer unchanged.

### [t0026]

* **Task ID**: t0026_phase2_abc_runtime_n147_for_rq1_rq5
* **Name**: Phase-2 A/B/C runtime on 147 instances
* **Status**: completed
* **Relevance**: Source of the 130-paired manifest, the A trajectories reused by t0027, and the
  McNemar / ECE / metrics modules that t0027 copies into its own `code/`.
