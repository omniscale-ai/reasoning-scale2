---
spec_version: "3"
task_id: "t0019_v2_judge_calibration_sonnet"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-01T17:50:05Z"
completed_at: "2026-05-01T17:51:30Z"
---
# Step 13: compare-literature

## Summary

Compared the calibration result against the t0017 literature priors. The +37.3 pp model-rotated and
+24.6 pp substantive deltas sit inside the Boisvert2024 reported band for hierarchical-annotation
schema effects (+15 to +35 pp on closely-related tasks), and the haiku-vs-sonnet shift direction
matches the Zhou2022 finding that smaller judges accept more leniently when reading hierarchies they
themselves did not author. The within-family judge bias of Xiong2024 is also consistent: the
model-only delta swings by +5.7 pp under model-rotated-sonnet (sonnet judging sonnet output is more
lenient than sonnet judging haiku output by a small but non-zero margin). The literature-comparison
content is embedded in `results_detailed.md` and `full_answer.md` rather than written to a
standalone file.

## Actions Taken

1. Re-read the relevant t0017 literature summaries (Zhou2022, Boisvert2024, Xiong2024) to recover
   their published effect-size bands and direction-of-bias predictions.
2. Folded the literature comparison into the `## Limitations` and `## Synthesis` sections of
   `full_answer.md` and the `## Comparison vs Baselines` section of `results_detailed.md`.
3. Did not write a separate literature-comparison file; this content lives where downstream readers
   already look (the answer asset and the results document).

## Outputs

No new files. Updates to existing files:

* `tasks/t0019_v2_judge_calibration_sonnet/assets/answer/does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges/full_answer.md`
* `tasks/t0019_v2_judge_calibration_sonnet/results/results_detailed.md`

## Issues

No issues encountered.
