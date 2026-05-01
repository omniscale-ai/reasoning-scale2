---
spec_version: "3"
paper_id: "10.48550_arXiv.2402.03620"
citation_key: "Zhou2024b"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures

## Metadata

* **File**: `files/zhou_2024_self-discover.pdf`
* **Published**: 2024-02-06 (NeurIPS 2024)
* **Authors**: Pei Zhou, Jay Pujara, Xiang Ren (USC), Xinyun Chen, Heng-Tze Cheng, Quoc V. Le, Ed H.
  Chi, Denny Zhou, Swaroop Mishra, Huaixiu Steven Zheng (Google DeepMind)
* **Venue**: NeurIPS 2024 (also arXiv:2402.03620)
* **DOI**: `10.48550/arXiv.2402.03620`

## Abstract

We introduce SELF-DISCOVER, a general framework for LLMs to self-discover the task-intrinsic
reasoning structures to tackle complex reasoning problems that are challenging for typical prompting
methods. Core to the framework is a self-discovery process where LLMs select multiple atomic
reasoning modules such as critical thinking and step-by-step thinking, and compose them into an
explicit reasoning structure for LLMs to follow during decoding. SELF-DISCOVER substantially
improves GPT-4 and PaLM 2's performance on challenging reasoning benchmarks such as BigBench-Hard,
grounded agent reasoning, and MATH, by as much as 32% compared to Chain of Thought (CoT).
Furthermore, SELF-DISCOVER outperforms inference-intensive methods such as CoT-Self-Consistency by
more than 20%, while requiring 10-40x fewer inference compute. Finally, we show that the
self-discovered reasoning structures are universally applicable across model families: from PaLM 2-L
to GPT-4, and from GPT-4 to Llama2, and share commonalities with human reasoning patterns.

## Overview

SELF-DISCOVER addresses a core limitation of prompting techniques like Chain-of-Thought (CoT),
Plan-and-Solve, and decomposition-based prompting: each technique is a single, atomic reasoning
module applied uniformly regardless of the task's intrinsic structure. The authors argue that
different tasks demand different reasoning programs — symbolic manipulation rewards least-to-most
decomposition, while social reasoning benefits from reflective and perspective-taking moves — and
that LLMs should compose these modules adaptively per task rather than committing to a single a
priori scaffold.

