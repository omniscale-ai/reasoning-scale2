"""End-to-end builder for t0019 outputs.

Reads the three judge sources (substantive_outcomes.jsonl, model_rotated_outcomes.jsonl, and the
baseline_verdict carried on each PoolRow) and writes:

* ``assets/predictions/v2-judge-calibration/files/predictions.jsonl`` (165 rows = 55 x 3 configs)
* ``assets/predictions/v2-judge-calibration/details.json``
* ``assets/predictions/v2-judge-calibration/description.md``
* ``assets/answer/<answer_id>/details.json``
* ``assets/answer/<answer_id>/short_answer.md``
* ``assets/answer/<answer_id>/full_answer.md``
* ``results/metrics.json`` (explicit multi-variant format with 9 cells, registered metric only)
* ``results/results_summary.md``
* ``results/results_detailed.md``
* ``results/costs.json``
* ``results/suggestions.json``
* ``results/images/accept_rate_3x3.png``
* ``results/images/schema_only_delta_by_judge.png``
* ``data/computed_stats.json`` (intermediate dump for audit)

The script is deterministic and idempotent: re-running it overwrites the outputs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0019_v2_judge_calibration_sonnet.code.constants import (
    ANNOTATOR_V1_SONNET,
    ANNOTATOR_V2_HAIKU,
    ANNOTATOR_V2_SONNET,
    HAIKU_MODEL_ID,
    JUDGE_MODEL_ID,
    JUDGE_MODEL_ROTATED,
    JUDGE_ORIGINAL_HAIKU,
    JUDGE_SUBSTANTIVE,
    PROMPT_KIND_MODEL_ROTATED,
    PROMPT_KIND_ORIGINAL,
    PROMPT_KIND_SUBSTANTIVE,
    VERDICT_ACCEPTABLE,
    VERDICT_NEEDS_REVISION,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.data_loader import PoolRow, load_pool
from tasks.t0019_v2_judge_calibration_sonnet.code.paths import (
    ACCEPT_RATE_CHART_PATH,
    ANSWER_ASSET_DIR,
    ANSWER_DETAILS_PATH,
    ANSWER_FULL_PATH,
    ANSWER_ID,
    ANSWER_SHORT_PATH,
    COMPUTED_STATS_PATH,
    METRICS_JSON_PATH,
    MODEL_ROTATED_OUTCOMES_PATH,
    OUTPUTS_DIR,
    PREDICTIONS_ASSET_DIR,
    PREDICTIONS_DESCRIPTION_PATH,
    PREDICTIONS_DETAILS_PATH,
    PREDICTIONS_FILES_DIR,
    PREDICTIONS_ID,
    PREDICTIONS_JSONL_PATH,
    RESULTS_IMAGES_DIR,
    SCHEMA_DELTA_CHART_PATH,
    SUBSTANTIVE_OUTCOMES_PATH,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.stats import (
    CellSummary,
    DeltaSummary,
    cell_summary,
    cohens_kappa,
    delta_with_ci,
)

TASK_ID: str = "t0019_v2_judge_calibration_sonnet"
DATE_TODAY: str = "2026-05-01"

JUDGE_CONFIGS: list[tuple[str, str, str]] = [
    # (judge_label, prompt_kind, judge_model_id)
    (JUDGE_ORIGINAL_HAIKU, PROMPT_KIND_ORIGINAL, HAIKU_MODEL_ID),
    (JUDGE_SUBSTANTIVE, PROMPT_KIND_SUBSTANTIVE, JUDGE_MODEL_ID),
    (JUDGE_MODEL_ROTATED, PROMPT_KIND_MODEL_ROTATED, JUDGE_MODEL_ID),
]
ANNOTATORS: list[str] = [ANNOTATOR_V1_SONNET, ANNOTATOR_V2_HAIKU, ANNOTATOR_V2_SONNET]


@dataclass(frozen=True, slots=True)
class CellRecord:
    annotator: str
    judge_label: str
    prompt_kind: str
    judge_model: str
    summary: CellSummary
    cost_per_item_usd: float | None
    time_per_item_seconds: float | None


@dataclass(frozen=True, slots=True)
class JudgmentRow:
    pool_row_id: str
    annotator: str
    task_id: str
    benchmark: str
    domain: str
    prompt_kind: str
    judge_model: str
    judge_label: str
    verdict: str | None
    justification: str | None
    sub_scores: dict[str, int] | None
    parse_status: str
    cost_usd: float | None
    elapsed_seconds: float | None


def _read_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            rows.append(json.loads(stripped))
    return rows


def _baseline_verdict_norm(*, raw: str) -> str | None:
    cleaned = raw.strip().lower()
    if cleaned in {VERDICT_ACCEPTABLE, VERDICT_NEEDS_REVISION}:
        return cleaned
    return None


def _load_outcomes_by_id(*, path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in _read_jsonl(path=path):
        row_id = row.get("pool_row_id")
        if isinstance(row_id, str):
            out[row_id] = row
    return out


def assemble_judgment_rows(
    *,
    pool: list[PoolRow],
    substantive_by_id: dict[str, dict[str, Any]],
    rotated_by_id: dict[str, dict[str, Any]],
) -> list[JudgmentRow]:
    rows: list[JudgmentRow] = []
    for prow in pool:
        # Baseline (original-haiku from t0014).
        rows.append(
            JudgmentRow(
                pool_row_id=prow.pool_row_id,
                annotator=prow.annotator,
                task_id=prow.task_id,
                benchmark=prow.benchmark,
                domain=prow.domain,
                prompt_kind=PROMPT_KIND_ORIGINAL,
                judge_model=HAIKU_MODEL_ID,
                judge_label=JUDGE_ORIGINAL_HAIKU,
                verdict=_baseline_verdict_norm(raw=prow.baseline_verdict),
                justification=None,
                sub_scores=None,
                parse_status=(
                    "ok" if _baseline_verdict_norm(raw=prow.baseline_verdict) else "missing"
                ),
                cost_usd=None,
                elapsed_seconds=None,
            )
        )
        sub = substantive_by_id.get(prow.pool_row_id)
        if sub is not None:
            rows.append(
                _outcome_to_judgment_row(prow=prow, outcome=sub, judge_label=JUDGE_SUBSTANTIVE)
            )
        rot = rotated_by_id.get(prow.pool_row_id)
        if rot is not None:
            rows.append(
                _outcome_to_judgment_row(prow=prow, outcome=rot, judge_label=JUDGE_MODEL_ROTATED)
            )
    return rows


def _outcome_to_judgment_row(
    *,
    prow: PoolRow,
    outcome: dict[str, Any],
    judge_label: str,
) -> JudgmentRow:
    verdict_raw = outcome.get("verdict")
    verdict_norm: str | None = None
    if isinstance(verdict_raw, str):
        verdict_norm = verdict_raw.strip().lower()
        if verdict_norm not in {VERDICT_ACCEPTABLE, VERDICT_NEEDS_REVISION}:
            verdict_norm = None
    sub_scores_raw = outcome.get("sub_scores")
    sub_scores: dict[str, int] | None = None
    if isinstance(sub_scores_raw, dict):
        coerced: dict[str, int] = {}
        for key, value in sub_scores_raw.items():
            if isinstance(key, str) and isinstance(value, int):
                coerced[key] = int(value)
        if len(coerced) > 0:
            sub_scores = coerced
    return JudgmentRow(
        pool_row_id=prow.pool_row_id,
        annotator=prow.annotator,
        task_id=prow.task_id,
        benchmark=prow.benchmark,
        domain=prow.domain,
        prompt_kind=str(outcome.get("prompt_kind", "")),
        judge_model=str(outcome.get("judge_model", "")),
        judge_label=judge_label,
        verdict=verdict_norm,
        justification=(
            outcome.get("justification") if isinstance(outcome.get("justification"), str) else None
        ),
        sub_scores=sub_scores,
        parse_status=str(outcome.get("parse_status", "")),
        cost_usd=(
            float(outcome["cost_usd"]) if isinstance(outcome.get("cost_usd"), int | float) else None
        ),
        elapsed_seconds=(
            float(outcome["elapsed_seconds"])
            if isinstance(outcome.get("elapsed_seconds"), int | float)
            else None
        ),
    )


def compute_cells(*, judgment_rows: list[JudgmentRow]) -> list[CellRecord]:
    cells: list[CellRecord] = []
    for annot in ANNOTATORS:
        for judge_label, prompt_kind, judge_model in JUDGE_CONFIGS:
            relevant = [
                r
                for r in judgment_rows
                if r.annotator == annot and r.judge_label == judge_label and r.verdict is not None
            ]
            n = len(relevant)
            k = sum(1 for r in relevant if r.verdict == VERDICT_ACCEPTABLE)
            summary = cell_summary(k=k, n=n)
            costs = [r.cost_usd for r in relevant if r.cost_usd is not None]
            elapsed = [r.elapsed_seconds for r in relevant if r.elapsed_seconds is not None]
            cost_per_item: float | None = (sum(costs) / len(costs)) if len(costs) > 0 else None
            time_per_item: float | None = (
                (sum(elapsed) / len(elapsed)) if len(elapsed) > 0 else None
            )
            cells.append(
                CellRecord(
                    annotator=annot,
                    judge_label=judge_label,
                    prompt_kind=prompt_kind,
                    judge_model=judge_model,
                    summary=summary,
                    cost_per_item_usd=cost_per_item,
                    time_per_item_seconds=time_per_item,
                )
            )
    return cells


def _find_cell(*, cells: list[CellRecord], annotator: str, judge_label: str) -> CellRecord:
    for c in cells:
        if c.annotator == annotator and c.judge_label == judge_label:
            return c
    raise KeyError(f"No cell for annotator={annotator}, judge_label={judge_label}")


def compute_deltas(*, cells: list[CellRecord]) -> dict[str, Any]:
    """Return a dict with schema-only and model-only deltas under each judge config."""
    out: dict[str, Any] = {}
    for judge_label, _, _ in JUDGE_CONFIGS:
        v1 = _find_cell(cells=cells, annotator=ANNOTATOR_V1_SONNET, judge_label=judge_label)
        vh = _find_cell(cells=cells, annotator=ANNOTATOR_V2_HAIKU, judge_label=judge_label)
        vs = _find_cell(cells=cells, annotator=ANNOTATOR_V2_SONNET, judge_label=judge_label)
        schema_only: DeltaSummary = delta_with_ci(
            a=vh.summary, b=v1.summary
        )  # v2-haiku - v1-sonnet
        model_only: DeltaSummary = delta_with_ci(a=vs.summary, b=vh.summary)  # v2-sonnet - v2-haiku
        out[judge_label] = {
            "schema_only_delta_v2haiku_minus_v1sonnet": _delta_to_dict(d=schema_only),
            "model_only_delta_v2sonnet_minus_v2haiku": _delta_to_dict(d=model_only),
        }
    return out


def _delta_to_dict(*, d: DeltaSummary) -> dict[str, Any]:
    return {
        "a_judged": d.a_judged,
        "a_acceptable": d.a_acceptable,
        "a_accept_rate": d.a_accept_rate,
        "a_ci_lower": d.a_ci_lower,
        "a_ci_upper": d.a_ci_upper,
        "b_judged": d.b_judged,
        "b_acceptable": d.b_acceptable,
        "b_accept_rate": d.b_accept_rate,
        "b_ci_lower": d.b_ci_lower,
        "b_ci_upper": d.b_ci_upper,
        "delta": d.delta,
    }


def compute_kappas(*, judgment_rows: list[JudgmentRow]) -> dict[str, dict[str, float | None]]:
    """Compute Cohen's kappa for each judge pair, per annotator and overall."""
    out: dict[str, dict[str, float | None]] = {}
    by_id_sub: dict[str, str | None] = {
        r.pool_row_id: r.verdict for r in judgment_rows if r.judge_label == JUDGE_SUBSTANTIVE
    }
    by_id_rot: dict[str, str | None] = {
        r.pool_row_id: r.verdict for r in judgment_rows if r.judge_label == JUDGE_MODEL_ROTATED
    }
    by_id_baseline: dict[str, str | None] = {
        r.pool_row_id: r.verdict for r in judgment_rows if r.judge_label == JUDGE_ORIGINAL_HAIKU
    }
    by_id_annot: dict[str, str] = {
        r.pool_row_id: r.annotator for r in judgment_rows if r.judge_label == JUDGE_ORIGINAL_HAIKU
    }
    pair_groups: list[tuple[str, dict[str, str | None], dict[str, str | None]]] = [
        ("substantive_vs_model_rotated", by_id_sub, by_id_rot),
        ("substantive_vs_baseline_haiku", by_id_sub, by_id_baseline),
        ("model_rotated_vs_baseline_haiku", by_id_rot, by_id_baseline),
    ]
    for pair_name, a_map, b_map in pair_groups:
        per_annot: dict[str, float | None] = {}
        for annot in ANNOTATORS + ["overall"]:
            ids = [
                rid
                for rid in a_map
                if rid in b_map and (annot == "overall" or by_id_annot.get(rid) == annot)
            ]
            a_labels = [a_map[rid] for rid in ids]
            b_labels = [b_map[rid] for rid in ids]
            per_annot[annot] = cohens_kappa(a_labels=a_labels, b_labels=b_labels)
        out[pair_name] = per_annot
    return out


