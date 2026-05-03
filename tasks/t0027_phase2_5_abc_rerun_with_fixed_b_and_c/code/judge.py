"""Sonnet/opus judge for variant outcomes; SWE-bench tests are NOT executed in this task.

Forked verbatim from t0026 with the import root rebased to t0027. Programmatic ground truth is
computed only for FrontierScience (substring exact-match against the ``Ground truth answer:``
segment in ``solution``). For SWE-bench, this task records the judge verdict as ``success_judge``
because actually running SWE-bench patches inside isolated environments is outside scope. For
Tau-bench, programmatic truth is also ``None`` since the per-task gold ``outputs`` field is a
free-form list and is left to the judge.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final

from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.anthropic_shim import (
    CostTracker,
    make_model_call,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.instance_loader import Instance
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.paths import (
    FORBIDDEN_HAIKU_MODEL_ID,
    JUDGE_MODEL_PRIMARY,
    SUBSET_FRONTSCI,
    SUBSET_SWEBENCH,
    SUBSET_TAUBENCH,
)


@dataclass(frozen=True, slots=True)
class JudgeResult:
    success: bool
    rationale: str
    raw_response: str


@dataclass(frozen=True, slots=True)
class Prediction:
    instance_id: str
    subset: str
    variant: str
    final_answer: str | None
    final_confidence: float | None
    cost_usd: float
    trajectory_path: str | None


SUBSTANTIVE_JUDGE_PROMPT_TEMPLATE: Final[str] = (
    "You are a strict but fair judge for an AI agent's solution to a benchmark problem. You have "
    "the original problem, optional gold-truth information, and the agent's final answer. Decide "
    "whether the agent's final answer SUCCEEDED at the task.\n\n"
    "Use these rules:\n"
    "* If the agent's final answer is empty, missing, or visibly incoherent, the verdict is FAIL.\n"
    "* If gold information is provided, the agent must demonstrably address the gold task. For "
    "code-fix problems, an answer that explains the correct change in concrete code-pointing terms "
    "passes; an answer that only describes the problem fails.\n"
    "* For exact-answer science problems, the agent's final numeric or symbolic answer must match "
    "the gold answer up to obvious formatting differences.\n"
    "* When in doubt, choose FAIL.\n\n"
    "BENCHMARK SUBSET: {subset}\n"
    "INSTANCE ID: {instance_id}\n\n"
    "PROBLEM:\n{problem_text}\n\n"
    "GOLD INFORMATION (may be partial):\n{gold_summary}\n\n"
    "AGENT'S FINAL ANSWER:\n{final_answer}\n\n"
    "Output exactly two lines:\n"
    "  RATIONALE: <one short sentence explaining your decision>\n"
    "  VERDICT: PASS\n"
    "or\n"
    "  RATIONALE: <one short sentence explaining your decision>\n"
    "  VERDICT: FAIL\n"
)

MODEL_ROTATED_JUDGE_PROMPT_TEMPLATE: Final[str] = (
    "You are an impartial judge. The agent was given a customer-service style task and produced a "
    "final answer summarizing what it did. There is no fully programmatic ground truth available. "
    "Rate whether the agent's final answer plausibly satisfied the task as stated.\n\n"
    "Use these rules:\n"
    "* The verdict is PASS only if the agent's final answer addresses the user's request and "
    "names a concrete outcome (a value, a confirmation, an action taken).\n"
    "* If the agent answered in vague terms, deferred to a human, or gave up, the verdict is "
    "FAIL.\n"
    "* If the agent produced nothing, the verdict is FAIL.\n\n"
    "BENCHMARK SUBSET: {subset}\n"
    "INSTANCE ID: {instance_id}\n\n"
    "USER TASK:\n{problem_text}\n\n"
    "EXPECTED OUTPUT (may be partial or absent):\n{gold_summary}\n\n"
    "AGENT'S FINAL ANSWER:\n{final_answer}\n\n"
    "Output exactly two lines:\n"
    "  RATIONALE: <one short sentence explaining your decision>\n"
    "  VERDICT: PASS\n"
    "or\n"
    "  RATIONALE: <one short sentence explaining your decision>\n"
    "  VERDICT: FAIL\n"
)

_VERDICT_RE: Final[re.Pattern[str]] = re.compile(
    r"VERDICT\s*[:\-]\s*(PASS|FAIL|YES|NO|TRUE|FALSE)", re.IGNORECASE
)
_RATIONALE_RE: Final[re.Pattern[str]] = re.compile(
    r"RATIONALE\s*[:\-]\s*(.+?)(?:\n|$)", re.IGNORECASE | re.DOTALL
)
_PASS_VALUES: Final[frozenset[str]] = frozenset({"pass", "yes", "true"})
_FAIL_VALUES: Final[frozenset[str]] = frozenset({"fail", "no", "false"})


def _summarize_gold(*, instance: Instance, max_chars: int = 1200) -> str:
    if instance.gold is None:
        return "(no gold information available)"
    pieces: list[str] = []
    if instance.subset == SUBSET_SWEBENCH:
        repo = instance.gold.get("repo")
        difficulty = instance.gold.get("difficulty")
        f2p = instance.gold.get("FAIL_TO_PASS")
        p2p = instance.gold.get("PASS_TO_PASS")
        if repo is not None:
            pieces.append(f"repo={repo}")
        if difficulty is not None:
            pieces.append(f"difficulty={difficulty}")
        if f2p is not None:
            pieces.append(f"FAIL_TO_PASS={str(f2p)[:300]}")
        if p2p is not None:
            pieces.append(f"PASS_TO_PASS={str(p2p)[:300]}")
    elif instance.subset == SUBSET_FRONTSCI:
        sol = instance.gold.get("solution")
        if isinstance(sol, str):
            pieces.append(f"solution={sol[:max_chars]}")
    elif instance.subset == SUBSET_TAUBENCH:
        outputs = instance.gold.get("outputs")
        if outputs is not None:
            pieces.append(f"expected_outputs={str(outputs)[:600]}")
    summary = "\n".join(pieces) if len(pieces) > 0 else "(no gold information available)"
    if len(summary) > max_chars:
        summary = summary[:max_chars] + "...(truncated)"
    return summary


def _select_template(*, subset: str) -> str:
    if subset == SUBSET_TAUBENCH:
        return MODEL_ROTATED_JUDGE_PROMPT_TEMPLATE
    return SUBSTANTIVE_JUDGE_PROMPT_TEMPLATE


def _parse_verdict(*, raw_response: str) -> tuple[bool | None, str]:
    match = _VERDICT_RE.search(raw_response)
    rationale_match = _RATIONALE_RE.search(raw_response)
    rationale = rationale_match.group(1).strip()[:500] if rationale_match else ""
    if match is None:
        return None, rationale
    token = match.group(1).strip().lower()
    if token in _PASS_VALUES:
        return True, rationale
    if token in _FAIL_VALUES:
        return False, rationale
    return None, rationale


def judge_outcome(
    *,
    instance: Instance,
    prediction: Prediction,
    cost_tracker: CostTracker,
    model_id: str = JUDGE_MODEL_PRIMARY,
) -> JudgeResult:
    assert model_id != FORBIDDEN_HAIKU_MODEL_ID, (
        f"haiku model {FORBIDDEN_HAIKU_MODEL_ID!r} is forbidden as judge"
    )
    template = _select_template(subset=instance.subset)
    final_answer = prediction.final_answer if prediction.final_answer is not None else "(none)"
    prompt = template.format(
        subset=instance.subset,
        instance_id=instance.instance_id,
        problem_text=instance.problem_text[:6000],
        gold_summary=_summarize_gold(instance=instance),
        final_answer=final_answer[:4000],
    )
    judge_call = make_model_call(
        model_id=model_id,
        cost_tracker=cost_tracker,
        max_tokens=512,
    )
    raw_response = judge_call(prompt)
    verdict, rationale = _parse_verdict(raw_response=raw_response)
    if verdict is None:
        cost_tracker.note_parse_failure()
        return JudgeResult(success=False, rationale=rationale, raw_response=raw_response)
    return JudgeResult(success=verdict, rationale=rationale, raw_response=raw_response)


def _normalize(*, text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def compute_program_truth(*, instance: Instance, prediction: Prediction) -> bool | None:
    if instance.subset == SUBSET_FRONTSCI:
        if prediction.final_answer is None or instance.gold is None:
            return False
        sol = instance.gold.get("solution")
        if not isinstance(sol, str):
            return None
        marker = "ground truth answer:"
        idx = sol.lower().find(marker)
        if idx < 0:
            return None
        gold_segment = sol[idx + len(marker) :]
        gold_first_line = gold_segment.split("\n", 1)[0]
        normalized_gold = _normalize(text=gold_first_line)
        if len(normalized_gold) == 0:
            return None
        normalized_pred = _normalize(text=prediction.final_answer)
        first_meaningful_token: str = ""
        for token in normalized_gold.split():
            if any(c.isdigit() or c.isalpha() for c in token):
                first_meaningful_token = token
                break
        if len(first_meaningful_token) > 0 and first_meaningful_token in normalized_pred:
            return True
        return normalized_gold[: min(80, len(normalized_gold))] in normalized_pred
    if instance.subset == SUBSET_SWEBENCH:
        return None
    return None


def prediction_to_dict(prediction: Prediction) -> dict[str, Any]:
    return {
        "instance_id": prediction.instance_id,
        "subset": prediction.subset,
        "variant": prediction.variant,
        "final_answer": prediction.final_answer,
        "final_confidence": prediction.final_confidence,
        "cost_usd": prediction.cost_usd,
        "trajectory_path": prediction.trajectory_path,
    }
