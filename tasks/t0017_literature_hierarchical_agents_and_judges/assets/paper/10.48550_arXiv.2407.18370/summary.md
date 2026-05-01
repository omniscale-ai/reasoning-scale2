---
spec_version: "3"
paper_id: "10.48550_arXiv.2407.18370"
citation_key: "Jung2024"
summarized_by_task: "t0017_literature_hierarchical_agents_and_judges"
date_summarized: "2026-05-01"
---
# Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement

## Metadata

* **File**: `files/jung_2024_trust-or-escalate.pdf`
* **Published**: 2024-07-25 (arXiv); ICLR 2025 (oral)
* **Authors**: Jaehun Jung 🇺🇸, Faeze Brahman 🇺🇸, Yejin Choi 🇺🇸
* **Venue**: ICLR 2025
* **DOI**: `10.48550/arXiv.2407.18370`

## Abstract

We present a principled approach to provide LLM-based evaluation with a rigorous guarantee of human
agreement. We first propose that a reliable evaluation method should not uncritically rely on model
preferences for pairwise evaluation, but rather assess the confidence of judge models and
selectively decide when to trust its judgement. We then show that under this selective evaluation
framework, human agreement can be provably guaranteed--such that the model evaluation aligns with
that of humans to a user-specified agreement level. As part of our framework, we also introduce
Simulated Annotators, a novel confidence estimation method that significantly improves judge
calibration and thus enables high coverage of evaluated instances. Finally, we propose Cascaded
Selective Evaluation, where we use cheaper models as initial judges and escalate to stronger models
only when necessary--again, while still providing a provable guarantee of human agreement.
Experimental results show that Cascaded Selective Evaluation guarantees strong alignment with
humans, far beyond what LLM judges could achieve without selective evaluation. For example, on a
subset of Chatbot Arena where GPT-4 almost never achieves 80% human agreement, our method, even
while employing substantially cost-effective models such as Mistral-7B, guarantees over 80% human
agreement with almost 80% test coverage.

## Overview

This paper attacks a foundational reliability gap in LLM-as-judge evaluation: even the strongest
judges (GPT-4) suffer from systematic biases and over-confidence, yet practitioners routinely trust
their pairwise verdicts without any provable agreement guarantee. The authors recast judge
evaluation as a **selective classification** problem: given a user-specified risk tolerance alpha
and an error level delta, the system either returns a verdict or abstains, with the formal guarantee
that conditional on non-abstention, the LLM agrees with the human majority label with probability at
least 1 - alpha (and this property itself holds with probability at least 1 - delta over the
calibration draw).

The framework has three pieces. First, **threshold calibration via fixed-sequence multiple
hypothesis testing** on a small held-out set yields an exact upper-confidence bound on selective
risk, tighter than Bonferroni or marginal conformal alternatives. Second, **Simulated Annotators**
is a new confidence measure: instead of using predictive probability or verbalized confidence (both
shown to be miscalibrated), the judge is conditioned on diverse few-shot annotator personas via
in-context learning, and confidence is the agreement ratio across simulated annotators. Third,
**Cascaded Selective Evaluation** chains weak-to-strong judges (Mistral-7B to GPT-3.5-turbo to
GPT-4-turbo): each stage either commits a verdict (if its calibrated confidence threshold is met) or
escalates to a stronger judge, with risk control proven across the full cascade. The headline
empirical result is that the cascade meets target agreement levels GPT-4 alone cannot reach, while
routing the majority of instances to substantially cheaper models.

## Architecture, Models and Methods

The selective evaluator is a pair (f_LM, c_LM): given an input x = (query, generation_a1,
generation_a2), it returns the judge label f_LM(x) when c_LM(x) >= lambda, and the abstain symbol
otherwise. The threshold lambda is chosen by **fixed-sequence testing** (Bauer 1991) on a
calibration set D_cal of human-annotated preferences (sizes |D_cal| = 500 for TL;DR and ChatArena,
392 for Auto-J). For each candidate lambda, the empirical risk R_hat(lambda) is the disagreement
rate over evaluated calibration instances; an exact binomial upper-confidence bound R_hat_plus gives
a (1 - delta)-valid risk estimate, and the search starts at lambda = 0.999 and decreases until
R_hat_plus first exceeds alpha. Theorem 1 proves the resulting selector satisfies P(f_LM(x) =
y_human | c_LM(x) >= lambda_hat) >= 1 - alpha with probability >= 1 - delta.

