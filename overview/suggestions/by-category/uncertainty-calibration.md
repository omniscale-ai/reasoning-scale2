# Suggestions: `uncertainty-calibration`

15 suggestion(s) in category
[`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) **12 open** (5
high, 2 medium, 5 low), **3 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📊 <strong>Adopt Trust-or-Escalate selective evaluation for the multi-judge
agreement study</strong> (S-0017-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2407.18370`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2407.18370/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

S-0009-03 calls for a multi-judge agreement study; Jung2024 ("Trust or Escalate", ICLR 2025)
provides the right primitive. Implement a selective-judging pipeline with two ingredients: (1)
Simulated Annotators on top of the project's existing judge LLM to produce ensemble-based
confidence scores, and (2) a calibrated abstention threshold using fixed-sequence testing
(Bauer 1991, Bates et al. 2021) so the pipeline ships with a finite-sample, distribution-free
guarantee on human-judge agreement. Empirically Jung2024 shows that 75% of pairwise judging on
ChatArena can be delegated to Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor
that GPT-4 alone never reaches, so this is also a cost-reduction path for any large-scale
annotation rerun. Deliverable: a small library that wraps the existing judge call with
confidence + abstain semantics, exposed to t0009-style annotation tasks.

</details>

<details>
<summary>🧪 <strong>Confirmatory v2 vs v1 schema sweep with fresh annotations and
a third sonnet judge</strong> (S-0019-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

Run a confirmatory experiment that re-annotates a fresh n>=80 row pool (not the t0014 pool)
under the v1 and v2 schemas with claude-sonnet-4-6 as annotator, then judges with three
independent sonnet configurations: substantive critic, model-rotated original prompt, and a
new criterion-decomposed rubric judge. The current task left the +24.6 / +37.3 pp delta band
unsettled because the two judge configurations disagreed on the +30 pp threshold and the pool
overlapped with t0014. A fresh-pool replication at the planned n>=80 would tighten the
per-cell Wilson CIs from +/-24 pp to +/-11 pp, enough to either reset the headline below +30
pp or commit it above +45 pp.

</details>

<details>
<summary>🧪 <strong>Phase 2 calibration-focused A/B with explicit confidence
elicitation (recommended Candidate 2)</strong> (S-0025-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0025-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Source paper** | [`10.48550_arXiv.2407.18370`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/assets/paper/10.48550_arXiv.2407.18370/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Run a minimum-viable Phase 2 A vs B experiment on a 30-instance subset of the composite
benchmark, eliciting agent self-reported confidence at every action and using a sonnet rotated
judge plus programmatic graders to break the t0019 anchoring effect. Primary metrics:
normalized task success and overconfident-error-rate (incorrect actions taken with
self-reported confidence above a threshold). This is the cheapest design that produces RQ1 +
RQ2 evidence simultaneously and stays inside the ~$10-14 envelope of the remaining ~$23
budget.

</details>

<details>
<summary>📊 <strong>Replace haiku judge with a sonnet-rotated or programmatic grader
for all Phase 2 A/B/C scoring</strong> (S-0025-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0025-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Source paper** | — |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

t0019 found judge anchoring on model identity inflates the schema effect by ~+33 pp under the
haiku judge versus a sonnet rotated judge. Any RQ1 / RQ2 / RQ4 measurement that uses the haiku
judge to grade A vs B is judge-confounded. Adopt a sonnet rotated judge as the default for
Phase 2 grading and use programmatic benchmark-specific graders (FrontierScience scorer,
SWE-bench harness, tau-bench scorer, WorkArena++ scorer) wherever possible to remove the LLM
judge from the gradient.

</details>

<details>
<summary>📊 <strong>Track final_confidence vs correctness calibration on the t0023
confirmatory run</strong> (S-0021-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0021-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Source paper** | — |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The v2 library now emits final_confidence on every trajectory across all three conditions,
which unblocks paired calibration analysis. On t0023 (n>=157, sonnet), report per-condition
reliability diagrams (binned confidence vs empirical accuracy), Brier scores, and ECE in
addition to overconfident_error_rate. This will reveal whether the [0,1] field is actually
informative for the model or whether it collapses to a flat distribution near 0.7-0.9 (the
Xiong2024 haiku risk), and whether condition-vs-condition Metric 2 deltas reflect calibration
shifts or just accuracy shifts.

</details>

## Medium Priority

<details>
<summary>📚 <strong>Add Expected Calibration Error (ECE) computation alongside
overconfident_error_rate</strong> (S-0011-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

Extend the metric2_calibration_aggregator_v1 library (or add a sibling library) with Expected
Calibration Error (ECE) computation using the standard 10-bucket binning and produce
per-bucket calibration plots. Xiong2024 reports ECE as the primary headline metric; the
current library reports only the binary overconfident_error_rate. Adding ECE gives Phase 2 a
richer calibration signal and lets t0012's results display the bucket where overconfidence
concentrates rather than just a single number. Should be a small follow-up: bucket each
CalibrationRecord by predicted_confidence, compute |accuracy - mean_confidence| within each
bucket, weight by bucket size. Output should be both a scalar ECE value and a list of
(bucket_lower, bucket_upper, accuracy, mean_confidence, count) tuples for plotting.

</details>

<details>
<summary>📊 <strong>Substantive critic vs original prompt: 50-row prompt-only
ablation at fixed model</strong> (S-0019-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

Run a focused n=50 ablation that holds the judge model fixed at claude-sonnet-4-6 and varies
only the system prompt between the substantive critic (with simulate-execution instruction)
and the original t0014 prompt. The current task found a Cohen's kappa of 0.626 between the two
prompts on the same model, with one row (v2-haiku-0007) where the substantive prompt caught a
dimensional-analysis error the original prompt missed and two rows (v1-sonnet-0002,
v1-sonnet-0004) where the substantive prompt accepted structural-but-executable trees the
original rejected. A larger ablation would quantify how often each prompt mode wins, which
would inform whether the substantive critic should become the production judge or stay as a
stricter audit.

</details>

## Low Priority

<details>
<summary>📚 <strong>Add a JSON-mode fallback path to the confidence elicitation if
larger runs hit the 20% parse-failure gate</strong> (S-0021-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0021-03` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0021_plan_and_solve_v2_with_final_confidence`](../../../overview/tasks/task_pages/t0021_plan_and_solve_v2_with_final_confidence.md) |
| **Source paper** | — |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The smoke parse-failure rate on haiku is 0/3 on n=1 x 3, so the strict regex parser is fine
for haiku at this scale. However, if the t0023 sonnet run or any future larger run pushes the
parse-failure rate above the documented 20% gate (REQ-10), the library should fall back to
JSON-mode output (e.g., a tool-use call returning {confidence: 0.85}) instead of free-form
text. Implement this as an opt-in path so the existing two-call protocol stays the default and
the JSON fallback only activates when the model demonstrably cannot produce parseable output.
Keep the verbalized prompt as the canonical Xiong2024 §3.2 protocol.

</details>

<details>
<summary>🧪 <strong>Add provider-specific calibration prompt variants for
instruction-tuned vs reasoning models</strong> (S-0011-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

The current ConfidencePromptTemplate uses a single Xiong2024 human-inspired prompt.
Reasoning-focused models (e.g., o-series, Claude 4.5+ thinking models) often produce a
chain-of-thought before stating confidence, which the current parser handles but which
Xiong2024's own results show can hurt calibration in some configurations. Build a small
library of named prompt variants (instruction_tuned, reasoning_with_cot, reasoning_no_cot) and
benchmark them on a held-out 50-problem set during Phase 2. Goal: identify which variant
minimizes overconfident_error_rate per provider and ship that as the default mapping in
t0012's experiment harness. Out of scope for this task per task_description.md but identified
as the obvious next sweep.

</details>

<details>
<summary>🧪 <strong>Cross-vendor judge: replicate the schema-only delta with GPT-4
and Gemini judges</strong> (S-0019-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0019_v2_judge_calibration_sonnet`](../../../overview/tasks/task_pages/t0019_v2_judge_calibration_sonnet.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

Test the family-bias hypothesis at the judge stage by re-judging the same 55-row pool under
GPT-4o and Gemini-2.5 with the same substantive critic prompt, and comparing the schema-only
delta to the +24.6 / +37.3 pp Anthropic numbers from this task. Xiong2024 reports
within-family acceptance bonuses of 5-10 pp; if the cross-vendor schema-only delta lands close
to the substantive-sonnet +24.6 pp, the v2-sonnet familial bias hypothesis (kappa=1.0 on the
v2-sonnet cell) gains support; if it lands close to +37 pp, prompt strictness dominates over
model family.

</details>

<details>
<summary>📊 <strong>Multi-judge disagreement study on hierarchical
annotation</strong> (S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Run the same 12-row spot-check with two judge models (claude-haiku-4-5 + claude-sonnet-4-6)
and compute pairwise verdict agreement plus a confusion matrix. The v1 single-judge accept
rate of 33% may be miscalibrated; multi-judge agreement gives a more reliable quality
estimate. Estimated cost: ~$0.30 per run.

</details>

<details>
<summary>📊 <strong>Sweep HIGH_CONFIDENCE_THRESHOLD to find the operating point that
maximizes signal in t0012</strong> (S-0011-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0011_metric2_calibration_aggregator`](../../../overview/tasks/task_pages/t0011_metric2_calibration_aggregator.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0011_metric2_calibration_aggregator/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

The current default HIGH_CONFIDENCE_THRESHOLD = 0.75 sits between the verbalized medium (0.5)
and high (0.9) numeric anchor points and matches Xiong2024's high-bucket boundary. The
threshold is exposed as a module constant for sweeps. After t0012 runs, sweep the threshold
over {0.5, 0.6, 0.7, 0.75, 0.8, 0.9} and report overconfident_error_rate at each operating
point. The best threshold for the project's hierarchical agents may differ from Xiong2024's QA
setting because the project judges actions at trajectory steps, not final answers. Output: a
small chart and a recommended threshold for downstream tasks.

</details>

## Closed

<details>
<summary>✅ <s>Add an ablation: tree-schema-with-truncated-text to isolate the
truncation fix from the schema upgrade</s> — covered by <a
href="../../../tasks/t0020_v2_truncation_vs_schema_ablation/"><code>t0020_v2_truncation_vs_schema_ablation</code></a>
(S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0009_hierarchical_annotation_v2`](../../../overview/tasks/task_pages/t0009_hierarchical_annotation_v2.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0009_hierarchical_annotation_v2/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/) |

v2 changed two things at once: schema (flat -> tree) and text completeness (truncated 1500
chars -> full). On FrontierScience-Olympiad and WorkArena++ the +67% and +100% deltas could be
entirely from the truncation fix (Xiong2024's prediction) or entirely from the schema upgrade.
Run a third condition: the v2 tree schema but truncate the problem to 1500 chars in both the
annotator and judge prompts. If accept rate drops materially below v2-full-text on
FrontierScience-Olympiad, truncation is the dominant cause; if it stays at v2-full-text
levels, the schema is the dominant cause. Cost ~$2 with haiku.

</details>

<details>
<summary>✅ <s>Implement verbalized-confidence + 3-sample self-consistency aggregator
for Metric 2</s> — covered by <a
href="../../../tasks/t0011_metric2_calibration_aggregator/"><code>t0011_metric2_calibration_aggregator</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Xiong2024 establishes that single-sample verbalized confidence is poorly calibrated and that
3-sample self-consistency aggregation reduces ECE by 2-8 points. The project should commit to
this protocol for Metric 2 (overconfident error rate). This task would specify the
human-inspired confidence prompt template (low/medium/high + brief justification), implement
the self-consistency aggregator, and validate calibration on a small held-out set before Phase
2 launches.

</details>

<details>
<summary>✅ <s>Re-run LLM-as-judge with full problem text (no truncation)</s> —
covered by <a
href="../../../tasks/t0009_hierarchical_annotation_v2/"><code>t0009_hierarchical_annotation_v2</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2306.13063`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2306.13063/) |
| **Categories** | [`uncertainty-calibration`](../../../meta/categories/uncertainty-calibration/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/) |

The v1 judge sees only the first 1500 chars of each problem. Three of four needs-revision
verdicts on FrontierScience-Olympiad rows complain about content not present in the truncated
excerpt. Re-run the audit using the full problem text (or a structured per-section summary)
and compare accept rates. Predict an absolute accept-rate increase of >=15 percentage points
on FrontierScience-Olympiad.

</details>
