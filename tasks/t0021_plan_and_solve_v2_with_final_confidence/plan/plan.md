---
spec_version: "2"
task_id: "t0021_plan_and_solve_v2_with_final_confidence"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Plan-and-Solve v2 with final_confidence Field

## Objective

Ship a new registered library `scope_unaware_planandsolve_v2` that wraps the existing v1
Plan-and-Solve agent (from task t0007) and emits a verbalized `final_confidence` field on every
trajectory it returns, following the Xiong et al. 2024 section 3.2 protocol. Prove the field is
wired end-to-end by running a 5-row × 3-condition smoke on FrontierScience-Olympiad with
`claude-haiku-4-5` and observing a non-zero, non-degenerate value for Metric 2
(`overconfident_error_rate`). Done = library asset passes verification, unit tests pass, smoke
validation produces non-degenerate Metric 2, and total spend stays under $1.

## Task Requirement Checklist

The operative task request from
`tasks/t0021_plan_and_solve_v2_with_final_confidence/task_description.md`:

> Extend the existing `tasks/t0007_*/code/` library so that every trajectory record produced by
> `scope_unaware_planandsolve_v1` carries a `final_confidence` field in the range [0.0, 1.0],
> populated by a verbalized confidence call following the Xiong2024 section 3.2 protocol. The new
> `final_confidence` field must be emitted by all three conditions (A scope-aware, B scope-unaware,
> C scope-mismatched) so paired analysis is well-defined.

The decomposed requirements:

* **REQ-1**: Ship a registered library asset at `assets/library/scope_unaware_planandsolve_v2/` with
  `details.json`, canonical description document, and source under `files/`. Evidence:
  `verify_library_asset` reports zero errors.
* **REQ-2**: Provide a v2 entry point that always emits `final_confidence` on the result. Evidence:
  unit test that asserts the field is present in `AgentResultV2.final_confidence` and
  `TrajectoryRecordV2.final_confidence` after every run.
* **REQ-3**: Keep the v1 entry point unchanged and importable; the v1 module file in t0007 is not
  edited, and v2 imports v1 symbols. Evidence: unit test that imports v1 and checks the legacy
  schema is unchanged.
* **REQ-4**: Implement the Xiong2024 §3.2 verbalized confidence protocol via a separate prompt
  issued after the answer, including the verbatim phrasing and 0/0.5/1 anchor language. Evidence:
  the prompt template at `assets/library/.../files/prompts/confidence_prompt.txt` contains the
  verbatim phrasing; description doc cites Xiong2024 §3.2.
* **REQ-5**: Parse the confidence with a strict regex; retry once on failure with a stricter prompt;
  on second failure write `None` and increment `AgentResultV2.final_confidence_parse_failures`.
  Evidence: unit tests for parse-success, single retry, and double-failure paths.
* **REQ-6**: Validate `final_confidence` lies in `[0.0, 1.0]` whenever non-`None`. Evidence: unit
  test with adversarial parse output.
* **REQ-7**: Emit `final_confidence` for **all three** conditions (A scope-aware ReAct, B
  scope-unaware Plan-and-Solve, C matched-mismatch). Evidence: smoke run JSONL has non-`null`
  `final_confidence` on every row in every condition (modulo parse failures recorded as `null`).
* **REQ-8**: Run a 5-row × 3-condition smoke on FrontierScience-Olympiad rows with
  `claude-haiku-4-5` and write per-condition Metric 2 values to `results/metrics.json`. Evidence:
  `metrics.json` contains three Metric 2 values, at least one is non-zero and non-1.
* **REQ-9**: Keep total cost under $1. Evidence: `results/costs.json` shows
  `total_cost_usd <= 1.00`.
* **REQ-10**: If parse failure rate > 20% on haiku, document it and tighten the prompt or move to
  JSON mode. Evidence: smoke run reports parse-failure rate; description doc and step log
  acknowledge any tightening.

Steps 1-3 satisfy REQ-1 through REQ-7. Step 4 satisfies REQ-7, REQ-8, REQ-9, REQ-10. Step 5 gathers
final outputs.

## Approach

The v2 library composes the v1 agent rather than rewriting it. Key decisions, with research
grounding from `research/research_code.md`:

* **Compose, don't fork.** The v1 module is stable and used by t0010's matched-mismatch agent;
  editing it risks breaking t0010. v2 imports `PlanAndSolveAgent`, `parse_plan`,
  `_parse_executor_output`, and prompt templates from
  `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` and runs them unchanged.
