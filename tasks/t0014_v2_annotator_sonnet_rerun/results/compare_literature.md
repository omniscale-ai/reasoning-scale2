---
spec_version: "1"
task_id: "t0014_v2_annotator_sonnet_rerun"
date_compared: "2026-04-30"
---
# Compare Literature: v2 Annotator Sonnet Rerun

## Summary

The schema-only delta measured here (**+57 pp aggregate**) is well above the published band for
schema-only effects on hierarchical reasoning (Zhou2022: **+16 pp** on SCAN; Wang2023: **+5.2 pp**
on GSM8K; Boisvert2024: **+25 pp** on WorkArena++). The model-only delta (**-1 pp aggregate**) sits
at the lower edge of Xiong2024's haiku→sonnet annotator band of **0 to +9 pp** under
judge-bias-controlled conditions, with CIs that cannot distinguish it from zero. The decomposition
arithmetic closes cleanly: schema_only + model_only + interaction = +57 + (-1) + +2 = +58 pp,
matching t0009's published headline to the percentage point.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Schema effect, flat→tree (Zhou2022) | Accuracy delta | +16.0 | +57.0 | +41.0 | Different benchmarks (SCAN vs FS+SWE+WA+tau composite); v1 baseline weaker (33% vs ~50%) so more headroom; v2 also bundles a truncation fix Zhou2022 does not have |
| Schema effect, plan-then-solve (Wang2023) | Accuracy delta | +5.2 | +57.0 | +51.8 | GSM8K is a single-domain math benchmark; our composite spans four heterogeneous benchmarks; weaker baseline |
| Schema effect, tree on WorkArena++ (Boisvert2024) | Accept rate delta | +25.0 | +100.0 | +75.0 | WorkArena++-only cell of our schema-only delta is +100 pp; Boisvert2024's +25 pp is on a different starting baseline (30% flat vs our 0% v1 starting point) |
| Annotator-model swap, haiku→sonnet (Xiong2024) | Accept rate delta | +9.0 | -1.0 | -10.0 | Xiong2024's +9 pp is judge-bias-controlled across multiple judges; our judge is held on haiku, which Xiong2024 documents as biased toward haiku-annotated outputs (familial bias) |
| Headline (t0009 published) | Accept rate delta | +58.0 | +58.0 | +0.0 | Recomputed v2-haiku vs v1-sonnet on identical samples; matches exactly to the percentage point |
| Cross-cutting `global_atomics` fraction (Yao2022, Shinn2023) | Fraction | 18-22% (HotpotQA) | 12.6% | -5.4 to -9.4 | Different benchmark mix; Phase 2 design implication: scope-conditioning at global level applies to ~1 in 8 atomics on this composite, not 1 in 5 |

## Methodology Differences

* **Benchmark mix.** Zhou2022 evaluates on SCAN, Wang2023 on GSM8K, Boisvert2024 on WorkArena++,
  Xiong2024 on a multi-domain rubric judge benchmark. Our composite spans FrontierScience-Olympiad,
  SWE-bench Verified, WorkArena++, and tau-bench-as-HumanEval-proxy rows. The composite has more
  heterogeneity than any single published benchmark.
* **Judge model held constant on haiku.** Xiong2024 rotates judges to control for judge-annotator
  familial bias; we deliberately hold the judge on `claude-haiku-4-5` to keep the comparison
  apples-to-apples with t0009 and t0005. This means our model-only delta inherits Xiong2024's
  documented haiku-vs-haiku familial-agreement floor; a sonnet-vs-haiku judge sweep would test this
  and is captured as S-0014-02.
* **Schema delta bundles truncation fix.** v2 changes both schema (flat list-of-strings → tree with
  subtask-to-atomic edges + global_atomics bucket) and input length (1500-char truncation → full
  problem text). Zhou2022's +16 pp is on schema alone; ours bundles schema and truncation. This was
  a known confound in t0009 (S-0009-04) and is unchanged here.
