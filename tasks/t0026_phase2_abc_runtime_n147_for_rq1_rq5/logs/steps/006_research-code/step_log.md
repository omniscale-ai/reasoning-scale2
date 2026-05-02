---
spec_version: "3"
task_id: "t0026_phase2_abc_runtime_n147_for_rq1_rq5"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-02T06:40:02Z"
completed_at: "2026-05-02T06:42:30Z"
---
## Summary

Surveyed all seven dependency tasks (t0003 benchmark subsets, t0006 scope-aware ReAct, t0010
matched-mismatch, t0011 calibration aggregator, t0019 sonnet judge findings, t0021 Plan-and-Solve v2
with final_confidence, t0022 ABC harness with progress rate and EAI error taxonomy) and wrote
`research/research_code.md` capturing the concrete file paths, public APIs, and known gotchas the
implementation step must respect.

## Actions Taken

1. Spawned an Explore subagent to read each dependency task's `assets/library/`, `code/`, and
   `assets/dataset/` (where applicable) and report public API signatures, default models, and known
   gotchas.
2. Confirmed JSONL file paths and instance counts for all three runnable subsets (60 SWE-bench
   Verified, 87 Tau-bench, 40 FrontierScience-Olympiad); WorkArena++ excluded.
3. Recorded that t0011 exposes only `overconfident_error_rate` and not ECE — t0026 must implement a
   10-bin ECE inline for RQ4.
4. Recorded that t0019 produced no reusable judge library — t0026 will implement a small
   `code/judge.py` reusing the t0019 sonnet prompt patterns plus a 30-instance opus inter-judge
   slice.
5. Wrote `research/research_code.md` with Objective, Background, Methodology Review, Key Findings
   (per-dependency subsections), Recommended Approach (7 numbered build steps), and References.

## Outputs

- `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/research/research_code.md`
- `tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/logs/steps/006_research-code/step_log.md`

## Issues

No issues encountered.
