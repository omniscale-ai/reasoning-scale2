---
spec_version: "2"
task_id: "t0020_v2_truncation_vs_schema_ablation"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: v2 Truncation vs Schema Ablation

## Objective

Run one new annotation condition — the v2 tree schema applied to the same instance pool as t0014 but
with the problem text truncated to 1500 characters in BOTH annotator and judge prompts (matching the
t0009 baseline truncation pattern exactly). Use the resulting accept rates to decompose the t0014
+57 pp v2-tree-full vs v1-flat-truncated delta into a pure schema effect (text held constant) and a
pure text-length effect (schema held constant). "Done" means: predictions and answer assets exist
and pass their verificators, `metrics.json` reports the three accept rates with Wilson 95% CIs and
the two decomposition deltas, and `costs.json` shows total cost at or below $2.

## Task Requirement Checklist

```text
v2 Truncation vs Schema Ablation
short_description: Re-run v2 annotation with the tree schema but problem text truncated to 1500
chars to isolate the truncation fix from the schema upgrade.

Long description (key clauses, paraphrased from task_description.md):
- Run ONE new annotation condition: v2 tree schema with problem text truncated to 1500 chars in
  both annotator and judge prompts (matching the t0009 baseline truncation style).
- Use the same instance pool as t0014 (subtract the 3 known sonnet-timeout rows so n is matched
  across conditions).
- Both annotator and judge are claude-haiku-4-5.
- Compute three accept-rate variants (v1-flat-truncated, v2-tree-truncated, v2-tree-full) with
  Wilson 95% CIs and efficiency metrics.
- Produce a decomposition table in results_detailed.md showing the two isolated deltas with
  95% CIs.
- Predictions asset (assets/predictions/v2_truncated_ablation/) with per-row annotator and judge
  outputs. Answer asset addressing: "Of the t0014 +57 pp schema-only delta, how much is attributable
  to schema vs truncation, holding the other constant?"
- Cost ceiling at $2 (per costs.json).
```

* **REQ-1**: Implement a haiku annotator that takes a v1 row, truncates `problem` to 1500 chars
  (same `_truncate(text, *, limit) -> text[:limit] + "…"` helper as t0005's
  `JUDGE_PROBLEM_EXCERPT_LIMIT`), and produces a v2-tree-shaped annotation. Satisfied by Step 3
  (`code/v2_truncated_annotator.py`).
* **REQ-2**: Implement a haiku judge that takes the v2 annotation plus a truncated 1500-char problem
  excerpt and produces an `acceptable | needs revision` verdict. Satisfied by Step 5
  (`code/v2_truncated_judge.py`).
* **REQ-3**: Match the instance pool to t0014's 20 sonnet-judged `_pilot_row_index` values (3
  sonnet-timeout rows already excluded). Satisfied by Step 4 (`code/select_judge_sample.py`).
* **REQ-4**: Compute accept rates with Wilson 95% CIs for v1-flat-truncated, v2-tree-truncated, and
  v2-tree-full on a consistent comparison basis (per-benchmark and aggregate). Satisfied by Step 6
  (`code/compute_stats.py`).
* **REQ-5**: Compute the two decomposition deltas with 95% CIs:
  `pure_schema = trunc - v1_flat_trunc` and `pure_text = full - trunc`. Satisfied by Step 6.
* **REQ-6**: Produce `metrics.json` with three accept-rate variants plus their stderrs and the
  inference cost-per-item / time-per-item efficiency metrics. Satisfied by Step 7
  (`code/build_metrics.py`).
* **REQ-7**: Produce a predictions asset under `assets/predictions/v2_truncated_ablation/` with
  `details.json`, `description.md`, and predictions jsonl. Satisfied by Step 8.
* **REQ-8**: Produce an answer asset addressing the decomposition question with both short and full
  answers. Satisfied by Step 9.
