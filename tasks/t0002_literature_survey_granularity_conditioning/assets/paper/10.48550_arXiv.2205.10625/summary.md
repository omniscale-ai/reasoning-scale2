---
spec_version: "3"
paper_id: "10.48550_arXiv.2205.10625"
citation_key: "Zhou2022"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# Least-to-Most Prompting Enables Complex Reasoning in Large Language Models

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2022 (arXiv); 2023 (ICLR)
* **Authors**: Denny Zhou 🇺🇸, Nathanael Schärli 🇺🇸, Le Hou 🇺🇸, Jason Wei 🇺🇸,
  Nathan Scales 🇺🇸, Xuezhi Wang 🇺🇸, Dale Schuurmans 🇺🇸, Claire Cui 🇺🇸,
  Olivier Bousquet 🇺🇸, Quoc Le 🇺🇸, Ed Chi 🇺🇸
* **Venue**: ICLR 2023
* **DOI**: `10.48550/arXiv.2205.10625`

## Abstract

Chain-of-thought prompting has demonstrated remarkable performance on various natural language
reasoning tasks. However, it tends to perform poorly on tasks which requires solving problems
harder than the exemplars shown in the prompts. To overcome this challenge of easy-to-hard
generalization, we propose a novel prompting strategy, least-to-most prompting. The key idea in
this strategy is to break down a complex problem into a series of simpler subproblems and then
solve them in sequence. Solving each subproblem is facilitated by the answers to previously
solved subproblems. Our experimental results on tasks related to symbolic manipulation,
compositional generalization, and math reasoning reveal that least-to-most prompting is capable
of generalizing to more difficult problems than those seen in the prompts. A notable finding is
that when the GPT-3 code-davinci-002 model is used with least-to-most prompting, it can solve the
compositional generalization benchmark SCAN in any split (including length split) with an
accuracy of at least 99% using just 14 exemplars, compared to only 16% accuracy with chain-of-
thought prompting.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. Least-to-Most (LtM) prompting is a two-stage prompting
technique that addresses chain-of-thought's *easy-to-hard generalization gap*: CoT works well
when test problems are similar in difficulty to the in-context exemplars but degrades sharply on
harder problems. LtM splits the prompt into (a) a **decomposition** stage where the model lists
the subproblems in increasing-difficulty order, and (b) a **sequential solving** stage where each
subproblem is solved using the answers to previously solved subproblems.

The empirical headline is striking: on the SCAN compositional generalization benchmark length
split, LtM with `code-davinci-002` reaches **>=99% accuracy** with **just 14 exemplars**, versus
**16% with vanilla chain-of-thought** — a **+83 absolute** gain. This is the strongest
single-paper evidence that explicit decomposition produces large effect sizes on hierarchical
tasks.

For the project, LtM provides the **strongest empirical anchor** for the scope-aware (A)
condition's expected effect size. The +83 absolute gain on SCAN sets an aspirational ceiling;
the project's +5 to +15 absolute target on the four-source composite is conservative against
this anchor.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, LtM
prompting has two stages:

**Stage 1 — Decomposition**:
```
Q: <complex problem>
A: To solve "<problem>", we need to first solve:
   1. <subproblem 1 (easiest)>
   2. <subproblem 2>
   ...
   k. <subproblem k (hardest)>
```

**Stage 2 — Sequential Solving**:
```
Q: <subproblem 1>
A: <solution 1>

Q: <subproblem 2 with subproblem 1's solution as context>
A: <solution 2>

...

Q: <subproblem k with all prior solutions as context>
A: <final answer>
```

Models evaluated: **GPT-3 code-davinci-002** primarily, with comparisons to other GPT-3 variants.
Tasks: SCAN (compositional generalization), GSM8K (math), MultiArith (math), DROP (reading
comprehension with reasoning), Last Letter Concatenation (symbolic).

## Results

* **>=99% accuracy on SCAN length-split** with `code-davinci-002` + LtM, vs. **16% with
  vanilla chain-of-thought** — a **+83 absolute** gain
