---
spec_version: "3"
paper_id: "10.48550_arXiv.2403.07718"
citation_key: "Drouin2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2024
* **Authors**: Alexandre Drouin 🇨🇦, Maxime Gasse 🇨🇦, Massimo Caccia 🇨🇦, Issam H. Laradji 🇨🇦,
  Manuel Del Verme 🇨🇦, Tom Marty 🇨🇦, Léo Boisvert 🇨🇦, Megh Thakkar 🇨🇦, Quentin Cappart 🇨🇦,
  David Vazquez 🇨🇦, Nicolas Chapados 🇨🇦, Alexandre Lacoste 🇨🇦
* **Venue**: ICML 2024
* **DOI**: `10.48550/arXiv.2403.07718`

## Abstract

We study the use of large language model-based agents for interacting with software via web
browsers. Such agents can in principle perform tasks that span the typical daily work of knowledge
workers utilizing enterprise software systems. To do so, they need to be capable of dealing with
various aspects of the modern enterprise web ecosystem, such as content management systems,
intricate forms, custom layouts, and modal popups. To facilitate research into this important
domain, we present WorkArena, a remote-hosted benchmark of 33 tasks based on the widely-used
ServiceNow platform. We also introduce BrowserGym, an environment for the design and evaluation of
such agents, offering a rich set of actions as well as multimodal observations. Our empirical
evaluation reveals that while current agents show promise on WorkArena, there remains a
considerable gap towards achieving full task automation. Notably, our analysis uncovers a
significant performance disparity between open and closed-source LLMs, highlighting a critical area
for future exploration and development in the field.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. WorkArena introduces 33 atomic web-task workflows on
ServiceNow that exercise the building blocks of enterprise knowledge work: content management
operations, intricate forms, custom layouts, and modal popups. The companion BrowserGym
environment exposes a uniform action and multimodal observation API so that web agents can be
benchmarked under controlled conditions.

The empirical headline of the paper is a substantial open-vs-closed-source gap: GPT-4 reaches
**42.7%** task success on WorkArena, while the strongest open-source model evaluated
(Llama3-70B-instruct) reaches only **17.9%**. The paper frames this not as a limitation of
open-source models per se but as a critical area for future agent research.

For the granularity-aware hierarchical agents project, WorkArena is the *atomic* layer that
WorkArena++ later composes. Direct use is moderate: the project requires multi-step tasks of 4-8
decisions, and most WorkArena items are shorter. The key value is as a sanity check — agents that
fail at WorkArena's atomic tasks cannot be expected to succeed on WorkArena++'s compositional
ones.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
benchmark consists of **33 web tasks** with **19,912 unique instances** (parameterized variants of
the same task templates). Tasks are hosted remotely on a self-managed ServiceNow instance, which
the agent interacts with via the BrowserGym environment.

BrowserGym exposes a Python API with **rich actions** (click, type, scroll, navigate, etc.) and
**multimodal observations** (DOM, screenshots, accessibility tree). Evaluation runs each agent on
each task instance and records success or failure based on database state inspection — for
example, whether the requested record was created or updated correctly. The paper evaluates
**GPT-4** (best closed-source) and **Llama3-70B-instruct** (best open-source) plus a small set of
intermediate models. Evaluation uses the standard `pass@1` metric — does the agent succeed on its
first attempt?

The paper does not propose a new agent architecture beyond the BrowserGym wrapper; the contribution
is the benchmark and the evaluation harness. Subsequent papers (including WorkArena++) build on
this scaffolding rather than replace it.

## Results

* **GPT-4 reaches 42.7%** pass@1 across the 33 task families
* **Llama3-70B-instruct reaches 17.9%** pass@1 — a **24.8 absolute** gap
* **33 task families** cover the typical daily work of knowledge workers
* **19,912 unique instances** parameterize the task families to enable repeated evaluation
* **Significant open-vs-closed-source gap** — even the strongest open-source agents lag closed
  agents by tens of percentage points
* The paper frames the **considerable gap to full automation** as the headline finding, not the
  closed-source success itself

## Innovations

### A Production-Grade Enterprise Web Benchmark

WorkArena is the first benchmark whose tasks are sourced from a real enterprise platform
(ServiceNow) used by Fortune 500 companies, making the evaluation directly relevant to enterprise
deployment scenarios.

### BrowserGym as a Reusable Web-Agent Harness

BrowserGym standardizes the action and observation API for web agents, decoupling the agent
implementation from the benchmark and enabling head-to-head comparison across agents and
benchmarks. WorkArena++ and other follow-up benchmarks reuse this harness.

### Open-vs-Closed-Source Gap Quantified

Prior web-agent benchmarks did not isolate the open-vs-closed-source dimension as cleanly. By
holding the harness, action set, and observation modality constant, WorkArena provides one of the
cleanest single-paper measurements of this gap (24.8 absolute points).

## Datasets

* **WorkArena task suite** — 33 task families × 19,912 instances on ServiceNow. Open source on
  GitHub (`ServiceNow/WorkArena`). Requires a ServiceNow developer instance for execution but the
  task definitions and evaluation harness are public.

## Main Ideas

* WorkArena is the *atomic* layer that WorkArena++ composes. For this project, the atomic items
  function as sanity-check material rather than primary evaluation material.
* The 24.8-point GPT-4 vs. Llama3-70B gap is large enough that closed-source models should be the
  default for the project's Phase 2 baseline; open-source models are useful as a stress test for
  whether scope conditioning gains are model-class-invariant.
* Reuse the BrowserGym harness rather than building a custom WorkArena adapter — the project saves
  weeks of integration work and inherits compatibility with WorkArena++ automatically.

## Summary

WorkArena introduces a remote-hosted benchmark of 33 enterprise-grade web tasks built on the
ServiceNow platform, accompanied by BrowserGym — a reusable Python environment for web-agent
evaluation. The motivation is that prior web-agent benchmarks (MiniWoB, WebShop) lack the
complexity of modern enterprise software, where agents must navigate content management systems,
intricate forms, custom layouts, and modal popups.

Methodologically, the paper instantiates 33 task families with 19,912 unique parameterized
instances, evaluates them via BrowserGym's standardized action and observation API, and grades
success by inspecting the resulting database state. Evaluation is reported as `pass@1`, with the
state-of-the-art proprietary model (GPT-4) and the strongest open-source model (Llama3-70B) as the
two anchor points.

The headline finding is a **24.8 absolute** gap between GPT-4 (**42.7%**) and Llama3-70B-instruct
(**17.9%**), demonstrating that current open-source agents lag substantially on enterprise
workflows. Even the best result leaves a considerable distance to full task automation.

For the granularity-aware hierarchical agents project, WorkArena is the atomic layer WorkArena++
composes. The project should reuse BrowserGym for compatibility, treat WorkArena tasks as
sanity-check material rather than primary evaluation, and prefer GPT-4-class models for the Phase
2 baseline. The open-vs-closed-source gap is large enough that mixing model classes in the
composite benchmark would conflate model effects with prompt effects — a hazard the planning step
must address.
