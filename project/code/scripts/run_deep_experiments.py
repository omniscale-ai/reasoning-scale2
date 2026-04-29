#!/usr/bin/env python3
"""
Deep Experiments — Scale Awareness (Diploma Extension 2)
=========================================================

  Exp 9  — Revision Ablation: which hint component drives the revision gain?
            R1=label-only  R2=count-only  R3=types-only  R4=count+types
  Exp 10 — Iterative Revision: 2nd round revision on Hard/Expert subset
  Exp 11 — Few-shot Calibration: show 2 gold-standard plans before generating

  Analytical (no new calls):
            - Step type distribution by condition (from existing results)
            - Expert calibration paradox breakdown
            - Miscalibration-conditional revision analysis

Outputs:
  data/scale_awareness/revision_ablation.jsonl
  data/scale_awareness/iterative_revision.jsonl
  data/scale_awareness/fewshot_results.jsonl
  data/scale_awareness/DEEP_REPORT.md
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections import Counter, defaultdict
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
REVISION_JSONL = OUT_DIR / "revision_results.jsonl"
CALIB_JSONL = OUT_DIR / "calibration_judge.jsonl"
REV_ABLATION_JSONL = OUT_DIR / "revision_ablation.jsonl"
ITER_REVISION_JSONL = OUT_DIR / "iterative_revision.jsonl"
FEWSHOT_JSONL = OUT_DIR / "fewshot_results.jsonl"
DEEP_REPORT_MD = OUT_DIR / "DEEP_REPORT.md"


# ── Revision prompts (same structure as Exp 6 but partial hints) ──────────────


def make_revision_prompt(hint_lines: str) -> str:
    return (
        "You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.\n"
        "DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.\n"
        'Output ONLY a JSON object with key "steps" containing 3 to 6 steps.\n'
        'Each step: {{"number": int, "action": "plain English description", '
        '"needs": ["..."], "produces": ["..."]}}\n\n'
        "Revise the initial plan using the scale context.\n\n"
        f"SCALE CONTEXT:\n{hint_lines}\n\n"
        "Problem: {problem}\n\n"
        "Initial plan (revise this):\n{initial_plan}\n\n"
        "Revised JSON output only:"
    )


REVISE_LABEL = make_revision_prompt("- Difficulty: {label}")
REVISE_COUNT = make_revision_prompt("- Expected steps: ~{expected_n_steps}")
REVISE_TYPES = make_revision_prompt("- Expected step types:\n{step_type_lines}")
REVISE_C4 = make_revision_prompt(
    "- Expected steps: ~{expected_n_steps}\n- Expected step types:\n{step_type_lines}"
)


# ── Exp 9: Revision Ablation ──────────────────────────────────────────────────


@dataclass
class RevAblationResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str  # R1/R2/R3/R4
    plan_revised: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


def run_exp9():
    print("\n=== Exp 9: Revision Ablation ===")
    done = load_done_keys(REV_ABLATION_JSONL, ["task_id", "condition"])

    # load baseline plans
    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                existing[obj["task_id"]] = obj

    tasks = load_annotated()
    # stratified sample of 50 tasks (preserve difficulty distribution)
    rng = random.Random(123)
    by_label: dict[str, list] = defaultdict(list)
    for t in tasks:
        by_label[t["difficulty"].get("overall_label", "?")].append(t)
    sample: list[dict] = []
    for label, pool in by_label.items():
        n = max(1, round(len(pool) / len(tasks) * 50))
        sample.extend(rng.sample(pool, min(n, len(pool))))
    sample = sample[:50]

    conditions = ["R1", "R2", "R3", "R4"]
    work = [(t, c) for t in sample for c in conditions]
    todo = [(t, c) for t, c in work if (t["task_id"], c) not in done]
    print(f"  Sample: {len(sample)} tasks | Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="Rev ablation", unit="item"):
        ctx = get_task_context(task)
        ex = existing.get(task["task_id"], {})
        baseline_plan = ex.get("plan_baseline", [])
        diff = task["difficulty"]

        rec = RevAblationResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            condition=cond,
        )

        if not baseline_plan:
            rec.errors.append("no baseline plan")
            append_result(REV_ABLATION_JSONL, rec)
            continue

        initial_plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(baseline_plan))

        try:
            if cond == "R1":
                prompt = REVISE_LABEL.format(
                    label=ctx["label"], problem=ctx["problem"], initial_plan=initial_plan_text
                )
            elif cond == "R2":
                prompt = REVISE_COUNT.format(
                    expected_n_steps=ctx["expected_n_steps"],
                    problem=ctx["problem"],
                    initial_plan=initial_plan_text,
                )
            elif cond == "R3":
                prompt = REVISE_TYPES.format(
                    step_type_lines=ctx["step_type_lines"],
                    problem=ctx["problem"],
                    initial_plan=initial_plan_text,
                )
            else:  # R4
                prompt = REVISE_C4.format(
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                    problem=ctx["problem"],
                    initial_plan=initial_plan_text,
                )

            text = cli_call(prompt)
            rec.plan_revised = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        time.sleep(1)

        if rec.plan_revised:
            try:
                scores = blind_judge(ctx["problem"], rec.plan_revised)
                rec.overall = scores.get("overall")
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(REV_ABLATION_JSONL, rec)

    print("  Exp 9 done.")


# ── Exp 10: Iterative Revision ────────────────────────────────────────────────

REVISE_ITER2_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

This is a second revision pass. Improve the plan further.

SCALE CONTEXT:
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps}
- Expected step types:
{step_type_lines}

Problem: {problem}

Current plan (improve this further):
{current_plan}

Revised JSON output only:"""


