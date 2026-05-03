"""Render the four-row comparison table consumed by the answer asset.

Reads decision_inputs.json (produced by build_decision_inputs.py) and writes a
single-table markdown file with exactly four data rows: option (a) existing-
results-only verdict, option (b) local / open-weight rerun, option (c)
alternative paid provider, option (d) project-level "underpowered, provider-
blocked" stop. Each row carries USD point estimate, validity / power risk,
comparability with t0027 / t0028, and time-to-result.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0032_no_anthropic_rq1_path_decision.code.paths import (
    COMPARISON_TABLE_PATH,
    DECISION_INPUTS_PATH,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OPTION_A_LABEL: str = "(a) existing-results-only verdict"
OPTION_B_LABEL: str = "(b) local / open-weight rerun"
OPTION_C_LABEL: str = "(c) alternative paid provider (GPT-5 / Gemini 2.5 Pro)"
OPTION_D_LABEL: str = "(d) project-level underpowered / provider-blocked stop"

T0029_CAP_PAIRS: int = 218

TABLE_HEADER: str = (
    "| Option | USD point estimate | Validity / power risk | "
    "Comparability with t0027 / t0028 | Time-to-result |"
)
TABLE_SEPARATOR: str = "| --- | ---: | --- | --- | --- |"


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TableRow:
    option: str
    usd_point_estimate: str
    validity_power_risk: str
    comparability: str
    time_to_result: str

    def render(self) -> str:
        return (
            f"| {self.option} | {self.usd_point_estimate} | "
            f"{self.validity_power_risk} | {self.comparability} | {self.time_to_result} |"
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_decision_inputs(*, file_path: Path) -> dict[str, Any]:
    if not file_path.exists():
        raise RuntimeError(f"decision_inputs.json missing: {file_path}")
    with file_path.open(encoding="utf-8") as handle:
        loaded: object = json.load(handle)
    if not isinstance(loaded, dict):
        raise RuntimeError("decision_inputs.json must be a JSON object")
    return loaded


def _format_dollars(value: float) -> str:
    return f"${value:.2f}"


def _build_rows(*, inputs: dict[str, Any]) -> list[TableRow]:
    option_costs: dict[str, Any] = inputs["option_costs"]
    discordance: dict[str, Any] = inputs["discordance"]

    a_total: float = float(option_costs["a_total_usd"])
    b_total: float = float(option_costs["b_total_usd"])
    c_per_pair: float = float(option_costs["c_per_pair_usd"])
    c_total: float = float(option_costs["c_total_usd"])
    d_total: float = float(option_costs["d_total_usd"])

    n_paired: int = int(discordance["n_paired"])
    n_disc: int = int(discordance["n_discordant"])
    p_value: float = float(discordance["mcnemar_p_two_sided"])

    option_a_validity: str = (
        f"Aggregate McNemar p={p_value:.4f} on N={n_paired} ({n_disc} discordant); "
        "verdict is null aggregate with documented per-stratum interaction. No new sampling."
    )
    option_a_comparability: str = (
        "Trivially preserved; no rerun, t0027 fixed-arm convention untouched."
    )
    option_a_time: str = "Hours (analysis-only; no compute)."

    option_b_validity: str = (
        "Same structural underpowering as (c) at the t0029 cap; open-weight policy quality "
        "is unbounded variance vs Sonnet baseline."
    )
    option_b_comparability: str = (
        "Lost: replaces the policy under arm A or arm B; verdict is on a different model, "
        "not on the t0027 arms."
    )
    option_b_time: str = "Days to weeks (engineering + GPU provisioning)."

    option_c_validity: str = (
        "Power < 0.80 unless true p1 >= 0.75 (per t0031 power grid); cap-sized rerun "
        "still likely null."
    )
    option_c_comparability: str = (
        "Lost: GPT-5 or Gemini 2.5 Pro plays arm B in place of Claude Sonnet 4.6; arm "
        "label preserved, policy under label changed."
    )
    option_c_time: str = "About 1-2 days (provider onboarding + 218-pair sweep)."

    option_d_validity: str = (
        "No verdict produced; forecloses analysis that (a) can already deliver."
    )
    option_d_comparability: str = (
        "Trivially preserved (no rerun); but the comparability is moot without a verdict."
    )
    option_d_time: str = "Immediate (hard stop)."

    return [
        TableRow(
            option=OPTION_A_LABEL,
            usd_point_estimate=_format_dollars(a_total),
            validity_power_risk=option_a_validity,
            comparability=option_a_comparability,
            time_to_result=option_a_time,
        ),
        TableRow(
            option=OPTION_B_LABEL,
            usd_point_estimate=f"{_format_dollars(b_total)} (hardware-bound)",
            validity_power_risk=option_b_validity,
            comparability=option_b_comparability,
            time_to_result=option_b_time,
        ),
        TableRow(
            option=OPTION_C_LABEL,
            usd_point_estimate=(
                f"{_format_dollars(c_per_pair)} / pair x {T0029_CAP_PAIRS} = "
                f"{_format_dollars(c_total)} (band $15-$25)"
            ),
            validity_power_risk=option_c_validity,
            comparability=option_c_comparability,
            time_to_result=option_c_time,
        ),
        TableRow(
            option=OPTION_D_LABEL,
            usd_point_estimate=_format_dollars(d_total),
            validity_power_risk=option_d_validity,
            comparability=option_d_comparability,
            time_to_result=option_d_time,
        ),
    ]


def _render(rows: list[TableRow]) -> str:
    lines: list[str] = [
        "# RQ1 path decision comparison table",
        "",
        "Generated from `decision_inputs.json` by `build_comparison_table.py`. "
        "All four required execution paths under the permanent no-Anthropic constraint.",
        "",
        TABLE_HEADER,
        TABLE_SEPARATOR,
    ]
    lines.extend(row.render() for row in rows)
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    inputs: dict[str, Any] = _load_decision_inputs(file_path=DECISION_INPUTS_PATH)
    rows: list[TableRow] = _build_rows(inputs=inputs)
    rendered: str = _render(rows)
    COMPARISON_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    COMPARISON_TABLE_PATH.write_text(rendered, encoding="utf-8")
    print(f"Wrote {COMPARISON_TABLE_PATH}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
