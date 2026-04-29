#!/usr/bin/env python3
"""
CoT Deliberation + Hint Compliance + Cross-difficulty Few-shot
==============================================================

  Exp A — CoT Deliberation:
           Does chain-of-thought reasoning before planning replicate the scale hint
           effect? Two new conditions on 40 stratified tasks:
             F = CoT-only  (think about complexity, then generate plan)
             G = CoT + scale hint  (think + annotator-provided hint)
           If F ≈ C(step_aware), the gain is from deliberation, not hint content.
           If F < C ≈ G, the semantic content of the hint is what matters.

  Exp B — Hint Compliance Audit (analytical, zero new calls):
           Measure whether models actually follow step-count hints.
           For each task with a step_aware plan, compute:
             compliance_error = |len(plan_step_aware) - expected_n_steps|
           Then split quality scores by low/mid/high compliance groups.
           If compliant plans score higher → hint content is causally effective.
           If non-compliant plans score just as well → model ignores numeric hints.

  Exp D — Cross-difficulty Few-shot Transfer:
           Shows 2 examples from the *wrong* difficulty level to test whether
           template-copying (structural mimicry) explains the few-shot advantage.
             F_up   = show Expert examples for Trivial/Easy tasks (over-scaffold)
             F_down = show Trivial examples for Hard/Expert tasks (under-scaffold)
           If mismatched examples still help → advantage is from template structure.
           If mismatched examples hurt vs baseline → advantage is from calibration.

Outputs:
  data/scale_awareness/cot_results.jsonl
  data/scale_awareness/cross_fewshot_results.jsonl
  data/scale_awareness/COT_COMPLIANCE_REPORT.md
"""

from __future__ import annotations

import math
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from scripts.run_diploma_experiments import (
    append_result,
    avg,
    blind_judge,
    cohens_d,
    get_task_context,
    load_done_keys,
    load_jsonl,
    t_stat,
)
from scripts.scale_awareness_experiment import (
    cli_call,
    extract_steps,
    load_annotated,
)

OUT_DIR = Path("data/scale_awareness")
RESULTS_JSONL = OUT_DIR / "results.jsonl"
ABLATION_JSONL = OUT_DIR / "ablation_results.jsonl"
COT_JSONL = OUT_DIR / "cot_results.jsonl"
CROSSFS_JSONL = OUT_DIR / "cross_fewshot_results.jsonl"
REPORT_MD = OUT_DIR / "COT_COMPLIANCE_REPORT.md"


# ── Exp A: CoT prompts ────────────────────────────────────────────────────────

COT_ONLY = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

Before writing the plan, briefly consider (internally):
- How difficult is this problem?
- How many steps would a thorough solution need?
- What types of reasoning steps are required?

Problem: {problem}

JSON output only:"""


COT_PLUS_HINT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

Before writing the plan, briefly consider (internally):
- How difficult is this problem?
- How many steps would a thorough solution need?
- What types of reasoning steps are required?

SCALE CONTEXT (use to guide your deliberation):
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps}
- Expected step composition:
{step_type_lines}

Problem: {problem}

JSON output only:"""


@dataclass
class CotResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    expected_n_steps: int
    condition: str  # "F" or "G"
    plan: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


# ── Exp D: Cross-difficulty few-shot prompts ──────────────────────────────────

CROSS_FEWSHOT_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

Here are two examples of well-structured plans:

--- Example 1 ({ex1_label}) ---
Problem: {ex1_problem}
Plan:
{ex1_plan}

--- Example 2 ({ex2_label}) ---
Problem: {ex2_problem}
Plan:
{ex2_plan}

---

Now generate a plan for the following problem:

Problem: {problem}

