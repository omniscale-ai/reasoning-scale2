---
spec_version: "3"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T15:59:14Z"
completed_at: "2026-05-01T20:35:00Z"
---
## Summary

Wrote five follow-up suggestions for t0022 in `results/suggestions.json` (spec_version 2). Two are
high-priority: S-0022-02 (hand-tighten FrontierScience-Olympiad subgoals before t0023) and S-0022-05
(run t0023's confirmatory ABC re-run consuming abc_harness_metrics). Three are medium-priority
technical follow-ups: S-0022-01 (skip-write fallback responses to disk cache), S-0022-03
(line-range/AST-node SWE-bench subgoals), and S-0022-04 (Sonnet vs Haiku spot-check on a stratified
20-step sample). All five have descriptions over 200 characters and use only valid category slugs
from `meta/categories/`. `verify_suggestions.py` passes with zero errors and zero warnings.

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` (v2) to confirm the schema.
2. Listed `meta/categories/` to confirm valid category slugs (agent-evaluation,
   benchmark-frontierscience, benchmark-swebench, granularity-conditioning, hierarchical-planning,
   uncertainty-calibration, etc.).
3. Drafted five suggestions covering: cache hygiene fix, FrontierScience subgoal hand-tightening,
   SWE-bench subgoal granularity refinement, judge model agreement spot-check, and t0023
   confirmatory ABC re-run.
4. Wrote `results/suggestions.json` with `spec_version: "2"` and 5 suggestion objects.
5. Ran `verify_suggestions.py` via `run_with_logs.py`; PASSED with 0 errors and 0 warnings.

## Outputs

* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/results/suggestions.json`

## Issues

No issues encountered.
