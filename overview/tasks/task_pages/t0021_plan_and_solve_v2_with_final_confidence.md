# ⏳ Plan-and-Solve v2 with final_confidence Field

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0021_plan_and_solve_v2_with_final_confidence` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-05-01T14:03:02Z |
| **Source suggestion** | `S-0012-01` |
| **Task types** | `write-library` |
| **Expected assets** | 1 library |
| **Task folder** | [`t0021_plan_and_solve_v2_with_final_confidence/`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/) |

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
