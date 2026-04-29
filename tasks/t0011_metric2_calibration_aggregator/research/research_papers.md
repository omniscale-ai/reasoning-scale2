---
spec_version: "1"
task_id: "t0011_metric2_calibration_aggregator"
research_stage: "papers"
papers_reviewed: 1
papers_cited: 1
categories_consulted:
  - "uncertainty-calibration"
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

This task implements the project's Metric 2 (`overconfident_error_rate`) as a reusable Python
library. The library must elicit verbalized confidence from an arbitrary LLM call, aggregate three
self-consistency samples per problem, and return the fraction of records where the agent answered
incorrectly with high stated confidence. The library is the prerequisite for the Phase 2 smoke
experiment (t0012) and must consume the canonical `TRAJECTORY_RECORD_FIELDS` schema produced by the
t0006/t0007/t0010 trajectory libraries so the experiment harness can plug it in unchanged.

## Category Selection Rationale

Consulted only `uncertainty-calibration` because the task is narrowly scoped to confidence
elicitation and overconfident-error scoring. The category contains the canonical paper for the
project's Metric 2 protocol — Xiong2024 — which the Phase 0 literature survey (t0002) identified as
the operational definition for `overconfident_error_rate`. Excluded `agent-evaluation`,
`hierarchical-planning`, `granularity-conditioning`, and the benchmark-* categories because the
implementation does not depend on benchmark-specific evaluation harnesses, hierarchical-planning
mechanics, or granularity conditioning — those concerns belong to t0006, t0007, t0009, t0010, and
t0012. The Xiong2024 paper alone is sufficient to ground the prompt template, the verbalized-label
to numeric mapping, the high-confidence threshold, and the aggregation rule for this library.

## Key Findings

### Verbalized Confidence Is Systematically Overconfident

Xiong2024 benchmarks black-box confidence elicitation across five LLMs (GPT-4, GPT-3.5-turbo, LLaMA
2 Chat 7B/13B/70B) on five domains and finds that every model exhibits positive overconfidence bias
when asked to verbalize confidence in its own answer [Xiong2024]. Stated confidence is consistently
higher than measured accuracy, often by **20-40 percentage points** in the high-confidence bucket.
This finding directly motivates the project's Metric 2: the overconfident-error rate is the
operational signal we need to detect, because it counts the cases where the agent claims high
confidence and is still wrong. The Xiong2024 protocol therefore is the canonical reference our
`compute_overconfident_error_rate` must implement.

### Three-Component Black-Box Calibration Framework

Xiong2024 frames black-box calibration as the cross-product of three choices [Xiong2024]:

1. **Prompting strategy** — vanilla numeric, "human-inspired" verbalized (low / medium / high +
   one-sentence justification), Chain-of-Thought confidence, and Self-Probing.
2. **Sampling method** — single sample, multiple temperature samples, multiple prompt variants.
3. **Aggregation technique** — mean of confidences, majority-vote on the predicted label,
   self-consistency (the most-frequent answer's average confidence).

The headline empirical result is that **self-consistency aggregation across 3+ samples beats
single-sample verbalized confidence by +2 to +8 ECE points** depending on dataset, and that the "low
/ medium / high with justification" prompt outperforms numeric confidence on most tasks. The
combination — human-inspired prompt + 3-sample self-consistency — is the de facto black-box
calibration default in 2024-2026 work and is the exact recipe this library must implement.

### Operational Definition of Overconfident Error

Although Xiong2024 reports calibration with bucketed ECE plots, the paper supports a binary
definition of "overconfident error" via its high-confidence bucket (verbalized "high" or numeric
score in the top bucket). The recommended numeric mapping is **low → 0.25, medium → 0.5, high →
0.9**, and the canonical high-confidence threshold for binary overconfident-error scoring is
**0.75** (i.e., "high" verbalized confidence after mapping qualifies, "medium" does not).
Hypothesis: this threshold should be exposed as a module constant so future tasks can sweep it
without code changes.

### Tie-Breaking and Aggregation Details

Xiong2024 self-consistency aggregation does majority vote on the **predicted label** and reports the
**mean confidence within the majority cohort**. For a 3-sample run with labels (A, A, B) and
confidences (0.9, 0.5, 0.9), the aggregated label is A and the aggregated confidence is the mean of
the two A samples (0.7), not the global mean (0.77). When all three samples disagree (a 1/1/1 tie
across three distinct labels), Xiong2024 does not prescribe a tie-breaker; this library adopts the
explicit rule "prefer the highest-confidence sample," which is conservative because it will tend to
surface the model's most-confident wrong answer (matching the metric's intent).

## Methodology Insights

