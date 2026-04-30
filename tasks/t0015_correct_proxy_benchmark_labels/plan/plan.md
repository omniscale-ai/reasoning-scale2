---
spec_version: "2"
task_id: "t0015_correct_proxy_benchmark_labels"
date_completed: "2026-04-30"
status: "complete"
---

# Plan — Correct Proxy-Benchmark Labels in t0009 v2 Dataset

## Objective

Correct the `benchmark` field of 52 rows in the `hierarchical-annotation-v2` dataset asset (produced
by `t0009_hierarchical_annotation_v2`) by relabeling 26 rows from `WorkArena++` to `Mind2Web` and 26
rows from `tau-bench` to `HumanEval`, plus rewriting the dataset's description and metadata so they
no longer mention the wrong proxy names. Delivery is a single correction-overlay file under this
task's `corrections/` folder. Done = `verify_corrections` passes and
`aggregate_datasets --ids hierarchical-annotation-v2` materializes the corrected labels in both
per-row data and prose. Cost is $0; no API or GPU calls.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md`:

```text
Name: Correct proxy-benchmark labels in t0009 v2 dataset

Short description: Write a correction file against the t0009 v2 dataset asset that relabels the
WorkArena++ benchmark to Mind2Web and tau-bench to HumanEval, reflecting the actual proxy sources.

Long description (excerpt):
* Write one correction file per affected benchmark (or one combined correction).
  * WorkArena++ → Mind2Web.
  * tau-bench → HumanEval.
* Action: update. The correction overlays details.json description_path (and any per-row benchmark
  fields exposed by the dataset aggregator) so downstream consumers see the corrected labels.
* Provide a one-paragraph rationale per correction file referencing the original proxy decision
  taken in t0003 (benchmark download) and t0005 (v1 annotation pilot).
* Run verify_corrections against the new files.

Out of scope: replacing proxy rows with actual WorkArena++/tau-bench data; editing t0009's task
folder; changing per-row IDs.

Expected Outputs:
* corrections/dataset_<t0009_dataset_id>.json (one or more correction files).
* If file_changes is needed: a replacement description document and/or replacement JSONL under this
  task's assets/dataset/...-relabeled/ folder.
* results/results_summary.md reporting how many rows had their benchmark label corrected and the
  before/after distribution.
* results/results_detailed.md with the rationale, the correction-file structure, and any follow-up
  suggestion to actually replace the proxy rows with native WorkArena++/tau-bench data.

