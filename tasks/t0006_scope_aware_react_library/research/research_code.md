---
spec_version: "1"
task_id: "t0006_scope_aware_react_library"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 5
libraries_found: 0
libraries_relevant: 0
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

Survey the project's existing code, libraries, and prior task outputs before implementing the
scope-aware ReAct library. The goal is to confirm there is no existing ReAct or trajectory-logging
implementation that can be reused, identify project-wide code conventions (path layout, style,
dataclasses, JSONL handling) that the new library should follow, and surface lessons learned from
the four completed tasks that should shape the implementation step.

## Library Landscape

`aggregate_libraries.py --format json --detail full` returns zero registered libraries (`libraries`
list is empty). The project has not yet published any reusable code as a library asset, which makes
sense: tasks `[t0001]` and `[t0004]` were brainstorms that produced no code, `[t0002]` was a
literature survey that produced only paper assets, and `[t0003]` produced datasets plus a small
download harness in `code/` but did not register a library.

Implication: the scope-aware ReAct library will be the project's first library asset, so it sets a
precedent for `assets/library/<library_id>/` layout, `details.json` schema, and `description.md`
shape. The library asset specification (`meta/asset_types/library/specification.md`) is the
authoritative reference; this library matches that v2 spec including `description_path` and
`module_paths`.

## Key Findings

### Project-Wide Python Style Is Already Codified

`[t0003]` follows the project Python style guide closely: dataclasses are
`@dataclass(frozen=True, slots=True)`, paths are centralized in `code/paths.py`, magic strings are
pulled into `code/constants.py`, public functions take keyword arguments, and absolute imports are
used throughout (e.g. `tasks.t0003_download_benchmark_subsets.code.constants`). The new library must
adopt the same conventions because Phase 2 experiments will import from it the same way.

The `[t0003]` Python footprint is non-trivial — about a dozen modules (`build_all.py`,
`build_frontierscience.py`, `build_swebench.py`, `build_taubench.py`, `build_workarena_pp.py`,
`constants.py`, `paths.py`, `dataset_asset.py`, `download_attempt.py`, `build_status_manifest.py`,
`access_status.json`) — and none of them is a ReAct-style agent loop, a Thought/Action parser, or a
JSONL trajectory writer. The new library cannot reuse or copy any agent code from `[t0003]`; it can
however mirror the style conventions.

### No Existing ReAct, Plan-and-Solve, or Trajectory-Log Implementations

Aggregator output for tasks and libraries confirms that no completed task has implemented a ReAct
loop, a Plan-and-Solve loop, or a trajectory-logging schema. The closest prior code is the
`access_status.json` writer in `[t0003]`, which is a single-shot JSON dump rather than a streaming
JSONL writer. The new library must implement its own JSONL writer; copying `[t0003]` JSON code would
not save effort.

The sister task `[t0007]` is in_progress in parallel and will produce the matched B baseline
library. This research notes that the trajectory schema documented in `research/research_papers.md`
is a contract between t0006 and t0007. If t0007 lands first, this task must adopt its schema; if
t0006 lands first, t0007 must mirror the schema documented in the asset's `description.md`. Either
order is acceptable per the task brief.

### Logging Conventions Established by Earlier Tasks

`[t0002]` and `[t0003]` write step logs to `logs/steps/<NNN_step-name>/step_log.md` with a fixed
YAML frontmatter and four mandatory `##` sections (Summary, Actions Taken, Outputs, Issues). They
also use `run_with_logs.py` for every CLI tool call. The new library inherits these conventions
because they are project-wide rules, not task-specific choices.

### Earlier Tasks Confirm the Verbalized-Confidence Pipeline Is Not Yet Wired

`[t0004]` brainstorm explicitly defers wiring of the verbalized-confidence pipeline to Phase 2
experiment tasks. No completed task computes overconfident error rate yet. The new library therefore
stores `confidence` as `float | None` in `[0, 1]` per turn but does not compute any calibration
metric — that remains a Phase 2 responsibility. This matches the literature stance from
`research/research_papers.md` (`[Xiong2023]`).

## Reusable Code and Assets

* **Source**: `tasks/t0003_download_benchmark_subsets/code/paths.py`

* **What it does**: Centralized `pathlib.Path` constants for the task's input and output
  directories, with the convention `TASK_ROOT = Path(__file__).resolve().parents[1]`.

* **Reuse method**: copy into task. The pattern is small (~20 lines) but is the canonical project
  layout for a `paths.py`. The new library will write its own `code/paths.py` that follows the same
  shape but defines library-specific constants (trajectory log default path, in-context exemplar
  fixture paths, scripted-model fixture paths).

* **Function signatures**: pure module-level constants only.

* **Adaptation needed**: rename constants to library-specific names. No functional code to copy.

* **Line count**: ~20 lines.

* **Source**: `tasks/t0003_download_benchmark_subsets/code/constants.py`

