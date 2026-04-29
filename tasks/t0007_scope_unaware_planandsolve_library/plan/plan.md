---
spec_version: "2"
task_id: "t0007_scope_unaware_planandsolve_library"
date_completed: "2026-04-29"
status: "complete"
---
## Objective

Produce a Python library asset that adapts the LangChain Plan-and-Execute reference implementation
of Wang et al.'s Plan-and-Solve (PS) prompting [Wang2023] as the canonical scope-unaware (B)
baseline for the project's A-vs-B-vs-C comparison. The library exposes a `PlanAndSolveAgent` class
with a deterministic-test mode and emits trajectory records whose schema is interchangeable with the
scope-aware (A) library produced by sister task t0006. Done is: an `assets/library/` entry that
passes `verify_library_asset`, a `code/planandsolve.py` module plus tests, and trajectory records
whose `granularity` field is the literal string `"unspecified"`.

## Task Requirement Checklist

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
>
> Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote execution.

The concrete requirements decomposed:

* **REQ-1**: Library asset under `assets/library/scope_unaware_planandsolve_v1/` with
  `details.json`, `description.md`, and `module_paths` referencing `code/planandsolve.py`. Satisfied
  by Step 5; evidence: `verify_library_asset` passes.
* **REQ-2**: `PlanAndSolveAgent` class accepting `(problem, tool_registry, model_call)` and a
  deterministic-test entry point. Satisfied by Steps 1-4; evidence: `pytest`-tested constructor.
* **REQ-3**: Free-form numbered plan generation followed by sequential per-step execution
  (Plan-and-Execute loop). Satisfied by Steps 1, 3; evidence: `test_sequential_execution`.
* **REQ-4**: Trajectory record schema with fields
  `{turn_index, granularity, thought, action, observation, confidence}` matching the t0006
  scope-aware (A) library. Satisfied by Step 2; evidence: `test_trajectory_schema_parity` and the
  `TRAJECTORY_RECORD_FIELDS` constant exported for t0006 to import.
* **REQ-5**: `granularity` is the literal string `"unspecified"` on every B-condition record.
  Satisfied by Step 4; evidence: `test_granularity_unspecified`.
* **REQ-6**: Deterministic-test mode accepting pre-recorded model outputs. Satisfied by Step 4
  (`ScriptedModel`); evidence: `test_scripted_model_round_trip`.
* **REQ-7**: Adapt LangChain Plan-and-Execute (Apache-2.0) and record attribution. Satisfied by Step
  3 prompt adoption and Step 5 description authorship; evidence: `## License & Attribution` section
  in `description.md`.
* **REQ-8**: Plan parsing test, sequential execution test, schema parity test, finish detection
  test, malformed-output recovery test, all under `code/test_planandsolve.py`. Satisfied by Step 6;
  evidence: at least 5 named pytest cases pass.
* **REQ-9**: Document the trajectory schema clearly so sister task t0006 can conform when its branch
  reaches implementation. Satisfied by Step 5 in `description.md` `## Trajectory Schema` section;
  evidence: schema table plus example JSON record.

## Approach

The library mirrors the LangChain Plan-and-Execute structure: (1) a planner LLM produces a numbered
plan as free-form text, (2) a parser splits the plan into ordered steps using a regex over
`^\s*\d+[\.\)]\s+(.+)$`, (3) an executor LLM runs each step in turn, and (4) the loop terminates
when the plan is exhausted or the executor emits a `FINAL_ANSWER:` token. Wang2023's PS+ prompt is
adopted verbatim as the planner prompt. Tools are passed as a registry mapping
`name -> callable(args_text) -> observation_text`; the executor produces lines in the form
`Action: <tool_name> | Args: <args>` or `FINAL_ANSWER: <text>`. Every step is logged as a trajectory
record with `granularity = "unspecified"`.

The trajectory schema is a frozen dataclass `TrajectoryRecord` with fields
`{turn_index: int, granularity: str, thought: str, action: str, observation: str, confidence: float | None}`,
matching the A-condition record so a Phase 2 harness can swap libraries by changing one import line.
The library exports the field tuple as `TRAJECTORY_RECORD_FIELDS` so t0006 can import-and-assert.

The deterministic-test mode is a `ScriptedModel` callable that returns pre-recorded responses from a
list, advancing on every call. This eliminates LLM cost during testing and is sufficient for the
five required pytest cases.

