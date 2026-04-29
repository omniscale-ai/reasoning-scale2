# Suggestions: `benchmark-swebench`

2 suggestion(s) in category
[`benchmark-swebench`](../../../meta/categories/benchmark-swebench/) **2 open** (1 high, 1
medium).

[Back to all suggestions](../README.md)

---

## High Priority

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

## Medium Priority

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
