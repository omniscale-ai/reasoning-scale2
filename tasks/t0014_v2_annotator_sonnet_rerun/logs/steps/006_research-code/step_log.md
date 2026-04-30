---
spec_version: "3"
task_id: "t0014_v2_annotator_sonnet_rerun"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-04-30T19:14:10Z"
completed_at: "2026-04-30T19:38:00Z"
---
# Step 6: research-code

## Summary

Surveyed the project's library landscape (4 libraries, 0 relevant), then read every t0009 code
module that produced the v2 dataset asset to inventory exactly what t0014 must copy and what it must
change. Produced `research/research_code.md` with the seven mandatory sections, identifying 8
reusable code files and the precise constant changes (annotator model -> sonnet, budget cap -> $10)
that distinguish t0014 from t0009.

## Actions Taken

1. Ran `aggregate_libraries --format ids` and confirmed the four registered libraries
   (`scope_aware_react_v1`, `scope_unaware_planandsolve_v1`, `matched_mismatch_v1`,
   `metric2_calibration_aggregator_v1`) are unrelated to annotation/judge work; t0014 reuses zero
   libraries.
2. Read t0009's full code suite: `v2_annotator.py` (615 lines), `v2_judge.py` (459 lines),
   `select_judge_sample.py` (86 lines), `build_v2_asset.py` (358 lines), `compute_stats.py` (196
   lines), `make_charts.py` (105 lines), `constants.py` (128 lines), `paths.py` (31 lines).
3. Read t0009's `assets/dataset/hierarchical-annotation-v2/details.json` and t0005's
   `hierarchical-annotation-v1/details.json` to confirm the v1 input file path and schema.
4. Read t0009's `results/results_summary.md` to capture the v2-haiku reference accept rates per
   benchmark.
5. Cross-checked t0005 to confirm the v1 annotator was `claude-sonnet-4-6` and the v1 judge was
   `claude-haiku-4-5-20251001` (same haiku family as t0009's judge), validating the t0014
   experimental design.
6. Wrote `research/research_code.md` covering: Task Objective, Library Landscape, five
   topic-organised Key Findings subsections, an 8-row Reusable Code table with adaptation notes and
   line counts, six Lessons Learned bullets, eight prioritised Recommendations ending with the
   v3-schema vs sonnet-default decision branch, and a Task Index of 8 cited tasks (t0002, t0005,
   t0006, t0007, t0009, t0010, t0011, t0012).
7. Ran `verify_research_code` -- initial run reported four `RC-E006` errors (unmatched `[t0006]`,
   `[t0007]`, `[t0010]`, `[t0014]` citations). Added Task Index entries for t0006/t0007/t0010
   (libraries cited in Library Landscape), removed the self-reference `[t0014]` (replaced with "this
   task"), and bumped frontmatter `tasks_reviewed: 7 -> 9`, `tasks_cited: 5 -> 8`. Re-ran
   verificator -- passed cleanly.
8. Ran `flowmark --inplace --nobackup` on the file; verificator still passed afterwards.

## Outputs

* `tasks/t0014_v2_annotator_sonnet_rerun/research/research_code.md`
* `tasks/t0014_v2_annotator_sonnet_rerun/logs/steps/006_research-code/step_log.md`

## Issues

No blocking issues. The four citation errors during draft were all fixed before commit.