JSON output only:"""


@dataclass
class CrossFewshotResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    transfer_dir: str  # "up" (easy task, expert examples) or "down" (hard task, trivial examples)
    ex1_task_id: str = ""
    ex2_task_id: str = ""
    ex1_label: str = ""
    ex2_label: str = ""
    plan: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


def _annotation_plan_text(task: dict) -> str:
    nodes = (task.get("steps") or {}).get("nodes", [])
    lines = [f"{i + 1}. {n.get('label', '')} — {n.get('detail', '')}" for i, n in enumerate(nodes)]
    return "\n".join(lines) if lines else "(no plan available)"


# ── Exp A: run ────────────────────────────────────────────────────────────────


def run_exp_a():
    """CoT deliberation conditions F and G on 40 stratified tasks."""
    print("\n=== Exp A: CoT Deliberation ===")
    done = load_done_keys(COT_JSONL, ["task_id", "condition"])

    tasks = load_annotated()
    # Stratified sample of 40 tasks (10 per difficulty level, balanced)
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        lbl = t["difficulty"].get("overall_label", "?")
        by_label[lbl].append(t)

    sample: list[dict] = []
    for lbl in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        pool = by_label.get(lbl, [])
        # 8 per label = 40 total
        sample.extend(pool[:8])

    print(f"  Sample: {len(sample)} tasks | Conditions: F, G")
    work = [(t, cond) for t in sample for cond in ["F", "G"]]
    todo = [(t, c) for t, c in work if (t["task_id"], c) not in done]
    print(f"  Already done: {len(done)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="CoT", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        rec = CotResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            expected_n_steps=ctx["expected_n_steps"],
            condition=cond,
        )

        try:
            if cond == "F":
                prompt = COT_ONLY.format(problem=ctx["problem"])
            else:  # G
                prompt = COT_PLUS_HINT.format(
                    problem=ctx["problem"],
                    label=ctx["label"],
                    score=ctx["score"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                )
            raw = cli_call(prompt)
            rec.plan = extract_steps(raw)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        if rec.plan:
            try:
                scores = blind_judge(ctx["problem"], rec.plan)
                rec.overall = scores.get("overall")
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(COT_JSONL, rec)
        time.sleep(1)

    print("  Exp A done.")


# ── Exp D: run ────────────────────────────────────────────────────────────────


def run_exp_d():
    """Cross-difficulty few-shot on 40 tasks (20 up-transfer + 20 down-transfer)."""
    print("\n=== Exp D: Cross-difficulty Few-shot Transfer ===")
    done = load_done_keys(CROSSFS_JSONL, ["task_id", "transfer_dir"])

    tasks = load_annotated()
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        lbl = t["difficulty"].get("overall_label", "?")
        by_label[lbl].append(t)

    # "up" transfer: Trivial/Easy tasks shown Expert examples (over-scaffolded)
    up_targets = (by_label.get("Trivial", []) + by_label.get("Easy", []))[:20]
    up_examples = by_label.get("Expert", [])

    # "down" transfer: Hard/Expert tasks shown Trivial examples (under-scaffolded)
    down_targets = (by_label.get("Hard", []) + by_label.get("Expert", []))[:20]
    down_examples = by_label.get("Trivial", [])

    work = [(t, "up", up_examples) for t in up_targets] + [
        (t, "down", down_examples) for t in down_targets
    ]
    todo = [(t, d, pool) for t, d, pool in work if (t["task_id"], d) not in done]
    print(f"  Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, transfer_dir, example_pool in tqdm(todo, desc="Cross-FS", unit="task"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        # pick 2 examples from pool (exclude the task itself)
        pool = [e for e in example_pool if e["task_id"] != task["task_id"]]
        if len(pool) < 2:
            rec = CrossFewshotResult(
                task_id=task["task_id"],
                benchmark=task["benchmark"],
                difficulty_label=diff.get("overall_label", "?"),
                difficulty_score=float(diff.get("overall_difficulty", 0)),
                transfer_dir=transfer_dir,
            )
            rec.errors.append("not enough examples in pool")
            append_result(CROSSFS_JSONL, rec)
            continue

        ex1, ex2 = pool[0], pool[1]
        ex1_plan = _annotation_plan_text(ex1)
        ex2_plan = _annotation_plan_text(ex2)

        rec = CrossFewshotResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            transfer_dir=transfer_dir,
            ex1_task_id=ex1["task_id"],
            ex2_task_id=ex2["task_id"],
            ex1_label=ex1["difficulty"].get("overall_label", "?"),
            ex2_label=ex2["difficulty"].get("overall_label", "?"),
        )

        try:
            prompt = CROSS_FEWSHOT_PROMPT.format(
                problem=ctx["problem"],
                ex1_label=rec.ex1_label,
                ex1_problem=(ex1.get("problem") or "")[:500],
                ex1_plan=ex1_plan[:600],
                ex2_label=rec.ex2_label,
                ex2_problem=(ex2.get("problem") or "")[:500],
                ex2_plan=ex2_plan[:600],
            )
            raw = cli_call(prompt)
            rec.plan = extract_steps(raw)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        if rec.plan:
            try:
                scores = blind_judge(ctx["problem"], rec.plan)
                rec.overall = scores.get("overall")
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(CROSSFS_JSONL, rec)
        time.sleep(1)

    print("  Exp D done.")


# ── Exp B: Hint Compliance Audit (analytical) ─────────────────────────────────


def run_exp_b_analytical(report_parts: list[str]) -> None:
    """
    Measure how well step_aware plans comply with hint step counts.
    Uses existing results.jsonl + ablation_results.jsonl.
    Returns summary as markdown section appended to report_parts.
    """
    print("\n=== Exp B: Hint Compliance Audit (analytical) ===")

    # Load main results for step_aware plans
    main_rows = load_jsonl(RESULTS_JSONL)
    task_expected: dict[str, int] = {}
    step_aware_plans: dict[str, list] = {}
    step_aware_scores: dict[str, float] = {}
    baseline_scores: dict[str, float] = {}

    for row in main_rows:
        tid = row["task_id"]
        expected = row.get("expected_plan_len") or 5
        task_expected[tid] = expected
        step_aware_plans[tid] = row.get("plan_step_aware", [])
        s_sa = row.get("score_step_aware")
        s_ba = row.get("score_baseline")
        if s_sa is not None:
            step_aware_scores[tid] = float(s_sa)
        if s_ba is not None:
            baseline_scores[tid] = float(s_ba)

    # Compute compliance error per task
    compliance: dict[str, dict] = {}
    for tid, plan in step_aware_plans.items():
        if not plan:
            continue
        expected = task_expected.get(tid, 5)
        actual = len(plan)
        error = abs(actual - expected)
        compliance[tid] = {
            "expected": expected,
            "actual": actual,
            "error": error,
            "score_sa": step_aware_scores.get(tid),
            "score_ba": baseline_scores.get(tid),
        }

    errors_all = [v["error"] for v in compliance.values()]
    avg_err = avg(errors_all)
    perfect_compliance = sum(1 for e in errors_all if e == 0)
    within_1 = sum(1 for e in errors_all if e <= 1)
    n = len(errors_all)

    print(f"  {n} tasks with step_aware plans")
    print(f"  Avg compliance error: {avg_err:.2f} steps")
    print(f"  Perfect (err=0): {perfect_compliance}/{n} ({100 * perfect_compliance / n:.0f}%)")
    print(f"  Within 1 step: {within_1}/{n} ({100 * within_1 / n:.0f}%)")

    # Split by compliance group
    low_comp = [v for v in compliance.values() if v["error"] >= 3]
    mid_comp = [v for v in compliance.values() if v["error"] == 1 or v["error"] == 2]
    high_comp = [v for v in compliance.values() if v["error"] == 0]

    def group_stats(group):
        scores_sa = [v["score_sa"] for v in group if v["score_sa"] is not None]
        scores_ba = [v["score_ba"] for v in group if v["score_ba"] is not None]
        delta = None
        if scores_sa and scores_ba and len(scores_sa) == len(scores_ba):
            delta = avg(scores_sa) - avg(scores_ba)
        return avg(scores_sa), avg(scores_ba), delta, len(group)

    hi_sa, hi_ba, hi_d, hi_n = group_stats(high_comp)
    mi_sa, mi_ba, mi_d, mi_n = group_stats(mid_comp)
    lo_sa, lo_ba, lo_d, lo_n = group_stats(low_comp)

    def fmt(v):
        return f"{v:.2f}" if v is not None else "—"

    # Also load C2 (count-only ablation) compliance
    ablation_rows = load_jsonl(ABLATION_JSONL)
    c2_rows = [r for r in ablation_rows if r.get("condition") == "C2"]
    c2_compliance = []
    for row in c2_rows:
        tid = row["task_id"]
        expected = task_expected.get(tid, 5)
        actual = len(row.get("plan", []))
        c2_compliance.append(abs(actual - expected))

    c2_avg_err = avg(c2_compliance) if c2_compliance else None
    c2_perfect = sum(1 for e in c2_compliance if e == 0) if c2_compliance else 0

    # Correlation: compliance error vs quality gain
    # For each task: gain = score_sa - score_ba; error = compliance error
    paired = [
        (compliance[tid]["error"], compliance[tid]["score_sa"] - compliance[tid]["score_ba"])
        for tid in compliance
        if compliance[tid]["score_sa"] is not None and compliance[tid]["score_ba"] is not None
    ]
    if paired:
        errs_p = [x[0] for x in paired]
        gains_p = [x[1] for x in paired]
        r_comp = pearson_r(errs_p, gains_p)
    else:
        r_comp = None

    section = f"""
