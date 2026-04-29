---
spec_version: "2"
task_id: "t0010_matched_mismatch_library"
date_completed: "2026-04-29"
status: "complete"
---
# Plan — Matched-Mismatch Library (Condition C)

## Objective

Implement the project's condition-C library: a `MatchedMismatchAgent` wrapper that walks the v2
hierarchy from t0009 in canonical phase order, determines the *correct* granularity tag at each step
from the annotation, and substitutes a *deliberately incorrect* tag according to a
`mismatch_strategy: "random" | "adversarial"` parameter. The wrapper delegates the actual model call
to either `scope_aware_react_v1` (t0006) or `scope_unaware_planandsolve_v1` (t0007), reuses t0007's
canonical `TRAJECTORY_RECORD_FIELDS` schema unchanged, and exposes deterministic-test mode via
`ScriptedModel`. "Done" means: (a) the library asset under `assets/library/matched_mismatch_v1/`
exists and passes `verify_library_asset`, (b) the test suite passes, and (c) every `REQ-*` checklist
item below is satisfied with explicit traceability in `results/results_detailed.md`.

## Task Requirement Checklist

The operative task request from `task.json`:

> **Name**: Matched-mismatch library: condition C with deliberately wrong granularity tags
>
> **Short description**: Write-library implementing condition C: wrap scope_unaware_planandsolve_v1
> with a tag-classifier that assigns deliberately incorrect granularity tags.
>
> **Long description** (`task_description.md`): Implement a `MatchedMismatchAgent` class accepting a
> problem statement, an annotation tree (the v2 hierarchy from t0009), a tool registry, a model-call
> callable, and a `mismatch_strategy: "random" | "adversarial"`; walk the hierarchy in phase order;
> assign an incorrect tag according to the strategy; delegate each step to either
> `scope_aware_react_v1` or `scope_unaware_planandsolve_v1`; emit trajectory records carrying the
> wrong `granularity` tag with the correct tag in `_correct_granularity` extras; support
> deterministic-test mode; provide pytest coverage covering random-strategy uniformity,
> adversarial-strategy correctness, schema parity with t0007, end-to-end runs with both delegates;
> produce `assets/library/matched_mismatch_v1/{details.json, description.md}` and
> `tasks/t0010_matched_mismatch_library/code/{matched_mismatch.py, test_matched_mismatch.py}`.

Concrete requirements:

* **REQ-1**: `MatchedMismatchAgent` class accepts `problem`, `annotation`, `tool_registry`,
  `model_call`, `mismatch_strategy`, and a delegate selector. Satisfied by step 1
  (`code/ matched_mismatch.py`); evidence: `_test_constructor_signature` and end-to-end tests pass.
* **REQ-2**: Phase-ordered walk over the v2 hierarchy
  (`global → for each subtask: (subtask, atomics) → global_atomics`). Satisfied by step 1
  (`iter_phases` iterator); evidence: `test_phase_order` reproduces the canonical sequence on a
  fixture annotation.
* **REQ-3**: `random` strategy picks uniformly from `{global, subtask, atomic} \ correct_tag`.
  Satisfied by step 1 (`pick_mismatch_tag`); evidence: `test_random_strategy_uniformity` confirms
  every wrong tag appears across N=300 trials and the correct tag never appears.
* **REQ-4**: `adversarial` strategy picks the most distant tag (`global → atomic`,
  `atomic → global`, `subtask → atomic`). Satisfied by step 1 (`ADVERSARIAL_MAP`); evidence:
  `test_adversarial_strategy_correctness` covers all three correct-tag cases.
* **REQ-5**: Schema parity with t0007's `TRAJECTORY_RECORD_FIELDS`. Satisfied by step 1
  (`from tasks.t0007_…import TRAJECTORY_RECORD_FIELDS` and a module-level `assert`); evidence:
  `test_trajectory_schema_parity_with_t0007`.
* **REQ-6**: Trajectory records carry the *wrong* tag in `granularity` and the correct tag in
  `extras["_correct_granularity"]`. Satisfied by step 1 (`MatchedMismatchRecord` extends the t0007
  schema with a `extras: dict[str, str]` field that survives JSON round-trips); evidence:
  `test_records_carry_wrong_tag_with_correct_tag_in_extras`.
