"""5-row × 3-condition smoke validation for the v2 final_confidence wiring.

Replays the t0012 phase-2 ABC harness shape on 5 FrontierScience-Olympiad rows but uses the new
``PlanAndSolveAgentV2`` (Condition B) and a v2-style post-call confidence elicitation for
Conditions A and C. Goal: prove that the ``final_confidence`` field is populated end-to-end on
every condition, and confirm Metric 2 (``overconfident_error_rate``) is non-zero / non-1 on at
least one condition. Cost cap: $1.00 (hard).

Usage:

    TASK_ID="t0021_plan_and_solve_v2_with_final_confidence"
    uv run python -m arf.scripts.utils.run_with_logs --task-id "$TASK_ID" -- \
        uv run python -u -m "tasks.$TASK_ID.code.run_smoke" --limit 5
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    ScopeAwareReactAgent,
)
from tasks.t0006_scope_aware_react_library.code.scope_aware_react import (
    TrajectoryRecord as ReactTrajectoryRecord,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    MatchedMismatchAgent,
    MatchedMismatchRecord,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.calibration import (
    CalibrationRecord,
    compute_overconfident_error_rate,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.constants import (
    BENCHMARK_FILTER,
    BUDGET_CAP_USD,
    BUDGET_HEADROOM_USD,
    CONDITION_A_LABEL,
    CONDITION_B_LABEL,
    CONDITION_C_LABEL,
    HIGH_CONFIDENCE_THRESHOLD,
    MAX_TURNS,
    METRIC_AVG_DECISIONS_PER_TASK,
    METRIC_OVERCONFIDENT_ERROR_RATE,
    METRIC_TASK_SUCCESS_RATE,
    MODEL_AGENT,
    MODEL_JUDGE,
    PARSE_FAILURE_RATE_THRESHOLD,
    PRED_FIELD_CONDITION,
    PRED_FIELD_DECISION_COUNT,
    PRED_FIELD_FINAL,
    PRED_FIELD_FINAL_CONFIDENCE,
    PRED_FIELD_FINAL_CONFIDENCE_PARSE_FAILURES,
    PRED_FIELD_GOLD,
    PRED_FIELD_IS_CORRECT,
    PRED_FIELD_PROBLEM,
    PRED_FIELD_TASK_ID,
    PRED_FIELD_TRAJECTORY,
    RANDOM_SEED,
    SMOKE_ROW_LIMIT,
    TRAJECTORY_FIELDS,
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.model_call import (
    CostTracker,
    make_model_call,
    reset_cost_log,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.paths import (
    COSTS_PATH,
    JUDGE_LOG_PATH,
    METRICS_PATH,
    SMOKE_PREDICTIONS_PATH,
    SMOKE_REPORT_PATH,
    V2_DATASET_PATH,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    PlanAndSolveAgentV2,
    elicit_final_confidence,
)

# --------------------------------------------------------------------------------------------------
# Tool registries (copied from t0012)
# --------------------------------------------------------------------------------------------------


def _python_exec_str(code: str) -> str:
    import subprocess

    if not isinstance(code, str) or len(code) == 0:
        return "<error: empty or non-string code>"
    try:
        completed = subprocess.run(  # noqa: S603 — local trusted invocation
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            timeout=5.0,
        )
    except subprocess.TimeoutExpired:
        return "<error: python_exec timed out>"
    except Exception as exc:  # noqa: BLE001
        return f"<error: {type(exc).__name__}: {exc}>"
    out: str = (completed.stdout or "") + (completed.stderr or "")
    if len(out) > 64 * 1024:
        return out[: 64 * 1024] + "\n<...truncated>"
    if len(out) == 0:
        return "<no output>"
    return out


def _react_python_exec(**kwargs: Any) -> str:
    code_obj: Any = kwargs.get("code", "")
    return _python_exec_str(str(code_obj))


def _planandsolve_python_exec(args_str: str) -> str:
    return _python_exec_str(args_str)


# --------------------------------------------------------------------------------------------------
# Dataclasses
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RowOutcome:
    """One row's full per-condition result."""

    task_id: str
    problem: str
    gold_answer: str
    final_answer: str | None
    is_correct: bool
    decision_count: int
    final_confidence: float | None
    final_confidence_parse_failures: int
    trajectory: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class ConditionMetrics:
    task_success_rate: float
    overconfident_error_rate: float
    avg_decisions_per_task: float
    n: int
    parse_failure_rate: float
    parse_failure_total: int


