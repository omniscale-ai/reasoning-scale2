"""Analysis 2: RQ1 power / futility under t0029's $35 cap."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

import matplotlib.pyplot as plt

from tasks.t0031_rq1_rq4_no_new_api_salvage.code.constants import (
    ALPHA,
    B_WINS_GRID,
    COST_PER_PAIR_USD,
    EXISTING_PAIRED_N,
    HARD_CAP_USD,
)
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.load_paired_outputs import load_paired_frame
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.paths import (
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
    RQ1_POWER_CURVE_PNG,
    RQ1_POWER_JSON,
)
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.stats_helpers import (
    best_case_p_value_one_sided,
    mcnemar_one_sided_critical_k,
    mcnemar_power_one_sided,
    smallest_n_disc_for_power,
)


@dataclass(frozen=True, slots=True)
class GridEntry:
    b_wins_conditional: float
    expected_discordant_n: int
    power_at_expected: float
    smallest_n_disc_for_80_power: int | None
    achievable_p_floor: float
    critical_k_at_expected: int | None


def _grid_entry(*, p1: float, expected_disc: int) -> GridEntry:
    power = mcnemar_power_one_sided(n_disc=expected_disc, p1_b_wins=p1, alpha=ALPHA)
    n80 = smallest_n_disc_for_power(p1_b_wins=p1, target_power=0.80, alpha=ALPHA, n_max=200)
    p_floor = best_case_p_value_one_sided(n_disc=expected_disc)
    crit_k = mcnemar_one_sided_critical_k(n_disc=expected_disc, alpha=ALPHA)
    return GridEntry(
        b_wins_conditional=p1,
        expected_discordant_n=expected_disc,
        power_at_expected=power,
        smallest_n_disc_for_80_power=n80,
        achievable_p_floor=p_floor,
        critical_k_at_expected=crit_k,
    )


def _draw_power_curve(*, entries: list[GridEntry], expected_disc: int, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    p1_vals = [e.b_wins_conditional for e in entries]
    powers = [e.power_at_expected for e in entries]
    ax.plot(p1_vals, powers, marker="o", linewidth=2, label="power at expected n_disc")
    ax.axhline(0.80, color="red", linestyle="--", alpha=0.7, label="target power = 0.80")
    ax.set_xlabel("conditional B-wins rate (p1)")
    ax.set_ylabel("McNemar power (one-sided, α=0.05)")
    ax.set_ylim(0.0, 1.0)
    ax.set_title(f"RQ1 power vs conditional B-wins under $35 cap (expected n_disc≈{expected_disc})")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    frame = load_paired_frame()

    new_pairs_at_cap = math.floor(HARD_CAP_USD / COST_PER_PAIR_USD)
    total_paired_n_at_cap = EXISTING_PAIRED_N + new_pairs_at_cap
    expected_discordant_at_cap = round(total_paired_n_at_cap * frame.discordance_rate)

    entries = [_grid_entry(p1=p1, expected_disc=expected_discordant_at_cap) for p1 in B_WINS_GRID]

    payload = {
        "spec_version": "1",
        "task_id": "t0031_rq1_rq4_no_new_api_salvage",
        "discordance_rate_t0027": frame.discordance_rate,
        "existing_paired_n": EXISTING_PAIRED_N,
        "hard_cap_usd": HARD_CAP_USD,
        "cost_per_pair_usd": COST_PER_PAIR_USD,
        "new_pairs_at_cap": new_pairs_at_cap,
        "total_paired_n_at_cap": total_paired_n_at_cap,
        "expected_discordant_at_cap": expected_discordant_at_cap,
        "alpha": ALPHA,
        "grid": [
            {
                "b_wins_conditional": e.b_wins_conditional,
                "expected_discordant_n": e.expected_discordant_n,
                "power_at_expected": e.power_at_expected,
                "smallest_n_disc_for_80_power": e.smallest_n_disc_for_80_power,
                "achievable_p_floor_one_sided": e.achievable_p_floor,
                "critical_k_at_expected": e.critical_k_at_expected,
            }
            for e in entries
        ],
    }
    RQ1_POWER_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    _draw_power_curve(
        entries=entries,
        expected_disc=expected_discordant_at_cap,
        output_path=str(RQ1_POWER_CURVE_PNG),
    )
    print(f"Wrote {RQ1_POWER_JSON}")
    print(f"Wrote {RQ1_POWER_CURVE_PNG}")
    print(
        f"Cap admits {new_pairs_at_cap} new pairs; total {total_paired_n_at_cap} paired; "
        f"expected disc ≈ {expected_discordant_at_cap}"
    )
    for e in entries:
        print(
            f"  p1={e.b_wins_conditional}: power={e.power_at_expected:.3f}, "
            f"smallest_n_for_80={e.smallest_n_disc_for_80_power}"
        )


if __name__ == "__main__":
    main()
