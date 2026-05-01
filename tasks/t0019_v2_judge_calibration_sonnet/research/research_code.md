---
spec_version: "1"
task_id: "t0019_v2_judge_calibration_sonnet"
research_stage: "code"
tasks_reviewed: 18
tasks_cited: 4
libraries_found: 5
libraries_relevant: 0
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: v2 Judge Calibration with Sonnet

## Task Objective

Re-judge the 55-row pool from t0014 (20 v2-sonnet + 23 v2-haiku + 12 v1-sonnet judged rows) under
two new judge configurations using `claude-sonnet-4-6`: a **substantive critic** prompt (simulates
execution to verify whether each atomic, executed in order, would actually solve the problem) and a
**model-rotated** judge (original t0014 prompt, sonnet model instead of haiku). The output is a
predictions asset with per-row verdicts under all three judge configurations (baseline from t0014,
substantive, model-rotated), an answer asset addressing whether the +57 pp schema-only delta
survives a stricter judge, and a multi-variant `metrics.json` covering all 9 cells (3 annotators × 3
judge configs). No re-annotation occurs; this task only re-judges using the Anthropic API directly.

## Library Landscape

Five libraries exist in the project. None is relevant to this task.

* **scope_aware_react_v1** (`t0006`): ReAct agent with explicit granularity tags. Unrelated to
  judging or statistical analysis.
* **scope_unaware_planandsolve_v1** (`t0007`): Plan-and-Solve baseline agent. Unrelated.
* **matched_mismatch_v1** (`t0010`): Condition-C agent wrapper. Unrelated.
* **metric2_calibration_aggregator_v1** (`t0011`): Verbalized-confidence + self-consistency
  aggregator computing `overconfident_error_rate`. Not applicable to binary accept/reject judging.
* **phase2_smoke_harness_v1** (`t0012`): Experiment harness for A/B/C agent evaluation. Unrelated to
  LLM-as-judge calibration.

None of the registered libraries provides judging, cost-tracking, or Wilson-CI utilities that are
applicable here. All reusable code must be copied from prior task `code/` directories.

## Key Findings

### Judge Prompts and Parsing Pattern from t0014

The core judging pattern used in [t0014] is in
`tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py` (458 lines). The key elements:

* **`_call_claude_cli()`** (lines 81–118): Invokes the `claude` CLI via `subprocess.run` with
  `--output-format json`, extracts `result` from the envelope, reads `usage.input_tokens` and
  `usage.output_tokens` when available, and falls back to character-based estimates (~4
  chars/token). Uses a 300-second timeout. Returns a `CliCallResult` frozen dataclass.
* **`_parse_verdict()`** (lines 145–163): Strips markdown fencing, finds the first `{...}` JSON
  object via `_extract_first_json_object()`, normalizes verdict to `"acceptable"` or
  `"needs revision"`, and returns `(verdict, justification, notes)`. The `notes` field signals parse
  failures.
* **`_judge_one()`** (lines 165–193): Formats the `JUDGE_USER_TEMPLATE` with the row's benchmark,
  domain, problem, `hierarchy_json`, and `gold_actions_json`. Calls `_call_claude_cli()` then
  `_parse_verdict()`.
* **`run_judge()`** (lines 196–260): Thread-pool executor (default 4 workers), idempotent via
  `_load_existing_indices()`, budget cap via `threading.Event halt`, JSONL append mode. Key: already
  judged rows (by `_pilot_row_index`) are skipped.
* **Output schema** (`_outputs/v2_sonnet_judge_outcomes.jsonl`): per row — `pilot_row_index`,
  `task_id`, `benchmark`, `verdict`, `justification`, `notes`, `cost_usd`. No input/output token
  counts in the file (only in the costs JSON). This task needs to extend the schema with
  `judge_prompt_version` and `judge_model` fields.