* **14 exemplars** are sufficient — a substantial improvement over the 15,000+ training examples
  that prior neural-symbolic models needed for SCAN
* **GSM8K math reasoning** also improves with LtM, though gains are smaller (single-digit
  absolute)
* **Last Letter Concatenation** (symbolic) shows similar large gains to SCAN
* **DROP reading comprehension** shows moderate gains
* The improvement comes specifically from **easy-to-hard generalization** — LtM's gain over CoT
  scales with how much harder the test problems are than the exemplars

## Innovations

### Two-Stage Decomposition Then Sequential Solving

Before LtM, prompting techniques either reasoned linearly (CoT) or planned-then-executed (PS).
LtM is the first to require both an *explicit ordering* of subproblems by difficulty and the
*reuse of earlier subproblems' solutions* in later subproblems' contexts.

### Easy-to-Hard Generalization as a Design Goal

LtM is explicitly designed for the case where test problems are *harder* than training/in-context
exemplars. This is the right characterization for the project's evaluation regime: the four
roadmap benchmarks include problems substantially harder than any in-context examples we can
realistically provide.

### Evidence That Prompting Alone Beats Specialized Architectures

The SCAN result demonstrates that prompting can match or exceed specialized neural-symbolic
architectures (which need 15,000+ training examples) using just 14 in-context exemplars. This is
a major argument for inference-time prompting strategies — exactly the methodological commitment
of this project.

## Datasets

* **SCAN** — compositional generalization, command-to-action mapping. Key splits: simple,
  length, around-right, jump.
* **GSM8K** — grade-school math word problems.
* **MultiArith** — arithmetic word problems.
* **DROP** — reading comprehension with discrete reasoning.
* **Last Letter Concatenation** — symbolic manipulation.

## Main Ideas

* The **+83 absolute gain on SCAN length-split** is the strongest published evidence that
  explicit decomposition produces large effect sizes on hierarchical tasks. The project's
  scope-aware (A) condition is conceptually similar to LtM (decompose first, then solve);
  achieving even **10-20% of LtM's relative gain** would be a strong Phase 2 outcome.
* **Sequential solution-reuse** (each subproblem uses prior solutions in its context) is a
  detail worth replicating in the project's scope-aware (A) implementation. Pure decomposition
  without solution-reuse is weaker.
* **Easy-to-hard generalization** is the right framing for the project's evaluation regime —
  the four benchmarks cover a wide difficulty range and any positive scope-conditioning effect
  must generalize beyond the in-context exemplars.

## Summary

Least-to-Most (LtM) prompting is a two-stage prompting technique designed to overcome chain-of-
thought's easy-to-hard generalization gap. The first stage decomposes a complex problem into a
sequence of simpler subproblems ordered by difficulty; the second stage solves each subproblem
using the answers to previously solved subproblems as additional context. The motivation is that
CoT performs well on test problems similar to in-context exemplars but degrades sharply when
test problems are harder.

Methodologically, LtM uses the same model (GPT-3 code-davinci-002 in the headline experiments)
in two prompting modes: decomposition and sequential solving. Evaluation covers SCAN
(compositional generalization), GSM8K (math), MultiArith (math), DROP (reading comprehension),
and Last Letter Concatenation (symbolic).

The headline result is **>=99% accuracy on SCAN length-split** with **just 14 exemplars**, vs.
**16% with vanilla chain-of-thought** — a **+83 absolute** gain. Other tasks show smaller but
consistent gains, with the improvement scaling with the easy-to-hard difficulty gap between
exemplars and test problems.

For the granularity-aware hierarchical agents project, LtM is the strongest empirical anchor for
the scope-aware (A) condition's expected effect size on hierarchical tasks. The +83 absolute SCAN
gain sets the aspirational ceiling; the project's +5-to-+15 abs target on the four-source
composite is conservative against this anchor. Solution-reuse — each subproblem using prior
solutions in its context — is a detail worth replicating in scope-aware (A); pure decomposition
without solution-reuse loses much of LtM's gain.
