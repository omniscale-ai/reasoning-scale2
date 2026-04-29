# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0007 — <strong>Scope-unaware Plan-and-Solve library: condition B
baseline</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-06` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Scope-unaware Plan-and-Solve library: condition B baseline](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../../tasks/t0007_scope_unaware_planandsolve_library/) |

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

<details>
<summary>⏹ 0006 — <strong>Scope-aware ReAct library: condition A with explicit
granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-07` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Scope-aware ReAct library: condition A with explicit granularity tags](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../../tasks/t0006_scope_aware_react_library/) |

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

<details>
<summary>⏹ 0005 — <strong>Hierarchical annotation pilot v1: audit and conform
existing 115 rows</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_hierarchical_annotation_pilot_v1` |
| **Status** | not_started |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0002-08` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
| **Task page** | [Hierarchical annotation pilot v1: audit and conform existing 115 rows](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Task folder** | [`t0005_hierarchical_annotation_pilot_v1/`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/) |

# Hierarchical Annotation Pilot v1

## Motivation

Phase 1 of the project's roadmap requires ≥100 tasks fully annotated with gold actions at
three granularity levels (global / subtask / atomic). The imported
`project/data/annotation_pilot/ tasks_annotated.jsonl` already contains 115 LLM-annotated
rows, but the rows have not been verified to conform to the project's three-level schema and
there is no human or LLM-as-judge spot-check pass on record. This task closes that gap in v1
form: keep the existing 115 rows in place, audit their structure, and produce a canonical
dataset asset that downstream Phase 2 / 3 experiments can consume. Implements suggestion
S-0002-08.

## Scope

* Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on
  each row to determine whether it carries explicit global / subtask / atomic granularity
  labels or whether the granularity must be inferred.
* If labels are missing, write a deterministic mapper that derives the three-level structure
  from the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block
  per row.
* Run an LLM-as-judge spot-check on at least 10% of rows (≥12 rows) to estimate hierarchy
  quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/`
  with rows of shape `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask,
  atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict,
  judge_notes}`.

Out of scope for v1: replacing the HumanEval and Mind2Web proxies, expanding beyond 115 rows,
human review, inter-rater agreement studies. All deferred to follow-up tasks.

## Approach

1. Load the 115-row pilot file. For each row, compute the inferred or stated hierarchy and
   emit the canonical schema record.
2. Sample at least 12 rows stratified across the four benchmarks (FrontierScience-Olympiad,
   SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Send each to the LLM judge with the
   row's problem text and proposed hierarchy; capture verdict ("acceptable" / "needs
   revision") plus a one-sentence justification.
3. Persist the consolidated dataset asset with `details.json` (source URL = the imported pilot
   path, version = "v1", license = inherited from each upstream benchmark, sample count = 115)
   and `files/hierarchical_annotation_v1.jsonl`.
4. Report distribution stats in `results/results_detailed.md` (per-benchmark counts,
   per-domain counts, hierarchy-completeness rate, judge accept rate).

## Expected Outputs

* `assets/dataset/hierarchical_annotation_v1/` with `details.json`, `files/`, and a
  `description.md`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate.
* `results/results_detailed.md` with the full audit table and any rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (the registered diagnostic
  metric).
* Follow-up suggestions for: extension to ≥200 rows, full human-review pass, and proxy
  benchmark remediation.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: under 3 USD for 12-15 LLM-as-judge calls on
`claude-haiku-4-5-20251001`. Per-task cap: 5 USD.

## Dependencies and Cross-References

* No task dependencies.
* Reads `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows).
* Reads `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules — wrap
  as black-box utilities, never modify in place.
* References the four benchmark dataset assets produced by `t0003_download_benchmark_subsets`.

## Source Suggestion

S-0002-08 — "Run a Phase 1 pilot annotation on 20 tasks before scaling to 100." This task
implements that idea in v1 form, leveraging the existing 115 rows rather than re-annotating
from scratch.

## Key Questions

1. Do the existing 115 rows already carry a global / subtask / atomic decomposition, or must
   one be inferred?
2. What is the per-benchmark hierarchy-completeness rate?
3. What is the LLM-as-judge accept rate? Does it differ across benchmarks?
4. Are there systematic patterns in rejected rows (e.g., one benchmark consistently failing)?

</details>
