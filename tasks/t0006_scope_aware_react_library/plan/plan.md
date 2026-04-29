---
spec_version: "2"
task_id: "t0006_scope_aware_react_library"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Scope-Aware ReAct Library

## Objective

Build a deterministic Python library that extends the canonical ReAct prompting loop with an
explicit `{global, subtask, atomic}` granularity tag at every Thought / Action turn, exposes a JSONL
trajectory writer whose schema both this library and the sister Plan-and-Solve library (t0007) emit,
and provides full pytest coverage that runs without any live LLM call. "Done" means the library
asset under `assets/library/scope_aware_react_v1/` passes `verify_library_asset`, every `REQ-*` item
below is satisfied, and `pytest tasks/t0006_scope_aware_react_library/code/` reports zero failures.

## Task Requirement Checklist

```text
Task name: Scope-aware ReAct library: condition A with explicit granularity tags
Short description: Write-library implementing ReAct extended with explicit granularity tags
                   ({global, subtask, atomic}) for the A condition.

Long description (task_description.md):
The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a {global, subtask, atomic} granularity tag emitted at every Thought / Action
turn, plus a logging hook that records the active tag alongside the model's confidence.

Scope:
- ScopeAwareReactAgent class accepts problem statement, fixed granularity argument, tool
  registry, and a model-call callable.
- Loops Thought / Action / Observation steps, prepending the active granularity tag, parses
  Action JSON until Finish.
- Logs every step's {turn_index, granularity, thought, action, observation, confidence} to a
  JSONL trajectory file.
- Supports a deterministic-test mode that accepts pre-recorded model outputs.
- Pytest coverage covering tag injection, action parsing, finish detection, error recovery on
  malformed JSON, and trajectory logging integrity.

Out of scope: A-vs-B-vs-C experiment, benchmark-specific tool registries, remote-execution wiring.
```

Concrete requirements extracted from the task text:

* **REQ-1** — Implement `ScopeAwareReactAgent` class accepting `problem`, `granularity`,
  `tool_registry`, and `model_call` parameters. Evidence: `code/scope_aware_react.py` exposes the
  class with that signature.
* **REQ-2** — Loop Thought / Action / Observation, prepending the active granularity tag to every
  Thought emission. Evidence: scripted test asserts the granularity tag prefix appears in the prompt
  sent to `model_call` on every turn.
* **REQ-3** — Parse Action JSON and terminate on a `Finish` action. Evidence: scripted test drives
  the agent through several actions until a `Finish` action; agent returns the answer and stops.
* **REQ-4** — Emit one JSONL record per turn with fields
  `{turn_index, granularity, thought, action, observation, confidence}`. Evidence: trajectory file
  content in tests is parsed back and checked field-by-field.
* **REQ-5** — Provide a deterministic-test mode that accepts pre-recorded model outputs. Evidence:
  `ScriptedModel` helper class plus tests that use it.
* **REQ-6** — Tests cover tag injection, action parsing, finish detection, error recovery on
  malformed JSON, and trajectory logging integrity. Evidence: `code/test_scope_aware_react.py` has
  at least one named test per bullet.
* **REQ-7** — Library asset at `assets/library/scope_aware_react_v1/` with `details.json`,
  `description.md`, no `files/` (per spec, code lives in `code/`). Evidence: `verify_library_asset`
  passes.
* **REQ-8** — `description.md` documents the trajectory schema and notes the LangChain ReAct prompt
  attribution under Apache 2.0. Evidence: dedicated sections in `description.md`.
* **REQ-9** — Library is benchmark-agnostic: tool registries are out of scope and supplied by the
  caller. Evidence: `tool_registry: Mapping[str, Callable[..., Any]]` parameter; no benchmark
  imports.
* **REQ-10** — Default-on-missing-tag behaviour: if the model omits a tag, default to `"atomic"` and
  emit a structured warning record into the trajectory log. Evidence: a dedicated test.

Each step in `## Step by Step` references the `REQ-*` items it satisfies.

## Approach

Implement a single Python module `code/scope_aware_react.py` that exposes the `ScopeAwareReactAgent`
class plus a small set of supporting types: `Granularity` (Literal type alias), `TrajectoryRecord`
(`@dataclass(frozen=True, slots=True)`), `MalformedActionError`, and a `ScriptedModel` helper for
deterministic replay. The agent loops over Thought / Action / Observation turns by calling the
injected `model_call(prompt: str) -> str` callable. Each model output is parsed into a
`(thought, action_json, confidence)` triple by a tolerant parser; the action is dispatched through
the tool registry; the resulting observation, the active granularity, the parsed thought, and the
confidence are written to the JSONL trajectory file. Termination is on a `Finish` action.