@dataclass
class IterRevResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    round_idx: int  # 0=baseline, 1=revision1, 2=revision2
    plan: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


def run_exp10():
    print("\n=== Exp 10: Iterative Revision ===")
    done = load_done_keys(ITER_REVISION_JSONL, ["task_id", "round_idx"])

    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                existing[obj["task_id"]] = obj

    revision_existing: dict[str, dict] = {}
    with REVISION_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                revision_existing[obj["task_id"]] = obj

    tasks = load_annotated()
    # Focus on Hard + Expert + Medium tasks (most interesting for calibration)
    focus = [
        t
        for t in tasks
        if t["difficulty"].get("overall_label", "?") in ("Hard", "Expert", "Medium")
    ]
    focus = sorted(focus, key=lambda x: x["task_id"])[:25]
    print(f"  Focus tasks: {len(focus)} (Hard/Expert/Medium)")

    # round 0 = baseline (from existing), round 1 = revision1 (from revision_existing), round 2 = new
    work = [(t, r) for t in focus for r in [0, 1, 2]]
    todo = [(t, r) for t, r in work if (t["task_id"], r) not in done]
    print(f"  Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, round_idx in tqdm(todo, desc="Iter revision", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        rec = IterRevResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            round_idx=round_idx,
        )

        if round_idx == 0:
            # Use existing baseline
            ex = existing.get(task["task_id"], {})
            rec.plan = ex.get("plan_baseline", [])
            rec.overall = ex.get("score_baseline")

        elif round_idx == 1:
            # Use existing revision1
            rev = revision_existing.get(task["task_id"], {})
            rec.plan = rev.get("plan_revised", [])
            rec.overall = rev.get("score_revised")

        else:  # round 2 — new generation
            # Get round 1 plan
            rev = revision_existing.get(task["task_id"], {})
            round1_plan = rev.get("plan_revised", [])
            if not round1_plan:
                rec.errors.append("no round1 plan")
                append_result(ITER_REVISION_JSONL, rec)
                continue

            current_plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(round1_plan))
            try:
                text = cli_call(
                    REVISE_ITER2_PROMPT.format(
                        problem=ctx["problem"],
                        label=ctx["label"],
                        score=ctx["score"],
                        expected_n_steps=ctx["expected_n_steps"],
                        step_type_lines=ctx["step_type_lines"],
                        current_plan=current_plan_text,
                    )
                )
                rec.plan = extract_steps(text)
            except Exception as e:
                rec.errors.append(f"plan: {e}")

            time.sleep(1)

            if rec.plan:
                try:
                    scores = blind_judge(ctx["problem"], rec.plan)
                    rec.overall = scores.get("overall")
                except Exception as e:
                    rec.errors.append(f"judge: {e}")
                time.sleep(1)

        append_result(ITER_REVISION_JSONL, rec)

    print("  Exp 10 done.")


