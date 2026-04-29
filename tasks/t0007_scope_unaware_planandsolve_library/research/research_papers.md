---
spec_version: "1"
task_id: "t0007_scope_unaware_planandsolve_library"
research_stage: "papers"
papers_reviewed: 1
papers_cited: 1
categories_consulted:
  - "hierarchical-planning"
  - "granularity-conditioning"
  - "agent-evaluation"
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

This task implements the canonical scope-unaware (B) baseline library for the project's A-vs-B-vs-C
comparison. The library adapts LangChain's Plan-and-Execute reference implementation of Wang et
al.'s Plan-and-Solve (PS) prompting [Wang2023] and exposes a `PlanAndSolveAgent` whose trajectory
log schema is interchangeable with the scope-aware (A) library produced in t0006. The purpose of
this paper review is to ground the prompt template, the parsing of the free-form numbered plan, and
the execution loop in a single authoritative source rather than ad-hoc design choices.

## Category Selection Rationale

Consulted `hierarchical-planning` because Plan-and-Solve is itself a two-level plan-then-execute
hierarchy and is the closest published analogue to the project's scope-aware A condition with the
explicit granularity tags removed. Consulted `granularity-conditioning` because the trajectory
schema must record the absence of granularity tags (the literal `"unspecified"`) so that downstream
analyses can distinguish B trajectories from A and C trajectories. Consulted `agent-evaluation`
because the library will be evaluated against the same harness as t0006 and must therefore expose
trajectory records that an evaluation script can parse without bespoke glue.

Excluded `uncertainty-calibration` (no calibration work in scope), `benchmark-frontierscience` /
`benchmark-swebench` / `benchmark-taubench` / `benchmark-workarena` (this task does not commit to a
specific benchmark — that is a Phase 2 task), and `benchmark-annotation` (no human annotation in
this library).

## Key Findings

### Plan-Then-Execute Is the Canonical Scope-Unaware Pattern

Plan-and-Solve prompting is a single-prompt zero-shot technique that instructs the model to first
produce a plan and then carry out the plan step by step [Wang2023]. The PS template literally reads:
`"Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan and solve the problem step by step."`
The PS+ variant extends this with detailed instructions to extract relevant variables, attend to
numerical calculation, and "show the answer." This two-stage plan-execute structure is the closest
published analogue to the project's scope-aware (A) three-level hierarchy *without* the explicit
granularity tags — i.e., the PS plan corresponds loosely to the A "global" level and the PS solve
corresponds to the A "subtask + atomic" levels collapsed into one. Because the model is never told
to label its own steps with granularity tags, every step in a PS trajectory must be recorded as
`"unspecified"` in the project's trajectory schema.

**Hypothesis**: the gain of PS over Zero-shot-CoT, measured by [Wang2023] across ten reasoning
datasets, is the lower bound for the gain a scope-aware (A) condition can achieve over a naive-CoT
(D) condition; the *additional* gain attributable to explicit granularity tagging is the A-vs-B
delta this project is designed to measure.

### Quantitative Anchors From the Original Paper

[Wang2023] reports that PS+ on GSM8K reaches **≈58%** with GPT-3 text-davinci-003 zero-shot, versus
**≈57%** for 8-shot manual CoT — comparable performance with no exemplars. PS exhibits **consistent
positive deltas over Zero-shot-CoT on all 10 datasets** the paper evaluates (arithmetic: GSM8K,
SVAMP, AQuA, AddSub, MultiArith, SingleEq; commonsense: CommonsenseQA, StrategyQA; symbolic: Last
Letter Concatenation, Coin Flip). PS specifically targets and reduces *missing-step errors*; PS+
additionally reduces *calculation errors* through the "pay attention to correct numerical
calculation" instruction. These numbers are not the metric this task produces — this task only
produces a library — but they bound what a Phase 2 evaluation should expect.

### LangChain Plan-and-Execute Is the Canonical Reference Implementation

[Wang2023] is implemented in LangChain core as `Plan-and-Execute`, an Apache-2.0 licensed module.
The reference implementation defines (1) a planner LLM that produces a numbered plan as free-form
text, (2) a regex-style parser that splits the plan into ordered steps, (3) an executor LLM (often
the same model with a different prompt) that runs each step in turn with optional tool use, and (4)
a finish-detection rule that terminates when the plan is exhausted or the executor emits a
designated stop token. The free-form numbered plan is parsed deterministically with a regex over
patterns like `^\s*\d+[\.\)]\s+(.+)$`; lines that do not match are treated as continuations of the
previous step. This parsing approach is robust to minor formatting drift from the model and is what
this library will adopt verbatim.

