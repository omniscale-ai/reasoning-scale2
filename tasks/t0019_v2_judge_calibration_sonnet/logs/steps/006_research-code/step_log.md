---
spec_version: "3"
task_id: "t0019_v2_judge_calibration_sonnet"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-01T14:08:20Z"
completed_at: "2026-05-01T14:14:49Z"
---
# Step 6: research-code

## Summary

Reviewed code, libraries, and prior task assets to identify reusable patterns for re-judging the
55-row pool from t0014 under two new judge configurations using `claude-sonnet-4-6`. Wrote
`research/research_code.md` covering the judge prompts, parsing logic, statistics utilities,
idempotency patterns, and dataset paths needed by the implementation step. None of the five
registered libraries applies to this task; reusable code must be copied from t0014's `code/`
directory.

## Actions Taken

1. Spawned `/research-code` subagent with task ID and skill instructions.
2. Subagent reviewed prior task code (t0005, t0009, t0014, t0015) and library registry, then wrote
   `research/research_code.md` with task objective, library landscape, key findings, reusable
   code/assets, dataset landscape, lessons learned, recommendations, and a task index.
3. Verified `research/research_code.md` exists and conforms to the research-code specification.

## Outputs

* `tasks/t0019_v2_judge_calibration_sonnet/research/research_code.md` (337 lines)
* Identified 4 reusable code blocks to copy from t0014: `_call_claude_cli`, `_parse_verdict`,
  `_wilson_ci`, `_delta_with_ci`, plus the original judge system prompt and user template.

## Issues

No issues encountered.