* **Add `final_confidence` at the result level.** v1's per-step `confidence` slot is unused. v2
  introduces a parallel `TrajectoryRecordV2` (six v1 fields plus `final_confidence`) and an
  `AgentResultV2(final_answer, trajectory, plan, final_confidence, final_confidence_parse_failures)`.
  The smoke harness reads `AgentResultV2.final_confidence` directly into the per-row JSONL slot.
* **Two-call protocol via prompt-level conversation reconstruction.** The v1 model-call shape is
  `Callable[[str], str]` with no chat memory. The confidence call therefore reconstructs the
  conversation in its prompt: "Question: …\nFinal Answer: …\nConfidence (0-1): …". This honors the
  Xiong2024 spirit (model rates its own answer without revising it) without requiring a stateful
  API.
* **Strict regex parse, single retry.** Match `\b(0(?:\.\d+)?|1(?:\.0+)?)\b` and pick the last
  match. On no match, retry once with a stricter prompt asking only for a single number on its own
  line. On second failure, set `final_confidence=None` and increment
  `final_confidence_parse_failures`.
* **All three conditions carry the field.** Condition A (scope-aware ReAct from t0006) and Condition
  C (matched-mismatch from t0010) are wrapped by the same `elicit_final_confidence(...)` helper so
  the field is present everywhere. This avoids three separate confidence implementations.

**Alternative considered**: editing the v1 module in place to add the field. Rejected because t0010
imports symbols from v1 and a structural change would either break t0010 or require coordinating
edits across two completed task folders, which the immutability rule forbids. A new v2 library is
the only ARF-compliant option.

**Task type**: `write-library`. Per `meta/task_types/write-library/`, this requires producing a
registered asset under `assets/library/<id>/` with `details.json`, a canonical description, and
source code; that requirement shaped the deliverable structure.

## Cost Estimation

Smoke run on `claude-haiku-4-5`: 5 rows × 3 conditions × ~3 calls each (plan + execute + confidence,
with ReAct potentially needing more turns) ≈ 50 calls. Haiku input ~4k tokens × 50 ≈ 200k input
tokens at ~$1/M input ≈ $0.20. Output ~300 tokens × 50 ≈ 15k output tokens at ~$5/M output ≈ $0.08.
Plus haiku judge calls (5 rows × 3 conditions = 15 judge calls × ~~2k tokens) ≈ $0.04. Estimated
total **~~$0.32**, hard cap **$1.00** enforced by `CostTracker.is_budget_ok(headroom_usd=0.05)` in
`code/run_smoke.py`. All other costs are $0 (no remote compute, datasets are local).

## Step by Step

1. **Copy non-library helpers into the task.** Copy
   `tasks/t0012_phase2_abc_smoke_frontierscience/code/model_call.py` to
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/model_call.py` (provides
   `make_model_call`, `CostTracker`). Copy
   `tasks/t0011_metric2_calibration_aggregator/code/calibration.py` to
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/calibration.py` (provides
   `compute_overconfident_error_rate`, `CalibrationRecord`, `HIGH_CONFIDENCE_THRESHOLD`). No
   adaptation needed beyond keeping the same imports. Satisfies REQ-8, REQ-9.

