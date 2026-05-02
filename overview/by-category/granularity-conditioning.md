# Category: Granularity Conditioning

Work that explicitly conditions an agent on its current operating granularity (global,
subtask, atomic).

[Back to Dashboard](../README.md)

**Detail pages**: [Papers (6)](../papers/by-category/granularity-conditioning.md) |
[Suggestions (26)](../suggestions/by-category/granularity-conditioning.md) | [Datasets
(3)](../datasets/by-category/granularity-conditioning.md) | [Libraries
(5)](../libraries/by-category/granularity-conditioning.md) | [Predictions
(2)](../predictions/by-category/granularity-conditioning.md)

---

## Papers (6)

<details>
<summary>🏤 <strong>Solving the Granularity Mismatch: Hierarchical Preference
Learning for Long-Horizon LLM Agents</strong> — Gao et al., 2026</summary>

| Field | Value |
|---|---|
| **ID** | `no-doi_Gao2026_hierarchical-preference-learning-llm-agents` |
| **Authors** | Heyang Gao, Zexu Sun, Erxue Min, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Xu Chen |
| **Venue** | ICLR 2026 (conference) |
| **DOI** | — |
| **URL** | https://openreview.net/forum?id=s8usvGHYlk |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/summary.md) |

Gao et al. tackle a real and well-defined problem in offline alignment of long-horizon LLM
agents: trajectory-level DPO is too coarse to attribute failure to a specific sub-task, and
step-level DPO is too noisy to capture the value of multi-step behaviour. They name this the
granularity mismatch and frame their solution, Hierarchical Preference Learning (HPL), as a
multi-resolution loss combined with a structured training schedule, rather than a single new
objective.

Methodologically, HPL has four moving parts: an LLM-driven segmenter that splits expert
trajectories into semantically coherent action groups, a procedure that generates contrasting
suboptimal groups via behaviour-cloned rollouts, a hierarchical DPO loss that sums
trajectory-, step-, and group-level DPO terms, and a dual-layer curriculum that orders
preference pairs by group length and reward gap. The curriculum runs in three phases and is
shown to be necessary in ablations. A bias-variance proposition gives theoretical grounding to
the choice of group-level granularity.

The empirical story is unambiguous. On three standard agent benchmarks (ALFWorld, WebShop,
InterCode-SQL) and two base models (Qwen2.5-1.5B / 7B), HPL beats SFT, ETO, and IPR. The
Qwen2.5-7B average rises from 63.84 (IPR) to 67.81 (HPL), with the largest gain on ALFWorld
seen (+10.71) and unseen (+8.96). Ablations cleanly localise the gain: the group-level DPO
term is the single most important component, the semantic segmenter beats fixed-length
alternatives, and the two-axis curriculum contributes about a full average point.

For this project, HPL is directly relevant in three ways. First, the granularity-mismatch
framing maps onto our scope-aware / scope-unaware / scope-mismatched conditions: HPL's group
level is exactly the subtask level in our hierarchy. Second, semantic action-group
segmentation is a methodology we can borrow when annotating gold actions at the subtask level
on FrontierScience-Olympiad, WorkArena++, tau-bench, and SWE-bench Verified. Third, HPL
provides a recent, strong, reproducible baseline if any downstream task in our pipeline trains
a scope-aware policy. Limitations: HPL relies on GPT-4o for segmentation (cost and licence
implications) and on the existence of expert demonstrations, neither of which transfers
automatically to settings without high-quality demos.

</details>

