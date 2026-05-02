---
spec_version: "1"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 9
libraries_found: 7
libraries_relevant: 6
date_completed: "2026-05-02"
status: "complete"
---
# Research Code

## Task Objective

t0026 produces project-internal runtime evidence for RQ1-RQ5 by running three agent variants (A:
scope-aware ReAct, B: Plan-and-Solve v2, C: mismatched-scope) on a paired N=147 slice that spans 20
SWE-bench Verified instances, 87 Tau-bench instances, and 40 FrontierScience-Olympiad instances.
This research surveys the seven dependency tasks so the planning step can map every component to a
concrete file path, public API, and judge configuration before the run is launched.

## Library Landscape

The library aggregator returns 7 libraries; 6 are directly relevant to t0026 and the seventh
(`scope_unaware_planandsolve_v1` from [t0007]) is transitively used because v2 wraps it.

* `scope_aware_react_v1` — created by [t0006]; current; relevant to variant A; import via library at
  `tasks.t0006_scope_aware_react_library.code.scope_aware_react`.
* `scope_unaware_planandsolve_v1` — created by [t0007]; current; transitively relevant via v2.
* `matched_mismatch_v1` — created by [t0010]; current; relevant to variant C; import via library at
  `tasks.t0010_matched_mismatch_library.code.matched_mismatch`.
* `metric2_calibration_aggregator_v1` — created by [t0011]; current; relevant for the Xiong2024
  overconfident-error-rate sanity check on variant B.
* `phase2_smoke_harness_v1` — created by [t0012]; current; relevant as a reference implementation of
  the per-instance loop pattern (smoke-test scope).
* `scope_unaware_planandsolve_v2` — created by [t0021]; current; relevant to variant B; import via
  library at `tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2`.
* `abc_harness_metrics` — created by [t0022]; current; relevant for AgentBoard subgoal progress rate
  and EAI error taxonomy classification.

The aggregator output is the effective state — no correction overlays exist for any of these
libraries.

## Key Findings

### Variant libraries are stable; ECE is the missing piece

The three variant libraries (A: [t0006], B: [t0021], C: [t0010]) all expose clean public entry
points whose signatures already accept an injected `model_call: Callable[[str], str]`. Wiring
`claude-sonnet-4-6` is a single shim in `code/judge.py`. The one piece of inferential infrastructure
that is *not* available is Expected Calibration Error: [t0011] only exposes
`overconfident_error_rate`. RQ4 demands ECE specifically — t0026 must implement a 10-equal-width-
bin ECE inline against `final_confidence` floats from variant B. This is a small (sub-50-line)
addition with no external dependencies.

### Judge infrastructure is not extracted as a library

[t0019] re-judged the [t0014] schema-only gap with two sonnet judge configurations and confirmed the
gap survives at +24.6 to +37.3 pp under sonnet but inflates to +58 pp under haiku. The operational
consequence is the no-haiku-judge constraint that t0026 inherits. The other operational consequence
is that no reusable judge library was extracted from [t0019] — its judge prompts live inside
`judge_runner.py` and `parse.py` of the [t0019] codebase. t0026 will implement a minimal
`code/judge.py` that reuses the same sonnet prompt patterns (substantive critic for
SWE-bench/FrontierScience where programmatic ground truth exists; model-rotated for Tau-bench where
it does not), and will run opus 4.7 on a 30-instance overlap slice for inter-judge agreement.

### Benchmark instances are staged as JSONL with no loader

[t0003] downloaded SWE-bench Verified (60 rows), Tau-bench (87 rows), and FrontierScience Olympiad
(40 rows) as JSONL files but produced no Python loader. The loader is a 30-line line-by-line
`json.loads()` plus stratified sampling by difficulty for the SWE-bench slice. Instance manifests
must record per-source seeds and dataset hashes for reproducibility.

### Progress rate is meaningful only on multi-step environments

[t0022]'s `compute_progress_rate` requires per-step subgoals. SWE-bench Verified provides them via
patch-level test groupings; Tau-bench has loose tool-trace structure; FrontierScience is
single-step. t0026 reports progress rate on SWE-bench only, EAI error taxonomy on all three.

