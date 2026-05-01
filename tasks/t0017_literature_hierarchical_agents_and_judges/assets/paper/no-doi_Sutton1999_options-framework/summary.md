---
spec_version: "3"
paper_id: "no-doi_Sutton1999_options-framework"
citation_key: "Sutton1999"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning

## Metadata

* **File**: `files/sutton_1999_options-framework.pdf`
* **Published**: 1999 (Artificial Intelligence 112, pp. 181-211)
* **Authors**: Richard S. Sutton 🇺🇸, Doina Precup 🇺🇸, Satinder Singh 🇺🇸
* **Venue**: Artificial Intelligence (Elsevier journal)
* **DOI**: `10.1016/S0004-3702(99)00052-1`
* **Note**: DOI contains parentheses that violate the slug character set, so this asset uses the
  `no-doi_` fallback ID. The DOI itself is preserved in `details.json`.

## Abstract

Learning, planning, and representing knowledge at multiple levels of temporal abstraction are key,
longstanding challenges for AI. In this paper we consider how these challenges can be addressed
within the mathematical framework of reinforcement learning and Markov decision processes (MDPs). We
extend the usual notion of action in this framework to include options-closed-loop policies for
taking action over a period of time. Examples of options include picking up an object, going to
lunch, and traveling to a distant city, as well as primitive actions such as muscle twitches and
joint torques. Overall, we show that options enable temporally abstract knowledge and action to be
included in the reinforcement learning framework in a natural and general way. In particular, we
show that options may be used interchangeably with primitive actions in planning methods such as
dynamic programming and in learning methods such as Q-learning. Formally, a set of options defined
over an MDP constitutes a semi-Markov decision process (SMDP), and the theory of SMDPs provides the
foundation for the theory of options. However, the most interesting issues concern the interplay
between the underlying MDP and the SMDP and are thus beyond SMDP theory. We present results for
three such cases: (1) we show that the results of planning with options can be used during execution
to interrupt options and thereby perform even better than planned, (2) we introduce new intra-option
methods that are able to learn about an option from fragments of its execution, and (3) we propose a
notion of subgoal that can be used to improve the options themselves.

## Overview

This paper introduces the *options framework*, the canonical formalization of temporal abstraction
in reinforcement learning. The PDF was downloaded successfully from Andrew Barto's UMass course
page, so the summary below reflects the full text of the paper rather than only the abstract. The
authors target a long-standing problem in AI: real decision making works at multiple time scales
(muscle twitches, picking up a phone, traveling to a city), but conventional MDPs only support a
single discrete time step.

The contribution is to extend MDPs with *options* - closed-loop policies with an initiation set,
internal policy, and stochastic termination condition. A fixed set of options over an MDP induces a
semi-Markov decision process (SMDP) over the same state space, so all classical SMDP planning and
learning machinery (value iteration, Q-learning) applies unchanged at the option level. The novel
contribution is the *interplay* between the underlying MDP and the induced SMDP: options are not
opaque black boxes but policies that can be inspected, interrupted, learned about during partial
executions, and improved against subgoals.

The framework subsumes prior temporal-abstraction work (HAMs, MAXQ, macro-operators) by providing a
single, minimal extension to MDPs. The paper proves three theorems beyond standard SMDP theory:
interruption (Theorem 2), intra-option Bellman equations (Theorem 3), and subgoal-based option
improvement (Theorem 4). It also gives empirical illustrations in a 4-rooms gridworld and a
continuous 2-D navigation task.

## Architecture, Models and Methods

The paper is theoretical. The core mathematical objects are:

**Option**: A triple `<I, pi, beta>` where `I` is the initiation set (states where the option can
start), `pi : S x A -> [0, 1]` is the option's internal policy over primitive actions, and
`beta : S+ -> [0, 1]` is the termination probability per state. A *Markov* option's `pi` and `beta`
depend only on the current state; a *semi-Markov* option may condition on the entire history
`h_{t,tau}` since the option started.

**Primitive actions as options**: Each primitive action `a` corresponds to a one-step option with
`I = {s : a in A_s}`, `pi(s, a) = 1`, `beta(s) = 1` everywhere. This unifies primitive and extended
actions under a single algebra.

**MDP + Options = SMDP (Theorem 1)**: For any MDP and any fixed set of options, the decision process
that selects only among those options and runs each to termination is a discrete-event SMDP. This
grants free use of SMDP value iteration and Q-learning at the option level.

**Multi-time model**: For each option `o` started in `s`, the model is
`r^o_s = E[r_{t+1} + gamma r_{t+2} + ... + gamma^{k-1} r_{t+k}]` for cumulative discounted reward
and `p^o_{ss'} = sum_k p(s', k) gamma^k` for the discounted state-prediction. The `gamma^k`
weighting bakes the temporal extension directly into the transition kernel.

**Bellman equations over options**: `V^mu(s) = sum_o mu(s, o) [r^o_s + sum_{s'} p^o_{ss'} V^mu(s')]`
and analogous `Q^mu(s, o)`.

