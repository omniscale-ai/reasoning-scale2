"""Named constants for the scope-aware ReAct library.

All magic strings used by the agent's prompt template, output parser, and trajectory writer live
here so that downstream tasks (and the sister Plan-and-Solve library t0007) can refer to the same
canonical values.
"""

from __future__ import annotations

from typing import Final

# ---- Granularity literals -------------------------------------------------

GRANULARITY_GLOBAL: Final[str] = "global"
GRANULARITY_SUBTASK: Final[str] = "subtask"
GRANULARITY_ATOMIC: Final[str] = "atomic"

GRANULARITY_VALUES: Final[tuple[str, str, str]] = (
    GRANULARITY_GLOBAL,
    GRANULARITY_SUBTASK,
    GRANULARITY_ATOMIC,
)

DEFAULT_GRANULARITY_ON_MISSING_TAG: Final[str] = GRANULARITY_ATOMIC

# ---- Trajectory schema field names ----------------------------------------

FIELD_TURN_INDEX: Final[str] = "turn_index"
FIELD_GRANULARITY: Final[str] = "granularity"
FIELD_THOUGHT: Final[str] = "thought"
FIELD_ACTION: Final[str] = "action"
FIELD_OBSERVATION: Final[str] = "observation"
FIELD_CONFIDENCE: Final[str] = "confidence"

TRAJECTORY_FIELDS: Final[tuple[str, str, str, str, str, str]] = (
    FIELD_TURN_INDEX,
    FIELD_GRANULARITY,
    FIELD_THOUGHT,
    FIELD_ACTION,
    FIELD_OBSERVATION,
    FIELD_CONFIDENCE,
)

# ---- Action schema field names --------------------------------------------

ACTION_NAME_FIELD: Final[str] = "name"
ACTION_ARGS_FIELD: Final[str] = "args"
FINISH_ACTION_NAME: Final[str] = "Finish"
FINISH_ANSWER_KEY: Final[str] = "answer"

# ---- Parser sentinels -----------------------------------------------------

THOUGHT_PREFIX: Final[str] = "Thought:"
ACTION_PREFIX: Final[str] = "Action:"
CONFIDENCE_PREFIX: Final[str] = "Confidence:"

GRANULARITY_TAG_OPEN: Final[str] = "<"
GRANULARITY_TAG_CLOSE: Final[str] = ">"

# ---- Observation sentinels for error paths --------------------------------

OBSERVATION_PARSE_ERROR: Final[str] = "<parse_error>"
OBSERVATION_UNKNOWN_TOOL: Final[str] = "<unknown_tool>"
OBSERVATION_TAG_MISSING_WARNING: Final[str] = "<tag_missing_defaulted_to_atomic>"

# ---- Safety / runtime caps -----------------------------------------------

DEFAULT_MAX_TURNS: Final[int] = 20

# ---- LangChain ReAct attribution ------------------------------------------
#
# This library reuses the canonical ReAct exemplar pattern published in the LangChain project
# (Apache License 2.0). The verbatim attribution string below is included in the system prompt
# and in description.md so downstream consumers can satisfy the Apache-2.0 NOTICE requirement.

LANGCHAIN_REACT_ATTRIBUTION: Final[str] = (
    "Prompt template adapted from the LangChain project (Apache License 2.0). "
    "See https://github.com/langchain-ai/langchain for the upstream source."
)
