"""Build decision_inputs.json for the no-Anthropic RQ1 path decision.

Reads the five upstream JSON sidecars enumerated in plan/plan.md (t0031 power
grid, t0031 RQ4 stratification, t0031 log audit, t0026 costs, t0027 costs) and
emits a single JSON file with the option-table cells: discordance, power_grid,
per_arm_costs, option_costs.

Numbers are quoted verbatim from the upstream files or computed by simple
arithmetic. No statistical libraries; no fabrication. If any required field is
missing, the script raises a RuntimeError instead of guessing.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from tasks.t0032_no_anthropic_rq1_path_decision.code.paths import (
    DECISION_INPUTS_PATH,
    LOG_AUDIT_PATH,
    RQ1_POWER_GRID_PATH,
    RQ4_STRATIFICATION_PATH,
    T0026_COSTS_PATH,
    T0027_COSTS_PATH,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PAIRED_N_FIELD: str = "n_paired"
N_DISCORDANT_FIELD: str = "n_discordant"
A_ONLY_FIELD: str = "a_only"
B_ONLY_FIELD: str = "b_only"
MCNEMAR_P_FIELD: str = "mcnemar_p_two_sided"
PER_STRATUM_FIELD: str = "per_stratum"

STRATA_FIELD: str = "strata"
STRATUM_LABEL_FIELD: str = "label"
STRATUM_N_FIELD: str = "n"
STRATUM_DISCORDANT_N_FIELD: str = "discordant_n"
STRATUM_CELLS_FIELD: str = "cells"
STRATUM_BOTH_PASS: str = "both_pass"
STRATUM_BOTH_FAIL: str = "both_fail"

# Source labels in the t0031 JSON use "swebench" / "frontsci" / "taubench".
# Output keys in decision_inputs.json use the canonical project benchmark slugs
# matching meta/categories/benchmark-* entries.
STRATUM_LABEL_TO_OUTPUT_KEY: dict[str, str] = {
    "swebench": "swe-bench",
    "frontsci": "frontierscience",
    "taubench": "tau-bench",
}

VARIANT_B_AGENT_KEY: str = "variant_b_agent_full"
VARIANT_C_AGENT_KEY: str = "variant_c_agent_full"
RUNS_VARIANT_A_USD_KEY: str = "runs_variant_a_usd"
COST_USD_KEY: str = "cost_usd"
BREAKDOWN_KEY: str = "breakdown"

# Per-arm denominator (paired N=130 from t0027 fixed-arm convention).
PAIRED_N: int = 130

# t0029 admission cap (locked when Anthropic API was lost).
T0029_NEW_PAIRS_CAP: int = 218

# Option (c) per-paired-instance point estimate, anchored in
# research/research_internet.md: ~33% cheaper output tokens on GPT-5 / Gemini
# 2.5 Pro vs Claude Sonnet 4.6, multiplied through the realized ~$0.107 paired-
# instance cost on Sonnet. The internet research locks $0.07 per pair.
OPTION_C_PER_PAIR_USD: float = 0.07

# Round dollars to 4 decimal places to preserve fractional cents while keeping
# the JSON compact.
DOLLAR_ROUND: int = 4


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class StratumCell:
    n: int
    n_discordant: int
    a_only: int
    b_only: int
    both_pass: int
    both_fail: int
    mcnemar_p_two_sided: float


@dataclass(frozen=True, slots=True)
class PowerRow:
    p1: float
    power: float


@dataclass(frozen=True, slots=True)
class PerArmCosts:
    a_per_instance_usd: float
    b_per_instance_usd: float
    c_per_instance_usd: float
    paired_per_instance_usd: float


@dataclass(frozen=True, slots=True)
class OptionCosts:
    a_total_usd: float
    b_total_usd: float
    c_per_pair_usd: float
    c_total_usd: float
    d_total_usd: float


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_json(*, file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise RuntimeError(f"Required input file is missing: {file_path}")
    with file_path.open(encoding="utf-8") as handle:
        loaded: object = json.load(handle)
    if not isinstance(loaded, dict):
        raise RuntimeError(
            f"Expected top-level JSON object in {file_path}, got {type(loaded).__name__}",
        )
    return loaded


def _require(*, data: dict[str, Any], key: str, context: str) -> Any:
    if key not in data:
        raise RuntimeError(f"Missing required key '{key}' in {context}")
    return data[key]


def _find_stratum(
    *,
    strata: list[dict[str, Any]],
    label: str,
) -> dict[str, Any]:
    for stratum in strata:
        if stratum.get(STRATUM_LABEL_FIELD) == label:
            return stratum
    raise RuntimeError(
        f"Stratum '{label}' not found in rq4_stratification.json strata",
    )


def _build_stratum_cell(
    *,
    strata: list[dict[str, Any]],
    label: str,
) -> StratumCell:
    stratum: dict[str, Any] = _find_stratum(strata=strata, label=label)
    cells: dict[str, Any] = _require(
        data=stratum,
        key=STRATUM_CELLS_FIELD,
        context=f"stratum '{label}'",
    )
    return StratumCell(
        n=int(_require(data=stratum, key=STRATUM_N_FIELD, context=f"stratum '{label}'")),
        n_discordant=int(
            _require(
                data=stratum,
                key=STRATUM_DISCORDANT_N_FIELD,
                context=f"stratum '{label}'",
            ),
        ),
        a_only=int(_require(data=cells, key=A_ONLY_FIELD, context=f"stratum '{label}' cells")),
        b_only=int(_require(data=cells, key=B_ONLY_FIELD, context=f"stratum '{label}' cells")),
        both_pass=int(
            _require(data=cells, key=STRATUM_BOTH_PASS, context=f"stratum '{label}' cells"),
        ),
        both_fail=int(
            _require(data=cells, key=STRATUM_BOTH_FAIL, context=f"stratum '{label}' cells"),
        ),
        mcnemar_p_two_sided=float(
            _require(data=stratum, key=MCNEMAR_P_FIELD, context=f"stratum '{label}'"),
        ),
    )


def _build_discordance(
    *,
    rq4: dict[str, Any],
    log_audit: dict[str, Any],
) -> dict[str, Any]:
    strata_obj: object = _require(data=rq4, key=STRATA_FIELD, context="rq4_stratification.json")
    if not isinstance(strata_obj, list):
        raise RuntimeError("rq4_stratification.json 'strata' must be a list")
    strata: list[dict[str, Any]] = [s for s in strata_obj if isinstance(s, dict)]

    all_stratum: dict[str, Any] = _find_stratum(strata=strata, label="ALL")
    cells_all: dict[str, Any] = _require(
        data=all_stratum,
        key=STRATUM_CELLS_FIELD,
        context="ALL stratum",
    )

    n_paired: int = int(
        _require(data=all_stratum, key=STRATUM_N_FIELD, context="ALL stratum"),
    )
    n_discordant: int = int(
        _require(data=all_stratum, key=STRATUM_DISCORDANT_N_FIELD, context="ALL stratum"),
    )
    a_only: int = int(_require(data=cells_all, key=A_ONLY_FIELD, context="ALL stratum cells"))
    b_only: int = int(_require(data=cells_all, key=B_ONLY_FIELD, context="ALL stratum cells"))
    mcnemar_p: float = float(
        _require(data=all_stratum, key=MCNEMAR_P_FIELD, context="ALL stratum"),
    )

    # Cross-check against rq4_stratification.json top-level fields and against
    # the log audit's post-fix paired total. If anything disagrees, halt.
    overall_a_wins: int = int(
        _require(
            data=rq4,
            key="discordant_a_wins_overall",
            context="rq4_stratification.json",
        ),
    )
    overall_b_wins: int = int(
        _require(
            data=rq4,
            key="discordant_b_wins_overall",
            context="rq4_stratification.json",
        ),
    )
    if overall_a_wins != a_only or overall_b_wins != b_only:
        raise RuntimeError(
            "rq4_stratification.json overall a_wins/b_wins disagree with ALL stratum a_only/b_only"
            f": {overall_a_wins=}/{overall_b_wins=} vs {a_only=}/{b_only=}",
        )
    audit_post_fix: dict[str, Any] = _require(
        data=log_audit,
        key="post_fix_t0027",
        context="log_audit.json",
    )
    audit_n_paired: int = int(
        _require(
            data=audit_post_fix,
            key="n_paired",
            context="log_audit.json post_fix_t0027",
        ),
    )
    if audit_n_paired != n_paired:
        raise RuntimeError(
            "log_audit.json post_fix_t0027.n_paired disagrees with rq4 ALL stratum n: "
            f"{audit_n_paired=} vs {n_paired=}",
        )

    per_stratum: dict[str, dict[str, Any]] = {}
    for source_label, output_key in STRATUM_LABEL_TO_OUTPUT_KEY.items():
        cell: StratumCell = _build_stratum_cell(strata=strata, label=source_label)
        per_stratum[output_key] = asdict(cell)

    return {
        PAIRED_N_FIELD: n_paired,
        N_DISCORDANT_FIELD: n_discordant,
        A_ONLY_FIELD: a_only,
        B_ONLY_FIELD: b_only,
        MCNEMAR_P_FIELD: mcnemar_p,
        PER_STRATUM_FIELD: per_stratum,
    }


def _build_power_grid(*, rq1: dict[str, Any]) -> list[dict[str, float]]:
    grid_obj: object = _require(data=rq1, key="grid", context="rq1_power_grid.json")
    if not isinstance(grid_obj, list):
        raise RuntimeError("rq1_power_grid.json 'grid' must be a list")
    rows: list[PowerRow] = []
    for entry in grid_obj:
        if not isinstance(entry, dict):
            raise RuntimeError("rq1_power_grid.json grid entries must be objects")
        p1: float = float(
            _require(data=entry, key="b_wins_conditional", context="rq1_power_grid.json grid row"),
        )
        power: float = float(
            _require(data=entry, key="power_at_expected", context="rq1_power_grid.json grid row"),
        )
        rows.append(PowerRow(p1=p1, power=power))

    # Ensure the row where power first crosses 0.80 is present (sanity check —
    # the grid covers p1 in [0.55, 0.80] so 0.80 crossing must exist).
    if not any(row.power >= 0.80 for row in rows):
        raise RuntimeError(
            "rq1_power_grid.json grid never reaches 0.80 power; expected to cross at p1>=0.75",
        )

    return [asdict(row) for row in rows]


def _build_per_arm_costs(
    *,
    t0026_costs: dict[str, Any],
    t0027_costs: dict[str, Any],
) -> PerArmCosts:
    t0026_breakdown: dict[str, Any] = _require(
        data=t0026_costs,
        key=BREAKDOWN_KEY,
        context="t0026 costs.json",
    )
    a_total_usd: float = float(
        _require(
            data=t0026_breakdown,
            key=RUNS_VARIANT_A_USD_KEY,
            context="t0026 costs.json breakdown",
        ),
    )
    a_per_instance: float = a_total_usd / PAIRED_N

    t0027_breakdown: dict[str, Any] = _require(
        data=t0027_costs,
        key=BREAKDOWN_KEY,
        context="t0027 costs.json",
    )
    variant_b: dict[str, Any] = _require(
        data=t0027_breakdown,
        key=VARIANT_B_AGENT_KEY,
        context="t0027 costs.json breakdown",
    )
    variant_c: dict[str, Any] = _require(
        data=t0027_breakdown,
        key=VARIANT_C_AGENT_KEY,
        context="t0027 costs.json breakdown",
    )
    b_total_usd: float = float(
        _require(data=variant_b, key=COST_USD_KEY, context="t0027 variant_b_agent_full"),
    )
    c_total_usd: float = float(
        _require(data=variant_c, key=COST_USD_KEY, context="t0027 variant_c_agent_full"),
    )
    b_per_instance: float = b_total_usd / PAIRED_N
    c_per_instance: float = c_total_usd / PAIRED_N

    paired_per_instance: float = a_per_instance + b_per_instance

    return PerArmCosts(
        a_per_instance_usd=round(a_per_instance, DOLLAR_ROUND),
        b_per_instance_usd=round(b_per_instance, DOLLAR_ROUND),
        c_per_instance_usd=round(c_per_instance, DOLLAR_ROUND),
        paired_per_instance_usd=round(paired_per_instance, DOLLAR_ROUND),
    )


def _build_option_costs() -> OptionCosts:
    c_total_usd: float = OPTION_C_PER_PAIR_USD * T0029_NEW_PAIRS_CAP
    return OptionCosts(
        a_total_usd=0.0,
        b_total_usd=0.0,
        c_per_pair_usd=round(OPTION_C_PER_PAIR_USD, DOLLAR_ROUND),
        c_total_usd=round(c_total_usd, DOLLAR_ROUND),
        d_total_usd=0.0,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    rq1: dict[str, Any] = _load_json(file_path=RQ1_POWER_GRID_PATH)
    rq4: dict[str, Any] = _load_json(file_path=RQ4_STRATIFICATION_PATH)
    log_audit: dict[str, Any] = _load_json(file_path=LOG_AUDIT_PATH)
    t0026_costs: dict[str, Any] = _load_json(file_path=T0026_COSTS_PATH)
    t0027_costs: dict[str, Any] = _load_json(file_path=T0027_COSTS_PATH)

    discordance: dict[str, Any] = _build_discordance(rq4=rq4, log_audit=log_audit)
    power_grid: list[dict[str, float]] = _build_power_grid(rq1=rq1)
    per_arm_costs: PerArmCosts = _build_per_arm_costs(
        t0026_costs=t0026_costs,
        t0027_costs=t0027_costs,
    )
    option_costs: OptionCosts = _build_option_costs()

    payload: dict[str, Any] = {
        "spec_version": "1",
        "task_id": "t0032_no_anthropic_rq1_path_decision",
        "discordance": discordance,
        "power_grid": power_grid,
        "per_arm_costs": asdict(per_arm_costs),
        "option_costs": asdict(option_costs),
    }

    DECISION_INPUTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    DECISION_INPUTS_PATH.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {DECISION_INPUTS_PATH}")
    print(
        f"discordance: n_paired={discordance[PAIRED_N_FIELD]}, "
        f"n_discordant={discordance[N_DISCORDANT_FIELD]}, "
        f"a_only={discordance[A_ONLY_FIELD]}, b_only={discordance[B_ONLY_FIELD]}, "
        f"mcnemar_p_two_sided={discordance[MCNEMAR_P_FIELD]}",
    )
    print(
        f"per_arm_costs: a={per_arm_costs.a_per_instance_usd}, "
        f"b={per_arm_costs.b_per_instance_usd}, c={per_arm_costs.c_per_instance_usd}, "
        f"paired={per_arm_costs.paired_per_instance_usd}",
    )
    print(
        f"option_costs: c_per_pair={option_costs.c_per_pair_usd}, "
        f"c_total={option_costs.c_total_usd}",
    )


if __name__ == "__main__":
    main()