## Exp B — Hint Compliance Audit (Analytical)

**Question:** Does the model actually follow the step-count hint in condition C (step_aware)?
And does compliance predict quality gain?

### Step-count compliance (condition C, all {n} tasks)

| Metric | Value |
|--------|-------|
| Avg compliance error (|actual − hint|) | {fmt(avg_err)} steps |
| Perfect compliance (error = 0) | {perfect_compliance}/{n} ({100 * perfect_compliance / n:.0f}%) |
| Within 1 step | {within_1}/{n} ({100 * within_1 / n:.0f}%) |
| Avg error in count-only (C2) ablation | {fmt(c2_avg_err)} steps |
| C2 perfect compliance | {c2_perfect}/{len(c2_compliance)} ({100 * c2_perfect / len(c2_compliance):.0f}%) if c2_compliance else "—" |

### Quality gain by compliance group

| Compliance group | N | SA score | Baseline | Δ |
|-----------------|---|----------|----------|---|
| High (err=0) | {hi_n} | {fmt(hi_sa)} | {fmt(hi_ba)} | {fmt(hi_d)} |
| Mid  (err=1-2) | {mi_n} | {fmt(mi_sa)} | {fmt(mi_ba)} | {fmt(mi_d)} |
| Low  (err≥3) | {lo_n} | {fmt(lo_sa)} | {fmt(lo_ba)} | {fmt(lo_d)} |

