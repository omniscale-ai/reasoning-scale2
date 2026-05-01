---
spec_version: "2"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: ABC Harness with Progress Rate and EAI Error Taxonomy

## Objective

Build a single Python library `abc_harness_metrics` exposing `compute_progress_rate`,
`classify_error`, and a high-level `score_trajectory` entry point so that future scope-aware vs.
scope-unaware ABC runs (notably t0023, N>=157) produce continuous, fine-grained signal even when
binary task success collapses to the floor. Done means: the library asset under
`assets/library/abc_harness_metrics/` passes `verify_library_asset.py`; unit tests pass; the t0012
smoke trajectories have been replayed through the library and scored; and `results_detailed.md`
shows progress-rate distribution stats and an A-vs-C error-taxonomy separation rate against the two
quantitative decision criteria stated in `task_description.md`.

## Task Requirement Checklist

The operative task request from `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/task.json`
plus its referenced `task_description.md` is reproduced verbatim below.

> **name**: ABC Harness with Progress Rate and EAI Error Taxonomy
> 
> **short_description**: Extend the ABC harness with AgentBoard subgoal progress rate and the
> Embodied Agent Interface error taxonomy so floor-bound runs still produce signal.
> 
> Build a single library that the existing ABC harness can import and call, exposing two functions:
> 
> 1. `compute_progress_rate(trajectory, environment_subgoals) -> float` — Implements the Ma2024
>    protocol: a list of subgoals defined per environment, scored 0/1 by a judge model, averaged
>    over the trajectory. Returns a float in `[0, 1]`.
> 2. `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel` — Implements the
>    Li2024 protocol: a strict-output judge call that returns one of six labels (`hallucination`,
>    `affordance`, `missing_step`, `extra_step`, `wrong_order`, `precondition_or_effect`) plus an
>    "ok" sentinel for non-error steps.
> 
> Both functions delegate to a judge model (default: claude-haiku-4-5; configurable to sonnet).
> Subgoal definitions for FrontierScience-Olympiad and SWE-bench Verified live in a JSON side-file
> in the library asset's `files/` directory. SWE-bench coverage is the priority since t0023 runs
> there.
> 
> The library exposes a single high-level entry point
> `score_trajectory(trajectory, environment) -> TrajectoryScore` that returns: `task_success: bool`,
> `progress_rate: float`, `step_errors: list[ErrorTaxonomyLabel]`,
> `error_distribution: dict[label, count]`.
> 
> Deliverables: library asset, unit tests, validation against t0012, subgoal-definition JSON for
> SWE-bench Verified Lite covering at least 50 instances.
> 
> Decision criteria: progress rate mean > 0.05 and stddev > 0.03 on t0012 sample; error taxonomy
> distinguishes C from A on >= 30% of paired steps. Cost <= $2.

The concrete requirements decomposed from this text:

* **REQ-1** — Implement `compute_progress_rate(trajectory, environment_subgoals) -> float` per
  Ma2024 (Ma2024 §C.2 prompt; discrete-subgoal coverage `(1/K) sum_k 1{subgoal_k hit by some step}`,
  scored 0/1 by a judge call). Satisfied by Step 4; evidence: function signature in
  `code/progress_rate.py` plus unit-test pass.
* **REQ-2** — Implement `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel`
  per Li2024 (§A.4), 6 error labels plus `"ok"` sentinel; ties default to `precondition_or_effect`.
  Satisfied by Step 5; evidence: function signature in `code/error_taxonomy.py` plus unit-test pass
  for each of the 7 labels.
* **REQ-3** — Implement `score_trajectory(trajectory, environment) -> TrajectoryScore` returning
  `task_success`, `progress_rate`, `step_errors`, `error_distribution`. Satisfied by Step 6;
  evidence: type-checked dataclass result in `code/score_trajectory.py`.
* **REQ-4** — Default judge `claude-haiku-4-5`, configurable to sonnet. Satisfied by Step 3
  (`code/model_call.py` constants); evidence: `JUDGE_MODEL` constant and unit test that overrides
  it.
* **REQ-5** — Subgoal-definition JSON for FrontierScience-Olympiad. Satisfied by Step 7; evidence:
  `assets/library/abc_harness_metrics/files/subgoals_frontierscience_olympiad.json` covers all 40
  smoke instances.
* **REQ-6** — Subgoal-definition JSON for SWE-bench Verified Lite covering at least 50 instances.
  Satisfied by Step 8; evidence:
  `assets/library/abc_harness_metrics/files/subgoals_swebench_verified_lite.json` with len >= 50.
