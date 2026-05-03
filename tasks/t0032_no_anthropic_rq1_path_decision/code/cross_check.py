"""Cross-check decision_inputs.json against the verbatim t0031 numbers.

This guard runs after build_decision_inputs.py and asserts that the headline
discordance counts and McNemar p-value match the values reported in
research/research_code.md verbatim. If anything disagrees, the script raises a
RuntimeError instead of silently passing — see plan/plan.md Step 3 [CRITICAL].
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tasks.t0032_no_anthropic_rq1_path_decision.code.paths import (
    DECISION_INPUTS_PATH,
)

# ---------------------------------------------------------------------------
# Verbatim t0031 numbers (from research/research_code.md)
# ---------------------------------------------------------------------------

EXPECTED_N_PAIRED: int = 130
EXPECTED_N_DISCORDANT: int = 12
EXPECTED_A_ONLY: int = 6
EXPECTED_B_ONLY: int = 6
EXPECTED_MCNEMAR_P_TWO_SIDED: float = 1.0

EXPECTED_PER_STRATUM: dict[str, dict[str, int]] = {
    "swe-bench": {"a_only": 0, "b_only": 6},
    "frontierscience": {"a_only": 5, "b_only": 0},
    "tau-bench": {"n_discordant": 1},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load(*, file_path: Path) -> dict[str, Any]:
    with file_path.open(encoding="utf-8") as handle:
        loaded: object = json.load(handle)
    if not isinstance(loaded, dict):
        raise RuntimeError(f"{file_path} must be a JSON object")
    return loaded


def _check_eq(*, label: str, expected: object, actual: object) -> None:
    if expected != actual:
        raise RuntimeError(
            f"Cross-check failed for {label}: expected={expected!r}, actual={actual!r}",
        )


def main() -> None:
    inputs: dict[str, Any] = _load(file_path=DECISION_INPUTS_PATH)
    discordance: dict[str, Any] = inputs["discordance"]

    _check_eq(
        label="discordance.n_paired",
        expected=EXPECTED_N_PAIRED,
        actual=int(discordance["n_paired"]),
    )
    _check_eq(
        label="discordance.n_discordant",
        expected=EXPECTED_N_DISCORDANT,
        actual=int(discordance["n_discordant"]),
    )
    _check_eq(
        label="discordance.a_only",
        expected=EXPECTED_A_ONLY,
        actual=int(discordance["a_only"]),
    )
    _check_eq(
        label="discordance.b_only",
        expected=EXPECTED_B_ONLY,
        actual=int(discordance["b_only"]),
    )
    _check_eq(
        label="discordance.mcnemar_p_two_sided",
        expected=EXPECTED_MCNEMAR_P_TWO_SIDED,
        actual=float(discordance["mcnemar_p_two_sided"]),
    )

    per_stratum: dict[str, Any] = discordance["per_stratum"]
    swebench: dict[str, Any] = per_stratum["swe-bench"]
    _check_eq(
        label="per_stratum.swe-bench.a_only",
        expected=EXPECTED_PER_STRATUM["swe-bench"]["a_only"],
        actual=int(swebench["a_only"]),
    )
    _check_eq(
        label="per_stratum.swe-bench.b_only",
        expected=EXPECTED_PER_STRATUM["swe-bench"]["b_only"],
        actual=int(swebench["b_only"]),
    )

    fsci: dict[str, Any] = per_stratum["frontierscience"]
    _check_eq(
        label="per_stratum.frontierscience.a_only",
        expected=EXPECTED_PER_STRATUM["frontierscience"]["a_only"],
        actual=int(fsci["a_only"]),
    )
    _check_eq(
        label="per_stratum.frontierscience.b_only",
        expected=EXPECTED_PER_STRATUM["frontierscience"]["b_only"],
        actual=int(fsci["b_only"]),
    )

    tau: dict[str, Any] = per_stratum["tau-bench"]
    _check_eq(
        label="per_stratum.tau-bench.n_discordant",
        expected=EXPECTED_PER_STRATUM["tau-bench"]["n_discordant"],
        actual=int(tau["n_discordant"]),
    )

    print("OK: decision_inputs.json matches t0031 verbatim numbers")


if __name__ == "__main__":
    main()
