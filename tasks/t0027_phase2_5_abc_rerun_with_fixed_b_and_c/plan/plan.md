---
spec_version: "2"
task_id: "t0027_phase2_5_abc_rerun_with_fixed_b_and_c"
date_completed: "2026-05-02"
status: "complete"
---
# Plan — t0027 Phase 2.5 A/B/C re-run with fault-tolerant B and structurally-distinct C

## Objective

Fork t0021's Plan-and-Solve v2 into a fault-tolerant `plan_and_solve_v3` library (re-prompt + JSON
tool-call fallback over `MalformedPlanError`), fork t0010's matched-mismatch wrapper into
`matched_mismatch_v2` re-targeted at v3, then re-run B and C on t0026's 130 paired instances and
re-run the paired McNemar test (Bonferroni α = 0.025) for RQ1 (A vs B) and RQ5 (B vs C). A is not
re-run — t0026's A trajectories are reused. "Done" means: two new library assets pass
`verify_library_asset`; three predictions assets exist (`abc_rerun_a_reused`, `abc_rerun_b`,
`abc_rerun_c`); B's re-run produces fewer than 3 `MalformedPlanError` trajectories; the McNemar JSON
for both pairs is written; all four charts are embedded in `results_detailed.md`.

## Task Requirement Checklist

Verbatim task instruction (from `task.json` `short_description` and `task_description.md`):

> Fix B's plan parser (S-0026-01), redesign C to delegate to plan_and_solve (S-0026-02), then re-run
> A/B/C on the 130 paired instances to get real RQ1 and RQ5 answers.
> 
> RQ1: Does scope-aware ReAct (A) achieve a higher paired task-success rate than scope-unaware
> Plan-and-Solve (B), once B's parser no longer collapses on noisy plans? RQ5: Is the
> matched-mismatch variant (C) strictly worse than both A and B, once C's scaffold is
> `plan_and_solve_v2` rather than `scope_aware_react`?

Decomposed requirements:

* **REQ-1** — Build `plan_and_solve_v3` library that wraps t0021 v2 with a `_robust_parse_plan`
  helper: try the existing parser, on `MalformedPlanError` re-prompt with a stricter format reminder
  and parse again, on second failure call Anthropic's tool-use JSON mode with a
  `{steps: list[string]}` schema, on third failure re-raise `MalformedPlanError`. Evidence:
  `assets/library/plan_and_solve_v3/` passes `verify_library_asset`. Satisfied by Step 2.
* **REQ-2** — Build `matched_mismatch_v2` library that forks t0010 verbatim and changes the
  `delegate` default from `"scope_aware_react"` to `"scope_unaware_planandsolve_v3"`. Evidence:
  `assets/library/matched_mismatch_v2/` passes `verify_library_asset`. Satisfied by Step 3.
* **REQ-3** — Re-use t0026's A predictions by reference (asset pointer in
  `assets/predictions/abc_rerun_a_reused/details.json`). Evidence: details.json points at t0026's
  variant_a asset. Satisfied by Step 4.
* **REQ-4** — Re-run B on the 130 paired instances using `plan_and_solve_v3`. Evidence: 130
  trajectory_<id>.json files in `assets/predictions/abc_rerun_b/` plus `details.json`. Satisfied by
  Step 5.
* **REQ-5** — Re-run C on the 130 paired instances using `matched_mismatch_v2`. Evidence: 130
  trajectory files in `assets/predictions/abc_rerun_c/` plus `details.json`. Satisfied by Step 6.
* **REQ-6** — B's re-run produces fewer than 3 `MalformedPlanError` trajectories (acceptance gate
  for REQ-1). Evidence: `data/parser_failure_count.json` reports a count < 3. Satisfied by Step 5.
* **REQ-7** — C's smoke trajectories show v3-shaped `decision_log` (acceptance gate for REQ-2).
  Evidence: 5-instance smoke trajectories include the v3 `final_confidence` field on the finishing
  record. Satisfied by Step 6.
* **REQ-8** — Compute paired McNemar exact-binomial for A-vs-B and B-vs-C with Bonferroni α = 0.025
  across both tests. Evidence: `data/mcnemar_results.json` with `discordant_b`, `discordant_c`,
  `statistic`, `p_value`, `method` fields per pair. Satisfied by Step 7.
* **REQ-9** — Compute Xiong2024 ECE 10-bin calibration on B and C trajectories; reuse t0026's A
  calibration. Evidence: `data/calibration.json` with B and C `ece` and per-bin breakdowns.
  Satisfied by Step 7.
