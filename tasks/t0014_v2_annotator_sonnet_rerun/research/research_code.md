---
spec_version: "1"
task_id: "t0014_v2_annotator_sonnet_rerun"
research_stage: "code"
tasks_reviewed: 9
tasks_cited: 8
libraries_found: 4
libraries_relevant: 0
date_completed: "2026-04-30"
status: "complete"
---
# Research Code: t0014 v2 Annotator Sonnet Rerun

## Task Objective

Re-annotate the same 115 v1 pilot rows under the v2 tree schema using `claude-sonnet-4-6` instead of
the `claude-haiku-4-5` model used in [t0009], then run the same haiku judge on the new hierarchies
and recover three accept-rate deltas — schema-only (v2-sonnet vs v1-sonnet), model-only (v2-sonnet
vs v2-haiku), and the original headline (v2-haiku vs v1-sonnet) — to disentangle the schema upgrade
from the model substitution that was a known confound in [t0009].

## Library Landscape

The `aggregate_libraries` aggregator returns four registered libraries in the project:
`scope_aware_react_v1` (created by `[t0006]`), `scope_unaware_planandsolve_v1` (`[t0007]`),
`matched_mismatch_v1` (`[t0010]`), and `metric2_calibration_aggregator_v1` (`[t0011]`). All four are
agent-loop or metric-aggregation libraries oriented toward Phase 2 scope-conditioning experiments;
none of them touch annotation, prompt construction, judge runners, or accept-rate analysis. This
task therefore consumes exactly **zero** registered libraries — every reusable component is
non-library code that must be **copied** from `[t0009]` into
`tasks/t0014_v2_annotator_sonnet_rerun/code/` per the cross-task code reuse rule.

The aggregator also confirms that no v1-vs-v2 comparator or LLM-as-judge wrapper has been promoted
into a library yet. Promoting one is therefore an open suggestion (see Recommendations below) but
out of scope for t0014, which must stay narrow to keep the budget defensible.

## Key Findings

### v2 annotator architecture is fully reusable for sonnet swap

`[t0009]` `code/v2_annotator.py` (615 lines) is the load-bearing module. It loads the 115-row v1
JSONL, calls the local `claude` CLI (`claude -p - --model <model> --output-format json`) per row
with `ANNOTATOR_SYSTEM_PROMPT` and `ANNOTATOR_USER_TEMPLATE` from `code/constants.py`, parses the
returned JSON envelope (`is_error`, `result`, `usage{input_tokens,output_tokens}`,
`total_cost_usd`), validates the tree schema (`global` string, `subtasks` list of
`{subtask, atomics}` objects, `global_atomics` list, parallel `gold_actions` mirror), and writes one
row per input to `code/_outputs/v2_annotated.jsonl`. The module is fully idempotent — re-runs load
`_load_existing_indices` from the output file and only re-attempt the missing `_pilot_row_index`
rows. Concurrency uses `ThreadPoolExecutor` with `workers=4` and a budget cap that signals a
`threading.Event` to halt new submissions when running cost crosses `ANNOTATOR_BUDGET_CAP_USD`. The
`_annotate_one(*, pilot_row_index, row, model)` signature already takes `model` as a parameter, but
the module currently hard-codes `ANNOTATOR_MODEL_ID = "claude-haiku-4-5"` and consumes the haiku
price constants when computing fallback cost estimates. For t0014 we change `ANNOTATOR_MODEL_ID` to
`"claude-sonnet-4-6"`, switch the cost-estimate constants from `HAIKU_*_COST_PER_MTOK_USD` to
`SONNET_*_COST_PER_MTOK_USD`, and raise the budget cap from $13 to $10 (the t0014 task description's
hard cap) — the rest of the module is unchanged.

### Judge runner is reused unchanged

`[t0009]` `code/v2_judge.py` (459 lines) drives the LLM-as-judge stage. It already uses
`JUDGE_MODEL_ID = "claude-haiku-4-5"`, the same haiku build that judged v2-haiku and the same family
that judged v1 (`claude-haiku-4-5-20251001` in `[t0005]`). To make the t0014 model-only delta clean
we hold `JUDGE_MODEL_ID` constant — the t0014 hypothesis is that swapping the **annotator** to
sonnet will move the accept rate, **with the judge held identical**. The judge runner is otherwise
idempotent (`_load_existing_indices(path=V2_JUDGE_OUTCOMES_PATH)`), uses the same JSON-envelope
parser, and writes outcomes as
`{pilot_row_index, task_id, benchmark, verdict, justification, notes, cost_usd}`. We copy this file
verbatim into t0014.

