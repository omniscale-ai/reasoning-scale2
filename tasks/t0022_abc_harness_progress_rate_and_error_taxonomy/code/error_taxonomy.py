"""Li2024 Embodied Agent Interface error-taxonomy classifier.

Implements the Li et al. 2024 (NeurIPS 2024) §A.4 strict-output classifier
schema. Each call returns exactly one of seven labels (six error labels plus
the project-added ``ok`` sentinel for non-error steps). On parse failure or
ambiguous output, the function returns
:attr:`ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT` per the t0022 task spec
tie-break rule.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.constants import (
    DEFAULT_TIE_BREAK_LABEL,
    ERROR_TAXONOMY_PROMPT_KEY,
    ERROR_TAXONOMY_SYSTEM_PROMPT,
    ERROR_TAXONOMY_USER_TEMPLATE,
    JUDGE_MODEL_DEFAULT,
    MAX_OBSERVATION_CHARS,
    MAX_THOUGHT_CHARS,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache import (
    cache_get,
    cache_put,
    hash_trajectory_step,
    make_cache_key,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.model_call import (
    CostTracker,
    make_judge_call,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    ErrorTaxonomyLabel,
    TrajectoryStep,
)

JudgeCallable = Callable[[str], str]

_VALID_LABEL_VALUES: frozenset[str] = frozenset(label.value for label in ErrorTaxonomyLabel)


def _truncate(*, text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def _build_error_prompt(*, step: TrajectoryStep, environment_state: dict[str, Any]) -> str:
    state_repr = json.dumps(environment_state, sort_keys=True)[:600]
    return ERROR_TAXONOMY_USER_TEMPLATE.format(
        environment_state=state_repr,
        thought=_truncate(text=step.thought or "", max_chars=MAX_THOUGHT_CHARS),
        action=_truncate(text=step.action or "", max_chars=MAX_THOUGHT_CHARS),
        observation=_truncate(text=step.observation or "", max_chars=MAX_OBSERVATION_CHARS),
    )


def parse_error_label(*, response: str) -> ErrorTaxonomyLabel:
    """Parse a judge response into an :class:`ErrorTaxonomyLabel`.

    Strategy:
        1. Strip whitespace and lowercase the response.
        2. If the cleaned string is exactly one of the seven valid label
           values, return that label.
        3. Otherwise, search for any valid label as a substring; if exactly
           one matches, return it.
        4. Otherwise, return
           :attr:`ErrorTaxonomyLabel.PRECONDITION_OR_EFFECT` (tie-break).
    """
    cleaned = response.strip().lower()
    if cleaned in _VALID_LABEL_VALUES:
        return ErrorTaxonomyLabel(cleaned)
    matches: list[str] = [label for label in _VALID_LABEL_VALUES if label in cleaned]
    if len(matches) == 1:
        return ErrorTaxonomyLabel(matches[0])
    return ErrorTaxonomyLabel(DEFAULT_TIE_BREAK_LABEL)


def classify_error(
    *,
    trajectory_step: TrajectoryStep,
    environment_state: dict[str, Any],
    judge_model: str = JUDGE_MODEL_DEFAULT,
    cost_tracker: CostTracker | None = None,
    judge: JudgeCallable | None = None,
    environment_id: str = "",
) -> ErrorTaxonomyLabel:
    """Classify one trajectory step into one of seven error-taxonomy labels.

    Either ``judge`` or a non-``None`` ``cost_tracker`` must be provided.
    When ``judge`` is ``None`` we construct one via ``make_judge_call``.

    The ``environment_id`` is used as part of the cache key so identical
    steps in different environments cache separately.
    """
    if judge is None:
        if cost_tracker is None:
            raise ValueError("classify_error requires either a judge callable or a cost_tracker")
        judge = make_judge_call(
            model=judge_model,
            cost_tracker=cost_tracker,
            system_prompt=ERROR_TAXONOMY_SYSTEM_PROMPT,
            note="error_taxonomy",
        )
    prompt = _build_error_prompt(step=trajectory_step, environment_state=environment_state)
    step_hash = hash_trajectory_step(
        turn_index=trajectory_step.turn_index,
        granularity=trajectory_step.granularity,
        thought=trajectory_step.thought,
        action=trajectory_step.action,
        observation=trajectory_step.observation,
    )
    key = make_cache_key(
        environment_id=environment_id,
        trajectory_hash=step_hash,
        prompt_key=ERROR_TAXONOMY_PROMPT_KEY,
        prompt_payload=prompt,
    )
    cached = cache_get(key=key)
    if cached is not None:
        return parse_error_label(response=cached)
    response = judge(prompt)
    cache_put(key=key, value=response)
    return parse_error_label(response=response)