**Simulated Annotators** estimates c_LM by prompting the same judge model with K different
in-context demonstrations (K few-shot annotators) and N simulation runs (typical K = N = 5, ablated
down to N = 1). The "Independent" variant uses per-annotator labels y_i,j; the "Majority" variant
uses majority labels and varies inputs. Confidence is the cross-simulation agreement ratio.

The **cascade** uses Mistral-7B-instruct-v0.2, GPT-3.5-turbo, and GPT-4-turbo by default. Each judge
gets its own calibrated threshold lambda_i; a stronger cascade ablation swaps in Mixtral-8x7B.
Calibration uses delta = 0.1 throughout. Evaluations report Expected Calibration Error (ECE), AUROC,
AUPRC for the confidence measure, plus Coverage and Guarantee Success Rate (fraction of 1000 random
calibration/test splits where empirical agreement >= 1 - alpha) for risk-control performance.

## Results

* On TL;DR with target 1 - alpha = 0.9, **Cascaded Selective Evaluation achieves 90.8% guarantee
  success rate** at 55.7% coverage, vs. 0.0% for No-Selection, 42.0% for Heuristic Selection, and
  47.5%-79.0% for Point-Estimate Calibration variants.
* The TL;DR cascade routes 28.3% of evaluations to Mistral-7B, 28.2% to GPT-3.5-turbo, and only
  43.5% to GPT-4-turbo at the 1 - alpha = 0.9 level.
* On ChatArena with target 1 - alpha = 0.85, the cascade achieves **91.0% guarantee success rate**
  at 63.2% coverage, while GPT-4 alone (No-Selection) hits 0.0% guarantee success rate at 100%
  coverage and only 77.8% empirical agreement.
* For ChatArena, the cascade routes 23.7% to Mistral-7B, 58.8% to GPT-3.5-turbo, and just 17.5% to
  GPT-4-turbo at the 0.85 target.
* **Simulated Annotators (Independent)** reduces ECE by ~50% relative to Predictive Probability
  (e.g., 0.095 vs. 0.217 on AlpacaEval with GPT-4-turbo) and improves AUROC by ~13% (0.723 vs.
  0.642).
* For weaker judges, Simulated Annotators is even more impactful: Mistral-7B-instruct ECE drops from
  0.374 (Predictive Probability) to 0.075 on AlpacaEval; accuracy rises from 0.618 to 0.684.
* **Cost reductions**: at the 1 - alpha = 0.8 ChatArena target, the stronger cascade uses 21.5% of
  GPT-4-only API cost, and the weaker cascade uses 12.6%, while both clear 90% guarantee success
  rate.
* **Abstention is principled, not heuristic**: abstained ChatArena samples have lower human
  inter-annotator agreement (0.815) than evaluated samples (0.902), but token overlap (0.623 vs.
  0.592) and length ratio (0.242 vs. 0.245) differ negligibly.
* Increasing N from 1 to 5 simulated annotators raises coverage from 60.9% to 63.2% on ChatArena
  while maintaining ~90% guarantee success rate and a 40% cost saving over GPT-4 baseline.

## Innovations

### Provable Human-Agreement Guarantee for LLM Judges

The paper is the first to deliver an **exact, conditional** risk bound for LLM-based pairwise
evaluation: P(judge agrees with human | non-abstention) >= 1 - alpha holds with probability >= 1 -
delta over the calibration sample. Prior conformal-style works for LLMs (Yadkori et al. 2024; Gui et
al. 2024) only achieve marginal or approximate control. This reframes "Can I trust this judge?" as a
calibrated, user-tunable knob rather than a heuristic.

### Simulated Annotators as an Unsupervised Confidence Measure

By prompting the judge with multiple distinct annotator personas via in-context learning and
measuring agreement across simulations, Simulated Annotators produces a confidence signal that beats
predictive probability and verbalized confidence on both calibration (ECE) and failure prediction
(AUROC/AUPRC), without any external supervision or calibration training data. Crucially, the gain is
largest for weaker judges (Mistral-7B, GPT-3.5), which is exactly what the cascade needs.

### Cost-Optimal Judge Cascading with End-to-End Risk Control

Cascaded Selective Evaluation generalizes selective evaluation across a sequence of judges and
proves that risk control composes across the cascade when each lambda_i is calibrated separately.
This is the first cascade-of-judges design with formal agreement guarantees, and it operationalizes
the slogan "trust or escalate": route easy instances to cheap models, escalate hard instances, and
abstain when even GPT-4 is uncertain. The mechanism delivers >75% cost savings vs. GPT-4-only
evaluation at higher empirical agreement.

## Datasets

