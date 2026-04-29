---
spec_version: "1"
task_id: "t0006_scope_aware_react_library"
research_stage: "papers"
papers_reviewed: 4
papers_cited: 4
categories_consulted:
  - "granularity-conditioning"
  - "hierarchical-planning"
  - "uncertainty-calibration"
  - "agent-evaluation"
date_completed: "2026-04-29"
status: "complete"
---
## Task Objective

Build the scope-aware (A) ReAct library that every Phase 2 A-condition experiment will import. The
library must extend canonical ReAct with an explicit `{global, subtask, atomic}` granularity tag at
every Thought / Action turn, expose a deterministic-test mode, and emit a JSONL trajectory log whose
schema the sister Plan-and-Solve library (`t0007`) can mirror exactly. This research stage grounds
the public API, prompt template, error-recovery behaviour, and trajectory schema in the existing
paper corpus rather than rediscovering them. The library implements suggestion S-0002-07 from the
t0001 brainstorm.

## Category Selection Rationale

Consulted four project categories that map directly to the design questions for this library.
`granularity-conditioning` is the central category — every paper that informs the per-turn
granularity tag and the ablation rationale lives here. `hierarchical-planning` was consulted for the
Plan-and-Solve baseline, since its prompting structure constrains the trajectory schema we emit (we
must emit records B can also emit). `uncertainty-calibration` was consulted for the `confidence`
field of the trajectory record so the Phase 2 evaluator can compute overconfident error rate.
`agent-evaluation` was consulted to confirm trajectory-level logs are what published agent
benchmarks expect to consume.

Excluded the four benchmark-specific categories (`benchmark-frontierscience`, `benchmark-workarena`,
`benchmark-swebench`, `benchmark-taubench`) because this task produces a benchmark-agnostic library.
Tool registries are explicitly out of scope (deferred to a follow-up task per
`task_description.md`). Excluded `benchmark-annotation` because the library does not depend on
annotation schemas.

## Key Findings

### ReAct Provides the Skeleton; Granularity Is the Extension

The canonical ReAct paper [Yao2022] introduces the Thought / Action / Observation loop with no
explicit notion of *scope*: every Thought is at the same conceptual level. Trajectories run until
the model emits a `Finish` action with the answer payload. The reported gains are large — **+34
absolute** success rate on ALFWorld and **+10 absolute** on WebShop versus imitation and RL
baselines — and critically these gains come from prompting alone with one or two in-context
examples, not from fine-tuning. This is the strongest published evidence that prompt-only agent
extensions can produce double-digit absolute effects, which is the empirical foundation for the
project's Phase 2 effect-size targets.

The minimal extension this task implements is a *single token* prepended to every Thought emission
(`<global>`, `<subtask>`, `<atomic>`) plus a parallel structured field in the trajectory log. The
Yao2022 prompt is otherwise reused verbatim, including the in-context exemplars convention and the
structured terminator action named `Finish`. **Hypothesis** (drawn from the gap between ReAct and
the project's three-level schema): an explicit per-Thought granularity tag will reduce off-task tool
calls and improve calibration on multi-step benchmarks without changing the underlying tool
registry.

### Plan-and-Solve as the Matched B Baseline Constrains the Trajectory Schema

[Wang2023a] introduces Plan-and-Solve prompting where the model first emits a global plan and then
executes each step. This is the project's scope-unaware (B) baseline: it has structure but no
explicit per-step granularity tag. Because t0007 (sister task) wraps Plan-and-Solve into the same
trajectory log shape, the schema we ship in t0006 is a contract for both libraries. The schema must
be expressive enough that B can emit the *same* shape with `granularity` always set to `"subtask"`
(the natural Plan-and-Solve default) while preserving turn ordering and confidence.

[Zhou2022] (least-to-most prompting) reinforces this: any "decompose then solve" prompting style
produces a tree of subgoals, and the trajectory log must capture the path actually taken. Both
[Wang2023a] and [Zhou2022] favour structured Action records over free-form text, which justifies
parsing the model's `Action:` line as JSON and validating it against a tool registry — the same
parsing pattern this library implements.

### Confidence Elicitation Is Cheap and Should Be Recorded Per Turn

[Xiong2023] systematically evaluates verbalized-confidence prompts and reports that asking the model
to emit a `Confidence: <0-100>` token per Thought adds well under one percent of token overhead and
gives a usable signal for downstream calibration. They report best-in-class
expected-calibration-error (ECE) values around **0.06-0.12** for verbalized prompts, which is
already competitive with logit-based calibration on benchmarks where logits are unavailable (closed
APIs). **Best practice**: include a `confidence` field in every trajectory record, even when the
model leaves it unset, so that downstream calibration code never has to special-case missing rows.

### Library Design: Deterministic Replay Is Required for Test Coverage

No paper in the corpus directly addresses how to *test* a ReAct-style library, but [Yao2022] reports
that ReAct trajectories are highly variable across LLM samples and that the authors used
hand-curated trajectories for their qualitative analysis. The implication for this library is that
unit tests cannot rely on a live LLM call — every test must run against pre-recorded model outputs.
This requires a `model_call` callable injection point and a deterministic-replay mode where the
callable returns successive elements of a script. This is the pattern the library exposes via the
`ScriptedModel` helper.

## Methodology Insights

* **Reuse the LangChain ReAct prompt verbatim where possible**. LangChain's ReAct prompt is
  Apache-2.0 licensed and is a near-verbatim implementation of [Yao2022]'s template; building on it
  avoids prompt-engineering rabbit-holes that are out of scope for this library task. Attribution is
  recorded in the asset's `description.md`.
* **Granularity tag injection happens at prompt-build time, not parse time**. The Thought parser
  accepts a tag-prefixed Thought, but the library *also* injects the granularity argument into the
  system prompt so the model is asked to emit the tag. Both directions are needed because some
  models will skip the tag; defaulting silently to `atomic` and logging a `tag_missing` warning is
  the documented fallback per the task description's Key Question 2.
* **Trajectory log schema must be locked before t0007 lands**. The schema is
  `{turn_index, granularity, thought, action, observation, confidence}` per record, JSONL, one
  record per turn. `granularity` is one of `"global" | "subtask" | "atomic"`. `action` is a parsed
  JSON object with `name` and `args` keys (or `{"name": "Finish", "args": {"answer": ...}}` to
  terminate). `confidence` is `float | null` in `[0, 1]` per [Xiong2023]'s normalized form (the
  paper uses 0-100; we divide by 100 at parse time).