The framework operates in two stages. Stage 1 runs once per task and uses three meta-prompts
(SELECT, ADAPT, IMPLEMENT) to pick relevant atomic modules from a pool of 39 (e.g., "step-by-step
thinking", "break the problem into sub-problems", "critical thinking", "reflective thinking"),
rephrase them for the task, and emit a JSON-formatted reasoning structure with key-value slots.
Stage 2 then prepends this discovered structure to every instance and asks the LLM to fill in the
slot values during decoding. Because Stage 1 amortizes its three extra inference calls across all
instances of the task, the per-instance cost is the same as plain CoT, while delivering large gains
on world-knowledge and grounded-agent tasks and modest gains on pure-arithmetic benchmarks.

## Architecture, Models and Methods

The seed module pool comprises 39 reasoning module descriptions in natural language, drawn from
prior cognitive-science and prompting literature, including "Use critical thinking", "Let's think
step by step", "Devise an experiment to test the hypothesis", and "How can I simplify this
problem?". Stage 1 issues three sequential meta-prompts to a generative model M with an unlabeled
task description and a few example instances t_i:

1. SELECT (D_S = M(p_S || D || t_i)) — choose a relevant subset of modules.
2. ADAPT (D_A = M(p_A || D_S || t_i)) — rephrase each selected module to be task-specific.
3. IMPLEMENT (D_I = M(p_A || S_human || D_A || t_i)) — convert the adapted modules into a JSON
   key-value reasoning structure, conditioned on a single human-written demonstration on a different
   task.

Stage 2 reuses D_I across all task instances: A = M(D_I || t). Models evaluated are GPT-4
(gpt-4-turbo-preview), GPT-3.5-turbo, instruction-tuned PaLM 2-L (with a stronger instruction-tuned
variant for MATH), and Llama-2-70B. Evaluation uses accuracy across 25 tasks: 23 BIG-Bench Hard
(BBH) tasks, Thinking for Doing (T4D) for grounded social-agent reasoning, and 200 subsampled MATH
test problems. Baselines include Direct Prompting, zero-shot CoT, Plan-and-Solve, CoT-Self-
Consistency (10 samples), Majority voting over each raw module (40 modules), Best-of-each-RM with
oracle labels, and the OPRO prompt-optimization method. Ablations remove each of SELECT, ADAPT, and
IMPLEMENT in turn.

## Results

* On 23 BBH tasks with PaLM 2-L, SELF-DISCOVER achieves **67%** average accuracy versus **60%** for
  CoT and **61%** for Plan-and-Solve (**+7 / +6** absolute), and outperforms Direct or CoT on
  **21/25** tasks.
* On BBH with GPT-4, SELF-DISCOVER reaches **81%** versus **75%** for CoT and **73%** for
  Plan-and-Solve (**+6 / +8** absolute).
* On the T4D grounded-agent task, SELF-DISCOVER reaches **69%** with PaLM 2-L (vs **40%** CoT,
  **42%** PS) and **85%** with GPT-4 (vs **52%** CoT, **53%** PS) — improvements of **+27 to +32**
  absolute, beating the expert-designed Foresee-and-Reflect (FaR) prompt.
* On MATH (200-example subsample), SELF-DISCOVER yields **50.5%** with PaLM 2-L and **73%** with
  GPT-4, a moderate **+1 to +7** gain. Error analysis shows the discovered reasoning structures are
  correct **87.5%** of the time; **74.7%** of remaining failures are downstream computation errors.
* On a per-category BBH breakdown for PaLM 2-L, SELF-DISCOVER vs CoT delta is largest on
  World-Knowledge (**+19.7**), strong on NLU (**+8.0**), moderate on Algorithmic (**+5.2**), and
  smallest on Multilingual (**+4.0** delta over Direct in the reported chart).
* SELF-DISCOVER uses **1** inference call per instance plus **3** task-level meta-prompts, while
  CoT-Self-Consistency requires **10x** more calls and majority-voting over each module requires
  **40x** more — yet SELF-DISCOVER still beats both in accuracy on the BBH-movie-recommendation and
  BBH-geometric-shapes subsets.
* Ablations show that all three actions matter: removing IMPLEMENT (using only SELECT+ADAPT in
  natural-language form) drops GPT-4 accuracy noticeably across the four ablation tasks, confirming
  that the JSON structured-output step is critical.
* Universality study: structures discovered by PaLM 2-L transfer to GPT-4 and structures discovered
  by GPT-4 transfer to Llama-2-70B with most of the gain retained, while OPRO-optimized prompts
  transfer worse.

## Innovations

### Two-Stage Self-Composition Framework

SELF-DISCOVER is the first prompting framework that explicitly composes a task-specific reasoning
program from a library of atomic modules using the LLM itself as the composer. Earlier methods such
as CoT, Plan-and-Solve, decomposition prompting, and step-back prompting each commit to one fixed
reasoning shape; SELF-DISCOVER instead chooses and combines among 39 modules based on the task,
producing a different structure per task family.

### SELECT-ADAPT-IMPLEMENT Meta-Prompts

The three-action decomposition (pick modules, rephrase to the task, lay out as JSON key-value slots)
is itself a contribution. Ablating any of the three drops performance, and using a single
human-written reasoning structure on a different task in the IMPLEMENT prompt is sufficient
in-context guidance to yield reliable JSON structures.

### Task-Level Amortization for Cheap Inference

By running Stage 1 once per task and reusing the resulting structure for every instance, the
per-instance cost is the same as CoT. This is the first method to combine self-consistency-level
accuracy with CoT-level inference cost on BBH and T4D, achieving a Pareto improvement of 10-40x
fewer calls at higher accuracy.

### Cross-Model Universality of Reasoning Structures

Self-discovered structures from a stronger model (PaLM 2-L or GPT-4) transfer to weaker models
(GPT-4 or Llama-2-70B) with most accuracy gain retained, more so than OPRO-optimized prompt wording.
This suggests reasoning structure is a model-agnostic abstraction, complementary to
prompt-engineering wording optimization.

## Datasets

* **BIG-Bench Hard (BBH)** — 23 challenging tasks selected from BIG-Bench, spanning Algorithmic and
  Multi-Step Arithmetic, Natural Language Understanding, Use of World Knowledge, and Multilingual
  Knowledge and Reasoning. Public; standard accuracy metric.
* **Thinking for Doing (T4D)** — grounded social agent reasoning task from Zhou et al. 2023 where
  models must use mental-state reasoning to determine actions; GPT-4 with CoT reaches around 50%.
  Public.
* **MATH** (Hendrycks et al. 2021) — 200 examples subsampled from the test set, using one-shot
  instance-level reasoning structures due to MATH's complexity. Public.
* **Seed reasoning modules** — 39 module descriptions in natural language taken from prior prompting
  literature; provided in Appendix A of the paper.

## Main Ideas

* Reasoning shape should be **task-conditioned, not method-conditioned**: prompting frameworks that
  fix a single reasoning style underperform on tasks whose intrinsic structure does not match.
  Letting the LLM compose from atomic modules is a low-cost way to get this conditioning.
* **Structure beats wording for transfer**: discovered reasoning structures move across model
  families more cleanly than optimized prompt phrasing, suggesting that "what to think about" is a
  more portable abstraction than "what words to use".
* **Computation-aware prompting matters**: SELF-DISCOVER's task-level amortization (3 extra calls
  total, then 1 per instance) achieves better accuracy than 10-40x more expensive ensembles, arguing
  that test-time compute should be invested in better structure not more samples.
