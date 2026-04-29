# Suggestions: `benchmark-frontierscience`

3 suggestion(s) in category
[`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) **3 open**
(2 high, 1 medium).

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📂 <strong>Negotiate Epoch AI access for full FrontierMath
benchmark</strong> (S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

FrontierMath (Glazer et al. 2024) is the closest publicly named analogue to
FrontierScience-Olympiad and is gated behind Epoch AI access. The current dataset asset uses
40 pilot rows as the v0 subset. Open a conversation with Epoch AI to obtain bona-fide research
access; if access is denied or delayed, add MATH-500 / AIME as a public Olympiad fallback per
the t0002 fallback plan.

</details>

<details>
<summary>📂 <strong>Negotiate FrontierMath access via Epoch AI evaluation
pipeline</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

FrontierMath [Glazer2024] uses contamination-resistant unpublished problems hosted via Epoch
AI's evaluation pipeline; the raw problems are not publicly downloadable. The project needs an
explicit access conversation with Epoch AI, plus a fallback to public Olympiad benchmarks
(MATH-500, AIME) if access is denied or delayed. Schedule this as a planning task before Phase
1 to avoid blocking the FrontierScience-Olympiad slot of the composite benchmark.

</details>

## Medium Priority

<details>
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>
