# ⏳ Tasks: In Progress

2 tasks. ⏳ **2 in_progress**.

[Back to all tasks](../README.md)

---

## ⏳ In Progress

<details>
<summary>⏳ 0019 — <strong>v2 Judge Calibration with Sonnet (Substantive + Familial
Bias)</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0019_v2_judge_calibration_sonnet` |
| **Status** | in_progress |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 predictions, 1 answer |
| **Source suggestion** | `S-0014-02` |
| **Task types** | [`comparative-analysis`](../../../meta/task_types/comparative-analysis/), [`data-analysis`](../../../meta/task_types/data-analysis/) |
| **Start time** | 2026-05-01T14:02:34Z |
| **Task page** | [v2 Judge Calibration with Sonnet (Substantive + Familial Bias)](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Task folder** | [`t0019_v2_judge_calibration_sonnet/`](../../../tasks/t0019_v2_judge_calibration_sonnet/) |

# v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

## Motivation

t0014 produced a schema-only delta of **+57 pp** for v2 over v1, well above Zhou2022's +16 pp
and Boisvert2024's +25 pp published bands, and a model-only delta of **-1 pp** that sits below
Xiong2024's lower edge (0 pp). Two plausible threats to validity remain:

1. **Judge anchoring** (S-0014-02): the haiku judge may be partially scoring "the model
   produced a parseable tree with subtask-to-atomic edges" rather than "the decomposition is
   substantively right". If so, the +57 pp gap to literature is a judge artefact, not a schema
   effect.
2. **Familial bias** (S-0014-03): the haiku judge gives the v2-haiku annotator a same-family
   agreement bonus (~5-10 pp per Xiong2024). If so, the -1 pp model-only delta is masking a
   real sonnet annotator advantage.

Both threats can be tested at the same 43-row pool used in t0014 by swapping the judge prompt
and judge model. Defending the +57 pp schema-only headline before scaling to a confirmatory
experiment is the cheapest paper-defensible step on the critical path.

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary).

## Scope

Re-judge **the same 43 v2 rows** that t0014 produced (20 v2-sonnet + 23 v2-haiku) plus the
matched 20 v1-sonnet rows from t0009/t0014, under two new judge configurations:

* **Substantive critic** prompt (S-0014-02): the judge simulates execution ("verify each
  atomic, executed in order, would actually solve the problem") and outputs a binary
  accept/reject plus a per-criterion sub-score.
* **Model-rotated** judge (S-0014-03): keep the original t0014 judge prompt, swap the judge
  model from haiku to claude-sonnet-4-6.

Both judges run against the same row pool. Combined output is a 4-condition matrix per row:

| Condition | Annotator | Judge Prompt | Judge Model |
| --- | --- | --- | --- |
| Baseline (from t0014) | v1-sonnet / v2-haiku / v2-sonnet | original | haiku |
| Substantive | v1-sonnet / v2-haiku / v2-sonnet | substantive critic | sonnet |
| Model-rotated | v1-sonnet / v2-haiku / v2-sonnet | original | sonnet |

This task does not re-annotate. It only re-judges. Annotation rows from t0014 are read in via
the existing predictions overlay applied by t0015.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_judge_calibration/`): per-row judge verdicts
   under the substantive and model-rotated conditions, plus the cached baseline t0014/t0015
   verdicts as reference. Includes prompt-version and judge-model fields per row.
2. **Answer asset** (`assets/answer/.../`) addressing the question: "Does the v2 schema retain
   a 30+ pp accept-rate delta over v1 under a substantive judge and under a sonnet judge, or
   is the +57 pp t0014 headline an artefact of haiku judge anchoring?"
3. **Reported metrics** in `results/metrics.json` using the explicit multi-variant format, one
   variant per (annotator x judge-prompt x judge-model) cell. Each cell reports:
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Comparison table** in `results/results_detailed.md` showing the schema-only and
   model-only deltas under all three judge configurations side by side, with explicit deltas
   vs t0014.

## Models and Configurations

* **Annotator outputs** (already produced; not re-run): claude-sonnet-4-6 v1 (20 rows), haiku
  v2 (23 rows), sonnet v2 (20 rows). All from t0014.
* **Substantive critic judge**: claude-sonnet-4-6 with the new prompt template.
* **Model-rotated judge**: claude-sonnet-4-6 with the original t0014 judge prompt.

Total judge calls: 43 rows x 2 new judge configurations = **86 sonnet judge calls**.

## Cost Estimate

* Sonnet input ~5k tokens per call x 86 = **~430k input tokens**.
* Sonnet output ~600 tokens per call x 86 = **~52k output tokens**.
* At claude-sonnet-4-6 pricing (approximately $3/M in, $15/M out): **about $2.05** sonnet
  spend.
* Reserve for retry/repair: **+$1**.
* Total: **~$3-5**.

This sits well within the remaining $51 budget.

## Decision Criteria

After this task:

* If schema-only delta drops below **+30 pp** under the substantive judge, the +57 pp t0014
  headline is partly judge-anchoring; reset the headline to the substantive number and revisit
  S-0014-01 (v3 schema iteration).
* If schema-only delta stays at or above **+45 pp** under both new judges, the schema effect
  is robust; commit to the t0023 confirmatory run as planned.
* If model-only delta swings to **at least +5 pp** under the sonnet judge, the t0014 -1 pp
  result is a haiku familial bias, and v2-sonnet should be the production annotator going
  forward.
* If model-only delta stays within +/-2 pp under the sonnet judge, the v2 schema does the work
  and sonnet annotation is not worth the cost premium.

## Dependencies

None on uncompleted tasks. Reads from t0014's predictions and t0015's correction overlay; both
are merged.

## Source Suggestion

This task covers `S-0014-02` (primary) and `S-0014-03` (secondary). Both suggestions remain
active as `source_suggestion` until t0019 results are merged; the secondary will be marked
covered in the next brainstorm round if the data answers it.

## Risks and Fallbacks

* **Substantive judge is slow or unstable**: if per-row judge time exceeds 30 s, drop
  sub-criteria and use a binary verdict only.
* **Sonnet judge disagrees with itself across the two prompt variants on the same row**: log
  per-row agreement; report Cohen's kappa across (substantive, model-rotated) at the same
  model. This is a free signal about prompt-vs-anchoring effects.
* **The t0014 row pool has masked instances** (we know 3 sonnet timeouts exist; S-0014-05 was
  rejected): exclude those rows from all conditions consistently and report the effective n.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` contains all 9 cells (3 annotators x 3 judge configs) with
  accept_rate and stderr.
* `results/results_detailed.md` contains a side-by-side delta table and an explicit
  decision-criteria check-off against the four bullets above.
* Cost in `results/costs.json` is at or below **$5**.

</details>

<details>
<summary>⏳ 0021 — <strong>Plan-and-Solve v2 with final_confidence Field</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0021_plan_and_solve_v2_with_final_confidence` |
| **Status** | in_progress |
| **Effective date** | 2026-05-01 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0012-01` |
| **Task types** | [`write-library`](../../../meta/task_types/write-library/) |
| **Start time** | 2026-05-01T14:03:02Z |
| **Task page** | [Plan-and-Solve v2 with final_confidence Field](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Task folder** | [`t0021_plan_and_solve_v2_with_final_confidence/`](../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/) |

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