### Cost defaults from [t0012] inform sizing

The [t0012] smoke harness measured ~$0.18 per FrontierScience instance and ~~$0.20 per Tau-bench
instance with sonnet 4.6 + sonnet judge. SWE-bench is heavier (~~$0.85/instance) due to multi-turn
ReAct on long codebases. These per-source numbers underwrite the t0026 budget plan.

## Reusable Code and Assets

* **Source**: `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` — variant A entry
  point. **Reuse method**: import via library `scope_aware_react_v1`. **Signature**:
  `ScopeAwareReactAgent(problem, granularity, tool_registry, model_call, trajectory_path, max_turns=20, default_granularity_on_missing_tag="atomic").run() -> AgentResult(answer, finished, turns, trajectory)`.
  **Adaptation needed**: t0026 supplies `model_call` wrapping `claude-sonnet-4-6`. **Approximate
  size**: ~250 LOC.

* **Source**: `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py` —
  variant B entry point. **Reuse method**: import via library `scope_unaware_planandsolve_v2`.
  **Signature**:
  `PlanAndSolveAgentV2(model_call, tool_registry={}, max_steps=32).run(problem) -> AgentResultV2(final_answer, trajectory, plan, final_confidence: float | None, final_confidence_parse_failures: int)`.
  **Adaptation needed**: none. **Approximate size**: ~300 LOC.

* **Source**: `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` — variant C entry
  point. **Reuse method**: import via library `matched_mismatch_v1`. **Signature**:
  `MatchedMismatchAgent(model_call, tool_registry, delegate="scope_aware_react", mismatch_strategy="adversarial", seed=0).run(problem, annotation) -> AgentRunResult(...)`.
  **Adaptation needed**: t0026 chooses `adversarial` for stable per-pair comparison. **Approximate
  size**: ~200 LOC.

* **Source**: `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/code/progress_rate.py` and
  `error_taxonomy.py` — metric helpers. **Reuse method**: import via library `abc_harness_metrics`.
  **Signatures**:
  `compute_progress_rate(trajectory, environment_subgoals, judge_model="claude-sonnet-4-6", cost_tracker, judge=None) -> float`
  and
  `classify_error(trajectory_step, environment_state, judge_model, cost_tracker, judge=None, environment_id) -> ErrorTaxonomyLabel`.
  **Adaptation needed**: pass `judge_model="claude- sonnet-4-6"` to override the haiku default.
  **Approximate size**: ~400 LOC combined.

* **Source**: `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` — calibration
  aggregator. **Reuse method**: import via library `metric2_calibration_aggregator_v1`. **Public**:
  `elicit_confidence`, `ConfidenceJudge(samples=3)`, `compute_overconfident_error_rate`,
  `CalibrationRecord`. **Adaptation needed**: ECE not exposed; t0026 implements it inline.
  **Approximate size**: ~200 LOC for the existing aggregator + ~50 LOC of new ECE code.

* **Source**: `tasks/t0003_download_benchmark_subsets/assets/dataset/*/files/*.jsonl` — three
  benchmark JSONL files. **Reuse method**: read directly from disk using a new ~30 LOC line-by-line
  `json.loads()` loader written in `code/instance_loader.py`. **Adaptation needed**: none for
  Tau-bench and FrontierScience; SWE-bench needs stratified sampling (20 of 60) by difficulty
  bucket.

## Lessons Learned