* **REQ-7** — Cache judge results to disk keyed by `(environment, trajectory_hash, prompt_key)`.
  Satisfied by Step 3 cache layer in `code/judge_cache.py`; evidence: re-run with same inputs makes
  zero new API calls (logged token cost == 0 on second pass).
* **REQ-8** — Unit tests in `tasks/t0022_*/code/test_*.py` covering: progress rate 0.0/1.0
  endpoints; each error label producible; high-level entry point composes without raising on a
  known-good t0012 row. Satisfied by Step 9; evidence: `uv run pytest -p tasks.t0022_*.code` passes
  with >= 7 test cases.
* **REQ-9** — Validation against t0012: replay smoke trajectories, report progress rate and error
  distribution per ABC condition. Satisfied by Step 10; evidence: per-condition stats in
  `code/replay_summary.json` (rendered into `results/results_detailed.md` by the orchestrator's
  `results` step).
* **REQ-10** — Library asset under `assets/library/abc_harness_metrics/` with `details.json`,
  `description.md`, and `files/` JSON side-files. Satisfied by Step 11; evidence:
  `verify_library_asset.py` passes.
* **REQ-11** — Decision criteria 1: progress rate mean > 0.05 and stddev > 0.03 on the t0012 sample.
  Satisfied by Step 10 evaluation; evidence: numbers reported in `results_detailed.md` and in
  `metrics.json`.
* **REQ-12** — Decision criteria 2: error taxonomy distinguishes C from A on >= 30% of paired steps.
  Satisfied by Step 10 evaluation; evidence: separation rate reported.
* **REQ-13** — Cost in `results/costs.json` is at or below $2. Satisfied by Step 10 cost accounting
  plus Step 12 cost roll-up; evidence: `costs.json` total <= 2.00 USD.

## Approach

The implementation copies the local `claude` CLI invocation pattern from
`tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py` (no Anthropic Python SDK; the
local CLI uses Claude Code OAuth credentials and is much cheaper when invoked with
`--system-prompt MIN --tools "" --setting-sources ""`, which gives a ~25x cost reduction relative to
the default invocation). Cross-task imports are forbidden, so the file is **copied** into
`tasks/t0022_*/code/model_call.py` (as confirmed by research_code.md). Progress rate uses the Ma2024
discrete-subgoal-coverage form `pr = (1/K) * sum_{k in subgoals} 1{some step hits k}`, implemented
with one judge call per (subgoal, step) pair, with an early-exit short-circuit once a subgoal flips
to hit. Error taxonomy uses Li2024's strict 6-class output schema with `"ok"` as the non-error
sentinel; ties or ambiguous outputs default to `precondition_or_effect` per the task spec. A SHA-256
disk cache keyed by `(environment_id, trajectory_hash, prompt_key)` prevents re-spending on
identical inputs. The high-level `score_trajectory` composes the two functions and returns a frozen
dataclass `TrajectoryScore`.

**Alternatives considered**:

* Using the Anthropic Python SDK directly was rejected — t0012 already established that the local
  `claude` CLI with the cost-reduction flags is the project-standard pattern and works without
  paying for additional API credits at the project level.
* A continuous-progress score that averages partial-credit judgments per step was rejected — Ma2024
  reports Pearson rho > 0.95 against humans only for the discrete-subgoal-coverage form, and
  introducing a partial-credit scheme would require new calibration that this task does not have
  budget for.

**Task types**: `write-library` (matches `task.json` `task_types`). The `write-library`-type
planning guidelines say the deliverable is a registered library asset plus a canonical description
document; no remote machines; no fresh experiments beyond a calibration replay; explicit unit tests
on synthetic inputs.

## Cost Estimation

