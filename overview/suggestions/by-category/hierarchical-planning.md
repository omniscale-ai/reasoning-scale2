# Suggestions: `hierarchical-planning`

5 suggestion(s) in category
[`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) **5 open** (2 high,
2 medium, 1 low).

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🔧 <strong>Implement Plan-and-Solve as the canonical scope-unaware (B)
baseline</strong> (S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Plan-and-Solve [Wang2023] is the strongest published prompt-only baseline that does not
condition on explicit granularity tags. The project should reuse LangChain's Plan-and-Execute
implementation rather than reimplementing from scratch. This task would adapt the LangChain
implementation to the project's task harness, log both stages (plan and solve) separately, and
produce a 10-instance validation run on the composite benchmark to confirm the baseline beats
vanilla Zero-shot-CoT.

</details>

<details>
<summary>🔧 <strong>Implement scope-aware (A) as ReAct extended with explicit
granularity tags</strong> (S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The scope-aware (A) condition can be implemented as ReAct [Yao2022] extended with a per-token
granularity tag from the set {global, subtask, atomic}. This task would specify the prompt
template per granularity, the tagging logic that decides which granularity is active at each
LLM call, and a logging schema that records the active granularity for every action so
post-hoc per-granularity analysis is possible. Replicate Least-to-Most's solution-reuse
pattern [Zhou2022] inside the implementation.

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

<details>
<summary>🧪 <strong>Run a Phase 1 pilot annotation on 20 tasks before scaling to
100</strong> (S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The project's success criteria require 100 tasks annotated at three granularity levels. Before
scaling, run a 20-task pilot to validate the annotation schema, measure inter-annotator
agreement, and refine the rubric. WorkArena++ [Boisvert2024] offers the cleanest
atomic-vs-compositional structure for the pilot; its synthetic trace generator can supply gold
atomic actions, leaving manual annotation effort focused on global and subtask levels.

</details>

## Low Priority

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2303.11366`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>
