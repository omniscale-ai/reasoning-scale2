# ⏳ Tasks: In Progress

1 tasks. ⏳ **1 in_progress**.

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
