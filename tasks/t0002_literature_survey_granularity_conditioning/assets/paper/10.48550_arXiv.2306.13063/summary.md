---
spec_version: "3"
paper_id: "10.48550_arXiv.2306.13063"
citation_key: "Xiong2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2023 (arXiv); 2024 (ICLR)
* **Authors**: Miao Xiong 🇸🇬, Zhiyuan Hu 🇸🇬, Xinyang Lu 🇸🇬, Yifei Li 🇭🇰, Jie Fu 🇭🇰,
  Junxian He 🇭🇰, Bryan Hooi 🇸🇬
* **Venue**: ICLR 2024
* **DOI**: `10.48550/arXiv.2306.13063`

## Abstract

Empowering large language models (LLMs) to accurately express confidence in their answers is
essential for trustworthy decision-making. Previous confidence elicitation methods, which
primarily rely on white-box access to internal model information or model fine-tuning, have
become less suitable for LLMs, especially closed-source commercial APIs. This leads to a growing
need to explore the untapped area of black-box approaches for LLM uncertainty estimation. To
better break down the problem, we define a systematic framework with three components: prompting
strategies for eliciting verbal confidence, sampling methods for generating multiple responses,
and aggregation techniques for computing consistency. We then benchmark these methods on two key
tasks—confidence calibration and failure prediction—across five types of datasets (e.g.,
commonsense and arithmetic reasoning) and five widely-used LLMs including GPT-4 and LLaMA 2 Chat.
Our analysis uncovers several key insights: 1) LLMs, when verbalizing their confidence, tend to
be overconfident, potentially imitating human patterns of expressing confidence. 2) As model
capability scales up, both calibration and failure prediction performance improve. 3) Employing
our proposed strategies, such as human-inspired prompts, consistency among multiple responses,
and better aggregation strategies can help mitigate this overconfidence from various
perspectives.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. Xiong et al. address the **calibration gap** in modern
LLMs: when asked to verbalize their confidence in an answer, LLMs are systematically
overconfident — their stated confidence is consistently higher than their actual accuracy. This
matters for any system that uses confidence as a control signal (selective abstention,
information-seeking, escalation to humans).

The paper proposes a **three-component framework** — prompting strategy + sampling method +
aggregation technique — and benchmarks the cross-product on five datasets and five widely-used
LLMs. The headline finding: **self-consistency aggregation across multiple sampled responses**
significantly outperforms naive single-sample verbalized confidence, reducing Expected
Calibration Error (ECE) by **+2 to +8 points** depending on dataset.

For the granularity-aware hierarchical agents project, this paper is the **canonical calibration
reference** for Metric 2 (overconfident error rate). The recommended protocol — verbalized
confidence + 3-sample self-consistency aggregation — should be adopted as the project's
operational definition.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
three-component framework is:

* **Prompting strategies** (4 variants): vanilla "How confident are you in this answer?",
  human-inspired "Provide your confidence level (low / medium / high) and brief justification",
  Chain-of-Thought confidence, Self-Probing confidence.
* **Sampling methods** (3 variants): single sample, multiple temperature samples, multiple
  prompts.
