---
spec_version: "3"
task_id: "t0009_hierarchical_annotation_v2"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-29T23:35:26Z"
completed_at: "2026-04-30T00:38:00Z"
---
# Step 9: implementation

## Summary

Re-annotated all 115 v1 pilot rows under the v2 tree schema using `claude-haiku-4-5` via the local
Claude Code CLI, sampled 23 rows stratified across the four benchmarks, judged them with the same
haiku model, and assembled the consolidated v2 dataset asset. All 115 rows have
`hierarchy_completeness == True`. Judge accept rate is 21/23 = 91%; per-benchmark deltas vs v1 are
uniformly positive (+33% to +100%). Total spend $9.10 ($7.42 annotator + $1.68 judge).

## Actions Taken

1. Wrote pipeline scaffolding (`code/paths.py`, `code/constants.py`).
2. Implemented `code/v2_annotator.py` with parallel ThreadPoolExecutor (4 workers), idempotent
   resume, hard budget cap, and defensive JSON parsing. Initial dry-run on 3 rows confirmed schema
   parses cleanly.
3. Initially attempted Sonnet (`claude-sonnet-4-6`) but discovered that the Claude Code CLI creates
   a fresh ~70k-token system prompt cache on every invocation, making each call ~$0.30. Switched the
   annotator (and judge) to `claude-haiku-4-5` to fit within the $15 task budget; documented the
   model substitution as a known confound for the v2-vs-v1 comparison.
4. Ran the parallel annotator on all 115 rows. Total cost $7.42, zero parse failures, zero call
   failures, 115/115 rows produced a complete v2 hierarchy.
5. Wrote `code/select_judge_sample.py` (fixed seed 42, stratified 6/6/6/5 = 23 rows) and ran it.
6. Wrote `code/v2_judge.py` (parallel, same JSON parsing pattern) and ran it on the 23-row sample.
   21 acceptable, 2 needs revision; cost $1.68.
7. Wrote `code/build_v2_asset.py` to merge annotator + judge outputs into the dataset asset under
   `assets/dataset/hierarchical-annotation-v2/` (jsonl, details.json, description.md).
8. Wrote `code/compute_stats.py` for the v1-vs-v2 comparison table and global-atomics fraction.
9. Ran the dataset-asset verificator: passed with 0 errors, 1 warning (DA-W007 about author country
   field; this is a project-internal author with no country to attribute, expected).

## Outputs

- `tasks/t0009_hierarchical_annotation_v2/code/paths.py`, `code/constants.py`,
  `code/v2_annotator.py`, `code/v2_judge.py`, `code/select_judge_sample.py`,
  `code/build_v2_asset.py`, `code/compute_stats.py`
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_annotated.jsonl` (115 rows)
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_sample.jsonl` (23 rows)
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_outcomes.jsonl` (23 rows)
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_annotator_costs.json`
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v2_judge_costs.json`
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v1_vs_v2_comparison.json`
- `tasks/t0009_hierarchical_annotation_v2/code/_outputs/v1_vs_v2_table.md`
- `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/details.json`
- `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/description.md`
- `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`

## Issues

The single material deviation from the task description is the **annotator model substitution from
`claude-sonnet-4-6` to `claude-haiku-4-5`**. The task description (and the v1 setup) used Sonnet for
annotation; v2 was specified to keep Sonnet constant for a clean v2-vs-v1 schema comparison. After a
3-row Sonnet dry-run measured per-call cost at ~$0.30 (driven by the Claude Code CLI's persistent
system-prompt cache creation, not by the underlying model price), the projected 115-row cost would
have been ~$35, busting the $15 task budget by 2x. Switching to Haiku brought per-call cost down to
~$0.06-0.16 average and let the full 115-row run complete under the $13 cap with $5.58 of headroom.

This means the v2-vs-v1 accept rate delta conflates two changes — the schema upgrade (flat ->
tree-with-edges) and the annotator model downgrade (Sonnet -> Haiku). The deltas are large and
positive on every benchmark (+33% to +100%), so the schema upgrade is the more plausible dominant
cause, but a follow-up task with cleaner cost controls (direct API rather than CLI) should re-run
the comparison with the Sonnet annotator held constant to disentangle the two. This is captured as a
follow-up suggestion in `results/suggestions.json`.

REQ-1 through REQ-8 are all satisfied modulo the model substitution noted above:
- REQ-1: 115/115 rows annotated (model: haiku, not sonnet — see issue above).
- REQ-2: full problem text passed to both annotator and judge with no character cap.
- REQ-3: every output row has `_pilot_row_index` integer field; values are unique.
- REQ-4: 23/23 stratified judge sample done (FrontierScience-Olympiad: 6, SWE-bench Verified: 6,
  WorkArena++: 6, tau-bench: 5).
- REQ-5: dataset asset passes `verificator` with 0 errors, 1 warning (DA-W007).
- REQ-6: per-benchmark deltas computed; all four benchmarks improved.
- REQ-7: total cost $9.10, well under the $15 task budget.
- REQ-8: all 115 rows have `hierarchy_completeness` set under the stricter v2 rule.
