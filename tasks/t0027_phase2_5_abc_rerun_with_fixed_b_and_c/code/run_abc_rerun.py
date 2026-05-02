"""Orchestrator for the t0027 phase-2.5 B/C re-run on the 130 paired instances.

Variant A is not re-run — its predictions are reused by reference from t0026's ``a-scope-aware``
asset. Only B (``PlanAndSolveAgentV3``) and C (``MatchedMismatchV2Agent``) are re-run. The
130-paired set is computed at run time as the intersection of the three t0026 variants' completed
instance ids.

Three subcommands:

* ``--paired-manifest`` — compute the 130-paired manifest from t0026 predictions and write it to
  ``data/paired_manifest.json``. Idempotent.
* ``--smoke <variant>`` — run B or C on a 5-instance FrontierScience smoke; halt early if the
  acceptance gate fails (variant B: <2/5 parser failures; variant C: trajectory shape matches
  v3 record schema). Writes ``data/runs/<variant>_smoke/`` and updates
  ``data/parser_failure_count.json``.
* ``--full <variant>`` — run B or C on the full 130-paired set, with a per-stream hard stop at
  ``PER_STREAM_HARD_STOP_USD``. Persists per-instance trajectories to ``data/runs/<variant>/`` and
  writes the final predictions JSONL to the predictions asset's ``files/`` directory after judging
  with the primary sonnet judge.

This task obeys the implementation-skill rule that [CRITICAL] steps must halt and write an
intervention file on block. Cost-cap and parser-failure halts are reflected as exit-code 2 returns
(the orchestrator captures these and writes intervention files outside the runner).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final, Literal

from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    MalformedPlanError,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.tools import (
    build_planandsolve_tool_registry,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.anthropic_shim import (
    CostTracker,
    make_model_call,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.instance_loader import (
    Instance,
    load_instances,
    write_manifest,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.judge import (
    JudgeResult,
    Prediction,
    judge_outcome,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.matched_mismatch_v2 import (
    AgentRunResultV2,
    MatchedMismatchV2Agent,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.paths import (
    INSTANCE_MANIFEST_PATH,
    JUDGE_MODEL_PRIMARY,
    MODEL_UNDER_TEST,
    PAIRED_MANIFEST_PATH,
    PARSER_FAILURE_PATH,
    PER_STREAM_HARD_STOP_USD,
    PREDICTIONS_B_JSONL,
    PREDICTIONS_C_JSONL,
    RUNS_DIR,
    SUBSET_FRONTSCI,
    T0026_PREDICTIONS_A_JSONL,
    T0026_PREDICTIONS_B_JSONL,
    T0026_PREDICTIONS_C_JSONL,
    VARIANT_B,
    VARIANT_C,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.planandsolve_v3 import (
    AgentResultV3,
    PlanAndSolveAgentV3,
)

type RerunVariantId = Literal["b", "c"]

_DEFAULT_MAX_TURNS: Final[int] = 10
_DEFAULT_MAX_WORKERS: Final[int] = 8
_DEFAULT_MAX_TOKENS: Final[int] = 4096
_SMOKE_N: Final[int] = 5
_SMOKE_MAX_PARSER_FAILURES_B: Final[int] = 1
_BUDGET_PROJECTION_FACTOR: Final[float] = 1.5  # safety margin on cost projection
# t0026 reference: variant B cost over 130 paired instances was $9.07 (average $0.07/instance).
# Variant C cost was $12.54 (average $0.097/instance). FrontierScience problems were systematically
# more expensive than taubench/swebench. We use a conservative per-instance non-frontsci cost prior
# of $0.10/inst (above t0026 averages, accounts for v3's extra plan-recovery attempts) when
# projecting the full-run cost from a FrontierScience-only smoke.
_NON_FRONTSCI_COST_PRIOR_USD: Final[float] = 0.10


@dataclass(frozen=True, slots=True)
class PairedManifest:
    """The 130 paired instance ids — intersection of all three t0026 variants' completed runs."""

    seed_t0026: int
    n_paired: int
    instance_ids: list[str]
    per_subset_counts: dict[str, int]