2. **Write the v2 library code.** Create
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py`. It must:
   * Import v1 symbols from `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve`
     (`PlanAndSolveAgent`, `parse_plan`, `_parse_executor_output`, `PLAN_PROMPT_TEMPLATE`,
     `EXECUTE_PROMPT_TEMPLATE`, `MalformedPlanError`).
   * Define `CONFIDENCE_PROMPT_TEMPLATE` with the verbatim Xiong2024 §3.2 phrasing on a separate
     line, including 0/0.5/1 anchor language.
   * Define `parse_final_confidence(text: str) -> float | None` using regex
     `\b(0(?:\.\d+)?|1(?:\.0+)?)\b` taking the last match; clamp to `[0.0, 1.0]`.
   * Define `TrajectoryRecordV2` (frozen dataclass): six v1 fields plus
     `final_confidence: float | None`.
   * Define
     `AgentResultV2(final_answer, trajectory, plan, final_confidence, final_confidence_parse_failures)`
     (frozen dataclass).
   * Define
     `elicit_final_confidence(model_call, question, final_answer) -> tuple[float | None, int]`:
     issue confidence call; on parse failure issue one stricter retry; return
     `(value, parse_failures_count)` where count is 0, 1, or 2.
   * Define `PlanAndSolveAgentV2(model_call, max_turns=12)` with `run(problem) -> AgentResultV2`:
     run v1 agent to produce final answer + trajectory, then call `elicit_final_confidence`, attach
     the value to a finishing `TrajectoryRecordV2`, and return `AgentResultV2`. Satisfies REQ-2,
     REQ-4, REQ-5, REQ-6.

3. **Write unit tests.** Create
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/test_planandsolve_v2.py` using the v1
   `ScriptedModel`. Tests:
   * `test_parse_final_confidence_success` — regex picks the last numeric value in `[0,1]`.
   * `test_parse_final_confidence_clamp` — values outside `[0,1]` clamp to bounds (or return None).
   * `test_parse_final_confidence_failure` — non-numeric text returns None.
   * `test_run_emits_field_when_parse_succeeds` — scripted model returns confidence "0.8";
     `final_confidence == 0.8`, `final_confidence_parse_failures == 0`.
   * `test_run_emits_null_when_parse_fails` — scripted model returns "I'm pretty sure" twice;
     `final_confidence is None`, `final_confidence_parse_failures == 2`.
   * `test_run_retries_once_on_first_failure` — scripted model returns "uncertain" then "0.6";
     `final_confidence == 0.6`, `final_confidence_parse_failures == 1`.
   * `test_v1_legacy_schema_unchanged` — import v1 `AgentResult` and verify it has fields
     `(final_answer, trajectory, plan)` and not `final_confidence`.
   * `test_trajectory_record_v2_has_field` — `TrajectoryRecordV2` exposes the seven expected fields.
     Run with `uv run pytest tasks/t0021_*/code/ -v` and require zero failures. Satisfies REQ-2,
     REQ-3, REQ-5, REQ-6.

4. **Build and run the smoke validation.** Create
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/code/run_smoke.py`. It must:
   * Load 5 rows from
     `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`
     filtered by `benchmark == "FrontierScience-Olympiad"` and `hierarchy_completeness == True`.
   * Initialize a `CostTracker(headroom_usd=0.05)` against a $1.00 hard budget.
   * For each of three conditions A/B/C run a per-row agent and the v2 confidence post-call:
     * **A** uses a chain-of-thought prompt-only call (single `model_call(...)` with a CoT-style
       instruction); confidence is elicited by `elicit_final_confidence` afterwards.
     * **B** uses `PlanAndSolveAgentV2.run(...)`.
     * **C** uses `MatchedMismatchAgent.run(...)` from
       `tasks.t0010_matched_mismatch_library.code.matched_mismatch` followed by
       `elicit_final_confidence`.
   * Write per-row JSONL with the t0012 schema (top-level `final_confidence`, `trajectory`,
     `final_answer`, `is_correct`, etc.) to
     `tasks/t0021_plan_and_solve_v2_with_final_confidence/results/smoke_predictions.jsonl`.
   * Issue a haiku judge call for each row with the t0012 `JUDGE_PROMPT_TEMPLATE` to set
     `is_correct`.
   * Compute `overconfident_error_rate` per condition with the copied calibration module.
   * Compute `final_confidence_parse_failure_rate = total_failures / (3 * 5)`.
   * **Validation gate**: trivial baseline = 0.0 (the t0012 result for B/C). If smoke Metric 2 on B
     is exactly 0.0 with all rows wrong, halt and inspect haiku confidence outputs row-by-row before
     declaring success. Use `--limit 1` first to validate the pipeline end-to-end before the full
     N=5 run. Satisfies REQ-7, REQ-8, REQ-9, REQ-10.

5. **Register the library asset.** Write
   `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/details.json`
   with `spec_version="2"`, `library_id="scope_unaware_planandsolve_v2"`, name, version "1", short
   description, `description_path="description.md"`,
   `module_paths=["tasks/t0021_plan_and_solve_v2_with_final_confidence/code/planandsolve_v2.py"]`,
   `entry_points` listing `PlanAndSolveAgentV2.run`, `parse_final_confidence`, etc.,
   `dependencies=["scope_unaware_planandsolve_v1"]`, categories,
   `created_by_task="t0021_plan_and_solve_v2_with_final_confidence"`, `date_created="2026-05-01"`.
   Write `description.md` with YAML frontmatter and the eight canonical sections (Metadata,
   Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary). Cite
   Xiong2024 §3.2. Copy the verbatim prompt to `files/prompts/confidence_prompt.txt`. Run
   `uv run python -m arf.scripts.verificators.verify_library_asset tasks/t0021_*/assets/library/scope_unaware_planandsolve_v2`
   and require zero errors. Satisfies REQ-1, REQ-4.

## Remote Machines

None required. Local-only task using the `claude` CLI for `claude-haiku-4-5`.

## Assets Needed

* **Library**: `scope_unaware_planandsolve_v1` (registered, t0007) — imported.
* **Library**: `matched_mismatch_v1` (registered, t0010) — imported.
* **Dataset**: FrontierScience-Olympiad rows from t0009 hierarchical annotation v2 dataset —
  read-only from
  `tasks/t0009_hierarchical_annotation_v2/assets/dataset/hierarchical-annotation-v2/files/hierarchical_annotation_v2.jsonl`.
* **Code (copied)**: `model_call.py` from t0012 and `calibration.py` from t0011 — copied into
  `code/`.
* **Paper**: Xiong et al. 2024 — cited (no asset to download; exact §3.2 phrasing comes from the
  task description).

## Expected Assets

* **Library** × 1: `scope_unaware_planandsolve_v2` at
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2/`
  with `details.json`, `description.md`, and `files/prompts/confidence_prompt.txt`. Implements
  Plan-and-Solve with verbalized `final_confidence` per Xiong2024 §3.2. This matches
  `expected_assets.library = 1` in `task.json`.

