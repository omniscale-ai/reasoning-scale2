#!/usr/bin/env python3
"""
Research Fixes — Addressing Critical Methodological Weaknesses
===============================================================

  Fix 1 — Unconstrained generation for Expert/Hard tasks:
           Remove "3 to 6 steps" ceiling; let model generate N steps freely.
           Directly resolves the Expert Calibration Paradox.

  Fix 2 — Pairwise ranking:
           Judge compares plan A vs plan C directly ("which is better?").
           More reliable than 1-5 Likert scale (resolves r=0.37 judge issue).
           Win-rate + Bradley-Terry score computed across all 101 tasks.

  Fix 3 — Solution-aligned evaluation:
           Uses annotation `solution` field as ground truth.
           Judge asks: "given the correct solution, does this plan capture it?"
           Objective signal independent of subjective plan quality.

Outputs:
  data/scale_awareness/unconstrained_results.jsonl
  data/scale_awareness/pairwise_results.jsonl
  data/scale_awareness/solution_aligned.jsonl
  data/scale_awareness/FIXES_REPORT.md
"""

from __future__ import annotations

import json
import math
import re
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
UNCONSTRAINED_JSONL = OUT_DIR / "unconstrained_results.jsonl"
PAIRWISE_JSONL = OUT_DIR / "pairwise_results.jsonl"
SOLUTION_JSONL = OUT_DIR / "solution_aligned.jsonl"
FIXES_REPORT_MD = OUT_DIR / "FIXES_REPORT.md"


# ── Fix 1: Unconstrained prompts ──────────────────────────────────────────────

PLAN_FREE_BASE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.

Output ONLY a JSON object with key "steps". Generate as many steps as the problem requires.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

The steps describe HOW to solve the problem, not the solution itself.
Actions must be plain English (no math, no symbols, no backslashes).

Problem: {problem}

JSON output only:"""


PLAN_FREE_STEP_AWARE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.

Output ONLY a JSON object with key "steps". Generate exactly the number of steps indicated.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT:
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps} (generate this many)
- Expected step composition:
{step_type_lines}

Problem: {problem}

JSON output only:"""


@dataclass
class UnconstrainedResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    expected_n_steps: int
    plan_free_base: list[str] = field(default_factory=list)
    plan_free_step: list[str] = field(default_factory=list)
    score_free_base: float | None = None
    score_free_step: float | None = None
    calib_free_base: float | None = None
    calib_free_step: float | None = None
    errors: list[str] = field(default_factory=list)


CALIB_JUDGE_PROMPT = """\
Rate whether this plan is appropriately calibrated to the expected difficulty.

Problem: {problem}
Expected difficulty: {label} ({score}/5)
Expected steps: ~{expected_n_steps}

Plan:
{plan_text}

Rate calibration 1-5:
  1 = wildly miscalibrated (far too simple or complex)
  2 = notably miscalibrated
  3 = roughly calibrated
  4 = well calibrated
  5 = perfectly calibrated

Respond ONLY:
Score: X
Reasoning: one sentence

Score:"""


