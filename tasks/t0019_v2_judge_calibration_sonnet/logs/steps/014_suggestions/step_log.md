---
spec_version: "3"
task_id: "t0019_v2_judge_calibration_sonnet"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T17:51:32Z"
completed_at: "2026-05-01T17:53:00Z"
---
# Step 14: suggestions

## Summary

Wrote four follow-up suggestions to `results/suggestions.json` (spec v2). The set covers the
canonical confirmation experiment (S-0019-01: fresh-pool v2 vs v1 schema sweep with a third sonnet
judge), the infrastructure unblocker (S-0019-02: provision a sonnet-quota API key to drop per-call
cost ~7x), the prompt-vs-model attribution ablation (S-0019-03: substantive critic vs original
prompt at fixed model on 50 rows), and the cross-vendor judge replication (S-0019-04: GPT-4 and
Gemini judges on the same 55-row pool).

## Actions Taken

1. Drafted four suggestions in `results/suggestions.json` following the v2 spec: ids
   `S-0019-01..04`, allowed kinds (`experiment`, `library`, `evaluation`, `experiment`), priorities
   (`high`, `medium`, `medium`, `low`), per-suggestion rationale, expected outcome, estimated cost,
   and dependency back-references.
2. Verified the file structure with `verify_suggestions`.

## Outputs

* `tasks/t0019_v2_judge_calibration_sonnet/results/suggestions.json` (4 suggestions)

## Issues

No issues encountered.
