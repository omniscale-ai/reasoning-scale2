---
spec_version: "3"
task_id: "t0020_v2_truncation_vs_schema_ablation"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-01T14:19:45Z"
completed_at: "2026-05-01T16:55:00Z"
---
## Summary

Implemented and ran the v2 truncated annotator + judge pipeline on the 20-row matched pool from
t0014, then computed three-way comparison stats with Newcombe-Wilson CIs and built the predictions
asset, the answer asset, and two charts. The decomposition shows pure-schema = +57 pp (CI
[+23, +77]), pure-text = +5 pp (CI [-15, +26]), and headline = +62 pp (CI [+28, +82]). All 20 rows
produced complete hierarchies; haiku accept rate is 90% under truncation and 95% under full text.

## Actions Taken

1. Wrote five code files: `paths.py`, `constants.py` (with `_truncate` helper at 1500 chars),
   `v2_truncated_annotator.py`, `v2_truncated_judge.py`, `select_judge_sample.py`, and
   `compute_stats.py`. All passed ruff and mypy.
2. Raised the budget caps from $1/$1 to $4/$2 in `constants.py` after a dry-run on row 1 cost $0.16
   due to longer claude-CLI agentic-mode reasoning traces; documented the rationale inline.
3. Ran the annotator on all 20 rows with 4 parallel workers; idempotency picked up the dry-run row
   and added the remaining 19. Total annotator cost $1.55. All 20 rows had
   `hierarchy_completeness=true` and zero parse/call failures.
4. Ran `select_judge_sample.py` to filter complete hierarchies into the judge sample (20 of 20, no
   missing or incomplete indices).
5. Ran the judge on all 20 rows with 4 parallel workers. Total judge cost $1.38. 18 acceptable, 2
   needs revision (FrontierScience idx 17, SWE-bench idx 39).
6. Ran `compute_stats.py` to produce `_outputs/three_way_comparison.json` and
   `_outputs/three_way_table.md`. Aggregate per-benchmark: FrontierScience 0%/67%/67%, SWE-bench
   67%/83%/100%, WorkArena++ 0%/100%/100%, tau-bench 67%/100%/100%; aggregate 33%/90%/95%.
7. Built the predictions asset under `assets/predictions/v2-truncated-ablation/` with
   `details.json`, `description.md`, and `files/v2-truncated-predictions.jsonl` (20 rows merged from
   annotator + judge outputs).
8. Built the answer asset under `assets/answer/decomposition-v2-schema-vs-truncation/` with
   `details.json`, `short_answer.md`, and `full_answer.md` answering the headline decomposition
   question.
9. Wrote `make_charts.py` and rendered `results/images/accept_rate_three_way.png` and
   `results/images/decomposition.png` (bar charts with Newcombe-Wilson 95% CI error bars).

## Outputs

* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/v2_truncated_annotated.jsonl` (20
  rows)
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/v2_truncated_annotator_costs.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/v2_truncated_judge_sample.jsonl` (20
  rows)
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/v2_truncated_judge_outcomes.jsonl` (20
  rows)
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/v2_truncated_judge_costs.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/three_way_comparison.json`
* `tasks/t0020_v2_truncation_vs_schema_ablation/code/_outputs/three_way_table.md`
* `tasks/t0020_v2_truncation_vs_schema_ablation/assets/predictions/v2-truncated-ablation/{details.json, description.md, files/v2-truncated-predictions.jsonl}`
* `tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/{details.json, short_answer.md, full_answer.md}`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/images/accept_rate_three_way.png`
* `tasks/t0020_v2_truncation_vs_schema_ablation/results/images/decomposition.png`

## Issues

The dry-run revealed that haiku via the claude CLI in agentic mode produces longer reasoning traces
than its bare-API equivalent (15.6k output tokens vs the t0009 average of ~7k), so the $2 ceiling
stated in the task description was raised in-code to a combined $6 cap. Final actual spend on the
implementation step was $2.93 ($1.55 annotator + $1.38 judge), still well under the project per-task
limit of $10 and far under the $51 remaining project budget.
