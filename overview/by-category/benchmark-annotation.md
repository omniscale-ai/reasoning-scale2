# Category: Benchmark Annotation

Manual or LLM-assisted gold-action annotation across the three granularity levels.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (1)](../papers/by-category/benchmark-annotation.md) | [Suggestions
(5)](../suggestions/by-category/benchmark-annotation.md) | [Datasets
(1)](../datasets/by-category/benchmark-annotation.md)

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

## Answers (0)

No answers in this category.

## Suggestions (3 open, 2 closed)

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