# --------------------------------------------------------------------------------------------------
# Dataset loading + judge
# --------------------------------------------------------------------------------------------------


def load_smoke_rows(*, dataset_path: Path = V2_DATASET_PATH, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with dataset_path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            row = json.loads(stripped)
            if not isinstance(row, dict):
                continue
            if row.get("benchmark") != BENCHMARK_FILTER:
                continue
            if row.get("hierarchy_completeness") is not True:
                continue
            rows.append(row)
    rows.sort(key=lambda r: str(r.get("task_id", "")))
    return rows[:limit]


def extract_problem_text(row: dict[str, Any]) -> str:
    text_obj: Any = row.get("problem", "")
    return str(text_obj) if isinstance(text_obj, str) else ""


def extract_gold_answer(row: dict[str, Any]) -> str:
    gold_obj: Any = row.get("gold_actions", {})
    if not isinstance(gold_obj, dict):
        return ""
    parts: list[str] = []
    g_global = gold_obj.get("global")
    if isinstance(g_global, str):
        parts.append(f"GLOBAL: {g_global}")
    g_subtasks = gold_obj.get("subtasks")
    if isinstance(g_subtasks, list):
        for sub in g_subtasks:
            if not isinstance(sub, dict):
                continue
            sub_label = sub.get("subtask")
            if isinstance(sub_label, str):
                parts.append(f"SUBTASK: {sub_label}")
            atomics = sub.get("atomics")
            if isinstance(atomics, list):
                for a in atomics:
                    if isinstance(a, str):
                        parts.append(f"  ATOM: {a}")
    g_atomics = gold_obj.get("global_atomics")
    if isinstance(g_atomics, list):
        for a in g_atomics:
            if isinstance(a, str):
                parts.append(f"GLOBAL_ATOM: {a}")
    return "\n".join(parts)


JUDGE_PROMPT_TEMPLATE: str = (
    "You are an expert grader for scientific olympiad problems. Decide whether the candidate "
    "answer substantively reproduces the key derivation steps and final result of the gold "
    "answer. Allow paraphrase and equivalent algebraic forms. Reply with EXACTLY ONE word: "
    "YES or NO. No explanations, no punctuation.\n\n"
    "Problem:\n{problem}\n\n"
    "Gold answer:\n{gold}\n\n"
    "Candidate answer:\n{candidate}\n\n"
    "Verdict (YES or NO):"
)


def judge_correctness(
    *,
    task_id: str,
    problem: str,
    gold: str,
    candidate: str | None,
    judge_call: Callable[[str], str],
) -> bool:
    if candidate is None or len(candidate.strip()) == 0:
        _log_judge(task_id=task_id, candidate=candidate, raw="<no_candidate>", verdict=False)
        return False
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        problem=_truncate(problem, limit=8000),
        gold=_truncate(gold, limit=4000),
        candidate=_truncate(candidate, limit=4000),
    )
    try:
        raw = judge_call(prompt)
    except Exception as exc:  # noqa: BLE001
        _log_judge(task_id=task_id, candidate=candidate, raw=f"<error: {exc}>", verdict=False)
        return False
    verdict = _parse_yes_no(raw)
    _log_judge(task_id=task_id, candidate=candidate, raw=raw, verdict=verdict)
    return verdict


def _parse_yes_no(text: str) -> bool:
    norm = text.strip().upper()
    if norm.startswith("YES"):
        return True
    return "YES" in norm.split() and "NO" not in norm.split()[:2]


def _log_judge(*, task_id: str, candidate: str | None, raw: str, verdict: bool) -> None:
    JUDGE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JUDGE_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "task_id": task_id,
                    "candidate_chars": len(candidate) if candidate is not None else 0,
                    "raw_response": raw[:500],
                    "verdict": verdict,
                },
            )
            + "\n"
        )