The prompt is assembled from a system header (granularity instruction), an Apache-2.0 LangChain
ReAct exemplar (verbatim, with attribution stored in `description.md`), the user problem, and the
trajectory-so-far rendered as a Thought/Action/Observation transcript. The granularity tag is
injected into the system header at agent construction time so the model is asked to emit
`<global>`/`<subtask>`/`<atomic>` on every Thought line.

**Alternatives considered**:

* *Subclass an existing LangChain agent.* Rejected: adds a heavy runtime dependency and obscures the
  trajectory-schema contract that t0007 must mirror. Implementing the loop directly keeps the
  library small (~250 lines) and removes any framework drift between A and B.
* *Use OpenAI tool-calling JSON instead of the ReAct text protocol.* Rejected: the project's Phase 2
  evaluator must support open-source models without tool-call fine-tuning, so the text ReAct
  protocol is the lowest common denominator.

**Task types**: `task.json` lists `task_types: ["write-library"]`. The write-library Planning
Guidelines say to define the public API before writing code (done in REQ-1..REQ-5), check existing
library assets (zero exist; this is the project's first library), and keep the library generic (no
benchmark coupling — REQ-9 captures this).

## Cost Estimation

* External API calls: **$0** — every test runs `ScriptedModel` with pre-recorded model outputs.
* Remote compute: **$0** — pure CPU; no GPU.
* Human-time tokens for this orchestration: incurred via the Claude Code session running the task,
  but classified as project overhead, not a per-task line item.

Total task cost: **$0**. Project budget impact: zero. The task type has `has_external_costs: false`
in `meta/task_types/write-library/`, so the budget gate was skipped per the execute-task spec.

## Step by Step

1. **Create `code/paths.py` and `code/constants.py`.** Define `TASK_ROOT`, `LIBRARY_ASSET_DIR`,
   `DEFAULT_TRAJECTORY_PATH` in `paths.py`; define granularity literals
   (`GRANULARITY_GLOBAL = "global"`, etc.), trajectory schema field names, parser sentinels
   (`THOUGHT_PREFIX = "Thought:"`, etc.), and the default tag-missing warning string in
   `constants.py`. Inputs: none. Outputs: two new modules. Satisfies REQ-1, REQ-9.
2. **Implement `code/scope_aware_react.py`.** Define `Granularity` (TypeAlias), `Action`
   (@dataclass), `TrajectoryRecord` (@dataclass, frozen, slots), `MalformedActionError`,
   `ScopeAwareReactAgent` with
   `__init__(problem, granularity, tool_registry, model_call, trajectory_path, max_turns=20, default_granularity_on_missing_tag="atomic")`
   and `run()`, `ScriptedModel`, plus a private
   `_parse_model_output(raw: str) -> (thought, action, confidence)` helper. Inputs: imports from
   `code.constants` and `code.paths`. Outputs: one new module (~250 lines). Satisfies REQ-1, REQ-2,
   REQ-3, REQ-5, REQ-10.
3. **Implement the JSONL trajectory writer inside the agent.** Open the trajectory file in `"w"`
   mode at agent start, write one record per turn via `json.dumps(asdict(record))` followed by
   `"\n"` and `flush()`, close on `__exit__`. Inputs: `pathlib.Path`. Outputs: trajectory file
   appended during `run()`. Satisfies REQ-4.
4. **Implement `code/test_scope_aware_react.py`.** Write at least seven named tests:
   `test_tag_injection_in_prompt`, `test_action_parsing_round_trip`, `test_finish_terminates_loop`,
   `test_malformed_action_recovery`, `test_trajectory_log_schema`,
   `test_missing_tag_defaults_to_atomic`, `test_max_turns_safety_cap`. Use `tmp_path` fixture for
   the trajectory file. Inputs: `pytest`, the library module. Outputs: passing test file. Satisfies
   REQ-6.
5. **Run quality checks.** Execute `uv run ruff check --fix .`, `uv run ruff format .`,
   `uv run mypy -p tasks.t0006_scope_aware_react_library.code`, and
   `uv run pytest tasks/t0006_scope_aware_react_library/code/ -v`. Validation gate: zero ruff
   errors, zero mypy errors, all tests passing. If any test fails, halt and inspect the trajectory
   output and prompt strings before retrying. Satisfies REQ-6.