* **What it does**: Defines typed string and integer constants for column names, status values, and
  tool exit codes used by the dataset builders.

* **Reuse method**: copy into task. Same convention but library-specific values: granularity
  literals (`GRANULARITY_GLOBAL = "global"`, etc.), trajectory schema field names
  (`FIELD_TURN_INDEX = "turn_index"`, etc.), default model token limits, and parser sentinel values.

* **Function signatures**: module-level constants only.

* **Adaptation needed**: replace `[t0003]` dataset constants with library-specific constants.

* **Line count**: ~25 lines in the new library.

No library imports are available; every cross-task dependency would have to be a copy. The library
will therefore depend only on the Python standard library plus `pydantic` for JSON-ish parsing where
helpful.

## Lessons Learned

* **`[t0002]` lesson**: the research-papers verificator silently parses any `[Word]` in body text as
  an inline citation. Avoid bracketed examples like `Finish[answer]` in research files (use
  backticks or rephrase). This already bit research-papers in this task; it is now a documented
  pitfall for all future research files.
* **`[t0003]` lesson**: keeping `code/paths.py` and `code/constants.py` cleanly separated from
  business logic kept the dataset builders readable and made tests trivial to write. Adopt the same
  structure here.
* **`[t0003]` lesson**: pre-commit hooks auto-format files (end-of-file-fixer, ruff, ruff-format).
  Always run flowmark on Markdown and ruff/mypy before the commit; otherwise the hook fails the
  commit and you have to retry. This was hit twice in t0006 already; it is the reason the reporting
  step also runs the formatters one final time.
* **`[t0004]` lesson**: every Phase 2 experiment library should ship a deterministic mode that
  replays pre-recorded model outputs so that unit tests do not call live APIs. The new library
  exposes a `ScriptedModel` helper for exactly that purpose.

## Recommendations for This Task

1. **Mirror the `[t0003]` code layout**: keep `paths.py` and `constants.py` separate from
   `scope_aware_react.py`. Tests live in `code/test_scope_aware_react.py`.
2. **Adopt project-wide style**: `@dataclass(frozen=True, slots=True)` for all records, keyword
   arguments for any 2+ heterogeneous-parameter call, absolute imports from
   `tasks.t0006_scope_aware_react_library.code...`, no relative imports.
3. **Write the JSONL trajectory writer from scratch**, since no prior task has one. Use stdlib
   `json` only; one record per line; UTF-8; an explicit `flush()` after every write so a crashed
   experiment leaves a partial-but-valid file.
4. **Do not reuse any `[t0003]` JSON code**; the dataset access manifest is a one-shot dump and does
   not match the streaming JSONL pattern this library needs.
5. **Document the trajectory schema in `description.md`** so the sister task `[t0007]` can mirror
   it. This is the load-bearing artifact across the t0006/t0007 contract.
6. **Run `verify_library_asset` and `pytest` before commit**, not only at reporting. Library assets
   break silently if `module_paths` point to a missing file or if `description.md` lacks a mandatory
   section.

## Task Index

### [t0001]

* **Task ID**: t0001_brainstorm_results_1
* **Name**: Brainstorm session 1: plan first project tasks
* **Status**: completed
* **Relevance**: Originated suggestion S-0002-07 ("implement scope-aware A as ReAct extended with
  explicit granularity tags") which this task implements. No reusable code; brainstorms produce
  suggestions only.

### [t0002]

* **Task ID**: t0002_literature_survey_granularity_conditioning
* **Name**: Literature survey: granularity conditioning and hierarchical agents
* **Status**: completed
* **Relevance**: Produced the four paper assets (Yao2022 ReAct, Wang2023a Plan-and-Solve, Zhou2022
  least-to-most, Xiong2023 confidence elicitation) cited in this task's
  `research/research_papers.md`. No reusable code.

### [t0003]

* **Task ID**: t0003_download_benchmark_subsets
* **Name**: Download benchmark subsets for the four roadmap sources
* **Status**: completed
* **Relevance**: First completed task with substantial Python under `code/`. Sets the project's
  layout convention (`paths.py`, `constants.py`, dataclasses, absolute imports). Style mirror, not
  code import.

### [t0004]

* **Task ID**: t0004_brainstorm_results_2
* **Name**: Brainstorm session 2: plan Phase 1 annotation and Phase 2 baseline libraries
* **Status**: completed
* **Relevance**: Crystallized the t0006/t0007 sister-task split and the deterministic-test
  requirement. No reusable code; informs the design of `ScriptedModel`.

### [t0007]

* **Task ID**: t0007_scope_unaware_planandsolve_library
* **Name**: Scope-unaware Plan-and-Solve library: condition B baseline
* **Status**: in_progress
* **Relevance**: Sister task running in parallel. Must emit the same trajectory schema as t0006. No
  code yet to reuse; this research documents the schema contract so either landing order works.
