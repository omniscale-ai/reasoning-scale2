"""Orchestrates RQ1-RQ5 metric computation across the three variants and three subsets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.calibration import (
    compute_ece_10bin,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.instance_loader import Instance
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.judge import (
    JudgeResult,
    Prediction,
    compute_program_truth,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.mcnemar import pairwise_mcnemar
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    SUBSET_FRONTSCI,
    SUBSET_SWEBENCH,
    SUBSET_TAUBENCH,
    SUBSETS,
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
)


@dataclass(frozen=True, slots=True)
class JudgePerInstance:
    sonnet: JudgeResult
    opus: JudgeResult | None


def _success_rate(*, success_list: list[bool]) -> float | None:
    if len(success_list) == 0:
        return None
    return sum(1 for s in success_list if s) / len(success_list)


def _filter_subset(*, predictions: list[Prediction], subset: str) -> list[Prediction]:
    return [p for p in predictions if p.subset == subset]


def compute_all_metrics(
    *,
    predictions_by_variant: dict[str, list[Prediction]],
    judge_results: dict[str, dict[str, JudgePerInstance]],
    manifest: list[Instance],
) -> dict[str, Any]:
    instances_by_id: dict[str, Instance] = {inst.instance_id: inst for inst in manifest}
    metrics: dict[str, Any] = {}

    success_judge: dict[str, dict[str, bool]] = {}
    for variant, preds in predictions_by_variant.items():
        per_variant_judge = judge_results.get(variant, {})
        success_judge[variant] = {}
        for pred in preds:
            jr = per_variant_judge.get(pred.instance_id)
            if jr is None:
                success_judge[variant][pred.instance_id] = False
            else:
                success_judge[variant][pred.instance_id] = jr.sonnet.success

    for variant in (VARIANT_A, VARIANT_B, VARIANT_C):
        preds = predictions_by_variant.get(variant, [])
        all_success = [success_judge[variant].get(p.instance_id, False) for p in preds]
        sr = _success_rate(success_list=all_success)
        metrics[f"success_rate_{variant}"] = sr
        for subset in SUBSETS:
            subset_preds = _filter_subset(predictions=preds, subset=subset)
            subset_success = [
                success_judge[variant].get(p.instance_id, False) for p in subset_preds
            ]
            metrics[f"success_rate_{variant}_{subset}"] = _success_rate(success_list=subset_success)

    if VARIANT_B in predictions_by_variant:
        b_preds = predictions_by_variant[VARIANT_B]
        confs: list[float] = []
        outs: list[bool] = []
        for p in b_preds:
            if p.final_confidence is None:
                continue
            confs.append(p.final_confidence)
            outs.append(success_judge[VARIANT_B].get(p.instance_id, False))
        if len(confs) > 0:
            ece_result = compute_ece_10bin(confidences=confs, outcomes=outs)
            metrics["final_confidence_ece"] = ece_result.ece
            metrics["final_confidence_ece_n"] = ece_result.n_total
        else:
            metrics["final_confidence_ece"] = None
            metrics["final_confidence_ece_n"] = 0

    judge_program_agree_n = 0
    judge_program_agree_total = 0
    for variant, preds in predictions_by_variant.items():
        for pred in preds:
            instance = instances_by_id.get(pred.instance_id)
            if instance is None:
                continue
            program_truth = compute_program_truth(instance=instance, prediction=pred)
            if program_truth is None:
                continue
            judge_verdict = success_judge[variant].get(pred.instance_id, False)
            judge_program_agree_total += 1
            if program_truth == judge_verdict:
                judge_program_agree_n += 1
    metrics["judge_agreement_with_program"] = (
        (judge_program_agree_n / judge_program_agree_total)
        if judge_program_agree_total > 0
        else None
    )
    metrics["judge_agreement_with_program_n"] = judge_program_agree_total

    inter_judge_agree_n = 0
    inter_judge_agree_total = 0
    for variant, per_variant_judge in judge_results.items():
        _ = variant
        for _instance_id, jpi in per_variant_judge.items():
            if jpi.opus is None:
                continue
            inter_judge_agree_total += 1
            if jpi.opus.success == jpi.sonnet.success:
                inter_judge_agree_n += 1
    metrics["inter_judge_agreement"] = (
        (inter_judge_agree_n / inter_judge_agree_total) if inter_judge_agree_total > 0 else None
    )
    metrics["inter_judge_agreement_n"] = inter_judge_agree_total

    if VARIANT_A in predictions_by_variant and VARIANT_B in predictions_by_variant:
        ids_a = [p.instance_id for p in predictions_by_variant[VARIANT_A]]
        ids_b_set = {p.instance_id for p in predictions_by_variant[VARIANT_B]}
        common_ab = [i for i in ids_a if i in ids_b_set]
        sa = [success_judge[VARIANT_A][i] for i in common_ab]
        sb = [success_judge[VARIANT_B][i] for i in common_ab]
        ab = pairwise_mcnemar(success_first=sa, success_second=sb)
        metrics["mcnemar_p_a_vs_b"] = ab["p_value"]
        metrics["mcnemar_a_vs_b_detail"] = ab
    if VARIANT_B in predictions_by_variant and VARIANT_C in predictions_by_variant:
        ids_b = [p.instance_id for p in predictions_by_variant[VARIANT_B]]
        ids_c_set = {p.instance_id for p in predictions_by_variant[VARIANT_C]}
        common_bc = [i for i in ids_b if i in ids_c_set]
        sb_bc = [success_judge[VARIANT_B][i] for i in common_bc]
        sc_bc = [success_judge[VARIANT_C][i] for i in common_bc]
        bc = pairwise_mcnemar(success_first=sb_bc, success_second=sc_bc)
        metrics["mcnemar_p_b_vs_c"] = bc["p_value"]
        metrics["mcnemar_b_vs_c_detail"] = bc

    p_ab = metrics.get("mcnemar_p_a_vs_b")
    p_bc = metrics.get("mcnemar_p_b_vs_c")
    sr_a = metrics.get("success_rate_a")
    sr_b = metrics.get("success_rate_b")
    sr_c = metrics.get("success_rate_c")
    rq5: bool | None
    if all(v is not None for v in (p_ab, p_bc, sr_a, sr_b, sr_c)):
        rq5 = bool(
            p_ab < 0.025  # type: ignore[operator]
            and p_bc < 0.025  # type: ignore[operator]
            and sr_a > sr_b  # type: ignore[operator]
            and sr_b > sr_c  # type: ignore[operator]
        )
    else:
        rq5 = None
    metrics["rq5_strict_inequality_supported"] = rq5
    metrics["bonferroni_alpha"] = 0.025

    total_cost = sum(p.cost_usd for preds in predictions_by_variant.values() for p in preds)
    total_n = sum(len(preds) for preds in predictions_by_variant.values())
    metrics["efficiency_inference_cost_per_item_usd"] = (
        (total_cost / total_n) if total_n > 0 else None
    )
    metrics["efficiency_inference_time_per_item_seconds"] = None

    metrics["_meta"] = {
        "subsets": list(SUBSETS),
        "subset_swebench": SUBSET_SWEBENCH,
        "subset_taubench": SUBSET_TAUBENCH,
        "subset_frontsci": SUBSET_FRONTSCI,
    }
    return metrics
