"""Analysis 3: infrastructure-vs-genuine-failure audit.

Splits failures into:
* infrastructure (timeouts, runtime errors, parser unknown, malformed-plan errors)
* genuine model failure (judged-fail rows with parser path clean/reprompt/json_fallback,
  plus parser all_failed which is a genuine plan-malformation)
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.t0031_rq1_rq4_no_new_api_salvage.code.constants import T0026_HARD_FAILURES_PRE_FIX
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.load_paired_outputs import load_paired_frame
from tasks.t0031_rq1_rq4_no_new_api_salvage.code.paths import (
    LOG_AUDIT_BAR_PNG,
    LOG_AUDIT_JSON,
    RESULTS_DATA_DIR,
    RESULTS_IMAGES_DIR,
)


@dataclass(frozen=True, slots=True)
class ArmAudit:
    arm_label: str
    n_total: int
    judged_fail: int
    judged_pass: int
    recovery_clean: int
    recovery_reprompt: int
    recovery_json_fallback: int
    recovery_all_failed: int
    recovery_unknown: int
    infra_failures: int  # parser unknown rows that are judged_fail
    genuine_failures: int  # judged-fail with clean / reprompt / json_fallback / all_failed
    infra_unknown_total: int  # all unknown rows (regardless of pass/fail)


def _audit_arm_with_recovery(
    *,
    df: pd.DataFrame,
    recovery_col: str,
    judge_col: str,
    label: str,
) -> ArmAudit:
    n_total = len(df)
    judged = df[judge_col].astype(bool)
    judged_pass = int(judged.sum())
    judged_fail = int((~judged).sum())
    rec = df[recovery_col].fillna("unknown")
    counts: dict[str, int] = rec.value_counts().to_dict()
    clean = int(counts.get("clean", 0))
    reprompt = int(counts.get("reprompt", 0))
    json_fb = int(counts.get("json_fallback", 0))
    all_failed = int(counts.get("all_failed", 0))
    unknown = int(counts.get("unknown", 0))

    # Infra failures (post-fix): unknown rows that are judged_fail are treated as
    # infrastructure noise (the cost-tracker boundary that swallowed the recovery
    # label still produced a trajectory and judged outcome — see research_code.md).
    fail_unknown = int(((~judged) & (rec == "unknown")).sum())
    fail_clean = int(((~judged) & (rec == "clean")).sum())
    fail_reprompt = int(((~judged) & (rec == "reprompt")).sum())
    fail_json_fb = int(((~judged) & (rec == "json_fallback")).sum())
    fail_all_failed = int(((~judged) & (rec == "all_failed")).sum())

    infra = fail_unknown
    genuine = fail_clean + fail_reprompt + fail_json_fb + fail_all_failed

    return ArmAudit(
        arm_label=label,
        n_total=n_total,
        judged_fail=judged_fail,
        judged_pass=judged_pass,
        recovery_clean=clean,
        recovery_reprompt=reprompt,
        recovery_json_fallback=json_fb,
        recovery_all_failed=all_failed,
        recovery_unknown=unknown,
        infra_failures=infra,
        genuine_failures=genuine,
        infra_unknown_total=unknown,
    )


def _audit_arm_no_recovery(*, df: pd.DataFrame, judge_col: str, label: str) -> ArmAudit:
    """Arm B (=variant_a) has no parser recovery field. All fails count as 'genuine' here.

    The arm-B (scope-aware ReAct) infra failures are captured in the t0026 pre-fix layer
    via timeouts and runtime errors — not in t0027 row-level data.
    """

    n_total = len(df)
    judged = df[judge_col].astype(bool)
    judged_pass = int(judged.sum())
    judged_fail = int((~judged).sum())
    return ArmAudit(
        arm_label=label,
        n_total=n_total,
        judged_fail=judged_fail,
        judged_pass=judged_pass,
        recovery_clean=0,
        recovery_reprompt=0,
        recovery_json_fallback=0,
        recovery_all_failed=0,
        recovery_unknown=0,
        infra_failures=0,
        genuine_failures=judged_fail,
        infra_unknown_total=0,
    )


def _draw_failure_breakdown(
    *,
    pre_fix: dict[str, dict[str, int]],
    post_fix_infra: dict[str, int],
    post_fix_genuine: dict[str, int],
    output_path: str,
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left subplot: pre-fix t0026 (per t0026 internal labels, mapped to t0031 arms).
    pre_labels = ["arm_a (PaS v2)", "arm_b (scope-aware)", "arm_c (mismatched)"]
    # t0026 B = arm_a, t0026 A = arm_b, t0026 C = arm_c
    pre_infra = [
        pre_fix["b_t0026_plan_and_solve_v2"]["timeouts"]
        + pre_fix["b_t0026_plan_and_solve_v2"]["runtime_errors"],
        pre_fix["a_t0026_scope_aware"]["timeouts"]
        + pre_fix["a_t0026_scope_aware"]["runtime_errors"],
        pre_fix["c_t0026_mismatched"]["timeouts"] + pre_fix["c_t0026_mismatched"]["runtime_errors"],
    ]
    pre_parser = [
        pre_fix["b_t0026_plan_and_solve_v2"]["malformed_plan_errors"],
        0,
        0,
    ]
    x = np.arange(len(pre_labels))
    axes[0].bar(x, pre_infra, label="timeouts + runtime errors", color="#FF6B6B")
    axes[0].bar(
        x,
        pre_parser,
        bottom=pre_infra,
        label="MalformedPlanError (parser)",
        color="#FFB347",
    )
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(pre_labels, rotation=15, ha="right")
    axes[0].set_ylabel("hard failures (out of 147)")
    axes[0].set_title("Pre-fix (t0026): infra-only hard failures")
    axes[0].legend(loc="upper left")
    axes[0].grid(axis="y", alpha=0.3)

    # Right subplot: post-fix t0027 (paired N=130).
    post_labels = ["arm_a (PaS v3)", "arm_b (scope-aware)", "arm_c (mismatched v2)"]
    arms_post = ["arm_a", "arm_b", "arm_c"]
    infra_vals = [post_fix_infra[a] for a in arms_post]
    genuine_vals = [post_fix_genuine[a] for a in arms_post]
    x2 = np.arange(len(post_labels))
    axes[1].bar(x2, infra_vals, label="infra (parser unknown, judged-fail)", color="#FF6B6B")
    axes[1].bar(
        x2,
        genuine_vals,
        bottom=infra_vals,
        label="genuine (clean/reprompt/json_fb/all_failed, judged-fail)",
        color="#4ECDC4",
    )
    axes[1].set_xticks(x2)
    axes[1].set_xticklabels(post_labels, rotation=15, ha="right")
    axes[1].set_ylabel("failures on 130 paired set")
    axes[1].set_title("Post-fix (t0027): infra vs genuine on paired set")
    axes[1].legend(loc="upper left")
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("Failure breakdown: pre-fix t0026 vs post-fix t0027", fontsize=12)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    frame = load_paired_frame()
    df = frame.df

    # Build per-arm DataFrame slices for the post-fix audit.
    arm_a_df = df[["instance_id", "subset", "arm_a_judge_success", "arm_a_recovery_path"]]
    arm_c_df = df[["instance_id", "subset", "arm_c_judge_success", "arm_c_recovery_path"]]
    arm_b_df = df[["instance_id", "subset", "arm_b_judge_success"]]

    audit_a = _audit_arm_with_recovery(
        df=arm_a_df,
        recovery_col="arm_a_recovery_path",
        judge_col="arm_a_judge_success",
        label="arm_a (Plan-and-Solve v3 baseline)",
    )
    audit_c = _audit_arm_with_recovery(
        df=arm_c_df,
        recovery_col="arm_c_recovery_path",
        judge_col="arm_c_judge_success",
        label="arm_c (matched-mismatch v2)",
    )
    audit_b = _audit_arm_no_recovery(
        df=arm_b_df,
        judge_col="arm_b_judge_success",
        label="arm_b (scope-aware ReAct)",
    )

    payload = {
        "spec_version": "1",
        "task_id": "t0031_rq1_rq4_no_new_api_salvage",
        "pre_fix_t0026": {
            "labels_note": (
                "t0026 internal labels: A=scope-aware (=arm_b), B=plan_and_solve_v2 (=arm_a), "
                "C=mismatched (=arm_c). All counts are out of 147 attempted instances."
            ),
            "arm_a_pre_fix": {
                **T0026_HARD_FAILURES_PRE_FIX["b_t0026_plan_and_solve_v2"],
                "infra_total": T0026_HARD_FAILURES_PRE_FIX["b_t0026_plan_and_solve_v2"]["timeouts"]
                + T0026_HARD_FAILURES_PRE_FIX["b_t0026_plan_and_solve_v2"]["runtime_errors"]
                + T0026_HARD_FAILURES_PRE_FIX["b_t0026_plan_and_solve_v2"]["malformed_plan_errors"],
            },
            "arm_b_pre_fix": {
                **T0026_HARD_FAILURES_PRE_FIX["a_t0026_scope_aware"],
                "infra_total": T0026_HARD_FAILURES_PRE_FIX["a_t0026_scope_aware"]["timeouts"]
                + T0026_HARD_FAILURES_PRE_FIX["a_t0026_scope_aware"]["runtime_errors"]
                + T0026_HARD_FAILURES_PRE_FIX["a_t0026_scope_aware"]["malformed_plan_errors"],
            },
            "arm_c_pre_fix": {
                **T0026_HARD_FAILURES_PRE_FIX["c_t0026_mismatched"],
                "infra_total": T0026_HARD_FAILURES_PRE_FIX["c_t0026_mismatched"]["timeouts"]
                + T0026_HARD_FAILURES_PRE_FIX["c_t0026_mismatched"]["runtime_errors"]
                + T0026_HARD_FAILURES_PRE_FIX["c_t0026_mismatched"]["malformed_plan_errors"],
            },
        },
        "post_fix_t0027": {
            "n_paired": frame.n_total,
            "labels_note": (
                "t0031 inversion applied: arm_a=PaS v3 baseline, arm_b=scope-aware ReAct, "
                "arm_c=matched-mismatch v2."
            ),
            "arm_a": {
                "n_total": audit_a.n_total,
                "judged_pass": audit_a.judged_pass,
                "judged_fail": audit_a.judged_fail,
                "recovery_clean": audit_a.recovery_clean,
                "recovery_reprompt": audit_a.recovery_reprompt,
                "recovery_json_fallback": audit_a.recovery_json_fallback,
                "recovery_all_failed": audit_a.recovery_all_failed,
                "recovery_unknown": audit_a.recovery_unknown,
                "infra_failures": audit_a.infra_failures,
                "genuine_failures": audit_a.genuine_failures,
            },
            "arm_b": {
                "n_total": audit_b.n_total,
                "judged_pass": audit_b.judged_pass,
                "judged_fail": audit_b.judged_fail,
                "recovery_unknown": audit_b.recovery_unknown,
                "infra_failures": audit_b.infra_failures,
                "genuine_failures": audit_b.genuine_failures,
                "note": (
                    "arm_b rows from t0026 variant_a have no parser_recovery_path field; "
                    "infra noise for arm_b is captured by the t0026 pre-fix counts (12 "
                    "timeouts + 1 runtime error)."
                ),
            },
            "arm_c": {
                "n_total": audit_c.n_total,
                "judged_pass": audit_c.judged_pass,
                "judged_fail": audit_c.judged_fail,
                "recovery_clean": audit_c.recovery_clean,
                "recovery_reprompt": audit_c.recovery_reprompt,
                "recovery_json_fallback": audit_c.recovery_json_fallback,
                "recovery_all_failed": audit_c.recovery_all_failed,
                "recovery_unknown": audit_c.recovery_unknown,
                "infra_failures": audit_c.infra_failures,
                "genuine_failures": audit_c.genuine_failures,
            },
        },
    }
    LOG_AUDIT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    post_fix_infra = {
        "arm_a": audit_a.infra_failures,
        "arm_b": audit_b.infra_failures,
        "arm_c": audit_c.infra_failures,
    }
    post_fix_genuine = {
        "arm_a": audit_a.genuine_failures,
        "arm_b": audit_b.genuine_failures,
        "arm_c": audit_c.genuine_failures,
    }
    _draw_failure_breakdown(
        pre_fix=T0026_HARD_FAILURES_PRE_FIX,
        post_fix_infra=post_fix_infra,
        post_fix_genuine=post_fix_genuine,
        output_path=str(LOG_AUDIT_BAR_PNG),
    )
    print(f"Wrote {LOG_AUDIT_JSON}")
    print(f"Wrote {LOG_AUDIT_BAR_PNG}")
    print(
        f"  arm_a: infra={audit_a.infra_failures}, genuine={audit_a.genuine_failures}, "
        f"unknown_total={audit_a.recovery_unknown}"
    )
    print(
        f"  arm_b: infra={audit_b.infra_failures}, "
        f"genuine={audit_b.genuine_failures} (no recovery field)"
    )
    print(
        f"  arm_c: infra={audit_c.infra_failures}, genuine={audit_c.genuine_failures}, "
        f"unknown_total={audit_c.recovery_unknown}"
    )


if __name__ == "__main__":
    main()
