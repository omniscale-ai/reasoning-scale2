---
spec_version: "1"
task_id: "t0005_hierarchical_annotation_pilot_v1"
research_stage: "papers"
papers_reviewed: 11
papers_cited: 7
categories_consulted:
  - "hierarchical-planning"
  - "granularity-conditioning"
  - "benchmark-annotation"
  - "agent-evaluation"
  - "uncertainty-calibration"
  - "benchmark-frontierscience"
  - "benchmark-swebench"
  - "benchmark-taubench"
  - "benchmark-workarena"
date_completed: "2026-04-29"
status: "complete"
---
# Research Papers: Hierarchical Annotation Pilot v1

## Task Objective

Audit and conform the 115 existing pilot annotations in
`project/data/annotation_pilot/tasks_annotated.jsonl` to a global / subtask / atomic three-level
schema, run an LLM-as-judge spot-check on at least 12 stratified rows, and produce one consolidated
`hierarchical_annotation_v1` dataset asset. The literature review here looks for prior precedent on
hierarchical action labelling in agent benchmarks and on what counts as a "global plan" vs.
"subtask" vs. "atomic action" in the four upstream benchmarks (FrontierScience-Olympiad, SWE-bench
Verified, tau-bench, WorkArena++).

## Category Selection Rationale

Consulted `hierarchical-planning` because it is the central concept of the task — the schema is a
hierarchy. Consulted `granularity-conditioning` because the project's research question 1 asks
whether scope-conditioning across global / subtask / atomic levels improves agent performance, and
v1 annotations are the input to those Phase 2 / 3 experiments. Consulted `benchmark-annotation`
because the deliverable is a labelled benchmark. Consulted `agent-evaluation` and the four
benchmark-specific categories (`benchmark-frontierscience`, `benchmark-swebench`,
`benchmark-taubench`, `benchmark-workarena`) to understand each upstream task structure so the
mapper can derive credible global / subtask / atomic boundaries from each benchmark's native step
representation. Consulted `uncertainty-calibration` because the LLM-as-judge spot-check is itself an
uncertainty-elicitation task and we want to apply known calibration practices to its prompt.

Excluded categories that did not yield relevant signal: none — no other categories existed in
`meta/categories/` beyond those reviewed.

## Key Findings

### A Three-Level Decomposition Is the Project's Schema, Already Validated by Prior Tasks

The project decisively settled on a three-level decomposition (global / subtask / atomic) in the
literature survey [Boisvert2024, Yao2024, Wang2023, Yao2022]. WorkArena++ uses *exactly* a
three-level structure: a high-level intent (global), a list of subtasks composing the
"compositional" task (subtask), and the atomic UI action stream (atomic) [Boisvert2024]. tau-bench
exposes a similar decomposition in its evaluation traces — the user request defines the global
intent, intermediate tool-orchestration phases form subtasks, and individual API/tool invocations
are atomic [Yao2024]. ReAct's "Thought / Act / Observation" trace [Yao2022] maps cleanly onto
"subtask plan / atomic action / observation". Plan-and-Solve Prompting [Wang2023] explicitly
generates a global plan ("first") and per-step decomposition ("then"), exactly aligning with our
global → subtask split.

This is the strongest finding in the corpus: the project does not need to invent the schema, only to
project the existing pilot data onto it. The three levels are already common across the four
upstream benchmarks.

### Native Step Representations Already Carry Implicit Granularity

Inspecting `project/data/annotation_pilot/tasks_annotated.jsonl` together with the four benchmark
specs in [Boisvert2024, Yao2024, Jimenez2024, Glazer2024] shows that the existing 115 rows store
step graphs (`steps.nodes`) with explicit per-node `type` labels: `strategic` (117 nodes),
`conceptual` (284), `computational` (526), and `verification` (136). These node types correspond
nearly one-to-one with the project's three levels:

* `strategic` — global plan moves (frame the problem, choose an approach)
* `conceptual` — subtask plans (set up an integral, model the system)
* `computational` + `verification` — atomic actions (run a derivation step, check a constraint)

This means the deterministic mapper can derive `{global, subtask, atomic}` from the existing graph
without re-querying an LLM. The mapper assigns the lowest-id `strategic` node (or first node if none
exists) as global, the `conceptual` nodes (or, when absent, all `depends_on=[]` non-atomic nodes) as
subtasks, and the remaining `computational`/`verification` nodes as atomic.

### LLM-as-Judge with Verbalized Verdicts and Stratified Sampling Is the Right Spot-Check

