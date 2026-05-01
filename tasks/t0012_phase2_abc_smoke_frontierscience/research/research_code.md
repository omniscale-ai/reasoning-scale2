---
spec_version: "1"
task_id: "t0012_phase2_abc_smoke_frontierscience"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 6
libraries_found: 4
libraries_relevant: 4
date_completed: "2026-04-30"
status: "complete"
---
# Research Code: Phase 2 A/B/C Smoke Harness on FrontierScience

## Task Objective

Build a thin orchestrator library `phase2_smoke_harness_v1` that loads the t0009 v2 dataset, filters
to FrontierScience-Olympiad complete rows, and dispatches each row to one of three condition
libraries (A: scope_aware_react_v1; B: scope_unaware_planandsolve_v1; C: matched_mismatch_v1). After
every run, compute three registered metrics per condition (`task_success_rate`,
`overconfident_error_rate`, `avg_decisions_per_task`) and emit one predictions asset per condition.
All four condition/metric libraries already exist; this code research catalogs their public APIs so
the harness can wire them together without reimplementing anything.

## Library Landscape

The aggregator (`aggregate_libraries`) reports four libraries in the project, all four are direct
dependencies of this task and all four are imported via library (no code copying):

* **scope_aware_react_v1** (`tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`) —
  produced by [t0006]. Public API: `ScopeAwareReactAgent`, `TrajectoryRecord`, `Action`,
  `ScriptedModel`, `MalformedActionError`, `_parse_model_output`. Trajectory schema:
  `(turn_index, granularity, thought, action, observation, confidence)` per
  `TRAJECTORY_RECORD_FIELDS`. The agent calls `model_call(prompt: str) -> str`. **Relevant**:
  condition A library — direct usage.
* **scope_unaware_planandsolve_v1**
  (`tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py`) — produced by [t0007].
  Public API: `PlanAndSolveAgent`, `TrajectoryRecord`, `parse_plan`, `MalformedPlanError`,
  `PLAN_PROMPT_TEMPLATE`, `EXECUTE_PROMPT_TEMPLATE`, `TRAJECTORY_RECORD_FIELDS`,
  `GRANULARITY_UNSPECIFIED`. Same six-field trajectory schema. **Relevant**: condition B library —
  direct usage.
* **matched_mismatch_v1** (`tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`) —
  produced by [t0010]. Public API: `MatchedMismatchAgent`, `MatchedMismatchRecord`,
  `AgentRunResult`, `Phase`, `iter_phases`, `pick_mismatch_tag`, `GRANULARITY_VALUES`,
  `ADVERSARIAL_MAP`, `CORRECT_GRANULARITY_EXTRAS_KEY`. The agent constructor takes
  `(model_call, tool_registry, delegate, mismatch_strategy, seed)` and exposes
  `run(*, problem, annotation)`. **Relevant**: condition C library — use
  `delegate="scope_unaware_planandsolve"`, `mismatch_strategy="random"`, `seed=42`.
* **metric2_calibration_aggregator_v1**
  (`tasks/t0011_metric2_calibration_aggregator/code/calibration.py`) — produced by [t0011]. Public
  API: `compute_overconfident_error_rate(records, threshold=0.75)`, `ConfidenceJudge`,
  `elicit_confidence`, `calibration_record_from_trajectory`, `CalibrationRecord`,
  `ConfidenceSample`, `ConfidenceAggregate`, `MalformedConfidenceError`, `ConfidencePromptTemplate`.
  Default `HIGH_CONFIDENCE_THRESHOLD = 0.75` and `SELF_CONSISTENCY_SAMPLES = 3`. **Relevant**:
  Metric 2 implementation.

## Key Findings

### All three condition libraries already conform to a single trajectory schema

The six-field schema `(turn_index, granularity, thought, action, observation, confidence)` is
defined exactly once, in [t0007] as `TRAJECTORY_RECORD_FIELDS`. Both [t0006] and [t0010] import that
constant and assert the field tuple matches at module load. This means the harness can serialize all
three conditions with a single JSONL writer and downstream metric code does not need per-condition
branching. The only difference between conditions: A writes the canonical granularity tag
(`global`/`subtask`/`atomic`); B always writes `"unspecified"`; C writes a deliberately-wrong tag
drawn from the matched-mismatch strategy. Condition C also adds an `extras` dict carrying the
correct tag under `_correct_granularity` — but `extras` is dropped when serializing only the
canonical six fields, which keeps the JSONL files schema-identical.

### Condition libraries already encapsulate their own prompts

