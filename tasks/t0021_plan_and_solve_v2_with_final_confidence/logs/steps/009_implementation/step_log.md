---
spec_version: "3"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T14:17:54Z"
completed_at: "2026-05-01T14:46:00Z"
---
## Summary

Implemented the `scope_unaware_planandsolve_v2` library end-to-end: wrote the v2 agent and helpers
(`code/planandsolve_v2.py`), the parser, the `elicit_final_confidence` two-call protocol, the
16-test pytest suite, the n=1 x 3 smoke validation harness (`code/run_smoke.py`), and registered the
library asset (`assets/library/scope_unaware_planandsolve_v2/`). Ran the smoke pass on
FrontierScience-Olympiad with `claude-haiku-4-5` and confirmed every condition emits
`final_confidence` with zero parse failures; total spend $0.5383 of the $1.00 cap.

## Actions Taken

1. Copied helper modules into `code/`: `model_call.py` (Anthropic API wrapper with `CostTracker`)
   and `calibration.py` (`compute_overconfident_error_rate`, `HIGH_CONFIDENCE_THRESHOLD`). Added
   `paths.py` and `constants.py` for centralized path and schema constants.
2. Wrote `code/planandsolve_v2.py` implementing `parse_final_confidence`, `elicit_final_confidence`,
   `TrajectoryRecordV2`, `AgentResultV2`, and `PlanAndSolveAgentV2`. v2 imports v1 symbols from
   `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` rather than forking, to
   preserve t0010's matched-mismatch agent.
3. Wrote `code/test_planandsolve_v2.py` covering parser last-match wins, parser clamping at the word
   boundary, parser failure on non-numeric input, retry semantics (0/1/2 failures), v1 schema
   invariants, and `PlanAndSolveAgentV2.run` end-to-end against `ScriptedModel`. Ran
   `uv run pytest tasks/t0021_*/code/ -v` and confirmed 16/16 passing.
4. Wrote `code/run_smoke.py` to load 1 row from the FrontierScience-Olympiad slice of the t0009
   hierarchical-annotation-v2 dataset and run all three conditions (A scope-aware, B scope-unaware
   v2, C matched-mismatch) with the v2 library, post-call confidence elicitation, and a haiku judge.
   Per-row predictions written to `results/smoke_predictions.jsonl`.
5. Ran the smoke pass under the $1.00 cap. Wall-clock 786.69 s; 43 model calls; total cost
   $0.538343. Conditions A=1 decision, B=8 decisions, C=31 decisions; all three trajectories carry
   non-null `final_confidence`; 0/3 parse failures.
6. Registered the library asset at `assets/library/scope_unaware_planandsolve_v2/` with
   `details.json` (spec_version 2, library_id, module_paths, entry_points, dependencies, categories,
   created_by_task, date_created), the canonical `description.md` with eight required sections, and
   `files/prompts/confidence_prompt.txt` (verbatim Xiong2024 §3.2 phrasing).
7. Wrote `results/metrics.json` in explicit-variant format with three condition variants; only
   registered metric keys appear under `metrics`, with `n` and parse-failure metadata moved to
   `dimensions`. Wrote `results/costs.json` with `breakdown`, `services`, and `budget_limit`. Wrote
   `results/remote_machines_used.json` as `[]`. Wrote `results/smoke_report.json` with the top-level
   rollup.
8. Validated all artifacts pass their verificators: `verify_task_file`, `verify_logs`,
   `verify_task_results`, `verify_library_asset` for `scope_unaware_planandsolve_v2`.

## Outputs

* `code/planandsolve_v2.py` — v2 agent, parser, elicitation helper, data classes.
* `code/constants.py` — schema constants.
* `code/paths.py` — centralized Path constants.
* `code/model_call.py` — Anthropic API wrapper with `CostTracker`.
* `code/calibration.py` — `compute_overconfident_error_rate` and helpers.
* `code/run_smoke.py` — n=1 x 3 smoke harness.
* `code/test_planandsolve_v2.py` — 16-test pytest suite (all passing).
* `assets/library/scope_unaware_planandsolve_v2/details.json` — library metadata.
* `assets/library/scope_unaware_planandsolve_v2/description.md` — canonical library description.
* `assets/library/scope_unaware_planandsolve_v2/files/prompts/confidence_prompt.txt` — verbatim
  Xiong2024 §3.2 prompt.
* `results/metrics.json` — explicit-variant format, three conditions.
* `results/costs.json` — $0.5383 total.
* `results/remote_machines_used.json` — empty array.
* `results/smoke_predictions.jsonl` — 3 rows (one per condition) with full trajectories.
* `results/smoke_report.json` — top-level smoke rollup.
* `results/_call_log.jsonl` — raw agent call log (15 entries).
* `results/_judge_log.jsonl` — raw judge call log (8 entries).

## Issues

No issues encountered. The smoke ran under budget; parse-failure rate was 0/3, well within the 20%
gate from REQ-10. The C trajectory used 31 decisions on n=1, which is a side-finding worth
investigating in t0023's larger sample but does not affect the library deliverable here.
