# Pre-Registered Predictions

This document fixes the predicted directions and detection thresholds **before** the smoke run is
executed, per the task description's hypothesis pre-registration requirement. After the run, the
results files will report observed effects, paired McNemar p-values, and confirmation/refutation
verdicts against this register.

## Hypotheses

### RQ1 — A success rate exceeds B success rate (`task_success_rate`)

* **Predicted direction**: `task_success_rate(A) − task_success_rate(B) ≥ +5 percentage points`.
* **Detection threshold at N=40 (paired)**: ≥ +15pp paired (paired McNemar / exact binomial sign
  test, two-tailed α = 0.05). Paired McNemar requires ~25 discordant pairs to detect a 15pp paired
  effect at α=0.05/0.8 power; ~150 discordant pairs to detect 5pp.
* **Confirmed if**: observed A−B paired effect ≥ +5pp AND McNemar two-tailed p < 0.10
  (smoke-run-relaxed threshold).
* **Refuted if**: observed A−B paired effect < 0pp OR observed effect ≥ +5pp but McNemar p > 0.30.

### RQ2 — A overconfident-error rate is at most B's (`overconfident_error_rate`)

* **Predicted direction**: `overconfident_error_rate(A) − overconfident_error_rate(B) ≤ −2pp`.
* **Detection threshold at N=40 (paired)**: ≥ |5pp| to |8pp| paired difference is the band reachable
  at this N.
* **Confirmed if**: observed A−B difference ≤ −2pp.
* **Refuted if**: observed A−B difference > 0pp.
* **Inconclusive otherwise** (smaller-than-detection-band difference): report effect size with 95%
  CI and the implied confirmatory N.

### RQ5 — C ranks worst on Metrics 1 and 2

* **Predicted direction**:
  `task_success_rate(C) ≤ min(task_success_rate(A), task_success_rate(B)) − 5pp` AND
  `overconfident_error_rate(C) ≥ max(overconfident_error_rate(A), overconfident_error_rate(B)) + 5pp`.
* **Confirmed if**: both predictions hold strictly.
* **Refuted if**: C is not strictly worst on either metric.

## Excluded by design

* **RQ3 (request-vs-act accuracy on low-level tasks)** — needs tau-bench, not FrontierScience.
* **RQ4 (gains concentrated in info-asymmetric states)** — needs WorkArena++ or a tool-using
  benchmark.

## Pre-registration provenance

* Date: 2026-04-30
* Author: t0012 planning step
* Source hypotheses: `task_description.md` § Hypotheses tested.
* Last opportunity for register edits: before the validation gate (Step 6) starts. After that, any
  amendment must be logged separately.
