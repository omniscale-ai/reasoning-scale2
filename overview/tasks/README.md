# Project Tasks

16 tasks. ✅ **16 completed**.

**Browse by view**: By status: [✅ `completed`](by-status/completed.md); [By date
added](by-date-added/README.md)

---

## Dependency Graph

All tasks completed.

---

## ✅ Completed

<details>
<summary>✅ 0016 — <strong>Brainstorm session 5: prune backlog after t0014
deconfound</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0016_brainstorm_results_5` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md), [`t0013_brainstorm_results_4`](../../overview/tasks/task_pages/t0013_brainstorm_results_4.md), [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md), [`t0015_correct_proxy_benchmark_labels`](../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T22:00:00Z |
| **End time** | 2026-04-30T22:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 5: prune backlog after t0014 deconfound](../../overview/tasks/task_pages/t0016_brainstorm_results_5.md) |
| **Task folder** | [`t0016_brainstorm_results_5/`](../../tasks/t0016_brainstorm_results_5/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0016_brainstorm_results_5/results/results_detailed.md) |

# Brainstorm Session 5: Prune Backlog After t0014 Deconfound

## Context

Session 5 ran on 2026-04-30 immediately after `t0014_v2_annotator_sonnet_rerun` and
`t0015_correct_proxy_benchmark_labels` merged. `t0012_phase2_abc_smoke_frontierscience` is in
progress; this session deliberately does not perturb it.

## Headline Inputs

`t0014` decomposed t0009's published +58 pp v2-vs-v1 judge-accept-rate gain into a **+57 pp
schema-only** delta and a **−1 pp model-only** delta. The annotator-model swap from haiku to
sonnet contributes essentially zero of the gain; the v2 tree schema accounts for nearly all of
it. The +57 pp schema-only delta also bundles a truncation fix (v1 had a 1500-character
`task_excerpt` truncation that v2 removed), which `compare_literature.md` flags as a real
confound.

`t0015` wrote a single corrections-overlay file relabelling 52 of 115 v2 rows: 26 `m2w_*` rows
from `WorkArena++` to `Mind2Web`, and 26 `he_*` rows from `tau-bench` to `HumanEval`.

## Decisions

This session is pure backlog cleanup. No new tasks. No task cancellations. No task updates.
Only suggestion-status corrections.

### Reject (3)

* **S-0005-04** — superseded by t0015 (proxy benchmark naming corrected) and by the inline
  task_id de-duplication fix in t0009.
* **S-0005-05** — duplicate of S-0009-03 (single-blind human review with Cohen's kappa serves
  the same role).
* **S-0014-04** — this is a project-level decision, not a task. The +57 pp schema / −1 pp
  model split already establishes haiku-default as the right policy; recorded as project
  policy rather than executed as a task.

### Reprioritize (5)

* **S-0009-04** medium → **high** — the per-benchmark pattern in t0014 (+100 pp on long-input
  benchmarks vs +13–17 pp on short ones) is exactly what the truncation hypothesis predicts.
  Splitting the schema-only +57 pp into "tree shape" vs "no truncation" is now load-bearing
  for the science.
* **S-0002-09** medium → low — infrastructure chore (re-fetch 11 PDFs with git LFS); low
  signal for the science.
* **S-0006-02** medium → low — async ScopeAwareReactAgent is performance optimization, not
  science; Phase 2 does not need it.
* **S-0011-02** medium → low — provider-specific calibration prompt variants; Phase 2
  currently uses Anthropic only, so variant work is premature.
* **S-0014-05** medium → low — re-running 3 FrontierScience-Olympiad sonnet timeouts only
  recovers 3 rows; n=20 → 23 does not materially change Wilson CIs on the existing
  decomposition.

## Out of Scope

* Creating new tasks (deferred to session 6 once t0012 lands).
* Modifying t0012's in-progress state.
* Replacing the proxy rows with native WorkArena++ / tau-bench data (S-0015-01 remains active
  at medium priority for a future session).

## Outputs

* 8 correction files in `corrections/` against six prior tasks.
* No new suggestions.
* No new assets.
* Updated effective suggestion view: 3 fewer active, 5 with revised priority.

**Results summary:**

> **Results Summary: t0016_brainstorm_results_5**
>
> **Summary**
>
> Brainstorm session 5 was a pure backlog cleanup pass after t0014 (v2 sonnet rerun
> deconfound) and
> t0015 (proxy benchmark relabel) merged. Eight corrections were issued: three rejections,
> five
> priority changes. No new tasks were created and no existing tasks were modified.
>
> **Session Overview**
>
> * **Session number**: 5
> * **Date**: 2026-04-30
> * **Duration**: ~30 minutes
> * **Mode**: Pure cleanup (no new tasks, no task updates)
> * **Researcher budget envelope**: < $5 total (no API spend; planning only)
>
> **Decisions**
>
> **Rejections (3)**
>

</details>

<details>
<summary>✅ 0015 — <strong>Correct proxy-benchmark labels in t0009 v2
dataset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0015_correct_proxy_benchmark_labels` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0009-06` |
| **Task types** | [`correction`](../../meta/task_types/correction/) |
| **Start time** | 2026-04-30T19:08:28Z |
| **End time** | 2026-04-30T19:32:45Z |
| **Step progress** | 9/15 |
| **Task page** | [Correct proxy-benchmark labels in t0009 v2 dataset](../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Task folder** | [`t0015_correct_proxy_benchmark_labels/`](../../tasks/t0015_correct_proxy_benchmark_labels/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0015_correct_proxy_benchmark_labels/results/results_detailed.md) |

# Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Motivation

The `t0009_hierarchical_annotation_v2` dataset asset labels its four benchmarks as
`FrontierScience-Olympiad`, `SWE-bench Verified`, `WorkArena++`, and `tau-bench`. The first
two are accurate. The latter two are mislabelled — the underlying rows are `Mind2Web` and
`HumanEval` rows used as proxies for browser-using and tool-using agent benchmarks, not actual
`WorkArena++` or `tau-bench` rows. Once t0012 (Phase 2 A/B/C smoke) reports per-benchmark
numbers, naïve consumers would attribute results to benchmarks the project does not actually
evaluate on.

This task fixes the labels via the corrections-overlay mechanism — no re-annotation, no API
spend, no change to the t0009 task folder. Implements `S-0009-06` variant b (label correction;
variant a would have replaced the proxy rows with actual WorkArena++/tau-bench data, which is
out of scope for this wave).

## Scope

* Write one correction file per affected benchmark (or one combined correction, depending on
  the aggregator's per-row update support):
  * `WorkArena++` → `Mind2Web`.
  * `tau-bench` → `HumanEval`.
* Action: `update`. The correction overlays `details.json` `description_path` (and any per-row
  `benchmark` fields exposed by the dataset aggregator) so downstream consumers see the
  corrected labels.
* Provide a one-paragraph rationale per correction file referencing the original proxy
  decision taken in t0003 (benchmark download) and t0005 (v1 annotation pilot).
* Run `verify_corrections` against the new files.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data (a separate dataset
task, deferred); editing t0009's task folder (immutable); changing per-row IDs (only the
benchmark label).

## Approach

1. Read t0009's `assets/dataset/hierarchical-annotation-v2/details.json` and the dataset
   aggregator schema to confirm where benchmark labels are exposed (top-level `benchmarks`
   list, per-row `benchmark` field, or both).
2. Confirm the dataset aggregator's correction-overlay support — if `file_changes` is
   required, author a replacement description document and (if applicable) replacement JSONL
   with corrected per-row labels.
3. Write the correction file(s) under `corrections/dataset_<dataset_id>.json` per
   `corrections_specification.md` v3.
4. Re-run the dataset aggregator with the correction overlay applied; confirm the corrected
   labels are visible in the materialized output.

## Expected Outputs

* `corrections/dataset_<t0009_dataset_id>.json` (one or more correction files).
* If `file_changes` is needed: a replacement description document and/or replacement JSONL
  under this task's `assets/dataset/...-relabeled/` folder.
* `results/results_summary.md` reporting how many rows had their benchmark label corrected and
  the before/after distribution.
* `results/results_detailed.md` with the rationale, the correction-file structure, and any
  follow-up suggestion to actually replace the proxy rows with native WorkArena++/tau-bench
  data.

## Compute and Budget

No GPU. No API spend. Estimated cost: **$0**. Per-task cap: $1.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the dataset asset whose labels are being
  corrected.
* Independent of `t0014_v2_annotator_sonnet_rerun`. Order does not matter; if both land before
  t0012 finishes, t0012's per-benchmark reporting will pick up both overlays through the
  aggregator.
* `t0012` (in_progress) reads the t0009 dataset through the aggregator, so the corrected
  labels flow through automatically once t0015 merges. The FrontierScience filter t0012 uses
  is unaffected.

## Source Suggestion

`S-0009-06` variant b — "Relabel the proxy benchmarks WorkArena++→Mind2Web and
tau-bench→HumanEval in the v2 dataset via a correction file."

## Key Questions

1. How many rows are affected by each label correction?
2. Does the t0009 dataset aggregator support per-row label overlays via `changes`, or is a
   `file_changes` overlay needed?
3. Are there any downstream consumers (other than t0012) that already cache the original
   labels and would need re-aggregation?

**Results summary:**

> **Results Summary: Correct Proxy-Benchmark Labels in t0009 v2 Dataset**
>
> **Summary**
>
> Wrote a single corrections-overlay file
> (`corrections/dataset_hierarchical-annotation-v2.json`) that
> relabels the **52** rows in the t0009 v2 hierarchical-annotation dataset whose `benchmark`
> field
> referred to a gated proxy-target benchmark instead of the actual data source: **26** `m2w_*`
> rows
> move from `WorkArena++` to `Mind2Web`, and **26** `he_*` rows move from `tau-bench` to
> `HumanEval`.
> The `aggregate_datasets` overlay applies cleanly: the effective JSONL now carries the
> corrected
> labels and the dataset metadata prose no longer mentions the wrong benchmark names.
>
> **Metrics**
>
> * **Rows relabeled, total**: **52** of 115 (45.2%)
> * **`WorkArena++` -> `Mind2Web`**: **26** rows (all rows whose `task_id` starts with `m2w_`)
> * **`tau-bench` -> `HumanEval`**: **26** rows (all rows whose `task_id` starts with `he_`)
> * **Rows unchanged**: **63** (40 `FrontierScience-Olympiad` + 23 `SWE-bench Verified`)
> * **Effective JSONL distribution after overlay**: 40 / 23 / 26 / 26
>   (FrontierScience-Olympiad /
> SWE-bench Verified / Mind2Web / HumanEval)
> * **Non-`benchmark` field diffs vs source**: **0**

</details>

<details>
<summary>✅ 0014 — <strong>v2 annotator Sonnet rerun: deconfound schema vs
model</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0014_v2_annotator_sonnet_rerun` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0009-01` |
| **Task types** | [`hierarchical-annotation`](../../meta/task_types/hierarchical-annotation/), [`comparative-analysis`](../../meta/task_types/comparative-analysis/) |
| **Start time** | 2026-04-30T19:07:28Z |
| **End time** | 2026-04-30T23:59:00Z |
| **Step progress** | 12/15 |
| **Task page** | [v2 annotator Sonnet rerun: deconfound schema vs model](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Task folder** | [`t0014_v2_annotator_sonnet_rerun/`](../../tasks/t0014_v2_annotator_sonnet_rerun/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0014_v2_annotator_sonnet_rerun/results/results_detailed.md) |

# v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)

## Motivation

`t0009_hierarchical_annotation_v2` reports a v2-vs-v1 judge accept-rate delta of approximately
+58 pp on the stratified haiku-judged sample. The v1 annotator was `claude-sonnet-4-6`; the v2
annotator was switched to `claude-haiku-4-5-20251001` mid-task to fit the cost budget. The
judge model was constant (`claude-haiku-4-5-20251001`). The +58 pp number therefore conflates
two effects:

* schema effect: tree decomposition with subtask-to-atomic edges and full problem text;
* model effect: switching annotator from Sonnet to Haiku.

Without isolating the schema component, the headline claim that "v2 unblocks Phase 2" rests on
a load-bearing-but-unverified assumption. `t0012` (Phase 2 A/B/C smoke on FrontierScience) is
already in flight against the v2 dataset, so this deconfound is needed before any
per-benchmark numbers from t0012 can be reported. Implements `S-0009-01`.

## Scope

* Re-annotate the **same 115 rows** under the same v2 tree schema using `claude-sonnet-4-6` as
  the annotator.
* Use the **same prompt** as t0009 (full problem text, tree-schema system instructions).
* Judge with **the same `claude-haiku-4-5-20251001`** judge on the **same 23-row stratified
  sample** used in t0009 (same row IDs, same seed=42).
* Report per-benchmark and aggregate judge accept rate. Compare against v2-haiku and v1-sonnet
  to decompose the +58 pp delta into a schema component and a model component.
* Persist as a new `dataset` asset under `assets/dataset/hierarchical-annotation-v2-sonnet/`
  with `details.json`, `description.md`, and `files/hierarchical_annotation_v2_sonnet.jsonl`.

Out of scope: re-judging on a different sample, re-running v1 (already in t0005), changing the
schema, expanding row count, fixing the proxy-benchmark labels (handled by `t0015`).

## Approach

1. Read t0009's v2 dataset asset and the original 115 v1 rows from t0005's dataset asset.
2. Construct a v2 annotation prompt (identical to t0009's) with the full problem text and the
   v2 tree schema in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree
   per row.
3. Apply the same task_id deduplication fix used in t0009.
4. Recover the same stratified sample IDs from t0009's results (seed=42, stratified across
   FrontierScience-Olympiad, SWE-bench Verified, and the two proxy benchmarks). Run the haiku
   judge on the v2-sonnet hierarchies for those rows.
5. Persist the dataset asset with `annotation_model: "claude-sonnet-4-6"`. Annotate the
   `description.md` with the deconfound experimental design and the comparison protocol.
6. Compute the three accept-rate deltas:
   * v2-sonnet vs v1-sonnet → schema component (annotator constant).
   * v2-sonnet vs v2-haiku → annotator-model component (schema constant).
   * v2-haiku vs v1-sonnet → original t0009 headline (for sanity check).

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2-sonnet/{details.json, description.md, files/}`.
* `results/results_summary.md` reporting the three deltas with confidence intervals.
* `results/results_detailed.md` with per-row judge verdicts and per-benchmark breakdowns.
* `results/metrics.json` reporting `judge_accept_rate_v2_sonnet` (aggregate) plus
  per-benchmark variants if the metrics registry supports them.
