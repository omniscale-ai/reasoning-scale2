"""Module constants for the metric2_calibration_aggregator_v1 library.

All magic numbers, magic strings, and reusable enumerations live here. The Xiong2024 protocol
parameters are exposed as overridable module-level constants so downstream tasks can audit and
sweep them without forking the library.
"""

from __future__ import annotations

from typing import Final

# --------------------------------------------------------------------------------------------------
# Library identity
# --------------------------------------------------------------------------------------------------

LIBRARY_NAME: Final[str] = "Metric 2 Calibration Aggregator"
"""Human-readable display name for the library asset."""


LIBRARY_VERSION: Final[str] = "0.1.0"
"""Library version string. Bump on any user-visible change."""


# --------------------------------------------------------------------------------------------------
# Verbalized confidence labels (Xiong2024 §3.2 human-inspired prompt)
# --------------------------------------------------------------------------------------------------

LABEL_LOW: Final[str] = "low"
"""Verbalized low-confidence label."""


LABEL_MEDIUM: Final[str] = "medium"
"""Verbalized medium-confidence label."""


LABEL_HIGH: Final[str] = "high"
"""Verbalized high-confidence label."""


VALID_CONFIDENCE_LABELS: Final[tuple[str, ...]] = (LABEL_LOW, LABEL_MEDIUM, LABEL_HIGH)
"""Ordered tuple of accepted verbalized confidence labels (lowercase canonical form)."""


# --------------------------------------------------------------------------------------------------
# Verbalized-to-numeric mapping (Xiong2024 §3.2)
# --------------------------------------------------------------------------------------------------

CONFIDENCE_LOW_VALUE: Final[float] = 0.25
"""Numeric value assigned to the verbalized 'low' label."""


CONFIDENCE_MEDIUM_VALUE: Final[float] = 0.5
"""Numeric value assigned to the verbalized 'medium' label."""


CONFIDENCE_HIGH_VALUE: Final[float] = 0.9
"""Numeric value assigned to the verbalized 'high' label."""


LABEL_TO_CONFIDENCE: Final[dict[str, float]] = {
    LABEL_LOW: CONFIDENCE_LOW_VALUE,
    LABEL_MEDIUM: CONFIDENCE_MEDIUM_VALUE,
    LABEL_HIGH: CONFIDENCE_HIGH_VALUE,
}
"""Canonical mapping from verbalized label to numeric confidence per Xiong2024."""


# --------------------------------------------------------------------------------------------------
# Aggregation parameters
# --------------------------------------------------------------------------------------------------

SELF_CONSISTENCY_SAMPLES: Final[int] = 3
"""Default number of self-consistency samples per problem."""


HIGH_CONFIDENCE_THRESHOLD: Final[float] = 0.75
"""Default high-confidence cutoff for overconfident-error scoring (Xiong2024 high-bucket boundary).

Sits strictly between MEDIUM (0.5) and HIGH (0.9) so that only fully-high samples qualify.
Override at call time if a future task wants to sweep it.
"""


# --------------------------------------------------------------------------------------------------
# Trajectory record schema (mirrors t0007's TRAJECTORY_RECORD_FIELDS)
# --------------------------------------------------------------------------------------------------

TRAJECTORY_FIELD_TURN_INDEX: Final[str] = "turn_index"
TRAJECTORY_FIELD_GRANULARITY: Final[str] = "granularity"
TRAJECTORY_FIELD_THOUGHT: Final[str] = "thought"
TRAJECTORY_FIELD_ACTION: Final[str] = "action"
TRAJECTORY_FIELD_OBSERVATION: Final[str] = "observation"
TRAJECTORY_FIELD_CONFIDENCE: Final[str] = "confidence"


TRAJECTORY_RECORD_FIELDS: Final[tuple[str, ...]] = (
    TRAJECTORY_FIELD_TURN_INDEX,
    TRAJECTORY_FIELD_GRANULARITY,
    TRAJECTORY_FIELD_THOUGHT,
    TRAJECTORY_FIELD_ACTION,
    TRAJECTORY_FIELD_OBSERVATION,
    TRAJECTORY_FIELD_CONFIDENCE,
)
"""Canonical ordered tuple of trajectory record field names.

Mirrors ``planandsolve.TRAJECTORY_RECORD_FIELDS`` from
``tasks.t0007_scope_unaware_planandsolve_library.code`` so trajectory records produced by
t0006/t0007/t0010 can be consumed by this library without modification. The library never
imports t0007 directly to avoid a cross-task code dependency (see CLAUDE.md rule on cross-task
imports).
"""


# --------------------------------------------------------------------------------------------------
# Prompt template (Xiong2024 §3.2 human-inspired prompt)
# --------------------------------------------------------------------------------------------------

DEFAULT_PROMPT_TEMPLATE: Final[str] = (
    "You are evaluating your own confidence in a proposed action.\n"
    "\n"
    "Problem:\n"
    "{problem}\n"
    "\n"
    "Proposed action:\n"
    "{action}\n"
    "\n"
    "On a scale of low / medium / high, how confident are you that this action is correct?\n"
    "Respond with exactly one line of the form `Confidence: <low|medium|high>` followed by\n"
    "one sentence of justification on a new line.\n"
)
"""Default human-inspired confidence-elicitation prompt (Xiong2024 §3.2).

The template uses ``str.format`` with two named placeholders: ``{problem}`` and ``{action}``.
"""


PROMPT_PROBLEM_PLACEHOLDER: Final[str] = "{problem}"
"""Placeholder that must appear exactly once in any custom prompt template."""


PROMPT_ACTION_PLACEHOLDER: Final[str] = "{action}"
"""Placeholder that must appear exactly once in any custom prompt template."""


CONFIDENCE_PREFIX: Final[str] = "confidence:"
"""Lowercase prefix the parser uses to locate the labeled confidence line."""