* **REQ-10** — Produce 4 charts in `results/images/` (paired contingency, per-subset success-rate,
  parser-failure rate before vs after, overconfident-error-rate per variant) and embed them in
  `results_detailed.md`. Satisfied by Step 8 (orchestrator-managed reporting; chart files written
  during analysis).
* **REQ-11** — `verify_task_metrics.py`, `verify_task_results.py`, and `verify_pr_premerge.py` pass
  with 0 errors. Satisfied across Steps 7-8 plus orchestrator reporting steps.

## Approach

The structural finding from research-code is that `MalformedPlanError` lives in t0007's v1
`parse_plan` (raised at `planandsolve.py:189-192`, called from `PlanAndSolveAgent.run` at
`planandsolve.py:280-282` with no retry path). t0021's v2 wrapper adds `final_confidence`
elicitation but does not parse plans, so the v3 fix must override v1's plan-parse step rather than
touching v2's confidence layer. The cleanest fork is a single new module that imports `parse_plan`,
`_PLAN_LINE_RE`, `MalformedPlanError`, the prompt templates, and the executor logic from t0007
verbatim, then overrides the parsing step in a v3 subclass with a
`_robust_parse_plan(model_call, problem, plan_text, *, max_attempts=2, json_fallback=True)` helper.
The v2 confidence shell is wrapped around the v3 agent unchanged.

For C, t0010's `MatchedMismatchAgent` accepts a `delegate` string literal at
`matched_mismatch.py:54-66` and dispatches to one of two parsers (`_parse_react_output` or
`_parse_planandsolve_output`). The adversarial mapping
`ADVERSARIAL_MAP = {"global": "atomic", "atomic": "global", "subtask": "atomic"}` at
`matched_mismatch.py:66-70` is delegate-agnostic. The fix is a one-line default-flip in
matched_mismatch_v2 plus a re-pointed import target.

For the harness, t0026's `runner.py:166-214` already provides the variant dispatch shape and the
trajectory output format (`_InstanceOutcome` dataclass at `runner.py:98-104`). The cross-task import
rule forbids importing t0026's `code/` directly, so the harness modules (`runner.py`, `mcnemar.py`,
`calibration.py`, `metrics.py`, `instance_loader.py`, `paths.py`, `anthropic_shim.py`, `judge.py`)
are copied into `tasks/t0027/.../code/` verbatim with two edits: `_run_variant_b` is redirected to
`PlanAndSolveAgentV3`, and `_run_variant_c` is redirected to `MatchedMismatchAgentV2`.

**Alternatives considered.** (1) Add the retry path inside t0021 v2 directly. Rejected — it violates
the immutability rule for completed tasks and would require a correction overlay. (2) Use only the
JSON tool-call path (skip the re-prompt). Rejected — re-prompt with a stricter format reminder is
cheap (~$0.005/call) and resolves most failures without invoking a different code path; reserving
the JSON fallback for genuine model confusion keeps the residual `MalformedPlanError` rate honest.
(3) Re-run A as well. Rejected — A is unaffected by either defect; reusing t0026 trajectories saves
~$10 and removes a source of run-to-run variance.

**Task types**: `write-library`, `experiment-run`, `comparative-analysis` (matches `task.json`). The
write-library guidelines drive the `assets/library/<id>/` layout and `description.md` +
`details.json` per library. The experiment-run guidelines drive the per-row checkpointing, budget
enforcement, and trajectory shape. The comparative-analysis guidelines drive the McNemar
+ Bonferroni reporting in `results_detailed.md`.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| B re-run, 130 instances, `claude-opus-4-7` | $14-18 |
| C re-run, 130 instances, `claude-opus-4-7` | $14-18 |
| A re-use (no re-run) | $0 |
| Calibration: 3-sample self-consistency over B and C | $4-6 |
| Smoke + parser-fix repro + plan-parse fallback overhead | $2-3 |
| **Total** | **$34-45** |

Project budget remaining: ~$87 at the start of t0027 (per `aggregate_costs`). Per-task cap: $50
declared in `task_description.md`. Hard stop in the harness if cumulative spend exceeds $50.

## Step by Step

Milestones: M1 = libraries built (Steps 1-3); M2 = predictions complete (Steps 4-6); M3 = analysis +
charts (Steps 7-8).

