"""Metric 2 calibration aggregator (Xiong2024 protocol).

This module operationalizes the project's Metric 2 ``overconfident_error_rate`` using the
Xiong2024 §3.2 black-box calibration protocol — verbalized "low / medium / high" confidence
elicitation plus 3-sample self-consistency aggregation.

The library is deliberately small and dependency-free. It exposes a model-call shape so
deterministic tests can pass a ``ScriptedModel``-style fake; it never makes live API calls.

Public surface:

* :class:`CalibrationRecord` — frozen dataclass consumed by
  :func:`compute_overconfident_error_rate`.
* :class:`ConfidenceSample` — one parsed (label, confidence) sample.
* :class:`ConfidenceAggregate` — output of self-consistency aggregation.
* :class:`MalformedConfidenceError` — raised when a model response cannot be parsed.
* :class:`ConfidencePromptTemplate` — wraps the human-inspired prompt template.
* :class:`ConfidenceJudge` — 3-sample self-consistency aggregator and judge.
* :func:`elicit_confidence` — single-call confidence elicitation.
* :func:`compute_overconfident_error_rate` — fraction of records that are wrong with high
  stated confidence.

The aggregation rules follow Xiong2024:

1. Sample the model :data:`SELF_CONSISTENCY_SAMPLES` times (default 3).
2. Majority vote on the predicted label (the action being judged).
3. Aggregated confidence is the mean confidence within the majority cohort.
4. If every sample has a distinct label (a 3-way tie), return the highest-confidence sample.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from tasks.t0011_metric2_calibration_aggregator.code.constants import (
    CONFIDENCE_PREFIX,
    DEFAULT_PROMPT_TEMPLATE,
    HIGH_CONFIDENCE_THRESHOLD,
    LABEL_TO_CONFIDENCE,
    PROMPT_ACTION_PLACEHOLDER,
    PROMPT_PROBLEM_PLACEHOLDER,
    SELF_CONSISTENCY_SAMPLES,
    TRAJECTORY_FIELD_ACTION,
    TRAJECTORY_FIELD_CONFIDENCE,
    VALID_CONFIDENCE_LABELS,
)

# --------------------------------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------------------------------


class MalformedConfidenceError(ValueError):
    """Raised when a model response does not contain a parseable confidence label."""


# --------------------------------------------------------------------------------------------------
# Dataclasses
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ConfidenceSample:
    """One parsed self-consistency sample for a single (problem, action) pair.

    ``predicted_label`` is the action label being judged; ``verbalized_confidence`` is the raw
    label the model produced (one of ``low``/``medium``/``high``); ``predicted_confidence`` is
    the numeric mapping per :data:`LABEL_TO_CONFIDENCE`.
    """

    predicted_label: str
    verbalized_confidence: str
    predicted_confidence: float
    raw_response: str


@dataclass(frozen=True, slots=True)
class ConfidenceAggregate:
    """Result of self-consistency aggregation across multiple :class:`ConfidenceSample` values."""

    predicted_label: str
    predicted_confidence: float
    samples: tuple[ConfidenceSample, ...]


@dataclass(frozen=True, slots=True)
class CalibrationRecord:
    """One calibrated prediction consumed by :func:`compute_overconfident_error_rate`.

    Produced by :meth:`ConfidenceJudge.judge` or constructed directly. ``predicted_confidence``
    is the aggregated numeric confidence. ``is_correct`` compares ``predicted_label`` against
    the gold action externally; this library does not infer correctness on its own.
    """

    problem_id: str
    predicted_label: str
    predicted_confidence: float
    is_correct: bool


# --------------------------------------------------------------------------------------------------
# Type aliases
# --------------------------------------------------------------------------------------------------


class ModelCall(Protocol):
    """Callable that takes a prompt string and returns a model response string."""

    def __call__(self, prompt: str) -> str: ...


# --------------------------------------------------------------------------------------------------
# Prompt template
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ConfidencePromptTemplate:
    """Human-inspired confidence-elicitation prompt template (Xiong2024 §3.2).

    The template must contain the placeholders ``{problem}`` and ``{action}`` exactly once
    each; otherwise :class:`ValueError` is raised at construction time. Use the default
    factory if you do not need to override the template body.
    """

    template: str = DEFAULT_PROMPT_TEMPLATE

    def __post_init__(self) -> None:
        if PROMPT_PROBLEM_PLACEHOLDER not in self.template:
            raise ValueError(
                f"Prompt template is missing the {PROMPT_PROBLEM_PLACEHOLDER} placeholder."
            )
        if PROMPT_ACTION_PLACEHOLDER not in self.template:
            raise ValueError(
                f"Prompt template is missing the {PROMPT_ACTION_PLACEHOLDER} placeholder."
            )

    def format(self, *, problem: str, action: str) -> str:
        """Return the rendered prompt for one (problem, action) pair."""
        return self.template.format(problem=problem, action=action)


# --------------------------------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------------------------------


_LABEL_TOKEN_RE: re.Pattern[str] = re.compile(
    r"\b(low|medium|high)\b",
    re.IGNORECASE,
)


def _parse_confidence_label(response: str) -> str:
    """Extract the verbalized confidence label from a model response.

    Strategy:

    1. Look for a line starting with ``Confidence:`` (case-insensitive). If found, use the
       first :data:`VALID_CONFIDENCE_LABELS` token on that line.
    2. Otherwise, fall back to the first matching token anywhere in the response.

    Raises :class:`MalformedConfidenceError` if no valid label is found.
    """
    for raw_line in response.splitlines():
        stripped = raw_line.strip()
        if stripped.lower().startswith(CONFIDENCE_PREFIX):
            tail = stripped[len(CONFIDENCE_PREFIX) :]
            match = _LABEL_TOKEN_RE.search(tail)
            if match is not None:
                return match.group(1).lower()
    fallback = _LABEL_TOKEN_RE.search(response)
    if fallback is not None:
        return fallback.group(1).lower()
    raise MalformedConfidenceError(
        "Model response does not contain a low/medium/high confidence label."
    )


# --------------------------------------------------------------------------------------------------
# Single-call elicitation
# --------------------------------------------------------------------------------------------------


def elicit_confidence(
    *,
    model_call: ModelCall,
    problem: str,
    action: str,
    prompt_template: ConfidencePromptTemplate | None = None,
) -> tuple[str, float]:
    """Format the confidence prompt, call the model once, and parse the response.

    Returns a tuple ``(verbalized_label, numeric_confidence)`` where ``verbalized_label`` is
    one of ``low``/``medium``/``high`` and ``numeric_confidence`` comes from
    :data:`LABEL_TO_CONFIDENCE`.

    Raises :class:`MalformedConfidenceError` if the model response cannot be parsed.
    """
    template = prompt_template if prompt_template is not None else ConfidencePromptTemplate()
    prompt = template.format(problem=problem, action=action)
    response = model_call(prompt=prompt)
    label = _parse_confidence_label(response=response)
    return label, LABEL_TO_CONFIDENCE[label]


# --------------------------------------------------------------------------------------------------
# Aggregator and judge
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class ConfidenceJudge:
    """Self-consistency aggregator and per-problem judge.

    ``samples`` is the number of (already-sampled) actions to aggregate; defaults to
    :data:`SELF_CONSISTENCY_SAMPLES` (3 per Xiong2024).

    Aggregation rules:

    * Majority vote on ``predicted_label``.
    * Aggregated confidence is the mean of ``predicted_confidence`` within the majority cohort.
    * On a 3-way tie (every sample has a distinct label), return the sample with the highest
      ``predicted_confidence``. If two samples in a 3-way tie share the maximum confidence, the
      first one in input order wins.
    """

    samples: int = SELF_CONSISTENCY_SAMPLES
    prompt_template: ConfidencePromptTemplate = field(default_factory=ConfidencePromptTemplate)

    def aggregate(
        self,
        confidence_samples: Sequence[ConfidenceSample],
    ) -> ConfidenceAggregate:
        """Aggregate ``confidence_samples`` into a single :class:`ConfidenceAggregate`."""
        if len(confidence_samples) == 0:
            raise ValueError("Cannot aggregate an empty sequence of confidence samples.")
        counts = Counter(sample.predicted_label for sample in confidence_samples)
        most_common = counts.most_common()
        top_count = most_common[0][1]
        top_labels = {label for label, count in most_common if count == top_count}
        is_clean_majority = len(top_labels) == 1
        if is_clean_majority:
            majority_label = most_common[0][0]
            cohort = tuple(s for s in confidence_samples if s.predicted_label == majority_label)
            mean_confidence = sum(s.predicted_confidence for s in cohort) / len(cohort)
            return ConfidenceAggregate(
                predicted_label=majority_label,
                predicted_confidence=mean_confidence,
                samples=tuple(confidence_samples),
            )
        # Tie: fall back to the highest-confidence sample (first wins on equal max).
        winner = max(
            confidence_samples,
            key=lambda s: s.predicted_confidence,
        )
        return ConfidenceAggregate(
            predicted_label=winner.predicted_label,
            predicted_confidence=winner.predicted_confidence,
            samples=tuple(confidence_samples),
        )

    def judge(
        self,
        *,
        problem_id: str,
        problem: str,
        sampled_actions: Sequence[str],
        gold_action: str,
        model_call: ModelCall,
    ) -> CalibrationRecord:
        """Score one problem end-to-end and return a :class:`CalibrationRecord`.

        For each entry in ``sampled_actions``, calls ``model_call`` once via
        :func:`elicit_confidence`, builds a :class:`ConfidenceSample`, and aggregates with
        :meth:`aggregate`. ``is_correct`` is set to
        ``aggregate.predicted_label == gold_action``.
        """
        if len(sampled_actions) == 0:
            raise ValueError("sampled_actions must contain at least one element.")
        samples: list[ConfidenceSample] = []
        for action in sampled_actions:
            template = self.prompt_template
            prompt = template.format(problem=problem, action=action)
            raw = model_call(prompt=prompt)
            label = _parse_confidence_label(response=raw)
            samples.append(
                ConfidenceSample(
                    predicted_label=action,
                    verbalized_confidence=label,
                    predicted_confidence=LABEL_TO_CONFIDENCE[label],
                    raw_response=raw,
                )
            )
        aggregate = self.aggregate(confidence_samples=samples)
        return CalibrationRecord(
            problem_id=problem_id,
            predicted_label=aggregate.predicted_label,
            predicted_confidence=aggregate.predicted_confidence,
            is_correct=aggregate.predicted_label == gold_action,
        )


# --------------------------------------------------------------------------------------------------
# Trajectory record adapter
# --------------------------------------------------------------------------------------------------


def calibration_record_from_trajectory(
    *,
    problem_id: str,
    record: Mapping[str, object],
    is_correct: bool,
) -> CalibrationRecord:
    """Adapt a trajectory record (t0006/t0007/t0010 schema) into a :class:`CalibrationRecord`.

    ``record`` must expose at least the canonical trajectory fields ``action`` and
    ``confidence``. ``confidence`` may be either a numeric value (already mapped) or one of the
    verbalized labels (low/medium/high); the latter is mapped via :data:`LABEL_TO_CONFIDENCE`.
    Records with ``confidence`` set to ``None`` raise :class:`ValueError` because the metric is
    undefined without a confidence value.
    """
    if TRAJECTORY_FIELD_ACTION not in record:
        raise KeyError(f"Trajectory record missing required field {TRAJECTORY_FIELD_ACTION!r}.")
    if TRAJECTORY_FIELD_CONFIDENCE not in record:
        raise KeyError(f"Trajectory record missing required field {TRAJECTORY_FIELD_CONFIDENCE!r}.")
    action_value = record[TRAJECTORY_FIELD_ACTION]
    if not isinstance(action_value, str):
        raise TypeError(
            f"Trajectory record {TRAJECTORY_FIELD_ACTION!r} must be a string; "
            f"got {type(action_value).__name__}."
        )
    confidence_value = record[TRAJECTORY_FIELD_CONFIDENCE]
    if confidence_value is None:
        raise ValueError(
            "Trajectory record has confidence=None; cannot compute calibration record."
        )
    if isinstance(confidence_value, str):
        normalized = confidence_value.strip().lower()
        if normalized not in VALID_CONFIDENCE_LABELS:
            raise ValueError(
                f"Trajectory record confidence string {confidence_value!r} is not a "
                "valid verbalized label."
            )
        numeric_confidence = LABEL_TO_CONFIDENCE[normalized]
    elif isinstance(confidence_value, int | float):
        numeric_confidence = float(confidence_value)
    else:
        raise TypeError(
            f"Trajectory record confidence must be a string label or a number; "
            f"got {type(confidence_value).__name__}."
        )
    return CalibrationRecord(
        problem_id=problem_id,
        predicted_label=action_value,
        predicted_confidence=numeric_confidence,
        is_correct=is_correct,
    )


# --------------------------------------------------------------------------------------------------
# Metric
# --------------------------------------------------------------------------------------------------


def compute_overconfident_error_rate(
    *,
    records: Iterable[CalibrationRecord],
    threshold: float = HIGH_CONFIDENCE_THRESHOLD,
) -> float:
    """Return the fraction of ``records`` that are incorrect with high stated confidence.

    A record is "overconfident" if ``not is_correct`` and ``predicted_confidence >= threshold``.
    Returns ``0.0`` for an empty input iterable.
    """
    materialized = list(records)
    if len(materialized) == 0:
        return 0.0
    overconfident = sum(
        1
        for record in materialized
        if (not record.is_correct) and record.predicted_confidence >= threshold
    )
    return overconfident / len(materialized)
