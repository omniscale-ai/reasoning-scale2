#!/usr/bin/env python3
"""
Extra Experiments — Scale Awareness (Diploma Extension)
=========================================================

  Exp 6  — Plan Revision: baseline plan + scale hint → ask model to revise.
            Compares revision vs from-scratch step_aware on same tasks.
  Exp 7  — Coverage metric: how many annotation step-graph nodes are
            semantically covered by each generated plan (objective, judge-free).
  Exp 8  — Calibration judge: judge rates whether the plan's depth/scope
            matches the task's expected difficulty level.

Outputs:
  data/scale_awareness/revision_results.jsonl
  data/scale_awareness/coverage_results.jsonl
  data/scale_awareness/calibration_judge.jsonl
  data/scale_awareness/EXTRA_REPORT.md
"""

from __future__ import annotations

import json
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
    PLAN_BASE,
    cli_call,
    extract_steps,
    load_annotated,
)

# ── paths ─────────────────────────────────────────────────────────────────────
OUT_DIR = Path("data/scale_awareness")
RESULTS_JSONL = OUT_DIR / "results.jsonl"
REVISION_JSONL = OUT_DIR / "revision_results.jsonl"
COVERAGE_JSONL = OUT_DIR / "coverage_results.jsonl"
CALIBJUDGE_JSONL = OUT_DIR / "calibration_judge.jsonl"
EXTRA_REPORT_MD = OUT_DIR / "EXTRA_REPORT.md"


# ── Experiment 6: Plan Revision ───────────────────────────────────────────────

REVISE_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

You have an initial plan for the problem below. Revise it using the scale context provided.

SCALE CONTEXT (use to calibrate depth and number of steps):
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps}
- Expected step types:
{step_type_lines}

Problem: {problem}

Initial plan (revise this):
{initial_plan}

Revised JSON output only:"""


@dataclass
class RevisionResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    plan_baseline: list[str] = field(default_factory=list)
    plan_revised: list[str] = field(default_factory=list)
    plan_stepaware: list[str] = field(default_factory=list)  # from original results
    # blind scores
    score_baseline: float | None = None
    score_revised: float | None = None
    score_stepaware: float | None = None
    errors: list[str] = field(default_factory=list)


def run_exp6():
    print("\n=== Exp 6: Plan Revision ===")
    done = load_done_keys(REVISION_JSONL, ["task_id"])

    # Load existing baseline plans from results.jsonl
    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                existing[obj["task_id"]] = obj

    tasks = load_annotated()
    todo = [t for t in tasks if t["task_id"] not in {k[0] for k in done}]
    print(f"  {len(tasks)} tasks | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task in tqdm(todo, desc="Revision", unit="task"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        ex = existing.get(task["task_id"], {})

        rec = RevisionResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            plan_baseline=ex.get("plan_baseline", []),
            plan_stepaware=ex.get("plan_step_aware", []),
        )

        # If no existing baseline, generate one
        if not rec.plan_baseline:
            try:
                text = cli_call(PLAN_BASE.format(problem=ctx["problem"]))
                rec.plan_baseline = extract_steps(text)
            except Exception as e:
                rec.errors.append(f"baseline: {e}")
            time.sleep(1)

        # Revision: baseline + scale hint
        if rec.plan_baseline:
            initial_plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(rec.plan_baseline))
            try:
                text = cli_call(
                    REVISE_PROMPT.format(
                        problem=ctx["problem"],
                        label=ctx["label"],
                        score=ctx["score"],
                        expected_n_steps=ctx["expected_n_steps"],
                        step_type_lines=ctx["step_type_lines"],
                        initial_plan=initial_plan_text,
                    )
                )
                rec.plan_revised = extract_steps(text)
            except Exception as e:
                rec.errors.append(f"revision: {e}")
            time.sleep(1)

        # Judge all three plans (baseline, revised, step_aware)
        for plan, score_attr in [
            (rec.plan_baseline, "score_baseline"),
            (rec.plan_revised, "score_revised"),
            (rec.plan_stepaware, "score_stepaware"),
        ]:
            if not plan:
                continue
            try:
                scores = blind_judge(ctx["problem"], plan)
                setattr(rec, score_attr, scores.get("overall"))
            except Exception as e:
                rec.errors.append(f"judge {score_attr}: {e}")
            time.sleep(1)

        append_result(REVISION_JSONL, rec)

    print("  Exp 6 done.")


# ── Experiment 7: Coverage Metric ────────────────────────────────────────────

COVERAGE_PROMPT = """\
You are a coverage evaluator.

Reference steps (from expert annotation):
{ref_steps}

Generated plan steps:
{gen_steps}