1. **Copy harness modules from t0026.** Copy
   `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/{runner.py,mcnemar.py,calibration.py,metrics.py,instance_loader.py,paths.py,anthropic_shim.py,judge.py}`
   to `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/`. Update `paths.py` constants for the
   new task root. Run `uv run mypy -p tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code`.
   Inputs: t0026 `code/`. Outputs: t0027 `code/`. Expected: mypy passes; no behavioral changes
   except path constants. Satisfies REQ-3 prep.

2. **Build `plan_and_solve_v3` library.** Create
   `assets/library/plan_and_solve_v3/{description.md,details.json,planandsolve_v3.py}`.
   `planandsolve_v3.py` imports `parse_plan`, `_PLAN_LINE_RE`, `MalformedPlanError`,
   `PLAN_PROMPT_TEMPLATE`, `TrajectoryRecord` from t0007's `planandsolve.py`, and
   `elicit_final_confidence`, `parse_final_confidence`, `CONFIDENCE_PROMPT_TEMPLATE`,
   `CONFIDENCE_RETRY_PROMPT_TEMPLATE`, `TrajectoryRecordV2` from t0021's `planandsolve_v2.py`.
   Define
   `_robust_parse_plan(model_call, problem, plan_text, *, max_attempts=2, json_fallback=True)` that
   (a) tries `parse_plan(plan_text)`; (b) on `MalformedPlanError`, re-prompts the model with a
   stricter format reminder ("Re-emit the plan as a numbered list. Each step must start with `1.`,
   `2.`, etc.") and tries `parse_plan` on the new text; (c) on second failure, calls Anthropic's
   tool-use JSON mode with schema
   `{"type": "object", "properties": {"steps": {"type": "array", "items": {"type": "string"}}}}`;
   (d) on third failure, re-raises `MalformedPlanError`. Subclass `PlanAndSolveAgent` as
   `PlanAndSolveAgentV3` and override the run-loop branch at lines 280-282 to call
   `_robust_parse_plan` instead of `parse_plan`. Wrap `PlanAndSolveAgentV3` in v2's confidence
   shell. Write `description.md` (project-format library description) and `details.json` per
   `meta/asset_types/library/specification.md`. Add `code/test_plan_and_solve_v3.py` with 4 unit
   tests: clean-parse, re-prompt success, JSON-fallback success, all-fail. Run
   `uv run pytest tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/test_plan_and_solve_v3.py -v`;
   confirm 4 passed. Satisfies REQ-1.

3. **Build `matched_mismatch_v2` library.** Create
   `assets/library/matched_mismatch_v2/{description.md,details.json,matched_mismatch_v2.py}`. Copy
   t0010's `matched_mismatch.py` verbatim, change the `_parse_planandsolve_output` import target to
   v3's library, and update the default `delegate` literal from `"scope_aware_react"` to
   `"scope_unaware_planandsolve_v3"`. Adversarial perturbation logic (`ADVERSARIAL_MAP`,
   `pick_mismatch_tag`) unchanged. Add `code/test_matched_mismatch_v2.py` with 2 unit tests: default
   delegate is v3, perturbation logic is identical to v1. Run `uv run pytest`. Satisfies REQ-2.

4. **Reuse A predictions by reference.** Create `assets/predictions/abc_rerun_a_reused/details.json`
   with a pointer to t0026's variant_a asset path. Do not copy the trajectory files — the harness
   reads them through the pointer. Verify by listing the resolved path: it must contain at least 130
   paired trajectory files. Inputs:
   `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/variant_a/`. Outputs: t0027
   `details.json` with the pointer. Satisfies REQ-3.

5. **[CRITICAL] Re-run B on the 130 paired set.** Write `code/run_abc_rerun.py` that loads the t0026
   manifest, intersects to the 130 paired ids, and calls
   `runner.run_variant("b", instances, agent_factory=PlanAndSolveAgentV3)` with checkpointing to
   `assets/predictions/abc_rerun_b/`. **Validation gate before full run**: run with `--limit 5`
   first; trivial baseline = 0 successes (parser collapses every run); failure condition = "if all 5
   limit-run trajectories are `MalformedPlanError`, halt and inspect `_robust_parse_plan` outputs
   individually before unblocking the full 130-instance run." Then run the full 130. Hard-stop if
   spend > $25. Compute and write `data/parser_failure_count.json` with
   `{"b_old_failures": 16, "b_new_failures": <n>, "n_total": 130}`. Inputs: t0026 manifest,
   plan_and_solve_v3, anthropic_shim. Outputs: 130 trajectory_<id>.json files plus `details.json`.
   Expected: B's success rate >= t0026 B's success rate; parser-failure count < 3. Satisfies REQ-4 +
   REQ-6.

6. **[CRITICAL] Re-run C on the 130 paired set.** Same harness as Step 5 but with
   `agent_factory=MatchedMismatchAgentV2`. **Validation gate before full run**: 5-instance
   FrontierScience smoke first; trivial baseline = trajectory shape matches A (would mean the
   delegate flip didn't take); failure condition = "if smoke trajectories use ReAct shape instead of
   v3 plan-and-solve shape, halt and re-inspect the import target in `matched_mismatch_v2.py` before
   unblocking." Then run the full 130. Hard-stop if spend > $25. Outputs: 130 trajectory_<id>.json
   files plus `details.json`. Expected: trajectories show `final_confidence` on the finishing record
   (v3 shape). Satisfies REQ-5 + REQ-7.

7. **Run McNemar + calibration analysis.** Write `code/run_analysis.py` that calls
   `mcnemar.pairwise_mcnemar(success_a, success_b_new)` and
   `mcnemar.pairwise_mcnemar(success_b_new, success_c_new)` over the 130 paired set. Apply
   Bonferroni α = 0.025 across {A-vs-B, B-vs-C}. Compute
   `calibration.compute_ece_10bin(confidences, outcomes)` for B and C; reuse A's ECE values from
   `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/calibration.json`. Compute
   `metrics.compute_overconfident_error_rate` per Xiong2024 for B and C. Write
   `data/mcnemar_results.json`, `data/calibration.json`, and `results/metrics.json` with registered
   keys: `task_success_rate`, `avg_decisions_per_task`, `overconfident_error_rate` (B and C only,
   per t0026 convention). Satisfies REQ-8 + REQ-9.

8. **Generate the 4 charts.** Write `code/make_plots.py` that produces: (1) paired contingency
   heatmaps for A-vs-B and B-vs-C → `results/images/contingency_a_b.png`,
   `results/images/contingency_b_c.png`; (2) per-subset task-success-rate bar chart for A/B/C →
   `results/images/per_subset_success_rate.png`; (3) parser-failure-rate bar chart B-old vs B-new →
   `results/images/parser_failure_rate.png`; (4) `overconfident_error_rate` bar chart for B/C with
   95% CIs → `results/images/overconfident_error_rate.png`. The orchestrator-managed reporting step
   embeds these via `![desc](images/file.png)`. Satisfies REQ-10.

## Remote Machines

None required. The task uses only the Anthropic API (`claude-opus-4-7`) and runs the harness locally
on the agent's host. No GPU compute, no vast.ai provisioning, no remote SSH. The `teardown` step is
therefore also skipped.

## Assets Needed

Inputs (read-only, no modifications):

* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` — v1 base for v3 fork
  (`parse_plan`, `_PLAN_LINE_RE`, `MalformedPlanError`, prompt templates, executor logic).
* `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py` — v2 confidence
  layer for v3 fork (`elicit_final_confidence`, `parse_final_confidence`, prompt templates,
  `TrajectoryRecordV2`).
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` — v1 base for v2 fork
  (`MatchedMismatchAgent`, `pick_mismatch_tag`, `ADVERSARIAL_MAP`).
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/code/{runner,mcnemar,calibration,metrics,instance_loader,paths,anthropic_shim,judge}.py`
  — copied into t0027 `code/` (cross-task import rule).
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/instance_manifest.json` — 147-id manifest,
  intersected to 130 paired ids.
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/assets/predictions/variant_a/` — A trajectories,
  reused by reference.
* `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/data/calibration.json` — A's ECE values.
* External: Anthropic API key (already provisioned in the project's `.env`).

## Expected Assets

Per `task.json` `expected_assets: {library: 2, predictions: 3}`:

* **library** `plan_and_solve_v3` — fault-tolerant Plan-and-Solve with re-prompt + JSON tool-call
  fallback. Folder: `assets/library/plan_and_solve_v3/`.
* **library** `matched_mismatch_v2` — matched-mismatch wrapper re-targeted to v3. Folder:
  `assets/library/matched_mismatch_v2/`.
* **predictions** `abc_rerun_a_reused` — pointer asset to t0026's variant_a (no new trajectory
  files; just `details.json`). Folder: `assets/predictions/abc_rerun_a_reused/`.
* **predictions** `abc_rerun_b` — fresh B trajectories on the 130 paired set, plus `details.json`.
  Folder: `assets/predictions/abc_rerun_b/`.
* **predictions** `abc_rerun_c` — fresh C trajectories on the 130 paired set, plus `details.json`.
  Folder: `assets/predictions/abc_rerun_c/`.

## Time Estimation

* Research already done.
* Step 1 (copy harness): ~10 min.
* Step 2 (build v3): ~60 min including 4 unit tests.
* Step 3 (build v2 wrapper): ~15 min.
* Step 4 (reuse A): ~5 min.
* Step 5 (run B, 130 instances): wall clock ~75-90 min at ~30-40 sec/instance, parallelized.
* Step 6 (run C, 130 instances): wall clock ~75-90 min similar.
* Step 7 (analysis): ~15 min.
* Step 8 (charts + embedding): ~30 min.
* Total wall clock: ~4-5 hours, mostly waiting on the API.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Re-prompt + JSON fallback still leave parser-failure rate >= 3/130 | Medium | RQ1 stays unanswered, paper claim has to be hedged | Document the residual cause in results, treat as a real finding ("no detectable difference even after parser fix"), do not re-engineer further. |
| C-new beats B-new (direction flip vs hypothesis) | Medium | RQ5 gets rejected for the right reason but with unexpected direction | Report as a finding with discussion; the mechanism is now real (perturbed granularity tags on a planning scaffold), not a delegation accident. |
| Cost overrun on B or C stream | Low | Budget pressure; truncated paired set | Per-stream hard stop at $25; if hit, truncate to whatever paired set was completed and re-run McNemar on truncated N with explicit reporting. |
| Anthropic API rate limit during 130-instance batch | Medium | Slowed wall-clock | Re-use t0026's per-row checkpointing; resume from last checkpoint after rate-limit pause; exponential backoff already in `anthropic_shim.py`. |
| Anthropic tool-use JSON mode returns malformed JSON | Low | Third-attempt parse failure, residual `MalformedPlanError` | Catch JSON parse error and re-raise `MalformedPlanError` like any other failure; the bound is intentional (max 2 attempts + JSON fallback) to keep residual rate honest. |
| t0026 manifest 130-paired intersection produces a different set than t0026 reported | Low | Asymmetry between A (reused) and B/C (fresh) breaks the paired McNemar | Compute the intersection explicitly in Step 5, assert it equals 130, and assert each paired id has a t0026 A trajectory; halt if either assertion fails. |

## Verification Criteria

* `uv run python -u -m arf.scripts.verificators.verify_library_asset plan_and_solve_v3 --task-id t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
  — expect 0 errors. Confirms REQ-1.
* `uv run python -u -m arf.scripts.verificators.verify_library_asset matched_mismatch_v2 --task-id t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
  — expect 0 errors. Confirms REQ-2.
* `uv run python -u -m arf.scripts.verificators.verify_predictions_asset abc_rerun_b --task-id t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
  and same for `abc_rerun_c` and `abc_rerun_a_reused` — expect 0 errors. Confirms REQ-3 + REQ-4 +
  REQ-5.
* `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0027_phase2_5_abc_rerun_with_fixed_b_and_c -- uv run pytest tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/code/`
  — expect all unit tests pass.
* `cat tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/parser_failure_count.json` — expect
  `b_new_failures < 3`. Confirms REQ-6.
* `head -20 tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/assets/predictions/abc_rerun_c/trajectory_<smoke_id>.json`
  on any of the 5 smoke ids — expect `final_confidence` field present on the finishing record.
  Confirms REQ-7.
* `cat tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/mcnemar_results.json` — expect both
  `a_vs_b` and `b_vs_c` blocks with `discordant_b`, `discordant_c`, `statistic`, `p_value`,
  `method`, plus `bonferroni_alpha: 0.025`. Confirms REQ-8.
* `cat tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/data/calibration.json` — expect `b` and `c`
  blocks with `ece` and 10-bin breakdowns. Confirms REQ-9.
* `ls tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/images/` — expect 4 PNG files
  (`contingency_a_b.png`, `contingency_b_c.png` or a single combined heatmap,
  `per_subset_success_rate.png`, `parser_failure_rate.png`, `overconfident_error_rate.png`).
  Confirms REQ-10.
* `uv run python -u -m arf.scripts.verificators.verify_task_metrics t0027_phase2_5_abc_rerun_with_fixed_b_and_c`
  and `verify_task_results` and `verify_pr_premerge` — all 0 errors. Confirms REQ-11.
