# Suggestions: `granularity-conditioning`

28 suggestion(s) in category
[`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) **21 open**
(4 high, 10 medium, 7 low), **7 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>🧪 <strong>Phase 2 A-vs-B-vs-C evaluation harness</strong> (S-0007-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0007_scope_unaware_planandsolve_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Build the experiment harness that runs all three libraries (scope_aware_react_v1,
scope_unaware_planandsolve_v1, and the planned matched-mismatch library) on a fixed benchmark
slice with a single shared LLM provider, recording trajectory_records.jsonl per condition and
computing the registered metrics task_success_rate, avg_decisions_per_task, and
overconfident_error_rate per condition. The harness must depend on this library only via the
trajectory schema, never via internal helpers, to preserve isolation.

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
<summary>🧪 <strong>Reframe the matched-mismatch wrapper so C is structurally
distinct from A</strong> (S-0026-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Variant C beat B (paired McNemar p = 0.019) but only because the 'adversarial' wrapper
delegates to scope_aware_react with a perturbed strategy label, making C structurally
A-with-noise rather than B-with-extra-degradation. Redesign the matched-mismatch interface so
the adversarial variant operates on top of B's plan-and-solve scaffold, not A's, then re-run
the B vs C pair on the same paired set to test whether the inversion survives.

</details>

<details>
<summary>🧪 <strong>Use hierarchical-annotation-v1 to seed Phase 2 scope-conditioning
experiments</strong> (S-0005-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0005_hierarchical_annotation_pilot_v1`](../../../overview/tasks/task_pages/t0005_hierarchical_annotation_pilot_v1.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0005_hierarchical_annotation_pilot_v1/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The dataset asset is now ready for downstream consumption. Plan a baseline-evaluation task
that uses the 102 hierarchy-complete rows to compare scope-conditioned vs scope-unaware agent
prompts (B vs G/S/A from the project's research questions).

</details>

## Medium Priority

<details>
<summary>🧪 <strong>Add a uniform-random vs. adversarial vs. matched ablation to
t0012</strong> (S-0010-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0010_matched_mismatch_library/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

When t0012 runs the A-vs-B-vs-C harness, include three C-condition variants in addition to A
and B: matched_mismatch_v1 with mismatch_strategy='random' and seed=0, matched_mismatch_v1
with mismatch_strategy='adversarial', and a phase-randomised C control (random walk over the
v2 hierarchy with the correct tag). The three-way ablation decomposes the C-condition gap into
'phase order matters', 'any wrong tag matters', and 'most-distant wrong tag matters',
preventing the granularity-mismatch effect from being conflated with a step-order-mismatch
effect (see research_papers.md, Wang2023 and Zhou2022).

</details>

<details>
<summary>📊 <strong>Adopt AgentBoard progress-rate as a secondary RQ1 metric
alongside binary task success</strong> (S-0025-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0025-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Source paper** | [`10.48550_arXiv.2401.13178`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/assets/paper/10.48550_arXiv.2401.13178/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Ma2024 (AgentBoard) shows that pairs of models with identical binary success rates differ by
up to 5.7 progress-rate points (Llama2-13b vs Mistral-7b), revealing differences invisible in
success-only evaluation. Add progress-rate as Metric 1b for every Phase 2 A/B/C run so that
even runs that tie on success surface granularity-conditioning differences in mid-trajectory
behaviour.

</details>

<details>
<summary>📂 <strong>Fix task_id collision in FrontierScience-Olympiad pilot
dataset</strong> (S-0012-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-04` |
| **Kind** | dataset |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

The hierarchical-annotation-v2 FrontierScience-Olympiad subset has 40 rows but only 26 unique
task_ids. Multiple rows share the same task_id (different granularity levels of the same
problem), which means the pairing logic treats them as separate predictions for the same task.
A deduplication or re-keying correction task should produce a version of the dataset with
unique task_ids per row, or document the intended semantics of multi-row task_ids.

</details>

<details>
<summary>📂 <strong>Fix task_id collision in FrontierScience-Olympiad pilot
dataset</strong> (S-0012-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-04` |
| **Kind** | dataset |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

The hierarchical-annotation-v2 FrontierScience-Olympiad subset has 40 rows but only 26 unique
task_ids. Multiple rows share the same task_id (different granularity levels of the same
problem), which means the pairing logic treats them as separate predictions for the same task.
A deduplication or re-keying correction task should produce a version of the dataset with
unique task_ids per row, or document the intended semantics of multi-row task_ids.

</details>

<details>
<summary>🧪 <strong>Give matched_mismatch a structurally distinct adversarial
behavior, not just a v3 delegation</strong> (S-0027-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0027_phase2_5_abc_rerun_with_fixed_b_and_c`](../../../overview/tasks/task_pages/t0027_phase2_5_abc_rerun_with_fixed_b_and_c.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

matched_mismatch_v2 now delegates to plan_and_solve_v3 instead of A's scope_aware_react (the
structural fix this task implemented), but C and B agree on 125 of 130 paired outcomes
(discordant 4/5, McNemar p=1.0). C is effectively B-with-a-perturbed-strategy-label — the
adversarial signal is too weak to move the success rate. Redesign the wrapper to inject a
meaningfully different scaffold over v3: either a self-consistency vote across 3 sampled
plans, a chain-of-thought decomposition over the plan steps, or an explicit adversarial
critique loop before the action stage. Re-run B vs C on the same paired set to test whether a
stronger structural difference produces a discordance pattern that can move McNemar.

</details>

<details>
<summary>📊 <strong>Measure the missing-tag fallback rate against real LLMs</strong>
(S-0006-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The library defaults to atomic when the model omits a granularity tag and emits a
tag_missing_defaulted_to_atomic warning observation. The deterministic tests cover the parser
path but the fallback rate against real LLMs (GPT-4o, Claude 3.7 Sonnet, Llama-3.1-70B) is
unknown. Build an evaluation task that runs each library at each granularity over N=20
problems per benchmark and reports the fallback rate alongside task success.

</details>

<details>
<summary>📚 <strong>Per-step strategy override for matched_mismatch_v1</strong>
(S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Extend matched_mismatch_v1 with a per-step strategy override so callers can inject targeted
mismatches in specific phases (e.g., wrong-tag only at the global level; correct everywhere
else). This decomposes the C-condition gap by phase kind and supports follow-up analysis on
which structural slots are most sensitive to tag mismatch. Should be additive: the existing
uniform-strategy API stays the default. Keep the trajectory schema unchanged; the override is
constructor-side only.

</details>

<details>
<summary>🧪 <strong>Phase 2 three-arm A/B/C pilot at half scale to test the
strict-double-inequality form of RQ5</strong> (S-0025-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0025-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Source paper** | [`10.48550_arXiv.2405.15821`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/assets/paper/10.48550_arXiv.2405.15821/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Wen2024 NTPO is the only paper that directly observes a mismatched-scope condition
underperforming both baselines, but it is in the RL fine-tuning regime, not prompting. To test
RQ5's strict double inequality (C < both A and B) under our prompting framing, run all three
arms on a half-scale (15-instance) subset of the composite benchmark, ~$15-20. Lower-priority
than S-0025-01 because RQ5 is a sub-hypothesis and the strict form is the most expensive to
falsify.

</details>

<details>
<summary>📊 <strong>Schema-parity dedup task between t0006 and t0007</strong>
(S-0007-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

After t0006 (scope_aware_react_v1) merges, run a small deduplication-style task that imports
both libraries' TRAJECTORY_RECORD_FIELDS tuples and asserts they are identical, plus a smoke
test that runs both libraries on the same toy problem and verifies the trajectory JSON shapes
round-trip through a single Pydantic loader. If they diverge, file a correction in the
later-merged task. This is the cheapest insurance against silent schema drift.

</details>

<details>
<summary>🔧 <strong>Use SELF-DISCOVER reasoning scaffolds as the scope-aware (A)
condition prompt template</strong> (S-0017-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-03` |
| **Kind** | technique |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2402.03620`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2402.03620/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

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

## Low Priority

<details>
<summary>🧪 <strong>Add tool use (search, code execution) to the smoke harness for
FrontierScience-Olympiad</strong> (S-0012-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

The smoke ran with calculator+finish only. FrontierScience-Olympiad requires multi-step
numerical computation, retrieval, and code execution for most problems. Adding a Python code
execution tool and a retrieval tool would lift accuracy above the current floor and make
A-vs-B-vs-C differences observable even on haiku. Cost per row would increase by ~2-5x but
confirmatory N would decrease proportionally.

</details>

<details>
<summary>🧪 <strong>Defer Reflexion-style episodic memory to a Phase 3
ablation</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2303.11366`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2303.11366/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Reflexion [Shinn2023] adds verbal self-reflection across trials and reaches 91% pass@1 on
HumanEval vs. 80% for vanilla GPT-4. Including episodic memory in Phase 2 would conflate scope
conditioning with cross-trial memory. Schedule a dedicated Phase 3 ablation that tests whether
Reflexion-style memory adds further gains on top of the scope-aware (A) condition established
in Phase 2.

</details>

<details>
<summary>🔧 <strong>Extend the library to support a granularity that varies within
a single run</strong> (S-0006-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-05` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Currently ScopeAwareReactAgent takes one fixed granularity for an entire run. A natural
extension is to let the agent emit a granularity transition (e.g., start global, drop to
subtask once a plan is established, drop to atomic during execution). Add a model-driven mode
where the parser also accepts <transition_to:subtask> markers and the agent updates the active
granularity per turn. This is a research extension worth Phase 2 ablation.

</details>

<details>
<summary>🧪 <strong>Investigate group-level (subtask-level) DPO as an alternative to
A/B/C prompting for granularity conditioning</strong> (S-0025-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0025-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0025_lit_survey_hierarchical_agents_and_judges_2024_2026`](../../../overview/tasks/task_pages/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026.md) |
| **Source paper** | [`no-doi_Gao2026_hierarchical-preference-learning-llm-agents`](../../../tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/assets/paper/no-doi_Gao2026_hierarchical-preference-learning-llm-agents/) |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/) |

Gao2026 HPL ablates trajectory-, step-, and group-level DPO and isolates the group-level term
as the primary driver of the +3.97 abs gain over IPR on Qwen2.5-7B. The group level
corresponds exactly to the project's mid-granularity (subtask) annotation layer. If Phase 2
A/B/C prompting shows weak runtime gains, the next experiment should be a small-scale
group-level DPO fine-tune on the v2-tree annotated subset, comparing to a flat-DPO baseline.
Defer until after Phase 2 is complete and budget is reassessed.

</details>

<details>
<summary>🧪 <strong>Multi-provider replication: run Phase 2 harness with GPT-4o and
Gemini 1.5 Pro</strong> (S-0012-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The smoke used only claude-haiku-4-5. Replicating on GPT-4o and Gemini 1.5 Pro (both now
available via project API keys) would test whether the granularity conditioning effect is
model-specific or generalizes across providers. The harness's model_call.py abstraction layer
makes this a configuration change rather than a code change. Defer until the confirmatory N
result is available from S-0012-02 to avoid spending budget before the primary hypothesis is
tested.

</details>

<details>
<summary>📊 <strong>Resolve the subtask-adversarial ambiguity with empirical
evidence</strong> (S-0010-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0010_matched_mismatch_library`](../../../overview/tasks/task_pages/t0010_matched_mismatch_library.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

ADVERSARIAL_MAP currently pins 'subtask -> atomic' because subtask is equidistant from global
and atomic. Run a small ablation in t0012 with both 'subtask -> atomic' and 'subtask ->
global' adversarial maps and report the per-step contribution. If the two choices differ
materially, document the chosen direction and the empirical justification in
matched_mismatch_v1's description.md. If they do not differ, lock the current choice and
remove the ambiguity note.

</details>

<details>
<summary>🧪 <strong>Run t0023's confirmatory ABC re-run with N>=157 using
abc_harness_metrics</strong> (S-0022-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The whole purpose of t0022 is to make t0023's confirmatory N>=157 ABC re-run produce signal at
the floor where binary task success failed in t0012. Schedule t0023 to consume
abc_harness_metrics: import score_trajectory, log per-trajectory progress_rate and per-step
error labels into the existing harness output, and report progress-rate means and
error-distribution mixtures per ABC condition with bootstrap CIs. Reuse the cached judge
responses from t0022 to keep marginal cost low. This is the direct downstream consumer this
task was built for.

</details>

## Closed

<details>
<summary>✅ <s>Adopt AgentBoard progress-rate metric and EAI error taxonomy in the
next ABC-condition run</s> — covered by <a
href="../../../tasks/t0022_abc_harness_progress_rate_and_error_taxonomy/"><code>t0022_abc_harness_progress_rate_and_error_taxonomy</code></a>
(S-0017-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0017_literature_hierarchical_agents_and_judges`](../../../overview/tasks/task_pages/t0017_literature_hierarchical_agents_and_judges.md) |
| **Source paper** | [`10.48550_arXiv.2401.13178`](../../../tasks/t0017_literature_hierarchical_agents_and_judges/assets/paper/10.48550_arXiv.2401.13178/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

t0012's smoke showed that all three ABC conditions hit the floor on FrontierScience-Olympiad
with claude-haiku-4-5 (A: 2.5%, B: 0%, C: 0%), so binary task success cannot distinguish the
conditions. Ma2024 (AgentBoard, NeurIPS 2024 D&B) defines a subgoal-coverage "progress rate"
with Pearson rho > 0.95 against humans across 1013 environments; Li2024 (Embodied Agent
Interface, NeurIPS 2024) defines a fine-grained error taxonomy (hallucination, affordance,
missing/extra/wrong-order steps, precondition/effect errors) that attributes failures to
specific modes. Adopt both: progress rate becomes a stronger Metric 1 candidate than binary
success, and the EAI taxonomy becomes the per-row diagnostic when scope-aware (A) and
scope-mismatched (C) conditions diverge. This is a precondition for S-0012-02 (sonnet
confirmatory run) producing legible results. Estimated effort: 1-2 days of
metric-implementation work.

</details>

<details>
<summary>✅ <s>Confirmatory Phase 2 run: sonnet on SWE-bench Verified or
tau-bench</s> — covered by <a
href="../../../tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/"><code>t0023_phase2_abc_confirmatory_sonnet_swebench</code></a>
(S-0012-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |

The smoke shows FrontierScience-Olympiad is beyond haiku capacity without tools (A: 2.5%, B:
0%, C: 0%). All three conditions are at the floor, making granularity conditioning effects
invisible. A confirmatory run requires: (1) a benchmark where the model can achieve 10-50%
accuracy without tools (SWE-bench Verified lite or tau-bench at the instance level), (2)
claude-sonnet-4-6 instead of haiku, (3) N≥157 paired rows per the confirmatory-N estimate from
this smoke. This is the highest-priority next experiment for RQ1/RQ5.

</details>

<details>
<summary>✅ <s>Extend scope_unaware_planandsolve_v1 to emit final_confidence</s> —
covered by <a
href="../../../tasks/t0021_plan_and_solve_v2_with_final_confidence/"><code>t0021_plan_and_solve_v2_with_final_confidence</code></a>
(S-0012-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-01` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0012_phase2_abc_smoke_frontierscience`](../../../overview/tasks/task_pages/t0012_phase2_abc_smoke_frontierscience.md) |
| **Source paper** | — |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

The t0007 Plan-and-Solve library does not emit a final_confidence field in trajectory records.
This collapses Metric 2 (overconfident_error_rate) to 0.0 for conditions B and C, making RQ2
untestable. Extend the library to emit a verbalized confidence label per the Xiong2024 §3.2
protocol: add a follow-up call after the final plan step asking the model to rate its
confidence on a 0-1 scale. This is a prerequisite for any confirmatory A-vs-B-vs-C run that
wants to test RQ2.

</details>

<details>
<summary>✅ <s>Implement matched-mismatch (C) library on top of
scope_unaware_planandsolve_v1</s> — covered by <a
href="../../../tasks/t0010_matched_mismatch_library/"><code>t0010_matched_mismatch_library</code></a>
(S-0007-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0007_scope_unaware_planandsolve_library`](../../../overview/tasks/task_pages/t0007_scope_unaware_planandsolve_library.md) |
| **Source paper** | — |
| **Categories** | [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/), [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Create a third agent library that wraps scope_unaware_planandsolve_v1 (or
scope_aware_react_v1) with a tag-classifier that retroactively labels each step's granularity,
producing the matched-mismatch (C) condition for the project's A-vs-B-vs-C comparison. Reuse
this task's TRAJECTORY_RECORD_FIELDS export so all three libraries share the same trajectory
schema. The classifier should be a small fine-tuned model or heuristic so the task is
local-only and deterministic.

</details>

<details>
<summary>✅ <s>Implement Plan-and-Solve as the canonical scope-unaware (B)
baseline</s> — covered by <a
href="../../../tasks/t0007_scope_unaware_planandsolve_library/"><code>t0007_scope_unaware_planandsolve_library</code></a>
(S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2305.04091`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

Plan-and-Solve [Wang2023] is the strongest published prompt-only baseline that does not
condition on explicit granularity tags. The project should reuse LangChain's Plan-and-Execute
implementation rather than reimplementing from scratch. This task would adapt the LangChain
implementation to the project's task harness, log both stages (plan and solve) separately, and
produce a 10-instance validation run on the composite benchmark to confirm the baseline beats
vanilla Zero-shot-CoT.

</details>

<details>
<summary>✅ <s>Implement scope-aware (A) as ReAct extended with explicit granularity
tags</s> — covered by <a
href="../../../tasks/t0006_scope_aware_react_library/"><code>t0006_scope_aware_react_library</code></a>
(S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | technique |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

The scope-aware (A) condition can be implemented as ReAct [Yao2022] extended with a per-token
granularity tag from the set {global, subtask, atomic}. This task would specify the prompt
template per granularity, the tagging logic that decides which granularity is active at each
LLM call, and a logging schema that records the active granularity for every action so
post-hoc per-granularity analysis is possible. Replicate Least-to-Most's solution-reuse
pattern [Zhou2022] inside the implementation.

</details>

<details>
<summary>✅ <s>Run the A-vs-B-vs-C Phase 2 experiment on the FrontierScience
subset</s> — covered by <a
href="../../../tasks/t0012_phase2_abc_smoke_frontierscience/"><code>t0012_phase2_abc_smoke_frontierscience</code></a>
(S-0006-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | [`10.48550_arXiv.2210.03629`](../../../tasks/t0006_scope_aware_react_library/assets/paper/10.48550_arXiv.2210.03629/) |
| **Categories** | [`granularity-conditioning`](../../../meta/categories/granularity-conditioning/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

scope_aware_react_v1 (A) and the in-progress scope_unaware_planandsolve_v1 (B) are now ready
as substrates. Run a controlled experiment on the t0003 FrontierScience subset with both
libraries plus a no-prompt-engineering baseline (C), measuring task_success_rate,
overconfident_error_rate, and avg_decisions_per_task across N=50 problems. Expected effect
size: +5 to +15 absolute success rate for A over B based on the Yao2022 ALFWorld result
anchor.

</details>