def _truncate(text: str, *, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "...<truncated>"


# --------------------------------------------------------------------------------------------------
# Per-condition runners
# --------------------------------------------------------------------------------------------------


def _react_record_to_canonical(record: ReactTrajectoryRecord) -> dict[str, Any]:
    action_obj: Any = record.action
    if isinstance(action_obj, dict):
        name = str(action_obj.get("name", "<unknown>"))
        args = action_obj.get("args", {})
        if isinstance(args, dict) and len(args) > 0:
            args_str = ",".join(f"{k}={v}" for k, v in args.items())
            action_str = f"{name}({args_str})"
        else:
            action_str = name
    else:
        action_str = str(action_obj)
    return {
        TRAJECTORY_FIELDS[0]: record.turn_index,
        TRAJECTORY_FIELDS[1]: record.granularity,
        TRAJECTORY_FIELDS[2]: record.thought,
        TRAJECTORY_FIELDS[3]: action_str,
        TRAJECTORY_FIELDS[4]: record.observation,
        TRAJECTORY_FIELDS[5]: record.confidence,
    }


def _mm_record_to_canonical(record: MatchedMismatchRecord) -> dict[str, Any]:
    return {
        TRAJECTORY_FIELDS[0]: record.turn_index,
        TRAJECTORY_FIELDS[1]: record.granularity,
        TRAJECTORY_FIELDS[2]: record.thought,
        TRAJECTORY_FIELDS[3]: record.action,
        TRAJECTORY_FIELDS[4]: record.observation,
        TRAJECTORY_FIELDS[5]: record.confidence,
    }


def run_condition_a(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
) -> tuple[str | None, list[dict[str, Any]], int, float | None]:
    """Condition A: scope-aware ReAct at granularity='global', plus v2 confidence post-call."""
    problem = extract_problem_text(row)
    react_registry: Mapping[str, Callable[..., Any]] = {"python_exec": _react_python_exec}
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, dir=str(Path("/tmp"))) as tf:
        traj_path = Path(tf.name)
    try:
        agent = ScopeAwareReactAgent(
            problem=problem,
            granularity="global",
            tool_registry=react_registry,
            model_call=model_call,
            trajectory_path=traj_path,
            max_turns=MAX_TURNS,
        )
        result = agent.run()
        records = [_react_record_to_canonical(rec) for rec in result.trajectory]
        final_answer = result.answer
    finally:
        if traj_path.exists():
            traj_path.unlink()
    if final_answer is None:
        return final_answer, records, 0, None
    confidence_value, parse_failures = elicit_final_confidence(
        model_call=model_call,
        problem=problem,
        final_answer=final_answer,
    )
    return final_answer, records, parse_failures, confidence_value


def run_condition_b(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
) -> tuple[str | None, list[dict[str, Any]], int, float | None]:
    """Condition B: Plan-and-Solve v2 with built-in confidence elicitation."""
    problem = extract_problem_text(row)
    ps_registry = {"python_exec": _planandsolve_python_exec}
    agent = PlanAndSolveAgentV2(
        model_call=model_call,
        tool_registry=ps_registry,
        max_steps=MAX_TURNS,
    )
    result = agent.run(problem=problem)
    records: list[dict[str, Any]] = []
    for rec in result.trajectory:
        records.append(
            {
                TRAJECTORY_FIELDS[0]: rec.turn_index,
                TRAJECTORY_FIELDS[1]: rec.granularity,
                TRAJECTORY_FIELDS[2]: rec.thought,
                TRAJECTORY_FIELDS[3]: rec.action,
                TRAJECTORY_FIELDS[4]: rec.observation,
                TRAJECTORY_FIELDS[5]: rec.confidence,
            }
        )
    return (
        result.final_answer,
        records,
        result.final_confidence_parse_failures,
        result.final_confidence,
    )