* **Explicit JSON key-value scaffolds outperform free-text plans**: ablations show the IMPLEMENT
  step that emits structured key-value slots is the largest single contributor, beyond mere module
  selection or natural-language planning.
* **Computation errors dominate residual failures on math**: 74.7% of MATH failures stem from
  arithmetic execution despite correct high-level structure, pointing toward tool-use or
  verifier-based mitigations as the next bottleneck.

## Summary

SELF-DISCOVER tackles the question of whether LLMs can themselves compose the right reasoning
program for a task instead of relying on a fixed prompting template. The authors argue that
single-shape methods like CoT and Plan-and-Solve are mismatched to many tasks, and that a task's
intrinsic reasoning structure is best discovered explicitly. Their framework supplies the LLM with a
pool of 39 atomic reasoning modules and three meta-prompts (SELECT, ADAPT, IMPLEMENT) that pick,
specialize, and lay out a JSON reasoning structure per task; this structure is then reused across
all instances of the task at no per-instance overhead beyond plain CoT.

The methodology runs Stage 1 once per task (three inference calls) and Stage 2 once per instance.
Models tested are GPT-4, GPT-3.5, PaLM 2-L, and Llama-2-70B, evaluated on 23 BIG-Bench Hard tasks,
the T4D grounded-agent task, and 200 MATH test problems. Baselines span Direct, CoT, Plan-and-
Solve, CoT-Self-Consistency, per-module majority voting, oracle best-of-each-module, and the OPRO
prompt optimizer. Ablations on SELECT/ADAPT/IMPLEMENT and a transfer study from PaLM 2-L to GPT-4
and GPT-4 to Llama-2-70B round out the experiments.

Headline results: SELF-DISCOVER beats CoT by 6-7 absolute on BBH average and by 27-32 absolute on
T4D for both PaLM 2-L and GPT-4, and beats CoT-Self-Consistency and per-module majority voting while
using 10-40x fewer inference calls. On MATH the gain is modest (1-7 points), and 74.7% of remaining
failures are downstream computation errors rather than structural reasoning errors. Discovered
structures transfer across model families with most of the gain retained, indicating that reasoning
structure is a portable abstraction.

For the t0017 hierarchical-agents-and-judges literature survey, this paper is directly relevant
because it operationalizes a hierarchical reasoning idea: a task-level "planner" composes an
explicit structure that an instance-level "executor" then fills in. It demonstrates that explicit
JSON-structured plans beat free-text plans, that task-level meta-prompts amortize cleanly to per-
instance cost, and that structured reasoning is more transferable than wording. These findings
support hierarchical-agent designs that separate plan composition from plan execution and motivate
judges that evaluate structural correctness independently from value-filling correctness — the exact
decomposition this project's hierarchical-judge designs are exploring.
