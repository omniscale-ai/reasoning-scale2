from __future__ import annotations

import re
from pathlib import Path

from src.models.base import LLMClient
from src.storage.schema import BenchmarkTask, PlanStep, SimulatedStepResult, SimulationMode

_PROMPTS_DIR = Path(__file__).parents[2] / "config" / "prompts"


def _load(name: str) -> str:
    return (_PROMPTS_DIR / name).read_text()


class Simulator:
    """Generate synthetic step results for honest or misleading simulation modes."""

    def __init__(self, client: LLMClient):
        self._client = client
        self._honest_tmpl = _load("step_simulation_honest.txt")
        self._misleading_tmpl = _load("step_simulation_misleading.txt")

    def simulate(
        self,
        task: BenchmarkTask,
        step: PlanStep,
        mode: SimulationMode,
    ) -> SimulatedStepResult:
        if mode == SimulationMode.HONEST:
            return self._honest(task, step)
        return self._misleading(task, step)

    def simulate_steps(
        self,
        task: BenchmarkTask,
        steps: list[PlanStep],
        mode: SimulationMode,
    ) -> list[SimulatedStepResult]:
        return [self.simulate(task, step, mode) for step in steps]

    # ------------------------------------------------------------------

    def _honest(self, task: BenchmarkTask, step: PlanStep) -> SimulatedStepResult:
        prompt = self._honest_tmpl.format(
            problem=task.problem,
            step_number=step.number,
            step_action=step.action,
            step_needs=", ".join(step.needs) or "none",
            step_produces=", ".join(step.produces) or "a result",
        )
        raw, usage = self._client.complete([{"role": "user", "content": prompt}], max_tokens=512)
        return SimulatedStepResult(
            step_number=step.number,
            mode=SimulationMode.HONEST,
            result_text=raw.strip(),
            deliberately_omitted=[],
            token_usage=usage,
        )

    def _misleading(self, task: BenchmarkTask, step: PlanStep) -> SimulatedStepResult:
        # The key items to omit are the things this step "produces" — i.e., what the next step needs
        omit_targets = step.produces if step.produces else [f"the result of step {step.number}"]

        prompt = self._misleading_tmpl.format(
            problem=task.problem,
            step_number=step.number,
            step_action=step.action,
            step_needs=", ".join(step.needs) or "none",
            step_produces=", ".join(step.produces) or "a result",
            omit_targets=", ".join(omit_targets),
        )
        raw, usage = self._client.complete([{"role": "user", "content": prompt}], max_tokens=512)

        result_text, omitted = _parse_misleading_response(raw, omit_targets)
        return SimulatedStepResult(
            step_number=step.number,
            mode=SimulationMode.MISLEADING,
            result_text=result_text,
            deliberately_omitted=omitted,
            token_usage=usage,
        )


def _parse_misleading_response(raw: str, fallback_omitted: list[str]) -> tuple[str, list[str]]:
    """Split LLM output into (result_text, omitted_list)."""
    omitted: list[str] = fallback_omitted

    # Look for OMITTED: ["..."] line
    match = re.search(r"OMITTED:\s*(\[.*?\])", raw, re.DOTALL)
    if match:
        try:
            import json

            omitted = json.loads(match.group(1))
        except Exception:
            pass
        result_text = raw[: match.start()].strip()
    else:
        result_text = raw.strip()

    return result_text, omitted
