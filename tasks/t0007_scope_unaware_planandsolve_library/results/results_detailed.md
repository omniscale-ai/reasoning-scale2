---
spec_version: "2"
task_id: "t0007_scope_unaware_planandsolve_library"
date_completed: "2026-04-29"
---
# Results — t0007_scope_unaware_planandsolve_library

## Summary

This task produced the canonical scope-unaware (B) baseline library `scope_unaware_planandsolve_v1`
for the project's A-vs-B-vs-C comparison. The library adapts the LangChain
`langchain_experimental.plan_and_execute` reference implementation of Wang et al.'s Plan-and-Solve
(PS+) prompting (arXiv 2305.04091, ACL 2023) and exposes a `PlanAndSolveAgent` class whose
trajectory record schema is byte-for-byte interchangeable with sister task t0006's forthcoming
`scope_aware_react_v1`. Every trajectory record sets `granularity = "unspecified"`, which is the
operational definition of the B condition. All 14 tests pass; the library asset verificator reports
zero errors and zero warnings.

## Methodology

* **Compute**: local-only. All work ran inside the worktree at
  `/Users/anaderi/git/reasoning-scale2-worktrees/t0007_scope_unaware_planandsolve_library` on a
  macOS Darwin 25.3.0 host, Python 3.13.11, with no GPU and no network access required for tests.
* **Runtime**: `pytest` reports the 14-case suite at **0.02 s**. End-to-end task wall-clock from the
  resumed `create-branch` step to the final commit was approximately one hour.
* **Timestamps**: task `start_time = 2026-04-29T19:35:48Z`; `end_time` is set in `task.json` at the
  close of the `reporting` step.
* **Tools**: `uv` 0.5.x for environment management; `ruff` and `mypy` for linting; `pytest` for
  testing; `flowmark` for markdown formatting. All command invocations were wrapped in
  `arf.scripts.utils.run_with_logs` per project rule.

## Verification

| Verificator / quality gate | Result |
| --- | --- |
| `verify_research_papers` | PASSED — 0 errors, 0 warnings |
| `verify_plan` | PASSED — 0 errors, 0 warnings |
| `meta.asset_types.library.verificator` (scope_unaware_planandsolve_v1) | PASSED — 0 errors, 0 warnings |
| `uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/` | 14 passed |
| `uv run mypy -p tasks.t0007_scope_unaware_planandsolve_library.code` | Success: no issues found in 1 source file |
| `uv run ruff check tasks/t0007_scope_unaware_planandsolve_library/code/` | All checks passed |

The remaining required verificators (`verify_task_file`, `verify_task_dependencies`,
`verify_suggestions`, `verify_task_metrics`, `verify_task_results`, `verify_task_folder`,
`verify_logs`) run during the `reporting` step.

## Limitations

* **Schema dependency on t0006**: this task defines the trajectory schema rather than reusing one.
  Sister task t0006 (running in parallel) must conform when its branch reaches implementation. The
  schema is documented at length in `description.md` `## Trajectory Schema` and exposed as
  `TRAJECTORY_RECORD_FIELDS`. If t0006 lands a different schema, a follow-up correction task will be
  required (see `suggestions.json`).
* **PS+ prompt provenance**: the verbatim PS+ instruction text was sourced from the t0002 Wang2023
  paper summary, which itself was grounded in the abstract because the paper PDF download failed in
  t0002. A Phase 2 evaluation should re-download the paper to confirm the prompt text against the
  published version.
* **Tool registry shape**: the executor expects a flat `dict[str, Callable[[str], str]]` registry.
  Hierarchical tool registries are out of scope for this library and will need a follow-up.
* **Error surfacing**: tool errors and unknown-tool conditions are written to the trajectory's
  `observation` field rather than raised as exceptions. Callers that want hard-failure semantics
  must inspect observation strings for the `"ERROR:"` prefix.
* **No live LLM exercise**: the test suite is fully deterministic. The library has been exercised
  against `ScriptedModel` only; no live LLM wiring exists yet — that is a Phase 2 task.

## Examples

The deliverable is a library, not predictions or LLM completions. Two concrete behaviours of the
library are reproduced below to make the API surface tangible.

### Example 1: Successful end-to-end run with one tool call

Input — the planner's pre-recorded response, the executor's two pre-recorded responses, and the
problem statement:

```text
Planner response (1):
1. Add the numbers two and three.
2. Report the result as the final answer.

Executor response (turn 1):
Action: add | Args: 2,3

Executor response (turn 2):
FINAL_ANSWER: 5

problem = "What is two plus three?"
tool_registry = {"add": lambda args: str(sum(int(x) for x in args.split(",")))}
```

Output — `agent.run(problem)` returns:

```text
AgentResult(
  final_answer="5",
  plan=["Add the numbers two and three.", "Report the result as the final answer."],
  trajectory=[
    TrajectoryRecord(turn_index=0, granularity="unspecified", thought="",
                     action="add(2,3)", observation="5", confidence=None),
    TrajectoryRecord(turn_index=1, granularity="unspecified", thought="",
                     action="finish", observation="5", confidence=None),
  ],
)
```

### Example 2: Malformed planner output raises `MalformedPlanError`

Input — the planner returns prose with no numbered steps:

