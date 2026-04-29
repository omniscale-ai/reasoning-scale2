from __future__ import annotations

from collections import defaultdict
from typing import Any


def compute_metrics(probes: list[dict]) -> dict[str, Any]:
    """
    Compute all experiment metrics from probe dicts (loaded from JSONL).

    Returns nested dict: metrics[model_id][context_mode][subject] -> metric values.
    Top-level keys also include "all" for aggregate.
    """
    by_model: dict[str, list[dict]] = defaultdict(list)
    for p in probes:
        by_model[p.get("model_id", "")].append(p)

    results: dict[str, Any] = {}
    for model_id, model_probes in by_model.items():
        results[model_id] = {}
        results[model_id]["all"] = _compute_group(model_probes)

        # Per context_mode
        for ctx in ["full", "stripped"]:
            ctx_probes = [p for p in model_probes if p.get("context_mode", "full") == ctx]
            if ctx_probes:
                results[model_id][ctx] = _compute_group(ctx_probes)

        # bypass_effect: how much does stripping context raise GDR?
        full_gdr = results[model_id].get("full", {}).get("gdr")
        strip_gdr = results[model_id].get("stripped", {}).get("gdr")
        if full_gdr is not None and strip_gdr is not None:
            results[model_id]["bypass_effect"] = strip_gdr - full_gdr

        # Per subject
        for subj in set(p.get("subject", "") for p in model_probes):
            if not subj:
                continue
            subj_probes = [p for p in model_probes if p.get("subject") == subj]
            for ctx in ["full", "stripped"]:
                ctx_subj = [p for p in subj_probes if p.get("context_mode", "full") == ctx]
                if ctx_subj:
                    results[model_id].setdefault(subj, {})[ctx] = _compute_group(ctx_subj)

    return results


def _compute_group(probes: list[dict]) -> dict[str, Any]:
    if not probes:
        return {}

    misleading = [p for p in probes if p.get("simulation_mode") == "misleading"]
    honest = [p for p in probes if p.get("simulation_mode") == "honest"]

    gdr = _rate(misleading, lambda p: not p.get("sufficient", True))
    far = _rate(honest, lambda p: not p.get("sufficient", True))
    cal = (gdr - far) if (gdr is not None and far is not None) else None

    gap_recall = _gap_description_recall(misleading)
    conf_miscal = _confidence_miscalibration_rate(misleading)
    parse_ok = sum(1 for p in probes if p.get("parse_success", False)) / len(probes)

    return {
        "n": len(probes),
        "n_misleading": len(misleading),
        "n_honest": len(honest),
        "gdr": gdr,
        "far": far,
        "cal": cal,
        "gap_recall": gap_recall,
        "conf_miscal": conf_miscal,
        "parse_success_rate": parse_ok,
    }


def _rate(probes: list[dict], condition) -> float | None:
    if not probes:
        return None
    return sum(1 for p in probes if condition(p)) / len(probes)


def _gap_description_recall(misleading_probes: list[dict]) -> float | None:
    scores = []
    for p in misleading_probes:
        if not p.get("sufficient", True):
            omitted: list[str] = []
            for sr in p.get("simulated_results", []):
                omitted.extend(sr.get("deliberately_omitted", []))
            missing = [s.lower() for s in p.get("missing_information", [])]
            if not omitted:
                continue
            hits = sum(
                1
                for item in omitted
                if any(item.lower() in m or m in item.lower() for m in missing)
            )
            scores.append(hits / len(omitted))
    return sum(scores) / len(scores) if scores else None


def _confidence_miscalibration_rate(misleading_probes: list[dict]) -> float | None:
    if not misleading_probes:
        return None
    dangerous = sum(
        1
        for p in misleading_probes
        if p.get("sufficient", False) and p.get("confidence", "") == "high"
    )
    return dangerous / len(misleading_probes)


def print_summary(metrics: dict) -> None:
    """Print a summary table including bypass_effect."""
    print(
        f"\n{'Model':<30} {'ctx':>8} {'n':>4} {'GDR':>6} {'FAR':>6} {'CAL':>6} {'ConfMisCal':>11}"
    )
    print("-" * 75)
    for model_id, model_data in metrics.items():
        bypass = model_data.get("bypass_effect")
        for ctx in ["full", "stripped", "all"]:
            d = model_data.get(ctx, {})
            if not d:
                continue
            n = d.get("n", 0)
            gdr = f"{d['gdr']:.3f}" if d.get("gdr") is not None else "  N/A"
            far = f"{d['far']:.3f}" if d.get("far") is not None else "  N/A"
            cal = f"{d['cal']:.3f}" if d.get("cal") is not None else "  N/A"
            cmc = f"{d['conf_miscal']:.3f}" if d.get("conf_miscal") is not None else "        N/A"
            label = f"{model_id[:28]}"
            print(f"{label:<30} {ctx:>8} {n:>4} {gdr:>6} {far:>6} {cal:>6} {cmc:>11}")
        if bypass is not None:
            print(f"  → bypass_effect (GDR_stripped − GDR_full) = {bypass:+.3f}")
        print()
