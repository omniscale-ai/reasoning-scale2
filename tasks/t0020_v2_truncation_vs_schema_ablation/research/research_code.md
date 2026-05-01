---
spec_version: "1"
task_id: "t0020_v2_truncation_vs_schema_ablation"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 4
libraries_found: 5
libraries_relevant: 0
date_completed: "2026-05-01"
status: "complete"
---
# Research Code

## Task Objective

Run one new annotation condition: the v2 tree schema applied to the same instance pool as t0014, but
with the problem text truncated to 1500 characters in BOTH annotator and judge prompts (matching the
t0005/t0009 v1 judge truncation exactly). Decompose the t0014 +57 pp v2-vs-v1 accept-rate delta into
a pure schema effect (text held constant) and a pure text-length effect (schema held constant).

## Library Landscape

The library aggregator returns 5 libraries (`scope_aware_react_v1`, `scope_unaware_planandsolve_v1`,
`matched_mismatch_v1`, plus two ABC-related entries). None are relevant to this task — the entire
pipeline is plain `claude` CLI calls plus JSON parsing on jsonl files. We re-use the well-tested
annotator/judge pipeline from `[t0014]` by copying its code into our `code/` directory rather than
importing across tasks (per the cross-task code reuse rule).

## Key Findings

### Truncation Mechanism (v1 baseline, t0005)

The v1 judge in `[t0005]` is the canonical "1500-char truncation" reference. Specifically:

* `tasks/t0005_hierarchical_annotation_pilot_v1/code/constants.py:33`:
  `JUDGE_PROBLEM_EXCERPT_LIMIT: Final[int] = 1500`.
* The user prompt template inserts `Problem (truncated to {limit} chars):\n{problem_excerpt}\n\n`.
* `judge_runner.py:55` defines `_truncate(text, *, limit) -> text[:limit] + "…"` — a hard cut with
  an ellipsis suffix.

The v1 ANNOTATOR also operated on truncated text (the original v1 design), so "v1-flat-truncated"
truly does mean both annotator and judge saw a 1500-char excerpt. The task description's intent is
to replicate this on the v2 tree schema: clip the same 1500 chars in both prompts.

### v2 Annotator/Judge Pipeline (t0009, t0014)

`[t0014]` is the most recent v2 pipeline; it uses claude-sonnet-4-6 for annotation and
claude-haiku-4-5 for judging. `[t0009]` is the v2-haiku reference (annotator = haiku, judge =
haiku). Both use:

* `ANNOTATOR_USER_TEMPLATE` with `Problem:\n{problem}` (no truncation).
* `JUDGE_USER_TEMPLATE` with `Full problem:\n{problem}` (no truncation).
* A `_call_claude_cli()` helper that invokes `claude -p - --model <id> --output-format json`,
  captures token usage and `total_cost_usd` from the envelope when present.
* A `ThreadPoolExecutor`-based parallel runner with idempotent jsonl appends (re-reads existing
  `_pilot_row_index` values to avoid double-spend).
* A `select_judge_sample.py` that intersects target indices with rows that have complete
  hierarchies; missing/incomplete rows are dropped and logged.

For this task we copy the t0014 patterns and modify only the two prompt templates (annotator and
judge) to insert truncation.

### Sample Pool Alignment

`[t0014]` produced 20 sonnet-judged rows after 3 sonnet timeouts dropped from the t0009 23-row
stratified sample. Ids analysis:

* 20 sonnet-judged ids ⊂ 23 haiku-judged ids (haiku\\sonnet = `{7, 8, 14}`).
* This means the same 20 `pilot_row_index` values can be re-used for v2-tree-truncated to enable
  paired comparison against both v2-tree-full (haiku) and v2-sonnet-full.

The v1 12-judged-row pool from `[t0005]` does not overlap with these 20 by `pilot_row_index` (v1
used a small 3-per-benchmark sample on different rows). So v1-vs-v2-truncated comparison is
benchmark-level accept-rate, not row-level paired.

### Cost Pricing (haiku-4-5)

`[t0014]` constants set `HAIKU_INPUT_COST_PER_MTOK_USD = 0.80` and
`HAIKU_OUTPUT_COST_PER_MTOK_USD = 4.00`, matching Anthropic's published list price as of 2026-04-30.
A typical haiku call on a v2 problem (2-3k input tokens, ~500 output tokens) costs about
$0.005-0.01, so 40 haiku annotation + 40 haiku judge calls fits well under the $2 ceiling.

## Reusable Code and Assets

For each item below, source = `tasks/t0014_v2_annotator_sonnet_rerun/code/`:

* **v2_annotator.py** (~620 lines) — full annotator harness (parallel, idempotent, budget-capped).
  Reuse method: **copy into task** and modify `ANNOTATOR_USER_TEMPLATE` to truncate the problem at
  1500 chars. Key signatures:
  `run_annotator(*, limit: int | None, dry_run: bool, workers: int) -> RunStats`,
  `_call_claude_cli(*, prompt: str, model: str, system_prompt: str) -> CliCallResult`,
  `_parse_v2_response(raw_text) -> tuple[hierarchy | None, gold_actions | None, notes]`. Adaptation:
  change `ANNOTATOR_USER_TEMPLATE` to insert `problem_excerpt` from a `_truncate` helper. Keep
  parsing logic intact.

* **v2_judge.py** (~370 lines) — judge harness with same parallel/idempotent pattern. Reuse method:
  **copy into task** and modify `JUDGE_USER_TEMPLATE` to insert truncated problem. Key signatures:
  `run_judge(*, limit, workers) -> RunStats`, `_judge_one(*, sample_row, model) -> JudgeOutcome`.

