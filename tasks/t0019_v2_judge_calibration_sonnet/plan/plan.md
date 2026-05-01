---
spec_version: "2"
task_id: "t0019_v2_judge_calibration_sonnet"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: v2 Judge Calibration with Sonnet (Substantive + Familial Bias)

## Objective

Re-judge the same 55-row pool that t0014 produced (20 v2-sonnet annotations + 23 v2-haiku
annotations + 12 v1-sonnet annotations from t0005) under two new judge configurations using
`claude-sonnet-4-6`: (a) a **substantive critic** prompt that asks the judge to simulate execution
("verify each atomic, executed in order, would actually solve the problem") and emit a binary
verdict, and (b) a **model-rotated** judge that keeps the original t0014 judge prompt verbatim but
swaps the judge model from `claude-haiku-4-5` to `claude-sonnet-4-6`. We do NOT re-annotate;
annotator outputs are reused from t0014 (v2-sonnet, v2-haiku) and t0005 (v1-sonnet) via the t0015
benchmark-label correction overlay. Success means a per-row predictions asset, an answer asset, and
a `results/metrics.json` with 9 cells (3 annotators x 3 judge configs) reporting `accept_rate` and
Wilson 95% CI half-widths, plus a comparison table that lets us decide whether the +57 pp t0014
schema-only headline survives a stricter judge.

## Task Requirement Checklist

The operative task text from `task.json` and `task_description.md`:

> Re-judge the same 43 v2 rows that t0014 produced (20 v2-sonnet + 23 v2-haiku) plus the matched 20
> v1-sonnet rows from t0009/t0014, under two new judge configurations: substantive critic
> (S-0014-02) and model-rotated (S-0014-03). Both judges run against the same row pool. This task
> does not re-annotate. It only re-judges. Annotation rows from t0014 are read in via the existing
> predictions overlay applied by t0015. Total: 43 rows x 2 new judge configurations = 86 sonnet
> judge calls. Cost ceiling: $5.

Concrete requirements extracted from the task text:

* **REQ-1**: Re-judge 43 v2 rows (20 v2-sonnet + 23 v2-haiku) plus 20 v1-sonnet rows under two new
  configurations. Note: research_code.md found only 12 v1-sonnet judged rows in
  `tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/mapped_with_judge.jsonl`. We will use
  all 12 v1 rows that have a judge verdict and document the n=12 vs the task's claim of 20 in
  `## Limitations`. Effective n = 20 v2-sonnet + 23 v2-haiku + 12 v1-sonnet = 55 rows. Satisfied by
  steps 4-7.
* **REQ-2**: Use the substantive critic prompt with `claude-sonnet-4-6` as judge for one of the new
  configurations. Satisfied by step 4.
* **REQ-3**: Use the original t0014 judge prompt with `claude-sonnet-4-6` as judge for the other new
  configuration. Satisfied by step 5.
* **REQ-4**: Produce a predictions asset at `assets/predictions/v2-judge-calibration/` with per-row
  judge verdicts under the two new configurations plus the cached baseline t0014/t0015/t0005
  verdicts as reference, including `judge_prompt_version` and `judge_model` fields per row.
  Satisfied by step 7.
* **REQ-5**: Produce an answer asset addressing the question "Does the v2 schema retain a 30+ pp
  accept-rate delta over v1 under a substantive judge and under a sonnet judge, or is the +57 pp
  t0014 headline an artefact of haiku judge anchoring?". Satisfied by step 8.
* **REQ-6**: Write `results/metrics.json` using the explicit multi-variant format with 9 cells (3
  annotators x 3 judge configs), each reporting `accept_rate`, `accept_rate_stderr` (Wilson 95% CI
  half-width), `efficiency_inference_cost_per_item_usd`, and
  `efficiency_inference_time_per_item_seconds`. Note: research_code.md confirmed these metric keys
  are NOT yet registered in `meta/metrics/`. The task scope forbids editing files outside the task
  folder, so we cannot add new metric registrations from this task branch. Mitigation: emit raw
  metrics into `results/metrics.json` using only registered metric keys (see below) and put the full
  9-cell table with `accept_rate`, stderr, cost-per-item, and time-per-item into
  `results/results_detailed.md`. Satisfied by step 9.
* **REQ-7**: Generate `results/results_detailed.md` with a side-by-side comparison table showing
  schema-only and model-only deltas under all three judge configurations and explicit deltas vs
  t0014. Orchestrator-managed step (results), but the data shapes for the table are produced in step
  9\.