* **REQ-7**: Wrapper delegates to either `ScopeAwareReactAgent` (t0006) or `PlanAndSolveAgent`
  (t0007), with the wrapper controlling only the granularity tag. Satisfied by step 1 (`Delegate`
  enum + adapter functions); evidence: two end-to-end tests using each delegate.
* **REQ-8**: Deterministic-test mode using t0007's `ScriptedModel`. Satisfied by step 2
  (`code/test_matched_mismatch.py` imports `ScriptedModel` from t0007 and t0006); evidence: tests
  run with no API keys and no network access.
* **REQ-9**: Library asset `assets/library/matched_mismatch_v1/` with `details.json` and
  `description.md` per spec. Satisfied by steps 3-4; evidence: `verify_library_asset` passes.
* **REQ-10**: `global_atomics` handling — treat as `atomic` for the mismatch policy. Satisfied by
  step 1 (`_phase_to_correct_tag` maps `global_atomics` → `atomic`); evidence:
  `test_global_atomics_treated_as_atomic`.

## Approach

**Task type**: `write-library`. Per the type's planning guidelines, the public API is fixed before
coding (see REQ-1 / REQ-7), tests live in `code/test_*.py`, and the library asset folder contains
only metadata + documentation while the code lives in `code/`.

**Design**: One module `code/matched_mismatch.py` with: (a) public `MismatchStrategy` literal type
and `Delegate` literal type, (b) public `MatchedMismatchAgent` dataclass with a
`run(problem, annotation)` method, (c) public `iter_phases(annotation)` iterator that walks the v2
tree in canonical phase order yielding `(phase_kind, correct_granularity_tag, payload)` tuples, (d)
public `pick_mismatch_tag(correct_tag, strategy, rng)` function, (e) public `MatchedMismatchRecord`
dataclass extending the t0007 schema with an `extras: dict[str, str]` field, and (f) module-level
`ADVERSARIAL_MAP` and `GRANULARITY_VALUES` constants. The wrapper delegates each phase's *model
call* to the chosen delegate (t0006 or t0007), substituting the wrong granularity tag *after* the
delegate runs but *before* the trajectory record is emitted — this keeps the delegate's
prompt-construction logic untouched and isolates the mismatch perturbation to the logged tag. Per
[Wang2023] and [Yao2022] (see `research/research_papers.md`), this is the correct way to isolate the
granularity-mismatch effect from delegate-specific reasoning effects.

**Alternative considered & rejected**: pre-rewriting the prompt the delegate receives (so the
delegate itself believes it is operating under the wrong granularity). Rejected because it requires
intimate knowledge of each delegate's prompt structure, breaks encapsulation, and conflates the
"what the model sees" axis with the "what we log" axis. Per [Shinn2023]'s mismatched-context
ablation, the cleaner experimental design is to perturb only the logged label, leaving the model's
reasoning surface unchanged.

**Imports**: from `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` import
`PlanAndSolveAgent`, `ScriptedModel`, `TRAJECTORY_RECORD_FIELDS`, `TrajectoryRecord` (as
`PlanAndSolveTrajectoryRecord` to disambiguate); from
`tasks.t0006_scope_aware_react_library.code.scope_aware_react` import `ScopeAwareReactAgent` and its
`Granularity`/`ToolRegistry` types. No new third-party dependencies.

## Cost Estimation

* Compute: $0 (deterministic local Python tests only; no LLM, GPU, or paid API calls).
* Project budget impact: $0 — the `write-library` task type has `has_external_costs: false`, so the
  budget gate is skipped per the execute-task spec.
* Total: **$0**.

## Step by Step

