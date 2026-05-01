---
spec_version: "2"
task_id: "t0012_phase2_abc_smoke_frontierscience"
---
# Results Summary — Phase 2 A/B/C Smoke (FrontierScience-Olympiad)

## Headline

All three agent conditions (scope-aware ReAct A, scope-unaware Plan-and-Solve B, scope-mismatched
Plan-and-Solve C) solved near-zero FrontierScience-Olympiad problems with claude-haiku-4-5 and no
tools: A solved 1/40 (2.5%), B solved 0/40, C solved 0/11 (budget halted at 11 rows). The paired
McNemar test across the 6 fully overlapping rows yields p=1.0 for all pairs — the null is not
rejected, and the smoke confirms that FrontierScience-Olympiad is beyond haiku capacity without tool
use.

## Metrics

| Metric | A: scope-aware ReAct (N=40) | B: scope-unaware Plan-Solve (N=40) | C: scope-mismatched (N=11) |
| --- | --- | --- | --- |
| `task_success_rate` | **0.025** (1/40) | 0.000 (0/40) | 0.000 (0/11) |
| `overconfident_error_rate` | **0.647** | 0.000 \* | 0.000 \* |
| `avg_decisions_per_task` | **1.20** | 6.53 | 26.0 |

\* Collapsed metric: Plan-and-Solve trajectories do not emit `final_confidence`, so the Xiong2024
aggregator sees zero overconfident errors for B and C. This gap is not comparable to A.

## Statistical Tests

All McNemar paired tests (6 overlapping pairs, 0 discordant pairs): p = 1.0 (exact binomial, no
discordant). None of the pre-registered hypotheses can be confirmed or refuted at this sample size.
Confirmatory-N estimate for a 5 pp effect: **N = 157**.

## Budget

Total spend: **$18.37** (halted above $18 cap). 665 claude-haiku-4-5 calls via local Claude Code CLI
with minimal system prompt (`--tools "" --setting-sources ""`). System prompt suppression reduced
per-call cost from ~$0.10 to ~$0.005 (25× reduction enabling 84+ rows within the $18 cap; C
condition cost ~4× per row due to long Plan-and-Solve trajectories).

## Key Findings

* **FrontierScience-Olympiad is too hard for haiku without tool use.** The benchmark requires
  multi-step scientific reasoning that exceeds no-tool haiku capacity regardless of granularity
  conditioning.
* **Granularity conditioning effect is inconclusive** at N=40 with p=1.0. The smoke is underpowered
  for RQ1/RQ2/RQ5; a confirmatory run needs N≥157 paired rows and likely a stronger model (sonnet).
* **Metric 2 cannot be compared across conditions** until Plan-and-Solve is extended to emit
  `final_confidence`. This is the most actionable methodological finding.
* **Per-row checkpointing and system-prompt override** are the two engineering techniques that made
  this smoke possible within the $18 budget constraint.
