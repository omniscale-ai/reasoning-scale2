# Category: WorkArena++

Per-source tag for tasks and assets sourced from the WorkArena++ web-task benchmark.

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (2)](../papers/by-category/benchmark-workarena.md) | [Suggestions
(4)](../suggestions/by-category/benchmark-workarena.md) | [Datasets
(1)](../datasets/by-category/benchmark-workarena.md)

---

## Papers (2)

<details>
<summary>🏤 <strong>WorkArena++: Towards Compositional Planning and Reasoning-based
Common Knowledge Work Tasks</strong> — Boisvert et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2407.05291` |
| **Authors** | Léo Boisvert, Megh Thakkar, Maxime Gasse, Massimo Caccia, Thibault Le Sellier De Chezelles, Quentin Cappart, Nicolas Chapados, Alexandre Lacoste, Alexandre Drouin |
| **Venue** | NeurIPS 2024 Datasets and Benchmarks Track (conference) |
| **DOI** | `10.48550/arXiv.2407.05291` |
| **URL** | https://arxiv.org/abs/2407.05291 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/summary.md) |

WorkArena++ extends the 33 atomic WorkArena task families into 682 compositional
knowledge-work tasks evaluated on the same ServiceNow + BrowserGym substrate. The motivation
is that prior benchmarks measure either atomic or end-to-end success but rarely the gap
between the two — the gap that explains why agents that handle individual web actions still
cannot complete realistic enterprise workflows.

Methodologically, the paper composes WorkArena atomic operations into multi-step workflows
whose ground-truth solutions exercise five skill axes: planning, problem-solving,
logical/arithmetic reasoning, retrieval, and contextual understanding. Evaluation uses the
BrowserGym harness with SOTA LLMs, VLMs, and human workers as comparison points. A trace
generator produces synthetic gold action sequences for fine-tuning research.

The headline finding is a **considerable gap** to full automation across all evaluated
systems, with detailed per-skill breakdowns in the NeurIPS 2024 D&B paper. The
atomic-vs-compositional gap is the central observation — agents that succeed on individual web
actions consistently fail to coordinate them across a multi-step workflow.

For the granularity-aware hierarchical agents project, WorkArena++ is the most directly
relevant single benchmark. It is the strongest test bed for sub-hypothesis 1 (gains
concentrated where local execution needs information not needed for higher-level planning); it
shares a harness with WorkArena, lowering integration cost; and its synthetic trace generator
can supply gold atomic actions to complement the project's manual global/subtask annotation.
The project should treat WorkArena++ as the primary metric source for Phase 2 stratified
analysis.

</details>

<details>
<summary>🏤 <strong>WorkArena: How Capable Are Web Agents at Solving Common Knowledge
Work Tasks?</strong> — Drouin et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2403.07718` |
| **Authors** | Alexandre Drouin, Maxime Gasse, Massimo Caccia, Issam H. Laradji, Manuel Del Verme, Tom Marty, Léo Boisvert, Megh Thakkar, Quentin Cappart, David Vazquez, Nicolas Chapados, Alexandre Lacoste |
| **Venue** | ICML 2024 (conference) |
| **DOI** | `10.48550/arXiv.2403.07718` |
| **URL** | https://arxiv.org/abs/2403.07718 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-workarena`](../../meta/categories/benchmark-workarena/), [`agent-evaluation`](../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2403.07718/summary.md) |

WorkArena introduces a remote-hosted benchmark of 33 enterprise-grade web tasks built on the
ServiceNow platform, accompanied by BrowserGym — a reusable Python environment for web-agent
evaluation. The motivation is that prior web-agent benchmarks (MiniWoB, WebShop) lack the
complexity of modern enterprise software, where agents must navigate content management
systems, intricate forms, custom layouts, and modal popups.

Methodologically, the paper instantiates 33 task families with 19,912 unique parameterized
instances, evaluates them via BrowserGym's standardized action and observation API, and grades
success by inspecting the resulting database state. Evaluation is reported as `pass@1`, with
the state-of-the-art proprietary model (GPT-4) and the strongest open-source model
(Llama3-70B) as the two anchor points.

The headline finding is a **24.8 absolute** gap between GPT-4 (**42.7%**) and
Llama3-70B-instruct (**17.9%**), demonstrating that current open-source agents lag
substantially on enterprise workflows. Even the best result leaves a considerable distance to
full task automation.

For the granularity-aware hierarchical agents project, WorkArena is the atomic layer
WorkArena++ composes. The project should reuse BrowserGym for compatibility, treat WorkArena
tasks as sanity-check material rather than primary evaluation, and prefer GPT-4-class models
for the Phase 2 baseline. The open-vs-closed-source gap is large enough that mixing model
classes in the composite benchmark would conflate model effects with prompt effects — a hazard
the planning step must address.

</details>

## Tasks (1)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |

## Answers (0)

No answers in this category.

## Suggestions (4 open, 0 closed)

<details>
<summary>📚 <strong>Set up ServiceNow + BrowserGym harness shared by WorkArena and
WorkArena++</strong> (S-0002-03)</summary>

**Kind**: library | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

Both WorkArena [Drouin2024] and WorkArena++ [Boisvert2024] require a self-hosted ServiceNow
developer instance and the BrowserGym Python harness. This is a substantial infrastructure
task with credentials, container orchestration, and end-to-end smoke tests. Schedule it before
any task that needs WorkArena or WorkArena++ data so the harness is ready when Phase 1
annotation begins.

</details>

<details>
<summary>📂 <strong>Provision a ServiceNow developer instance for WorkArena++ live
evaluation</strong> (S-0003-02)</summary>

**Kind**: dataset | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0003_download_benchmark_subsets](../../tasks/t0003_download_benchmark_subsets/)

WorkArena++ instance enumeration requires a live ServiceNow developer instance plus access to
the gated `ServiceNow/WorkArena-Instances` HuggingFace dataset. This task captures only the
upstream task-class manifest. Provision a free ServiceNow developer instance, request HF
access, install browsergym-workarena, and produce an instance-level subset filtered to 4-8
decisions per task. Until then, the Mind2Web pilot proxy is frozen as the de-facto Phase 2
fallback.

</details>

<details>
<summary>🔧 <strong>Reconcile WorkArena++ flat-action sequences with the three-level
schema</strong> (S-0005-03)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

The judge rejected all three WorkArena++ rows because the upstream annotation lacks
`conceptual` nodes, causing the mapper to emit empty subtask lists. Investigate whether the
WorkArena++ source carries an implicit subtask boundary (e.g., screen transitions) that can be
detected automatically, or alternatively change the v2 schema to accept flat atomic-only rows
as a distinct hierarchy_kind. Document the chosen approach and update the mapper.

</details>

<details>
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>
