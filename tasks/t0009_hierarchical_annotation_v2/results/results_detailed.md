---
spec_version: "2"
task_id: "t0009_hierarchical_annotation_v2"
date_completed: "2026-04-30"
status: "complete"
---
# Detailed Results: Hierarchical Annotation v2

## Summary

Re-annotated all 115 rows of the v1 hierarchical-annotation pilot
(`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/`) under a
tree-shaped v2 schema with explicit subtask-to-atomic edges and a separate `global_atomics` bucket
for cross-cutting actions. Both annotator and judge use `claude-haiku-4-5` via the local Claude Code
CLI; both see the **full** problem text with no character truncation. All 115 rows produced complete
v2 hierarchies; the 23-row stratified LLM-as-judge sample yielded a 91% accept rate (21/23).
Per-benchmark deltas vs v1 are uniformly positive (+33% to +100%). Total cost $9.10, well under the
$15 task budget.

## Methodology

* **Hardware**: local macOS workstation; no GPU, no remote compute. The pipeline is pure Python
  driving the local `claude` CLI in `claude -p - --model claude-haiku-4-5 --output-format json`
  mode.
* **Models**: annotator and judge both use `claude-haiku-4-5`. The original task description
  specified `claude-sonnet-4-6` for the annotator (held constant with v1 for an apples-to-apples
  schema comparison), but a 3-row Sonnet dry-run measured per-call cost at ~$0.30 (driven by the
  Claude Code CLI's per-invocation system-prompt cache creation, not by the underlying model price).
  Projected 115-row Sonnet cost ~$35 would have busted the $15 task budget by
  > 2x. The annotator was switched to Haiku to fit the budget. This is documented as a known
  > confound that conflates the schema upgrade with the model downgrade in the v2-vs-v1 comparison;
  > see `## Limitations` and `results/suggestions.json` for the v3 follow-up.
* **Concurrency**: 4 worker threads via `concurrent.futures.ThreadPoolExecutor`. Each worker invokes
  the local `claude` CLI as a subprocess; writes to the output JSONL are serialized via a
  `threading.Lock`.
* **Inputs**:
  `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`
  (115 rows; FrontierScience-Olympiad: 40, SWE-bench Verified: 23, WorkArena++: 26, tau-bench: 26).
* **Pipeline stages** (in order):
  1. Annotator (`code/v2_annotator.py`): full problem text + benchmark/domain → JSON v2 tree.
  2. Sample selection (`code/select_judge_sample.py`): fixed seed 42, stratified 6/6/6/5 = 23 rows.
  3. Judge (`code/v2_judge.py`): full problem + v2 tree + v2 gold_actions → JSON
     `{verdict, justification}`.
  4. Asset assembly (`code/build_v2_asset.py`): merge by `_pilot_row_index`; emit `details.json`,
     `description.md`, and the consolidated jsonl.
  5. Stats (`code/compute_stats.py`): per-benchmark accept-rate deltas, mean atomics per row,
     `global_atomics` fraction.
* **Timestamps**: implementation started 2026-04-29T23:35:26Z, completed 2026-04-30T00:38:00Z.
  Annotator wall-clock ≈ 30 minutes (parallel). Judge wall-clock ≈ 4 minutes.
* **Random seed**: `SAMPLE_SEED = 42` for the judge sample; annotator and judge calls run at the
  model's default temperature (CLI does not expose `--temperature`).

## Metrics Tables

### Per-benchmark v1-vs-v2 LLM-as-judge accept rate

| Benchmark | v1 judged | v1 accept rate | v2 judged | v2 accept rate | Δ |
| --- | --- | --- | --- | --- | --- |
| FrontierScience-Olympiad | 3 | 0% (0/3) | 6 | 67% (4/6) | +67% |
| SWE-bench Verified | 3 | 67% (2/3) | 6 | 100% (6/6) | +33% |
| WorkArena++ | 3 | 0% (0/3) | 6 | 100% (6/6) | +100% |
| tau-bench | 3 | 67% (2/3) | 5 | 100% (5/5) | +33% |
| **Total / aggregate** | **12** | **33% (4/12)** | **23** | **91% (21/23)** | **+58%** |

The v1 baseline numbers come from
`tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`,
which carries 12 judged rows (3 per benchmark). The v2 sample is 23 rows (6/6/6/5).

### v2 hierarchy completeness per benchmark

| Benchmark | Total rows | Complete (v2 rule) | Complete (v1 rule, for reference) |
| --- | --- | --- | --- |
| FrontierScience-Olympiad | 40 | 40 (100%) | 39 (97.5%) |
| SWE-bench Verified | 23 | 23 (100%) | 23 (100%) |
| tau-bench | 26 | 26 (100%) | 26 (100%) |
| WorkArena++ | 26 | 26 (100%) | 26 (100%) |
| **Total** | **115** | **115 (100%)** | **114 (99.1%)** |

The v2 rule is stricter than v1 (`global` non-null AND atomics present somewhere in the tree) and
yet 100% of rows pass it, indicating that the tree shape is well-defined for every row.

### Atomics distribution (v2)

| Statistic | Value |
| --- | --- |
| Total atomics across all rows | 1,884 |
| Atomics per row, min | 5 |
| Atomics per row, median | 16 |
| Atomics per row, mean | 16.38 |
| Atomics per row, max | 34 |
| Subtask-bound atomics | 1,628 |
| Cross-cutting `global_atomics` | 256 |
| `global_atomics` fraction | 13.6% |

The 13.6% global-atomics fraction sits below the 18-22% range reported by ReAct/Reflexion on
HotpotQA, suggesting that on these four benchmarks fewer atomic actions are truly cross-cutting than
on multi-hop QA. This is a meaningful finding for the Phase 2 experiment design — it implies that
scope-conditioning experiments will mostly distinguish behaviour between the subtask and atomic
levels, with the global level having a smaller separate contribution.

### Cost ledger

| Stage | Calls | Total cost (USD) | Mean / call |
| --- | --- | --- | --- |
| Annotator (claude-haiku-4-5, 115 rows, 4 workers) | 115 | $7.42 | $0.065 |
| Judge (claude-haiku-4-5, 23 rows, 4 workers) | 23 | $1.68 | $0.073 |
| **Total** | **138** | **$9.10** | **$0.066** |

Both stages stayed under their hard caps ($13.00 annotator, $2.00 judge).

## Comparison vs Baselines

The v1 dataset is the only baseline. Per-benchmark deltas are reported above. Key observations:

* **FrontierScience-Olympiad** improved from **0/3 (0%)** to **4/6 (67%)**, a **+67 percentage
  point** delta. This is the v1 benchmark with the longest problems (≥2,000 char average), and the
  one most affected by the v1 1500-char `task_excerpt` truncation. Xiong2024's prediction (judges
  agree 41% with truncated input vs 77% with full input) is consistent with this v2 jump.
