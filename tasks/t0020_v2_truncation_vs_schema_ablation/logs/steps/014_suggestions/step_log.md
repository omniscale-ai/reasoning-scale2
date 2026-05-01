---
spec_version: "3"
task_id: "t0020_v2_truncation_vs_schema_ablation"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T17:09:00Z"
completed_at: "2026-05-01T17:11:00Z"
---
## Summary

Wrote 5 follow-up suggestions to `results/suggestions.json`. Two are high/medium priority and
directly tighten the statistical bounds on the t0020 decomposition: (1) re-judging the remaining 8
v1 rows would shrink the pure-schema CI half-width from ~28 pp to ~14 pp at minimal cost; (2) sonnet
judge rerun on v2-tree-truncated would confirm the schema effect is not a haiku artifact. Three
lower-priority follow-ups extend the result to n=80, sweep the truncation budget, and produce a
cost-quality Pareto chart for downstream tasks.

## Actions Taken

1. Read `arf/specifications/suggestions_specification.md` to confirm format requirements.
2. Drafted 5 suggestion entries grounded in the run's actual limitations (v1 sample size, single
   judge model, n=20 power, single truncation budget) and concrete next-step costs.
3. Wrote `results/suggestions.json` with `spec_version: "2"` and `suggestions` array.
4. Ran `verify_suggestions.py`; PASSED with no errors or warnings.

## Outputs

* `tasks/t0020_v2_truncation_vs_schema_ablation/results/suggestions.json` (5 suggestions)
* `tasks/t0020_v2_truncation_vs_schema_ablation/logs/steps/014_suggestions/step_log.md`

## Issues

No issues encountered.
