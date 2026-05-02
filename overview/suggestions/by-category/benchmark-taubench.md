# Suggestions: `benchmark-taubench`

3 suggestion(s) in category
[`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) **3 open** (3 medium).

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
<summary>📊 <strong>Register pass^k as a project metric for reliability
reporting</strong> (S-0002-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2406.12045`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/) |
| **Categories** | [`agent-evaluation`](../../../meta/categories/agent-evaluation/), [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/) |

tau-bench [Yao2024] introduces pass^k, a metric that measures whether an agent succeeds across
k independent rollouts. The 25-percentage-point gap between pass@1 and pass^8 in retail
demonstrates that single-rollout pass@1 systematically overstates agent reliability. The
project should register a pass_at_k metric (with k=1, 8) under meta/metrics/ to complement
task_success_rate. This enables Phase 4 paper-ready claims to be robust to single-rollout
luck.

</details>

<details>
<summary>📊 <strong>Wire a real Tau-bench tool registry to escape the harness
floor</strong> (S-0026-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0026_phase2_abc_runtime_n147_for_rq1_rq5`](../../../overview/tasks/task_pages/t0026_phase2_abc_runtime_n147_for_rq1_rq5.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Tau-bench numbers in this sweep are a harness floor, not a benchmark score: A=0.0%, B=2.3%,
C=10.3% on a stub python_exec only. Port the published Tau-bench retail/airline tool stack (or
a minimal viable subset) into the harness and rerun the A/B/C grid on the Tau-bench subset
(n=87). The Tau-bench leg of the comparison currently dominates the absolute-rate gap with
literature.

</details>