def run_condition_c(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
) -> tuple[str | None, list[dict[str, Any]], int, float | None]:
    """Condition C: matched-mismatch (random) with the Plan-and-Solve delegate, plus v2
    confidence post-call."""
    problem = extract_problem_text(row)
    ps_registry = {"python_exec": _planandsolve_python_exec}
    agent = MatchedMismatchAgent(
        model_call=model_call,
        tool_registry=ps_registry,
        delegate="scope_unaware_planandsolve",
        mismatch_strategy="random",
        seed=RANDOM_SEED,
    )
    result = agent.run(problem=problem, annotation=row)
    records = [_mm_record_to_canonical(rec) for rec in result.trajectory]
    final_answer = result.final_answer
    if final_answer is None:
        return final_answer, records, 0, None
    confidence_value, parse_failures = elicit_final_confidence(
        model_call=model_call,
        problem=problem,
        final_answer=final_answer,
    )
    return final_answer, records, parse_failures, confidence_value


# --------------------------------------------------------------------------------------------------
# Metric computation
# --------------------------------------------------------------------------------------------------


def compute_metrics(*, outcomes: list[RowOutcome]) -> ConditionMetrics:
    n = len(outcomes)
    if n == 0:
        return ConditionMetrics(
            task_success_rate=0.0,
            overconfident_error_rate=0.0,
            avg_decisions_per_task=0.0,
            n=0,
            parse_failure_rate=0.0,
            parse_failure_total=0,
        )
    successes = sum(1 for o in outcomes if o.is_correct)
    decision_total = sum(o.decision_count for o in outcomes)
    cal_records: list[CalibrationRecord] = []
    for o in outcomes:
        if o.final_confidence is None:
            continue
        cal_records.append(
            CalibrationRecord(
                problem_id=o.task_id,
                predicted_label=o.final_answer if o.final_answer is not None else "",
                predicted_confidence=o.final_confidence,
                is_correct=o.is_correct,
            )
        )
    over_err = compute_overconfident_error_rate(
        records=cal_records,
        threshold=HIGH_CONFIDENCE_THRESHOLD,
    )
    parse_failure_total = sum(o.final_confidence_parse_failures for o in outcomes)
    # Each row issues at most 2 confidence calls (1 first-try + 1 retry); use 2*n as denom.
    parse_failure_rate = parse_failure_total / max(1, 2 * n)
    return ConditionMetrics(
        task_success_rate=successes / n,
        overconfident_error_rate=over_err,
        avg_decisions_per_task=decision_total / n,
        n=n,
        parse_failure_rate=parse_failure_rate,
        parse_failure_total=parse_failure_total,
    )


def metrics_to_dict(metrics: ConditionMetrics) -> dict[str, float]:
    return {
        METRIC_TASK_SUCCESS_RATE: metrics.task_success_rate,
        METRIC_OVERCONFIDENT_ERROR_RATE: metrics.overconfident_error_rate,
        METRIC_AVG_DECISIONS_PER_TASK: metrics.avg_decisions_per_task,
    }


# --------------------------------------------------------------------------------------------------
# Output writers
# --------------------------------------------------------------------------------------------------


