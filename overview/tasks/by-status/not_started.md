# ⏹ Tasks: Not Started

4 tasks. ⏹ **4 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0012 — <strong>Phase 2 A/B/C smoke harness on FrontierScience
subset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_phase2_abc_smoke_frontierscience` |
| **Status** | not_started |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Expected assets** | 3 predictions, 1 library |
| **Source suggestion** | `S-0006-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **Task page** | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Task folder** | [`t0012_phase2_abc_smoke_frontierscience/`](../../../tasks/t0012_phase2_abc_smoke_frontierscience/) |

# Phase 2 A/B/C Smoke Harness on FrontierScience Subset

## Motivation

This is the project's **first end-to-end Phase 2 result**. It tests the headline hypothesis on
a real benchmark for the first time: scope-aware (A) > scope-unaware (B) > scope-mismatched
(C). The smoke test is intentionally narrow — single benchmark (FrontierScience-Olympiad),
single provider (Anthropic Claude), N=28 hierarchy-complete rows from the v2 dataset, paired
across conditions. The goal is a directional signal plus a sample-size calibration for
follow-up confirmatory runs. Implements suggestions S-0006-03, S-0007-02, and S-0005-06.

## Hypotheses tested

| RQ | Predicted direction | Detection threshold at N=28 |
| --- | --- | --- |
| RQ1 — A success rate > B success rate | A − B ≥ +5pp | ~15pp paired (McNemar/sign test, α=0.05) |
| RQ2 — A overconfident error rate < B | A − B ≤ −2pp | ~5-8pp paired |
| RQ5 — C worst on Metrics 1 and 2 | C < min(A, B) on both | clear ranking when A > B + 5pp |

Excluded by design (handled in separate experiments on the right benchmarks):

* RQ3 (request-vs-act accuracy on low-level tasks) — needs tau-bench, not FrontierScience.
* RQ4 (gains concentrated in info-asymmetric states) — needs WorkArena++ or tool-using
  benchmark.

## Scope