<details>
<summary>🏤 <strong>Reinforcing Language Agents via Policy Optimization with Action
Decomposition</strong> — Wen et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2405.15821` |
| **Authors** | Muning Wen, Ziyu Wan, Weinan Zhang, Jun Wang, Ying Wen |
| **Venue** | NeurIPS 2024 (conference) |
| **DOI** | `10.48550/arXiv.2405.15821` |
| **URL** | https://arxiv.org/abs/2405.15821 |
| **Date added** | 2026-05-01 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2405.15821/summary.md) |

Wen et al. confront a structural tension in RL fine-tuning of LLM agents: action-level methods
(GLAM, TWOSOME) must hand-prune the action space and fail to assign credit to specific tokens
inside an action, while naive token-level methods that embed token generation into the MDP
implicitly assume that later tokens are more important than earlier ones. The paper makes this
informal complaint formal by deriving a closed-form expression for the discrepancy between
action-level and naive token-level Bellman updates, splitting the discount factor into gamma_a
and gamma_w and showing the discrepancy is proportional to (1 - gamma_w^{|a_t|-j}).

The fix is the Bellman backup with Action Decomposition (BAD): set gamma_w = 1 and only apply
gamma_a at the action boundary, which the authors prove recovers the action-level optimum
exactly while still giving per-token credit. They package BAD inside PPO as POAD, with a
critic loss that explicitly splits intra-action and inter-action errors and an actor loss that
uses per-token clipped ratios and GAE-estimated per-token advantages. The complexity drops
from O(|V|^|a|) to O(|a| * |V|).

Empirically, POAD wins on three families of tasks. On Overcooked and VirtualHome it converges
faster and more stably than TWOSOME and beats NTPO clearly. On 8 unseen Food Preparation
variants it wins 7 of 8 against TWOSOME, NTPO, and the LLaMA2-7B base model. Most importantly,
on the new DataSciCoding benchmark, where TWOSOME is inapplicable because the action space is
unrestricted, POAD-Best with CodeLLaMA-7B beats CAAFE with GPT-4 on every one of six datasets
while training in under three hours on a single A100. Ablations on gamma_w track the
theoretical prediction that the NTPO-vs-POAD gap widens as gamma_w drops, and the LLM
Evaluation Harness shows no loss of base language ability.

For our project, this paper is directly relevant in three ways. First, it gives the most
rigorous existing answer to "what is the right granularity for assigning credit inside an LLM
agent's action," which is the formal counterpart of the v2 hierarchical-annotation result from
t0009 and t0014. Second, the length-dependence of the action-level/token-level discrepancy
predicts that any scope-aware vs scope-mismatched ABC condition that varies action length will
see widening performance gaps under TWOSOME-style updates - a useful theoretical anchor for
our Phase 2 ABC analysis. Third, POAD's unrestricted-action-space results on DataSciCoding
suggest that, if we ever move beyond evaluation into RL fine-tuning of judges or agents,
BAD/POAD is the principled starting point. The main caveat is that POAD requires a
quantitative reward function, which is not available in our annotation-only pipeline; this
aligns with the authors' own listed limitation.

</details>

<details>
<summary>🏤 <strong>Reflexion: Language Agents with Verbal Reinforcement
Learning</strong> — Shinn et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2303.11366` |
| **Authors** | Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao |
| **Venue** | NeurIPS 2023 (conference) |
| **DOI** | `10.48550/arXiv.2303.11366` |
| **URL** | https://arxiv.org/abs/2303.11366 |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/summary.md) |

Reflexion is a language-agent framework that adds a verbal self-reflection loop on top of
ReAct-style prompting agents. After each trial, the agent writes a free-form natural-language
critique of its own behavior, stores the critique in an episodic memory buffer, and uses the
buffer as additional context for the next trial. No model weights are updated — the learning
is entirely linguistic.

Methodologically, Reflexion has three components: an actor (ReAct policy), an evaluator
(scalar or free-form feedback), and a reflector (LLM in critique mode). The architecture is
evaluated on HumanEval coding, AlfWorld sequential decision-making, and HotpotQA reasoning,
with ablations on feedback type, feedback source, and reflection horizon.

The headline result is **91% pass@1 on HumanEval** with GPT-4 + Reflexion, an **+11 absolute**
gain over vanilla GPT-4 (80%) without any weight updates. Free-form text feedback outperforms
scalar feedback; internally simulated feedback is nearly as effective as external feedback;
last-trial reflection captures most of the gain.

For the granularity-aware hierarchical agents project, Reflexion's actor/evaluator/reflector
decomposition aligns with the global/subtask/atomic schema and is a strong template for the
scope-aware (A) condition's between-trial component. However, including cross-trial memory in
Phase 2 would conflate scope conditioning with episodic memory; Reflexion should be treated as
a Phase 3 ablation that tests whether memory adds gains *on top of* scope conditioning, not as
the Phase 2 baseline.

