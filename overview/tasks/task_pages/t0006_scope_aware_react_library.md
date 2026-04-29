# ✅ Scope-aware ReAct library: condition A with explicit granularity tags

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | ✅ completed |
| **Started** | 2026-04-29T19:35:38Z |
| **Completed** | 2026-04-29T20:07:30Z |
| **Duration** | 31m |
| **Source suggestion** | `S-0002-07` |
| **Task types** | `write-library` |
| **Categories** | [`agent-evaluation`](../../by-category/agent-evaluation.md), [`granularity-conditioning`](../../by-category/granularity-conditioning.md) |
| **Expected assets** | 1 library |
| **Step progress** | 10/15 |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../../tasks/t0006_scope_aware_react_library/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0006_scope_aware_react_library/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0006_scope_aware_react_library/task_description.md)*

# Scope-Aware ReAct Library (Condition A)

## Motivation

The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a `{global, subtask, atomic}` granularity tag emitted at every Thought /
Action turn, plus a logging hook that records the active tag alongside the model's confidence.
The library is the substrate every Phase 2 A-condition experiment will import. Implements
suggestion S-0002-07.

## Scope

* Implement a library asset under `assets/library/scope_aware_react_v1/` exposing a
  `ScopeAwareReactAgent` class that:
  * Accepts a problem statement, a fixed `granularity` argument (`"global" | "subtask" |
    "atomic"`), a tool registry, and a model-call callable.
  * Loops Thought / Action / Observation steps, prepending the active granularity tag to every
    Thought emission, and parses Action JSON until the agent emits a `Finish` action.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}` to
    a JSONL trajectory file the experiment harness can replay.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` covering: tag
  injection, action parsing, finish detection, error recovery on malformed JSON, and
  trajectory logging integrity.

Out of scope: the actual A-vs-B-vs-C experiment (a separate experiment-run task), benchmark-
specific tool registries (also a separate task), and any remote-execution wiring.

## Approach

1. Read t0002's `research/research_papers.md` and the Yao2022 paper summary to ground the
   prompt format. Reuse LangChain's ReAct prompt where appropriate; the project licence is
   Apache 2.0.
2. Implement the library in `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`
   and re-export the public API from a `library/__init__.py` shim under `assets/library/
   scope_aware_react_v1/`.
3. Write the asset's `details.json`, `description.md`, and `files/` directory with the
   runnable source.
4. Write tests as deterministic unit tests; no live API calls.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_aware_react_v1/` with `details.json`, `description.md`, and `files/`.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` and matching test file.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for benchmark-specific tool registries.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Yao2022 paper asset (`10.48550_arXiv.2210.03629`) from t0002.
* Sister task `t0007_scope_unaware_planandsolve_library` produces the matched B baseline; both
  must follow the same trajectory-logging schema so a Phase 2 experiment can consume both.

## Source Suggestion

S-0002-07 — "Implement scope-aware (A) as ReAct extended with explicit granularity tags."

## Key Questions

1. What is the minimal extension to ReAct's prompt template that reliably elicits a
   granularity tag on every Thought emission?
2. How should the library handle a model that refuses to emit a tag (back off, abort, or
   default to `atomic`)?
3. What schema for the trajectory log lets t0007 emit identical-shape records?

</details>

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Scope-Aware ReAct Agent](../../../tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/) | [`description.md`](../../../tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/description.md) |

## Suggestions Generated

<details>
<summary><strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

**Kind**: library | **Priority**: high

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>

<details>
<summary><strong>Add an async ScopeAwareReactAgent variant for streaming and
parallel tool calls</strong> (S-0006-02)</summary>

**Kind**: library | **Priority**: medium

The current agent is synchronous. Phase 2 experiments at scale will benefit from streaming
model output and from issuing multiple independent tool calls concurrently within a single
Thought block. Build async_scope_aware_react.py exposing AsyncScopeAwareReactAgent with an
async model_call signature and asyncio.gather over Action lists. Tests should use
AsyncScriptedModel mirroring the sync helper.

</details>

<details>
<summary><strong>Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience
subset</strong> (S-0006-03)</summary>

**Kind**: experiment | **Priority**: high

scope_aware_react_v1 (A) and the in-progress scope_unaware_planandsolve_v1 (B) are now ready
as substrates. Run a controlled experiment on the t0003 FrontierScience subset with both
libraries plus a no-prompt-engineering baseline (C), measuring task_success_rate,
overconfident_error_rate, and avg_decisions_per_task across N=50 problems. Expected effect
size: +5 to +15 absolute success rate for A over B based on the Yao2022 ALFWorld result
anchor.

