"""Verdict-parsing helpers for t0019.

Adapted (copy + extension) from `tasks/t0014_v2_annotator_sonnet_rerun/code/v2_judge.py`. The
substantive critic prompt may emit an optional `sub_scores` object; the parser captures it when
present but does not require it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from tasks.t0019_v2_judge_calibration_sonnet.code.constants import (
    VERDICT_ACCEPTABLE,
    VERDICT_NEEDS_REVISION,
)


@dataclass(frozen=True, slots=True)
class ParsedVerdict:
    verdict: str | None
    justification: str | None
    sub_scores: dict[str, int] | None
    parse_status: str  # "ok" or "parse-failure: <detail>"


def _strip_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1 :].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    return cleaned


def _extract_first_json_object(text: str) -> str | None:
    cleaned = _strip_fences(text)
    start = cleaned.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(cleaned)):
        ch = cleaned[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return cleaned[start : i + 1]
    return None


def _coerce_sub_scores(obj: object) -> dict[str, int] | None:
    if not isinstance(obj, dict):
        return None
    out: dict[str, int] = {}
    for key, value in obj.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, bool):
            out[key] = 1 if value else 0
        elif isinstance(value, int):
            out[key] = 1 if value != 0 else 0
        elif isinstance(value, float):
            out[key] = 1 if value >= 0.5 else 0
        else:
            continue
    if len(out) == 0:
        return None
    return out


def parse_verdict(*, raw_text: str) -> ParsedVerdict:
    snippet = _extract_first_json_object(raw_text)
    if snippet is None:
        return ParsedVerdict(
            verdict=None,
            justification=None,
            sub_scores=None,
            parse_status="parse-failure: no JSON object found",
        )
    try:
        payload = json.loads(snippet)
    except json.JSONDecodeError as exc:
        return ParsedVerdict(
            verdict=None,
            justification=None,
            sub_scores=None,
            parse_status=f"parse-failure: {exc}",
        )
    if not isinstance(payload, dict):
        return ParsedVerdict(
            verdict=None,
            justification=None,
            sub_scores=None,
            parse_status="parse-failure: not a JSON object",
        )
    verdict_raw = payload.get("verdict")
    justification = payload.get("justification")
    if not isinstance(verdict_raw, str) or not isinstance(justification, str):
        return ParsedVerdict(
            verdict=None,
            justification=None,
            sub_scores=_coerce_sub_scores(payload.get("sub_scores")),
            parse_status="parse-failure: missing required fields",
        )
    verdict_norm = verdict_raw.strip().lower()
    if verdict_norm not in {VERDICT_ACCEPTABLE, VERDICT_NEEDS_REVISION}:
        return ParsedVerdict(
            verdict=None,
            justification=justification.strip(),
            sub_scores=_coerce_sub_scores(payload.get("sub_scores")),
            parse_status=f"parse-failure: invalid verdict {verdict_raw!r}",
        )
    return ParsedVerdict(
        verdict=verdict_norm,
        justification=justification.strip(),
        sub_scores=_coerce_sub_scores(payload.get("sub_scores")),
        parse_status="ok",
    )
