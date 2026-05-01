---
spec_version: "3"
paper_id: "no-doi_Gao2026_hierarchical-preference-learning-llm-agents"
citation_key: "Gao2026"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents

## Metadata

* **File**: `files/gao_2026_hierarchical-preference-learning.pdf`
* **Published**: 2026 (ICLR 2026; arXiv preprint 2025-10-03)
* **Authors**: Heyang Gao 🇨🇳, Zexu Sun 🇨🇳, Erxue Min 🇨🇳, Hengyi Cai 🇨🇳, Shuaiqiang Wang 🇨🇳, Dawei
  Yin 🇨🇳, Xu Chen 🇨🇳
* **Venue**: ICLR 2026 (conference)
* **arXiv**: `2510.03253`
* **OpenReview**: `s8usvGHYlk`

## Abstract

Large Language Models (LLMs) as autonomous agents are increasingly tasked with solving complex,
long-horizon problems. Aligning these agents via preference-based offline methods like Direct
Preference Optimization (DPO) is a promising direction, yet it faces a critical granularity
mismatch. Trajectory-level DPO provides a signal that is too coarse for precise credit assignment,
while step-level DPO is often too myopic to capture the value of multi-step behaviors. To resolve
this challenge, we introduce Hierarchical Preference Learning (HPL), a hierarchical framework that
optimizes LLM agents by leveraging preference signals at multiple, synergistic granularities. While
HPL incorporates trajectory- and step-level DPO for global and local policy stability, its core
innovation lies in group-level preference optimization guided by a dual-layer curriculum. Our
approach first decomposes expert trajectories into semantically coherent action groups and then
generates contrasting suboptimal groups to enable preference learning at a fine-grained, sub-task
level. Then, instead of treating all preference pairs equally, HPL introduces a curriculum scheduler
that organizes the learning process from simple to complex. This curriculum is structured along two
axes: the group length, representing sub-task complexity, and the sample difficulty, defined by the
reward gap between preferred and dispreferred action groups. Experiments on three challenging agent
benchmarks show that HPL outperforms existing state-of-the-art methods. Our analyses demonstrate
that the hierarchical DPO loss effectively integrates preference signals across multiple
granularities, while the dual-layer curriculum is crucial for enabling the agent to solve a wide
range of tasks, from simple behaviors to complex multi-step sequences.

## Overview

Long-horizon LLM agents must produce dozens of interleaved reasoning and tool-use steps before a
sparse terminal reward arrives. Two existing offline preference paradigms each fail in distinct
ways. Trajectory-level DPO compresses an entire rollout into a single preferred-vs-dispreferred
pair, which yields stable gradients but cannot localise where the trajectory went wrong. Step-level
DPO prefers a contrasting action at every individual step, which is fine-grained but statistically
noisy and frequently rewards locally plausible moves that hurt the global plan. The authors call
this the "granularity mismatch" and frame their contribution as a principled middle ground: a
group-level DPO loss whose preference unit is a semantically coherent cluster of consecutive actions
corresponding to a sub-task, paired with full trajectory- and step-level DPO terms for
multi-resolution stability.

The work goes beyond defining a new loss. The authors construct contrasting suboptimal groups for
each expert sub-task and show that naively training on all such pairs is suboptimal, motivating a
dual-layer curriculum that progresses from short, high-margin groups to long, low-margin ones. The
combination beats the strongest published baselines on three established agent benchmarks (ALFWorld,
WebShop, InterCode-SQL) for both Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct base policies, and
the ablations cleanly attribute the gains to the group-level loss and the curriculum.

## Architecture, Models and Methods

