from __future__ import annotations

import json
import re
from pathlib import Path

from src.models.base import LLMClient
from src.storage.schema import BenchmarkTask, PlanRecord, PlanStep

_PROMPT_PATH = Path(__file__).parents[2] / "config" / "prompts" / "plan_generation.txt"


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text()


def _parse_steps(raw: str) -> tuple[list[PlanStep], bool]:
    """Parse JSON plan from LLM response. Returns (steps, success)."""
    # Strip markdown code fences
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip()
    cleaned = re.sub(r"```\s*$", "", cleaned).strip()

    # Try direct JSON parse
    try:
        data = json.loads(cleaned)
        steps = _steps_from_data(data)
        if steps:
            return steps, True
    except json.JSONDecodeError:
        pass

    # Try extracting first JSON object containing "steps"
    match = re.search(r'\{[^{}]*"steps"\s*:\s*\[.*?\]\s*\}', cleaned, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            steps = _steps_from_data(data)
            if steps:
                return steps, True
        except json.JSONDecodeError:
            pass

    # Broader JSON extraction
    match = re.search(r'\{.*"steps".*\}', cleaned, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            steps = _steps_from_data(data)
            if steps:
                return steps, True
        except json.JSONDecodeError:
            pass

    # Regex fallback: extract numbered steps from prose (exclude LaTeX line numbers)
    steps = _regex_fallback(cleaned)
    return steps, len(steps) > 0


def _steps_from_data(data: dict) -> list[PlanStep]:
    steps = []
    for item in data.get("steps", []):
        steps.append(
            PlanStep(
                number=int(item.get("number", len(steps) + 1)),
                action=str(item.get("action", "")),
                needs=list(item.get("needs", [])),
                produces=list(item.get("produces", [])),
            )
        )
    return steps


def _regex_fallback(text: str) -> list[PlanStep]:
    """Extract numbered steps from free-form text, ignoring LaTeX-looking fragments."""
    steps = []
    pattern = re.compile(r"(?:^|\n)\s*(?:Step\s+)?(\d+)[.):\-]\s*([^\n]{10,})", re.IGNORECASE)
    for m in pattern.finditer(text):
        number = int(m.group(1))
        action = m.group(2).strip()
        # Skip if looks like LaTeX (contains \, $$, _{, ^{)
        if re.search(r"[\\$]|_\{|\^\{|\\frac|\\sum", action):
            continue
        if number > 10:
            continue
        steps.append(PlanStep(number=number, action=action, needs=[], produces=[]))
    # Deduplicate by number, keep first
    seen = set()
    unique = []
    for s in steps:
        if s.number not in seen:
            seen.add(s.number)
            unique.append(s)
    return unique


class Planner:
    def __init__(self, client: LLMClient, min_steps: int = 2, max_steps: int = 6):
        self._client = client
        self._min_steps = min_steps
        self._max_steps = max_steps
        self._prompt_template = _load_prompt()

    def generate(self, task: BenchmarkTask, model_id: str) -> PlanRecord:
        prompt = self._prompt_template.format(problem=task.problem)
        messages = [{"role": "user", "content": prompt}]

        raw, usage = self._client.complete(messages, max_tokens=1024)
        steps, success = _parse_steps(raw)

        # Filter degenerate plans
        if len(steps) < self._min_steps:
            success = False
        if len(steps) > self._max_steps:
            steps = steps[: self._max_steps]

        return PlanRecord(
            task_id=task.task_id,
            model_id=model_id,
            raw_response=raw,
            steps=steps,
            parse_success=success,
            token_usage=usage,
        )
