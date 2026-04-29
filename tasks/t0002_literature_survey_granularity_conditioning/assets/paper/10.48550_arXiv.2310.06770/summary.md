---
spec_version: "3"
paper_id: "10.48550_arXiv.2310.06770"
citation_key: "Jimenez2024"
summarized_by_task: "t0002_literature_survey_granularity_conditioning"
date_summarized: "2026-04-29"
---

# SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

## Metadata

* **File**: Download failed (PDF deferred to future task; abstract used)
* **Published**: 2024
* **Authors**: Carlos E. Jimenez 🇺🇸, John Yang 🇺🇸, Alexander Wettig 🇺🇸, Shunyu Yao 🇺🇸,
  Kexin Pei 🇺🇸, Ofir Press 🇺🇸, Karthik Narasimhan 🇺🇸
* **Venue**: ICLR 2024 (oral)
* **DOI**: `10.48550/arXiv.2310.06770`

## Abstract

Language models have outpaced our ability to evaluate them effectively, but for their future
development it is essential to study the frontier of their capabilities. We find real-world
software engineering to be a rich, sustainable, and challenging testbed for evaluating the next
generation of language models. To this end, we introduce SWE-bench, an evaluation framework
consisting of 2,294 software engineering problems drawn from real GitHub issues and corresponding
pull requests across 12 popular Python repositories. Given a codebase along with a description of
an issue to be resolved, a language model is tasked with editing the codebase to address the
issue. Resolving issues in SWE-bench frequently requires understanding and coordinating changes
across multiple functions, classes, and even files simultaneously, calling for models to interact
with execution environments, process extremely long contexts and perform complex reasoning that
goes far beyond traditional code generation tasks. Our evaluations show that both
state-of-the-art proprietary models and our fine-tuned model SWE-Llama can resolve only the
simplest issues. The best-performing model, Claude 2, is able to solve a mere 1.96% of the issues.
Advances on SWE-bench represent steps towards LMs that are more practical, intelligent, and
autonomous.

## Overview

This summary is based on the abstract and publicly available information only; the full paper
could not be downloaded for this task. SWE-bench introduces an evaluation framework that grounds
LLM software-engineering capability in real GitHub history: 2,294 problems are sourced from
genuine issues in 12 popular Python repositories, with each problem paired to the actual pull
request that resolved it. The model is given the codebase plus the issue description and must
generate a patch; success is measured by running the repository's existing test suite, including
the tests added in the resolving PR.

This evaluation protocol is significantly harder than prior code-generation benchmarks (HumanEval,
MBPP) because (a) the codebase context can be tens of thousands of tokens, (b) resolution requires
coordinated changes across multiple files, and (c) success is judged by *passing existing tests*,
which means the model cannot game the metric by producing plausible-looking but functionally
wrong code.

For the granularity-aware hierarchical agents project, SWE-bench (and its Verified subset) is the
canonical "atomic execution" benchmark — every successful resolution is an atomic patch, and
success requires precise execution rather than abstract planning. It is the project's strongest
counterweight to FrontierMath's strategic-planning emphasis.

## Architecture, Models and Methods

Full methodology not available — paper not downloaded. From the abstract and public sources, the
benchmark sources problems from **12 popular Python repositories** including Django, scikit-learn,
SymPy, Matplotlib, Sphinx, Astropy, requests, flask, pylint, pytest, xarray, and seaborn. Each
problem provides:

* The full repository state at the issue's commit hash
* The issue text (title + body)
* The "gold" patch from the merged PR (held out from the model)
* The test suite, including tests added in the resolving PR

Evaluation runs the model's generated patch against the test suite in a Docker-isolated environment
and reports `resolve@1` — the fraction of problems where every test passes after applying the
model's patch. The original paper evaluated **Claude 2**, **GPT-4**, and a fine-tuned **SWE-Llama**
model. The benchmark has since been expanded with SWE-bench Verified (500-instance human-validated
subset), SWE-bench Lite (300-instance subset for faster iteration), and SWE-bench Multimodal.

Resolving an issue typically requires processing **tens of thousands of tokens** of codebase
context, identifying the relevant files (often without explicit guidance from the issue), and
producing a patch that respects the repository's coding conventions and existing tests.