The **original judge system prompt** (`JUDGE_SYSTEM_PROMPT` in `constants.py`, lines 90–105 of
`tasks/t0014_v2_annotator_sonnet_rerun/code/constants.py`): checks that (1) global captures the
plan, (2) subtasks cover what the problem asks, (3) atomics under each subtask are operational steps
executed in order, (4) global_atomics crosses subtasks, (5) gold_actions mirrors the structure.
Binary verdict only: no per-criterion sub-scores. This is the exact prompt to reuse for the
**model-rotated** condition.

The **original judge user template** (`JUDGE_USER_TEMPLATE`, `constants.py` lines 106–115):

```
Benchmark: {benchmark}
Domain: {domain}

Full problem:
{problem}

Candidate v2 hierarchy:
{hierarchy_json}

Candidate v2 gold_actions:
{gold_actions_json}

Output the JSON verdict now.
```

This exact template is reused for the model-rotated condition; only `JUDGE_MODEL_ID` changes from
`claude-haiku-4-5` to `claude-sonnet-4-6`.

### Row Pool Assembly from Multiple Source Files

The 55 judged rows come from three separate JSONL files:

* **v2-sonnet judged rows** (n=20): embedded in
  `tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/files/hierarchical_annotation_v2_sonnet.jsonl`
  — rows where `judge_verdict` is non-null. Fields include `_pilot_row_index`, `task_id`,
  `benchmark`, `problem`, `hierarchy`, `gold_actions`, `judge_verdict`, `annotation_model`.
* **v2-haiku judged rows** (n=23): embedded in
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
  — rows where `judge_verdict` is non-null.
* **v1-sonnet judged rows** (n=12): in
  `tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/mapped_with_judge.jsonl` — rows where
  `judge_verdict` is non-null. Note: v1 uses a different flat schema (`hierarchy.global`,
  `hierarchy.subtask[]`, `hierarchy.atomic[]` vs the v2 tree schema). The v1 judge prompt was also
  different (t0005 used a v1-specific template). For re-judging v1 rows under the new conditions,
  the same v2 judge prompt format is used with the v1 hierarchy rendered as JSON.

Note: t0015's correction overlay relabels Mind2Web → WorkArena++ and HumanEval → tau-bench in the
t0009 v2-haiku dataset. The effective corrected file is in
`tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`.
Per the correction spec, this file replaces the original for analysis purposes. However, since we
are re-judging existing rows (not re-computing per-benchmark statistics from scratch), we should use
the corrected benchmark labels from t0015 when assembling the row pool.

### Cost and Token Tracking Pattern

[t0014]'s `_call_claude_cli()` returns a `CliCallResult` with `input_tokens`, `output_tokens`,
`cost_usd`. The CLI's `--output-format json` envelope exposes `usage.input_tokens` and
`usage.output_tokens` when the Claude Code CLI returns them; the code falls back to `len(text) / 4`
estimates otherwise. The `total_cost_usd` field in the envelope (when present) overrides the
computed estimate.

For this task, the sonnet pricing is `$3.00/M` input, `$15.00/M` output. The per-call cost formula
from [t0014] `constants.py`:

```python
cost_usd = input_tokens * 3.00 / 1_000_000 + output_tokens * 15.00 / 1_000_000
```

### Wilson Confidence Intervals and Statistics Pattern

[t0014]'s `compute_stats.py` implements `_wilson_ci(k, n, z=1.96)` (lines 161–176). This is the
exact function needed for `accept_rate_stderr` (Wilson 95% CI half-width) in the multi-variant
metrics. The function returns `(lower, upper)` bounds. For `accept_rate_stderr` we can report half
the CI width: `(upper - lower) / 2`.

The `_delta_with_ci()` function in `compute_stats.py` (lines 178–199) computes deltas with Wilson
CIs on both sides and is reusable for the side-by-side delta table in `results_detailed.md`.

### Idempotency and Parallel Execution Pattern