**SMDP Q-learning** (Bradtke and Duff): `Q(s, o) <- Q(s, o) + alpha [r + gamma^k max_{o'} Q(s', o')
- Q(s, o)]`where`r`is the cumulative discounted option reward and`k` the option duration.

**Interruption (Theorem 2)**: Define `mu'` from `mu` by terminating any option `o` whenever
`Q^mu(s, o) < V^mu(s)`. Then `V^{mu'} >= V^mu` everywhere, with strict inequality at any non-zero
probability interrupted history.

**Intra-option learning (Theorem 3)**: Off-policy Bellman update for *all* Markov options consistent
with the executed primitive action, learning many option-value functions in parallel from one
trajectory.

**Subgoals (Theorem 4)**: Define a per-option pseudo-reward `g(s)` (a "subgoal") and learn the
option's policy `pi` to maximize discounted return plus a termination bonus `g(s_terminal)`.

Experiments use a 4-rooms gridworld (stochastic 4-direction primitive actions, 2/3 success rate)
with 8 hand-crafted hallway options and a continuous 2-D navigation task. Discount `gamma = 0.9`,
epsilon-greedy with `epsilon = 0.1`, step sizes optimized to nearest power of 2.

## Results

* **Theorem 1**: Any MDP plus a fixed set of options forms an SMDP, so SMDP value iteration and
  Q-learning apply at the option level (proved via SMDP definition).
* **Planning speedup with options**: In the rooms gridworld synchronous value iteration with the
  hallway options reaches the optimal value function for goal G1 (a hallway state) in 2 iterations,
  versus needing roughly the diameter of the gridworld in iterations with primitive actions only.
* **Mixed option set A union H**: When the goal G2 lies inside a room, planning with both primitive
  options and hallway options reaches a near-optimal value function in 4 iterations; primitives
  alone propagate value at one cell per iteration.
* **SMDP Q-learning**: Learning curves in the rooms task show multi-step options reach the goal far
  faster on the very first episode and maintain a long-term advantage over flat Q-learning when the
  goal aligns with option subgoals; with the goal inside a room (G2), `H` alone underperforms but
  `A union H` still beats `A`.
* **Interruption theorem (Theorem 2)**: For any policy `mu`, the interrupted policy `mu'` satisfies
  `V^{mu'}(s) >= V^mu(s)` for all `s`, with strict improvement whenever a non-zero-probability
  history is interrupted. This gives a nearly-free improvement over SMDP optimal policies once
  `Q*_O` is known.
* **Continuous-navigation interruption demo**: In the 2-D navigation task interruption tightens
  trajectories around obstacles relative to running options to natural termination, illustrating the
  theorem in a continuous-state setting.
* **Intra-option learning (Theorem 3)**: Off-policy intra-option Bellman updates converge to the
  correct option-value function while observing only fragments of an option's execution, enabling
  parallel learning of many options from one trajectory.
* **Subgoal improvement (Theorem 4)**: Defining a per-option pseudo-reward and improving the option
  policy against it yields strictly better options under standard policy-improvement conditions; in
  the rooms task this recovers near-optimal hallway navigators from learned subgoals.
* **Generality**: All results are obtained without committing to any particular state abstraction,
  function approximation, or hierarchical structure - the framework strictly *extends* MDPs.

## Innovations

### The Options Framework

The paper's central innovation. An option `<I, pi, beta>` is the minimal extension of a primitive
action that adds (a) a domain of applicability, (b) an internal closed-loop policy, and (c) a
stochastic termination rule. By making primitive actions a special case (one-step options that
always terminate), the algebra unifies flat and hierarchical control under one type. This is the
formal construct that virtually all subsequent hierarchical RL work (option-critic, FuN, HIRO,
DIAYN, hierarchical actor-critic) builds on or contrasts with.

### MDP + Options = SMDP (Theorem 1)

Establishes that augmenting an MDP with any fixed option set yields an SMDP at the option level, so
*all classical SMDP machinery* - value iteration, Q-learning, policy iteration, convergence
guarantees - lifts to options for free. This factors the hierarchical-RL problem into "design
options" plus "do standard SMDP RL", and is the theoretical backbone of SMDP Q-learning over
options.

### Interruption Theorem

Proves that an SMDP-optimal policy can be strictly improved by interrupting options whenever
continuing is dominated by switching, *without* re-solving the SMDP. This is the formal
justification for greedy / call-and-return / polling execution in hierarchical agents and for "early
exit" mechanisms in modern LLM-agent planners.

### Intra-Option Learning

Introduces off-policy Bellman updates that learn about *every* Markov option consistent with the
observed primitive action, from any trajectory. This breaks the SMDP assumption that options must be
executed to termination to be learned about, dramatically improving sample efficiency and enabling
counterfactual learning across an option library.

### Subgoal-Based Option Improvement

Formalizes "subgoal" as a state-dependent pseudo-reward used to shape an option's internal policy,
proving that policy improvement against the subgoal yields a strictly better option. This is the
direct ancestor of feudal RL, intrinsic-motivation hierarchies, and modern goal-conditioned
hierarchical agents.