</details>

<details>
<summary>🏤 <strong>Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought
Reasoning by Large Language Models</strong> — Wang et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2305.04091` |
| **Authors** | Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, Ee-Peng Lim |
| **Venue** | ACL 2023 (conference) |
| **DOI** | `10.48550/arXiv.2305.04091` |
| **URL** | https://arxiv.org/abs/2305.04091 |
| **Date added** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/summary.md) |

Plan-and-Solve (PS) prompting is a zero-shot prompting technique that explicitly forces a
language model to first produce a plan, then execute the plan step by step. The motivation is
that Zero-shot-CoT — while a powerful zero-shot baseline — exhibits three error modes:
calculation errors, missing-step errors, and semantic-misunderstanding errors. PS targets the
missing-step mode by demanding an explicit plan; PS+ extends to calculation errors via
additional in-prompt instructions to "pay attention to correct numerical calculation."

Methodologically, PS is a single-prompt template that instructs the model to plan-then-solve.
Evaluation covers ten datasets across arithmetic, commonsense, and symbolic reasoning, all in
zero-shot mode with GPT-3 text-davinci-003 as the primary model. PS+ adds more detailed
per-stage instructions.

The headline outcome is **consistent improvement over Zero-shot-CoT across all 10 datasets**,
with PS+ achieving **comparable performance to 8-shot manual CoT** on GSM8K (≈58% vs ≈57%) — a
strong zero-shot result that eliminates the manual exemplar-curation cost. PS+ is available in
LangChain core as Plan-and-Execute and has been adopted in production agent systems.

For the granularity-aware hierarchical agents project, PS is the canonical scope-unaware (B)
baseline for Phase 2. Its two-stage plan-then-solve structure is the closest published
analogue to the project's scope-aware (A) condition without the explicit granularity tags. The
project should reuse LangChain's Plan-and-Execute implementation, log both stages separately,
and measure how much of PS's gain over CoT comes from the plan-execute separation alone — that
delta is the lower bound for the scope-aware (A) condition's expected gain.

</details>

<details>
<summary>🏤 <strong>ReAct: Synergizing Reasoning and Acting in Language
Models</strong> — Yao et al., 2023</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2210.03629` |
| **Authors** | Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao |
| **Venue** | ICLR 2023 (conference) |
| **DOI** | `10.48550/arXiv.2210.03629` |
| **URL** | https://arxiv.org/abs/2210.03629 |
| **Date added** | 2026-04-29 |
| **Categories** | [`granularity-conditioning`](../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../meta/categories/hierarchical-planning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/summary.md) |

ReAct introduces an agent prompting paradigm where the language model alternates between
Thought tokens (free-form reasoning) and Action tokens (calls to external tools or
environments). The motivation is that prior work treated reasoning (chain-of-thought) and
acting (tool-use) as separate problems, missing the synergy where reasoning helps the agent
track and update its plan while acting lets the agent ground its reasoning in real
information.

Methodologically, ReAct uses one or two in-context examples to teach the model the
Thought/Action/Observation pattern, then runs autoregressively until the model emits a Finish
action. No fine-tuning is required. The paper evaluates on HotpotQA, Fever (knowledge tasks)
and ALFWorld, WebShop (interactive decision-making tasks).

The headline result is **+34 absolute** success-rate improvement on ALFWorld and **+10
absolute** on WebShop, both compared to imitation and reinforcement-learning baselines. ReAct
also reduces hallucination on HotpotQA and improves fact-verification on Fever via Wikipedia
API grounding, with the bonus of producing human-interpretable trajectories.

For the granularity-aware hierarchical agents project, ReAct is the conceptual ancestor of the
three-level granularity schema. The project's scope-aware (A) condition can be implemented as
a ReAct extension with explicit per-token granularity tags, preserving ReAct's
interpretability while adding scope discipline. The +34 ALFWorld gain is the strongest
published evidence that prompt-only agent improvements can produce large absolute effect sizes
— the project's +5-to-+15 abs targets are conservative against this benchmark.

</details>