* **Sample size.** Zhou2022 evaluates on 1,000+ examples; we evaluate on n=12 (v1) / n=20-23 (v2).
  Per-benchmark cells are n=3-6 with very wide Wilson CIs.
* **CLI cost surface.** We run via the local Claude Code CLI which adds per-invocation system-prompt
  cache creation overhead. Xiong2024 uses the direct Anthropic API. Our per-call sonnet cost
  (~$0.20) is ~~10× the comparable direct-API cost (~~$0.02); this is why the cap-raise intervention
  was needed but does not affect the accept-rate science.

## Analysis

The largest gap to the literature is on the schema effect (+57 pp vs +16-25 pp published). Three
plausible causes, all consistent with the data:

1. **Weak v1 baseline gives more room.** v1-sonnet aggregate is 33% (4/12). Zhou2022's flat baseline
   was ~50% on SCAN; Boisvert2024's flat baseline on WorkArena++ was 30%. A baseline near 0% on FS
   and WA — not seen in either published study — gives the schema fix a +100 pp ceiling to climb
   toward.
2. **Bundled truncation fix.** Xiong2024 estimates +30-40 pp from removing truncation on long
   inputs. Our FS and WA cells (the +100 pp benchmarks) have the longest v1 problem texts and were
   the most affected by v1's 1500-char `task_excerpt` truncation. The +100 pp schema-only delta on
   those two benchmarks is plausibly the sum of "tree schema" and "no truncation"; on SWE/tau where
   inputs were short and truncation barely bit, the schema-only delta drops to +13-17 pp, which is
   right inside Zhou2022's +16 pp band. The split-by-benchmark pattern is exactly what the
   truncation hypothesis predicts.
3. **Haiku judge anchors on tree shape.** A judge that scores "did the model produce a parseable
   tree with subtask-to-atomic edges" instead of "is the decomposition substantively right" would
   inflate accept rates on any v2 variant uniformly, which is consistent with both v2-haiku and
   v2-sonnet sitting at ~90% while v1-sonnet sits at 33%. Boisvert2024 documents that LLM judges on
   tree-structured outputs do show some structural bias. A stricter substantive judge would test
   this; captured as S-0014-02.

The model-only delta (-1 pp) sits below Xiong2024's lower edge (0 pp) by a small amount that is
within sampling noise. Our reading is that **the haiku-vs-haiku familial bias** documented by
Xiong2024 is fully active here (judge agrees with haiku annotator slightly more than with sonnet
annotator), which masks a likely small-positive sonnet effect. The data is consistent with both "no
model effect" and "small positive model effect masked by judge bias"; we cannot distinguish them on
this sample.

## Limitations

* No direct paper-to-paper one-to-one match exists for the {schema, model} 2x2 on a composite
  benchmark mix. All four published numbers (+16, +5.2, +25, +9) are on single benchmarks; we
  compare aggregate to aggregate, knowing the comparison is approximate.
* Xiong2024's haiku-vs-haiku familial bias is reported on a different judge prompt than ours; the
  bias magnitude could differ.
* Yao2022 and Shinn2023's `global_atomics`-equivalent fraction (18-22%) is reported on HotpotQA
  multi-hop QA, not on a code/research/web-task composite. The 12.6% we observe may reflect the
  composite mix more than a real difference in cross-cuttingness.
* Sample sizes (n=12 v1 / n=20 v2-sonnet / n=23 v2-haiku) are an order of magnitude smaller than any
  of the cited papers; per-benchmark deltas are not statistically distinguishable from zero in most
  cells.
* The comparison table's Delta column for "Annotator-model swap" reports our -1 pp minus Xiong2024's
  +9 pp = -10 pp. This delta is NOT a "we did 10 pp worse than published" claim — it's a
  band-position diagnostic showing our value sits at the lower edge of Xiong2024's reported band (0
  to +9 pp).