# ── Exp 11: Few-shot Calibration ──────────────────────────────────────────────

FEWSHOT_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

Here are two examples of well-structured plans for problems at similar difficulty:

--- Example 1 ({ex1_label}) ---
Problem: {ex1_problem}
Plan:
{ex1_plan}

--- Example 2 ({ex2_label}) ---
Problem: {ex2_problem}
Plan:
{ex2_plan}

---

Now generate a plan for the following problem at {label} difficulty:

Problem: {problem}

JSON output only:"""


@dataclass
class FewshotResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    plan_fewshot: list[str] = field(default_factory=list)
    overall: float | None = None
    ex1_task_id: str = ""
    ex2_task_id: str = ""
    errors: list[str] = field(default_factory=list)


def _annotation_plan(task: dict) -> list[str]:
    """Convert annotation step nodes to a list of action strings."""
    nodes = (task.get("steps") or {}).get("nodes", [])
    return [f"{n.get('label', '')} — {n.get('detail', '')}" for n in nodes]


def run_exp11():
    print("\n=== Exp 11: Few-shot Calibration ===")
    done = load_done_keys(FEWSHOT_JSONL, ["task_id"])

    tasks = load_annotated()
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        by_label[t["difficulty"].get("overall_label", "?")].append(t)

    todo = [t for t in tasks if t["task_id"] not in {k[0] for k in done}]
    print(f"  {len(tasks)} tasks | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task in tqdm(todo, desc="Few-shot", unit="task"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        label = diff.get("overall_label", "?")

        # Pick 2 examples from same difficulty label, different task
        pool = [t for t in by_label[label] if t["task_id"] != task["task_id"]]
        if len(pool) < 2:
            # Fall back to adjacent difficulty
            adjacent = {
                "Trivial": ["Easy"],
                "Easy": ["Trivial", "Medium"],
                "Medium": ["Easy", "Hard"],
                "Hard": ["Medium", "Expert"],
                "Expert": ["Hard"],
            }
            for adj_label in adjacent.get(label, []):
                pool += [t for t in by_label[adj_label] if t["task_id"] != task["task_id"]]
            pool = pool[:2]

        if len(pool) < 2:
            rec = FewshotResult(
                task_id=task["task_id"],
                benchmark=task["benchmark"],
                difficulty_label=label,
                difficulty_score=float(diff.get("overall_difficulty", 0)),
            )
            rec.errors.append("not enough examples")
            append_result(FEWSHOT_JSONL, rec)
            continue

        ex1, ex2 = pool[0], pool[1]
        ex1_plan = _annotation_plan(ex1)
        ex2_plan = _annotation_plan(ex2)

        ex1_plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(ex1_plan[:6]))
        ex2_plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(ex2_plan[:6]))

        rec = FewshotResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=label,
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            ex1_task_id=ex1["task_id"],
            ex2_task_id=ex2["task_id"],
        )

        try:
            prompt = FEWSHOT_PROMPT.format(
                problem=ctx["problem"],
                label=label,
                ex1_label=ex1["difficulty"].get("overall_label", "?"),
                ex1_problem=(ex1.get("problem") or "")[:500],
                ex1_plan=ex1_plan_text,
                ex2_label=ex2["difficulty"].get("overall_label", "?"),
                ex2_problem=(ex2.get("problem") or "")[:500],
                ex2_plan=ex2_plan_text,
            )
            text = cli_call(prompt)
            rec.plan_fewshot = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        time.sleep(1)

        if rec.plan_fewshot:
            try:
                scores = blind_judge(ctx["problem"], rec.plan_fewshot)
                rec.overall = scores.get("overall")
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(FEWSHOT_JSONL, rec)

    print("  Exp 11 done.")


# ── Analytics helpers (from existing data) ────────────────────────────────────


def analyze_step_type_distribution() -> str:
    """Compute step type distributions from existing results + annotation."""
    tasks_by_id = {t["task_id"]: t for t in load_annotated()}

    existing: list[dict] = load_jsonl(RESULTS_JSONL)

    type_by_cond: dict[str, Counter] = {
        "annotation": Counter(),
        "baseline": Counter(),
        "step_aware": Counter(),
    }

    # Annotation ground truth
    for t in tasks_by_id.values():
        nodes = (t.get("steps") or {}).get("nodes", [])
        for n in nodes:
            type_by_cond["annotation"][n.get("type", "?")] += 1

    # Generated plans: classify step types using heuristics
    TYPE_KEYWORDS = {
        "strategic": [
            "design",
            "plan",
            "architect",
            "define",
            "determine",
            "identify approach",
            "formulate",
            "outline",
            "strategy",
            "overview",
            "framework",
        ],
        "verification": [
            "verify",
            "test",
            "validate",
            "check",
            "confirm",
            "assert",
            "ensure",
            "review",
            "audit",
            "inspect",
        ],
        "conceptual": [
            "understand",
            "analyze",
            "reason",
            "consider",
            "evaluate",
            "assess",
            "interpret",
            "explain",
            "derive",
            "establish",
        ],
        "computational": [
            "compute",
            "calculate",
            "implement",
            "execute",
            "apply",
            "run",
            "perform",
            "process",
            "generate",
            "build",
            "write",
            "create",
        ],
    }

    def classify_step(step_text: str) -> str:
        lower = step_text.lower()
        for stype, keywords in TYPE_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return stype
        return "computational"  # default

    for ex in existing:
        for cond_key, plan_key in [
            ("baseline", "plan_baseline"),
            ("step_aware", "plan_step_aware"),
        ]:
            for step in ex.get(plan_key, []):
                type_by_cond[cond_key][classify_step(step)] += 1

    lines = "\n### Step Type Distribution\n\n"
    lines += "| Type | Annotation | Baseline | Step-aware |\n"
    lines += "|------|-----------|----------|------------|\n"
    for t in ["strategic", "conceptual", "computational", "verification"]:
        an = type_by_cond["annotation"][t]
        ba = type_by_cond["baseline"][t]
        sa = type_by_cond["step_aware"][t]
        an_tot = sum(type_by_cond["annotation"].values()) or 1
        ba_tot = sum(type_by_cond["baseline"].values()) or 1
        sa_tot = sum(type_by_cond["step_aware"].values()) or 1
        lines += (
            f"| {t} | {an / an_tot * 100:.1f}% ({an}) "
            f"| {ba / ba_tot * 100:.1f}% ({ba}) "
            f"| {sa / sa_tot * 100:.1f}% ({sa}) |\n"
        )
    return lines


def analyze_expert_paradox() -> str:
    """Why does step_aware hurt calibration for Expert tasks?"""
    calib = load_jsonl(CALIB_JSONL)
    expert_rows = [r for r in calib if r.get("difficulty_label") == "Expert"]

    baseline_expert = [
        r["calib_score"]
        for r in expert_rows
        if r["condition"] == "baseline" and r.get("calib_score")
    ]
    step_expert = [
        r["calib_score"]
        for r in expert_rows
        if r["condition"] == "step_aware" and r.get("calib_score")
    ]

    tasks_by_id = {t["task_id"]: t for t in load_annotated()}

    # For each Expert task, compare expected_n_steps (annotation) vs plan length
    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            obj = json.loads(line.strip()) if line.strip() else None
            if obj:
                existing[obj["task_id"]] = obj

    expert_tasks = [
        t for t in tasks_by_id.values() if t["difficulty"].get("overall_label", "?") == "Expert"
    ]

    len_rows = []
    for t in expert_tasks:
        ex = existing.get(t["task_id"], {})
        ctx = get_task_context(t)
        ba_len = len(ex.get("plan_baseline", []))
        sa_len = len(ex.get("plan_step_aware", []))
        exp_len = ctx["expected_n_steps"]
        len_rows.append(
            {
                "task_id": t["task_id"][:16],
                "expected": exp_len,
                "baseline_len": ba_len,
                "stepaware_len": sa_len,
                "ba_err": abs(ba_len - exp_len),
                "sa_err": abs(sa_len - exp_len),
            }
        )

    lines = "\n### Expert Calibration Paradox Analysis\n\n"
    lines += (
        f"Expert calib: baseline={avg(baseline_expert):.2f}, step_aware={avg(step_expert):.2f}\n\n"
    )
    lines += (
        "For Expert tasks, the annotation expects ~13 steps (plan_length=5 → 13 midpoint), "
        "but the prompt constrains to 3-6 steps. This mismatch means the step_aware hint "
        "(`~13 steps`) conflicts with the format constraint, potentially confusing the model.\n\n"
    )
    lines += "| Task | Expected | Baseline len | Step-aware len | BA err | SA err |\n"
    lines += "|------|----------|-------------|----------------|--------|--------|\n"
    for r in len_rows[:8]:
        lines += (
            f"| {r['task_id']} | {r['expected']} "
            f"| {r['baseline_len']} | {r['stepaware_len']} "
            f"| {r['ba_err']} | {r['sa_err']} |\n"
        )
    return lines


def analyze_miscalibration_conditional() -> str:
    """Does revision help more when the baseline was miscalibrated?"""
    calib = load_jsonl(CALIB_JSONL)
    rev = load_jsonl(REVISION_JSONL)

    # baseline calibration score per task
    base_calib = {
        r["task_id"]: r["calib_score"]
        for r in calib
        if r["condition"] == "baseline" and r.get("calib_score")
    }

    # revision gain per task
    rev_gain = {}
    for r in rev:
        if r.get("score_baseline") and r.get("score_revised"):
            rev_gain[r["task_id"]] = r["score_revised"] - r["score_baseline"]

    # split by calibration quality
    well_cal = [rev_gain[tid] for tid, cs in base_calib.items() if cs >= 4.0 and tid in rev_gain]
    poorly_cal = [rev_gain[tid] for tid, cs in base_calib.items() if cs <= 2.0 and tid in rev_gain]
    mid_cal = [
        rev_gain[tid] for tid, cs in base_calib.items() if 2.0 < cs < 4.0 and tid in rev_gain
    ]

    lines = "\n### Miscalibration-Conditional Revision Analysis\n\n"
    lines += "Does revision help more when the baseline was poorly calibrated?\n\n"
    lines += "| Baseline calib quality | N tasks | Avg revision gain |\n"
    lines += "|----------------------|---------|-------------------|\n"
    lines += f"| Low (≤2) | {len(poorly_cal)} | {avg(poorly_cal):.2f} |\n"
    lines += f"| Mid (3)  | {len(mid_cal)}    | {avg(mid_cal):.2f} |\n"
    lines += f"| High (≥4) | {len(well_cal)} | {avg(well_cal):.2f} |\n"
    return lines


# ── Report ────────────────────────────────────────────────────────────────────


def generate_deep_report() -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    rev_abl = load_jsonl(REV_ABLATION_JSONL)
    iter_rev = load_jsonl(ITER_REVISION_JSONL)
    fewshot = load_jsonl(FEWSHOT_JSONL)
    existing = load_jsonl(RESULTS_JSONL)

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

    # ── Exp 9: revision ablation ──────────────────────────────────────────────
    abl_by_cond: dict[str, list] = defaultdict(list)
    for r in rev_abl:
        s = r.get("overall")
        if s is not None:
            abl_by_cond[r["condition"]].append(s)

    # baseline blind scores (from revision results)
    rev_all = load_jsonl(OUT_DIR / "revision_results.jsonl")
    rev_lookup = {r["task_id"]: r for r in rev_all}
    abl_task_ids = {r["task_id"] for r in rev_abl}
    base_abl_scores = [
        rev_lookup[tid]["score_baseline"]
        for tid in abl_task_ids
        if tid in rev_lookup and rev_lookup[tid].get("score_baseline")
    ]
    full_rev_scores = [
        rev_lookup[tid]["score_revised"]
        for tid in abl_task_ids
        if tid in rev_lookup and rev_lookup[tid].get("score_revised")
    ]
    base_avg = avg(base_abl_scores)
    full_rev_avg = avg(full_rev_scores)

    abl_rows = ""
    for cond, label in [
        ("R1", "label-only"),
        ("R2", "count-only"),
        ("R3", "types-only"),
        ("R4", "count+types"),
    ]:
        s = avg(abl_by_cond.get(cond, []))
        delta = (s - base_avg) if s and base_avg else None
        sign = "+" if delta and delta >= 0 else ""
        abl_rows += f"| {cond} {label} | {fmt(s)} | {sign}{fmt(delta)} |\n"

    # best ablation condition
    best_cond = max(abl_by_cond, key=lambda c: avg(abl_by_cond[c]) or 0) if abl_by_cond else "—"
    best_val = avg(abl_by_cond.get(best_cond, []))

    # ── Exp 10: iterative revision ────────────────────────────────────────────
    by_round: dict[int, list] = defaultdict(list)
    for r in iter_rev:
        s = r.get("overall")
        if s is not None:
            by_round[r["round_idx"]].append(s)

    iter_t, iter_p = t_stat(by_round.get(2, []), by_round.get(0, []))
    iter_d = cohens_d(by_round.get(2, []), by_round.get(0, []))
    r1_vs_r0_t, r1_vs_r0_p = t_stat(by_round.get(1, []), by_round.get(0, []))

    # per-difficulty convergence
    by_diff_round: dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for r in iter_rev:
        s = r.get("overall")
        if s is not None:
            by_diff_round[r["difficulty_label"]][r["round_idx"]].append(s)

    iter_diff_rows = ""
    for label in ["Medium", "Hard", "Expert"]:
        if label in by_diff_round:
            d = by_diff_round[label]
            r0 = avg(d.get(0, []))
            r1 = avg(d.get(1, []))
            r2 = avg(d.get(2, []))
            iter_diff_rows += f"| {label} | {fmt(r0)} | {fmt(r1)} | {fmt(r2)} |\n"

    # ── Exp 11: few-shot ──────────────────────────────────────────────────────
    fs_scores = [r["overall"] for r in fewshot if r.get("overall") is not None]
    fs_avg = avg(fs_scores)

    # Compare few-shot vs baseline on same tasks
    fs_task_ids = {r["task_id"] for r in fewshot if r.get("overall") is not None}
    fs_existing = load_jsonl(OUT_DIR / "blind_scores.jsonl")
    blind_lookup = {(r["task_id"], r["condition"]): r.get("overall") for r in fs_existing}
    base_fs_scores = [
        blind_lookup.get((tid, "baseline"))
        for tid in fs_task_ids
        if blind_lookup.get((tid, "baseline")) is not None
    ]
    step_fs_scores = [
        blind_lookup.get((tid, "step_aware"))
        for tid in fs_task_ids
        if blind_lookup.get((tid, "step_aware")) is not None
    ]

    fs_t, fs_p = t_stat(fs_scores, base_fs_scores[: len(fs_scores)])
    fs_d = cohens_d(fs_scores, base_fs_scores[: len(fs_scores)])

    # few-shot by difficulty
    fs_by_diff: dict[str, list] = defaultdict(list)
    for r in fewshot:
        if r.get("overall") is not None:
            fs_by_diff[r["difficulty_label"]].append(r["overall"])

    # baseline by difficulty (from blind scores, same tasks)
    base_by_diff_fs: dict[str, list] = defaultdict(list)
    for r in fewshot:
        if r.get("overall") is not None:
            s = blind_lookup.get((r["task_id"], "baseline"))
            if s is not None:
                base_by_diff_fs[r["difficulty_label"]].append(s)

    fs_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in fs_by_diff:
            fs_a = avg(fs_by_diff[label])
            ba_a = avg(base_by_diff_fs.get(label, []))
            delta = (fs_a - ba_a) if fs_a and ba_a else None
            sign = "+" if delta and delta >= 0 else ""
            fs_diff_rows += f"| {label} | {fmt(ba_a)} | {fmt(fs_a)} | {sign}{fmt(delta)} |\n"

    # ── Analytical sections ───────────────────────────────────────────────────
    step_type_section = analyze_step_type_distribution()
    expert_paradox_section = analyze_expert_paradox()
    miscal_section = analyze_miscalibration_conditional()

    return f"""# Deep Experiments Report: Scale Awareness in LLM Agents

