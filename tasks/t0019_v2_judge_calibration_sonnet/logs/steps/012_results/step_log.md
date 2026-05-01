---
spec_version: "3"
task_id: "t0019_v2_judge_calibration_sonnet"
step_number: 12
step_name: "results"
status: "completed"
started_at: "2026-05-01T17:39:45Z"
completed_at: "2026-05-01T17:50:00Z"
---
# Step 12: results

## Summary

Wrote `results/results_summary.md` and `results/results_detailed.md` (spec v2) covering the 9-cell
accept-rate matrix, schema-only and model-only deltas under the three judge configurations,
Cohen's-kappa agreement between judge configs, the two charts produced in step 9, an Examples
section with 10 disagreement rows (mandatory for `comparative-analysis` + `data-analysis` task
types), explicit Verification, Limitations, Files Created, and the Task Requirement Coverage section
mapping REQ-1..REQ-12 to status, direct answer, and evidence path. The `metrics.json` multi-variant
file produced in step 9 was not modified here; only its variant-id format was patched during step-15
verification when TM-E003 surfaced.

## Actions Taken

1. Drafted `results_summary.md` with headline finding (substantive +24.6 pp, model-rotated +37.3 pp
   vs t0014 baseline +58.0 pp).
2. Drafted `results_detailed.md` with spec-v2 mandatory sections plus the Examples section triggered
   by the `comparative-analysis` and `data-analysis` task types: 10 rows with full system prompts,
   raw verdict + justification JSON snippets from each judge config, and pattern notes (7/10 = haiku
   rejects + both sonnet judges accept; 1/10 substantive prompt adds strictness; 2/10 same-model
   prompt-driven flips on structural-but-executable trees).
3. Ran `uv run flowmark --inplace --nobackup` on both files.
4. Verified embeds for `accept_rate_3x3.png` and `schema_only_delta_by_judge.png` resolve to the
   files produced in step 9.

## Outputs

* `tasks/t0019_v2_judge_calibration_sonnet/results/results_summary.md`
* `tasks/t0019_v2_judge_calibration_sonnet/results/results_detailed.md`

## Issues

No issues at this step. Verificator-driven fixes to `metrics.json` variant-id format,
`assets/answer/.../details.json` answer_methods value, and `full_answer.md` evidence-section word
counts were applied in step 15 (reporting) when verificators surfaced TM-E003, AA-E006, and AA-W003.
