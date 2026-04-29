---
spec_version: "2"
task_id: "t0006_scope_aware_react_library"
---
# Results Detailed: Scope-Aware ReAct Library

## Summary

Implemented the project's first library asset, `scope_aware_react_v1`, which extends the canonical
ReAct prompting loop ([Yao2022]) with explicit `{global, subtask, atomic}` granularity tags and a
JSONL trajectory writer. The library is benchmark-agnostic, has zero third-party runtime
dependencies, and ships an 8-test deterministic test suite that runs without any live API call. The
trajectory schema is the canonical contract between this library and the sister Plan-and-Solve
library (`t0007_scope_unaware_planandsolve_library`).

## Methodology

* **Machine**: macOS Darwin 25.3.0 on Apple Silicon (local CPU); no GPU.
* **Python**: 3.13.11 (`uv run` against the project's lockfile).
* **Runtime**: Approximately 70 minutes of Claude Code orchestration end-to-end, covering 6 active
  steps (plus 5 skipped). The pytest suite itself runs in **0.03 s**.
* **Started**: 2026-04-29T19:35:48Z (`task.start_time`).
* **Completed (results step)**: 2026-04-29T20:03:12Z.
* **Approach**: Implemented a single Python module exposing `ScopeAwareReactAgent` plus supporting
  dataclasses (`Action`, `TrajectoryRecord`, `AgentResult`, `ParsedOutput`), `ScriptedModel` for
  deterministic tests, a tolerant output parser, and an explicit-flush JSONL writer. The prompt
  template was assembled from a system header (granularity instruction literally including
  `<global>` / `<subtask>` / `<atomic>` examples), the user problem, and a rendered Thought / Action
  / Observation transcript. Apache-2.0 attribution to LangChain's ReAct prompt is stored as a
  constant in `code/constants.py` and is included in every system prompt.
* **Test approach**: Each of the 8 tests injects a `ScriptedModel` whose script is hand-curated to
  exercise one path: tag injection, action parsing, finish termination, malformed-JSON recovery,
  schema integrity, missing-tag fallback, max-turns cap, unknown-tool handling. No live LLM call is
  made.

## Verification

* `meta.asset_types.library.verificator --task-id t0006_scope_aware_react_library scope_aware_react_v1`
  — PASSED (0 errors, 0 warnings).
* `verify_research_papers t0006_scope_aware_react_library` — PASSED.
* `verify_research_code t0006_scope_aware_react_library` — PASSED.
* `verify_plan t0006_scope_aware_react_library` — PASSED.
* `pytest tasks/t0006_scope_aware_react_library/code/ -v` — 8 / 8 tests pass in 0.03 s.
* `ruff check tasks/t0006_scope_aware_react_library/code/` — 0 errors.
* `ruff format` — no changes after the initial autoformat.
* `mypy -p tasks.t0006_scope_aware_react_library.code` — Success: no issues found.

The pre-merge verificator (`verify_pr_premerge`) is run as part of the reporting step.

## Limitations

* The agent is **synchronous and single-threaded**; it does not support concurrent tool calls or
  streaming model output. Phase 2 experiments that need parallel tool invocations will need to
  extend this library or wrap it in an async adapter.
* The output parser assumes **English-language `Thought:` / `Action:` / `Confidence:` prefixes** and
  the literal angle-bracket tag format. Models that systematically deviate from this convention
  (e.g., "Reasoning:" instead of "Thought:") will fall through to the missing-tag default and
  produce poorer-quality trajectories.
* **Confidence is a single scalar per turn**. Per-claim confidence breakdowns are not supported;
  this matches the project Phase 2 stance from `[t0004]` brainstorming.
* The library supports a **fixed granularity for the entire run**. Experiments that vary granularity
  within one run (e.g., start global, drop to atomic mid-run) require either multiple agent
  instances run sequentially or a future extension. This limitation is captured in
  `results/suggestions.json`.
* No **benchmark-specific tool registries** are bundled with this library. Phase 2 tasks that target
  FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, or tau-bench need to provide their own
  `tool_registry` mapping. This is intentional per the task description's "Out of scope" clause.
* The library has **not been exercised against a real LLM yet**. The `ScriptedModel` pattern
  guarantees parser/loop correctness against pre-recorded inputs, but live-model behaviour
  (especially around the missing-tag fallback rate) is a Phase 2 unknown.

## Files Created

* `tasks/t0006_scope_aware_react_library/code/paths.py` — module-level `Path` constants.
* `tasks/t0006_scope_aware_react_library/code/constants.py` — granularity literals, schema field
  names, parser sentinels, LangChain attribution string.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` — main library module (~370
  lines).
* `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` — 8 deterministic tests.
* `tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/details.json` — library
  asset metadata (spec v2).
* `tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/description.md` —
  canonical library documentation including the Trajectory Log Schema subsection.
* `tasks/t0006_scope_aware_react_library/research/research_papers.md` — synthesis across Yao2022,
  Wang2023a, Zhou2022, Xiong2023.
* `tasks/t0006_scope_aware_react_library/research/research_code.md` — survey of prior task outputs.
* `tasks/t0006_scope_aware_react_library/plan/plan.md` — eleven-section plan with 10 REQ items.
* `tasks/t0006_scope_aware_react_library/results/results_summary.md` — this task's headline
  outcomes.
* `tasks/t0006_scope_aware_react_library/results/results_detailed.md` — this file.
* `tasks/t0006_scope_aware_react_library/results/metrics.json` — empty (no registered metrics
  measured).
* `tasks/t0006_scope_aware_react_library/results/costs.json` —
  `{"total_cost_usd": 0, "breakdown": {}}`.
* `tasks/t0006_scope_aware_react_library/results/remote_machines_used.json` — `[]`.
* Step logs at `tasks/t0006_scope_aware_react_library/logs/steps/NNN_<step>/step_log.md` for every
  active and skipped step.

## Trajectory Log Schema (Sister-Task Contract)

The library writes one JSONL record per turn with the six canonical fields. This is the load-
bearing artifact for the Phase 2 evaluator and the contract that t0007 mirrors:

| Field | Type | Source |
| --- | --- | --- |
| `turn_index` | int | `FIELD_TURN_INDEX` constant in `constants.py`. |
| `granularity` | str | One of `GRANULARITY_VALUES` in `constants.py`. |
| `thought` | str | Free-form Thought (tag stripped). |
| `action` | dict | `{"name": str, "args": dict[str, Any]}`; `name == "Finish"` terminates. |
| `observation` | str | Tool output or `<parse_error>` / `<unknown_tool>` / `<tag_missing_defaulted_to_atomic>` marker. |
| `confidence` | float \| null | Verbalized confidence in `[0.0, 1.0]`. |

t0007 (Plan-and-Solve, condition B) emits records of identical shape with `granularity` set to
`"subtask"` for every record, so the Phase 2 evaluator can ingest A and B trajectories with one
parser. If t0007 lands first, this library adopts whatever schema it ships; if t0006 lands first,
t0007 mirrors the schema documented above. Either landing order is acceptable per the original task
brief.

## Task Requirement Coverage

Operative task text (verbatim from `task.json` and `task_description.md`):

```text
Name: Scope-aware ReAct library: condition A with explicit granularity tags

Short description: Write-library implementing ReAct extended with explicit granularity tags
({global, subtask, atomic}) for the A condition.

Long description (task_description.md):
The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a {global, subtask, atomic} granularity tag emitted at every Thought / Action
turn, plus a logging hook that records the active tag alongside the model's confidence. The
library is the substrate every Phase 2 A-condition experiment will import. Implements suggestion
S-0002-07.

Scope:
- ScopeAwareReactAgent class accepting a problem, a fixed granularity argument, a tool
  registry, and a model-call callable.
- Loops Thought / Action / Observation steps, prepending the active granularity tag, parses
  Action JSON until Finish.
- Logs every step's {turn_index, granularity, thought, action, observation, confidence} to a
  JSONL trajectory file.
- Supports a deterministic-test mode that accepts pre-recorded model outputs.
- Pytest coverage covering tag injection, action parsing, finish detection, error recovery on
  malformed JSON, and trajectory logging integrity.

Out of scope: A-vs-B-vs-C experiment, benchmark-specific tool registries, remote-execution
wiring.
```

| ID | Requirement | Status | Result | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | `ScopeAwareReactAgent` accepts `problem`, `granularity`, `tool_registry`, `model_call`. | Done | Class signature matches. | `code/scope_aware_react.py` lines defining `ScopeAwareReactAgent.__init__`. |
| REQ-2 | Loop prepends granularity tag to every Thought; tag injected into prompt. | Done | System prompt includes `<{granularity}>` literal. | `code/scope_aware_react.py` `_build_system_prompt`; test `test_tag_injection_in_prompt`. |
| REQ-3 | Action JSON parsed until `Finish`. | Done | Finish action terminates the loop and returns answer. | Tests `test_action_parsing_round_trip`, `test_finish_terminates_loop`. |
| REQ-4 | JSONL record per turn with six canonical fields. | Done | `TrajectoryWriter` writes ordered six-field dicts. | `code/scope_aware_react.py` `TrajectoryWriter.write`; test `test_trajectory_log_schema`. |
| REQ-5 | Deterministic-test mode replaying pre-recorded outputs. | Done | `ScriptedModel` helper. | `code/scope_aware_react.py` `ScriptedModel`; used by all 8 tests. |
| REQ-6 | Tests cover tag injection, action parsing, finish, malformed JSON, trajectory log. | Done | 8 named tests, all passing. | `code/test_scope_aware_react.py` (`pytest -v` output recorded in `logs/commands/010_*`). |
| REQ-7 | Library asset at `assets/library/scope_aware_react_v1/`. | Done | Asset folder with `details.json` and `description.md`; verificator passed. | `assets/library/scope_aware_react_v1/`; verificator log at `logs/commands/012_*`. |
| REQ-8 | `description.md` documents trajectory schema and Apache-2.0 attribution. | Done | `## API Reference -> ### Trajectory Log Schema` and `## Dependencies` Apache-2.0 paragraph. | `assets/library/scope_aware_react_v1/description.md`. |
| REQ-9 | Library is benchmark-agnostic; tool registries injected. | Done | `tool_registry: Mapping[str, Callable[..., Any]]` is a constructor parameter; no benchmark imports. | `code/scope_aware_react.py` `ScopeAwareReactAgent.__init__`; type alias `ToolRegistry`. |
| REQ-10 | Default-on-missing-tag falls back to `atomic` and emits warning. | Done | `OBSERVATION_TAG_MISSING_WARNING` prefix; default literal `"atomic"`. | `code/scope_aware_react.py` `default_granularity_on_missing_tag`; test `test_missing_tag_defaults_to_atomic`. |

All 10 REQ items are `Done`. No partial or blocked items.