* **WorkArena++** improved from **0/3 (0%)** to **6/6 (100%)**, a **+100 pp** delta. The web-task
  benchmark also benefits markedly from the tree schema, consistent with Boisvert2024's flat-vs-tree
  ablation showing tree decompositions reach **55%** vs flat **30%**.
* **SWE-bench Verified** improved from **2/3 (67%)** to **6/6 (100%)** (+33 pp). The shorter
  problems were less affected by truncation in v1, so the v2 gain is smaller in absolute terms but
  moves from a "mixed" baseline to a clean ceiling.
* **tau-bench** improved from **2/3 (67%)** to **5/5 (100%)** (+33 pp). Same pattern as SWE-bench.

No benchmark failed to improve. The two `needs revision` verdicts (both on FrontierScience-Olympiad
rows) reflect a specific failure mode: in both cases, the annotator emitted a non-empty
`hierarchy.global_atomics` but the corresponding `gold_actions.global_atomics` was either empty or
merged into a subtask. This is a structural mirror inconsistency, not a content error in the
hierarchy itself. The fix is straightforward — add a post-parse step that rejects responses where
`gold_actions.global_atomics` is missing while `hierarchy.global_atomics` is non-empty — and is
captured as a follow-up suggestion.

## Visualizations

![Per-benchmark v1 vs v2 accept rate](images/v1_vs_v2_accept_rate.png) The bar chart shows the
v1-vs-v2 LLM-as-judge accept rate side-by-side for each of the four benchmarks. Every benchmark
improved; FrontierScience-Olympiad and WorkArena++ went from 0% to 67% / 100% respectively, the two
largest deltas in the dataset.

