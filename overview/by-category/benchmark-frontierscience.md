# Category: FrontierScience-Olympiad

Per-source tag for tasks and assets sourced from the FrontierScience-Olympiad benchmark.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (1)](../papers/by-category/benchmark-frontierscience.md) |
[Suggestions (5)](../suggestions/by-category/benchmark-frontierscience.md) | [Datasets
(1)](../datasets/by-category/benchmark-frontierscience.md)

---

## Papers (1)

<details>
<summary>📝 <strong>FrontierMath: A Benchmark for Evaluating Advanced Mathematical
Reasoning in AI</strong> — Glazer et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2411.04872` |
| **Authors** | Elliot Glazer, Ege Erdil, Tamay Besiroglu, Diego Chicharro, Evan Chen, Alex Gunning, Caroline Falkman Olsson, Jean-Stanislas Denain, Anson Ho, Emily de Oliveira Santos, Olli Järviniemi, Matthew Barnett, Robert Sandler, Matej Vrzala, Jaime Sevilla, Qiuyu Ren, Elizabeth Pratt, Lionel Levine, Grant Barkley, Natalie Stewart, Bogdan Grechuk, Tetiana Grechuk, Shreepranav Varma Enugandla, Mark Wildon |
| **Venue** | arXiv preprint (preprint) |
| **DOI** | `10.48550/arXiv.2411.04872` |
| **URL** | https://arxiv.org/abs/2411.04872 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-frontierscience`](../../meta/categories/benchmark-frontierscience/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/summary.md) |

The paper introduces FrontierMath, a research-mathematician-grade math reasoning benchmark
designed to evaluate frontier LLMs on problems that require hours to days of human expert
effort. The motivation is the saturation of prior math benchmarks (GSM8K, MATH) by SOTA models
and the contamination risk of using publicly available problems for evaluation.

The benchmark is built by commissioning hundreds of original, unpublished problems from expert
mathematicians, with programmatic answer-checking that scales to repeated automated runs.
Problems span number theory, real analysis, algebraic geometry, and category theory;
difficulty tiers cover undergraduate through research level. Endorsements from Fields
Medalists (Tao, Gowers, Borcherds) characterize the upper-tier problems as exceptionally
challenging.

The headline result is that current state-of-the-art models solve **under 2% of problems** at
release, revealing a large gap between AI and expert-mathematician performance. This is the
hardest published math benchmark to date.

For the granularity-aware hierarchical agents project, FrontierMath is the canonical
instantiation of the FrontierScience-Olympiad slot named in `project/description.md`. The <2%
baseline means the benchmark contributes mainly to the failure tail of the composite Phase 2
benchmark, and any per-condition (scope-aware vs. scope-unaware) effect must be measured
against a near-zero floor — which makes per-source stratification mandatory. Access via Epoch
AI's evaluation pipeline is a known operational risk for the t0003 download-dataset task.

</details>

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (0)

No answers in this category.

## Suggestions (4 open, 1 closed)

<details>
<summary>📂 <strong>Negotiate FrontierMath access via Epoch AI evaluation
pipeline</strong> (S-0002-04)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

FrontierMath [Glazer2024] uses contamination-resistant unpublished problems hosted via Epoch
AI's evaluation pipeline; the raw problems are not publicly downloadable. The project needs an
explicit access conversation with Epoch AI, plus a fallback to public Olympiad benchmarks
(MATH-500, AIME) if access is denied or delayed. Schedule this as a planning task before Phase
1 to avoid blocking the FrontierScience-Olympiad slot of the composite benchmark.

</details>

<details>
<summary>📂 <strong>Negotiate Epoch AI access for full FrontierMath
benchmark</strong> (S-0003-01)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0003_download_benchmark_subsets](../../tasks/t0003_download_benchmark_subsets/)

FrontierMath (Glazer et al. 2024) is the closest publicly named analogue to
FrontierScience-Olympiad and is gated behind Epoch AI access. The current dataset asset uses
40 pilot rows as the v0 subset. Open a conversation with Epoch AI to obtain bona-fide research
access; if access is denied or delayed, add MATH-500 / AIME as a public Olympiad fallback per
the t0002 fallback plan.

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
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>
