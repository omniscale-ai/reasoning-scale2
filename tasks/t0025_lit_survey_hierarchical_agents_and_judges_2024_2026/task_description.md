# Literature Survey: Hierarchical Agents and LLM-as-Judge (2024-2026)

## Motivation

Brainstorm Session 7 (t0024) cancelled the originally planned phase 2 ABC sonnet experiment (t0023,
$40-45 estimate exceeds remaining budget) and rescoped the next move toward a focused literature
refresh. The earlier project surveys (t0002 granularity-conditioning, t0017 hierarchical agents and
judges) were authored before the t0014, t0019, and t0020 findings revealed that the haiku judge
anchors heavily on model identity and that the v2 schema effect collapses by ~25-35 pp under
stronger judges.

This task brings the project's reading current with 2024-2026 work on hierarchical /
granularity-aware LLM agents, agent search and planning structure, reasoning-structure discovery,
agent benchmarks, and LLM-as-judge methodology. The synthesis section is intended to feed directly
into Brainstorm Session 8, which will scope the next agent-iteration experiment given the remaining
~$23 budget after this survey.

## Scope

Ten papers, organized by theme:

### Hierarchical / granularity-aware agents (4 papers)

These papers most directly inform the project's RQ1 (granularity → success) and RQ4 (info-asymmetric
states):

1. "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents"
   — ICLR 2026.
2. "ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL" — ICML 2024.
3. "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" — NeurIPS 2024.
4. Sutton, Precup & Singh 1999. "Between MDPs and Semi-MDPs: A framework for temporal abstraction in
   reinforcement learning." (foundational options-framework theory anchor)

### Search and planning structure (2 papers)

Inform candidate experiment designs that compose granularity with explicit planning:

5. "Can Graph Learning Improve Planning in LLM-based Agents?" — NeurIPS 2024.
6. "LATS: Language Agent Tree Search" — ICML 2024.

### Reasoning structure discovery (1 paper)

Method for self-discovered task-specific reasoning structures (an alternative axis to the
hand-designed v2 schema in t0014/t0019):

7. SELF-DISCOVER — NeurIPS 2024.

### Agent benchmarks (2 papers)

Inform RQ3 / RQ4 / benchmark choice for the next experiment:

8. Embodied Agent Interface — NeurIPS 2024.
9. AgentBoard — NeurIPS 2024 Datasets and Benchmarks.

### LLM-as-judge methodology (1 paper)

Directly addresses the t0019 finding (judge anchoring) and informs the design of the next-step judge
protocol:

10. "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement."

## Approach

For each paper, follow the `add-paper` skill (`arf/skills/add-paper/SKILL.md`):

1. Resolve identity (DOI / arXiv ID / canonical paper ID).
2. Collect full metadata (CrossRef + Semantic Scholar + OpenAlex).
3. Download the PDF into `assets/paper/<paper_id>/files/`.
4. Write `details.json` per `meta/asset_types/paper/specification.md` v3.
5. Read the full paper and write the canonical summary document with all 9 mandatory sections.
6. Run `verify_paper_asset` and fix any errors.

Paper-add invocations are independent and may run in parallel via sub-agents. After all 10 papers
are added, write the `results/results_summary.md` synthesis that maps findings to candidate
next-experiment designs (this is the only payload of this task that informs Brainstorm Session 8).

## Cost Estimation

Total: ~$3.

* PDF downloads: free.
* Paper reading + summarization: 10 papers × ~$0.20-0.30 per paper for sonnet to read full PDF and
  produce a thorough summary ≈ $2-3.
* Synthesis writeup: ~$0.30.
* Buffer: ~$0.30.

Hard cap enforced: halt if projection at 5 papers in exceeds $5.

## Expected Outputs

* 10 paper assets in `assets/paper/`, each passing `verify_paper_asset` with zero errors.
* `results/results_summary.md` with: per-paper one-paragraph takeaway, cross-paper synthesis, and a
  "next-experiment design candidates" section explicitly mapping findings to the project's RQ1, RQ2,
  RQ4, RQ5.
* `results/results_detailed.md` with theme-grouped synthesis and a comparison table of the surveyed
  methods against the project's t0014/t0019/t0020 findings.

## Hard Kill Switches

* Cost: halt if projection exceeds $5 after 5 papers.
* Download: if more than 2 of 10 papers cannot be downloaded after exhausting the standard sources,
  halt and produce abstract-based summaries plus a triage note documenting which papers failed and
  why.

## Dependencies

None. The survey reads only published literature; no upstream task assets are required.

## Risks & Fallbacks

* Risk: paywall blocks more than 2 papers. Fallback: write abstract-based summaries with
  `download_status: "failed"` and `download_failure_reason` populated, per `add-paper` Phase 3.
* Risk: a paper turns out to be unrelated after reading. Fallback: keep the asset (it is still
  documented project knowledge) and note the irrelevance in the synthesis.
* Risk: multiple parallel paper-add agents collide on category creation. Fallback: serialize the
  category-touching steps; the rest of the asset construction can stay parallel.

## Time Estimation

~4-6 hours of agent execution (10 papers × ~30-40 min each, with parallelism cutting wall-clock to
~2-3 hours).

## Assets Needed

None.

## Expected Assets

10 paper assets in `assets/paper/`.

## Remote Machines

None. All work runs against external APIs (CrossRef, Semantic Scholar, OpenAlex, arXiv) and the LLM
API.

## Verification Criteria

* All 10 paper assets pass `verify_paper_asset` with zero errors.
* `verify_task_results` passes for the task.
* `verify_logs` passes for all step folders.
* `results_summary.md` explicitly maps survey findings to RQ1, RQ2, RQ4, RQ5 design implications for
  Brainstorm Session 8.

## Categories

Categories will be assigned per paper based on the project's `meta/categories/` registry. Likely
categories include `hierarchical-agents`, `agent-benchmarks`, `llm-as-judge`, `reasoning-structure`,
`agent-planning`, `reinforcement-learning`. Any missing categories will be created via
`/add-category` before the paper assets are written.
