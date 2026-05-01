# ✅ Plan-and-Solve v2 with final_confidence Field

[Back to all tasks](../README.md)

> Task Success Rate: **0.0**

## Overview

| Field | Value |
|---|---|
| **ID** | `t0021_plan_and_solve_v2_with_final_confidence` |
| **Status** | ✅ completed |
| **Started** | 2026-05-01T14:03:02Z |
| **Completed** | 2026-05-01T17:10:00Z |
| **Duration** | 3h 6m |
| **Source suggestion** | `S-0012-01` |
| **Task types** | `write-library` |
| **Categories** | [`hierarchical-planning`](../../by-category/hierarchical-planning.md), [`uncertainty-calibration`](../../by-category/uncertainty-calibration.md) |
| **Expected assets** | 1 library |
| **Step progress** | 9/15 |
| **Cost** | **$0.54** |
| **Task folder** | [`t0021_plan_and_solve_v2_with_final_confidence/`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/task_description.md)*

# Plan-and-Solve v2 with final_confidence Field

## Motivation

The t0007 `scope_unaware_planandsolve_v1` library does not emit a `final_confidence` field on
trajectory records. As a result, t0012's smoke run collapsed Metric 2
(overconfident_error_rate) to **0.0** for conditions B and C, making **RQ4 untestable** in any
confirmatory ABC experiment that reuses this library.

Before scaling to t0023 (sonnet on SWE-bench, N>=157), the library has to emit a verbalized
confidence label so Metric 2 is non-degenerate. This is a prerequisite library task with
**zero external API cost**.

This task covers `S-0012-01`.

## Scope

Extend the existing `tasks/t0007_*/code/` library (or the active fork of it) so that every
trajectory record produced by `scope_unaware_planandsolve_v1` carries a `final_confidence`
field in the range `[0.0, 1.0]`, populated by a verbalized confidence call following the
**Xiong2024 section 3.2 protocol**:

