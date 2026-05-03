---
spec_version: "3"
task_id: "t0029_rq1_discordance_rich_resample"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-03T10:02:18Z"
completed_at: "2026-05-03T10:10:00Z"
---
## Summary

Surveyed t0027's harness, t0021's Plan-and-Solve v2 library, and t0010's matched-mismatch library to
inventory reusable code, identify the cost-tracking and cap-guardrail integration points, and flag a
variant-labeling ambiguity between t0028 brainstorm session 8 (which calls Plan-and-Solve baseline
arm A, scope-aware ReAct arm B) and t0027/t0026 (which inverts that labeling). Findings are recorded
in `research/research_code.md`.

## Actions Taken

1. Ran prestep to mark research-code in_progress.
2. Spawned an Explore subagent to inventory t0027 code, predictions assets, and results.
3. Read `t0027/results/results_summary.md` directly to confirm the per-variant success rates and the
   parser-recovery distribution.
4. Inspected `run_abc_rerun.py` lines 100-300 to confirm the paired-manifest computation and the
   per-instance runner integration with `CostTracker`.
5. Verified t0010's library contains a description but no separate paired-instance file — expansion
   beyond t0027's 130 must run A and B directly on new instances.
6. Documented the variant-labeling ambiguity in `research_code.md` with a recommended internal
   convention (use t0027's labels, relabel in final writeup).

## Outputs

* `tasks/t0029_rq1_discordance_rich_resample/research/research_code.md`
* `tasks/t0029_rq1_discordance_rich_resample/logs/steps/006_research-code/step_log.md`

## Issues

Variant-labeling conflict between brainstorm session 8 (arm A = baseline, arm B = scope-aware) and
t0027 (Variant A = scope-aware, Variant B = baseline). Resolved internally by adopting t0027's
labeling for the harness and relabeling only in the final writeup so reused t0027 predictions remain
valid without renaming files.
