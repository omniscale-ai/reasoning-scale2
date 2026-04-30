---
spec_version: "2"
task_id: "t0014_v2_annotator_sonnet_rerun"
date_completed: "2026-04-30"
status: "complete"
---
# Plan: v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)

## Objective

Produce a new dataset asset, `hierarchical-annotation-v2-sonnet`, that re-annotates the same 115 v1
pilot rows under the v2 tree schema using `claude-sonnet-4-6` as the annotator, then re-runs the
same `claude-haiku-4-5` judge on the same 23-row stratified sample (seed=42) used by t0009. Compute
three judge accept-rate deltas (schema-only, model-only, original headline) per benchmark and in
aggregate. "Done" means: the new asset is persisted and verified, the three deltas are tabulated
with Wilson 95% confidence intervals, and follow-up suggestions reflect which component dominates.

## Task Requirement Checklist

The operative request from `tasks/t0014_v2_annotator_sonnet_rerun/task.json` and
`task_description.md`:

```text
Re-run the v2 tree-schema annotator with claude-sonnet-4-6 on the same 115 rows; reuse the
haiku judge on the same stratified sample to isolate the schema component of t0009's +58 pp
delta.

Scope:
- Re-annotate the same 115 rows under the same v2 tree schema using claude-sonnet-4-6 as the
  annotator.
- Use the same prompt as t0009 (full problem text, tree-schema system instructions).
- Judge with the same claude-haiku-4-5 judge on the same 23-row stratified sample used in
  t0009 (same row IDs, same seed=42).
- Report per-benchmark and aggregate judge accept rate. Compare against v2-haiku and v1-sonnet
  to decompose the +58 pp delta into a schema component and a model component.
- Persist as a new dataset asset under assets/dataset/hierarchical-annotation-v2-sonnet/ with
  details.json, description.md, and files/hierarchical_annotation_v2_sonnet.jsonl.
- Apply the t0009 task_id deduplication fix.

Key Questions:
1. What is the per-benchmark accept-rate delta of v2-sonnet vs v2-haiku?
2. What is the per-benchmark accept-rate delta of v2-sonnet vs v1-sonnet?
3. Does FrontierScience-Olympiad improve under v2-sonnet? By how much vs t0009 v2-haiku?
4. If the schema component is small, is there a v3 schema change worth scoping?

Compute and budget: no GPU, Anthropic API only, ~$5 estimated, $10 hard cap.
```

| ID | Requirement | Step(s) | Evidence of completion |
| --- | --- | --- | --- |
| REQ-1 | Re-annotate the same 115 rows under v2 tree schema with `claude-sonnet-4-6`. | Steps 2-4 | `code/_outputs/v2_sonnet_annotated.jsonl` has exactly 115 rows; every row's `annotation_model` field is `"claude-sonnet-4-6"`. |
| REQ-2 | Reuse the t0009 v2 prompts (system + user) verbatim, including full problem text. | Step 2 | The copied `code/constants.py` contains `ANNOTATOR_SYSTEM_PROMPT` and `ANNOTATOR_USER_TEMPLATE` byte-identical to t0009's; only `ANNOTATOR_MODEL_ID` and budget cap differ. |
| REQ-3 | Apply the t0009 `task_id` deduplication fix (the v1 source has 14 task_id collisions; the v2 schema keys on `_pilot_row_index` not `task_id`). | Steps 2-3 | Final jsonl has 115 unique `_pilot_row_index` values; `task_id` values may repeat as in t0009. |
| REQ-4 | Reuse the same 23-row stratified sample at seed=42 (FrontierScience-Olympiad=6, SWE-bench Verified=6, WorkArena++=6, tau-bench=5). | Step 5 | Sample selector deterministically reproduces the same 23 `_pilot_row_index` set as t0009 when completeness is 115/115; if completeness drops, intersection logged. |
| REQ-5 | Run `claude-haiku-4-5` judge on the v2-sonnet hierarchies for the 23 sampled rows. | Step 6 | `code/_outputs/v2_sonnet_judge_outcomes.jsonl` has 23 rows; every row has `verdict in {acceptable, needs revision}`. |
| REQ-6 | Compute schema-only delta (v2-sonnet vs v1-sonnet). | Step 8 | `_outputs/three_way_comparison.json` field `schema_only` populated per benchmark and aggregate, with Wilson 95% CIs. |
| REQ-7 | Compute model-only delta (v2-sonnet vs v2-haiku). | Step 8 | `_outputs/three_way_comparison.json` field `model_only` populated. |
| REQ-8 | Re-derive the original headline delta (v2-haiku vs v1-sonnet). | Step 8 | `_outputs/three_way_comparison.json` field `headline` populated; matches t0009's published numbers within sampling noise. |
| REQ-9 | Persist the dataset asset at `assets/dataset/hierarchical-annotation-v2-sonnet/` with `details.json` + `description.md` + `files/hierarchical_annotation_v2_sonnet.jsonl`. | Step 7 | `verify_dataset_asset` passes with no errors. |
| REQ-10 | Stay within the $10 task budget. | Step 1 (dry-run gate) and Step 4 (live-run cap) | `code/_outputs/v2_sonnet_annotator_costs.json` `total_cost_usd` < $10 and `code/_outputs/v2_sonnet_judge_costs.json` `total_cost_usd` < $2. |
| REQ-11 | Answer Key Question 4 in suggestions: if schema component is small, propose a v3 schema iteration; if model component dominates, propose a sonnet-default policy. | Reporting step (orchestrated separately) | `results/suggestions.json` contains at least one suggestion that explicitly cites the schema-only and model-only deltas. |

