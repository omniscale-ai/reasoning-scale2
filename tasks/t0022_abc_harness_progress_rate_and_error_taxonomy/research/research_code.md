---
spec_version: "1"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
research_stage: "code"
tasks_reviewed: 6
tasks_cited: 6
libraries_found: 5
libraries_relevant: 2
date_completed: "2026-05-01"
status: "complete"
---
# Research Code — t0022 ABC Harness Progress Rate and EAI Error Taxonomy

## Task Objective

Build a single zero-API library `abc_harness_metrics` that exposes two functions plus a high-level
entry point: `compute_progress_rate(trajectory, environment_subgoals) -> float` (Ma2024 AgentBoard
protocol) and `classify_error(trajectory_step, environment_state) -> ErrorTaxonomyLabel` (Li2024
Embodied Agent Interface 6-class taxonomy plus an "ok" sentinel). The library is consumed by t0023's
N>=157 ABC confirmatory run on SWE-bench Verified Lite. It must validate against t0012's smoke
trajectories on FrontierScience-Olympiad and pass the decision criteria (non-degenerate progress
rate distribution; A-vs-C separation rate >= 30% on paired steps).

## Library Landscape

The library aggregator returns five existing project libraries. None implements progress rate or an
EAI-style error taxonomy, so this task is genuinely additive.

* `scope_aware_react_v1` [t0006] — ReAct agent with granularity tags. Produces trajectory rows with
  fields `(turn_index, granularity, thought, action, observation, confidence)`. **Relevant**: this
  trajectory schema is the input schema my `compute_progress_rate` and `classify_error` must accept.
  Imported indirectly by walking the t0012 prediction JSONL.
* `scope_unaware_planandsolve_v1` [t0007] — Plan-and-Solve agent. Same trajectory schema as
  scope_aware_react_v1. **Relevant** for the same reason.
* `matched_mismatch_v1` [t0010] — Condition-C wrapper that injects deliberately wrong granularity
  tags. Same trajectory schema. **Relevant** for the same reason.
* `metric2_calibration_aggregator_v1` [t0011] — Verbalized-confidence + 3-sample self-consistency
  aggregator. **Not relevant** to this task; progress-rate and error-taxonomy do not depend on
  calibration.
* `phase2_smoke_harness_v1` [t0012] — End-to-end A/B/C harness with judge call, predictions writer,
  metric computation, charts, and stats. **Relevant**: I will reuse the local Claude Code CLI
  invocation pattern from `model_call.py` (Anthropic credentials are vended through the `claude` CLI
  rather than `ANTHROPIC_API_KEY`).

The aggregator produces no correction overlays for any of these libraries.

## Key Findings

### Trajectory Schema is Stable Across A/B/C

Every t0012 prediction row [t0012] stores `trajectory: list[Step]` where each `Step` is a dict with
`turn_index: int`, `granularity: "global"|"subtask"|"atomic"`, `thought: str`, `action: str`,
`observation: str`, and `confidence: float`. Trajectory length is `1` for floor-bound A and B runs
on FrontierScience-Olympiad and `15-40` for C runs. The 91 t0012 predictions split as 40 A + 40 B +
11 C. The error-taxonomy A-vs-C separation criterion in t0022's `task_description.md` will work
because C trajectories have plenty of steps (mean ~26.0) to grade against the A baseline (mean
~1.18).

### Local CLI is the Required Model Call Backend

`tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py` documents in its module docstring
that the project uses the local `claude` CLI for Anthropic access, not the Anthropic Python SDK,
because `setup-project` Phase 4 vends OAuth via Claude Code rather than an API key. Cost-tracking is
done via a process-wide `CostTracker` that reads `total_cost_usd` from the CLI's JSON envelope and
appends a `_call_log.jsonl` per call. The 25× cost reduction trick
(`--system-prompt MIN --tools "" --setting-sources ""`) is the difference between this task fitting
in $2 and not [t0012]. I will copy this pattern into my library code.

### Ma2024 Protocol is Subgoal-Coverage with Regex or Judge Predicates

The Ma2024 (AgentBoard) summary in t0017's paper assets confirms two forms of progress rate: a
continuous similarity function `f(s_i, g)` for tasks with comparable states (PDDL, WebShop) and a
fraction-of-matched-subgoals form `(1/K) sum_k f(s_i, g_k)` for discrete subgoal sequences
(AlfWorld, ScienceWorld, BabyAI, Jericho, Tool-Query, Tool-Operation, WebArena) [t0017]. AgentBoard
achieves Pearson rho > 0.95 against four-author human ratings. Regex predicates work for
environments where state transitions are textually predictable; for FrontierScience-Olympiad and
SWE-bench, the trajectories are textual but state transitions are not regex-able, so a **judge call
per (subgoal, trajectory) pair** is the right adaptation, with disk-cached results.

