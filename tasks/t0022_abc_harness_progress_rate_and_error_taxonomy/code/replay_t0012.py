"""Replay t0012 smoke trajectories through the abc_harness_metrics library.

For each row in the t0012 phase2 smoke prediction JSONLs (conditions A, B, C):

    1. Reconstruct a :class:`Trajectory` from the row's ``trajectory`` list.
    2. Look up the matching :class:`EnvironmentSubgoals` by ``task_id`` from the
       FrontierScience-Olympiad subgoal JSON.
    3. Run :func:`score_trajectory` against the local Claude judge CLI to compute
       progress rate and per-step error labels.
    4. Aggregate into ``code/replay_summary.json`` with progress-rate distribution
       statistics and A-vs-C error-distribution separation.

Cost cap: $2 per :data:`MAX_BUDGET_USD`. Calls beyond the cap raise.

CLI usage:
    uv run python -m tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.replay_t0012 \\
        [--limit N] [--dry-run]

The ``--dry-run`` flag substitutes a deterministic mock judge (always "yes" for
progress and "ok" for errors) so the pipeline can be exercised offline at zero
cost.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.constants import (
    ERROR_TAXONOMY_SYSTEM_PROMPT,
    JUDGE_MODEL_DEFAULT,
    MAX_BUDGET_USD,
    PROGRESS_RATE_SYSTEM_PROMPT,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.model_call import (
    CostTracker,
    make_judge_call,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import (
    REPLAY_SUMMARY_PATH,
    SUBGOALS_FRONTIERSCIENCE_JSON,
    T0012_PRED_A,
    T0012_PRED_B,
    T0012_PRED_C,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.score_trajectory import (
    score_trajectory,
)
from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.types import (
    EnvironmentSubgoals,
    ErrorTaxonomyLabel,
    Subgoal,
    Trajectory,
    TrajectoryScore,
    TrajectoryStep,
)


def _load_environments() -> dict[str, EnvironmentSubgoals]:
    raw = json.loads(SUBGOALS_FRONTIERSCIENCE_JSON.read_text(encoding="utf-8"))
    out: dict[str, EnvironmentSubgoals] = {}
    for entry in raw:
        env_id = entry["environment_id"]
        subgoals = tuple(
            Subgoal(subgoal_id=s["id"], description=s["description"]) for s in entry["subgoals"]
        )
        out[env_id] = EnvironmentSubgoals(environment_id=env_id, subgoals=subgoals)
    return out


def _row_to_trajectory(*, row: dict[str, Any]) -> Trajectory:
    raw_steps = row.get("trajectory") or []
    steps_list: list[TrajectoryStep] = []
    for i, s in enumerate(raw_steps):
        if not isinstance(s, dict):
            continue
        steps_list.append(
            TrajectoryStep(
                turn_index=int(s.get("turn_index", i)),
                granularity=str(s.get("granularity", "atomic")),
                thought=str(s.get("thought", "")),
                action=str(s.get("action", "thought_only")),
                observation=str(s.get("observation", "")),
                confidence=None,
            )
        )
    return Trajectory(
        task_id=str(row.get("task_id", "")),
        steps=tuple(steps_list),
        task_success=bool(row.get("is_correct", False)),
    )


def _yes_judge(_prompt: str) -> str:
    return "yes"


def _ok_judge(_prompt: str) -> str:
    return "ok"


def _iter_predictions(*, limit: int | None) -> list[tuple[str, dict[str, Any]]]:
    """Yield (condition_label, row) pairs for each row in A, B, C up to ``limit``."""
    pairs: list[tuple[str, dict[str, Any]]] = []
    for label, path in (("A", T0012_PRED_A), ("B", T0012_PRED_B), ("C", T0012_PRED_C)):
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            for line in f:
                pairs.append((label, json.loads(line)))
    if limit is not None:
        return pairs[:limit]
    return pairs


def _condition_distribution(
    *,
    scores_by_condition: dict[str, list[TrajectoryScore]],
    condition: str,
) -> Counter[ErrorTaxonomyLabel]:
    aggregate: Counter[ErrorTaxonomyLabel] = Counter()
    for score in scores_by_condition.get(condition, []):
        aggregate.update(score.error_distribution)
    return aggregate


def _separation_rate(
    *, dist_a: Counter[ErrorTaxonomyLabel], dist_c: Counter[ErrorTaxonomyLabel]
) -> float:
    """Compute total-variation distance between A and C error distributions.

    Both distributions are normalized to probabilities before comparison. Returns
    a value in [0, 1] where 0 means identical and 1 means disjoint support.
    """
    total_a = sum(dist_a.values())
    total_c = sum(dist_c.values())
    if total_a == 0 or total_c == 0:
        return 0.0
    keys: set[ErrorTaxonomyLabel] = set(dist_a) | set(dist_c)
    tvd = 0.5 * sum(abs((dist_a.get(k, 0) / total_a) - (dist_c.get(k, 0) / total_c)) for k in keys)
    return float(tvd)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Process at most N rows.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use a mock judge (always yes/ok) instead of the live CLI.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPLAY_SUMMARY_PATH,
        help="Where to write the replay summary JSON.",
    )
    args = parser.parse_args()

    environments = _load_environments()
    pairs = _iter_predictions(limit=args.limit)

    progress_judge: Callable[[str], str]
    error_judge: Callable[[str], str]
    cost_tracker: CostTracker | None = None
    prior_spend_usd: float = 0.0
    if args.dry_run:
        # Redirect cache to a temp path so dry-run never pollutes the live cache.
        import tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.judge_cache as _jc

        _jc.JUDGE_CACHE_DIR = Path("/tmp") / "_t0022_dryrun_cache"
        progress_judge = _yes_judge
        error_judge = _ok_judge
    else:
        # Account for spend already recorded in _cost_log.jsonl from prior partial runs.
        # The CostTracker is process-local but our budget cap is global per the t0022 spec.
        from tasks.t0022_abc_harness_progress_rate_and_error_taxonomy.code.paths import (
            COST_LOG_PATH,
        )

        if COST_LOG_PATH.exists():
            for raw in COST_LOG_PATH.read_text(encoding="utf-8").splitlines():
                if not raw.strip():
                    continue
                try:
                    entry = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                prior_spend_usd += float(entry.get("cost_usd", 0.0))
        remaining_budget_usd: float = max(0.0, MAX_BUDGET_USD - prior_spend_usd)
        cost_tracker = CostTracker(cap_usd=remaining_budget_usd)
        raw_progress_judge = make_judge_call(
            model=JUDGE_MODEL_DEFAULT,
            cost_tracker=cost_tracker,
            system_prompt=PROGRESS_RATE_SYSTEM_PROMPT,
            note="progress_rate",
        )
        raw_error_judge = make_judge_call(
            model=JUDGE_MODEL_DEFAULT,
            cost_tracker=cost_tracker,
            system_prompt=ERROR_TAXONOMY_SYSTEM_PROMPT,
            note="error_taxonomy",
        )

        def _budget_guarded(*, inner: Callable[[str], str], fallback: str) -> Callable[[str], str]:
            """Wrap a judge so it returns ``fallback`` once the budget cap is hit.

            This prevents the replay from over-spending: any call attempted after the
            cap returns the conservative fallback (which the parser maps to ``no`` for
            progress and ``precondition_or_effect`` for errors). The wrapper still
            consults the disk cache via the underlying score path -- it only kicks in
            on cache misses where the live CLI call would push us over budget.

            Headroom is set to 0.10 USD to absorb the worst observed per-call cost
            (~0.04 USD) so an in-flight call after the guard fires cannot push the
            project total past MAX_BUDGET_USD.
            """

            def call(prompt: str) -> str:
                if not cost_tracker.is_budget_ok(headroom_usd=0.10):
                    return fallback
                return inner(prompt)

            return call

        progress_judge = _budget_guarded(inner=raw_progress_judge, fallback="no")
        error_judge = _budget_guarded(inner=raw_error_judge, fallback="ok")

    scores_by_condition: dict[str, list[TrajectoryScore]] = {"A": [], "B": [], "C": []}
    skipped: int = 0
    processed: int = 0
    for condition, row in pairs:
        traj = _row_to_trajectory(row=row)
        if len(traj.steps) == 0:
            skipped += 1
            continue
        env = environments.get(traj.task_id)
        if env is None:
            skipped += 1
            continue
        score = score_trajectory(
            trajectory=traj,
            environment=env,
            progress_judge=progress_judge,
            error_judge=error_judge,
        )
        scores_by_condition[condition].append(score)
        processed += 1

    all_scores: list[TrajectoryScore] = (
        scores_by_condition["A"] + scores_by_condition["B"] + scores_by_condition["C"]
    )
    progress_rates: list[float] = [s.progress_rate for s in all_scores]
    pr_mean = float(statistics.mean(progress_rates)) if len(progress_rates) > 0 else 0.0
    pr_stddev = float(statistics.pstdev(progress_rates)) if len(progress_rates) > 1 else 0.0

    dist_a = _condition_distribution(scores_by_condition=scores_by_condition, condition="A")
    dist_b = _condition_distribution(scores_by_condition=scores_by_condition, condition="B")
    dist_c = _condition_distribution(scores_by_condition=scores_by_condition, condition="C")
    a_vs_c_separation = _separation_rate(dist_a=dist_a, dist_c=dist_c)

    summary = {
        "processed_rows": processed,
        "skipped_rows": skipped,
        "rows_per_condition": {k: len(v) for k, v in scores_by_condition.items()},
        "progress_rate_mean": pr_mean,
        "progress_rate_stddev": pr_stddev,
        "progress_rate_distribution": {
            "min": float(min(progress_rates)) if len(progress_rates) > 0 else 0.0,
            "max": float(max(progress_rates)) if len(progress_rates) > 0 else 0.0,
            "values": progress_rates,
        },
        "error_distribution_a": {label.value: count for label, count in dist_a.items()},
        "error_distribution_b": {label.value: count for label, count in dist_b.items()},
        "error_distribution_c": {label.value: count for label, count in dist_c.items()},
        "a_vs_c_separation_rate": a_vs_c_separation,
        "decision_criteria": {
            "progress_rate_mean_above_0_05": pr_mean > 0.05,
            "progress_rate_stddev_above_0_03": pr_stddev > 0.03,
            "a_vs_c_separation_above_0_30": a_vs_c_separation >= 0.30,
        },
        "total_cost_usd": float(cost_tracker.total_usd) if cost_tracker is not None else 0.0,
        "total_cost_usd_including_prior": (
            float(cost_tracker.total_usd) + (prior_spend_usd if not args.dry_run else 0.0)
            if cost_tracker is not None
            else 0.0
        ),
        "dry_run": args.dry_run,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"  processed: {processed} rows; skipped: {skipped}")
    print(f"  progress_rate: mean={pr_mean:.3f} stddev={pr_stddev:.3f}")
    print(f"  a_vs_c_separation_rate: {a_vs_c_separation:.3f}")
    print(f"  total_cost_usd: {summary['total_cost_usd']:.4f}")


if __name__ == "__main__":
    main()
