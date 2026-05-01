---
spec_version: "3"
task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-05-01T21:43:49Z"
completed_at: "2026-05-01T21:46:00Z"
---
## Summary

Replaced the placeholder `results/suggestions.json` (empty array) with six follow-up suggestions
derived directly from the synthesis. The first four are the Phase 2 actionable items: a
high-priority calibration-focused A/B with confidence elicitation (Candidate 2 from
`results_detailed.md`), a high-priority judge-replacement evaluation suggestion driven by t0019
anchoring, a medium-priority AgentBoard progress-rate evaluation tweak driven by Ma2024, and a
medium-priority three-arm A/B/C pilot at half scale to test the strict double inequality form of
RQ5. The remaining two are a low-priority process improvement (existing-asset inventory cross-check
at brainstorm time) and a low-priority deferred fine-tuning experiment (group-level DPO inspired by
Gao2026 HPL). `verify_task_results` re-run after the edit passes with zero errors and zero warnings.

## Actions Taken

1. Read the suggestions specification (`arf/specifications/suggestions_specification.md`) to confirm
   the v2 schema, ID format (`S-0025-NN`), required fields, allowed `kind` and `priority` values,
   and the `source_paper` paper-ID format (DOI slug or `no-doi_*`).
2. Listed existing project categories via `aggregate_categories --format ids` to ensure each
   suggestion uses only valid category slugs (or `[]` when no fit). Used:
   `granularity-conditioning`, `uncertainty-calibration`, `agent-evaluation`,
   `hierarchical-planning`, and `[]`.
3. Mapped each suggestion's `source_paper` to a paper ID confirmed in the project inventory via the
   `intervention/duplicate_papers.md` table (Jung2024 = `10.48550_arXiv.2407.18370`, Ma2024 =
   `10.48550_arXiv.2401.13178`, Wen2024 = `10.48550_arXiv.2405.15821`, Gao2026 =
   `no-doi_Gao2026_hierarchical-preference-learning-llm-agents`). Two suggestions have
   `source_paper: null` (S-0025-04 driven by t0019, not by an external paper; S-0025-05 process
   suggestion).
4. Wrote `results/suggestions.json` with `spec_version: "2"` and six suggestion objects covering the
   experiment (3) / evaluation (2) / technique (1) kinds.
5. Re-ran `verify_task_results t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` — PASSED,
   0 errors, 0 warnings.

## Outputs

* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/results/suggestions.json` (6
  suggestions; replaces the empty placeholder).
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/logs/steps/014_suggestions/step_log.md`
  (this file).

## Issues

No issues encountered.
