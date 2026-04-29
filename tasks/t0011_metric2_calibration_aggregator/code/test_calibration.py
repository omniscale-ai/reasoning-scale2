"""Tests for the metric2_calibration_aggregator_v1 library."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from tasks.t0011_metric2_calibration_aggregator.code.calibration import (
    CalibrationRecord,
    ConfidenceJudge,
    ConfidencePromptTemplate,
    ConfidenceSample,
    MalformedConfidenceError,
    calibration_record_from_trajectory,
    compute_overconfident_error_rate,
    elicit_confidence,
)
from tasks.t0011_metric2_calibration_aggregator.code.constants import (
    CONFIDENCE_HIGH_VALUE,
    CONFIDENCE_LOW_VALUE,
    CONFIDENCE_MEDIUM_VALUE,
    HIGH_CONFIDENCE_THRESHOLD,
    LABEL_HIGH,
    LABEL_LOW,
    LABEL_MEDIUM,
    SELF_CONSISTENCY_SAMPLES,
)

# --------------------------------------------------------------------------------------------------
# Test fakes
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class ScriptedModel:
    """Deterministic fake mirroring t0007's ``ScriptedModel`` interface.

    Returns the next response in ``responses`` on each call, ignoring the prompt. Raises
    ``IndexError`` when exhausted so test failures surface immediately rather than silently
    repeating the last response.
    """

    responses: list[str]
    cursor: int = field(default=0)

    def __call__(self, *, prompt: str) -> str:  # noqa: ARG002 — prompt intentionally ignored
        if self.cursor >= len(self.responses):
            raise IndexError("ScriptedModel exhausted: no more pre-recorded responses")
        out = self.responses[self.cursor]
        self.cursor += 1
        return out


# --------------------------------------------------------------------------------------------------
# ConfidencePromptTemplate
# --------------------------------------------------------------------------------------------------


def test_prompt_template_default_contains_placeholders() -> None:
    template = ConfidencePromptTemplate()
    rendered = template.format(problem="What is 2+2?", action="Compute the sum.")
    assert "What is 2+2?" in rendered
    assert "Compute the sum." in rendered
    assert "low" in rendered
    assert "medium" in rendered
    assert "high" in rendered


def test_prompt_template_rejects_missing_problem_placeholder() -> None:
    with pytest.raises(ValueError, match="problem"):
        ConfidencePromptTemplate(template="Action: {action}")


def test_prompt_template_rejects_missing_action_placeholder() -> None:
    with pytest.raises(ValueError, match="action"):
        ConfidencePromptTemplate(template="Problem: {problem}")


# --------------------------------------------------------------------------------------------------
# elicit_confidence and label parsing
# --------------------------------------------------------------------------------------------------


def test_elicit_confidence_parses_high_label() -> None:
    model = ScriptedModel(responses=["Confidence: high\nThe answer follows from arithmetic."])
    label, value = elicit_confidence(
        model_call=model,
        problem="2+2?",
        action="Add 2 and 2",
    )
    assert label == LABEL_HIGH
    assert value == CONFIDENCE_HIGH_VALUE


def test_elicit_confidence_parses_low_label() -> None:
    model = ScriptedModel(responses=["Confidence: LOW\nUnsure about edge case."])
    label, value = elicit_confidence(
        model_call=model,
        problem="?",
        action="Try X",
    )
    assert label == LABEL_LOW
    assert value == CONFIDENCE_LOW_VALUE


def test_elicit_confidence_parses_medium_label_in_freeform_text() -> None:
    # No "Confidence:" prefix; parser falls back to first matching token in body.
    model = ScriptedModel(responses=["I would say my confidence is medium overall, honestly."])
    label, value = elicit_confidence(
        model_call=model,
        problem="?",
        action="Try Y",
    )
    assert label == LABEL_MEDIUM
    assert value == CONFIDENCE_MEDIUM_VALUE


def test_elicit_confidence_raises_on_unparseable_response() -> None:
    model = ScriptedModel(responses=["I cannot determine confidence here."])
    with pytest.raises(MalformedConfidenceError):
        elicit_confidence(
            model_call=model,
            problem="?",
            action="Z",
        )


def test_elicit_confidence_prefix_overrides_freeform_text() -> None:
    # Freeform body contains "low", but the Confidence: prefix says high — the prefix wins.
    model = ScriptedModel(
        responses=["I have a low opinion of this question.\nConfidence: high\nReason."],
    )
    label, _ = elicit_confidence(
        model_call=model,
        problem="?",
        action="W",
    )
    assert label == LABEL_HIGH


# --------------------------------------------------------------------------------------------------
# ConfidenceJudge.aggregate
# --------------------------------------------------------------------------------------------------


def _sample(label: str, conf: float, verbalized: str = "high") -> ConfidenceSample:
    return ConfidenceSample(
        predicted_label=label,
        verbalized_confidence=verbalized,
        predicted_confidence=conf,
        raw_response="<scripted>",
    )


def test_aggregate_clean_majority_uses_cohort_mean() -> None:
    judge = ConfidenceJudge()
    aggregate = judge.aggregate(
        confidence_samples=[
            _sample("A", 0.9),
            _sample("A", 0.5),
            _sample("B", 0.9),
        ],
    )
    assert aggregate.predicted_label == "A"
    # Mean within majority cohort (A, A) is (0.9 + 0.5) / 2 = 0.7, NOT global mean 0.7666...
    assert aggregate.predicted_confidence == pytest.approx(0.7)


def test_aggregate_unanimous_returns_global_mean() -> None:
    judge = ConfidenceJudge()
    aggregate = judge.aggregate(
        confidence_samples=[
            _sample("A", 0.9),
            _sample("A", 0.9),
            _sample("A", 0.5),
        ],
    )
    assert aggregate.predicted_label == "A"
    assert aggregate.predicted_confidence == pytest.approx((0.9 + 0.9 + 0.5) / 3)


def test_aggregate_three_way_tie_returns_highest_confidence_sample() -> None:
    judge = ConfidenceJudge()
    aggregate = judge.aggregate(
        confidence_samples=[
            _sample("A", 0.5),
            _sample("B", 0.9),
            _sample("C", 0.25),
        ],
    )
    assert aggregate.predicted_label == "B"
    assert aggregate.predicted_confidence == pytest.approx(0.9)


def test_aggregate_three_way_tie_picks_first_on_equal_max() -> None:
    judge = ConfidenceJudge()
    aggregate = judge.aggregate(
        confidence_samples=[
            _sample("A", 0.9),
            _sample("B", 0.9),
            _sample("C", 0.9),
        ],
    )
    # All three labels tied with identical confidence; first wins.
    assert aggregate.predicted_label == "A"
    assert aggregate.predicted_confidence == pytest.approx(0.9)


def test_aggregate_rejects_empty_samples() -> None:
    judge = ConfidenceJudge()
    with pytest.raises(ValueError, match="empty"):
        judge.aggregate(confidence_samples=[])


# --------------------------------------------------------------------------------------------------
# ConfidenceJudge.judge — end-to-end with ScriptedModel
# --------------------------------------------------------------------------------------------------


def test_judge_end_to_end_correct_majority() -> None:
    model = ScriptedModel(
        responses=[
            "Confidence: high\nReason 1.",
            "Confidence: high\nReason 2.",
            "Confidence: medium\nReason 3.",
        ],
    )
    judge = ConfidenceJudge()
    record = judge.judge(
        problem_id="p1",
        problem="What is 2+2?",
        sampled_actions=["Add 2 and 2", "Add 2 and 2", "Multiply 2 by 2"],
        gold_action="Add 2 and 2",
        model_call=model,
    )
    assert record.problem_id == "p1"
    assert record.predicted_label == "Add 2 and 2"
    # Majority cohort = 2 samples both verbalized "high" -> mean 0.9.
    assert record.predicted_confidence == pytest.approx(CONFIDENCE_HIGH_VALUE)
    assert record.is_correct is True


def test_judge_marks_wrong_when_majority_label_differs_from_gold() -> None:
    model = ScriptedModel(
        responses=[
            "Confidence: high\nReason 1.",
            "Confidence: high\nReason 2.",
            "Confidence: low\nReason 3.",
        ],
    )
    judge = ConfidenceJudge()
    record = judge.judge(
        problem_id="p2",
        problem="?",
        sampled_actions=["wrong_action", "wrong_action", "right_action"],
        gold_action="right_action",
        model_call=model,
    )
    assert record.predicted_label == "wrong_action"
    assert record.is_correct is False
    assert record.predicted_confidence == pytest.approx(CONFIDENCE_HIGH_VALUE)


def test_judge_rejects_empty_sampled_actions() -> None:
    judge = ConfidenceJudge()
    with pytest.raises(ValueError, match="sampled_actions"):
        judge.judge(
            problem_id="p3",
            problem="?",
            sampled_actions=[],
            gold_action="x",
            model_call=ScriptedModel(responses=[]),
        )


# --------------------------------------------------------------------------------------------------
# compute_overconfident_error_rate
# --------------------------------------------------------------------------------------------------


def _record(
    *, is_correct: bool, conf: float, problem_id: str = "p", label: str = "x"
) -> CalibrationRecord:
    return CalibrationRecord(
        problem_id=problem_id,
        predicted_label=label,
        predicted_confidence=conf,
        is_correct=is_correct,
    )


def test_overconfident_error_rate_at_threshold_boundary() -> None:
    # 0.75 is exactly the threshold; >= must qualify.
    records = [
        _record(is_correct=False, conf=HIGH_CONFIDENCE_THRESHOLD, problem_id="p1"),
        _record(is_correct=False, conf=HIGH_CONFIDENCE_THRESHOLD - 0.01, problem_id="p2"),
    ]
    rate = compute_overconfident_error_rate(records=records)
    # One out of two qualifies (the at-threshold one).
    assert rate == pytest.approx(0.5)


def test_overconfident_error_rate_correct_high_confidence_does_not_count() -> None:
    records = [
        _record(is_correct=True, conf=0.9, problem_id="p1"),
        _record(is_correct=True, conf=0.9, problem_id="p2"),
    ]
    assert compute_overconfident_error_rate(records=records) == pytest.approx(0.0)


def test_overconfident_error_rate_empty_returns_zero() -> None:
    assert compute_overconfident_error_rate(records=[]) == 0.0


def test_overconfident_error_rate_synthetic_ten_record_dataset() -> None:
    # Synthesize 10 records: 4 overconfident-error, 3 correct-high, 2 wrong-low, 1 correct-low.
    records: list[CalibrationRecord] = [
        _record(is_correct=False, conf=0.9, problem_id=f"p{i}") for i in range(4)
    ]
    records += [_record(is_correct=True, conf=0.9, problem_id=f"p{i}") for i in range(4, 7)]
    records += [_record(is_correct=False, conf=0.25, problem_id=f"p{i}") for i in range(7, 9)]
    records += [_record(is_correct=True, conf=0.5, problem_id="p9")]
    assert len(records) == 10
    rate = compute_overconfident_error_rate(records=records)
    assert rate == pytest.approx(4.0 / 10.0)


def test_overconfident_error_rate_respects_custom_threshold() -> None:
    records = [
        _record(is_correct=False, conf=0.5, problem_id="p1"),
        _record(is_correct=False, conf=0.9, problem_id="p2"),
    ]
    # With threshold 0.4, both qualify.
    assert compute_overconfident_error_rate(records=records, threshold=0.4) == pytest.approx(1.0)
    # With threshold 0.95, neither qualifies.
    assert compute_overconfident_error_rate(records=records, threshold=0.95) == pytest.approx(0.0)


# --------------------------------------------------------------------------------------------------
# Trajectory record adapter
# --------------------------------------------------------------------------------------------------


def test_calibration_record_from_trajectory_with_verbalized_label() -> None:
    record = calibration_record_from_trajectory(
        problem_id="p1",
        record={
            "turn_index": 0,
            "granularity": "unspecified",
            "thought": "...",
            "action": "do_x",
            "observation": "ok",
            "confidence": "high",
        },
        is_correct=False,
    )
    assert record.predicted_label == "do_x"
    assert record.predicted_confidence == pytest.approx(CONFIDENCE_HIGH_VALUE)
    assert record.is_correct is False


def test_calibration_record_from_trajectory_with_numeric_confidence() -> None:
    record = calibration_record_from_trajectory(
        problem_id="p2",
        record={
            "turn_index": 1,
            "granularity": "unspecified",
            "thought": "...",
            "action": "do_y",
            "observation": "ok",
            "confidence": 0.42,
        },
        is_correct=True,
    )
    assert record.predicted_confidence == pytest.approx(0.42)


def test_calibration_record_from_trajectory_rejects_none_confidence() -> None:
    with pytest.raises(ValueError, match="confidence=None"):
        calibration_record_from_trajectory(
            problem_id="p3",
            record={
                "turn_index": 0,
                "granularity": "unspecified",
                "thought": "...",
                "action": "do_z",
                "observation": "ok",
                "confidence": None,
            },
            is_correct=False,
        )


# --------------------------------------------------------------------------------------------------
# Constants sanity
# --------------------------------------------------------------------------------------------------


def test_constants_match_xiong2024_protocol() -> None:
    assert SELF_CONSISTENCY_SAMPLES == 3
    assert HIGH_CONFIDENCE_THRESHOLD == 0.75
    assert CONFIDENCE_LOW_VALUE == 0.25
    assert CONFIDENCE_MEDIUM_VALUE == 0.5
    assert CONFIDENCE_HIGH_VALUE == 0.9
