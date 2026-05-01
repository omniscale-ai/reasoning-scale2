---
spec_version: "3"
paper_id: "10.48550_arXiv.2405.15821"
citation_key: "Wen2024"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Reinforcing Language Agents via Policy Optimization with Action Decomposition

## Metadata

* **File**: `files/wen_2024_action-decomposition.pdf`
* **Published**: 2024
* **Authors**: Muning Wen, Ziyu Wan, Weinan Zhang, Jun Wang, Ying Wen
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.15821`
* **Code**: <https://github.com/morning9393/ADRL>

## Abstract

Language models as intelligent agents push the boundaries of sequential decision-making agents but
struggle with limited knowledge of environmental dynamics and exponentially huge action space.
Recent efforts like GLAM and TWOSOME manually constrain the action space to a restricted subset and
employ reinforcement learning to align agents' knowledge with specific environments. However, they
overlook fine-grained credit assignments for intra-action tokens, which is essential for efficient
language agent optimization, and rely on human's prior knowledge to restrict action space. This
paper proposes decomposing language agent optimization from the action level to the token level,
offering finer supervision for each intra-action token and manageable optimization complexity in
environments with unrestricted action spaces. Beginning with the simplification of flattening all
actions, we theoretically explore the discrepancies between action-level optimization and this naive
token-level optimization. We then derive the Bellman backup with Action Decomposition (BAD) to
integrate credit assignments for both intra-action and inter-action tokens, effectively eliminating
the discrepancies. Implementing BAD within the PPO algorithm, we introduce Policy Optimization with
Action Decomposition (POAD). POAD benefits from a finer-grained credit assignment process and lower
optimization complexity, leading to enhanced learning efficiency and generalization abilities in
aligning language agents with interactive environments. We validate POAD across diverse testbeds,
with results affirming the advantages of our approach and the correctness of our theoretical
analysis.

## Overview

This paper tackles a core obstacle in fine-tuning LLM-based language agents with reinforcement
learning: the credit assignment uncertainty that arises when a multi-token textual action is treated
as a single atomic unit. Action-level methods such as GLAM and TWOSOME multiply per-token
conditional probabilities into one action probability and update that joint quantity with PPO, which
hides which tokens within the action actually drove the reward signal. The authors argue that this
opacity, combined with action-space sizes that grow as |V|^|a|, forces practitioners to hand-prune
the feasible action set and still leaves training inefficient on long actions.

The natural alternative is naive token-level optimization (NTPO), which embeds the auto-regressive
token generation process into the MDP and treats every token as a micro-action. The authors prove
formally that this transformation is *not* equivalent to the original action-level MDP.
Specifically, splitting the discount factor into intra-action gamma_w and inter-action gamma_a, the
discrepancy between the two value functions vanishes only when gamma_w = 1 and grows monotonically
with action length. Intuitively, NTPO assumes "later tokens in a sentence convey more meaning than
earlier ones," which is unrealistic for linguistic actions.

The contribution is the Bellman backup with Action Decomposition (BAD), a principled token-level
backup that sets the intra-action discount to 1 while keeping the inter-action discount strict, and
the resulting PPO instantiation called POAD. The authors show theoretically that BAD recovers the
optimal action-level Q and V functions, while empirically POAD trains faster and reaches higher
returns than TWOSOME and NTPO across Overcooked, VirtualHome, and a newly introduced DataSciCoding
benchmark with unrestricted action spaces.

## Architecture, Models and Methods

The paper formalises language-agent RL as a language-augmented POMDP M = (V, S, O, A, T, R, gamma)
in which actions are token sequences a_t = (w^1_t, ..., w^|a_t|_t). Standard action-level methods
update Q_pi(o_t, a_t) and V_pi(o_t) via the chain rule pi(a|o) = prod_j pi(w^j|o, w^{1:j-1}), but
the action space size is |V|^|a|. The authors split the discount factor into gamma_w (intra-action)
and gamma_a (inter-action) and derive a closed-form expression for the discrepancy between
action-level Bellman updates (Eqs. 4-5) and naive token-level Bellman updates (Eqs. 9-10). The
discrepancy is proportional to (1 - gamma_w^{|a_t|-j}) and goes to zero only as gamma_w approaches
1\.

BAD (Eqs. 13-14) sets the intra-action transition to a deterministic max over the next token with no
discount, applies the reward and gamma_a only at the action boundary, and is proven equivalent to
the action-level optimum (Appendix B). This reduces RL complexity from O(|V|^|a|) to O(|a| * |V|),
making unrestricted action spaces tractable.

POAD plugs BAD into PPO. The critic is trained with a token-level Bellman error split into
inter-action and intra-action terms (Eq. 15). The actor uses the clipping PPO objective with
per-token ratios ratio^j_t = pi_phi(w^j_t | o_t, w^{1:j-1}_t) / pi_phi_old(...) and per-token
advantages estimated with GAE (Eq. 16). Backbones are LLaMA2-7B for Overcooked and VirtualHome and
CodeLLaMA-7B for DataSciCoding, all fine-tuned with LoRA on a single Nvidia A100. Hyperparameters
include actor lr 5e-7 to 1e-6, critic lr 1e-5 to 5e-5, batch size 128, PPO clip 0.2, KL threshold
0.02, gamma_a = 0.95-0.99, with 5 PPO epochs for Overcooked/VirtualHome and 1 for DataSciCoding. An
sBAD extension supports entropy-regularised SAC-style algorithms (Appendix B.3).

## Results

* On Overcooked Tomato Salad and Tomato-lettuce Salad, POAD matches or exceeds TWOSOME's final
  episodic return (~1.0) while converging in roughly half the environment steps and with smaller
  variance across 3 seeds.
* On VirtualHome Food Preparation and Entertainment (sparse +1 terminal reward), POAD reaches ~0.8
  episodic return well before TWOSOME and NTPO, with NTPO converging to a clearly lower plateau.
* On 8 unseen Food Preparation generalisation tasks (cheese, hamburger, apple pie, pizza, washing
  plate, laundry, etc.), POAD wins 7 of 8: Cheese **0.7553**, Hamburger **0.7602**, Apple Pie
  **0.7650**, Pizza **0.7625**, Laundry **0.7014**, vs LLaMA2-7B base 0.13-0.17.
* On DataSciCoding (unrestricted action space, up to 128 tokens per action), POAD-Best beats
  CAAFE+GPT-4 on every dataset: pharyngitis **0.7282 vs 0.7078**, spaceship-titanic **0.8628 vs
  0.8405**, airlines **0.664 vs 0.6203**, balance-scale **0.9651 vs 0.882**, breast-w **0.9981 vs
  0.9809**, health-insurance **0.5939 vs 0.5748**.
* The performance gap between POAD and NTPO grows with action length: small on Overcooked (~5-10
  tokens) and much larger on DataSciCoding (up to 128 tokens), consistent with the theoretical
  prediction that the NTPO discrepancy scales with |a_t|.
* Ablations on gamma_w in {0.95, 0.9, 0.8, 0.5} show monotonically widening gaps to POAD as gamma_w
  drops, empirically confirming Insight (i) of Section 4.2.
* Setting gamma_a = 1.0 collapses both TWOSOME and POAD performance, confirming gamma_a < 1.0 is
  necessary and that simply unifying gamma_a = gamma_w cannot resolve the discrepancy.
* Zero-shot evaluation on Language Model Evaluation Harness shows no degradation of base abilities
  after POAD fine-tuning: ARC_C 0.45 vs 0.44 base, HellaSwag 0.59 vs 0.57, PIQA 0.78 = 0.78, MMLU
  0.41 = 0.41.

## Innovations

### Bellman Backup with Action Decomposition (BAD)

A token-level Bellman backup that is provably consistent with the original action-level MDP. By
separating gamma into gamma_a (inter-action) and gamma_w (intra-action) and pinning gamma_w = 1, the
authors recover the action-level optimum while still propagating per-token credit. Appendices A and
B provide the full derivation of the discrepancy and the proof of optimality, and Appendix B.3
extends the result to soft Q-functions (sBAD) for SAC-style entropy-regularised RL.

### POAD: PPO with Per-Token Credit Assignment

POAD is the first PPO instantiation that performs both a per-token actor update with clipped ratios
and a per-token critic update split into intra-action and inter-action losses (Eq. 15-16). The
complexity of the RL problem drops from O(|V|^|a|) to O(|a| * |V|), making language agents trainable
in environments with unrestricted action spaces (up to 128 tokens per action) without
hand-engineered action masks.

### DataSciCoding: An Unrestricted-Action-Space Benchmark

The authors construct a new sequential decision-making benchmark covering 6 tabular datasets (3
Kaggle, 3 OpenML) where the agent emits free-form scikit-learn classifier code, executes it, and
receives a ROC-AUC reward (or -1 on failure). This is the first benchmark where TWOSOME-style
action-level baselines are simply inapplicable, exposing where token-level RL is genuinely
necessary.

### Empirical Verification of the Length-Discrepancy Law

By varying gamma_w and showing the gap to POAD grows monotonically as gamma_w drops, the paper turns
the theoretical insight "discrepancy increases with |a_t|" into a measurable, reproducible curve.
This provides a rare instance where an RL theory prediction is closely tracked by experiments.

## Datasets

* **Overcooked** (from Tan et al. 2024 / TWOSOME): 7x7 grid kitchen, 2 tasks (Tomato Salad,
  Tomato-lettuce Salad), ~10 macro-actions per state of 5-10 tokens each. Public.
* **VirtualHome** (from Tan et al. 2024 / TWOSOME): simulated household, 2 tasks (Food Preparation,
  Entertainment) plus 8 generalisation variants substituting target objects/appliances. Public.
* **DataSciCoding** (introduced in this paper): 3 Kaggle datasets - Pharyngitis (19 features, 512
  samples, 2 classes), Health Insurance (13/2000/2), Spaceship Titanic (13/2000/2) - and 3 OpenML
  datasets - Airlines (7/2000/2), Balance Scale (4/125/3), Breast-w (9/69/2). Pruning matches CAAFE
  (Hollmann et al. 2023). Released with the code at <https://github.com/morning9393/ADRL>.
* **NLP evaluation suite** (Language Model Evaluation Harness, Gao et al. 2021): ARC_Challenge,
  HellaSwag, PIQA, MMLU. Used only for measuring whether POAD damages general-purpose LM abilities.
* No human studies; no proprietary data.

## Main Ideas

* The right granularity for credit assignment in LLM-agent RL is the token, not the textual action,
  but it must be done with BAD's intra-action gamma_w = 1 to stay consistent with the original MDP.
  This is the single most useful idea for our project's hierarchical-conditioning agenda: it gives a
  formal handle on what "fine-grained" actually means.
* The discrepancy between action-level and naive token-level optimisation grows with action length.
  Any task with long actions (e.g., subtask-level plans, or atomic-execution code blocks) will
  silently underperform under TWOSOME-style updates, which is directly relevant to our scope-aware
  vs scope-mismatched conditions in t0009 / t0014.
* Token-level credit assignment, when done correctly, also yields better open-vocabulary
  generalisation (7/8 unseen Food Preparation variants), suggesting that finer-grained alignment
  signals do not memorise but rather generalise.
* The complexity reduction from O(|V|^|a|) to O(|a| * |V|) is what makes RL on free-form action
  spaces tractable; this is a precondition for any future work in our project that uses RL on agent
  traces with arbitrary text outputs.
* sBAD extends the approach to entropy-regularised SAC-style algorithms, which keeps the door open
  for off-policy variants if we adopt this method downstream.

## Summary

Wen et al. confront a structural tension in RL fine-tuning of LLM agents: action-level methods
(GLAM, TWOSOME) must hand-prune the action space and fail to assign credit to specific tokens inside
an action, while naive token-level methods that embed token generation into the MDP implicitly
assume that later tokens are more important than earlier ones. The paper makes this informal
complaint formal by deriving a closed-form expression for the discrepancy between action-level and
naive token-level Bellman updates, splitting the discount factor into gamma_a and gamma_w and
showing the discrepancy is proportional to (1 - gamma_w^{|a_t|-j}).

The fix is the Bellman backup with Action Decomposition (BAD): set gamma_w = 1 and only apply
gamma_a at the action boundary, which the authors prove recovers the action-level optimum exactly
while still giving per-token credit. They package BAD inside PPO as POAD, with a critic loss that
explicitly splits intra-action and inter-action errors and an actor loss that uses per-token clipped
ratios and GAE-estimated per-token advantages. The complexity drops from O(|V|^|a|) to O(|a| * |V|).

Empirically, POAD wins on three families of tasks. On Overcooked and VirtualHome it converges faster
and more stably than TWOSOME and beats NTPO clearly. On 8 unseen Food Preparation variants it wins 7
of 8 against TWOSOME, NTPO, and the LLaMA2-7B base model. Most importantly, on the new DataSciCoding
benchmark, where TWOSOME is inapplicable because the action space is unrestricted, POAD-Best with
CodeLLaMA-7B beats CAAFE with GPT-4 on every one of six datasets while training in under three hours
on a single A100. Ablations on gamma_w track the theoretical prediction that the NTPO-vs-POAD gap
widens as gamma_w drops, and the LLM Evaluation Harness shows no loss of base language ability.

For our project, this paper is directly relevant in three ways. First, it gives the most rigorous
existing answer to "what is the right granularity for assigning credit inside an LLM agent's
action," which is the formal counterpart of the v2 hierarchical-annotation result from t0009 and
t0014. Second, the length-dependence of the action-level/token-level discrepancy predicts that any
scope-aware vs scope-mismatched ABC condition that varies action length will see widening
performance gaps under TWOSOME-style updates - a useful theoretical anchor for our Phase 2 ABC
analysis. Third, POAD's unrestricted-action-space results on DataSciCoding suggest that, if we ever
move beyond evaluation into RL fine-tuning of judges or agents, BAD/POAD is the principled starting
point. The main caveat is that POAD requires a quantitative reward function, which is not available
in our annotation-only pipeline; this aligns with the authors' own listed limitation.