### Sample selector reproduces t0009's 23-row stratified sample at seed=42

`[t0009]` `code/select_judge_sample.py` (86 lines) reads `V2_RAW_OUTPUT`, filters to rows with
`hierarchy_completeness == True`, partitions by `benchmark`, and uses
`random.Random(SAMPLE_SEED=42)` to draw `JUDGE_SAMPLE_PER_BENCHMARK` rows per bucket
(`FrontierScience-Olympiad: 6, SWE-bench Verified: 6, WorkArena++: 6, tau-bench: 5` = 23 total, 20%
of 115). Because the seed and per-benchmark targets are identical between t0009 and t0014, and
because the v1 input set is fixed, the same 23 `_pilot_row_index` values will be sampled in t0014
**iff** all 23 source rows pass `hierarchy_completeness` again under sonnet (`[t0009]` reported
115/115 completeness on haiku, so the 23-row sample is the same population unless sonnet's parse
rate drops). To guarantee identical sample composition for the model-only delta, t0014's
implementation step will assert that the 23 selected `_pilot_row_index` values are exactly the same
set as t0009's 23, and if they differ we widen the model-only comparison to the intersection.

### Asset assembly: details.json + description.md + jsonl is the canonical layout

`[t0009]` `code/build_v2_asset.py` (358 lines) assembles
`assets/dataset/hierarchical-annotation-v2/` with three pieces:
`files/hierarchical_annotation_v2.jsonl` (115 rows, sample joined with verdicts), `details.json`
(spec_version "2", `dataset_id: hierarchical-annotation-v2`, categories, size description),
`description.md` (seven mandatory sections: Metadata, Overview, Content & Annotation, Statistics,
Usage Notes, Main Ideas, Summary). t0014's analogue must rename `dataset_id` to
`hierarchical-annotation-v2-sonnet`, change the canonical jsonl filename to
`hierarchical_annotation_v2_sonnet.jsonl`, set `version: "v2-sonnet"`, and rewrite the prose to
reference sonnet (not haiku) and to flag this asset as the **second** v2 annotation produced under
the same schema, **for delta analysis**, not as a replacement for `[t0009]`'s asset. The verificator
is `meta.asset_types.dataset.verificator.verify_dataset_asset`; `[t0009]` passed with 0 errors and 1
warning (DA-W007 — author has no `country`, intentional for project-internal authorship).

### v1 vs v2 comparator is the template for the three-way analysis

`[t0009]` `code/compute_stats.py` (196 lines) reads both v2 and v1 jsonl, computes
`_benchmark_judge_summary()` per file (counting `acceptable` vs `needs revision` per benchmark and
deriving `accept_rate`), and emits `_outputs/v1_vs_v2_comparison.json` and
`_outputs/v1_vs_v2_table.md`. For t0014 we extend this to a three-way comparator that loads:

1. `[t0005]` v1 jsonl (annotator sonnet, judge haiku, **flat schema**, 12-row judge sample),
2. `[t0009]` v2-haiku jsonl (annotator haiku, judge haiku, **tree schema**, 23-row judge sample),
3. t0014 v2-sonnet jsonl (annotator sonnet, judge haiku, **tree schema**, 23-row judge sample).

The three deltas of interest are:

* `schema_only` = `v2_sonnet_accept - v1_sonnet_accept` (annotator and judge constant; only schema
  + full-text fix differs). Hypothesised positive at +15 to +35 pp aggregate (matches Zhou2022 +16
    pp tree-vs-flat band, Boisvert2024 +25 pp tree-vs-flat band per `research_papers.md`).
* `model_only` = `v2_sonnet_accept - v2_haiku_accept` (schema and judge constant; only annotator
  model differs). Hypothesised in the +0 to +9 pp band (Xiong2024 +9 pp judge-bias floor).
* `headline` = `v2_haiku_accept - v1_sonnet_accept` (already reported by `[t0009]`: aggregate +59
  pp, ranging from +33 pp on tau-bench to +100 pp on WorkArena++). t0014 simply re-derives this from
  the same files for cross-check.

