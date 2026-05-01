# Brainstorm Session 7: Refresh Literature Before the Next Agent Iteration

## Motivation

Brainstorm Session 6 (t0018) scheduled the headline confirmatory experiment as t0023
(`phase2_abc_confirmatory_sonnet_swebench`, N=157, $40-45 estimated). Two facts moved between t0018
and now:

1. **t0019 weakened the headline schema effect**. The schema-only accept-rate delta from t0014 (+58
   pp under haiku judge) shrinks to +24.6 pp under a substantive sonnet judge and +37.3 pp under a
   model-rotated sonnet judge. Both numbers are below the +45 pp commit threshold the task
   pre-registered. Model-anchoring is the dominant judge-side effect.
2. **Budget**: $26.12 remaining of the $100 project budget. Tasks have run 3-4x estimates (t0014
   $21.16, t0019 $19.30 against $5 plans). t0023 at $40-45 does not fit even with the minimum-viable
   cuts described in its `task_description.md` Risks & Fallbacks.

The brainstorm-6 slate intentionally separated infrastructure (t0021, t0022) from the headline agent
run. Both libraries are now shipped and verified. Before consuming them with another expensive
sonnet experiment, the researcher chose to refresh the project's literature understanding of
hierarchical / granularity-aware agents and judge methodology, so the next experiment iteration is
designed against the current state of the art rather than the t0002 / t0017 surveys that predate the
t0014, t0019, t0020 findings.

## Decisions

### Direction

The five project research questions in `project/description.md` have **zero confirmed answers**
across 22 completed tasks. The brainstorm-6 plan was to answer 4 of 5 RQs in one rescoped sonnet
experiment. After dialogue, the researcher decided that the cheapest correct next move is a focused
2024-2026 literature survey covering hierarchical / granularity-aware LLM agents, search and
planning structure, reasoning-structure discovery, agent benchmarks, and LLM-as-judge methodology,
plus the foundational options-framework theory anchor (Sutton, Precup & Singh 1999). The survey
informs the design of the next agent-iteration experiment, which is deferred to a post-survey
brainstorm session.

RQ3 (low-level "can-execute-now" vs "must-request-information") remains deferred — it requires a
different instrumentation (τ-bench-style) regardless of which experiment comes next.

### New Tasks (1)

| ID | Slug | Covers | Cost cap | Depends |
| --- | --- | --- | --- | --- |
| t0025 | `lit_survey_hierarchical_agents_and_judges_2024_2026` | reading list of 10 papers; informs next agent-iteration design | ~$3 | none |

### Cancellations (1)

| ID | Action | Reason |
| --- | --- | --- |
| t0023 | `not_started` → `cancelled` | Original $40-45 estimate exceeds remaining budget. The phase 2 ABC sonnet experiment is deferred to a post-literature-survey brainstorm so the design can incorporate hierarchical-agent and judge-methodology findings from t0025. |

### Corrections (5)

| Suggestion | Action | Reason |
| --- | --- | --- |
| S-0014-03 | active → rejected | Covered by t0019 model-rotated judge run; data merged. |
| S-0019-01 | active → rejected | Confirmatory v3 schema iteration not on critical path within remaining budget. |
| S-0017-01 | active → rejected | Trust-or-Escalate selective-evaluation library setup cost exceeds RQ-level value; the Trust-or-Escalate paper itself is on the t0025 reading list. |
| S-0002-03 | priority high → low | ServiceNow + WorkArena harness out of scope; SWE-bench is the chosen benchmark for the deferred phase 2 experiment. |
| S-0010-01 | priority high → medium | C-adversarial dropped from the immediate slate; partial coverage by C-random remains in the planned phase 2 successor. |

## t0025 Reading List

Ten papers organized by theme. Asset format: standard paper assets in
`tasks/t0025_*/assets/paper/<paper_id>/` per `meta/asset_types/paper/specification.md`.

* **Hierarchical / granularity-aware agents** (4):
  * "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents"
    (ICLR 2026)
  * ArCHer: "Training Language Model Agents via Hierarchical Multi-Turn RL" (ICML 2024)
  * "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024)
  * Sutton, Precup & Singh 1999: "Between MDPs and Semi-MDPs" (foundational options framework)
* **Search and planning structure** (2):
  * "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024)
  * LATS: "Language Agent Tree Search" (ICML 2024)
* **Reasoning structure discovery** (1):
  * SELF-DISCOVER (NeurIPS 2024)
* **Agent benchmarks** (2):
  * Embodied Agent Interface (NeurIPS 2024)
  * AgentBoard (NeurIPS 2024 Datasets and Benchmarks)
* **LLM-as-judge methodology** (1):
  * "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"

## Hard Kill Switches for t0025

A literature-survey task does not need experiment-style kill switches, but the cost cap is enforced:

* **Hard cap**: ~$3 ceiling for the whole survey (PDF downloads are free; cost comes only from agent
  reading and summarization). Halt if the projection at 5 papers in exceeds $5.
* **Stop on paywall block**: if more than 2 of the 10 papers cannot be downloaded after exhausting
  arXiv, Semantic Scholar, OpenAlex, and conference proceedings, halt and produce a summary based on
  abstracts plus a triage note.

## Parallelism

t0025 is the only new task. The 10 paper-add invocations inside t0025 can run in parallel via
sub-agents (each `add-paper` invocation is independent).

## RQ Coverage After This Session

| RQ | Status After t0024 | Addressed by |
| --- | --- | --- |
| RQ1 (granularity → success) | open → still open | future post-survey experiment |
| RQ2 (overconfident error) | open → still open | future post-survey experiment |
| RQ3 (can-execute vs must-request) | open → deferred | future task |
| RQ4 (gains in info-asymmetric states) | open → still open | future post-survey experiment |
| RQ5 (mismatch penalty) | open → still open | future post-survey experiment |

The literature survey itself does not answer any RQ; it informs the design of the experiment that
will. If post-survey brainstorming concludes that no remaining-budget experiment can credibly answer
the RQs, the project pivots to a thesis headlined on the offline annotation + judge calibration
findings (t0014 + t0019 + t0020) plus the literature-survey synthesis.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — full brainstorm task folder.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold (status
  `not_started`).
* 5 correction files in `tasks/t0024_brainstorm_results_7/corrections/`.
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to `cancelled`.

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no compute, no
  empirical findings. Decisions are quality-controlled only by reviewer judgement.
* A literature survey does not directly answer any RQ. It is preparatory work for the next
  experiment design, which itself is not yet scheduled.
* The remaining $26 budget after t0025's ~$3 leaves only ~$23 for any post-survey experiment — which
  is below most realistic cost estimates for an above-floor sonnet ABC run with N>=80. The
  post-survey brainstorm may have to choose between a tightly minimal experiment and a thesis pivot.
* RQ3 is deferred without a scheduled successor task.

## Next Steps

* Execute t0025 next: download and summarize the 10 papers, then write a synthesis section in the
  results that explicitly maps findings to candidate next-experiment designs.
* After t0025 completes: open Brainstorm Session 8 to scope the next agent-iteration experiment
  given the survey synthesis and the ~$23 remaining budget.