Key questions:
1. How many rows are affected by each label correction?
2. Does the aggregator support per-row label overlays via changes, or is file_changes needed?
3. Are there any downstream consumers (other than t0012) that already cache the original labels?
```

| ID | Requirement | Satisfied by step | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Relabel `WorkArena++` rows to `Mind2Web` | Step 4 + Step 6 | All 26 `m2w_*` rows in the relabeled JSONL carry `benchmark == "Mind2Web"`. |
| REQ-2 | Relabel `tau-bench` rows to `HumanEval` | Step 4 + Step 6 | All 26 `he_*` rows in the relabeled JSONL carry `benchmark == "HumanEval"`. |
| REQ-3 | Use action `update` in the correction file | Step 5 | `corrections/dataset_hierarchical-annotation-v2.json` `action == "update"`. |
| REQ-4 | Overlay `description_path` and any prose mentioning the wrong labels | Step 3 + Step 5 | `file_changes` swaps `description.md`; `changes` overrides `short_description` and `size_description`. |
| REQ-5 | One-paragraph rationale referencing the t0003 / t0005 proxy decision | Step 5 | `rationale` field in the correction file cites both tasks. |
| REQ-6 | `verify_corrections` passes against the new files | Step 7 | Verificator output: PASSED. |
| REQ-7 | Confirm corrected labels visible in materialized aggregator output | Step 7 | `aggregate_datasets --ids hierarchical-annotation-v2 --detail full` shows the new prose; loading the effective JSONL shows the new benchmark counts. |
| REQ-8 | Out of scope: do not edit t0009's folder, do not change per-row IDs, do not replace proxy rows with native data | Step 4 | Diff of relabeled JSONL vs source: only `benchmark` differs in 52 rows; `_pilot_row_index` and `task_id` unchanged. |
| REQ-9 | Report row counts and before/after distribution | Step 12 (results — orchestrator) | `results/results_summary.md`. |
| REQ-10 | Provide a follow-up suggestion to replace proxy rows with native WorkArena++ / tau-bench data | Step 14 (suggestions — orchestrator) | `results/suggestions.json`. |

The mapping of question 1 → 26 + 26 rows (52 total). Question 2 → both `changes` and `file_changes`
are needed because per-row `benchmark` is exposed through the JSONL, which the metadata-only
`changes` block cannot reach. Question 3 → no other downstream consumer caches the labels at write
time; aggregator output is computed fresh on every read.

## Approach

The correction is a pure data overlay. The plan creates one replacement dataset asset under this
task's `assets/dataset/hierarchical-annotation-v2-relabeled/` folder containing two files: a new
`description.md` with corrected benchmark names and a new
`files/hierarchical_annotation_v2_relabeled.jsonl` with the 52 benchmark fields rewritten. The
correction file at `corrections/dataset_hierarchical-annotation-v2.json` uses `action: update` with
both `changes` (override `short_description` and `size_description` so prose stops mentioning the
wrong proxy names) and `file_changes` (replace `description.md` and
`files/hierarchical_annotation_v2.jsonl` with this task's replacements).

This approach was selected because the dataset aggregator at
`meta/asset_types/dataset/aggregator.py` exposes per-row data only through the JSONL file: a
metadata-only `update` cannot reach the `benchmark` field inside each row. Research confirmed this
in `research/research_code.md`. **Alternative considered**: a `delete` correction followed by a
`replace` correction pointing at a brand-new dataset asset. Rejected because that would force every
downstream consumer to re-resolve the asset ID, and the project already has [t0012] depending on
`hierarchical-annotation-v2` by ID. The `update` overlay preserves the ID and is the canonical
in-place fix.

**Task type**: `correction` (already set in `task.json`). The correction task type's planning
guideline is "no remote machines, no expensive operations, deliver via overlay" — the plan respects
all three. No additional task type is needed.

## Cost Estimation

Total: **$0**.

* OpenAI API: $0 (no LLM calls).
* Anthropic API: $0 (no LLM calls).
* Vast.ai: $0 (no GPU).
* Local compute: a few seconds of Python to stream and rewrite a 115-line JSONL.

The project budget cap for this task is $1; estimated spend is $0, so the cap is not at risk.

## Step by Step

1. **Verify the source row counts and prefix mapping.** Run a Python one-liner on
   `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
   that groups rows by `benchmark` and by `task_id` prefix. Expected: `m2w_` → 26 rows all
   `WorkArena++`, `he_` → 26 rows all `tau-bench`, `fs_` → 40 rows all `FrontierScience-Olympiad`,
   `swe_` → 23 rows all `SWE-bench Verified`. Halt if the counts do not match; the mapping
   assumption is wrong if they do not. Satisfies REQ-1, REQ-2, REQ-8.

2. **Create the replacement dataset asset folder.** Make
   `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/`
   and a `files/` subfolder. Add `.gitkeep` to `files/` only if needed (a real file follows in step
   4). Satisfies REQ-4.

3. **Write the relabeled `description.md`.** Copy the source `description.md` from t0009's asset
   verbatim, then rewrite every occurrence of `WorkArena++` to `Mind2Web` and every occurrence of
   `tau-bench` to `HumanEval` (including in tables, prose, and the abstract sentence). Update the
   YAML frontmatter `dataset_id` to `hierarchical-annotation-v2-relabeled` and the
   `summarized_by_task` to `t0015_correct_proxy_benchmark_labels`. Add a short note in the Overview
   section explaining that this is the relabeled overlay and the source dataset still carries the
   proxy labels. Save to
   `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md`.
   Run `uv run flowmark --inplace --nobackup` on the result. Satisfies REQ-1, REQ-2, REQ-4.