* **REQ-8**: Cost in `results/costs.json` must be at most $5. Satisfied by step 6's budget cap and
  step 10.
* **REQ-9**: Predictions asset passes `verify_predictions_asset.py`. Verified during reporting.
* **REQ-10**: Answer asset passes `verify_answer_asset.py`. Verified during reporting.
* **REQ-11**: Apply the t0015 benchmark-label correction overlay when assembling the v2-haiku rows
  (Mind2Web -> WorkArena++, HumanEval -> tau-bench mappings). Satisfied by step 1.
* **REQ-12**: Report Cohen's kappa across (substantive, model-rotated) at the same model as a free
  signal about prompt-vs-anchoring effects (per task description risk note). Satisfied by step 9.

## Approach

The task is a focused calibration sweep that re-runs only the LLM-as-judge stage on a fixed,
already-annotated row pool. No re-annotation is required. Prior research in
`tasks/t0019_v2_judge_calibration_sonnet/research/research_code.md` identified that t0014's
`v2_judge.py` already contains every needed code block: a CLI wrapper, a robust JSON-verdict parser
with markdown fence stripping, an idempotent thread-pool runner with a budget cap, and a Wilson 95%
CI helper. The cross-task import rule forbids importing those modules; we will copy the relevant
functions into `code/judge_runner.py`, `code/parse.py`, and `code/stats.py`.

Recommended task types: `comparative-analysis` and `data-analysis`. Both match the task: the
analysis compares three judge configurations (baseline-haiku, substantive-sonnet, model-rotated
sonnet) across three annotator conditions. Per the comparative-analysis Planning Guidelines we
define the comparison dimensions upfront (annotator x judge-prompt x judge-model), use identical
input rows across all conditions, and produce per-cell accept_rate plus pairwise deltas with Wilson
CIs. Per the data-analysis Planning Guidelines we generate at least one chart, report
counts-and-ratios in the markdown, and use named constants for column names and dtypes.

Departure from t0014: research_code.md recommended using the **Anthropic Python SDK directly**
(`anthropic.Anthropic().messages.create()`) instead of the `claude` CLI subprocess wrapper. The CLI
adds cache-creation overhead per call (~$0.06-0.12/call for haiku) that inflates costs and obscures
authoritative token counts. The SDK gives clean `usage.input_tokens` / `usage.output_tokens` and
exact wall-clock latency. The `anthropic` library is already in `pyproject.toml` (the CLI itself
wraps it). We use `claude-sonnet-4-6` as the model identifier in both new configurations.

**Substantive critic prompt design.** The new prompt extends the original judge prompt with a
"simulate execution" instruction: the judge must mentally walk through the atomics in order and
verify they would actually solve the original problem. Output schema stays binary (`verdict`
+ `justification`) so the existing parser is reused with no changes. Per-criterion sub-scores are
  optional: if the model emits them under a `sub_scores` key, we capture them in the predictions
  output for descriptive analysis but do not require them.

**Alternatives considered.** (a) Use a different stronger judge (e.g., GPT-4o or Gemini-2.5) to
isolate cross-vendor familial bias. Rejected because the project already commits to the Anthropic
SDK and a single-model rotation is sufficient to test the schema-only artefact hypothesis at this
budget; cross-vendor would re-open prompt compatibility questions and double the cost. (b)
Re-annotate before re-judging to strengthen statistical power. Rejected because re-annotation is a
separate experiment (S-0014-04 / t0023) with much higher cost; this task's purpose is to defend the
existing +57 pp headline before scaling. (c) Run a 100-row pool by adding new annotations. Rejected:
the task scope explicitly fixes the pool to 55 rows; expansion is t0023.

## Cost Estimation

* **Sonnet judge calls**: 55 rows x 2 new configurations = 110 calls. Per `task_description.md` and
  `tasks/t0014_v2_annotator_sonnet_rerun/code/constants.py`, sonnet pricing is $3.00/M input and
  $15.00/M output. Estimated tokens per call: ~5,000 input (system prompt ~250 tokens + user prompt
  ~4,500 tokens with hierarchy + gold_actions JSON + problem) and ~600 output (binary verdict + 1-2
  sentence justification, with optional sub_scores).