```text
Planner response (1):
I refuse to make a plan.

problem = "Anything."
tool_registry = {}
```

Output — `agent.run(problem)` raises:

```text
MalformedPlanError: No numbered plan steps were found in the planner output.
Expected lines starting with '1.' or '1)'.
```

The full set of 14 deterministic test cases is in
`tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` and exercises every
behaviour referenced in this section.

## Files Created

* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` — library implementation
  (about 290 lines).
* `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` — 14-case deterministic
  pytest suite (about 220 lines).
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/details.json`
  — library asset metadata.
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md`
  — library description with all 8 mandatory sections plus `## Trajectory Schema` and
  `## License & Attribution`.
* `tasks/t0007_scope_unaware_planandsolve_library/research/research_papers.md` — paper review
  grounded in the t0002 Wang2023 summary.
* `tasks/t0007_scope_unaware_planandsolve_library/plan/plan.md` — eight-step plan with nine `REQ-*`
  items.
* `tasks/t0007_scope_unaware_planandsolve_library/results/results_summary.md`,
  `results_detailed.md`, `metrics.json`, `costs.json`, `remote_machines_used.json`,
  `suggestions.json`.

## Task Requirement Coverage

The operative task text from `task.json` and `task_description.md`:

> Scope-unaware Plan-and-Solve library: condition B baseline. Write-library adapting LangChain
> Plan-and-Execute as the canonical scope-unaware (B) baseline.
>
> Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
> `PlanAndSolveAgent` class that: accepts a problem statement, a tool registry, and a model-call
> callable; generates a free-form numbered plan, then executes each step sequentially through a
> Plan-and-Execute loop; emits trajectory records in the same schema as `scope_aware_react_v1` so
> both libraries are drop-in interchangeable; the `granularity` field in the schema is filled with
> the literal string `"unspecified"` to mark the B condition; logs every step's
> `{turn_index, granularity, thought, action, observation, confidence}`; supports a
> deterministic-test mode that accepts pre-recorded model outputs.
>
> Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing from
> scratch. License is Apache 2.0; record attribution in `description.md`.
>
> Provide pytest coverage at `tasks/t0007_.../code/test_planandsolve.py` covering: plan parsing,
> sequential execution, trajectory schema parity with t0006, finish detection, and error recovery on
> malformed model output.

* **REQ-1** (library asset folder under `assets/library/scope_unaware_planandsolve_v1/`): **Done**.
  Asset exists with `details.json`, `description.md`, and `module_paths` pointing at
  `code/planandsolve.py`. Evidence:
  `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/details.json`;
  asset verificator passes.
* **REQ-2** (`PlanAndSolveAgent` accepts problem, tool registry, and model-call callable): **Done**.
  `PlanAndSolveAgent.__init__(model_call, tool_registry, max_steps, granularity_label)` and
  `.run(problem)`. Evidence: `code/planandsolve.py` lines 230-265.
* **REQ-3** (numbered plan generation + sequential per-step execution): **Done**. The `run()` method
  calls the planner, parses the plan with `parse_plan`, then iterates over plan steps calling the
  executor. Evidence: `test_sequential_execution` passes; `code/planandsolve.py` `run` method.
* **REQ-4** (trajectory schema matching `scope_aware_react_v1`): **Done**. `TrajectoryRecord` with
  the canonical six fields plus `TRAJECTORY_RECORD_FIELDS` exposed at module scope. Evidence:
  `test_trajectory_schema_parity` and `test_trajectory_record_fields_match_canonical_tuple` pass;
  the `## Trajectory Schema` block in `assets/library/scope_unaware_planandsolve_v1/description.md`.
* **REQ-5** (`granularity == "unspecified"` on every B record): **Done**. The default
  `granularity_label` is `"unspecified"`. Evidence: `test_granularity_unspecified` passes.
* **REQ-6** (deterministic-test mode with pre-recorded outputs): **Done**. `ScriptedModel` class.
  Evidence: `test_scripted_model_round_trip` passes; the entire 14-case suite runs without LLM
  calls.
* **REQ-7** (LangChain Apache-2.0 attribution): **Done**. `## License & Attribution` block in
  `description.md` plus a license note in the module docstring. Evidence:
  `assets/library/scope_unaware_planandsolve_v1/description.md` `## License & Attribution`.
* **REQ-8** (pytest coverage for plan parsing, sequential execution, schema parity, finish
  detection, malformed output): **Done**. 14 named test cases including `test_parse_plan_simple`,
  `test_parse_plan_continuation`, `test_parse_plan_paren_separator`,
  `test_parse_plan_malformed_raises`, `test_sequential_execution`, `test_trajectory_schema_parity`,
  `test_finish_detection_final_answer`, `test_malformed_planner_output_propagates`. Evidence:
  `pytest` reports 14 passed.
* **REQ-9** (trajectory schema documented for sister task t0006): **Done**. The
  `## Trajectory Schema` block in `description.md` provides a field table, JSON example, and Python
  assertion snippet; `TRAJECTORY_RECORD_FIELDS` is exported as the canonical tuple. Evidence:
  `assets/library/scope_unaware_planandsolve_v1/description.md` `## Trajectory Schema`.
* **Out-of-scope items** (A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
  execution): **Confirmed out of scope**. None of these were implemented in this task; they are
  Phase 2 deliverables.
