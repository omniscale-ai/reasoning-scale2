---
spec_version: "2"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
date_completed: "2026-05-02"
status: "complete"
---
# Plan: Phase 2 A/B/C Runtime (N=147) for RQ1-RQ5

## Objective

Produce project-internal runtime evidence answering RQ1-RQ5 by running three paired agent variants
(A: scope-aware ReAct, B: Plan-and-Solve v2, C: mismatched-scope) on the same N=147 instances drawn
from SWE-bench Verified (20), Tau-bench (87), and FrontierScience-Olympiad (40). Done means three
predictions assets exist, paired McNemar p-values for `A>B` and `B>C` are computed at Bonferroni
alpha=0.025, ECE on `final_confidence` is reported, sonnet-vs-programmatic judge agreement is
measured, and the strict double inequality `success(A) > success(B) > success(C)` is either affirmed
or refuted with a project-internal number.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md`:

```text
Run A (scope-aware ReAct) / B (Plan-and-Solve v2) / C (mismatched-scope) on 20 SWE-bench + 87
Tau-bench + 40 FrontierScience instances to answer RQ1-RQ5. Three variants on the SAME 147
instances (paired). Model under test: claude-sonnet-4-6. Judge: claude-sonnet-4-6 primary on every
instance + claude-opus-4-7 on a 30-instance overlap slice (10 per benchmark). NO haiku judge.
Compute success_rate, progress_rate (SWE-bench only), eai_error_breakdown, final_confidence ECE
(10-bin), judge_agreement_with_program, inter_judge_agreement, paired McNemar p_a_vs_b and
p_b_vs_c at Bonferroni alpha=0.025, plus efficiency. Total budget envelope ~$135, hard cap $145.
Shrink SWE-bench first if cap will be breached.
```

* **REQ-1**: Build a paired N=147 instance manifest from the three t0003 JSONL subsets with
  reproducible seed and per-source hashes. Satisfied by Step 1; evidence:
  `data/instance_manifest.json` exists with 20+87+40 IDs and a `seed` field.
* **REQ-2**: Run variant A (scope-aware ReAct) on every one of those 147 instances using
  `claude-sonnet-4-6`. Satisfied by Steps 4 and 6; evidence:
  `assets/predictions/a_scope_aware/predictions.jsonl` has 147 rows.
* **REQ-3**: Run variant B (Plan-and-Solve v2) on the same 147 instances and capture
  `final_confidence`. Satisfied by Steps 4 and 6; evidence:
  `assets/predictions/b_plan_and_solve/predictions.jsonl` has 147 rows with non-null
  `final_confidence` on >=140 of them.
* **REQ-4**: Run variant C (mismatched-scope) on the same 147 instances using the adversarial
  strategy. Satisfied by Steps 4 and 6; evidence:
  `assets/predictions/c_mismatched/predictions.jsonl` has 147 rows.
* **REQ-5**: Judge every (variant, instance) outcome with `claude-sonnet-4-6` and re-judge a
  30-instance overlap (10 per benchmark) with `claude-opus-4-7`. NO haiku judge anywhere. Satisfied
  by Step 5; evidence: `data/judges/sonnet/` has 441 records (3×147) and `data/judges/opus_overlap/`
  has 90 records (3×30).
* **REQ-6**: Compute paired McNemar p-values for `success(A)>success(B)` and `success(B)>success(C)`
  at Bonferroni alpha=0.025. Satisfied by Step 7; evidence: `data/mcnemar_results.json` includes
  `p_a_vs_b`, `p_b_vs_c`, and a `bonferroni_alpha` field.
* **REQ-7**: Compute 10-bin ECE on variant-B `final_confidence` against per-instance outcomes.
  Satisfied by Step 7; evidence: `data/calibration.json` has `ece_10bin` and the 10 bin records.
* **REQ-8**: Report sonnet-judge vs programmatic-truth agreement (SWE-bench tests + FrontierScience
  exact-match) and inter-judge sonnet-vs-opus agreement on the 30-instance slice. Satisfied by Step
  7; evidence: `data/judge_agreement.json` has `agreement_with_program` and `inter_judge_agreement`
  keys.
* **REQ-9**: Decide RQ5 (strict double inequality) on both McNemar tests reaching alpha=0.025.
  Satisfied by Step 7; evidence: `data/mcnemar_results.json` includes a boolean
  `rq5_strict_inequality_supported` field.
* **REQ-10**: Stay at or under the $145 hard cap; reestimate after the first 5 paired instances per
  subset and shrink SWE-bench first if the projection overshoots. Satisfied by Step 3 (validation
  gate) and Step 6; evidence: `data/cost_reestimate.json` and the final `results/costs.json` total
  is `<= 145`.
* **REQ-11**: Produce three predictions assets and the standard results bundle. Satisfied by Steps 6
  and 8; evidence: three `assets/predictions/<variant>/details.json` files plus
  `results/results_summary.md`, `results_detailed.md`, `metrics.json`, `images/*.png`.

## Approach

The approach is a paired-design A/B/C runtime built on top of three already-extracted libraries
(`scope_aware_react_v1`, `scope_unaware_planandsolve_v2`, `matched_mismatch_v1`) plus the
`abc_harness_metrics` library for progress rate and the EAI error taxonomy. Each variant accepts an
injected `model_call: Callable[[str], str]`; t0026 supplies a single Anthropic shim that wraps
`claude-sonnet-4-6` with retry-with-exponential-backoff and a per-call cost tally. Variant B emits
`final_confidence` natively (no extra elicitation prompt); variants A and C reuse the same field
convention as documented in research_code.md. The judge is implemented inline in `code/judge.py`
because t0019 did not extract a reusable judge library — but it reuses t0019's substantive-critic
prompt for SWE-bench/FrontierScience and the model-rotated prompt for Tau-bench. ECE is implemented
inline as a 10-equal-width-bin computation because `t0011_metric2_calibration_aggregator` exposes
only `overconfident_error_rate`. Paired McNemar is a sub-50-line stdlib `scipy.stats`-free
implementation.

**Alternatives considered**: (1) Sample-with-replacement bootstrap for RQ1/RQ2 instead of McNemar.
Rejected: McNemar is the canonical paired binary test, has higher power at this N, and is already
the metric specified in `task.json`. (2) Run a haiku judge as a third inter-judge point. Rejected:
t0019 explicitly disqualified haiku at this scale (+58pp gap) — using it would invalidate RQ3. (3)
Sample 147 instances entirely from SWE-bench. Rejected: cross-benchmark coverage is essential for
the generalisation claim under RQ1.

**Task types** (from `task.json`): `experiment-run`, `comparative-analysis`. The Planning Guidelines
for `comparative-analysis` push us toward the paired design (same instances, different variants) and
toward explicit pairwise hypothesis tests with multiple-comparison correction; we adopt both.

## Cost Estimation

Per-variant cost estimate (sonnet 4.6 agent + sonnet 4.6 judge), grounded in t0012's smoke-run unit
costs:

* SWE-bench: 20 instances × $0.85 = $17.00 per variant
* Tau-bench: 87 instances × $0.20 = $17.40 per variant
* FrontierScience: 40 instances × $0.18 = $7.20 per variant
* Per-variant subtotal: $41.60
* Three variants: $124.80
* Inter-judge slice (opus 4.7 on 30 items × ~$0.17): $5.10
* Buffer for retries / parse-failure replays: $5.00

**Estimated total**: $135 — fits inside the project budget left ($125.92) only with the buffer spent
and within the project hard cap of $145 with $10 of headroom. Step 3 mandates a real prompt-token
reestimation on the first 5 paired instances per subset; if the projection overshoots $145, the
SWE-bench slice (largest cost share) is shrunk before any other action. Project budget status: total
$200, spent $74.08, left $125.92 — enough at the estimate but not at the hard cap; the validation
gate is the hedge.

## Step by Step

1. **Build the instance manifest.** Write `code/instance_loader.py` (~30 LOC) reading the three
   t0003 JSONL files
   (`tasks/t0003_download_benchmark_subsets/assets/dataset/{swebench-verified,taubench,frontierscience-olympiad}-subset/files/*.jsonl`),
   stratified-sampling 20 from SWE-bench by difficulty bucket with `seed=20260502` and taking all 87
   \+ 40 from the other two. Write `data/instance_manifest.json` with per-source IDs, sha256 of each
   source file, and the seed. Expected: file exists with `len(instances) == 147`. Satisfies REQ-1.

2. **Wire the model-call and tool registries.** Write `code/anthropic_shim.py` (~80 LOC)
   implementing `make_model_call(model_id: str, cost_tracker: CostTracker) -> Callable[[str], str]`
   with exponential backoff (5 retries, 2-32s) and per-call usage accounting via the Anthropic SDK
   `usage` field. Reuse the `tool_registry` patterns from t0012's smoke harness — a thin dispatch
   over `read_file`, `write_file`, `run_python`, and SWE-bench-specific `apply_patch` / `run_tests`.
   Expected: a unit smoke test in `code/test_anthropic_shim.py` calls `claude-sonnet-4-6` once with
   a 50-token prompt and observes a non-empty response and a non-zero cost. Satisfies
   REQ-2/REQ-3/REQ-4 (shared infrastructure).

3. **[CRITICAL] Validation gate: 5-instance preflight per subset.** Run `code/main.py --preflight`
   which executes 5 paired instances per subset (15 instances × 3 variants = 45 runs) using the real
   shim and judge but writes to `data/preflight/`. Trivial baseline: cost-per-instance measured on
   these 15 should agree with the t0012 smoke numbers within ±25%. Failure condition: if the
   projected total for N=147 × 3 + judge + buffer exceeds $145, halt and execute the
   SWE-bench-shrink fallback (drop SWE-bench from 20 to 12 first; if still over cap, drop to 8).
   Inspect at least 3 individual trajectories across variants for parse failures or premature
   termination. Expected: `data/cost_reestimate.json` and a printed projection. Satisfies REQ-10.

4. **Implement the per-variant runner.** Write `code/runner.py` (~200 LOC) exposing
   `run_variant(variant: Literal["a", "b", "c"], manifest: InstanceManifest, model_call, tool_registry, output_dir: Path) -> VariantRunSummary`.
   Variant A imports
   `from tasks.t0006_scope_aware_react_library.code.scope_aware_react import ScopeAwareReactAgent`
   and constructs
   `ScopeAwareReactAgent(problem, granularity, tool_registry, model_call, trajectory_path, max_turns=20)`.
   Variant B imports
   `from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import PlanAndSolveAgentV2`
   and constructs `PlanAndSolveAgentV2(model_call, tool_registry, max_steps=32)`. Variant C imports
   `from tasks.t0010_matched_mismatch_library.code.matched_mismatch import MatchedMismatchAgent`
   with `delegate="scope_aware_react"`, `mismatch_strategy="adversarial"`, `seed=0`. Per-instance
   results are appended to `data/runs/<variant>/trajectory_<instance_id>.json`. Expected: dry-run on
   1 instance per variant emits 3 trajectory files. Satisfies REQ-2/REQ-3/REQ-4.

5. **Implement the judge.** Write `code/judge.py` (~150 LOC) with two prompt templates copied from
   the t0019 codebase and adapted: the substantive-critic prompt for SWE-bench / FrontierScience
   (programmatic-truth-aware) and the model-rotated prompt for Tau-bench. Public:
   `judge_outcome(instance, prediction, model_id="claude-sonnet-4-6") -> JudgeResult(success: bool, rationale: str, cost: float)`
   and
   `run_inter_judge_slice(predictions, n_per_subset=10, model_id="claude-opus-4-7") -> InterJudgeResults`.
   NO haiku judge — assert that `model_id != "claude-haiku-4-5"` at the top of `judge_outcome`.
   Per-judge records go to `data/judges/<judge_id>/<variant>/<instance_id>.json`. Expected: a
   1-instance dry-run produces one JSON record per variant with `success` ∈ {true, false}. Satisfies
   REQ-5.

6. **Run the full N=147 × 3 sweep.** Execute `code/main.py --full` which calls `run_variant` three
   times then runs the judge on every (variant, instance) pair plus the 30-instance opus overlap.
   Write progress to stdout every 10 instances. After completion, write predictions assets at
   `assets/predictions/{a_scope_aware,b_plan_and_solve,c_mismatched}/predictions.jsonl` and
   accompanying `details.json`. Expected: three predictions assets exist, each with 147 rows
   carrying `instance_id`, `variant`, `final_answer`, `final_confidence` (variant B only),
   `success_program` (where program-truth exists), `success_judge`, `cost_usd`. Satisfies
   REQ-2/REQ-3/REQ-4/REQ-5/REQ-11.

7. **Compute metrics.** Write `code/calibration.py` (~80 LOC) with
   `compute_ece_10bin(confidences, outcomes) -> ECEResult(ece, bins)`. Write `code/mcnemar.py` (~50
   LOC) with `mcnemar_paired(b: int, c: int) -> McNemarResult(statistic, p_value)` using the exact
   binomial in the small-n branch and the chi-squared continuity-corrected formula otherwise. Write
   `code/metrics.py` (~150 LOC) orchestrating: success_rate per (variant, subset), progress_rate via
   `compute_progress_rate(...)` from
   `tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.progress_rate` on SWE-bench only,
   EAI error breakdown via `classify_error(...)` on all subsets, sonnet-vs-program agreement on
   items with program truth, sonnet-vs-opus on the overlap slice, ECE on variant B, and the two
   McNemar p-values. Outputs: `data/{calibration,mcnemar_results,judge_agreement}.json` and
   `results/metrics.json`. Compute
   `rq5_strict_inequality_supported = (p_a_vs_b < 0.025) and (p_b_vs_c < 0.025) and (success_rate_a > success_rate_b > success_rate_c)`.
   Satisfies REQ-6/REQ-7/REQ-8/REQ-9.

8. **Generate plots.** Write `code/plots.py` (~120 LOC) producing
   `results/images/{success_rate_by_variant, success_rate_by_benchmark, ece_reliability_diagram, judge_agreement, eai_error_breakdown}.png`
   using matplotlib. Each plot's axis labels and title state the underlying metric and N. Expected:
   five PNG files exist, each ≥ 30 KB. Satisfies REQ-11.

## Remote Machines

None required. All work runs locally calling the Anthropic API. No GPU, no vast.ai, no remote worker
— this is a pure inference workload bounded by API rate limits, which the shim handles.

## Assets Needed

* **Datasets** (from `t0003_download_benchmark_subsets`): `swebench-verified-subset.jsonl` (60
  rows), `taubench-subset.jsonl` (87 rows), `frontierscience-olympiad-subset.jsonl` (40 rows).
* **Libraries** (from prior tasks, imported via the registered library paths):
  `scope_aware_react_v1` (t0006), `scope_unaware_planandsolve_v2` (t0021), `matched_mismatch_v1`
  (t0010), `abc_harness_metrics` (t0022), `metric2_calibration_aggregator_v1` (t0011, used as a
  sanity-check beside the inline ECE), `phase2_smoke_harness_v1` (t0012, referenced for
  tool-registry patterns).
* **Project secret**: `ANTHROPIC_API_KEY` from the local environment (already present).

## Expected Assets

Three predictions assets — one per variant — each with `assets/predictions/<asset_id>/details.json`
plus `assets/predictions/<asset_id>/predictions.jsonl`:

* `a_scope_aware` — 147 per-instance rows for variant A
* `b_plan_and_solve` — 147 per-instance rows for variant B (carries `final_confidence`)
* `c_mismatched` — 147 per-instance rows for variant C

Plus the standard results bundle (results_summary.md, results_detailed.md, metrics.json,
suggestions.json, costs.json, images/*.png) — produced by orchestrator steps 12-15, not by
implementation.

## Time Estimation

* Implementation + unit smoke tests: ~3-4 hours
* Preflight gate (15 instances × 3 variants): ~25 minutes wall-clock
* Full sweep (147 × 3 = 441 runs + 441 judge calls + 90 opus inter-judge calls): ~3-4 hours
  wall-clock (limited by Anthropic rate limits, not compute)
* Metric computation, plotting, results writeup (across analysis + reporting steps): ~2 hours

Total wall-clock from prestep planning through merged PR: ~10 hours.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Cost overrun past $145 hard cap | Medium | Blocking | Step 3 validation gate reestimates from real preflight tokens; SWE-bench shrunk first if projection exceeds cap (REQ-10) |
| Anthropic API rate limit / 429 | Medium | Delays | Exponential backoff in `code/anthropic_shim.py` (5 retries, 2-32s); spread sweep across multiple sessions if rate-limit budget is exhausted |
| Variant B `final_confidence` parse failures inflate >5% | Low | RQ4 signal degraded | t0021's parser already retries once; runner counts parse failures and the implementation flags any subset with >5% failures for re-run with stricter prompt |
| SWE-bench `apply_patch` / `run_tests` infrastructure breaks | Low | Variant-A signal lost on SWE | Each instance has an isolated workspace; on tool failure, mark `success_program=false` and continue, do not abort the sweep |
| Sonnet judge agrees with programmatic truth at <80% | Medium | RQ3 reports unreliability | This is an outcome, not a failure — report it transparently; do not retry with a different judge |
| Strict RQ5 inequality refuted | Medium | RQ5 directional only | Documented as a possible outcome in the task description's falsifiability list; report direction-only and explain |
| Implementation regression breaks paired-design invariant | Low | Wrong McNemar p-values | Manifest pinned in `data/instance_manifest.json` with sha256s; runner asserts the same instance set across variants before accepting the run |

Pre-mortem framing: the most likely "this run failed" scenarios are (a) cost overrun caught after
the fact rather than during preflight, (b) parse failures on variant B silently degrading ECE, and
(c) a tooling regression in the SWE-bench infrastructure. The Step 3 validation gate, parse- failure
counters, and per-instance success_program/judge dual-logging address each respectively.

## Verification Criteria

* `data/instance_manifest.json` exists with exactly 147 instances and a `seed` field — confirm with
  `uv run python -c "import json; d = json.load(open('data/instance_manifest.json')); assert len(d['instances']) == 147 and 'seed' in d"`.
  Confirms REQ-1.
* Three predictions assets verify cleanly — confirm with
  `uv run python -u -m arf.scripts.verificators.verify_predictions_asset a_scope_aware --task-id t0026_phase2_abc_runtime_n147_for_rq1_rq5`
  (and analogous for the other two); expected: zero errors. Confirms REQ-2/REQ-3/REQ-4/REQ-11.
* `data/mcnemar_results.json` contains numeric `p_a_vs_b`, `p_b_vs_c`, `bonferroni_alpha == 0.025`,
  and a boolean `rq5_strict_inequality_supported` — confirm with
  `uv run python -c "import json; r = json.load(open('data/mcnemar_results.json')); assert all(k in r for k in ['p_a_vs_b', 'p_b_vs_c', 'bonferroni_alpha', 'rq5_strict_inequality_supported'])"`.
  Confirms REQ-6/REQ-9.
* `data/calibration.json` reports `ece_10bin` as a float in [0, 1] and 10 `bins` records — confirm
  with
  `uv run python -c "import json; d = json.load(open('data/calibration.json')); assert 0 <= d['ece_10bin'] <= 1 and len(d['bins']) == 10"`.
  Confirms REQ-7.
* `data/judge_agreement.json` carries `agreement_with_program` (float in [0, 1]) and
  `inter_judge_agreement` (float in [0, 1] over the 30-instance slice). Confirms REQ-8.
* `results/metrics.json` registers every metric key listed in the task description and every metric
  key resolves against `meta/metrics/` — confirm with
  `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format json` and a follow-up
  Python check that the metrics from `results/metrics.json` are a subset of the registered keys.
  Confirms REQ-11.
* `results/costs.json` `total_cost_usd` is at most 145.00 — confirm with
  `uv run python -c "import json; assert json.load(open('results/costs.json'))['total_cost_usd'] <= 145.00"`.
  Confirms REQ-10.