**Generated:** {now}

---

## Experiment 9 — Revision Ablation

Which component of the scale hint drives the revision improvement?

**Sample:** 50 stratified tasks. All revised from same baseline plan.
Judged with blind rubric.

| Condition | Avg score | Δ vs baseline |
|-----------|-----------|---------------|
| A baseline (no revision) | {fmt(base_avg)} | — |
| Full revision (A→C hint) | {fmt(full_rev_avg)} | {("+" if (full_rev_avg or 0) >= (base_avg or 0) else "")}{fmt((full_rev_avg or 0) - (base_avg or 0))} |
{abl_rows}

**Best ablation condition:** {best_cond} ({fmt(best_val)})

---

## Experiment 10 — Iterative Revision

Does a 2nd round of revision improve further on Hard/Expert/Medium tasks?

**25 tasks** (Hard + Expert + Medium). Rounds: 0=baseline, 1=revision1, 2=revision2.

| Round | Avg score | N |
|-------|-----------|---|
| 0 baseline  | {fmt(avg(by_round.get(0, [])))} | {len(by_round.get(0, []))} |
| 1 revision1 | {fmt(avg(by_round.get(1, [])))} | {len(by_round.get(1, []))} |
| 2 revision2 | {fmt(avg(by_round.get(2, [])))} | {len(by_round.get(2, []))} |