1. **Implement `code/matched_mismatch.py`.** Create the module with these public symbols:
   `GRANULARITY_VALUES: tuple[Literal["global", "subtask", "atomic"], ...]`,
   `ADVERSARIAL_MAP: dict[str, str]`, `MismatchStrategy = Literal["random", "adversarial"]`,
   `Delegate = Literal["scope_aware_react", "scope_unaware_planandsolve"]`, frozen dataclass `Phase`
   with fields `(kind: str, correct_tag: str, payload: str)`, frozen dataclass
   `MatchedMismatchRecord` with fields
   `(turn_index, granularity, thought, action, observation, confidence, extras)` where the first six
   match `TRAJECTORY_RECORD_FIELDS`, frozen dataclass `AgentRunResult` with `final_answer`,
   `trajectory: list[MatchedMismatchRecord]`, and `phases: list[Phase]`, function
   `iter_phases(annotation: Mapping[str, Any]) -> Iterator[Phase]` that yields phases in canonical
   order, function
   `pick_mismatch_tag(correct_tag: str, *, strategy: MismatchStrategy, rng: random.Random) -> str`
   that returns one of the two wrong tags, and class `MatchedMismatchAgent` with keyword-only init
   `(model_call, tool_registry, delegate, mismatch_strategy, seed: int = 0, max_turns_per_phase: int = 8)`
   and method `run(problem: str, annotation: Mapping[str, Any]) -> AgentRunResult`. Module-level
   `assert TRAJECTORY_RECORD_FIELDS == ("turn_index", "granularity", "thought", "action", "observation", "confidence")`
   enforces parity. Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-5, REQ-6, REQ-7, REQ-10.

2. **Write `code/test_matched_mismatch.py`.** Tests (each is a self-contained pytest function;
   target ≥ 12 tests):
   * `test_granularity_values_and_adversarial_map` — assert constants are correct.
   * `test_trajectory_schema_parity_with_t0007` — assert
     `TRAJECTORY_RECORD_FIELDS == ("turn_index", "granularity", "thought", "action", "observation", "confidence")`
     and that `MatchedMismatchRecord`'s first six dataclass-field names match in order (REQ-5).
   * `test_phase_order` — fixture annotation with two subtasks (each with two atomics) and one
     `global_atomic`; assert `iter_phases` yields
     `[global, subtask_0, atomic_0_0, atomic_0_1, subtask_1, atomic_1_0, atomic_1_1, global_atomic_0]`
     in this exact order with correct `correct_tag` values (REQ-2).
   * `test_global_atomics_treated_as_atomic` — `iter_phases` yields `correct_tag == "atomic"` for
     items in the `global_atomics` list (REQ-10).
   * `test_random_strategy_uniformity` — for each correct tag in `{global, subtask, atomic}`, run
     `pick_mismatch_tag(correct, strategy="random", rng=Random(seed))` 300 times and assert each of
     the two wrong tags appears at least 100 times and the correct tag never appears (REQ-3).
   * `test_adversarial_strategy_correctness` — `pick_mismatch_tag(correct, "adversarial")` returns
     the canonical adversarial tag for each of the three correct values (REQ-4).
   * `test_records_carry_wrong_tag_with_correct_tag_in_extras` — drive a one-phase annotation
     through `MatchedMismatchAgent.run` with the t0007 delegate; assert every emitted record has
     `granularity != correct_tag` and `extras["_correct_granularity"] == correct_tag` (REQ-6).
   * `test_end_to_end_with_planandsolve_delegate` — full v2-shaped fixture, delegate=
     `"scope_unaware_planandsolve"`, `ScriptedModel` from t0007 with pre-recorded planner/executor
     responses; assert `final_answer` matches the script's `FINAL_ANSWER:` payload, the trajectory
     length matches the number of phases, and every record's `granularity` is wrong (REQ-7, REQ-8).
   * `test_end_to_end_with_react_delegate` — same fixture, delegate=`"scope_aware_react"`,
     `ScriptedModel` from t0006; assert similar invariants (REQ-7, REQ-8).
   * `test_unknown_strategy_raises` — invalid `mismatch_strategy` raises `ValueError` (defensive).
   * `test_unknown_delegate_raises` — invalid `delegate` raises `ValueError` (defensive).
   * `test_seed_determinism` — same seed produces identical wrong-tag sequences across two runs for
     `mismatch_strategy="random"`.

3. **Run quality checks.** `uv run ruff check --fix .`, `uv run ruff format .`,
   `uv run mypy -p tasks.t0010_matched_mismatch_library.code`,
   `uv run pytest tasks/t0010_matched_mismatch_library/code/ -v`. Expected: zero ruff issues, zero
   mypy errors, all tests pass.

4. **Create `assets/library/matched_mismatch_v1/details.json`** per the v2 library spec, with:
   `library_id="matched_mismatch_v1"`, `version="0.1.0"`,
   `module_paths=["code/ matched_mismatch.py"]`, `entry_points` listing `MatchedMismatchAgent`,
   `MatchedMismatchRecord`, `AgentRunResult`, `Phase`, `iter_phases`, `pick_mismatch_tag`,
   `ADVERSARIAL_MAP`, `GRANULARITY_VALUES`; `description_path="description.md"`;
   `test_paths=["code/test_matched_mismatch.py"]`; categories `granularity-conditioning`,
   `hierarchical-planning`, `agent-evaluation`. Satisfies REQ-9.

