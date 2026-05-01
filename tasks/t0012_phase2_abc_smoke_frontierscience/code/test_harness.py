"""Unit tests for the smoke-harness pure-function helpers.

These tests do not call any LLM; they exercise the dataset loader, gold-answer extraction, the
trajectory canonicalizers, the JSONL writer, and the stats helpers.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Any

import pytest

from tasks.t0012_phase2_abc_smoke_frontierscience.code.harness import (
    RowOutcome,
    compute_metrics,
    extract_final_confidence,
    extract_gold_answer,
    extract_problem_text,
    load_smoke_rows,
    write_predictions_jsonl,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.stats import (
    confirmatory_n_for_paired_difference,
    mcnemar_paired,
    wilson_interval,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.tools import python_exec_str


@pytest.fixture
def synthetic_dataset_path() -> Any:
    rows: list[dict[str, Any]] = [
        {
            "task_id": "fs_a",
            "benchmark": "FrontierScience-Olympiad",
            "hierarchy_completeness": True,
            "problem": "Compute 2+2.",
            "hierarchy": {"global": "g", "subtasks": [], "global_atomics": []},
            "gold_actions": {
                "global": "Answer: 4",
                "subtasks": [{"subtask": "Add", "atomics": ["2+2=4"]}],
                "global_atomics": ["finish"],
            },
        },
        {
            "task_id": "fs_b",
            "benchmark": "FrontierScience-Olympiad",
            "hierarchy_completeness": False,
            "problem": "Skip me.",
            "hierarchy": {},
            "gold_actions": {},
        },
        {
            "task_id": "wa_x",
            "benchmark": "WorkArena++",
            "hierarchy_completeness": True,
            "problem": "Skip me too.",
            "hierarchy": {},
            "gold_actions": {},
        },
    ]
    with NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8") as tf:
        for row in rows:
            tf.write(json.dumps(row) + "\n")
        path = Path(tf.name)
    yield path
    path.unlink()


def test_load_smoke_rows_filters_correctly(synthetic_dataset_path: Path) -> None:
    rows = load_smoke_rows(dataset_path=synthetic_dataset_path)
    assert len(rows) == 1
    assert rows[0]["task_id"] == "fs_a"


def test_extract_problem_and_gold(synthetic_dataset_path: Path) -> None:
    rows = load_smoke_rows(dataset_path=synthetic_dataset_path)
    row = rows[0]
    assert extract_problem_text(row=row) == "Compute 2+2."
    gold = extract_gold_answer(row=row)
    assert "GLOBAL: Answer: 4" in gold
    assert "SUBTASK: Add" in gold
    assert "ATOM: 2+2=4" in gold
    assert "GLOBAL_ATOM: finish" in gold


def test_python_exec_str_basic() -> None:
    out = python_exec_str("print(2+3)")
    assert out.strip() == "5"


def test_python_exec_str_timeout() -> None:
    out = python_exec_str("import time; time.sleep(10)")
    assert "timed out" in out


def test_python_exec_str_empty() -> None:
    assert python_exec_str("") == "<error: empty code>"


def test_extract_final_confidence_uses_last_numeric() -> None:
    traj = [
        {"turn_index": 0, "confidence": 0.6},
        {"turn_index": 1, "confidence": None},
        {"turn_index": 2, "confidence": 0.85},
    ]
    assert extract_final_confidence(trajectory=traj) == 0.85


def test_extract_final_confidence_returns_none_if_all_missing() -> None:
    traj = [
        {"turn_index": 0, "confidence": None},
        {"turn_index": 1, "confidence": None},
    ]
    assert extract_final_confidence(trajectory=traj) is None


def test_compute_metrics_basic() -> None:
    outcomes = [
        RowOutcome(
            task_id="t1",
            problem="p1",
            gold_answer="g1",
            final_answer="a1",
            is_correct=True,
            decision_count=3,
            final_confidence=0.9,
            trajectory=[],
        ),
        RowOutcome(
            task_id="t2",
            problem="p2",
            gold_answer="g2",
            final_answer="a2",
            is_correct=False,
            decision_count=2,
            final_confidence=0.85,
            trajectory=[],
        ),
        RowOutcome(
            task_id="t3",
            problem="p3",
            gold_answer="g3",
            final_answer="a3",
            is_correct=False,
            decision_count=4,
            final_confidence=0.50,
            trajectory=[],
        ),
    ]
    metrics = compute_metrics(outcomes=outcomes)
    assert abs(metrics.task_success_rate - 1 / 3) < 1e-9
    # 1 row is wrong with confidence >= 0.75 (t2) → over-rate = 1/3
    assert abs(metrics.overconfident_error_rate - 1 / 3) < 1e-9
    assert abs(metrics.avg_decisions_per_task - 3.0) < 1e-9
    assert metrics.n == 3


def test_write_predictions_jsonl_round_trip() -> None:
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "files" / "x.jsonl"
        outcomes = [
            RowOutcome(
                task_id="t1",
                problem="p",
                gold_answer="g",
                final_answer="a",
                is_correct=True,
                decision_count=2,
                final_confidence=0.5,
                trajectory=[
                    {
                        "turn_index": 0,
                        "granularity": "global",
                        "thought": "t",
                        "action": "Finish(answer=a)",
                        "observation": "a",
                        "confidence": 0.5,
                    }
                ],
            ),
        ]
        write_predictions_jsonl(path=path, condition_label="A", outcomes=outcomes)
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["task_id"] == "t1"
        assert record["is_correct"] is True
        assert len(record["trajectory"]) == 1


def test_mcnemar_paired_balanced() -> None:
    a = [True, False, True, False]
    b = [True, False, True, False]
    result = mcnemar_paired(a_correct=a, b_correct=b)
    assert result.discordant_pairs == 0
    assert result.p_value == 1.0


def test_mcnemar_paired_extreme() -> None:
    # 10 vs 0 discordant pairs → p ≈ 0.002
    a = [True] * 10 + [False] * 10
    b = [False] * 10 + [False] * 10
    result = mcnemar_paired(a_correct=a, b_correct=b)
    assert result.discordant_pairs == 10
    assert result.p_value < 0.01


def test_wilson_interval_basic() -> None:
    interval = wilson_interval(successes=8, n=10)
    assert interval.estimate == 0.8
    assert interval.lower < 0.8 < interval.upper
    assert 0.4 < interval.lower < 0.5


def test_wilson_interval_zero_n() -> None:
    interval = wilson_interval(successes=0, n=0)
    assert interval.estimate == 0.0
    assert interval.lower == 0.0
    assert interval.upper == 0.0


def test_confirmatory_n_for_5pp() -> None:
    n = confirmatory_n_for_paired_difference(
        discordant_rate_estimate=0.3,
        target_effect_pp=5.0,
    )
    assert n > 100  # 5pp paired effect needs hundreds of pairs