**Alternatives considered**: (a) Re-implementing PS from scratch — rejected because the LangChain
reference is widely known, Apache-2.0 licensed, and adapting it preserves provenance; (b) Defining
the trajectory schema as a Pydantic model — rejected because the project Python style prefers stdlib
`@dataclass(frozen=True, slots=True)` for internal data, with Pydantic only at I/O boundaries; (c)
Tool registry as a class hierarchy — rejected for simplicity, a flat dict of callables is enough for
the deterministic-test surface this library exposes.

**Task type**: `write-library`. The Planning Guidelines for `write-library` emphasize a small,
focused API with explicit `module_paths` and `entry_points`; this plan follows that guidance.

## Cost Estimation

Total cost: **$0**. The library is a deterministic Python module; tests use a `ScriptedModel` fake.
No paid API calls, no GPU compute, no external data downloads. The project budget is not moved by
this task.

## Step by Step

1. **Define the trajectory record dataclass.** Create `code/planandsolve.py` and write a
   `@dataclass(frozen=True, slots=True)` `TrajectoryRecord` with fields `turn_index: int`,
   `granularity: str`, `thought: str`, `action: str`, `observation: str`,
   `confidence: float | None`. Export `TRAJECTORY_RECORD_FIELDS: tuple[str, ...]` listing the field
   names in order. Expected output: importable dataclass; `mypy` passes. Satisfies REQ-4.

2. **Write the model-call protocol and ScriptedModel.** In the same module, define a
   `ModelCall = Callable[[str], str]` type alias and a `ScriptedModel` class wrapping a `list[str]`
   of pre-recorded responses, raising `IndexError` when exhausted. The `ScriptedModel` is callable
   `(prompt) -> response`. Expected output: `ScriptedModel(["a", "b"])("ignored")` returns `"a"`,
   then `"b"`. Satisfies REQ-6.

3. **Write the plan parser and PS+ prompt constants.** Add `PLAN_PROMPT_TEMPLATE` (verbatim PS+
   prompt followed by a problem placeholder) and `EXECUTE_PROMPT_TEMPLATE` (problem + plan +
   completed-step log + current step + tool list + instruction to emit
   `Action: <tool> | Args: <args>` or `FINAL_ANSWER: <text>`). Implement
   `parse_plan(text: str) -> list[str]` using `re.compile(r"^\s*\d+[\.\)]\s+(.+)$", re.MULTILINE)`.
   Lines that do not match the regex are appended to the previous step. Raise `MalformedPlanError`
   if the parser yields zero steps. Expected: `parse_plan("1. a\n2. b")` returns `["a", "b"]`.
   Satisfies REQ-3, REQ-7.

4. **Write the agent class.** Implement
   `PlanAndSolveAgent.__init__(self, model_call: ModelCall, tool_registry: dict[str, Callable[[str], str]], max_steps: int = 32, granularity_label: str = "unspecified")`.
   The class exposes `run(problem: str) -> AgentResult` where `AgentResult` is a frozen dataclass
   with `final_answer: str | None`, `trajectory: list[TrajectoryRecord]`, and `plan: list[str]`. The
   `run()` method (i) calls the model with `PLAN_PROMPT_TEMPLATE.format(problem=problem)` to get the
   plan text, (ii) parses the plan with `parse_plan`, (iii) iterates over plan steps appending
   trajectory records as `model_call` is invoked, parses the executor's line for the action, runs
   the tool from the registry (or records `observation = ""` if no tool was needed), and (iv) stops
   when the executor emits `FINAL_ANSWER:` or the plan is exhausted (also stops at `max_steps`).
   Every record sets `granularity = "unspecified"` (`granularity_label`). Satisfies REQ-2, REQ-3,
   REQ-5.

5. **Author the asset description and details.** Create
   `assets/library/scope_unaware_planandsolve_v1/details.json` with
   `library_id = "scope_unaware_planandsolve_v1"`, `module_paths = ["code/planandsolve.py"]`,
   `test_paths = ["code/test_planandsolve.py"]`, `entry_points` listing `PlanAndSolveAgent`,
   `ScriptedModel`, `TrajectoryRecord`, `parse_plan`, and `TRAJECTORY_RECORD_FIELDS`. Set
   `description_path = "description.md"`. Categories:
   `["hierarchical-planning", "granularity-conditioning"]`. Then write `description.md` with all 8
   mandatory sections (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing,
   Main Ideas, Summary) plus a `## Trajectory Schema` block (REQ-9), a `## License & Attribution`
   block crediting the LangChain Plan-and-Execute reference under Apache-2.0 (REQ-7), and the
   verbatim PS+ prompt. Satisfies REQ-1, REQ-7, REQ-9.