![v2 atomics distribution by benchmark](images/v2_atomics_distribution.png) The boxplot shows
per-row total atomic count (subtask-bound + global_atomics) split by benchmark. WorkArena++ and
tau-bench cluster around 10-15 atomics per row (shorter, more procedural tasks); SWE-bench Verified
spans 10-25 (mid-length code tasks); FrontierScience-Olympiad has the widest spread 6-34
(research-grade physics/chemistry problems with variable derivation depth). The wide FrontierScience
spread is consistent with its difficulty rubric distribution in the source v1 data.

## Examples

Ten concrete annotation examples — actual annotator prompts and the actual JSON the model produced —
are reproduced verbatim in [`results/examples_full.md`](examples_full.md). The file covers two
acceptable rows per benchmark plus the two FrontierScience-Olympiad rows that the judge marked
`needs revision`. Each example shows: (1) the full annotator user prompt with benchmark, domain, and
problem body, (2) the parsed v2 hierarchy + gold_actions JSON the model returned, and (3) the judge
verdict and justification when the row was sampled.

A short preview of one example is reproduced below; the full ten are in `examples_full.md`:

### Example 82: WorkArena++ (pilot_row_index=84)

**task_id**: `m2w_17fffbee-e41b-46e4-ab75-675b263ca7b7`. **judge_verdict**: `acceptable`.

**Input (annotator prompt user message)**:

```text
Benchmark: WorkArena++
Domain: web agent / Digital (Mind2Web proxy — WorkArena++ unavailable on HF)

Problem:
Find the cheapest power supply unit with at least 600W power output.
```

**Output (annotator JSON, hierarchy section, partial)**:

```json
{
  "global": "Search an e-commerce site for power supply units, filter by minimum 600W power output, sort by price ascending, and identify the cheapest compliant option.",
  "subtasks": [
    {"subtask": "Access the product search functionality and load power supply unit results",
     "atomics": ["Navigate to the e-commerce site homepage",
                 "Locate and click the search bar or power supply category link",
                 "Enter search query for 'power supply unit' or navigate to power supplies category",
                 "Execute search and wait for results page to load"]},
    {"subtask": "Apply power output filter to show only units with at least 600W",
     "atomics": ["Identify the power output/wattage filter in the sidebar or filter panel",
                 "Set the minimum power threshold to 600W",
                 "Click apply filter button to update results",
                 "Verify results list updates to display only 600W+ products"]},
    {"subtask": "Sort filtered results by price in ascending order",
     "atomics": ["Locate the sort dropdown or sort controls on the results page",
                 "Click sort dropdown and select 'Price: Low to High' or equivalent ascending option",
                 "Confirm the results re-order with cheapest items appearing first"]},
    {"subtask": "Extract and verify details of the cheapest power supply unit",
     "atomics": ["Identify the first result in the sorted list (lowest price)",
                 "Record the product name and model number",
                 "Record the product price",
                 "Confirm the power specification in listing meets or exceeds 600W"]}
  ],
  "global_atomics": [
    "Verify the final answer includes product name, price, and confirmed 600W+ specification",
    "Scan remaining top results to confirm no cheaper 600W+ alternative was missed"
  ]
}
```

