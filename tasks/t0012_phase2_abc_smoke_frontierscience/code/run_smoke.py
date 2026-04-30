"""CLI entrypoint: run the phase2 A/B/C smoke harness on FrontierScience-Olympiad.

Usage:
    uv run python -m arf.scripts.utils.run_with_logs \\
        --task-id t0012_phase2_abc_smoke_frontierscience -- \\
        uv run python -u -m tasks.t0012_phase2_abc_smoke_frontierscience.code.run_smoke \\
        [--limit N] [--budget-cap-usd USD] [--skip-condition {a,b,c}]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from tasks.t0012_phase2_abc_smoke_frontierscience.code.charts import (
    render_condition_metric_bar,
    render_per_row_success_heatmap,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.constants import (
    BUDGET_CAP_USD,
    CONDITION_A_LABEL,
    CONDITION_B_LABEL,
    CONDITION_C_LABEL,
    MODEL_AGENT,
    MODEL_JUDGE,
    VARIANT_A,
    VARIANT_B,
    VARIANT_C,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.harness import (
    RowOutcome,
    compute_metrics,
    extract_final_confidence,
    extract_gold_answer,
    extract_problem_text,
    jsonable_to_outcomes,
    judge_correctness,
    load_smoke_rows,
    metrics_to_dict,
    outcomes_to_jsonable,
    run_condition_a,
    run_condition_b,
    run_condition_c,
    write_predictions_jsonl,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.model_call import (
    CostTracker,
    make_model_call,
    reset_cost_log,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.paths import (
    INTERMEDIATE_A_PATH,
    INTERMEDIATE_B_PATH,
    INTERMEDIATE_C_PATH,
    INTERMEDIATE_STATS_PATH,
    METRICS_PATH,
    PREDICTIONS_A_FILE,
    PREDICTIONS_B_FILE,
    PREDICTIONS_C_FILE,
    RESULTS_DIR,
    RESULTS_IMAGES_DIR,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.stats import (
    confirmatory_n_for_paired_difference,
    mcnemar_paired,
    wilson_interval,
)
from tasks.t0012_phase2_abc_smoke_frontierscience.code.tools import (
    build_planandsolve_tool_registry,
    build_react_tool_registry,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 2 A/B/C smoke harness.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap N rows to process (default: all FrontierScience-Olympiad complete rows).",
    )
    parser.add_argument(
        "--budget-cap-usd",
        type=float,
        default=BUDGET_CAP_USD,
        help=f"Budget cap in USD (default: {BUDGET_CAP_USD}).",
    )
    parser.add_argument(
        "--skip-condition",
        choices=["a", "b", "c"],
        default=None,
        help="Skip a single condition (debug only; not for production runs).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Reuse existing _intermediate_*.json files when present.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = load_smoke_rows()
    if args.limit is not None:
        rows = rows[: args.limit]
    print(f"Loaded {len(rows)} FrontierScience-Olympiad complete rows", flush=True)
    if len(rows) == 0:
        print("No rows to process; exiting.", file=sys.stderr)
        return 1

    tracker = CostTracker(cap_usd=args.budget_cap_usd)
    if not args.resume:
        reset_cost_log()
    agent_call = make_model_call(model=MODEL_AGENT, cost_tracker=tracker, note="agent")
    judge_call = make_model_call(model=MODEL_JUDGE, cost_tracker=tracker, note="judge")

    react_registry = build_react_tool_registry()
    plansolve_registry = build_planandsolve_tool_registry()

    outcomes_a: list[RowOutcome] = _load_intermediate(INTERMEDIATE_A_PATH) if args.resume else []
    outcomes_b: list[RowOutcome] = _load_intermediate(INTERMEDIATE_B_PATH) if args.resume else []
    outcomes_c: list[RowOutcome] = _load_intermediate(INTERMEDIATE_C_PATH) if args.resume else []

    halted = False
    cond_specs: list[tuple[str, str, list[RowOutcome], Path, Path]] = []
    if args.skip_condition != "a":
        cond_specs.append(
            ("A", CONDITION_A_LABEL, outcomes_a, INTERMEDIATE_A_PATH, PREDICTIONS_A_FILE)
        )
    if args.skip_condition != "b":
        cond_specs.append(
            ("B", CONDITION_B_LABEL, outcomes_b, INTERMEDIATE_B_PATH, PREDICTIONS_B_FILE)
        )
    if args.skip_condition != "c":
        cond_specs.append(
            ("C", CONDITION_C_LABEL, outcomes_c, INTERMEDIATE_C_PATH, PREDICTIONS_C_FILE)
        )

    for cond_key, cond_label, outcomes, intermediate_path, _pred_path in cond_specs:
        already = {o.task_id for o in outcomes}
        print(
            f"\n=== Condition {cond_key} ({cond_label}) — already done: {len(already)} ===",
            flush=True,
        )
        for idx, row in enumerate(rows, start=1):
            task_id_obj = row.get("task_id")
            task_id = str(task_id_obj) if isinstance(task_id_obj, str) else f"row{idx}"
            if task_id in already:
                continue
            if not tracker.is_budget_ok(headroom_usd=0.20):
                print(
                    f"  [BUDGET-HALT] tracker total ${tracker.total_usd:.4f} "
                    f"reached cap ${args.budget_cap_usd}",
                    flush=True,
                )
                halted = True
                break
            problem = extract_problem_text(row)
            gold = extract_gold_answer(row)
            t0 = time.monotonic()
            agent_refused = False
            try:
                if cond_key == "A":
                    final, traj = run_condition_a(
                        row=row,
                        model_call=agent_call,
                        react_tool_registry=react_registry,
                    )
                elif cond_key == "B":
                    final, traj = run_condition_b(
                        row=row,
                        model_call=agent_call,
                        plansolve_tool_registry=plansolve_registry,
                    )
                else:
                    final, traj = run_condition_c(
                        row=row,
                        model_call=agent_call,
                        plansolve_tool_registry=plansolve_registry,
                    )
            except Exception as exc:  # noqa: BLE001
                exc_msg = str(exc)
                # Detect content-filter refusals: API rejects with "Usage Policy" or similar.
                refusal_markers = (
                    "Usage Policy",
                    "usage policy",
                    "violates",
                    "I cannot help",
                    "I can't help",
                    "I'm not able to",
                    "content_filter",
                )
                agent_refused = any(m in exc_msg for m in refusal_markers)
                tag = "REFUSED" if agent_refused else "ERRORED"
                print(
                    f"  [{cond_key}] row {idx}/{len(rows)} {task_id} {tag}: "
                    f"{type(exc).__name__}: {exc_msg[:200]}",
                    flush=True,
                )
                final = None
                traj = []
            verdict = judge_correctness(
                task_id=task_id,
                problem=problem,
                gold=gold,
                candidate=final,
                judge_call=judge_call,
            )
            confidence = extract_final_confidence(trajectory=traj)
            outcome = RowOutcome(
                task_id=task_id,
                problem=problem,
                gold_answer=gold,
                final_answer=final,
                is_correct=verdict,
                decision_count=len(traj),
                final_confidence=confidence,
                trajectory=traj,
                agent_refused=agent_refused,
            )
            outcomes.append(outcome)
            elapsed = time.monotonic() - t0
            print(
                f"  [{cond_key}] {idx}/{len(rows)} {task_id} verdict={verdict} "
                f"decisions={len(traj)} conf={confidence} "
                f"final={(final or '<none>')[:60]!r} "
                f"elapsed={elapsed:.1f}s "
                f"running_cost=${tracker.total_usd:.4f}",
                flush=True,
            )
            # Persist intermediate state every row for crash safety.
            _save_intermediate(intermediate_path, outcomes)
        if halted:
            break

    # Compute metrics per condition (using all outcomes collected, even if halted).
    metrics_a = compute_metrics(outcomes=outcomes_a)
    metrics_b = compute_metrics(outcomes=outcomes_b)
    metrics_c = compute_metrics(outcomes=outcomes_c)

    # Persist final predictions JSONL if we have outcomes for that condition.
    if len(outcomes_a) > 0:
        write_predictions_jsonl(
            path=PREDICTIONS_A_FILE,
            condition_label=CONDITION_A_LABEL,
            outcomes=outcomes_a,
        )
    if len(outcomes_b) > 0:
        write_predictions_jsonl(
            path=PREDICTIONS_B_FILE,
            condition_label=CONDITION_B_LABEL,
            outcomes=outcomes_b,
        )
    if len(outcomes_c) > 0:
        write_predictions_jsonl(
            path=PREDICTIONS_C_FILE,
            condition_label=CONDITION_C_LABEL,
            outcomes=outcomes_c,
        )

    # metrics.json (explicit-variant format).
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    metrics_doc: dict[str, Any] = {
        "variants": [
            {
                "variant_id": VARIANT_A,
                "label": CONDITION_A_LABEL,
                "dimensions": {
                    "condition": "A",
                    "agent": "scope_aware_react_v1",
                    "delegate": None,
                    "n": metrics_a.n,
                    "model": MODEL_AGENT,
                },
                "metrics": metrics_to_dict(metrics_a),
            },
            {
                "variant_id": VARIANT_B,
                "label": CONDITION_B_LABEL,
                "dimensions": {
                    "condition": "B",
                    "agent": "scope_unaware_planandsolve_v1",
                    "delegate": None,
                    "n": metrics_b.n,
                    "model": MODEL_AGENT,
                },
                "metrics": metrics_to_dict(metrics_b),
            },
            {
                "variant_id": VARIANT_C,
                "label": CONDITION_C_LABEL,
                "dimensions": {
                    "condition": "C",
                    "agent": "matched_mismatch_v1",
                    "delegate": "scope_unaware_planandsolve",
                    "n": metrics_c.n,
                    "model": MODEL_AGENT,
                },
                "metrics": metrics_to_dict(metrics_c),
            },
        ],
    }
    METRICS_PATH.write_text(json.dumps(metrics_doc, indent=2), encoding="utf-8")

    # Pre-registered hypothesis tests + statistics.
    paired_ids = sorted(
        {o.task_id for o in outcomes_a}
        & {o.task_id for o in outcomes_b}
        & {o.task_id for o in outcomes_c}
    )
    a_by_id = {o.task_id: o for o in outcomes_a}
    b_by_id = {o.task_id: o for o in outcomes_b}
    c_by_id = {o.task_id: o for o in outcomes_c}
    a_correct_paired = [a_by_id[t].is_correct for t in paired_ids]
    b_correct_paired = [b_by_id[t].is_correct for t in paired_ids]
    c_correct_paired = [c_by_id[t].is_correct for t in paired_ids]
    n_paired = len(paired_ids)
    a_b_test = mcnemar_paired(a_correct=a_correct_paired, b_correct=b_correct_paired)
    b_c_test = mcnemar_paired(a_correct=b_correct_paired, b_correct=c_correct_paired)
    a_c_test = mcnemar_paired(a_correct=a_correct_paired, b_correct=c_correct_paired)
    a_succ = sum(1 for x in a_correct_paired if x)
    b_succ = sum(1 for x in b_correct_paired if x)
    c_succ = sum(1 for x in c_correct_paired if x)
    a_ci = wilson_interval(successes=a_succ, n=n_paired)
    b_ci = wilson_interval(successes=b_succ, n=n_paired)
    c_ci = wilson_interval(successes=c_succ, n=n_paired)

    # Confirmatory N for 5pp paired effect, using observed discordant rate as input.
    discord_rate_ab = a_b_test.discordant_pairs / max(n_paired, 1) if n_paired > 0 else 0.0
    confirmatory_n = confirmatory_n_for_paired_difference(
        discordant_rate_estimate=max(discord_rate_ab, 0.05),
        target_effect_pp=5.0,
    )

    stats_doc: dict[str, Any] = {
        "n_paired": n_paired,
        "halted_for_budget": halted,
        "task_ids_paired": paired_ids,
        "metrics": {
            "a": metrics_to_dict(metrics_a) | {"n": metrics_a.n},
            "b": metrics_to_dict(metrics_b) | {"n": metrics_b.n},
            "c": metrics_to_dict(metrics_c) | {"n": metrics_c.n},
        },
        "wilson_ci_task_success": {
            "a": _ci_to_dict(a_ci),
            "b": _ci_to_dict(b_ci),
            "c": _ci_to_dict(c_ci),
        },
        "mcnemar": {
            "a_vs_b": _mcnemar_to_dict(a_b_test),
            "b_vs_c": _mcnemar_to_dict(b_c_test),
            "a_vs_c": _mcnemar_to_dict(a_c_test),
        },
        "deltas_pp": {
            "a_minus_b_task_success": (
                100.0 * (metrics_a.task_success_rate - metrics_b.task_success_rate)
            ),
            "a_minus_b_overconfident": (
                100.0 * (metrics_a.overconfident_error_rate - metrics_b.overconfident_error_rate)
            ),
            "b_minus_c_task_success": (
                100.0 * (metrics_b.task_success_rate - metrics_c.task_success_rate)
            ),
            "a_minus_c_task_success": (
                100.0 * (metrics_a.task_success_rate - metrics_c.task_success_rate)
            ),
        },
        "rq1_pre_registered": {
            "predicted_direction_pp": "+5",
            "observed_pp": 100.0 * (metrics_a.task_success_rate - metrics_b.task_success_rate),
            "p_value_a_b": a_b_test.p_value,
            "confirmed": (
                (metrics_a.task_success_rate - metrics_b.task_success_rate) >= 0.05
                and a_b_test.p_value < 0.10
            ),
            "refuted": (
                (metrics_a.task_success_rate - metrics_b.task_success_rate) < 0.0
                or (
                    (metrics_a.task_success_rate - metrics_b.task_success_rate) >= 0.05
                    and a_b_test.p_value > 0.30
                )
            ),
        },
        "rq2_pre_registered": {
            "predicted_direction_pp": "-2",
            "observed_pp": 100.0
            * (metrics_a.overconfident_error_rate - metrics_b.overconfident_error_rate),
            "confirmed": (
                metrics_a.overconfident_error_rate - metrics_b.overconfident_error_rate <= -0.02
            ),
            "refuted": (
                metrics_a.overconfident_error_rate - metrics_b.overconfident_error_rate > 0.0
            ),
        },
        "rq5_pre_registered": {
            "predicted": "C strictly worst on metric 1 and metric 2",
            "c_lt_min_ab_metric1_pp": (
                100.0
                * (
                    metrics_c.task_success_rate
                    - min(metrics_a.task_success_rate, metrics_b.task_success_rate)
                )
            ),
            "c_gt_max_ab_metric2_pp": (
                100.0
                * (
                    metrics_c.overconfident_error_rate
                    - max(metrics_a.overconfident_error_rate, metrics_b.overconfident_error_rate)
                )
            ),
            "confirmed": (
                metrics_c.task_success_rate
                < min(metrics_a.task_success_rate, metrics_b.task_success_rate)
                and metrics_c.overconfident_error_rate
                > max(metrics_a.overconfident_error_rate, metrics_b.overconfident_error_rate)
            ),
        },
        "confirmatory_n_for_5pp_effect_at_alpha_0.05_power_0.8": confirmatory_n,
        "cost_breakdown": tracker.per_model_breakdown(),
        "total_cost_usd": tracker.total_usd,
        "budget_cap_usd": args.budget_cap_usd,
    }
    INTERMEDIATE_STATS_PATH.write_text(json.dumps(stats_doc, indent=2), encoding="utf-8")

    # Charts.
    metrics_by_condition = {
        "A": metrics_to_dict(metrics_a),
        "B": metrics_to_dict(metrics_b),
        "C": metrics_to_dict(metrics_c),
    }
    successes_n_by_condition: dict[str, tuple[int, int]] = {
        "A": (sum(1 for o in outcomes_a if o.is_correct), len(outcomes_a)),
        "B": (sum(1 for o in outcomes_b if o.is_correct), len(outcomes_b)),
        "C": (sum(1 for o in outcomes_c if o.is_correct), len(outcomes_c)),
    }
    render_condition_metric_bar(
        metrics_by_condition=metrics_by_condition,
        successes_n_by_condition=successes_n_by_condition,
        output_path=RESULTS_IMAGES_DIR / "condition_metric_bar.png",
    )
    if n_paired > 0:
        render_per_row_success_heatmap(
            task_ids=paired_ids,
            a_correct=a_correct_paired,
            b_correct=b_correct_paired,
            c_correct=c_correct_paired,
            output_path=RESULTS_IMAGES_DIR / "per_row_success_heatmap.png",
        )

    print(
        "\n========================================\n"
        f"Total cost: ${tracker.total_usd:.4f} (cap ${args.budget_cap_usd})\n"
        f"Halted: {halted}\n"
        f"N paired: {n_paired}\n"
        f"Metrics A: success={metrics_a.task_success_rate:.3f} "
        f"overconf={metrics_a.overconfident_error_rate:.3f} "
        f"avg_dec={metrics_a.avg_decisions_per_task:.2f}\n"
        f"Metrics B: success={metrics_b.task_success_rate:.3f} "
        f"overconf={metrics_b.overconfident_error_rate:.3f} "
        f"avg_dec={metrics_b.avg_decisions_per_task:.2f}\n"
        f"Metrics C: success={metrics_c.task_success_rate:.3f} "
        f"overconf={metrics_c.overconfident_error_rate:.3f} "
        f"avg_dec={metrics_c.avg_decisions_per_task:.2f}\n"
        f"A-B McNemar p={a_b_test.p_value:.4f} "
        f"discordant={a_b_test.discordant_pairs} method={a_b_test.method}\n"
        f"B-C McNemar p={b_c_test.p_value:.4f} discordant={b_c_test.discordant_pairs}\n"
        f"Confirmatory N for 5pp effect: {confirmatory_n}\n"
        "========================================",
        flush=True,
    )
    return 0


def _save_intermediate(path: Path, outcomes: list[RowOutcome]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(outcomes_to_jsonable(outcomes), indent=2), encoding="utf-8")


def _load_intermediate(path: Path) -> list[RowOutcome]:
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8").strip()
    if len(raw) == 0:
        return []
    items = json.loads(raw)
    if not isinstance(items, list):
        return []
    return jsonable_to_outcomes(items)


def _mcnemar_to_dict(result: Any) -> dict[str, Any]:
    return {
        "n_pairs": result.n_pairs,
        "discordant_pairs": result.discordant_pairs,
        "pos_minus_neg": result.pos_minus_neg,
        "p_value": result.p_value,
        "statistic": result.statistic,
        "method": result.method,
    }


def _ci_to_dict(ci: Any) -> dict[str, float]:
    return {"estimate": ci.estimate, "lower": ci.lower, "upper": ci.upper}


# Ensure RESULTS_DIR exists at import.
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    sys.exit(main())
