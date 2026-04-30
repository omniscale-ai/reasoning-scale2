---
spec_version: "3"
task_id: "t0015_correct_proxy_benchmark_labels"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-30T19:31:07Z"
completed_at: "2026-04-30T19:31:30Z"
---

# Step 14: suggestions

## Summary

Authored two follow-up suggestions in `results/suggestions.json` and verified the file passes
`verify_suggestions`. S-0015-01 carries the variant-a follow-up explicitly requested by the task
brief: replace the Mind2Web and HumanEval proxy rows with native WorkArena++ and tau-bench data.
S-0015-02 is a smaller meta-suggestion proposing a row-level provenance convention (`original_*`
fields) so future relabel overlays leave an in-row trail.

## Actions Taken

1. Drafted S-0015-01 (kind: `dataset`, priority: `medium`) carrying the S-0009-06 variant-a
   follow-up: obtain real WorkArena++ and tau-bench splits (treat their gating as an intervention),
   re-annotate the 26 + 26 rows under the v2 tree schema with the same haiku annotator and judge as
   t0009, and issue a corrections-overlay against `hierarchical-annotation-v2` that swaps the proxy
   rows for native rows.
2. Drafted S-0015-02 (kind: `evaluation`, priority: `low`) proposing a soft convention to add
   `original_<field>` to rows whose values are rewritten by a corrections overlay, so per-row
   provenance is auditable from the effective JSONL alone.
3. Wrote `results/suggestions.json` with `spec_version: "1"` and the two suggestion objects.
4. Ran `verify_suggestions t0015_correct_proxy_benchmark_labels` -> PASSED, 0 errors, 0 warnings.

## Outputs

* `tasks/t0015_correct_proxy_benchmark_labels/results/suggestions.json`
* `tasks/t0015_correct_proxy_benchmark_labels/logs/steps/014_suggestions/step_log.md`

## Issues

No issues encountered.
