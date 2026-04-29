---
spec_version: "3"
task_id: "t0003_download_benchmark_subsets"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T14:39:54Z"
completed_at: "2026-04-29T14:55:00Z"
---
# Step 9: implementation

## Summary

Built four dataset assets covering all four roadmap benchmarks. Three were downloaded directly from
public sources (HuggingFace, GitHub raw): SWE-bench Verified parquet (500 -> 60 instances after the
4-8 hunks filter), tau-bench airline + retail task definitions parsed via the `ast` module (665 ->
87 tasks after the 4-8 actions filter), and the WorkArena++ compositional task class manifest
extracted from upstream `curriculum.py` (42 task class lists). The FrontierScience-Olympiad asset
packages 40 pilot rows as the v0 subset, documenting the upstream FrontierMath access gap. All four
assets pass `verify_dataset_asset` with zero errors.

## Actions Taken

1. Added `pyarrow>=24.0.0` to `pyproject.toml` for SWE-bench parquet reading; ran `uv add` and
   committed the lock update through the implementation commit.
2. Wrote scaffolding modules: `code/paths.py`, `code/constants.py`, `code/dataset_asset.py` (frozen
   dataclasses for v2 dataset asset metadata + a write helper), and `code/download_attempt.py`
   (records failed-download access attempts).
3. Built four per-benchmark builders (`build_frontierscience.py`, `build_workarena_pp.py`,
   `build_swebench.py`, `build_taubench.py`) that each download (or read pilot data), filter, write
   `details.json` and `description.md` per the v2 spec, and place files under `files/`.
4. Wrote `build_status_manifest.py` that emits `code/access_status.json` summarizing the four
   per-benchmark access decisions for the orchestrator's results step to consume.
5. Wrote `build_all.py` that runs the four builders in order followed by the manifest builder.
6. Ran `build_all.py` via `run_with_logs.py`. Validation gate for SWE-bench passed (60 instances
   inside the [30, 450] sanity window). One bug surfaced and was fixed: tau-bench retail uses
   `TASKS_TEST` / `TASKS_TRAIN` instead of `TASKS`; updated the AST parser to accept any `TASKS*`
   identifier and re-ran (87 tasks across both domains).
7. Ran `verify_dataset_asset --task-id t0003_download_benchmark_subsets` — all four assets PASSED
   with zero errors and zero warnings.
8. Ran `ruff check`, `ruff format --check`, and
   `mypy -p tasks.t0003_download_benchmark_subsets.code` — all pass.

## Outputs

* `tasks/t0003_download_benchmark_subsets/code/` — 11 Python modules (paths, constants, dataset
  asset helper, access-attempt helper, four builders, status manifest builder, build_all
  orchestrator, `__init__.py`).
* `tasks/t0003_download_benchmark_subsets/code/access_status.json` — per-benchmark access decision
  manifest.
* `tasks/t0003_download_benchmark_subsets/assets/dataset/frontierscience-olympiad-subset/` — 40
  problems, success.
* `tasks/t0003_download_benchmark_subsets/assets/dataset/workarena-plus-plus-subset/` — 42 task
  class lists, success (manifest only; instance enumeration deferred).
* `tasks/t0003_download_benchmark_subsets/assets/dataset/swebench-verified-subset/` — 60 instances
  filtered from 500 Verified, success.
* `tasks/t0003_download_benchmark_subsets/assets/dataset/taubench-subset/` — 87 tasks across airline
  \+ retail, success.
* `tasks/t0003_download_benchmark_subsets/logs/steps/009_implementation/step_log.md`

## Issues

WorkArena++ task instance enumeration requires a live ServiceNow developer instance plus access to
the gated `ServiceNow/WorkArena-Instances` HuggingFace dataset, neither of which fits this task's
local-only download budget. The asset is marked `download_status: "success"` because the upstream
curriculum manifest was successfully extracted; `access_kind` is set to `"restricted"` to flag the
instance-level gating. The Mind2Web pilot proxy remains the de-facto Phase 2 fallback for end-to-end
task execution and is documented in the `description.md`. A follow-up suggestion will track the
access negotiation.