## Approach

The technical approach is a controlled-experiment rerun. We hold three of the four experimental
factors constant and vary exactly one: the annotator model. The factors are:

1. **Schema** (flat list-of-strings vs tree). Held constant at *tree* (matches t0009).
2. **Annotator model** (`claude-sonnet-4-6` vs `claude-haiku-4-5`). **Varied** — t0014 uses sonnet,
   t0009 used haiku.
3. **Judge model** (`claude-haiku-4-5`). Held constant — same model that judged t0009 v2-haiku and
   t0005 v1.
4. **Sample** (seed=42 stratified 6/6/6/5 split = 23 rows). Held constant.

This means t0014's accept rate vs t0009's accept rate isolates the **annotator-model component** of
the original +58 pp v2-vs-v1 delta. t0014's accept rate vs t0005's v1 accept rate (sonnet annotator,
flat schema) isolates the **schema component**. The two components decompose the headline delta
cleanly:

> headline = schema_only + model_only + interaction

where `interaction` measures whether the schema and the model interact (e.g., sonnet only helps
under tree, or vice versa). With small samples (n=23) the interaction term is hard to estimate
precisely, so we report all three direct deltas with CIs and let the reader infer interaction from
the pattern.

**Research findings embedded:**

* Zhou2022 reports +16 pp accuracy on hierarchical reasoning when adding parent-child edges (flat ->
  tree). t0014's expected schema-only delta is in the **+15 to +35 pp** band.
* Boisvert2024 reports +25 pp on WorkArena++ with task-tree structure. Within band.
* Xiong2024 reports +9 pp from haiku -> sonnet on judge-bias-controlled annotation tasks. t0014's
  expected model-only delta is in the **0 to +9 pp** band.
* t0009 (`results_summary.md`) measured a +59 pp aggregate v2-haiku vs v1-sonnet delta. If
  schema-only ≈ +25 pp and model-only ≈ +9 pp under the same direction of effect, the arithmetic
  does NOT close to +59 pp without an interaction term — implying either schema is doing more than
  +25 pp or there is a positive interaction. We will surface this gap honestly rather than fudge it.

**Reuse plan:** Per `research/research_code.md`, eight code modules from t0009 are copied into
`tasks/t0014_v2_annotator_sonnet_rerun/code/` and changed only at two constants. No registered
libraries are imported (none touch annotation/judge work).

**Alternatives considered:**

* **A. Subsample to 60 rows on sonnet to halve cost.** Rejected: would break the same-sample
  guarantee for the model-only delta and would not let us cross-check t0009's headline number.
* **B. Use a different judge (e.g., GPT-4o) to remove judge-haiku bias.** Rejected: changing the
  judge would re-introduce a confound on the model-only axis and would prevent direct comparison
  with t0009's published numbers. Add this as a future suggestion if t0014's results warrant.
* **C. Use the Anthropic API directly instead of the Claude Code CLI.** Considered. Rejected because
  t0009 used the CLI, so changing it would introduce yet another varying factor (input formatting,
  system-prompt caching). The CLI's per-call cost on sonnet is the binding budget constraint,
  mitigated by the dry-run gate.