Per-benchmark intersections must use the **23-row** sample for v2-sonnet vs v2-haiku (same
`_pilot_row_index` set, same judge model, only annotator differs) and the **12-row** v1 sample for
v2-sonnet vs v1-sonnet (the populations differ: v1's 12 rows are 3-per-benchmark, v2's 23 are
6/6/6/5; the schema-only delta is therefore reported on **the v1-sample subset of v2-sonnet**, not
on disjoint samples).

### Charts: copy and adapt for the three-way comparison

`[t0009]` `code/make_charts.py` (105 lines) produces two PNGs: `v1_vs_v2_accept_rate.png` (grouped
bar chart) and `v2_atomics_distribution.png` (boxplot of total atomics per row by benchmark). t0014
replicates the boxplot for v2-sonnet (atomics distribution sanity-check) and extends the bar chart
to a three-way grouped bar (v1-sonnet, v2-haiku, v2-sonnet, side by side per benchmark + aggregate).
Existing matplotlib idioms (`Agg` backend, `figsize=(9, 5)`, `dpi=120`, `tick_labels` for 3.9+
matplotlib boxplot) carry over unchanged.

## Reusable Code and Assets

All items below are non-library and must be **copied into the task** per the cross-task rule. None
require library import.

| Source | What it does | Reuse method | Adaptation | Lines |
| --- | --- | --- | --- | --- |
| `tasks/t0009_hierarchical_annotation_v2/code/v2_annotator.py` | v1-row -> v2-tree annotator with idempotent re-runs and budget cap | copy into task | Switch `ANNOTATOR_MODEL_ID` constant to `"claude-sonnet-4-6"`; cost helper now uses sonnet prices; lower budget cap to $10 | ~615 |
| `tasks/t0009_hierarchical_annotation_v2/code/v2_judge.py` | LLM-as-judge runner using haiku, parses verdict + justification | copy into task | None (judge stays haiku) | ~459 |
| `tasks/t0009_hierarchical_annotation_v2/code/select_judge_sample.py` | Stratified 23-row sample at seed=42 | copy into task | None (seed and per-benchmark targets unchanged) | ~86 |
| `tasks/t0009_hierarchical_annotation_v2/code/build_v2_asset.py` | Assembles dataset asset (details.json + description.md + jsonl) | copy into task | Rename `dataset_id` to `hierarchical-annotation-v2-sonnet`; filename to `hierarchical_annotation_v2_sonnet.jsonl`; rewrite description.md prose | ~358 |
| `tasks/t0009_hierarchical_annotation_v2/code/compute_stats.py` | Per-benchmark accept-rate comparator (v1 vs v2) | copy into task and extend | Extend to three-way: load v1, v2-haiku, v2-sonnet; compute schema_only, model_only, headline deltas with Wilson 95% CIs; emit per-benchmark + aggregate | ~196 -> ~280 |
| `tasks/t0009_hierarchical_annotation_v2/code/make_charts.py` | Per-benchmark bar + atomics boxplot | copy into task and extend | Three-way grouped bar; replicate boxplot on v2-sonnet | ~105 -> ~140 |
| `tasks/t0009_hierarchical_annotation_v2/code/constants.py` | Shared prompts, prices, sample sizes | copy into task | Annotator model -> sonnet; budget cap -> $10; everything else unchanged | ~128 |
| `tasks/t0009_hierarchical_annotation_v2/code/paths.py` | Centralised pathlib constants | copy into task | Repoint `TASK_ROOT` to t0014; rename outputs (`v2_sonnet_*`); add v2-haiku and v1 input paths for the three-way comparator | ~31 |

Public-API signatures we depend on:

* `_annotate_one(*, pilot_row_index: int, row: dict[str, Any], model: str) -> AnnotationOutcome`
* `_judge_one(*, row: dict[str, Any], model: str) -> JudgeOutcome`
* `select_sample() -> list[dict[str, Any]]`
* `merge_and_write_jsonl() -> dict[str, Any]`
* `compute() -> dict[str, Any]`

Source datasets needed (read-only, **never modify**):

* `tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`
  (115 rows, fields:
  `task_id, benchmark, domain, problem, hierarchy{global, subtask:list[str], atomic:list[str]}, gold_actions{...}, judge_verdict, judge_notes`).
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
  (115 rows, v2 tree schema with judge verdicts on 23 rows).