* **Test-first against malformed JSON**. [Yao2022] reports models occasionally emit malformed Action
  lines. The library wraps `json.loads` and converts failures into a structured
  `MalformedActionError` that is logged into the trajectory's observation field as `"<parse_error>"`
  without aborting the run. The unit tests cover this path explicitly.
* **Hypothesis to test downstream (not in this task)**: A granularity-tag injection improves agent
  success on benchmarks where steps differ in scope (WorkArena++, FrontierScience-Olympiad) more
  than on benchmarks where steps are uniform (SWE-bench Verified). This is the key Phase 2
  experiment the library exists to enable.

## Gaps and Limitations

* **No paper in the corpus directly evaluates a three-level granularity tag against a two-level
  ReAct or unstructured Plan-and-Solve**. The project's main hypothesis is novel; this library is
  the substrate for the experiment that will fill that gap.
* **Confidence calibration on multi-step agent trajectories** is under-studied. [Xiong2023]
  evaluates single-question confidence; how confidence behaves across long trajectories is unknown
  and is a Phase 2 question.
* **Trajectory schema portability**. No paper proposes a canonical agent-trajectory schema. The
  schema this library defines is project-internal; future tasks may need to map it to OpenAI tool
  call format or W3C activity logs, but that is out of scope here.
* **Robustness when the model refuses to emit a tag**. [Yao2022] does not discuss tag fallbacks
  because it has no tags. The library's `default_granularity_on_missing_tag="atomic"` policy is
  pragmatic but unvalidated — Phase 2 should report how often this fallback fires.

## Recommendations for This Task

1. **Reuse LangChain's Apache-2.0 ReAct prompt and inject the granularity instruction as an
   additional system message.** [Yao2022] gives the canonical prompt; LangChain provides a
   battle-tested implementation. Acknowledge the attribution in `description.md`.
2. **Lock the trajectory schema as
   `{turn_index, granularity, thought, action, observation, confidence}` JSONL** so t0007 can emit
   identical-shape records for the matched B baseline.
3. **Default `granularity` to `"atomic"` and log a warning when the model omits the tag**, per
   [Yao2022]-style robustness practice. Phase 2 reports the fallback rate.
4. **Verbalize confidence per turn in `[0, 100]` and divide by 100 at parse time**, following
   [Xiong2023]'s prompt format. Store as `float | None` so missing values are unambiguous.
5. **Inject a `model_call` callable and ship a `ScriptedModel` deterministic helper** so unit tests
   cover tag injection, action parsing, finish detection, malformed-JSON recovery, and trajectory
   logging integrity without any live API call.
6. **Defer benchmark-specific tool registries to a follow-up task**, as the task description states.
   The library accepts an arbitrary tool registry mapping `name -> callable`.

## Paper Index

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2210.03629`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/`
* **Categories**: `granularity-conditioning`, `agent-evaluation`
* **Relevance**: Direct ancestor of the scope-aware (A) condition. Defines the Thought / Action /
  Observation loop, the in-context exemplar convention, and the `Finish[]` terminator that this
  library reuses verbatim. Headline gains (+34 ALFWorld / +10 WebShop) anchor the project's
  effect-size expectations.

### [Wang2023a]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R., Lim, E.-P.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `hierarchical-planning`
* **Relevance**: Defines the matched B baseline this library's trajectory schema must accommodate.
  Sister task t0007 wraps Plan-and-Solve into the same JSONL shape; locking the schema in t0006 is
  therefore a contract between the two libraries.

### [Zhou2022]

* **Title**: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
* **Authors**: Zhou, D., Schärli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui,
  C., Bousquet, O., Le, Q., Chi, E.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2205.10625`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2205.10625/`
* **Categories**: `hierarchical-planning`
* **Relevance**: Reinforces that decompose-then-solve prompting is a tree of subgoals. The
  trajectory log must capture the path actually taken, not the abstract subgoal tree, which is the
  motivation for the linear JSONL `turn_index` schema.

### [Xiong2023]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2306.13063`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/`
* **Categories**: `uncertainty-calibration`
* **Relevance**: Justifies the per-turn `confidence` field in the trajectory schema. Reports ECE
  around 0.06-0.12 for verbalized confidence prompts, with negligible token overhead. Used to decide
  on the 0-100 input format and the normalized `[0, 1]` storage form.
