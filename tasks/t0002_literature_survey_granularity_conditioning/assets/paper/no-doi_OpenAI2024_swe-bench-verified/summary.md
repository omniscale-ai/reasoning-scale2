---
spec_version: "3"
paper_id: "no-doi_OpenAI2024_swe-bench-verified"
citation_key: "OpenAI2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# Introducing SWE-bench Verified

## Metadata

* **File**: Download failed (HTML technical card; not retrieved into git)
* **Published**: 2024
* **Authors**: OpenAI Preparedness team 🇺🇸
* **Venue**: OpenAI institutional technical card (not peer-reviewed)
* **DOI**: N/A

## Abstract

We are releasing SWE-bench Verified, a human-validated subset of SWE-bench that more reliably
evaluates AI models' ability to solve real-world software issues. SWE-bench Verified consists of
500 problems that real software engineers have confirmed are solvable: each problem description
is clear, the test patches correctly identify the issue's resolution, and the tests are not
flaky. The original SWE-bench dataset can include problems with under-specified instructions or
test patches that miss the intended fix; OpenAI's Preparedness team worked with the SWE-bench
authors and 93 expert software engineers to filter to 500 problems where the issue description is
unambiguous, the unit tests cover the intended fix, and the development environment can be
reliably reproduced. SWE-bench Verified is intended to be the new standard subset for measuring
frontier autonomous-software-engineering capability.

## Overview

This summary is based on the public technical card and the original SWE-bench paper [Jimenez2024];
the technical card itself was not retrieved into the git repository. SWE-bench Verified addresses
two limitations of the original SWE-bench [Jimenez2024]: (a) some problems have ambiguous issue
descriptions where the "correct" fix depends on guessing what the maintainer wanted, and (b) some
problems' test suites have flaky tests or tests that pass for incorrect patches. Both issues
caused the original SWE-bench to slightly underestimate model capability — in particular, low
scores conflated genuine model limitations with benchmark artifacts.

OpenAI's Preparedness team partnered with the SWE-bench authors (Jimenez, Yang, et al.) and 93
expert software engineers to **manually validate every problem** in a 500-instance subset. Each
problem went through three independent expert reviews. The result, SWE-bench Verified, has become
the de facto standard subset for measuring frontier autonomous-software-engineering capability
across 2024-2026.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
**atomic-execution** slot in the four-source composite. Its 500-instance size is small enough to
evaluate at reasonable cost, and the human validation removes the noise that the larger 2,294-
problem original would introduce.

## Architecture, Models and Methods

Full methodology not available — technical card not downloaded into the repo. From public
sources, the validation process was:

1. **Take the 1,699 candidate problems** from the original SWE-bench.
2. **Each problem reviewed by three independent expert software engineers** (93 experts total).
3. Reviewers scored: (a) is the issue description clear and unambiguous? (b) do the test patches
   correctly identify the resolution? (c) is the development environment reliably reproducible?
4. **Filter to 500 problems** that all three reviewers approved on all three axes.

The resulting subset preserves the original SWE-bench evaluation harness — Docker-isolated
container per repository, patch-application + test-suite execution, `resolve@1` scoring. The only
change is the 500-instance set itself; the harness, scoring, and Docker images are identical to
the parent benchmark [Jimenez2024].

The set spans the same 12 Python repositories as the parent (Django, scikit-learn, SymPy,
Matplotlib, etc.), with relative weight roughly proportional to original-benchmark size.

## Results

* **500 problems** human-validated by 93 expert software engineers
* **3 independent expert reviews per problem** before inclusion
* **Three-axis validation**: clear instructions, correct test patches, reproducible environment
* The Verified leaderboard tracks 43+ frontier LLMs as of early 2026
* As of April 2026, **Claude Mythos Preview leads at 93.9%**, **Claude Opus 4.7 (Adaptive) at
  87.6%**, **GPT-5.3 Codex at 85%** — far above the 1.96% Claude 2 baseline on the parent
  benchmark
* OpenAI noted in their April 2026 follow-up that Verified saturation may make it less useful as
  a frontier-capability measurement going forward — a meta-finding for the project's choice of
  benchmarks

## Innovations

### Three-Reviewer Manual Validation

Prior code benchmarks rely on automated filters; SWE-bench Verified uses three independent expert
reviewers per problem. This is unusually thorough for a 500-instance set and explains why other
groups have been willing to treat Verified as the standard.

### Decoupling Capability From Benchmark Noise

By filtering for unambiguous issues and reliable tests, Verified scores can be interpreted as
genuine capability rather than capability-plus-benchmark-luck. This is what made it the
de-facto standard.

### Industry-Academic Collaboration as a Reproducibility Norm

The OpenAI + SWE-bench-authors collaboration is an example of industry resources (paid expert
reviewers) being used to improve a peer-reviewed academic benchmark. This collaboration model has
since been replicated for other benchmarks.

## Datasets

* **SWE-bench Verified** — 500 problems, JSON metadata + Docker images. Public on GitHub
  (`SWE-bench/SWE-bench`) under a permissive license. Loadable via the `datasets` library.

## Main Ideas

* Adopt SWE-bench Verified (500 instances) as the project's atomic-execution slot in the
  four-source composite. The full 2,294-instance original is too noisy and too expensive to run
  at scale.
* Note OpenAI's April 2026 observation that Verified is approaching saturation. The project
  should plan a fallback to SWE-bench Multimodal or SWE-bench Pro if frontier models score >95%
  on Verified by Phase 2.
* The technical card is not peer-reviewed but the underlying benchmark is. Cite both
  [OpenAI2024] (for Verified) and [Jimenez2024] (for SWE-bench parent) in the Phase 4
  paper-ready report.

## Summary

SWE-bench Verified is a 500-instance human-validated subset of SWE-bench produced by OpenAI's
Preparedness team in collaboration with the original SWE-bench authors. The motivation is that
the parent benchmark of 2,294 problems contains some items with ambiguous issue descriptions or
flaky tests, which add noise to capability measurements at the frontier.

Methodologically, 93 expert software engineers each reviewed candidate problems on three axes:
(a) clear instructions, (b) correct test patches, (c) reproducible environments. Three
independent reviewers per problem; only problems passing all three axes from all three reviewers
were included. The harness, Docker images, and resolve@1 scoring are identical to the parent
benchmark.

The headline outcome is that Verified has become the de facto standard subset for measuring
frontier autonomous-software-engineering capability in 2024-2026. Modern models score far above
the parent benchmark's 1.96% Claude 2 baseline — Claude Mythos Preview leads at **93.9%**
(April 2026). OpenAI's own April 2026 commentary noted that this saturation may limit
Verified's usefulness as a frontier-capability measurement going forward.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the Phase 2 composite benchmark. Its 500-instance size is tractable for
multiple-condition evaluation, the human validation removes benchmark noise, and stratified
reporting is essential because Verified's >90%-achievable ceiling would otherwise drown out
FrontierMath's <2% baseline. The project should plan a fallback to SWE-bench Multimodal or
SWE-bench Pro if Verified saturates further before Phase 2 completes.