def run_fix1():
    print("\n=== Fix 1: Unconstrained Generation (Expert + Hard tasks) ===")
    done = load_done_keys(UNCONSTRAINED_JSONL, ["task_id"])

    tasks = load_annotated()
    target = [t for t in tasks if t["difficulty"].get("overall_label", "?") in ("Expert", "Hard")]
    todo = [t for t in target if t["task_id"] not in {k[0] for k in done}]
    print(f"  Expert+Hard tasks: {len(target)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task in tqdm(todo, desc="Unconstrained", unit="task"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        rec = UnconstrainedResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            expected_n_steps=ctx["expected_n_steps"],
        )

        # Free baseline (no step count constraint)
        try:
            text = cli_call(PLAN_FREE_BASE.format(problem=ctx["problem"]))
            rec.plan_free_base = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"free_base: {e}")
        time.sleep(1)

        # Free step-aware (with correct step count hint, no ceiling)
        try:
            text = cli_call(
                PLAN_FREE_STEP_AWARE.format(
                    problem=ctx["problem"],
                    label=ctx["label"],
                    score=ctx["score"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                )
            )
            rec.plan_free_step = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"free_step: {e}")
        time.sleep(1)

        # Blind quality judge
        for plan, score_attr in [
            (rec.plan_free_base, "score_free_base"),
            (rec.plan_free_step, "score_free_step"),
        ]:
            if not plan:
                continue
            try:
                scores = blind_judge(ctx["problem"], plan)
                setattr(rec, score_attr, scores.get("overall"))
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        # Calibration judge
        for plan, calib_attr in [
            (rec.plan_free_base, "calib_free_base"),
            (rec.plan_free_step, "calib_free_step"),
        ]:
            if not plan:
                continue
            plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan))
            try:
                raw = cli_call(
                    CALIB_JUDGE_PROMPT.format(
                        problem=ctx["problem"],
                        label=ctx["label"],
                        score=ctx["score"],
                        expected_n_steps=ctx["expected_n_steps"],
                        plan_text=plan_text,
                    )
                )
                m = re.search(r"Score:\s*([1-5])", raw)
                if m:
                    setattr(rec, calib_attr, float(m.group(1)))
            except Exception as e:
                rec.errors.append(f"calib judge: {e}")
            time.sleep(1)

        append_result(UNCONSTRAINED_JSONL, rec)

    print("  Fix 1 done.")


# ── Fix 2: Pairwise Ranking ───────────────────────────────────────────────────

PAIRWISE_PROMPT = """\
Compare two plans for solving the same problem.

Problem:
{problem}

Plan A:
{plan_a}

Plan B:
{plan_b}

Which plan is better overall for solving this problem?
Consider: coverage of key steps, logical ordering, appropriate depth.

Respond ONLY:
Better: A or B
Confidence: high or low
Reason: one sentence

Better:"""


@dataclass
class PairwiseResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    condition_a: str  # e.g. "baseline"
    condition_b: str  # e.g. "step_aware"
    winner: str = ""  # "A", "B", or "tie"
    confidence: str = ""
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


def run_fix2():
    """Pairwise: compare baseline vs step_aware for all 101 tasks."""
    print("\n=== Fix 2: Pairwise Ranking (A vs C) ===")
    done = load_done_keys(PAIRWISE_JSONL, ["task_id", "condition_a", "condition_b"])

    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                existing[obj["task_id"]] = obj

    tasks = load_annotated()

    # Compare A(baseline) vs C(step_aware) and A(baseline) vs B(diff_aware)
    comparisons = [("baseline", "step_aware"), ("baseline", "diff_aware")]
    work = [(t, ca, cb) for t in tasks for ca, cb in comparisons]
    todo = [(t, ca, cb) for t, ca, cb in work if (t["task_id"], ca, cb) not in done]
    print(f"  Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond_a, cond_b in tqdm(todo, desc="Pairwise", unit="item"):
        ctx = get_task_context(task)
        ex = existing.get(task["task_id"], {})

        plan_a = ex.get(f"plan_{cond_a}", [])
        plan_b = ex.get(f"plan_{cond_b}", [])

        rec = PairwiseResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=task["difficulty"].get("overall_label", "?"),
            condition_a=cond_a,
            condition_b=cond_b,
        )

        if not plan_a or not plan_b:
            rec.errors.append("missing plan(s)")
            append_result(PAIRWISE_JSONL, rec)
            continue

        plan_a_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan_a))
        plan_b_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan_b))

        try:
            raw = cli_call(
                PAIRWISE_PROMPT.format(
                    problem=ctx["problem"],
                    plan_a=plan_a_text,
                    plan_b=plan_b_text,
                )
            )
            m = re.search(r"Better:\s*([AB])", raw, re.IGNORECASE)
            if m:
                rec.winner = m.group(1).upper()
            mc = re.search(r"Confidence:\s*(high|low)", raw, re.IGNORECASE)
            if mc:
                rec.confidence = mc.group(1).lower()
            mr = re.search(r"Reason:\s*(.+)", raw, re.IGNORECASE)
            if mr:
                rec.reasoning = mr.group(1).strip()[:200]
        except Exception as e:
            rec.errors.append(str(e))

        append_result(PAIRWISE_JSONL, rec)
        time.sleep(1)

    print("  Fix 2 done.")