## Time Estimation

* Implementation + unit tests: 30 min
* Library asset registration + verification: 15 min
* Smoke validation (5 × 3 + judge calls, network bound): 15 min
* Results, suggestions, reporting: 20 min

Total: ~80 min wall clock.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Haiku confidence parse failure rate > 20% | Medium | Blocks shipping (REQ-10) | Stricter retry prompt explicitly demanding "a single number 0-1 on its own line"; if still > 20%, document and tighten further |
| All 5 smoke rows correct → Metric 2 trivially 0 | Low | Cannot validate Metric 2 wiring | Smoke is on FrontierScience-Olympiad where t0012 saw 0/40 correct for B; haiku is unlikely to suddenly become accurate |
| Haiku confidence flat at 0.5 → Metric 2 trivially 0 | Medium | Validates "field wired" but Metric 2 doesn't move | Document as "haiku flat distribution risk" per task brief; the field still works (REQ-7), and t0023's sonnet run will exercise the metric |
| `claude` CLI cost spike | Low | Budget breach | `CostTracker.is_budget_ok(headroom_usd=0.05)` halts before `$1.00`; smoke is preceded by a `--limit 1` dry-run |
| t0010 matched-mismatch import breaks after v2 module ships | Low | Breaks Condition C | v2 does not edit v1; unit test imports v1 symbols and asserts the legacy schema; smoke directly calls `MatchedMismatchAgent` |
| Library verificator rejects asset structure | Medium | Blocks REQ-1 | Read `meta/asset_types/library/specification.md` first; run verificator iteratively on the asset folder until clean |

## Verification Criteria

* **Unit tests pass**: run
  `uv run python -m arf.scripts.utils.run_with_logs --task-id t0021_plan_and_solve_v2_with_final_confidence -- uv run pytest tasks/t0021_plan_and_solve_v2_with_final_confidence/code/ -v`
  and observe `0 failed` plus all REQ-2/3/5/6 tests passing.
* **Library asset verifies**: run
  `uv run python -m arf.scripts.verificators.verify_library_asset tasks/t0021_plan_and_solve_v2_with_final_confidence/assets/library/scope_unaware_planandsolve_v2`
  and observe zero errors. Confirms REQ-1.
* **Smoke produces non-degenerate Metric 2**: open
  `tasks/t0021_plan_and_solve_v2_with_final_confidence/results/metrics.json` and confirm at least
  one of the three conditions has `0.0 < overconfident_error_rate < 1.0`. Confirms REQ-7, REQ-8.
* **Cost under $1**: open `tasks/t0021_plan_and_solve_v2_with_final_confidence/results/costs.json`
  and confirm `total_cost_usd <= 1.00`. Confirms REQ-9.
* **Parse failure rate documented**: smoke output JSON contains
  `final_confidence_parse_failure_rate`; if > 0.20 the description doc has been tightened. Confirms
  REQ-10.
* **All conditions emit the field**: open `results/smoke_predictions.jsonl` and confirm each row has
  a `final_confidence` value (or a recorded null with a parse-failure flag). Confirms REQ-7.
* **Markdown and Python pass quality checks**: `uv run flowmark --inplace --nobackup` on every
  edited markdown; `uv run ruff check --fix . && uv run ruff format .` and
  `uv run mypy -p tasks.t0021_plan_and_solve_v2_with_final_confidence.code` exit 0.