4. **Write the relabeled JSONL.** Stream the source JSONL line by line. For each line, parse the
   JSON, rewrite `benchmark` to `Mind2Web` if `task_id` starts with `m2w_`, rewrite to `HumanEval`
   if `task_id` starts with `he_`, and leave it unchanged otherwise. Write each row as a single-line
   JSON object using `json.dumps(row, ensure_ascii=False, separators=(",", ": "))` — match the
   source's serialization style exactly so the diff stays clean. Confirm the output counts: 40
   FrontierScience-Olympiad, 26 Mind2Web, 23 SWE-bench Verified, 26 HumanEval. Save to
   `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/files/hierarchical_annotation_v2_relabeled.jsonl`.
   Satisfies REQ-1, REQ-2, REQ-8.

5. **Write the replacement asset's `details.json`.** Create
   `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/details.json`
   following the dataset asset spec v2: `dataset_id` = `hierarchical-annotation-v2-relabeled`,
   `description_path` = `description.md`, `files` lists the new JSONL only (path
   `files/hierarchical_annotation_v2_relabeled.jsonl`), `added_by_task` =
   `t0015_correct_proxy_benchmark_labels`. Mirror the source asset's authors, license, access_kind,
   and categories. Update `short_description` and `size_description` to use `Mind2Web` and
   `HumanEval` instead of `WorkArena++` and `tau-bench`. Satisfies REQ-4.

6. **Write the correction overlay file.** Create
   `tasks/t0015_correct_proxy_benchmark_labels/corrections/dataset_hierarchical-annotation-v2.json`:
   * `spec_version`: `"3"`
   * `correction_id`: `C-0015-01`
   * `correcting_task`: `t0015_correct_proxy_benchmark_labels`
   * `target_task`: `t0009_hierarchical_annotation_v2`
   * `target_kind`: `dataset`
   * `target_id`: `hierarchical-annotation-v2`
   * `action`: `update`
   * `changes`: object overriding `short_description`, `size_description` (these contain the wrong
     proxy names in the source), and `files` (rewrite the single file entry's `path` to point at the
     relabeled JSONL).
   * `file_changes`:
     * `description.md` → `replace` from
       `(t0015_correct_proxy_benchmark_labels, hierarchical-annotation-v2-relabeled, description.md)`.
     * `files/hierarchical_annotation_v2.jsonl` → `replace` from
       `(t0015_correct_proxy_benchmark_labels, hierarchical-annotation-v2-relabeled, files/hierarchical_annotation_v2_relabeled.jsonl)`.
   * `rationale`: a one-paragraph explanation citing [t0003] (where Mind2Web and HumanEval were
     selected as drop-in proxies for the gated WorkArena++ and tau-bench splits) and [t0005] (where
     the proxy slices were used verbatim in v1 annotation, propagating the mislabel into v2).
     Satisfies REQ-3, REQ-4, REQ-5.

7. **Verify and materialize.** Run the verificator and aggregator inside `run_with_logs`:
   * `uv run python -m arf.scripts.verificators.verify_corrections t0015_correct_proxy_benchmark_labels`
     — expected: PASSED, no errors.
   * `uv run python -m arf.scripts.aggregators.aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json`
     — expected: the materialized record's `description_path` resolves through the overlay to this
     task's relabeled `description.md`; the materialized `files[].path` resolves to the relabeled
     JSONL.
   * Stream the effective JSONL through Python and re-count benchmarks — expected: 40 / 23 / 26 / 26
     split across `FrontierScience-Olympiad`, `SWE-bench Verified`, `Mind2Web`, `HumanEval`.
     Satisfies REQ-6, REQ-7.