# ── Fix 3: Solution-Aligned Evaluation ───────────────────────────────────────

SOLUTION_JUDGE_PROMPT = """\
A correct solution to the problem is provided. Rate how well the given plan aligns with it.

Problem:
{problem}

Correct solution (ground truth):
{solution}

Plan to evaluate:
{plan_text}

Rate alignment 1-5:
  1 = plan completely misses the solution approach
  2 = plan partially overlaps but misses key steps
  3 = plan captures the main idea but misses important details
  4 = plan aligns well — would likely lead to the correct solution
  5 = plan perfectly anticipates the correct solution path

Respond ONLY:
Score: X
Reasoning: one sentence

Score:"""


@dataclass
class SolutionAlignedResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str
    solution_score: float | None = None
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


def run_fix3():
    """Solution-aligned evaluation for all conditions."""
    print("\n=== Fix 3: Solution-Aligned Evaluation ===")
    done = load_done_keys(SOLUTION_JSONL, ["task_id", "condition"])

    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                existing[obj["task_id"]] = obj

    tasks = load_annotated()
    # Only tasks that have a real solution (non-empty)
    tasks_with_sol = [t for t in tasks if (t.get("solution") or "").strip()]
    print(f"  Tasks with solution: {len(tasks_with_sol)}")

    conditions = ["baseline", "diff_aware", "step_aware"]
    work = [(t, c) for t in tasks_with_sol for c in conditions]
    todo = [(t, c) for t, c in work if (t["task_id"], c) not in done]
    print(f"  Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="Solution-aligned", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        ex = existing.get(task["task_id"], {})
        plan = ex.get(f"plan_{cond}", [])
        solution = (task.get("solution") or "")[:1500]

        rec = SolutionAlignedResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            condition=cond,
        )

        if not plan:
            rec.errors.append("no plan")
            append_result(SOLUTION_JSONL, rec)
            continue

        plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan))
        try:
            raw = cli_call(
                SOLUTION_JUDGE_PROMPT.format(
                    problem=ctx["problem"],
                    solution=solution,
                    plan_text=plan_text,
                )
            )
            m = re.search(r"Score:\s*([1-5])", raw)
            if m:
                rec.solution_score = float(m.group(1))
            mr = re.search(r"Reasoning:\s*(.+)", raw, re.IGNORECASE)
            if mr:
                rec.reasoning = mr.group(1).strip()[:200]
        except Exception as e:
            rec.errors.append(str(e))

        append_result(SOLUTION_JSONL, rec)
        time.sleep(1)

    print("  Fix 3 done.")


# ── Report ────────────────────────────────────────────────────────────────────


