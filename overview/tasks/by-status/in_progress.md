# ⏳ Tasks: In Progress

2 tasks. ⏳ **2 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0009 — <strong>Hierarchical annotation v2: tree schema with
subtask-to-atomic edges</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_hierarchical_annotation_v2` |
| **Status** | in_progress |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T23:24:52Z |
| **Task page** | [Hierarchical annotation v2: tree schema with subtask-to-atomic edges](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Task folder** | [`t0009_hierarchical_annotation_v2/`](../../../tasks/t0009_hierarchical_annotation_v2/) |

# Hierarchical Annotation v2 (Tree Schema)

## Motivation

The v1 annotation produced by `t0005_hierarchical_annotation_pilot_v1` uses a flat schema:
`subtask` is a `list[str]`, `atomic` is a `list[str]`, and there is no encoded edge mapping
atomics to their parent subtask. The v1 schema also truncates problem text to 1500 characters
in the `task_excerpt` field, which the v1 LLM-as-judge identified as the dominant failure mode
on FrontierScience-Olympiad rows (0/3 accept rate). This task fixes both issues: re-annotates
all 115 rows under a tree-shaped v2 schema with full problem text, and spot-checks at least
20% of rows with the LLM judge to estimate quality. Implements suggestion S-0005-02 and the
partial v2-schema portion of S-0005-01.

## v2 Schema

```json
{
  "task_id": "...",
  "benchmark": "...",
  "domain": "...",
  "difficulty": { ... },
  "problem": "...",
  "hierarchy": {
    "global": "<one-sentence top-level approach>",
    "subtasks": [
      {
        "subtask": "<subtask description>",
        "atomics": ["<atomic step>", "..."]
      },
      ...
    ],
    "global_atomics": ["<cross-cutting atomic step>", "..."]
  },
  "gold_actions": {
    "global": "<resolved global action>",
    "subtasks": [
      {
        "subtask": "<resolved subtask action>",
        "atomics": ["<resolved atomic action>", "..."]
      },
      ...
    ],
    "global_atomics": ["<resolved cross-cutting atomic action>", "..."]
  },
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "...",
  "hierarchy_completeness": true | false
}
```

`global_atomics` captures atomic steps that do not belong to any single subtask (typically
verification, sanity checks, or cross-cutting concerns surfaced in v1's flat `atomic` list).

## Scope

* Re-run the v1 annotator (`claude-sonnet-4-6`) with a new prompt that elicits the tree schema
  above. Pass the **full problem text** (no `task_excerpt` truncation).
* Apply the same task_id deduplication fix from v1 (the source pilot file has 14 rows with
  colliding `task_id`s; thread `_pilot_row_index` through the asset).
* Spot-check at least 23 rows (20%) with `claude-haiku-4-5-20251001` as judge. Sample is
  stratified across the four benchmarks (FrontierScience-Olympiad, SWE-bench Verified,
  HumanEval-proxy, Mind2Web-proxy).
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical-annotation-v2/`
  with the schema above and a `description.md` explaining the v2 → v1 migration.
* Compare v2 vs v1 judge accept rate per benchmark and flag any benchmark where v2 fails to
  improve.

Out of scope: scaling beyond 115 rows (S-0005-01 expansion), human review (full review pass
deferred to v3), proxy benchmark replacement (deferred to follow-up).

## Approach

1. Read the v1 dataset `assets/dataset/hierarchical-annotation-v1/files/*.jsonl` from t0005
   and load all 115 rows.
2. For each row, construct a v2 annotation prompt with the full problem text and the v2 schema
   in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree.
3. Stratified-sample 23 rows. For each, call the haiku judge with the row's full problem and
   the proposed v2 hierarchy; capture verdict + one-sentence justification.
4. Persist as a `dataset` asset with `details.json` (source = t0005's v1 dataset asset,
   version = "v2", license inherited per row, sample count = 115) and
   `files/hierarchical_annotation_v2.jsonl`.
5. Report per-benchmark v2-vs-v1 judge accept rate delta in `results/results_detailed.md`.

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2/{details.json, description.md, files/}`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate vs v1.
* `results/results_detailed.md` with the full audit table, the v2-vs-v1 comparison, and any
  rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (mean atomics per row).
* Follow-up suggestions for: row-count expansion to ≥200, human review pass, proxy benchmark
  remediation, and any benchmark where v2 fails to improve over v1.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$15** (115 sonnet annotations + 23 haiku
judges). Per-task cap: $20.

## Dependencies and Cross-References

* No task dependencies. Reads t0005's v1 dataset asset as input but does not depend on the
  t0005 task being incomplete.
* References `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows, original).
* Sister-task coordination: t0012 will consume the v2 dataset; this task must publish the v2
  dataset asset before t0012's implementation step runs.

