# Papers: `uncertainty-calibration` (2)

2 papers across 1 year(s).

[Back to all papers](../README.md)

---

## 2024 (2)

<details>
<summary>🏤 Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence
Elicitation in LLMs — Xiong et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2306.13063` |
| **Authors** | Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, Bryan Hooi |
| **Venue** | ICLR 2024 (conference) |
| **DOI** | `10.48550/arXiv.2306.13063` |
| **URL** | https://arxiv.org/abs/2306.13063 |
| **Date added** | 2026-04-29 |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/summary.md) |

Xiong et al. address the calibration gap in modern LLMs: verbalized confidence is
systematically higher than actual accuracy, making it an unreliable signal for any system that
needs to abstain or escalate based on uncertainty. The motivation is that previous calibration
methods relied on white-box access to internal logits or model fine-tuning, neither of which
is available for closed-source commercial APIs.

Methodologically, the paper proposes a three-component black-box framework: prompting strategy
(vanilla, human-inspired, CoT, self-probing) × sampling method (single, multiple temperature,
multiple prompts) × aggregation technique (mean, majority vote, self-consistency). The
cross-product is benchmarked on five datasets across reasoning, math, code, factual recall,
and ethics, using five widely-used LLMs (GPT-4, GPT-3.5, LLaMA 2 Chat at three sizes).

The headline findings are (a) LLMs are systematically overconfident when verbalizing
confidence, (b) self-consistency aggregation beats single-sample confidence by **+2 to +8 ECE
points**, (c) larger models calibrate better, (d) human-inspired prompting ("low / medium /
high with justification") outperforms numeric confidence, (e) CoT confidence sometimes worsens
calibration counterintuitively.

For the granularity-aware hierarchical agents project, this paper is the canonical calibration
reference for Metric 2 (overconfident error rate). The project should adopt verbalized
confidence + 3-sample self-consistency aggregation as its operational definition, define
overconfident error as `incorrect AND high_confidence`, and report bucketed ECE plots
alongside single-number ECE. The human-inspired prompt is recommended for the scope-aware (A)
condition's confidence elicitation.

</details>

<details>
<summary>🏤 Trust or Escalate: LLM Judges with Provable Guarantees for Human
Agreement — Jung et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2407.18370` |
| **Authors** | Jaehun Jung, Faeze Brahman, Yejin Choi |
| **Venue** | ICLR 2025 (conference) |
| **DOI** | `10.48550/arXiv.2407.18370` |
| **URL** | https://arxiv.org/abs/2407.18370 |
| **Date added** | 2026-05-01 |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |
| **Added by** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/summary.md) |

Jung, Brahman, and Choi address a central reliability gap in LLM-as-judge evaluation: when
used at scale to grade pairs of model generations, even GPT-4-class judges have no provable
bound on their agreement with humans, yet downstream leaderboards and benchmarks treat their
verdicts as ground truth. The authors reframe evaluation as a **selective classification with
risk control** problem, deriving a fixed-sequence multiple-testing procedure that calibrates a
confidence threshold lambda on a small human-labeled calibration set and yields an exact
binomial upper bound on selective disagreement risk.

Methodologically, the paper contributes three components. **Selective evaluation** provides
the formal P(agreement | non-abstention) >= 1 - alpha guarantee; **Simulated Annotators**
produces high-quality unsupervised confidence estimates by prompting the judge with diverse
few-shot annotator personas and aggregating cross-simulation agreement; and **Cascaded
Selective Evaluation** chains weak-to-strong judges so that easy instances are decided cheaply
and only hard instances escalate, with the risk-control proof composing across cascade stages.

Empirically, on TL;DR, ChatArena, and Auto-J, the cascade achieves 90%+ guarantee success rate
at target agreement levels (0.85, 0.9) where GPT-4 alone has 0% guarantee success rate.
Coverage remains in the 55-65% range, but the routing concentrates GPT-4 calls on the hardest
17-44% of instances, cutting evaluation cost by 78-87% versus a GPT-4-only baseline. Simulated
Annotators roughly halves ECE for GPT-4 (0.217 to 0.095 on AlpacaEval) and improves both ECE
and accuracy for Mistral-7B (ECE 0.374 to 0.075). The abstention policy correlates with
human-perceived subjectivity (IAA 0.815 abstained vs. 0.902 evaluated) rather than shallow
features.

For this project on hierarchical agents and judges, the paper is highly load-bearing. It
supplies (i) a formal abstention/escalation primitive directly applicable to agent-as-judge
evaluation of multi-step trajectories, (ii) Simulated Annotators as a strong, cheap baseline
confidence measure to compare any new uncertainty methods against, and (iii) a worked-out
cost-vs-coverage trade-off showing that mixed cascades can deliver higher empirical
reliability than monolithic GPT-4 judging at a fraction of the API cost. Adopting calibrated
selective evaluation should be a default for any judge-driven metric we report.

</details>