**Task types:** `hierarchical-annotation` and `comparative-analysis` (matches `task.json`). The
hierarchical-annotation type's planning guidance ("hold prompt and schema constant; vary only the
named factor under test") informs Steps 2-6. The comparative-analysis type's guidance ("report
deltas with CIs; surface interaction terms honestly") informs Step 8 and the eventual results
writeup.

## Cost Estimation

| Item | Quantity | Unit cost | Subtotal |
| --- | --- | --- | --- |
| Sonnet annotator calls (115 rows) | 115 | ~$0.04-0.08/call (envelope-reported, full problem text + tree response) | ~$5-9 |
| Haiku judge calls (23 rows) | 23 | ~$0.07/call (matches t0009's $1.68 / 23 ≈ $0.073) | ~$1.7 |
| **Estimated total** |  |  | **~$5-11** |
| **Hard cap** |  |  | **$10 (task description) + $2 judge cap = $12 envelope** |

Compared against `project/budget.json`: the total project budget is $200; this task uses ~3-5% of
remaining headroom. The annotator's hard cap is set at $10 in code (lower of estimate and task
ceiling); a per-call cost > $0.20 will trigger a halt during the dry-run gate (Step 1) so we never
reach the cap blindly. If the dry-run reports per-call cost in the $0.10-0.20 band, we'll consider
lowering `workers` from 4 to 2 to slow down the spend rate (the cap will still be enforced; this is
just to leave more time to react manually if needed).

## Step by Step

**Milestone A: Code scaffolding (Steps 1-2).** Copy and parameterise all reusable t0009 code.

**Milestone B: Validation gate (Step 3).** 5-row dry-run on sonnet to confirm per-call cost.

**Milestone C: Live annotation + judging (Steps 4-6).** Full 115-row annotation, sample selection,
23-row judging.

**Milestone D: Asset assembly + analysis (Steps 7-8).** Build dataset asset, compute three-way
deltas, generate charts.

* * *

1. **Copy reusable code from t0009.** Copy these eight files from
   `tasks/t0009_hierarchical_annotation_v2/code/` into `tasks/t0014_v2_annotator_sonnet_rerun/code/`
   (keep filenames identical so cross-references stay clean): `v2_annotator.py`, `v2_judge.py`,
   `select_judge_sample.py`, `build_v2_asset.py`, `compute_stats.py`, `make_charts.py`,
   `constants.py`, `paths.py`. Update every `from tasks.t0009_hierarchical_annotation_v2.code...`
   import to `from tasks.t0014_v2_annotator_sonnet_rerun.code...`. Expected output: `code/` has 8
   .py files plus `__init__.py`. Satisfies REQ-2.

2. **[CRITICAL] Parameterise constants.py and paths.py for sonnet.** In the copied
   `code/constants.py` change exactly: `ANNOTATOR_MODEL_ID = "claude-sonnet-4-6"` and
   `ANNOTATOR_BUDGET_CAP_USD = 10.0`. Hold `JUDGE_MODEL_ID = "claude-haiku-4-5"`,
   `SAMPLE_SEED = 42`,
   `JUDGE_SAMPLE_PER_BENCHMARK = {Olympiad: 6, SWE-bench: 6, WorkArena++: 6, tau-bench: 5}`. In
   `code/v2_annotator.py` `_cost_usd()` change the price constants used for fallback estimates from
   `HAIKU_*_COST_PER_MTOK_USD` to `SONNET_*_COST_PER_MTOK_USD`. In `code/paths.py` change
   `TASK_ROOT` to `Path("tasks/t0014_v2_annotator_sonnet_rerun")`, rename outputs to
   `v2_sonnet_annotated.jsonl`, `v2_sonnet_annotator_costs.json`, `v2_sonnet_judge_sample.jsonl`,
   `v2_sonnet_judge_outcomes.jsonl`, `v2_sonnet_judge_costs.json`, `three_way_comparison.json`,
   `three_way_table.md`. Add a `V2_HAIKU_INPUT_PATH` pointing at
   `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
   for the comparator. Add a `DATASET_ASSET_DIR` of
   `assets/dataset/hierarchical-annotation-v2-sonnet`. Run
   `mypy -p tasks.t0014_v2_annotator_sonnet_rerun.code` and confirm zero errors. Satisfies REQ-1,
   REQ-2.

3. **Validation gate: 5-row sonnet dry-run.** Run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.v2_annotator --limit 5 --workers 1`
   wrapped in `run_with_logs.py`. The dry-run flag is implicit when `limit < 115`; after each row,
   observe envelope-reported `total_cost_usd` and `usage`. **Failure condition:** if any row reports
   cost ≥ $0.20, halt and inspect the prompt/response (the prompt may have regressed in length); do
   not proceed to Step 4 until per-call cost ≤ $0.15. **Baseline:** t0009's haiku per-call cost was
   ~$0.06 (averaged from `_outputs/v2_annotator_costs.json` = $7.42 / 115); sonnet at ~3.75× haiku
   list price implies ~$0.04-0.10 per call given identical prompts. **Inspection:** print and read
   the parsed `hierarchy` of all 5 dry-run rows; confirm each has a non-null `global`, ≥ 1 subtask
   with atomics, and a parallel `gold_actions`. If parse rate is < 5/5, halt and re-tune Step 2
   before the full run. Satisfies REQ-10.

