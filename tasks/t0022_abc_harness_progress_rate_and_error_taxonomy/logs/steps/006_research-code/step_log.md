---
spec_version: "3"
task_id: "t0022_abc_harness_progress_rate_and_error_taxonomy"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-01T14:07:40Z"
completed_at: "2026-05-01T14:09:30Z"
---
# Research Code

## Summary

Surveyed all five existing project libraries via the library aggregator (`scope_aware_react_v1`,
`scope_unaware_planandsolve_v1`, `matched_mismatch_v1`, `metric2_calibration_aggregator_v1`,
`phase2_smoke_harness_v1`) plus the t0017 paper assets (Ma2024 AgentBoard, Li2024 EAI) that contain
the protocol specifications this library implements. None of the existing libraries provide
progress-rate or error-taxonomy functionality, so this task is genuinely additive. The local
`claude` CLI invocation pattern from `t0012/code/model_call.py` will be copied (not imported) into
the new library because cross-task imports are forbidden outside library assets.

## Actions Taken

1. Ran the library aggregator to enumerate all existing libraries and their relevance.
2. Read the t0017 paper-asset summaries for Ma2024 (AgentBoard, paper id
   `10.48550_arXiv.2401.13178`) and Li2024 (EAI, paper id `10.48550_arXiv.2410.07166`) to confirm
   the protocol shapes.
3. Inspected t0012's `harness.py`, `model_call.py`, `constants.py`, and prediction JSONL format to
   understand the trajectory schema (`turn_index`, `granularity`, `thought`, `action`,
   `observation`, `confidence`) and the local CLI cost-tracking pattern.
4. Counted trajectory lengths in t0012 predictions (40 A, 40 B, 11 C with mean lengths ~1.18, ~1.13,
   ~26.0 respectively) to confirm A-vs-C step counts will support the 30% separation criterion.
5. Wrote `research/research_code.md` with all seven mandatory sections, six cited tasks, and
   detailed reuse plans.
6. Ran `verify_research_code.py` — passed with zero errors and zero warnings.

## Outputs

* `tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/research/research_code.md`

## Issues

First verificator run flagged six errors: one missing Task Index entry for t0011 (which was cited
inline) and five Task Index entries with non-bold "Task ID" field labels. Fixed by adding the t0011
entry, bumping `tasks_cited` to 6, and changing field labels to `**Task ID**:` etc. Re-ran
verificator and it passed.
