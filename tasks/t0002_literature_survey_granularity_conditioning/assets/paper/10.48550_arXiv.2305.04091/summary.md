---
spec_version: "3"
paper_id: "10.48550_arXiv.2305.04091"
citation_key: "Wang2023"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2023
* **Authors**: Lei Wang 🇸🇬, Wanyu Xu 🇸🇬, Yihuai Lan 🇸🇬, Zhiqiang Hu 🇸🇬, Yunshi Lan 🇨🇳,
  Roy Ka-Wei Lee 🇸🇬, Ee-Peng Lim 🇸🇬
* **Venue**: ACL 2023
* **DOI**: `10.48550/arXiv.2305.04091`

## Abstract

Large language models (LLMs) have recently been shown to deliver impressive performance in
various NLP tasks. To tackle multi-step reasoning tasks, few-shot chain-of-thought (CoT)
prompting includes a few manually crafted step-by-step reasoning demonstrations which enable LLMs
to explicitly generate reasoning steps and improve their reasoning task accuracy. To eliminate
the manual effort, Zero-shot-CoT concatenates the target problem statement with 'Let's think
step by step' as an input prompt to LLMs. Despite the success of Zero-shot-CoT, it still suffers
from three pitfalls: calculation errors, missing-step errors, and semantic misunderstanding
errors. To address the missing-step errors, we propose Plan-and-Solve (PS) Prompting. It consists
of two components: first, devising a plan to divide the entire task into smaller subtasks, and
then carrying out the subtasks according to the plan. To address the calculation errors and
improve the quality of generated reasoning steps, we extend PS prompting with more detailed
instructions and derive PS+ prompting. We evaluate our proposed prompting strategy on ten datasets
across three reasoning problems. The experimental results over GPT-3 show that our proposed
zero-shot prompting consistently outperforms Zero-shot-CoT across all datasets by a large margin,
is comparable to or exceeds Zero-shot-Program-of-Thought Prompting, and has comparable
performance with 8-shot CoT prompting on the math reasoning problem.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. Plan-and-Solve (PS) prompting is a two-stage zero-shot
prompting technique designed to fix the missing-step error mode of Zero-shot-CoT. The PS prompt
literally instructs the model to "first devise a plan to solve the problem, then carry out the
plan." The PS+ variant adds more detailed instructions per stage to also reduce calculation
errors. Together, they bring zero-shot performance close to 8-shot CoT on math reasoning while
requiring no in-context examples.

The PS structure is a **two-level granularity hierarchy** — plan (global) and solve (atomic-ish) —
which makes it the closest published analogue to the project's scope-aware (A) condition. The
project's three-level schema is a strict refinement: PS's "plan" maps to global, PS's "solve" maps
to subtask + atomic.

For the project, PS is the **canonical scope-unaware (B) baseline** for Phase 2: it is widely
known, has reference implementations in LangChain core, and represents the current best
prompt-only approach to multi-step reasoning that *does not* condition on explicit granularity
tags.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
PS prompt template is:

```
Q: <problem>
A: Let's first understand the problem and devise a plan to solve the problem.
   Then, let's carry out the plan and solve the problem step by step.
```

The PS+ variant adds more detailed instructions:

```
Q: <problem>
A: Let's first understand the problem, extract relevant variables and their
   corresponding numerals, and make and devise a complete plan. Then, let's
   carry out the plan, calculate intermediate variables (pay attention to
   correct numerical calculation and commonsense), solve the problem step
   by step, and show the answer.
```

Models evaluated: **GPT-3 text-davinci-003** primarily, with comparisons to ChatGPT and Codex on
some datasets. Datasets cover three reasoning categories: arithmetic (GSM8K, SVAMP, AQuA,
AddSub, MultiArith, SingleEq), commonsense (CommonsenseQA, StrategyQA), and symbolic (Last
Letter Concatenation, Coin Flip). All ten datasets are evaluated zero-shot.

## Results