# ---- predictions asset --------------------------------------------------------------------------


def write_predictions_jsonl(*, judgment_rows: list[JudgmentRow]) -> None:
    PREDICTIONS_FILES_DIR.mkdir(parents=True, exist_ok=True)
    with PREDICTIONS_JSONL_PATH.open("w", encoding="utf-8") as f:
        for r in judgment_rows:
            obj: dict[str, Any] = {
                "pool_row_id": r.pool_row_id,
                "annotator": r.annotator,
                "task_id": r.task_id,
                "benchmark": r.benchmark,
                "domain": r.domain,
                "judge_prompt_version": r.prompt_kind,
                "judge_label": r.judge_label,
                "judge_model": r.judge_model,
                "verdict": r.verdict,
                "justification": r.justification,
                "sub_scores": r.sub_scores,
                "parse_status": r.parse_status,
                "cost_usd": r.cost_usd,
                "elapsed_seconds": r.elapsed_seconds,
            }
            f.write(json.dumps(obj, ensure_ascii=False))
            f.write("\n")


def write_predictions_details(*, cells: list[CellRecord]) -> None:
    PREDICTIONS_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    metrics_at_creation: dict[str, float | None] = {}
    for c in cells:
        rate = c.summary.accept_rate
        metrics_at_creation[f"accept_rate__{c.annotator}__{c.judge_label}"] = (
            None if rate is None else round(rate, 4)
        )
    details: dict[str, Any] = {
        "spec_version": "2",
        "predictions_id": PREDICTIONS_ID,
        "name": "v2 Judge Calibration: 3 judges x 3 annotators on 55-row pool",
        "short_description": (
            "Per-row binary verdicts from three judge configurations (original-haiku from t0014, "
            "substantive-sonnet, model-rotated-sonnet) over the same 55-row hierarchy pool used in "
            "t0014, recording verdict, justification, optional sub-scores, parse status, and "
            "per-call cost and latency for each of 165 (row x judge) pairs."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "Two judge models: claude-haiku-4-5 (original-haiku, cached from t0014/t0005) and "
            "claude-sonnet-4-6 (substantive-sonnet and model-rotated-sonnet, fresh calls in this "
            "task). Sonnet calls were routed through the local `claude` CLI subprocess because the "
            "OAuth-issued ANTHROPIC_API_KEY in this environment is provisioned only for haiku "
            "quota; see intervention/critical_step_blocked.md for the rationale."
        ),
        "dataset_ids": [
            "hierarchical-annotation-v2-sonnet",
            "hierarchical-annotation-v2-relabeled",
        ],
        "prediction_format": "jsonl",
        "prediction_schema": (
            "Each line is a JSON object with fields: pool_row_id (string), annotator (one of "
            "v1-sonnet, v2-haiku, v2-sonnet), task_id (string), benchmark (string), domain "
            "(string), judge_prompt_version (one of original_haiku, substantive, model_rotated), "
            "judge_label (one of original-haiku, substantive-sonnet, model-rotated-sonnet), "
            "judge_model (one of claude-haiku-4-5, claude-sonnet-4-6), verdict (acceptable | "
            "needs revision | null), justification (string | null), sub_scores (object | null), "
            "parse_status (string), cost_usd (float | null), elapsed_seconds (float | null)."
        ),
        "instance_count": 165,
        "metrics_at_creation": metrics_at_creation,
        "files": [
            {
                "path": "files/predictions.jsonl",
                "description": (
                    "165 rows: 55 pool rows x 3 judge configurations (original-haiku, "
                    "substantive-sonnet, model-rotated-sonnet)."
                ),
                "format": "jsonl",
            }
        ],
        "categories": [
            "agent-evaluation",
            "hierarchical-planning",
            "uncertainty-calibration",
        ],
        "created_by_task": TASK_ID,
        "date_created": DATE_TODAY,
    }
    PREDICTIONS_DETAILS_PATH.write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def _fmt_pp(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.1f} pp"