[t0014]'s `run_judge()` uses `ThreadPoolExecutor(max_workers=4)` with an append-mode JSONL output
and an existing-index set for idempotency. This pattern works for parallelizing the 55 × 2 = 110
judge calls. A 4-worker pool at ~10–30 s/call will complete in ~5–15 minutes.

The pattern also includes a budget-cap `threading.Event halt` that stops new submissions when the
running total exceeds the cap. This should be retained with a `$6` cap (slightly above the $5 task
budget to allow for retry overhead).

### v1 Schema Difference

The v1 flat schema (`t0005`) uses `hierarchy.subtask` (list of strings) and `hierarchy.atomic` (list
of strings), not the tree structure (`hierarchy.subtasks[].atomics[]`) of v2. When feeding v1 rows
to the v2 judge prompts, the hierarchy JSON is rendered as-is; the judge can handle either schema
since it evaluates structural and semantic coverage, not a specific schema. This is documented in
[t0005]'s `judge_runner.py` (uses a different v1-specific prompt template that references `global`,
`subtask[]`, and `atomic[]` directly).

### Metrics Registry Alignment

Registered metrics in `meta/metrics/` must be checked before writing `results/metrics.json`. The
multi-variant format is:
`{"variants": [{"variant_id": "...", "dimensions": {...}, "metrics": {...}}]}`. Required metrics per
cell: `accept_rate`, `accept_rate_stderr`, `efficiency_inference_cost_per_item_usd`,
`efficiency_inference_time_per_item_seconds`. These must be registered to be usable in metrics.json.

## Reusable Code and Assets

All reusable items are from `tasks/t0014_v2_annotator_sonnet_rerun/code/`. Cross-task imports from
other task `code/` directories are forbidden; all items below must be **copied into task**.

### `_call_claude_cli()` — CLI wrapper

* **Source**: `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py`, lines 81–118 (~38 lines)
* **What it does**: subprocess call to the `claude` CLI with `--output-format json`, extracts the
  result and usage tokens, falls back to character estimates, returns `CliCallResult`.
* **Reuse method**: **copy into task** →
  `tasks/t0019_v2_judge_calibration_sonnet/code/judge_runner.py`
* **Signature**: `_call_claude_cli(*, prompt: str, model: str, system_prompt: str) -> CliCallResult`
* **Adaptation needed**: The t0014 version takes `system_prompt` as a parameter. Extend to accept a
  `timeout` parameter (default 300 s) and log per-call timing via `time.monotonic()`.

### `_parse_verdict()` and `_extract_first_json_object()` — verdict parser

* **Source**: `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py`, lines 121–163 (~43 lines)
* **What it does**: strips markdown fencing, extracts the first JSON object, normalizes
  `"acceptable"` / `"needs revision"`, returns `(verdict, justification, notes)`.
* **Reuse method**: **copy into task**
* **Signature**: `_parse_verdict(*, raw_text: str) -> tuple[str | None, str | None, str]`
* **Adaptation needed**: For the substantive critic judge, extend `_parse_verdict_substantive()` to
  also extract `sub_scores` if the judge returns per-criterion fields.

### `_wilson_ci()` — Wilson confidence interval

* **Source**: `tasks/t0014_v2_annotator_sonnet_rerun/code/compute_stats.py`, lines 161–176 (~16
  lines)
* **What it does**: Computes Wilson 95% CI for a binomial proportion. Returns `(lower, upper)`.
* **Reuse method**: **copy into task** → `tasks/t0019_v2_judge_calibration_sonnet/code/stats.py`
* **Signature**:
  `_wilson_ci(*, k: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]`
* **Adaptation needed**: None; copy verbatim.

### `_delta_with_ci()` — pairwise delta with CIs

* **Source**: `tasks/t0014_v2_annotator_sonnet_rerun/code/compute_stats.py`, lines 178–199 (~22
  lines)
* **What it does**: Computes accept-rate delta `a - b` with Wilson CIs for both sides.
* **Reuse method**: **copy into task** → `tasks/t0019_v2_judge_calibration_sonnet/code/stats.py`
* **Signature**: `_delta_with_ci(*, a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]`