* **Sonnet-vs-haiku judge calibration matters more than expected** ([t0019]). The same evaluation
  gave +58 pp under haiku and +24-37 pp under sonnet. Encoding the no-haiku constraint at the task
  definition level (per t0026's task_description) prevents silent recurrence.
* **Cost dominates on SWE-bench** ([t0012]). The smoke run exposed that SWE-bench costs 4-5x as much
  per instance as the other subsets. The planning step must double-check this with real prompt-token
  measurements before launching N=20 SWE-bench × 3 variants.
* **ReAct truncation defaults matter** ([t0020] referenced indirectly via the t0026 task
  description). Long observations get clipped; t0022 documents max-field constants. Variant A and C
  are most affected because they emit more thoughts/observations than variant B.
* **Schema validation prevents silent failures** ([t0019] / [t0021]). The `final_confidence` parser
  already has one retry; the planning step still must monitor parse-failure counts to ensure variant
  B's RQ4 signal is not silently degraded.

## Recommendations for This Task

1. Write `code/instance_loader.py` (~30 LOC) reading the three [t0003] JSONL files; emit
   `data/instance_manifest.json` with seeds and dataset hashes.
2. Wire `code/runner.py` (~200 LOC) to dispatch per-variant calls into the [t0006] / [t0021] /
   [t0010] library entry points, threading a `model_call` shim that calls `claude-sonnet-4-6`.
3. Implement `code/judge.py` (~150 LOC) with two prompt patterns reused from [t0019] (substantive
   critic and model-rotated) plus a 30-instance opus-4.7 inter-judge slice.
4. Implement `code/calibration.py` (~80 LOC) with inline 10-bin ECE on variant-B `final_confidence`;
   cross-check against [t0011]'s `overconfident_error_rate`.
5. Implement `code/mcnemar.py` (~50 LOC) for paired McNemar p-values for `success(A) > success(B)`
   and `success(B) > success(C)` at Bonferroni alpha=0.025.
6. Use [t0022]'s `compute_progress_rate` on SWE-bench only and `classify_error` on all three
   subsets; pass `judge_model="claude-sonnet-4-6"`.
7. Reestimate cost on the first 5 paired instances per subset before launching the full N=147 run;
   if SWE-bench projects over budget, shrink the SWE-bench slice first as the task description
   authorizes.

## Task Index

### [t0003]

* **Task ID**: `t0003_download_benchmark_subsets`
* **Name**: Download benchmark subsets for the four roadmap sources
* **Status**: completed
* **Relevance**: ships the three runnable JSONL subsets t0026 samples 147 instances from.

### [t0006]

* **Task ID**: `t0006_scope_aware_react_library`
* **Name**: Scope-aware ReAct library: condition A with explicit granularity tags
* **Status**: completed
* **Relevance**: provides the variant A library used directly via `scope_aware_react_v1`.

### [t0007]

* **Task ID**: `t0007_scope_unaware_planandsolve_library`
* **Name**: Scope-Unaware Plan-and-Solve library (v1)
* **Status**: completed
* **Relevance**: transitively used by variant B via [t0021]'s wrapping; library
  `scope_unaware_planandsolve_v1`.

### [t0010]

* **Task ID**: `t0010_matched_mismatch_library`
* **Name**: Matched-mismatch library: condition C with deliberately wrong granularity tags
* **Status**: completed
* **Relevance**: provides the variant C library used directly via `matched_mismatch_v1`.

### [t0011]

* **Task ID**: `t0011_metric2_calibration_aggregator`
* **Name**: Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency
* **Status**: completed
* **Relevance**: source of `overconfident_error_rate` used as a sanity check beside t0026's inline
  ECE for RQ4.

### [t0012]

* **Task ID**: `t0012_phase2_abc_smoke_frontierscience`
* **Name**: Phase 2 A/B/C smoke (FrontierScience) — sizing and unit-cost reference
* **Status**: completed
* **Relevance**: the smoke run that established the per-instance cost numbers driving t0026's budget
  plan.

### [t0019]

* **Task ID**: `t0019_v2_judge_calibration_sonnet`
* **Name**: v2 Judge Calibration with Sonnet (Substantive + Familial Bias)
* **Status**: completed
* **Relevance**: encoded the no-haiku-judge constraint and documented the substantive-critic and
  model-rotated sonnet judge prompt patterns t0026 reuses.

### [t0021]

* **Task ID**: `t0021_plan_and_solve_v2_with_final_confidence`
* **Name**: Plan-and-Solve v2 with final_confidence Field
* **Status**: completed
* **Relevance**: provides the variant B library and the `final_confidence` field that RQ4 (ECE) is
  computed against.

### [t0022]

* **Task ID**: `t0022_abc_harness_progress_rate_and_error_taxonomy`
* **Name**: ABC Harness with Progress Rate and EAI Error Taxonomy
* **Status**: completed
* **Relevance**: source of progress_rate and EAI error-taxonomy helpers t0026 imports for the full
  run.