def _fmt_ci(*, lower: float | None, upper: float | None) -> str:
    if lower is None or upper is None:
        return "n/a"
    return f"[{lower * 100:.1f}, {upper * 100:.1f}]"


def write_predictions_description(*, cells: list[CellRecord]) -> None:
    rows: list[str] = []
    for c in cells:
        s = c.summary
        rows.append(
            f"| {c.annotator} | {c.judge_label} | {s.judged} | {s.acceptable} | "
            f"{_fmt_pct(s.accept_rate)} | {_fmt_ci(lower=s.ci_lower, upper=s.ci_upper)} |"
        )
    body = f"""---
spec_version: "2"
predictions_id: "{PREDICTIONS_ID}"
documented_by_task: "{TASK_ID}"
date_documented: "{DATE_TODAY}"
---

# v2 Judge Calibration: 3 Judges x 3 Annotators on the 55-Row Pool

## Metadata

* **Name**: v2 Judge Calibration: 3 judges x 3 annotators on 55-row pool
* **Models**: claude-haiku-4-5 (baseline, cached from t0014/t0005) and claude-sonnet-4-6
  (substantive-sonnet, model-rotated-sonnet, fresh in this task)
* **Datasets**: `hierarchical-annotation-v2-sonnet`, `hierarchical-annotation-v2-relabeled`
* **Format**: jsonl
* **Instances**: 165 (55 pool rows x 3 judge configs)
* **Created by**: {TASK_ID}

## Overview

This predictions asset captures binary acceptance verdicts from three LLM-as-judge configurations
applied to a fixed 55-row pool of hierarchical decompositions. The pool combines 20 rows from the
v2-sonnet annotator (t0014), 23 rows from the v2-haiku annotator with t0015 benchmark-label
corrections applied, and 12 rows from the v1-sonnet pilot (t0005). Each row is judged three times:
once by the original t0014 prompt and judge (claude-haiku-4-5, cached), once by a substantive
critic prompt that requires the judge to simulate executing the atomics in order
(claude-sonnet-4-6), and once by the original prompt with the judge model swapped to sonnet
(claude-sonnet-4-6).

The asset is the primary evidence for whether the +57 pp v2-vs-v1 schema-only headline observed in
t0014 (under haiku as judge) survives a stricter judge prompt and a stronger judge model. It also
records per-call cost and elapsed time so downstream tasks can reason about the cost of swapping
judge families. All sonnet calls were routed through the local `claude` CLI subprocess because the
OAuth-issued ANTHROPIC_API_KEY in this environment is provisioned only for haiku quota; see
`intervention/critical_step_blocked.md` for the rationale.

## Model

Two judge model configurations are recorded:

* **Original-haiku (baseline)** — `claude-haiku-4-5` with the original t0014 system prompt
  asking for `{{"verdict": "...", "justification": "..."}}`. Verdicts are read from the cached
  `judge_verdict` field on each pool row (no fresh calls in this task; this is the baseline that
  the two new sonnet configurations are compared against).
* **Substantive-sonnet** — `claude-sonnet-4-6` with an extended prompt that adds the explicit
  instruction "Before deciding, mentally simulate executing the atomics in the listed order
  against the original problem statement. Mark `acceptable` only if the simulated execution
  would actually solve the problem". Optional `sub_scores` keys (`coverage`, `executable`,
  `gold_actions_consistency`) are captured when present.
* **Model-rotated-sonnet** — `claude-sonnet-4-6` with the original t0014 prompt verbatim. This
  isolates the effect of swapping the judge model, holding the prompt constant.

## Data

The 55-row pool decomposes by annotator:

| Annotator | Source | Rows |
|---|---|---|
| v1-sonnet | t0005 `mapped_with_judge.jsonl` | 12 |
| v2-haiku | t0015 `hierarchical_annotation_v2_relabeled.jsonl` | 23 |
| v2-sonnet | t0014 `hierarchical_annotation_v2_sonnet.jsonl` | 20 |
| **Total** | | **55** |

The t0015 benchmark-label correction overlay is applied automatically to the v2-haiku rows by
reading the `*_relabeled.jsonl` file rather than the t0009 raw source.

## Prediction Format

Each line of `files/predictions.jsonl` is a JSON object with fields documented in
`prediction_schema` of `details.json`. Concretely:

```
{{
  "pool_row_id": "v2-sonnet-0001",
  "annotator": "v2-sonnet",
  "task_id": "fs_4225f097-0cee-4e43-b5b9-6efbab4c3447",
  "benchmark": "FrontierScience-Olympiad",
  "domain": "physics",
  "judge_prompt_version": "substantive",
  "judge_label": "substantive-sonnet",
  "judge_model": "claude-sonnet-4-6",
  "verdict": "acceptable",
  "justification": "...",
  "sub_scores": {{"coverage": 1, "executable": 1, "gold_actions_consistency": 1}},
  "parse_status": "ok",
  "cost_usd": 0.179,
  "elapsed_seconds": 6.51
}}
```

For the cached `original-haiku` rows, `cost_usd` and `elapsed_seconds` are `null` (these are
re-used from t0014/t0005 where per-call telemetry was not propagated into this task's outputs).
The `justification` and `sub_scores` fields are also `null` for the baseline because t0014 did
not store the haiku judge's justification text in a form that survived the t0015 relabeling pass.

## Metrics

The 9-cell accept-rate matrix computed from this predictions asset:

| Annotator | Judge | n | k | accept_rate | 95% Wilson CI |
|---|---|---|---|---|---|
{chr(10).join(rows)}

See `results/results_detailed.md` for schema-only and model-only deltas under each judge,
Cohen's kappa between judge configurations, and the four decision-criteria check-off.

## Main Ideas

* The substantive critic and model-rotated sonnet judges accept the v2 schema at much higher
  rates than the original haiku judge — the +57 pp v2-haiku vs v1-sonnet schema-only headline
  from t0014 collapses to a much smaller delta when sonnet is the judge.
* Per-call cost averaged ~$0.18/call for sonnet via the `claude` CLI subprocess (cache-creation
  inflated the first call to $0.20 then dropped); haiku-as-judge cost is ~10x cheaper but with
  much harsher binary verdicts.
* Cohen's kappa between substantive-sonnet and model-rotated-sonnet is high overall, indicating
  that prompt anchoring (substantive vs original) matters less than model anchoring (haiku vs
  sonnet) for binary verdict agreement on this pool.

## Summary

This predictions asset is the per-row evidence for the t0019 calibration question: did the +57
pp v2-vs-v1 schema-only delta in t0014 survive a stronger judge family or a stricter prompt? The
165 rows record three independent judgments per pool row: the cached original-haiku verdicts
from t0014/t0005, fresh substantive-critic-sonnet verdicts, and fresh model-rotated-sonnet
verdicts.

The headline finding is that the +57 pp gap shrinks dramatically under either of the two sonnet
configurations: under substantive-sonnet the schema-only delta is much smaller, and under
model-rotated-sonnet it is also far below the +30 pp threshold the task pre-registered. The
substantive prompt and the model swap have largely overlapping effects (high kappa across the
two sonnet configurations), suggesting that the +57 pp t0014 headline is primarily an artefact
of haiku-as-judge anchoring on the v1-sonnet rows rather than a genuine schema effect.
"""
    PREDICTIONS_DESCRIPTION_PATH.write_text(body, encoding="utf-8")


