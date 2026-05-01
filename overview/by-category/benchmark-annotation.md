# Category: Benchmark Annotation

Manual or LLM-assisted gold-action annotation across the three granularity levels.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (1)](../papers/by-category/benchmark-annotation.md) | [Answers
(1)](../answers/by-category/benchmark-annotation.md) | [Suggestions
(22)](../suggestions/by-category/benchmark-annotation.md) | [Datasets
(4)](../datasets/by-category/benchmark-annotation.md) | [Predictions
(1)](../predictions/by-category/benchmark-annotation.md)

---

## Papers (1)

<details>
<summary>📋 <strong>Introducing SWE-bench Verified</strong> — team, 2024</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_OpenAI2024_swe-bench-verified` |
| **Authors** | OpenAI Preparedness team |
| **Venue** | OpenAI technical card (institutional, not peer-reviewed) (technical_report) |
| **DOI** | — |
| **URL** | https://openai.com/index/introducing-swe-bench-verified/ |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-swebench`](../../meta/categories/benchmark-swebench/), [`benchmark-annotation`](../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/no-doi_OpenAI2024_swe-bench-verified/summary.md) |

SWE-bench Verified is a 500-instance human-validated subset of SWE-bench produced by OpenAI's
Preparedness team in collaboration with the original SWE-bench authors. The motivation is that
the parent benchmark of 2,294 problems contains some items with ambiguous issue descriptions
or flaky tests, which add noise to capability measurements at the frontier.

Methodologically, 93 expert software engineers each reviewed candidate problems on three axes:
(a) clear instructions, (b) correct test patches, (c) reproducible environments. Three
independent reviewers per problem; only problems passing all three axes from all three
reviewers were included. The harness, Docker images, and resolve@1 scoring are identical to
the parent benchmark.

The headline outcome is that Verified has become the de facto standard subset for measuring
frontier autonomous-software-engineering capability in 2024-2026. Modern models score far
above the parent benchmark's 1.96% Claude 2 baseline — Claude Mythos Preview leads at
**93.9%** (April 2026). OpenAI's own April 2026 commentary noted that this saturation may
limit Verified's usefulness as a frontier-capability measurement going forward.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the Phase 2 composite benchmark. Its 500-instance size is tractable
for multiple-condition evaluation, the human validation removes benchmark noise, and
stratified reporting is essential because Verified's >90%-achievable ceiling would otherwise
drown out FrontierMath's <2% baseline. The project should plan a fallback to SWE-bench
Multimodal or SWE-bench Pro if Verified saturates further before Phase 2 completes.

</details>

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (1)

<details>
<summary><strong>How much of the +57 pp v2-tree-full vs v1-flat-truncated
acceptance-rate gap on the matched t0014 pool is due to the v2 tree schema
itself versus the full (untruncated) problem text?</strong></summary>

**Confidence**: medium | **Date**: 2026-05-01 | **Full answer**:
[`decomposition-v2-schema-vs-truncation`](../../tasks/t0020_v2_truncation_vs_schema_ablation/assets/answer/decomposition-v2-schema-vs-truncation/)

The v2 tree schema explains essentially all of the gap: switching from flat-v1 to tree-v2
while holding the 1500-char truncation constant lifts the haiku judge accept rate from 33% to
90%, a +57 pp jump (95% Wilson CI on the difference: +23 pp to +77 pp). Adding the full
untruncated problem text on top of the v2 schema lifts accept from 90% to 95%, a further +5 pp
(95% CI -15 pp to +26 pp), which is not statistically significant. The headline +62 pp v2-full
vs v1-truncated gap is therefore ~92% pure-schema and ~8% pure-text-length on the 20-row
matched pool.

</details>

## Suggestions (16 open, 6 closed)