Pearson r(compliance_error, quality_gain) = {fmt(r_comp)}

**Interpretation:**
- If r < 0 and high-compliance group shows larger Δ → model leverages hint numerically.
- If r ≈ 0 → step count in the plan is decoupled from hint; any gain is from hint framing.
"""
    report_parts.append(section)
    print("  Exp B done.")


def pearson_r(xs: list, ys: list) -> float | None:
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


# ── Report ────────────────────────────────────────────────────────────────────


def generate_report():
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    parts: list[str] = [f"# CoT, Compliance & Cross-FS Report\n\n**Generated:** {ts}\n\n---\n"]

    # Exp A results
    cot_rows = load_jsonl(COT_JSONL)
    if cot_rows:
        f_rows = [r for r in cot_rows if r.get("condition") == "F"]
        g_rows = [r for r in cot_rows if r.get("condition") == "G"]

        f_scores = [r["overall"] for r in f_rows if r.get("overall") is not None]
        g_scores = [r["overall"] for r in g_rows if r.get("overall") is not None]

        # load baseline and step_aware scores for the same tasks
        main_rows = load_jsonl(RESULTS_JSONL)
        main_by_id = {r["task_id"]: r for r in main_rows}

        cot_tids = {r["task_id"] for r in cot_rows}
        base_scores_cot = [
            main_by_id[tid]["score_baseline"]
            for tid in cot_tids
            if tid in main_by_id and main_by_id[tid].get("score_baseline") is not None
        ]
        step_scores_cot = [
            main_by_id[tid]["score_step_aware"]
            for tid in cot_tids
            if tid in main_by_id and main_by_id[tid].get("score_step_aware") is not None
        ]

        tf, pf = t_stat(f_scores, base_scores_cot) if base_scores_cot else (0, 1)
        tg, pg = t_stat(g_scores, base_scores_cot) if base_scores_cot else (0, 1)
        df = cohens_d(f_scores, base_scores_cot) if base_scores_cot else None
        dg = cohens_d(g_scores, base_scores_cot) if base_scores_cot else None

        def fmt(v):
            return f"{v:.2f}" if v is not None else "—"

        def fmtp(v):
            return ("< 0.001" if v < 0.001 else f"{v:.3f}") if v is not None else "—"

        # by difficulty
        diff_labels = ["Trivial", "Easy", "Medium", "Hard", "Expert"]
        diff_table = []
        for lbl in diff_labels:
            f_lbl = [
                r["overall"]
                for r in f_rows
                if r.get("difficulty_label") == lbl and r.get("overall") is not None
            ]
            g_lbl = [
                r["overall"]
                for r in g_rows
                if r.get("difficulty_label") == lbl and r.get("overall") is not None
            ]
            base_lbl = [
                main_by_id[r["task_id"]]["score_baseline"]
                for r in f_rows
                if r.get("difficulty_label") == lbl
                and r["task_id"] in main_by_id
                and main_by_id[r["task_id"]].get("score_baseline") is not None
            ]
            diff_table.append((lbl, avg(base_lbl), avg(f_lbl), avg(g_lbl), len(f_lbl)))

        rows_table = "\n".join(
            f"| {lbl} | {fmt(ba)} | {fmt(fa)} | {fmt(ga)} | {fmt((fa - ba) if fa and ba else None)} | {fmt((ga - ba) if ga and ba else None)} | {n} |"
            for lbl, ba, fa, ga, n in diff_table
        )

        parts.append(f"""