@dataclass(slots=True)
class _RerunOutcome:
    instance_id: str
    subset: str
    final_answer: str | None
    final_confidence: float | None
    cost_usd: float
    parser_recovery_path: str
    parser_attempts: int
    trajectory_payload: Any
    raised_malformed_plan_error: bool


def _read_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line_stripped = line.strip()
            if len(line_stripped) == 0:
                continue
            rows.append(json.loads(line_stripped))
    return rows


def _is_completed_t0026_record(*, record: Mapping[str, Any]) -> bool:
    """Per task description: 'instances where every variant returned a non-null final answer or
    judge verdict from the JSONL files'.

    Concretely we accept a record as completed iff it has a non-null judge_sonnet_success field —
    that field is False both on agent failure and on judged-fail; the requirement is just that the
    pipeline actually ran end-to-end for that instance.
    """
    return record.get("judge_sonnet_success") is not None


def _compute_paired_manifest() -> PairedManifest:
    a_rows = _read_jsonl(path=T0026_PREDICTIONS_A_JSONL)
    b_rows = _read_jsonl(path=T0026_PREDICTIONS_B_JSONL)
    c_rows = _read_jsonl(path=T0026_PREDICTIONS_C_JSONL)
    a_completed = {r["instance_id"] for r in a_rows if _is_completed_t0026_record(record=r)}
    b_completed = {r["instance_id"] for r in b_rows if _is_completed_t0026_record(record=r)}
    c_completed = {r["instance_id"] for r in c_rows if _is_completed_t0026_record(record=r)}
    paired = a_completed & b_completed & c_completed
    subset_by_iid: dict[str, str] = {}
    for r in a_rows:
        subset_by_iid[r["instance_id"]] = r["subset"]
    paired_sorted = sorted(paired)
    counts: dict[str, int] = {}
    for iid in paired_sorted:
        s = subset_by_iid.get(iid, "unknown")
        counts[s] = counts.get(s, 0) + 1
    return PairedManifest(
        seed_t0026=20260502,
        n_paired=len(paired_sorted),
        instance_ids=paired_sorted,
        per_subset_counts=counts,
    )