The harness does not need to construct any agent prompts itself. [t0006] builds the system prompt in
`_build_system_prompt(granularity=...)` and the per-turn prompt in `_build_prompt(...)`, both
internal to `ScopeAwareReactAgent.run()`. [t0007] uses the module-level
`PLAN_PROMPT_TEMPLATE.format(problem=...)` for planning and `EXECUTE_PROMPT_TEMPLATE.format(...)`
for execution. [t0010] builds two prompt variants internally
(`_build_react_phase_prompt`/`_build_planandsolve_phase_prompt`) selected by the `delegate` literal.
Therefore the harness only owns: (a) the model_call wrapper around the Anthropic API, (b) the tool
registry, (c) the data loading and answer extraction, and (d) the post-run metric computation.

### Tool registry shape differs between conditions A and (B, C)

[t0006]'s ReAct registry calls `tool(**action.args)` because `Action.args` is already a dict.
[t0007]'s Plan-and-Solve registry calls `tool(args_str: str)` with a single argument string. [t0010]
inherits whichever shape its `delegate` uses. This means the harness must construct **two** tool
registries from the same underlying implementation: one keyword-args wrapper (for A) and one
string-args wrapper (for B and C with `delegate="scope_unaware_planandsolve"`). This is a small
adapter, not a duplication of the tool itself.

### Metric 2 needs verbalized confidence; trajectory `confidence` field may be numeric or null

t0006 records numeric confidence (0-1) when the model emits a `Confidence: <0-100>` line. t0007
always records `None`. t0010 records whatever the chosen delegate produces. To compute
`overconfident_error_rate` we need a numeric confidence per problem; for B (and for trajectories
where the model omitted the confidence line) the harness must call `elicit_confidence` from [t0011]
post-hoc on the agent's final action and use 3-sample self-consistency aggregation. The recommended
path for the smoke run: skip self-consistency for cost and use the trajectory's own final-turn
`confidence` when present, falling back to a single `elicit_confidence` call when absent. Document
this simplification in the plan and the results.

### Dataset filtering is straightforward; row count is 40, not 28

The v2 dataset asset is one JSONL file (115 rows, all `hierarchy_completeness=true` under the v2
stricter rule). Filtering to `benchmark == "FrontierScience-Olympiad"` yields **40 rows**, not 28.
The task description noted N≈28 (matching v1) and instructs us to proceed with whatever count v2
provides. v2's annotator was Claude Haiku 4.5 (not Sonnet as originally specified) — confound
already documented as S-0009-01 and acceptable for the smoke. [t0009] is the producer.

## Reusable Code and Assets

* **Source**: `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` (~470 lines)
  * **What it does**: condition A agent + trajectory schema + scripted-model test fake.
  * **Reuse method**: **import via library** as
    `tasks.t0006_scope_aware_react_library.code.scope_aware_react`.
  * **Function signatures**:
    `ScopeAwareReactAgent(*, problem, granularity, tool_registry, model_call, trajectory_path, max_turns=12)`;
    `agent.run() -> AgentResult(answer, finished, turns, trajectory)`.
  * **Adaptation**: none.
* **Source**: `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` (~360 lines)
  * **What it does**: condition B planner+executor agent.
  * **Reuse method**: **import via library** as
    `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve`.
  * **Function signatures**:
    `PlanAndSolveAgent(model_call, tool_registry, max_steps=32, granularity_label="unspecified")`;
    `agent.run(problem) -> AgentResult(final_answer, trajectory, plan)`.
  * **Adaptation**: none.
* **Source**: `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` (~650 lines)
  * **What it does**: condition C agent that walks the v2 hierarchy and substitutes wrong
    granularity tags.
  * **Reuse method**: **import via library** as
    `tasks.t0010_matched_mismatch_library.code.matched_mismatch`.
  * **Function signatures**:
    `MatchedMismatchAgent(model_call, tool_registry, delegate, mismatch_strategy, seed=0)`;
    `agent.run(*, problem, annotation) -> AgentRunResult(final_answer, trajectory, phases)`. Use
    `delegate="scope_unaware_planandsolve"` and `mismatch_strategy="random"` for the smoke (per task
    description).
  * **Adaptation**: none.
* **Source**: `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` (~390 lines)
  * **What it does**: Metric 2 aggregator with verbalized confidence elicitation and
    self-consistency.
  * **Reuse method**: **import via library** as
    `tasks.t0011_metric2_calibration_aggregator.code.calibration`.
  * **Function signatures**:
    `compute_overconfident_error_rate(*, records: Iterable[CalibrationRecord], threshold=0.75) -> float`;
    `calibration_record_from_trajectory(*, problem_id, record, is_correct) -> CalibrationRecord`;
    `elicit_confidence(*, model_call, problem, action, prompt_template=None) -> tuple[str, float]`.
  * **Adaptation**: none.