* Follow-up suggestions if the schema component turns out to be small (motivating a v3 schema
  iteration) or the model swap dominates (motivating a Sonnet-default annotation policy).

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$5** (115 sonnet annotations at the same prompt
length as t0009's haiku run + 23 haiku judge calls reusing the same protocol). Per-task cap:
$10.

## Dependencies and Cross-References

* Depends on `t0009_hierarchical_annotation_v2` for the v2 schema, the prompt, the stratified
  sample IDs, and the v2-haiku baseline accept rates.
* Independent of `t0015_correct_proxy_benchmark_labels`. Either order is fine, but if t0015
  lands first, this task should consume the corrected labels in its per-benchmark breakdown
  via the aggregator's correction overlay.
* `t0012` (in_progress) is unaffected — its FrontierScience filter and pre-locked v2 inputs do
  not change retroactively when this task lands.

## Source Suggestion

`S-0009-01` — "Re-run v2 annotation with claude-sonnet-4-6 to isolate the schema effect from
the annotator-model swap."

## Key Questions

1. What is the per-benchmark accept-rate delta of v2-sonnet vs v2-haiku (annotator-model
   component)?
2. What is the per-benchmark accept-rate delta of v2-sonnet vs v1-sonnet (schema component)?
3. Does the FrontierScience-Olympiad benchmark — the worst performer in v1 — improve under
   v2-sonnet? By how much vs the t0009 v2-haiku improvement?
4. If the schema component is small, is there a v3 schema change worth scoping, and should
   t0012's smoke be paused until that lands?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0014_v2_annotator_sonnet_rerun"
> date_completed: "2026-04-30"
> status: "complete"
> ---
> **Results Summary: v2 Annotator Sonnet Rerun (Deconfound Schema vs Model)**
>
> **Summary**
>
> Re-annotated the same 115-row v1 pilot under the v2 tree schema with `claude-sonnet-4-6`,
> re-judged
> with the t0009 `claude-haiku-4-5` judge on the same seed-42 stratified sample (intersected
> to 20
> rows after 3 FrontierScience-Olympiad sonnet timeouts), and decomposed the t0009 +58 pp
> headline
> into a **+57 pp schema-only** delta and a **-1 pp model-only** delta. The annotator-model
> swap
> (haiku -> sonnet) contributes essentially zero of the t0009 gain; the v2 tree schema
> accounts for
> nearly all of it. Total cost $21.16 (annotator $19.77 + judge $1.40), within the
> user-authorised $25
> cumulative cap.
>
> **Metrics**
>

</details>

<details>
<summary>✅ 0013 — <strong>Brainstorm session 4: v2 schema-vs-model confound and
proxy-benchmark labels</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0013_brainstorm_results_4` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md), [`t0008_brainstorm_results_3`](../../overview/tasks/task_pages/t0008_brainstorm_results_3.md), [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T18:00:00Z |
| **End time** | 2026-04-30T18:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 4: v2 schema-vs-model confound and proxy-benchmark labels](../../overview/tasks/task_pages/t0013_brainstorm_results_4.md) |
| **Task folder** | [`t0013_brainstorm_results_4/`](../../tasks/t0013_brainstorm_results_4/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0013_brainstorm_results_4/results/results_detailed.md) |

# Brainstorm Session 4

## Context

Three of the four wave 3 tasks completed: t0009 (v2 tree-schema annotation), t0010 (matched-
mismatch library), t0011 (Metric 2 calibration aggregator). t0012 (Phase 2 A/B/C smoke on
FrontierScience) is `in_progress`. Total spend stands at roughly $9.16 of the $100 project
budget.

Two issues surfaced in t0009 that the headline experiment cannot rest on cleanly:

1. **Schema-vs-model confound.** t0009 reports a +58 pp judge-acceptance delta over v1, but
   the annotation provider was swapped from Claude Sonnet (v1) to Claude Haiku (v2) midway.
   The +58 pp number conflates the tree-schema upgrade with the model swap. Without a Sonnet
   rerun on the v2 schema, we cannot say whether the schema actually moved acceptance — and
   the "v2 unblocks Phase 2" story has a load-bearing dependency on that being a real schema
   effect.
2. **Proxy-benchmark provenance.** The v2 dataset labels two of its four benchmarks
   "WorkArena++" and "tau-bench". The underlying rows are actually Mind2Web and HumanEval rows
   used as proxies. Downstream consumers (and the t0012 in-flight smoke) read the labels at
   face value, which would misrepresent results once the headline numbers are reported.

Suggestion backlog also accumulated: 17 high-priority suggestions across S-0001-* through
S-0011-*, several with overlap and a few that the t0012 in-flight task already covers.

## Decisions

Two new tasks created, both `not_started`, parallel-safe, no dependencies on each other:

* `t0014_v2_annotator_sonnet_rerun` (covers `S-0009-01`) — re-run the v2 annotator on the same
  115 rows using `claude-sonnet-4-6`, judge with the same haiku judge on the same stratified
  sample. Compare per-benchmark accept rate against v2-haiku to isolate the schema component
  of the +58 pp delta. Budget: ~$5.
* `t0015_correct_proxy_benchmark_labels` (covers `S-0009-06` variant b) — write a correction
  file against the t0009 dataset asset that renames the `WorkArena++` benchmark label to
  `Mind2Web` and the `tau-bench` benchmark label to `HumanEval`, with a one-paragraph
  rationale. No new annotation, no API spend. Budget: $0.

Wave budget cap: **$10** combined for both tasks (t0014 ~$5; t0015 ~$0; ~$5 of headroom).

Parallelism: t0014 and t0015 launch in parallel. t0012 stays in_progress and is not modified
by this session — its FrontierScience filter is unaffected by the proxy-benchmark relabel.

## Suggestion cleanup

Five rejections (duplicates or already covered by an in-flight task):

* `S-0002-04` — duplicate of `S-0003-01` (FrontierMath access negotiation).
* `S-0003-02` — duplicate of `S-0002-03` (ServiceNow lab provisioning).
* `S-0005-06` — covered by t0012 (Phase 2 A/B/C smoke FrontierScience scope).
* `S-0007-02` — covered by t0012 (matched-mismatch C condition is exercised inside t0012).
* `S-0005-01` — superseded by `S-0009-03` + `S-0009-05` (the v2 follow-ups are now the
  canonical scaling and human-review track, not the v1-era "row-count expansion" framing).

Three reprioritizations (high → medium):

* `S-0002-01` — pass^k metric (replication infrastructure; not on the headline path until
  after the smoke).
* `S-0002-05` — SWE-bench Docker harness (compute infrastructure; not on the headline path).
* `S-0006-01` — tool registries (registry instrumentation; not on the headline path).

Two follow-ups intentionally **not** corrected:

* `S-0010-01` — kept active as a Phase-2 follow-up to land after t0012's first headline
  result.
* `S-0009-01` — covered by `t0014`, so it stays active and the new task references it through
  `source_suggestion`.

## Out of scope this session

* Multi-provider replication of t0012 (Gemini, OpenAI). Deferred until t0012 produces a
  single- provider headline result.
* v2 row-count expansion beyond 115 rows. Tracked under `S-0009-03`/`S-0009-05`.
* Human review pass over v2 annotations.
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.
* Any change to t0012 itself (in_progress; immutable for this session).

**Results summary:**

> **Brainstorm Session 4 — Results Summary**
>
> **Summary**
>
> Fourth brainstorm produced two new not-started tasks (t0014 and t0015) and applied eight
> correction
> files for the Round 2 cleanup deferred from brainstorm 3. The two tasks address the
> schema-vs-model
> confound and proxy-benchmark provenance issues surfaced by t0009. Wave budget cap: $10. Both
> new
> tasks are parallel-safe; t0012 stays in_progress and unaffected.
>
> **Session Overview**
>
> * **Date**: 2026-04-30
> * **Context**: Triggered after t0009-t0011 merged with $9.16 / $100 spent. t0012 is
>   in_progress.
> t0009 reported a +58 pp v2-vs-v1 judge accept rate but the annotation provider was swapped
> from
> Sonnet (v1) to Haiku (v2), so the headline delta is confounded with the model swap. The v2
> dataset
> also labels two proxy benchmarks under their proxy targets' names instead of the true source
> corpora.
> * **Prompt**: Resolve both pre-Phase-2 issues so t0012's headline experiment can rest on a
>   clean v2
> foundation, and prune the 17-suggestion high-priority backlog.
>

</details>

<details>
<summary>✅ 0012 — <strong>Phase 2 A/B/C smoke harness on FrontierScience
subset</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0012_phase2_abc_smoke_frontierscience` |
| **Status** | completed |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md), [`t0010_matched_mismatch_library`](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md), [`t0011_metric2_calibration_aggregator`](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Expected assets** | 3 predictions, 1 library |
| **Source suggestion** | `S-0006-03` |
| **Task types** | [`experiment-run`](../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../meta/task_types/baseline-evaluation/) |
| **Start time** | 2026-04-30T00:55:11Z |
| **End time** | 2026-05-01T04:43:00Z |
| **Step progress** | 11/15 |
| **Key metrics** | Task Success Rate: **0.025** |
| **Task page** | [Phase 2 A/B/C smoke harness on FrontierScience subset](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Task folder** | [`t0012_phase2_abc_smoke_frontierscience/`](../../tasks/t0012_phase2_abc_smoke_frontierscience/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0012_phase2_abc_smoke_frontierscience/results/results_detailed.md) |

# Phase 2 A/B/C Smoke Harness on FrontierScience Subset

## Motivation

This is the project's **first end-to-end Phase 2 result**. It tests the headline hypothesis on
a real benchmark for the first time: scope-aware (A) > scope-unaware (B) > scope-mismatched
(C). The smoke test is intentionally narrow — single benchmark (FrontierScience-Olympiad),
single provider (Anthropic Claude), N=28 hierarchy-complete rows from the v2 dataset, paired
across conditions. The goal is a directional signal plus a sample-size calibration for
follow-up confirmatory runs. Implements suggestions S-0006-03, S-0007-02, and S-0005-06.

## Hypotheses tested

| RQ | Predicted direction | Detection threshold at N=28 |
| --- | --- | --- |
| RQ1 — A success rate > B success rate | A − B ≥ +5pp | ~15pp paired (McNemar/sign test, α=0.05) |
| RQ2 — A overconfident error rate < B | A − B ≤ −2pp | ~5-8pp paired |
| RQ5 — C worst on Metrics 1 and 2 | C < min(A, B) on both | clear ranking when A > B + 5pp |

Excluded by design (handled in separate experiments on the right benchmarks):

* RQ3 (request-vs-act accuracy on low-level tasks) — needs tau-bench, not FrontierScience.
* RQ4 (gains concentrated in info-asymmetric states) — needs WorkArena++ or tool-using
  benchmark.

## Scope

* Build a small `phase2_smoke_harness_v1` library under `assets/library/` that:
  * Loads the v2 dataset asset from t0009 and filters to FrontierScience-Olympiad rows with
    `hierarchy_completeness == true`.
  * Runs a phase-order walk over each row's `hierarchy` (global → all subtasks → all
    `global_atomics`); for each step in the walk, dispatches to one of the three libraries (A:
    t0006, B: t0007, C: t0010).
  * Captures every step's trajectory record into one JSONL per condition under
    `assets/predictions/`.
  * Calls t0011's `compute_overconfident_error_rate` on each trajectory file.
  * Computes `task_success_rate` by parsing each trajectory's final `Finish` answer and
    comparing to the row's gold final answer (FrontierScience problems end with `FINAL ANSWER:
    ...`).
  * Reports `avg_decisions_per_task` per condition.
* Produce three `predictions` assets (one per condition: A, B, C).
* Produce one `library` asset for the harness itself.
* Run on the **28 hierarchy-complete FrontierScience-Olympiad rows** from the v2 dataset (this
  matches the v1 hierarchy-complete count; refine after t0009 lands if v2 row count differs).

Out of scope: multi-provider replication (deferred), benchmark-specific tool registries beyond
a minimal `python_exec` for FrontierScience math problems, scaling N beyond ~28.

## Approach

1. Read the v2 dataset asset from t0009 once t0009 has merged. Filter to FrontierScience-
   Olympiad and `hierarchy_completeness == true`.
2. Implement the harness library that drives the phase-order walk and dispatches
   per-condition. Reuse t0006, t0007, t0010 libraries; reuse t0011's calibration aggregator.
3. For each row, run all three conditions against the same model (`claude-sonnet-4-6-20251001`
   recommended) with paired execution (same seed where applicable, same problem text, same
   tool registry).
4. Tool registry is minimal: a single `python_exec` tool for arithmetic and one
   `Finish(answer)` tool. FrontierScience-Olympiad rows are mostly verbal reasoning; tools
   exist for explicit computation only.
5. Persist trajectory JSONLs under `assets/predictions/<condition>/files/`. Compute and
   persist metrics.
6. Write `results/results_summary.md` with the 3×3 condition × metric table and the predicted-
   versus-observed effect sizes. Write `results/results_detailed.md` with per-row trajectories
   summarised, the McNemar p-value for A-vs-B and B-vs-C, and the implied sample size for
   follow-up confirmatory runs.
7. Generate at least 2 charts: condition × metric bar chart with confidence intervals; per-row
   success matrix heatmap (rows=problems, columns=conditions).

## Expected Outputs

* `assets/library/phase2_smoke_harness_v1/` — the harness library.
* `assets/predictions/phase2_smoke_a/`, `assets/predictions/phase2_smoke_b/`,
  `assets/predictions/phase2_smoke_c/` — three predictions assets, one per condition.
* `results/metrics.json` in explicit-variant format (3 variants: A, B, C; metrics:
  `task_success_rate`, `overconfident_error_rate`, `avg_decisions_per_task`).
* `results/results_summary.md` and `results/results_detailed.md` with hypothesis-test results,
  effect sizes, sample-size calibration, and clear acknowledgement of the excluded RQs.
* `results/images/` with at least 2 charts.
* Follow-up suggestions for: multi-provider replication (Gemini, OpenAI), expansion to
  tool-using benchmarks (SWE-bench, tau-bench), confirmatory N expansion based on observed
  variance.

## Compute and Budget

No GPU. Anthropic API only. **Budget cap: USD 20** (per-task default cap is $10; this task
exceeds the default and explicitly opts up). Estimated breakdown: 28 rows × 3 conditions × ~3
self-consistency calls per step × ~6 steps per row × ~$0.005 per call = $7.5 baseline; budget
$20 leaves headroom for retries and the calibration prompt.

## Dependencies and Cross-References

* **Hard dependencies (must be `completed`)**:
  * `t0009_hierarchical_annotation_v2` — produces the v2 dataset asset this task consumes.
  * `t0010_matched_mismatch_library` — produces the C-condition library.
  * `t0011_metric2_calibration_aggregator` — produces the Metric 2 implementation.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  libraries.
* References Yao2022 ReAct, Wang2023 Plan-and-Solve, and Xiong2024 calibration paper assets
  from t0002.

## Source Suggestion

S-0006-03 — "Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience subset." Also
covers S-0007-02 and S-0005-06 by consolidation.

## Key Questions

1. Does A − B reach the +5pp threshold on `task_success_rate`?
2. Does A − B reach the −2pp threshold on `overconfident_error_rate`?
3. Does C rank strictly worst on both metrics relative to A and B?
4. What is the within-condition variance, and what N does the FrontierScience confirmatory run
   need to detect a 5pp effect at α=0.05 with paired test?
5. Are there per-domain (physics / chemistry / biology) effect-size differences worth
   surfacing to the next brainstorm?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0012_phase2_abc_smoke_frontierscience"
> ---
> **Results Summary — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)**
>
> **Summary**
>
> All three agent conditions (scope-aware ReAct A, scope-unaware Plan-and-Solve B,
> scope-mismatched
> Plan-and-Solve C) solved near-zero FrontierScience-Olympiad problems with claude-haiku-4-5
> and no
> tools: A solved 1/40 (2.5%), B solved 0/40, C solved 0/11 (budget halted at 11 rows). The
> paired
> McNemar test across the 6 fully overlapping rows yields p=1.0 for all pairs — the null is
> not
> rejected, and the smoke confirms that FrontierScience-Olympiad is beyond haiku capacity
> without tool
> use.
>
> **Metrics**
>
> * **task_success_rate**: A=0.025 (1/40), B=0.000 (0/40), C=0.000 (0/11)
> * **overconfident_error_rate**: A=0.647, B=0.000\*, C=0.000\* (\*collapsed — no
>   final_confidence in
> Plan-and-Solve trajectories; not comparable to A)

</details>

<details>
<summary>✅ 0011 — <strong>Metric 2 calibration aggregator: verbalized confidence
+ 3-sample self-consistency</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0011_metric2_calibration_aggregator` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-02` |
| **Task types** | [`write-library`](../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:12Z |
| **End time** | 2026-04-29T23:43:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Metric 2 calibration aggregator: verbalized confidence + 3-sample self-consistency](../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Task folder** | [`t0011_metric2_calibration_aggregator/`](../../tasks/t0011_metric2_calibration_aggregator/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0011_metric2_calibration_aggregator/results/results_detailed.md) |

# Metric 2 Calibration Aggregator (Xiong2024 Protocol)

## Motivation

The project's Metric 2 (`overconfident_error_rate`) has no implementation: it is registered in
`meta/metrics/` but no code computes it. The literature survey (t0002) identified Xiong2024 as
the canonical calibration protocol — verbalized confidence elicitation (low / medium / high +
brief justification) plus 3-sample self-consistency aggregation. Without this library, the
Phase 2 smoke test (t0012) cannot report Metric 2 — only Metric 1 (success rate) and the
diagnostic Metric 3 (avg decisions per task). This task unblocks the headline experiment by
producing a library that any agent's trajectory records can be passed through to compute
`overconfident_error_rate`. Implements suggestion S-0002-02.

## Scope

* Implement a library asset under `assets/library/metric2_calibration_aggregator_v1/`
  exposing:
  * `class ConfidencePromptTemplate`: the human-inspired confidence-elicitation prompt (low /
    medium / high + one-sentence justification) per Xiong2024 §3.2.
  * `class ConfidenceJudge`: aggregator that takes 3 trajectory samples for the same problem
    and returns `(predicted_label, predicted_confidence, is_correct)`. Self-consistency is
    majority-vote on the predicted label; confidence is the mean across samples.
  * `function compute_overconfident_error_rate(records: Iterable[CalibrationRecord]) -> float`
    that returns the fraction of records where `is_correct == False` and `predicted_confidence
    > = HIGH_CONFIDENCE_THRESHOLD`. The threshold is a module constant (default 0.75).
  * `function elicit_confidence(model_call, problem, action) -> tuple[str, float]` that calls
    the model with the prompt template and parses the response.
  * `dataclass CalibrationRecord(frozen=True, slots=True)`: the canonical record shape that
    `compute_overconfident_error_rate` consumes.
* Implementation must accept trajectory records emitted by t0006/t0007/t0010 libraries — i.e.,
  must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema as input.
* Provide pytest coverage at
  `tasks/t0011_metric2_calibration_aggregator/code/test_calibration.py` covering: prompt
  template formatting, parsing of low / medium / high confidence labels, majority-vote
  aggregation across 3 samples (including ties), threshold-based overconfident detection, and
  end-to-end run on a synthetic 10-record dataset.

Out of scope: the actual experiment harness (handled by t0012), live API calls (deterministic
tests only), provider-specific calibration variants.

## Approach

1. Read t0002's Xiong2024 paper summary
   (`tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md`)
   to ground the prompt template and threshold choice.
2. Implement in `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` with a
   `paths.py` and `constants.py` per the project Python style guide.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests use `ScriptedModel` from t0007 to simulate model responses for the confidence prompt.
5. Run `verify_library_asset`, ruff, mypy, and pytest.

## Expected Outputs

* `assets/library/metric2_calibration_aggregator_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` and tests.
* `results/results_summary.md` with API surface description, test summary, and the threshold
  default rationale.
* Follow-up suggestion for: provider-specific calibration variants, ECE (expected calibration
  error) computation in addition to overconfident-error-rate.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Xiong2024 paper asset (`10.48550_arXiv.2306.13063`) from t0002's library.
* Output format consumed by t0012's experiment harness.

## Source Suggestion

S-0002-02 — "Implement verbalized-confidence + 3-sample self-consistency aggregator for Metric
2."

## Key Questions

1. What is the right default `HIGH_CONFIDENCE_THRESHOLD`? Xiong2024 uses 0.75 with verbalized
   labels mapped to {low: 0.25, medium: 0.5, high: 0.9}; the default should match.
2. How should the aggregator handle ties in the majority vote across 3 samples? Default:
   prefer the highest-confidence sample.
3. What is the expected output schema for compute_overconfident_error_rate so Phase 2 results
   can include it in `metrics.json` directly?

**Results summary:**

> **Results Summary — Metric 2 Calibration Aggregator**
>
> **Summary**
>
> Implemented the metric2_calibration_aggregator_v1 library that operationalizes the project's
> Metric
> 2 (`overconfident_error_rate`) using the Xiong2024 §3.2 black-box calibration protocol. The
> library
> exposes `ConfidencePromptTemplate`, `ConfidenceJudge`, `elicit_confidence`,
> `compute_overconfident_error_rate`, and `CalibrationRecord` plus a trajectory-record
> adapter, with a
> single overridable threshold default (`HIGH_CONFIDENCE_THRESHOLD = 0.75`) and the canonical
> low/medium/high → 0.25/0.5/0.9 numeric mapping.
>
> **Metrics**
>
> * **Tests run**: 25 — all passed in 0.03 s
> (`uv run pytest tasks/t0011_metric2_calibration_aggregator/code/`).
> * **Code lines written**: ~340 in `code/calibration.py`, ~125 in `code/constants.py`, ~40 in
> `code/paths.py`, ~370 in `code/test_calibration.py` (test count includes the `ScriptedModel`
> fake).
> * **Public API surface**: 5 entry points required by the task description plus 1 helper
> (`calibration_record_from_trajectory`); 6 entry points listed in `details.json`.

</details>

<details>
<summary>✅ 0010 — <strong>Matched-mismatch library: condition C with deliberately
wrong granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0010_matched_mismatch_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0007-01` |
| **Task types** | [`write-library`](../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T23:25:02Z |
| **End time** | 2026-04-29T23:46:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Matched-mismatch library: condition C with deliberately wrong granularity tags](../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Task folder** | [`t0010_matched_mismatch_library/`](../../tasks/t0010_matched_mismatch_library/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0010_matched_mismatch_library/results/results_detailed.md) |

# Matched-Mismatch Library (Condition C)

## Motivation

The project's main hypothesis includes sub-hypothesis 2: scope-mismatched agents perform
strictly worse than both scope-aware (A) and scope-unaware (B) baselines. Without a C library,
research question 5 cannot be tested. This task implements C by wrapping the existing
libraries (`scope_aware_react_v1` from t0006 or `scope_unaware_planandsolve_v1` from t0007)
with a granularity-tag layer that emits **deliberately incorrect** tags at each step. The
library shares the canonical `TRAJECTORY_RECORD_FIELDS` schema from t0007 so a Phase 2 harness
can run all three conditions interchangeably. Implements suggestion S-0007-01.

## Scope

* Implement a library asset under `assets/library/matched_mismatch_v1/` exposing a
  `MatchedMismatchAgent` class that:
  * Accepts a problem statement, an annotation tree (the v2 hierarchy from t0009), a tool
    registry, a model-call callable, and a `mismatch_strategy: "random" | "adversarial"`.
  * Walks the v2 hierarchy in phase order (the harness's canonical walk), determines the
    correct granularity at each step from the annotation, and **assigns an incorrect tag**
    according to the strategy:
    * `random`: pick uniformly from `{global, subtask, atomic} \ correct_tag`.
    * `adversarial`: always pick the most distant tag (`atomic` when correct is `global`,
      `global` when correct is `atomic`, `atomic` when correct is `subtask`).
  * Delegates each step to either `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`
    (configurable). The delegate handles the actual model call; the wrapper only controls the
    granularity tag.
  * Emits trajectory records in the canonical `TRAJECTORY_RECORD_FIELDS` schema, with the
    `granularity` field carrying the *wrong* tag (the actual correct tag is logged separately
    as `_correct_granularity` in an extras blob).
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0010_matched_mismatch_library/code/test_matched_mismatch.py` covering:
  random-strategy uniformity over `{global, subtask, atomic} \ correct_tag`,
  adversarial-strategy correctness, schema parity with t0007, end-to-end run with both
  delegate options.

Out of scope: the actual A/B/C experiment (handled by t0012), benchmark-specific tool
registries, remote execution.

## Approach

1. Read t0007's `scope_unaware_planandsolve_v1` library and t0006's `scope_aware_react_v1`
   library. Confirm the canonical trajectory schema is `TRAJECTORY_RECORD_FIELDS` from t0007.
2. Implement the library in `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py`.
   Re-export the public API from `assets/library/matched_mismatch_v1/library/`.
3. Write `details.json`, `description.md`, and `files/` for the asset.
4. Tests are deterministic (no live API calls). Use `ScriptedModel` from t0007 as the
   delegate's model.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/matched_mismatch_v1/` with `details.json`, `description.md`, `files/`.
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion to make the random-strategy mismatch ablation (uniform random vs.
  adversarial vs. matched) explicit in t0012.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References t0006 (`scope_aware_react_v1`) and t0007 (`scope_unaware_planandsolve_v1`)
  library assets. Reads `TRAJECTORY_RECORD_FIELDS` from t0007.

## Source Suggestion

S-0007-01 — "Implement matched-mismatch (C) library on top of scope_unaware_planandsolve_v1."

## Key Questions

1. What is the cleanest way to handle a granularity tag for steps that fall under
   `global_atomics` (cross-cutting atomics with no parent subtask)? Default: treat as `atomic`
   for the purposes of the mismatch strategy.
2. Should the wrapper expose a way to override the mismatch policy per-step (e.g., to inject
   targeted mismatches in specific phases)? Default: no, keep the wrapper minimal.
3. How should the schema's `_correct_granularity` extras field be standardised so a downstream
   experiment can compute the mismatch contribution per step?

**Results summary:**

> **Results Summary: Matched-Mismatch Library (Condition C)**
>
> **Summary**
>
> Implemented the project's condition-C library `matched_mismatch_v1` — a wrapper that walks
> the v2
> hierarchy from t0009 in canonical phase order, substitutes a deliberately incorrect
> granularity tag
> according to a `random` or `adversarial` strategy, and delegates the per-phase model call to
> either
> the t0006 ReAct or t0007 Plan-and-Solve format. The library reuses t0007's
> `TRAJECTORY_RECORD_FIELDS` schema unchanged and stores the correct tag in
> `extras["_correct_granularity"]`. All 14 deterministic tests pass and every `REQ-*`
> checklist item
> is satisfied.
>
> **Metrics**
>
> * **Tests passed**: 14 of 14 (`uv run pytest tasks/t0010_matched_mismatch_library/code/
>   -v`).
> * **Source lines (`matched_mismatch.py`)**: 463 lines including documentation and `__all__`
>   export
> list.
> * **Public API entry points**: 6 (`MatchedMismatchAgent`, `MatchedMismatchRecord`,
>   `AgentRunResult`,
> `Phase`, `iter_phases`, `pick_mismatch_tag`).
> * **Module-level constants exported**: 4 (`GRANULARITY_VALUES`, `ADVERSARIAL_MAP`,

</details>

<details>
<summary>✅ 0009 — <strong>Hierarchical annotation v2: tree schema with
subtask-to-atomic edges</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0009_hierarchical_annotation_v2` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0005-02` |
| **Task types** | [`hierarchical-annotation`](../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T23:24:52Z |
| **End time** | 2026-04-30T00:53:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Hierarchical annotation v2: tree schema with subtask-to-atomic edges](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Task folder** | [`t0009_hierarchical_annotation_v2/`](../../tasks/t0009_hierarchical_annotation_v2/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0009_hierarchical_annotation_v2/results/results_detailed.md) |

# Hierarchical Annotation v2 (Tree Schema)

## Motivation

The v1 annotation produced by `t0005_hierarchical_annotation_pilot_v1` uses a flat schema:
`subtask` is a `list[str]`, `atomic` is a `list[str]`, and there is no encoded edge mapping
atomics to their parent subtask. The v1 schema also truncates problem text to 1500 characters
in the `task_excerpt` field, which the v1 LLM-as-judge identified as the dominant failure mode
on FrontierScience-Olympiad rows (0/3 accept rate). This task fixes both issues: re-annotates
all 115 rows under a tree-shaped v2 schema with full problem text, and spot-checks at least
20% of rows with the LLM judge to estimate quality. Implements suggestion S-0005-02 and the
partial v2-schema portion of S-0005-01.

## v2 Schema

```json
{
  "task_id": "...",
  "benchmark": "...",
  "domain": "...",
  "difficulty": { ... },
  "problem": "...",
  "hierarchy": {
    "global": "<one-sentence top-level approach>",
    "subtasks": [
      {
        "subtask": "<subtask description>",
        "atomics": ["<atomic step>", "..."]
      },
      ...
    ],
    "global_atomics": ["<cross-cutting atomic step>", "..."]
  },
  "gold_actions": {
    "global": "<resolved global action>",
    "subtasks": [
      {
        "subtask": "<resolved subtask action>",
        "atomics": ["<resolved atomic action>", "..."]
      },
      ...
    ],
    "global_atomics": ["<resolved cross-cutting atomic action>", "..."]
  },
  "annotation_model": "claude-sonnet-4-6",
  "judge_verdict": "acceptable" | "needs revision" | null,
  "judge_notes": "...",
  "hierarchy_completeness": true | false
}
```

`global_atomics` captures atomic steps that do not belong to any single subtask (typically
verification, sanity checks, or cross-cutting concerns surfaced in v1's flat `atomic` list).

## Scope

* Re-run the v1 annotator (`claude-sonnet-4-6`) with a new prompt that elicits the tree schema
  above. Pass the **full problem text** (no `task_excerpt` truncation).
* Apply the same task_id deduplication fix from v1 (the source pilot file has 14 rows with
  colliding `task_id`s; thread `_pilot_row_index` through the asset).
* Spot-check at least 23 rows (20%) with `claude-haiku-4-5-20251001` as judge. Sample is
  stratified across the four benchmarks (FrontierScience-Olympiad, SWE-bench Verified,
  HumanEval-proxy, Mind2Web-proxy).
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical-annotation-v2/`
  with the schema above and a `description.md` explaining the v2 → v1 migration.
* Compare v2 vs v1 judge accept rate per benchmark and flag any benchmark where v2 fails to
  improve.

Out of scope: scaling beyond 115 rows (S-0005-01 expansion), human review (full review pass
deferred to v3), proxy benchmark replacement (deferred to follow-up).

## Approach

1. Read the v1 dataset `assets/dataset/hierarchical-annotation-v1/files/*.jsonl` from t0005
   and load all 115 rows.
2. For each row, construct a v2 annotation prompt with the full problem text and the v2 schema
   in the system prompt. Pass to `claude-sonnet-4-6`. Capture the parsed tree.
3. Stratified-sample 23 rows. For each, call the haiku judge with the row's full problem and
   the proposed v2 hierarchy; capture verdict + one-sentence justification.
4. Persist as a `dataset` asset with `details.json` (source = t0005's v1 dataset asset,
   version = "v2", license inherited per row, sample count = 115) and
   `files/hierarchical_annotation_v2.jsonl`.
5. Report per-benchmark v2-vs-v1 judge accept rate delta in `results/results_detailed.md`.

## Expected Outputs

* `assets/dataset/hierarchical-annotation-v2/{details.json, description.md, files/}`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate vs v1.
* `results/results_detailed.md` with the full audit table, the v2-vs-v1 comparison, and any
  rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (mean atomics per row).
* Follow-up suggestions for: row-count expansion to ≥200, human review pass, proxy benchmark
  remediation, and any benchmark where v2 fails to improve over v1.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: **~$15** (115 sonnet annotations + 23 haiku
judges). Per-task cap: $20.

## Dependencies and Cross-References

* No task dependencies. Reads t0005's v1 dataset asset as input but does not depend on the
  t0005 task being incomplete.
* References `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows, original).
* Sister-task coordination: t0012 will consume the v2 dataset; this task must publish the v2
  dataset asset before t0012's implementation step runs.

## Source Suggestion

S-0005-02 — "Re-run LLM-as-judge with full problem text (no truncation)." Also partially
addresses S-0005-01 (annotation v2 schema) and the schema-gap finding from brainstorm 3.

## Key Questions

1. What is the per-benchmark judge accept rate under v2 vs v1?
2. How does the v2 schema's tree shape affect FrontierScience-Olympiad acceptance specifically
   (the worst-performing benchmark in v1)?
3. Are there rows where the v2 tree decomposition is well-defined but the v1 flat
   decomposition was empty (hierarchy_completeness: false in v1)?
4. What fraction of atomics fall under `global_atomics` vs assigned to a specific subtask?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0009_hierarchical_annotation_v2"
> date_completed: "2026-04-30"
> status: "complete"
> ---
> **Results Summary: Hierarchical Annotation v2**
>
> **Summary**
>
> All 115 rows of the v1 hierarchical-annotation pilot were re-annotated under the v2 tree
> schema with
> `claude-haiku-4-5` and full problem text, achieving 115/115 hierarchy completeness and a
> 21/23 (91%)
> judge accept rate on the stratified spot-check. Per-benchmark v2-vs-v1 deltas are uniformly
> positive, ranging from +33% (SWE-bench Verified, tau-bench) to +100% (WorkArena++).
>
> **Metrics**
>
> * **avg_decisions_per_task** = **16.38** atomic actions per row across the 115-row v2
>   dataset (range
> 4-65, median 14). Tracks plan-length distribution.
> * **Per-benchmark v2 judge accept rate**: FrontierScience-Olympiad **67% (4/6)**, SWE-bench
>   Verified

</details>

<details>
<summary>✅ 0008 — <strong>Brainstorm session 3: insert v2 re-annotation, plan Phase
2 smoke</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0008_brainstorm_results_3` |
| **Status** | completed |
| **Effective date** | 2026-04-30 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md), [`t0004_brainstorm_results_2`](../../overview/tasks/task_pages/t0004_brainstorm_results_2.md), [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md), [`t0006_scope_aware_react_library`](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md), [`t0007_scope_unaware_planandsolve_library`](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-30T00:00:00Z |
| **End time** | 2026-04-30T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 3: insert v2 re-annotation, plan Phase 2 smoke](../../overview/tasks/task_pages/t0008_brainstorm_results_3.md) |
| **Task folder** | [`t0008_brainstorm_results_3/`](../../tasks/t0008_brainstorm_results_3/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0008_brainstorm_results_3/results/results_detailed.md) |

# Brainstorm Session 3

## Context

Wave 2 (t0004 brainstorm + t0005, t0006, t0007) merged at $0.06 total cost. The literature
survey, benchmark download, annotation pilot v1, and both scope-aware / scope-unaware
libraries are complete. The project is poised for the first Phase 2 result — but the v1
annotation schema has a structural gap that must be fixed first.

## Schema gap discovered

While modelling A/C condition prompts on the `is_bored` (HumanEval/91) row, we found that the
v1 annotation schema is **flat**: `subtask` is a list of strings, `atomic` is a list of
strings, and there is **no encoded edge** mapping atomics to their parent subtask. For the
`hierarchical-annotation-v1` smoke harness this forces one of three orderings — none of them
faithful to how humans actually reason hierarchically — and undermines the cleanliness of the
A-vs-B-vs-C contrast in the planned Phase 2 smoke test.

The fix is a tree-shaped v2 schema:

```json
{
  "hierarchy": {
    "global": "...",
    "subtasks": [
      {"subtask": "...", "atomics": ["...", "..."]},
      ...
    ],
    "global_atomics": ["..."]
  }
}
```

This change is **inserted as the new ASAP task** (t0009) before any of the previously-planned
wave 3 tasks can build on it.

## Decisions

Four new tasks created, all `not_started`. Three are parallel-safe; one waits on the others:

* `t0009_hierarchical_annotation_v2` (covers `S-0005-01` partial + `S-0005-02` + new schema
  finding) — re-annotate all 115 rows under the tree schema with full problem text. **No
  deps.**
* `t0010_matched_mismatch_library` (covers `S-0007-01`) — matched-mismatch (C) library; reuses
  t0007's `TRAJECTORY_RECORD_FIELDS`. Schema-independent. **No deps.**
* `t0011_metric2_calibration_aggregator` (covers `S-0002-02`) — Xiong2024
  verbalized-confidence + 3-sample self-consistency aggregator. Schema-independent. **No
  deps.**
* `t0012_phase2_abc_smoke_frontierscience` (covers `S-0006-03`, `S-0007-02`, `S-0005-06`) —
  first end-to-end Phase 2 A/B/C run on the FrontierScience subset of the **v2** dataset.
  **Deps**: t0009, t0010, t0011.

## Why this wave

Three tasks unblock the headline experiment:

* t0009 fixes the schema so the harness can drive granularity transitions naturally
  (depth-first by subtask in v2) instead of by an artificial phase walk over flat lists.
* t0010 provides the C condition without which RQ5 (sub-hypothesis 2) cannot be tested.
* t0011 implements Metric 2; without it the smoke test can only report Metric 1.

t0012 is the first run that produces a directional A/B/C signal on a real benchmark. It is
deliberately scoped as a smoke test (N=28 on hierarchy-complete FS-Olympiad rows, single
provider Anthropic, paired across conditions) rather than a definitive experiment. The
follow-up multi-provider replication (Gemini + OpenAI keys are now available) is queued for
the next brainstorm.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03; demoting four high-priority access/infrastructure suggestions to medium) —
  flagged earlier but explicitly deferred to keep this session focused on the v2 ASAP work.
* Multi-provider (Gemini, OpenAI) replication of the smoke test — deferred until t0012
  produces a single-provider headline result.
* Annotation v2 row-count expansion to ≥200 (covered by S-0005-01 in part; t0009 only
  re-encodes the existing 115 rows, not new annotation work).
* SWE-bench Docker harness, ServiceNow provisioning, FrontierMath access negotiation.

**Results summary:**

> **Brainstorm Session 3 — Results Summary**
>
> **Summary**
>
> Third brainstorm produced four new not-started tasks. The v1 annotation schema was found to
> lack
> subtask-to-atomic edges; a v2 re-annotation task was inserted ASAP as t0009. The original
> wave 3
> plan (matched-mismatch library, Metric 2 calibration, A/B/C smoke harness) was preserved and
> renumbered to t0010-t0012, with t0012 gated on the other three.
>
> **Session Overview**
>
> * **Date**: 2026-04-30
> * **Context**: Triggered after wave 2 (t0004-t0007) merged at $0.06 spend, with 27 uncovered
> suggestions and the v2 schema gap surfaced during prompt-modelling discussion of the
> `is_bored`
> annotation.
> * **Prompt**: Plan the first Phase 2 result on a real benchmark, with whatever schema
>   upgrades are
> needed to make the harness honest about the granularity transitions.
>
> **Decisions**
>

</details>

<details>
<summary>✅ 0007 — <strong>Scope-unaware Plan-and-Solve library: condition B
baseline</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0007_scope_unaware_planandsolve_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-06` |
| **Task types** | [`write-library`](../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:48Z |
| **End time** | 2026-04-29T20:01:00Z |
| **Step progress** | 9/15 |
| **Task page** | [Scope-unaware Plan-and-Solve library: condition B baseline](../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Task folder** | [`t0007_scope_unaware_planandsolve_library/`](../../tasks/t0007_scope_unaware_planandsolve_library/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0007_scope_unaware_planandsolve_library/results/results_detailed.md) |

# Scope-Unaware Plan-and-Solve Library (Condition B)

## Motivation

The literature survey in t0002 identified Plan-and-Solve (Wang2023) as the strongest published
prompt-only baseline that does not condition on explicit granularity tags. It is therefore the
canonical scope-unaware (B) baseline for the project's A-vs-B-vs-C comparison. This task
produces the matching library asset, sharing the trajectory-log schema with t0006 so a Phase 2
experiment can run both libraries against the same harness without bespoke glue. Implements
suggestion S-0002-06.

## Scope

* Implement a library asset under `assets/library/scope_unaware_planandsolve_v1/` exposing a
  `PlanAndSolveAgent` class that:
  * Accepts a problem statement, a tool registry, and a model-call callable.
  * Generates a free-form numbered plan, then executes each step sequentially through a
    Plan-and-Execute loop.
  * Emits trajectory records in the same schema as `scope_aware_react_v1` so both libraries
    are drop-in interchangeable. The `granularity` field in the schema is filled with the
    literal string `"unspecified"` to mark the B condition.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}`.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Adapt LangChain's `Plan-and-Execute` reference implementation rather than re-implementing
  from scratch. License is Apache 2.0; record attribution in `description.md`.
* Provide pytest coverage at
  `tasks/t0007_scope_unaware_planandsolve_library/code/test_planandsolve.py` covering: plan
  parsing, sequential execution, trajectory schema parity with t0006, finish detection, and
  error recovery on malformed model output.

Out of scope: actual A-vs-B-vs-C experiment, benchmark-specific tool registries, remote
execution.

## Approach

1. Read t0002's Wang2023 paper summary and the LangChain Plan-and-Execute source to ground the
   prompt template and execution loop.
2. Implement the library in
   `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and re-export the
   public API from `assets/library/scope_unaware_planandsolve_v1/library/`.
3. Reuse the trajectory log schema defined in t0006 by reading t0006's library when it lands;
   if t0006 has not landed yet, define the schema here and document that t0006 must conform.
4. Write `details.json`, `description.md`, and `files/` for the asset.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_unaware_planandsolve_v1/` with `details.json`, `description.md`,
  `files/`.
* `tasks/t0007_scope_unaware_planandsolve_library/code/planandsolve.py` and tests.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for the matched mismatch (C) library.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. May reference t0006's library if it merges first; otherwise this task
  defines the trajectory schema and t0006 must conform.
* References Wang2023 paper asset (`10.48550_arXiv.2305.04091`) from t0002.

## Source Suggestion

S-0002-06 — "Implement Plan-and-Solve as the canonical scope-unaware (B) baseline."

## Key Questions

1. What plan format does Plan-and-Solve produce, and how should it be parsed
   deterministically?
2. How should the library mark the absence of a granularity tag in the trajectory record?
3. What is the minimal API surface that lets a Phase 2 harness swap between this and t0006's
   library by changing only one line?

**Results summary:**

> ---
> spec_version: "2"
> task_id: "t0007_scope_unaware_planandsolve_library"
> date_completed: "2026-04-29"
> ---
> **Results Summary — t0007_scope_unaware_planandsolve_library**
>
> **Summary**
>
> Produced one library asset, `scope_unaware_planandsolve_v1`, that adapts LangChain's
> Plan-and-Execute reference implementation of Wang et al.'s Plan-and-Solve prompting (arXiv
> 2305.04091) as the canonical scope-unaware (B) baseline for the project. The library passes
> its
> asset verificator and a 14-case pytest suite, all without any paid API calls.
>
> **Metrics**
>
> * **Library tests passing**: **14 / 14** (zero failures)
> * **Ruff errors on task code**: **0**
> * **Mypy errors on task code**: **0**
> * **Library asset verificator errors / warnings**: **0 / 0**

</details>

<details>
<summary>✅ 0006 — <strong>Scope-aware ReAct library: condition A with explicit
granularity tags</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0006_scope_aware_react_library` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0002-07` |
| **Task types** | [`write-library`](../../meta/task_types/write-library/) |
| **Start time** | 2026-04-29T19:35:38Z |
| **End time** | 2026-04-29T20:07:30Z |
| **Step progress** | 10/15 |
| **Task page** | [Scope-aware ReAct library: condition A with explicit granularity tags](../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Task folder** | [`t0006_scope_aware_react_library/`](../../tasks/t0006_scope_aware_react_library/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0006_scope_aware_react_library/results/results_detailed.md) |

# Scope-Aware ReAct Library (Condition A)

## Motivation

The project's main hypothesis is that explicit granularity conditioning improves agent
performance. The literature survey in t0002 identified ReAct (Yao2022) as the canonical
foundation for the scope-aware (A) condition. This task produces a self-contained library that
extends ReAct with a `{global, subtask, atomic}` granularity tag emitted at every Thought /
Action turn, plus a logging hook that records the active tag alongside the model's confidence.
The library is the substrate every Phase 2 A-condition experiment will import. Implements
suggestion S-0002-07.

## Scope

* Implement a library asset under `assets/library/scope_aware_react_v1/` exposing a
  `ScopeAwareReactAgent` class that:
  * Accepts a problem statement, a fixed `granularity` argument (`"global" | "subtask" |
    "atomic"`), a tool registry, and a model-call callable.
  * Loops Thought / Action / Observation steps, prepending the active granularity tag to every
    Thought emission, and parses Action JSON until the agent emits a `Finish` action.
  * Logs every step's `{turn_index, granularity, thought, action, observation, confidence}` to
    a JSONL trajectory file the experiment harness can replay.
  * Supports a deterministic-test mode that accepts pre-recorded model outputs.
* Provide pytest coverage at
  `tasks/t0006_scope_aware_react_library/code/test_scope_aware_react.py` covering: tag
  injection, action parsing, finish detection, error recovery on malformed JSON, and
  trajectory logging integrity.

Out of scope: the actual A-vs-B-vs-C experiment (a separate experiment-run task), benchmark-
specific tool registries (also a separate task), and any remote-execution wiring.

## Approach

1. Read t0002's `research/research_papers.md` and the Yao2022 paper summary to ground the
   prompt format. Reuse LangChain's ReAct prompt where appropriate; the project licence is
   Apache 2.0.
2. Implement the library in `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py`
   and re-export the public API from a `library/__init__.py` shim under `assets/library/
   scope_aware_react_v1/`.
3. Write the asset's `details.json`, `description.md`, and `files/` directory with the
   runnable source.
4. Write tests as deterministic unit tests; no live API calls.
5. Run `verify_library_asset` and the test suite.

## Expected Outputs

* `assets/library/scope_aware_react_v1/` with `details.json`, `description.md`, and `files/`.
* `tasks/t0006_scope_aware_react_library/code/scope_aware_react.py` and matching test file.
* `results/results_summary.md` with API surface description and test summary.
* Follow-up suggestion for benchmark-specific tool registries.

## Compute and Budget

No GPU. No paid API calls (deterministic tests only). Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies.
* References Yao2022 paper asset (`10.48550_arXiv.2210.03629`) from t0002.
* Sister task `t0007_scope_unaware_planandsolve_library` produces the matched B baseline; both
  must follow the same trajectory-logging schema so a Phase 2 experiment can consume both.

## Source Suggestion

S-0002-07 — "Implement scope-aware (A) as ReAct extended with explicit granularity tags."

## Key Questions

1. What is the minimal extension to ReAct's prompt template that reliably elicits a
   granularity tag on every Thought emission?
2. How should the library handle a model that refuses to emit a tag (back off, abort, or
   default to `atomic`)?
3. What schema for the trajectory log lets t0007 emit identical-shape records?

**Results summary:**

> **Results Summary: Scope-Aware ReAct Library**
>
> **Summary**
>
> Shipped the project's first library asset: `scope_aware_react_v1`, implementing condition A
> (scope-aware ReAct) with explicit `{global, subtask, atomic}` granularity tags, a JSONL
> trajectory
> writer whose six-field schema is the canonical contract for both this library and t0007, and
> deterministic-replay testing via `ScriptedModel`. All quality gates clean and the asset
> verificator
> passed.
>
> **Metrics**
>
> * **Library asset**: 1 (`scope_aware_react_v1`), passes
>   `meta.asset_types.library.verificator` with
> **0 errors / 0 warnings**.
> * **Tests**: **8 / 8** passing in `code/test_scope_aware_react.py`
> (`pytest tasks/t0006_scope_aware_react_library/code/ -v` reported all tests passing).
> * **Source files**: **3 modules** in `code/` (`scope_aware_react.py` ~370 lines,
>   `constants.py`,
> `paths.py`) plus 1 test file.
> * **Public entry points**: **6** (`ScopeAwareReactAgent`, `ScriptedModel`,
>   `TrajectoryRecord`,
> `Action`, `AgentResult`, `MalformedActionError`).

</details>

<details>
<summary>✅ 0005 — <strong>Hierarchical annotation pilot v1: audit and conform
existing 115 rows</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0005_hierarchical_annotation_pilot_v1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 1 dataset |
| **Source suggestion** | `S-0002-08` |
| **Task types** | [`hierarchical-annotation`](../../meta/task_types/hierarchical-annotation/) |
| **Start time** | 2026-04-29T19:35:28Z |
| **End time** | 2026-04-29T20:14:30Z |
| **Step progress** | 9/15 |
| **Task page** | [Hierarchical annotation pilot v1: audit and conform existing 115 rows](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Task folder** | [`t0005_hierarchical_annotation_pilot_v1/`](../../tasks/t0005_hierarchical_annotation_pilot_v1/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0005_hierarchical_annotation_pilot_v1/results/results_detailed.md) |

# Hierarchical Annotation Pilot v1

## Motivation

Phase 1 of the project's roadmap requires ≥100 tasks fully annotated with gold actions at
three granularity levels (global / subtask / atomic). The imported
`project/data/annotation_pilot/ tasks_annotated.jsonl` already contains 115 LLM-annotated
rows, but the rows have not been verified to conform to the project's three-level schema and
there is no human or LLM-as-judge spot-check pass on record. This task closes that gap in v1
form: keep the existing 115 rows in place, audit their structure, and produce a canonical
dataset asset that downstream Phase 2 / 3 experiments can consume. Implements suggestion
S-0002-08.

## Scope

* Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on
  each row to determine whether it carries explicit global / subtask / atomic granularity
  labels or whether the granularity must be inferred.
* If labels are missing, write a deterministic mapper that derives the three-level structure
  from the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block
  per row.
* Run an LLM-as-judge spot-check on at least 10% of rows (≥12 rows) to estimate hierarchy
  quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
* Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/`
  with rows of shape `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask,
  atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict,
  judge_notes}`.

Out of scope for v1: replacing the HumanEval and Mind2Web proxies, expanding beyond 115 rows,
human review, inter-rater agreement studies. All deferred to follow-up tasks.

## Approach

1. Load the 115-row pilot file. For each row, compute the inferred or stated hierarchy and
   emit the canonical schema record.
2. Sample at least 12 rows stratified across the four benchmarks (FrontierScience-Olympiad,
   SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy). Send each to the LLM judge with the
   row's problem text and proposed hierarchy; capture verdict ("acceptable" / "needs
   revision") plus a one-sentence justification.
3. Persist the consolidated dataset asset with `details.json` (source URL = the imported pilot
   path, version = "v1", license = inherited from each upstream benchmark, sample count = 115)
   and `files/hierarchical_annotation_v1.jsonl`.
4. Report distribution stats in `results/results_detailed.md` (per-benchmark counts,
   per-domain counts, hierarchy-completeness rate, judge accept rate).

## Expected Outputs

* `assets/dataset/hierarchical_annotation_v1/` with `details.json`, `files/`, and a
  `description.md`.
* `results/results_summary.md` with per-benchmark completeness and judge accept rate.
* `results/results_detailed.md` with the full audit table and any rows that failed the judge.
* `results/metrics.json` reporting `avg_decisions_per_task` (the registered diagnostic
  metric).
* Follow-up suggestions for: extension to ≥200 rows, full human-review pass, and proxy
  benchmark remediation.

## Compute and Budget

No GPU. Anthropic API only. Estimated cost: under 3 USD for 12-15 LLM-as-judge calls on
`claude-haiku-4-5-20251001`. Per-task cap: 5 USD.

## Dependencies and Cross-References

* No task dependencies.
* Reads `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows).
* Reads `project/code/scripts/collect_and_annotate.py` and `project/code/src/` modules — wrap
  as black-box utilities, never modify in place.
* References the four benchmark dataset assets produced by `t0003_download_benchmark_subsets`.

## Source Suggestion

S-0002-08 — "Run a Phase 1 pilot annotation on 20 tasks before scaling to 100." This task
implements that idea in v1 form, leveraging the existing 115 rows rather than re-annotating
from scratch.

## Key Questions

1. Do the existing 115 rows already carry a global / subtask / atomic decomposition, or must
   one be inferred?
2. What is the per-benchmark hierarchy-completeness rate?
3. What is the LLM-as-judge accept rate? Does it differ across benchmarks?
4. Are there systematic patterns in rejected rows (e.g., one benchmark consistently failing)?

**Results summary:**

> **Results Summary: Hierarchical Annotation Pilot v1**
>
> **Summary**
>
> Audited the 115-row pilot annotation file, projected each row's `steps.nodes` graph onto the
> project's three-level global / subtask / atomic schema with a deterministic Python mapper,
> ran an
> LLM-as-judge spot-check on a 12-row stratified sample using `claude-haiku-4-5-20251001` via
> the
> local `claude` CLI, and produced a single canonical `hierarchical-annotation-v1` dataset
> asset (115
> rows). The asset passes the dataset verificator with 0 errors and 1 warning.
>
> **Metrics**
>
> * **Rows in dataset**: **115** (FrontierScience-Olympiad **40**, SWE-bench Verified **23**,
> tau-bench **26**, WorkArena++ **26**)
> * **Overall hierarchy completeness**: **88.7%** (102 / 115 rows have a non-null `global` and
>   a
> non-empty `atomic` list)
> * **Per-benchmark completeness**: FrontierScience-Olympiad **70.0%** (28/40), SWE-bench
>   Verified
> **100.0%** (23/23), tau-bench **96.2%** (25/26), WorkArena++ **100.0%** (26/26)
> * **LLM-as-judge accept rate (overall)**: **33.3%** (4/12 rows accepted)
> * **Per-benchmark judge accept rate**: FrontierScience-Olympiad **0.0%** (0/3), SWE-bench
>   Verified

</details>

<details>
<summary>✅ 0004 — <strong>Brainstorm session 2: plan Phase 1 annotation and Phase
2 baseline libraries</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0004_brainstorm_results_2` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | [`t0001_brainstorm_results_1`](../../overview/tasks/task_pages/t0001_brainstorm_results_1.md), [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md), [`t0003_download_benchmark_subsets`](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T15:30:00Z |
| **End time** | 2026-04-29T15:30:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 2: plan Phase 1 annotation and Phase 2 baseline libraries](../../overview/tasks/task_pages/t0004_brainstorm_results_2.md) |
| **Task folder** | [`t0004_brainstorm_results_2/`](../../tasks/t0004_brainstorm_results_2/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0004_brainstorm_results_2/results/results_detailed.md) |

# Brainstorm Session 2

## Context

Second brainstorm session. The first wave (t0001 brainstorm + t0002 literature survey + t0003
benchmark download) completed at $0 cost. Three completed tasks have produced 11 paper assets,
4 dataset assets, and 15 uncovered follow-up suggestions.

Key findings carried into this session:

* **Literature survey (t0002)** identified Plan-and-Solve [Wang2023] as the canonical
  scope-unaware (B) baseline, ReAct [Yao2022] as the foundation for the scope-aware (A)
  condition, and Xiong2024 as the calibration protocol for Metric 2.
* **Benchmark download (t0003)** confirmed FrontierMath (gated by Epoch AI) and WorkArena++
  (gated by ServiceNow + HF) cannot be unblocked by infrastructure work in the current
  session. Pilot proxies are frozen as fallback. SWE-bench Verified and tau-bench are
  accessible.
* The deferred T3 candidate from session 1 (`hierarchical_annotation_pilot`) is now
  appropriate to schedule, but in a smaller v1 form: audit and conform the existing 115 pilot
  rows rather than attempt a full re-annotation.

## Decisions

Three new tasks created, all `not_started`, no inter-task dependencies (parallel-safe):

* `t0005_hierarchical_annotation_pilot_v1` (covers `S-0002-08`) — audit & conform the existing
  pilot annotations to the global / subtask / atomic schema.
* `t0006_scope_aware_react_library` (covers `S-0002-07`) — write-library: ReAct extended with
  granularity tags. Implements the A condition.
* `t0007_scope_unaware_planandsolve_library` (covers `S-0002-06`) — write-library:
  Plan-and-Solve adapted from LangChain. Implements the B condition.

## Why this wave

t0005 unblocks Phase 1 (annotation deliverable). t0006 + t0007 are the two libraries the Phase
2 baseline experiment will consume. Once all three are merged, the Phase 2 smoke-test
experiment (deferred T4 from session 1) becomes practical to schedule.

## Out of scope this session

* Round 2 suggestion cleanup (rejecting S-0003-01 and S-0003-02 as duplicates of S-0002-04 and
  S-0002-03) is intentionally deferred to a follow-up session.
* SWE-bench Docker harness (S-0002-05) is deferred until experiment tasks need it.
* FrontierMath (S-0002-04 / S-0003-01) and ServiceNow (S-0002-03 / S-0003-02) access remain
  open high-priority blockers but not on the path to first Phase 2 results.

**Results summary:**

> **Brainstorm Session 2 — Results Summary**
>
> **Summary**
>
> Second brainstorm produced three new not-started tasks for parallel execution: a v1
> hierarchical
> annotation pilot and two baseline libraries (ReAct+tags for the A condition, Plan-and-Solve
> for the
> B condition). Round 2 suggestion cleanup deferred to a follow-up session.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Triggered after t0001-t0003 wave completed at $0 spend, with 15 uncovered
>   suggestions
> queued.
> * **Prompt**: Plan Phase 1 annotation deliverable and the libraries Phase 2 baseline
>   experiment will
> need.
>
> **Decisions**
>
> 1. **Create `t0005_hierarchical_annotation_pilot_v1`** (covers `S-0002-08`,
> `hierarchical-annotation`). Audit and conform the 115 existing pilot rows to the global /
> subtask

</details>

<details>
<summary>✅ 0003 — <strong>Download benchmark subsets for the four roadmap
sources</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0003_download_benchmark_subsets` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 4 dataset |
| **Source suggestion** | — |
| **Task types** | [`download-dataset`](../../meta/task_types/download-dataset/) |
| **Start time** | 2026-04-29T14:30:55Z |
| **End time** | 2026-04-29T14:58:30Z |
| **Step progress** | 8/15 |
| **Task page** | [Download benchmark subsets for the four roadmap sources](../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Task folder** | [`t0003_download_benchmark_subsets/`](../../tasks/t0003_download_benchmark_subsets/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0003_download_benchmark_subsets/results/results_detailed.md) |

# Download Benchmark Subsets

## Motivation

Phase 1 (annotation) and Phase 2 (baseline scope-aware vs. scope-unaware experiment) both
depend on having local, reproducible subsets of the four roadmap benchmarks. The existing
pilot annotation data uses HumanEval and Mind2Web proxies for tau-bench and WorkArena++
because the real benchmarks were "unavailable on HF" at original-annotation time. This task
either resolves that gap by acquiring the real benchmarks or, if access is genuinely
unavailable, documents the decision to keep proxies and freezes the choice for Phase 2.

## Scope

Acquire four benchmark subsets, each targeted at multi-step tasks of 4-8 decisions per task to
match the project's stated difficulty range:

* FrontierScience-Olympiad — full official distribution path; subset by domain to match the
  pilot's physics / chemistry / biology focus.
* WorkArena++ — official distribution. If genuinely inaccessible (gated, retired, dataset
  moved), document the access attempt and keep the Mind2Web proxy already present in the
  pilot.
* SWE-bench Verified — official Princeton/HF distribution; subset to instances that map
  cleanly onto the project's three-level hierarchy.
* tau-bench — official distribution. If genuinely inaccessible, keep the HumanEval proxy with
  documented justification.

Out of scope: full benchmark execution harnesses (those belong in later experiment-run tasks),
custom annotation (that belongs in T3 hierarchical-annotation pilot), and modifications of
benchmark data (subsetting only, no relabelling).

## Approach

1. For each benchmark, attempt the official distribution path documented in its source paper
   or GitHub README. Cache successful downloads under the task's
   `assets/dataset/<slug>/files/`.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata
   the benchmark provides. If no such metadata exists, sample uniformly and document the
   sampling seed.
3. Produce one dataset asset per benchmark with `details.json` describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log to the dataset asset's
   `details.json` with `download_status: "failed"` and a clear `download_failure_reason`. The
   project's policy in this case is to keep the existing pilot proxy and not block on access.
5. Emit follow-up suggestions for any benchmark whose access pathway is non-obvious or whose
   subsetting choice deserves a Phase 2 sensitivity check.

## Expected Outputs

* Four dataset assets under
  `assets/dataset/{frontierscience,workarena_plus_plus,swebench_verified, taubench}/` with
  `details.json` and `files/` directories (or empty `files/` plus a clear failed status if
  inaccessible).
* `results/results_summary.md` with a per-benchmark access status, sample count, and any
  subset decisions.
* `results/suggestions.json` flagging any benchmarks where the proxy choice is now permanent.

## Compute and Budget

No GPU. No paid API calls anticipated. All work is local downloads and metadata writing.
Estimated cost: USD 0.

## Dependencies and Cross-References

* No task dependencies. Independent of T1.
* Cross-references: existing pilot annotation data at
  `project/data/annotation_pilot/tasks_annotated.jsonl` documents the proxy decisions this
  task must either resolve or formalise.

**Results summary:**

> **Results Summary: Download Benchmark Subsets**
>
> **Summary**
>
> Acquired four benchmark subsets covering the project's roadmap sources
> (FrontierScience-Olympiad,
> WorkArena++, SWE-bench Verified, tau-bench). Three were downloaded directly from public
> sources;
> WorkArena++ instance enumeration is gated on a live ServiceNow developer instance, so its
> asset
> captures the upstream curriculum manifest only and freezes the Mind2Web pilot proxy as the
> de-facto
> Phase 2 fallback. All four dataset assets pass `verify_dataset_asset` with zero errors.
>
> **Metrics**
>
> * **4 of 4** dataset assets created and passing `verify_dataset_asset` (zero errors, zero
>   warnings).
> * **FrontierScience-Olympiad subset**: **40** problems (15 physics, 10 chemistry, 15
>   biology),
> packaged from pilot rows; status **success** (FrontierMath upstream still gated).
> * **WorkArena++ subset**: **42** compositional task class lists extracted from upstream
> `curriculum.py`; status **success (manifest only)**, instance enumeration deferred and
> Mind2Web
> pilot proxy frozen.
> * **SWE-bench Verified subset**: **60** instances filtered from **500** Verified using the
>   4-8 hunks
> rule; status **success**.

</details>

<details>
<summary>✅ 0002 — <strong>Literature survey: granularity conditioning and
hierarchical agents</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0002_literature_survey_granularity_conditioning` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | 10 paper |
| **Source suggestion** | — |
| **Task types** | [`literature-survey`](../../meta/task_types/literature-survey/) |
| **Start time** | 2026-04-29T13:50:47Z |
| **End time** | 2026-04-29T14:26:49Z |
| **Step progress** | 11/15 |
| **Task page** | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Task folder** | [`t0002_literature_survey_granularity_conditioning/`](../../tasks/t0002_literature_survey_granularity_conditioning/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0002_literature_survey_granularity_conditioning/results/results_detailed.md) |

# Literature Survey: Granularity Conditioning and Hierarchical Agents

## Motivation

The project's central hypothesis is that explicitly conditioning an LLM agent on its current
operating granularity (global / subtask / atomic) improves task success, calibration, and
request-vs-act discrimination. Before designing the Phase 2 baseline experiment we need
literature grounding on three threads: how prior work has framed and operationalised
"granularity" or "scope" labels for hierarchical agents, what hierarchical task decomposition
schemas exist in the four benchmark sources, and which uncertainty-calibration metrics have
been used in agent settings (in particular, definitions and prior measurements of the
overconfident error rate). The survey output anchors every later planning decision and lets us
cite prior work in the Phase 4 paper-ready report.

## Scope

* Granularity / scope / scale conditioning in LLM agents and prompt engineering. Include any
  work that varies the level of abstraction at which an agent receives its instructions, even
  if the authors do not use the word "granularity".
* Hierarchical task decomposition: papers proposing two-, three-, or n-level decompositions
  for benchmarks similar to those in this project (FrontierScience-Olympiad, WorkArena++,
  SWE-bench Verified, tau-bench).
* Uncertainty calibration in LLM agents: confidence elicitation methods, definitions of
  overconfident error rate, calibration plots and metrics, and prior reports on how
  calibration changes with prompt design.
* The four roadmap benchmarks themselves: their official task structures, scoring conventions,
  and any published results that bracket what counts as competitive performance.

Out of scope: training-time techniques (RL, gradient-based fine-tuning), non-English
benchmarks, production deployment papers — all consistent with the project's Out of Scope
section.

## Approach

1. Run the standard `/research-papers` and `/research-internet` stages with the three thread
   queries above. Use the `download-paper` skill for any candidate paper found via search.
2. Produce paper assets under `assets/paper/` for at least 10 highly relevant papers, each
   with a summary that conforms to the paper asset specification.
3. Aggregate findings into `research/research_papers.md` with a section per thread:
   granularity conditioning, hierarchical decomposition, calibration metrics, benchmark
   grounding.
4. Connect each thread back to the project's research questions and explicitly flag (a) any
   prior work that already answers a research question, (b) any methodological choices the
   survey resolves for Phase 2, and (c) any open questions to surface as suggestions.

## Expected Outputs

* At least 10 paper assets under `assets/paper/<paper_id>/` with `details.json`, summary, and
  PDF or markdown file.
* `research/research_papers.md` and `research/research_internet.md` synthesising the survey.
* `results/results_summary.md` with a thread-by-thread takeaway and explicit follow-up
  suggestions for the next brainstorm session (typically: which benchmarks to deprioritise,
  which conditioning prompts to adopt, which calibration metric to register as a project
  metric).
* `results/suggestions.json` with concrete follow-up ideas surfaced by the survey.

## Compute and Budget

No GPU. Anthropic API only (the project's `available_services` list dropped `openai_api` until
an API key is provided). Estimated cost: under 5 USD for paper summarisation through Claude.

## Dependencies and Cross-References

* No task dependencies. Independent of T2.
* Reads `project/description.md` for research questions and success criteria.
* The project's pre-existing `project/data/annotation_pilot/tasks_annotated.jsonl` should be
  inspected during the survey to ground discussion of benchmark coverage.

## Key Questions

1. What prior work explicitly compares scope-aware vs. scope-unaware vs. scope-mismatched LLM
   agents on multi-step benchmarks, and what effect sizes did they report?
2. What definitions of "overconfident error rate" exist in the agent calibration literature,
   and which is most appropriate for our Metric 2 specification?
3. What hierarchical decomposition schemas are already published for FrontierScience-Olympiad,
   WorkArena++, SWE-bench Verified, and tau-bench, and how do they map to our global / subtask
   / atomic split?
4. Are the WorkArena++ and tau-bench benchmarks truly inaccessible (as the existing pilot data
   suggests), or are there standard distribution channels we missed?

**Results summary:**

> **Results Summary: Literature Survey on Granularity Conditioning and Hierarchical Agents**
>
> **Summary**
>
> Completed a literature survey of 11 papers covering granularity / scope conditioning of LLM
> agents,
> hierarchical task decomposition, uncertainty calibration, and the four roadmap benchmarks
> (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). All 11 paper assets
> pass the
> v3 paper-asset verificator and are tagged with project categories.
>
> **Metrics**
>
> * **11 paper assets created** out of a 10-paper minimum target — exceeds REQ-1 by one paper.
> * **4 of 4 survey threads covered** with at least 2 papers each: granularity / hierarchical
> prompting (Yao2022, Wang2023, Shinn2023, Zhou2022, Wei2022 noted but not added in this round
> — 4
> added), four roadmap benchmarks (Glazer2024, Drouin2024, Boisvert2024, Jimenez2024,
> OpenAI2024,
> Yao2024 — 6 added), calibration (Xiong2024 — 1 added).
> * **0 errors** across 11 verificator runs; 1 minor warning (PA-W007 missing-country) on the
>   first
> paper, fixed by adding country codes.
>
> **Verification**

</details>

<details>
<summary>✅ 0001 — <strong>Brainstorm session 1: plan first project tasks</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0001_brainstorm_results_1` |
| **Status** | completed |
| **Effective date** | 2026-04-29 |
| **Dependencies** | — |
| **Expected assets** | — |
| **Source suggestion** | — |
| **Task types** | [`brainstorming`](../../meta/task_types/brainstorming/) |
| **Start time** | 2026-04-29T00:00:00Z |
| **End time** | 2026-04-29T00:00:00Z |
| **Step progress** | 4/4 |
| **Task page** | [Brainstorm session 1: plan first project tasks](../../overview/tasks/task_pages/t0001_brainstorm_results_1.md) |
| **Task folder** | [`t0001_brainstorm_results_1/`](../../tasks/t0001_brainstorm_results_1/) |
| **Detailed report** | [results_detailed.md](../../tasks/t0001_brainstorm_results_1/results/results_detailed.md) |

# Brainstorm Session 1

## Context

This is the first brainstorm session for the granularity-aware hierarchical agents project,
executed inline as part of `/setup-project` immediately after `meta/` was populated. The
project has no completed tasks, no suggestions, and no answer assets, so the session focused
on Round 1 (propose first tasks). Rounds 2 (suggestion cleanup) and 3 (confirmation) had
nothing to clean up and proceeded straight to confirmation.

## Decisions

The researcher accepted two child tasks for immediate creation:

* `t0002_literature_survey_granularity_conditioning` — survey papers on granularity / scope /
  scale conditioning in LLM agents, hierarchical task decomposition, and uncertainty
  calibration metrics.
* `t0003_download_benchmark_subsets` — wire up access to subsets of the four roadmap
  benchmarks (FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench) at
  difficulty 4-8 decisions per task.

Two further candidate tasks (`hierarchical_annotation_pilot` and
`baseline_scope_experiment_smoke_test`) were discussed in detail but deferred — the researcher
will review T1 and T2 outputs before committing.

## Why these tasks first

T1 and T2 are independent and low-cost. T1 anchors later planning decisions in the literature;
T2 unblocks every Phase 1 annotation extension and every Phase 2/3 experiment. Running them in
parallel keeps the project moving while preserving the option to redirect after the literature
survey.

## Out-of-band notes

* `project/data/annotation_pilot/tasks_annotated.jsonl` already contains 115 LLM-annotated
  rows, but tau-bench and WorkArena++ rows use HumanEval and Mind2Web proxies because the real
  benchmarks were "unavailable on HF" at original-annotation time. T2 must address this
  directly.
* The `available_services` list dropped `openai_api` during setup because no API key was
  provided; `anthropic_api` remains. T1 and T2 should plan their LLM use accordingly.

**Results summary:**

> **Brainstorm Session 1 — Results Summary**
>
> **Summary**
>
> The first brainstorm session for the granularity-aware hierarchical agents project produced
> two new
> not-started tasks (literature survey and benchmark download) and deferred two further
> candidates
> pending the literature-survey output. No suggestions, corrections, or answer assets were
> produced;
> the project is brand new and the suggestion backlog is empty.
>
> **Session Overview**
>
> * **Date**: 2026-04-29
> * **Context**: Inline brainstorm executed by `/setup-project` immediately after `meta/` was
> populated. Project repository was a fresh fork of the Glite ARF template.
> * **Prompt**: Translate the project description and four-phase roadmap into concrete first
>   tasks the
> researcher can launch.
>
> **Decisions**
>
> 1. **Create `t0002_literature_survey_granularity_conditioning`**. Survey the literature on

</details>
