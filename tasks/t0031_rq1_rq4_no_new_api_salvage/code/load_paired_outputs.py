"""Single inversion point for t0027 variant_a/b/c -> arm A/B/C.

t0031 reporting convention:
  arm A = Plan-and-Solve baseline
  arm B = scope-aware ReAct
  arm C = mismatched-strategy

t0027 internal labelling:
  variant_a = scope-aware ReAct        (= arm B after inversion)
  variant_b = plan_and_solve_v3        (= arm A after inversion)
  variant_c = matched_mismatch_v2      (= arm C, no inversion)

This helper is the ONLY place where this rename happens. Downstream consumers
must use only the post-inversion arm-labelled DataFrame returned by
``load_paired_frame``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tasks.t0031_rq1_rq4_no_new_api_salvage.code.constants import (
    EXISTING_PAIRED_N,
    EXISTING_PER_SUBSET,
    INSTANCE_ID,
    JUDGE_SUCCESS,
    RECOVERY_PATH,
    ArmKind,
)
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.paths import (
    PAIRED_MANIFEST_JSON,
    VARIANT_A_JSONL,
    VARIANT_B_JSONL,
    VARIANT_C_JSONL,
)

# Variant -> arm mapping. THE single inversion point.
VARIANT_TO_ARM: dict[str, ArmKind] = {
    "a": ArmKind.ARM_B,
    "b": ArmKind.ARM_A,
    "c": ArmKind.ARM_C,
}


@dataclass(frozen=True, slots=True)
class PairedFrame:
    df: pd.DataFrame
    n_total: int
    n_per_subset: dict[str, int]
    n_discordant_a_vs_b: int
    discordant_b_wins: int  # arm_b correct AND arm_a incorrect
    discordant_a_wins: int  # arm_a correct AND arm_b incorrect
    discordance_rate: float


def _load_paired_ids(*, manifest_path: Path) -> set[str]:
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    ids = raw["instance_ids"]
    assert isinstance(ids, list), "paired_manifest.instance_ids must be a list"
    assert len(ids) == EXISTING_PAIRED_N, (
        f"paired manifest has {len(ids)} ids, expected {EXISTING_PAIRED_N}"
    )
    return set(ids)


def _load_jsonl(*, path: Path) -> pd.DataFrame:
    return pd.read_json(path, lines=True)


def _filter_to_paired(*, df: pd.DataFrame, paired_ids: set[str]) -> pd.DataFrame:
    return df[df[INSTANCE_ID].isin(paired_ids)].copy()


def load_paired_frame() -> PairedFrame:
    paired_ids = _load_paired_ids(manifest_path=PAIRED_MANIFEST_JSON)

    df_a_raw = _load_jsonl(path=VARIANT_A_JSONL)
    df_b_raw = _load_jsonl(path=VARIANT_B_JSONL)
    df_c_raw = _load_jsonl(path=VARIANT_C_JSONL)

    # Variant A (t0026) has 147 rows but only 130 unique instance_ids;
    # the 17 extras are duplicate retries with consistent judge_sonnet_success.
    # Filter to paired IDs, then dedupe by instance_id keeping the first occurrence.
    df_a_filtered = _filter_to_paired(df=df_a_raw, paired_ids=paired_ids)
    n_dups = len(df_a_filtered) - df_a_filtered[INSTANCE_ID].nunique()
    if n_dups > 0:
        # Sanity check: all duplicates have identical judge outcomes.
        per_id_unique = df_a_filtered.groupby(INSTANCE_ID)[JUDGE_SUCCESS].nunique().to_numpy()
        assert int(per_id_unique.max()) == 1, (
            "variant_a has duplicate rows with disagreeing judge_sonnet_success — "
            "cannot safely dedupe"
        )
    df_a = df_a_filtered.drop_duplicates(subset=[INSTANCE_ID], keep="first").copy()
    df_b = _filter_to_paired(df=df_b_raw, paired_ids=paired_ids)
    df_c = _filter_to_paired(df=df_c_raw, paired_ids=paired_ids)

    assert len(df_a) == EXISTING_PAIRED_N, f"variant_a after dedup: {len(df_a)}"
    assert len(df_b) == EXISTING_PAIRED_N, f"variant_b after filter: {len(df_b)}"
    assert len(df_c) == EXISTING_PAIRED_N, f"variant_c after filter: {len(df_c)}"

    # Variant A rows lack `plan_parser_recovery_path`.
    # After inversion, arm_b inherits this lack; arm_a (variant_b) and arm_c (variant_c) keep it.
    arm_b_df = df_a.rename(
        columns={
            JUDGE_SUCCESS: "arm_b_judge_success",
            "cost_usd": "arm_b_cost_usd",
        }
    )[[INSTANCE_ID, "subset", "arm_b_judge_success", "arm_b_cost_usd"]]

    arm_a_df = df_b.rename(
        columns={
            JUDGE_SUCCESS: "arm_a_judge_success",
            "cost_usd": "arm_a_cost_usd",
            RECOVERY_PATH: "arm_a_recovery_path",
        }
    )[
        [
            INSTANCE_ID,
            "subset",
            "arm_a_judge_success",
            "arm_a_cost_usd",
            "arm_a_recovery_path",
        ]
    ]

    arm_c_df = df_c.rename(
        columns={
            JUDGE_SUCCESS: "arm_c_judge_success",
            "cost_usd": "arm_c_cost_usd",
            RECOVERY_PATH: "arm_c_recovery_path",
        }
    )[
        [
            INSTANCE_ID,
            "subset",
            "arm_c_judge_success",
            "arm_c_cost_usd",
            "arm_c_recovery_path",
        ]
    ]

    # Merge on instance_id + subset.
    merged = arm_a_df.merge(
        arm_b_df,
        on=[INSTANCE_ID, "subset"],
        how="inner",
        validate="one_to_one",
    ).merge(
        arm_c_df,
        on=[INSTANCE_ID, "subset"],
        how="inner",
        validate="one_to_one",
    )

    assert len(merged) == EXISTING_PAIRED_N, f"merged paired frame size: {len(merged)}"

    # Coerce judge bool columns to plain bool.
    for col in ("arm_a_judge_success", "arm_b_judge_success", "arm_c_judge_success"):
        merged[col] = merged[col].fillna(False).astype(bool)

    n_per_subset = merged.groupby("subset", observed=True).size().to_dict()
    for k, expected in EXISTING_PER_SUBSET.items():
        actual = int(n_per_subset.get(k, 0))
        assert actual == expected, f"subset {k}: got {actual}, expected {expected}"

    # Discordance: arm_a vs arm_b.
    a_pass = merged["arm_a_judge_success"]
    b_pass = merged["arm_b_judge_success"]
    discordant_b_wins = int(((~a_pass) & b_pass).sum())
    discordant_a_wins = int((a_pass & (~b_pass)).sum())
    n_discordant = discordant_b_wins + discordant_a_wins
    discordance_rate = n_discordant / EXISTING_PAIRED_N

    return PairedFrame(
        df=merged,
        n_total=EXISTING_PAIRED_N,
        n_per_subset={k: int(v) for k, v in n_per_subset.items()},
        n_discordant_a_vs_b=n_discordant,
        discordant_b_wins=discordant_b_wins,
        discordant_a_wins=discordant_a_wins,
        discordance_rate=discordance_rate,
    )


def main() -> None:
    frame = load_paired_frame()
    print(f"Loaded paired frame: n={frame.n_total}")
    print(f"  per_subset: {frame.n_per_subset}")
    print(
        f"  discordant: {frame.n_discordant_a_vs_b} "
        f"(b_wins={frame.discordant_b_wins}, a_wins={frame.discordant_a_wins})"
    )
    print(f"  discordance_rate: {frame.discordance_rate:.4f}")


if __name__ == "__main__":
    main()
