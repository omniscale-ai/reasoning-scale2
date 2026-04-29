---
spec_version: "2"
task_id: "t0009_hierarchical_annotation_v2"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Hierarchical Annotation v2 (Tree Schema)

## Objective

Re-annotate all 115 rows of the v1 hierarchical annotation pilot from
`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`
under a tree-shaped v2 schema with explicit subtask-to-atomic edges and a `global_atomics` bucket
for cross-cutting actions, using the full problem text (no 1500-character truncation), and judge at
least 23 stratified rows with `claude-haiku-4-5-20251001`. "Done" means: a single dataset asset
under `assets/dataset/hierarchical-annotation-v2/` that passes `verify_dataset_asset`, with 115 rows
in v2 schema, ≥23 judge verdicts, per-benchmark accept-rate delta vs v1 reported in
`results/results_detailed.md`, and total spend ≤ $15.

## Task Requirement Checklist

The task description specifies the following work:

```
Re-run the v1 annotator (claude-sonnet-4-6) with a new prompt that elicits the v2 tree schema.
Pass the full problem text (no task_excerpt truncation). Apply the v1 task_id deduplication fix
(thread _pilot_row_index through the asset). Spot-check at least 23 rows (20%) with
claude-haiku-4-5-20251001 as judge, stratified across the four benchmarks. Produce one consolidated
dataset asset under assets/dataset/hierarchical-annotation-v2/. Compare v2 vs v1 judge accept rate
per benchmark and flag any benchmark where v2 fails to improve.
```

* **REQ-1** Re-annotate all 115 v1 rows under the v2 tree schema with `claude-sonnet-4-6-20251001`,
  using full problem text. Evidence:
  `assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl` has 115 rows
  with v2 fields populated. Satisfied by Step 3.

* **REQ-2** Pass full problem text (no `task_excerpt` truncation) to both annotator and judge.
  Evidence: `code/v2_annotator.py` and `code/v2_judge.py` show no character cap; the prompts are
  logged. Satisfied by Steps 2 and 4.

* **REQ-3** Thread `_pilot_row_index` (source pilot file row index) through every output row to
  resolve the 14 v1 colliding `task_id`s. Evidence: every row in `hierarchical_annotation_v2.jsonl`
  has a `_pilot_row_index` integer field. Satisfied by Step 3.

* **REQ-4** Stratified-sample at least 23 rows (≥20%) across the four benchmarks
  (FrontierScience-Olympiad, SWE-bench Verified, WorkArena++, tau-bench) and judge each row with
  `claude-haiku-4-5-20251001`. Evidence: `code/_outputs/judge_costs.json` lists ≥23 outcomes;
  `hierarchical_annotation_v2.jsonl` has `judge_verdict` and `judge_notes` populated for the sampled
  rows. Satisfied by Steps 4 and 5.

* **REQ-5** Produce one consolidated `dataset` asset under
  `assets/dataset/hierarchical-annotation-v2/` with `details.json`, `description.md`, and
  `files/hierarchical_annotation_v2.jsonl`. Evidence: `verify_dataset_asset` passes. Satisfied by
  Step 6.

