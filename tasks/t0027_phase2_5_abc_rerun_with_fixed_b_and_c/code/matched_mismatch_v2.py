"""Matched-mismatch v2: delegates to plan_and_solve_v3 instead of scope_aware_react (S-0026-02).

t0026's matched-mismatch wrapper (variant C) used ``delegate="scope_aware_react"`` from t0010,
which mechanically guaranteed that C inherited variant A's scaffold and merely added perturbed
granularity labels — not B's scaffold plus extra degradation. The paired McNemar B-vs-C
significance came from the scaffold difference, not the label perturbation, and so the RQ5
hypothesis was rejected for the wrong reason.

This v2 wrapper fixes the structural defect by running ``PlanAndSolveAgentV3`` (the fault-tolerant
fork in this same task) on the problem and then post-processing the resulting trajectory to attach
adversarially-perturbed granularity labels drawn from the v2 hierarchy annotation. The inner agent
is now Plan-and-Solve, the trajectory record shape is the v2 record shape (so RQ5 is comparable to
RQ1 on the same scaffolding), and the adversarial-perturbation logic is preserved verbatim from
t0010.

The library exports a single entry point used by the t0027 harness:

* :class:`MatchedMismatchV2Agent.run(problem=..., annotation=...)` — returns
  :class:`AgentRunResultV2`, which has a ``trajectory: list[TrajectoryRecordV2]`` field shaped
  exactly like :class:`PlanAndSolveAgentV3`'s output, plus the diagnostic counters from v3.

Adversarial-perturbation policy (verbatim from t0010):

* ``global → atomic``
* ``subtask → atomic``
* ``atomic → global``

Mapping rule from PnS-v3 trajectory records to perturbed labels:

* If the v2 hierarchy yields a phase walk of length ``P`` (one phase per "step the model should
  have done"), and the v3 trajectory has length ``T``, then for each record at index ``i`` we
  consult ``phases[min(i, P-1)].correct_tag``, apply the adversarial map, and overwrite the
  record's ``granularity`` field. If ``P == 0`` (annotation has no parseable phases), every record
  is given the literal label ``"atomic"`` (a fixed adversarial default — ``"unspecified"`` does not
  exist in the granularity vocabulary).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Final, Literal

from tasks.t0010_matched_mismatch_library.code.matched_mismatch import (
    ADVERSARIAL_MAP,
    GRANULARITY_VALUES,
    Phase,
    iter_phases,
)
from tasks.t0021_plan_and_solve_v2_with_final_confidence.code.planandsolve_v2 import (
    TrajectoryRecordV2,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.planandsolve_v3 import (
    AgentResultV3,
    PlanAndSolveAgentV3,
)

# --------------------------------------------------------------------------------------------------
# Type aliases
# --------------------------------------------------------------------------------------------------


type ModelCall = Callable[[str], str]
type Tool = Callable[[str], str]
type ToolRegistry = dict[str, Tool]
type MismatchStrategy = Literal["adversarial"]


# --------------------------------------------------------------------------------------------------
# Public constants
# --------------------------------------------------------------------------------------------------


DELEGATE_PLAN_AND_SOLVE_V3: Final[str] = "scope_unaware_planandsolve_v3"
"""Single supported delegate id; used in the task harness for symmetry with t0010 logging."""


# Default adversarial label when the v2 annotation has no parseable phases. Chosen as ``"atomic"``
# because it is the most distant from the implicit ``"global"`` PnS plans tend to take.
_DEFAULT_ADVERSARIAL_TAG: Final[str] = "atomic"


# --------------------------------------------------------------------------------------------------
# Data classes
# --------------------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AgentRunResultV2:
    """Aggregate output of one :meth:`MatchedMismatchV2Agent.run` invocation.

    The trajectory shape is identical to :class:`PlanAndSolveAgentV3`'s output, with each
    ``TrajectoryRecordV2.granularity`` overwritten by an adversarially-perturbed label drawn from
    the per-instance v2 hierarchy. The ``phases`` field carries the un-perturbed v2 phase walk so
    downstream consumers can reconstruct each step's correct tag.
    """

    final_answer: str | None
    trajectory: list[TrajectoryRecordV2]
    plan: list[str]
    final_confidence: float | None
    final_confidence_parse_failures: int
    plan_parser_recovery_path: str
    plan_parser_attempts: int
    phases: list[Phase]
    delegate: str


# --------------------------------------------------------------------------------------------------
# Internal helpers
# --------------------------------------------------------------------------------------------------


def _adversarial_tag_for_correct(*, correct_tag: str) -> str:
    if correct_tag in ADVERSARIAL_MAP:
        return ADVERSARIAL_MAP[correct_tag]
    if correct_tag in GRANULARITY_VALUES:
        # Defensive: fall back to atomic for any future granularity that lacks a map entry.
        return _DEFAULT_ADVERSARIAL_TAG
    return _DEFAULT_ADVERSARIAL_TAG


def _perturb_trajectory(
    *,
    v3_trajectory: list[TrajectoryRecordV2],
    phases: list[Phase],
) -> list[TrajectoryRecordV2]:
    """Overwrite each record's ``granularity`` with an adversarial label drawn from ``phases``.

    For an empty phase walk every record is tagged with :data:`_DEFAULT_ADVERSARIAL_TAG`. For a
    non-empty walk the adversarial label for record ``i`` is computed from
    ``phases[min(i, len(phases) - 1)].correct_tag``.
    """
    if len(v3_trajectory) == 0:
        return []
    out: list[TrajectoryRecordV2] = []
    for i, record in enumerate(v3_trajectory):
        if len(phases) == 0:
            wrong_tag = _DEFAULT_ADVERSARIAL_TAG
        else:
            phase_index = min(i, len(phases) - 1)
            correct_tag = phases[phase_index].correct_tag
            wrong_tag = _adversarial_tag_for_correct(correct_tag=correct_tag)
        out.append(
            TrajectoryRecordV2(
                turn_index=record.turn_index,
                granularity=wrong_tag,
                thought=record.thought,
                action=record.action,
                observation=record.observation,
                confidence=record.confidence,
                final_confidence=record.final_confidence,
            )
        )
    return out


# --------------------------------------------------------------------------------------------------
# Agent
# --------------------------------------------------------------------------------------------------


@dataclass(slots=True)
class MatchedMismatchV2Agent:
    """Variant-C agent (matched-mismatch v2): runs ``PlanAndSolveAgentV3`` then perturbs labels.

    The ``mismatch_strategy`` is fixed at ``"adversarial"`` because the t0026 finding (S-0026-02)
    motivated specifically this perturbation policy. Random perturbation is intentionally not
    supported in v2 — the random strategy from t0010 stays available there for backward-compat.

    Args:
        model_call: callable taking a prompt and returning a model response.
        tool_registry: mapping of tool name to a callable returning an observation. Forwarded
            verbatim to the inner :class:`PlanAndSolveAgentV3`.
        max_steps: maximum number of plan steps to execute before forcibly halting. Forwarded to
            the inner agent. Defaults to ``32``.
        mismatch_strategy: pinned to ``"adversarial"``.
        seed: retained for API symmetry with :class:`MatchedMismatchAgent`; the adversarial map is
            deterministic so this seed is currently unused but kept for forward compatibility.
    """

    model_call: ModelCall
    tool_registry: ToolRegistry = field(default_factory=dict)
    max_steps: int = 32
    mismatch_strategy: MismatchStrategy = "adversarial"
    seed: int = 0

    def run(
        self,
        *,
        problem: str,
        annotation: Mapping[str, Any],
    ) -> AgentRunResultV2:
        if self.mismatch_strategy != "adversarial":
            raise ValueError(
                f"mismatch_strategy must be 'adversarial' in v2, got {self.mismatch_strategy!r}."
            )
        inner_agent = PlanAndSolveAgentV3(
            model_call=self.model_call,
            tool_registry=self.tool_registry,
            max_steps=self.max_steps,
        )
        v3_result: AgentResultV3 = inner_agent.run(problem=problem)
        phases: list[Phase] = list(iter_phases(annotation))
        perturbed_trajectory = _perturb_trajectory(
            v3_trajectory=v3_result.trajectory,
            phases=phases,
        )
        return AgentRunResultV2(
            final_answer=v3_result.final_answer,
            trajectory=perturbed_trajectory,
            plan=v3_result.plan,
            final_confidence=v3_result.final_confidence,
            final_confidence_parse_failures=v3_result.final_confidence_parse_failures,
            plan_parser_recovery_path=v3_result.plan_parser_recovery_path,
            plan_parser_attempts=v3_result.plan_parser_attempts,
            phases=phases,
            delegate=DELEGATE_PLAN_AND_SOLVE_V3,
        )


# --------------------------------------------------------------------------------------------------
# Re-exports
# --------------------------------------------------------------------------------------------------


__all__ = [
    "DELEGATE_PLAN_AND_SOLVE_V3",
    "AgentRunResultV2",
    "MatchedMismatchV2Agent",
]
