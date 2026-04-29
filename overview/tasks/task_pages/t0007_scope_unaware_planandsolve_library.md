# ✅ Scope-unaware Plan-and-Solve library: condition B baseline

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T19:35:48Z |
| **Completed** | 2026-04-29T20:01:00Z |
| **Duration** | 25m |
| **Source suggestion** | `S-0002-06` |
| **Task types** | `write-library` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md), [`hierarchical-planning`](../../by-category/hierarchical-planning.md) |
| **Expected assets** | 1 library |
| **Step progress** | 9/15 |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../../tasks/t0007_scope_unaware_planandsolve_library/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/task_description.md)*

# Scope-Unaware Plan-and-Solve Library (Condition B)

## Motivation

The literature survey in t0002 identified Plan-and-Solve (Wang2023) as the strongest published
prompt-only baseline that does not condition on explicit granularity tags. It is therefore the
canonical scope-unaware (B) baseline for the project's A-vs-B-vs-C comparison. This task
produces the matching library asset, sharing the trajectory-log schema with t0006 so a Phase 2
experiment can run both libraries against the same harness without bespoke glue. Implements
suggestion S-0002-06.

## Scope

* Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
  `PlanAndSolveAgent` class that:
  * Accepts a problem statement, a tool registry, and a model-call callable.
  * Generates a free-form numbered plan, then executes each step sequentially through a
    Plan-and-Execute loop.
  * Emits trajectory records in the same schema as `scope_aware_react_v1` so both libraries
    are drop-in interchangeable. The `granularity` field in the schema is filled with the
    literal string `"unspecified"` to mark the B condition.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}`.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing
  from scratch. License is Apache 2.0; record attribution in `description.md`.
* Provide pytest coverage at
  `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` covering: plan
  parsing, sequential execution, trajectory schema parity with t0006, finish detection, and
  error recovery on malformed model output.

Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
execution.

## Approach

1. Read t0002's Wang2023 paper summary and the LangChain Plan-and-Execute source to ground the
   prompt template and execution loop.
2. Implement the library in
   `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and re-export the
   public API from `assets/library/scope_unaware_planandsolve_v1/library/`.
3. Reuse the trajectory log schema defined in t0006 by reading t0006's library when it lands;
   if t0006 has not landed yet, define the schema here and document that t0006 must conform.
4. Write `details.json`, `description.md`, and `files/` for the asset.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_unaware_planandsolve_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for the matched mismatch (C) library.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. May reference t0006's library if it merges first; otherwise this task
  defines the trajectory schema and t0006 must conform.
* References Wang2023 paper asset (`10.48550_arXiv.2305.04091`) from t0002.

## Source Suggestion

S-0002-06 — "Implement Plan-and-Solve as the canonical scope-unaware (B) baseline."

## Key Questions

1. What plan format does Plan-and-Solve produce, and how should it be parsed
   deterministically?
2. How should the library mark the absence of a granularity tag in the trajectory record?
3. What is the minimal API surface that lets a Phase 2 harness swap between this and t0006's
   library by changing only one line?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Scope-Unaware Plan-and-Solve Agent (v1)](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/) | [`description.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md) |

## Suggestions Generated

<details>
<summary><strong>Implement matched-mismatch (C) library on top of
scope_unaware_planandsolve_v1</strong> (S-0007-01)</summary>

**Kind**: library | **Priority**: high

Create a third agent library that wraps scope_unaware_planandsolve_v1 (or
scope_aware_react_v1) with a tag-classifier that retroactively labels each step's granularity,
producing the matched-mismatch (C) condition for the project's A-vs-B-vs-C comparison. Reuse
this task's TRAJECTORY_RECORD_FIELDS export so all three libraries share the same trajectory
schema. The classifier should be a small fine-tuned model or heuristic so the task is
local-only and deterministic.

</details>

<details>
<summary><strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

**Kind**: experiment | **Priority**: high

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

</details>

<details>
<summary><strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

**Kind**: evaluation | **Priority**: medium

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

<details>
<summary><strong>Re-download Wang2023 PDF and verify the verbatim PS+ prompt
text</strong> (S-0007-04)</summary>

**Kind**: evaluation | **Priority**: low

The PS+ instruction string in scope_unaware_planandsolve_v1 was sourced through the t0002
paper summary, which was itself grounded only in the abstract because the PDF download failed
in t0002. A small download-paper task should re-attempt the download against arXiv:2305.04091
and verify that the prompt text in code/planandsolve.py matches the published version
verbatim. If it diverges, file a correction.

</details>

## Research

* [`research_papers.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/results/results_summary.md)*

