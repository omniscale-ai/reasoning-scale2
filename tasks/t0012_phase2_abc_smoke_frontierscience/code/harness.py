"""Phase-2 A/B/C smoke harness: dataset loader, condition dispatcher, judge, metrics.

Runs the three condition libraries (A: scope-aware ReAct, B: scope-unaware Plan-and-Solve,
C: matched-mismatch with the Plan-and-Solve delegate) over a per-row paired loop on the
FrontierScience-Olympiad subset of the t0009 v2 dataset. Persists trajectories to a per-condition
JSONL under ``assets/predictions/`` and computes the three registered metrics per condition.
"""

from __future__ import annotations

import json
from collections.abc import Callable
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
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    PlanAndSolveAgent,
)
from tasks.t0007_scope_unaware_planandsolve_library.code.planandsolve import (
    TrajectoryRecord as PsTrajectoryRecord,
)
from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    MatchedMismatchAgent,
    MatchedMismatchRecord,
)
from tasks.t0011_metric2_calibration_aggregator.code.calibration import (
    CalibrationRecord,
    compute_overconfident_error_rate,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.constants import (
    BENCHMARK_FILTER,
    HIGH_CONFIDENCE_THRESHOLD,
    MAX_TURNS,
    METRIC_AVG_DECISIONS_PER_TASK,
    METRIC_OVERCONFIDENT_ERROR_RATE,
    METRIC_TASK_SUCCESS_RATE,
    PRED_FIELD_CONDITION,
    PRED_FIELD_DECISION_COUNT,
    PRED_FIELD_FINAL,
    PRED_FIELD_FINAL_CONFIDENCE,
    PRED_FIELD_GOLD,
    PRED_FIELD_IS_CORRECT,
    PRED_FIELD_PROBLEM,
    PRED_FIELD_TASK_ID,
    PRED_FIELD_TRAJECTORY,
    RANDOM_SEED,
    TRAJECTORY_FIELDS,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.paths import (
    JUDGE_LOG_PATH,
    V2_DATASET_PATH,
)

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
    trajectory: list[dict[str, Any]]


@dataclass(frozen=True, slots=True)
class ConditionMetrics:
    """Computed metrics for one condition."""

    task_success_rate: float
    overconfident_error_rate: float
    avg_decisions_per_task: float
    n: int


# --------------------------------------------------------------------------------------------------
# Dataset loading
# --------------------------------------------------------------------------------------------------


def load_smoke_rows(*, dataset_path: Path = V2_DATASET_PATH) -> list[dict[str, Any]]:
    """Load FrontierScience-Olympiad rows with hierarchy_completeness=True, sorted by task_id."""
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
    return rows


def extract_problem_text(row: dict[str, Any]) -> str:
    text_obj: Any = row.get("problem", "")
    return str(text_obj) if isinstance(text_obj, str) else ""


def extract_gold_answer(row: dict[str, Any]) -> str:
    """Concatenate gold_actions['global'] plus all subtask + global_atomic gold actions."""
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


# --------------------------------------------------------------------------------------------------
# Judge
# --------------------------------------------------------------------------------------------------


def judge_correctness(
    *,
    task_id: str,
    problem: str,
    gold: str,
    candidate: str | None,
    judge_call: Callable[[str], str],
) -> bool:
    """Haiku binary judge. Returns False on null candidate (early termination before Finish)."""
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


def run_condition_a(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
    react_tool_registry: Any,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Condition A: scope-aware ReAct at granularity='global'."""
    problem = extract_problem_text(row)
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, dir=str(Path("/tmp"))) as tf:
        traj_path = Path(tf.name)
    try:
        agent = ScopeAwareReactAgent(
            problem=problem,
            granularity="global",
            tool_registry=react_tool_registry,
            model_call=model_call,
            trajectory_path=traj_path,
            max_turns=MAX_TURNS,
        )
        result = agent.run()
        records: list[dict[str, Any]] = [
            _react_record_to_canonical(rec) for rec in result.trajectory
        ]
        return result.answer, records
    finally:
        if traj_path.exists():
            traj_path.unlink()


def _react_record_to_canonical(record: ReactTrajectoryRecord) -> dict[str, Any]:
    """Map t0006's TrajectoryRecord (action is dict) onto the canonical six-field schema where
    action is a string (matching t0007/t0010)."""
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


def run_condition_b(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
    plansolve_tool_registry: Any,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Condition B: scope-unaware Plan-and-Solve."""
    problem = extract_problem_text(row)
    agent = PlanAndSolveAgent(
        model_call=model_call,
        tool_registry=plansolve_tool_registry,
        max_steps=MAX_TURNS,
    )
    result = agent.run(problem)
    records: list[dict[str, Any]] = [_ps_record_to_canonical(rec) for rec in result.trajectory]
    return result.final_answer, records


def _ps_record_to_canonical(record: PsTrajectoryRecord) -> dict[str, Any]:
    return {
        TRAJECTORY_FIELDS[0]: record.turn_index,
        TRAJECTORY_FIELDS[1]: record.granularity,
        TRAJECTORY_FIELDS[2]: record.thought,
        TRAJECTORY_FIELDS[3]: record.action,
        TRAJECTORY_FIELDS[4]: record.observation,
        TRAJECTORY_FIELDS[5]: record.confidence,
    }


def run_condition_c(
    *,
    row: dict[str, Any],
    model_call: Callable[[str], str],
    plansolve_tool_registry: Any,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Condition C: matched-mismatch with the Plan-and-Solve delegate, random strategy."""
    problem = extract_problem_text(row)
    agent = MatchedMismatchAgent(
        model_call=model_call,
        tool_registry=plansolve_tool_registry,
        delegate="scope_unaware_planandsolve",
        mismatch_strategy="random",
        seed=RANDOM_SEED,
    )
    result = agent.run(problem=problem, annotation=row)
    records: list[dict[str, Any]] = [_mm_record_to_canonical(rec) for rec in result.trajectory]
    return result.final_answer, records


def _mm_record_to_canonical(record: MatchedMismatchRecord) -> dict[str, Any]:
    """Strip extras to keep schema parity with A/B JSONL."""
    return {
        TRAJECTORY_FIELDS[0]: record.turn_index,
        TRAJECTORY_FIELDS[1]: record.granularity,
        TRAJECTORY_FIELDS[2]: record.thought,
        TRAJECTORY_FIELDS[3]: record.action,
        TRAJECTORY_FIELDS[4]: record.observation,
        TRAJECTORY_FIELDS[5]: record.confidence,
    }


# --------------------------------------------------------------------------------------------------
# Per-condition metric computation
# --------------------------------------------------------------------------------------------------


def extract_final_confidence(*, trajectory: list[dict[str, Any]]) -> float | None:
    """Use the last numeric confidence value present in the trajectory; else None.

    The smoke run skips post-hoc confidence elicitation per the plan's documented simplification —
    if the trajectory carries no confidence (e.g., Plan-and-Solve never emits one), the row
    contributes None and is excluded from the overconfident-error-rate denominator.
    """
    for rec in reversed(trajectory):
        c: Any = rec.get(TRAJECTORY_FIELDS[5])
        if isinstance(c, int | float):
            return float(c)
    return None


def compute_metrics(*, outcomes: list[RowOutcome]) -> ConditionMetrics:
    """Compute the three registered metrics for one condition."""
    n = len(outcomes)
    if n == 0:
        return ConditionMetrics(
            task_success_rate=0.0,
            overconfident_error_rate=0.0,
            avg_decisions_per_task=0.0,
            n=0,
        )
    successes = sum(1 for o in outcomes if o.is_correct)
    success_rate = successes / n
    decision_total = sum(o.decision_count for o in outcomes)
    avg_decisions = decision_total / n
    # Overconfident error rate: only count rows that actually have a numeric confidence.
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
    return ConditionMetrics(
        task_success_rate=success_rate,
        overconfident_error_rate=over_err,
        avg_decisions_per_task=avg_decisions,
        n=n,
    )


def metrics_to_dict(metrics: ConditionMetrics) -> dict[str, float]:
    return {
        METRIC_TASK_SUCCESS_RATE: metrics.task_success_rate,
        METRIC_OVERCONFIDENT_ERROR_RATE: metrics.overconfident_error_rate,
        METRIC_AVG_DECISIONS_PER_TASK: metrics.avg_decisions_per_task,
    }


# --------------------------------------------------------------------------------------------------
# JSONL writer
# --------------------------------------------------------------------------------------------------


def write_predictions_jsonl(
    *,
    path: Path,
    condition_label: str,
    outcomes: list[RowOutcome],
) -> None:
    """Write one prediction per row to ``path``, JSON Lines, schema-stable across conditions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
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
                PRED_FIELD_TRAJECTORY: outcome.trajectory,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def outcomes_to_jsonable(outcomes: list[RowOutcome]) -> list[dict[str, Any]]:
    """Adapt outcomes for intermediate-state JSON persistence."""
    return [asdict(o) for o in outcomes]


def jsonable_to_outcomes(items: list[dict[str, Any]]) -> list[RowOutcome]:
    out: list[RowOutcome] = []
    for it in items:
        out.append(
            RowOutcome(
                task_id=str(it["task_id"]),
                problem=str(it["problem"]),
                gold_answer=str(it["gold_answer"]),
                final_answer=(None if it.get("final_answer") is None else str(it["final_answer"])),
                is_correct=bool(it["is_correct"]),
                decision_count=int(it["decision_count"]),
                final_confidence=(
                    None if it.get("final_confidence") is None else float(it["final_confidence"])
                ),
                trajectory=list(it.get("trajectory", [])),
            )
        )
    return out