6. **Create the library asset folder.** Write `assets/library/scope_aware_react_v1/details.json` per
   `meta/asset_types/library/specification.md` v2, with `module_paths` listing
   `code/scope_aware_react.py`, `code/constants.py`, `code/paths.py`; `entry_points` for
   `ScopeAwareReactAgent`, `ScriptedModel`, `TrajectoryRecord`, `MalformedActionError`; `test_paths`
   listing `code/test_scope_aware_react.py`; `categories` set to `granularity-conditioning`,
   `agent-evaluation`. Satisfies REQ-7.
7. **Write `assets/library/scope_aware_react_v1/description.md`.** Cover all mandatory sections from
   the v2 spec (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing, Main
   Ideas, Summary). The API Reference must document every entry point. Include a dedicated
   `### Trajectory Log Schema` subsection inside API Reference. Note the LangChain ReAct prompt
   attribution under Apache-2.0 in Dependencies. Satisfies REQ-7, REQ-8.
8. **Run `verify_library_asset` for `scope_aware_react_v1`.** Execute
   `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0006_scope_aware_react_library scope_aware_react_v1`.
   Validation gate: zero LA-E errors. Warnings on word counts may be addressed by adding prose where
   flagged. Satisfies REQ-7.

## Remote Machines

None required. This is a deterministic library task with all tests running on local CPU.

## Assets Needed

* No paper assets directly imported, but the trajectory schema and prompt template are grounded in
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/`
  (Yao2022) per `research/research_papers.md`.
* No prior library assets (zero registered). Style and layout mirrored from
  `tasks/t0003_download_benchmark_subsets/code/`.

## Expected Assets

* **Library asset** `scope_aware_react_v1` at `assets/library/scope_aware_react_v1/` containing
  `details.json` and `description.md` per `meta/asset_types/library/specification.md` v2. Backs the
  task's declared `expected_assets.library: 1`.

## Time Estimation

* Implementation (steps 1-3): ~30 minutes.
* Tests (step 4): ~20 minutes.
* Quality checks (step 5): ~5 minutes.
* Asset folder + description (steps 6-7): ~20 minutes.
* Verification (step 8): ~5 minutes.
* Wall-clock total: ~1.5 hours of agent-driven work.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Trajectory schema drifts from t0007 | Medium | Phase 2 cannot ingest both | Lock the schema in `description.md` and tests; this PR lands first or t0007 mirrors it. Either order works. |
| `ScriptedModel` masks parser bugs that real LLM output would surface | Medium | Hidden runtime errors | Include malformed-JSON test cases drawn from real-LLM failure modes ([Yao2022] reports these); document the parser's tolerance contract in `description.md`. |
| `verify_library_asset` rejects `description.md` for missing sections | Medium | Cannot ship asset | Re-read the v2 spec before writing; run the verificator iteratively; fix word-count warnings promptly. |
| LangChain prompt attribution gets dropped during edits | Low | Apache-2.0 NOTICE not propagated | Put the attribution in `description.md` Dependencies section AND as a top-of-file comment in `code/scope_aware_react.py`. |
| `mypy` complains about `Callable` shape for `model_call` | Low | Cannot commit | Type as `Callable[[str], str]`; if the user wants async, that is a follow-up suggestion. |

## Verification Criteria

* `uv run python -m arf.scripts.utils.run_with_logs --task-id t0006_scope_aware_react_library -- uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0006_scope_aware_react_library scope_aware_react_v1`
  exits 0 with no LA-E errors.
* `uv run pytest tasks/t0006_scope_aware_react_library/code/ -v` reports all tests passing (target:
  7+ tests).
* `uv run ruff check tasks/t0006_scope_aware_react_library/code/` and
  `uv run ruff format --check tasks/t0006_scope_aware_react_library/code/` exit 0.
* `uv run mypy -p tasks.t0006_scope_aware_react_library.code` exits 0.
* `assets/library/scope_aware_react_v1/details.json` contains `module_paths` pointing at
  `code/scope_aware_react.py`, `code/constants.py`, `code/paths.py` and `entry_points` covering
  `ScopeAwareReactAgent`, `ScriptedModel`, `TrajectoryRecord`, `MalformedActionError`.
* `description.md` contains an explicit `Trajectory Log Schema` subsection with the
  `{turn_index, granularity, thought, action, observation, confidence}` field listing — this is the
  contract that t0007 must mirror. Direct check for REQ-8.
* The trajectory file produced by a sample test run contains exactly one JSON record per turn,
  parses cleanly, and has all six schema fields per record. Direct check for REQ-4.
