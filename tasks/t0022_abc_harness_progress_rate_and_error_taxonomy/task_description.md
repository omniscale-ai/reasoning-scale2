# ABC Harness with Progress Rate and EAI Error Taxonomy

## Motivation

t0012's smoke run on FrontierScience-Olympiad with claude-haiku-4-5 hit the floor across all three
ABC conditions (A: 2.5%, B: 0%, C: 0%). At the floor, **binary task success cannot distinguish**
scope-aware from scope-unaware behaviour, so RQ1, RQ2, and RQ5 are invisible no matter how big the
sample.

t0017 surfaced two literature instruments that fix this:

* **AgentBoard progress rate** (Ma2024, NeurIPS 2024 D&B): subgoal coverage scoring with Pearson rho
  \> 0.95 against humans across 1013 environments. A continuous metric in `[0, 1]` that gives signal
  even when no run reaches the terminal goal.
* **Embodied Agent Interface error taxonomy** (Li2024, NeurIPS 2024): a 6-class per-step taxonomy
  (hallucination, affordance violation, missing step, extra step, wrong-order step,
  precondition/effect error) that attributes failures to specific modes.

Both instruments must be in place **before** t0023's confirmatory N>=157 run, otherwise t0023 risks
producing the same uninformative floor result that t0012 produced. This task is a zero-API library
task that builds the two instruments and validates them on the t0012 sample.

This task covers `S-0017-02`.

## Scope

Build a single library that the existing ABC harness can import and call, exposing two functions:

1. `compute_progress_rate(trajectory, environment_subgoals) -> float`
   * Implements the Ma2024 protocol: a list of subgoals defined per environment, scored 0/1 by a
     judge model, averaged over the trajectory. Returns a float in `[0, 1]`.
2. `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel`
   * Implements the Li2024 protocol: a strict-output judge call that returns one of six labels
     (`hallucination`, `affordance`, `missing_step`, `extra_step`, `wrong_order`,
     `precondition_or_effect`) plus an "ok" sentinel for non-error steps.

Both functions delegate to a judge model (default: claude-haiku-4-5; configurable to sonnet).
Subgoal definitions for FrontierScience-Olympiad and SWE-bench Verified live in a JSON side-file in
the library asset's `files/` directory. SWE-bench coverage is the priority since t0023 runs there.

The library exposes a single high-level entry point
`score_trajectory(trajectory, environment) -> TrajectoryScore` that returns:

* `task_success: bool`
* `progress_rate: float`
* `step_errors: list[ErrorTaxonomyLabel]`
* `error_distribution: dict[label, count]`

## Deliverables

1. **Library asset** (`assets/library/abc_harness_metrics/`) with `details.json`, canonical
   description document, source code under `files/`, and subgoal-definition JSON for at least
   FrontierScience-Olympiad and SWE-bench Verified Lite.
2. **Unit tests** in `tasks/t0022_*/code/test_*.py`:
   * Progress rate is `0.0` when no subgoal is hit and `1.0` when all subgoals are hit, on a
     synthetic trajectory.
   * Each error taxonomy label is producible on a hand-crafted trajectory step.
   * The high-level entry point composes the two without raising on a known-good t0012 row.
3. **Validation against t0012**: replay the t0012 smoke trajectories through the new library and
   report progress rate and error distribution per ABC condition. Save these as a side-by-side table
   in `results/results_detailed.md`.
4. **Subgoal-definition JSON** for SWE-bench Verified Lite covering at least 50 instances (the
   subset t0023 will use). Use the SWE-bench Verified hint annotations as the seed.

## Implementation Notes

* **Subgoal scoring is a judge call**, not a deterministic check. Cache results to disk keyed by
  (environment, trajectory hash, subgoal text) so re-runs in t0023 do not re-spend.
* **Judge prompt** for progress rate: copy the Ma2024 supplementary material §C.2 prompt verbatim
  where licensing allows; otherwise paraphrase with explicit attribution in the library description
  document.
* **Error taxonomy prompt** for `classify_error`: use Li2024's appendix A.4 schema. The classifier
  returns exactly one label; ties default to `precondition_or_effect`.
* **Subgoal coverage on SWE-bench**: a "subgoal hit" is operationalised as the agent producing an
  edit that touches the same file as the gold patch hunk; finer-grained subgoals (line ranges, AST
  nodes) are out of scope here and can land in a follow-up.

## Cost Estimate

* Validation pass on t0012 smoke trajectories (~40 rows x 3 conditions x ~5 steps each = 600
  step-classifications + 120 progress-rate scores): **~720 haiku judge calls**.
* Haiku ~2k tokens in, ~150 tokens out per call: **~1.4M in, ~110k out**.
* At haiku pricing: **~$1.50**.
* Reserve: **+$0.50**.
* Total: **~$2**.

## Decision Criteria

After this task:

* If progress rate on the t0012 sample produces a non-degenerate distribution (mean > 0.05 and
  stddev > 0.03), the metric is a viable Metric 1 candidate for t0023. Otherwise, document the
  calibration problem and propose a different subgoal granularity.
* If the error taxonomy correctly distinguishes condition C trajectories from condition A
  trajectories on at least **30% of paired steps**, the taxonomy is doing real work and t0023 can
  rely on it. Otherwise, flag and recommend tightening the per-environment subgoal lists before
  t0023.

## Dependencies

None. Output is consumed by t0023.

## Source Suggestion

`S-0017-02`.

## Risks and Fallbacks

* **Judge cost on t0023 explodes**: t0023 with N=157 x 3 conditions x ~5 steps each = ~2400
  step-classifications. Plan haiku as the default judge; reserve sonnet for spot-check re-grading on
  a 20-row stratified sample only.
* **Subgoal definitions miscalibrate**: the SWE-bench JSON has to be reviewed by hand on a
  10-instance pilot before t0023 ships.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass.
* Subgoal-definition JSON contains entries for at least 50 SWE-bench Verified Lite instances.
* The t0012 replay produces a per-condition breakdown of progress rate and error distribution in
  `results/results_detailed.md`.
* Cost in `results/costs.json` is at or below **$2**.