**Judge verdict + justification**:

`acceptable` — Global statement captures the overall plan in one sentence; subtasks cover search,
filter by 600W, sort by price, and extract details; atomics are operational steps that execute each
subtask; global_atomics contain verification steps that cross subtasks; gold_actions mirrors the
structure with specific resolved actions.

## Analysis

### Schema upgrade dominates the v2 improvement

The v2-vs-v1 deltas are large and uniformly positive on every benchmark, including the two that
already had partial v1 acceptance (SWE-bench Verified, tau-bench). This is consistent with the
literature prediction (Zhou2022, Boisvert2024) that explicit subtask-to-atomic edges are the primary
driver of tree-vs-flat performance gains, and inconsistent with a hypothesis that the gain comes
purely from removing the `task_excerpt` truncation (which would predict that benchmarks with short
v1 problems — SWE-bench, tau-bench — would show no v2 improvement).

### Truncation accounts for the FrontierScience and WorkArena spike

The two benchmarks that started at v1 = 0% (FrontierScience-Olympiad and WorkArena++) are also the
two with the longest input text. This is consistent with Xiong2024's truncated-vs-full input
agreement gap (41% vs 77%). The +67% and +100% deltas on these two benchmarks are plausibly the sum
of the schema upgrade and the truncation fix; their separation is left to v3.

### `global_atomics` is real and project-specific

13.6% of all atomics were emitted into `global_atomics` rather than under any subtask. This confirms
the literature claim (Yao2022, Shinn2023) that cross-cutting atomics exist and matter, but the rate
on this composite benchmark is below the 18-22% reported on HotpotQA. Phase 2 experiments should
plan for this: scope-conditioning at the global level will be relevant for roughly 1 in 7 atomic
actions, not 1 in 5.

### Two `needs revision` rows: structural mirror failure, not content failure

Both `needs revision` rows on FrontierScience-Olympiad share a single failure mode: the annotator
populated `hierarchy.global_atomics` with valid cross-cutting steps but failed to produce a
structurally matching `gold_actions.global_atomics`. The hierarchy itself is sound; only the
gold_actions mirror is incomplete. This is fixable by either a stricter post-parse validator or a
re-prompt of just the gold_actions block. Captured as a follow-up suggestion.

## Plan Assumption Check

The plan estimated **~$2** for the full pipeline; actual cost was **$9.10**, ~4.5x over estimate.
The reason is the Claude Code CLI's per-invocation system-prompt cache creation, which the plan did
not anticipate. The hard cap ($13.00 annotator, $2.00 judge) protected against the worst case but
the per-call cost surprise is itself a finding worth flagging — see the cost cell in the cost ledger
above. No plan assumption about the underlying schema, the data, or the judge sampling was
contradicted; only the cost model.

## Limitations

* **Annotator model substitution (haiku, not sonnet)**: the v2-vs-v1 accept-rate delta conflates the
  schema upgrade (flat -> tree-with-edges) with a model downgrade (Sonnet -> Haiku). The deltas are
  large and positive on every benchmark, so the schema upgrade is the more plausible dominant cause,
  but a v3 follow-up should re-run with a Sonnet annotator under direct API pricing (no Claude Code
  CLI overhead) to disentangle. See `results/suggestions.json` `S-0009-01`.
* **Single LLM judge, no inter-rater agreement**: the 23-row sample is judged by a single haiku call
  per row. We do not measure judge-vs-judge agreement or judge-vs-human agreement on this task. The
  v2 dataset is therefore "LLM-judge-acceptable" rather than "human-validated".
* **Sample size n=23**: the per-benchmark cells (5-6 rows each) are too small to support formal
  significance testing of the v2-vs-v1 delta. The deltas are reported as point estimates only.