For each reference step, check whether any generated step semantically covers it.
Respond ONLY as JSON:
{{"covered": [<true/false for each reference step>], "coverage_ratio": <0.0-1.0>}}

JSON:"""


@dataclass
class CoverageResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    condition: str  # "baseline", "diff_aware", "step_aware", "self_aware"
    n_ref_steps: int = 0
    n_covered: int = 0
    coverage_ratio: float = 0.0
    errors: list[str] = field(default_factory=list)


def run_exp7():
    print("\n=== Exp 7: Coverage Metric ===")
    done = load_done_keys(COVERAGE_JSONL, ["task_id", "condition"])

    # Load existing plans
    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                existing[obj["task_id"]] = obj

    # Also load self_calibration plans
    selfcal: dict[str, dict] = {}
    sc_path = OUT_DIR / "self_calibration.jsonl"
    if sc_path.exists():
        with sc_path.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    obj = json.loads(line)
                    selfcal[obj["task_id"]] = obj

    tasks = load_annotated()
    conditions = ["baseline", "diff_aware", "step_aware", "self_aware"]

    work = [(t, cond) for t in tasks for cond in conditions]
    todo = [(t, cond) for t, cond in work if (t["task_id"], cond) not in done]
    print(f"  Work items: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="Coverage", unit="item"):
        nodes = (task.get("steps") or {}).get("nodes", [])
        ref_steps = [n.get("label", "") + ": " + n.get("detail", "") for n in nodes]

        if not ref_steps:
            rec = CoverageResult(
                task_id=task["task_id"],
                benchmark=task["benchmark"],
                difficulty_label=task["difficulty"].get("overall_label", "?"),
                condition=cond,
            )
            rec.errors.append("no annotation nodes")
            append_result(COVERAGE_JSONL, rec)
            continue

        # Get generated plan
        ex = existing.get(task["task_id"], {})
        if cond == "self_aware":
            sc = selfcal.get(task["task_id"], {})
            gen_plan = sc.get("plan_self_aware", [])
        elif cond == "baseline":
            gen_plan = ex.get("plan_baseline", [])
        elif cond == "diff_aware":
            gen_plan = ex.get("plan_diff_aware", [])
        else:  # step_aware
            gen_plan = ex.get("plan_step_aware", [])

        rec = CoverageResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=task["difficulty"].get("overall_label", "?"),
            condition=cond,
            n_ref_steps=len(ref_steps),
        )

        if not gen_plan:
            rec.errors.append("no generated plan")
            append_result(COVERAGE_JSONL, rec)
            continue

        ref_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(ref_steps))
        gen_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(gen_plan))

        try:
            raw = cli_call(COVERAGE_PROMPT.format(ref_steps=ref_text, gen_steps=gen_text))
            # parse JSON
            parsed = None
            for pat in [r"```json\s*([\s\S]+?)```", r"```\s*([\s\S]+?)```"]:
                m = re.search(pat, raw)
                if m:
                    parsed = json.loads(m.group(1))
                    break
            if not parsed:
                parsed = json.loads(raw)
            covered_list = parsed.get("covered", [])
            rec.n_covered = sum(1 for x in covered_list if x)
            rec.coverage_ratio = parsed.get(
                "coverage_ratio", rec.n_covered / len(ref_steps) if ref_steps else 0
            )
        except Exception as e:
            rec.errors.append(str(e))

        append_result(COVERAGE_JSONL, rec)
        time.sleep(1)

    print("  Exp 7 done.")


# ── Experiment 8: Calibration Judge ──────────────────────────────────────────

CALIB_JUDGE_PROMPT = """\
You are a calibration evaluator. Your task is to rate whether a plan is
appropriately calibrated to the expected difficulty of the problem.

Problem:
{problem}

Expected difficulty: {label} ({score}/5)
Expected steps: ~{expected_n_steps}

Plan to evaluate:
{plan_text}

Rate calibration on 1-5:
  1 = wildly miscalibrated (plan is far too simple or far too complex)
  2 = notably miscalibrated (missing key depth or over-engineered)
  3 = roughly calibrated (close but off in depth or scope)
  4 = well calibrated (depth and scope match the difficulty)
  5 = perfectly calibrated (plan matches exactly what an expert would expect)

Respond ONLY:
Score: X
Reasoning: one sentence