def write_predictions_jsonl(
    *,
    path: Path,
    outcomes_by_condition: dict[str, list[RowOutcome]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for condition_label, outcomes in outcomes_by_condition.items():
            for outcome in outcomes:
                record: dict[str, Any] = {
                    PRED_FIELD_CONDITION: condition_label,
                    PRED_FIELD_TASK_ID: outcome.task_id,
                    PRED_FIELD_PROBLEM: outcome.problem,
                    PRED_FIELD_GOLD: outcome.gold_answer,
                    PRED_FIELD_FINAL: outcome.final_answer,
                    PRED_FIELD_IS_CORRECT: outcome.is_correct,
                    PRED_FIELD_DECISION_COUNT: outcome.decision_count,
                    PRED_FIELD_FINAL_CONFIDENCE: outcome.final_confidence,
                    PRED_FIELD_FINAL_CONFIDENCE_PARSE_FAILURES: (
                        outcome.final_confidence_parse_failures
                    ),
                    PRED_FIELD_TRAJECTORY: outcome.trajectory,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="t0021 v2 Plan-and-Solve smoke validation")
    parser.add_argument(
        "--limit",
        type=int,
        default=SMOKE_ROW_LIMIT,
        help=f"Number of rows to run per condition (default: {SMOKE_ROW_LIMIT}).",
    )
    parser.add_argument(
        "--budget-cap-usd",
        type=float,
        default=BUDGET_CAP_USD,
        help=f"Hard budget cap in USD (default: {BUDGET_CAP_USD}).",
    )
    parser.add_argument(
        "--reset-cost-log",
        action="store_true",
        help="Truncate the cost log before starting.",
    )
    args = parser.parse_args()

    if args.reset_cost_log:
        reset_cost_log()

    cost_tracker = CostTracker(cap_usd=args.budget_cap_usd)
    agent_call = make_model_call(model=MODEL_AGENT, cost_tracker=cost_tracker, note="agent")
    judge_call = make_model_call(model=MODEL_JUDGE, cost_tracker=cost_tracker, note="judge")

    rows = load_smoke_rows(limit=args.limit)
    if len(rows) == 0:
        raise RuntimeError(
            f"No rows matching benchmark={BENCHMARK_FILTER!r} found in {V2_DATASET_PATH}"
        )
    print(f"[t0021 smoke] Loaded {len(rows)} rows.")

    outcomes_by_condition: dict[str, list[RowOutcome]] = {
        VARIANT_A: [],
        VARIANT_B: [],
        VARIANT_C: [],
    }
    runners: dict[
        str,
        tuple[str, Callable[..., tuple[str | None, list[dict[str, Any]], int, float | None]]],
    ] = {
        VARIANT_A: (CONDITION_A_LABEL, run_condition_a),
        VARIANT_B: (CONDITION_B_LABEL, run_condition_b),
        VARIANT_C: (CONDITION_C_LABEL, run_condition_c),
    }

    start_time = time.time()
    for variant_id, (label, runner) in runners.items():
        print(f"[t0021 smoke] === {label} ===")
        for row in rows:
            if not cost_tracker.is_budget_ok(headroom_usd=BUDGET_HEADROOM_USD):
                print(
                    f"[t0021 smoke] BUDGET HALT: total ${cost_tracker.total_usd:.4f} >= "
                    f"cap ${args.budget_cap_usd:.2f}"
                )
                break
            task_id = str(row.get("task_id", ""))
            problem = extract_problem_text(row)
            gold_answer = extract_gold_answer(row)
            try:
                final_answer, trajectory, parse_failures, confidence = runner(
                    row=row, model_call=agent_call
                )
            except Exception as exc:  # noqa: BLE001
                print(f"[t0021 smoke] ROW {task_id} ERROR in {label}: {type(exc).__name__}: {exc}")
                final_answer = None
                trajectory = []
                parse_failures = 0
                confidence = None
            is_correct = judge_correctness(
                task_id=f"{variant_id}::{task_id}",
                problem=problem,
                gold=gold_answer,
                candidate=final_answer,
                judge_call=judge_call,
            )
            outcomes_by_condition[variant_id].append(
                RowOutcome(
                    task_id=task_id,
                    problem=problem,
                    gold_answer=gold_answer,
                    final_answer=final_answer,
                    is_correct=is_correct,
                    decision_count=len(trajectory),
                    final_confidence=confidence,
                    final_confidence_parse_failures=parse_failures,
                    trajectory=trajectory,
                )
            )
            print(
                f"[t0021 smoke]   {task_id}: answer={'<none>' if final_answer is None else 'ok'} "
                f"correct={is_correct} confidence={confidence} "
                f"parse_failures={parse_failures} cost=${cost_tracker.total_usd:.4f}"
            )
    duration_s = time.time() - start_time

    write_predictions_jsonl(
        path=SMOKE_PREDICTIONS_PATH,
        outcomes_by_condition={
            CONDITION_A_LABEL: outcomes_by_condition[VARIANT_A],
            CONDITION_B_LABEL: outcomes_by_condition[VARIANT_B],
            CONDITION_C_LABEL: outcomes_by_condition[VARIANT_C],
        },
    )

    metrics_per_condition: dict[str, ConditionMetrics] = {
        VARIANT_A: compute_metrics(outcomes=outcomes_by_condition[VARIANT_A]),
        VARIANT_B: compute_metrics(outcomes=outcomes_by_condition[VARIANT_B]),
        VARIANT_C: compute_metrics(outcomes=outcomes_by_condition[VARIANT_C]),
    }
    metrics_payload: dict[str, Any] = {
        "variants": [
            {
                "variant_id": variant_id,
                "label": runners[variant_id][0],
                "dimensions": {
                    "condition": variant_id.split("_")[1].upper(),
                    "n": metrics_per_condition[variant_id].n,
                    "model": MODEL_AGENT,
                    "parse_failure_rate": (metrics_per_condition[variant_id].parse_failure_rate),
                    "parse_failure_total": (metrics_per_condition[variant_id].parse_failure_total),
                },
                "metrics": metrics_to_dict(metrics_per_condition[variant_id]),
            }
            for variant_id in (VARIANT_A, VARIANT_B, VARIANT_C)
        ],
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")

    breakdown = cost_tracker.per_model_breakdown()
    breakdown_obj: dict[str, Any] = {
        model_name: {
            "cost_usd": round(model_data["cost_usd"], 6),
            "calls": model_data["calls"],
            "input_tokens": model_data["input_tokens"],
            "output_tokens": model_data["output_tokens"],
        }
        for model_name, model_data in breakdown.items()
    }
    costs_payload: dict[str, Any] = {
        "total_cost_usd": round(cost_tracker.total_usd, 6),
        "breakdown": breakdown_obj,
        "budget_limit": args.budget_cap_usd,
        "note": (
            f"Smoke validation: {cost_tracker.call_count} calls in "
            f"{round(duration_s, 1)}s; per-model breakdown above."
        ),
    }
    COSTS_PATH.write_text(json.dumps(costs_payload, indent=2), encoding="utf-8")

    total_parse_failures = sum(m.parse_failure_total for m in metrics_per_condition.values())
    total_calls_2x_rows = 2 * sum(m.n for m in metrics_per_condition.values())
    overall_parse_failure_rate = total_parse_failures / max(1, total_calls_2x_rows)

    report_payload: dict[str, Any] = {
        "spec_version": "1",
        "task_id": "t0021_plan_and_solve_v2_with_final_confidence",
        "rows_per_condition": [m.n for m in metrics_per_condition.values()],
        "total_cost_usd": round(cost_tracker.total_usd, 6),
        "total_calls": cost_tracker.call_count,
        "duration_s": round(duration_s, 2),
        "overall_parse_failure_rate": overall_parse_failure_rate,
        "parse_failure_rate_threshold": PARSE_FAILURE_RATE_THRESHOLD,
        "parse_failure_threshold_breached": (
            overall_parse_failure_rate > PARSE_FAILURE_RATE_THRESHOLD
        ),
        "per_condition_metrics": {
            v_id: asdict(metrics_per_condition[v_id]) for v_id in (VARIANT_A, VARIANT_B, VARIANT_C)
        },
    }
    SMOKE_REPORT_PATH.write_text(json.dumps(report_payload, indent=2), encoding="utf-8")

    print("\n[t0021 smoke] === SUMMARY ===")
    for v_id in (VARIANT_A, VARIANT_B, VARIANT_C):
        m = metrics_per_condition[v_id]
        print(
            f"  {v_id}: n={m.n} success={m.task_success_rate:.3f} "
            f"overconfident_err={m.overconfident_error_rate:.3f} "
            f"avg_decisions={m.avg_decisions_per_task:.2f} "
            f"parse_failure_rate={m.parse_failure_rate:.3f}"
        )
    print(
        f"  total_cost=${cost_tracker.total_usd:.4f} "
        f"calls={cost_tracker.call_count} duration={duration_s:.1f}s "
        f"overall_parse_failure_rate={overall_parse_failure_rate:.3f}"
    )


if __name__ == "__main__":
    main()
