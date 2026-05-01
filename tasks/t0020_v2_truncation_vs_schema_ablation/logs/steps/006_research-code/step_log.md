---
spec_version: "3"
task_id: "t0020_v2_truncation_vs_schema_ablation"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-01T14:09:43Z"
completed_at: "2026-05-01T14:15:00Z"
---
# Research Code Step Log

## Summary

Reviewed the t0005, t0009, and t0014 annotator and judge code to confirm the exact code structure
that needs to be replicated and the precise location of the 1500-char truncation logic. Established
that the v1 baseline uses `JUDGE_PROBLEM_EXCERPT_LIMIT = 1500` with a `_truncate(text, limit)`
helper, and that the t0014 pipeline is the most complete v2 implementation to copy. Confirmed
sample-pool alignment: 20 sonnet-judged rows are a subset of the 23 haiku-judged rows, enabling
paired comparison.

## Actions Taken

1. Read `tasks/t0005_hierarchical_annotation_pilot_v1/code/{constants.py,judge_runner.py}` to
   identify the canonical truncation pattern (`JUDGE_PROBLEM_EXCERPT_LIMIT: Final[int] = 1500`,
   `_truncate(text, *, limit) -> text[:limit] + "…"`).
2. Read
   `tasks/t0014_v2_annotator_sonnet_rerun/code/{constants.py,v2_annotator.py,v2_judge.py, select_judge_sample.py,compute_stats.py}`
   to capture the full pipeline structure.
3. Aligned the sample pools by checking `_pilot_row_index` overlap between t0014's 20 sonnet judged
   rows and t0009's 23 haiku judged rows; confirmed sonnet ⊂ haiku (haiku\\sonnet = `{7, 8, 14}`).
4. Ran `aggregate_libraries` to confirm no existing libraries are reusable for this task.
5. Wrote `research/research_code.md` and ran `verify_research_code` (passed with one warning about
   in-progress t0019 not existing on this branch).

## Outputs

* `tasks/t0020_v2_truncation_vs_schema_ablation/research/research_code.md`

## Issues

No issues encountered. The verificator warning RC-W002 (t0019 task not existing) is expected; t0019
is in progress on a parallel worktree.