## Lessons Learned

* **CLI overhead dominates per-call cost on Sonnet.** `[t0009]`'s constants comment
  ("`Sonnet ~$0.30 / call, which would bust the $15 task-description budget at 115 rows`")
  explicitly diagnosed why t0009 dropped sonnet for haiku. At 115 rows × $0.30 ≈ $34.5, t0014's $10
  cap is tight. The task description targets ~$5; we will (a) verify the per-call cost on the first
  5 sonnet rows in dry-run before launching the full run, (b) use the envelope's `total_cost_usd`
  field which Sonnet via the CLI does report (so we are not relying on the 4-chars-per-token
  estimate), and (c) keep the same `ThreadPoolExecutor(workers=4)` to amortise the CLI startup cost.
* **Idempotent JSONL append is the right pattern.** `[t0009]` writes one row at a time with a
  `flush()` and re-loads the indices on restart, so an interrupted run is safe to resume. Copy this
  verbatim — it saved $1+ in `[t0009]` after a transient claude CLI hiccup at row 71.
* **Always pass full `problem` text to both annotator and judge.** This is the single most impactful
  fix from `[t0005]` -> `[t0009]`: v1 truncated to 1500 chars and the judge could not see the actual
  question. Inheriting `[t0009]`'s prompt template guarantees we keep this fix.
* **JSON envelope parsing must defend against `is_error: true` and against unfenced output.**
  `[t0009]`'s `_extract_first_json_object` walks brace depth with string-mode awareness. Sonnet is
  MORE compliant than haiku at "output ONLY the JSON object", but we still keep the fence-stripping
  path because regression on prompt-following is a real risk.
* **`hierarchy_completeness` is the gate for sample selection.** `[t0009]` reported 115/115
  completeness on haiku. If sonnet reports anything less (e.g., 113/115 due to a parse failure on
  two FrontierScience problems), the 23-row stratified sample at seed=42 may pull a different
  `_pilot_row_index` set than t0009. The plan mitigates this by (a) re-running any parse-failure
  rows once with `--limit 1`, and (b) reporting the schema-vs-model delta on the intersection if the
  23-row sets differ.
* **Verificator runs after every step, not just at the end.** `[t0009]`'s logs show
  `verify_dataset_asset` ran during the implementation step, not post-facto, which caught a
  malformed `details.json` field (`spec_version: 2` instead of `"2"`). Mirror this — run the
  verificator inside the implementation step before committing the asset.

## Recommendations for This Task

In priority order:

1. **Copy** all eight `[t0009]` code modules listed in Reusable Code into
   `tasks/t0014_v2_annotator_sonnet_rerun/code/`. Do not import from `[t0009]` — the cross-task rule
   forbids it and t0009 is `completed` (immutable), so any later edit there would break t0014's
   reproducibility.
2. **Change exactly two constants** in the copied `constants.py`:
   `ANNOTATOR_MODEL_ID = "claude-sonnet-4-6"` and `ANNOTATOR_BUDGET_CAP_USD = 10.0`. Switch
   `_cost_usd` in `v2_annotator.py` to use `SONNET_INPUT_COST_PER_MTOK_USD` /
   `SONNET_OUTPUT_COST_PER_MTOK_USD` for fallback estimates. Hold
   `JUDGE_MODEL_ID = "claude-haiku-4-5"`, `SAMPLE_SEED = 42`, and `JUDGE_SAMPLE_PER_BENCHMARK`
   constant.
3. **Run a 5-row dry-run** before the full run to verify per-call cost is in the ~$0.04-0.10
   envelope-reported range. If actual cost ≥ $0.20/call, halt and revisit (escalate to intervention
   before busting the $10 cap).
4. **Run the full 115-row annotator** with workers=4 once dry-run passes. Then run
   `select_judge_sample.py` (will deterministically reproduce the 23-row set if completeness is
   115/115). Then run `v2_judge.py` on the 23-row sample.
5. **Extend `compute_stats.py` to a three-way comparator.** Load v1, v2-haiku, v2-sonnet; output
   `_outputs/three_way_comparison.json` with per-benchmark and aggregate accept rates plus Wilson
   95% CIs for each delta. Sample sizes are small (5-6 per benchmark), so CIs will be wide — this is
   expected and must be reported, not hidden. Use the v1-sample subset (12 rows) for the schema-only
   delta to avoid contaminating it with population differences.