4. **Run the full 115-row sonnet annotator.** Once Step 3 gate passes, run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.v2_annotator --workers 4` wrapped in
   `run_with_logs.py`. Append-mode JSONL writes per row, idempotent on resume. Expected output:
   `code/_outputs/v2_sonnet_annotated.jsonl` with 115 rows;
   `code/_outputs/v2_sonnet_annotator_costs.json` with `rows_with_complete_hierarchy >= 113`
   (allowing for up to 2 sonnet parse failures); `total_cost_usd <= $10`. Satisfies REQ-1, REQ-3,
   REQ-10.

5. **Recover the 23-row stratified sample.** Run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.select_judge_sample` wrapped in
   `run_with_logs.py`. Expected output: `code/_outputs/v2_sonnet_judge_sample.jsonl` with 23 rows.
   **Cross-check:** load both this file and t0009's `code/_outputs/v2_judge_sample.jsonl`; confirm
   both contain the same 23 `_pilot_row_index` values (the seed and per-benchmark targets are
   identical, so the only way they diverge is if a sonnet row dropped completeness). If divergence
   found, log it in the step_log; the model-only delta will then be computed on the 23 ∩ 23
   intersection rather than on disjoint sets. Satisfies REQ-4.

6. **Run the 23-row haiku judge on v2-sonnet hierarchies.** Run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.v2_judge --workers 4` wrapped in
   `run_with_logs.py`. Expected output: `code/_outputs/v2_sonnet_judge_outcomes.jsonl` with 23 rows;
   every row has `verdict in {acceptable, needs revision}` and a non-empty `justification`.
   `code/_outputs/v2_sonnet_judge_costs.json` `total_cost_usd <= $2.00`. Satisfies REQ-5, REQ-10.

7. **Build the dataset asset.** Run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.build_v2_asset` wrapped in
   `run_with_logs.py`. Inside the script, `dataset_id` is `"hierarchical-annotation-v2-sonnet"`,
   `version` is `"v2-sonnet"`, the canonical jsonl filename is
   `hierarchical_annotation_v2_sonnet.jsonl`, and the description.md prose is rewritten to flag this
   asset as the "model-controlled" companion to t0009's "schema-controlled" v2-haiku asset (with
   explicit cross-reference to t0009 in the Overview, Main Ideas, and Summary sections). Run
   `uv run python -m meta.asset_types.dataset.verificator.verify_dataset_asset tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet`
   wrapped in `run_with_logs.py`. Expected: 0 errors, ≤ 1 warning (DA-W007 author has no country,
   intentional). Satisfies REQ-9.

