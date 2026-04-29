from __future__ import annotations

import json
import re
from pathlib import Path

from src.models.base import LLMClient
from src.storage.schema import (
    BenchmarkTask,
    PlanRecord,
    PlanStep,
    ProbeRecord,
    SimulatedStepResult,
    SimulationMode,
)

_PROBE_PROMPT_PATH = Path(__file__).parents[2] / "config" / "prompts" / "gap_probe.txt"

_STRIPPED_SYSTEM = (
    "You are reviewing the execution log of a multi-step scientific plan. "
    "You do NOT have access to the original problem specification. "
    "Base your assessment ONLY on the plan steps and the step results shown in the conversation. "
    "Do not re-derive values from memory or scientific knowledge."
)

# Exp 1: instruction suppression — problem stays visible, but explicit constraint added
_INHIBIT_SOFT_SUFFIX = (
    "\n\nIMPORTANT: Base your assessment ONLY on the step results provided above. "
    "Do not use values from the problem statement to fill in gaps."
)
_INHIBIT_HARD_SYSTEM = (
    "The original problem is shown for structural context only. "
    "You MUST NOT use specific values, formulas, or quantities from the problem statement "
    "to infer missing step outputs. If a value was not explicitly delivered in a completed "
    "step result, treat it as unknown — even if you could compute it from the problem."
)


def _load_probe_prompt() -> str:
    return _PROBE_PROMPT_PATH.read_text()


def _format_plan(steps: list[PlanStep]) -> str:
    lines = []
    for s in steps:
        lines.append(f"Step {s.number}: {s.action}")
        if s.needs:
            lines.append(f"  Needs: {', '.join(s.needs)}")
        if s.produces:
            lines.append(f"  Produces: {', '.join(s.produces)}")
    return "\n".join(lines)


def _parse_probe_response(raw: str) -> tuple[bool, dict]:
    """Parse JSON probe response. Returns (parse_success, fields_dict)."""
    fields = {"sufficient": None, "confidence": "", "missing_information": [], "reasoning": ""}

    # Strip markdown fences
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("`").strip()

    # Try direct parse
    try:
        data = json.loads(cleaned)
        fields["sufficient"] = bool(data.get("sufficient"))
        fields["confidence"] = str(data.get("confidence", ""))
        fields["missing_information"] = list(data.get("missing_information", []))
        fields["reasoning"] = str(data.get("reasoning", ""))
        return True, fields
    except json.JSONDecodeError:
        pass

    # Try extracting first JSON object
    match = re.search(r'\{.*?"sufficient".*?\}', cleaned, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            fields["sufficient"] = bool(data.get("sufficient"))
            fields["confidence"] = str(data.get("confidence", ""))
            fields["missing_information"] = list(data.get("missing_information", []))
            fields["reasoning"] = str(data.get("reasoning", ""))
            return True, fields
        except json.JSONDecodeError:
            pass

    # Boolean regex fallback
    if re.search(r'"sufficient"\s*:\s*true', cleaned, re.IGNORECASE):
        fields["sufficient"] = True
        return False, fields
    if re.search(r'"sufficient"\s*:\s*false', cleaned, re.IGNORECASE):
        fields["sufficient"] = False
        return False, fields

    return False, fields


class Prober:
    """Probe the model for information sufficiency after simulated step execution."""

    def __init__(self, client: LLMClient):
        self._client = client
        self._probe_template = _load_probe_prompt()

    def probe(
        self,
        task: BenchmarkTask,
        plan: PlanRecord,
        simulated_results: list[SimulatedStepResult],
        probe_step: int,
        model_id: str,
        context_mode: str = "full",  # "full"|"stripped"|"inhibit_soft"|"inhibit_hard"|"swapped"
        swap_task: BenchmarkTask | None = None,
    ) -> ProbeRecord:
        probe_step_obj = next((s for s in plan.steps if s.number == probe_step), None)
        if probe_step_obj is None:
            raise ValueError(f"Step {probe_step} not found in plan {plan.plan_id}")

        # Determine which problem text to show (for "swapped" mode)
        context_task = swap_task if (context_mode == "swapped" and swap_task) else task
        include_problem = context_mode != "stripped"
        system = {
            "stripped": _STRIPPED_SYSTEM,
            "inhibit_hard": _INHIBIT_HARD_SYSTEM,
        }.get(context_mode)
        inhibit_soft = context_mode == "inhibit_soft"

        messages = self._build_conversation(
            context_task,
            plan,
            simulated_results,
            probe_step_obj,
            include_problem,
            inhibit_soft=inhibit_soft,
        )
        raw, usage = self._client.complete(messages, system=system, max_tokens=1024)

        parse_ok, fields = _parse_probe_response(raw)
        mode = simulated_results[0].mode if simulated_results else SimulationMode.HONEST

        return ProbeRecord(
            plan_id=plan.plan_id,
            task_id=task.task_id,
            model_id=model_id,
            probed_step=probe_step,
            simulation_mode=mode,
            context_mode=context_mode,
            simulated_results=simulated_results,
            raw_probe_response=raw,
            parse_success=parse_ok,
            sufficient=fields["sufficient"],
            confidence=fields["confidence"],
            missing_information=fields["missing_information"],
            reasoning=fields["reasoning"],
            token_usage=usage,
        )

    def _build_conversation(
        self,
        task: BenchmarkTask,
        plan: PlanRecord,
        simulated_results: list[SimulatedStepResult],
        probe_step: PlanStep,
        include_problem: bool,
        inhibit_soft: bool = False,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []

        if include_problem:
            messages.append(
                {
                    "role": "user",
                    "content": f"Please solve the following problem:\n\n{task.problem}",
                }
            )
            messages.append(
                {"role": "assistant", "content": f"Here is my plan:\n\n{_format_plan(plan.steps)}"}
            )
        else:
            # Stripped: no problem statement — only the plan structure
            messages.append(
                {
                    "role": "user",
                    "content": "You have been working on a multi-step scientific problem. Here is the plan you are following:",
                }
            )
            messages.append({"role": "assistant", "content": _format_plan(plan.steps)})

        for result in simulated_results:
            messages.append(
                {
                    "role": "user",
                    "content": f"Step {result.step_number} has been completed. Result:\n{result.result_text}",
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": f"Understood. Step {result.step_number} result recorded.",
                }
            )

        probe_prompt = self._probe_template.format(
            probe_step=probe_step.number,
            probe_step_action=probe_step.action,
            probe_step_needs=", ".join(probe_step.needs) or "none",
            probe_step_produces=", ".join(probe_step.produces) or "a result",
        )
        if inhibit_soft:
            probe_prompt += _INHIBIT_SOFT_SUFFIX
        messages.append({"role": "user", "content": probe_prompt})
        return messages
