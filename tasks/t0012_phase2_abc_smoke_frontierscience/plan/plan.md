---
spec_version: "2"
task_id: "t0012_phase2_abc_smoke_frontierscience"
date_completed: "2026-04-30"
status: "complete"
---
# Plan: Phase 2 A/B/C Smoke Harness on FrontierScience-Olympiad

## Objective

Run the project's first end-to-end Phase 2 A/B/C comparison on the FrontierScience-Olympiad subset
of the t0009 v2 hierarchical-annotation dataset. Produce three predictions assets (one per
condition: A scope-aware ReAct, B scope-unaware Plan-and-Solve, C scope-mismatched), one harness
library asset, and a `results/metrics.json` in explicit-variant format with the three registered
metrics (`task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`) per condition.
"Done" means: all four asset verificators pass, paired McNemar p-values are reported for A-vs-B and
B-vs-C, observed effects are reported against the pre-registered hypotheses (RQ1, RQ2, RQ5), the
implied confirmatory N for a 5pp effect is computed, and the total cumulative API spend is at or
below the **USD 20** budget cap.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md`:

> **Phase 2 A/B/C smoke harness on FrontierScience subset** — First end-to-end Phase 2 A/B/C run on
> the FrontierScience subset of the v2 dataset; N=28 paired across conditions, single provider
> Anthropic. Test the headline hypothesis: scope-aware (A) > scope-unaware (B) > scope-mismatched
> (C). Smoke test → directional signal plus sample-size calibration for follow-up confirmatory runs.
> Expected assets: 3 predictions, 1 library. Source suggestion: S-0006-03 (also covers S-0007-02 and
> S-0005-06).

Concrete requirements:

* **REQ-1**: Build a `phase2_smoke_harness_v1` library that loads the v2 dataset, filters to
  FrontierScience-Olympiad complete rows, runs all three conditions paired per row, captures every
  trajectory record into a per-condition JSONL, and computes the three registered metrics. Satisfied
  by Steps 1-7.
* **REQ-2**: Produce three predictions assets: `phase2_smoke_a` (A), `phase2_smoke_b` (B),
  `phase2_smoke_c` (C). Each must pass `verify_predictions_asset.py`,
  `verify_predictions_description.py`, and `verify_predictions_details.py`. Satisfied by Step 8.
* **REQ-3**: Produce one library asset `phase2_smoke_harness_v1` that passes
  `verify_library_asset.py`. Satisfied by Step 7.
* **REQ-4**: `results/metrics.json` must use the explicit-variant format with three variants
  (`condition_a_scope_aware`, `condition_b_scope_unaware`, `condition_c_scope_mismatched`), each
  carrying `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`. Satisfied by
  Step 9.
* **REQ-5**: At least 2 charts in `results/images/` (condition × metric bar chart with CIs; per-row
  success-matrix heatmap), embedded in `results_detailed.md`. Satisfied by Step 9.
* **REQ-6**: Pair runs by `task_id` so paired statistical tests (paired McNemar / sign test) are
  valid. Same model, same temperature, same problem text per row across conditions. Satisfied by
  Step 5.
* **REQ-7**: Total cost ≤ **USD 20**. After each variant run, check cumulative cost vs the cap; halt
  remaining variants if exceeded and document overrun in `results/costs.json` `note` field.
  Satisfied by Steps 5-6 and Step 9.
* **REQ-8**: Pre-register predictions per RQ1, RQ2, RQ5 (predicted directions and detection
  thresholds) before running. Report observed effects, paired McNemar p-values, 95% CI, implied
  confirmatory N. Satisfied by Step 4 (pre-registration), Step 9 (post-run analysis), and the
  results files written in the orchestrator's `results` step.

## Approach

The harness is a thin orchestrator. All four sister libraries (t0006 ReAct, t0007 Plan-and-Solve,
t0010 matched-mismatch, t0011 calibration aggregator) are imported via library — no code is copied
or reimplemented. The harness owns: (a) a small `model_call.py` Anthropic SDK wrapper that enforces
a per-task cost ceiling and returns the raw text, (b) a tool registry with one `python_exec` tool
plus an implicit `Finish(answer)` action, (c) the dataset loader that reads the v2 JSONL and filters
to FrontierScience-Olympiad complete rows, (d) the per-row condition-dispatcher that calls
`ScopeAwareReactAgent` (A), `PlanAndSolveAgent` (B), and `MatchedMismatchAgent` (C with
`delegate="scope_unaware_planandsolve"`, `mismatch_strategy="random"`, `seed=42`), and (e) the
metric computation that calls `compute_overconfident_error_rate` from t0011 plus a Haiku-as-judge
correctness check.

**Alternative considered**: running self-consistency for the confidence elicitation (3 calls per
final action, ~120 extra calls). Rejected because the smoke run prioritizes within-budget
directional signal over Brier-score precision, and t0006 already produces numeric confidence inline
so most A trajectories yield confidence without a second round-trip. We document the simplification
and queue a confirmatory run with full self-consistency as a follow-up suggestion.

**Task types**: This task is `experiment-run` + `baseline-evaluation` (per `task.json`). The
`experiment-run` instructions emphasize per-condition variants, cost tracking, charts ≥ 2, and
predictions assets — all reflected in REQ-2/4/5/7. The `baseline-evaluation` instructions emphasize
a comparison table against published numbers — handled in the orchestrator's `compare-literature`
step using the ReAct/Plan-and-Solve published gain bands cited in `research/research_papers.md`.

## Cost Estimation

**Budget cap: USD 20** (per-task default $10; this task explicitly opts up — confirmed in
`task_description.md` § Compute and Budget). Project total budget is $100 with $90.84 remaining
before this task.

Per-call cost estimates (Anthropic, March 2026 pricing):

* `claude-sonnet-4-6-20251001` agent calls: $3 / $15 per million input/output tokens.
* `claude-haiku-4-5-20251001` judge calls: $0.80 / $4 per million input/output tokens.

| Component | Calls | Avg input tokens | Avg output tokens | Per-call cost | Subtotal |
| --- | --- | --- | --- | --- | --- |
| Condition A (Sonnet, 40 rows × ~6 turns) | 240 | 4,000 | 800 | $0.024 | $5.76 |
| Condition B (Sonnet, 40 rows × 1 plan + ~5 exec) | 240 | 3,000 | 600 | $0.018 | $4.32 |
| Condition C (Sonnet, 40 rows × ~6 phases) | 240 | 3,500 | 700 | $0.021 | $5.04 |
| Judge (Haiku, 40 rows × 3 conditions) | 120 | 5,000 | 50 | $0.0042 | $0.50 |
| Confidence elicitation (Haiku, ~50 fill-ins) | 50 | 2,000 | 30 | $0.0017 | $0.09 |
| **Estimated total** |  |  |  |  | **$15.71** |

**Headroom**: ~$4.30 (~22%) for retries, longer trajectories than expected, and the self-consistency
calls if the budget allows. The harness MUST check cumulative spend after each condition's run
completes and halt if it exceeds **USD 20**.

## Step by Step

1. **Create `code/paths.py` and `code/constants.py`.** `paths.py` centralizes:
   `V2_DATASET_PATH = Path("tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl")`,
   `PREDICTIONS_A_DIR`, `PREDICTIONS_B_DIR`, `PREDICTIONS_C_DIR` (each pointing into
   `assets/predictions/phase2_smoke_{a,b,c}/files/`), and `RESULTS_DIR`. `constants.py` defines:
   `BENCHMARK_FILTER = "FrontierScience-Olympiad"`, `MODEL_AGENT = "claude-sonnet-4-6-20251001"`,
   `MODEL_JUDGE = "claude-haiku-4-5-20251001"`, `BUDGET_CAP_USD = 20.0`,
   `HIGH_CONFIDENCE_THRESHOLD = 0.75`, `MAX_TURNS = 12`, `RANDOM_SEED = 42`. Satisfies REQ-1.

2. **Create `code/tools.py`.** Implements `python_exec(code: str) -> str` that runs Python in a
   `subprocess.run` sandbox with a 5-second timeout and 64 KB output cap. Returns stdout
   concatenated with stderr or a structured error message. Wraps the same callable into two shapes:
   `react_tool_registry: dict[str, Callable[..., Any]]` (called with kwargs by t0006 ReAct) and
   `plansolve_tool_registry: dict[str, Callable[[str], str]]` (called with single string arg by
   t0007 Plan-and-Solve and t0010). Satisfies REQ-1.

3. **Create `code/model_call.py`.** Implements
   `make_anthropic_call(model: str, system: str | None) -> Callable[[str], str]` that returns a
   closure invoking the Anthropic Messages API. The closure tracks input/output tokens and
   accumulates spend in a module-level `CostTracker` dataclass. Provides
   `current_spend_usd() -> float` and `assert_budget_ok(cap: float)`. Uses `anthropic` Python SDK
   (already a project dep). Reads `ANTHROPIC_API_KEY` from env. Satisfies REQ-1, REQ-7.

4. **Create `code/harness.py`.** Implements:
   * `load_smoke_rows() -> list[dict]` — reads V2 JSONL, filters to `BENCHMARK_FILTER` ∧
     `hierarchy_completeness == True`, returns deterministic-ordered list of row dicts (sorted by
     `task_id` for paired serialization, REQ-6).
   * `extract_problem_text(row: dict) -> str` — returns `row["problem"]`.
   * `extract_gold_answer(row: dict) -> str` — concatenates `gold_actions["global"]` plus all
     subtask gold actions; LLM judge will compare candidate against this concatenation.
   * `judge_correctness(*, problem: str, gold: str, candidate: str | None, judge_call: Callable[[str], str]) -> bool`
     — Haiku binary judge with prompt:
     `"Given the problem, the gold derivation, and the candidate answer, decide whether the candidate substantively reproduces the key derivation steps and final result of the gold. Reply with exactly YES or NO."`.
     Returns `False` if `candidate is None` (early termination before Finish). Logs every judge call
     to a JSONL.
   * `count_decisions(trajectory: list[dict]) -> int` — number of trajectory records (one per turn /
     phase).
   * `extract_final_confidence(trajectory: list[dict], final_action: str | None, problem: str, judge_call: Callable[[str], str]) -> float`
     — uses the trajectory's final-turn `confidence` when present and numeric; falls back to a
     single `elicit_confidence` Haiku call from t0011.
   * `run_condition_a(*, row, model_call, tool_registry) -> dict` — runs `ScopeAwareReactAgent` once
     per row with `granularity="global"` (the highest-level scope is the most natural default for
     FrontierScience-Olympiad's open derivation prompts; A's distinguishing feature is that the
     model receives the explicit scope tag, not which scope is used). Trajectory is written to a
     per-row temp path and read back as a list of dicts.
   * `run_condition_b(*, row, model_call, tool_registry) -> dict` — runs `PlanAndSolveAgent`.
   * `run_condition_c(*, row, model_call, tool_registry) -> dict` — runs `MatchedMismatchAgent` with
     `delegate="scope_unaware_planandsolve"`, `mismatch_strategy="random"`, `seed=42`. The full v2
     row is passed as `annotation`.
   * `compute_metrics(trajectory_records: list[dict], judge_results: list[bool], decision_counts: list[int], confidences: list[float]) -> dict[str, float]`
     — returns
     `{"task_success_rate": mean(judge_results), "overconfident_error_rate": compute_overconfident_error_rate(records=...), "avg_decisions_per_task": mean(decision_counts)}`.
     Satisfies REQ-1, REQ-4, REQ-6.

5. **Create `code/run_smoke.py` (CLI entrypoint).** Sequence:
   1. Load smoke rows; assert N matches the expected v2 count and log it.
   2. Pre-register predictions in `plan/predictions.md` (handled by orchestrator before this step
      runs; the script asserts the file exists).
   3. Build `agent_call` (Sonnet) and `judge_call` (Haiku) once.
   4. Build the two tool registries.
   5. For condition in (A, B, C), in order: iterate over rows in deterministic order; per row call
      the matched `run_condition_*`, append the trajectory records (with `extras` stripped) to the
      per-condition JSONL at the predictions-asset path; record final answer, confidence, and
      decision count. After each condition completes, call `assert_budget_ok` and halt if the cap is
      reached. Persist intermediate state to `results/_intermediate_<cond>.json` per condition so a
      partial run can be resumed and so partial results can still be reported.
   6. After all three conditions complete (or are halted), compute metrics per condition and write
      `results/metrics.json`, `results/costs.json`, and the per-condition `details.json` for each
      predictions asset.
   7. **[CRITICAL]** Generate the two charts via `code/charts.py`: `images/condition_metric_bar.png`
      (3 conditions × 3 metrics with 95% Wilson CIs) and `images/per_row_success_heatmap.png` (40
      rows × 3 conditions, green=correct, red=wrong). Use matplotlib only. Satisfies REQ-1, REQ-2,
      REQ-4, REQ-5, REQ-6, REQ-7.

6. **Validation gate before full run.** Before launching the full sweep, run with `--limit 2` (two
   rows × three conditions = 6 runs ≈ $0.30) to verify:
   * the harness produces JSONL files that satisfy the trajectory schema;
   * the judge returns a YES/NO that parses;
   * the metric computation completes;
   * the cost tracker reports a non-zero, plausible spend. Trivial baseline:
     `task_success_rate >= 0` (parser is sound). Failure condition: any of the four checks above
     fail → halt and inspect individual outputs (Anthropic raw response, parsed `Finish` answer,
     judge prompt + reply) before running the full sweep.

7. **Build the `phase2_smoke_harness_v1` library asset.** Write
   `assets/library/phase2_smoke_harness_v1/details.json` pointing to all five `code/*.py` files;
   write `description.md` with the seven mandatory sections (Metadata, Overview, API, Internals,
   Limitations, Main Ideas, Summary). Run `verify_library_asset.py`. Satisfies REQ-3.

8. **Build the three predictions assets.** For each condition, write
   `assets/predictions/phase2_smoke_{a,b,c}/details.json` and `description.md` referencing the
   per-condition trajectory JSONL produced in Step 5. Categories: `granularity-conditioning`,
   `agent-evaluation`, `benchmark-frontierscience`, plus `hierarchical-planning` (A and C) or
   `uncertainty-calibration` (all three). Run `verify_predictions_asset.py`,
   `verify_predictions_description.py`, `verify_predictions_details.py` per asset. Satisfies REQ-2.

9. **Compute headline statistics and write metrics.** Compute observed A−B, B−C, A−C deltas on
   `task_success_rate` and `overconfident_error_rate`; the paired McNemar (or exact binomial sign
   test for ≤ 25 discordant pairs) p-value for each pair; Wilson 95% CIs for each variant rate; the
   implied confirmatory N for a 5pp effect at α=0.05/0.8 power per the rule of thumb in the task
   description. Persist these in `results/_intermediate_stats.json` so the orchestrator's `results`
   step can read them when writing `results_detailed.md`. Satisfies REQ-4, REQ-8.

The plan ends at metric computation and chart generation. Results-summary writing, suggestions
generation, and compare-literature are orchestrator steps managed by execute-task.

## Remote Machines

None required. The harness runs locally and only consumes the Anthropic API.

## Assets Needed

* **Dataset (input)**:
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2` — read directly
  from disk, no aggregator call.
* **Library (input)**: `scope_aware_react_v1`, `scope_unaware_planandsolve_v1`,
  `matched_mismatch_v1`, `metric2_calibration_aggregator_v1` — imported via library.
* **External**: Anthropic API access using `ANTHROPIC_API_KEY` from `.env`. No other paid service.

## Expected Assets

* `assets/predictions/phase2_smoke_a/` — predictions, condition A scope-aware ReAct.
* `assets/predictions/phase2_smoke_b/` — predictions, condition B scope-unaware Plan-and-Solve.
* `assets/predictions/phase2_smoke_c/` — predictions, condition C scope-mismatched (random).
* `assets/library/phase2_smoke_harness_v1/` — the harness orchestrator library.

This matches `task.json` `expected_assets`: `{"predictions": 3, "library": 1}`.

## Time Estimation

* Implementation (Steps 1-4 + Step 7 + Step 8 docs): ~2 hours.
* Validation gate (Step 6, `--limit 2` run): ~5 minutes including review.
* Full smoke run (Step 5, all conditions): ~30-45 minutes wall clock (rate-limited by Anthropic API
  throughput, ~5-10 calls per second).
* Metric computation + charts (Steps 5.7 + 9): ~10 minutes.
* Total: ~3-4 hours implementation; an additional ~30-60 minutes for the orchestrator's results,
  compare-literature, and suggestions steps after the harness completes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Budget cap reached mid-sweep | Medium | Partial coverage of conditions | Per-condition cost check + halt; partial results written with explicit incompleteness note in `costs.json` `note` field. |
| Anthropic API rate-limit errors | Medium | Run delays, possible truncated trajectories | Exponential backoff with `tenacity` (already a project dep) on 429/5xx; log each retry. |
| Judge produces ambiguous YES/NO output | Medium | Slightly noisy correctness labels | Liberal regex (`^\s*(YES |
| Trajectory schema drift in a sister library | Low | Harness writes malformed JSONL | Module-load-time `assert TRAJECTORY_RECORD_FIELDS == ...` mirroring t0010's pattern. |
| FrontierScience problems exceed Anthropic context window | Low | A small fraction of rows truncated | Truncate problem text to 12 K tokens before sending; record truncation in trajectory `extras`. |
| All-zero `task_success_rate` across conditions | Low | Smoke test cannot discriminate hypotheses | Investigate as a pipeline bug per the experiment-run instructions: read 5 individual judge calls and 5 raw model responses; do not declare "no effect" without confirming the harness is correct. |
| Effect size below detection threshold | High | Hypothesis cannot be confirmed at N=40 | This is the explicit smoke-test outcome — report observed effect, p-value, and the implied confirmatory N as the deliverable, not a failure. |

## Verification Criteria

* `uv run python -m arf.scripts.verificators.verify_task_metrics t0012_phase2_abc_smoke_frontierscience`
  passes with zero errors. Confirms `results/metrics.json` uses the explicit-variant format with the
  three registered metrics per variant. Direct REQ-4 check.
* For each of `phase2_smoke_a`, `phase2_smoke_b`, `phase2_smoke_c`:
  `uv run python -m arf.scripts.verificators.verify_predictions_asset --task-id t0012_phase2_abc_smoke_frontierscience phase2_smoke_X`,
  `verify_predictions_description --task-id t0012_phase2_abc_smoke_frontierscience phase2_smoke_X`,
  `verify_predictions_details --task-id t0012_phase2_abc_smoke_frontierscience phase2_smoke_X` all
  pass. Direct REQ-2 check.
* `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0012_phase2_abc_smoke_frontierscience phase2_smoke_harness_v1`
  passes with zero errors. Direct REQ-3 check.
* `python -c "from pathlib import Path; assert Path('tasks/t0012_phase2_abc_smoke_frontierscience/results/metrics.json').exists() and Path('tasks/t0012_phase2_abc_smoke_frontierscience/results/images/condition_metric_bar.png').exists() and Path('tasks/t0012_phase2_abc_smoke_frontierscience/results/images/per_row_success_heatmap.png').exists()"`
  exits 0. Direct REQ-5 check.
* `python -c "import json; d=json.load(open('tasks/t0012_phase2_abc_smoke_frontierscience/results/costs.json')); assert d['total_cost_usd'] <= 20.0, d"`
  exits 0. Direct REQ-7 check.
* For each predictions JSONL: `wc -l <file>` returns 40 (or fewer with documented incompleteness)
  and every line parses as JSON with the canonical six-field trajectory record schema. Direct REQ-1
  check.
* `results_detailed.md` contains a `## Examples` section with at least 10 concrete input-output
  pairs (problem text + agent's final response per row). Pre-flight check before
  `verify_task_results`.