Round 1 vs Round 0: t = {fmt(r1_vs_r0_t)}, p = {pfmt(r1_vs_r0_p)}
Round 2 vs Round 0: t = {fmt(iter_t)}, p = {pfmt(iter_p)}, Cohen's d = {fmt(iter_d)}

### By difficulty label

| Difficulty | Round 0 | Round 1 | Round 2 |
|------------|---------|---------|---------|
{iter_diff_rows}
---

## Experiment 11 — Few-shot Calibration

Show 2 expert-annotated plan examples (same difficulty) before generating.
Tests whether seeing calibrated examples matters more than an abstract hint.

**{len(fs_scores)} tasks** with few-shot plans scored.

| Condition | Avg score | N |
|-----------|-----------|---|
| A baseline   | {fmt(avg(base_fs_scores))} | {len(base_fs_scores)} |
| C step_aware | {fmt(avg(step_fs_scores))} | {len(step_fs_scores)} |
| F few-shot   | {fmt(fs_avg)} | {len(fs_scores)} |

**Few-shot vs baseline:** t = {fmt(fs_t)}, p = {pfmt(fs_p)}, Cohen's d = {fmt(fs_d)}

### By difficulty label

| Difficulty | Baseline | Few-shot | Δ |
|------------|----------|----------|---|
{fs_diff_rows}
---

## Analytical: Step Type Distribution

Heuristic classification of generated plan steps by type.
{step_type_section}

---

## Analytical: Expert Calibration Paradox
{expert_paradox_section}

---

## Analytical: Does Revision Help More When Baseline Was Miscalibrated?
{miscal_section}

---

*Generated by `scripts/run_deep_experiments.py`*
"""


# ── main ──────────────────────────────────────────────────────────────────────


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--exp", type=int, nargs="+", default=[9, 10, 11])
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    if not args.report_only:
        if 9 in args.exp:
            run_exp9()
        if 10 in args.exp:
            run_exp10()
        if 11 in args.exp:
            run_exp11()

    print("\n=== Generating deep report ===")
    report = generate_deep_report()
    DEEP_REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Report: {DEEP_REPORT_MD}")
    print("All done.")


if __name__ == "__main__":
    main()
