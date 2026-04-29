# Research Roadmap

## Research Question

In hierarchical problem solving, does explicitly specifying the agent's current operating granularity (global planning, subtask planning, or atomic execution) improve action quality, uncertainty calibration, and final task success compared with an otherwise identical agent that is not told its current granularity?

## Hypothesis

Explicit granularity/scale conditioning improves agent performance. An agent given the correct operating granularity will achieve higher expected task reward, higher scope-conditioned action accuracy, and lower overconfident error rates than an agent given the same state without an explicit granularity label. Incorrect granularity labels will reduce performance.

### Sub-hypothesis 1
The strongest gains appear in states where local execution requires information not needed for higher-level planning — i.e., when granularity mismatch most directly causes scope confusion.

### Sub-hypothesis 2
Granularity-mismatched agents perform worst (below both scope-aware and scope-unaware baselines).

## Key Variables

| Condition | Description |
|-----------|-------------|
| **A — Scope-aware** | Prompt explicitly specifies required level: global planning / subtask planning / atomic execution |
| **B — Scope-unaware** | Same state and goal, no explicit granularity label |
| **C — Scope-mismatched** | Agent given an incorrect operating level |
| *(secondary)* | Full global context vs. local runtime trace only |

## Evaluation Metrics

- **Metric 1:** Normalized final task success rate (or binary success on full task)
- **Metric 2:** Fraction of incorrect actions taken with high confidence (overconfident error rate)
- **Metric 3:** For low-level tasks — accuracy in distinguishing "can execute now" vs. "must request information"

## Statistical Validation Plan

- **Sample size:** ~100 per group
- **Grouping:** Stratified across difficulty and granularity level
- **Statistical test:** TBD
- **Significance threshold:** TBD

## Dataset & Task Selection

**Composite benchmark** combining:
- FrontierScience-Olympiad
- WorkArena++
- SWE-bench Verified
- τ-bench

**Selection criteria:** Each problem must admit at least three levels of control (global plan / subtask / execution), include states where the correct action depends on the requested granularity, and allow gold-annotated valid actions at each level.

**Difficulty range:** Multi-step tasks requiring 4–8 decisions per task.

## Validation Phase Tree

---

## Phase 1: Task Decomposition & Annotation

**Goal:** Decompose each task solution into a hierarchical structure with three levels: strategic (high-level planning), subtask, and execution (low-level). Annotate golden solutions.
**Depends on:** —
**Method:** Manual + LLM-assisted annotation of benchmark tasks; define annotation schema for levels and gold actions
**Success criterion:** ≥100 tasks fully annotated with gold actions at each of 3 granularity levels
**Scripts:** `scripts/collect_and_annotate.py`, `data/annotation_pilot/`
**Status:** in progress

---

## Phase 2: Baseline Experiment (Scope-aware vs. Scope-unaware)

**Goal:** Evaluate conditions A vs. B across annotated tasks; measure Metrics 1–3.
**Depends on:** Phase 1
**Method:** Run same model on same states under conditions A and B; record chosen action, confidence, replanning behavior, final outcome
**Success criterion:** Statistically significant difference in at least 2 of 3 metrics at chosen threshold
**Scripts:** `scripts/run_experiment.py`, `scripts/run_diploma_experiments.py`
**Status:** pending

---

## Phase 3: Mismatch Condition

**Goal:** Add condition C (scope-mismatched) to test sub-hypothesis 2.
**Depends on:** Phase 2
**Method:** Run model with incorrect granularity labels; compare to A and B
**Success criterion:** C performs worst on Metrics 1 and 2
**Scripts:** `config/experiment_exp3_mismatch.yaml`
**Status:** pending

---

## Phase 4: Analysis & Synthesis

**Goal:** Statistical analysis, cross-dataset breakdown, paper-ready findings.
**Depends on:** Phases 2–3
**Method:** Significance tests, stratified breakdown by task family and difficulty, ablations
**Success criterion:** Clear confirm/refute verdict on main hypothesis with effect sizes
**Scripts:** `scripts/analyze_results.py`, `scripts/run_synthesis.py`
**Status:** pending
