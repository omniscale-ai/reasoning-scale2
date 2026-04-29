# Suggestions: `benchmark-workarena`

2 suggestion(s) in category
[`benchmark-workarena`](../../../meta/categories/benchmark-workarena/) **2 open** (2 high).

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📂 <strong>Provision a ServiceNow developer instance for WorkArena++ live
evaluation</strong> (S-0003-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-02` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/) |

WorkArena++ instance enumeration requires a live ServiceNow developer instance plus access to
the gated `ServiceNow/WorkArena-Instances` HuggingFace dataset. This task captures only the
upstream task-class manifest. Provision a free ServiceNow developer instance, request HF
access, install browsergym-workarena, and produce an instance-level subset filtered to 4-8
decisions per task. Until then, the Mind2Web pilot proxy is frozen as the de-facto Phase 2
fallback.

</details>

<details>
<summary>📚 <strong>Set up ServiceNow + BrowserGym harness shared by WorkArena and
WorkArena++</strong> (S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2407.05291`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/) |
| **Categories** | [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Both WorkArena [Drouin2024] and WorkArena++ [Boisvert2024] require a self-hosted ServiceNow
developer instance and the BrowserGym Python harness. This is a substantial infrastructure
task with credentials, container orchestration, and end-to-end smoke tests. Schedule it before
any task that needs WorkArena or WorkArena++ data so the harness is ready when Phase 1
annotation begins.

</details>
