from __future__ import annotations

import json
import re

from src.models.base import LLMClient
from src.storage.schema import BenchmarkTask, PlanRecord

_RUBRIC_PROMPT = """
You are evaluating the quality of a step-by-step plan for solving a scientific problem.

Rate the plan on 3 criteria, each 0 or 1:
1. completeness: if all steps were executed in order, would they yield the final answer? (0=no, 1=yes)
2. necessity: are all steps necessary, with no redundant/duplicate steps? (0=no, 1=yes)
3. granularity: does each step do exactly one logical thing (not two independent things bundled together)? (0=no, 1=yes)

Output ONLY valid JSON:
{{"completeness": 0_or_1, "necessity": 0_or_1, "granularity": 0_or_1, "reasoning": "brief justification"}}

Problem:
{problem}

Plan:
{plan}
"""


def _normalize_answer(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", "", s)
    # Remove units (simple heuristic)
    s = re.sub(r"[a-zA-Z]+$", "", s)
    return s


def _answers_match(predicted: str, ground_truth: str, tol: float = 0.01) -> bool:
    if _normalize_answer(predicted) == _normalize_answer(ground_truth):
        return True
    # Try numerical comparison
    try:
        p = float(re.sub(r"[^\d.eE+\-]", "", predicted))
        g = float(re.sub(r"[^\d.eE+\-]", "", ground_truth))
        if g != 0:
            return abs(p - g) / abs(g) <= tol
        return abs(p - g) <= tol
    except (ValueError, ZeroDivisionError):
        return False


class Grader:
    def __init__(self, judge_client: LLMClient):
        self._judge = judge_client

    def grade_plan(self, task: BenchmarkTask, plan: PlanRecord) -> dict:
        """Score plan quality 0-1 via rubric."""
        from .prober import _format_plan

        prompt = _RUBRIC_PROMPT.format(
            problem=task.problem,
            plan=_format_plan(plan.steps),
        )
        raw, usage = self._judge.complete([{"role": "user", "content": prompt}], max_tokens=256)

        scores = {"completeness": 0, "necessity": 0, "granularity": 0}
        try:
            match = re.search(r"\{.*?\}", raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                for k in scores:
                    scores[k] = int(bool(data.get(k, 0)))
        except Exception:
            pass

        total = sum(scores.values()) / 3.0
        return {"scores": scores, "quality": total, "raw": raw, "token_usage": usage}

    def grade_answer(self, predicted: str, task: BenchmarkTask) -> bool:
        """Check if predicted answer matches ground truth."""
        return _answers_match(predicted, task.ground_truth)
