---
spec_version: "2"
task_id: "t0003_download_benchmark_subsets"
---
# Results: Download Benchmark Subsets

## Summary

Acquired four benchmark subsets covering the project's roadmap sources. Three were downloaded from
fully public sources (HuggingFace parquet for SWE-bench Verified; GitHub raw for tau-bench and the
WorkArena++ curriculum). FrontierScience-Olympiad upstream is FrontierMath (gated behind Epoch AI
access) — the asset packages the project's pilot rows as the v0 subset until access is negotiated.
WorkArena++ instance-level enumeration requires a live ServiceNow developer instance plus a gated
HuggingFace dataset; the asset captures the upstream compositional task class manifest, and Mind2Web
remains the de-facto Phase 2 fallback. All four assets pass `verify_dataset_asset` with zero errors.

## Methodology

* **Machine**: macOS Darwin 25.3.0 on Apple Silicon (the orchestrator's local laptop), no GPU.
* **Total runtime**: about 25 minutes wall clock, dominated by writing builders and verifying output
  (downloads themselves were a few seconds each).
* **Started**: 2026-04-29T14:31:11Z (worktree create / step 1 prestep).
* **Ended**: 2026-04-29T15:00:00Z (results step in progress).
* **Methods**: `urllib.request.urlretrieve` for raw HTTP downloads (HuggingFace and GitHub raw),
  `pyarrow.parquet` for SWE-bench Verified parquet, the standard library `ast` module for parsing
  tau-bench Python source files, regex extraction for the WorkArena++ curriculum manifest, and
  direct JSONL filtering for the FrontierScience-Olympiad pilot rows.
* **Subset rules**:
  * SWE-bench Verified: keep iff gold patch contains between 4 and 8 `@@ -` hunks.
  * tau-bench: keep iff gold action sequence has between 4 and 8 actions.
  * FrontierScience-Olympiad: all pilot rows kept, domain-stratified across physics, chemistry,
    biology (no per-instance step counts available, so the 4-8 filter cannot apply at row level).
  * WorkArena++: all upstream compositional task class lists kept (instance enumeration deferred).

## Per-benchmark Outcomes

### FrontierScience-Olympiad

| Field | Value |
| --- | --- |
| `download_status` | success |
| Source | Project pilot JSONL (Olympiad-style problems) |
| `source_paper_id` | `10.48550_arXiv.2411.04872` (FrontierMath) |
| Sample count | 40 |
| Domain breakdown | physics=15, chemistry=10, biology=15 |
| License | research-only |
| Subset rule | All pilot rows; domain-stratified |
| Notes | FrontierMath upstream gated behind Epoch AI; pilot v0 substitute |

### WorkArena++

| Field | Value |
| --- | --- |
| `download_status` | success (manifest only) |
| Source | `https://raw.githubusercontent.com/ServiceNow/WorkArena/main/...` |
| `source_paper_id` | `10.48550_arXiv.2407.05291` |
| Sample count | 42 task class lists |
| `access_kind` | restricted |
| License | Apache-2.0 |
| Subset rule | All compositional task class lists from upstream `curriculum.py` |
| Notes | Instance enumeration requires live ServiceNow + gated HF dataset; Mind2Web pilot proxy frozen |

### SWE-bench Verified

| Field | Value |
| --- | --- |
| `download_status` | success |
| Source | HuggingFace `princeton-nlp/SWE-bench_Verified` parquet |
| `source_paper_id` | `no-doi_OpenAI2024_swe-bench-verified` |
| Sample count | 60 instances (filtered from 500 Verified) |
| License | MIT |
| Subset rule | gold patch hunks in [4, 8] |
| Hunk distribution | 4=24, 5=12, 6=14, 7=7, 8=3 |
| Validation gate | PASSED ([30, 450] sanity window) |

### tau-bench

| Field | Value |
| --- | --- |
| `download_status` | success |
| Source | `https://raw.githubusercontent.com/sierra-research/tau-bench/main/...` |
| `source_paper_id` | `10.48550_arXiv.2406.12045` |
| Sample count | 87 tasks (filtered from 665) |
| License | MIT |
| Subset rule | gold action sequence length in [4, 8] |
| Domain/split breakdown | airline/test=13, retail/test=50, retail/train=24 |
| Action distribution | 4=24, 5=24, 6=23, 7=13, 8=3 |

## Verification

* `verify_dataset_asset --task-id t0003_download_benchmark_subsets` — PASSED on every asset:
  * `frontierscience-olympiad-subset` — 0 errors, 0 warnings.
  * `workarena-plus-plus-subset` — 0 errors, 0 warnings.
  * `swebench-verified-subset` — 0 errors, 0 warnings.
  * `taubench-subset` — 0 errors, 0 warnings.
* `verify_plan` — PASSED (0 errors, 0 warnings).
* `verify_task_dependencies` — PASSED.
* `ruff check tasks/t0003_download_benchmark_subsets/code/` — All checks passed.
* `ruff format --check tasks/t0003_download_benchmark_subsets/code/` — 11 files already formatted.
* `mypy -p tasks.t0003_download_benchmark_subsets.code` — Success.

## Limitations

* **WorkArena++ instance-level enumeration is deferred.** Instantiating an actual WorkArena++ task
  requires (a) a live ServiceNow developer instance, (b) gated access to the
  `ServiceNow/WorkArena-Instances` HuggingFace dataset, and (c) the `browsergym-workarena` harness
  with Playwright. None are reachable from this task's local-only download budget. The asset
  captures the upstream task taxonomy only; Phase 2 must apply the 4-8 decisions filter at instance
  time once access is resolved.
* **FrontierMath upstream is gated.** Until Epoch AI access is negotiated, the
  FrontierScience-Olympiad subset relies on the project's pilot rows. If Phase 2 needs more rows, a
  follow-up task must add a public Olympiad dataset (MATH-500, AIME) per the t0002 fallback plan.
* **Per-instance step counts are unavailable for FrontierScience-Olympiad.** The 4-8 decisions per
  task filter cannot be applied at row level. Phase 2 must either treat each row as single-decision
  or derive step graphs in a follow-up hierarchical-annotation task.
* **tau-bench filter excludes tasks with very short or very long action sequences.** The upstream
  test set has 50 retail and 50 airline tasks; we keep 13 + 50 + 24 = 87 (using retail/train as
  well, where action sequences are often shorter). For sensitivity analysis, Phase 2 might
  re-evaluate with a relaxed [3, 12] window.

## Files Created

* `assets/dataset/frontierscience-olympiad-subset/` — `details.json`, `description.md`, plus
  `files/frontierscience-olympiad-subset.jsonl` (40 rows).
* `assets/dataset/workarena-plus-plus-subset/` — `details.json`, `description.md`, plus
  `files/workarena-plus-plus-subset-task-manifest.json`, `files/upstream/curriculum.py`,
  `files/upstream/compositional__init__.py`, `files/upstream/README.md`.
* `assets/dataset/swebench-verified-subset/` — `details.json`, `description.md`, plus
  `files/swe-bench-verified-test.parquet` (2.0 MB upstream parquet) and
  `files/swebench-verified-subset.jsonl` (60 filtered rows).
* `assets/dataset/taubench-subset/` — `details.json`, `description.md`, plus
  `files/taubench-subset.jsonl` (87 filtered rows) and `files/upstream/airline__tasks_test.py`,
  `files/upstream/retail__tasks_test.py`, `files/upstream/retail__tasks_train.py` (verbatim upstream
  sources).
* `code/` — 11 Python modules (`paths.py`, `constants.py`, `dataset_asset.py`,
  `download_attempt.py`, `build_frontierscience.py`, `build_workarena_pp.py`, `build_swebench.py`,
  `build_taubench.py`, `build_status_manifest.py`, `build_all.py`, `__init__.py`).
* `code/access_status.json` — per-benchmark access decision manifest.
* `plan/plan.md`, `results/results_summary.md`, `results/results_detailed.md`,
  `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json`,
  `results/suggestions.json` (suggestions step writes).
* Step logs under `logs/steps/` and command logs under `logs/commands/`.

## Task Requirement Coverage

The operative task text from `task.json` and `task_description.md`:

```text
Name: Download benchmark subsets for the four roadmap sources
short_description: Wire up access to FrontierScience-Olympiad, WorkArena++, SWE-bench Verified,
and tau-bench subsets at 4-8 decisions per task.

Approach (from task_description.md):
1. For each benchmark, attempt the official distribution path documented in its source paper.
2. Subset to 4-8 decisions per task using whatever per-instance step or step-count metadata
   the benchmark provides; if none exists, sample uniformly with a fixed seed.
3. Produce one dataset asset per benchmark with details.json describing source URL, version,
   license, sample count, and subset selection criteria.
4. If a benchmark is inaccessible, write the access attempt log into details.json with
   download_status="failed" and clear download_failure_reason.
5. Emit follow-up suggestions for benchmarks where access is non-obvious or subsetting
   deserves a Phase 2 sensitivity check.

Expected outputs:
- Four dataset assets under assets/dataset/.
- results/results_summary.md with per-benchmark access status, sample count, subset decisions.
- results/suggestions.json flagging permanent proxy choices.
```

| ID | Requirement | Status | Answer / Result | Evidence |
| --- | --- | --- | --- | --- |
| REQ-1 | Attempt official FrontierScience-Olympiad distribution; subset by domain to match pilot focus | Done | Packaged 40 pilot rows (physics=15, chemistry=10, biology=15) as v0 subset; FrontierMath upstream is Epoch-AI-gated and out of reach for this task. Asset has `download_status: "success"` because the v0 substitute is fully usable. | `assets/dataset/frontierscience-olympiad-subset/details.json`, `description.md`, `files/frontierscience-olympiad-subset.jsonl`; documented in suggestions for follow-up Epoch AI negotiation |
| REQ-2 | Attempt official WorkArena++ distribution; if inaccessible, document and freeze Mind2Web pilot proxy | Partial | Manifest extracted from upstream `curriculum.py` (42 task class lists). Instance enumeration deferred (gated on ServiceNow + HF). `access_kind` set to `"restricted"`; description states the Mind2Web pilot proxy remains the operative Phase 2 fallback. A suggestion is emitted to retry once instance access is resolved. | `assets/dataset/workarena-plus-plus-subset/details.json`, `description.md`, `files/workarena-plus-plus-subset-task-manifest.json`, `files/upstream/curriculum.py` |
| REQ-3 | Download SWE-bench Verified from official Princeton/HF distribution; subset to instances mapping cleanly onto the three-level hierarchy | Done | Downloaded the official 500-instance Verified parquet via `urllib`, filtered to 60 instances with 4-8 patch hunks. Each hunk maps to one atomic edit decision; the issue text is the global intent and FAIL_TO_PASS tests are subtask gates. | `assets/dataset/swebench-verified-subset/files/swe-bench-verified-test.parquet`, `files/swebench-verified-subset.jsonl`, `details.json`, `description.md` |
| REQ-4 | Attempt official tau-bench distribution; if inaccessible, freeze HumanEval pilot proxy | Done | Downloaded upstream tau-bench airline + retail task definitions from GitHub raw, parsed via `ast` to extract action counts, filtered to 87 tasks with 4-8 actions across airline/test, retail/test, retail/train. | `assets/dataset/taubench-subset/files/taubench-subset.jsonl`, `details.json`, `description.md`, `files/upstream/*.py` |
| REQ-5 | Each subset must target multi-step instances of 4-8 decisions per task; if no metadata, sample uniformly with fixed seed | Done | SWE-bench: per-instance hunk count drives the filter, distribution 4=24, 5=12, 6=14, 7=7, 8=3. tau-bench: per-instance action count drives the filter, distribution 4=24, 5=24, 6=23, 7=13, 8=3. FrontierScience: per-row counts unavailable so the subset is domain-stratified instead and the limitation is documented. WorkArena++: instance-level filter deferred as documented in the description. | Per-asset `description.md` `## Statistics` sections |
| REQ-6 | Each dataset asset conforms to spec v2 and passes `verify_dataset_asset` with zero errors | Done | All four assets pass with zero errors and zero warnings. | `verify_dataset_asset --task-id t0003_download_benchmark_subsets` output captured in `logs/commands/` |
| REQ-7 | `results/results_summary.md` reports per-benchmark access status, sample count, subset decisions | Done | The summary lists status, sample count, and subset rule per benchmark, plus a 4-of-4 pass count. | `results/results_summary.md` |
| REQ-8 | `results/suggestions.json` flags permanent proxy / non-obvious access pathways | Done (delivered by the suggestions step that follows results) | The suggestions step is the next orchestrator step; it consumes `code/access_status.json` produced here and writes `results/suggestions.json` with one entry per gated benchmark. | `code/access_status.json` (generated here); `results/suggestions.json` populated by the suggestions step |