<details>
<summary>🧪 <strong>Re-judge the remaining 8 v1 paired rows to tighten the
pure-schema CI</strong> (S-0020-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

The pure-schema delta CI (+22.5 to +77.5 pp) is dominated by the v1 sample size (n=12) because
t0005 only judged 12 of the 20 paired rows in its subsampled pool. Re-running the t0005 v1
judge on the remaining 8 paired indices (rows that t0014 judged but t0005 did not) would
extend v1 from n=12 to n=20 with no new annotation calls and tighten the pure-schema CI from a
half-width of ~28 pp to ~14 pp. Cost is ~8 haiku judge calls (~$0.50). This is the cheapest
possible follow-up that materially improves statistical power.

</details>

<details>
<summary>🧪 <strong>Scale the truncated-v2 condition to n=80 to detect a true +5 pp
pure-text effect if it exists</strong> (S-0020-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

The pure-text delta on this run is +5 pp with a CI of [-15, +26] pp at n=20. To resolve
whether the true pure-text effect is zero, +5 pp, or larger, the experiment needs n>=80 per
condition (Newcombe-Wilson half-width drops to ~10 pp at n=80 vs ~20 pp at n=20). This
requires running the v2 annotator and judge on 60 additional matched rows from the same
hierarchical-annotation-v1 source dataset, with both truncated and full conditions. Estimated
cost: 60 haiku annotations + 120 haiku judge verdicts at ~$0.07/call = ~$13. The result would
either confirm the schema-dominance claim with tight bounds or upgrade pure-text to a
meaningful contributor.

</details>

<details>
<summary>🧪 <strong>Truncation-budget sweep to map the marginal value of additional
context</strong> (S-0020-04)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

t0020 shows 1500 chars is sufficient on 3 of 4 benchmarks but loses ~17 pp on SWE-bench
Verified. A finer truncation grid (500 / 1000 / 1500 / 2500 / 5000 / full) on a
SWE-bench-heavy pool would map where the marginal value of additional context drops to zero.
This is a single-condition sweep (v2 schema held constant; only the truncation budget varies)
so the cost scales linearly with the number of budget points. Estimated cost: 6 budgets x 20
SWE-bench rows x 2 calls per row x ~$0.07 = ~$17.

</details>

<details>
<summary>📊 <strong>Cost-quality Pareto chart across t0009/t0014/t0020 to inform
downstream task budgets</strong> (S-0020-05)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0020_v2_truncation_vs_schema_ablation](../../tasks/t0020_v2_truncation_vs_schema_ablation/)

Three conditions now exist on the same 20-row pool: v1-flat-truncated (cheap, low quality),
v2-tree-truncated (cheap, high quality), v2-tree-full (expensive, slightly higher quality). A
Pareto chart with cost-per-row on the x-axis and accept rate on the y-axis would crisply
communicate that v2-tree-truncated is on the Pareto frontier and v2-tree-full is dominated by
it once the +5 pp gain is weighed against the ~2x cost. Useful as input to the t0022 ABC
harness budget planning.

</details>

<details>
<summary>🔧 <strong>Add a gold_actions structural-mirror validator for non-empty
global_atomics</strong> (S-0009-02)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

The two needs-revision rows on FrontierScience-Olympiad both failed for the same reason: the
annotator emitted hierarchy.global_atomics correctly but produced gold_actions.global_atomics
empty or merged into a subtask. This is a structural-mirror inconsistency, not a content
error. Add a post-parse validator to v2_annotator.py that detects this pattern, re-prompts the
model on just the gold_actions block (or rejects the row to the parse-failure bucket), and
logs the rate. This should bring the FrontierScience-Olympiad accept rate from 67% to ~100%
with zero additional model cost on the happy path.

</details>

<details>
<summary>📊 <strong>Run a single-blind human review pass on the 115 v2 rows and
report human-vs-judge agreement (Cohen's kappa)</strong> (S-0009-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

v2 is judged only by a single LLM call per row. The dataset is 'LLM-judge-acceptable' but not
'human-validated'. To upgrade to v3, recruit 1-2 human annotators to review the same 23-row
stratified sample (or all 115 rows for higher precision) and emit acceptable/needs-revision
verdicts. Compute Cohen's kappa between human and the haiku judge to estimate how much of the
+58% v2-vs-v1 aggregate gain is real quality vs judge-LLM agreement-with-itself. Budget
estimate: 4-6 hours of human review time at $50/hour = $200-300.

</details>

<details>
<summary>📂 <strong>Expand the v2 dataset from 115 rows to >=200 rows by sampling
additional benchmark instances</strong> (S-0009-05)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0009_hierarchical_annotation_v2](../../tasks/t0009_hierarchical_annotation_v2/)

The Phase 1 success criterion is >=100 annotated tasks per condition; v2 is at 115 which is
just over the threshold. The downstream Phase 2 experiments need stratification by difficulty
AND by benchmark, which becomes statistically thin at 5-6 rows per stratum. Expand to >=200
rows by sampling 20-25 additional rows from each of the four benchmarks (especially the
smaller ones: SWE-bench Verified, tau-bench). Re-use v2_annotator.py at the same haiku-CLI
rate, ~$5-6 added cost. Inherits S-0005-01.

</details>

<details>
<summary>🧪 <strong>Scope a v3 schema iteration motivated by per-benchmark
schema-only deltas, not aggregate</strong> (S-0014-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

The aggregate schema-only delta is +57 pp (90% v2-sonnet vs 33% v1-sonnet) but the
per-benchmark split is bimodal: FrontierScience-Olympiad and WorkArena++ are at +100 pp (0% ->
100%), while SWE-bench Verified and tau-bench are at +13-17 pp (67% -> 80-83%). The +100 pp
cells suggest the v2 tree schema converts unsolvable v1 outputs into acceptable v2 outputs,
but this is potentially confounded with the truncation fix bundled into v2 (S-0009-04). The
+13-17 pp cells suggest a real but modest schema improvement on benchmarks where v1 was
already adequate. A v3 schema should target SWE/tau-style structured-action tasks specifically
— e.g., add explicit precondition/postcondition fields to atomics, since the SWE/tau cells
already saturate the high-level subtask abstraction.

</details>

<details>
<summary>🧪 <strong>Rotate the judge model to test the haiku-vs-haiku familial bias
hypothesis on the model-only delta</strong> (S-0014-03)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

The model-only delta of -1 pp sits below Xiong2024's lower edge (0 pp). Xiong2024 documents
that judges trained on the same model family as the annotator show a small positive familial
bias (~5-10 pp). Our judge is held on haiku to keep apples-to-apples with t0009/t0005, which
means v2-haiku has a familial-agreement advantage over v2-sonnet. Re-judge the same 20-row
v2-sonnet sample and 23-row v2-haiku sample with claude-sonnet-4-6 as the judge instead of
haiku. If the model-only delta swings positive (e.g., +5-10 pp) under the sonnet judge, the
haiku-vs-haiku familial bias is masking a real sonnet annotator advantage. If it stays near
zero, sonnet really does provide no annotator-quality lift on this composite. Cost ~$2 with
sonnet judge on 43 rows.

</details>

<details>
<summary>🔧 <strong>Adopt a haiku-default annotation policy for Phase 2: model swap
is not justified</strong> (S-0014-04)</summary>

**Kind**: technique | **Priority**: high | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

Under the t0014 measurement, haiku and sonnet annotators produce statistically
indistinguishable accept rates under the v2 tree schema (90% sonnet vs 91% haiku, CIs overlap
completely). Sonnet annotation costs ~$0.20 per call vs haiku ~$0.02 per call (10x via Claude
Code CLI; 7-8x via direct API). For Phase 2 ABC/main-experiment annotation budgets in the
$50-200 range, the cost differential dominates: a 200-row sonnet annotation pass would cost
$40 vs $5 for haiku, with no measurable accept-rate benefit. Adopt haiku as the default
annotator unless and until S-0014-02 or S-0014-03 surfaces a real sonnet advantage masked by
judge bias.

</details>

<details>
<summary>🧪 <strong>Re-run the three FrontierScience-Olympiad sonnet timeouts under a
longer CLI timeout to recover the missing rows</strong> (S-0014-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-30 | **Source**:
[t0014_v2_annotator_sonnet_rerun](../../tasks/t0014_v2_annotator_sonnet_rerun/)

Three FrontierScience-Olympiad rows (pilot indices 7, 8, 14) timed out at the 300s Claude Code
CLI ceiling during the sonnet annotation pass. They were dropped from the judge sample,
reducing FS sample size from 6 (t0009 v2-haiku) to 3 (t0014 v2-sonnet). The +33 pp model-only
delta on FS (67% v2-haiku vs 100% v2-sonnet, n=6 vs n=3) is therefore on a smaller sample than
the other benchmarks. Re-run those three rows with a 600s or 900s CLI timeout (or via direct
Anthropic API which has no per-call wall-clock cap) and re-judge. If all three pass, FS
aggregate v2-sonnet stays at 100% on n=6 and the +33 pp model-only delta becomes more
credible. Cost <$1.

</details>

<details>
<summary>📂 <strong>Replace Mind2Web/HumanEval proxy rows with native WorkArena++
and tau-bench data</strong> (S-0015-01)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-30 | **Source**:
[t0015_correct_proxy_benchmark_labels](../../tasks/t0015_correct_proxy_benchmark_labels/)

Variant a of S-0009-06 (now folded into this follow-up). The 26 m2w_* rows in the v2
hierarchical-annotation dataset are Mind2Web data used as a proxy for the gated WorkArena++
split, and the 26 he_* rows are HumanEval data used as a proxy for the gated tau-bench split.
t0015 corrected the labels but did not replace the underlying data. This task should (1)
obtain access to a real WorkArena++ split and a real tau-bench split (both currently gated;
expect a registration / agreement step that must be tracked as an intervention), (2)
re-annotate 26 + 26 rows under the v2 tree schema using the same haiku annotator and judge as
t0009 to keep variant b apples-to-apples, and (3) issue a corrections-overlay against
hierarchical-annotation-v2 that swaps the proxy rows for the native rows. Out of scope: any
change to the FrontierScience-Olympiad or SWE-bench Verified rows.

</details>

<details>
<summary>📊 <strong>Add a row-level original_benchmark provenance field to future
relabel corrections</strong> (S-0015-02)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-30 | **Source**:
[t0015_correct_proxy_benchmark_labels](../../tasks/t0015_correct_proxy_benchmark_labels/)

The t0015 overlay rewrites the per-row benchmark string but does not preserve the original
proxy label inside the row. A reader inspecting only the effective JSONL cannot tell that the
row was previously labeled differently — provenance lives only in the corrections overlay's
description.md. For future relabel corrections, the framework would benefit from a soft
convention where the corrected row carries an original_benchmark field (or, more generally,
original_<field> for any field rewritten by a corrections overlay). This makes per-row
provenance auditable without round-tripping through the corrections file. The task should: (1)
propose the convention as a small extension to the corrections specification, (2) update the
dataset-asset verificator to surface a warning when an overlay rewrites a per-row field
without preserving the original, and (3) backfill the convention into the t0015 overlay.

</details>

<details>
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0003_download_benchmark_subsets](../../tasks/t0003_download_benchmark_subsets/)

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>

<details>
<summary>📂 <strong>Hierarchical annotation v2: scale to >=200 rows with full human
review</strong> (S-0005-01)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

Extend the v1 pilot to >=200 rows by re-running the upstream pilot pipeline with a stricter
retry policy (eliminate the 11 FrontierScience-Olympiad rows where steps==null), then perform
a full human-rater review of every row. Compute inter-rater agreement (Krippendorff's alpha or
Cohen's kappa) between the human rater and the LLM annotator.

</details>

<details>
<summary>📂 <strong>Remediate proxy benchmark naming and task_id
non-uniqueness</strong> (S-0005-04)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

The pilot file uses tau-bench and WorkArena++ as proxies but task_id prefixes are still `he_*`
(HumanEval) and `m2w_*` (Mind2Web) from earlier drafts; additionally 14 of 115 task_ids are
duplicated. Re-key the source data with synthetic per-row UUIDs and align task_id prefixes
with the actual benchmark slugs (`tau_*`, `wa_*`).

</details>
