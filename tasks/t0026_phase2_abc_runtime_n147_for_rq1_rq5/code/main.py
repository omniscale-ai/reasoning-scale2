"""Orchestrator entry: t0026 phase-2 A/B/C runtime; --build-manifest --smoke --preflight --full."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import time
from typing import Any

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.anthropic_shim import (
    CostTracker,
    make_model_call,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.full_runner import (
    execute_full_sweep,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.instance_loader import (
    Instance,
    load_instances,
    sample_per_subset,
    write_manifest,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.judge import (
    JudgeResult,
    Prediction,
    judge_outcome,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.paths import (
    COST_REESTIMATE_PATH,
    HARD_BUDGET_CAP_USD,
    INSTANCE_MANIFEST_PATH,
    JUDGE_MODEL_PRIMARY,
    MODEL_UNDER_TEST,
    N_FRONTSCI_TARGET,
    N_SWEBENCH_TARGET,
    N_TAUBENCH_TARGET,
    N_TOTAL_TARGET,
    PREFLIGHT_DIR,
    PREFLIGHT_PER_SUBSET,
    SMOKE_TEST_PATH,
    SUBSETS,
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
    VARIANTS,
)
from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code.runner import VariantId, run_variant


def _build_manifest_command() -> int:
    instances = load_instances()
    write_manifest(instances=instances, output_path=INSTANCE_MANIFEST_PATH)
    print(f"wrote manifest with {len(instances)} instances to {INSTANCE_MANIFEST_PATH}")
    counts: dict[str, int] = {}
    for inst in instances:
        counts[inst.subset] = counts.get(inst.subset, 0) + 1
    print(f"per-subset counts: {counts}")
    return 0


def _smoke_command() -> int:
    cost_tracker = CostTracker()
    call = make_model_call(model_id=MODEL_UNDER_TEST, cost_tracker=cost_tracker, max_tokens=128)
    prompt = "Reply with the single word: ready"
    response = call(prompt)
    snapshot = cost_tracker.snapshot()
    payload = {
        "model_id": MODEL_UNDER_TEST,
        "prompt": prompt,
        "response": response,
        "cost_snapshot": snapshot,
    }
    SMOKE_TEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    SMOKE_TEST_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"smoke test wrote {SMOKE_TEST_PATH}")
    print(f"response: {response[:200]}")
    print(f"cost: ${snapshot['cost_usd']:.6f}, n_calls={snapshot['n_calls']}")
    return 0


def _judge_predictions(
    *,
    predictions: list[Prediction],
    instances_by_id: dict[str, Instance],
    cost_tracker: CostTracker,
) -> dict[str, JudgeResult]:
    results: dict[str, JudgeResult] = {}
    for pred in predictions:
        instance = instances_by_id[pred.instance_id]
        try:
            jr = judge_outcome(
                instance=instance,
                prediction=pred,
                cost_tracker=cost_tracker,
                model_id=JUDGE_MODEL_PRIMARY,
            )
        except Exception as exc:  # noqa: BLE001
            jr = JudgeResult(
                success=False,
                rationale=f"judge call failed: {type(exc).__name__}: {exc!s}"[:300],
                raw_response="",
            )
        results[pred.instance_id] = jr
    return results


def _project_full_run_cost(*, preflight_cost: float) -> float:
    n_runs_preflight = PREFLIGHT_PER_SUBSET * len(SUBSETS) * len(VARIANTS)
    n_judge_calls_preflight = n_runs_preflight
    cost_per_unit = preflight_cost / max(1, n_runs_preflight + n_judge_calls_preflight)
    n_runs_full = N_TOTAL_TARGET * len(VARIANTS)
    n_judge_calls_full = n_runs_full
    n_inter_judge = 30 * len(VARIANTS)
    projected_main = (n_runs_full + n_judge_calls_full) * cost_per_unit
    projected_inter = n_inter_judge * cost_per_unit * (15.0 / 3.0)
    return projected_main + projected_inter


def _preflight_command() -> int:
    instances = load_instances()
    write_manifest(instances=instances, output_path=INSTANCE_MANIFEST_PATH)
    instances_by_id = {inst.instance_id: inst for inst in instances}
    preflight_instances = sample_per_subset(
        instances=instances,
        n_per_subset=PREFLIGHT_PER_SUBSET,
    )
    print(
        f"preflight: {len(preflight_instances)} instances "
        f"(per subset = {PREFLIGHT_PER_SUBSET}); 3 variants -> "
        f"{len(preflight_instances) * len(VARIANTS)} runs + judges"
    )
    cost_tracker = CostTracker()
    PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    summaries: dict[str, Any] = {}
    predictions_by_variant: dict[str, list[Prediction]] = {}
    for variant in VARIANTS:
        print(f"--- variant {variant!r} ---")
        variant_id: VariantId = variant  # type: ignore[assignment]
        summary = run_variant(
            variant=variant_id,
            instances=preflight_instances,
            cost_tracker=cost_tracker,
            model_id=MODEL_UNDER_TEST,
            output_dir=PREFLIGHT_DIR,
            max_turns=8,
            max_tokens=2048,
            max_workers=4,
        )
        summaries[variant] = {
            "n_instances": summary.n_instances,
            "elapsed_seconds": summary.elapsed_seconds,
            "predictions": [
                {
                    "instance_id": p.instance_id,
                    "subset": p.subset,
                    "final_answer_excerpt": (p.final_answer or "")[:200],
                    "final_confidence": p.final_confidence,
                    "cost_usd": p.cost_usd,
                }
                for p in summary.predictions
            ],
        }
        predictions_by_variant[variant] = summary.predictions
        cost_so_far = cost_tracker.snapshot()["cost_usd"]
        print(f"  variant {variant} done: cost so far ${cost_so_far:.4f}")
    print("--- judging preflight predictions ---")
    judge_summaries: dict[str, dict[str, Any]] = {}
    for variant, preds in predictions_by_variant.items():
        verdicts = _judge_predictions(
            predictions=preds,
            instances_by_id=instances_by_id,
            cost_tracker=cost_tracker,
        )
        judge_summaries[variant] = {
            iid: {"success": jr.success, "rationale": jr.rationale[:200]}
            for iid, jr in verdicts.items()
        }
    elapsed = time.monotonic() - started
    snapshot = cost_tracker.snapshot()
    preflight_cost = snapshot["cost_usd"]
    projected_full = _project_full_run_cost(preflight_cost=preflight_cost)
    payload: dict[str, Any] = {
        "preflight_n_instances": len(preflight_instances),
        "preflight_n_per_subset": PREFLIGHT_PER_SUBSET,
        "n_variants": len(VARIANTS),
        "preflight_cost_usd": preflight_cost,
        "preflight_n_calls": snapshot["n_calls"],
        "preflight_parse_failures": snapshot["parse_failures"],
        "preflight_elapsed_seconds": elapsed,
        "projected_full_run_cost_usd": projected_full,
        "hard_budget_cap_usd": HARD_BUDGET_CAP_USD,
        "model_under_test": MODEL_UNDER_TEST,
        "judge_model_primary": JUDGE_MODEL_PRIMARY,
        "n_swebench_target": N_SWEBENCH_TARGET,
        "n_taubench_target": N_TAUBENCH_TARGET,
        "n_frontsci_target": N_FRONTSCI_TARGET,
        "summaries_per_variant": summaries,
        "judge_summaries_per_variant": judge_summaries,
        "fits_within_cap": projected_full <= HARD_BUDGET_CAP_USD,
    }
    COST_REESTIMATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    COST_REESTIMATE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {COST_REESTIMATE_PATH}")
    print(
        f"preflight cost: ${preflight_cost:.4f}, "
        f"projected full run: ${projected_full:.2f}, "
        f"cap: ${HARD_BUDGET_CAP_USD:.2f}"
    )
    if projected_full > HARD_BUDGET_CAP_USD:
        print("PROJECTION EXCEEDS HARD CAP; halting before full sweep.")
        return 2
    return 0


def _full_command() -> int:
    instances = load_instances()
    write_manifest(instances=instances, output_path=INSTANCE_MANIFEST_PATH)
    cost_tracker = CostTracker()
    today_iso = _dt.datetime.now(tz=_dt.UTC).strftime("%Y-%m-%d")
    try:
        result = execute_full_sweep(
            instances=instances,
            cost_tracker=cost_tracker,
            today_iso=today_iso,
            max_turns=10,
            hard_cap_usd=HARD_BUDGET_CAP_USD,
        )
    except RuntimeError as exc:
        print(f"FULL SWEEP HALTED: {exc}")
        return 2
    snapshot = cost_tracker.snapshot()
    print(
        f"full sweep complete: total cost ${result.total_cost_usd:.4f}, "
        f"n_calls={snapshot['n_calls']}, parse_failures={snapshot['parse_failures']}"
    )
    print(
        f"rq5_strict_inequality_supported = {result.metrics.get('rq5_strict_inequality_supported')}"
    )
    return 0


def _make_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="t0026 phase-2 A/B/C runtime orchestrator.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build-manifest", action="store_true")
    group.add_argument("--smoke", action="store_true")
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--full", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _make_arg_parser()
    args = parser.parse_args(argv)
    _ = VARIANT_A, VARIANT_B, VARIANT_C
    if args.build_manifest:
        return _build_manifest_command()
    if args.smoke:
        return _smoke_command()
    if args.preflight:
        return _preflight_command()
    if args.full:
        return _full_command()
    return 1


if __name__ == "__main__":
    sys.exit(main())
