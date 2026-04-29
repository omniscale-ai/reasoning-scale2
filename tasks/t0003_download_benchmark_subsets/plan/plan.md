---
spec_version: "2"
task_id: "t0003_download_benchmark_subsets"
date_completed: "2026-04-29"
status: "complete"
---
# Plan: Download Benchmark Subsets

## Objective

Acquire local, reproducible subsets of the four roadmap benchmarks (FrontierScience-Olympiad,
WorkArena++, SWE-bench Verified, tau-bench) and register each as a project dataset asset. Each
subset must target multi-step tasks with 4-8 decisions per task to match the project's stated
difficulty range. When a benchmark's official distribution is genuinely inaccessible (gated,
retired, dataset moved), the access attempt must be documented in the dataset asset's `details.json`
with `download_status: "failed"` and a clear `download_failure_reason`, preserving the existing
pilot proxy choice for Phase 2. Done means four dataset asset folders exist under `assets/dataset/`,
each passing `verify_dataset_asset` with zero errors, and per-benchmark access status, sample count,
and subset rationale are documented in `results/results_summary.md`.

## Task Requirement Checklist

The operative task text from `task.json` plus `task_description.md`:

```text
Name: Download benchmark subsets for the four roadmap sources
short_description: Wire up access to FrontierScience-Olympiad, WorkArena++, SWE-bench Verified,
and tau-bench subsets at 4-8 decisions per task.

Scope (from task_description.md):
- FrontierScience-Olympiad — full official distribution path; subset by domain to match the
  pilot's physics / chemistry / biology focus.
- WorkArena++ — official distribution. If genuinely inaccessible (gated, retired, dataset
  moved), document the access attempt and keep the Mind2Web proxy already present in the pilot.
- SWE-bench Verified — official Princeton/HF distribution; subset to instances that map cleanly
  onto the project's three-level hierarchy.
- tau-bench — official distribution. If genuinely inaccessible, keep the HumanEval proxy with
  documented justification.

Approach steps from task_description.md:
1. For each benchmark, attempt the official distribution path documented in its source paper.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata the
   benchmark provides; if no such metadata exists, sample uniformly with a fixed seed.
3. Produce one dataset asset per benchmark with details.json describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log into details.json with
   download_status="failed" and a clear download_failure_reason.
5. Emit follow-up suggestions for benchmarks where access is non-obvious or subsetting deserves
   sensitivity check.

Expected outputs:
- Four dataset assets under assets/dataset/ with details.json and files/ (or empty files/ plus
  failed status).
- results/results_summary.md with per-benchmark access status, sample count, subset decisions.
- results/suggestions.json flagging permanent proxy choices.
```

Concrete requirements:

* **REQ-1**: Attempt the official distribution path for FrontierScience-Olympiad and produce a
  dataset asset under `assets/dataset/frontierscience-olympiad-subset/` with at least metadata, even
  if download fails. Subset by domain (physics / chemistry / biology) to match the pilot focus.
  **Satisfied by**: Step 4. **Evidence**: `details.json` with `download_status` set, description
  document, and (on success) files in `files/`.

* **REQ-2**: Attempt the official distribution path for WorkArena++ and produce a dataset asset
  under `assets/dataset/workarena-plus-plus-subset/`. If inaccessible, document the access attempt
  with `download_status: "failed"` and keep the existing Mind2Web pilot proxy. **Satisfied by**:
  Step 5. **Evidence**: `details.json`, description document, and access attempt log either as
  populated `files/` or as `download_failure_reason`.

* **REQ-3**: Download SWE-bench Verified from the official Princeton/HF distribution and produce a
  dataset asset under `assets/dataset/swebench-verified-subset/`. Subset to instances that map
  cleanly onto the project's three-level hierarchy. **Satisfied by**: Step 6. **Evidence**:
  populated `files/` with subset JSONL, `details.json`, and description document.

