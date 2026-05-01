---
spec_version: "1"
task_id: "t0025_lit_survey_hierarchical_agents_and_judges_2024_2026"
created_at: "2026-05-01T21:25:00Z"
resolved_at: "2026-05-01T21:55:00Z"
intervention_kind: "scope_conflict"
status: "resolved"
resolution: "user_redirected_to_synthesis_only"
---
# Intervention: All 10 Target Papers Already Exist in the Project

## Resolution (2026-05-01)

Researcher decision: pivot the task scope to **answering the project's Research Questions (RQ1-RQ5)
directly**, using the existing 10 paper summaries under
`tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md` plus the
prior project findings from t0014, t0019, t0020 as the evidence base. Drop the asset-addition half
of the task entirely.

This is a stronger version of the previously offered Option B:
* `task.json` `expected_assets` → `{}` (no new paper assets).
* `task.json` `task_types` keeps `["literature-survey"]` and adds `["answer-question"]` to reflect
  the RQ-answering deliverable.
* `task_description.md` rewritten to describe the RQ-by-RQ synthesis deliverable.
* Implementation step (step 9) writes `results/results_summary.md` and `results/results_detailed.md`
  structured around RQ1-RQ5, with explicit per-RQ verdicts (strong support / partial support / no
  direct evidence / contradictory) and residual-uncertainty notes flagging which RQs require Phase 2
  A/B/C empirical experiments still to be run.

The original three-option list below is preserved for audit purposes.

## Summary

The task `t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` was planned to add 10 paper
assets (`expected_assets: {"paper": 10}`). During the implementation step, a check via
`aggregate_papers` revealed that **all 10 target papers are already present in the project**, having
been added by an earlier task `t0017_literature_hierarchical_agents_and_judges`.

The `add-paper` skill explicitly forbids creating duplicate paper assets (Phase 1, Step 5: "If any
match is found, stop and report that the paper is already in the project"). All three pilot
sub-agents (papers 1, 2, 3) detected the duplicate and self-stopped without writing assets. The
remaining 7 papers will trigger the same duplicate stop.

## Evidence

Mapping of the 10 target titles to existing paper IDs (all under
`t0017_literature_hierarchical_agents_and_judges`):

| # | Title (target) | Existing paper_id | Citation key |
| --- | --- | --- | --- |
| 1 | Solving the Granularity Mismatch (ICLR 2026) | `no-doi_Gao2026_hierarchical-preference-learning-llm-agents` | Gao2026 |
| 2 | ArCHer (ICML 2024) | `10.48550_arXiv.2402.19446` | Zhou2024 |
| 3 | Reinforcing LLM Agents via Action Decomposition (NeurIPS 2024) | `10.48550_arXiv.2405.15821` | Wen2024 |
| 4 | Sutton, Precup & Singh 1999 (options framework) | `no-doi_Sutton1999_options-framework` | Sutton1999 |
| 5 | Can Graph Learning Improve Planning (NeurIPS 2024) | `10.48550_arXiv.2405.19119` | Wu2024 |
| 6 | LATS (ICML 2024) | `10.48550_arXiv.2310.04406` | Zhou2024a |
| 7 | SELF-DISCOVER (NeurIPS 2024) | `10.48550_arXiv.2402.03620` | Zhou2024b |
| 8 | Embodied Agent Interface (NeurIPS 2024) | `10.48550_arXiv.2410.07166` | Li2024 |
| 9 | AgentBoard (NeurIPS 2024 D&B) | `10.48550_arXiv.2401.13178` | Ma2024 |
| 10 | Trust or Escalate | `10.48550_arXiv.2407.18370` | Jung2024 |

## Why this happened

Brainstorm Session 7 (`t0024`) created `t0025` to refresh the project's reading on hierarchical
agents and LLM-as-judge methodology in light of the t0014, t0019, and t0020 findings (judge
anchoring on model identity, v2 schema effect collapse under stronger judges). However, the same
10-paper list was already added under `t0017_literature_hierarchical_agents_and_judges` before the
brainstorm session ran, and the brainstorm's task scoping did not check the existing paper
inventory.

The **synthesis writeup** that t0025 was meant to feed into Brainstorm Session 8 IS new work — the
post-t0014/t0019/t0020 perspective on these papers has never been written. But the asset-addition
half of the task is fully redundant.

## Decision Required

The researcher must choose one of the following resolutions:

### Option A — Cancel t0025 entirely

Set `task.json` status to `cancelled` with reason "10 target papers already exist; brainstorm
duplication". Brainstorm Session 8 will need to re-scope with awareness that the synthesis was never
produced.

### Option B — Re-scope t0025 to synthesis-only

Update `task.json`:
* `expected_assets`: change from `{"paper": 10}` to `{}` (no new assets).
* `task_types`: keep `["literature-survey"]` (still applicable; synthesis IS literature survey).
* `short_description`: update to reflect synthesis-only scope.

Re-scope `task_description.md` to:
* Remove the "add 10 paper assets" requirement.
* Keep all synthesis requirements (results_summary.md, results_detailed.md mapping to RQ1, RQ2, RQ4,
  RQ5; comparison table against t0014/t0019/t0020 findings).
* Use the existing 10 paper summaries under
  `tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/<paper_id>/summary.md` as the
  source material for the synthesis.

Then continue execution from the implementation step with synthesis as the only deliverable.

### Option C — Keep adding the papers under t0025 anyway

This option violates the project's no-duplication principle and the `add-paper` skill's
duplicate-stop rule. **Not recommended.** It would also require modifying the verificator behavior,
which is out of scope for a task branch.

## Recommendation

**Option B** is the cleanest fit for the task's stated goal. The task description's own motivation
section ("brings the project's reading current with 2024-2026 work ... synthesis section is intended
to feed directly into Brainstorm Session 8") is satisfied by re-scoping to synthesis-only.

## Files Affected on the Task Branch So Far

* `plan/plan.md` (revised to use existing-categories-only mapping; this revision is still useful
  under Option B).
* `step_tracker.json` (implementation step marked `in_progress` by prestep).
* `logs/steps/008_implementation/` (will not exist until poststep runs; currently work-in-progress).

No paper asset folders were written under `tasks/t0025_*/assets/paper/`.

## Next Action After Researcher Decision

Once the researcher picks an option, the orchestrator will:
* Option A: set task status to `cancelled`, run poststep on implementation as `skipped`, push
  branch, open a brief PR documenting the cancellation, and merge.
* Option B: edit `task.json`, edit `task_description.md`, write step_log for implementation, then
  resume by writing the synthesis documents using t0017's existing summaries as input.
* Option C: not implementable on a task branch; would require a framework change.