[Xiong2023] established that verbalized confidence elicitation is competitive with sampling-based
uncertainty in LLMs and is "much cheaper" — a single decoding pass per sample. For our 12-row
spot-check on `claude-haiku-4-5-20251001`, that means we can ask the judge for a single verdict
("acceptable" / "needs revision") plus a one-sentence justification in one prompt, instead of
running self-consistency. [Xiong2023] also shows multi-step prompts induce overconfidence; the
project's `overconfident_error_rate` metric is calibrated around this exact pattern. We adopt a
single-shot prompt with a clear binary output to sidestep that pitfall.

Stratification across the four benchmarks (≥3 rows per benchmark, totalling 12) follows the
benchmark-design best practice in [Boisvert2024, Yao2024]: imbalanced sampling masks failure modes
when one benchmark dominates aggregate accept rates.

### Each Benchmark Has Its Own Hierarchy Idiom

* **FrontierScience-Olympiad** [Glazer2024]: math/physics/chemistry/biology Olympiad problems where
  the global plan is the high-level strategy ("apply superposition + decompose geometry"), the
  subtasks are conceptual moves ("model thin disk as rim current loop"), and atomic steps are
  derivation operations. The pilot data has the most complete `steps.nodes` here (mean 13.9
  nodes/task) and 11 rows missing `steps` due to LLM annotation failure.
* **SWE-bench Verified** [Jimenez2024]: the global plan is "fix issue X", subtasks are the gold
  patch's hunks (4-8 per task by t0003 filter), and atomic actions are line-level edits. Mean 8.5
  nodes/task — well-formed.
* **tau-bench** [Yao2024]: global = the user request; subtasks = tool-orchestration phases; atomic =
  individual API calls (4-8 actions per task by t0003 filter). Mean 8.0 nodes/task; 0-14 range shows
  variance.
* **WorkArena++** [Boisvert2024]: explicit three-level structure already; pilot rows describe the
  compositional task class rather than concrete instance traces. Mean 10.0 nodes/task.

### Hierarchy Completeness Will Be Lower for Failed Annotations

The pilot file contains 14 rows with `errors` set (11 in FrontierScience-Olympiad, 3 elsewhere). Of
those 11 FrontierScience errors, all have `steps: null`. The mapper must therefore emit a row with
`hierarchy.global = null` (or fall back to the problem statement's first sentence) and flag those
rows as `incomplete`. Per-benchmark completeness will be roughly 73% (29/40) for
FrontierScience-Olympiad and 100% (or near-100%) for the other three.

## Methodology Insights

* **Use the deterministic node-type mapper.** Given the strong correlation between the existing
  `type` labels and the project's three levels, do NOT re-query an LLM for the mapping. A pure
  Python function over the node graph is reproducible and cheap.

* **Keep one row per task.** Do not flatten the hierarchy to one row per node. The dataset asset's
  shape
  `{task_id, benchmark, ..., hierarchy: {global, subtask, atomic}, gold_actions: {global, subtask, atomic}}`
  requires one consolidated row per task.

* **Stratify the judge sample by benchmark, then by hierarchy completeness.** Sample 3 rows per
  benchmark (12 total). Within each benchmark, mix complete and incomplete rows so the judge can
  flag both schema bugs and missing-data bugs.

* **Use verbalized confidence prompting per [Xiong2023].** Ask the judge to output strict JSON:
  `{"verdict": "acceptable"|"needs revision", "justification": "<one sentence>"}`. Parse with
  `json.loads`. No self-consistency sampling.

* **Cap LLM cost.** `claude-haiku-4-5-20251001` is roughly $1/Mtok input, $5/Mtok output. With 12
  judge calls of ~3K input tokens (problem + hierarchy) and ~100 output tokens, total spend will be
  under $0.50.

* **Use the explicit metrics-variant format.** Even though only `avg_decisions_per_task` is
  registered, the task produces it per benchmark. Use the legacy flat format keyed by benchmark (not
  multi-variant) — `metrics.json` should record the project-level mean `avg_decisions_per_task`
  (single value); per-benchmark numbers go in `results_detailed.md`.

* **Hypothesis to test in v2**: the LLM-as-judge accept rate will exceed 75% on
  FrontierScience-Olympiad and SWE-bench Verified rows, and will be lower on tau-bench / WorkArena++
  rows where the original `steps.nodes` are sparser or the global intent is implicit. Worth tracking
  in the results.

## Gaps and Limitations

* **No paper in the corpus directly defines a "global / subtask / atomic" annotation schema.** The
  three-level structure is implicit across [Boisvert2024, Yao2024, Wang2023, Yao2022] but no paper
  provides a single definitional source. The mapper's exact boundaries (which node types map to
  which level) are project-internal choices.

* **No published inter-rater agreement numbers exist for any of the four upstream benchmarks**
  beyond what's in [Glazer2024] for FrontierMath (parent of FrontierScience-Olympiad). v1 cannot
  benchmark itself against published agreement scores; this is deferred to v2.