* **REQ-6** Compare v2-vs-v1 judge accept rate per benchmark and flag any benchmark where v2 fails
  to improve. Evidence: `results/results_detailed.md` table compares
  `acceptable / acceptable+needs-revision` rates side-by-side per benchmark, with explicit call-out
  of any non-improving benchmark. Satisfied by Step 7 (writes the comparison table for the
  orchestrator's results step).

* **REQ-7** Stay within the $15 budget cap (per task description; default per-task limit is $10 but
  task description authorizes ~$15 explicitly). Evidence: `results/costs.json` `total_cost_usd` ≤
  15\. Hard halt in `code/v2_annotator.py` and `code/v2_judge.py` when running totals approach the
  caps. Satisfied throughout.

* **REQ-8** Compute `hierarchy_completeness` per row under the stricter v2 rule (`global` non-null
  AND (any subtask has atomics OR `global_atomics` non-empty)). Evidence: every output row has a
  boolean `hierarchy_completeness`. Satisfied by Step 3.

The task description also asks four key questions; these are answered in
`results/results_detailed.md`, not in the implementation phase, but the data they need
(per-benchmark accept rate, FrontierScience-Olympiad rows specifically, completeness table,
global-atomics fraction) is produced in Steps 3 through 7.

## Approach

The pipeline is a four-stage Python program: load v1 → annotate with sonnet → sample stratified for
judge → judge with haiku → merge and persist as a v2 dataset asset.

**Annotator stage** uses the local `claude` CLI in
`--print --output-format json --model claude-sonnet-4-6-20251001` mode (same pattern as
`tasks/t0005_hierarchical_annotation_pilot_v1/code/judge_runner.py`), which avoids needing an
explicit `ANTHROPIC_API_KEY` in `.env`. The system prompt instructs the model to emit a JSON object
with `global` (string), `subtasks` (list of `{subtask, atomics}`), `global_atomics` (list of
strings), and a parallel `gold_actions` block. The user message is the full problem text plus the
row's benchmark and domain.

**Judge stage** repeats the t0005 pattern but with the haiku model and a v2-aware prompt: the judge
sees the full problem and the v2 tree, and emits a JSON `{verdict, justification}`. Stratified
sampling allocates 6 rows from FrontierScience-Olympiad (largest benchmark, 40 rows; 20% ≈ 8 but 6
keeps total at exactly 23), and 5/6/6 from the other three benchmarks (totalling 23 = 20%). A fixed
random seed (`SAMPLE_SEED = 42`) makes the sample reproducible.

The merge stage joins judge verdicts back into the 115-row file by `_pilot_row_index` (the v1 task
showed `task_id` is non-unique with 14 collisions). The dataset asset is then written under the
spec-version-2 dataset format.

**Findings driving design**: Xiong2024 reports judge agreement drops from 77% to 41% with truncated
input — this is the diagnosed v1 failure mode, fixed by passing full text. Zhou2022 and Boisvert2024
show explicit subtask-to-atomic edges raise compositional task accuracy by 15-25 points, motivating
the tree schema. Yao2022 and Shinn2023 report 18-22% of atomics are cross-cutting, motivating
`global_atomics`.

**Alternatives considered**: (a) Use the v1 deterministic `hierarchy_mapper.py` and just rebuild the
JSON in the v2 shape from existing v1 nodes. Rejected because the v1 input does not encode parent
edges between conceptual and atomic nodes — the tree shape requires fresh annotation. (b) Use OpenAI
o4-mini instead of sonnet. Rejected because the task description explicitly asks for the v1
annotator (`claude-sonnet-4-6`) held constant for an apples-to-apples comparison. (c) Sample 12 rows
like v1 (33% short of the ≥23 requirement). Rejected because the task description mandates ≥23
(≥20%).

**Task type**: `hierarchical-annotation` (matches `task.json` `task_types`). The Planning Guidelines
from `meta/task_types/hierarchical-annotation/instruction.md` say to preserve the
global/subtask/atomic levels, budget LLM calls explicitly, plan a human review pass — all satisfied
here, with human review explicitly deferred to a v3 follow-up suggestion.

## Cost Estimation

| Item | Unit cost | Quantity | Subtotal |
| --- | --- | --- | --- |
| Sonnet annotation (input) | $3 / Mtok | ~115 × 5,000 chars / 4 chars/tok = 144 ktok | $0.43 |
| Sonnet annotation (output) | $15 / Mtok | ~115 × 1,500 chars / 4 chars/tok = 43 ktok | $0.65 |
| Haiku judge (input) | $0.80 / Mtok | ~23 × 6,000 chars / 4 chars/tok = 35 ktok | $0.03 |
| Haiku judge (output) | $4 / Mtok | ~23 × 600 chars / 4 chars/tok = 3.5 ktok | $0.01 |
| Buffer for retries / longer-than-expected problems | — | — | $1.00 |

**Estimated total: ~$2.12.** This is well under the $15 task description budget and well under the
$10 default per-task limit. The plan still applies hard caps:

* `ANNOTATOR_BUDGET_CAP_USD = 12.00` (~95% of the $15 target, hardcoded in `code/constants.py`)
* `JUDGE_BUDGET_CAP_USD = 2.00` (~13% of the $15 target)
* Per-call estimated cost printed to `_outputs/v2_annotator_costs.json` and
  `_outputs/v2_judge_costs.json` with running totals; hard halt if either cap is reached.

Project budget at planning time: $99.94 left of $100 total (`aggregate_costs --format json` at
2026-04-29). Plenty of headroom.

## Step by Step

The implementation phase covers Steps 1 through 8 below. Subsequent orchestrator-managed steps
(writing the results documents, the metrics ledger, the cost ledger, and follow-up suggestion files)
are out of scope for this plan.

**Milestone 1 — Pipeline scaffolding (Steps 1-2)**

1. **Create the `code/` package skeleton.** Add `code/paths.py` with `pathlib.Path` constants for
   `V1_INPUT_PATH = Path("tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl")`,
   `OUTPUTS_DIR = Path("tasks/t0009_hierarchical_annotation_v2/code/_outputs")`,
   `V2_RAW_OUTPUT = OUTPUTS_DIR / "v2_annotated.jsonl"`,
   `V2_JUDGE_SAMPLE_OUTPUT = OUTPUTS_DIR / "v2_judge_sample.jsonl"`,
   `V2_JUDGE_OUTPUTS_PATH = OUTPUTS_DIR / "v2_judge_outcomes.jsonl"`,
   `V2_FINAL_JSONL = Path("tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl")`.
   Add `code/constants.py` with `ANNOTATOR_MODEL_ID = "claude-sonnet-4-6-20251001"`,
   `JUDGE_MODEL_ID = "claude-haiku-4-5-20251001"`, `SAMPLE_SEED = 42`,
   `JUDGE_SAMPLE_PER_BENCHMARK = {"FrontierScience-Olympiad": 6, "SWE-bench Verified": 6, "WorkArena++": 6, "tau-bench": 5}`
   (totals 23), the cost-per-Mtok constants, the budget caps (annotator $12, judge $2), and the v2
   system prompt strings. Inputs: none. Outputs: two `.py` files. Satisfies REQ-1 (scaffolding
   only).

2. **Implement the annotator.** Create `code/v2_annotator.py` with a
   `run_annotator(input_path, output_path)` function that iterates the 115 v1 rows, builds the v2
   prompt with the full `row["problem"]` body, calls the local `claude` CLI with
   `--model claude-sonnet-4-6-20251001 --output-format json`, parses the JSON response, defends
   against bad JSON (markdown fences, partial output) by falling back to a per-row error note, and
   writes one v2-shaped row per input line to `_outputs/v2_annotated.jsonl`. Each row must include
   `_pilot_row_index` (the 0-based input row index). Track running cost; halt if
   `ANNOTATOR_BUDGET_CAP_USD` reached. Inputs: `V1_INPUT_PATH`. Outputs:
   `_outputs/v2_annotated.jsonl`, `_outputs/v2_annotator_costs.json`. Validation gate: dry-run on
   the first 3 rows and inspect the JSON output before the full run; baseline = "every row parses
   without falling back to error note". If ≥1 of the 3 dry-run rows lands in the error path, halt
   and inspect prompts before paying for the full 115. Satisfies REQ-1, REQ-2, REQ-3, REQ-7, REQ-8.

**Milestone 2 — Run annotation (Step 3)**

3. **[CRITICAL] Run the full annotator on all 115 rows.** Invoke
   `python -m tasks.t0009_hierarchical_annotation_v2.code.v2_annotator` via `run_with_logs.py`.
   Expected: `_outputs/v2_annotated.jsonl` exists with 115 lines, ≥95% of rows have
   `hierarchy.global != None` and ≥1 atomic somewhere in the tree, and
   `_outputs/v2_annotator_costs.json` `total_cost_usd` ≤ 12. If any of these checks fail, halt and
   create an intervention file. Satisfies REQ-1, REQ-7, REQ-8.

**Milestone 3 — Judge sampling and call (Steps 4-5)**

4. **Sample 23 rows for the judge.** Create `code/select_judge_sample.py` that reads
   `_outputs/v2_annotated.jsonl`, partitions rows by `benchmark`, and uses
   `random.Random(SAMPLE_SEED)` to draw `JUDGE_SAMPLE_PER_BENCHMARK[bench]` rows from each bucket
   without replacement. Writes the sample (with `_pilot_row_index` preserved) to
   `_outputs/v2_judge_sample.jsonl`. Inputs: `_outputs/v2_annotated.jsonl`. Outputs:
   `_outputs/v2_judge_sample.jsonl` with 23 rows. Validation: row count = 23, each benchmark present
   at expected count. Satisfies REQ-4.

5. **Implement and run the judge.** Create `code/v2_judge.py` adapted from
   `tasks/t0005_hierarchical_annotation_pilot_v1/code/judge_runner.py`. Differences from v1: the
   prompt embeds the **full** `row["problem"]` (no truncation), and the candidate hierarchy block is
   the v2 tree shape, and the model is haiku. Parse the JSON `{verdict, justification}` defensively.
   Track running cost; halt if `JUDGE_BUDGET_CAP_USD` reached. Inputs:
   `_outputs/v2_judge_sample.jsonl`. Outputs: `_outputs/v2_judge_outcomes.jsonl`,
   `_outputs/v2_judge_costs.json`. Validation gate: judge the first 3 rows in dry-run mode and
   confirm the JSON parses cleanly before the full 23. Baseline = "every dry-run row produces a
   verdict in {acceptable, needs revision}". If ≥1 fails, halt. Satisfies REQ-2, REQ-4, REQ-7.

**Milestone 4 — Asset assembly (Steps 6-8)**

6. **Build the dataset asset.** Create `code/build_v2_asset.py` that:
   * Reads `_outputs/v2_annotated.jsonl` (115 rows).
   * Reads `_outputs/v2_judge_outcomes.jsonl` and joins by `_pilot_row_index`.
   * For each row: writes `judge_verdict`, `judge_notes` (justification or error string). Unjudged
     rows get `null` for both.
   * Writes the merged 115-row JSONL to
     `assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`.
   * Writes `assets/dataset/hierarchical-annotation-v2/details.json` per the dataset spec
     (`spec_version: "2"`, `dataset_id: "hierarchical-annotation-v2"`, `version: "v2"`,
     `description_path: "description.md"`, `license: "inherited-per-row"`,
     `access_kind: "restricted"`, four categories from `meta/categories/`).
   * Writes `assets/dataset/hierarchical-annotation-v2/description.md` with the seven mandatory
     dataset description sections, explaining the v2 → v1 migration. Satisfies REQ-5.

7. **Compute the v2-vs-v1 comparison table.** Create `code/compute_stats.py` that reads both v1 and
   v2 jsonl files, computes per-benchmark `acceptable / (acceptable + needs revision)` accept rates,
   and writes a comparison JSON to `_outputs/v1_vs_v2_comparison.json` and a markdown table fragment
   to `_outputs/v1_vs_v2_table.md`. Outputs are read by the orchestrator's `results` step. Also
   computes:
   * `mean_atomics_per_row` (`avg_decisions_per_task` for `metrics.json`)
   * `global_atomics_fraction` =
     `total_global_atomics / (total_global_atomics + total subtask_atomics)` across all 115 rows.
   * `n_rows_complete_v2`: rows where v2 `hierarchy_completeness == true`. Satisfies REQ-6.

8. **Run all asset and dataset verificators in dry-run.** Execute
   `verify_dataset_asset --task-id t0009_hierarchical_annotation_v2 hierarchical-annotation-v2` via
   `run_with_logs.py`. Fix any errors before marking implementation complete.

## Remote Machines

None required. All work is local Python plus calls to the local `claude` CLI which forwards to the
Anthropic API. No GPU, no remote provisioning.

## Assets Needed

* **Input dataset**: v1 hierarchical annotation, 115 rows JSONL, located at
  `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`.
  This is read but not modified; t0005 is already merged.
* **Anthropic API access** via the local `claude` CLI (configured in the user's environment; same
  setup t0005 used). No API key file is touched in this task.
* No other tasks' code is imported. The v1 `judge_runner.py` is a *reference* for the prompt pattern
  but is not imported (cross-task imports are forbidden by project rule 9).

## Expected Assets

* **Dataset asset** `assets/dataset/hierarchical-annotation-v2/` containing:
  * `details.json` (dataset spec v2, `dataset_id: "hierarchical-annotation-v2"`, version `"v2"`, 115
    rows, four categories: `hierarchical-planning`, `benchmark-annotation`, `agent-evaluation`,
    `granularity-conditioning`).
  * `description.md` documenting the v2 → v1 migration, schema, and judge sample.
  * `files/hierarchical_annotation_v2.jsonl` with 115 rows in v2 schema.

This matches `task.json` `expected_assets: {dataset: 1}`.

## Time Estimation

* Research (already done): completed in step 4 (~25 minutes).
* Implementation pipeline coding (Steps 1-2, 4, 6, 7): ~30 minutes.
* Annotator full run (Step 3, 115 calls): ~15-25 minutes wall-clock with API latency.
* Judge full run (Step 5, 23 calls): ~3-5 minutes.
* Asset assembly + verification (Steps 6-8): ~10 minutes.
* Total wall-clock implementation: ~60-75 minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| `claude` CLI returns malformed JSON for some rows | Medium | Per-row data loss | Defensive parser strips markdown fences and falls back to a per-row error note with `hierarchy_completeness=false`; rerun affected rows manually if >5% fail |
| Anthropic API rate-limit or transient timeout | Medium | Annotator/judge halts mid-run | The runner is idempotent — it skips rows already present in the output JSONL; on retry, only missing rows are re-attempted |
| Annotator running cost exceeds $12 cap | Low | Partial dataset (some rows missing) | Hard halt in code; create an intervention file noting how many rows landed; the partial JSONL is still useful for downstream work |
| FrontierScience-Olympiad rows are too long even for full sonnet context | Low | Some rows truncated by API | Sonnet has 200k context; the longest pilot row is <10k chars. If truncation does occur, the response is logged and the row is flagged in the error column |
| Sample shape: tau-bench has 26 rows but we draw 5 (others draw 6) | Low | Mild stratification asymmetry | The 5/6/6/6 split is documented; the imbalance is at most one row per benchmark and does not affect the per-benchmark v2-vs-v1 comparison |
| Judge verdict variance between runs | Low | Slightly different accept rates on rerun | Temperature-0 calls + fixed sample seed make the haiku run deterministic up to API-side variance; the comparison table is a snapshot, not a population estimate |

## Verification Criteria

* Run
  `uv run python -m arf.scripts.verificators.verify_dataset_asset --task-id t0009_hierarchical_annotation_v2 hierarchical-annotation-v2`
  and confirm zero errors. (REQ-5)
* Confirm `assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl` exists,
  has exactly 115 lines, and every line is valid JSON with the v2 schema fields. Run `wc -l` and a
  one-liner Python check. (REQ-1, REQ-3)
* Confirm at least 23 rows have a non-null `judge_verdict` field, distributed across the four
  benchmarks per the stratified plan. (REQ-4)
* Confirm `_outputs/v2_annotator_costs.json` `total_cost_usd` ≤ 12 and
  `_outputs/v2_judge_costs.json` `total_cost_usd` ≤ 2; combined ≤ 15. (REQ-7)
* Confirm `_outputs/v1_vs_v2_comparison.json` exists with per-benchmark accept-rate deltas, and
  every benchmark name from v1 appears. (REQ-6)
* Confirm every row of the v2 jsonl has a `_pilot_row_index` integer field and the values are
  pairwise unique. (REQ-3)
* Confirm `hierarchy_completeness` is set on every row and computed under the stricter v2 rule (the
  count of `true` rows is reported in `results_detailed.md`). (REQ-8)
* Run `uv run ruff check --fix .`, `uv run ruff format .`, and
  `uv run mypy -p tasks.t0009_hierarchical_annotation_v2.code` and confirm zero errors.