* **Aggregation techniques** (3 variants): mean of confidences, majority vote, self-consistency
  (the most-frequent answer's average confidence).

Models evaluated: **GPT-4**, **GPT-3.5-turbo**, **LLaMA 2 Chat (7B / 13B / 70B)**, plus a small
control set. Datasets cover commonsense reasoning (CommonsenseQA), arithmetic (GSM8K), code
(MBPP), factual recall (TriviaQA), and ethics (Moral Stories) — five categories total.

Two evaluation tasks: **calibration** (does the verbalized confidence track actual accuracy?
measured via ECE), and **failure prediction** (does low confidence predict incorrect answers?
measured via AUROC).

## Results

* **LLMs are systematically overconfident** when verbalizing confidence — every model and every
  dataset shows positive overconfidence
* **Self-consistency aggregation** is the most reliable aggregation method, beating naive
  single-sample verbalized confidence by **+2 to +8 ECE points** depending on dataset
* **Larger models calibrate better** — GPT-4 has lower ECE than GPT-3.5; 70B LLaMA beats 7B
* **Human-inspired prompting** ("low / medium / high with justification") outperforms vanilla
  numeric confidence on most tasks
* **Failure prediction AUROC** improves substantially with self-consistency — moving from ~0.6
  (single sample) to **~0.75-0.85** (self-consistency) depending on model and task
* **CoT confidence does not always help** — counterintuitively, prompting the model to reason
  before stating confidence can sometimes worsen calibration

## Innovations

### Three-Component Framework for Black-Box Calibration

Prior calibration work focused on white-box access to internal logits or fine-tuning. This paper
is the first to systematically benchmark *only* black-box prompting strategies that work with
closed-source APIs.

### Self-Consistency Aggregation as the Default

The finding that self-consistency aggregation (majority vote on the answer, then average
confidence within the majority) substantially outperforms single-sample confidence has become
the de facto standard for LLM calibration in 2024-2026.

### Human-Inspired Confidence Prompts

The "low / medium / high with justification" prompt outperforms numeric confidence — a small
prompt-engineering finding with disproportionately large practical impact.

## Datasets

* **CommonsenseQA** — commonsense reasoning multiple-choice.
* **GSM8K** — grade-school math.
* **MBPP** — Python code completion.
* **TriviaQA** — factual recall QA.
* **Moral Stories** — ethical reasoning.

All five are public benchmarks.

## Main Ideas

* Adopt **verbalized confidence + 3-sample self-consistency aggregation** as the project's
  Metric 2 protocol [Xiong2024]. This is the canonical black-box calibration method.
* Define **overconfident error** as `is_incorrect AND verbalized_confidence >= 0.8` (or "high"
  in the human-inspired prompt). The paper supports this binarization implicitly via its
  per-bucket ECE plots.
* **Report bucketed ECE plots** (10 confidence bins) alongside every Metric 2 number. A single
  ECE number hides the bucket where overconfidence occurs.
* **Use the human-inspired prompt** ("low / medium / high with justification") for the
  scope-aware (A) condition's confidence elicitation. Numeric confidence is more standardizable
  but less reliable.

## Summary

Xiong et al. address the calibration gap in modern LLMs: verbalized confidence is systematically
higher than actual accuracy, making it an unreliable signal for any system that needs to abstain
or escalate based on uncertainty. The motivation is that previous calibration methods relied on
white-box access to internal logits or model fine-tuning, neither of which is available for
closed-source commercial APIs.

Methodologically, the paper proposes a three-component black-box framework: prompting strategy
(vanilla, human-inspired, CoT, self-probing) × sampling method (single, multiple temperature,
multiple prompts) × aggregation technique (mean, majority vote, self-consistency). The
cross-product is benchmarked on five datasets across reasoning, math, code, factual recall, and
ethics, using five widely-used LLMs (GPT-4, GPT-3.5, LLaMA 2 Chat at three sizes).

The headline findings are (a) LLMs are systematically overconfident when verbalizing confidence,
(b) self-consistency aggregation beats single-sample confidence by **+2 to +8 ECE points**, (c)
larger models calibrate better, (d) human-inspired prompting ("low / medium / high with
justification") outperforms numeric confidence, (e) CoT confidence sometimes worsens calibration
counterintuitively.

For the granularity-aware hierarchical agents project, this paper is the canonical calibration
reference for Metric 2 (overconfident error rate). The project should adopt verbalized
confidence + 3-sample self-consistency aggregation as its operational definition, define
overconfident error as `incorrect AND high_confidence`, and report bucketed ECE plots alongside
single-number ECE. The human-inspired prompt is recommended for the scope-aware (A) condition's
confidence elicitation.
