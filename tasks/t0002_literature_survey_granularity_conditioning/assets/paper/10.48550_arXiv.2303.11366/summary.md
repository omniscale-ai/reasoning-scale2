---
spec_version: "3"
paper_id: "10.48550_arXiv.2303.11366"
citation_key: "Shinn2023"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2023
* **Authors**: Noah Shinn 🇺🇸, Federico Cassano 🇺🇸, Edward Berman 🇺🇸, Ashwin Gopinath 🇺🇸,
  Karthik Narasimhan 🇺🇸, Shunyu Yao 🇺🇸
* **Venue**: NeurIPS 2023
* **DOI**: `10.48550/arXiv.2303.11366`

## Abstract

Large language models (LLMs) have been increasingly used to interact with external environments
(e.g., games, compilers, APIs) as goal-driven agents. However, it remains challenging for these
language agents to quickly and efficiently learn from trial-and-error as traditional
reinforcement learning methods require extensive training samples and expensive model
fine-tuning. We propose Reflexion, a novel framework to reinforce language agents not by updating
weights, but instead through linguistic feedback. Concretely, Reflexion agents verbally reflect
on task feedback signals, then maintain their own reflective text in an episodic memory buffer to
induce better decision-making in subsequent trials. Reflexion is flexible enough to incorporate
various types (scalar values or free-form language) and sources (external or internally
simulated) of feedback signals, and obtains significant improvements over a baseline agent
across diverse tasks (sequential decision-making, coding, language reasoning). For example,
Reflexion achieves a 91% pass@1 accuracy on the HumanEval coding benchmark, surpassing the
previous state-of-the-art GPT-4 that achieves 80%. We also conduct ablation and analysis studies
using different feedback signals, feedback incorporation methods, and agent types, and provide
insights into how they affect performance.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. Reflexion extends ReAct-style prompting agents [Yao2022]
with a **verbal self-reflection** loop across trials. After each failed trial, the agent writes
a natural-language critique of its own behavior, stores the critique in an episodic memory
buffer, and uses the buffer as additional context for the next trial. No model weights are
updated — the "learning" is entirely linguistic.

The architecture is hierarchical in a way directly relevant to the project: the per-trial
execution agent operates at one granularity (atomic action / subtask), while the reflector
operates at a higher granularity (global / strategic). This naturally maps onto the project's
global/subtask/atomic schema and is a strong template for the scope-aware (A) condition's
between-trial component.

For the project, Reflexion is best treated as a **Phase 3 ablation** rather than a Phase 2
baseline: the project should first establish whether scope conditioning helps without cross-trial
memory, then test whether Reflexion-style memory adds further gains.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
Reflexion architecture is:

```
For trial t = 1, 2, ..., T:
    [actor] runs ReAct-style policy on the task, producing trajectory τ_t
    [evaluator] grades τ_t and produces a feedback signal f_t
    [reflector] reads (τ_t, f_t) and writes a natural-language critique r_t
    Store r_t in the episodic memory buffer M
    For trial t+1, prepend M to the actor's prompt
```

The **actor** is typically a ReAct agent (Thought/Action/Observation). The **evaluator** can be
external (test runner, environment reward) or internally simulated (LLM judge). The **reflector**
is the same LLM in a different prompt mode that produces a free-form critique.

Datasets evaluated:
* **HumanEval** (Python coding) — Reflexion + GPT-4 reaches **91% pass@1**, vs. **80%** for
  vanilla GPT-4
* **AlfWorld** — significant gains over ReAct baseline
* **HotpotQA** — significant gains via reflection on QA failures

The paper's key ablations: feedback type (scalar vs. free-form text), feedback source (external
vs. internal), reflection horizon (last trial vs. all trials).

## Results

* **91% pass@1 on HumanEval** with Reflexion + GPT-4 — **+11 absolute** over vanilla GPT-4 (80%)
* Significant gains on **AlfWorld** sequential decision-making
* Significant gains on **HotpotQA** language reasoning
* **No weight updates** — pure prompting + memory buffer
* **Free-form text feedback outperforms scalar feedback** across most tasks
* **Internally simulated feedback** (LLM judge) is nearly as effective as external feedback for
  some tasks
* **Last-trial reflection** is often as effective as all-trials reflection, suggesting most of
  the gain comes from one-shot self-correction

## Innovations

### Verbal Reinforcement Learning Without Weight Updates

Reflexion is the first framework to deliver substantial multi-trial improvements via natural-
language self-reflection alone. This is a meaningful complement to RLHF, which requires expensive
gradient updates.

### Three-Component Architecture

Splitting the agent into actor, evaluator, and reflector — each potentially a different prompt
mode of the same model — is a clean architectural pattern that has been adopted by many later
agent systems.

### Episodic Memory as Linguistic State

The episodic memory buffer is the agent's "learned policy" expressed as natural language. This
makes the policy human-readable and editable, which is a significant departure from RL-trained
policies.

## Datasets

* **HumanEval** — 164 hand-written Python coding problems with unit tests.
* **AlfWorld** — text-based simulated household tasks.
* **HotpotQA** — multi-hop QA with Wikipedia.

All three are public benchmarks. AlfWorld requires the simulator runtime.

## Main Ideas

* Reflexion's actor/evaluator/reflector decomposition naturally aligns with the project's
  global/subtask/atomic schema. The reflector operates at the global granularity; the actor
  operates at subtask + atomic granularity.
* **Defer Reflexion to Phase 3 ablation**, not Phase 2 baseline. Including cross-trial memory in
  Phase 2 would conflate scope conditioning with episodic memory; the project's main hypothesis
  is about scope alone.
* The free-form-text-feedback finding (text > scalar) suggests that the project's Metric 2
  (overconfident error rate) should also be expressed as free-form rationale at evaluation time,
  not just a numeric score.

## Summary

Reflexion is a language-agent framework that adds a verbal self-reflection loop on top of
ReAct-style prompting agents. After each trial, the agent writes a free-form natural-language
critique of its own behavior, stores the critique in an episodic memory buffer, and uses the
buffer as additional context for the next trial. No model weights are updated — the learning is
entirely linguistic.

Methodologically, Reflexion has three components: an actor (ReAct policy), an evaluator (scalar
or free-form feedback), and a reflector (LLM in critique mode). The architecture is evaluated
on HumanEval coding, AlfWorld sequential decision-making, and HotpotQA reasoning, with ablations
on feedback type, feedback source, and reflection horizon.

The headline result is **91% pass@1 on HumanEval** with GPT-4 + Reflexion, an **+11 absolute**
gain over vanilla GPT-4 (80%) without any weight updates. Free-form text feedback outperforms
scalar feedback; internally simulated feedback is nearly as effective as external feedback;
last-trial reflection captures most of the gain.

For the granularity-aware hierarchical agents project, Reflexion's actor/evaluator/reflector
decomposition aligns with the global/subtask/atomic schema and is a strong template for the
scope-aware (A) condition's between-trial component. However, including cross-trial memory in
Phase 2 would conflate scope conditioning with episodic memory; Reflexion should be treated as a
Phase 3 ablation that tests whether memory adds gains *on top of* scope conditioning, not as the
Phase 2 baseline.