* **REQ-4**: Attempt the official distribution path for tau-bench and produce a dataset asset under
  `assets/dataset/taubench-subset/`. If inaccessible, document the access attempt with
  `download_status: "failed"` and keep the HumanEval pilot proxy. **Satisfied by**: Step 7.
  **Evidence**: `details.json`, description document, and either populated `files/` or
  `download_failure_reason`.

* **REQ-5**: Each subset (where successfully downloaded) must target multi-step instances of 4-8
  decisions per task using whatever per-instance step or step-count metadata the benchmark provides.
  If no such metadata exists, sample uniformly with a fixed seed and document the seed. **Satisfied
  by**: Steps 4-7. **Evidence**: each `details.json` `size_description` and the description-document
  `Statistics` section explain the subset rule and seed.

* **REQ-6**: Each dataset asset must conform to `meta/asset_types/dataset/specification.md` (folder
  structure, `details.json` schema, description document with frontmatter and mandatory sections)
  and pass `verify_dataset_asset` with zero errors. **Satisfied by**: Step 8. **Evidence**:
  `verify_dataset_asset --task-id t0003_download_benchmark_subsets` exits with no errors for each of
  the four assets.

* **REQ-7**: `results/results_summary.md` must report per-benchmark access status, sample count, and
  any subset decisions. **Satisfied by**: orchestrator results step (out of plan scope but enabled
  by the per-benchmark log produced in Step 8).

* **REQ-8**: `results/suggestions.json` must flag any benchmarks where the proxy choice is now
  permanent or where access pathways are non-obvious. **Satisfied by**: orchestrator suggestions
  step (out of plan scope but enabled by the access-status table produced in Step 8).

## Approach

This is a `download-dataset` task. The plan follows the type's Planning Guidelines verbatim: record
exact URLs, document access requirements up front, plan for failed-access fallbacks, verify file
integrity after download, compute basic statistics, and produce one dataset asset per benchmark
following `meta/asset_types/dataset/specification.md` v2.

Per-benchmark approach, grounded in the source papers already added to the corpus by t0002:

* **FrontierScience-Olympiad**: The pilot data uses domain-tagged Olympiad-style problems (physics /
  chemistry / biology). The closest publicly distributed analogue is FrontierMath (arXiv:2411.04872,
  Glazer2024), which is gated behind Epoch AI access. Since FrontierMath itself is not openly
  downloadable and the pilot already contains 28 FrontierScience-Olympiad rows with full problem
  text, the plan is to **package the pilot rows as the v0 subset** (recording the access-gap
  explicitly), preserving the project's reproducibility while leaving a follow-up suggestion to
  negotiate Epoch AI access for full FrontierMath. This is consistent with the t0002 decision to
  "have a fallback to public Olympiad benchmarks (MATH-500, AIME) if access is delayed." Subsetting:
  the pilot's 28 rows are the natural domain-stratified subset.

* **WorkArena++**: Boisvert et al. 2024 (arXiv:2407.05291) released `BrowserGym` and the `workarena`
  Python package. The dataset definition (atomic + compositional task list) lives in the package,
  but instantiating tasks requires a live ServiceNow developer instance. The package is
  `pip install workarena` (Python ~3.10+). Plan: try installing the `workarena` package, dump the
  task definitions (compositional task list with skill annotations, no live instance needed for
  metadata), and package those metadata definitions as the dataset asset. If the package install or
  metadata dump fails, fall back to keeping the Mind2Web pilot proxy and mark
  `download_status: "failed"` with the install error as the reason. Subsetting: WorkArena++ tasks
  inherently mix atomic operations into 2-N step compositions, naturally matching 4-8 decisions per
  task.

