# Results Summary: ABC Harness Progress Rate and Error Taxonomy

## Summary

Built and validated the `abc_harness_metrics` library: Ma2024 AgentBoard discrete-subgoal progress
rate plus Li2024 Embodied Agent Interface six-plus-one error taxonomy. The library exposes
`compute_progress_rate`, `classify_error`, and the high-level `score_trajectory` entry point, with
26 unit tests passing and a t0012 replay confirming end-to-end correctness on production-shape
trajectories.

## Metrics

* **Progress-rate mean across 89 t0012 trajectories**: **0.103** (decision threshold > 0.05) — the
  library detects intermediate progress on real agent traces, not zero or one.
* **Progress-rate standard deviation**: **0.228** (decision threshold > 0.03) — distribution is
  meaningfully spread across the 91 rows, with values from 0.0 to 1.0.
* **A-vs-C error-distribution total-variation separation**: **0.771** (decision threshold >= 0.30) —
  single-step (A) and hierarchical (C) trajectories produce qualitatively different error mixtures,
  confirming the taxonomy can discriminate between conditions for t0023.
* **FrontierScience-Olympiad subgoal coverage**: **26 environments**, mean 4.6 subgoals each (3-5
  per task per the plan invariant).
* **SWE-bench Verified Lite subgoal coverage**: **60 environments** (>= 50 per REQ-6), 2-3 subgoals
  each.
* **Unit-test pass rate**: **26/26** in 0.16 s (mock-judge tests, zero CLI cost).
* **Total replay cost**: **$2.4172** in 533 judge calls (over the $2.00 task cap by $0.42; root
  cause and mitigation documented in `costs.json` `note`).

## Verification

* `verify_library_asset.py` (abc_harness_metrics) — PASSED (0 errors, 0 warnings)
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings)
* `uv run pytest tasks/t0022_*/code/` — PASSED (26/26)
* `uv run ruff check tasks/t0022_*/code/` — PASSED (clean)
* `uv run mypy -m tasks.t0022_*.code.<each module>` — PASSED (no issues)