* Build a small `phase2_smoke_harness_v1` library under `assets/library/` that:
  * Loads the v2 dataset asset from t0009 and filters to FrontierScience-Olympiad rows with
    `hierarchy_completeness == true`.
  * Runs a phase-order walk over each row's `hierarchy` (global → all subtasks → all
    `global_atomics`); for each step in the walk, dispatches to one of the three libraries (A:
    t0006, B: t0007, C: t0010).
  * Captures every step's trajectory record into one JSONL per condition under
    `assets/predictions/`.
  * Calls t0011's `compute_overconfident_error_rate` on each trajectory file.
  * Computes `task_success_rate` by parsing each trajectory's final `Finish` answer and
    comparing to the row's gold final answer (FrontierScience problems end with `FINAL ANSWER:
    ...`).
  * Reports `avg_decisions_per_task` per condition.
* Produce three `predictions` assets (one per condition: A, B, C).
* Produce one `library` asset for the harness itself.
* Run on the **28 hierarchy-complete FrontierScience-Olympiad rows** from the v2 dataset (this
  matches the v1 hierarchy-complete count; refine after t0009 lands if v2 row count differs).

Out of scope: multi-provider replication (deferred), benchmark-specific tool registries beyond
a minimal `python_exec` for FrontierScience math problems, scaling N beyond ~28.

## Approach

1. Read the v2 dataset asset from t0009 once t0009 has merged. Filter to FrontierScience-
   Olympiad and `hierarchy_completeness == true`.
2. Implement the harness library that drives the phase-order walk and dispatches
   per-condition. Reuse t0006, t0007, t0010 libraries; reuse t0011's calibration aggregator.
3. For each row, run all three conditions against the same model (`claude-sonnet-4-6-20251001`
   recommended) with paired execution (same seed where applicable, same problem text, same
   tool registry).
4. Tool registry is minimal: a single `python_exec` tool for arithmetic and one
   `Finish(answer)` tool. FrontierScience-Olympiad rows are mostly verbal reasoning; tools
   exist for explicit computation only.
5. Persist trajectory JSONLs under `assets/predictions/<condition>/files/`. Compute and
   persist metrics.
6. Write `results/results_summary.md` with the 3×3 condition × metric table and the predicted-
   versus-observed effect sizes. Write `results/results_detailed.md` with per-row trajectories
   summarised, the McNemar p-value for A-vs-B and B-vs-C, and the implied sample size for
   follow-up confirmatory runs.
7. Generate at least 2 charts: condition × metric bar chart with confidence intervals; per-row
   success matrix heatmap (rows=problems, columns=conditions).

## Expected Outputs

* `assets/library/phase2_smoke_harness_v1/` — the harness library.
* `assets/predictions/phase2_smoke_a/`, `assets/predictions/phase2_smoke_b/`,
  `assets/predictions/phase2_smoke_c/` — three predictions assets, one per condition.
* `results/metrics.json` in explicit-variant format (3 variants: A, B, C; metrics:
  `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`).
* `results/results_summary.md` and `results/results_detailed.md` with hypothesis-test results,
  effect sizes, sample-size calibration, and clear acknowledgement of the excluded RQs.
* `results/images/` with at least 2 charts.
* Follow-up suggestions for: multi-provider replication (Gemini, OpenAI), expansion to
  tool-using benchmarks (SWE-bench, tau-bench), confirmatory N expansion based on observed
  variance.

## Compute and Budget

No GPU. Anthropic API only. **Budget cap: USD 20** (per-task default cap is $10; this task
exceeds the default and explicitly opts up). Estimated breakdown: 28 rows × 3 conditions × ~3
self-consistency calls per step × ~6 steps per row × ~$0.005 per call = $7.5 baseline; budget
$20 leaves headroom for retries and the calibration prompt.

## Dependencies and Cross-References

* **Hard dependencies (must be `completed`)**:
  * `t0009_hierarchical_annotation_v2` — produces the v2 dataset asset this task consumes.
  * `t0010_matched_mismatch_library` — produces the C-condition library.
  * `t0011_metric2_calibration_aggregator` — produces the Metric 2 implementation.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  libraries.
* References Yao2022 ReAct, Wang2023 Plan-and-Solve, and Xiong2024 calibration paper assets
  from t0002.

## Source Suggestion

S-0006-03 — "Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience subset." Also
covers S-0007-02 and S-0005-06 by consolidation.

## Key Questions

1. Does A − B reach the +5pp threshold on `task_success_rate`?
2. Does A − B reach the −2pp threshold on `overconfident_error_rate`?
3. Does C rank strictly worst on both metrics relative to A and B?
4. What is the within-condition variance, and what N does the FrontierScience confirmatory run
   need to detect a 5pp effect at α=0.05 with paired test?
5. Are there per-domain (physics / chemistry / biology) effect-size differences worth
   surfacing to the next brainstorm?

</details>

<details>
<summary>⏹ 0011 — <strong>Metric 2 calibration aggregator: verbalized confidence
+ 3-sample self-consistency</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_metric2_calibration_aggregator` |
| **Status** | not_started |
| **Effective date** | 2026-04-30 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Task page** | [Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Task folder** | [`t0011_metric2_calibration_aggregator/`](../../../tasks/t0011_metric2_calibration_aggregator/) |

# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as
the canonical calibration protocol — verbalized confidence elicitation (low / medium / high +
brief justification) plus 3-sample self-consistency aggregation. Without this library, the
Phase 2 smoke test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the
diagnostic Metric 3 (avg decisions per task). This task unblocks the headline experiment by
producing a library that any agent's trajectory records can be passed through to compute
`overconfident_error_rate`. Implements suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/`
  exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low /
    medium / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem
    and returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is
    majority-vote on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float`
    that returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls
    the model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at
  `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` covering: prompt
  template formatting, parsing of low / medium / high confidence labels, majority-vote
  aggregation across 3 samples (including ties), threshold-based overconfident detection, and
  end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic
tests only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a
   `paths.py` and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold
  default rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration
  error) computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric
2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized
   labels mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default:
   prefer the highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results
   can include it in `metrics.json` directly?

</details>

<details>
<summary>⏹ 0010 — <strong>Matched-mismatch library: condition C with deliberately
wrong granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | not_started |
| **Effective date** | 2026-04-30 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0007-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
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

<details>
<summary>⏹ 0009 — <strong>Hierarchical annotation v2: tree schema with
subtask-to-atomic edges</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_hierarchical_annotation_v2` |
| **Status** | not_started |
| **Effective date** | 2026-04-30 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`hierarchical-annotation`](../../../meta/task_types/hierarchical-annotation/) |
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