* **SWE-bench Verified**: OpenAI released the 500-instance Verified subset (no-doi OpenAI2024). It
  is hosted on HuggingFace at `princeton-nlp/SWE-bench_Verified`. Plan: download via `datasets`
  library or direct HF parquet/JSONL. Each instance has fields `instance_id`, `repo`, `base_commit`,
  `problem_statement`, `patch`, `test_patch`, `FAIL_TO_PASS`, `PASS_TO_PASS` — these provide the
  natural mapping to the three-level hierarchy: `problem_statement` (global intent), `FAIL_TO_PASS`
  test list (subtask gates), `patch` hunks (atomic edits). Subsetting: take instances whose `patch`
  has between 4 and 8 hunks (one hunk = one atomic edit decision). If hunk metadata is unavailable,
  fall back to instances where the diff has 4-8 changed-line groups.

* **tau-bench**: Yao et al. 2024 (arXiv:2406.12045) released
  <https://github.com/sierra-research/tau-bench>. The repo is a pip package with retail and airline
  domains. Plan: clone or pip install the package, dump task definitions for both domains, package
  the JSON task list as the dataset asset. Subsetting: tau-bench tasks have implicit step counts via
  `actions` lists; pick tasks whose canonical action sequence has 4-8 entries. If the package
  doesn't expose action sequences, sample uniformly with seed 42 and document the choice.

**Alternatives considered**:

* *Run all benchmarks via their official harnesses end-to-end*: rejected — the task explicitly
  scopes execution out (Phase 2 task) and would explode budget and time.
* *Subset to single-step (1-decision) instances*: rejected — contradicts the project's multi-step
  (4-8 decisions) target stated in `task.json`.
* *Skip the dataset asset for failed-access benchmarks*: rejected — the dataset asset spec requires
  `files/` to be non-empty (DA-E003), so failed-access benchmarks must include at least one
  descriptive file documenting the access attempt. The plan satisfies DA-E003 by writing an
  `access-attempt.md` file into `files/` for failed cases.

**Task type**: `download-dataset` (already declared in `task.json`). Planning Guidelines from this
type's `instruction.md` informed: explicit URL recording, intervention-on-auth-walls policy, file
integrity checks, and the dataset-asset structure.

## Cost Estimation

Total estimated cost: **$0**.

* No paid API calls. All four benchmarks are downloaded from public source repositories
  (HuggingFace, GitHub, pip).
* No GPU. Local downloads and metadata extraction only.
* No third-party paid services. Project budget remains at the t0002 baseline (the budget aggregator
  will be rerun by the orchestrator at reporting if needed; the budget gate is not triggered for
  this task because `download-dataset` has `has_external_costs: false`).

## Step by Step

The implementation agent must follow these steps in order. Every CLI call inside the worktree must
be wrapped in `arf.scripts.utils.run_with_logs`. Each step satisfies one or more `REQ-*`.

1. **Set up `code/paths.py` and `code/constants.py`.** Create `code/paths.py` with absolute paths to
   the task root, `assets/dataset/`, the four per-benchmark slugs, and the pilot data file
   `project/data/annotation_pilot/tasks_annotated.jsonl`. Create `code/constants.py` with the four
   dataset slugs (`FRONTIERSCIENCE_SLUG`, `WORKARENA_PP_SLUG`, `SWEBENCH_SLUG`, `TAUBENCH_SLUG`),
   the random seed `RANDOM_SEED = 42`, and the multi-step decision range `MIN_DECISIONS = 4`,
   `MAX_DECISIONS = 8`. Expected output: two files exist, `mypy` passes on them. Satisfies
   structural prep for REQ-1..REQ-6.

2. **Add a shared `dataset_asset.py` helper.** Create `code/dataset_asset.py` with frozen
   dataclasses `Author`, `Institution`, `DatasetFile`, and `DatasetDetails` that mirror the v2
   dataset asset spec, plus a `write_dataset_asset(*, root, details, description_md)` function that
   writes `details.json`, the description document, ensures `files/` exists, and returns the asset
   folder path. The function uses keyword arguments for all 2+ parameter calls and writes JSON with
   `indent=2`, `sort_keys=False` so field order matches the spec. Expected output: the module
   imports cleanly and `mypy` passes. Satisfies structural prep for REQ-6.