Score:"""


@dataclass
class CalibJudgeResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str
    calib_score: float | None = None
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


def run_exp8():
    print("\n=== Exp 8: Calibration Judge ===")
    done = load_done_keys(CALIBJUDGE_JSONL, ["task_id", "condition"])

    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                existing[obj["task_id"]] = obj

    tasks = load_annotated()
    conditions = ["baseline", "step_aware"]
    work = [(t, cond) for t in tasks for cond in conditions]
    todo = [(t, cond) for t, cond in work if (t["task_id"], cond) not in done]
    print(f"  Work items: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="Calib judge", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        ex = existing.get(task["task_id"], {})
        plan = ex.get(f"plan_{cond}", [])

        rec = CalibJudgeResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            condition=cond,
        )

        if not plan:
            rec.errors.append("no plan")
            append_result(CALIBJUDGE_JSONL, rec)
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
                rec.calib_score = float(m.group(1))
            m2 = re.search(r"Reasoning:\s*(.+)", raw)
            if m2:
                rec.reasoning = m2.group(1).strip()[:200]
        except Exception as e:
            rec.errors.append(str(e))

        append_result(CALIBJUDGE_JSONL, rec)
        time.sleep(1)

    print("  Exp 8 done.")


# ── Report ────────────────────────────────────────────────────────────────────


def generate_extra_report() -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    revision = load_jsonl(REVISION_JSONL)
    coverage = load_jsonl(COVERAGE_JSONL)
    calib = load_jsonl(CALIBJUDGE_JSONL)

    # ── Exp 6: Revision ───────────────────────────────────────────────────────
    rev_valid = [r for r in revision if r.get("score_baseline") and r.get("score_revised")]
    rev_base_scores = [r["score_baseline"] for r in rev_valid]
    rev_revised_scores = [r["score_revised"] for r in rev_valid]
    rev_step_scores = [r["score_stepaware"] for r in rev_valid if r.get("score_stepaware")]

    rev_t, rev_p = t_stat(rev_revised_scores, rev_base_scores)
    rev_d = cohens_d(rev_revised_scores, rev_base_scores)

    # by difficulty
    rev_by_diff: dict[str, dict] = defaultdict(lambda: {"base": [], "rev": [], "step": []})
    for r in rev_valid:
        label = r["difficulty_label"]
        rev_by_diff[label]["base"].append(r["score_baseline"])
        rev_by_diff[label]["rev"].append(r["score_revised"])
        if r.get("score_stepaware"):
            rev_by_diff[label]["step"].append(r["score_stepaware"])

    rev_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in rev_by_diff:
            d = rev_by_diff[label]
            ba = avg(d["base"])
            ra = avg(d["rev"])
            sa = avg(d["step"])
            delta = (ra - ba) if ra and ba else None
            s = "+" if delta and delta >= 0 else ""
            sa_str = f"{sa:.2f}" if sa else "—"
            rev_diff_rows += f"| {label} | {ba:.2f} | {ra:.2f} | {s}{delta:.2f} | {sa_str} |\n"

    # ── Exp 7: Coverage ───────────────────────────────────────────────────────
    cov_by_cond: dict[str, list] = defaultdict(list)
    for r in coverage:
        if r.get("n_ref_steps", 0) > 0 and not r.get("errors"):
            cov_by_cond[r["condition"]].append(r.get("coverage_ratio", 0))

    # coverage by difficulty × condition
    cov_by_diff_cond: dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for r in coverage:
        if r.get("n_ref_steps", 0) > 0 and not r.get("errors"):
            cov_by_diff_cond[r["difficulty_label"]][r["condition"]].append(
                r.get("coverage_ratio", 0)
            )

    cov_t, cov_p = t_stat(cov_by_cond.get("step_aware", []), cov_by_cond.get("baseline", []))
    cov_d = cohens_d(cov_by_cond.get("step_aware", []), cov_by_cond.get("baseline", []))

    cov_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in cov_by_diff_cond:
            d = cov_by_diff_cond[label]
            ba = avg(d.get("baseline", []))
            sa = avg(d.get("step_aware", []))
            da = avg(d.get("diff_aware", []))
            sc = avg(d.get("self_aware", []))

            def pct(v):
                return f"{v * 100:.1f}%" if v is not None else "—"

            cov_diff_rows += f"| {label} | {pct(ba)} | {pct(da)} | {pct(sa)} | {pct(sc)} |\n"

    # ── Exp 8: Calibration Judge ──────────────────────────────────────────────
    cal_by_cond: dict[str, list] = defaultdict(list)
    for r in calib:
        s = r.get("calib_score")
        if s is not None:
            cal_by_cond[r["condition"]].append(s)

    cal_t, cal_p = t_stat(cal_by_cond.get("step_aware", []), cal_by_cond.get("baseline", []))
    cal_d = cohens_d(cal_by_cond.get("step_aware", []), cal_by_cond.get("baseline", []))

    cal_by_diff: dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for r in calib:
        s = r.get("calib_score")
        if s is not None:
            cal_by_diff[r["difficulty_label"]][r["condition"]].append(s)

    cal_diff_rows = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in cal_by_diff:
            d = cal_by_diff[label]
            ba = avg(d.get("baseline", []))
            sa = avg(d.get("step_aware", []))
            delta = (sa - ba) if sa and ba else None
            s = "+" if delta and delta >= 0 else ""
            cal_diff_rows += f"| {label} | {ba:.2f} | {sa:.2f} | {s}{delta:.2f} |\n"

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

    return f"""# Extra Experiments Report: Scale Awareness in LLM Agents

