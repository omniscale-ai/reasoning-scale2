# Results Summary: Literature Survey on Granularity Conditioning and Hierarchical Agents

## Summary

Completed a literature survey of 11 papers covering granularity / scope conditioning of LLM agents,
hierarchical task decomposition, uncertainty calibration, and the four roadmap benchmarks
(FrontierScience-Olympiad, WorkArena++, SWE-bench Verified, tau-bench). All 11 paper assets pass the
v3 paper-asset verificator and are tagged with project categories.

## Metrics

* **11 paper assets created** out of a 10-paper minimum target — exceeds REQ-1 by one paper.
* **4 of 4 survey threads covered** with at least 2 papers each: granularity / hierarchical
  prompting (Yao2022, Wang2023, Shinn2023, Zhou2022, Wei2022 noted but not added in this round — 4
  added), four roadmap benchmarks (Glazer2024, Drouin2024, Boisvert2024, Jimenez2024, OpenAI2024,
  Yao2024 — 6 added), calibration (Xiong2024 — 1 added).
* **0 errors** across 11 verificator runs; 1 minor warning (PA-W007 missing-country) on the first
  paper, fixed by adding country codes.

## Verification

* `verify_paper_asset` — PASSED zero-errors on all 11 papers.
* `verify_research_papers` — PASSED with 1 word-count warning (resolved).
* `verify_research_internet` — PASSED with zero errors and zero warnings.
* `verify_research_code` — PASSED with zero errors and zero warnings.
* `verify_plan` — PASSED with zero errors and zero warnings.
* `aggregate_papers --format ids` — confirms 11 paper IDs visible in the corpus.

## Synthesis: Thread-by-Thread Takeaways

### Thread A — Granularity / scope conditioning of LLM agents

Three foundational prompting papers establish that explicit decomposition into subtasks improves
multi-step reasoning. ReAct [Yao2022] introduces the canonical think-vs-act split with **+34
absolute** gain on ALFWorld and **+10 abs** on WebShop — the conceptual ancestor of the project's
three-level granularity schema. Plan-and-Solve [Wang2023] is the strongest published scope-unaware
(B) baseline candidate, achieving comparable performance to 8-shot manual CoT on GSM8K with no
exemplars. Reflexion [Shinn2023] extends ReAct with verbal self-reflection across trials and reaches
**91% pass@1 on HumanEval** vs. 80% for vanilla GPT-4 — a Phase 3 ablation candidate, not Phase 2
baseline (cross-trial memory would conflate scope with episodic memory).

**Decision for Phase 2**: Adopt Plan-and-Solve [Wang2023] as the canonical scope-unaware (B)
baseline; implement scope-aware (A) as a ReAct extension with explicit per-token granularity tags
(`{global, subtask, atomic}`); defer Reflexion to Phase 3.

### Thread B — Hierarchical task decomposition

Least-to-Most prompting [Zhou2022] provides the strongest empirical anchor for the scope-aware
condition's expected effect size: **>=99% on SCAN length-split** with 14 exemplars vs. **16% with
vanilla CoT** — a **+83 absolute** gain. The ReAct, Plan-and-Solve, and Reflexion papers
[Yao2022, Wang2023, Shinn2023] all use a two-tier hierarchy that the project's three-tier schema
strictly refines.

**Decision for Phase 2**: Replicate Least-to-Most's solution-reuse pattern (each subproblem uses
prior solutions in its context) inside the scope-aware (A) implementation. Pure decomposition
without solution-reuse loses much of LtM's gain. Set the +5-to-+15 absolute target on the
four-source composite as conservative against LtM's +83 SCAN gain.

### Thread C — Uncertainty calibration / overconfident error rate