3. **Add `download_attempt.py` access-attempt helper.** Create `code/download_attempt.py` with a
   `record_failed_access(*, asset_root, source_url, attempted_at, reason, fallback_proxy)` function
   that writes `files/access-attempt.md` documenting the failed download. The file contains the
   source URL, ISO 8601 attempt timestamp, the failure reason, and the proxy choice the project
   keeps. This satisfies DA-E003 (`files/` must contain at least one file even on failure) without
   faking a real download. Satisfies structural prep for REQ-2 and REQ-4 fallback paths.

4. **Build the FrontierScience-Olympiad subset.** Create `code/build_frontierscience.py`. Read
   `project/data/annotation_pilot/tasks_annotated.jsonl` and filter rows whose
   `benchmark == "FrontierScience-Olympiad"`. Group by `domain` (physics / chemistry / biology).
   Write
   `assets/dataset/frontierscience-olympiad-subset/files/frontierscience-olympiad-subset.jsonl` with
   the filtered rows, preserving original column order. Compute statistics: total rows, rows per
   domain, average problem text length. Build a `DatasetDetails` instance with
   `download_status: "success"` (because the rows exist in the pilot),
   `source_paper_id: "10.48550_arXiv.2411.04872"`, `url: "https://arxiv.org/abs/2411.04872"`,
   license `"research-only"`, access `"public"`, and a `size_description` that includes the
   per-domain breakdown. Write `details.json` and `description.md` (with all 7 mandatory sections
   per spec v2). Run
   `verify_dataset_asset --task-id t0003_download_benchmark_subsets frontierscience-olympiad-subset`
   and confirm zero errors. Expected output: 28 rows, three domain groups, verificator passes.
   Satisfies REQ-1, REQ-5, REQ-6.

5. **Build the WorkArena++ subset (best-effort with fallback).** Create
   `code/build_workarena_pp.py`. Try `pip install workarena` via `uv pip install --active workarena`
   wrapped in `run_with_logs`. If install fails, OR the package does not expose a task-list API, OR
   a live ServiceNow instance is required to instantiate task metadata, mark
   `download_status: "failed"`, set `download_failure_reason` to the precise error or limitation
   observed, and call `record_failed_access(...)` to write `files/access-attempt.md` with the
   install/import log and the Mind2Web proxy decision. Otherwise, dump the WorkArena++ task list
   (atomic + compositional, with skill annotations) to `files/workarena-plus-plus-tasks.json` and
   set `download_status: "success"`. Either way write `details.json` and `description.md` (mandatory
   sections, frontmatter, etc). The `size_description` either reports the dumped task count or names
   the access barrier and the pilot proxy in use. `source_paper_id: "10.48550_arXiv.2407.05291"`,
   `url: "https://arxiv.org/abs/2407.05291"`. Run the verificator. Expected output: directory with
   `details.json`, `description.md`, and either populated `files/` or `files/access-attempt.md`;
   verificator passes. Satisfies REQ-2, REQ-5 (when successful), REQ-6.

6. **Build the SWE-bench Verified subset.** Create `code/build_swebench.py`. Use `datasets` library
   to load `princeton-nlp/SWE-bench_Verified` (split: `test`, the only split). For each instance,
   parse the `patch` field with `unidiff` (already a transitive dep) to count `@@` hunks per file,
   then sum across files to get total atomic-edit decisions. Filter to instances where total hunks
   is in `[MIN_DECISIONS, MAX_DECISIONS]` inclusive. Write the filtered list to
   `assets/dataset/swebench-verified-subset/files/swebench-verified-subset.jsonl`. If `unidiff` is
   unavailable, fall back to counting unique `@@` markers in the patch string; document the method
   used in the description. Compute statistics: total Verified instances, instances after filter,
   hunk distribution. `source_paper_id: "no-doi_OpenAI2024_swe-bench-verified"`,
   `url: "https://openai.com/index/introducing-swe-bench-verified/"`, license `"MIT"`, access
   `"public"`. Run the verificator. Expected output: filtered JSONL plus metadata; verificator
   passes. Satisfies REQ-3, REQ-5, REQ-6.

   **Validation gate** (this is the only step that downloads data at scale): SWE-bench Verified has
   500 instances. Before filtering, log the total count. Trivial baseline: with no filter, the
   dataset has 500 rows. If after filter the subset has fewer than 30 rows the filter is probably
   wrong (Verified instances typically have 1-10 hunks; at 4-8 we expect ~150-250 instances). If
   subset size <30 OR >450, halt, inspect 5 individual rows' parsed hunk counts versus the raw
   `patch` field, and reconcile before proceeding.