### `JUDGE_SYSTEM_PROMPT` and `JUDGE_USER_TEMPLATE` — original judge prompt

* **Source**: `tasks/t0014_v2_annotator_sonnet_rerun/code/constants.py`, lines 90–115
* **What it does**: The original haiku judge system and user prompt templates — used verbatim for
  the **model-rotated** condition (only model changes).
* **Reuse method**: **copy into task** → `tasks/t0019_v2_judge_calibration_sonnet/code/constants.py`
* **Adaptation needed**: Rename constants for clarity: `ORIGINAL_JUDGE_SYSTEM_PROMPT`,
  `ORIGINAL_JUDGE_USER_TEMPLATE`. Add new `SUBSTANTIVE_JUDGE_SYSTEM_PROMPT` and
  `SUBSTANTIVE_JUDGE_USER_TEMPLATE`.

### Source data paths

* v2-sonnet dataset:
  `tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/files/hierarchical_annotation_v2_sonnet.jsonl`
* v2-haiku corrected dataset:
  `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
* v1-sonnet with judge:
  `tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/mapped_with_judge.jsonl`

## Dataset Landscape

Three datasets are used as read-only inputs:

* **hierarchical-annotation-v2-sonnet** (`t0014`): 115 rows, 20 judged by `claude-haiku-4-5`. JSONL
  with fields: `_pilot_row_index`, `task_id`, `benchmark`, `problem`, `hierarchy`, `gold_actions`,
  `judge_verdict`, `annotation_model`.
* **hierarchical-annotation-v2** (`t0009`, corrected by `t0015`): 115 rows, 23 judged. Same v2 tree
  schema. Effective corrected file: `hierarchical_annotation_v2_relabeled.jsonl` from t0015. The
  benchmark labels for 52 rows differ from the uncorrected file.
* **v1 mapped_with_judge** (`t0005`): 115 rows, 12 judged. Flat schema (`hierarchy.global`,
  `.subtask[]`, `.atomic[]`). Located in `code/_outputs/`, not in `assets/`.

## Lessons Learned

* **Claude CLI overhead**: t0014 and t0009 documented that the Claude Code CLI invokes
  cache-creation overhead on each call (~$0.06–0.12/call for Haiku despite the "estimated" cost
  being much lower). For Sonnet the per-call cost is higher; the `total_cost_usd` field in the CLI
  envelope is authoritative when present. The task should always prefer the envelope's
  `total_cost_usd` over the character-based estimate.
* **Idempotency via `_pilot_row_index`**: t0014's approach of keying the existing-outcomes set on
  `_pilot_row_index` is the correct pattern because `task_id` is not globally unique within a JSONL
  that mixes benchmarks.
* **v1 haiku timeouts**: t0009 had 3 FrontierScience-Olympiad sonnet annotation timeouts that
  reduced the judge sample from 23 to 20. The equivalent issue for this task is already baked in —
  we inherit exactly those 20 and 23 rows, and the 12 v1 rows are fixed. No new annotation occurs.
* **JSON parse failures**: t0014 saw no parse failures on haiku but the pattern of
  `_parse_verdict()` using `_extract_first_json_object()` proved robust against markdown fencing and
  extra prose. Keep this pattern.
* **Thread-pool with budget cap**: The `halt = threading.Event()` budget enforcement in t0014's
  `run_judge()` correctly prevents over-spending when running parallel jobs. This pattern is
  essential for the 110-call budget-sensitive run.
* **Per-row timing not tracked**: t0014 did not record per-call wall-clock time in the outcomes
  JSONL. This task needs `elapsed_seconds` per row in the output for the
  `efficiency_inference_time_per_item_seconds` metric.

## Recommendations for This Task

1. **Copy `_call_claude_cli()`, `_parse_verdict()`, `_extract_first_json_object()`, and the
   `CliCallResult` dataclass** from `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py` into
   `tasks/t0019_v2_judge_calibration_sonnet/code/judge_runner.py`. Extend `_call_claude_cli()` to
   record `elapsed_seconds` via `time.monotonic()`.

2. **Copy `_wilson_ci()` and `_delta_with_ci()`** from
   `tasks/t0014_v2_annotator_sonnet_rerun/code/compute_stats.py` into
   `tasks/t0019_v2_judge_calibration_sonnet/code/stats.py`.

3. **Use the t0015 corrected file** for v2-haiku rows to get correct benchmark labels in
   per-benchmark breakdowns.

4. **Design the new substantive critic prompt** to produce binary `verdict` + `justification` (same
   as the original) but with the additional instruction to simulate execution. Keep the output
   schema identical to avoid a new parser. Per-criterion sub-scores are optional; if the model
   returns them, capture them in a `sub_scores` field but do not require them.

5. **Use the Anthropic Python SDK directly** (not the Claude CLI subprocess) to reduce per-call
   overhead and get clean token counts. The CLI's cache-creation overhead inflates costs; the SDK
   `anthropic.Anthropic().messages.create()` call gives authoritative `usage.input_tokens`,
   `usage.output_tokens`, and response latency. This is a departure from t0014's approach but better
   suits the 110-call budget.

6. **Run both judge conditions in a single script** with a `judge_config` parameter (`"substantive"`
   or `"model_rotated"`), writing to separate JSONL output files. Use 4 parallel workers per config.

7. **Verify registered metrics** before writing `metrics.json`. Run
   `uv run python -u -m arf.scripts.aggregators.aggregate_metrics --format ids` to confirm that
   `accept_rate`, `accept_rate_stderr`, `efficiency_inference_cost_per_item_usd`, and
   `efficiency_inference_time_per_item_seconds` are all registered.

## Task Index

### [t0005]

* **Task ID**: t0005_hierarchical_annotation_pilot_v1
* **Name**: Hierarchical annotation pilot v1: audit and conform existing 115 rows
* **Status**: completed
* **Relevance**: Provides the v1-sonnet judged rows (n=12) in
  `code/_outputs/mapped_with_judge.jsonl`. The v1 flat schema (global/subtask/atomic lists vs the v2
  tree) must be understood when feeding v1 rows to the new v2-format judge prompts.

### [t0009]

* **Task ID**: t0009_hierarchical_annotation_v2
* **Name**: Hierarchical annotation v2: tree schema with subtask-to-atomic edges
* **Status**: completed
* **Relevance**: Provides the v2-haiku judged rows (n=23) in the dataset asset file. The judge
  outcomes JSONL at `code/_outputs/v2_judge_outcomes.jsonl` (23 rows) shows the per-row haiku
  verdicts that serve as the baseline for the model-rotated and substantive conditions.

### [t0014]

* **Task ID**: t0014_v2_annotator_sonnet_rerun
* **Name**: v2 annotator Sonnet rerun: deconfound schema vs model
* **Status**: completed
* **Relevance**: The primary source of reusable code. `v2_judge.py` contains the
  `_call_claude_cli()`, `_parse_verdict()`, and `run_judge()` patterns. `compute_stats.py` has
  `_wilson_ci()` and `_delta_with_ci()`. `constants.py` has the original judge system prompt and
  user template needed for the model-rotated condition. The three-way comparison logic is the
  template for the nine-cell comparison table.

### [t0015]

* **Task ID**: t0015_correct_proxy_benchmark_labels
* **Name**: Correct proxy-benchmark labels in t0009 v2 dataset
* **Status**: completed
* **Relevance**: Provides the corrected v2-haiku JSONL with accurate benchmark labels (Mind2Web
  instead of WorkArena++, HumanEval instead of tau-bench) at
  `assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`.
  Per-benchmark breakdowns in this task must use the corrected labels.