HPL is an offline preference-optimization recipe with four interlocking components. (1) **Action
group segmentation.** Each expert trajectory of T thought-action-observation steps is partitioned
into G semantically coherent groups. The paper compares four segmentation strategies: Fixed-N (fixed
number of groups), Fixed-K (fixed group length), Uncertainty-based (segment boundaries at high
token-level entropy), and Semantic (GPT-4o is asked to insert sub-task boundaries). The Semantic
variant is the default. (2) **Suboptimal group construction.** For every expert group the authors
generate one or more contrasting suboptimal groups by rolling out a behaviour-cloned policy from the
same prefix; only rollouts whose group-level reward is strictly worse become "dispreferred" and pair
with the expert group as "preferred". (3) **Hierarchical DPO loss.** The training objective is a
weighted sum L = L_traj + lambda_step * L_step + lambda_group * L_group, where L_group applies the
standard DPO log-sigmoid contrast at the group level (the policy log-ratio is summed only over
tokens inside the group). The reference is a frozen SFT policy. (4) **Dual-layer curriculum.** Pairs
are bucketed along two axes: group length (short -> long, a proxy for sub-task complexity) and
reward gap deltaR between preferred and dispreferred groups (large gap = easy, small gap = hard).
Training proceeds in three phases: foundational (short groups, large deltaR), expanding (medium
groups and gaps), full-scale (all pairs).

Base models are Qwen2.5-1.5B-Instruct and Qwen2.5-7B-Instruct. SFT uses learning rate 1e-5, batch
size 32, 3 epochs. Group-DPO uses learning rate 3e-6 on ALFWorld and 1e-6 on WebShop and
InterCode-SQL, batch size 32, 1 epoch, beta = 0.3, max sequence length 6000. The paper additionally
provides Proposition 1, a bias-variance analysis showing that group-level DPO improves estimator
variance by a factor of order Omega(T / log(1 / epsilon)) over step-level DPO while keeping bias
bounded.

## Results

* **Average across 3 benchmarks (Qwen2.5-7B-Instruct):** SFT 61.28, ETO 62.93, IPR 63.84, **HPL
  (Semantic) 67.81** — a +3.97 absolute gain over the strongest baseline (IPR) and +4.88 over ETO.
* **ALFWorld seen / unseen (Qwen2.5-7B):** SFT 67.14 / 76.12, ETO 70.00 / 76.87, IPR 72.86 / 77.61,
  **HPL 83.57 / 86.57** (+10.71 / +8.96 over IPR).
* **WebShop (Qwen2.5-7B):** SFT 60.53, ETO 61.57, IPR 61.90, **HPL 62.56**.
* **InterCode-SQL (Qwen2.5-7B):** SFT 66.86, ETO 68.63, IPR 69.19, **HPL 70.63**.
* **Curriculum ablation (Qwen2.5-1.5B average):** removing the dual-layer curriculum drops HPL from
  **58.73 to 57.58**; both axes (length and difficulty) contribute positively.
* **Loss ablation:** the group-level DPO term is the most critical of the three losses; removing it
  produces the largest drop on every benchmark, confirming it as the source of the headline
  improvement rather than just adding extra DPO regularisation.
* **Segmentation ablation:** Semantic (GPT-4o) > Uncertainty > Fixed-K ~ Fixed-N, with the gap
  between Semantic and Fixed-N around 1-2 average points.

## Innovations

### Group-Level DPO with Bias-Variance Guarantee

The headline contribution is a DPO objective whose preference unit is a semantically coherent action
group rather than the whole trajectory or a single step. Proposition 1 formalises the intuitive
claim: at fixed sample budget, group-level DPO achieves a variance reduction of order Omega(T /
log(1 / epsilon)) versus step-level DPO while keeping bias bounded by the group size times the
per-step bias. This is the first published bias-variance analysis specifically for mid-granularity
preference learning.

### Semantic Action Group Segmentation

The default segmentation strategy uses GPT-4o to insert sub-task boundaries inside each expert
trajectory. The paper compares this to three non-LLM alternatives (Fixed-N, Fixed-K, and
token-uncertainty-based) and shows the semantic strategy wins. This isolates "what is a sub-task" as
a quantifiable design choice rather than an implementation detail.

### Dual-Layer Curriculum on Length and Reward Gap

Curriculum learning for DPO is not new, but ordering pairs along two orthogonal axes — sub-task
length and reward gap — is. The three-phase schedule (foundational -> expanding -> full-scale) is
shown to be necessary: the ablation removing it loses ~1 absolute point and the ablation removing
either single axis loses less but still hurts.

### Multi-Granularity Loss Composition