## Exp A — CoT Deliberation

**Question:** Is the scale hint advantage driven by deliberation overhead (any "think first"
instruction) or by the specific semantic content of the annotator-provided hint?

**Conditions on {len(cot_tids)} tasks:**
- F = CoT-only (think about complexity, then plan — no hint content)
- G = CoT + scale hint (think + annotator-provided difficulty/step info)
- Comparison: A (baseline, plain generation), C (step_aware, same hint as G but no CoT prefix)

### Overall scores

| Condition | Avg score | N | vs baseline t | p | Cohen's d |
|-----------|-----------|---|--------------|---|-----------|
| A baseline | {fmt(avg(base_scores_cot))} | {len(base_scores_cot)} | — | — | — |
| F CoT-only | {fmt(avg(f_scores))} | {len(f_scores)} | {fmt(tf)} | {fmtp(pf)} | {fmt(df)} |
| G CoT+hint | {fmt(avg(g_scores))} | {len(g_scores)} | {fmt(tg)} | {fmtp(pg)} | {fmt(dg)} |

### By difficulty label

| Difficulty | A baseline | F CoT-only | G CoT+hint | Δ F−A | Δ G−A | N |
|------------|-----------|-----------|-----------|-------|-------|---|
{rows_table}

**Interpretation guide:**
- F ≈ C and F > A → deliberation alone explains the gain (not hint content)
- G > F > A → hint content adds beyond deliberation overhead
- F ≈ A < G → deliberation without content is inert; specific hint information is what matters
""")

    # Exp B
    run_exp_b_analytical(parts)

    # Exp D results
    cf_rows = load_jsonl(CROSSFS_JSONL)
    if cf_rows:
        up_rows = [r for r in cf_rows if r.get("transfer_dir") == "up"]
        down_rows = [r for r in cf_rows if r.get("transfer_dir") == "down"]

        up_scores = [r["overall"] for r in up_rows if r.get("overall") is not None]
        down_scores = [r["overall"] for r in down_rows if r.get("overall") is not None]

        main_rows = load_jsonl(RESULTS_JSONL)
        main_by_id = {r["task_id"]: r for r in main_rows}

        # same-difficulty fewshot scores (from Exp 11)
        fewshot_rows = load_jsonl(OUT_DIR / "fewshot_results.jsonl")
        fewshot_by_id = {r["task_id"]: r.get("overall") for r in fewshot_rows}

        up_tids = {r["task_id"] for r in up_rows}
        down_tids = {r["task_id"] for r in down_rows}

        def base_for(tids):
            return [
                main_by_id[tid]["score_baseline"]
                for tid in tids
                if tid in main_by_id and main_by_id[tid].get("score_baseline") is not None
            ]

        def fs_for(tids):
            return [
                fewshot_by_id[tid]
                for tid in tids
                if tid in fewshot_by_id and fewshot_by_id[tid] is not None
            ]

        def fmt(v):
            return f"{v:.2f}" if v is not None else "—"

        def fmtp(v):
            return ("< 0.001" if v < 0.001 else f"{v:.3f}") if v is not None else "—"

        t_up, p_up = t_stat(up_scores, base_for(up_tids)) if base_for(up_tids) else (0, 1)
        t_down, p_down = t_stat(down_scores, base_for(down_tids)) if base_for(down_tids) else (0, 1)
        d_up = cohens_d(up_scores, base_for(up_tids)) if base_for(up_tids) else None
        d_down = cohens_d(down_scores, base_for(down_tids)) if base_for(down_tids) else None

        parts.append(f"""
