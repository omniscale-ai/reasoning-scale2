# Suggestions: `benchmark-swebench`

5 suggestion(s) in category
[`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) **4 open** (3 medium, 1
low), **1 closed**.

[Back to all suggestions](../README.md)

---

## Medium Priority

<details>
<summary>📚 <strong>Build benchmark-specific tool registries for the four roadmap
benchmarks</strong> (S-0006-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0006-01` |
| **Kind** | library |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0006_scope_aware_react_library`](../../../overview/tasks/task_pages/t0006_scope_aware_react_library.md) |
| **Source paper** | — |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`benchmark-workarena`](../../../meta/categories/benchmark-workarena/), [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/), [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) |

scope_aware_react_v1 accepts an arbitrary tool_registry but ships none. Phase 2 needs
registries for FrontierScience-Olympiad (calculator, search, paper lookup), WorkArena++
(browser, form filler, table lookup), SWE-bench Verified (file read, file write, run tests,
git diff), and tau-bench (DB query, API call, customer-action stubs). Each should be its own
write-library task that imports scope_aware_react_v1 and registers a registry with consistent
naming conventions.

</details>

<details>
<summary>📂 <strong>Build the SWE-bench Verified Docker harness</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`no-doi_OpenAI2024_swe-bench-verified`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/no-doi_OpenAI2024_swe-bench-verified/) |
| **Categories** | [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |

SWE-bench Verified [OpenAI2024] is the canonical atomic-execution slot in the four-source
composite. Its evaluation harness uses Docker per repository to isolate test runs. This task
would download the Verified problem set, pull the Docker images, and run a 10-instance smoke
test to confirm the harness reproduces published baseline numbers (e.g., one of the early
Claude or GPT scores).

</details>

<details>
<summary>📊 <strong>Sensitivity-check the SWE-bench Verified 4-8-hunks subset against
[3, 12]</strong> (S-0003-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`no-doi_OpenAI2024_swe-bench-verified`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/no-doi_OpenAI2024_swe-bench-verified/) |
| **Categories** | [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |

The current SWE-bench Verified subset filters to 60 instances with exactly 4-8 patch hunks.
The full 500 Verified instances have hunks ranging from 1 to 45. Run a sensitivity check by
re-filtering with windows [3, 12] and [2, 16] and comparing the difficulty / repo
distributions; this informs whether the 4-8 boundary is too narrow for Phase 2's atomic-edit
experiments.

</details>

## Low Priority

<details>
<summary>🧪 <strong>Truncation-budget sweep to map the marginal value of additional
context</strong> (S-0020-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0020_v2_truncation_vs_schema_ablation`](../../../overview/tasks/task_pages/t0020_v2_truncation_vs_schema_ablation.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) |

t0020 shows 1500 chars is sufficient on 3 of 4 benchmarks but loses ~17 pp on SWE-bench
Verified. A finer truncation grid (500 / 1000 / 1500 / 2500 / 5000 / full) on a
SWE-bench-heavy pool would map where the marginal value of additional context drops to zero.
This is a single-condition sweep (v2 schema held constant; only the truncation budget varies)
so the cost scales linearly with the number of budget points. Estimated cost: 6 budgets x 20
SWE-bench rows x 2 calls per row x ~$0.07 = ~$17.

</details>

## Closed

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