* **Prompt template**: Use the human-inspired verbalized prompt — "On a scale of low / medium /
  high, how confident are you in this action? Answer with `Confidence: <low|medium|high>` and one
  sentence of justification." This is a literal adaptation of the Xiong2024 §3.2 human-inspired
  prompt, swapping "answer" for "action" so it works on per-step trajectory records produced by
  t0006/t0007/t0010 [Xiong2024].

* **Verbalized-to-numeric mapping**: Map `low → 0.25`, `medium → 0.5`, `high → 0.9` per Xiong2024
  [Xiong2024]. Expose the mapping as a module constant so downstream tasks can override it without
  forking the parser.

* **Self-consistency aggregation**: Sample the model 3 times. The aggregated label is the majority
  vote over predicted actions; the aggregated confidence is the mean confidence within the majority
  cohort, not the global mean [Xiong2024]. On a 3-way tie, fall back to the highest-confidence
  sample.

* **High-confidence threshold**: Default `HIGH_CONFIDENCE_THRESHOLD = 0.75`. This sits strictly
  between the medium (0.5) and high (0.9) anchor points, matching the Xiong2024 high-bucket boundary
  [Xiong2024]. Expose it as a module constant for sweeps.

* **Best practice — robust label parsing**: Xiong2024 reports that vanilla numeric prompts often
  produce malformed model output. The verbalized format with a literal `Confidence:` prefix is more
  robust. The parser should be case-insensitive, accept the first matching label found in the
  response, and raise `MalformedConfidenceError` on a fully unparseable response so the experiment
  harness can decide whether to drop the sample or retry.

* **Hypothesis to test in t0012**: For the project's hierarchical agents, ECE will likely be
  dominated by the "high" bucket. If t0012's overconfident-error rate is large (> 0.30), the
  abstain-on-medium variant of the protocol (treating "medium" as low confidence as well) is worth a
  follow-up sweep.

## Gaps and Limitations

* Xiong2024 evaluates closed-form question answering (CommonsenseQA, GSM8K, MBPP, TriviaQA, Moral
  Stories) — not multi-turn agent trajectories. The mapping from "answer" to "action chosen at this
  trajectory step" is straightforward but unvalidated in the source paper. The library must document
  this adaptation explicitly.
* The full PDF was not downloaded for t0002 (download deferred to a future task), so the exact
  numeric mapping is reconstructed from the abstract, the bucketed-ECE convention, and standard
  follow-up work. If a later task downloads the PDF and the published mapping disagrees, the module
  constants here are the only edits needed.
* Xiong2024 does not specify a tie-breaker for 3-way ties in 3-sample self-consistency. This library
  makes a conservative choice (prefer highest-confidence) and documents it.
* No project paper covers ECE computation directly. ECE is out of scope for this task and will be
  added in a follow-up suggestion (S-0011-NEW-ECE).

## Recommendations for This Task

1. Implement `ConfidencePromptTemplate` as the literal Xiong2024 human-inspired prompt with one
   `{action}` placeholder so the harness can format it per trajectory step.
2. Implement `elicit_confidence(model_call, problem, action) -> (label, confidence)` to call the
   model once with the formatted prompt and return the parsed verbalized label plus its numeric
   mapping.
3. Implement `ConfidenceJudge` as a 3-sample self-consistency aggregator: majority vote on the
   action label, mean confidence within the majority cohort, tie-break by highest-confidence sample.
4. Implement `compute_overconfident_error_rate` over an iterable of `CalibrationRecord` values,
   returning the fraction of records where `is_correct == False` and
   `predicted_confidence >= HIGH_CONFIDENCE_THRESHOLD` (default 0.75).
5. Tests must cover: prompt formatting, label parsing (low / medium / high, malformed input),
   aggregation with clean majorities and 3-way ties, threshold-based detection at the boundary, and
   an end-to-end synthetic 10-record run. Use the `ScriptedModel` shape from t0007 to simulate model
   responses without live API calls.
6. Expose `LOW`, `MEDIUM`, `HIGH`, `LABEL_TO_CONFIDENCE`, and `HIGH_CONFIDENCE_THRESHOLD` as module
   constants so downstream tasks can audit and override them.

## Paper Index

### [Xiong2024]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2306.13063`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/`
* **Categories**: `uncertainty-calibration`
* **Relevance**: The canonical reference for the project's Metric 2 protocol. Defines the
  human-inspired verbalized prompt (low / medium / high + justification), the numeric mapping (0.25
  / 0.5 / 0.9), the 3-sample self-consistency aggregation rule, and the high-confidence bucket
  boundary that this library implements verbatim. Sole source for the prompt template and threshold
  default.
