---
spec_version: "3"
paper_id: "10.48550_arXiv.2210.03629"
citation_key: "Yao2022"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# ReAct: Synergizing Reasoning and Acting in Language Models

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2022 (arXiv); 2023 (ICLR)
* **Authors**: Shunyu Yao 🇺🇸, Jeffrey Zhao 🇺🇸, Dian Yu 🇺🇸, Nan Du 🇺🇸, Izhak Shafran 🇺🇸,
  Karthik Narasimhan 🇺🇸, Yuan Cao 🇺🇸
* **Venue**: ICLR 2023
* **DOI**: `10.48550/arXiv.2210.03629`

## Abstract

While large language models (LLMs) have demonstrated impressive capabilities across tasks in
language understanding and interactive decision making, their abilities for reasoning (e.g.
chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied
as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces
and task-specific actions in an interleaved manner, allowing for greater synergy between the
two: reasoning traces help the model induce, track, and update action plans as well as handle
exceptions, while actions allow it to interface with external sources, such as knowledge bases or
environments, to gather additional information. We apply our approach, named ReAct, to a diverse
set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art
baselines, alongside improved human interpretability and trustworthiness over methods without
reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification
(Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-
thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-
solving trajectories that are more interpretable than baselines without reasoning traces. On two
interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and
reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while
being prompted with only one or two in-context examples.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. ReAct introduces an agent paradigm where the language model
**alternates** between two kinds of tokens at each decision point: **Thought:** tokens (free-form
reasoning) and **Action:** tokens (calls to external tools or environments). This interleaving
prevents two failure modes that pure chain-of-thought suffers from: hallucinated facts (because
the agent can fetch real information via Action) and error propagation (because the next Thought
can revise the plan based on the Action's Observation).

The think-vs-act split that ReAct introduces is the **direct conceptual ancestor** of the
project's three-level granularity schema. ReAct uses two levels (think, act); the project's
schema refines this to three (global, subtask, atomic). The implementation and prompting patterns
in ReAct are therefore highly relevant: the project's scope-aware (A) condition can be viewed as
ReAct extended with an explicit per-token granularity tag.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources,
ReAct's prompting template is:

```
Thought 1: <reasoning>
Action 1: <tool_call>
Observation 1: <tool_response>
Thought 2: <reasoning>
Action 2: <tool_call>
Observation 2: <tool_response>
...
Thought N: I now know the answer.
Action N: Finish[<answer>]
```

Each `Thought` is free-form natural-language reasoning; each `Action` is a structured tool call
(`Search[query]`, `Lookup[entity]`, `Finish[answer]`, etc.); each `Observation` is the tool's
response. The model is prompted with **one or two complete trajectories** as in-context examples
and then runs autoregressively until it emits a `Finish[]` action.

Models evaluated include **PaLM-540B** and **GPT-3** at various sizes. Tasks include question
answering (HotpotQA), fact verification (Fever), interactive decision-making in a simulated
household (ALFWorld), and online shopping (WebShop). The paper does not fine-tune any model — all
gains come from prompting alone.

## Results

* **+34 absolute** success rate over imitation and RL baselines on **ALFWorld**
* **+10 absolute** success rate over imitation and RL baselines on **WebShop**
* On **HotpotQA**, ReAct overcomes hallucination and error-propagation issues that affect pure
  chain-of-thought
* On **Fever**, ReAct improves fact-verification accuracy via Wikipedia API access
* Only **one or two in-context examples** are needed — ReAct is a prompting technique, not a
  fine-tuned model
* Trajectories are **more interpretable** than baselines because the Thought tokens are
  human-readable

## Innovations

### Interleaved Thought-Action Prompting

Before ReAct, agent prompting typically separated reasoning from acting (chain-of-thought for
reasoning, prompt-and-execute for action). ReAct's interleaved structure lets the model use each
modality where it is strongest: reasoning for plan tracking, action for fact retrieval.

### Hallucination Reduction via Tool Grounding

By giving the model the option to fetch information from a knowledge base or environment, ReAct
substantially reduces the rate at which the model invents facts. This is the practical foundation
for all later retrieval-augmented and tool-augmented agent architectures.

### Trajectory Interpretability

Because Thought tokens are natural language, a human can read a ReAct trajectory and understand
why the agent made each decision. This is a significant departure from RL-trained agents where
intermediate states are opaque vectors.

## Datasets

* **HotpotQA** — multi-hop question answering with Wikipedia.
* **Fever** — fact verification.
* **ALFWorld** — interactive simulated household tasks.
* **WebShop** — online shopping environment with product search and purchase actions.

All four datasets are public; ALFWorld and WebShop require a custom simulator runtime.

## Main Ideas

* ReAct's think-vs-act split is the direct conceptual ancestor of the project's
  global/subtask/atomic schema. The project's scope-aware (A) condition can be implemented as
  ReAct extended with an explicit per-token granularity tag.
* The +34 absolute gain on ALFWorld is the strongest published evidence that prompt-only
  agent improvements can produce double-digit absolute effect sizes on multi-step decision tasks.
  The project's Phase 2 effect-size targets (+5 to +15 abs) are conservative against this
  reference.
* Trajectory interpretability is a side benefit worth preserving. The project should ensure
  scope-aware (A) trajectories remain human-readable and avoid opaque tool-call wrappers that
  would defeat ReAct's interpretability gain.

## Summary

ReAct introduces an agent prompting paradigm where the language model alternates between Thought
tokens (free-form reasoning) and Action tokens (calls to external tools or environments). The
motivation is that prior work treated reasoning (chain-of-thought) and acting (tool-use) as
separate problems, missing the synergy where reasoning helps the agent track and update its plan
while acting lets the agent ground its reasoning in real information.

Methodologically, ReAct uses one or two in-context examples to teach the model the
Thought/Action/Observation pattern, then runs autoregressively until the model emits a Finish
action. No fine-tuning is required. The paper evaluates on HotpotQA, Fever (knowledge tasks) and
ALFWorld, WebShop (interactive decision-making tasks).

The headline result is **+34 absolute** success-rate improvement on ALFWorld and **+10
absolute** on WebShop, both compared to imitation and reinforcement-learning baselines. ReAct
also reduces hallucination on HotpotQA and improves fact-verification on Fever via Wikipedia API
grounding, with the bonus of producing human-interpretable trajectories.

For the granularity-aware hierarchical agents project, ReAct is the conceptual ancestor of the
three-level granularity schema. The project's scope-aware (A) condition can be implemented as a
ReAct extension with explicit per-token granularity tags, preserving ReAct's interpretability
while adding scope discipline. The +34 ALFWorld gain is the strongest published evidence that
prompt-only agent improvements can produce large absolute effect sizes — the project's
+5-to-+15 abs targets are conservative against this benchmark.