5. **Create `assets/library/matched_mismatch_v1/description.md`** with all eight mandatory sections
   (Metadata, Overview, API Reference, Usage Examples, Dependencies, Testing, Main Ideas, Summary)
   per the library asset spec. The description must include: a worked example combining the v2
   annotation walk + delegate selection + ScriptedModel; the adversarial mapping table; the
   `global_atomics → atomic` rule; and a `## Trajectory Schema` note that the canonical six-field
   schema is unchanged and `extras["_correct_granularity"]` records the correct tag. Satisfies
   REQ-9.

6. **Run the library verificator.**
   `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0010_matched_mismatch_library matched_mismatch_v1`.
   Expected: zero errors and zero warnings. Satisfies REQ-9.

## Remote Machines

None required. The implementation is pure Python with deterministic tests and no remote compute.

## Assets Needed

* No task dependencies. References two existing libraries as imports only:
  `tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve` (TRAJECTORY_RECORD_FIELDS,
  ScriptedModel, PlanAndSolveAgent) and
  `tasks.t0006_scope_aware_react_library.code.scope_aware_react` (ScopeAwareReactAgent,
  ScriptedModel as `ReactScriptedModel`).

## Expected Assets

* One library asset: `library` × 1 → `assets/library/matched_mismatch_v1/` with `details.json` and
  `description.md`. Module code lives at `code/matched_mismatch.py` and tests at
  `code/test_matched_mismatch.py`. Matches `task.json` `expected_assets.library = 1`.

## Time Estimation

* Research (already done): 30 min.
* Implementation (steps 1-3): 60 min.
* Asset creation + docs (steps 4-6): 30 min.
* Results & reporting (orchestrator-managed): 30 min.
* Total wall-clock: ~2.5 h, all local.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Sister t0006/t0007 libraries change their public API on a parallel branch | Low | Medium | The `assert TRAJECTORY_RECORD_FIELDS == (...)` parity check at module import surfaces any drift immediately; pin imports to the constants the libraries already export. |
| t0009's v2 annotation schema differs subtly from the documented shape (`global`, `subtasks[].subtask`, `subtasks[].atomics`, `global_atomics`) | Low | Medium | The wrapper accepts a `Mapping[str, Any]` annotation and reads only the documented keys; an unknown shape raises `KeyError` rather than producing silent garbage. Tests use a fixture matching the documented shape. |
| Random-strategy test flakes due to RNG variance over 300 trials | Low | Low | Use a seeded `random.Random(42)`; assert each wrong tag appears in `[100, 200]` (3-sigma bounds for a fair coin). |
| `mypy` rejects `Literal` narrowing across the `Delegate` switch | Medium | Low | Use `assert_never` on the exhaustive match — pattern matches t0007's existing style. |
| Adversarial mapping for `subtask` is genuinely ambiguous (equidistant from `global` and `atomic`) | High | Low | Document the choice (`subtask → atomic`) explicitly in `description.md` and `ADVERSARIAL_MAP`'s docstring; the test pinning the choice prevents accidental flips. |

## Verification Criteria

* `uv run ruff check --fix .` exits with code 0 (zero remaining issues).
* `uv run ruff format .` is a no-op (formatting clean).
* `uv run mypy -p tasks.t0010_matched_mismatch_library.code` exits with code 0.
* `uv run pytest tasks/t0010_matched_mismatch_library/code/ -v` reports `passed` for all ≥ 12 tests
  and zero failures.
* `uv run python -m arf.scripts.verificators.verify_library_asset --task-id t0010_matched_mismatch_library matched_mismatch_v1`
  prints `PASSED — no errors or warnings`.
* `uv run python -m arf.scripts.verificators.verify_task_metrics t0010_matched_mismatch_library`
  exits with code 0 (an empty `metrics.json` `{}` is valid for write-library tasks).
* `tasks/t0010_matched_mismatch_library/code/matched_mismatch.py` exposes the public symbols listed
  in REQ-1/REQ-7 — confirmed by REQ traceability in `results/results_detailed.md`'s
  `## Task Requirement Coverage` section.
