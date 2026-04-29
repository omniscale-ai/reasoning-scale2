---
spec_version: "3"
paper_id: "10.48550_arXiv.2406.12045"
citation_key: "Yao2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2024
* **Authors**: Shunyu Yao 🇺🇸, Noah Shinn 🇺🇸, Pedram Razavi 🇺🇸, Karthik Narasimhan 🇺🇸
* **Venue**: arXiv preprint (Sierra Research)
* **DOI**: `10.48550/arXiv.2406.12045`

## Abstract

Existing benchmarks do not test language agents on their interaction with human users or ability
to follow domain-specific rules, both of which are vital for deploying them in real applications.
We propose tau-bench, a benchmark emulating dynamic conversations between a user (simulated by
language models) and a language agent provided with domain-specific API tools and policy
guidelines. We employ an efficient and faithful evaluation process that compares the database
state at the end of a conversation with the annotated goal state, and propose a new metric
(pass^k) to evaluate the reliability of agent behavior over multiple trials. Our experiments show
that even state-of-the-art function calling agents (like gpt-4o) succeed on less than 50% of the
tasks, and are quite inconsistent (pass^8 < 25% in retail). Our findings point to the need for
methods that can improve the ability of agents to act consistently and follow rules reliably.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. tau-bench evaluates language agents in two simulated
customer-service domains — **retail** and **airline** — where the agent is given a set of
domain-specific API tools (refund, cancel, look up, etc.) plus a policy document that constrains
which actions are allowed under what circumstances. The "user" is itself a language model
roleplaying a customer with a goal state, and the conversation continues until the agent claims
the task is done.

The methodological novelty is **pass^k**, a consistency metric that measures whether the same
agent succeeds across `k` independent trials of the same task. A high pass@1 with low pass^8
indicates an agent that *sometimes* succeeds but is unreliable — a critical distinction the prior
benchmarks (which report only pass@1) cannot capture.

For the granularity-aware hierarchical agents project, tau-bench is the canonical
**request-vs-act** benchmark: many of its failures come from agents that proceed with insufficient
information instead of asking the simulated user a clarifying question. This makes tau-bench the
direct test bed for the project's Metric 3 (can-execute-now vs. must-request-information
accuracy).

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
benchmark builds two domains:

* **Retail** (modeled on a generic e-commerce platform): tools include `cancel_order`,
  `return_item`, `lookup_user`, `update_address`, etc., plus a policy document describing
  allowable refund windows, identity-verification requirements, and dispute escalation rules.
* **Airline** (modeled on flight booking and changes): tools include `book_flight`,
  `cancel_reservation`, `change_seat`, `apply_voucher`, plus a policy on cancellation fees,
  loyalty-tier benefits, and ticket-class change rules.

Each task pairs (a) a user-goal state (represented as a database state diff), (b) the user
language model's persona and goal, (c) the policy document. The agent must conduct a conversation
with the user, call appropriate tools, and reach the goal state without violating policy.

Evaluation compares the **final database state** with the annotated **goal state**. The pass^k
metric runs `k` independent rollouts and measures the fraction of tasks succeeding on every one.
This penalizes agents whose success is non-deterministic or context-luck-dependent.

## Results

* **GPT-4o achieves under 50% pass@1** in both domains
* **GPT-4o pass^8 < 25% in retail** — substantial inconsistency across rollouts
* **Pass^k metric** is the key contribution; gap between pass@1 and pass^8 is the core measure of
  reliability
* **Two domains** (retail and airline) provide cross-domain generalization signal
* **Policy following** is a major failure mode — agents frequently violate explicit policy rules
  even when those rules are in the system prompt
* **Request-vs-act discrimination** is a major failure mode — agents proceed with insufficient
  information rather than asking the user clarifying questions

## Innovations

### The pass^k Reliability Metric

Pass^k is the first widely-cited metric to penalize inconsistent agents. By requiring success
across `k` independent trials, it surfaces the gap between "the agent can solve this task" and
"the agent reliably solves this task" — a distinction prior benchmarks ignored.

### User-Simulation as a First-Class Component

Prior tool-use benchmarks (ToolBench, APIBench) provided fixed user requests. tau-bench instead
simulates the user with another LLM, creating dynamic conversations where the agent must adapt to
the user's responses and ask clarifying questions when needed.

### Domain-Policy Following as an Evaluation Axis

Most agent benchmarks focus on tool-use correctness; tau-bench explicitly tests *policy
following*, which is a central concern for production deployment. This separates capable agents
from agents that produce plausible-looking but policy-violating actions.

## Datasets

* **tau-bench retail domain** — task definitions, tool schemas, policy document, user persona
  templates. Open source on GitHub (`sierra-research/tau-bench`).
* **tau-bench airline domain** — same structure as retail. Open source.
* **τ²-bench / τ³-bench** — successor benchmarks adding banking and voice modalities, with fixes
  to the original retail and airline tasks.

## Main Ideas

* tau-bench is the canonical *request-vs-act* benchmark and should be the primary test bed for
  the project's Metric 3 (can-execute-now vs. must-request-information accuracy).
* The pass^k metric should be **adopted by the project** as a reliability indicator alongside
  Metric 1 (task success). Single-trial pass@1 reporting will systematically overstate agent
  reliability.
* Policy following is a meaningful axis. The scope-aware (A) ATOMIC prompt should explicitly
  reference the policy document at every tool-call decision; the scope-unaware (B) baseline does
  not.

## Summary

tau-bench introduces a tool-agent-user interaction benchmark in two simulated customer-service
domains (retail and airline). The motivation is that prior tool-use benchmarks fail to test two
critical capabilities for production agents: dynamic interaction with a human user (simulated here
by another LLM) and adherence to domain-specific policy documents that constrain allowable
actions.

Methodologically, each task pairs a user-goal database state, an LLM-roleplayed user persona, and
a policy document. The agent conducts a multi-turn conversation, calls tools as needed, and
attempts to reach the goal state without policy violations. Evaluation compares the final
database state with the annotated goal. The novel pass^k metric runs `k` independent rollouts and
measures the fraction of tasks where every rollout succeeds — exposing inconsistency that pass@1
hides.

The headline finding is that even state-of-the-art models (GPT-4o) achieve **under 50% pass@1**
and **pass^8 below 25% in retail**, indicating that current frontier agents are both
moderately-capable and substantially unreliable. The gap between pass@1 and pass^8 is the core
diagnostic.

For the granularity-aware hierarchical agents project, tau-bench is the canonical
request-vs-act benchmark — most of its failures stem from agents that proceed without sufficient
information rather than asking the simulated user. This makes tau-bench the primary test bed for
Metric 3. The project should also adopt the pass^k metric as a project-wide reliability signal,
especially in the Phase 4 paper-ready report where overall claims about scope-conditioning gains
must be robust to single-rollout luck.