Xiong2024 is the **canonical calibration reference**. It benchmarks black-box confidence elicitation
across 5 LLMs and 5 datasets and finds (a) LLMs are systematically overconfident, (b)
self-consistency aggregation across multiple samples beats single-sample by **+2 to +8 ECE points**,
(c) larger models calibrate better, (d) human-inspired prompting ("low / medium / high with
justification") outperforms numeric confidence on most tasks.

**Decision for Phase 2**: Adopt verbalized confidence + 3-sample self-consistency aggregation as the
operational definition of Metric 2. Define overconfident error as
`incorrect AND verbalized_confidence in {high, p>=0.8}`. Report bucketed ECE plots (10 bins)
alongside every Metric 2 number. Use the human-inspired prompt for confidence elicitation in the
scope-aware (A) condition.

### Thread D — The four roadmap benchmarks

The four benchmarks span a wide difficulty range that requires **stratified per-source reporting**
of all three project metrics:

| Benchmark | Headline | Achievable today | Project role |
| --- | --- | --- | --- |
| FrontierMath [Glazer2024] | <2% SOTA at release | low single-digit | global / strategic planning |
| WorkArena [Drouin2024] | GPT-4 42.7%, Llama3-70B 17.9% | 30-50% | atomic web actions (sanity check) |
| WorkArena++ [Boisvert2024] | "considerable gap" | depends on skill axis | mid-level subtask planning + reasoning |
| SWE-bench [Jimenez2024] | Claude 2 1.96% (parent) | far higher on Verified | atomic patch generation |
| SWE-bench Verified [OpenAI2024] | Claude Mythos Preview 93.9% (Apr 2026) | 80-95% | curated atomic execution |
| tau-bench [Yao2024] | gpt-4o <50% pass@1, pass^8 <25% retail | <50% | request-vs-act discrimination |

**Decision for Phase 2**: Use SWE-bench Verified (500 instances) instead of full SWE-bench (2,294
instances). Use WorkArena++ as the primary test bed for sub-hypothesis 1 (atomic-vs-compositional
gap). Adopt tau-bench's pass^k metric as the project's reliability indicator alongside Metric 1.
Plan an Epoch AI access conversation for FrontierMath; have a fallback to public Olympiad benchmarks
(MATH-500, AIME) if access is delayed.

## Cross-Cutting Findings

* **The atomic-vs-compositional gap is the project's main lever**. WorkArena++'s 682 compositional
  tasks built from 33 WorkArena atomic operations are the cleanest empirical instantiation of this
  gap [Boisvert2024]. Sub-hypothesis 1 — "gains concentrated in states where local execution
  requires information not needed for higher-level planning" — should be tested primarily on
  WorkArena++.
* **Verbalized confidence is the dominant calibration signal but unreliable single-sample**. The
  literature converges on self-consistency aggregation across 3+ samples [Xiong2024]. Phase 2 must
  commit to this protocol.
* **Reliability matters as much as capability**. tau-bench's pass^k metric exposes the gap between
  agents that *can* solve a task and agents that *reliably* solve it [Yao2024]. The project's Phase
  4 paper-ready report should report both pass@1 and pass^k for headline claims to be robust to
  single-rollout luck.
* **Effect-size targets**: A **+5 to +15 absolute** improvement on Phase 2 metrics for scope-aware
  (A) over scope-unaware (B) is conservative against the literature's strongest references (ReAct's
  +34 abs on ALFWorld, LtM's +83 abs on SCAN).
* **No prior work explicitly compares scope-aware vs. scope-mismatched agents** on a multi-step
  composite benchmark. The project's three-condition (A/B/C) experiment is genuinely novel; the
  literature has analogues for A vs. B (decomposition prompts) but not for the C (mismatch) control.

## Follow-Up Suggestions

These feed into the suggestions stage (`results/suggestions.json`):

1. Register `pass_at_k` (k=1, 8) as a project metric to complement `task_success_rate`.
2. Schedule a dedicated task to download the FrontierMath problem-set sample (or a fallback Olympiad
   set) and the SWE-bench Verified Docker images.
3. Schedule a task to spin up a ServiceNow developer instance and the BrowserGym harness, used by
   both WorkArena and WorkArena++.
4. Schedule a task to specify the verbalized-confidence prompt template (low / medium / high +
   justification) and implement the 3-sample self-consistency aggregator.
5. Schedule a Phase 1 annotation task to label gold actions at the three granularity levels on a
   pilot of 20 tasks before scaling to 100.

## Files Produced

* `tasks/t0002_*/research/research_papers.md` — empty-corpus baseline survey.
* `tasks/t0002_*/research/research_internet.md` — 17 queries, 11 discovered papers.
* `tasks/t0002_*/research/research_code.md` — empty library landscape.
* `tasks/t0002_*/plan/plan.md` — 11-section plan with REQ-1 through REQ-7.
* `tasks/t0002_*/assets/paper/<paper_id>/details.json` and `summary.md` — 11 paper assets.