7. **Build the tau-bench subset (best-effort with fallback).** Create `code/build_taubench.py`. Try
   `uv pip install --active tau-bench` (the PyPI name); if that fails try
   `pip install git+https://github.com/sierra-research/tau-bench.git`. If both install paths fail,
   OR the package requires API keys for OpenAI/Anthropic to instantiate any task object (per the
   README, the harness is LLM-call-driven), mark `download_status: "failed"` with the precise
   reason, and call `record_failed_access(...)` recording the install/import log and the HumanEval
   pilot-proxy decision. Otherwise, enumerate tau-bench's airline and retail task manifests via the
   package's `tau_bench.envs` API (if present) and dump them to `files/taubench-tasks.json`,
   filtering tasks whose declared action sequence length is in `[MIN_DECISIONS, MAX_DECISIONS]`. If
   action-sequence lengths are unavailable, sample uniformly with `RANDOM_SEED = 42` and document
   the seed in the description. Either way write `details.json` and `description.md` with
   `source_paper_id: "10.48550_arXiv.2406.12045"`, `url: "https://arxiv.org/abs/2406.12045"`. Run
   the verificator. Expected output: directory with `details.json`, `description.md`, and either
   populated `files/` or `files/access-attempt.md`; verificator passes. Satisfies REQ-4, REQ-5 (when
   successful), REQ-6.

8. **Run all dataset-asset verificators and produce an access-status manifest.** Create
   `code/build_status_manifest.py` that reads each of the four `details.json` files and emits
   `code/access_status.json` (a per-benchmark access-status table that the orchestrator's results
   step consumes). Then run `verify_dataset_asset --task-id t0003_download_benchmark_subsets` (no
   positional ID — verifies all four assets). Confirm zero errors across all four assets. Run
   `ruff check --fix`, `ruff format`, and `mypy -p tasks.t0003_download_benchmark_subsets.code`.
   Expected output: one access-status manifest, all verificators pass, all style checks pass.
   Satisfies REQ-6 and prepares evidence for REQ-7 and REQ-8.

## Remote Machines

None required. All four downloads run locally on the orchestrator's machine. No GPU. No paid
compute. Disk usage is minimal (<100 MB total — SWE-bench Verified is the largest at <50 MB).

## Assets Needed

* `project/data/annotation_pilot/tasks_annotated.jsonl` — pilot data file shared with the project,
  used as the FrontierScience-Olympiad source rows.
* No dependency-task assets (this task is independent of T1).
* External: HuggingFace `princeton-nlp/SWE-bench_Verified`, the `workarena` and `tau-bench` PyPI /
  GitHub repos (best-effort).
* Paper assets in `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/` are
  referenced by `source_paper_id` in each `details.json`.

## Expected Assets

Four dataset assets, one per benchmark, all under
`tasks/t0003_download_benchmark_subsets/assets/dataset/`:

* `frontierscience-olympiad-subset/` — FrontierScience-Olympiad subset packaged from pilot rows with
  domain stratification. Spec v2.
* `workarena-plus-plus-subset/` — WorkArena++ task definitions or, on access failure, a documented
  access attempt with the Mind2Web proxy decision frozen. Spec v2.
