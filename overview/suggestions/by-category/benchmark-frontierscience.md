# Suggestions: `benchmark-frontierscience`

9 suggestion(s) in category
[`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) **7 open**
(1 high, 3 medium, 3 low), **2 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📂 <strong>Negotiate FrontierMath access via Epoch AI evaluation
pipeline</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

FrontierMath [Glazer2024] uses contamination-resistant unpublished problems hosted via Epoch
AI's evaluation pipeline; the raw problems are not publicly downloadable. The project needs an
explicit access conversation with Epoch AI, plus a fallback to public Olympiad benchmarks
(MATH-500, AIME) if access is denied or delayed. Schedule this as a planning task before Phase
1 to avoid blocking the FrontierScience-Olympiad slot of the composite benchmark.

</details>

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
<summary>🧪 <strong>Derive step graphs for FrontierScience-Olympiad rows</strong>
(S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`hierarchical-planning`](../../../meta/categories/hierarchical-planning/) |

FrontierScience-Olympiad pilot rows currently lack per-instance step graphs because Olympiad
solutions are graded as final answers. Run a hierarchical-annotation task that decomposes each
problem into global / subtask / atomic steps with gold actions at each level, so Phase 2 can
apply the canonical 4-8 decisions filter consistently across all four benchmarks.

</details>

<details>
<summary>📂 <strong>Negotiate Epoch AI access for full FrontierMath
benchmark</strong> (S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0003_download_benchmark_subsets`](../../../overview/tasks/task_pages/t0003_download_benchmark_subsets.md) |
| **Source paper** | [`10.48550_arXiv.2411.04872`](../../../tasks/t0003_download_benchmark_subsets/assets/paper/10.48550_arXiv.2411.04872/) |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

FrontierMath (Glazer et al. 2024) is the closest publicly named analogue to
FrontierScience-Olympiad and is gated behind Epoch AI access. The current dataset asset uses
40 pilot rows as the v0 subset. Open a conversation with Epoch AI to obtain bona-fide research
access; if access is denied or delayed, add MATH-500 / AIME as a public Olympiad fallback per
the t0002 fallback plan.

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
<summary>🧪 <strong>Re-run the three FrontierScience-Olympiad sonnet timeouts under a
longer CLI timeout to recover the missing rows</strong> (S-0014-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0014_v2_annotator_sonnet_rerun`](../../../overview/tasks/task_pages/t0014_v2_annotator_sonnet_rerun.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-annotation`](../../../meta/categories/benchmark-annotation/), [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/) |

Three FrontierScience-Olympiad rows (pilot indices 7, 8, 14) timed out at the 300s Claude Code
CLI ceiling during the sonnet annotation pass. They were dropped from the judge sample,
reducing FS sample size from 6 (t0009 v2-haiku) to 3 (t0014 v2-sonnet). The +33 pp model-only
delta on FS (67% v2-haiku vs 100% v2-sonnet, n=6 vs n=3) is therefore on a smaller sample than
the other benchmarks. Re-run those three rows with a 600s or 900s CLI timeout (or via direct
Anthropic API which has no per-call wall-clock cap) and re-judge. If all three pass, FS
aggregate v2-sonnet stays at 100% on n=6 and the +33 pp model-only delta becomes more
credible. Cost <$1.

</details>

<details>
<summary>📊 <strong>Tighten FrontierScience-Olympiad subgoal lists by hand on a
5-task pilot before t0023</strong> (S-0022-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0022_abc_harness_progress_rate_and_error_taxonomy`](../../../overview/tasks/task_pages/t0022_abc_harness_progress_rate_and_error_taxonomy.md) |
| **Source paper** | — |
| **Categories** | [`benchmark-frontierscience`](../../../meta/categories/benchmark-frontierscience/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |

Current FrontierScience-Olympiad subgoals are derived mechanically from SUBTASK lines in t0012
gold answers (mean 4.6 per environment). On the 89-row replay, 73 of 89 trajectories scored
0.0 progress rate, suggesting the subgoals may be too coarse to register intermediate
progress. Hand-review subgoals for 5 randomly chosen environments, refining them into 3-5
verifiable intermediate states each (e.g., "derived intermediate equation X", "identified
relevant principle Y"). If hand-tightening doubles the non-zero rate, roll the recipe out to
all 26 environments before t0023 ships. Cheap and high-leverage for t0023 signal quality.

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
