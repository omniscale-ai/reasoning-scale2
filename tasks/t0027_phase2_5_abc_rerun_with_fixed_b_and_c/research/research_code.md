# research_code.md — t0027 prior-task code review

## Objective

Identify the exact entry points, file/line locations, data shapes, and dispatch sites in t0010
(matched-mismatch wrapper), t0007+t0021 (Plan-and-Solve v1 + v2 confidence layer), and t0026 (A/B/C
harness, McNemar, calibration) so that t0027 can fork them with minimal surface area:

* `plan_and_solve_v3` — t0007 `PlanAndSolveAgent` planning step + t0021 confidence elicitation, with
  a re-prompt-on-parse-failure path and a structured-output (Anthropic JSON tool-call) fallback.
* `matched_mismatch_v2` — t0010 `MatchedMismatchAgent` re-targeted to delegate to
  `plan_and_solve_v3` instead of `scope_aware_react`.
* B/C re-runs reuse the t0026 harness with the same trajectory shape, manifest, and McNemar pipeline
  — no changes to A.

## Background

t0026 finished with two structural defects: 16/130 paired runs collapsed to `MalformedPlanError`
(B), and C delegated to `scope_aware_react` (so it was structurally A-with-noise rather than
B-with-extra-degradation). t0027 fixes both and re-runs B and C on the same 130-paired manifest; A's
t0026 trajectories are reused verbatim.

## Methodology Review

### t0010_matched_mismatch_library

* Library asset path: `tasks/t0010_matched_mismatch_library/assets/library/matched_mismatch_v1/`
  (`description.md`, `details.json`).