</details>

<details>
<summary><strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

**Kind**: evaluation | **Priority**: medium

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary><strong>Extend the library to support a granularity that varies within
a single run</strong> (S-0006-05)</summary>

**Kind**: technique | **Priority**: low

Currently ScopeAwareReactAgent takes one fixed granularity for an entire run. A natural
extension is to let the agent emit a granularity transition (e.g., start global, drop to
subtask once a plan is established, drop to atomic during execution). Add a model-driven mode
where the parser also accepts <transition_to:subtask> markers and the agent updates the active
granularity per turn. This is a research extension worth Phase 2 ablation.

</details>

## Research

* [`research_code.md`](../../../tasks/t0006_scope_aware_react_library/research/research_code.md)
* [`research_papers.md`](../../../tasks/t0006_scope_aware_react_library/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0006_scope_aware_react_library/results/results_summary.md)*

# Results Summary: Scope-Aware ReAct Library

## Summary

Shipped the project's first library asset: `scope_aware_react_v1`, implementing condition A
(scope-aware ReAct) with explicit `{global, subtask, atomic}` granularity tags, a JSONL
trajectory writer whose six-field schema is the canonical contract for both this library and
t0007, and deterministic-replay testing via `ScriptedModel`. All quality gates clean and the
asset verificator passed.

## Metrics

* **Library asset**: 1 (`scope_aware_react_v1`), passes `meta.asset_types.library.verificator`
  with **0 errors / 0 warnings**.
* **Tests**: **8 / 8** passing in `code/test_scope_aware_react.py` (`pytest
  tasks/t0006_scope_aware_react_library/code/ -v` reported all tests passing).
* **Source files**: **3 modules** in `code/` (`scope_aware_react.py` ~370 lines,
  `constants.py`, `paths.py`) plus 1 test file.
* **Public entry points**: **6** (`ScopeAwareReactAgent`, `ScriptedModel`, `TrajectoryRecord`,
  `Action`, `AgentResult`, `MalformedActionError`).
* **REQ items satisfied**: **10 / 10** (REQ-1 through REQ-10 from `plan/plan.md`, all marked
  `Done`).
* **Quality gates**: ruff check **0 errors**, ruff format clean, mypy **0 errors**, pre-commit
  hooks **all passing**.
* **Cost**: USD **$0** (deterministic tests; no live API calls).

## Verification

* `meta.asset_types.library.verificator` (asset `scope_aware_react_v1`) — PASSED (0 errors, 0
  warnings).
* `verify_research_papers` — PASSED.
* `verify_research_code` — PASSED.
* `verify_plan` — PASSED.
* `pytest tasks/t0006_scope_aware_react_library/code/` — 8 / 8 passing.
* `ruff check`, `ruff format`, `mypy -p tasks.t0006_scope_aware_react_library.code` — all
  clean.

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0006_scope_aware_react_library/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0006_scope_aware_react_library" ---
# Results Detailed: Scope-Aware ReAct Library

## Summary

Implemented the project's first library asset, `scope_aware_react_v1`, which extends the
canonical ReAct prompting loop ([Yao2022]) with explicit `{global, subtask, atomic}`
granularity tags and a JSONL trajectory writer. The library is benchmark-agnostic, has zero
third-party runtime dependencies, and ships an 8-test deterministic test suite that runs
without any live API call. The trajectory schema is the canonical contract between this
library and the sister Plan-and-Solve library (`t0007_scope_unaware_planandsolve_library`).

## Methodology