<details>
<summary>🏤 <strong>Least-to-Most Prompting Enables Complex Reasoning in Large
Language Models</strong> — Zhou et al., 2022</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2205.10625` |
| **Authors** | Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, Ed Chi |
| **Venue** | ICLR 2023 (conference) |
| **DOI** | `10.48550/arXiv.2205.10625` |
| **URL** | https://arxiv.org/abs/2205.10625 |
| **Date added** | 2026-04-29 |
| **Categories** | [`hierarchical-planning`](../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../meta/categories/granularity-conditioning/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2205.10625/summary.md) |

Least-to-Most (LtM) prompting is a two-stage prompting technique designed to overcome
chain-of- thought's easy-to-hard generalization gap. The first stage decomposes a complex
problem into a sequence of simpler subproblems ordered by difficulty; the second stage solves
each subproblem using the answers to previously solved subproblems as additional context. The
motivation is that CoT performs well on test problems similar to in-context exemplars but
degrades sharply when test problems are harder.

Methodologically, LtM uses the same model (GPT-3 code-davinci-002 in the headline experiments)
in two prompting modes: decomposition and sequential solving. Evaluation covers SCAN
(compositional generalization), GSM8K (math), MultiArith (math), DROP (reading comprehension),
and Last Letter Concatenation (symbolic).

The headline result is **>=99% accuracy on SCAN length-split** with **just 14 exemplars**, vs.
**16% with vanilla chain-of-thought** — a **+83 absolute** gain. Other tasks show smaller but
consistent gains, with the improvement scaling with the easy-to-hard difficulty gap between
exemplars and test problems.

For the granularity-aware hierarchical agents project, LtM is the strongest empirical anchor
for the scope-aware (A) condition's expected effect size on hierarchical tasks. The +83
absolute SCAN gain sets the aspirational ceiling; the project's +5-to-+15 abs target on the
four-source composite is conservative against this anchor. Solution-reuse — each subproblem
using prior solutions in its context — is a detail worth replicating in scope-aware (A); pure
decomposition without solution-reuse loses much of LtM's gain.

</details>

## Tasks (2)

| # | Task | Status | Completed |
|---|------|--------|-----------|
| 0002 | [Literature survey: granularity conditioning and hierarchical agents](../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) | completed | 2026-04-29 14:26 |
| 0017 | [Literature: Hierarchical Agents and LLM-as-Judge](../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) | completed | 2026-05-01 01:40 |

## Answers (0)

No answers in this category.

## Suggestions (19 open, 7 closed)

<details>
<summary>🧪 <strong>Reframe the matched-mismatch wrapper so C is structurally
distinct from A</strong> (S-0026-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-02 | **Source**:
[t0026_phase2_abc_runtime_n147_for_rq1_rq5](../../tasks/t0026_phase2_abc_runtime_n147_for_rq1_rq5/)

Variant C beat B (paired McNemar p = 0.019) but only because the 'adversarial' wrapper
delegates to scope_aware_react with a perturbed strategy label, making C structurally
A-with-noise rather than B-with-extra-degradation. Redesign the matched-mismatch interface so
the adversarial variant operates on top of B's plan-and-solve scaffold, not A's, then re-run
the B vs C pair on the same paired set to test whether the inversion survives.

</details>

<details>
<summary>🧪 <strong>Add tool use (search, code execution) to the smoke harness for
FrontierScience-Olympiad</strong> (S-0012-03)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0012_phase2_abc_smoke_frontierscience](../../tasks/t0012_phase2_abc_smoke_frontierscience/)

The smoke ran with calculator+finish only. FrontierScience-Olympiad requires multi-step
numerical computation, retrieval, and code execution for most problems. Adding a Python code
execution tool and a retrieval tool would lift accuracy above the current floor and make
A-vs-B-vs-C differences observable even on haiku. Cost per row would increase by ~2-5x but
confirmatory N would decrease proportionally.

</details>

<details>
<summary>📂 <strong>Fix task_id collision in FrontierScience-Olympiad pilot
dataset</strong> (S-0012-04)</summary>

**Kind**: dataset | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0012_phase2_abc_smoke_frontierscience](../../tasks/t0012_phase2_abc_smoke_frontierscience/)

The hierarchical-annotation-v2 FrontierScience-Olympiad subset has 40 rows but only 26 unique
task_ids. Multiple rows share the same task_id (different granularity levels of the same
problem), which means the pairing logic treats them as separate predictions for the same task.
A deduplication or re-keying correction task should produce a version of the dataset with
unique task_ids per row, or document the intended semantics of multi-row task_ids.

</details>

<details>
<summary>🧪 <strong>Multi-provider replication: run Phase 2 harness with GPT-4o and
Gemini 1.5 Pro</strong> (S-0012-05)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0012_phase2_abc_smoke_frontierscience](../../tasks/t0012_phase2_abc_smoke_frontierscience/)

The smoke used only claude-haiku-4-5. Replicating on GPT-4o and Gemini 1.5 Pro (both now
available via project API keys) would test whether the granularity conditioning effect is
model-specific or generalizes across providers. The harness's model_call.py abstraction layer
makes this a configuration change rather than a code change. Defer until the confirmatory N
result is available from S-0012-02 to avoid spending budget before the primary hypothesis is
tested.

</details>

<details>
<summary>🔧 <strong>Use SELF-DISCOVER reasoning scaffolds as the scope-aware (A)
condition prompt template</strong> (S-0017-03)</summary>

**Kind**: technique | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0017_literature_hierarchical_agents_and_judges](../../tasks/t0017_literature_hierarchical_agents_and_judges/)

Zhou2024b (SELF-DISCOVER, NeurIPS 2024) shows that a task-conditioned reasoning structure --
selected from atomic reasoning modules and composed once per task type, then re-used across
instances -- transfers across model families and outperforms CoT-Self-Consistency at 10-40x
lower inference cost. The IMPLEMENT step (explicit JSON key-value scaffold) is the largest
ablation contributor. This is a near-zero-cost upgrade to our scope-aware (A) condition
prompt: produce one SELF-DISCOVER structure per benchmark family (FrontierScience-Olympiad,
SWE-bench Verified, tau-bench, WorkArena++), then re-use it across all rows of that family.
Predicts a measurable improvement on RQ1/RQ5 even without re-running annotation. Out of scope:
any retraining; this is purely a prompting change.

</details>

<details>
<summary>🧪 <strong>Run t0023's confirmatory ABC re-run with N>=157 using
abc_harness_metrics</strong> (S-0022-05)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0022_abc_harness_progress_rate_and_error_taxonomy](../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/)

The whole purpose of t0022 is to make t0023's confirmatory N>=157 ABC re-run produce signal at
the floor where binary task success failed in t0012. Schedule t0023 to consume
abc_harness_metrics: import score_trajectory, log per-trajectory progress_rate and per-step
error labels into the existing harness output, and report progress-rate means and
error-distribution mixtures per ABC condition with bootstrap CIs. Reuse the cached judge
responses from t0022 to keep marginal cost low. This is the direct downstream consumer this
task was built for.

</details>

<details>
<summary>🧪 <strong>Phase 2 calibration-focused A/B with explicit confidence
elicitation (recommended Candidate 2)</strong> (S-0025-01)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Run a minimum-viable Phase 2 A vs B experiment on a 30-instance subset of the composite
benchmark, eliciting agent self-reported confidence at every action and using a sonnet rotated
judge plus programmatic graders to break the t0019 anchoring effect. Primary metrics:
normalized task success and overconfident-error-rate (incorrect actions taken with
self-reported confidence above a threshold). This is the cheapest design that produces RQ1 +
RQ2 evidence simultaneously and stays inside the ~$10-14 envelope of the remaining ~$23
budget.

</details>

<details>
<summary>📊 <strong>Adopt AgentBoard progress-rate as a secondary RQ1 metric
alongside binary task success</strong> (S-0025-02)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Ma2024 (AgentBoard) shows that pairs of models with identical binary success rates differ by
up to 5.7 progress-rate points (Llama2-13b vs Mistral-7b), revealing differences invisible in
success-only evaluation. Add progress-rate as Metric 1b for every Phase 2 A/B/C run so that
even runs that tie on success surface granularity-conditioning differences in mid-trajectory
behaviour.

</details>

<details>
<summary>🧪 <strong>Phase 2 three-arm A/B/C pilot at half scale to test the
strict-double-inequality form of RQ5</strong> (S-0025-03)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Wen2024 NTPO is the only paper that directly observes a mismatched-scope condition
underperforming both baselines, but it is in the RL fine-tuning regime, not prompting. To test
RQ5's strict double inequality (C < both A and B) under our prompting framing, run all three
arms on a half-scale (15-instance) subset of the composite benchmark, ~$15-20. Lower-priority
than S-0025-01 because RQ5 is a sub-hypothesis and the strict form is the most expensive to
falsify.

</details>

<details>
<summary>🧪 <strong>Investigate group-level (subtask-level) DPO as an alternative to
A/B/C prompting for granularity conditioning</strong> (S-0025-06)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-05-01 | **Source**:
[t0025_lit_survey_hierarchical_agents_and_judges_2024_2026](../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/)

Gao2026 HPL ablates trajectory-, step-, and group-level DPO and isolates the group-level term
as the primary driver of the +3.97 abs gain over IPR on Qwen2.5-7B. The group level
corresponds exactly to the project's mid-granularity (subtask) annotation layer. If Phase 2
A/B/C prompting shows weak runtime gains, the next experiment should be a small-scale
group-level DPO fine-tune on the v2-tree annotated subset, comparing to a flat-DPO baseline.
Defer until after Phase 2 is complete and budget is reassessed.

</details>

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

**Kind**: experiment | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0002_literature_survey_granularity_conditioning](../../tasks/t0002_literature_survey_granularity_conditioning/)

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>

<details>
<summary>🧪 <strong>Use hierarchical-annotation-v1 to seed Phase 2 scope-conditioning
experiments</strong> (S-0005-06)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0005_hierarchical_annotation_pilot_v1](../../tasks/t0005_hierarchical_annotation_pilot_v1/)

The dataset asset is now ready for downstream consumption. Plan a baseline-evaluation task
that uses the 102 hierarchy-complete rows to compare scope-conditioned vs scope-unaware agent
prompts (B vs G/S/A from the project's research questions).

</details>

<details>
<summary>📊 <strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary>🔧 <strong>Extend the library to support a granularity that varies within
a single run</strong> (S-0006-05)</summary>

**Kind**: technique | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0006_scope_aware_react_library](../../tasks/t0006_scope_aware_react_library/)

Currently ScopeAwareReactAgent takes one fixed granularity for an entire run. A natural
extension is to let the agent emit a granularity transition (e.g., start global, drop to
subtask once a plan is established, drop to atomic during execution). Add a model-driven mode
where the parser also accepts <transition_to:subtask> markers and the agent updates the active
granularity per turn. This is a research extension worth Phase 2 ablation.

</details>

<details>
<summary>🧪 <strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

**Kind**: experiment | **Priority**: high | **Date**: 2026-04-29 | **Source**:
[t0007_scope_unaware_planandsolve_library](../../tasks/t0007_scope_unaware_planandsolve_library/)

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

</details>

<details>
<summary>📊 <strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

**Kind**: evaluation | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0007_scope_unaware_planandsolve_library](../../tasks/t0007_scope_unaware_planandsolve_library/)

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

<details>
<summary>🧪 <strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

**Kind**: experiment | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0010_matched_mismatch_library](../../tasks/t0010_matched_mismatch_library/)

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

</details>

<details>
<summary>📚 <strong>Per-step strategy override for matched_mismatch_v1</strong>
(S-0010-02)</summary>

**Kind**: library | **Priority**: medium | **Date**: 2026-04-29 | **Source**:
[t0010_matched_mismatch_library](../../tasks/t0010_matched_mismatch_library/)

Extend matched_mismatch_v1 with a per-step strategy override so callers can inject targeted
mismatches in specific phases (e.g., wrong-tag only at the global level; correct everywhere
else). This decomposes the C-condition gap by phase kind and supports follow-up analysis on
which structural slots are most sensitive to tag mismatch. Should be additive: the existing
uniform-strategy API stays the default. Keep the trajectory schema unchanged; the override is
constructor-side only.

</details>

<details>
<summary>📊 <strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

**Kind**: evaluation | **Priority**: low | **Date**: 2026-04-29 | **Source**:
[t0010_matched_mismatch_library](../../tasks/t0010_matched_mismatch_library/)

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>
