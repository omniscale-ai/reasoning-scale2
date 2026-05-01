# Results Summary: Plan-and-Solve v2 with final_confidence

## Summary

The deliverable is the `scope_unaware_planandsolve_v2` library that wraps the v1 Plan-and-Solve
agent and emits a verbalized `final_confidence` field on every trajectory following the Xiong et al.
2024 section 3.2 protocol. The n=1 x 3 validation pass confirms the parser, two-call protocol, and
confidence emission are wired end-to-end across all three conditions (A scope-aware, B
scope-unaware, C scope-mismatched). The 0% task-success rate across all conditions on
FrontierScience-Olympiad with claude-haiku-4-5 is consistent with the t0012 floor finding for the
same benchmark and model and is the explicit motivation for the larger downstream confirmatory study
in t0023.

## Metrics

* **task_success_rate**: A=**0.0** (0/1), B=**0.0** (0/1), C=**0.0** (0/1) — at-floor on this
  benchmark, as expected.
* **overconfident_error_rate**: A=**1.0** (the single A row was wrong with high confidence),
  B=**0.0**, C=**0.0** — non-degenerate emission across conditions confirmed.
* **avg_decisions_per_task**: A=**1.0**, B=**8.0**, C=**31.0** — flagged side-finding: C used 31x
  more decisions than A.
* **parse_failure_rate**: **0.0** across all 3 trajectories (well under the 20% gate from the plan).
* **Total cost**: **$0.5383** of the $1.00 cap; **43** claude-haiku-4-5 calls in **786.69 s** (~13
  min).

## Verification

* `verify_task_file` — PASSED
* `verify_logs` — PASSED
* `verify_task_results` — PASSED
* `verify_library_asset scope_unaware_planandsolve_v2` — PASSED