* **REQ-9**: `results/results_detailed.md` contains the decomposition table and at least 2 charts.
  Satisfied by Step 10 (orchestrator's `results` step uses outputs from Step 6 and 7).
* **REQ-10**: Total cost in `results/costs.json` ≤ $2. Satisfied by validation gate in Step 3 and
  Step 5 plus the budget caps `ANNOTATOR_BUDGET_CAP_USD = 1.0` and `JUDGE_BUDGET_CAP_USD = 1.0`.

## Approach

This task replicates t0014's annotator + judge pipeline with one targeted change: insert
`_truncate(text, limit=1500)` on the `problem` string in BOTH prompt templates. Everything else
(model, parsing, output schema, judge sample selection, Wilson CI math) stays identical.

Why this design:

* **Reuses well-tested code**: t0014's pipeline has already been validated end-to-end and the
  Wilson-CI implementation in its `compute_stats.py` is correct and reusable verbatim. Copying
  rather than importing across tasks (per the project's cross-task code reuse rule) keeps the task
  self-contained.
* **Minimal surface area for bugs**: only the two prompt templates change. The truncation logic is
  exactly t0005's `_truncate(text, *, limit) -> text[:limit] + "…"`, copied verbatim.
* **Matched pool**: using the same 20 `_pilot_row_index` values that t0014 judged means the
  v2-tree-full reference accept rate (filtered from t0009's haiku judged 23 rows down to those same
  20\) is paired with v2-tree-truncated row-by-row. This makes `pure_text = full - trunc` a paired
  comparison; only `pure_schema = trunc - v1_flat_trunc` is unpaired (since v1's 12 rows use
  different `_pilot_row_index` values from a small unstratified sample).

**Alternatives considered**:

* *Re-judge the v2-haiku-full data with the same haiku judge for paired comparison*: rejected
  because that's already what t0009's outputs represent — re-running would just duplicate cost.
* *Run on n=80 instead of n=20*: rejected because the task description says ~40 of each call (and
  cap at $2). The 20-row pool gives Wilson CIs of about ±20 pp on rates near 50%, which is
  acceptable for a decomposition with two known-large deltas (the task description's decision
  thresholds are ±40 pp, well outside the CI noise).

**Task types**: `experiment-run` and `data-analysis`, matching `task.json`. Per the experiment-run
planning guidelines, we include a baseline (v1-flat-truncated at 33%) and a validation gate (one-row
dry-run before unleashing the full 20-row run). Per data-analysis, we register all three accept
rates as named metric variants in `metrics.json`.

## Cost Estimation

* **Haiku annotator**: 20 rows × ~3k input tokens × $0.80/M = ~$0.048 input; 20 rows × ~500 output
  tokens × $4/M = ~$0.04 output. Subtotal ~**$0.09**.
* **Haiku judge**: similar volume. Subtotal ~**$0.09**.
* **Total estimate**: ~**$0.18**, with `ANNOTATOR_BUDGET_CAP_USD = 1.0` and
  `JUDGE_BUDGET_CAP_USD = 1.0` as hard caps. Combined ceiling = $2 matches the task description's
  cost ceiling.
* **Project budget impact**: $51.31 left of $100 (per `aggregate_costs --detail full` on
  2026-05-01). Adding ~$0.20 keeps us well below the warning threshold of $80.

## Step by Step

1. **Bootstrap code module structure.** Create `code/paths.py`, `code/constants.py`,
   `code/__init__.py` inside the task. Define path constants for the v1 source jsonl, the t0014
   sonnet judge sample, and the new outputs (`code/_outputs/v2_truncated_annotated.jsonl`, etc.).
   Define `PROBLEM_EXCERPT_LIMIT: Final[int] = 1500`, the haiku model id, prices, and budget caps.
   Define `ANNOTATOR_USER_TEMPLATE` and `JUDGE_USER_TEMPLATE` containing
   `Problem (truncated to {limit} chars):\n{problem_excerpt}\n\n`. Satisfies REQ-1, REQ-2.

2. **Copy the t0014 pipeline.** Copy `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_annotator.py` to
   `code/v2_truncated_annotator.py`, `v2_judge.py` to `code/v2_truncated_judge.py`,
   `select_judge_sample.py` to `code/select_judge_sample.py`, and `compute_stats.py` to
   `code/compute_stats.py`. Update import paths to point at our `paths.py` and `constants.py`.

3. **[CRITICAL] Modify the annotator to truncate the problem.** In `code/v2_truncated_annotator.py`,
   replace the call site that builds the prompt with one that calls
   `_truncate(problem, limit=PROBLEM_EXCERPT_LIMIT)` and feeds the result into
   `ANNOTATOR_USER_TEMPLATE.format(benchmark=..., domain=..., limit=PROBLEM_EXCERPT_LIMIT, problem_excerpt=...)`.
   Validation gate: run with `--limit 1 --dry-run` first, observe one complete-hierarchy output,
   confirm the prompt sent to claude does NOT exceed `PROBLEM_EXCERPT_LIMIT + 200` chars (problem
   block only, system prompt is separate). Halt and debug if the dry-run row produces
   `parse-failure` or call-failure. Trivial baseline: t0009's haiku-full annotator achieved ~91%
   complete-hierarchy rate with no truncation; we expect at least 80% with truncation (because
   1500-char excerpts are still informative on most rows). Satisfies REQ-1.

4. **Select the matched judge sample.** In `code/select_judge_sample.py`, point the upstream sample
   path at `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl` (the
   20-row matched pool) and intersect it with our `v2_truncated_annotated.jsonl` rows that have
   complete hierarchies. Output `code/_outputs/v2_truncated_judge_sample.jsonl`. Satisfies REQ-3.

5. **[CRITICAL] Modify the judge to truncate the problem.** In `code/v2_truncated_judge.py`, replace
   the prompt build with one that calls `_truncate(problem, limit=PROBLEM_EXCERPT_LIMIT)` and uses
   the modified `JUDGE_USER_TEMPLATE`. Validation gate: run with `--limit 3` first, inspect the
   three verdicts, confirm at least one parses to `acceptable` or `needs revision` (no
   parse-failures). Trivial baseline: t0009's haiku judge on full text accepted 91% of v2-tree rows;
   we expect the truncated condition to land somewhere between 33% (v1) and 91% (full). Satisfies
   REQ-2.

6. **Compute statistics.** In `code/compute_stats.py`, load the three sources:
   * `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`
     filtered to the 12 v1 rows with non-null `judge_verdict` (v1-flat-truncated baseline).
   * Our `code/_outputs/v2_truncated_judge_outcomes.jsonl` (v2-tree-truncated condition).
   * `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl` filtered to the
     20 `_pilot_row_index` values that match our sample (v2-tree-full reference). For each, compute
     aggregate accept rate plus per-benchmark accept rates with Wilson 95% CIs. Compute the two
     decomposition deltas (`pure_schema = trunc_rate - v1_rate` and
     `pure_text = full_rate - trunc_rate`) with difference-of-proportions Wilson CIs. Output
     `code/_outputs/three_way_comparison.json` and a markdown table. Satisfies REQ-4, REQ-5.

7. **Build the metrics file.** In `code/build_metrics.py`, read
   `code/_outputs/three_way_comparison.json` and write `results/metrics.json` with the multi-variant
   format: variants `v1_flat_truncated`, `v2_tree_truncated`, `v2_tree_full`, each with
   `accept_rate`, `accept_rate_stderr` (half-width of 95% Wilson CI),
   `efficiency_inference_cost_per_item_usd`, and `efficiency_inference_time_per_item_seconds`.
   Time-per-item is read from the `claude` CLI envelope's `duration_ms` averaged over all calls in
   that condition (annotator + judge). Cost-per-item is the running cost / n. Satisfies REQ-6.

8. **Build the predictions asset.** In `code/build_predictions.py`, write
   `assets/predictions/v2_truncated_ablation/details.json`, `description.md`, and copy the
   `v2_truncated_judge_outcomes.jsonl` plus annotated jsonl into
   `assets/predictions/v2_truncated_ablation/files/`. Run
   `uv run python -m arf.scripts.verificators.verify_predictions_asset \ tasks/t0020_v2_truncation_vs_schema_ablation/assets/predictions/v2_truncated_ablation`.
   Satisfies REQ-7.

9. **Build the answer asset.** In `code/build_answer.py`, write
   `assets/answer/decomposition_v2_schema_vs_truncation/details.json`, `short_answer.md`, and
   `full_answer.md` synthesizing the decomposition and explicitly addressing which decision
   threshold (per task description: ±40 pp dominance or ±15 pp roughly additive) the data support.
   Run `verify_answer_asset.py` on the asset path. Satisfies REQ-8.

10. **Generate charts.** In `code/build_charts.py`, produce two PNGs in `results/images/`:
    `accept_rate_three_way.png` (bar chart of the three accept rates with 95% CI error bars) and
    `decomposition.png` (waterfall-style chart showing v1 → trunc → full with the two delta arrows
    annotated). Satisfies REQ-9.

## Remote Machines

None required. All `claude` CLI calls run locally with default authentication.

## Assets Needed

* **Input dataset** (read-only):
  `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`
  (115 rows; the `problem` field is the source text we truncate; the 12 rows with `judge_verdict`
  set are the v1-flat-truncated baseline).
* **Matched pool reference**:
  `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl` (20 rows; the
  matched pool of `_pilot_row_index` values).
* **v2-tree-full reference**:
  `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl` (23 haiku-judged
  rows; we filter to the 20 ids that intersect our sample for paired comparison).

## Expected Assets

* **Predictions asset**: `assets/predictions/v2_truncated_ablation/`. Contains `details.json` (with
  `predictions_id`, `model`, sample size, total accepted, per-benchmark breakdown), `description.md`
  (mandatory sections per spec), and `files/v2_truncated_judge_outcomes.jsonl`
  + `files/v2_truncated_annotated.jsonl`. Asset count: 1 (matches `task.json`
    `expected_assets.predictions = 1`).
* **Answer asset**: `assets/answer/decomposition_v2_schema_vs_truncation/`. Contains `details.json`
  (with `question`, decision threshold and outcome), `short_answer.md`, and `full_answer.md`. Asset
  count: 1 (matches `task.json` `expected_assets.answer = 1`).

## Time Estimation

* Implementation (Steps 1-10): ~30 minutes wall-clock once code is written. Most of the time is
  spent on the actual claude CLI calls (40 calls × ~10 sec each = ~7 minutes serialized; ~2-3
  minutes with workers=4). The remainder is asset construction and verification.
* Validation: ~5 minutes for dry-run gates and verificator runs.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Truncation makes annotator/judge fail to parse problem (especially FrontierScience-Olympiad math) | Medium | Some rows drop out, reducing n below 20 | Log per-row truncation impact (was the problem cut mid-sentence), report n for each split. The decomposition still holds at lower n with widened CIs. |
| Haiku judge accepts everything (degenerate) | Medium | Decomposition is meaningless | Compare against t0009 judge outcomes — t0009 also used haiku judge and saw 21/23 acceptable; this means the v2-tree-full rate IS already saturated at ~91%. The decomposition with trunc landing in [33%, 91%] is still informative even with that ceiling. |
| Total cost overruns the $2 ceiling | Low | Budget breach | Hard caps `ANNOTATOR_BUDGET_CAP_USD = 1.0` and `JUDGE_BUDGET_CAP_USD = 1.0` halt new submissions. The estimated total is $0.20, so the cap has 10x headroom. |
| One-row dry-run hides parse failures that show up at scale | Low | Wasted spend | The annotator records parse-failure as a notes string and continues; the judge does the same. We aggregate failure counts in `compute_stats.py` and report n explicitly. |
| `claude` CLI authentication or rate limits | Low | Run halts mid-batch | Idempotent jsonl appends mean retries are safe; `_load_existing_indices()` skips already-completed rows. The halt-on-cap mechanism halts cleanly. |

## Verification Criteria

* `uv run python -m arf.scripts.verificators.verify_predictions_asset tasks/t0020_v2_truncation_vs_schema_ablation/assets/predictions/v2_truncated_ablation/`
  exits 0 with no errors. Confirms REQ-7.
* `uv run python -m arf.scripts.verificators.verify_answer_asset tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition_v2_schema_vs_truncation/`
  exits 0 with no errors. Confirms REQ-8.
* `cat results/metrics.json` shows three named variants (`v1_flat_truncated`, `v2_tree_truncated`,
  `v2_tree_full`) each with `accept_rate`, `accept_rate_stderr`,
  `efficiency_inference_cost_per_item_usd`, `efficiency_inference_time_per_item_seconds` keys.
  Confirms REQ-6.
* `grep -E "^\\| v1-flat-truncated" results/results_detailed.md` finds the decomposition table row
  and `grep "pure_schema\\|pure_text" results/results_detailed.md` finds both deltas with CIs.
  Confirms REQ-5, REQ-9.
* `cat results/costs.json` shows total cost ≤ $2. Confirms REQ-10.
* `ls results/images/*.png | wc -l` ≥ 2. Confirms REQ-9 chart output.
* `uv run python -m arf.scripts.verificators.verify_task_complete t0020_v2_truncation_vs_schema_ablation`
  exits 0.