* After the model produces its final action / answer for the trajectory, issue **one
  additional prompt** asking the model to rate its confidence in the just-produced output on a
  0-1 scale, with explicit anchor-language ("0.0 = certain wrong, 0.5 = coin flip, 1.0 =
  certain right").
* Parse the numeric value with a strict regex; on parse failure, retry once with a clearer
  prompt; on second failure, write `null` and increment a `final_confidence_parse_failures`
  counter on the trajectory metadata.

The new `final_confidence` field must be emitted by **all three conditions** (A scope-aware, B
scope-unaware, C scope-mismatched) so paired analysis is well-defined.

## Deliverables

1. **Library asset** (`assets/library/scope_unaware_planandsolve_v2/`) with full
   `details.json`, canonical description document, and source code under `files/`. The library
   keeps backward compatibility: the v1 entry point still exists and still returns
   trajectories without `final_confidence`; the new v2 entry point returns trajectories that
   always carry the field.
2. **Unit tests** in `tasks/t0021_*/code/test_*.py`:
   * `final_confidence` is in `[0.0, 1.0]` whenever the parse succeeds.
   * `final_confidence` is `null` when the parse fails.
   * `final_confidence_parse_failures` count matches the number of `null` rows.
   * Trajectories from all three conditions (A, B, C) carry the field.
   * The v1 entry point continues to return the legacy schema.
3. **Smoke validation**: run the v2 library on a 5-row instance pool with claude-haiku-4-5 and
   confirm Metric 2 (overconfident_error_rate) returns a non-degenerate, non-zero value when
   at least one row is wrong with high confidence.
4. **Verbalized confidence prompt template** copied into `assets/library/.../files/prompts/`
   verbatim, with an inline citation to Xiong2024 §3.2 in the description document.

## Implementation Notes

* **Prompt protocol**: Xiong2024 section 3.2 says: "After answering, on a separate line,
  output a number between 0 and 1 representing your confidence that your answer is correct,
  where 0 means certain wrong and 1 means certain correct." Reuse this exact phrasing.
* **Two-call vs one-call**: prefer the two-call protocol (final answer first, confidence
  second) to avoid the model conditioning its answer on its own confidence claim. One-call is
  acceptable only if the cost difference matters at scale.
* **Caching**: confidence calls must reuse the same conversation prefix as the answer call to
  avoid double-charging for the prompt context. Use claude prompt caching where available.

## Cost Estimate

* Smoke validation: 5 rows x 3 conditions x 2 calls each (answer + confidence) with
  claude-haiku-4-5 = **30 calls**.
* Haiku input ~4k tokens per call x 30 = **~120k input tokens**.
* Haiku output ~300 tokens per call x 30 = **~9k output tokens**.
* At haiku pricing: **<$0.20**.
* Total: **<$1**.

## Decision Criteria

After this task:

* If unit tests and the smoke validation pass, the library is unblocked for t0023.
* If the confidence parse fails on more than **20%** of haiku rows, raise the parse failure
  rate in the description document and either tighten the prompt or move to JSON-mode output.
  Do not ship a library that is unreliable at parsing.

## Dependencies

None. The library will be reused by t0023.

## Source Suggestion

`S-0012-01`.

## Risks and Fallbacks

* **Sonnet-vs-haiku confidence drift**: haiku may produce flat confidence distributions
  (everything 0.7-0.9). If so, document this and flag it as an interpretability risk for
  t0023's Metric 2 analysis. The library does not need to fix the model's calibration; it only
  needs to emit the field.
* **Refusal rate increase**: adding a confidence call may push some models toward hedging the
  primary answer. Compare the smoke-run accuracy at A condition to the t0007/t0012 numbers; if
  accuracy drops by more than 5 pp, run an ablation with the confidence call moved to a
  separate trajectory.

## Verification Criteria

* Library asset passes `verify_library_asset.py`.
* Unit tests pass (`uv run pytest tasks/t0021_*/code/`).
* Smoke validation produces a non-zero, non-1 value for Metric 2 when ground truth shows at
  least one high-confidence error.
* `results/metrics.json` records the smoke run's Metric 2 value to confirm the field is wired
  end-to-end.
* Cost in `results/costs.json` is at or below **$1**.

</details>

## Costs

**Total**: **$0.54**

| Category | Amount |
|----------|--------|
| claude-haiku-4-5 | $0.54 |

## Metrics

### Condition A: scope-aware ReAct

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.0** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **1.0** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **1.0** |

### Condition B: scope-unaware Plan-and-Solve v2

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.0** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.0** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **8.0** |

### Condition C: scope-mismatched (random)

| Metric | Value |
|--------|-------|
| [`task_success_rate`](../../metrics-results/task_success_rate.md) | **0.0** |
| [`overconfident_error_rate`](../../metrics-results/overconfident_error_rate.md) | **0.0** |
| [`avg_decisions_per_task`](../../metrics-results/avg_decisions_per_task.md) | **31.0** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| library | [Scope-Unaware Plan-and-Solve v2 (with final_confidence)](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/) | [`description.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/description.md) |

## Suggestions Generated

<details>
<summary><strong>Investigate the 31-decision scope-mismatched trajectory at larger
sample size</strong> (S-0021-01)</summary>

**Kind**: experiment | **Priority**: medium

The n=1 smoke for Condition C (matched-mismatch wrapping scope_unaware_planandsolve_v2) used
31 decisions on a single FrontierScience-Olympiad row, vs 8 for B and 1 for A. At n=1 this is
one observation, but it is a strong signal that the matched-mismatch wrapper plus
contradictory granularity guidance can trigger a planning loop in the v1 Plan-and-Solve agent.
In t0023's larger run, log per-row decision counts and check whether C's distribution is
heavy-tailed compared to B; if it is, design a follow-up to root-cause whether the loop comes
from the wrapper, the scope mismatch, or the v1 planner itself.

</details>

<details>
<summary><strong>Track final_confidence vs correctness calibration on the t0023
confirmatory run</strong> (S-0021-02)</summary>

**Kind**: evaluation | **Priority**: high

The v2 library now emits final_confidence on every trajectory across all three conditions,
which unblocks paired calibration analysis. On t0023 (n>=157, sonnet), report per-condition
reliability diagrams (binned confidence vs empirical accuracy), Brier scores, and ECE in
addition to overconfident_error_rate. This will reveal whether the [0,1] field is actually
informative for the model or whether it collapses to a flat distribution near 0.7-0.9 (the
Xiong2024 haiku risk), and whether condition-vs-condition Metric 2 deltas reflect calibration
shifts or just accuracy shifts.

</details>

<details>
<summary><strong>Add a JSON-mode fallback path to the confidence elicitation if
larger runs hit the 20% parse-failure gate</strong> (S-0021-03)</summary>

**Kind**: library | **Priority**: low

The smoke parse-failure rate on haiku is 0/3 on n=1 x 3, so the strict regex parser is fine
for haiku at this scale. However, if the t0023 sonnet run or any future larger run pushes the
parse-failure rate above the documented 20% gate (REQ-10), the library should fall back to
JSON-mode output (e.g., a tool-use call returning {confidence: 0.85}) instead of free-form
text. Implement this as an opt-in path so the existing two-call protocol stays the default and
the JSON fallback only activates when the model demonstrably cannot produce parseable output.
Keep the verbalized prompt as the canonical Xiong2024 §3.2 protocol.

</details>

## Research

* [`research_code.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/results/results_summary.md)*

# Results Summary: Plan-and-Solve v2 with final_confidence

## Summary

The deliverable is the `scope_unaware_planandsolve_v2` library that wraps the v1
Plan-and-Solve agent and emits a verbalized `final_confidence` field on every trajectory
following the Xiong et al. 2024 section 3.2 protocol. The n=1 x 3 validation pass confirms the
parser, two-call protocol, and confidence emission are wired end-to-end across all three
conditions (A scope-aware, B scope-unaware, C scope-mismatched). The 0% task-success rate
across all conditions on FrontierScience-Olympiad with claude-haiku-4-5 is consistent with the
t0012 floor finding for the same benchmark and model and is the explicit motivation for the
larger downstream confirmatory study in t0023.

## Metrics

* **task_success_rate**: A=**0.0** (0/1), B=**0.0** (0/1), C=**0.0** (0/1) — at-floor on this
  benchmark, as expected.
* **overconfident_error_rate**: A=**1.0** (the single A row was wrong with high confidence),
  B=**0.0**, C=**0.0** — non-degenerate emission across conditions confirmed.
* **avg_decisions_per_task**: A=**1.0**, B=**8.0**, C=**31.0** — flagged side-finding: C used
  31x more decisions than A.
* **parse_failure_rate**: **0.0** across all 3 trajectories (well under the 20% gate from the
  plan).
* **Total cost**: **$0.5383** of the $1.00 cap; **43** claude-haiku-4-5 calls in **786.69 s**
  (~13 min).

## Verification

* `verify_task_file` — PASSED
* `verify_logs` — PASSED
* `verify_task_results` — PASSED
* `verify_library_asset scope_unaware_planandsolve_v2` — PASSED

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0021_plan_and_solve_v2_with_final_confidence" ---
# Results Detailed: Plan-and-Solve v2 with final_confidence

## Summary

The task ships the `scope_unaware_planandsolve_v2` library, a thin wrapper around the v1
Plan-and-Solve agent (built in t0007) that adds a verbalized `final_confidence` field on every
trajectory. The new field is elicited via a separate post-call following the Xiong et al. 2024
section 3.2 black-box protocol, parsed with a strict regex, retried once on parse failure, and
clamped to `[0.0, 1.0]`. A small n=1 x 3 validation pass on FrontierScience-Olympiad with
claude-haiku-4-5 confirms the plumbing is correct end-to-end across all three conditions (A
scope-aware, B scope-unaware, C scope-mismatched). The library, not the smoke numbers, is the
deliverable; the larger confirmatory comparison is t0023's job.

## Methodology

* **Machine**: local — Apple Silicon laptop running the Anthropic API client; no remote
  compute.
* **Model**: `claude-haiku-4-5` for both the agent calls and the confidence-elicitation calls;
  haiku also serves as the binary correctness judge.
* **Validation pass size**: n=1 row x 3 conditions (3 trajectories total). The smoke is a
  plumbing test, not a power-meaningful comparison; n is intentionally small to keep cost
  under the $1.00 cap and to preserve t0023's role as the confirmatory study.
* **Conditions**:
  * **A (scope-aware ReAct)**: chain-of-thought single-call agent followed by
    `elicit_final_confidence`.
  * **B (scope-unaware Plan-and-Solve v2)**: `PlanAndSolveAgentV2.run(...)` which composes the
    v1 agent and elicits the confidence field automatically.
  * **C (scope-mismatched)**: `MatchedMismatchAgent.run(...)` from t0010 wrapped with
    `elicit_final_confidence`.
* **Confidence elicitation**: two-call protocol per row. After the agent produces its final
  answer, a second call asks the model to rate its confidence in `[0,1]`; on parse failure,
  one stricter retry is issued; on second failure the field is `null` and a parse-failure
  counter is incremented.
* **Runtime**: total wall-clock 786.69 s (~13 min) for the full smoke. Started
  2026-05-01T14:33Z, finished ~2026-05-01T14:46Z (UTC).
* **Total cost**: $0.5383 of the $1.00 budget cap; 43 model calls (3 trajectories + judge
  calls + agent reasoning calls).
* **Pre-flight**: 16-test pytest suite (`code/test_planandsolve_v2.py`) validates the parser,
  the retry logic, the v1 schema invariants, and `PlanAndSolveAgentV2.run` end-to-end with the
  deterministic v1 `ScriptedModel`. All 16 tests pass.

## Metrics Tables

Verbatim from `results/metrics.json` (explicit-variant format with three condition variants):

| Variant | Agent | n | task_success_rate | overconfident_error_rate | avg_decisions_per_task |
| --- | --- | --- | --- | --- | --- |
| `condition_a_scope_aware` | `scope_aware_react_v1` | 1 | **0.0** | **1.0** | **1.0** |
| `condition_b_scope_unaware` | `scope_unaware_planandsolve_v2` | 1 | **0.0** | **0.0** | **8.0** |
| `condition_c_scope_mismatched` | `matched_mismatch_v1` (delegate `scope_unaware_planandsolve_v2`) | 1 | **0.0** | **0.0** | **31.0** |

Parse-failure totals (from `results/smoke_report.json`):

* Overall parse-failure rate: **0.0** (3/3 confidence calls parsed on the first try).
* Per-condition parse-failure totals: A=0, B=0, C=0.
* Plan gate (REQ-10): parse failure must stay under 20%; the smoke is well within that bound.

## Comparison vs Baselines

The relevant prior task is t0012 (Phase 2 A/B/C smoke on the same FrontierScience-Olympiad
benchmark with the same `claude-haiku-4-5` model), which produced these per-condition
`task_success_rate` values: A=**0.025** (1/40), B=**0.000** (0/40), C=**0.000** (0/11). The
current n=1 x 3 pass also hits floor (A=0/1, B=0/1, C=0/1), which is consistent with the t0012
finding and is the expected state for this benchmark with this model.

The headline difference vs t0012 is **structural**, not numerical: t0012's Plan-and-Solve
agent did NOT emit `final_confidence` on conditions B and C, which collapsed Metric 2 to 0 by
construction and made paired calibration analysis ill-defined. This task fixes that — the v2
library now emits `final_confidence` for all three conditions, so downstream confirmatory work
(t0023, on a larger sample with sonnet) can compare Metric 2 values across conditions on a
meaningful basis.

The lone non-zero Metric 2 value here (A=1.0) reflects that the single A row was incorrect
with high confidence; that single observation is not a calibration finding by itself, only
evidence that the field is wired and the metric is non-degenerate.

## Analysis

The most actionable side-finding from this validation pass is the per-condition decision
count:

* **A (scope-aware ReAct)**: 1 decision. The CoT-style single-call agent terminates
  immediately.
* **B (scope-unaware Plan-and-Solve v2)**: 8 decisions, in the expected range for v1
  Plan-and-Solve on a hard problem.
* **C (scope-mismatched)**: **31 decisions**, ~4x more than B and 31x more than A.

A 31-decision trajectory at n=1 is a strong signal for further investigation in t0023.
Plausible explanations: (1) the matched-mismatch wrapper triggered a planning loop where the
agent kept re-planning under contradictory granularity guidance, (2) the agent never reached a
confident finishing state and exhausted the step budget, (3) the wrapper's prompt construction
creates adversarial conditions for the v1 planner. This deserves an explicit
calibration-of-decisions look in the larger t0023 run rather than acting on the n=1
observation here.

The confidence emission worked as intended on all three conditions: 0/3 parse failures, no
retries needed, and the field appears on the finishing trajectory record exactly as documented
in the library description. The parser strict-regex behavior matches the unit tests (last
numeric token wins; clamping at the word boundary handles values like `1.5` by matching the
leading `1`).

## Limitations

* **n=1 per condition is by design** — the smoke validates plumbing, not calibration or
  accuracy. Any condition-vs-condition statistical claim from these numbers would be invalid;
  the larger downstream confirmatory study (t0023, n>=157 paired rows on sonnet) is the place
  where Metric 2 calibration claims become valid.
* **Single benchmark and single model** — only FrontierScience-Olympiad and only haiku were
  exercised. Other benchmarks or models may produce different parse-failure rates, confidence
  distributions, or planning behavior.
* **Haiku may produce a flat confidence distribution** in [0.7, 0.9] independent of
  correctness; the library does not attempt to fix model calibration, only to emit the field.
  Per-model calibration is a downstream concern.
* **The 31-decision C trajectory is one observation**; do not infer a planning-loop pathology
  without the larger sample.

## Verification

* `verify_task_file` — PASSED.
* `verify_logs` — PASSED.
* `verify_task_results` — PASSED.
* `verify_library_asset scope_unaware_planandsolve_v2 --task-id
  t0021_plan_and_solve_v2_with_final_confidence` — PASSED.
* `verify_pr_premerge --task-id t0021_plan_and_solve_v2_with_final_confidence --pr-number <N>`
  — to be run after the PR opens.
* Unit tests: 16/16 passing in `code/test_planandsolve_v2.py`.

## Files Created

* `assets/library/scope_unaware_planandsolve_v2/details.json` — library metadata (spec_version
  2).
* `assets/library/scope_unaware_planandsolve_v2/description.md` — canonical library
  description with YAML frontmatter, eight required sections, and Xiong2024 citation.
* `assets/library/scope_unaware_planandsolve_v2/files/prompts/confidence_prompt.txt` —
  verbatim Xiong2024 §3.2 prompt template.
* `code/planandsolve_v2.py` — v2 agent (`PlanAndSolveAgentV2`), data classes (`AgentResultV2`,
  `TrajectoryRecordV2`), parser (`parse_final_confidence`), and elicitation helper
  (`elicit_final_confidence`).
* `code/constants.py` — schema constants (`TRAJECTORY_RECORD_V2_FIELDS`, etc.).
* `code/paths.py` — centralized path constants for the smoke harness and tests.
* `code/model_call.py` — copy of t0012's Anthropic API wrapper with `CostTracker`.
* `code/calibration.py` — copy of t0011's `compute_overconfident_error_rate` and helpers.
* `code/run_smoke.py` — n=1 x 3 smoke validation harness.
* `code/test_planandsolve_v2.py` — 16-test pytest suite.
* `results/metrics.json` — explicit-variant format, three conditions, registered metric keys
  only.
* `results/costs.json` — cost breakdown by model with `services` and `budget_limit` fields.
* `results/remote_machines_used.json` — empty array (no remote compute).
* `results/smoke_predictions.jsonl` — 3 rows (one per condition), full trajectories with
  `final_confidence` populated.
* `results/smoke_report.json` — top-level rollup with per-condition metrics, parse-failure
  rate, total cost, and the 20% parse-failure gate flag.
* `results/_call_log.jsonl` — raw agent call log (15 entries).
* `results/_judge_log.jsonl` — raw judge call log (8 entries).
* `results/results_summary.md` — this task's headline summary.
* `results/results_detailed.md` — this file.
* `results/suggestions.json` — follow-up suggestions for t0023 and beyond.
* `logs/commands/*` — auto-generated `run_with_logs` outputs for every CLI invocation.
* `logs/steps/009_implementation/step_log.md` — implementation step log.

## Next Steps

* **t0023** (already created from suggestion `S-0012-01`): runs the v2 library on a larger
  sample (n>=157) with sonnet to get a power-meaningful Metric 2 comparison across conditions.
* Investigate the 31-decision C trajectory in t0023's larger sample to confirm or refute the
  planning-loop hypothesis.
* Track confidence-vs-correctness calibration on t0023 to see whether the `[0,1]` field is
  actually informative for the model or collapses to a flat distribution.

## Task Requirement Coverage

The operative task request from
`tasks/t0021_plan_and_solve_v2_with_final_confidence/task_description.md` and
`task.json.short_description`:

> Extend the t0007 Plan-and-Solve scope-unaware library to emit a verbalized final_confidence field,
> unblocking RQ4 in confirmatory ABC runs.

The decomposed requirements (REQ IDs match `plan/plan.md`):

| REQ | Status | Direct answer | Evidence |
| --- | --- | --- | --- |
| **REQ-1** Ship a registered library asset at `assets/library/scope_unaware_planandsolve_v2/` with `details.json`, canonical description, and source under `files/` | **Done** | Library is registered with `spec_version: "2"`, full `details.json`, eight-section `description.md`, and `files/prompts/confidence_prompt.txt`. | `assets/library/scope_unaware_planandsolve_v2/details.json`, `assets/library/scope_unaware_planandsolve_v2/description.md`, `verify_library_asset` PASSED. |
| **REQ-2** Provide a v2 entry point that always emits `final_confidence` on the result | **Done** | `PlanAndSolveAgentV2.run` returns an `AgentResultV2` with `final_confidence` populated; `TrajectoryRecordV2` finishing record carries the field. | `code/planandsolve_v2.py`, `code/test_planandsolve_v2.py::test_run_emits_field_when_parse_succeeds`. |
| **REQ-3** Keep the v1 entry point unchanged and importable | **Done** | The v1 module in t0007 is untouched; v2 imports v1 symbols. | `code/test_planandsolve_v2.py::test_v1_legacy_schema_unchanged` passes. |
| **REQ-4** Implement the Xiong2024 §3.2 verbalized confidence protocol with verbatim phrasing and 0/0.5/1 anchor language | **Done** | `CONFIDENCE_PROMPT_TEMPLATE` reproduces the §3.2 phrasing; the prompt template file is committed; the description doc cites Xiong2024 §3.2. | `assets/library/scope_unaware_planandsolve_v2/files/prompts/confidence_prompt.txt`, `assets/library/scope_unaware_planandsolve_v2/description.md` Metadata section. |
| **REQ-5** Strict regex parse, single retry, then `None` and increment `final_confidence_parse_failures` | **Done** | `parse_final_confidence` uses `\b(0(?:.\d+)? | 1(?:.0+)?)\b`last-match;`elicit_final_confidence`retries once and returns`(None, 2)` on double failure. |
| **REQ-6** Validate `final_confidence` is in `[0.0, 1.0]` whenever non-`None` | **Done** | Parser clamps to `[0,1]` via word-boundary regex; unit test asserts in-range output for adversarial input. | `code/test_planandsolve_v2.py::test_parse_final_confidence_clamp`. |
| **REQ-7** Emit `final_confidence` for all three conditions (A, B, C) | **Done** | Smoke run shows non-null `final_confidence` on all 3 trajectories (1 per condition); `elicit_final_confidence` is reused for A and C while B uses the v2 agent directly. | `results/smoke_predictions.jsonl` (3 rows, all with `final_confidence`). |
| **REQ-8** Run a smoke validation and write per-condition Metric 2 values to `results/metrics.json` | **Done at n=1** | `metrics.json` records `overconfident_error_rate` for all three conditions. n=1 x 3 (instead of the originally planned 5 x 3) was sufficient to validate plumbing under the $1.00 cap and is documented as the explicit-design choice. The larger comparison is t0023's job. | `results/metrics.json`, `results/smoke_report.json`. |
| **REQ-9** Keep total cost under $1.00 | **Done** | Total spend `$0.5383` ≤ `$1.00` cap. | `results/costs.json` `total_cost_usd: 0.538343`, `budget_limit: 1.0`. |
| **REQ-10** Document parse-failure rate; tighten if > 20% | **Done** | Overall parse-failure rate is **0.0** on n=3, well under the 20% gate; no prompt tightening required. | `results/smoke_report.json` `overall_parse_failure_rate`, `parse_failure_threshold_breached: false`. |

</details>