### Unification of Prior Work

Subsumes macro-operators, behaviors, abstract actions, hierarchical abstract machines (Parr) and
MAXQ (Dietterich) under one minimal extension, making prior results comparable and clarifying which
features are essential vs. incidental.

## Datasets

This is a theoretical paper; no datasets were used. Empirical illustrations use two synthetic
environments constructed by the authors:

* A discrete 4-rooms gridworld (104 cells across 4 rooms with 8 hallway options) used for value
  iteration and SMDP Q-learning experiments.
* A continuous 2-D navigation task with obstacles used to illustrate the interruption theorem.

Both environments are described in full in the paper and have been re-used widely in subsequent
hierarchical RL literature.

## Main Ideas

* **Options as the unit of hierarchy**: Treat *every* level of decision as an option `<I, pi, beta>`
  with primitive actions as the one-step special case. For this project, the global / subtask /
  atomic levels in the three-level hierarchy correspond directly to options at different time
  scales, and the framework gives us a single formalism in which to reason about scope-aware vs.
  scope-unaware vs. scope-mismatched conditioning (conditions A, B, C).
* **Hierarchical decomposition is free SMDP**: Once you fix a set of options the decision process
  *is* an SMDP, and standard convergence guarantees apply - no new theory is needed to justify
  hierarchical evaluation. This means that when we run condition A (scope-aware) with explicit
  granularity labels, we are essentially executing an SMDP policy at the labeled level, while
  conditions B and C correspond to running the same option library without the matching policy
  index.
* **Interruption as a cheap improvement**: An optimal SMDP policy can be strictly improved by
  switching whenever continuing is dominated, at near-zero extra compute. This maps directly onto
  "must-request" vs "can-execute-now" decisions (Metric 3) - an agent that can interrupt a subtask
  when continuation is suboptimal makes better request decisions.
* **Subgoal pseudo-rewards**: Improving options against subgoals gives a principled, theorem-backed
  recipe for distilling new options from data - relevant when we generate gold sub-actions during
  benchmark annotation (Phase 1).
* **Avoid premature commitment to hierarchy**: The framework deliberately separates "what is an
  option" from "how is the option set organized". Our project should adopt the same separation -
  define hierarchy levels as labels on options, not as a baked-in tree structure that the agent must
  commit to.

## Summary

Sutton, Precup, and Singh address a foundational gap in reinforcement learning theory: classical
MDPs operate at a single discrete time scale and cannot natively express temporally extended courses
of action like "drive to the airport" or "search a room". They propose the *options framework*, in
which an option `<I, pi, beta>` packages an initiation set, an internal closed-loop policy, and a
stochastic termination condition. Primitive actions become one-step options, so the framework
strictly extends - rather than replaces - the existing MDP formalism. The motivation is to find the
*minimal* extension that enables temporally abstract knowledge while preserving every standard RL
algorithm.

Methodologically, the authors prove that any MDP equipped with a fixed option set induces a
semi-Markov decision process (SMDP) at the option level, so SMDP value iteration and Q-learning -
including the multi-time discount model `r^o_s` and `p^o_{ss'} = sum_k p(s', k) gamma^k` - apply
unchanged. They then go beyond SMDP theory in three directions: (1) the *interruption theorem*
proves that switching options whenever `Q^mu(s, o) < V^mu(s)` strictly improves the policy, (2)
*intra-option learning* lets a single trajectory update value estimates for every option whose
policy is consistent with the observed action, and (3) *subgoal-based improvement* shows that
defining a per-option pseudo-reward and running policy improvement against it yields strictly better
options.

Empirically, in a 4-rooms gridworld with 8 hand-designed hallway options, synchronous value
iteration with options reaches the optimal value function in 2 iterations versus diameter-many for
primitives, and SMDP Q-learning attains the goal far faster on the very first episode. The combined
option set `A union H` works robustly even when the goal lies in a room interior, where hallway-only
planning is insufficient. A continuous 2-D navigation task illustrates that the interruption theorem
tightens trajectories around obstacles. The headline qualitative result is that all of this is
accomplished without committing to any particular hierarchy, function approximator, or state
abstraction.

For this project the paper is foundational. The three-level hierarchy (global / subtask / atomic) is
naturally expressed as options at different time scales, and conditions A/B/C can be formalized as
the *same* option library executed under different conditioning policies. The interruption theorem
provides theoretical backing for the "can-execute-now vs. must-request" distinction (Metric 3): an
agent that interrupts a subtask whenever continuing is dominated makes better request decisions, and
the resulting policy improvement is provably bounded below by the SMDP-optimal policy. The
intra-option learning result is relevant for any future task that wants to learn from partial
trajectories of agent runs, and the subgoal construction gives a principled way to derive options
from gold sub-actions produced during benchmark annotation. We should treat this paper as the
canonical reference whenever the project formalizes the relationship between hierarchy levels and
conditioning.
