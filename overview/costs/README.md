# Project Costs

Spent $54.58 of $100.00 USD. $45.42 remains overall and $45.42 remains before the 100% stop
threshold.

## Budget Summary

| Field | Value |
|-------|-------|
| Total budget | $100.00 USD |
| Total spent | $54.58 USD |
| Budget left | $45.42 USD |
| Budget left before stop threshold | $45.42 USD |
| Spent percent | 54.58% |
| Warn threshold | 80% ($80.00) |
| Stop threshold | 100% ($100.00) |
| Default per-task limit | $10.00 USD |
| Tasks with cost records | 21 |
| Tasks with non-zero spend | 7 |
| Skipped tasks | 2 |

## Service Totals

| Key | Cost (USD) |
|-----|------------|
| `anthropic_api` | $24.32 |

## Breakdown Totals

| Key | Cost (USD) |
|-----|------------|
| `annotator_sonnet_4_6` | $19.77 |
| `claude-haiku-4-5` | $18.91 |
| `annotator_haiku_4_5` | $7.42 |
| `judge_haiku_4_5` | $3.08 |
| `claude-haiku-4-5_progress_rate_judge` | $1.55 |
| `claude-haiku-4-5-annotator` | $1.55 |
| `claude-haiku-4-5-judge` | $1.38 |
| `claude-haiku-4-5_error_taxonomy_judge` | $0.86 |
| `anthropic_api` | $0.06 |

14 task cost record(s) are zero-cost and omitted from the main spend table.

## Task Spend

| Task | Status | Total (USD) | Limit (USD) | Over limit |
|------|--------|-------------|-------------|------------|
| [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) | completed | $0.06 | $10.00 | no |
| [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) | completed | $9.10 | $10.00 | no |
| [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) | completed | $18.37 | $10.00 | yes |
| [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) | completed | $21.16 | $10.00 | yes |
| [`t0020_v2_truncation_vs_schema_ablation`](../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) | completed | $2.93 | $6.00 | no |
| [`t0021_plan_and_solve_v2_with_final_confidence`](../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) | completed | $0.54 | $1.00 | no |
| [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) | completed | $2.42 | $2.00 | yes |

## Skipped Tasks

| Task ID | Reason |
|---------|--------|
| `t0019_v2_judge_calibration_sonnet` | results/costs.json is missing or invalid |
| `t0023_phase2_abc_confirmatory_sonnet_swebench` | results/costs.json is missing or invalid |