* **Source**:
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
  * **What it is**: 115 rows of hierarchical annotations across four benchmarks.
  * **Reuse method**: read directly from disk; no import needed. Filter to
    `benchmark == "FrontierScience-Olympiad"` and `hierarchy_completeness == True` to obtain the 40
    smoke-run rows.

## Lessons Learned

* **Always assert schema parity at module load.** [t0010] imports [t0007]'s
  `TRAJECTORY_RECORD_FIELDS` and `assert`s the field tuple matches at top-level. The harness should
  do the same so a future schema drift fails loudly instead of producing silently mismatched
  trajectory files.
* **Never reimplement a published prompt.** [t0007]'s `PS_PLUS_INSTRUCTION` is the verbatim Wang2023
  instruction; [t0006]'s system prompt is adapted from LangChain (Apache 2.0). Both attribution
  lines are encoded in the source. The harness must not invent its own prompts for conditions A or
  B.
* **Predict cost before running.** [t0009] used Haiku for annotation because Sonnet ran 5x over
  budget; the v2 confound is documented and accepted. The smoke run must compute a per-call cost
  estimate before launching the full sweep, then halt at $20 per the task description's explicit
  cap.
* **Pair runs by `task_id`.** McNemar / paired sign tests need paired binary outcomes. The harness
  must serialize problems and conditions in a deterministic order (alphabetical task_id × A,B,C) so
  every problem appears in all three trajectory files even if some agent runs error out.
* **LLM-as-judge is unavoidable for FrontierScience.** Direct string comparison of agent
  `Finish(answer)` against `gold_actions['global']` will produce near-zero match rates. Use
  Anthropic Haiku as a binary judge with a simple "Does the candidate match the gold?" prompt. Log
  every judge call.

## Recommendations for This Task

1. Build `phase2_smoke_harness_v1` as a pure orchestrator with five modules in `code/`: `paths.py`
   (centralized paths), `constants.py` (model IDs, registries, schema constants), `model_call.py`
   (Anthropic SDK wrapper with cost tracking), `harness.py` (the dataset loader, per-condition
   dispatcher, judge, and metric computer), `run_smoke.py` (the CLI entrypoint).
2. Use the same `model_call` callable for all three conditions on the same row to ensure paired
   results have identical model behavior assumptions. The model call is `claude-sonnet-4-6-20251001`
   for the agent runs and `claude-haiku-4-5-20251001` for the judge and any post-hoc confidence
   elicitation.
3. Persist trajectories as JSONL under
   `assets/predictions/phase2_smoke_{a,b,c}/files/predictions-frontierscience-olympiad.jsonl` and
   write per-condition metrics to `results/metrics.json` in the explicit-variant format with three
   variants.
4. After every variant run, sum API spend and check the $20 cap. If the cap is approached mid-run,
   halt remaining variants, write the partial result, and document the overrun.
5. Reuse all four sister libraries verbatim. Do not reimplement, do not modify, do not copy
   non-library code. The harness's only original code is the dataset loader, the cost tracker, the
   judge prompt, and the metric aggregator.

## Task Index

### [t0006]

* **Task ID**: t0006_scope_aware_react_library
* **Name**: Scope-aware ReAct library (condition A)
* **Status**: completed
* **Relevance**: Provides the condition A agent and the canonical trajectory schema referenced by
  every other library.

### [t0007]

* **Task ID**: t0007_scope_unaware_planandsolve_library
* **Name**: Scope-unaware Plan-and-Solve library (condition B)
* **Status**: completed
* **Relevance**: Provides the condition B agent and defines `TRAJECTORY_RECORD_FIELDS` shared across
  all conditions.

### [t0009]

* **Task ID**: t0009_hierarchical_annotation_v2
* **Name**: Hierarchical annotation v2: tree schema with subtask-to-atomic edges
* **Status**: completed
* **Relevance**: Produces the dataset asset this task consumes; filtered to
  `benchmark == "FrontierScience-Olympiad"` (40 complete rows).

### [t0010]

* **Task ID**: t0010_matched_mismatch_library
* **Name**: Matched-mismatch library: condition C with deliberately wrong granularity tags
* **Status**: completed
* **Relevance**: Provides the condition C agent and the v2-hierarchy phase walk used by the harness.

### [t0011]

* **Task ID**: t0011_metric2_calibration_aggregator
* **Name**: Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency
* **Status**: completed
* **Relevance**: Provides `compute_overconfident_error_rate` and the verbalized-confidence
  elicitation utilities required for the Metric 2 column.

### [t0002]

* **Task ID**: t0002_literature_survey_granularity_conditioning
* **Name**: Literature survey on granularity conditioning
* **Status**: completed
* **Relevance**: Holds the paper assets for ReAct, Plan-and-Solve, and Xiong2024 cited in
  research_papers.md.