## Results

* **2,294 problems** across 12 popular Python repositories
* **Claude 2 resolves 1.96%** — the best of the original-paper baselines
* **GPT-4 resolves a similarly small fraction** (single-digit percent in the original paper;
  improved substantially in later 2024-2025 evaluations on the Verified subset)
* **SWE-Llama** (fine-tuned by the authors) underperforms the closed-source models on the original
  benchmark
* By April 2026 the leaderboard for the **Verified** subset is led by Claude Mythos Preview at
  **93.9%**, Claude Opus 4.7 (Adaptive) at **87.6%**, and GPT-5.3 Codex at **85%** — orders of
  magnitude above the 1.96% original-paper baseline, illustrating how fast progress has been
* The benchmark is the de facto industry standard for autonomous-software-engineering evaluation
  in 2024-2026

## Innovations

### GitHub-Issue-to-Patch Evaluation Format

SWE-bench is the first benchmark to source coding problems from real GitHub history at scale. The
issue-and-test pairing means models cannot game the metric by producing plausible-looking code —
they must produce code that actually resolves the issue and passes the existing tests.

### Cross-File Coordination as a First-Class Requirement

Resolution typically requires changes across multiple files, classes, or functions. This makes
SWE-bench one of the few code benchmarks that exercises *cross-file reasoning*, which is critical
for any agent operating in a real codebase.

### Long-Context Code Understanding

Codebases routinely exceed 100K tokens. The model must select relevant files, often without
explicit guidance from the issue, before producing a patch. This stretches retrieval and long-
context reasoning capabilities far beyond function-level benchmarks like HumanEval.

## Datasets

* **SWE-bench full set** — 2,294 problems from 12 Python repositories. Open source on GitHub
  (`SWE-bench/SWE-bench`) with a Docker-based evaluation harness.
* **SWE-bench Verified** — 500-instance human-validated subset (separate paper asset
  `no-doi_OpenAI2024_swe-bench-verified`).

## Main Ideas

* SWE-bench (and its Verified subset) is the canonical *atomic execution* benchmark for the
  project's four-source composite. It anchors the low-level / atomic granularity slot.
* Cross-file coordination matters: any granularity-conditioning prompt that fails to support
  multi-file edits will lose points on SWE-bench. The scope-aware (A) condition's ATOMIC tag
  prompt should explicitly allow file reads and multi-file patches.
* Use the **Verified subset (500 instances)** rather than the full 2,294 for the project's
  composite. The full benchmark's Docker harness is heavy and the 500-instance Verified subset is
  the version other benchmarks compare against in 2024-2026.

## Summary

SWE-bench introduces a real-world software-engineering evaluation framework where 2,294 problems
are sourced from genuine GitHub issues in 12 popular Python repositories. The motivation is that
prior code-generation benchmarks (HumanEval, MBPP) test isolated function-level capability and
saturate quickly with frontier models, while real software engineering requires multi-file
coordination, long codebase context, and resolution of issues whose correct fix is judged by
existing test suites.

Methodologically, each problem provides the full repository state at the issue's commit, the issue
text, and the held-out gold patch from the merged PR. Models generate a patch; success is measured
by running the test suite (including tests added in the resolving PR) inside a Docker-isolated
environment. The original paper evaluates Claude 2, GPT-4, and a fine-tuned SWE-Llama, with the
best baseline (Claude 2) resolving only **1.96%** of issues.

Since the original paper, the benchmark has spawned three notable subsets — SWE-bench Verified
(500 instances, human-validated by OpenAI), SWE-bench Lite (300 instances), and SWE-bench
Multimodal. Modern models score far above the original baseline on Verified: Claude Mythos
Preview at **93.9%** (April 2026), illustrating how fast the field has moved.

For the granularity-aware hierarchical agents project, SWE-bench Verified is the canonical
atomic-execution slot in the four-source composite. The project should adopt the Verified subset
(500 instances) for Phase 2 evaluation, support multi-file edits in the scope-aware (A)
condition's ATOMIC prompt, and stratify metrics per source benchmark — the >90% achievable
baseline on Verified would otherwise drown out FrontierMath's <2% baseline.