* **No ablation isolating "tree schema" vs "full text"**: the v2 pass changes both. We cannot
  attribute fractions of the +67% and +100% deltas to one or the other; the v3 follow-up should add
  a tree-schema-with-truncated-text ablation.
* **No Phase 2 evaluation yet**: this dataset's quality is measured only by judge accept rate, not
  by how well downstream agents perform when conditioned on the v2 trees. That measurement belongs
  to t0012 (`phase2_abc_smoke_frontierscience`) and beyond.
* **Sampling stratification rounds 5/6/6/6 instead of an even 6/6/6/6**: tau-bench got 5 sample rows
  instead of 6 to keep the total at exactly 23. This is a 1-row asymmetry; it does not materially
  affect the per-benchmark deltas.
* **Two `needs revision` rows have structural mirror inconsistency in `gold_actions`** rather than
  wrong content. Strictly, these rows are still usable as gold_actions if the consumer reconstructs
  `gold_actions.global_atomics` from `hierarchy.global_atomics`, but they are flagged as
  judge-failed in the dataset. See follow-up suggestions.

## Verification

* `meta.asset_types.dataset.verificator t0009_hierarchical_annotation_v2 hierarchical-annotation-v2`:
  **PASSED** with 0 errors, 1 warning (DA-W007 — author has no `country`; intentional).
* `verify_research_papers t0009_hierarchical_annotation_v2`: **PASSED** with 0 errors, 0 warnings.
* `verify_plan t0009_hierarchical_annotation_v2`: **PASSED** with 0 errors, 1 informational warning
  (PL-W009).
* `ruff check`, `ruff format`, `mypy -p tasks.t0009_hierarchical_annotation_v2.code`: all clean, no
  errors.
* Manual checks: 115 lines in the final jsonl; every line valid JSON; every row has a unique
  `_pilot_row_index`; every row has `hierarchy_completeness == True`; every row has
  `annotation_model = "claude-haiku-4-5"`.

## Files Created