### Li2024 Taxonomy Maps Cleanly to Six Labels

The Li2024 (Embodied Agent Interface) summary in t0017's paper assets confirms the six diagnostic
categories: hallucination (predicates or objects that do not exist), affordance violations, missing
steps, wrong-order steps, additional/extra unnecessary steps, missing-precondition/effect errors
[t0017]. The paper reports that VirtualHome failures are dominated by hallucination + affordance
errors, while BEHAVIOR failures are dominated by missing-step + wrong-order errors. This maps to
exactly the six labels specified in t0022 `task_description.md` plus an "ok" sentinel for non-error
steps.

### t0012 Floor Result is Why This Task Exists

[t0012] reports task-success rates of 2.5% (A), 0% (B), 0% (C) on FrontierScience-Olympiad with
claude-haiku-4-5. At this floor, RQ1, RQ2, and RQ5 are statistically invisible regardless of N.
Progress rate (continuous in `[0, 1]`) plus per-step error taxonomy (categorical, 7 classes) recover
signal because they are *trajectory-level* metrics, not *outcome-level*.

## Reusable Code and Assets

* **Source**: `tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py` (~265 lines). **What
  it does**: Wraps the local `claude` CLI, parses the JSON envelope, tracks cost, retries on
  transient errors. **Reuse method**: **copy into task** (rule: cross-task code copy, no imports
  outside libraries). I will trim the unused `make_model_call` closure and keep `_invoke_cli`,
  `_retry_invoke`, `CostTracker`, and `CallRecord`. **Function signatures**:
  `_invoke_cli(*, prompt: str, model: str) -> tuple[str, dict[str, Any]]` and
  `CostTracker.record(*, record: CallRecord) -> None`. **Adaptation**: rename the cost-log path to
  `tasks/t0022.../logs/judge_calls.jsonl`. **Line count**: ~120 lines after trimming.

* **Source**:
  `tasks/t0012_phase2_abc_smoke_frontierscience/assets/predictions/phase2-smoke-{a,b,c}/files/predictions-frontierscience-olympiad.jsonl`
  (40 + 40 + 11 rows). **What it does**: Stores the actual ABC trajectories with the schema above.
  **Reuse method**: **read at validation time** — no copy. I will load these JSONL files in
  `code/replay_t0012.py` and feed them through `score_trajectory()` to produce the per-condition
  progress-rate and error-distribution table required by `task_description.md` § Deliverables 3.

* **Source**: `tasks/t0012_phase2_abc_smoke_frontierscience/code/constants.py`. **What it does**:
  Defines `MODEL_JUDGE`, `BUDGET_CAP_USD`, `CLAUDE_CLI`, etc. **Reuse method**: **copy into task** —
  the library needs its own constants module per the project Python style guide. I will keep only
  the relevant constants plus add new ones for subgoal/error prompts.

* **Source**: t0017 paper assets (Ma2024, Li2024). **What it does**: Provides the protocol
  specifications. **Reuse method**: **read at design time**, not imported. The relevant prompts are
  paraphrased from the summary documents because the original supplementary material is not in the
  asset folder; the library's description document will explicitly attribute them.

The total amount of new code is roughly:

