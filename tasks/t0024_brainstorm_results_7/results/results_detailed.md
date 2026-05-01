# Brainstorm Session 7 — Detailed Results

## Summary

Brainstorm Session 7 cancelled t0023 (phase 2 ABC confirmatory sonnet experiment) because its $40-45
cost estimate exceeds the $26.12 remaining project budget after t0019's weakened headline, and
replaced it with t0025 — a focused 10-paper literature survey of 2024-2026 hierarchical-agent and
LLM-as-judge work, plus the 1999 options-framework paper as a theory anchor. The phase 2 ABC sonnet
experiment is deferred to a post-survey Brainstorm Session 8 so the design can incorporate
hierarchical-agent and judge-methodology findings. No RQ was answered; all five remain open or
deferred.

## Methodology

This was a planning session — no compute, no remote machines, no metric runs. Inputs and procedure:

* Aggregated project state via `aggregate_tasks`, `aggregate_suggestions --uncovered`,
  `aggregate_answers`, `aggregate_costs` (all with `--format json`).
* Read the four results summaries produced since Brainstorm Session 6 (t0019, t0020, t0021, t0022)
  and the t0019 model-rotated judge finding in detail.
* Independently reassessed every active high-priority suggestion against current task results before
  presenting to the researcher.
* Iterated through three candidate paths (rescope-and-answer-RQ, thesis-pivot,
  literature-refresh-first) with the researcher, who pivoted mid-session to the literature-refresh
  path and provided the 10-paper reading list.
* Applied the agreed slate by editing `tasks/t0023_*/task.json` to `cancelled`, writing 5 correction
  files in `tasks/t0024_brainstorm_results_7/corrections/`, and creating the t0025 task scaffold via
  the `/create-task` skill.

## Context

Brainstorm Session 6 (t0018) had scheduled t0023 (`phase2_abc_confirmatory_sonnet_swebench`, N>=157,
$40-45 estimated) as the headline confirmatory ABC experiment. Two facts moved between t0018 and the
start of this session:

1. **t0019 weakened the headline schema effect**. The schema-only accept-rate delta from t0014 (+58
   pp under haiku judge) shrinks to **+24.6 pp** under a substantive sonnet judge and **+37.3 pp**
   under a model-rotated sonnet judge. Both numbers are below the +45 pp commit threshold the task
   pre-registered. Model-anchoring is the dominant judge-side effect.
2. **Budget**: $26.12 remaining of the $100 project budget after t0019 ($19.30) and t0014 ($21.16)
   cost overruns. t0023 at $40-45 does not fit even with the minimum-viable cuts.

## Project State Going In

| Aspect | Status |
| --- | --- |
| Completed tasks | 22 |
| In progress / not-started | t0023 only |
| RQs answered | 0 of 5 |
| Suggestions: high-priority active | several across t0010, t0014, t0017, t0019 |
| Budget remaining | $26.12 |
| Latest libraries shipped | t0021 (plan-and-solve v2), t0022 (ABC harness + progress rate + error taxonomy) |

## Discussion Summary

The session opened with the researcher reviewing the project state and noting that no RQ has a
confirmed answer despite 22 tasks. Three candidate paths were surfaced:

* **Path A — rescope-and-answer-RQ**: trim t0023 to N=80, drop C-adversarial, drop sonnet judge
  spot-check, hard-cap at $25. Estimated to fit in budget but with no margin and per-task overruns
  of 3-4x as the historical norm.
* **Path B — thesis-pivot**: stop new experiment work and write the thesis around the offline
  annotation findings (t0014 + t0019 + t0020). Defensible body of work but leaves all 5 RQs
  unanswered.
* **Path C — literature-refresh-first**: spend ~$3 on a focused 2024-2026 literature survey before
  committing the bulk of the remaining budget to another sonnet experiment, so the next-experiment
  design is informed by current state-of-the-art on hierarchical agents and LLM-as-judge
  methodology.

After dialogue, the researcher chose Path C and provided a 10-paper reading list. The reasoning was
that the existing project surveys (t0002, t0017) predate the t0014, t0019, t0020 findings and may
have under-weighted hierarchical-RL, options-framework, and judge-anchoring literature that bears
directly on what the next experiment should look like.

