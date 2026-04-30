---
spec_version: "3"
task_id: "t0014_v2_annotator_sonnet_rerun"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-04-30T23:40:00Z"
completed_at: "2026-04-30T23:48:00Z"
---
# Step 13: compare-literature

## Summary

Wrote `results/compare_literature.md` comparing the t0014 schema-only and model-only deltas against
the four most relevant published findings: Zhou2022 (+16 pp schema effect on SCAN), Wang2023 (+5.2
pp plan-then-solve on GSM8K), Boisvert2024 (+25 pp tree-schema on WorkArena++), and Xiong2024 (+9 pp
haiku→sonnet annotator under judge-bias-controlled conditions). Also compared against the internal
t0009 +58 pp headline (recomputed exactly here) and Yao2022/Shinn2023's `global_atomics` fraction
(18-22% on HotpotQA). The compare doc is the single literature deliverable for this task.

## Actions Taken

1. Re-read t0009's `compare_literature.md` for structure and citation reuse. Pulled the four primary
   published-value anchors that t0009 used (Zhou2022, Wang2023, Boisvert2024, Xiong2024), then added
   the t0009 headline as the cross-check row and Yao2022/Shinn2023 as the cross-cutting
   `global_atomics` reference.
2. Built the comparison table with six rows. Each row includes published value, our value, delta,
   and a one-line note explaining whether the comparison is apples-to-apples or which knobs differ
   (benchmark mix, baseline strength, judge model, sample size).
3. Wrote the Methodology Differences section covering five axes: benchmark mix (SCAN/GSM8K/WA vs our
   four-benchmark composite), judge held constant on haiku (vs Xiong2024's rotated judges), schema
   delta bundles truncation fix (v2 changed both schema and `task_excerpt` length — inherited
   confound from t0009 S-0009-04), sample size (n=12 / n=20-23 vs 1,000+ in published studies), and
   CLI cost surface (per-call cache overhead).
4. Wrote the Analysis section explaining why our schema-only +57 pp is well above the published
   +16-25 pp band. Three plausible causes, all consistent with the per-benchmark split:
   * Weak v1 baseline (33% aggregate; 0% on FS and WA) gives more headroom than Zhou2022's 50% SCAN
     baseline or Boisvert2024's 30% WA baseline.
   * Bundled truncation fix: the +100 pp benchmarks (FS and WA) are the ones where v1's 1500-char
     truncation bit hardest. SWE/tau, where inputs were short, drop to +13-17 pp — right inside
     Zhou2022's +16 pp band. This split-by-benchmark pattern is what the truncation hypothesis
     predicts.
   * Haiku judge may anchor on tree shape rather than substantive correctness — would inflate v2
     accept rates uniformly. Captured for follow-up as S-0014-02.
5. Documented why the model-only -1 pp sits below Xiong2024's lower edge (0 pp): haiku-vs-haiku
   familial bias documented by Xiong2024 is fully active here because we deliberately held the judge
   on haiku to keep apples-to-apples with t0009/t0005. Sample size cannot distinguish "no model
   effect" from "small positive model effect masked by judge bias".
6. Wrote the Limitations section flagging that no published paper does the {schema, model} 2x2 on a
   composite benchmark mix, and clarified that the -10 pp delta in the model-only row is NOT a "we
   did 10 pp worse" claim — it's a band-position diagnostic.
7. Confirmed the decomposition arithmetic in the Summary section: schema_only + model_only +
   interaction = +57 + (-1) + +2 = +58 pp, matches t0009's published headline exactly.

## Outputs

* `tasks/t0014_v2_annotator_sonnet_rerun/results/compare_literature.md`

## Issues

None. The literature comparison is approximate by necessity (composite benchmark vs single-benchmark
publications) but the per-benchmark split makes the truncation-fix hypothesis falsifiable in a
follow-up task; captured as S-0014-02 / S-0014-03 in step 14.