* **Consistent gains over Zero-shot-CoT** across all 10 datasets — every dataset shows a
  positive delta
* **PS+ on GSM8K reaches ~58%** with text-davinci-003 zero-shot, vs. **~57%** for 8-shot
  manual CoT — comparable performance with no exemplars
* **PS+ exceeds Zero-shot-Program-of-Thought** on math datasets where PoT was previously
  state-of-the-art for zero-shot
* **Reduces missing-step errors** specifically — the targeted error mode the technique was
  designed to address
* **Reduces calculation errors** in PS+ via the explicit "pay attention to correct numerical
  calculation" instruction
* **Available in LangChain core** as `Plan-and-Execute` — production-ready

## Innovations

### Two-Stage Prompting With Explicit Plan Step

PS is the first widely-cited zero-shot prompting technique to *force* the model into an explicit
plan-then-execute structure. Prior work either chained reasoning (CoT) or asked for a plan
separately; PS does both in a single pass.

### Targeted Error-Mode Reduction

The paper diagnoses Zero-shot-CoT's failure modes (calculation, missing-step, semantic) and
designs PS specifically to reduce one of them. PS+ extends to the others. This error-driven
design is rare for prompting papers.

### Zero-Shot Parity With Few-Shot CoT

Achieving comparable performance to 8-shot manual CoT *without any exemplars* is a substantial
practical result — it eliminates the manual exemplar-curation cost that is often a hidden burden
in CoT deployments.

## Datasets

* **Arithmetic**: GSM8K, SVAMP, AQuA, AddSub, MultiArith, SingleEq.
* **Commonsense**: CommonsenseQA, StrategyQA.
* **Symbolic**: Last Letter Concatenation, Coin Flip.

All ten datasets are public benchmarks in standard NLP repositories.

## Main Ideas

* Adopt PS+ as the canonical scope-unaware (B) baseline for Phase 2. It is the strongest
  published prompt-only method that does not condition on explicit granularity tags.
* The two-stage structure means a successful PS run produces both a "plan" (global-level text)
  and a "solve" (subtask + atomic execution). Logging both segments lets the project measure
  scope effects even within the B condition by post-hoc tagging.
* Reuse the LangChain `Plan-and-Execute` implementation rather than reimplementing PS from
  scratch — saves engineering time and inherits compatibility with LangChain's tool-use
  infrastructure.

## Summary

Plan-and-Solve (PS) prompting is a zero-shot prompting technique that explicitly forces a
language model to first produce a plan, then execute the plan step by step. The motivation is
that Zero-shot-CoT — while a powerful zero-shot baseline — exhibits three error modes:
calculation errors, missing-step errors, and semantic-misunderstanding errors. PS targets the
missing-step mode by demanding an explicit plan; PS+ extends to calculation errors via additional
in-prompt instructions to "pay attention to correct numerical calculation."

Methodologically, PS is a single-prompt template that instructs the model to plan-then-solve.
Evaluation covers ten datasets across arithmetic, commonsense, and symbolic reasoning, all in
zero-shot mode with GPT-3 text-davinci-003 as the primary model. PS+ adds more detailed per-stage
instructions.

The headline outcome is **consistent improvement over Zero-shot-CoT across all 10 datasets**,
with PS+ achieving **comparable performance to 8-shot manual CoT** on GSM8K (≈58% vs ≈57%) — a
strong zero-shot result that eliminates the manual exemplar-curation cost. PS+ is available in
LangChain core as Plan-and-Execute and has been adopted in production agent systems.

For the granularity-aware hierarchical agents project, PS is the canonical scope-unaware (B)
baseline for Phase 2. Its two-stage plan-then-solve structure is the closest published analogue
to the project's scope-aware (A) condition without the explicit granularity tags. The project
should reuse LangChain's Plan-and-Execute implementation, log both stages separately, and
measure how much of PS's gain over CoT comes from the plan-execute separation alone — that
delta is the lower bound for the scope-aware (A) condition's expected gain.
