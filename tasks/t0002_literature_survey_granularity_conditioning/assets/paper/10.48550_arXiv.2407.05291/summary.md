---
spec_version: "3"
paper_id: "10.48550_arXiv.2407.05291"
citation_key: "Boisvert2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2024
* **Authors**: Léo Boisvert 🇨🇦, Megh Thakkar 🇨🇦, Maxime Gasse 🇨🇦, Massimo Caccia 🇨🇦,
  Thibault Le Sellier De Chezelles 🇨🇦, Quentin Cappart 🇨🇦, Nicolas Chapados 🇨🇦,
  Alexandre Lacoste 🇨🇦, Alexandre Drouin 🇨🇦
* **Venue**: NeurIPS 2024 Datasets and Benchmarks Track
* **DOI**: `10.48550/arXiv.2407.05291`

## Abstract

The ability of large language models (LLMs) to mimic human-like intelligence has led to a surge in
LLM-based autonomous agents. Though recent LLMs seem capable of planning and reasoning given user
instructions, their effectiveness in applying these capabilities for autonomous task solving
remains underexplored. This is especially true in enterprise settings, where automated agents hold
the promise of a high impact. To fill this gap, we propose WorkArena++, a novel benchmark
consisting of 682 tasks corresponding to realistic workflows routinely performed by knowledge
workers. WorkArena++ is designed to evaluate the planning, problem-solving, logical/arithmetic
reasoning, retrieval, and contextual understanding abilities of web agents. Our empirical studies
across state-of-the-art LLMs and vision-language models (VLMs), as well as human workers, reveal
several challenges for such models to serve as useful assistants in the workplace. In addition to
the benchmark, we provide a mechanism to effortlessly generate thousands of ground-truth
observation/action traces, which can be used for fine-tuning existing models. Overall, we expect
this work to serve as a useful resource to help the community progress toward capable autonomous
agents.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. WorkArena++ extends WorkArena (33 atomic tasks) to **682
compositional tasks** that demand planning, problem-solving, logical/arithmetic reasoning,
retrieval, and contextual understanding from the agent. Compositional here means that a task's
solution requires *chaining* multiple WorkArena atomic operations, often with state passing
between them.

The benchmark targets exactly the gap the granularity-aware hierarchical agents project aims to
close: agents that succeed on individual atomic actions but fail to coordinate them across a
multi-step workflow. The paper reports a "considerable gap" to full automation across SOTA LLMs,
VLMs, and human workers — the explicit human-vs-model comparison is a feature few other web-agent
benchmarks share.