8. **Compute three-way deltas and emit charts.** Run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.compute_stats` wrapped in
   `run_with_logs.py`. The extended comparator loads three jsonls (v1, v2-haiku, v2-sonnet),
   computes per-benchmark and aggregate accept rates with Wilson 95% CIs (use
   `statsmodels.stats.proportion.proportion_confint(..., method='wilson')` or a hand-rolled Wilson
   formula — declare a single utility in `code/stats.py`), and emits
   `code/_outputs/three_way_comparison.json` with three top-level fields: `schema_only`,
   `model_only`, `headline`. Each field has per-benchmark and aggregate sub-objects with `delta`,
   `delta_ci_lower`, `delta_ci_upper`, sample sizes, and accept rates. Then run
   `uv run python -m tasks.t0014_v2_annotator_sonnet_rerun.code.make_charts` to emit
   `results/images/three_way_accept_rate.png` (grouped bar: v1-sonnet / v2-haiku / v2-sonnet ×
   benchmarks + aggregate) and `results/images/v2_sonnet_atomics_distribution.png` (boxplot per
   benchmark). Satisfies REQ-6, REQ-7, REQ-8.

## Remote Machines

None required. All work runs locally via the `claude` CLI (Anthropic API). No GPU, no remote
provisioning, no `setup-machines` step.

## Assets Needed

* **Input dataset (read-only)**: t0005's
  `assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl` — the canonical
  115-row source (annotator: sonnet, schema: flat, judge: haiku).
* **Reference dataset (read-only)**: t0009's
  `assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl` — the canonical
  115-row v2-haiku output (annotator: haiku, schema: tree, judge: haiku, 23-row judge sample). Used
  for the model-only delta and the headline cross-check.
* **Reference code (read-only)**: t0009's
  `code/{v2_annotator.py, v2_judge.py, select_judge_sample.py, build_v2_asset.py, compute_stats.py, make_charts.py, constants.py, paths.py}`.
  **Copied** into t0014's `code/` per the cross-task code reuse rule (no library import).
* **Anthropic API access** via the local `claude` CLI. No project-level keys or vast.ai provisioning
  needed.
* **Registered libraries**: none. The four registered libraries (`scope_aware_react_v1`,
  `scope_unaware_planandsolve_v1`, `matched_mismatch_v1`, `metric2_calibration_aggregator_v1`) are
  unrelated to annotation/judge work.

## Expected Assets

t0014 produces exactly **one** dataset asset, matching `task.json`
`expected_assets: {"dataset": 1}`:

* **Type**: `dataset`
* **Asset ID**: `hierarchical-annotation-v2-sonnet`
* **Location**:
  `tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet/`
* **Files**: `details.json`, `description.md`, `files/hierarchical_annotation_v2_sonnet.jsonl` (115
  rows, v2 tree schema, judge verdicts on the 23-row sample).
* **Categories**: `hierarchical-planning`, `benchmark-annotation`, `agent-evaluation`,
  `granularity-conditioning` (matches t0009's v2-haiku asset).
* **Description**: explicitly framed as the "model-controlled" companion to t0009's
  "schema-controlled" v2-haiku asset, intended for the three-way delta analysis. NOT a replacement
  for t0009's asset.

## Time Estimation

| Phase | Wall-clock |
| --- | --- |
| Research (already done — papers + code) | 0 min (complete) |
| Code copy + parameterise (Steps 1-2) | ~15 min |
| Sonnet dry-run gate (Step 3) | ~5 min |
| Sonnet annotator full run (Step 4) | ~30-45 min (115 rows × ~15s/row at workers=4) |
| Sample selection (Step 5) | < 1 min |
| Haiku judge run (Step 6) | ~5-10 min (23 rows × ~10s/row at workers=4) |
| Asset build + verify (Step 7) | ~5 min |
| Three-way comparator + charts (Step 8) | ~10 min |
| Reporting (orchestrator) | ~30 min |
| **Total active runtime** | **~1.5-2 hours** |

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Sonnet per-call cost is much higher than the haiku reference (~$0.20+ vs $0.06), busting the $10 cap mid-run | Medium | Blocks step 4 | Step 3 dry-run gate halts on first ≥ $0.20 row. Fallback: lower `workers` from 4 to 1 and re-evaluate; if still too expensive, escalate via `intervention/` and request budget increase before resuming. |
| Sonnet parse-failure rate drops `hierarchy_completeness` below 23-of-23 in the sampled buckets, so the seed-42 sample diverges from t0009's | Low | Weakens model-only delta cleanliness | Run any parse-failure row once with `--limit 1` to retry. If still failing, compute model-only delta on the intersection set and report sample size in the results table. |
| t0015 (proxy benchmark relabel) lands during execution and corrects benchmark assignments via the corrections overlay | Low | Per-benchmark numbers shift slightly | The aggregator-based comparator already applies corrections. Re-run Step 8 if t0015 merges before t0014; rerun is cheap (no API calls). |
| Anthropic API hiccup mid-run causes call-failures | Low | Partial annotated jsonl; user time | Annotator already idempotent: append-mode writes per row and `_load_existing_indices` on restart. Re-run command continues from last completed row. |
| Wilson CI on n=5-6 buckets is so wide that per-benchmark deltas are not statistically distinguishable | High | Reduces interpretability of per-benchmark conclusions | Report aggregate (n=23) deltas as the primary numbers; per-benchmark numbers are supplementary. State CI widths in results explicitly. |
| The schema-only delta uses populations of different sizes (12-row v1 sample vs 23-row v2-sonnet sample) | Medium | Schema-only delta is on disjoint samples, weakening interpretation | Compute schema-only delta on the v1-sample subset of v2-sonnet (filter to the 12 `_pilot_row_index` values that v1 judged); accept smaller n in exchange for matched sampling. |
| Sonnet's tree output formatting differs subtly from haiku (e.g., adds prose before/after JSON) | Medium | Parse failures | The copied parser already strips fences and walks brace depth; t0009 reported zero parse failures on haiku. If sonnet regresses, add a small post-processor that retries the parse after stripping leading/trailing prose. |

## Verification Criteria

* **REQ-1, REQ-2, REQ-3 (annotation)**: run
  `python -c "import json; rows=[json.loads(l) for l in open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_annotated.jsonl')]; assert len(rows)==115; assert len({r['_pilot_row_index'] for r in rows})==115; assert all(r['annotation_model']=='claude-sonnet-4-6' for r in rows); print('OK')"`.
  Expected output: `OK`. Confirms 115 rows, unique `_pilot_row_index`, sonnet model on every row.
* **REQ-4 (sample reproduction)**: run
  `python -c "import json; a={json.loads(l)['_pilot_row_index'] for l in open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_sample.jsonl')}; b={json.loads(l)['_pilot_row_index'] for l in open('tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_sample.jsonl')}; print(f'overlap={len(a & b)}/{len(a)} of {len(b)}')"`.
  Expected: `overlap=23/23 of 23` (or, in the divergence fallback case, the actual intersection
  size, logged in the step_log).
* **REQ-5 (judge)**: run
  `python -c "import json; rows=[json.loads(l) for l in open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_outcomes.jsonl')]; assert len(rows)==23; assert all(r['verdict'] in ('acceptable','needs revision') for r in rows); print('OK')"`.
* **REQ-6, REQ-7, REQ-8 (deltas)**: run
  `python -c "import json; d=json.load(open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/three_way_comparison.json')); assert all(k in d for k in ('schema_only','model_only','headline')); for k in ('schema_only','model_only','headline'): print(k, d[k]['aggregate']['delta'])"`.
  Expected: prints three numeric deltas; signs and magnitudes broadly match the hypotheses band
  (schema_only positive, model_only positive-or-near-zero, headline ≈ +50-65 pp).
* **REQ-9 (asset)**: run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0014_v2_annotator_sonnet_rerun -- python -m meta.asset_types.dataset.verificator.verify_dataset_asset tasks/t0014_v2_annotator_sonnet_rerun/assets/dataset/hierarchical-annotation-v2-sonnet`.
  Expected: `PASSED — 0 errors, 0 or 1 warning(s)`.
