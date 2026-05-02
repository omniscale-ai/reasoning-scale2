"""Full N=147 × 3-variant sweep with resumable trajectories, judges, and asset writers."""

from __future__ import annotations

import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.anthropic_shim import (
    CostTracker,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.calibration import (
    compute_ece_10bin,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.instance_loader import Instance
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.judge import (
    JudgeResult,
    Prediction,
    judge_outcome,
    prediction_to_dict,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.mcnemar import pairwise_mcnemar
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.metrics import (
    JudgePerInstance,
    compute_all_metrics,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    ASSETS_PREDICTIONS_DIR,
    JUDGE_MODEL_INTER,
    JUDGE_MODEL_PRIMARY,
    JUDGES_DIR,
    MODEL_UNDER_TEST,
    PREDICTIONS_A_DIR,
    PREDICTIONS_B_DIR,
    PREDICTIONS_C_DIR,
    RUNS_DIR,
    SEED,
    SUBSETS,
    TASK_ID,
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
    VARIANTS,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.runner import (
    VariantId,
    run_variant,
)

INTER_JUDGE_SAMPLE_PER_VARIANT: int = 30
_JUDGE_MAX_WORKERS: int = 8


@dataclass(frozen=True, slots=True)
class FullSweepResult:
    predictions_by_variant: dict[str, list[Prediction]]
    judge_results: dict[str, dict[str, JudgePerInstance]]
    manifest: list[Instance]
    metrics: dict[str, Any]
    total_cost_usd: float


def _load_prediction_from_trajectory(*, traj_path: Path, variant: str) -> Prediction | None:
    if not traj_path.exists():
        return None
    try:
        record = json.loads(traj_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(record, dict):
        return None
    return Prediction(
        instance_id=str(record.get("instance_id", "")),
        subset=str(record.get("subset", "")),
        variant=variant,
        final_answer=record.get("final_answer"),
        final_confidence=record.get("final_confidence"),
        cost_usd=float(record.get("cost_usd", 0.0)),
        trajectory_path=str(traj_path),
    )


def _filter_pending_instances(
    *, instances: list[Instance], variant_dir: Path
) -> tuple[list[Instance], list[Prediction]]:
    pending: list[Instance] = []
    existing: list[Prediction] = []
    for inst in instances:
        traj_path = variant_dir / f"trajectory_{inst.instance_id}.json"
        loaded = _load_prediction_from_trajectory(traj_path=traj_path, variant="")
        if loaded is None:
            pending.append(inst)
        else:
            existing.append(loaded)
    return pending, existing


def _run_variant_resumable(
    *,
    variant: VariantId,
    instances: list[Instance],
    cost_tracker: CostTracker,
    model_id: str,
    output_dir: Path,
    max_turns: int,
    max_workers: int,
) -> list[Prediction]:
    variant_dir = output_dir / variant
    variant_dir.mkdir(parents=True, exist_ok=True)
    pending, existing = _filter_pending_instances(instances=instances, variant_dir=variant_dir)
    print(
        f"  variant {variant}: {len(existing)} pre-existing, {len(pending)} to run "
        f"(of {len(instances)} total)"
    )
    if len(pending) > 0:
        summary = run_variant(
            variant=variant,
            instances=pending,
            cost_tracker=cost_tracker,
            model_id=model_id,
            output_dir=output_dir,
            max_turns=max_turns,
            max_workers=max_workers,
        )
        new_predictions = summary.predictions
    else:
        new_predictions = []
    by_iid: dict[str, Prediction] = {}
    for pred in existing:
        by_iid[pred.instance_id] = Prediction(
            instance_id=pred.instance_id,
            subset=pred.subset,
            variant=variant,
            final_answer=pred.final_answer,
            final_confidence=pred.final_confidence,
            cost_usd=pred.cost_usd,
            trajectory_path=pred.trajectory_path,
        )
    for pred in new_predictions:
        by_iid[pred.instance_id] = pred
    ordered: list[Prediction] = []
    for inst in instances:
        if inst.instance_id in by_iid:
            ordered.append(by_iid[inst.instance_id])
    return ordered


def run_full_sweep(
    *,
    instances: list[Instance],
    cost_tracker: CostTracker,
    model_id: str,
    output_dir: Path,
    max_turns: int = 10,
    max_workers: int = 8,
) -> dict[str, list[Prediction]]:
    out: dict[str, list[Prediction]] = {}
    for variant in VARIANTS:
        variant_id: VariantId = variant  # type: ignore[assignment]
        started = time.monotonic()
        preds = _run_variant_resumable(
            variant=variant_id,
            instances=instances,
            cost_tracker=cost_tracker,
            model_id=model_id,
            output_dir=output_dir,
            max_turns=max_turns,
            max_workers=max_workers,
        )
        elapsed = time.monotonic() - started
        cost_so_far = float(cost_tracker.snapshot()["cost_usd"])
        print(
            f"  variant {variant} complete: {len(preds)} predictions, "
            f"elapsed {elapsed:.1f}s, cost so far ${cost_so_far:.4f}"
        )
        out[variant] = preds
    return out


def _judge_dump_path(*, variant: str, role: str) -> Path:
    JUDGES_DIR.mkdir(parents=True, exist_ok=True)
    return JUDGES_DIR / f"{role}_{variant}.json"


def _load_judge_dump(*, path: Path) -> dict[str, JudgeResult]:
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw, dict):
        return {}
    out: dict[str, JudgeResult] = {}
    for iid, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        out[iid] = JudgeResult(
            success=bool(payload.get("success", False)),
            rationale=str(payload.get("rationale", "")),
            raw_response=str(payload.get("raw_response", "")),
        )
    return out


def _save_judge_dump(*, path: Path, dump: dict[str, JudgeResult]) -> None:
    payload = {
        iid: {
            "success": jr.success,
            "rationale": jr.rationale,
            "raw_response": jr.raw_response[:2000],
        }
        for iid, jr in dump.items()
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _judge_variant(
    *,
    variant: str,
    predictions: list[Prediction],
    instances_by_id: dict[str, Instance],
    cost_tracker: CostTracker,
    model_id: str,
    role: str,
    sample_iids: set[str] | None = None,
) -> dict[str, JudgeResult]:
    dump_path = _judge_dump_path(variant=variant, role=role)
    cached = _load_judge_dump(path=dump_path)
    out: dict[str, JudgeResult] = dict(cached)
    todo: list[Prediction] = []
    for pred in predictions:
        if sample_iids is not None and pred.instance_id not in sample_iids:
            continue
        if pred.instance_id in cached:
            continue
        todo.append(pred)
    print(f"  judge {role}/{variant}: {len(cached)} cached, {len(todo)} new (model={model_id})")

    def _one(pred: Prediction) -> tuple[str, JudgeResult] | None:
        instance = instances_by_id.get(pred.instance_id)
        if instance is None:
            return None
        try:
            jr = judge_outcome(
                instance=instance,
                prediction=pred,
                cost_tracker=cost_tracker,
                model_id=model_id,
            )
        except Exception as exc:  # noqa: BLE001
            jr = JudgeResult(
                success=False,
                rationale=f"judge call failed: {type(exc).__name__}: {exc!s}"[:300],
                raw_response="",
            )
        return pred.instance_id, jr

    save_lock = threading.Lock()
    workers = max(1, min(_JUDGE_MAX_WORKERS, len(todo)))
    if workers <= 1 or len(todo) <= 1:
        for i, pred in enumerate(todo, start=1):
            result = _one(pred)
            if result is not None:
                iid, jr = result
                out[iid] = jr
            if i % 10 == 0 or i == len(todo):
                _save_judge_dump(path=dump_path, dump=out)
                cost_so_far = cost_tracker.snapshot()["cost_usd"]
                print(f"    {role}/{variant} {i}/{len(todo)} done, cost so far ${cost_so_far:.4f}")
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(_one, pred) for pred in todo]
            for i, future in enumerate(as_completed(futures), start=1):
                try:
                    result = future.result()
                except Exception as exc:  # noqa: BLE001
                    print(f"    judge worker raised: {type(exc).__name__}: {exc!s}"[:200])
                    continue
                if result is None:
                    continue
                iid, jr = result
                with save_lock:
                    out[iid] = jr
                    if i % 10 == 0 or i == len(todo):
                        _save_judge_dump(path=dump_path, dump=out)
                        cost_so_far = cost_tracker.snapshot()["cost_usd"]
                        print(
                            f"    {role}/{variant} {i}/{len(todo)} done, "
                            f"cost so far ${cost_so_far:.4f}"
                        )
    _save_judge_dump(path=dump_path, dump=out)
    return out


def _select_inter_judge_sample(
    *,
    predictions: list[Prediction],
    n: int,
    seed: int,
) -> set[str]:
    if len(predictions) <= n:
        return {p.instance_id for p in predictions}
    rng = random.Random(seed)
    pool = sorted(predictions, key=lambda p: p.instance_id)
    sampled = rng.sample(pool, n)
    return {p.instance_id for p in sampled}


def judge_full_sweep(
    *,
    predictions_by_variant: dict[str, list[Prediction]],
    instances_by_id: dict[str, Instance],
    cost_tracker: CostTracker,
    inter_per_variant: int = INTER_JUDGE_SAMPLE_PER_VARIANT,
) -> dict[str, dict[str, JudgePerInstance]]:
    judge_results: dict[str, dict[str, JudgePerInstance]] = {}
    for variant in VARIANTS:
        preds = predictions_by_variant.get(variant, [])
        sonnet = _judge_variant(
            variant=variant,
            predictions=preds,
            instances_by_id=instances_by_id,
            cost_tracker=cost_tracker,
            model_id=JUDGE_MODEL_PRIMARY,
            role="sonnet",
            sample_iids=None,
        )
        sample = _select_inter_judge_sample(
            predictions=preds, n=inter_per_variant, seed=SEED + ord(variant[0])
        )
        opus = _judge_variant(
            variant=variant,
            predictions=preds,
            instances_by_id=instances_by_id,
            cost_tracker=cost_tracker,
            model_id=JUDGE_MODEL_INTER,
            role="opus",
            sample_iids=sample,
        )
        per_iid: dict[str, JudgePerInstance] = {}
        for pred in preds:
            sj = sonnet.get(pred.instance_id)
            if sj is None:
                sj = JudgeResult(
                    success=False,
                    rationale="sonnet judge missing",
                    raw_response="",
                )
            oj = opus.get(pred.instance_id)
            per_iid[pred.instance_id] = JudgePerInstance(sonnet=sj, opus=oj)
        judge_results[variant] = per_iid
    return judge_results


def _summarize_predictions_metrics(
    *, predictions: list[Prediction], judge_per_iid: dict[str, JudgePerInstance]
) -> dict[str, Any]:
    n = len(predictions)
    n_success = sum(
        1
        for p in predictions
        if judge_per_iid.get(p.instance_id) is not None
        and judge_per_iid[p.instance_id].sonnet.success
    )
    by_subset: dict[str, dict[str, int]] = {}
    for p in predictions:
        bucket = by_subset.setdefault(p.subset, {"n": 0, "n_success": 0})
        bucket["n"] += 1
        jpi = judge_per_iid.get(p.instance_id)
        if jpi is not None and jpi.sonnet.success:
            bucket["n_success"] += 1
    total_cost = sum(p.cost_usd for p in predictions)
    return {
        "n_instances": n,
        "n_success": n_success,
        "success_rate": (n_success / n) if n > 0 else None,
        "total_cost_usd": total_cost,
        "cost_per_item_usd": (total_cost / n) if n > 0 else None,
        "per_subset": by_subset,
    }


_VARIANT_DIR_BY_ID: dict[str, Path] = {
    VARIANT_A: PREDICTIONS_A_DIR,
    VARIANT_B: PREDICTIONS_B_DIR,
    VARIANT_C: PREDICTIONS_C_DIR,
}

_VARIANT_NAME_BY_ID: dict[str, str] = {
    VARIANT_A: "Variant A: Scope-Aware ReAct (atomic granularity)",
    VARIANT_B: "Variant B: Plan-and-Solve v2 with final_confidence",
    VARIANT_C: "Variant C: Mismatched (atomic granularity, adversarial annotation)",
}

_VARIANT_DESC_BY_ID: dict[str, str] = {
    VARIANT_A: (
        "Scope-Aware ReAct agent operating at atomic granularity over a paired "
        "N=147 instance manifest spanning SWE-bench Verified, Tau-bench, and "
        "FrontierScience Olympiad."
    ),
    VARIANT_B: (
        "Plan-and-Solve v2 agent emitting a final_confidence in [0,1] alongside "
        "final_answer, evaluated on the same paired N=147 manifest."
    ),
    VARIANT_C: (
        "Matched-Mismatch agent fed an intentionally adversarial synthetic "
        "annotation, evaluated on the same paired N=147 manifest as the negative "
        "control for RQ5 strict ordering."
    ),
}


def write_predictions_assets(
    *,
    predictions_by_variant: dict[str, list[Prediction]],
    judge_results: dict[str, dict[str, JudgePerInstance]],
    today_iso: str,
) -> None:
    ASSETS_PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
    for variant in VARIANTS:
        preds = predictions_by_variant.get(variant, [])
        per_iid = judge_results.get(variant, {})
        target_dir = _VARIANT_DIR_BY_ID[variant]
        files_dir = target_dir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        jsonl_name = f"predictions_variant_{variant}.jsonl"
        jsonl_path = files_dir / jsonl_name
        with jsonl_path.open("w", encoding="utf-8") as f:
            for pred in preds:
                jpi = per_iid.get(pred.instance_id)
                row: dict[str, Any] = prediction_to_dict(pred)
                if jpi is not None:
                    row["judge_sonnet_success"] = jpi.sonnet.success
                    row["judge_sonnet_rationale"] = jpi.sonnet.rationale
                    row["judge_opus_success"] = jpi.opus.success if jpi.opus is not None else None
                    row["judge_opus_rationale"] = (
                        jpi.opus.rationale if jpi.opus is not None else None
                    )
                f.write(json.dumps(row) + "\n")

        slug = target_dir.name
        summary = _summarize_predictions_metrics(predictions=preds, judge_per_iid=per_iid)
        details: dict[str, Any] = {
            "spec_version": "2",
            "predictions_id": slug,
            "name": _VARIANT_NAME_BY_ID[variant],
            "short_description": _VARIANT_DESC_BY_ID[variant],
            "description_path": "description.md",
            "model_id": None,
            "model_description": (
                f"{MODEL_UNDER_TEST} via Anthropic API (CLI transport). "
                f"max_turns=10, max_tokens=4096."
            ),
            "dataset_ids": [
                "swebench-verified-subset",
                "taubench-subset",
                "frontierscience-olympiad-subset",
            ],
            "prediction_format": "jsonl",
            "prediction_schema": (
                "Each line is a JSON object with fields: instance_id (str), "
                "subset (str), variant (str), final_answer (str|null), "
                "final_confidence (float|null), cost_usd (float), trajectory_path "
                "(str|null), judge_sonnet_success (bool), judge_sonnet_rationale "
                "(str), judge_opus_success (bool|null), judge_opus_rationale "
                "(str|null)."
            ),
            "instance_count": len(preds),
            "metrics_at_creation": {
                "success_rate_judge_sonnet": summary["success_rate"],
                "n_success": summary["n_success"],
                "n_instances": summary["n_instances"],
                "total_cost_usd": summary["total_cost_usd"],
            },
            "files": [
                {
                    "path": f"files/{jsonl_name}",
                    "description": (
                        f"Per-instance predictions for variant {variant} on the "
                        f"paired N=147 manifest (SWE+Tau+FS) with sonnet and opus "
                        f"judge verdicts attached."
                    ),
                    "format": "jsonl",
                }
            ],
            "categories": [
                "agent-evaluation",
                "llm-as-judge",
            ],
            "created_by_task": TASK_ID,
            "date_created": today_iso,
        }
        details_path = target_dir / "details.json"
        details_path.write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")

        description_md = _build_description_md(
            variant=variant,
            slug=slug,
            today_iso=today_iso,
            summary=summary,
            n_inter_judge=sum(1 for jpi in per_iid.values() if jpi.opus is not None),
        )
        (target_dir / "description.md").write_text(description_md, encoding="utf-8")


def _build_description_md(
    *,
    variant: str,
    slug: str,
    today_iso: str,
    summary: dict[str, Any],
    n_inter_judge: int,
) -> str:
    sr = summary["success_rate"]
    sr_str = f"{sr:.4f}" if sr is not None else "n/a"
    cpi = summary["cost_per_item_usd"]
    cpi_str = f"${cpi:.4f}" if cpi is not None else "n/a"
    per_subset_lines: list[str] = []
    for subset in SUBSETS:
        bucket = summary["per_subset"].get(subset, {"n": 0, "n_success": 0})
        n = bucket["n"]
        ns = bucket["n_success"]
        rate = (ns / n) if n > 0 else None
        rate_str = f"{rate:.4f}" if rate is not None else "n/a"
        per_subset_lines.append(f"* {subset}: n={n}, n_success={ns}, success_rate={rate_str}")
    per_subset_block = "\n".join(per_subset_lines)
    return (
        f"---\n"
        f'spec_version: "2"\n'
        f'predictions_id: "{slug}"\n'
        f'documented_by_task: "{TASK_ID}"\n'
        f'date_documented: "{today_iso}"\n'
        f"---\n\n"
        f"# {_VARIANT_NAME_BY_ID[variant]}\n\n"
        f"## Metadata\n\n"
        f"* **Variant**: {variant}\n"
        f"* **Model**: {MODEL_UNDER_TEST}\n"
        f"* **Datasets**: swebench-verified-subset, taubench-subset, "
        f"frontierscience-olympiad-subset\n"
        f"* **Format**: jsonl\n"
        f"* **Instances**: {summary['n_instances']}\n"
        f"* **Created by**: {TASK_ID}\n\n"
        f"## Overview\n\n"
        f"{_VARIANT_DESC_BY_ID[variant]} Each prediction includes the agent's "
        f"final answer, the trajectory path, the per-instance cost, and primary "
        f"sonnet judge verdicts. A subset of {n_inter_judge} instances also "
        f"carries an opus inter-judge verdict for inter-rater agreement.\n\n"
        f"## Model\n\n"
        f"{MODEL_UNDER_TEST} accessed via the Anthropic CLI transport. The "
        f"agent runs use a 10-turn cap with 4096 max output tokens per call.\n\n"
        f"## Data\n\n"
        f"The paired N=147 manifest spans 20 SWE-bench Verified instances "
        f"(stratified by difficulty bucket), 87 Tau-bench instances "
        f"(deterministic by domain+task_index), and 40 FrontierScience "
        f"Olympiad instances (deterministic by task_id). The manifest "
        f"`data/instance_manifest.json` records the exact instance IDs and "
        f"source SHA-256 hashes per subset.\n\n"
        f"## Prediction Format\n\n"
        f"JSON Lines. Each row has: instance_id, subset, variant, "
        f"final_answer (nullable), final_confidence (nullable; only "
        f"populated for variant B), cost_usd, trajectory_path, "
        f"judge_sonnet_success, judge_sonnet_rationale, judge_opus_success "
        f"(nullable; non-null only for the inter-judge sample), "
        f"judge_opus_rationale (nullable).\n\n"
        f"## Metrics\n\n"
        f"* Success rate (sonnet judge, all subsets): **{sr_str}**\n"
        f"* Cost per instance: **{cpi_str}**\n\n"
        f"Per-subset breakdown:\n\n"
        f"{per_subset_block}\n\n"
        f"## Main Ideas\n\n"
        f"* These predictions provide the runtime evidence base for RQ1-RQ5 "
        f"in t0026 — calibration (RQ1-RQ2), judge agreement (RQ3-RQ4), and "
        f"strict A>B>C ordering (RQ5) are all computed from these JSONL files.\n"
        f"* Judge verdicts attached inline avoid recomputing judge calls "
        f"across downstream tasks; opus inter-judge subset enables "
        f"inter-rater agreement without a full opus pass.\n"
        f"* Empty or null final_answer entries are recorded honestly and "
        f"judged as FAIL by the substantive prompt; downstream analyses can "
        f"treat them as legitimate failures rather than missing data.\n\n"
        f"## Summary\n\n"
        f"This predictions asset captures variant {variant} runs across the "
        f"paired N=147 manifest under the {MODEL_UNDER_TEST} model. The "
        f"trajectory files in `data/runs/{variant}/` contain the full "
        f"action history; the JSONL here is the analysis-ready summary "
        f"with judge verdicts joined inline. Together with `assets/"
        f"predictions/{{a-scope-aware,b-plan-and-solve,c-mismatched}}` for "
        f"the other two variants, this asset supplies the full dataset "
        f"used in `results/metrics.json` and the per-research-question "
        f"comparisons reported in `results/results_detailed.md`.\n"
    )


def write_metric_outputs(
    *,
    predictions_by_variant: dict[str, list[Prediction]],
    judge_results: dict[str, dict[str, JudgePerInstance]],
    manifest: list[Instance],
    output_dir_data: Path,
    output_dir_results: Path,
) -> dict[str, Any]:
    metrics = compute_all_metrics(
        predictions_by_variant=predictions_by_variant,
        judge_results=judge_results,
        manifest=manifest,
    )

    confs: list[float] = []
    outs: list[bool] = []
    if VARIANT_B in predictions_by_variant:
        per_iid_b = judge_results.get(VARIANT_B, {})
        for pred in predictions_by_variant[VARIANT_B]:
            if pred.final_confidence is None:
                continue
            jpi = per_iid_b.get(pred.instance_id)
            if jpi is None:
                continue
            confs.append(pred.final_confidence)
            outs.append(jpi.sonnet.success)
    if len(confs) > 0:
        ece_result = compute_ece_10bin(confidences=confs, outcomes=outs)
        calibration_payload: dict[str, Any] = {
            "ece": ece_result.ece,
            "n_total": ece_result.n_total,
            "bins": [
                {
                    "bin_index": b.bin_index,
                    "lower": b.lower,
                    "upper": b.upper,
                    "n": b.n,
                    "mean_confidence": b.mean_confidence,
                    "mean_outcome": b.mean_outcome,
                    "abs_gap": b.abs_gap,
                }
                for b in ece_result.bins
            ],
        }
    else:
        calibration_payload = {
            "ece": None,
            "n_total": 0,
            "bins": [],
        }
    output_dir_data.mkdir(parents=True, exist_ok=True)
    (output_dir_data / "calibration.json").write_text(
        json.dumps(calibration_payload, indent=2) + "\n", encoding="utf-8"
    )

    mcnemar_payload: dict[str, Any] = {
        "alpha_bonferroni": 0.025,
        "a_vs_b": metrics.get("mcnemar_a_vs_b_detail"),
        "b_vs_c": metrics.get("mcnemar_b_vs_c_detail"),
        "p_a_vs_b": metrics.get("mcnemar_p_a_vs_b"),
        "p_b_vs_c": metrics.get("mcnemar_p_b_vs_c"),
        "rq5_strict_inequality_supported": metrics.get("rq5_strict_inequality_supported"),
    }
    (output_dir_data / "mcnemar_results.json").write_text(
        json.dumps(mcnemar_payload, indent=2) + "\n", encoding="utf-8"
    )

    judge_agreement_payload: dict[str, Any] = {
        "judge_agreement_with_program": metrics.get("judge_agreement_with_program"),
        "judge_agreement_with_program_n": metrics.get("judge_agreement_with_program_n"),
        "inter_judge_agreement": metrics.get("inter_judge_agreement"),
        "inter_judge_agreement_n": metrics.get("inter_judge_agreement_n"),
    }
    (output_dir_data / "judge_agreement.json").write_text(
        json.dumps(judge_agreement_payload, indent=2) + "\n", encoding="utf-8"
    )

    output_dir_results.mkdir(parents=True, exist_ok=True)
    metrics_for_results: dict[str, Any] = dict(metrics)
    metrics_for_results.pop("mcnemar_a_vs_b_detail", None)
    metrics_for_results.pop("mcnemar_b_vs_c_detail", None)
    (output_dir_results / "metrics.json").write_text(
        json.dumps(metrics_for_results, indent=2) + "\n", encoding="utf-8"
    )

    return metrics


def execute_full_sweep(
    *,
    instances: list[Instance],
    cost_tracker: CostTracker,
    today_iso: str,
    max_turns: int = 10,
    hard_cap_usd: float,
    max_workers: int = 8,
) -> FullSweepResult:
    instances_by_id = {inst.instance_id: inst for inst in instances}

    def cost_snapshot() -> float:
        return float(cost_tracker.snapshot()["cost_usd"])

    print("--- running full sweep ---")
    predictions_by_variant = run_full_sweep(
        instances=instances,
        cost_tracker=cost_tracker,
        model_id=MODEL_UNDER_TEST,
        output_dir=RUNS_DIR,
        max_turns=max_turns,
        max_workers=max_workers,
    )
    cost_after_runs = cost_snapshot()
    print(f"runs cost: ${cost_after_runs:.4f}")
    if cost_after_runs >= hard_cap_usd:
        raise RuntimeError(
            f"runs phase exceeded hard cap before judging: "
            f"${cost_after_runs:.2f} >= ${hard_cap_usd:.2f}"
        )

    print("--- judging ---")
    judge_results = judge_full_sweep(
        predictions_by_variant=predictions_by_variant,
        instances_by_id=instances_by_id,
        cost_tracker=cost_tracker,
    )
    cost_after_judges = cost_snapshot()
    print(f"judges cost: ${cost_after_judges:.4f}")

    print("--- writing predictions assets ---")
    write_predictions_assets(
        predictions_by_variant=predictions_by_variant,
        judge_results=judge_results,
        today_iso=today_iso,
    )

    print("--- computing and writing metric outputs ---")
    from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
        DATA_DIR,
        RESULTS_DIR,
    )

    metrics = write_metric_outputs(
        predictions_by_variant=predictions_by_variant,
        judge_results=judge_results,
        manifest=instances,
        output_dir_data=DATA_DIR,
        output_dir_results=RESULTS_DIR,
    )
    total_cost = cost_snapshot()
    return FullSweepResult(
        predictions_by_variant=predictions_by_variant,
        judge_results=judge_results,
        manifest=instances,
        metrics=metrics,
        total_cost_usd=total_cost,
    )


__all__ = [
    "FullSweepResult",
    "execute_full_sweep",
    "run_full_sweep",
    "judge_full_sweep",
    "write_predictions_assets",
    "write_metric_outputs",
]


_ = pairwise_mcnemar  # silence unused-import lint; kept for re-export consistency