6. **Write the tests and run them.** Create `code/test_planandsolve.py` with at least these cases:
   `test_parse_plan_simple`, `test_parse_plan_continuation`, `test_parse_plan_malformed`,
   `test_scripted_model_round_trip`, `test_sequential_execution`, `test_trajectory_schema_parity`,
   `test_granularity_unspecified`, `test_finish_detection_final_answer`. Run
   `uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/`. Expected: all tests pass
   with zero failures. Satisfies REQ-8.

7. **Run quality gates.** Run
   `uv run ruff check --fix tasks/t0007_scope_unaware_planandsolve_library/code/`,
   `uv run ruff format tasks/t0007_scope_unaware_planandsolve_library/code/`, and
   `uv run mypy -p tasks.t0007_scope_unaware_planandsolve_library.code`. Expected: zero ruff errors
   and zero mypy errors.

8. **Run the library asset verificator.**
   `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0007_scope_unaware_planandsolve_library`.
   Expected: zero errors.

## Remote Machines

None required. The library is a deterministic local Python module with deterministic tests that do
not touch any network or GPU.

## Assets Needed

* The Wang2023 paper summary at
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/summary.md`
  for prompt grounding.
* The library asset specification at `meta/asset_types/library/specification.md` for asset format.

## Expected Assets

* `assets/library/scope_unaware_planandsolve_v1/` (one library asset). `library_id` is
  `scope_unaware_planandsolve_v1`. Description: scope-unaware Plan-and-Solve agent, Phase 2 baseline
  B, with trajectory schema interchangeable with t0006's `scope_aware_react_v1`.

This matches `task.json` `expected_assets: {"library": 1}`.

## Time Estimation

Implementation (Steps 1-4): ~30 minutes. Description authoring (Step 5): ~15 minutes. Tests and
quality gates (Steps 6-7): ~10 minutes. Library asset verification (Step 8): ~2 minutes. Total
wall-clock: roughly one hour.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| t0006 sister task lands a different trajectory schema before merge | Medium | Schema mismatch forces a follow-up correction | Document the schema in this task's `description.md` clearly, and in this task's results suggest a follow-up dedup task if t0006 disagrees; merge conflicts on `task.json` are resolved by keeping the task branch version. |
| LangChain Plan-and-Execute reference behaves slightly differently from the published Wang2023 prompt | Low | Minor prompt drift; no functional impact | Adopt the PS+ prompt verbatim from the paper abstract rather than copying LangChain's variant; record both verbatim in `description.md`. |
| `parse_plan` mis-handles unusual model output (Roman numerals, bullet points) | Low | Plan-step extraction returns the wrong list | Tests cover the malformed-plan path; raising `MalformedPlanError` lets the caller decide whether to retry. |
| Asset folder layout misalignment with the v2 library spec | Low | Verificator failure | Read `meta/asset_types/library/specification.md` before authoring and re-run `verify_library_asset` after each edit. |

## Verification Criteria

* `uv run pytest tasks/t0007_scope_unaware_planandsolve_library/code/` — all tests pass with zero
  failures and at least 8 named test cases (covering REQ-3 through REQ-8).
* `uv run mypy -p tasks.t0007_scope_unaware_planandsolve_library.code` — zero errors.
* `uv run ruff check tasks/t0007_scope_unaware_planandsolve_library/code/` — zero errors.
* `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0007_scope_unaware_planandsolve_library`
  — zero errors.
* `assets/library/scope_unaware_planandsolve_v1/details.json` exists with
  `library_id = "scope_unaware_planandsolve_v1"`, `description_path = "description.md"`, and
  `module_paths` referencing the existing `code/planandsolve.py`.
* `assets/library/scope_unaware_planandsolve_v1/description.md` exists, contains all 8 mandatory
  sections, the `## Trajectory Schema` block (covering REQ-9), and the `## License & Attribution`
  block (covering REQ-7), and is at least 400 words.
* Every trajectory record produced by `PlanAndSolveAgent.run()` has `granularity == "unspecified"`
  (asserted in `test_granularity_unspecified`, covering REQ-5).