* **TL;DR** (Stiennon et al., 2020) -- Reddit summarization preference dataset; multi-annotator
  labels per instance; used with Simulated Annotators (Independent), |D_cal| = 500.
* **AlpacaEval** -- pairwise preference dataset over Alpaca-style instruction-following responses;
  used in calibration tables for confidence-measure evaluation.
* **Chat(bot) Arena** (Zheng et al. 2023; Li et al. 2024a) -- 5.2k subsampled real-world
  user-assistant comparison instances; single human annotation per input; used with Simulated
  Annotators (Majority), |D_cal| = 500.
* **Auto-J** (Li et al., 2023) -- 392-instance curated benchmark for meta-evaluation of LLM judges,
  including ties; used with K = N = 3.

All datasets are publicly available preference benchmarks; the cascade uses Mistral-7B-instruct,
GPT-3.5-turbo, and GPT-4-turbo as judges (with Mixtral-8x7B in cascade ablations). No new dataset is
introduced; ChatArena human IAA annotations were collected for the abstention-policy analysis.

## Main Ideas

* **Selective evaluation with calibrated thresholds is the right primitive for trustworthy
  LLM-as-judge**: any project that uses LLM judges (including agent-as-judge for multi-step trace
  evaluation) should expose a user-specified risk tolerance and abstain rather than emit unreliable
  verdicts.
* **Confidence estimation for judges should be ensemble-based, not single-shot probability**:
  Simulated Annotators is a drop-in technique that works on top of any judge LLM and is particularly
  valuable for cheaper models -- which matters when GPT-4 cost is prohibitive.
* **Judge cascades convert "model choice" into "abstention policy"**: instead of picking one
  expensive judge, route by confidence and only escalate when needed. This is highly relevant for
  hierarchical agent evaluation pipelines where most steps are easy and a small minority require
  expensive scrutiny.
* The **fixed-sequence testing** calibration recipe (Bauer 1991, Bates et al. 2021) gives tighter
  bounds than Bonferroni or marginal conformal control and should be the default for selective LLM
  applications with monotone risk.
* **Empirical lesson**: Even at 80% human agreement on ChatArena -- a level GPT-4 alone never
  reaches -- 75% of the work can be handled by Mistral-7B/GPT-3.5, dramatically changing the cost
  envelope for large-scale benchmarking.

## Summary

Jung, Brahman, and Choi address a central reliability gap in LLM-as-judge evaluation: when used at
scale to grade pairs of model generations, even GPT-4-class judges have no provable bound on their
agreement with humans, yet downstream leaderboards and benchmarks treat their verdicts as ground
truth. The authors reframe evaluation as a **selective classification with risk control** problem,
deriving a fixed-sequence multiple-testing procedure that calibrates a confidence threshold lambda
on a small human-labeled calibration set and yields an exact binomial upper bound on selective
disagreement risk.

Methodologically, the paper contributes three components. **Selective evaluation** provides the
formal P(agreement | non-abstention) >= 1 - alpha guarantee; **Simulated Annotators** produces
high-quality unsupervised confidence estimates by prompting the judge with diverse few-shot
annotator personas and aggregating cross-simulation agreement; and **Cascaded Selective Evaluation**
chains weak-to-strong judges so that easy instances are decided cheaply and only hard instances
escalate, with the risk-control proof composing across cascade stages.

Empirically, on TL;DR, ChatArena, and Auto-J, the cascade achieves 90%+ guarantee success rate at
target agreement levels (0.85, 0.9) where GPT-4 alone has 0% guarantee success rate. Coverage
remains in the 55-65% range, but the routing concentrates GPT-4 calls on the hardest 17-44% of
instances, cutting evaluation cost by 78-87% versus a GPT-4-only baseline. Simulated Annotators
roughly halves ECE for GPT-4 (0.217 to 0.095 on AlpacaEval) and improves both ECE and accuracy for
Mistral-7B (ECE 0.374 to 0.075). The abstention policy correlates with human-perceived subjectivity
(IAA 0.815 abstained vs. 0.902 evaluated) rather than shallow features.

For this project on hierarchical agents and judges, the paper is highly load-bearing. It supplies
(i) a formal abstention/escalation primitive directly applicable to agent-as-judge evaluation of
multi-step trajectories, (ii) Simulated Annotators as a strong, cheap baseline confidence measure to
compare any new uncertainty methods against, and (iii) a worked-out cost-vs-coverage trade-off
showing that mixed cascades can deliver higher empirical reliability than monolithic GPT-4 judging
at a fraction of the API cost. Adopting calibrated selective evaluation should be a default for any
judge-driven metric we report.
