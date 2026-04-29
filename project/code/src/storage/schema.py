from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


def _now() -> datetime:
    return datetime.now(UTC)


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


@dataclass
class BenchmarkTask:
    task_id: str
    source: str  # "frontierscience_olympiad"
    subject: str  # "physics" | "chemistry" | "biology"
    problem: str
    ground_truth: str  # expected short answer
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------


@dataclass
class PlanStep:
    number: int
    action: str
    needs: list[str]
    produces: list[str]


@dataclass
class PlanRecord:
    plan_id: str = field(default_factory=_uid)
    task_id: str = ""
    model_id: str = ""
    raw_response: str = ""
    steps: list[PlanStep] = field(default_factory=list)
    parse_success: bool = True
    created_at: datetime = field(default_factory=_now)
    token_usage: dict[str, int] = field(default_factory=dict)

    @property
    def num_steps(self) -> int:
        return len(self.steps)


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------


class SimulationMode(str, Enum):
    HONEST = "honest"
    MISLEADING = "misleading"


@dataclass
class SimulatedStepResult:
    step_number: int
    mode: SimulationMode
    result_text: str
    deliberately_omitted: list[str] = field(default_factory=list)
    token_usage: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Probe
# ---------------------------------------------------------------------------


@dataclass
class ProbeRecord:
    probe_id: str = field(default_factory=_uid)
    plan_id: str = ""
    task_id: str = ""
    model_id: str = ""
    probed_step: int = 0
    simulation_mode: SimulationMode = SimulationMode.HONEST
    simulated_results: list[SimulatedStepResult] = field(default_factory=list)
    context_mode: str = "full"  # "full" | "stripped"
    raw_probe_response: str = ""
    parse_success: bool = True
    # Parsed probe fields
    sufficient: bool | None = None
    confidence: str = ""  # "high" | "medium" | "low"
    missing_information: list[str] = field(default_factory=list)
    reasoning: str = ""
    created_at: datetime = field(default_factory=_now)
    token_usage: dict[str, int] = field(default_factory=dict)

    @property
    def gap_detected(self) -> bool:
        return self.sufficient is False


# ---------------------------------------------------------------------------
# Revision
# ---------------------------------------------------------------------------


@dataclass
class RevisionRecord:
    revision_id: str = field(default_factory=_uid)
    probe_id: str = ""
    plan_id: str = ""
    task_id: str = ""
    model_id: str = ""
    triggered_by: str = ""  # "gap_detected" | "none"
    original_steps: list[PlanStep] = field(default_factory=list)
    revised_steps: list[PlanStep] = field(default_factory=list)
    raw_response: str = ""
    parse_success: bool = True
    created_at: datetime = field(default_factory=_now)
    token_usage: dict[str, int] = field(default_factory=dict)

    @property
    def num_steps_changed(self) -> int:
        orig = {s.number: s.action for s in self.original_steps}
        rev = {s.number: s.action for s in self.revised_steps}
        changed = sum(1 for k, v in rev.items() if orig.get(k) != v)
        added = len(set(rev) - set(orig))
        removed = len(set(orig) - set(rev))
        return changed + added + removed


# ---------------------------------------------------------------------------
# Experiment run (top-level record)
# ---------------------------------------------------------------------------


@dataclass
class ExperimentRun:
    run_id: str = field(default_factory=_uid)
    experiment_name: str = ""
    task: BenchmarkTask | None = None
    plan: PlanRecord | None = None
    probes: list[ProbeRecord] = field(default_factory=list)
    revisions: list[RevisionRecord] = field(default_factory=list)
    created_at: datetime = field(default_factory=_now)