The phase 2 ABC sonnet experiment (formerly t0023, considered as t0025 in earlier session drafts) is
deferred to a post-survey Brainstorm Session 8.

## Decisions Applied in Step 3

### Cancellation

* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — `status: not_started` →
  `status: cancelled`. No other fields changed.

### New task

| ID | Slug | Type | Cost cap | Expected assets |
| --- | --- | --- | --- | --- |
| t0025 | `lit_survey_hierarchical_agents_and_judges_2024_2026` | `literature-survey` | ~$3 | `paper: 10` |

### Suggestion corrections (5)

| Suggestion | Action | Rationale |
| --- | --- | --- |
| S-0014-03 | reject | Covered by t0019 model-rotated judge run; data merged. |
| S-0019-01 | reject | Confirmatory v3 schema iteration not on critical path within remaining budget. |
| S-0017-01 | reject | Trust-or-Escalate library setup cost exceeds RQ-level value; the paper is on the t0025 reading list. |
| S-0002-03 | demote (high → low) | ServiceNow + WorkArena out of scope; SWE-bench is the chosen benchmark for the deferred phase 2. |
| S-0010-01 | demote (high → medium) | C-adversarial dropped from immediate slate; partial coverage by C-random remains in the planned phase 2 successor. |

## t0025 Reading List

* Hierarchical / granularity-aware agents (4):
  * "Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM Agents"
    (ICLR 2026)
  * ArCHer: "Training Language Model Agents via Hierarchical Multi-Turn RL" (ICML 2024)
  * "Reinforcing LLM Agents via Policy Optimization with Action Decomposition" (NeurIPS 2024)
  * Sutton, Precup & Singh 1999: "Between MDPs and Semi-MDPs" (foundational options framework)
* Search and planning structure (2):
  * "Can Graph Learning Improve Planning in LLM-based Agents?" (NeurIPS 2024)
  * LATS: "Language Agent Tree Search" (ICML 2024)
* Reasoning structure discovery (1):
  * SELF-DISCOVER (NeurIPS 2024)
* Agent benchmarks (2):
  * Embodied Agent Interface (NeurIPS 2024)
  * AgentBoard (NeurIPS 2024 Datasets and Benchmarks)
* LLM-as-judge methodology (1):
  * "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"

## Limitations

* Brainstorm sessions are planning artifacts, not experimental results. No metrics, no compute, no
  empirical findings. Decisions are quality-controlled only by reviewer judgement.
* The remaining $26 budget after t0025's ~$3 leaves only ~$23 for any post-survey experiment — below
  most realistic cost estimates for an above-floor sonnet ABC run with N>=80. The post-survey
  brainstorm may have to choose between a tightly minimal experiment and a thesis pivot.
* RQ3 is deferred without a scheduled successor task.

## Verification

* `verify_task_file t0024_brainstorm_results_7` — pass (expected).
* `verify_task_file t0025_lit_survey_hierarchical_agents_and_judges_2024_2026` — pass.
* `verify_task_results t0024_brainstorm_results_7` — to be run during finalize step.
* `verify_logs t0024_brainstorm_results_7` — to be run during finalize step.
* `verify_corrections t0024_brainstorm_results_7` — to be run during finalize step.

## Files Created

* `tasks/t0024_brainstorm_results_7/` — brainstorm task folder with `task.json`,
  `task_description.md`, `step_tracker.json`, plan, research placeholders, results files, step logs,
  and 5 correction files.
* `tasks/t0025_lit_survey_hierarchical_agents_and_judges_2024_2026/` — task scaffold (`task.json`,
  `task_description.md`, status `not_started`).
* `tasks/t0023_phase2_abc_confirmatory_sonnet_swebench/task.json` — status edited to `cancelled`.

## Next Steps / Suggestions

This brainstorm produces no follow-on suggestions of its own — the immediate next executable task is
t0025, and the post-survey Brainstorm Session 8 will produce the next round of suggestions and
tasks. Any suggestions written in `results/suggestions.json` would prejudge that session.
