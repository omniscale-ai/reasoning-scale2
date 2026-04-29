---
spec_version: "3"
paper_id: "10.48550_arXiv.2411.04872"
citation_key: "Glazer2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2024
* **Authors**: Elliot Glazer, Ege Erdil, Tamay Besiroglu, and 21 others (Epoch AI and external
  contributors)
* **Venue**: arXiv preprint (cs.AI)
* **DOI**: `10.48550/arXiv.2411.04872`

## Abstract

We introduce FrontierMath, a benchmark of hundreds of original, exceptionally challenging
mathematics problems crafted and vetted by expert mathematicians. The questions cover most major
branches of modern mathematics — from computationally intensive problems in number theory and real
analysis to abstract questions in algebraic geometry and category theory. Solving a typical problem
requires multiple hours of effort from a researcher in the relevant branch of mathematics, and for
the upper end questions, multiple days. FrontierMath uses new, unpublished problems and automated
verification to reliably evaluate models while minimizing risk of data contamination. Current
state-of-the-art AI models solve under 2% of problems, revealing a vast gap between AI capabilities
and the prowess of the mathematical community.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. FrontierMath is the canonical research-grade math reasoning
benchmark released by Epoch AI in November 2024 to address two limitations of prior math
benchmarks (GSM8K, MATH, MathOdyssey): saturation by frontier models and risk of training-data
contamination. The authors interviewed Fields Medalist mathematicians (Terence Tao, Timothy Gowers,
Richard Borcherds) who characterised the problems as "exceptionally challenging" — even
research-active mathematicians need hours per problem, and the upper-tier problems require multiple
days.

For this project, FrontierMath is the canonical instantiation of the
"FrontierScience-Olympiad" benchmark named in `project/description.md`. Its <2% SOTA solve rate at
release means that on the granularity-conditioning composite benchmark, FrontierMath items will
contribute almost exclusively to the *failure* tail. The implication is that effect sizes for
scope-aware vs. scope-unaware comparisons will be measured against a near-zero baseline on this
benchmark, making relative gains numerically large but absolute gains tiny.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
benchmark uses **automated verification** (programmatic answer-checking against expert-supplied
solutions) rather than human grading, which makes it scalable for repeated evaluation. Problems
span **most major branches of modern mathematics**: number theory, real analysis, algebraic
geometry, and category theory among others. Each problem is **original and unpublished** at the
time of release — minimizing the risk of contamination from training data scraped before the
benchmark cutoff.

The benchmark is organised in **difficulty tiers** (Tiers 1-4 in public communications): Tiers 1-3
covering undergraduate to early-postdoc level, Tier 4 reaching research level. The Epoch AI
benchmark page reports that current SOTA models solve under 2% across all tiers combined at
release; later 2025 models have made progress but the gap to mathematician-level performance
remains large. The paper does not propose a new agent architecture — it is a benchmark paper.

## Results

* **<2% SOTA solve rate** by leading AI models (GPT-4o, Claude 3.5 Sonnet, etc.) at release
* **Hundreds** of problems vetted by expert mathematicians (exact count not in the public abstract)
* **Hours to multiple days** of expert effort required per problem
* **Tier 4** (research-grade) problems are characterized as "exceptionally challenging" by Fields
  Medalists Terence Tao, Timothy Gowers, and Richard Borcherds
* **Automated verification** scales to repeat evaluations without human grading bottleneck
* No prior leaderboard or benchmark paper reports comparable headline numbers — FrontierMath is the
  hardest published math benchmark in this difficulty regime

## Innovations

### Research-Grade Difficulty as a Design Goal

FrontierMath is the first openly described benchmark to *explicitly* target research-mathematician
difficulty rather than competition-math or homework-math difficulty. This places it as the most
aspirational ceiling for the project's "FrontierScience-Olympiad" slot.

### Contamination Avoidance via Unpublished Problems

By commissioning entirely new problems, the authors sidestep the dominant criticism of prior math
benchmarks — that LLMs may have seen the test sets during training. This makes year-over-year
comparison of model progress more credible.

### Programmatic Answer Verification

Automated answer-checking distinguishes FrontierMath from human-graded benchmarks (e.g., USAMO
solutions). Scaling to repeated automated runs is essential for the hundreds of prompt-conditioning
ablations the granularity-aware project will need to run.

## Datasets

* **FrontierMath problem set** — hundreds of unpublished mathematics problems, expert-vetted, with
  programmatic answer checks. Public via Epoch AI's hosted evaluation; the raw problems are not
  released to the public to preserve contamination resistance. Access requires Epoch AI's
  evaluation pipeline.

## Main Ideas

* FrontierMath maps directly to the project's "FrontierScience-Olympiad" benchmark slot and should
  be treated as the canonical source for top-of-hierarchy strategic-planning items.
* The <2% SOTA solve rate means that on the composite Phase 2 benchmark, FrontierMath items will
  dominate the failure tail. The composite must therefore be **stratified by source benchmark**
  when reporting the project's three metrics, otherwise FrontierMath's near-zero baseline will
  swamp any per-condition delta.
* Because access requires Epoch AI's evaluation pipeline, the t0003 download-dataset task should
  budget extra time for credentials, sample-size negotiation, and a fallback to
  publicly-available stand-ins (e.g., Olympiad benchmarks like MATH-500 or AIME) if Epoch AI
  access cannot be obtained in time.

## Summary

The paper introduces FrontierMath, a research-mathematician-grade math reasoning benchmark
designed to evaluate frontier LLMs on problems that require hours to days of human expert effort.
The motivation is the saturation of prior math benchmarks (GSM8K, MATH) by SOTA models and the
contamination risk of using publicly available problems for evaluation.

The benchmark is built by commissioning hundreds of original, unpublished problems from expert
mathematicians, with programmatic answer-checking that scales to repeated automated runs. Problems
span number theory, real analysis, algebraic geometry, and category theory; difficulty tiers cover
undergraduate through research level. Endorsements from Fields Medalists (Tao, Gowers, Borcherds)
characterize the upper-tier problems as exceptionally challenging.

The headline result is that current state-of-the-art models solve **under 2% of problems** at
release, revealing a large gap between AI and expert-mathematician performance. This is the
hardest published math benchmark to date.

For the granularity-aware hierarchical agents project, FrontierMath is the canonical instantiation
of the FrontierScience-Olympiad slot named in `project/description.md`. The <2% baseline means the
benchmark contributes mainly to the failure tail of the composite Phase 2 benchmark, and any
per-condition (scope-aware vs. scope-unaware) effect must be measured against a near-zero floor —
which makes per-source stratification mandatory. Access via Epoch AI's evaluation pipeline is a
known operational risk for the t0003 download-dataset task.