* **Total input tokens**: 110 x 5,000 = 550,000 -> 550,000 x $3 / 1,000,000 = **$1.65**.
* **Total output tokens**: 110 x 600 = 66,000 -> 66,000 x $15 / 1,000,000 = **$0.99**.
* **Subtotal**: **$2.64** for clean runs.
* **Retry / repair reserve**: $1.00 (covers transient API errors, parse failures, and one full
  re-run of one configuration if Cohen's kappa investigation requires it).
* **Total estimate**: **$3.64**, well within the **$5.00** task cap and the **$51.31** project
  budget left (per `aggregate_costs.py` summary, 2026-05-01).

We enforce a hard budget cap of **$4.50** at the runner level (a `threading.Event halt` triggered
when the per-call running total exceeds the cap, copied from t0014's pattern). If the cap fires we
truncate the run and document partial coverage in `## Limitations`.

## Step by Step

This is implementation-only. Results writing, suggestions, and compare-literature are
orchestrator-managed steps in execute-task.

1. **Build the row pool loader.** Create `code/data_loader.py` with constants for the three input
   JSONL paths (v2-sonnet, v2-haiku-corrected, v1-sonnet-with-judge). Read each file, filter to rows
   with `judge_verdict is not None`, normalize each row into a `PoolRow` frozen dataclass with
   fields: `_pilot_row_index`, `task_id`, `benchmark`, `domain`, `problem`, `hierarchy_json`,
   `gold_actions_json`, `annotator`, `baseline_verdict`, `source_file`. Apply the t0015
   benchmark-label correction overlay automatically by reading from
   `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
   for v2-haiku rather than the t0009 raw file. Expected output: a function
   `load_pool() -> list[PoolRow]` returning 55 rows. Satisfies REQ-1, REQ-11.

2. **Copy parse/stats helpers.** Create `code/parse.py` with `_strip_fences`,
   `_extract_first_json_object`, and `parse_verdict` (returns
   `(verdict, justification, notes, sub_scores | None)`) — copied verbatim from
   `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py` lines 121-193, extended to also extract
   an optional `sub_scores` dict if present. Create `code/stats.py` with
   `wilson_ci(*, k, n, z=1.96) -> tuple[float | None, float | None]` and `delta_with_ci(*, a, b)` —
   copied verbatim from `tasks/t0014_v2_annotator_sonnet_rerun/code/compute_stats.py` lines 161-199.
   Add `accept_rate_stderr_half_width(*, k, n)` returning `(upper - lower) / 2`. Add
   `cohens_kappa(*, a_labels, b_labels)` for the kappa computation in step 9. Satisfies REQ-12.

3. **Write the prompts and constants.** Create `code/constants.py` with:
   * `SONNET_INPUT_COST_PER_MTOK_USD = 3.00`, `SONNET_OUTPUT_COST_PER_MTOK_USD = 15.00`.
   * `JUDGE_MODEL_ID = "claude-sonnet-4-6"`.
   * `BUDGET_CAP_USD = 4.50`.
   * `ORIGINAL_JUDGE_SYSTEM_PROMPT` and `ORIGINAL_JUDGE_USER_TEMPLATE` — verbatim copies of
     `JUDGE_SYSTEM_PROMPT` and `JUDGE_USER_TEMPLATE` from
     `tasks/t0014_v2_annotator_sonnet_rerun/code/constants.py` lines 90-115.
   * `SUBSTANTIVE_JUDGE_SYSTEM_PROMPT`: extends the original prompt with the explicit instruction
     "Before deciding, mentally simulate executing the atomics in the listed order against the
     original problem statement. Mark `acceptable` only if the simulated execution would actually
     solve the problem; mark `needs revision` if the simulated execution exposes any missing,
     incorrect, or non-operational step. You may optionally include a `sub_scores` field with keys
     `coverage`, `executable`, `gold_actions_consistency`, each in {0, 1}.".
   * `SUBSTANTIVE_JUDGE_USER_TEMPLATE`: identical to `ORIGINAL_JUDGE_USER_TEMPLATE` (we want only
     the system prompt to differ so the user-facing input is held constant). Satisfies REQ-2, REQ-3.

4. **Build the SDK-based judge runner.** Create `code/judge_runner.py` with
   `call_anthropic(*, system_prompt, user_prompt, model, max_tokens=900) -> CallResult` using
   `anthropic.Anthropic().messages.create(...)`. `CallResult` (frozen dataclass) records `text`,
   `input_tokens`, `output_tokens`, `cost_usd`, and `elapsed_seconds`. Add
   `judge_one(*, row, prompt_kind, model, system_prompt, user_template) -> JudgeOutcome` that
   formats the user prompt, calls the SDK, parses the verdict, and returns a `JudgeOutcome` with all
   fields including `judge_prompt_version`, `judge_model`, `cost_usd`, `elapsed_seconds`. Add
   `run_pool(*, prompt_kind, model, system_prompt, user_template, output_jsonl_path, max_workers=4, budget_cap_usd=BUDGET_CAP_USD) -> RunStats`
   that uses `ThreadPoolExecutor` with idempotency by `_pilot_row_index`, append-mode JSONL output,
   and a `threading.Event halt` budget guard. Satisfies REQ-2, REQ-3.

   **Validation gate (per validation-gates rule).** Before any full run, the entry-point script
   takes a `--limit N` flag. The first invocation runs `--limit 5` against the substantive
   configuration, prints the verdicts, parses them, and stops. Trivial baseline: every row in t0014
   was judged `acceptable` by haiku at ~99% rate, so a substantive sonnet judge should accept
   strictly fewer than 100% on the 5-row probe AND yield zero parse failures. Failure conditions: if
   any of the 5 calls returns a parse failure, or per-call cost exceeds $0.10 (well above the
   estimate of ~$0.024/call), STOP and inspect individual responses. The agent must read all 5 probe
   responses, confirm the verdict format is well-formed and the justification is grounded in the
   simulated execution, and verify the cost matches expectations before launching the full run.

5. **Run the substantive configuration.** Create `code/run_substantive.py` that calls
   `run_pool(prompt_kind="substantive", model="claude-sonnet-4-6", system_prompt=SUBSTANTIVE_JUDGE_SYSTEM_PROMPT, user_template=SUBSTANTIVE_JUDGE_USER_TEMPLATE, output_jsonl_path=OUTPUTS_DIR / "substantive_outcomes.jsonl")`
   after the validation gate passes. Stage 5a: `--limit 5` validation gate (see step 4). Stage 5b:
   full 55-row run after gate passes. Idempotent — re-running skips already-judged rows. Expected
   output: 55 rows in `_outputs/substantive_outcomes.jsonl`, each with
   `verdict in {"acceptable", "needs revision"}` or `notes` indicating parse failure. Satisfies
   REQ-1, REQ-2.

6. **Run the model-rotated configuration.** Create `code/run_model_rotated.py` that calls
   `run_pool(prompt_kind="model_rotated", model="claude-sonnet-4-6", system_prompt=ORIGINAL_JUDGE_SYSTEM_PROMPT, user_template=ORIGINAL_JUDGE_USER_TEMPLATE, output_jsonl_path=OUTPUTS_DIR / "model_rotated_outcomes.jsonl")`.
   Same validation gate applies on stage 6a (`--limit 5`). Stage 6b: full 55-row run. Expected
   output: 55 rows in `_outputs/model_rotated_outcomes.jsonl`. Satisfies REQ-1, REQ-3.

7. **Build the predictions asset.** Create `code/build_predictions_asset.py` that reads the two
   outcome JSONLs and the baseline verdicts, joins them by `_pilot_row_index`, and writes:
   * `assets/predictions/v2-judge-calibration/files/predictions.jsonl` — one row per
     (`_pilot_row_index`, `judge_config`) pair, so 55 x 3 = 165 rows. Each row has
     `_pilot_row_index`, `task_id`, `benchmark`, `annotator`, `judge_prompt_version` (one of
     `original_haiku`, `substantive`, `model_rotated`), `judge_model` (one of `claude-haiku-4-5`,
     `claude-sonnet-4-6`), `verdict`, `justification`, `sub_scores`, `parse_status`, `cost_usd`,
     `elapsed_seconds`.
   * `assets/predictions/v2-judge-calibration/details.json` — per
     `meta/asset_types/predictions/specification.md`, with
     `predictions_id = "v2-judge-calibration"`, model description "Anthropic Sonnet 4.6 used as
     substantive critic and model-rotated judge over t0014's 55-row pool", `dataset_ids` referencing
     the source datasets, `instance_count = 165`, and `metrics_at_creation` populated with the 9
     accept_rate values.
   * `assets/predictions/v2-judge-calibration/description.md` — frontmatter + Metadata + Source
     Datasets + Prediction Schema + How to Reproduce + Quality Notes per the asset spec. Satisfies
     REQ-4.

8. **Build the answer asset.** Create `code/build_answer_asset.py` that writes
   `assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/`. Files:
   * `details.json` per `meta/asset_types/answer/specification.md`.
     `answer_methods = ["existing project findings", "code experiment"]`.
     `source_task_ids = ["t0014_v2_annotator_sonnet_rerun", "t0015_correct_proxy_benchmark_labels", "t0009_hierarchical_annotation_v2", "t0005_hierarchical_annotation_pilot_v1"]`.
     `source_paper_ids = ["10.18653_v1_2022.acl-long.244" (Zhou2022), "10.48550_arXiv.2410.04707" (Boisvert2024), "10.48550_arXiv.2402.10669" (Xiong2024)]`
     if these are present in the project's paper corpus; otherwise leave empty and cite via
     `source_urls`. `confidence = "medium"` (n=55 is small but sufficient to detect a 30 pp swing).
   * `short_answer.md` — frontmatter + 3-5 sentence direct answer to the question.
   * `full_answer.md` — frontmatter + Question + Direct Answer + Evidence (the 9-cell table) +
     Methodology + Limitations + Sources sections per the answer spec. Satisfies REQ-5.

9. **Compute statistics and write metrics.** Create `code/compute_stats.py` that reads the two new
   outcome JSONLs and the baseline (built from existing `judge_verdict` fields in the source files
   for v2-sonnet/v2-haiku and from `mapped_with_judge.jsonl` for v1-sonnet) and produces:
   * Per-cell accept_rate, Wilson 95% CI half-width, mean cost-per-item, mean time-per-item for each
     of 9 cells (annotator in {v1-sonnet, v2-haiku, v2-sonnet} x judge in {original-haiku,
     substantive-sonnet, model-rotated-sonnet}).
   * Schema-only delta (v2-haiku - v1-sonnet) and model-only delta (v2-sonnet - v2-haiku) under each
     of the three judge configurations, with delta CIs from `delta_with_ci`.
   * Cohen's kappa over the per-row binary verdicts between (substantive, model-rotated) judges,
     stratified by annotator.
   * `results/metrics.json` using the explicit multi-variant format. Variant ID format:
     `<annotator>_<judge_config>` (e.g., `v2-sonnet_substantive-sonnet`). Per-variant `metrics` uses
     ONLY the registered metric `task_success_rate` (we map `accept_rate` to `task_success_rate`
     because each judge call is a binary success/failure and the registered metric description
     allows "binary success on the full task"). The full per-cell table with `accept_rate`, stderr,
     cost-per-item, and time-per-item is duplicated into the orchestrator-managed
     `results/results_detailed.md`.
   * Charts: `results/images/accept_rate_3x3.png` (grouped bar chart, x = annotator, hue = judge
     config) and `results/images/schema_only_delta_by_judge.png` (3-bar chart of schema-only delta
     under each judge). Satisfies REQ-6, REQ-7, REQ-12.

10. **Compute final cost.** Create `code/build_costs.py` that reads the two outcome JSONLs, sums
    per-call `cost_usd` and `elapsed_seconds`, writes nothing (the orchestrator owns
    `results/costs.json`) but prints the running total to stdout so the orchestrator can copy the
    number into `results/costs.json` during the results step. Satisfies REQ-8.

## Remote Machines

None required. All judge calls go through the Anthropic API. Local CPU is sufficient for parsing,
statistics, and charting.

## Assets Needed

* **Input dataset (read-only)**: t0014's v2-sonnet annotation JSONL at
  `tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/files/hierarchical_annotation_v2_sonnet.jsonl`
  (115 rows, 20 with `judge_verdict`).
* **Input dataset (read-only)**: t0015 corrected v2-haiku JSONL at
  `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`
  (115 rows, 23 with `judge_verdict`, with corrected benchmark labels).
* **Input data file (read-only)**: t0005 v1-sonnet judge output at
  `tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/mapped_with_judge.jsonl` (115 rows, 12
  with `judge_verdict`).
* **Anthropic API access**: project budget covers up to $51.31; this task budget cap is $5.

## Expected Assets

* **predictions** asset `v2-judge-calibration` (REQ-4): 165-row JSONL with per-row judge verdicts
  under all three judge configurations plus annotator label, judge_prompt_version, judge_model,
  cost, and elapsed time. Conforms to `meta/asset_types/predictions/specification.md` v2.
* **answer** asset `does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges` (REQ-5):
  structured short-answer + full-answer pair with evidence table and decision-criteria check-off.
  Conforms to `meta/asset_types/answer/specification.md` v2.

These match `task.json` `expected_assets`: `{"predictions": 1, "answer": 1}`.

## Time Estimation

* Research (already done): 0 (steps 4-6 of step_tracker complete).
* Implementation phase (steps 1-10 above): ~90 minutes wall-clock total.
  * Code writing (steps 1-4 above + step 7-10): ~45 minutes.
  * Validation gate runs (steps 5a + 6a): ~3 minutes each = 6 minutes.
  * Full judge runs (steps 5b + 6b): 55 rows x ~12 s/call / 4 workers ~= 165 s per config = ~6
    minutes per config = 12 minutes total.
  * Predictions / answer asset build + verification (steps 7, 8): ~15 minutes.
  * Stats + charts (step 9): ~10 minutes.
* Orchestrator-managed reporting + verificators + PR + merge: ~30 minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Anthropic API rate limit triggers during 110-call run | medium | medium | 4-worker pool keeps concurrency low; runner uses exponential backoff on 429s; idempotent JSONL append means partial failures are resumable. |
| Substantive critic judge produces malformed JSON (e.g., emits prose) | medium | high | The parser already handles markdown fences and finds the first JSON object; the validation gate at `--limit 5` exposes parse failures before the full run; STOP if any of the 5 probe calls returns a parse failure. |
| Per-call sonnet cost > estimate, blowing the $5 cap | low | high | Hard `BUDGET_CAP_USD = 4.50` `threading.Event halt` in the runner stops new submissions when the running total exceeds the cap; the validation gate also asserts per-call cost <= $0.10. |
| Effective n is 55 (not 63 as task description says) | high | low | Document the n=12 v1 rows in `## Limitations`; the schema-only delta is still detectable at 95% Wilson CI for a 30 pp swing (k=10 v2 acceptable / 23 trials yields ~14-58% CI; k=5 v1 acceptable / 12 trials yields ~21-77% CI; non-overlap at 30 pp is feasible). |
| Substantive critic accepts everything (no calibration effect) | medium | medium | This IS the result; report honestly. The task is a calibration sweep, not a hypothesis-confirmation run. |
| Cohen's kappa low (substantive vs model-rotated disagree on most rows) | medium | medium | Report kappa and discuss; low kappa would itself be informative about prompt-anchoring vs model-anchoring effects. |
| Network or SDK error mid-run | medium | low | Idempotent append-mode JSONL output; restart the runner and it will skip already-judged rows. |
| Pre-mortem failure: agent silently substitutes a different model after seeing the cost | low | high | Plan locks `JUDGE_MODEL_ID = "claude-sonnet-4-6"` as a constant and documents it as REQ-2/REQ-3; any deviation must produce an intervention file. |

## Verification Criteria

* Predictions asset verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_predictions_asset --task-id t0019_v2_judge_calibration_sonnet`
  expected: zero errors. Satisfies REQ-9.
* Answer asset verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset --task-id t0019_v2_judge_calibration_sonnet`
  expected: zero errors. Satisfies REQ-10.
* Metrics file passes registered-metric validation:
  `uv run python -u -m arf.scripts.verificators.verify_task_metrics t0019_v2_judge_calibration_sonnet`
  expected: zero errors and at least 9 variants in `results/metrics.json`. Satisfies REQ-6.
* The 9-cell table in `results/results_detailed.md` reports the same accept_rate values as
  `results/metrics.json` `task_success_rate`. Satisfies REQ-7.
* `results/costs.json` `total_cost_usd` <= $5. Satisfies REQ-8.
* Cohen's kappa is reported in `results/results_detailed.md` for at least one (substantive,
  model_rotated) pair. Satisfies REQ-12.
* Step 5a / 6a `--limit 5` probes both produced 0 parse failures and per-call cost <= $0.10 (logged
  in `_outputs/run_log.txt`). Confirms the validation gate fired correctly.
* All 165 rows in `assets/predictions/v2-judge-calibration/files/predictions.jsonl` have
  `judge_prompt_version` and `judge_model` populated and
  `verdict in {"acceptable", "needs revision", null}` (null only when `parse_status != "ok"`).
  Confirms REQ-4 schema.