* Implementation: `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
* Entry point: `MatchedMismatchAgent` dataclass at `matched_mismatch.py:54-66`, with
  `run(problem, annotation) -> AgentRunResult`.
* Delegate dispatch: t0010 itself walks phases and calls `model_call()` per phase, then parses via
  `_parse_react_output` (`matched_mismatch.py:42`) or `_parse_planandsolve_output`
  (`matched_mismatch.py:50`). The `delegate` parameter is a string literal, `"scope_aware_react"` or
  `"scope_unaware_planandsolve"`. The harness call sites are
  `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/runner.py:200-214`.
* Adversarial mapping:
  `ADVERSARIAL_MAP = {"global": "atomic", "atomic": "global", "subtask": "atomic"}` at
  `matched_mismatch.py:66-70`. `pick_mismatch_tag(correct_tag, strategy, rng)` at
  `matched_mismatch.py:136-146`. Records emit the perturbed tag in `granularity` and the original
  tag in `extras["_correct_granularity"]`.

### t0007 + t0021 (Plan-and-Solve v1 → v2)

* v1 library: `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`. v2 library:
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`,
  with implementation at
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py`.
* Plan parser: `parse_plan(text: str) -> list[str]` at `planandsolve.py:165-193`. It splits on
  `_PLAN_LINE_RE` (`\d+\.|\d+\)` at line start) and raises `MalformedPlanError`
  (`planandsolve.py:90`) when no numbered step is found. The exception path is the bare line
  `raise MalformedPlanError(...)` at `planandsolve.py:189-192`.
* The agent's run loop is `PlanAndSolveAgent.run` at `planandsolve.py:280-…`, which calls
  `plan_text = self.model_call(PLAN_PROMPT_TEMPLATE.format(problem=problem))` and immediately
  `plan = parse_plan(plan_text)` at lines 281-282 — there is no retry.
* `decision_log` shape is preserved by `TrajectoryRecord` (`planandsolve.py:99-114`) and extended by
  `TrajectoryRecordV2` in v2 (`planandsolve_v2.py:111-127`) with a `final_confidence: float | None`
  carried only on the finishing record. v3 must keep the same dataclass field set so the t0026
  trajectory-to-JSON converter (`runner.py:217-224`) keeps working unchanged.
* Confidence elicitation: `elicit_final_confidence(model_call, problem, final_answer)` at
  `planandsolve_v2.py:182-207`, with parser `parse_final_confidence(text)` at lines 152-174 and
  prompt templates `CONFIDENCE_PROMPT_TEMPLATE` / `CONFIDENCE_RETRY_PROMPT_TEMPLATE` at lines 61-83.
  v3 reuses these unchanged.

### t0026_phase2_abc_runtime_n147_for_rq1_rq5

* Code files (`tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/`): `anthropic_shim.py`,
  `calibration.py`, `full_runner.py`, `instance_loader.py`, `judge.py`, `main.py`, `mcnemar.py`,
  `metrics.py`, `paths.py`, `plot_results.py`, `runner.py`, `test_smoke.py`.
* Manifest: `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json`. Top
  level:
  `{seed: int, n_total: 147, per_subset_counts: {swebench: 20, taubench: 87, frontsci: 40}, source_sha256: {...}, instance_ids: [147 strings]}`.
  The 130-paired set is derived inside `metrics.py:130-147` by intersecting completed instance ids
  across variants — t0027 reuses the same intersection logic.
* Variant dispatch: `runner.py:166-214` defines three helpers `_run_variant_a/b/c`. A calls
  `ScopeAwareReactAgent.run()`, B calls `PlanAndSolveAgentV2.run()`, C calls
  `MatchedMismatchAgent.run()`. t0027 only needs to redirect B's helper to `PlanAndSolveAgentV3` and
  C's helper to `MatchedMismatchAgentV2`.
* Trajectory output shape: `_InstanceOutcome` dataclass at `runner.py:98-104` with fields
  `instance_id, subset, variant, final_answer, final_confidence, cost_usd, trajectory`. Persisted
  via `_persist_outcome()` to `variant_dir / f"trajectory_{instance_id}.json"`. t0027 must produce
  the same shape so the t0026 plotting and judging code keeps working.
* McNemar: `pairwise_mcnemar(success_first, success_second)` at `mcnemar.py:75-94` — input is two
  paired bool lists, output is a dict with `discordant_b`, `discordant_c`, `statistic`, `p_value`,
  `method`. Called for A-vs-B (`metrics.py:136`) and B-vs-C (`metrics.py:145`).
* Calibration: `compute_ece_10bin(confidences, outcomes) -> ECEResult` at `calibration.py:28-78`. 10
  equal-width bins, returns `ECEResult(ece, bins, n_total)`. Called at `metrics.py:87`. t0027
  re-uses this aggregator; A's calibration values are taken from `t0026/data/calibration.json`.

## Key Findings

* `MalformedPlanError` lives in **t0007** (v1), not t0021 (v2). v2 does not parse plans — it just
  wraps v1 and adds confidence elicitation. So `plan_and_solve_v3` must replace v1's parsing step,
  not v2's. The cleanest fork is a new module that imports `parse_plan`, the prompt templates, and
  the executor logic from t0007 verbatim, but overrides the plan-parsing step in
  `PlanAndSolveAgent.run` with a `_robust_parse_plan` helper that:
  1. Tries `parse_plan(plan_text)`.
  2. On `MalformedPlanError`, calls the model again with a stricter format reminder
     (`"Re-emit the plan as a numbered list. Each step must start with `1.`, `2.`, etc."`) and tries
     `parse_plan` again.
  3. On a second failure, falls back to the Anthropic JSON tool-calling path (`anthropic_shim.py`)
     with a tool schema like `{steps: list[string]}`.
  4. On a third failure, re-raises `MalformedPlanError` so t0026 still records the residual
     parser-failure rate.
* `MatchedMismatchAgentV2` is a one-line change: copy t0010 verbatim, swap the
  `_parse_planandsolve_output` import target to v3, and update the `delegate` literal default to
  `"scope_unaware_planandsolve_v3"`. Adversarial perturbation logic is unchanged.
* The B/C re-run harness can be a single Python script in `code/` that imports `runner.run_variant`
  from t0026 with two helper overrides for B and C. A is not re-run — its t0026 trajectories are
  symlinked or copied into `assets/predictions/abc_rerun_a_reused/` with a pointer in
  `details.json`.
* The acceptance gates in the task description map cleanly to this implementation: gate 1 is "B's
  re-run produces <3 `MalformedPlanError` trajectories" (verifiable from
  `assets/predictions/abc_rerun_b/`); gate 2 is "C's smoke trajectories show v3-shaped
  `decision_log`" (verifiable from a 5-instance smoke).
* Cost: 130 instances × (B ~$0.10/inst + C ~$0.10/inst + ~$0.03 calibration overhead each) ≈ $30-32,
  well under the $50 cap.

## Recommended Approach

1. **plan_and_solve_v3 library** — fork t0007's `planandsolve.py` and t0021's `planandsolve_v2.py`
   into one module under `tasks/t0027/.../assets/library/plan_and_solve_v3/`. Add
   `_robust_parse_plan(model_call, problem, plan_text, *, max_attempts=2, json_fallback=True)`.
   Tests cover: clean parse, re-prompt success, JSON-fallback success, all-fail.
2. **matched_mismatch_v2 library** — fork t0010, swap the inner agent for v3.
3. **Re-run harness** — write `code/run_abc_rerun.py` that:
   * Loads t0026's manifest, restricts to the 130 paired ids (intersection of t0026's three
     completed runs).
   * Copies t0026's A trajectories into the reused predictions asset.
   * Calls t0026's `runner.run_variant("b", instances, agent_factory=plan_and_solve_v3)` and
     `run_variant("c", instances, agent_factory=matched_mismatch_v2)` with checkpointing.
4. **Analysis** — re-use t0026's `mcnemar.pairwise_mcnemar`, `calibration.compute_ece_10bin`, and
   `metrics.compute_overconfident_error_rate` with the new B/C trajectories and the reused A
   trajectories. Bonferroni α = 0.025 across {A-vs-B, B-vs-C}. No new code beyond a thin glue
   script.

## References

* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` (v1, plan parser)
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` (delegate wrapper)
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py` (confidence layer)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/runner.py` (variant dispatch)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/mcnemar.py` (paired McNemar)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/calibration.py` (Xiong2024 ECE)
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` (147-id manifest)