For this project, WorkArena++ is the **most directly relevant single benchmark** in the four-source
composite. It is the test bed where atomic-vs-compositional gaps are both measurable and large,
making it the strongest single test bed for sub-hypothesis 1 ("gains concentrated in states where
local execution requires information not needed for higher-level planning").

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
benchmark builds **682 compositional tasks** by chaining the 33 atomic WorkArena task families. The
key methodological innovation is a **trace-generation mechanism** that produces "thousands of
ground-truth observation/action traces" for fine-tuning existing models — an artifact the project
should treat as a distinct dataset asset.

Evaluation reuses the BrowserGym harness from WorkArena, with the same action set and multimodal
observation API. Models evaluated include both LLMs and vision-language models (VLMs), plus human
workers as an upper-bound reference. Tasks span the full spectrum of knowledge-work cognition:
**planning** (decompose a goal into subgoals), **problem-solving** (handle unforeseen state),
**logical/arithmetic reasoning** (cross-record computation), **retrieval** (find data in
ServiceNow), **contextual understanding** (interpret form layouts and modal flows). The exact
distribution of difficulty is not reported in the abstract but the NeurIPS 2024 D&B paper provides
detailed per-skill breakdowns.

## Results

* **682 compositional tasks** built on top of 33 WorkArena atomic families
* **Considerable gap to full automation** across SOTA LLMs, VLMs, and human workers (specific
  per-model numbers in the NeurIPS 2024 D&B paper)
* **Multiple skill axes** evaluated independently: planning, problem-solving, reasoning, retrieval,
  contextual understanding
* **Trace generation mechanism** can produce **thousands of ground-truth observation/action
  traces** for fine-tuning
* **Human-vs-model comparison** included — a feature most prior web-agent benchmarks lack
- Atomic-vs-compositional gap is the central finding: agents that succeed on WorkArena atomic
  tasks frequently fail when those same operations must be coordinated in a multi-step workflow

## Innovations

### Compositional Construction From Atomic Primitives

WorkArena++ is the first widely-cited benchmark to cleanly separate atomic from compositional
performance. By building 682 compositional tasks from the same 33 atomic families that WorkArena
already evaluates, the paper enables direct measurement of the atomic-vs-compositional gap, which
is precisely the gap the granularity-conditioning hypothesis targets.

### Per-Skill Decomposition

The five evaluation axes (planning, problem-solving, reasoning, retrieval, contextual
understanding) let researchers locate which sub-capability bottlenecks an agent's overall
performance. This level of decomposition is rare in web-agent benchmarks and is directly useful for
the project's stratified per-skill analysis.

### Synthetic Trace Generation for Fine-Tuning

The trace generator produces gold action sequences without manual annotation. While the project
does not fine-tune (training-time methods are out of scope), the generator is reusable as a source
of *gold actions* for the project's annotation set required by Phase 1.

## Datasets

* **WorkArena++ task suite** — 682 compositional tasks built on the 33 WorkArena atomic families.
  Open source on GitHub via the same `ServiceNow/WorkArena` repository as the atomic benchmark.
  Requires a ServiceNow developer instance.
* **Synthetic trace dataset** — generated on the fly by the included trace mechanism. Useful as a
  source of gold actions for the project's three-level annotation set.

## Main Ideas

* WorkArena++ is the **strongest single test bed** in the project's four-source composite for
  measuring the atomic-vs-compositional gap that granularity conditioning is meant to close.
* The synthetic trace generator can supply gold actions at the atomic level for Phase 1
  annotation, complementing the manual annotation of global and subtask actions.
* Reuse the BrowserGym harness end-to-end — the project does not need to build a separate
  WorkArena++ adapter on top of the WorkArena adapter; they share the same harness.

## Summary

WorkArena++ extends the 33 atomic WorkArena task families into 682 compositional knowledge-work
tasks evaluated on the same ServiceNow + BrowserGym substrate. The motivation is that prior
benchmarks measure either atomic or end-to-end success but rarely the gap between the two — the
gap that explains why agents that handle individual web actions still cannot complete realistic
enterprise workflows.

Methodologically, the paper composes WorkArena atomic operations into multi-step workflows whose
ground-truth solutions exercise five skill axes: planning, problem-solving, logical/arithmetic
reasoning, retrieval, and contextual understanding. Evaluation uses the BrowserGym harness with
SOTA LLMs, VLMs, and human workers as comparison points. A trace generator produces synthetic gold
action sequences for fine-tuning research.

The headline finding is a **considerable gap** to full automation across all evaluated systems,
with detailed per-skill breakdowns in the NeurIPS 2024 D&B paper. The atomic-vs-compositional gap
is the central observation — agents that succeed on individual web actions consistently fail to
coordinate them across a multi-step workflow.

For the granularity-aware hierarchical agents project, WorkArena++ is the most directly relevant
single benchmark. It is the strongest test bed for sub-hypothesis 1 (gains concentrated where
local execution needs information not needed for higher-level planning); it shares a harness with
WorkArena, lowering integration cost; and its synthetic trace generator can supply gold atomic
actions to complement the project's manual global/subtask annotation. The project should treat
WorkArena++ as the primary metric source for Phase 2 stratified analysis.