## Exp D — Cross-difficulty Few-shot Transfer

**Question:** Does the few-shot advantage (Exp 11, d=0.64) come from structural template
copying, or from seeing calibrated difficulty-appropriate examples?

**Design:**
- F_up   (n={len(up_rows)}): Trivial/Easy target tasks shown **Expert** examples (over-scaffolded)
- F_down (n={len(down_rows)}): Hard/Expert target tasks shown **Trivial** examples (under-scaffolded)
- Compare to A (baseline) and F_matched (same-difficulty few-shot from Exp 11)

### Cross-difficulty transfer vs baseline

| Condition | Tasks | Avg score | vs baseline t | p | Cohen's d |
|-----------|-------|-----------|--------------|---|-----------|
| A baseline (up-target tasks) | {len(base_for(up_tids))} | {fmt(avg(base_for(up_tids)))} | — | — | — |
| F_up (Expert examples for Easy tasks) | {len(up_scores)} | {fmt(avg(up_scores))} | {fmt(t_up)} | {fmtp(p_up)} | {fmt(d_up)} |
| A baseline (down-target tasks) | {len(base_for(down_tids))} | {fmt(avg(base_for(down_tids)))} | — | — | — |
| F_down (Trivial examples for Hard tasks) | {len(down_scores)} | {fmt(avg(down_scores))} | {fmt(t_down)} | {fmtp(p_down)} | {fmt(d_down)} |

### Cross vs same-difficulty few-shot

| Group | Matched FS (Exp 11) | Cross FS | Δ |
|-------|---------------------|----------|---|
| Up transfer (Trivial/Easy targets) | {fmt(avg(fs_for(up_tids)))} | {fmt(avg(up_scores))} | {fmt((avg(up_scores) - avg(fs_for(up_tids))) if avg(up_scores) and avg(fs_for(up_tids)) else None)} |
| Down transfer (Hard/Expert targets) | {fmt(avg(fs_for(down_tids)))} | {fmt(avg(down_scores))} | {fmt((avg(down_scores) - avg(fs_for(down_tids))) if avg(down_scores) and avg(fs_for(down_tids)) else None)} |

**Interpretation guide:**
- Cross ≈ Matched → few-shot advantage is template/format copying, not calibration
- Cross < Matched → difficulty-matched calibration is essential to the few-shot gain
- F_down > A even when examples are "too simple" → structural mimicry hypothesis supported
""")

    REPORT_MD.write_text("".join(parts), encoding="utf-8")
    print(f"\n  Report written → {REPORT_MD}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "a"):
        run_exp_a()
    if mode in ("all", "d"):
        run_exp_d()

    print("\n=== Generating report ===")
    generate_report()
    print("Done.")
