"""Per-variant runner for variants A (scope-aware ReAct), B (Plan-and-Solve v2), C (mismatched).

Tool registries: Tau-bench and FrontierScience are reasoning-bound and use a stub registry with a
single ``python_exec`` tool that runs Python in a short-timeout subprocess; SWE-bench in this task
is also driven by reasoning only — the harness does NOT execute SWE-bench patches inside isolated
environments. The judge module documents this scope constraint.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Final, Literal

from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    AgentResult as ReactAgentResult,
)
from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScopeAwareReactAgent,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    AgentRunResult as MismatchAgentResult,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    MatchedMismatchAgent,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.tools import (
    build_planandsolve_tool_registry,
    build_react_tool_registry,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    AgentResultV2 as PlanAndSolveV2Result,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    PlanAndSolveAgentV2,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.anthropic_shim import (
    CostTracker,
    make_model_call,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.instance_loader import Instance
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.judge import Prediction
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
)

type VariantId = Literal["a", "b", "c"]

_DEFAULT_MAX_TURNS: Final[int] = 12
_DEFAULT_MAX_WORKERS: Final[int] = 8


@dataclass(slots=True)
class VariantRunSummary:
    variant: str
    n_instances: int
    predictions: list[Prediction] = field(default_factory=list)
    elapsed_seconds: float = 0.0


def _synthetic_annotation(*, problem_text: str) -> dict[str, Any]:
    snippet = problem_text.strip()[:500]
    if len(snippet) == 0:
        snippet = "(empty problem)"
    return {
        "hierarchy": {
            "global": f"Solve the following problem end-to-end: {snippet}",
            "subtasks": [
                {
                    "subtask": "Restate the problem and identify the target output type.",
                    "atomics": [
                        "Read the problem carefully.",
                        "List any quantities or constraints mentioned in the problem.",
                    ],
                },
                {
                    "subtask": "Plan the solution and produce a final answer.",
                    "atomics": [
                        "Outline the solution steps.",
                        "Compute or formulate the final answer.",
                    ],
                },
            ],
            "global_atomics": [
                "Emit the final answer with a Finish action.",
            ],
        }
    }


@dataclass(frozen=True, slots=True)
class _InstanceOutcome:
    instance_id: str
    subset: str
    final_answer: str | None
    final_confidence: float | None
    cost_usd: float
    trajectory_payload: Any


def _process_one_instance(
    *,
    variant: VariantId,
    instance: Instance,
    cost_tracker: CostTracker,
    model_id: str,
    variant_dir: Path,
    max_turns: int,
    max_tokens: int,
) -> _InstanceOutcome:
    local_tracker = CostTracker()
    model_call = make_model_call(
        model_id=model_id,
        cost_tracker=cost_tracker,
        max_tokens=max_tokens,
        secondary_cost_tracker=local_tracker,
    )
    traj_path = variant_dir / f"trajectory_{instance.instance_id}.json"
    final_answer: str | None = None
    final_confidence: float | None = None
    trajectory_payload: Any
    try:
        if variant == VARIANT_A:
            react_result = _run_variant_a(
                instance=instance,
                model_call=model_call,
                trajectory_path=traj_path.with_suffix(".jsonl"),
                max_turns=max_turns,
            )
            final_answer = react_result.answer
            trajectory_payload = _trajectory_to_jsonable(obj=react_result.trajectory)
        elif variant == VARIANT_B:
            v2_result = _run_variant_b(
                instance=instance,
                model_call=model_call,
                max_turns=max_turns,
            )
            final_answer = v2_result.final_answer
            final_confidence = v2_result.final_confidence
            trajectory_payload = _trajectory_to_jsonable(obj=v2_result.trajectory)
        elif variant == VARIANT_C:
            mismatch_result = _run_variant_c(instance=instance, model_call=model_call)
            final_answer = mismatch_result.final_answer
            trajectory_payload = _trajectory_to_jsonable(obj=mismatch_result.trajectory)
        else:
            raise ValueError(f"unknown variant: {variant!r}")
    except Exception as exc:  # noqa: BLE001 — surface as a recorded failure and continue
        trajectory_payload = {"error": f"{type(exc).__name__}: {exc!s}"[:500]}
    cost_for_instance = float(local_tracker.snapshot()["cost_usd"])
    return _InstanceOutcome(
        instance_id=instance.instance_id,
        subset=instance.subset,
        final_answer=final_answer,
        final_confidence=final_confidence,
        cost_usd=cost_for_instance,
        trajectory_payload=trajectory_payload,
    )


def _run_variant_a(
    *,
    instance: Instance,
    model_call: Callable[[str], str],
    trajectory_path: Path,
    max_turns: int,
) -> ReactAgentResult:
    tool_registry = build_react_tool_registry()
    agent = ScopeAwareReactAgent(
        problem=instance.problem_text,
        granularity="atomic",
        tool_registry=tool_registry,
        model_call=model_call,
        trajectory_path=trajectory_path,
        max_turns=max_turns,
    )
    return agent.run()


def _run_variant_b(
    *,
    instance: Instance,
    model_call: Callable[[str], str],
    max_turns: int,
) -> PlanAndSolveV2Result:
    tool_registry = build_planandsolve_tool_registry()
    agent = PlanAndSolveAgentV2(
        model_call=model_call,
        tool_registry=dict(tool_registry),
        max_steps=max_turns,
    )
    return agent.run(problem=instance.problem_text)


def _run_variant_c(
    *,
    instance: Instance,
    model_call: Callable[[str], str],
) -> MismatchAgentResult:
    tool_registry = build_planandsolve_tool_registry()
    agent = MatchedMismatchAgent(
        model_call=model_call,
        tool_registry=tool_registry,
        delegate="scope_aware_react",
        mismatch_strategy="adversarial",
        seed=0,
    )
    annotation = _synthetic_annotation(problem_text=instance.problem_text)
    return agent.run(problem=instance.problem_text, annotation=annotation)


def _trajectory_to_jsonable(*, obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    if isinstance(obj, list):
        return [_trajectory_to_jsonable(obj=x) for x in obj]
    if isinstance(obj, dict):
        return {k: _trajectory_to_jsonable(obj=v) for k, v in obj.items()}
    return obj


def run_variant(
    *,
    variant: VariantId,
    instances: list[Instance],
    cost_tracker: CostTracker,
    model_id: str,
    output_dir: Path,
    max_turns: int = _DEFAULT_MAX_TURNS,
    max_tokens: int = 4096,
    max_workers: int = _DEFAULT_MAX_WORKERS,
) -> VariantRunSummary:
    variant_dir = output_dir / variant
    variant_dir.mkdir(parents=True, exist_ok=True)
    summary = VariantRunSummary(variant=variant, n_instances=len(instances))
    started = time.monotonic()
    instance_by_id: dict[str, Instance] = {inst.instance_id: inst for inst in instances}
    outcomes: dict[str, _InstanceOutcome] = {}
    workers = max(1, min(max_workers, len(instances)))
    if workers <= 1 or len(instances) <= 1:
        for instance in instances:
            outcome = _process_one_instance(
                variant=variant,
                instance=instance,
                cost_tracker=cost_tracker,
                model_id=model_id,
                variant_dir=variant_dir,
                max_turns=max_turns,
                max_tokens=max_tokens,
            )
            outcomes[outcome.instance_id] = outcome
            _persist_outcome(
                outcome=outcome,
                variant=variant,
                variant_dir=variant_dir,
            )
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_iid = {
                executor.submit(
                    _process_one_instance,
                    variant=variant,
                    instance=instance,
                    cost_tracker=cost_tracker,
                    model_id=model_id,
                    variant_dir=variant_dir,
                    max_turns=max_turns,
                    max_tokens=max_tokens,
                ): instance.instance_id
                for instance in instances
            }
            total = len(future_to_iid)
            for done, future in enumerate(as_completed(future_to_iid), start=1):
                iid = future_to_iid[future]
                try:
                    outcome = future.result()
                except Exception as exc:  # noqa: BLE001
                    inst = instance_by_id[iid]
                    outcome = _InstanceOutcome(
                        instance_id=iid,
                        subset=inst.subset,
                        final_answer=None,
                        final_confidence=None,
                        cost_usd=0.0,
                        trajectory_payload={
                            "error": f"executor: {type(exc).__name__}: {exc!s}"[:500]
                        },
                    )
                outcomes[outcome.instance_id] = outcome
                _persist_outcome(
                    outcome=outcome,
                    variant=variant,
                    variant_dir=variant_dir,
                )
                if done % 5 == 0 or done == total:
                    elapsed = time.monotonic() - started
                    print(f"    variant {variant}: {done}/{total} done, elapsed {elapsed:.1f}s")
    for instance in instances:
        outcome = outcomes[instance.instance_id]
        traj_path = variant_dir / f"trajectory_{instance.instance_id}.json"
        summary.predictions.append(
            Prediction(
                instance_id=outcome.instance_id,
                subset=outcome.subset,
                variant=variant,
                final_answer=outcome.final_answer,
                final_confidence=outcome.final_confidence,
                cost_usd=outcome.cost_usd,
                trajectory_path=str(traj_path),
            )
        )
    summary.elapsed_seconds = time.monotonic() - started
    return summary


def _persist_outcome(
    *,
    outcome: _InstanceOutcome,
    variant: VariantId,
    variant_dir: Path,
) -> None:
    traj_path = variant_dir / f"trajectory_{outcome.instance_id}.json"
    record = {
        "instance_id": outcome.instance_id,
        "subset": outcome.subset,
        "variant": variant,
        "final_answer": outcome.final_answer,
        "final_confidence": outcome.final_confidence,
        "cost_usd": outcome.cost_usd,
        "trajectory": outcome.trajectory_payload,
    }
    traj_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