* **select_judge_sample.py** (~95 lines) — selects same `_pilot_row_index` set as upstream sample,
  intersected with rows that have complete hierarchies. Reuse method: **copy into task**, point
  `V2_HAIKU_JUDGE_SAMPLE_PATH` at the t0014 sonnet judge sample (the 20-row matched pool) and
  `V2_RAW_OUTPUT` at our truncated annotator output.

* **compute_stats.py** — three-way comparator with Wilson CIs and `_delta_with_ci(a, b)` helper.
  Reuse method: **copy into task** and adapt to compute the decomposition deltas instead of the
  schema/model deltas. The Wilson-CI implementation can stay verbatim.

* **t0005 truncation snippet** — lines 33, 55-58 of t0005's `constants.py` and `judge_runner.py`.
  Reuse method: **copy into task** as `JUDGE_PROBLEM_EXCERPT_LIMIT: Final[int] = 1500` and the
  `_truncate(text, *, limit) -> str` helper. Use the same helper for annotator-side truncation so
  both prompts see identical clipped text.

* **t0014 sonnet judge sample** (`v2_sonnet_judge_sample.jsonl`, 20 rows) — the matched pool. Read
  this file to get the `_pilot_row_index` set; for each id pull the original v1 row from
  `tasks/t0005_hierarchical_annotation_pilot_v1/.../hierarchical_annotation_v1.jsonl` and
  re-annotate with truncation on. Reuse method: **read-only data access** (no code copy needed).

## Lessons Learned

* `[t0009]` and `[t0014]` both encountered 3 sonnet/haiku timeouts on the FrontierScience benchmark
  (long problem text). With a 1500-char truncation in our condition, those calls become cheaper and
  shorter — call-failure rate should be at least as low as t0009's. Still, set a generous timeout
  (300s) and log call-failures the same way.
* The `claude` CLI returns `total_cost_usd` in its JSON envelope for haiku-4-5; trust this number
  over the char-based estimate when present. `[t0014]` validates this pattern.
* Idempotent jsonl appends (re-read `_pilot_row_index` set on each invocation) prevent double-spend
  on retries — critical for a task with a $2 ceiling.
* `[t0014]`'s `compute_stats.py` uses Wilson 95% CIs for binomial proportions; that's the correct
  test here (small-n with n=20 means Wilson is much better-calibrated than normal approximation).

## Recommendations for This Task

1. **Code structure**: copy t0014's `v2_annotator.py`, `v2_judge.py`, `select_judge_sample.py`, and
   `compute_stats.py` into `code/`. Rename to `v2_truncated_annotator.py`, `v2_truncated_judge.py`,
   etc. Modify only the prompt templates and the path constants.
2. **Truncation**: define `PROBLEM_EXCERPT_LIMIT: Final[int] = 1500` and a
   `_truncate(text, *, limit)` helper in `constants.py`. Use it in BOTH `ANNOTATOR_USER_TEMPLATE`
   and `JUDGE_USER_TEMPLATE`.
3. **Pool**: read `tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl`
   to get the 20-id matched pool; re-annotate those 20 rows from the v1 source jsonl with truncation
   on; then judge with truncation on.
4. **Reference data**: for the decomposition, intersect with the 20 haiku-judged rows (haiku judged
   23, sonnet 20 ⊂ 23). Compute v2-tree-full accept rate from t0009's `v2_judge_outcomes.jsonl`
   filtered to those 20 ids. v1-flat-truncated rate is the population 12-row v1 sample (12 different
   ids, not paired); report as a separate baseline.
5. **Stats**: Wilson 95% CIs for each rate; difference-of-proportions Wilson CI for the two
   decomposition deltas (pure-schema = trunc - v1, pure-text = full - trunc).
6. **Budget**: 20 annotations + 20 judge calls = 40 haiku calls. At ~$0.01 per call this is ~$0.40,
   well under the $2 ceiling.

## Task Index

### [t0005]

* **Task ID**: `t0005_hierarchical_annotation_pilot_v1`
* **Name**: Hierarchical Annotation Pilot v1
* **Status**: completed
* **Relevance**: Source of the canonical 1500-char truncation pattern
  (`JUDGE_PROBLEM_EXCERPT_LIMIT`, `_truncate` helper) and the v1-flat-truncated baseline 12-row
  judge sample. We replicate the truncation logic exactly.

### [t0009]

* **Task ID**: `t0009_hierarchical_annotation_v2`
* **Name**: Hierarchical Annotation v2
* **Status**: completed
* **Relevance**: Produced the v2-tree-full haiku reference (23-row stratified judge sample). Our
  v2-tree-full reference points are extracted from this task's `v2_judge_outcomes.jsonl` for paired
  comparison.

### [t0014]

* **Task ID**: `t0014_v2_annotator_sonnet_rerun`
* **Name**: V2 Annotator Sonnet Rerun
* **Status**: completed
* **Relevance**: The most recent v2 pipeline; we copy its annotator, judge, select_judge_sample, and
  compute_stats code structure verbatim. Its 20-row sonnet judge sample defines our matched instance
  pool.

### [t0019]

* **Task ID**: `t0019_v2_judge_calibration`
* **Name**: V2 Judge Calibration
* **Status**: in_progress
* **Relevance**: Addresses the judge-side calibration of the v2 result; this task addresses the
  input-side. Together they decompose the t0014 +57 pp delta. Our task does NOT depend on t0019 (per
  `task.json` `dependencies: []`).
