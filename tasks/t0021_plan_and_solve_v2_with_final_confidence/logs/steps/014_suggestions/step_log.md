---
spec_version: "3"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T16:50:00Z"
completed_at: "2026-05-01T16:55:00Z"
---
## Summary

Wrote three forward-looking suggestions to `results/suggestions.json` covering the side-finding from
the smoke run and follow-up calibration work for the downstream t0023 confirmatory study. Suggestion
IDs `S-0021-01`, `S-0021-02`, `S-0021-03` follow the canonical `S-XXXX-NN` format with `task_index`
21\.

## Actions Taken

1. Reviewed `results/smoke_report.json` and `results/results_detailed.md` for actionable
   side-findings. Identified the 31-decision Condition C trajectory and the absence of calibration
   analysis as the two strongest candidate suggestions.
2. Wrote `S-0021-01` (medium priority, kind `experiment`): investigate the 31-decision C trajectory
   in t0023's larger sample; check whether the planning loop hypothesis holds at scale.
3. Wrote `S-0021-02` (high priority, kind `evaluation`): track confidence-vs-correctness calibration
   on t0023 with reliability diagrams, Brier scores, ECE in addition to `overconfident_error_rate`.
4. Wrote `S-0021-03` (low priority, kind `library`): add a JSON-mode fallback path to confidence
   elicitation if larger runs hit the 20% parse-failure gate from REQ-10.
5. Validated each suggestion's `categories` against `meta/categories/` (all use existing slugs:
   `hierarchical-planning`, `agent-evaluation`, `uncertainty-calibration`).

## Outputs

* `results/suggestions.json` — three suggestions with `spec_version: "2"`.

## Issues

No issues encountered. The two-suggestion floor from the task description was met (three suggestions
written).
