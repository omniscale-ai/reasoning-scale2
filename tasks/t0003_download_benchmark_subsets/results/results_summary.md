# Results Summary: Download Benchmark Subsets

## Summary

Acquired four benchmark subsets covering the project's roadmap sources (FrontierScience-Olympiad,
WorkArena++, SWE-bench Verified, tau-bench). Three were downloaded directly from public sources;
WorkArena++ instance enumeration is gated on a live ServiceNow developer instance, so its asset
captures the upstream curriculum manifest only and freezes the Mind2Web pilot proxy as the de-facto
Phase 2 fallback. All four dataset assets pass `verify_dataset_asset` with zero errors.

## Metrics

* **4 of 4** dataset assets created and passing `verify_dataset_asset` (zero errors, zero warnings).
* **FrontierScience-Olympiad subset**: **40** problems (15 physics, 10 chemistry, 15 biology),
  packaged from pilot rows; status **success** (FrontierMath upstream still gated).
* **WorkArena++ subset**: **42** compositional task class lists extracted from upstream
  `curriculum.py`; status **success (manifest only)**, instance enumeration deferred and Mind2Web
  pilot proxy frozen.
* **SWE-bench Verified subset**: **60** instances filtered from **500** Verified using the 4-8 hunks
  rule; status **success**.
* **tau-bench subset**: **87** tasks across airline + retail (test + train) filtered from **665**
  upstream tasks using the 4-8 actions rule; status **success**.
* **Total cost**: **$0** (no paid APIs, no GPU, no third-party paid services).

## Verification

* `verify_dataset_asset --task-id t0003_download_benchmark_subsets` — PASSED on all 4 assets (0
  errors, 0 warnings each).
* `verify_plan` — PASSED (0 errors, 0 warnings).
* `verify_task_dependencies` — PASSED (no dependencies).
* `ruff check` and `ruff format --check` on `tasks/t0003_download_benchmark_subsets/code/` — PASSED.
* `mypy -p tasks.t0003_download_benchmark_subsets.code` — PASSED.
