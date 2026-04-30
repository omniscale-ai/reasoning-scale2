---
spec_version: "3"
task_id: "t0014_v2_annotator_sonnet_rerun"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-30T23:48:00Z"
completed_at: "2026-04-30T23:55:00Z"
---
# Step 14: suggestions

## Summary

Wrote `results/suggestions.json` with five follow-up suggestions (S-0014-01 through S-0014-05) all
of which explicitly cite the schema-only +57 pp and model-only -1 pp deltas as their motivation.
This satisfies plan REQ-11 ("at least one suggestion that explicitly cites the schema-only and
model-only deltas") and answers plan task description Key Question 4 ("If the schema component is
small, is there a v3 schema change worth scoping?") with the inversion: the schema component is
*large*, so a v3 schema iteration is motivated by the bimodal per-benchmark split (S-0014-01) and a
sonnet-default annotation policy is *not* justified (S-0014-04).

## Actions Taken

1. Re-read `results/results_summary.md` (90% v2-sonnet, +57 pp schema-only, -1 pp model-only),
   `results/compare_literature.md` (band positions vs Zhou2022, Boisvert2024, Xiong2024), and
   `logs/steps/011_creative-thinking/step_log.md` (stricter-judge stress test framing).
2. Mapped each suggestion to a load-bearing decomposition finding:
   * S-0014-01 (v3 schema iteration) — cites the bimodal +100 vs +13-17 pp per-benchmark schema-only
     split. The +100 pp benchmarks suggest the v2 schema converts unsolvable v1 outputs; the +13-17
     pp ones suggest a real but modest improvement on already-adequate benchmarks. v3 should target
     SWE/tau-style structured-action tasks specifically (e.g., precondition/postcondition fields).
   * S-0014-02 (stricter substantive judge) — cites the +57 pp vs Zhou2022's +16 pp gap. Tests the
     judge-anchoring-on-tree-shape hypothesis from the creative-thinking step.
   * S-0014-03 (rotate judge to sonnet) — cites the model-only -1 pp vs Xiong2024's 0-9 pp band.
     Tests the haiku-vs-haiku familial bias hypothesis from the literature comparison.
   * S-0014-04 (haiku-default annotation policy) — cites the -1 pp model-only delta and the 10x cost
     ratio. Direct policy implication for Phase 2 budgeting.
   * S-0014-05 (re-run FS timeouts) — cites the n=3 vs n=6 sample-size asymmetry on FrontierScience
     between v2-sonnet and v2-haiku, which weakens the +33 pp FS model-only delta.
3. Used kinds: `experiment` (S-0014-01, S-0014-03, S-0014-05), `evaluation` (S-0014-02), `technique`
   (S-0014-04). Priorities: high for S-0014-02 / S-0014-03 / S-0014-04 (each has direct Phase 2
   policy implications); medium for S-0014-01 / S-0014-05 (scoping work and small recovery).
4. Used categories from `meta/categories/` only: `hierarchical-planning`, `benchmark-annotation`,
   `agent-evaluation`, `benchmark-frontierscience`.
5. All `source_task` fields set to `t0014_v2_annotator_sonnet_rerun`. All `source_paper` fields set
   to `null` (none of the suggestions are derived from a single paper).
6. Ran `verify_suggestions t0014_v2_annotator_sonnet_rerun`: **PASSED** with 0 errors, 0 warnings.

## Outputs

* `tasks/t0014_v2_annotator_sonnet_rerun/results/suggestions.json`

## Issues

None. All five suggestions cite specific delta magnitudes and propose concrete next-step experiments
with cost estimates.