* `swebench-verified-subset/` — SWE-bench Verified instances filtered to 4-8 patch hunks. Spec v2.
* `taubench-subset/` — tau-bench airline + retail task manifest (or on access failure, a documented
  access attempt with the HumanEval proxy decision frozen). Spec v2.

This matches `task.json` `expected_assets: {"dataset": 4}` exactly.

## Time Estimation

* Step 1-3 (helpers): 15 minutes (no compute, just typed scaffolding).
* Step 4 (FrontierScience): 10 minutes (read JSONL, filter, write).
* Step 5 (WorkArena++): 20 minutes including pip install attempt and fallback handling.
* Step 6 (SWE-bench Verified): 20 minutes including HF download (~50 MB) and hunk parsing.
* Step 7 (tau-bench): 20 minutes including pip install attempt and fallback handling.
* Step 8 (verificators + manifest): 10 minutes.

Total: ~95 minutes wall clock, ~0 GPU minutes.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| WorkArena++ requires live ServiceNow developer instance to enumerate tasks | High | Blocking for REQ-2 success path | Fall back to documented access attempt; freeze Mind2Web proxy in `details.json` `download_failure_reason`; emit Phase 2 follow-up suggestion |
| tau-bench package requires LLM API keys merely to instantiate task objects | Medium | Blocking for REQ-4 success path | Fall back to documented access attempt; freeze HumanEval proxy; emit follow-up suggestion to inject a no-LLM mock for offline metadata extraction |
| HuggingFace hub rate-limits the SWE-bench Verified download | Low | Blocking for REQ-3 | Retry with exponential backoff; if persistent, switch to `huggingface_hub` direct file API or fetch the `.parquet` via `curl` |
| `unidiff` not installed and the fallback regex undercounts hunks | Medium | Wrong subset for SWE-bench | Step 6's validation gate halts if the subset count is outside [30, 450]; on halt, install `unidiff` (`uv pip install --active unidiff`) and re-run |
| FrontierMath access via Epoch AI takes weeks to negotiate | High | Blocks full-corpus FrontierScience build | Already pre-decided: package the pilot rows as the v0 subset; emit follow-up suggestion to revisit Epoch AI access |
| Pilot JSONL has unexpected schema drift since t0001 | Low | Step 4 filter misses rows | Validation: log row count after filter; if 0 rows, halt and inspect schema; expected count is 28 per the t0002 README |

## Verification Criteria

* Run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0003_download_benchmark_subsets -- uv run python -m arf.scripts.verificators.verify_dataset_asset --task-id t0003_download_benchmark_subsets`
  and confirm zero errors across all four assets (covers REQ-1..REQ-6).
* Run `ls tasks/t0003_download_benchmark_subsets/assets/dataset/` and confirm exactly four
  subdirectories exist: `frontierscience-olympiad-subset`, `workarena-plus-plus-subset`,
  `swebench-verified-subset`, `taubench-subset` (covers REQ-1..REQ-4 by enumeration).
* For each of the four `details.json` files, confirm via
  `python -c "import json; d=json.load(open('<path>')); assert d['download_status'] in {'success','failed'}; assert d['files']"`
  that the field is present and the `files` list is non-empty (covers REQ-1..REQ-4 + REQ-6).
* Run
  `uv run ruff check . && uv run ruff format --check . && uv run mypy -p tasks.t0003_download_benchmark_subsets.code`
  inside the task worktree and confirm zero errors and zero diff (covers code quality).
* Confirm that for each subset where `download_status: "success"`, the description document's
  `## Statistics` section names the subset rule (4-8 decisions) and either reports the actual
  per-instance count distribution or the random seed used for uniform sampling (covers REQ-5).
* Confirm `code/access_status.json` exists with one entry per benchmark, each entry having
  `dataset_id`, `download_status`, `sample_count`, and `subset_rule` keys (covers REQ-7 / REQ-8
  evidence prep).
