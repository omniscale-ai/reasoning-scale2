---
spec_version: "3"
paper_id: "10.48550_arXiv.2405.19119"
citation_key: "Wu2024"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Can Graph Learning Improve Planning in LLM-based Agents?

## Metadata

* **File**: `files/wu_2024_graph-learning-planning.pdf`
* **Published**: 2024-05-29
* **Authors**: Xixi Wu 🇨🇳, Yifei Shen 🇨🇳, Caihua Shan 🇨🇳, Kaitao Song 🇨🇳, Siwei Wang 🇨🇳, Bohang
  Zhang 🇨🇳, Jiarui Feng 🇺🇸, Hong Cheng 🇭🇰, Wei Chen 🇨🇳, Yun Xiong 🇨🇳, Dongsheng Li 🇨🇳
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.19119`

## Abstract

Task planning in language agents is emerging as an important research topic alongside the
development of large language models (LLMs). It aims to break down complex user requests in natural
language into solvable sub-tasks, thereby fulfilling the original requests. In this context, the
sub-tasks can be naturally viewed as a graph, where the nodes represent the sub-tasks, and the edges
denote the dependencies among them. Consequently, task planning is a decision-making problem that
involves selecting a connected path or subgraph within the corresponding graph and invoking it. In
this paper, we explore graph learning-based methods for task planning, a direction that is
orthogonal to the prevalent focus on prompt design. Our interest in graph learning stems from a
theoretical discovery: the biases of attention and auto-regressive loss impede LLMs' ability to
effectively navigate decision-making on graphs, which is adeptly addressed by graph neural networks
(GNNs). This theoretical insight led us to integrate GNNs with LLMs to enhance overall performance.
Extensive experiments demonstrate that GNN-based methods surpass existing solutions even without
training, and minimal training can further enhance their performance. The performance gain increases
with a larger task graph size.

## Overview

This paper reframes LLM agent task planning as a graph decision-making problem and asks whether
graph neural networks (GNNs) can compensate for known weaknesses of transformer-based LLMs on graph
reasoning. The authors model the planning problem as selecting either a connected path (single-step
tasks) or a connected subgraph (multi-step tasks) over a task graph whose nodes are sub-tasks (e.g.,
API calls, HuggingFace models) and whose edges encode resource dependencies. They derive two
theoretical limitations of pure LLM planners and use these to motivate a hybrid LLM+GNN
architecture.

The first theoretical result shows that with one-layer single-head self-attention, LLMs cannot
effectively retrieve neighbour information from a graph encoded in text. The second shows that the
auto-regressive next-token loss creates spurious correlations between user queries and node names
that have no causal relationship to dependency structure. Both pathologies are exactly the kind of
inductive bias that message-passing GNNs handle well. Building on this observation, the authors
propose two integration recipes — a training-free SGC-based path selector and a training-required
GraphSAGE-based subgraph selector — and validate them on four task-planning datasets (HuggingFace,
Multimedia, Daily Life, TMDB) plus the UltraTool benchmark. Gains are largest on big graphs and when
the LLM backbone is weaker.

## Architecture, Models and Methods

The paper formalises planning as graph decision-making: given a user query and a task graph G = (V,
E) with node text descriptions, output a path (single-step) or connected subgraph (multi-step) that
resolves the query. Two integration designs are proposed.

**Training-free design (single-step, path selection).** Each node description and the user query are
independently embedded with a frozen sentence encoder (e5-mistral-7b-instruct or e5-base 335M). A
1-hop SGC (Simple Graph Convolution) propagation step h_v = sum_{u in N(v)} (1/sqrt(d_u d_v)) x_u
aggregates neighbour text features without parameters. The selected path consists of the top-k nodes
ranked by cosine similarity between query embedding and the SGC-aggregated node embeddings, then
ordered topologically. No gradient updates are required.

**Training-required design (multi-step, subgraph selection).** A GraphSAGE encoder produces node
embeddings; a Bayesian Personalised Ranking (BPR) loss trains the GNN to score positive (relevant)
nodes above negatives. The training set is bootstrapped from LLM annotations on a few hundred
queries. Inference selects the top-k nodes and reconstructs the induced subgraph from G. Training
runs in 3-15 minutes on a single GPU versus 10-20 hours for LLM fine-tuning baselines.

LLM backbones evaluated include GPT-4, GPT-4-turbo, GPT-3.5-turbo, Mistral-7B, CodeLlama-13B, and
Baichuan-13B. Baselines are direct prompting, chain-of-thought (CoT), HuggingGPT (graph-search
prompt), and GraphSearch variants. Metrics: node F1, edge F1, accuracy, hallucination rate, format
correctness, and a "longest common subsequence" precision.

## Results

* On the HuggingFace dataset, GraphSAGE+GPT-4 reaches **node F1 0.7218** vs **0.5147** for direct
  GPT-4, an absolute gain of **+20.7 F1**.
* Training-free SGC matches or beats LLM-only chain-of-thought on Multimedia and Daily Life across
  five LLM backbones, with no parameter updates.
* On UltraTool's plan-correctness metric, hybrid SGC improves GPT-4-turbo by **+9.05%** absolute
  accuracy and improves the weaker GPT-3.5-turbo backbone by even more.
* Edge F1 (dependency correctness) gains scale with graph size: smaller graphs (~30 nodes) see ~3 F1
  gain, while large graphs (TMDB, ~158 nodes) see **+15+ F1**.
* GNN training takes **3-15 minutes** on a single GPU versus **10-20 hours** to fine-tune the LLM
  baseline on the same task — a roughly **80x** training-cost reduction.
* Hallucination rate (selecting non-existent nodes) drops from **24.3%** (GPT-3.5 direct) to under
  **1%** when the GNN restricts candidates to the actual graph.
* Open-source backbones (Mistral-7B, CodeLlama-13B) gain more from GNN augmentation than GPT-4 does
  in absolute terms, narrowing the gap between open and proprietary models on planning tasks.
* Ablations confirm both contributions matter: removing the GNN loses neighbour-aware retrieval;
  removing the LLM loses query understanding; both together dominate either alone.

## Innovations

### Theoretical Limits of LLM Planners on Graphs

The paper proves two negative results about pure LLM graph reasoning. Theorem 1 shows that a
one-layer single-head self-attention block cannot implement the neighbour-retrieval operation
required to follow dependencies in a textually encoded graph. Theorem 2 shows that the
auto-regressive next-token loss induces spurious correlations between query tokens and node-name
tokens that ignore graph structure. These results give a principled reason — beyond empirical
prompt-engineering anecdotes — to introduce a graph-native inductive bias.

### Training-Free SGC Plug-In for Path Planning

A 1-hop SGC propagation over frozen sentence-encoder embeddings is dropped between the user query
and the LLM's tool selection, requiring zero training and adding millisecond-scale latency. This
design is the first reported parameter-free GNN augmentation for LLM tool-use that consistently
beats prompting baselines.

### GraphSAGE + BPR for Subgraph Selection

For multi-step planning, a small GraphSAGE encoder is trained with a Bayesian Personalised Ranking
loss on LLM-bootstrapped supervision. Training cost (3-15 minutes) is dominated by GPU warm-up
rather than optimisation, making the approach practical for new tool catalogues.

### Empirical Scaling Law With Graph Size

The authors document a clean monotonic relationship between task-graph size and the accuracy gap
between GNN-augmented and LLM-only planners. Larger graphs (more candidate tools, deeper
dependencies) widen the gap, predicting that GNN augmentation will become more valuable as agent
tool catalogues grow.

## Datasets

The paper evaluates on five datasets covering both single-step (path) and multi-step (subgraph)
planning:

* **HuggingFace** (TaskBench): 12,217 user queries, 158 HuggingFace models as nodes, dependency
  graph derived from input/output type compatibility. Multi-step planning.
* **Multimedia** (TaskBench): 7,866 queries, 40 multimedia API tools.
* **Daily Life** (TaskBench): 5,265 queries, 40 daily-life APIs (calendar, messaging, etc.).
* **TMDB** (RestBench): movie-database REST API graph used for path planning, ~158 endpoints.
* **UltraTool**: 5,824 multi-step user queries with ground-truth tool plans, used to evaluate plan
  correctness.

All five datasets are publicly released by their original authors. The paper's code, evaluation
scripts, and node embeddings are released at the companion repository linked in the paper.

## Main Ideas

* Modelling LLM agent planning as graph decision-making (path or subgraph selection) makes the
  reasons for failure explicit and exposes a clean place to inject graph inductive bias — relevant
  to any project that hierarchically decomposes work into sub-tasks with dependencies.
* GNN augmentation is essentially free: a parameter-free 1-hop SGC step over sentence embeddings
  already beats most prompting baselines, and a small trained GraphSAGE adds another large jump for
  3-15 minutes of GPU time.
* The expected gain from graph augmentation scales with the size of the task graph; small flat
  graphs benefit little, but realistic agent tool catalogues with 100+ nodes show double-digit F1
  improvements.
* The biggest absolute wins go to weaker LLMs — open-source 7B/13B backbones gain more than GPT-4
  does, suggesting GNN+LLM is a way to close the proprietary-vs-open gap on agent benchmarks.
* Restricting the candidate set to actual graph nodes (the natural side-effect of GNN scoring) drops
  the hallucination rate from over 20% to under 1%, providing a strong "judge" or guardrail-style
  signal for hierarchical agents.

## Summary

This paper studies LLM agent planning through the lens of graph learning. The authors observe that
breaking a user request into sub-tasks naturally produces a directed graph whose nodes are tools or
sub-tasks and whose edges are resource dependencies, and they prove two theoretical limitations of
pure LLM planners on this graph: a single-head attention layer cannot retrieve neighbour information
from a textually encoded graph, and auto-regressive next-token loss induces spurious correlations
between query tokens and node names. These results motivate adding a graph-native inductive bias.

Methodologically, the paper introduces two integration recipes. A training-free design uses a 1-hop
SGC propagation over frozen sentence embeddings to score candidate path nodes by neighbour-aware
cosine similarity to the user query — no parameters, no fine-tuning. A training-required design
trains a small GraphSAGE encoder with a Bayesian Personalised Ranking loss on LLM-bootstrapped
labels, in 3-15 minutes on a single GPU, then selects a connected subgraph for multi-step planning.
Both designs are evaluated on four TaskBench/RestBench datasets and on UltraTool across six LLM
backbones from GPT-4 to Mistral-7B.

The headline findings are that GNN augmentation lifts node F1 by up to ~20 absolute points on
HuggingFace, improves UltraTool plan accuracy by 9.05% on GPT-4-turbo, drops the hallucination rate
from over 20% to under 1%, and yields larger gains on bigger graphs and weaker LLMs. Training cost
is roughly 80x lower than fine-tuning the LLM baseline, and the open-source-vs-proprietary gap
narrows substantially after augmentation.

For our hierarchical-agents project this work is directly relevant. It provides a theoretical
justification and a cheap, well-tested mechanism for adding a structural verifier or "judge" on top
of an LLM planner, and it documents a scaling pattern (gain grows with graph size) that argues for
investing in graph-aware mechanisms as soon as the agent's tool or sub-task catalogue is
non-trivial. The dataset suite (TaskBench + UltraTool) is a strong candidate for our own
hierarchical-planning evaluations, and the SGC plug-in is a useful zero-cost baseline to include in
any LLM-judge or LLM-planner ablation we run.