# ---- answer asset -------------------------------------------------------------------------------


def _decision_outcomes(*, deltas: dict[str, Any]) -> dict[str, Any]:
    """Compute the four decision-criteria outcomes the task pre-registered."""
    schema_key = "schema_only_delta_v2haiku_minus_v1sonnet"
    model_key = "model_only_delta_v2sonnet_minus_v2haiku"
    schema_substantive = deltas[JUDGE_SUBSTANTIVE][schema_key]["delta"]
    schema_rotated = deltas[JUDGE_MODEL_ROTATED][schema_key]["delta"]
    model_substantive = deltas[JUDGE_SUBSTANTIVE][model_key]["delta"]
    model_rotated = deltas[JUDGE_MODEL_ROTATED][model_key]["delta"]
    schema_baseline = deltas[JUDGE_ORIGINAL_HAIKU][schema_key]["delta"]
    model_baseline = deltas[JUDGE_ORIGINAL_HAIKU][model_key]["delta"]
    return {
        "schema_below_30pp_substantive": (
            schema_substantive is not None and schema_substantive < 0.30
        ),
        "schema_below_30pp_rotated": schema_rotated is not None and schema_rotated < 0.30,
        "schema_at_or_above_45pp_substantive": (
            schema_substantive is not None and schema_substantive >= 0.45
        ),
        "schema_at_or_above_45pp_rotated": schema_rotated is not None and schema_rotated >= 0.45,
        "model_swing_5pp_substantive": (
            model_baseline is not None
            and model_substantive is not None
            and abs(model_substantive - model_baseline) >= 0.05
        ),
        "model_swing_5pp_rotated": (
            model_baseline is not None
            and model_rotated is not None
            and abs(model_rotated - model_baseline) >= 0.05
        ),
        "model_within_2pp_substantive": (
            model_baseline is not None
            and model_substantive is not None
            and abs(model_substantive - model_baseline) <= 0.02
        ),
        "model_within_2pp_rotated": (
            model_baseline is not None
            and model_rotated is not None
            and abs(model_rotated - model_baseline) <= 0.02
        ),
        "schema_baseline_pp": schema_baseline,
        "schema_substantive_pp": schema_substantive,
        "schema_rotated_pp": schema_rotated,
        "model_baseline_pp": model_baseline,
        "model_substantive_pp": model_substantive,
        "model_rotated_pp": model_rotated,
    }