* `code/constants.py` — ~80 lines
* `code/paths.py` — ~30 lines
* `code/types.py` — `~60 lines (dataclasses for TrajectoryStep, ErrorTaxonomyLabel enum,
  TrajectoryScore)
* `code/cli.py` — ~150 lines (copied + trimmed from t0012 model_call.py)
* `code/cache.py` — ~80 lines (disk-cached judge calls keyed by hash)
* `code/progress_rate.py` — ~120 lines
* `code/error_taxonomy.py` — ~140 lines
* `code/score_trajectory.py` — ~80 lines
* `code/subgoal_loader.py` — ~50 lines
* `code/replay_t0012.py` — ~150 lines (validation harness)
* `code/test_progress_rate.py`, `code/test_error_taxonomy.py`, `code/test_score_trajectory.py` —
  ~250 lines

Plus the subgoal definition JSON file at `assets/library/abc_harness_metrics/files/subgoals.json`
covering FrontierScience-Olympiad and >=50 SWE-bench Verified Lite instances.

## Lessons Learned

* **Cache aggressively** — t0012 [t0012] paid $20 because every judge call was uncached; with the
  CLI cost trick described in `model_call.py` plus disk caching keyed by
  `(environment, trajectory hash, subgoal text)`, t0023 with N=157 should re-spend zero on
  already-graded subgoals. This matches t0022 `task_description.md` § Implementation Notes.
* **Strict-output judge prompts** — t0012 used a one-word `YES|NO` correctness judge [t0012] and
  found that even Haiku reliably emits a single token under that constraint. I will copy that
  pattern: progress-rate judge returns `YES|NO` per (step, subgoal); error-taxonomy judge returns
  exactly one of seven label tokens.
* **Floor-bound runs need trajectory-level metrics** — t0012's floor result is the motivation for
  this task; the lesson is that confirmatory phases must register progress-rate + error-taxonomy
  alongside task-success-rate before launching, not after.
* **Trajectory length asymmetry is real** — A trajectories on FrontierScience-Olympiad are
  effectively single-shot (`Finish` at turn 0) [t0012], while C trajectories are 15-40 steps. The
  A-vs-C separation criterion in `task_description.md` must be measured on the C side because A has
  too few steps to dominate.

## Recommendations for This Task

1. **Reuse the t0012 CLI invocation pattern verbatim**, copy into `code/cli.py`. Do not introduce a
   new model call backend.
2. **Disk-cache judge calls** via SHA-256 of `(environment, trajectory hash, prompt key)` to enable
   t0023 reuse. Put the cache at `tasks/t0022.../assets/library/abc_harness_metrics/files/cache/`.
3. **Use the explicit subgoal-coverage form of progress rate** (the discrete-subgoal form, not the
   continuous-state form). FrontierScience-Olympiad has no symbolic state to compare against.
4. **Author subgoals manually for FrontierScience-Olympiad** — six 10-row tasks have already been
   sampled by t0012; I will define 3-5 subgoals per task by reading the gold answer.
5. **Author SWE-bench Verified Lite subgoals from gold patch hunks** — per `task_description.md` §
   Implementation Notes, a "subgoal hit" is operationalised as an edit that touches the same file as
   a gold patch hunk. This is mechanical and does not require a judge call.
6. **Default judge model = `claude-haiku-4-5`**. Allow override via constructor argument so t0023
   can use sonnet for spot-check re-grading.
7. **Validation = replay only the 91 t0012 trajectories**, not a fresh run. Save the per-condition
   progress-rate distribution and error-taxonomy distribution as `results/replay_summary.json` and
   embed the side-by-side table in `results/results_detailed.md`.

## Task Index

### [t0006]

* **Task ID**: t0006_scope_aware_react_library
* **Name**: Scope-Aware ReAct Library
* **Status**: completed
* **Relevance**: Defines the trajectory schema this library consumes; no direct import.

### [t0007]

* **Task ID**: t0007_scope_unaware_planandsolve_library
* **Name**: Scope-Unaware Plan-and-Solve Library
* **Status**: completed
* **Relevance**: Produces trajectories with the same schema; consumed indirectly via t0012's
  predictions JSONL.

### [t0010]

* **Task ID**: t0010_matched_mismatch_library
* **Name**: Matched Mismatch Library
* **Status**: completed
* **Relevance**: Produces condition-C trajectories used in the validation replay.

### [t0011]

* **Task ID**: t0011_metric2_calibration_aggregator
* **Name**: Metric-2 Calibration Aggregator
* **Status**: completed
* **Relevance**: Discovered via the library aggregator; not imported because progress-rate and
  error-taxonomy do not depend on calibration scoring.

### [t0012]

* **Task ID**: t0012_phase2_abc_smoke_frontierscience
* **Name**: Phase 2 ABC Smoke (FrontierScience-Olympiad)
* **Status**: completed
* **Relevance**: Provides 91 paired ABC trajectories that this task replays; provides the local CLI
  model-call pattern that this task copies into `code/cli.py`.

### [t0017]

* **Task ID**: t0017_literature_hierarchical_agents_and_judges
* **Name**: Hierarchical Agents and Judges Literature Review
* **Status**: completed
* **Relevance**: Contains the Ma2024 (AgentBoard, `10.48550_arXiv.2401.13178`) and Li2024 (Embodied
  Agent Interface, `10.48550_arXiv.2410.07166`) paper assets. The summaries in those assets define
  the protocols this task implements.