--- spec_version: "2" task_id: "t0007_scope_unaware_planandsolve_library" date_completed:
"2026-04-29" ---
# Results Summary — t0007_scope_unaware_planandsolve_library

## Summary

Produced one library asset, `scope_unaware_planandsolve_v1`, that adapts LangChain's
Plan-and-Execute reference implementation of Wang et al.'s Plan-and-Solve prompting (arXiv
2305.04091) as the canonical scope-unaware (B) baseline for the project. The library passes
its asset verificator and a 14-case pytest suite, all without any paid API calls.

## Metrics

* **Library tests passing**: **14 / 14** (zero failures)
* **Ruff errors on task code**: **0**
* **Mypy errors on task code**: **0**
* **Library asset verificator errors / warnings**: **0 / 0**
* **API spend**: **$0.00** (deterministic-test mode, no LLM calls)

## Verification

* `uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/` — 14 passed in 0.02s
* `uv run mypy -p tasks.t0007_scope_unaware_planandsolve_library.code` — Success: no issues
* `uv run ruff check tasks/t0007_scope_unaware_planandsolve_library/code/` — All checks passed
* `uv run python -m meta.asset_types.library.verificator --task-id
  t0007_scope_unaware_planandsolve_library` — PASSED — no errors or warnings

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0007_scope_unaware_planandsolve_library/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0007_scope_unaware_planandsolve_library" date_completed:
"2026-04-29" ---
# Results — t0007_scope_unaware_planandsolve_library

## Summary

This task produced the canonical scope-unaware (B) baseline library
`scope_unaware_planandsolve_v1` for the project's A-vs-B-vs-C comparison. The library adapts
the LangChain `langchain_experimental.plan_and_execute` reference implementation of Wang et
al.'s Plan-and-Solve (PS+) prompting (arXiv 2305.04091, ACL 2023) and exposes a
`PlanAndSolveAgent` class whose trajectory record schema is byte-for-byte interchangeable with
sister task t0006's forthcoming `scope_aware_react_v1`. Every trajectory record sets
`granularity = "unspecified"`, which is the operational definition of the B condition. All 14
tests pass; the library asset verificator reports zero errors and zero warnings.

## Methodology

* **Compute**: local-only. All work ran inside the worktree at
  `/Users/anaderi/git/reasoning-scale2-worktrees/t0007_scope_unaware_planandsolve_library` on
  a macOS Darwin 25.3.0 host, Python 3.13.11, with no GPU and no network access required for
  tests.
* **Runtime**: `pytest` reports the 14-case suite at **0.02 s**. End-to-end task wall-clock
  from the resumed `create-branch` step to the final commit was approximately one hour.
* **Timestamps**: task `start_time = 2026-04-29T19:35:48Z`; `end_time` is set in `task.json`
  at the close of the `reporting` step.
* **Tools**: `uv` 0.5.x for environment management; `ruff` and `mypy` for linting; `pytest`
  for testing; `flowmark` for markdown formatting. All command invocations were wrapped in
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

* **Schema dependency on t0006**: this task defines the trajectory schema rather than reusing
  one. Sister task t0006 (running in parallel) must conform when its branch reaches
  implementation. The schema is documented at length in `description.md` `## Trajectory
  Schema` and exposed as `TRAJECTORY_RECORD_FIELDS`. If t0006 lands a different schema, a
  follow-up correction task will be required (see `suggestions.json`).
* **PS+ prompt provenance**: the verbatim PS+ instruction text was sourced from the t0002
  Wang2023 paper summary, which itself was grounded in the abstract because the paper PDF
  download failed in t0002. A Phase 2 evaluation should re-download the paper to confirm the
  prompt text against the published version.
* **Tool registry shape**: the executor expects a flat `dict[str, Callable[[str], str]]`
  registry. Hierarchical tool registries are out of scope for this library and will need a
  follow-up.
* **Error surfacing**: tool errors and unknown-tool conditions are written to the trajectory's
  `observation` field rather than raised as exceptions. Callers that want hard-failure
  semantics must inspect observation strings for the `"ERROR:"` prefix.