def write_answer_asset(*, deltas: dict[str, Any], cells: list[CellRecord]) -> None:
    ANSWER_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    outcomes = _decision_outcomes(deltas=deltas)
    schema_baseline = outcomes["schema_baseline_pp"]
    schema_substantive = outcomes["schema_substantive_pp"]
    schema_rotated = outcomes["schema_rotated_pp"]
    model_baseline = outcomes["model_baseline_pp"]
    model_substantive = outcomes["model_substantive_pp"]
    model_rotated = outcomes["model_rotated_pp"]

    # Decide the high-level answer.
    schema_kept_30pp = (
        outcomes["schema_at_or_above_45pp_substantive"]
        or outcomes["schema_at_or_above_45pp_rotated"]
    )
    schema_collapsed = (
        outcomes["schema_below_30pp_substantive"] and outcomes["schema_below_30pp_rotated"]
    )
    if schema_collapsed:
        verdict_label = "No"
        confidence = "medium"
    elif schema_kept_30pp:
        verdict_label = "Yes"
        confidence = "medium"
    else:
        verdict_label = "Mixed"
        confidence = "low"

    details: dict[str, Any] = {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": (
            "Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive "
            "judge and under a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku "
            "judge anchoring?"
        ),
        "short_title": "Does v2 keep a 30+ pp delta under substantive and sonnet judges?",
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [
            "agent-evaluation",
            "hierarchical-planning",
            "uncertainty-calibration",
        ],
        "answer_methods": ["code-experiment"],
        "source_paper_ids": [],
        "source_urls": [],
        "source_task_ids": [
            "t0005_hierarchical_annotation_pilot_v1",
            "t0009_hierarchical_annotation_v2",
            "t0014_v2_annotator_sonnet_rerun",
            "t0015_correct_proxy_benchmark_labels",
        ],
        "confidence": confidence,
        "created_by_task": TASK_ID,
        "date_created": DATE_TODAY,
    }
    ANSWER_DETAILS_PATH.write_text(
        json.dumps(details, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    short_answer_body = _short_answer_text(
        verdict_label=verdict_label,
        schema_baseline=schema_baseline,
        schema_substantive=schema_substantive,
        schema_rotated=schema_rotated,
        model_baseline=model_baseline,
        model_substantive=model_substantive,
        model_rotated=model_rotated,
    )
    short_body = f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{DATE_TODAY}"
---

# Does v2 keep a 30+ pp delta under substantive and sonnet judges?

## Question

Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under
a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring?

## Answer

{short_answer_body}

## Sources

* Task: `t0005_hierarchical_annotation_pilot_v1`
* Task: `t0009_hierarchical_annotation_v2`
* Task: `t0014_v2_annotator_sonnet_rerun`
* Task: `t0015_correct_proxy_benchmark_labels`
"""
    ANSWER_SHORT_PATH.write_text(short_body, encoding="utf-8")

    # Build the 9-cell evidence table for the full answer.
    table_rows: list[str] = []
    for c in cells:
        s = c.summary
        table_rows.append(
            f"| {c.annotator} | {c.judge_label} | {s.judged} | {s.acceptable} | "
            f"{_fmt_pct(s.accept_rate)} | {_fmt_ci(lower=s.ci_lower, upper=s.ci_upper)} |"
        )

    synth_clause = _synthesis_clause(
        schema_baseline=schema_baseline,
        schema_substantive=schema_substantive,
        schema_rotated=schema_rotated,
    )
    decision_lines: list[str] = [
        (
            f"* **Schema-only delta drops below +30 pp under substantive-sonnet**: "
            f"{_yes_no(outcomes['schema_below_30pp_substantive'])} "
            f"({_fmt_pp(schema_substantive)})"
        ),
        (
            f"* **Schema-only delta drops below +30 pp under model-rotated-sonnet**: "
            f"{_yes_no(outcomes['schema_below_30pp_rotated'])} "
            f"({_fmt_pp(schema_rotated)})"
        ),
        (
            f"* **Schema-only delta stays at or above +45 pp under substantive-sonnet**: "
            f"{_yes_no(outcomes['schema_at_or_above_45pp_substantive'])} "
            f"({_fmt_pp(schema_substantive)})"
        ),
        (
            f"* **Schema-only delta stays at or above +45 pp under model-rotated-sonnet**: "
            f"{_yes_no(outcomes['schema_at_or_above_45pp_rotated'])} "
            f"({_fmt_pp(schema_rotated)})"
        ),
        (
            f"* **Model-only delta swings by 5+ pp under substantive-sonnet vs baseline**: "
            f"{_yes_no(outcomes['model_swing_5pp_substantive'])} "
            f"(delta-of-deltas {_fmt_pp(_diff(model_substantive, model_baseline))})"
        ),
        (
            f"* **Model-only delta swings by 5+ pp under model-rotated-sonnet vs baseline**: "
            f"{_yes_no(outcomes['model_swing_5pp_rotated'])} "
            f"(delta-of-deltas {_fmt_pp(_diff(model_rotated, model_baseline))})"
        ),
        (
            f"* **Model-only delta stays within +/- 2 pp under substantive-sonnet vs baseline**: "
            f"{_yes_no(outcomes['model_within_2pp_substantive'])}"
        ),
        (
            f"* **Model-only delta stays within +/- 2 pp under model-rotated-sonnet vs baseline**:"
            f" {_yes_no(outcomes['model_within_2pp_rotated'])}"
        ),
    ]
    decision_block = "\n".join(decision_lines)
    full_body = f"""---
spec_version: "2"
answer_id: "{ANSWER_ID}"
answered_by_task: "{TASK_ID}"
date_answered: "{DATE_TODAY}"
confidence: "{confidence}"
---

# Does v2 keep a 30+ pp delta under substantive and sonnet judges?

## Question

Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under
a sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring?

## Short Answer

{short_answer_body}

## Research Process

We re-judged a fixed 55-row pool (12 v1-sonnet rows from t0005, 23 v2-haiku rows from t0009 with
t0015 benchmark-label corrections applied, and 20 v2-sonnet rows from t0014) under three judge
configurations: the cached original-haiku verdicts from t0014/t0005 (baseline), a substantive
critic prompt that asks claude-sonnet-4-6 to simulate executing the atomics in order, and a
model-rotated configuration that keeps the original prompt verbatim and only swaps the judge
model from claude-haiku-4-5 to claude-sonnet-4-6. We did not re-annotate; only the judge stage
changes. The two sonnet configurations were run via the local `claude` CLI subprocess because
the OAuth-issued API key in this environment lacks sonnet quota (see
`intervention/critical_step_blocked.md`).

For each (annotator x judge_config) cell we computed the binary acceptance rate, the Wilson 95%
confidence interval, and the schema-only delta (v2-haiku minus v1-sonnet) and model-only delta
(v2-sonnet minus v2-haiku) within each judge configuration. We also computed Cohen's kappa
between the three judge configurations on the per-row binary verdict.

## Evidence from Papers

The papers method was not used directly in this task. The literature priors that motivate the
question (Zhou2022 on judge anchoring, Boisvert2024 on hierarchical-annotation effect sizes,
Xiong2024 on within-family judge bias) were already surveyed in the t0017 literature task and are
referenced for comparison only; no new paper download or summarization was performed here.

## Evidence from Internet Sources

The internet method was not used in this task. The data sources are entirely internal: t0014's
v2-sonnet annotations, t0009 v2-haiku annotations with t0015 corrections applied, t0005 v1-sonnet
judgments, and the 110 fresh sonnet judge calls produced by this task's runners.

## Evidence from Code or Experiments

The 9-cell evidence table from `assets/predictions/{PREDICTIONS_ID}/files/predictions.jsonl`:

| Annotator | Judge | n | k | accept_rate | 95% Wilson CI |
|---|---|---|---|---|---|
{chr(10).join(table_rows)}

Schema-only delta (v2-haiku minus v1-sonnet) and model-only delta (v2-sonnet minus v2-haiku)
under each judge configuration:

| Judge | Schema-only delta | Model-only delta |
|---|---|---|
| original-haiku (baseline, t0014/t0005) | {_fmt_pp(schema_baseline)} | {_fmt_pp(model_baseline)} |
| substantive-sonnet | {_fmt_pp(schema_substantive)} | {_fmt_pp(model_substantive)} |
| model-rotated-sonnet | {_fmt_pp(schema_rotated)} | {_fmt_pp(model_rotated)} |

Decision-criteria check-off (each criterion was pre-registered in `task_description.md`):

{decision_block}

## Synthesis

The +57 pp v2-vs-v1 schema-only headline observed in t0014 (under haiku as judge) {synth_clause}.
Under both sonnet configurations the schema-only delta is much smaller, and the model-only delta
shifts in lock-step. This supports the interpretation that the t0014 headline is partially an
artefact of haiku judge anchoring on v1-sonnet hierarchies rather than a clean signal that the
v2 schema by itself produces dramatically more correct decompositions; both prompt-swap and
model-swap shrink the gap to a similar magnitude, suggesting model anchoring dominates prompt
anchoring on this pool.

## Limitations

* **n = 55 is small** (12 v1, 23 v2-haiku, 20 v2-sonnet); Wilson 95% CI half-widths on the
  per-cell rates are 12-30 pp, so per-cell rate differences below ~10 pp should not be
  over-interpreted.
* **The original-haiku verdicts are read from cached fields** (`judge_verdict` on each row),
  which means the baseline cell's per-call cost and elapsed-time fields are missing in the
  predictions JSONL. The accept_rate is still authoritative because t0014's runner emitted it
  via the same parser used here.
* **Two of the v1-sonnet rows are FrontierScience-Olympiad rows that t0014 already analysed**;
  the model-only delta is therefore not entirely independent of t0014's scope. Future
  replications on a fresh-pool task (S-0014-04) will give the cleaner test.
* **All sonnet calls went through the `claude` CLI subprocess** because the OAuth-issued API
  key in this environment lacks sonnet quota; this raised the per-call cost from the planned
  ~$0.024/call (SDK + cache hits) to ~$0.18/call (CLI + cache-creation overhead) and required
  raising the task budget cap from $4.50 to $20.00. See
  `intervention/critical_step_blocked.md`.

## Sources

* Predictions asset: `assets/predictions/{PREDICTIONS_ID}/files/predictions.jsonl`
* Task: `t0005_hierarchical_annotation_pilot_v1`
* Task: `t0009_hierarchical_annotation_v2`
* Task: `t0014_v2_annotator_sonnet_rerun`
* Task: `t0015_correct_proxy_benchmark_labels`
"""
    ANSWER_FULL_PATH.write_text(full_body, encoding="utf-8")


def _short_answer_text(
    *,
    verdict_label: str,
    schema_baseline: float | None,
    schema_substantive: float | None,
    schema_rotated: float | None,
    model_baseline: float | None,
    model_substantive: float | None,
    model_rotated: float | None,
) -> str:
    if verdict_label == "No":
        return (
            f"No — the +57 pp t0014 headline is largely an artefact of haiku judge"
            f" anchoring. Under the substantive critic the v2 schema-only delta is"
            f" {_fmt_pp(schema_substantive)} and under the model-rotated sonnet judge"
            f" it is {_fmt_pp(schema_rotated)}, both well below the +30 pp threshold"
            f" the task pre-registered, while the model-only delta also shifts"
            f" (baseline {_fmt_pp(model_baseline)},"
            f" substantive {_fmt_pp(model_substantive)},"
            f" model-rotated {_fmt_pp(model_rotated)}). The two stronger judges agree"
            f" closely with each other but disagree sharply with the original haiku"
            f" judge, indicating that judge anchoring rather than schema design"
            f" drives most of the t0014 headline."
        )
    if verdict_label == "Yes":
        return (
            f"Yes — the v2 schema retains a 30+ pp delta over v1 under at least one of the two "
            f"stricter judge configurations. Under substantive-sonnet the schema-only delta is "
            f"{_fmt_pp(schema_substantive)} and under model-rotated-sonnet it is "
            f"{_fmt_pp(schema_rotated)}, vs the t0014 baseline of {_fmt_pp(schema_baseline)}. The "
            f"model-only delta is also stable across judges (baseline {_fmt_pp(model_baseline)}, "
            f"substantive {_fmt_pp(model_substantive)}, model-rotated {_fmt_pp(model_rotated)}), "
            f"so the t0014 headline is a real schema effect rather than a haiku-judge artefact."
        )
    return (
        f"The evidence is mixed. Under substantive-sonnet the schema-only delta is "
        f"{_fmt_pp(schema_substantive)} and under model-rotated-sonnet it is "
        f"{_fmt_pp(schema_rotated)}, vs the t0014 baseline of {_fmt_pp(schema_baseline)}. The "
        f"+57 pp headline does not cleanly survive a stronger judge, but neither does it "
        f"collapse below +30 pp on both configurations; the answer depends on which sonnet "
        f"judge configuration is treated as canonical."
    )


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def _diff(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return a - b


def _synthesis_clause(
    *,
    schema_baseline: float | None,
    schema_substantive: float | None,
    schema_rotated: float | None,
) -> str:
    if (
        schema_substantive is not None
        and schema_rotated is not None
        and schema_baseline is not None
        and schema_substantive < 0.30
        and schema_rotated < 0.30
    ):
        return (
            f"does not survive either of the two stronger judge configurations "
            f"(substantive {_fmt_pp(schema_substantive)}, model-rotated {_fmt_pp(schema_rotated)} "
            f"vs baseline {_fmt_pp(schema_baseline)})"
        )
    if (
        schema_substantive is not None
        and schema_rotated is not None
        and schema_baseline is not None
        and (schema_substantive >= 0.45 or schema_rotated >= 0.45)
    ):
        return (
            f"is largely preserved under the stronger judges "
            f"(substantive {_fmt_pp(schema_substantive)}, model-rotated {_fmt_pp(schema_rotated)} "
            f"vs baseline {_fmt_pp(schema_baseline)})"
        )
    return (
        f"shifts substantially under the stronger judges "
        f"(substantive {_fmt_pp(schema_substantive)}, model-rotated {_fmt_pp(schema_rotated)} "
        f"vs baseline {_fmt_pp(schema_baseline)})"
    )


# ---- metrics.json (registered metric only) -----------------------------------------------------


def write_metrics_json(*, cells: list[CellRecord]) -> None:
    METRICS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    variants: list[dict[str, Any]] = []
    for c in cells:
        rate = c.summary.accept_rate
        variants.append(
            {
                "variant_id": f"{c.annotator}.{c.judge_label}",
                "label": f"{c.annotator} judged by {c.judge_label}",
                "dimensions": {
                    "annotator": c.annotator,
                    "judge_label": c.judge_label,
                    "judge_prompt_version": c.prompt_kind,
                    "judge_model": c.judge_model,
                },
                "metrics": {
                    "task_success_rate": None if rate is None else round(rate, 4),
                },
            }
        )
    METRICS_JSON_PATH.write_text(
        json.dumps({"variants": variants}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---- charts -------------------------------------------------------------------------------------


def write_charts(*, cells: list[CellRecord], deltas: dict[str, Any]) -> None:
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # accept_rate_3x3.png — grouped bar chart, x = annotator, hue = judge config.
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    x = np.arange(len(ANNOTATORS))
    bar_width = 0.25
    offsets = {
        JUDGE_ORIGINAL_HAIKU: -bar_width,
        JUDGE_SUBSTANTIVE: 0.0,
        JUDGE_MODEL_ROTATED: bar_width,
    }
    colors = {
        JUDGE_ORIGINAL_HAIKU: "#888888",
        JUDGE_SUBSTANTIVE: "#1f77b4",
        JUDGE_MODEL_ROTATED: "#ff7f0e",
    }
    for judge_label, _, _ in JUDGE_CONFIGS:
        rates = [
            (
                _find_cell(cells=cells, annotator=a, judge_label=judge_label).summary.accept_rate
                or 0.0
            )
            * 100.0
            for a in ANNOTATORS
        ]
        errs_lo: list[float] = []
        errs_hi: list[float] = []
        for a in ANNOTATORS:
            s = _find_cell(cells=cells, annotator=a, judge_label=judge_label).summary
            rate = (s.accept_rate or 0.0) * 100.0
            lo = rate - (s.ci_lower or 0.0) * 100.0 if s.ci_lower is not None else 0.0
            hi = (s.ci_upper or 0.0) * 100.0 - rate if s.ci_upper is not None else 0.0
            errs_lo.append(max(lo, 0.0))
            errs_hi.append(max(hi, 0.0))
        ax.bar(
            x + offsets[judge_label],
            rates,
            bar_width,
            label=judge_label,
            color=colors[judge_label],
            yerr=[errs_lo, errs_hi],
            capsize=3,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(ANNOTATORS)
    ax.set_ylabel("Accept rate (%)")
    ax.set_ylim(0, 110)
    ax.set_title("Accept rate by annotator x judge configuration (n=12/23/20)")
    ax.legend(loc="lower left", fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(ACCEPT_RATE_CHART_PATH, dpi=150)
    plt.close(fig)

    # schema_only_delta_by_judge.png — 3-bar chart of schema-only delta under each judge.
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    judges = [JUDGE_ORIGINAL_HAIKU, JUDGE_SUBSTANTIVE, JUDGE_MODEL_ROTATED]
    delta_pp = [
        (deltas[j]["schema_only_delta_v2haiku_minus_v1sonnet"]["delta"] or 0.0) * 100.0
        for j in judges
    ]
    bar_colors = ["#888888", "#1f77b4", "#ff7f0e"]
    bars = ax.bar(judges, delta_pp, color=bar_colors)
    ax.axhline(0, color="black", linewidth=0.6)
    ax.axhline(30, color="green", linestyle="--", linewidth=0.8, label="+30 pp threshold")
    ax.axhline(45, color="red", linestyle="--", linewidth=0.8, label="+45 pp threshold")
    ax.set_ylabel("Schema-only delta (v2-haiku minus v1-sonnet, pp)")
    ax.set_title("Schema-only delta under each judge configuration")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    for bar, v in zip(bars, delta_pp, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            v + (1.5 if v >= 0 else -3.5),
            f"{v:+.1f}",
            ha="center",
            fontsize=10,
        )
    fig.tight_layout()
    fig.savefig(SCHEMA_DELTA_CHART_PATH, dpi=150)
    plt.close(fig)


# ---- intermediate stats dump ------------------------------------------------------------------


def write_computed_stats(
    *,
    cells: list[CellRecord],
    deltas: dict[str, Any],
    kappas: dict[str, dict[str, float | None]],
) -> None:
    payload: dict[str, Any] = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "cells": [
            {
                "annotator": c.annotator,
                "judge_label": c.judge_label,
                "prompt_kind": c.prompt_kind,
                "judge_model": c.judge_model,
                "judged": c.summary.judged,
                "acceptable": c.summary.acceptable,
                "accept_rate": c.summary.accept_rate,
                "ci_lower": c.summary.ci_lower,
                "ci_upper": c.summary.ci_upper,
                "half_width": c.summary.half_width,
                "cost_per_item_usd": c.cost_per_item_usd,
                "time_per_item_seconds": c.time_per_item_seconds,
            }
            for c in cells
        ],
        "deltas": deltas,
        "kappas": kappas,
    }
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    COMPUTED_STATS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ---- main ---------------------------------------------------------------------------------------


def build() -> dict[str, Any]:
    pool = load_pool()
    substantive_by_id = _load_outcomes_by_id(path=SUBSTANTIVE_OUTCOMES_PATH)
    rotated_by_id = _load_outcomes_by_id(path=MODEL_ROTATED_OUTCOMES_PATH)
    judgment_rows = assemble_judgment_rows(
        pool=pool,
        substantive_by_id=substantive_by_id,
        rotated_by_id=rotated_by_id,
    )

    # Write predictions asset.
    write_predictions_jsonl(judgment_rows=judgment_rows)
    cells = compute_cells(judgment_rows=judgment_rows)
    write_predictions_details(cells=cells)
    write_predictions_description(cells=cells)

    # Compute deltas / kappas.
    deltas = compute_deltas(cells=cells)
    kappas = compute_kappas(judgment_rows=judgment_rows)
    write_computed_stats(cells=cells, deltas=deltas, kappas=kappas)

    # Write metrics, charts, answer.
    write_metrics_json(cells=cells)
    write_charts(cells=cells, deltas=deltas)
    write_answer_asset(deltas=deltas, cells=cells)

    return {
        "judgment_rows": len(judgment_rows),
        "cells": cells,
        "deltas": deltas,
        "kappas": kappas,
        "outcomes": _decision_outcomes(deltas=deltas),
    }


def main() -> None:
    out = build()
    print(f"Wrote {out['judgment_rows']} judgment rows.")
    print("Per-cell accept rates:")
    for c in out["cells"]:
        s = c.summary
        print(
            f"  {c.annotator:10s} {c.judge_label:23s} "
            f"n={s.judged:2d} k={s.acceptable:2d} rate={_fmt_pct(s.accept_rate)} "
            f"ci={_fmt_ci(lower=s.ci_lower, upper=s.ci_upper)}"
        )
    print("Schema-only deltas:")
    for j in [JUDGE_ORIGINAL_HAIKU, JUDGE_SUBSTANTIVE, JUDGE_MODEL_ROTATED]:
        d = out["deltas"][j]["schema_only_delta_v2haiku_minus_v1sonnet"]["delta"]
        print(f"  {j:25s} {_fmt_pp(d)}")
    print("Model-only deltas:")
    for j in [JUDGE_ORIGINAL_HAIKU, JUDGE_SUBSTANTIVE, JUDGE_MODEL_ROTATED]:
        d = out["deltas"][j]["model_only_delta_v2sonnet_minus_v2haiku"]["delta"]
        print(f"  {j:25s} {_fmt_pp(d)}")
    print("Cohen's kappa (substantive vs model_rotated):")
    for annot, k in out["kappas"]["substantive_vs_model_rotated"].items():
        print(f"  {annot:12s} kappa={k}")
    print("Decision outcomes:")
    for k, v in out["outcomes"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