HPL is the first paper to combine trajectory-, step-, and group-level DPO losses simultaneously into
a single training objective. Prior work picked one granularity (e.g. ETO uses trajectory, IPR uses
step). The composition is empirically shown to be additive: each level contributes and the
combination is best.

## Datasets

* **ALFWorld** — 3,553 training scenarios, 140 seen + 134 unseen test scenarios. Embodied household
  tasks with high-level natural language goals; long horizons (often 30+ actions). Public release;
  standard agent benchmark.
* **WebShop** — 200 test tasks over a simulated e-commerce site with ~1.18M products. Web-based
  product search and purchase task. Public release.
* **InterCode-SQL (Spider split)** — 200 test tasks over Spider databases. Multi-turn SQL generation
  with execution feedback. Public release.
* **Expert demonstrations** — for each benchmark the authors use the publicly released expert
  trajectories from the ETO and IPR papers; no new human annotation is collected.

The paper does not introduce a new dataset.

## Main Ideas

* The "granularity mismatch" framing is a useful lens for our project: trajectory-level signals
  conflate scope-aware and scope-mismatched failures, while step-level signals lose the sub-task
  context this project's hierarchy explicitly tracks.
* Semantically coherent action groups (i.e. sub-tasks identified by an LLM) are an effective
  intermediate granularity for both training signal and evaluation; this aligns directly with our
  three-level (global / subtask / atomic) annotation schema.
* A curriculum that starts with short, high-margin pairs and progresses to long, low-margin ones
  produces measurable gains on top of plain DPO. If we ever fine-tune a scope-aware policy, this is
  the curriculum recipe to copy.
* HPL's experiments on ALFWorld, WebShop, and InterCode-SQL provide strong recent baselines (ETO,
  IPR, HPL itself) for any agent-training task we may launch downstream.
* The bias-variance analysis (Proposition 1) gives a principled reason to prefer mid-granularity
  signals when reward sparsity and trajectory length are large — relevant for our long-horizon
  benchmarks (FrontierScience-Olympiad, SWE-bench Verified).

## Summary

Gao et al. tackle a real and well-defined problem in offline alignment of long-horizon LLM agents:
trajectory-level DPO is too coarse to attribute failure to a specific sub-task, and step-level DPO
is too noisy to capture the value of multi-step behaviour. They name this the granularity mismatch
and frame their solution, Hierarchical Preference Learning (HPL), as a multi-resolution loss
combined with a structured training schedule, rather than a single new objective.

Methodologically, HPL has four moving parts: an LLM-driven segmenter that splits expert trajectories
into semantically coherent action groups, a procedure that generates contrasting suboptimal groups
via behaviour-cloned rollouts, a hierarchical DPO loss that sums trajectory-, step-, and group-level
DPO terms, and a dual-layer curriculum that orders preference pairs by group length and reward gap.
The curriculum runs in three phases and is shown to be necessary in ablations. A bias-variance
proposition gives theoretical grounding to the choice of group-level granularity.

The empirical story is unambiguous. On three standard agent benchmarks (ALFWorld, WebShop,
InterCode-SQL) and two base models (Qwen2.5-1.5B / 7B), HPL beats SFT, ETO, and IPR. The Qwen2.5-7B
average rises from 63.84 (IPR) to 67.81 (HPL), with the largest gain on ALFWorld seen (+10.71) and
unseen (+8.96). Ablations cleanly localise the gain: the group-level DPO term is the single most
important component, the semantic segmenter beats fixed-length alternatives, and the two-axis
curriculum contributes about a full average point.

For this project, HPL is directly relevant in three ways. First, the granularity-mismatch framing
maps onto our scope-aware / scope-unaware / scope-mismatched conditions: HPL's group level is
exactly the subtask level in our hierarchy. Second, semantic action-group segmentation is a
methodology we can borrow when annotating gold actions at the subtask level on
FrontierScience-Olympiad, WorkArena++, tau-bench, and SWE-bench Verified. Third, HPL provides a
recent, strong, reproducible baseline if any downstream task in our pipeline trains a scope-aware
policy. Limitations: HPL relies on GPT-4o for segmentation (cost and licence implications) and on
the existence of expert demonstrations, neither of which transfers automatically to settings without
high-quality demos.