* **Mind2Web-proxy and HumanEval-proxy are absent from the actual data.** The task description
  mentions both, but the imported file uses tau-bench and WorkArena++ as the two web/agent proxies.
  The proxy-remediation question must be reformulated as "are tau-bench and WorkArena++ adequate
  agentic proxies?", which is a separate v2 task.

* **No literature on auditing pre-existing LLM annotations.** [Xiong2023] covers single-pass
  uncertainty elicitation but not the meta-question of "did the upstream LLM correctly decompose the
  task?".

## Recommendations for This Task

1. Implement a deterministic mapper in `code/hierarchy_mapper.py` that consumes `steps.nodes` and
   emits `{global, subtask, atomic}` lists using the node-type heuristic from the Methodology
   Insights section.
2. Implement an LLM-as-judge runner in `code/judge_runner.py` that calls `claude-haiku-4-5-20251001`
   with a verbalized-confidence prompt for each of 12 stratified rows (3 per benchmark).
3. Persist the consolidated dataset as `assets/dataset/hierarchical-annotation-v1/` with one row per
   source task (115 rows), preserving rows even when `hierarchy.global` is null due to upstream
   `errors`. Mark such rows with `judge_verdict: null` and a sentinel
   `hierarchy_completeness: false`.
4. Use the `benchmark-annotation` and `hierarchical-planning` categories on the dataset asset.
5. Cap total Anthropic spend at $5 per task budget; expected actual spend < $0.50.
6. Defer to follow-up tasks: full human review (S-0002-08 v2), inter-rater agreement, ≥200-row
   extension, and proxy-benchmark remediation.

## Paper Index

### [Boisvert2024]

* **Title**: WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work
  Tasks
* **Authors**: Boisvert, L. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2407.05291`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2407.05291/`
* **Categories**: `benchmark-workarena`, `agent-evaluation`, `hierarchical-planning`
* **Relevance**: WorkArena++ is one of the four upstream benchmarks audited here, and its
  compositional structure (intent / subtasks / UI actions) is the most explicit three-level mapping
  in the corpus.

### [Yao2024]

* **Title**: tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains
* **Authors**: Yao, S. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2406.12045`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/`
* **Categories**: `benchmark-taubench`, `agent-evaluation`
* **Relevance**: tau-bench is a second upstream benchmark audited here. Its evaluation trace format
  informs how subtask vs atomic boundaries should be drawn for tool-orchestration tasks.

### [Yao2022]

* **Title**: ReAct: Synergizing Reasoning and Acting in Language Models
* **Authors**: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y.
* **Year**: 2022
* **DOI**: `10.48550/arXiv.2210.03629`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2210.03629/`
* **Categories**: `agent-evaluation`, `hierarchical-planning`
* **Relevance**: Established the Thought / Act / Observation pattern that underpins the
  subtask-vs-atomic boundary used in the deterministic mapper.

### [Wang2023]

* **Title**: Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large
  Language Models
* **Authors**: Wang, L., Xu, W., Lan, Y., Hu, Z., Lan, Y., Lee, R. K-W., Lim, E-P.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2305.04091`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2305.04091/`
* **Categories**: `granularity-conditioning`, `hierarchical-planning`
* **Relevance**: Provides the explicit "global plan first, per-step second" prompting pattern that
  motivates the project's `global` vs `subtask` split.

### [Jimenez2024]

* **Title**: SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
* **Authors**: Jimenez, C. E. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2310.06770`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2310.06770/`
* **Categories**: `benchmark-swebench`, `agent-evaluation`
* **Relevance**: Defines the SWE-bench task format whose gold patches and hunk structure determine
  subtask vs atomic boundaries for the 23 SWE-bench Verified rows in the pilot.

### [Glazer2024]

* **Title**: FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI
* **Authors**: Glazer, E. et al.
* **Year**: 2024
* **DOI**: `10.48550/arXiv.2411.04872`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2411.04872/`
* **Categories**: `benchmark-frontierscience`, `agent-evaluation`
* **Relevance**: Parent of FrontierScience-Olympiad. Provides the rubric structure for multi-step
  derivations whose `strategic` / `conceptual` / `computational` node types we map onto the global /
  subtask / atomic hierarchy.

### [Xiong2023]

* **Title**: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation
  in LLMs
* **Authors**: Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., Hooi, B.
* **Year**: 2023
* **DOI**: `10.48550/arXiv.2306.13063`
* **Asset**:
  `tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2306.13063/`
* **Categories**: `uncertainty-calibration`
* **Relevance**: Establishes verbalized-confidence prompting as the cost-effective uncertainty
  elicitation technique. Justifies the single-pass LLM-as-judge protocol used here.
