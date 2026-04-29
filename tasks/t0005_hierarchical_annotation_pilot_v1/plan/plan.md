---
spec_version: "2"
task_id: "t0005_hierarchical_annotation_pilot_v1"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Hierarchical Annotation Pilot v1

## Objective

Audit the 115 LLM-annotated rows in `project/data/annotation_pilot/tasks_annotated.jsonl`,
deterministically project each row's `steps.nodes` graph onto the project's three-level global /
subtask / atomic schema, run an LLM-as-judge spot-check on a stratified sample of at least 12 rows
(>=3 per benchmark) using `claude-haiku-4-5-20251001`, and produce one consolidated
`hierarchical-annotation-v1` dataset asset under `assets/dataset/hierarchical-annotation-v1/`.
"Done" means the dataset asset exists, passes `verify_dataset_asset`, contains exactly 115 rows, and
`results/results_summary.md` reports per-benchmark hierarchy completeness and judge accept rate.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md` (verbatim):

> Audit and conform the 115 existing pilot annotations to the global/subtask/atomic schema; produce
> one dataset asset.
>
> Scope:
>
> * Read `project/data/annotation_pilot/tasks_annotated.jsonl` and inspect the `steps` field on each
>   row to determine whether it carries explicit global / subtask / atomic granularity labels or
>   whether the granularity must be inferred.
> * If labels are missing, write a deterministic mapper that derives the three-level structure from
>   the existing `steps` and adds an explicit `hierarchy: {global, subtask, atomic}` block per row.
> * Run an LLM-as-judge spot-check on at least 10% of rows (>=12 rows) to estimate hierarchy
>   quality. Use `claude-haiku-4-5-20251001` for the judge to keep cost low.
> * Produce one consolidated `dataset` asset under `assets/dataset/hierarchical_annotation_v1/` with
>   rows of shape
>   `{task_id, benchmark, difficulty, problem, hierarchy, gold_actions, annotation_model, judge_verdict, judge_notes}`.
>
> Expected outputs: dataset asset, results files, follow-up suggestions.

Concrete requirements:

* **REQ-1**: Inspect every row of `tasks_annotated.jsonl` and determine whether `steps` carries
  explicit hierarchy labels. Document the finding in `results/results_detailed.md`. Satisfied by
  Step 1.
* **REQ-2**: Implement a deterministic mapper that consumes `steps.nodes` and emits a
  `{global, subtask, atomic}` triple per row. Code in `code/hierarchy_mapper.py`. Satisfied by Step
  2\.
* **REQ-3**: Implement an LLM-as-judge runner that calls `claude-haiku-4-5-20251001` with a
  verbalized-confidence prompt and parses a strict JSON verdict. Code in `code/judge_runner.py`.
  Satisfied by Step 3.
* **REQ-4**: Stratify the judge sample at >=3 rows per benchmark (>=12 rows total). Satisfied by
  Step 4.
* **REQ-5**: Produce a single `hierarchical-annotation-v1` dataset asset with `details.json`,
  `description.md`, and `files/hierarchical_annotation_v1.jsonl` containing exactly 115 rows of
  shape
  `{task_id, benchmark, difficulty, problem, hierarchy: {global, subtask, atomic}, gold_actions: {global, subtask, atomic}, annotation_model, judge_verdict, judge_notes}`.
  Satisfied by Steps 2-5.
* **REQ-6**: Per-benchmark hierarchy-completeness rate, per-domain counts, and judge accept rate
  reported in `results/results_detailed.md`. Satisfied by Step 6.
* **REQ-7**: `results/metrics.json` reports the registered `avg_decisions_per_task` metric.
  Satisfied by Step 6. Note: results writing itself is the orchestrator's `results` step, not an
  implementation step — implementation only ensures the metric is computed and emitted to a JSON
  artifact in `code/` outputs.
* **REQ-8**: Cost capped at $5; expected actual under $0.50. Satisfied by the budget-gate code in
  `code/judge_runner.py`.
* **REQ-9**: Dataset asset passes `verify_dataset_asset` with zero errors. Satisfied by Step 5.

Ambiguity: the task description names the four benchmarks as
`FrontierScience-Olympiad, SWE-bench Verified, HumanEval-proxy, Mind2Web-proxy`, but the actual
imported file uses tau-bench and WorkArena++ as the two web/agent proxies. The plan treats tau-bench
and WorkArena++ as the proxies (per the actual data) and calls this discrepancy out in
`results_detailed.md` with a follow-up suggestion to remediate the proxy naming in v2.

## Approach

The approach is a deterministic projection followed by a sample-based LLM audit. The research
finding from `research/research_papers.md` is that the existing 115 rows already carry per-node
`type` labels (`strategic`, `conceptual`, `computational`, `verification`) that map nearly
one-to-one onto the project's three levels. So no LLM call is needed for the mapping itself — a
pure-Python function over the node graph suffices and is reproducible. For the audit we adopt the
verbalized-confidence pattern from Xiong2023: a single decoding pass per sampled row asking for a
JSON `{"verdict": "...", "justification": "..."}` output.

Mapper rules:

* `global`: the node text from the lowest-id `strategic` node. If no strategic node exists, the
  first node in the graph (or `null` if the graph is empty). Prepend the row's `problem`'s first
  sentence to provide intent context.
* `subtask`: the list of `conceptual`-typed node labels. If empty, fall back to all `strategic`
  nodes beyond the first.
* `atomic`: the list of `computational` and `verification` node labels concatenated in id order.

`gold_actions` mirrors `hierarchy` but uses each node's `detail` field rather than `label` to
preserve the action description.

Rows where `steps` is `null` (annotation-failure rows) get `hierarchy.global = null`,
`hierarchy.subtask = []`, `hierarchy.atomic = []`, and `hierarchy_completeness = false`. They are
preserved in the output to keep the row count at 115 — downstream tasks can re-annotate these.

Alternatives considered:

* **LLM-driven re-annotation of every row**: rejected because it would cost roughly 115 * 5K input
  tokens * $1/Mtok input ≈ $0.60 plus output cost, with no scientific gain over the deterministic
  mapping (the existing `type` labels were produced by a strong LLM and are already calibrated). The
  deterministic path is cheaper, faster, and reproducible.

Task type: `hierarchical-annotation` (already set in `task.json`). The Planning Guidelines for this
type emphasise (a) producing a single dataset asset, (b) tracking judge accept rate per-benchmark,
and (c) limiting LLM cost. All three are reflected in the steps below.

## Cost Estimation

| Item | Estimate |
| --- | --- |
| `claude-haiku-4-5-20251001` judge calls (12 rows, ~3K input + ~150 output tokens each) | $0.06 |
| Buffer for retries / extra rows | $0.20 |
| **Total expected** | **~$0.30** |
| **Hard cap (REQ-8)** | **$5.00** |

Project budget is $100 total with $0 spent so far; per-task default cap is $10. This task is well
under both. No remote compute costs.

## Step by Step

1. **[CRITICAL] Inspect the pilot file and confirm the granularity-label state.** Write
   `code/inspect_pilot.py` that loads `project/data/annotation_pilot/tasks_annotated.jsonl`, prints
   per-benchmark counts, the keys present on each row, the node-type distribution across all
   `steps.nodes`, and the count of rows with `errors` or `steps == null`. Run it once. Expected
   output: 115 rows, four benchmarks (FrontierScience-Olympiad, SWE-bench Verified, tau-bench,
   WorkArena++), and the absence of any explicit `hierarchy` field on the input rows. Satisfies
   REQ-1.

2. **[CRITICAL] Implement the deterministic mapper.** Create `code/hierarchy_mapper.py` exporting
   `map_row(row: dict) -> dict` and `iter_mapped_rows(path: Path) -> Iterator[dict]`. The mapper
   produces the canonical row shape
   `{task_id, benchmark, difficulty, problem, hierarchy, gold_actions, annotation_model, judge_verdict, judge_notes, hierarchy_completeness}`.
   `judge_verdict` and `judge_notes` are initialised to `null`. Use the rules from the Approach
   section. Add a `paths.py` with `PILOT_INPUT`, `MAPPED_OUTPUT`, `JUDGE_OUTPUT`,
   `DATASET_ASSET_DIR`, `DATASET_FILES_DIR`, `DATASET_FILE_PATH`. Run the mapper end-to-end and
   write `code/_outputs/mapped.jsonl` (gitignored via being inside `code/_outputs/`, but actually
   since we cannot create gitignores in task folders, we keep this short-lived and avoid committing
   it; the canonical output is the dataset asset file). Satisfies REQ-2, REQ-5 (partial).

3. **[CRITICAL] Implement the LLM-as-judge runner.** Create `code/judge_runner.py` that uses the
   `anthropic` SDK with model `claude-haiku-4-5-20251001`. Prompt template (single-shot,
   verbalized-confidence per Xiong2023):

   ```text
   You are auditing a hierarchical decomposition of a benchmark task.
   Benchmark: {benchmark}
   Problem (truncated to 1500 chars): {problem_excerpt}
   Proposed hierarchy:
     global: {global}
     subtasks: {subtasks_joined}
     atomic actions: {atomic_joined}
   Question: Is this decomposition acceptable as a global / subtask / atomic
   labelling of the problem? Respond with strict JSON of the form
   {"verdict": "acceptable" | "needs revision",
    "justification": "<one sentence>"}.
   ```

   Parse the response with `json.loads`; on parse failure, retry once with a stricter system prompt
   and otherwise mark the row's `judge_verdict` as `null` and the notes as `"parse-failure"`. Record
   per-call input/output tokens to a costs sidecar file `code/_outputs/judge_costs.json`. Satisfies
   REQ-3.

4. **Stratify and run the judge sample.** Create `code/select_judge_sample.py` that consumes
   `code/_outputs/mapped.jsonl` and selects exactly 3 rows per benchmark (12 total). Within each
   benchmark, prefer rows with non-null `hierarchy.global` and a non-empty `atomic` list, and
   include at least one `hierarchy_completeness == false` row when one exists for that benchmark.
   Use random seed 42. Run the judge runner over the selected rows and persist verdicts back into
   the mapped rows, producing `code/_outputs/mapped_with_judge.jsonl`. Validation gate: do a trivial
   dry-run by calling the judge on the first selected row only first; if the response is not strict
   JSON, halt and inspect before processing the remaining 11. The trivial baseline is "0%
   acceptable" (judge always says "needs revision") — if observed accept rate is 0, halt and
   inspect. Satisfies REQ-3, REQ-4, REQ-8.

5. **[CRITICAL] Build the dataset asset.** Create `code/build_dataset_asset.py` that copies
   `code/_outputs/mapped_with_judge.jsonl` into
   `assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`, writes
   `details.json` per `meta/asset_types/dataset/specification.md` v2 (asset id
   `hierarchical-annotation-v1`, name "Hierarchical Annotation v1 (115-row pilot audit)", version
   "v1", license `inherited-per-row`, access_kind `restricted`, categories
   `[hierarchical-planning, benchmark-annotation, agent-evaluation]`, source_paper_id `null`,
   `description_path` "description.md"), and writes `description.md` with all six mandatory sections
   (Metadata, Overview, Content & Annotation, Statistics, Usage Notes, Main Ideas, Summary). Run
   `verify_dataset_asset` on the asset at the end. Expected: zero errors and at most a small number
   of warnings (e.g., DA-W005 if any category resolves missing — verify they all exist). Satisfies
   REQ-5, REQ-9.

6. **Compute summary statistics for results.** Create `code/compute_stats.py` that reads the final
   dataset file and emits `code/_outputs/stats.json` with: per-benchmark row counts, per-benchmark
   hierarchy-completeness rate, per-domain counts (using the `domain` field for
   FrontierScience-Olympiad rows), per-benchmark judge accept rate, and the project-wide mean
   `avg_decisions_per_task` (defined as the mean length of `gold_actions.atomic` across all 115
   rows). Also emit a per-benchmark bar chart `results/images/per_benchmark_completeness.png` and a
   hierarchy-size histogram `results/images/atomic_lengths.png` using matplotlib. The orchestrator's
   `results` step will consume `code/_outputs/stats.json` to populate `results_summary.md`,
   `results_detailed.md`, and `metrics.json`. Satisfies REQ-6, REQ-7.

## Remote Machines

None required. All work runs locally with the Anthropic API; the project venv has the `anthropic`
package via the `claude-api` dependency family.

## Assets Needed

* `project/data/annotation_pilot/tasks_annotated.jsonl` (115 rows; black-box utility input).
* `project/code/scripts/collect_and_annotate.py` and `project/code/src/` are referenced for context
  only and treated as black-box utilities; no imports from them.
* The four benchmark dataset assets in `tasks/t0003_download_benchmark_subsets/assets/dataset/` —
  referenced for license inheritance metadata in `details.json`.
* The 11 papers reviewed in `research/research_papers.md`.
* Anthropic API credentials via `OPENAI_API_KEY`-style env var resolution from `.env` (the Anthropic
  SDK reads `ANTHROPIC_API_KEY` automatically).

## Expected Assets

One `dataset` asset:

* `assets/dataset/hierarchical-annotation-v1/details.json` (v2 spec)
* `assets/dataset/hierarchical-annotation-v1/description.md` (six mandatory sections)
* `assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl` (115 rows)

Matches `task.json` `expected_assets.dataset = 1`.

## Time Estimation

* Implementation: ~30 min (mapper + judge + asset build).
* Judge run: ~3 min (12 API calls).
* Stats + charts: ~5 min.
* Verification + commit: ~5 min.
* Total: ~45 min wall-clock.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Judge JSON parse failure | Medium | One row marked null; minor data gap | Retry once with stricter system prompt; otherwise persist `parse-failure` and continue |
| Anthropic API outage / rate limit | Low | Step 4 blocks | Exponential backoff with `tenacity`; if persistent, halt step and emit intervention file |
| Mapper produces empty `subtask` list for many rows | Medium | Lower hierarchy-completeness rate; still valid v1 output | Document in `results_detailed.md`; the v1 spec accepts empty subtask lists when `conceptual` nodes are absent |
| Cost overrun beyond $5 cap | Very low | Budget breach | `judge_runner.py` checks running cost after every call and halts at $4.50 |
| Dataset id slug `hierarchical_annotation_v1` rejected by spec (no underscores) | High at first attempt | Block | Use canonical kebab-case slug `hierarchical-annotation-v1`; the JSONL filename keeps the readable underscore form per task description |
| Pilot file has unexpected schema variance not seen in the 5-row preview | Low | Mapper crash on row N | `map_row` wraps each row in try/except, logs offending row id, and emits a fallback row with `hierarchy_completeness=false` so the run still completes |

## Verification Criteria

* Run
  `uv run python -u -m arf.scripts.verificators.verify_dataset_asset --task-id t0005_hierarchical_annotation_pilot_v1 hierarchical-annotation-v1`.
  Expected: zero errors. Satisfies REQ-9.
* Run
  `wc -l tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl`.
  Expected: 115. Satisfies REQ-5.
* Run
  `python -c "import json; rows=[json.loads(l) for l in open('tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/files/hierarchical_annotation_v1.jsonl')]; assert all(set(['task_id','benchmark','difficulty','problem','hierarchy','gold_actions','annotation_model','judge_verdict','judge_notes']).issubset(r) for r in rows); print('schema ok')"`.
  Expected stdout: `schema ok`. Satisfies REQ-5.
* Run
  `cat tasks/t0005_hierarchical_annotation_pilot_v1/code/_outputs/stats.json | jq '.judge.accept_rate_overall'`.
  Expected: a float between 0 and 1. Satisfies REQ-4, REQ-6.
* Run `uv run ruff check tasks/t0005_hierarchical_annotation_pilot_v1/code/` and
  `uv run mypy -p tasks.t0005_hierarchical_annotation_pilot_v1.code`. Expected: zero errors.
* Confirm the four `REQ-*` items REQ-2, REQ-3, REQ-5, REQ-9 are visibly satisfied by inspection of
  the asset folder and the dataset asset's `description.md`.