* **No live LLM exercise**: the test suite is fully deterministic. The library has been
  exercised against `ScriptedModel` only; no live LLM wiring exists yet — that is a Phase 2
  task.

## Examples

The deliverable is a library, not predictions or LLM completions. Two concrete behaviours of
the library are reproduced below to make the API surface tangible.

### Example 1: Successful end-to-end run with one tool call

Input — the planner's pre-recorded response, the executor's two pre-recorded responses, and
the problem statement:

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

* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` — library
  implementation (about 290 lines).
* `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` — 14-case
  deterministic pytest suite (about 220 lines).
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/details.json`
  — library asset metadata.
* `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/description.md`
  — library description with all 8 mandatory sections plus `## Trajectory Schema` and `##
  License & Attribution`.
* `tasks/t0007_scope_unaware_planandsolve_library/research/research_papers.md` — paper review
  grounded in the t0002 Wang2023 summary.
* `tasks/t0007_scope_unaware_planandsolve_library/plan/plan.md` — eight-step plan with nine
  `REQ-*` items.
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

* **REQ-1** (library asset folder under `assets/library/scope_unaware_planandsolve_v1/`):
  **Done**. Asset exists with `details.json`, `description.md`, and `module_paths` pointing at
  `code/planandsolve.py`. Evidence:
  `tasks/t0007_scope_unaware_planandsolve_library/assets/library/scope_unaware_planandsolve_v1/details.json`;
  asset verificator passes.
* **REQ-2** (`PlanAndSolveAgent` accepts problem, tool registry, and model-call callable):
  **Done**. `PlanAndSolveAgent.__init__(model_call, tool_registry, max_steps,
  granularity_label)` and `.run(problem)`. Evidence: `code/planandsolve.py` lines 230-265.
* **REQ-3** (numbered plan generation + sequential per-step execution): **Done**. The `run()`
  method calls the planner, parses the plan with `parse_plan`, then iterates over plan steps
  calling the executor. Evidence: `test_sequential_execution` passes; `code/planandsolve.py`
  `run` method.
* **REQ-4** (trajectory schema matching `scope_aware_react_v1`): **Done**. `TrajectoryRecord`
  with the canonical six fields plus `TRAJECTORY_RECORD_FIELDS` exposed at module scope.
  Evidence: `test_trajectory_schema_parity` and
  `test_trajectory_record_fields_match_canonical_tuple` pass; the `## Trajectory Schema` block
  in `assets/library/scope_unaware_planandsolve_v1/description.md`.
* **REQ-5** (`granularity == "unspecified"` on every B record): **Done**. The default
  `granularity_label` is `"unspecified"`. Evidence: `test_granularity_unspecified` passes.
* **REQ-6** (deterministic-test mode with pre-recorded outputs): **Done**. `ScriptedModel`
  class. Evidence: `test_scripted_model_round_trip` passes; the entire 14-case suite runs
  without LLM calls.
* **REQ-7** (LangChain Apache-2.0 attribution): **Done**. `## License & Attribution` block in
  `description.md` plus a license note in the module docstring. Evidence:
  `assets/library/scope_unaware_planandsolve_v1/description.md` `## License & Attribution`.
* **REQ-8** (pytest coverage for plan parsing, sequential execution, schema parity, finish
  detection, malformed output): **Done**. 14 named test cases including
  `test_parse_plan_simple`, `test_parse_plan_continuation`, `test_parse_plan_paren_separator`,
  `test_parse_plan_malformed_raises`, `test_sequential_execution`,
  `test_trajectory_schema_parity`, `test_finish_detection_final_answer`,
  `test_malformed_planner_output_propagates`. Evidence: `pytest` reports 14 passed.
* **REQ-9** (trajectory schema documented for sister task t0006): **Done**. The `## Trajectory
  Schema` block in `description.md` provides a field table, JSON example, and Python assertion
  snippet; `TRAJECTORY_RECORD_FIELDS` is exported as the canonical tuple. Evidence:
  `assets/library/scope_unaware_planandsolve_v1/description.md` `## Trajectory Schema`.
* **Out-of-scope items** (A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
  execution): **Confirmed out of scope**. None of these were implemented in this task; they
  are Phase 2 deliverables.

</details>