**Generated:** {now}

---

## Experiment 6 — Plan Revision

Does scale context help more as *revision feedback* (showing the model its own baseline plan + hint)
than as *upfront priming* (generating from scratch with hint)?

**{len(rev_valid)} tasks** with both baseline and revised plans scored.

### Overall scores

| Condition | Avg score | Δ vs baseline |
|-----------|-----------|---------------|
| A baseline              | {fmt(avg(rev_base_scores))} | — |
| A→C revised (baseline + hint) | {fmt(avg(rev_revised_scores))} | {("+" if (avg(rev_revised_scores) or 0) >= (avg(rev_base_scores) or 0) else "")}{fmt((avg(rev_revised_scores) or 0) - (avg(rev_base_scores) or 0))} |
| C step_aware (scratch)  | {fmt(avg(rev_step_scores))} | {("+" if (avg(rev_step_scores) or 0) >= (avg(rev_base_scores) or 0) else "")}{fmt((avg(rev_step_scores) or 0) - (avg(rev_base_scores) or 0))} |

**Revised vs baseline:** t = {fmt(rev_t)}, p = {pfmt(rev_p)}, Cohen's d = {fmt(rev_d)}

### By difficulty label

| Difficulty | Baseline | Revised | Δ rev−base | Step-aware |
|------------|----------|---------|------------|------------|
{rev_diff_rows}
---

## Experiment 7 — Coverage Metric

Fraction of annotation step-graph nodes semantically covered by each plan.
Objective metric — no judge needed.

### Overall coverage by condition

| Condition | Avg coverage | N plans |
|-----------|-------------|---------|
| A baseline   | {fmt(avg(cov_by_cond.get("baseline", [])), 3)} | {len(cov_by_cond.get("baseline", []))} |
| B diff_aware | {fmt(avg(cov_by_cond.get("diff_aware", [])), 3)} | {len(cov_by_cond.get("diff_aware", []))} |
| C step_aware | {fmt(avg(cov_by_cond.get("step_aware", [])), 3)} | {len(cov_by_cond.get("step_aware", []))} |
| D self_aware | {fmt(avg(cov_by_cond.get("self_aware", [])), 3)} | {len(cov_by_cond.get("self_aware", []))} |

**Step_aware vs baseline:** t = {fmt(cov_t)}, p = {pfmt(cov_p)}, Cohen's d = {fmt(cov_d)}

### Coverage by difficulty × condition

| Difficulty | A baseline | B diff_aware | C step_aware | D self_aware |
|------------|------------|--------------|--------------|--------------|
{cov_diff_rows}
---

## Experiment 8 — Calibration Judge

Judge rates whether plan depth/scope matches the task's expected difficulty.
(Separate from plan quality — a plan can be good but miscalibrated.)

### Overall calibration score by condition

| Condition | Avg calib score | N |
|-----------|-----------------|---|
| A baseline   | {fmt(avg(cal_by_cond.get("baseline", [])))} | {len(cal_by_cond.get("baseline", []))} |
| C step_aware | {fmt(avg(cal_by_cond.get("step_aware", [])))} | {len(cal_by_cond.get("step_aware", []))} |

**Step_aware vs baseline:** t = {fmt(cal_t)}, p = {pfmt(cal_p)}, Cohen's d = {fmt(cal_d)}

### Calibration by difficulty label

| Difficulty | A baseline | C step_aware | Δ |
|------------|------------|--------------|---|
{cal_diff_rows}
---

*Generated by `scripts/run_extra_experiments.py`*
"""


# ── main ──────────────────────────────────────────────────────────────────────


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--exp", type=int, nargs="+", default=[6, 7, 8])
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    if not args.report_only:
        if 6 in args.exp:
            run_exp6()
        if 7 in args.exp:
            run_exp7()
        if 8 in args.exp:
            run_exp8()

    print("\n=== Generating extra report ===")
    report = generate_extra_report()
    EXTRA_REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Report: {EXTRA_REPORT_MD}")
    print("All done.")


if __name__ == "__main__":
    main()