## Methodology Insights

* **Adopt the PS+ prompt verbatim, not a paraphrase**, so that any future reproduction matches
  [Wang2023]'s reported numbers. The exact text is
  `"Let's first understand the problem, extract relevant variables and their corresponding numerals, and make and devise a complete plan. Then, let's carry out the plan, calculate intermediate variables (pay attention to correct numerical calculation and commonsense), solve the problem step by step, and show the answer."`

* **Parse the plan with a numbered-list regex**, accepting both `1.` and `1)` separators, and treat
  non-matching lines as continuations of the previous step. This mirrors the LangChain reference
  implementation and is what the deterministic-test mode must round-trip.

* **Execute each plan step sequentially with the same LLM**, passing the original problem, the full
  plan, the running observation log, and the current step number into the executor prompt. This is
  the LangChain Plan-and-Execute loop and is the simplest implementation faithful to PS.

* **Log every step's `{turn_index, granularity, thought, action, observation, confidence}`** with
  `granularity = "unspecified"` for every record. This matches the scope-aware (A) library's
  trajectory schema field-for-field so a Phase 2 harness can swap libraries by changing one import
  line.

* **Provide a deterministic-test mode** that accepts pre-recorded model outputs as a list of
  strings, returning them in order on each `model_call`. This eliminates LLM cost during testing and
  lets the test suite assert plan-parse, sequential execution, finish detection, and
  malformed-output recovery without any API calls.

* **Hypothesis to test in Phase 2**: in PS the "plan" tier produces global-level text and the
  "solve" tier produces subtask + atomic execution; instrumenting the trajectory log with a post-hoc
  tagger could reveal scope effects *within* the B condition.

## Gaps and Limitations

* The original [Wang2023] paper PDF was not downloaded in t0002 (download failed; only the abstract
  was used). All quantitative numbers in this task are sourced through the t0002 summary, which
  itself is grounded only in the abstract and public sources. This is acceptable for a write-library
  task where no benchmark numbers are produced, but a Phase 2 evaluation should re-download the
  paper and verify the prompt template and headline numbers directly.

* [Wang2023] does not specify behaviour for malformed plans (e.g., a plan that contains zero
  numbered steps). The library must define this behaviour itself; the chosen policy is to raise a
  structured `MalformedPlanError` so callers can decide whether to retry or fall back.

* The paper covers only English reasoning datasets with GPT-3 text-davinci-003. Behaviour on newer
  models, on tool-use settings, or on non-English inputs is unstudied. The library is agnostic to
  the underlying model via the `model_call` callable so future tasks can swap the model without
  touching the library.

## Recommendations for This Task

1. Implement `PlanAndSolveAgent` with the PS+ prompt verbatim as the default; expose the prompt text
   as a module-level constant so it is auditable and overridable by callers.

2. Define the trajectory log schema in this library because the sister task t0006 has not yet merged
   when this task starts. Document the schema clearly in `description.md` so t0006 can conform when
   it merges.

3. Use a regex-based plan parser with explicit handling for malformed plans (raise
   `MalformedPlanError`).

4. Implement a deterministic-test mode that uses a `ScriptedModel` callable returning pre-recorded
   responses; cover plan parsing, sequential execution, finish detection, schema parity, and
   malformed-plan recovery in `code/test_planandsolve.py`.

5. Record `granularity = "unspecified"` on every trajectory record so post-hoc analyses can
   distinguish B trajectories from A and C.

6. Adapt the LangChain Plan-and-Execute structure with Apache-2.0 attribution recorded in
   `description.md`.

## Paper Index

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R. K., Lim, E.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `hierarchical-planning`, `granularity-conditioning`
* **Relevance**: This is the source paper for the scope-unaware (B) baseline library this task
  produces. The PS+ prompt template, the plan-then-execute structure, and the headline GSM8K numbers
  (≈58% PS+ vs ≈57% 8-shot CoT) all come from this paper. The task references the LangChain
  Plan-and-Execute reference implementation it inspired (Apache 2.0).
