# Datasets by Date Added

7 dataset(s) grouped by project added date.

[Back to all datasets](../README.md)

---

## 2026-04-30 (2)

<details>
<summary>📂 <strong>Hierarchical Annotation v2 (115-row pilot, tree schema)
vv2</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v2` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale2 project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree. 115 rows passed the v2 hierarchy_completeness check. 23 rows received an LLM-as-judge verdict (21 acceptable, 2 needs revision). Per-row benchmark labels: 40 FrontierScience-Olympiad, 23 SWE-bench Verified, 26 Mind2Web (proxy for WorkArena++), 26 HumanEval (proxy for tau-bench). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Description** | [`description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md) |
| **Summary** | Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench Verified, Mind2Web (proxy for WorkArena++), and HumanEval (proxy for tau-bench). Re-annotates the v1 pilot under a v2 schema with explicit subtask-to-atomic edges and full problem text. Includes a 23-row LLM-as-judge spot-check. |

</details>

<details>
<summary>📂 <strong>Hierarchical Annotation v2 (115-row pilot, tree schema,
relabeled) vv2-relabeled</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v2-relabeled` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale2 project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total; each row carries a tree-shaped hierarchy (global / subtasks-with-atomics / global_atomics) and a parallel gold_actions tree. 115 rows passed the v2 hierarchy_completeness check. 23 rows received an LLM-as-judge verdict (21 acceptable, 2 needs revision). Per-row benchmark labels: 40 FrontierScience-Olympiad, 23 SWE-bench Verified, 26 Mind2Web (proxy for WorkArena++), 26 HumanEval (proxy for tau-bench). |
| **Date added** | 2026-04-30 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0015_correct_proxy_benchmark_labels`](../../../overview/tasks/task_pages/t0015_correct_proxy_benchmark_labels.md) |
| **Description** | [`description.md`](../../../tasks/t0015_correct_proxy_benchmark_labels/assets/dataset/hierarchical-annotation-v2-relabeled/description.md) |
| **Summary** | Tree-shaped (global / subtasks-with-atomics / global_atomics) hierarchical annotation of 115 benchmark tasks from FrontierScience-Olympiad, SWE-bench Verified, Mind2Web (proxy for WorkArena++), and HumanEval (proxy for tau-bench). Same rows as the v2 source dataset; only the per-row benchmark label has been corrected to match the actual data source. Includes a 23-row LLM-as-judge spot-check. |

</details>

## 2026-04-29 (5)

<details>
<summary>📂 <strong>FrontierScience-Olympiad subset (pilot v0) vv0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `frontierscience-olympiad-subset` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale project |
| **URL** | https://arxiv.org/abs/2411.04872 |
| **License** | research-only |
| **Access** | public |
| **Size** | 40 Olympiad-style problems (physics, chemistry, biology) packaged from the project pilot annotation run; per-domain: biology=15, chemistry=10, physics=15 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |
| **Added by** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Description** | [`description.md`](../../../tasks/t0003_download_benchmark_subsets/assets/dataset/frontierscience-olympiad-subset/description.md) |
| **Summary** | FrontierScience-Olympiad pilot v0 subset: 40 Olympiad problems across physics, chemistry, biology with gold solutions, packaged for Phase 2 experiments. |

</details>

<details>
<summary>📂 <strong>Hierarchical Annotation v1 (115-row pilot audit) vv1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `hierarchical-annotation-v1` |
| **Year** | 2026 |
| **Authors** | Glite ARF reasoning-scale project |
| **URL** | — |
| **License** | inherited-per-row |
| **Access** | restricted |
| **Size** | 115 rows total (FrontierScience-Olympiad=40, SWE-bench Verified=23, WorkArena++=26, tau-bench=26); each row carries a global / subtask / atomic hierarchy and gold-action triple. Twelve rows (three per benchmark) carry an LLM-as-judge verdict. |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Description** | [`description.md`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/dataset/hierarchical-annotation-v1/description.md) |
| **Summary** | Three-level (global / subtask / atomic) hierarchical annotation of 115 benchmark tasks drawn from FrontierScience-Olympiad, SWE-bench Verified, tau-bench, and WorkArena++. Includes a 12-row LLM-as-judge spot-check. |

</details>

<details>
<summary>📂 <strong>SWE-bench Verified subset (4-8 hunks) vverified-2024</strong></summary>

| Field | Value |
|---|---|
| **ID** | `swebench-verified-subset` |
| **Year** | 2024 |
| **Authors** | Carlos E. Jimenez (parent SWE-bench), OpenAI Verified curation team |
| **URL** | https://openai.com/index/introducing-swe-bench-verified/ |
| **License** | MIT |
| **Access** | public |
| **Size** | 60 instances filtered from 500 SWE-bench Verified instances (kept iff gold patch has between 4 and 8 `@@` hunks) |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |
| **Added by** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Description** | [`description.md`](../../../tasks/t0003_download_benchmark_subsets/assets/dataset/swebench-verified-subset/description.md) |
| **Summary** | SWE-bench Verified subset filtered to 60 instances whose gold patch has 4 to 8 diff hunks; suitable for multi-step code-edit experiments. |

</details>

<details>
<summary>📂 <strong>tau-bench subset (4-8 actions) vgithub-main</strong></summary>

| Field | Value |
|---|---|
| **ID** | `taubench-subset` |
| **Year** | 2024 |
| **Authors** | Shunyu Yao |
| **URL** | https://arxiv.org/abs/2406.12045 |
| **License** | MIT |
| **Access** | public |
| **Size** | 87 tasks filtered from 665 upstream tau-bench tasks (kept iff gold action sequence has between 4 and 8 actions) |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) |
| **Added by** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Description** | [`description.md`](../../../tasks/t0003_download_benchmark_subsets/assets/dataset/taubench-subset/description.md) |
| **Summary** | tau-bench subset: 87 tool-agent-user interaction tasks across airline and retail domains, filtered to 4-8 gold actions per task. |

</details>

<details>
<summary>📂 <strong>WorkArena++ compositional task manifest vgithub-main</strong></summary>

| Field | Value |
|---|---|
| **ID** | `workarena-plus-plus-subset` |
| **Year** | 2024 |
| **Authors** | Léo Boisvert |
| **URL** | https://arxiv.org/abs/2407.05291 |
| **License** | Apache-2.0 |
| **Access** | restricted |
| **Size** | 42 compositional task class lists from the upstream curriculum manifest. Task instances are not enumerated (requires live ServiceNow + gated HF). |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/) |
| **Added by** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Description** | [`description.md`](../../../tasks/t0003_download_benchmark_subsets/assets/dataset/workarena-plus-plus-subset/description.md) |
| **Summary** | WorkArena++ compositional task class manifest (42 task class lists) extracted from upstream curriculum.py; end-to-end execution remains gated. |

</details>