* **Machine**: macOS Darwin 25.3.0 on Apple Silicon (local CPU); no GPU.
* **Python**: 3.13.11 (`uv run` against the project's lockfile).
* **Runtime**: Approximately 70 minutes of Claude Code orchestration end-to-end, covering 6
  active steps (plus 5 skipped). The pytest suite itself runs in **0.03 s**.
* **Started**: 2026-04-29T19:35:48Z (`task.start_time`).
* **Completed (results step)**: 2026-04-29T20:03:12Z.
* **Approach**: Implemented a single Python module exposing `ScopeAwareReactAgent` plus
  supporting dataclasses (`Action`, `TrajectoryRecord`, `AgentResult`, `ParsedOutput`),
  `ScriptedModel` for deterministic tests, a tolerant output parser, and an explicit-flush
  JSONL writer. The prompt template was assembled from a system header (granularity
  instruction literally including `<global>` / `<subtask>` / `<atomic>` examples), the user
  problem, and a rendered Thought / Action / Observation transcript. Apache-2.0 attribution to
  LangChain's ReAct prompt is stored as a constant in `code/constants.py` and is included in
  every system prompt.
* **Test approach**: Each of the 8 tests injects a `ScriptedModel` whose script is
  hand-curated to exercise one path: tag injection, action parsing, finish termination,
  malformed-JSON recovery, schema integrity, missing-tag fallback, max-turns cap, unknown-tool
  handling. No live LLM call is made.

## Verification

* `meta.asset_types.library.verificator --task-id t0006_scope_aware_react_library
  scope_aware_react_v1` — PASSED (0 errors, 0 warnings).
* `verify_research_papers t0006_scope_aware_react_library` — PASSED.
* `verify_research_code t0006_scope_aware_react_library` — PASSED.
* `verify_plan t0006_scope_aware_react_library` — PASSED.
* `pytest tasks/t0006_scope_aware_react_library/code/ -v` — 8 / 8 tests pass in 0.03 s.
* `ruff check tasks/t0006_scope_aware_react_library/code/` — 0 errors.
* `ruff format` — no changes after the initial autoformat.
* `mypy -p tasks.t0006_scope_aware_react_library.code` — Success: no issues found.

The pre-merge verificator (`verify_pr_premerge`) is run as part of the reporting step.

## Limitations

* The agent is **synchronous and single-threaded**; it does not support concurrent tool calls
  or streaming model output. Phase 2 experiments that need parallel tool invocations will need
  to extend this library or wrap it in an async adapter.
* The output parser assumes **English-language `Thought:` / `Action:` / `Confidence:`
  prefixes** and the literal angle-bracket tag format. Models that systematically deviate from
  this convention (e.g., "Reasoning:" instead of "Thought:") will fall through to the
  missing-tag default and produce poorer-quality trajectories.
* **Confidence is a single scalar per turn**. Per-claim confidence breakdowns are not
  supported; this matches the project Phase 2 stance from `[t0004]` brainstorming.
* The library supports a **fixed granularity for the entire run**. Experiments that vary
  granularity within one run (e.g., start global, drop to atomic mid-run) require either
  multiple agent instances run sequentially or a future extension. This limitation is captured
  in `results/suggestions.json`.
* No **benchmark-specific tool registries** are bundled with this library. Phase 2 tasks that
  target FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, or tau-bench need to
  provide their own `tool_registry` mapping. This is intentional per the task description's
  "Out of scope" clause.
* The library has **not been exercised against a real LLM yet**. The `ScriptedModel` pattern
  guarantees parser/loop correctness against pre-recorded inputs, but live-model behaviour
  (especially around the missing-tag fallback rate) is a Phase 2 unknown.

## Files Created

* `tasks/t0006_scope_aware_react_library/code/paths.py` — module-level `Path` constants.
* `tasks/t0006_scope_aware_react_library/code/constants.py` — granularity literals, schema
  field names, parser sentinels, LangChain attribution string.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` — main library module
  (~370 lines).
* `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` — 8 deterministic
  tests.
* `tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/details.json` —
  library asset metadata (spec v2).
* `tasks/t0006_scope_aware_react_library/assets/library/scope_aware_react_v1/description.md` —
  canonical library documentation including the Trajectory Log Schema subsection.
* `tasks/t0006_scope_aware_react_library/research/research_papers.md` — synthesis across
  Yao2022, Wang2023a, Zhou2022, Xiong2023.
* `tasks/t0006_scope_aware_react_library/research/research_code.md` — survey of prior task
  outputs.
* `tasks/t0006_scope_aware_react_library/plan/plan.md` — eleven-section plan with 10 REQ
  items.
* `tasks/t0006_scope_aware_react_library/results/results_summary.md` — this task's headline
  outcomes.
* `tasks/t0006_scope_aware_react_library/results/results_detailed.md` — this file.
* `tasks/t0006_scope_aware_react_library/results/metrics.json` — empty (no registered metrics
  measured).
* `tasks/t0006_scope_aware_react_library/results/costs.json` — `{"total_cost_usd": 0,
  "breakdown": {}}`.
* `tasks/t0006_scope_aware_react_library/results/remote_machines_used.json` — `[]`.
* Step logs at `tasks/t0006_scope_aware_react_library/logs/steps/NNN_<step>/step_log.md` for
  every active and skipped step.

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
`"subtask"` for every record, so the Phase 2 evaluator can ingest A and B trajectories with
one parser. If t0007 lands first, this library adopts whatever schema it ships; if t0006 lands
first, t0007 mirrors the schema documented above. Either landing order is acceptable per the
original task brief.

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

</details>
