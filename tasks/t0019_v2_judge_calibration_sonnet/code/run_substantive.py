"""Run the substantive critic judge configuration on the 55-row pool."""

from __future__ import annotations

from tasks.t0019_v2_judge_calibration_sonnet.code.constants import (
    PROMPT_KIND_SUBSTANTIVE,
    SUBSTANTIVE_JUDGE_SYSTEM_PROMPT,
    SUBSTANTIVE_JUDGE_USER_TEMPLATE,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.data_loader import load_pool
from tasks.t0019_v2_judge_calibration_sonnet.code.judge_runner import (
    make_arg_parser,
    run_pool,
)
from tasks.t0019_v2_judge_calibration_sonnet.code.paths import SUBSTANTIVE_OUTCOMES_PATH


def main() -> None:
    parser = make_arg_parser(description="Run substantive critic judge (Sonnet) on the pool")
    args = parser.parse_args()
    pool = load_pool()
    print(
        f"Pool size: {len(pool)} rows. Running prompt_kind={PROMPT_KIND_SUBSTANTIVE} "
        f"with model={args.model} workers={args.workers} limit={args.limit}."
    )
    stats = run_pool(
        pool=pool,
        prompt_kind=PROMPT_KIND_SUBSTANTIVE,
        model=args.model,
        system_prompt=SUBSTANTIVE_JUDGE_SYSTEM_PROMPT,
        user_template=SUBSTANTIVE_JUDGE_USER_TEMPLATE,
        output_jsonl_path=SUBSTANTIVE_OUTCOMES_PATH,
        max_workers=args.workers,
        limit=args.limit,
        transport=args.transport,
        budget_cap_usd=args.budget_cap,
    )
    print(
        f"DONE substantive: judged={stats.rows_judged} acceptable={stats.rows_acceptable} "
        f"needs_revision={stats.rows_needs_revision} parse_fail={stats.rows_parse_failure} "
        f"call_fail={stats.rows_call_failure} total_cost=${stats.total_cost_usd:.4f} "
        f"total_elapsed={stats.total_elapsed_seconds:.2f}s"
    )


if __name__ == "__main__":
    main()