6. **Extend `make_charts.py`** with a three-way grouped bar chart and a copy of the atomics
   distribution boxplot. Both go to `results/images/`.
7. **Build the dataset asset** as `assets/dataset/hierarchical-annotation-v2-sonnet/` with the
   spec-v2 layout. The description.md must explicitly state this is the "model-controlled" companion
   to `[t0009]`'s "schema-controlled" v2-haiku asset, intended for the three-way delta analysis, not
   as a replacement.
8. **Open a v3-schema follow-up suggestion** (out of scope for t0014 but the natural next
   experiment): if the schema-only delta is large (≥ 25 pp aggregate), the schema is doing the work
   and a richer v3 (e.g., explicit verification edges or atomics-with-types) is justified. If the
   model-only delta dominates, the recommendation is to default the project to sonnet for annotation
   everywhere and to bypass v3-schema iteration. This decision branch is the primary research output
   of t0014.

## Task Index

### [t0002]

* **Task ID**: `t0002_literature_survey_granularity_conditioning`
* **Name**: Literature Survey: Granularity Conditioning
* **Status**: completed
* **Relevance**: Source of the existing paper corpus that this task's `research_papers.md` draws on
  (Zhou2022, Boisvert2024, Xiong2024, etc.). Provides the prior numerical bands for the schema-only
  and model-only deltas.

### [t0005]

* **Task ID**: `t0005_hierarchical_annotation_pilot_v1`
* **Name**: Hierarchical Annotation Pilot v1
* **Status**: completed
* **Relevance**: Producer of the source 115-row v1 dataset (`hierarchical-annotation-v1`), using
  `claude-sonnet-4-6` annotator + `claude-haiku-4-5-20251001` judge under the **flat**
  list-of-strings schema. The schema-only delta uses this dataset's accept rate as the v1 reference
  point.

### [t0009]

* **Task ID**: `t0009_hierarchical_annotation_v2`
* **Name**: Hierarchical Annotation v2
* **Status**: completed
* **Relevance**: Direct dependency. Provides the v2 tree schema, prompts, parser, judge runner,
  sample selector, asset builder, and the v2-haiku reference accept rate that the model-only delta
  uses. All annotator/judge code is copied verbatim except the two constants noted in Recommendation
  2\.

### [t0006]

* **Task ID**: `t0006_scope_aware_react_library`
* **Name**: Scope-Aware ReAct Library
* **Status**: completed
* **Relevance**: Producer of the `scope_aware_react_v1` library surveyed in Library Landscape. Not
  relevant to t0014 (no annotation or judge code) but enumerated to document that no agent-loop
  library is reused.

### [t0007]

* **Task ID**: `t0007_scope_unaware_planandsolve_library`
* **Name**: Scope-Unaware Plan-and-Solve Library
* **Status**: completed
* **Relevance**: Producer of the `scope_unaware_planandsolve_v1` library surveyed in Library
  Landscape. Not relevant to t0014; cited only for completeness of the library survey.

### [t0010]

* **Task ID**: `t0010_matched_mismatch_library`
* **Name**: Matched-Mismatch Library
* **Status**: completed
* **Relevance**: Producer of the `matched_mismatch_v1` library surveyed in Library Landscape. Not
  relevant to t0014; cited only for completeness of the library survey.

### [t0011]

* **Task ID**: `t0011_metric2_calibration_aggregator`
* **Name**: Metric-2 Calibration Aggregator
* **Status**: completed
* **Relevance**: Producer of the `metric2_calibration_aggregator_v1` library surveyed in Library
  Landscape. Demonstrates the matplotlib + per-benchmark grouped-bar idiom; t0014 follows the same
  `Agg` backend / `dpi=120` / `tick_labels` conventions in the three-way bar chart.

### [t0012]

* **Task ID**: `t0012_phase2_abc_smoke_frontierscience`
* **Name**: Phase 2 ABC Smoke Test (FrontierScience)
* **Status**: in_progress
* **Relevance**: Downstream consumer of `[t0009]`'s v2 dataset (and a potential consumer of t0014's
  v2-sonnet asset if the schema-only delta is small enough that the v2-haiku asset is fit for
  purpose). Sets the practical bar for "is the v2 schema usable as Phase 2 input?".