Validation pass on t0012 smoke trajectories: 40 + 40 + 11 = 91 trajectories. C trajectories average
~26 steps; A and B average ~1.2 steps. Estimated step-classification calls: 11 * 26 + 80 * 1.2 ~=
286 + 96 = 382 calls; with retries and progress-rate calls (estimate ~120 progress-rate scoring
calls split over subgoals), total ~720 haiku judge calls. Haiku pricing: ~2k tokens in / ~150 tokens
out per call → ~1.4M in, ~~110k out → **~~$1.50**. Reserve **+$0.50** for caching misses and
retries. Total **~$2.00** (matches `task_description.md`'s cost cap). Implementation steps that do
not call the judge cost $0. **Hard cap: $2** — the implementation must abort if the running cost
exceeds this.

## Step by Step

1. **Copy CLI invocation module from t0012.** Copy
   `tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py` to
   `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/model_call.py` verbatim, then
   adapt: change the module docstring to mention t0022, keep the
   `--system-prompt MIN --tools "" --setting-sources ""` cost-reduction flags, keep `CostTracker`
   and `CallRecord` dataclasses, leave the public
   `_invoke_cli(*, prompt: str, model: str) -> tuple[str, dict[str, Any]]` signature unchanged.
   Inputs: t0012 file. Outputs: `code/model_call.py`. Satisfies REQ-4.

2. **Define shared types and constants.** Create `code/types.py` with frozen dataclasses
   `TrajectoryStep`, `Trajectory`, `Subgoal`, `EnvironmentSubgoals`, `TrajectoryScore` and an
   `ErrorTaxonomyLabel` `StrEnum` containing exactly the 7 values (`hallucination`, `affordance`,
   `missing_step`, `extra_step`, `wrong_order`, `precondition_or_effect`, `ok`). Create
   `code/constants.py` with `JUDGE_MODEL_DEFAULT = "claude-haiku-4-5"`,
   `JUDGE_MODEL_FALLBACK = "claude-sonnet-4-5"`, `MAX_BUDGET_USD = 2.00`, prompt-template constants.
   Create `code/paths.py` with library-asset paths and the cache root `tasks/t0022_*/code/_cache/`.
   Inputs: none. Outputs: 3 files. Satisfies REQ-1, REQ-2, REQ-3.

3. **Implement disk-cache layer.** Create `code/judge_cache.py` exposing
   `cache_get(*, key: str) -> str | None` and `cache_put(*, key: str, value: str) -> None`. Cache
   key is `sha256(environment_id + "|" + trajectory_hash + "|" + prompt_key).hexdigest()`. Storage:
   one JSON file per key under `_cache/<first-2-hex>/<rest-of-hex>.json`. Inputs: `code/types.py`.
   Outputs: `code/judge_cache.py`. Satisfies REQ-7.

4. **Implement progress rate.** Create `code/progress_rate.py` with
   `compute_progress_rate(*, trajectory: Trajectory, environment_subgoals: EnvironmentSubgoals, judge_model: str = JUDGE_MODEL_DEFAULT, cost_tracker: CostTracker | None = None) -> float`.
   Algorithm: for each subgoal `g_k` in `environment_subgoals.subgoals`, iterate steps until either
   the judge returns `hit=True` (then mark subgoal k hit and continue to next subgoal) or all steps
   exhausted; return `sum(hits) / len(subgoals)`. Each judge call goes through the cache first. The
   judge prompt is the Ma2024 §C.2 schema paraphrased (verbatim attribution in `description.md`).
   Use `_invoke_cli` from Step 1. Inputs: `types.py`, `model_call.py`, `judge_cache.py`. Outputs:
   `code/progress_rate.py`. Satisfies REQ-1.

5. **Implement error taxonomy classifier.** Create `code/error_taxonomy.py` with
   `classify_error(*, trajectory_step: TrajectoryStep, environment_state: dict[str, Any], judge_model: str = JUDGE_MODEL_DEFAULT, cost_tracker: CostTracker | None = None) -> ErrorTaxonomyLabel`.
   Algorithm: build a Li2024 §A.4 strict-output prompt that lists the 7 labels and asks for exactly
   one; cache lookup; on judge response, parse out the label; if parsing fails or the response is
   ambiguous, return `ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT` per the spec. Inputs: `types.py`,
   `model_call.py`, `judge_cache.py`. Outputs: `code/error_taxonomy.py`. Satisfies REQ-2.

6. **Implement high-level `score_trajectory`.** Create `code/score_trajectory.py` with
   `score_trajectory(*, trajectory: Trajectory, environment: EnvironmentSubgoals, judge_model: str = JUDGE_MODEL_DEFAULT, cost_tracker: CostTracker | None = None) -> TrajectoryScore`.
   It calls `compute_progress_rate`, then iterates each step calling `classify_error`, then
   assembles a
   `TrajectoryScore(task_success=trajectory.success, progress_rate=..., step_errors=[...], error_distribution=Counter([labels]))`.
   Inputs: `progress_rate.py`, `error_taxonomy.py`, `types.py`. Outputs: `code/score_trajectory.py`.
   Satisfies REQ-3.

7. **Build FrontierScience-Olympiad subgoal JSON.** Read t0012's
   `tasks/t0012_*/assets/predictions/phase2-smoke-c/files/predictions-frontierscience-olympiad.jsonl`
   and the FrontierScience-Olympiad task descriptions; for each unique `instance_id`, write a
   subgoal list of 3-5 entries describing intermediate problem-solving milestones. File:
   `tasks/t0022_*/assets/library/abc_harness_metrics/files/subgoals_frontierscience_olympiad.json`.
   Schema: `{"environment_id": "...", "subgoals": [{"id": "g1", "description": "..."}, ...]}`.
   Inputs: t0012 predictions JSONL and FrontierScience-Olympiad task data. Outputs: the JSON file.
   Satisfies REQ-5.

8. **Build SWE-bench Verified Lite subgoal JSON.** [CRITICAL] Pull the SWE-bench Verified Lite
   subset metadata via `datasets` (already in `pyproject.toml` deps), pick at least 50 instances,
   and for each, write 1-3 subgoals derived from the gold-patch file paths. Heuristic: subgoal
   description = "Edit a file at `<path>`" for each unique file in the gold patch. File:
   `tasks/t0022_*/assets/library/abc_harness_metrics/files/subgoals_swebench_verified_lite.json`,
   same schema as Step 7. Validation gate: assert `len(subgoals) >= 50`. Inputs:
   `princeton-nlp/SWE-bench_Verified` HuggingFace dataset. Outputs: the JSON file. Satisfies REQ-6.

9. **Write unit tests.** Create:

   * `code/test_progress_rate.py` — synthetic trajectory hits 0/2 subgoals → 0.0; hits 2/2 → 1.0
     (judge mocked via monkey-patch of `_invoke_cli`).
   * `code/test_error_taxonomy.py` — for each of the 7 labels, hand-craft a step + mocked judge
     response and assert the parser returns that label.
   * `code/test_score_trajectory.py` — load one known-good t0012 row, mock judge, assert
     `score_trajectory` returns a valid `TrajectoryScore` without raising and that
     `error_distribution` is a `Counter`.
   * `code/test_judge_cache.py` — round-trip put/get; second `cache_get` with the same key returns
     the cached value.

   Run with `uv run pytest -p tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code -v`.
   Expected: all pass, 0 failures. Satisfies REQ-8.

10. **t0012 replay validation.** [CRITICAL] Create `code/replay_t0012.py` that:

    1. loads all three smoke-A/B/C prediction JSONLs;
    2. runs `score_trajectory` on each row using the FrontierScience-Olympiad subgoal JSON;
    3. emits a per-condition JSON summary (mean progress rate, stddev, error-label histogram) into
       `code/replay_summary.json`;
    4. computes A-vs-C separation rate as the fraction of paired (step-index-matched) steps where
       the predicted error label differs and includes it in `code/replay_summary.json`;
    5. asserts `cost_tracker.total_usd <= 2.00` after the full run; aborts otherwise.

    Validation gate (preflight): run with `--limit 3 --condition c` first; trivial baseline is
    progress_rate ~= 0 (since smoke C scored 0% on binary success); if the limit-3 run produces
    progress_rate == 0 across all rows, halt and inspect raw judge output before scaling. Use cached
    judge calls so the limit-3 preflight is free on the full run. Inputs: t0012 prediction JSONLs,
    all library code, FrontierScience subgoal JSON. Outputs: `code/replay_summary.json` (with
    `progress_rate_mean`, `progress_rate_stddev`, `a_vs_c_separation_rate`, plus per-condition
    stats), updated `code/_cache/`. The orchestrator's analysis step then renders these into
    `results/`. Satisfies REQ-9, REQ-11, REQ-12, REQ-13.

11. **Build the library asset.** Create:

    * `assets/library/abc_harness_metrics/details.json` (spec_version 2, library_id
      `abc_harness_metrics`, module_paths covering all `code/*.py` files except tests and
      `replay_t0012.py`, entry_points listing the three public functions plus the `TrajectoryScore`
      dataclass and `ErrorTaxonomyLabel` enum; categories as registered in `meta/categories/`).
    * `assets/library/abc_harness_metrics/description.md` with all 7 mandatory sections (Metadata,
      Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary).
    * Move the two subgoal JSONs from Steps 7 and 8 under
      `assets/library/abc_harness_metrics/files/` (note: spec says no `files/` directory for *code*
      — but data files are allowed there per `task_description.md` "Subgoal definitions ... live in
      a JSON side-file in the library asset's `files/` directory").

    Run
    `uv run python -m arf.scripts.verificators.verify_library_asset t0022_abc_harness_progress_rate_and_error_taxonomy abc_harness_metrics`.
    Expected: zero errors, zero warnings. Satisfies REQ-10.

## Remote Machines

None required. All compute is local: judge calls run via the `claude` CLI (no remote GPU). No
`setup-machines` step.

## Assets Needed

* **Input**: t0012 prediction JSONLs at
  `tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-{a,b,c}/files/predictions-frontierscience-olympiad.jsonl`
  (already in repo).
* **Input**: SWE-bench Verified Lite metadata via the `datasets` HF library (downloaded on demand;
  already in `pyproject.toml`).
* **Input**: t0017 paper summaries for Ma2024 (`10.48550_arXiv.2401.13178`) and Li2024
  (`10.48550_arXiv.2410.07166`) for prompt-schema attribution (already in repo).
* **Input**: t0012 `code/model_call.py` for CLI invocation pattern (copied, not imported).

## Expected Assets

* **library**: `assets/library/abc_harness_metrics/` containing `details.json`, `description.md`,
  and `files/subgoals_frontierscience_olympiad.json` plus
  `files/subgoals_swebench_verified_lite.json`. This is the single deliverable matching `task.json`
  `expected_assets.library = 1`. Categories expected: `library`, `evaluation`, `agents` (validate
  against `meta/categories/`).

## Time Estimation

* Research (already complete): ~10 min.
* Planning (this step): ~10 min.
* Implementation (Steps 1-9): ~30 min coding + ~5 min unit-test debug.
* Replay validation (Step 10): ~15-25 min wall clock for ~720 cached/uncached judge calls.
* Library asset packaging (Step 11): ~10 min.
* Results, suggestions, reporting: ~15 min.
* Total: ~90-120 min wall clock.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Local `claude` CLI throttles or returns malformed output during 720-call replay | Medium | Replay incomplete | Disk cache on every call so retries are free; on parse failure default to `precondition_or_effect`; Step 10 preflight `--limit 3` catches systemic failures before scaling. |
| Progress rate distribution is degenerate (mean <= 0.05 OR stddev <= 0.03) | Medium | Decision criteria fails | Document exactly which criterion failed in `results_detailed.md`; emit a follow-up suggestion to retry with finer-grained subgoals; do not silently relax the threshold. |
| A-vs-C error-label separation rate < 30% | Medium | Decision criteria fails | Same as above — document, emit suggestion, do not relax. Add a sub-table with per-label disagreement rates so t0023 can pick a tighter subgoal list. |
| SWE-bench Verified HF download fails or licensing blocks the script | Low | Step 8 incomplete | Fall back to a hand-curated 50-instance JSON drafted from the SWE-bench Verified Lite GitHub README; record the fallback in `results_detailed.md`. |
| Judge cost approaches $2 cap before replay finishes | Low | Aborted run, partial signal | Hard `MAX_BUDGET_USD = 2.00` check inside `CostTracker.record`; on cap-hit the script aborts cleanly and writes partial results plus a budget-exhausted intervention file. |
| Subgoal JSON judge prompts leak FrontierScience-Olympiad task content (potential prompt injection) | Low | Inflated progress rates | Use the t0012 vetted prompts; do not pass full task descriptions to the judge — only the subgoal description and the trajectory step. |
| Unit tests pass but replay raises on a real t0012 row | Low | Implementation bug | Step 9 includes a known-good t0012 row test that uses real input shapes (mocked judge), catching schema mismatches before Step 10. |

## Verification Criteria

* Run
  `uv run python -m arf.scripts.verificators.verify_library_asset t0022_abc_harness_progress_rate_and_error_taxonomy abc_harness_metrics`
  and confirm zero errors (REQ-10).
* Run `uv run pytest -p tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code -v` and
  confirm all 7+ test cases pass with 0 failures (REQ-1, REQ-2, REQ-3, REQ-7, REQ-8).
* Confirm
  `tasks/t0022_*/assets/library/abc_harness_metrics/files/subgoals_swebench_verified_lite.json` is a
  valid JSON list with `len >= 50` via
  `uv run python -c "import json; print(len(json.load(open(...))))"` (REQ-6).
* Confirm `results/results_detailed.md` contains a section "Replay Stats" with a per-condition table
  including columns `progress_rate_mean`, `progress_rate_stddev`, and a section "A-vs-C
  Error-Taxonomy Separation" reporting the fraction (REQ-9, REQ-11, REQ-12).
* Confirm `results/metrics.json` contains keys `progress_rate_mean`, `progress_rate_stddev`,
  `a_vs_c_separation_rate` and that the values satisfy the decision criteria or that
  `results_detailed.md` explicitly documents the failure (REQ-11, REQ-12).
* Confirm `results/costs.json` `total_usd <= 2.00` (REQ-13).
* Run `uv run mypy -p tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code` and confirm
  zero errors.