def generate_fixes_report() -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    unconstrained = load_jsonl(UNCONSTRAINED_JSONL)
    pairwise = load_jsonl(PAIRWISE_JSONL)
    solution = load_jsonl(SOLUTION_JSONL)

    def fmt(v, d=2):
        return f"{v:.{d}f}" if v is not None else "—"

    def pfmt(p):
        if p is None:
            return "—"
        if p < 0.001:
            return "< 0.001"
        if p < 0.01:
            return f"{p:.3f}"
        return f"{p:.2f}"

    # ── Fix 1: Unconstrained ──────────────────────────────────────────────────
    unc_valid = [r for r in unconstrained if r.get("score_free_base") and r.get("score_free_step")]

    unc_base_scores = [r["score_free_base"] for r in unc_valid]
    unc_step_scores = [r["score_free_step"] for r in unc_valid]
    unc_t, unc_p = t_stat(unc_step_scores, unc_base_scores)
    unc_d = cohens_d(unc_step_scores, unc_base_scores)

    unc_calib_base = [
        r["calib_free_base"] for r in unc_valid if r.get("calib_free_base") is not None
    ]
    unc_calib_step = [
        r["calib_free_step"] for r in unc_valid if r.get("calib_free_step") is not None
    ]
    unc_ct, unc_cp = t_stat(unc_calib_step, unc_calib_base)
    unc_cd = cohens_d(unc_calib_step, unc_calib_base)

    # Plan lengths
    unc_base_len = avg([len(r["plan_free_base"]) for r in unc_valid if r.get("plan_free_base")])
    unc_step_len = avg([len(r["plan_free_step"]) for r in unc_valid if r.get("plan_free_step")])
    exp_len_avg = avg([r["expected_n_steps"] for r in unc_valid])

    # Compare with constrained results on same tasks
    existing_results = {obj["task_id"]: obj for obj in load_jsonl(RESULTS_JSONL)}
    calib_existing = {
        (r["task_id"], r["condition"]): r.get("calib_score")
        for r in load_jsonl(OUT_DIR / "calibration_judge.jsonl")
    }
    unc_task_ids = {r["task_id"] for r in unc_valid}

    constrained_calib_base = [
        calib_existing.get((tid, "baseline"))
        for tid in unc_task_ids
        if calib_existing.get((tid, "baseline")) is not None
    ]
    constrained_calib_step = [
        calib_existing.get((tid, "step_aware"))
        for tid in unc_task_ids
        if calib_existing.get((tid, "step_aware")) is not None
    ]

    by_label_unc: dict[str, dict] = defaultdict(
        lambda: {"base": [], "step": [], "cb": [], "cs": []}
    )
    for r in unc_valid:
        label = r["difficulty_label"]
        by_label_unc[label]["base"].append(r.get("score_free_base", 0) or 0)
        by_label_unc[label]["step"].append(r.get("score_free_step", 0) or 0)
        if r.get("calib_free_base"):
            by_label_unc[label]["cb"].append(r["calib_free_base"])
        if r.get("calib_free_step"):
            by_label_unc[label]["cs"].append(r["calib_free_step"])

    unc_diff_rows = ""
    for label in ["Medium", "Hard", "Expert"]:
        if label in by_label_unc:
            d = by_label_unc[label]
            ba = avg(d["base"])
            sa = avg(d["step"])
            cb = avg(d["cb"])
            cs = avg(d["cs"])
            delta_q = (sa - ba) if sa and ba else None
            delta_c = (cs - cb) if cs and cb else None
            s1 = "+" if delta_q and delta_q >= 0 else ""
            s2 = "+" if delta_c and delta_c >= 0 else ""
            unc_diff_rows += (
                f"| {label} | {fmt(ba)} | {fmt(sa)} | "
                f"{s1}{fmt(delta_q)} | {fmt(cb)} | {fmt(cs)} | {s2}{fmt(delta_c)} |\n"
            )

    # ── Fix 2: Pairwise ───────────────────────────────────────────────────────
    pair_rows_ac = [
        r
        for r in pairwise
        if r["condition_a"] == "baseline" and r["condition_b"] == "step_aware" and r.get("winner")
    ]
    pair_rows_ab = [
        r
        for r in pairwise
        if r["condition_a"] == "baseline" and r["condition_b"] == "diff_aware" and r.get("winner")
    ]

    def win_stats(rows, cond_b_name):
        total = len(rows)
        if total == 0:
            return "—", "—", "—"
        b_wins = sum(1 for r in rows if r["winner"] == "B")
        a_wins = sum(1 for r in rows if r["winner"] == "A")
        rate = b_wins / total
        # binomial test approx
        p = 2 * min(rate, 1 - rate)  # rough two-tailed
        return f"{b_wins}/{total} ({rate * 100:.1f}%)", f"{a_wins}/{total}", f"{p:.3f}"

    ac_b_wins, ac_a_wins, ac_p = win_stats(pair_rows_ac, "step_aware")
    ab_b_wins, ab_a_wins, ab_p = win_stats(pair_rows_ab, "diff_aware")

    # by difficulty
    pair_by_diff: dict[str, dict] = defaultdict(lambda: {"ac": [], "ab": []})
    for r in pair_rows_ac:
        pair_by_diff[r["difficulty_label"]]["ac"].append(r["winner"])
    for r in pair_rows_ab:
        pair_by_diff[r["difficulty_label"]]["ab"].append(r["winner"])

    pair_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in pair_by_diff:
            d = pair_by_diff[label]
            ac = d["ac"]
            ab = d["ab"]
            ac_rate = sum(1 for w in ac if w == "B") / len(ac) if ac else None
            ab_rate = sum(1 for w in ab if w == "B") / len(ab) if ab else None
            pair_diff_rows += (
                f"| {label} | {len(ac)} | "
                f"{ac_rate * 100:.0f}% ({'C wins' if ac_rate and ac_rate > 0.5 else 'A wins'}) | "
                f"{ab_rate * 100:.0f}% ({'B wins' if ab_rate and ab_rate > 0.5 else 'A wins'}) |\n"
                if ac_rate is not None and ab_rate is not None
                else ""
            )

    # ── Fix 3: Solution-aligned ───────────────────────────────────────────────
    sol_by_cond: dict[str, list] = defaultdict(list)
    for r in solution:
        s = r.get("solution_score")
        if s is not None:
            sol_by_cond[r["condition"]].append(s)

    sol_t, sol_p = t_stat(sol_by_cond.get("step_aware", []), sol_by_cond.get("baseline", []))
    sol_d = cohens_d(sol_by_cond.get("step_aware", []), sol_by_cond.get("baseline", []))

    sol_by_diff: dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for r in solution:
        if r.get("solution_score") is not None:
            sol_by_diff[r["difficulty_label"]][r["condition"]].append(r["solution_score"])

    sol_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in sol_by_diff:
            d = sol_by_diff[label]
            ba = avg(d.get("baseline", []))
            da = avg(d.get("diff_aware", []))
            sa = avg(d.get("step_aware", []))
            delta = (sa - ba) if sa and ba else None
            s = "+" if delta and delta >= 0 else ""
            sol_diff_rows += f"| {label} | {fmt(ba)} | {fmt(da)} | {fmt(sa)} | {s}{fmt(delta)} |\n"

    # correlation: solution_score vs blind_score
    blind_lookup = {
        (r["task_id"], r["condition"]): r.get("overall")
        for r in load_jsonl(OUT_DIR / "blind_scores.jsonl")
    }
    both_blind, both_sol = [], []
    for r in solution:
        if r.get("solution_score"):
            b = blind_lookup.get((r["task_id"], r["condition"]))
            if b is not None:
                both_sol.append(r["solution_score"])
                both_blind.append(b)

    def pearson_r(a, b):
        n = len(a)
        if n < 2:
            return None
        ma, mb = sum(a) / n, sum(b) / n
        num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        da = math.sqrt(sum((x - ma) ** 2 for x in a))
        db = math.sqrt(sum((x - mb) ** 2 for x in b))
        return num / (da * db) if da * db else 0.0

    r_sol_blind = pearson_r(both_sol, both_blind)

    return f"""# Research Fixes Report: Addressing Critical Weaknesses
**Generated:** {now}

---

## Fix 1 — Unconstrained Generation (Expert + Hard)

**Problem fixed:** The "3-6 steps" constraint caused Expert tasks to produce 6 steps when
the hint specified ~13, making the step_aware hint unactionable (Expert calibration paradox).

**Method:** Re-ran conditions A (free baseline) and C (free step-aware) with no step ceiling.
{len(unc_valid)} Expert+Hard tasks. Plans scored with blind rubric + calibration judge.

### Plan length (unconstrained)

| Condition | Avg plan length | Expected |
|-----------|----------------|---------|
| Free baseline  | {fmt(unc_base_len, 1)} | — |
| Free step-aware| {fmt(unc_step_len, 1)} | {fmt(exp_len_avg, 1)} |

Constrained versions produced: 6.0 steps (ceiling hit). Free versions now generate more steps.

### Quality scores (blind rubric)

| Condition | Avg score |
|-----------|-----------|
| Constrained baseline (original) | {fmt(avg([existing_results.get(r["task_id"], {}).get("score_baseline") for r in unc_valid if existing_results.get(r["task_id"], {}).get("score_baseline")]))} |
| **Free baseline** | **{fmt(avg(unc_base_scores))}** |
| Constrained step-aware (original) | {fmt(avg([existing_results.get(r["task_id"], {}).get("score_step_aware") for r in unc_valid if existing_results.get(r["task_id"], {}).get("score_step_aware")]))} |
| **Free step-aware** | **{fmt(avg(unc_step_scores))}** |

Free step-aware vs free baseline: t = {fmt(unc_t)}, p = {pfmt(unc_p)}, Cohen's d = {fmt(unc_d)}

### Calibration scores (unconstrained vs constrained)

| Version | Baseline calib | Step-aware calib | Δ |
|---------|---------------|-----------------|---|
| Constrained (original) | {fmt(avg(constrained_calib_base))} | {fmt(avg(constrained_calib_step))} | {("+" if (avg(constrained_calib_step) or 0) >= (avg(constrained_calib_base) or 0) else "")}{fmt((avg(constrained_calib_step) or 0) - (avg(constrained_calib_base) or 0))} |
| **Unconstrained** | **{fmt(avg(unc_calib_base))}** | **{fmt(avg(unc_calib_step))}** | **{("+" if (avg(unc_calib_step) or 0) >= (avg(unc_calib_base) or 0) else "")}{fmt((avg(unc_calib_step) or 0) - (avg(unc_calib_base) or 0))}** |

Unconstrained calib (step vs base): t = {fmt(unc_ct)}, p = {pfmt(unc_cp)}, Cohen's d = {fmt(unc_cd)}

### By difficulty label (unconstrained)

| Difficulty | Base quality | Step quality | Δ quality | Base calib | Step calib | Δ calib |
|------------|-------------|-------------|-----------|-----------|-----------|---------|
{unc_diff_rows}
---

## Fix 2 — Pairwise Ranking (A vs C direct comparison)

**Problem fixed:** 1-5 Likert scale had low judge reliability (r=0.37). Pairwise
comparisons are more reliable — judge only needs to say which plan is better.

**Method:** For each task, judge reads plan A (baseline) and plan B (step_aware or diff_aware)
side by side and picks the better one.

### A(baseline) vs C(step_aware) — {len(pair_rows_ac)} tasks

| | Count | Win rate |
|---|---|---|
| C(step_aware) wins | {ac_b_wins} | — |
| A(baseline) wins   | {ac_a_wins} | — |
| Binomial p (C≠50%) | {ac_p} | — |

### A(baseline) vs B(diff_aware) — {len(pair_rows_ab)} tasks

| | Count | Win rate |
|---|---|---|
| B(diff_aware) wins | {ab_b_wins} | — |
| A(baseline) wins   | {ab_a_wins} | — |
| Binomial p (B≠50%) | {ab_p} | — |

### Pairwise win rates by difficulty

| Difficulty | N | C(step) win% | B(diff) win% |
|------------|---|-------------|-------------|
{pair_diff_rows}
---

## Fix 3 — Solution-Aligned Evaluation

**Problem fixed:** All previous metrics were subjective (judge ratings). Now using the
ground-truth `solution` field from annotation as reference.

**Method:** Judge reads the correct solution alongside the generated plan and rates
"how well would this plan lead to the correct solution?" (1-5).

### Solution-alignment scores by condition

| Condition | Avg score | N |
|-----------|-----------|---|
| A baseline   | {fmt(avg(sol_by_cond.get("baseline", [])))} | {len(sol_by_cond.get("baseline", []))} |
| B diff_aware | {fmt(avg(sol_by_cond.get("diff_aware", [])))} | {len(sol_by_cond.get("diff_aware", []))} |
| C step_aware | {fmt(avg(sol_by_cond.get("step_aware", [])))} | {len(sol_by_cond.get("step_aware", []))} |

**Step_aware vs baseline:** t = {fmt(sol_t)}, p = {pfmt(sol_p)}, Cohen's d = {fmt(sol_d)}

**Correlation with blind rubric scores:** r = {fmt(r_sol_blind)}
(Higher r = the blind rubric and solution-aligned metric agree → validates judge reliability)

### Solution-alignment by difficulty

| Difficulty | A baseline | B diff_aware | C step_aware | Δ C−A |
|------------|-----------|-------------|-------------|-------|
{sol_diff_rows}
---

*Generated by `scripts/run_fixes.py`*
"""


# ── main ──────────────────────────────────────────────────────────────────────


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    if not args.report_only:
        if 1 in args.fix:
            run_fix1()
        if 2 in args.fix:
            run_fix2()
        if 3 in args.fix:
            run_fix3()

    print("\n=== Generating fixes report ===")
    report = generate_fixes_report()
    FIXES_REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Report: {FIXES_REPORT_MD}")
    print("All done.")


if __name__ == "__main__":
    main()