## Source Suggestion

S-0005-02 — "Re-run LLM-as-judge with full problem text (no truncation)." Also partially
addresses S-0005-01 (annotation v2 schema) and the schema-gap finding from brainstorm 3.

## Key Questions

1. What is the per-benchmark judge accept rate under v2 vs v1?
2. How does the v2 schema's tree shape affect FrontierScience-Olympiad acceptance specifically
   (the worst-performing benchmark in v1)?
3. Are there rows where the v2 tree decomposition is well-defined but the v1 flat
   decomposition was empty (hierarchy_completeness: false in v1)?
4. What fraction of atomics fall under `global_atomics` vs assigned to a specific subtask?

</details>

<details>
<summary>⏳ 0010 — <strong>Matched-mismatch library: condition C with deliberately
wrong granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | in_progress |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0007-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:02Z |
| **Task page** | [Matched-mismatch library: condition C with deliberately wrong granularity tags](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../../tasks/t0010_matched_mismatch_library/) |

# Matched-Mismatch Library (Condition C)

## Motivation

The project's main hypothesis includes sub-hypothesis 2: scope-mismatched agents perform
strictly worse than both scope-aware (A) and scope-unaware (B) baselines. Without a C library,
research question 5 cannot be tested. This task implements C by wrapping the existing
libraries (`scope_aware_react_v1` from t0006 or `scope_unaware_planandsolve_v1` from t0007)
with a granularity-tag layer that emits **deliberately incorrect** tags at each step. The
library shares the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007 so a Phase 2 harness
can run all three conditions interchangeably. Implements suggestion S-0007-01.

## Scope

* Implement a library asset under `assets/library/matched_mismatch_v1/` exposing a
  `MatchedMismatchAgent` class that:
  * Accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
    registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`.
  * Walks the v2 hierarchy in phase order (the harness's canonical walk), determines the
    correct granularity at each step from the annotation, and **assigns an incorrect tag**
    according to the strategy:
    * `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`.
    * `adversarial`: always pick the most distant tag (`atomic` when correct is `global`,
      `global` when correct is `atomic`, `atomic` when correct is `subtask`).
  * Delegates each step to either `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`
    (configurable). The delegate handles the actual model call; the wrapper only controls the
    granularity tag.
  * Emits trajectory records in the canonical `TRAJECTORY_RECORD_FIELDS` schema, with the
    `granularity` field carrying the *wrong* tag (the actual correct tag is logged separately
    as `_correct_granularity` in an extras blob).
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` covering:
  random-strategy uniformity over `{global, subtask, atomic} \ correct_tag`,
  adversarial-strategy correctness, schema parity with t0007, end-to-end run with both
  delegate options.

Out of scope: the actual A/B/C experiment (handled by t0012), benchmark-specific tool
registries, remote execution.

## Approach

1. Read t0007's `scope_unaware_planandsolve_v1` library and t0006's `scope_aware_react_v1`
   library. Confirm the canonical trajectory schema is `TRAJECTORY_RECORD_FIELDS` from t0007.
2. Implement the library in `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
   Re-export the public API from `assets/library/matched_mismatch_v1/library/`.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests are deterministic (no live API calls). Use `ScriptedModel` from t0007 as the
   delegate's model.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/matched_mismatch_v1/` with `details.json`, `description.md`, `files/`.
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion to make the random-strategy mismatch ablation (uniform random vs.
  adversarial vs. matched) explicit in t0012.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  library assets. Reads `TRAJECTORY_RECORD_FIELDS` from t0007.

## Source Suggestion

S-0007-01 — "Implement matched-mismatch (C) library on top of scope_unaware_planandsolve_v1."

## Key Questions

1. What is the cleanest way to handle a granularity tag for steps that fall under
   `global_atomics` (cross-cutting atomics with no parent subtask)? Default: treat as `atomic`
   for the purposes of the mismatch strategy.
2. Should the wrapper expose a way to override the mismatch policy per-step (e.g., to inject
   targeted mismatches in specific phases)? Default: no, keep the wrapper minimal.
3. How should the schema's `_correct_granularity` extras field be standardised so a downstream
   experiment can compute the mismatch contribution per step?

</details>
