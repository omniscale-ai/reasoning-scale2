# Project Costs

Spent $48.69 of $100.00 USD. $51.31 remains overall and $51.31 remains before the 100% stop
threshold.

## Budget Summary

| Field | Value |
|-------|-------|
| Total budget | $100.00 USD |
| Total spent | $48.69 USD |
| Budget left | $51.31 USD |
| Budget left before stop threshold | $51.31 USD |
| Spent percent | 48.69% |
| Warn threshold | 80% ($80.00) |
| Stop threshold | 100% ($100.00) |
| Default per-task limit | $10.00 USD |
| Tasks with cost records | 18 |
| Tasks with non-zero spend | 4 |
| Skipped tasks | 5 |

## Service Totals

| Key | Cost (USD) |
|-----|------------|
| `anthropic_api` | $18.43 |

## Breakdown Totals

| Key | Cost (USD) |
|-----|------------|
| `annotator_sonnet_4_6` | $19.77 |
| `claude-haiku-4-5` | $18.37 |
| `annotator_haiku_4_5` | $7.42 |
| `judge_haiku_4_5` | $3.08 |
| `anthropic_api` | $0.06 |

14 task cost record(s) are zero-cost and omitted from the main spend table.

## Task Spend

| Task | Status | Total (USD) | Limit (USD) | Over limit |
|------|--------|-------------|-------------|------------|
| [`t0005_hierarchical_annotation_pilot_v1`](../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) | completed | $0.06 | $10.00 | no |
| [`t0009_hierarchical_annotation_v2`](../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) | completed | $9.10 | $10.00 | no |
| [`t0012_phase2_abc_smoke_frontierscience`](../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) | completed | $18.37 | $10.00 | yes |
| [`t0014_v2_annotator_sonnet_rerun`](../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) | completed | $21.16 | $10.00 | yes |

## Skipped Tasks

| Task ID | Reason |
|---------|--------|
| `t0019_v2_judge_calibration_sonnet` | results/costs.json is missing or invalid |
| `t0020_v2_truncation_vs_schema_ablation` | results/costs.json is missing or invalid |
| `t0021_plan_and_solve_v2_with_final_confidence` | results/costs.json is missing or invalid |
| `t0022_abc_harness_progress_rate_and_error_taxonomy` | results/costs.json is missing or invalid |
| `t0023_phase2_abc_confirmatory_sonnet_swebench` | results/costs.json is missing or invalid |
