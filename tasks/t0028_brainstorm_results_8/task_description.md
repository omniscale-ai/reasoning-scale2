# Brainstorm Session 8: Close RQ1/RQ4 with Discordance-Rich Resample

## Context

Following t0024 (brainstorm 7), three substantive tasks ran:

* **t0025** literature survey synthesized RQ1-RQ5 status from 10 papers; flagged that direct runtime
  ABC evidence was missing.
* **t0026** Phase 2 ABC at N=147 produced first runtime data but ran $38.61 (over budget) and
  surfaced fault-tolerance bugs in arm B and a structurally-weak C wrapper.
* **t0027** Phase 2.5 ABC re-ran on N=130 paired instances with a fault-tolerant B and revised C.
  Headline: A=B=6 successes (4.62%), C=7 (5.38%). McNemar 6 vs 6 discordant pairs p=1.0 (RQ1); 4 vs
  5 discordant pairs p=1.0 (RQ5). ECE B=0.336, C=0.374 (still floored by all-100 confidence).

## RQ Status After t0027

* **RQ1** (granularity → success): underpowered. 12 discordant pairs total; need ≥30 for a verdict.
* **RQ2** (overconfident error rate): blocked by template floor; needs content-driven calibrator
  + A confidence emission.
* **RQ3** (execute-now vs request-info): not operationalized; no decision field in agent output.
* **RQ4** (info-asymmetric gain concentration): underpowered; analysis-only follow-up on TaskA.
* **RQ5** (scope-mismatched strict-worse): counter-direction (C ≥ B) on small N; C wrapper not
  structurally distinct enough.

Remaining budget: **$66.54**.

## Decisions

This session schedules a minimum viable wave to close RQ1 and RQ4.

### New tasks

1. **t0029 TaskA — Discordance-rich paired resample for RQ1**
   * Hard cap: **$35**.
   * Goal: ≥30 discordant pairs across A vs B for a McNemar verdict on RQ1.
   * Abort rule: if the cap is hit before reaching 30 discordant pairs, stop and report a partial
     verdict with a power caveat. Do not launch replacement tasks in this wave.
   * Source suggestion: S-0025-04. Covers: S-0027-05.

2. **t0030 TaskE — RQ4 info-asymmetry stratification analysis**
   * Zero API cost (analysis on TaskA outputs).
   * Goal: stratify TaskA paired sample by subset (swebench / taubench / frontsci) and by
     concordance to test whether granularity gains concentrate where information asymmetry is
     highest.
   * Dependency: t0029.

### Suggestion cleanup

* **Reject as duplicate**: S-0026-02 (duplicate of S-0027-02).
* **Reject as obsolete**: S-0025-01 (pre-Phase-2 sampling proposal superseded by t0029).
* **Demote HIGH → MEDIUM**: S-0027-01 (calibrator), S-0027-02 (C structural rebuild) — deferred to
  next wave but still load-bearing.
* **Demote HIGH → LOW**: S-0020-01, S-0021-02, S-0022-02, S-0022-05 — pre-Phase-2 hypotheses
  superseded by direct runtime evidence in t0026/t0027.
* **Mark covered**: S-0025-04 (t0029 source), S-0027-05 (t0029 covers).

### Tasks not in this wave

TaskB (calibrator), TaskC (C structural rebuild), TaskD (RQ3 instrumentation) were proposed but
deferred. The guardrail explicitly forbids launching them as replacements if t0029 hits the cap
before reaching 30 discordant pairs — preserve the budget for the next session.

## Expected Outputs

* Two new task scaffolds (t0029, t0030) at status `not_started`.
* Eight correction files in `corrections/` reflecting the suggestion cleanup above.
* Updated overview after merge.

No paid external services are used by this brainstorm task itself.