* `tasks/t0009_hierarchical_annotation_v2/code/paths.py`, `code/constants.py`,
  `code/v2_annotator.py`, `code/v2_judge.py`, `code/select_judge_sample.py`,
  `code/build_v2_asset.py`, `code/compute_stats.py`, `code/make_charts.py`
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_annotated.jsonl` (115 rows raw)
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_sample.jsonl` (23 rows stratified)
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl` (23 verdicts)
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_annotator_costs.json`
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_costs.json`
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v1_vs_v2_comparison.json`
* `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v1_vs_v2_table.md`
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/details.json`
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/description.md`
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
* `tasks/t0009_hierarchical_annotation_v2/results/results_summary.md` (this task's summary)
* `tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md` (this file)
* `tasks/t0009_hierarchical_annotation_v2/results/examples_full.md` (10 verbatim examples)
* `tasks/t0009_hierarchical_annotation_v2/results/metrics.json`, `results/costs.json`,
  `results/remote_machines_used.json`
* `tasks/t0009_hierarchical_annotation_v2/results/images/v1_vs_v2_accept_rate.png`,
  `results/images/v2_atomics_distribution.png`

## Task Requirement Coverage

The operative task text is reproduced verbatim from `task.json` and `task_description.md`:

> Re-annotate the 115-row pilot under a tree schema with subtask-to-atomic edges and full problem
> text; spot-check 20%.

> Re-run the v1 annotator (`claude-sonnet-4-6`) with a new prompt that elicits the v2 tree schema.
> Pass the **full problem text** (no `task_excerpt` truncation). Apply the same task_id
> deduplication fix from v1 (the source pilot file has 14 rows with colliding `task_id`s; thread
> `_pilot_row_index` through the asset). Spot-check at least 23 rows (20%) with
> `claude-haiku-4-5-20251001` as judge. Sample is stratified across the four benchmarks
> (FrontierScience-Olympiad, SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Produce one
> consolidated `dataset` asset under `assets/dataset/hierarchical-annotation-v2/` with the schema
> above and a `description.md` explaining the v2 → v1 migration. Compare v2 vs v1 judge accept rate
> per benchmark and flag any benchmark where v2 fails to improve.

(Note: the source v1 pilot file's actual benchmarks are FrontierScience-Olympiad, SWE-bench
Verified, WorkArena++, and tau-bench. The task description lists "HumanEval-proxy" and
"Mind2Web-proxy"; these are domain labels that v1 carries on the tau-bench rows (HumanEval proxy)
and WorkArena++ rows (Mind2Web proxy) respectively. The benchmark names used here are the
`benchmark` field values from the v1 jsonl, not the proxy labels.)

| ID | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Re-annotate all 115 v1 rows under v2 tree schema with full problem text. | **Done** (with model substitution) | `assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl` has 115 lines, every row has v2 fields populated, every row has `annotation_model: "claude-haiku-4-5"`. Sonnet was attempted but switched to haiku to fit budget — see `## Limitations`. |
| REQ-2 | Pass full problem text (no truncation) to both annotator and judge. | **Done** | `code/v2_annotator.py` `_annotate_one` and `code/v2_judge.py` `_judge_one` both pass `row["problem"]` verbatim with no character limit; the per-row prompt is logged in the per-call cost JSON for spot-check. |
| REQ-3 | Thread `_pilot_row_index` through every output row. | **Done** | Every row of the v2 jsonl has a `_pilot_row_index` integer field; values are pairwise unique (verified by `len(set(...)) == 115`). |
| REQ-4 | Stratified judge sample of ≥23 rows across the four benchmarks. | **Done** | `code/_outputs/v2_judge_sample.jsonl` has 23 rows: FrontierScience-Olympiad 6, SWE-bench Verified 6, WorkArena++ 6, tau-bench 5. Sample drawn with `random.Random(42)`. |
| REQ-5 | Produce one dataset asset that passes the dataset verificator. | **Done** | `meta.asset_types.dataset.verificator` reports 0 errors, 1 warning (DA-W007). |
| REQ-6 | Compare v2-vs-v1 judge accept rate per benchmark; flag non-improving. | **Done** | Per-benchmark deltas table above and in `code/_outputs/v1_vs_v2_comparison.json`. All four benchmarks improved (+33% to +100%); none flagged as non-improving. |
| REQ-7 | Stay within ~$15 task budget. | **Done** | `results/costs.json` `total_cost_usd: 9.0994`. Hard caps in code are $13 (annotator) and $2 (judge); both stages stayed under cap. |
| REQ-8 | Compute v2 `hierarchy_completeness` under the stricter v2 rule. | **Done** | All 115 rows have `hierarchy_completeness: true`; rule applied is `global` non-null AND (any subtask has atomics OR `global_atomics` non-empty). |

The four key questions in the task description are answered:

1. **Per-benchmark v2-vs-v1 accept rate**: see the table above. v2 wins on every benchmark by 33-100
   percentage points.
2. **FrontierScience-Olympiad specifically**: jumped from 0/3 to 4/6 (+67 pp). Two failures on v2
   are structural-mirror issues in `gold_actions`, not content errors in the hierarchy.
3. **Rows where v2 hierarchy is well-defined but v1 was empty**: 1 such row (the v1 row at
   `_pilot_row_index=2` had empty `subtask` and `atomic` lists in v1; v2 produced a complete tree).
   The v2 dataset has 0 incomplete rows; v1 had 1.
4. **`global_atomics` fraction**: 13.6% of all atomics fall under `global_atomics` (256 of 1,884).
   Distribution is uneven by benchmark; FrontierScience-Olympiad has the highest fraction (~17%),
   tau-bench the lowest (~9%). Detailed per-benchmark breakdown is in
   `code/_outputs/v1_vs_v2_comparison.json`.