## Remote Machines

None required. The entire task is local Python, JSON file authoring, and verificator runs. Nothing
depends on a GPU.

## Assets Needed

* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/details.json` —
  source metadata.
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/description.md`
  — source description prose.
* `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
  — 115 rows of source data.
* `arf/specifications/corrections_specification.md` v3 — correction file format.
* `meta/asset_types/dataset/specification.md` v2 — replacement dataset asset format.

No external data, no API keys, no project libraries.

## Expected Assets

`task.json` `expected_assets` is `{}` — this task does not register a new asset in the project-level
catalog. The replacement asset under
`tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/`
exists only to provide replacement files for the overlay; the aggregator will not advertise it as a
separate dataset because the overlay redirects the existing `hierarchical-annotation-v2` ID to those
files.

## Time Estimation

* Step 1 (verify counts): 2 minutes.
* Steps 2-5 (write replacement files): 15 minutes.
* Step 6 (write correction file): 5 minutes.
* Step 7 (verify and materialize): 5 minutes.
* Buffer for flowmark / mypy / commits: 10 minutes.

Total wall-clock for implementation: ~40 minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Verificator rejects the replacement dataset asset because the relabeled folder is incomplete | Medium | Blocks `verify_corrections` (which checks that referenced files exist) | Author `details.json`, `description.md`, and `files/...jsonl` together; do not commit a partial asset. |
| JSONL serialization style differs from the source, producing a noisy diff | Medium | Reviewers cannot easily see what changed | Use `json.dumps(..., separators=(",", ": "))` and explicitly verify a non-relabeled row is byte-identical between input and output before committing. |
| `file_changes` `replacement_path` mismatch (path in correction file differs from path actually present in this task's asset) | Medium | `verify_corrections` fails | Copy the path strings used in `details.json` `files` directly into the correction file; do not retype them. |
| Aggregator caches the original output and does not pick up the overlay | Low | Materialized output stale | The dataset aggregator does not cache; every run resolves overlays fresh. Confirmed in `meta/asset_types/dataset/aggregator.py`. |
| t0012 (in_progress, parallel) merges before this task and ships a results file using the old labels | Low | Stale results in t0012 | t0012's per-benchmark numbers are aggregator-driven; they will pick up the overlay on its next read. If t0012 ships first, file a follow-up correction against its results in a future task. |
| Hidden mention of the proxy benchmark names somewhere outside the two replaced files (e.g., a sibling document in the asset folder) | Low | Inconsistent prose downstream | Inspection of t0009's asset folder shows only `details.json`, `description.md`, and the JSONL; nothing else is exposed by the aggregator. |

## Verification Criteria

* `uv run python -m arf.scripts.verificators.verify_corrections t0015_correct_proxy_benchmark_labels`
  — exit 0, no errors, no warnings. Confirms file existence, target-task validity, action semantics,
  and `file_changes` replacement-path validity.
* `uv run python -m arf.scripts.aggregators.aggregate_datasets --ids hierarchical-annotation-v2 --detail full --format json`
  — `short_description` and `size_description` no longer contain the strings `WorkArena++` or
  `tau-bench`; `files[0].path` resolves through the overlay to a path under
  `tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/`.
* Loading the effective JSONL with Python and grouping by `benchmark` returns:
  `{"FrontierScience-Olympiad": 40, "SWE-bench Verified": 23, "Mind2Web": 26, "HumanEval": 26}`.
* Diff between source and relabeled JSONL: exactly 52 rows differ, every diff is in the `benchmark`
  field, no row's `_pilot_row_index` or `task_id` changes. Confirms REQ-8.
* The repository contains no edits under `tasks/t0009_hierarchical_annotation_v2/`. Run
  `git diff main..HEAD -- tasks/t0009_hierarchical_annotation_v2/` and expect no output.
