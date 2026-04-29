from __future__ import annotations

from pathlib import Path

from src.models.base import LLMClient
from src.storage.schema import (
    BenchmarkTask,
    PlanRecord,
    ProbeRecord,
    RevisionRecord,
)

from .planner import _parse_steps

_REVISION_PROMPT_PATH = Path(__file__).parents[2] / "config" / "prompts" / "plan_revision.txt"


def _load_revision_prompt() -> str:
    return _REVISION_PROMPT_PATH.read_text()


class Revisor:
    """Ask the model to revise its plan when it detects a gap."""

    def __init__(self, client: LLMClient):
        self._client = client
        self._template = _load_revision_prompt()

    def revise(
        self,
        task: BenchmarkTask,
        plan: PlanRecord,
        probe: ProbeRecord,
        model_id: str,
    ) -> RevisionRecord | None:
        if not probe.gap_detected:
            return None

        missing_str = (
            "\n".join(f"- {item}" for item in probe.missing_information) or "- (unspecified gaps)"
        )
        prompt = self._template.format(missing_information=missing_str)

        # Re-use the probe conversation + add the revision request
        from .prober import _format_plan

        messages = [
            {"role": "user", "content": f"Please solve the following problem:\n\n{task.problem}"},
            {"role": "assistant", "content": f"Here is my plan:\n\n{_format_plan(plan.steps)}"},
        ]
        for result in probe.simulated_results:
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
        messages.append(
            {"role": "user", "content": probe.raw_probe_response}
        )  # model's gap analysis
        messages.append({"role": "user", "content": prompt})

        raw, usage = self._client.complete(messages, max_tokens=1024)
        steps, success = _parse_steps(raw)

        return RevisionRecord(
            probe_id=probe.probe_id,
            plan_id=plan.plan_id,
            task_id=task.task_id,
            model_id=model_id,
            triggered_by="gap_detected",
            original_steps=plan.steps,
            revised_steps=steps,
            raw_response=raw,
            parse_success=success,
            token_usage=usage,
        )