def _write_paired_manifest(*, manifest: PairedManifest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "spec_version": "1",
        "computation": "intersection of t0026 a-scope-aware, b-plan-and-solve, c-mismatched "
        "predictions JSONL records where judge_sonnet_success is non-null",
        "seed_t0026": manifest.seed_t0026,
        "n_paired": manifest.n_paired,
        "per_subset_counts": manifest.per_subset_counts,
        "instance_ids": manifest.instance_ids,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _load_paired_instances(*, manifest: PairedManifest) -> list[Instance]:
    all_instances = load_instances()
    by_id: dict[str, Instance] = {inst.instance_id: inst for inst in all_instances}
    paired: list[Instance] = []
    for iid in manifest.instance_ids:
        if iid in by_id:
            paired.append(by_id[iid])
    return paired


def _paired_manifest_command() -> int:
    manifest = _compute_paired_manifest()
    _write_paired_manifest(manifest=manifest, path=PAIRED_MANIFEST_PATH)
    print(
        f"wrote paired manifest: {manifest.n_paired} instances, "
        f"per_subset={manifest.per_subset_counts}, path={PAIRED_MANIFEST_PATH}"
    )
    instances = load_instances()
    write_manifest(instances=instances, output_path=INSTANCE_MANIFEST_PATH)
    print(
        f"wrote full instance manifest: {len(instances)} instances, path={INSTANCE_MANIFEST_PATH}"
    )
    return 0


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


def _trajectory_to_jsonable(*, obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    if isinstance(obj, list):
        return [_trajectory_to_jsonable(obj=x) for x in obj]
    if isinstance(obj, dict):
        return {k: _trajectory_to_jsonable(obj=v) for k, v in obj.items()}
    return obj


def _process_one_instance(
    *,
    variant: RerunVariantId,
    instance: Instance,
    cost_tracker: CostTracker,
    variant_dir: Path,
    max_turns: int,
    max_tokens: int,
) -> _RerunOutcome:
    local_tracker = CostTracker()
    model_call = make_model_call(
        model_id=MODEL_UNDER_TEST,
        cost_tracker=cost_tracker,
        max_tokens=max_tokens,
        secondary_cost_tracker=local_tracker,
    )
    final_answer: str | None = None
    final_confidence: float | None = None
    parser_recovery_path: str = "unknown"
    parser_attempts: int = 0
    trajectory_payload: Any
    raised_malformed: bool = False
    try:
        if variant == VARIANT_B:
            tool_registry = build_planandsolve_tool_registry()
            agent_b = PlanAndSolveAgentV3(
                model_call=model_call,
                tool_registry=dict(tool_registry),
                max_steps=max_turns,
            )
            v3_result: AgentResultV3 = agent_b.run(problem=instance.problem_text)
            final_answer = v3_result.final_answer
            final_confidence = v3_result.final_confidence
            parser_recovery_path = v3_result.plan_parser_recovery_path
            parser_attempts = v3_result.plan_parser_attempts
            trajectory_payload = {
                "plan": v3_result.plan,
                "trajectory": _trajectory_to_jsonable(obj=v3_result.trajectory),
                "final_confidence": v3_result.final_confidence,
                "final_confidence_parse_failures": v3_result.final_confidence_parse_failures,
                "plan_parser_recovery_path": v3_result.plan_parser_recovery_path,
                "plan_parser_attempts": v3_result.plan_parser_attempts,
            }
        elif variant == VARIANT_C:
            tool_registry = build_planandsolve_tool_registry()
            agent_c = MatchedMismatchV2Agent(
                model_call=model_call,
                tool_registry=dict(tool_registry),
                max_steps=max_turns,
                mismatch_strategy="adversarial",
                seed=0,
            )
            annotation = _synthetic_annotation(problem_text=instance.problem_text)
            mm_result: AgentRunResultV2 = agent_c.run(
                problem=instance.problem_text,
                annotation=annotation,
            )
            final_answer = mm_result.final_answer
            final_confidence = mm_result.final_confidence
            parser_recovery_path = mm_result.plan_parser_recovery_path
            parser_attempts = mm_result.plan_parser_attempts
            phases_payload = [
                {"kind": p.kind, "correct_tag": p.correct_tag, "payload": p.payload[:200]}
                for p in mm_result.phases
            ]
            trajectory_payload = {
                "plan": mm_result.plan,
                "trajectory": _trajectory_to_jsonable(obj=mm_result.trajectory),
                "final_confidence": mm_result.final_confidence,
                "final_confidence_parse_failures": mm_result.final_confidence_parse_failures,
                "plan_parser_recovery_path": mm_result.plan_parser_recovery_path,
                "plan_parser_attempts": mm_result.plan_parser_attempts,
                "phases": phases_payload,
                "delegate": mm_result.delegate,
            }
        else:
            raise ValueError(f"unknown re-run variant: {variant!r}")
    except MalformedPlanError as exc:
        raised_malformed = True
        parser_recovery_path = "all_failed"
        parser_attempts = 3
        trajectory_payload = {"error": f"MalformedPlanError: {exc!s}"[:500]}
    except Exception as exc:  # noqa: BLE001 — surface as a recorded failure and continue
        trajectory_payload = {"error": f"{type(exc).__name__}: {exc!s}"[:500]}
    cost_for_instance = float(local_tracker.snapshot()["cost_usd"])
    return _RerunOutcome(
        instance_id=instance.instance_id,
        subset=instance.subset,
        final_answer=final_answer,
        final_confidence=final_confidence,
        cost_usd=cost_for_instance,
        parser_recovery_path=parser_recovery_path,
        parser_attempts=parser_attempts,
        trajectory_payload=trajectory_payload,
        raised_malformed_plan_error=raised_malformed,
    )


def _persist_trajectory(
    *, outcome: _RerunOutcome, variant: RerunVariantId, variant_dir: Path
) -> Path:
    traj_path = variant_dir / f"trajectory_{outcome.instance_id}.json"
    record = {
        "instance_id": outcome.instance_id,
        "subset": outcome.subset,
        "variant": variant,
        "final_answer": outcome.final_answer,
        "final_confidence": outcome.final_confidence,
        "cost_usd": outcome.cost_usd,
        "parser_recovery_path": outcome.parser_recovery_path,
        "parser_attempts": outcome.parser_attempts,
        "trajectory": outcome.trajectory_payload,
    }
    traj_path.parent.mkdir(parents=True, exist_ok=True)
    traj_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return traj_path


def _run_variant(
    *,
    variant: RerunVariantId,
    instances: list[Instance],
    cost_tracker: CostTracker,
    output_dir: Path,
    max_turns: int = _DEFAULT_MAX_TURNS,
    max_tokens: int = _DEFAULT_MAX_TOKENS,
    max_workers: int = _DEFAULT_MAX_WORKERS,
    hard_stop_usd: float = PER_STREAM_HARD_STOP_USD,
) -> list[_RerunOutcome]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outcomes_by_iid: dict[str, _RerunOutcome] = {}
    started = time.monotonic()
    workers = max(1, min(max_workers, len(instances)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_iid = {
            executor.submit(
                _process_one_instance,
                variant=variant,
                instance=instance,
                cost_tracker=cost_tracker,
                variant_dir=output_dir,
                max_turns=max_turns,
                max_tokens=max_tokens,
            ): instance.instance_id
            for instance in instances
        }
        total = len(future_to_iid)
        halt = False
        for done, future in enumerate(as_completed(future_to_iid), start=1):
            try:
                outcome = future.result()
            except Exception as exc:  # noqa: BLE001
                iid = future_to_iid[future]
                inst = next(i for i in instances if i.instance_id == iid)
                outcome = _RerunOutcome(
                    instance_id=iid,
                    subset=inst.subset,
                    final_answer=None,
                    final_confidence=None,
                    cost_usd=0.0,
                    parser_recovery_path="executor_failure",
                    parser_attempts=0,
                    trajectory_payload={"error": f"executor: {type(exc).__name__}: {exc!s}"[:500]},
                    raised_malformed_plan_error=False,
                )
            outcomes_by_iid[outcome.instance_id] = outcome
            _persist_trajectory(outcome=outcome, variant=variant, variant_dir=output_dir)
            cost_so_far = cost_tracker.snapshot()["cost_usd"]
            if done % 5 == 0 or done == total:
                elapsed = time.monotonic() - started
                print(
                    f"  variant {variant}: {done}/{total} done, "
                    f"cost ${cost_so_far:.4f}, elapsed {elapsed:.1f}s"
                )
            if cost_so_far >= hard_stop_usd:
                print(
                    f"PER-STREAM HARD STOP HIT: variant {variant} cost ${cost_so_far:.4f} "
                    f">= ${hard_stop_usd:.2f}; cancelling pending futures."
                )
                halt = True
                break
        if halt:
            for fut in future_to_iid:
                fut.cancel()
    final_outcomes: list[_RerunOutcome] = []
    for instance in instances:
        if instance.instance_id in outcomes_by_iid:
            final_outcomes.append(outcomes_by_iid[instance.instance_id])
    return final_outcomes


def _outcome_to_prediction(
    *, outcome: _RerunOutcome, variant: RerunVariantId, variant_dir: Path
) -> Prediction:
    traj_path = variant_dir / f"trajectory_{outcome.instance_id}.json"
    return Prediction(
        instance_id=outcome.instance_id,
        subset=outcome.subset,
        variant=variant,
        final_answer=outcome.final_answer,
        final_confidence=outcome.final_confidence,
        cost_usd=outcome.cost_usd,
        trajectory_path=str(traj_path),
    )


def _judge_predictions(
    *,
    predictions: list[Prediction],
    instances_by_id: dict[str, Instance],
    cost_tracker: CostTracker,
) -> dict[str, JudgeResult]:
    results: dict[str, JudgeResult] = {}
    for pred in predictions:
        instance = instances_by_id[pred.instance_id]
        try:
            jr = judge_outcome(
                instance=instance,
                prediction=pred,
                cost_tracker=cost_tracker,
                model_id=JUDGE_MODEL_PRIMARY,
            )
        except Exception as exc:  # noqa: BLE001
            jr = JudgeResult(
                success=False,
                rationale=f"judge call failed: {type(exc).__name__}: {exc!s}"[:300],
                raw_response="",
            )
        results[pred.instance_id] = jr
    return results


def _write_predictions_jsonl(
    *,
    predictions: list[Prediction],
    judge_results: dict[str, JudgeResult],
    outcomes_by_iid: dict[str, _RerunOutcome],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for pred in predictions:
            jr = judge_results.get(pred.instance_id)
            outcome = outcomes_by_iid[pred.instance_id]
            row: dict[str, Any] = {
                "instance_id": pred.instance_id,
                "subset": pred.subset,
                "variant": pred.variant,
                "final_answer": pred.final_answer,
                "final_confidence": pred.final_confidence,
                "cost_usd": pred.cost_usd,
                "trajectory_path": pred.trajectory_path,
                "judge_sonnet_success": jr.success if jr is not None else False,
                "judge_sonnet_rationale": jr.rationale if jr is not None else "judge missing",
                "judge_opus_success": None,
                "judge_opus_rationale": None,
                "plan_parser_recovery_path": outcome.parser_recovery_path,
                "plan_parser_attempts": outcome.parser_attempts,
                "raised_malformed_plan_error": outcome.raised_malformed_plan_error,
            }
            f.write(json.dumps(row) + "\n")


def _update_parser_failure_count(
    *,
    variant: RerunVariantId,
    outcomes: list[_RerunOutcome],
    is_smoke: bool,
) -> dict[str, Any]:
    existing: dict[str, Any]
    if PARSER_FAILURE_PATH.exists():
        existing = json.loads(PARSER_FAILURE_PATH.read_text(encoding="utf-8"))
    else:
        existing = {"variants": {}}
    failures = [o for o in outcomes if o.raised_malformed_plan_error]
    recovery_breakdown: dict[str, int] = {}
    for o in outcomes:
        path = o.parser_recovery_path
        recovery_breakdown[path] = recovery_breakdown.get(path, 0) + 1
    key = f"{variant}_smoke" if is_smoke else variant
    existing["variants"][key] = {
        "n_total": len(outcomes),
        "n_malformed_plan_error": len(failures),
        "malformed_instance_ids": [o.instance_id for o in failures],
        "recovery_path_counts": recovery_breakdown,
    }
    PARSER_FAILURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PARSER_FAILURE_PATH.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    return existing


def _smoke_command(*, variant: RerunVariantId) -> int:
    if variant not in (VARIANT_B, VARIANT_C):
        print(f"smoke variant must be 'b' or 'c', got {variant!r}")
        return 1
    manifest = _compute_paired_manifest()
    paired_instances = _load_paired_instances(manifest=manifest)
    fs_paired = [i for i in paired_instances if i.subset == SUBSET_FRONTSCI]
    smoke_instances = fs_paired[:_SMOKE_N]
    print(
        f"smoke run for variant {variant!r}: "
        f"{len(smoke_instances)} FrontierScience paired instances"
    )
    if len(smoke_instances) == 0:
        print("ERROR: no FrontierScience paired instances found for smoke run.")
        return 1
    cost_tracker = CostTracker()
    smoke_dir = RUNS_DIR / f"{variant}_smoke"
    outcomes = _run_variant(
        variant=variant,
        instances=smoke_instances,
        cost_tracker=cost_tracker,
        output_dir=smoke_dir,
        max_turns=8,
        max_tokens=2048,
        max_workers=4,
        hard_stop_usd=PER_STREAM_HARD_STOP_USD,
    )
    failure_state = _update_parser_failure_count(variant=variant, outcomes=outcomes, is_smoke=True)
    snapshot = cost_tracker.snapshot()
    smoke_cost = float(snapshot["cost_usd"])
    n_failures = sum(1 for o in outcomes if o.raised_malformed_plan_error)
    n_runs = len(outcomes)
    cost_per_run = smoke_cost / max(1, n_runs)
    # Subset-aware projection: apply the FrontierScience-smoke avg (with a safety factor for
    # uncertainty since n=5 is small) only to the frontsci slots in the paired set; use
    # _NON_FRONTSCI_COST_PRIOR_USD (already above t0026's $0.07 average) for taubench+swebench
    # without an additional factor since the prior is itself conservative.
    n_fs_paired = manifest.per_subset_counts.get(SUBSET_FRONTSCI, 0)
    n_other_paired = manifest.n_paired - n_fs_paired
    fs_component = cost_per_run * n_fs_paired * _BUDGET_PROJECTION_FACTOR
    other_component = _NON_FRONTSCI_COST_PRIOR_USD * n_other_paired
    projected_full_cost = fs_component + other_component
    print(
        f"smoke variant {variant} complete: cost ${smoke_cost:.4f}, runs={n_runs}, "
        f"parser_failures={n_failures}, projected_full=${projected_full_cost:.2f} "
        f"(fs=${cost_per_run:.4f}*{n_fs_paired}*{_BUDGET_PROJECTION_FACTOR}=${fs_component:.2f} + "
        f"other=${_NON_FRONTSCI_COST_PRIOR_USD:.4f}*{n_other_paired}=${other_component:.2f})"
    )
    smoke_state = failure_state["variants"].get(f"{variant}_smoke", {})
    print(f"recovery_path_counts: {smoke_state.get('recovery_path_counts')}")
    if variant == VARIANT_B and n_failures > _SMOKE_MAX_PARSER_FAILURES_B:
        print(
            f"SMOKE GATE FAIL: variant B parser_failures={n_failures}/{n_runs} > "
            f"{_SMOKE_MAX_PARSER_FAILURES_B}; halting before full run."
        )
        return 2
    if variant == VARIANT_C:
        # Acceptance gate: trajectories must contain TrajectoryRecordV2 records (i.e., the
        # trajectory payload must have a 'trajectory' list and a 'plan_parser_recovery_path'
        # key — the v3 shape).
        for outcome in outcomes:
            payload = outcome.trajectory_payload
            if not isinstance(payload, dict):
                continue
            if "error" in payload:
                continue
            if "plan_parser_recovery_path" not in payload or "plan" not in payload:
                print(
                    f"SMOKE GATE FAIL: variant C instance {outcome.instance_id} "
                    f"has wrong shape: keys={list(payload.keys())}; "
                    f"expected v3 shape with plan_parser_recovery_path."
                )
                return 2
    if projected_full_cost > PER_STREAM_HARD_STOP_USD:
        print(
            f"SMOKE GATE FAIL: variant {variant} projected full cost "
            f"${projected_full_cost:.2f} > per-stream cap ${PER_STREAM_HARD_STOP_USD:.2f}; halting."
        )
        return 2
    print(f"SMOKE GATE PASS: variant {variant} OK to proceed with full run.")
    return 0


def _full_command(*, variant: RerunVariantId) -> int:
    if variant not in (VARIANT_B, VARIANT_C):
        print(f"full variant must be 'b' or 'c', got {variant!r}")
        return 1
    manifest = _compute_paired_manifest()
    _write_paired_manifest(manifest=manifest, path=PAIRED_MANIFEST_PATH)
    paired_instances = _load_paired_instances(manifest=manifest)
    print(
        f"full run for variant {variant!r}: {len(paired_instances)} paired instances "
        f"(target N_PAIRED_EXPECTED={manifest.n_paired})"
    )
    cost_tracker = CostTracker()
    variant_dir = RUNS_DIR / variant
    outcomes = _run_variant(
        variant=variant,
        instances=paired_instances,
        cost_tracker=cost_tracker,
        output_dir=variant_dir,
        max_turns=_DEFAULT_MAX_TURNS,
        max_tokens=_DEFAULT_MAX_TOKENS,
        max_workers=_DEFAULT_MAX_WORKERS,
        hard_stop_usd=PER_STREAM_HARD_STOP_USD,
    )
    _update_parser_failure_count(variant=variant, outcomes=outcomes, is_smoke=False)
    snapshot = cost_tracker.snapshot()
    run_cost = float(snapshot["cost_usd"])
    n_failures = sum(1 for o in outcomes if o.raised_malformed_plan_error)
    print(
        f"full variant {variant} agent run complete: cost ${run_cost:.4f}, "
        f"runs={len(outcomes)}, parser_failures={n_failures}"
    )
    if run_cost >= PER_STREAM_HARD_STOP_USD:
        print(
            f"PER-STREAM HARD STOP HIT during full run: cost ${run_cost:.4f} "
            f">= ${PER_STREAM_HARD_STOP_USD:.2f}. Truncating to whatever ran."
        )
    print(f"--- judging variant {variant} predictions with primary sonnet judge ---")
    instances_by_id = {inst.instance_id: inst for inst in paired_instances}
    predictions = [
        _outcome_to_prediction(outcome=o, variant=variant, variant_dir=variant_dir)
        for o in outcomes
    ]
    judge_results = _judge_predictions(
        predictions=predictions,
        instances_by_id=instances_by_id,
        cost_tracker=cost_tracker,
    )
    final_snapshot = cost_tracker.snapshot()
    final_cost = float(final_snapshot["cost_usd"])
    print(
        f"variant {variant} judging complete: total cost ${final_cost:.4f} "
        f"(agent ${run_cost:.4f} + judge ${final_cost - run_cost:.4f})"
    )
    if final_cost > PER_STREAM_HARD_STOP_USD * 1.1:
        print(
            f"WARNING: variant {variant} total cost exceeded per-stream cap by >10%: "
            f"${final_cost:.4f} > ${PER_STREAM_HARD_STOP_USD * 1.1:.4f}"
        )
    output_jsonl = PREDICTIONS_B_JSONL if variant == VARIANT_B else PREDICTIONS_C_JSONL
    outcomes_by_iid = {o.instance_id: o for o in outcomes}
    _write_predictions_jsonl(
        predictions=predictions,
        judge_results=judge_results,
        outcomes_by_iid=outcomes_by_iid,
        output_path=output_jsonl,
    )
    print(f"wrote predictions JSONL: {output_jsonl}")
    n_success = sum(1 for jr in judge_results.values() if jr.success)
    print(
        f"variant {variant} success rate (sonnet judge): "
        f"{n_success}/{len(predictions)} = {n_success / max(1, len(predictions)):.4f}"
    )
    return 0


def _make_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="t0027 phase-2.5 B/C re-run orchestrator.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--paired-manifest", action="store_true")
    group.add_argument("--smoke", choices=["b", "c"])
    group.add_argument("--full", choices=["b", "c"])
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _make_arg_parser()
    args = parser.parse_args(argv)
    if args.paired_manifest:
        return _paired_manifest_command()
    if args.smoke is not None:
        return _smoke_command(variant=args.smoke)
    if args.full is not None:
        return _full_command(variant=args.full)
    return 1


if __name__ == "__main__":
    sys.exit(main())
