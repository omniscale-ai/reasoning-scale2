"""Paired McNemar (RQ1: A vs B; RQ5: B vs C) and 10-bin ECE analysis on the 130-paired set.

This script reads:

* the t0026 variant-A predictions JSONL (reused by reference; claude-sonnet-4-6)
* the t0027 variant-B predictions JSONL (re-run with plan_and_solve_v3; claude-sonnet-4-6)
* the t0027 variant-C predictions JSONL (re-run with matched_mismatch_v2 over v3; claude-sonnet-4-6)

It emits:

* ``data/mcnemar_results.json`` — full McNemar contingency tables, p-values, Bonferroni-corrected
  decision (α = 0.025) for both RQ1 (A vs B) and RQ5 (B vs C), plus per-subset breakdowns.
* ``data/calibration.json`` — 10-equal-width-bin ECE on variants B and C
  (calibration is undefined for A: A does not elicit verbalised confidence).
* ``results/metrics.json`` — three registered metrics per variant: ``task_success_rate``,
  ``overconfident_error_rate`` (B and C only), ``avg_decisions_per_task`` (informational).

All three variants use the same model (claude-sonnet-4-6), matching what t0026 actually ran. The
original task description erroneously stated claude-opus-4-7; we discovered the mismatch from
t0026's paths.py and trajectory error messages and corrected it here for scientific validity.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.calibration import (
    ECEResult,
    compute_ece_10bin,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.mcnemar import (
    pairwise_mcnemar,
)
from tasks.t0027_phase2_5_abc_rerun_with_fixed_b_and_c.code.paths import (
    CALIBRATION_PATH,
    MCNEMAR_RESULTS_PATH,
    METRICS_PATH,
    PAIRED_MANIFEST_PATH,
    PREDICTIONS_B_JSONL,
    PREDICTIONS_C_JSONL,
    SUBSET_FRONTSCI,
    SUBSET_SWEBENCH,
    SUBSET_TAUBENCH,
    T0026_PREDICTIONS_A_JSONL,
)

_BONFERRONI_ALPHA: Final[float] = 0.025
_OVERCONFIDENT_THRESHOLD: Final[float] = 0.8


@dataclass(frozen=True, slots=True)
class _PredictionRow:
    instance_id: str
    subset: str
    variant: str
    final_answer: str | None
    final_confidence: float | None
    cost_usd: float
    judge_sonnet_success: bool
    raised_malformed_plan_error: bool
    plan_parser_recovery_path: str
    plan_parser_attempts: int


def _read_jsonl(*, path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line_stripped = line.strip()
            if len(line_stripped) == 0:
                continue
            rows.append(json.loads(line_stripped))
    return rows


def _to_pred_row(*, raw: Mapping[str, Any]) -> _PredictionRow:
    return _PredictionRow(
        instance_id=str(raw["instance_id"]),
        subset=str(raw["subset"]),
        variant=str(raw["variant"]),
        final_answer=raw.get("final_answer"),
        final_confidence=(
            float(raw["final_confidence"]) if raw.get("final_confidence") is not None else None
        ),
        cost_usd=float(raw.get("cost_usd", 0.0)),
        judge_sonnet_success=bool(raw.get("judge_sonnet_success", False)),
        raised_malformed_plan_error=bool(raw.get("raised_malformed_plan_error", False)),
        plan_parser_recovery_path=str(raw.get("plan_parser_recovery_path") or "unknown"),
        plan_parser_attempts=int(raw.get("plan_parser_attempts") or 0),
    )


def _load_predictions_by_iid(*, path: Path) -> dict[str, _PredictionRow]:
    rows = _read_jsonl(path=path)
    return {r["instance_id"]: _to_pred_row(raw=r) for r in rows}


def _load_paired_instance_ids() -> tuple[list[str], dict[str, int]]:
    payload = json.loads(PAIRED_MANIFEST_PATH.read_text(encoding="utf-8"))
    return list(payload["instance_ids"]), dict(payload["per_subset_counts"])


def _filter_to_paired(
    *,
    predictions_by_iid: dict[str, _PredictionRow],
    paired_iids: list[str],
) -> list[_PredictionRow]:
    return [predictions_by_iid[iid] for iid in paired_iids if iid in predictions_by_iid]


def _success_arrays_aligned(
    *,
    a_rows: list[_PredictionRow],
    b_rows: list[_PredictionRow],
    paired_iids: list[str],
) -> tuple[list[bool], list[bool], list[str]]:
    """Return aligned [success_a, success_b] arrays in paired_iids order, dropping any iid
    missing from either side. Also return the list of iids actually used.
    """
    by_iid_a = {r.instance_id: r for r in a_rows}
    by_iid_b = {r.instance_id: r for r in b_rows}
    used_iids: list[str] = []
    success_a: list[bool] = []
    success_b: list[bool] = []
    for iid in paired_iids:
        ra = by_iid_a.get(iid)
        rb = by_iid_b.get(iid)
        if ra is None or rb is None:
            continue
        used_iids.append(iid)
        success_a.append(ra.judge_sonnet_success)
        success_b.append(rb.judge_sonnet_success)
    return success_a, success_b, used_iids


def _per_subset_mcnemar(
    *,
    a_rows: list[_PredictionRow],
    b_rows: list[_PredictionRow],
    paired_iids: list[str],
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    by_iid_a = {r.instance_id: r for r in a_rows}
    by_iid_b = {r.instance_id: r for r in b_rows}
    for subset in (SUBSET_SWEBENCH, SUBSET_TAUBENCH, SUBSET_FRONTSCI):
        sa: list[bool] = []
        sb: list[bool] = []
        for iid in paired_iids:
            ra = by_iid_a.get(iid)
            rb = by_iid_b.get(iid)
            if ra is None or rb is None:
                continue
            if ra.subset != subset:
                continue
            sa.append(ra.judge_sonnet_success)
            sb.append(rb.judge_sonnet_success)
        if len(sa) == 0:
            out[subset] = {"n_paired": 0, "note": "no paired instances in this subset"}
            continue
        result = pairwise_mcnemar(success_first=sa, success_second=sb)
        out[subset] = {
            "n_paired": len(sa),
            "success_rate_first": sum(sa) / len(sa),
            "success_rate_second": sum(sb) / len(sb),
            **result,
        }
    return out


def _bonferroni_decision(*, p_value: float) -> str:
    if p_value < _BONFERRONI_ALPHA:
        return f"reject_null (p={p_value:.6g} < alpha={_BONFERRONI_ALPHA})"
    return f"do_not_reject (p={p_value:.6g} >= alpha={_BONFERRONI_ALPHA})"


def _ece_for_variant(*, rows: list[_PredictionRow]) -> ECEResult | None:
    confidences: list[float] = []
    outcomes: list[bool] = []
    for r in rows:
        if r.final_confidence is None:
            continue
        confidences.append(r.final_confidence)
        outcomes.append(r.judge_sonnet_success)
    if len(confidences) == 0:
        return None
    return compute_ece_10bin(confidences=confidences, outcomes=outcomes)


def _ece_to_jsonable(*, result: ECEResult | None) -> Any:
    if result is None:
        return None
    return {
        "ece": result.ece,
        "n_total": result.n_total,
        "bins": [asdict(b) for b in result.bins],
    }


def _overconfident_error_rate(*, rows: list[_PredictionRow]) -> float | None:
    """Fraction of rows where final_confidence >= 0.8 AND judge_sonnet_success == False,
    over the rows that actually have a final_confidence value.
    """
    high_conf_rows = [r for r in rows if r.final_confidence is not None]
    if len(high_conf_rows) == 0:
        return None
    n_overconfident_errors = sum(
        1
        for r in high_conf_rows
        if r.final_confidence is not None
        and r.final_confidence >= _OVERCONFIDENT_THRESHOLD
        and not r.judge_sonnet_success
    )
    return n_overconfident_errors / len(high_conf_rows)


def _success_rate(*, rows: list[_PredictionRow]) -> float:
    if len(rows) == 0:
        return 0.0
    return sum(1 for r in rows if r.judge_sonnet_success) / len(rows)


def main() -> int:
    paired_iids, per_subset_counts = _load_paired_instance_ids()
    print(f"loaded paired manifest: {len(paired_iids)} instances, per_subset={per_subset_counts}")

    a_by_iid = _load_predictions_by_iid(path=T0026_PREDICTIONS_A_JSONL)
    b_by_iid = _load_predictions_by_iid(path=PREDICTIONS_B_JSONL)
    c_by_iid = _load_predictions_by_iid(path=PREDICTIONS_C_JSONL)
    print(
        f"loaded predictions: A={len(a_by_iid)} (t0026), B={len(b_by_iid)} (t0027), "
        f"C={len(c_by_iid)} (t0027)"
    )

    a_rows = _filter_to_paired(predictions_by_iid=a_by_iid, paired_iids=paired_iids)
    b_rows = _filter_to_paired(predictions_by_iid=b_by_iid, paired_iids=paired_iids)
    c_rows = _filter_to_paired(predictions_by_iid=c_by_iid, paired_iids=paired_iids)
    print(f"paired-filter rows: A={len(a_rows)}, B={len(b_rows)}, C={len(c_rows)}")

    success_a_b_a, success_a_b_b, ab_iids = _success_arrays_aligned(
        a_rows=a_rows, b_rows=b_rows, paired_iids=paired_iids
    )
    success_b_c_b, success_b_c_c, bc_iids = _success_arrays_aligned(
        a_rows=b_rows, b_rows=c_rows, paired_iids=paired_iids
    )

    rq1_overall = pairwise_mcnemar(success_first=success_a_b_a, success_second=success_a_b_b)
    rq5_overall = pairwise_mcnemar(success_first=success_b_c_b, success_second=success_b_c_c)

    rq1_per_subset = _per_subset_mcnemar(a_rows=a_rows, b_rows=b_rows, paired_iids=paired_iids)
    rq5_per_subset = _per_subset_mcnemar(a_rows=b_rows, b_rows=c_rows, paired_iids=paired_iids)

    mcnemar_payload: dict[str, Any] = {
        "spec_version": "1",
        "alpha_per_test_after_bonferroni": _BONFERRONI_ALPHA,
        "n_paired_target": len(paired_iids),
        "model_confound_note": (
            "All three variants were produced with claude-sonnet-4-6: A inherited from t0026 and "
            "B/C re-run in t0027 with the same model under test. No cross-model confound."
        ),
        "rq1_a_vs_b": {
            "label": "A (sonnet-4-6 scope-aware ReAct) vs B (sonnet-4-6 plan_and_solve_v3)",
            "n_paired_used": len(ab_iids),
            "success_rate_a": _success_rate(rows=[r for r in a_rows if r.instance_id in ab_iids]),
            "success_rate_b": _success_rate(rows=[r for r in b_rows if r.instance_id in ab_iids]),
            "overall": rq1_overall,
            "decision_bonferroni": _bonferroni_decision(p_value=float(rq1_overall["p_value"])),
            "per_subset": rq1_per_subset,
        },
        "rq5_b_vs_c": {
            "label": (
                "B (sonnet-4-6 plan_and_solve_v3) vs C (sonnet-4-6 matched_mismatch_v2 over v3)"
            ),
            "n_paired_used": len(bc_iids),
            "success_rate_b": _success_rate(rows=[r for r in b_rows if r.instance_id in bc_iids]),
            "success_rate_c": _success_rate(rows=[r for r in c_rows if r.instance_id in bc_iids]),
            "overall": rq5_overall,
            "decision_bonferroni": _bonferroni_decision(p_value=float(rq5_overall["p_value"])),
            "per_subset": rq5_per_subset,
        },
        "parser_failure_rates": {
            "b_t0027": (
                sum(1 for r in b_rows if r.raised_malformed_plan_error) / max(1, len(b_rows))
            ),
            "c_t0027": (
                sum(1 for r in c_rows if r.raised_malformed_plan_error) / max(1, len(c_rows))
            ),
        },
        "recovery_path_distribution": {
            "b_t0027": _recovery_path_counts(rows=b_rows),
            "c_t0027": _recovery_path_counts(rows=c_rows),
        },
    }
    MCNEMAR_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MCNEMAR_RESULTS_PATH.write_text(json.dumps(mcnemar_payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MCNEMAR_RESULTS_PATH}")

    ece_b = _ece_for_variant(rows=b_rows)
    ece_c = _ece_for_variant(rows=c_rows)
    calibration_payload = {
        "spec_version": "1",
        "method": "10-equal-width-bin Expected Calibration Error (Xiong2024 §3.2)",
        "n_bins": 10,
        "variants": {
            "b_t0027": _ece_to_jsonable(result=ece_b),
            "c_t0027": _ece_to_jsonable(result=ece_c),
            "a_t0026": {
                "note": "calibration not computed for variant A: scope-aware ReAct does not "
                "elicit a verbalised final_confidence; final_confidence is null for all rows."
            },
        },
    }
    CALIBRATION_PATH.write_text(json.dumps(calibration_payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {CALIBRATION_PATH}")

    metrics_payload = {
        "variants": [
            {
                "variant_id": "abc-rerun-a-reused",
                "label": "A — scope-aware ReAct (reused from t0026)",
                "dimensions": {
                    "variant": "a",
                    "scaffold": "scope_aware_react",
                    "model": "claude-sonnet-4-6",
                    "n_paired": len(a_rows),
                    "task_id_origin": "t0026_phase2_abc_runtime_n147_for_rq1_rq5",
                },
                "metrics": {
                    "task_success_rate": _success_rate(rows=a_rows),
                    "avg_decisions_per_task": None,
                },
            },
            {
                "variant_id": "abc-rerun-b",
                "label": "B — plan_and_solve_v3 with bounded plan-recovery chain",
                "dimensions": {
                    "variant": "b",
                    "scaffold": "plan_and_solve_v3",
                    "model": "claude-sonnet-4-6",
                    "n_paired": len(b_rows),
                },
                "metrics": {
                    "task_success_rate": _success_rate(rows=b_rows),
                    "overconfident_error_rate": _overconfident_error_rate(rows=b_rows),
                    "avg_decisions_per_task": None,
                },
            },
            {
                "variant_id": "abc-rerun-c",
                "label": "C — matched_mismatch_v2 over plan_and_solve_v3 (adversarial)",
                "dimensions": {
                    "variant": "c",
                    "scaffold": "matched_mismatch_v2_adversarial_over_plan_and_solve_v3",
                    "model": "claude-sonnet-4-6",
                    "n_paired": len(c_rows),
                },
                "metrics": {
                    "task_success_rate": _success_rate(rows=c_rows),
                    "overconfident_error_rate": _overconfident_error_rate(rows=c_rows),
                    "avg_decisions_per_task": None,
                },
            },
        ],
    }
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics_payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {METRICS_PATH}")
    return 0


def _recovery_path_counts(*, rows: list[_PredictionRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.plan_parser_recovery_path] = counts.get(r.plan_parser_recovery_path, 0) + 1
    return counts


if __name__ == "__main__":
    sys.exit(main())
