---
spec_version: "3"
task_id: "t0003_download_benchmark_subsets"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-29T14:56:47Z"
completed_at: "2026-04-29T14:58:00Z"
---
# Step 14: suggestions

## Summary

Wrote `results/suggestions.json` with five follow-up suggestions covering the two access-gated
benchmarks (FrontierMath / Epoch AI access for FrontierScience and ServiceNow + HF access for
WorkArena++), a SWE-bench subsetting sensitivity check, a hierarchical-annotation suggestion to
derive step graphs for FrontierScience-Olympiad rows, and a library-promotion suggestion for the
dataset-asset writer helpers. The verificator passes with zero errors and zero warnings.

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` to confirm the v2 schema and ID format.
2. Reviewed `code/access_status.json` and the per-benchmark outcome tables in
   `results/results_detailed.md` to identify follow-ups.
3. Drafted five suggestions: two `dataset`-kind (high-priority access negotiations), one
   `evaluation`-kind (medium-priority subset sensitivity check), one `experiment`-kind
   (medium-priority hierarchical-annotation), and one `library`-kind (low-priority).
4. Ran `verify_suggestions` and confirmed PASSED with zero errors / zero warnings.

## Outputs

* `tasks/t0003_download_benchmark_subsets/results/suggestions.json` — five suggestions.
* `tasks/t0003_download_benchmark_subsets/logs/steps/014_suggestions/step_log.md`

## Issues

No issues encountered. All five suggestions are scoped to address gaps documented in the results
files; two are direct consequences of the deliberate access-fallback policy.