* **REQ-10 (budget)**: run
  `python -c "import json; a=json.load(open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_annotator_costs.json')); j=json.load(open('tasks/t0014_v2_annotator_sonnet_rerun/code/_outputs/v2_sonnet_judge_costs.json')); print(f'annotator={a[\"total_cost_usd\"]:.2f} judge={j[\"total_cost_usd\"]:.2f} total={a[\"total_cost_usd\"]+j[\"total_cost_usd\"]:.2f}'); assert a['total_cost_usd']+j['total_cost_usd']<10.0"`.
  Expected: combined cost < $10.
* **Code quality**: run
  `uv run ruff check tasks/t0014_v2_annotator_sonnet_rerun/ && uv run ruff format --check tasks/t0014_v2_annotator_sonnet_rerun/ && uv run mypy -p tasks.t0014_v2_annotator_sonnet_rerun.code`.
  Expected: all three commands exit 0.
* **Plan verificator**: run
  `uv run python -m arf.scripts.verificators.verify_plan t0014_v2_annotator_sonnet_rerun`. Expected:
  `PASSED — 0 errors, ≤ 2 warnings`.
* **Charts present and embedded**: run
  `ls tasks/t0014_v2_annotator_sonnet_rerun/results/images/three_way_accept_rate.png tasks/t0014_v2_annotator_sonnet_rerun/results/images/v2_sonnet_atomics_distribution.png`.
  Expected: both files exist (results writeup will embed them).
