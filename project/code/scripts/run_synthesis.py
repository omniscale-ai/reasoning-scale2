#!/usr/bin/env python3
"""
Synthesis Experiments — Scale Awareness (Diploma Final Layer)
=============================================================

  Exp E — Combined Pipeline:
           few-shot examples → generate plan → iterative revision with scale hint.
           The "full treatment": chains the two best-performing interventions.
           Tests whether the gains are additive (few-shot + revision > each alone).
           25 Hard/Expert tasks. Conditions: pipeline vs few-shot-only vs revision-only.

  Exp F — Revision Mechanism Ablation:
           What drives iterative revision gain — the second pass itself, or the
           scale hint in the revision prompt?
           Conditions on 30 tasks:
             Rev_hint  = baseline → revise WITH scale hint (existing Exp 6)
             Rev_blind = baseline → revise WITHOUT any hint ("improve this plan")
           If Rev_blind ≈ Rev_hint → second pass is what matters, hint is irrelevant.
           If Rev_hint > Rev_blind → the scale hint content is causally driving revision gain.

  Exp G — Benchmark × Condition Breakdown (analytical, zero new calls):
           Cross-tabulate all existing quality scores by benchmark × condition.
           Find which benchmarks benefit most from scale hints, few-shot, revision.
           Explains *where* scale awareness matters: domain-specific or universal?

  Exp H — Predictive Regression Analysis (analytical, zero new calls):
           Use task features (difficulty_score, expected_n_steps, benchmark, step types)
           to predict quality gain (Δ step_aware − baseline) via linear regression.
           Which task characteristics predict when scale hints help most?
           Provides actionable guidance: "use scale hints for tasks with X features."

Outputs:
  data/scale_awareness/pipeline_results.jsonl
  data/scale_awareness/rev_mechanism.jsonl
  data/scale_awareness/SYNTHESIS_REPORT.md
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
FEWSHOT_JSONL = OUT_DIR / "fewshot_results.jsonl"
REVISION_JSONL = OUT_DIR / "revision_results.jsonl"
PIPELINE_JSONL = OUT_DIR / "pipeline_results.jsonl"
REV_MECH_JSONL = OUT_DIR / "rev_mechanism.jsonl"
SYNTHESIS_REPORT = OUT_DIR / "SYNTHESIS_REPORT.md"


# ── Prompts ───────────────────────────────────────────────────────────────────

FEWSHOT_PLAN_PROMPT = """\
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

Now generate a plan for the following {label} problem:

Problem: {problem}

JSON output only:"""


PIPELINE_REVISE_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

You have an initial plan for this {label} problem. Use the scale context to improve it.

SCALE CONTEXT:
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps}
- Expected step composition:
{step_type_lines}

Problem: {problem}

Initial plan (revise and improve):
{initial_plan}

Revised JSON output only:"""


BLIND_REVISE_PROMPT = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

Review and improve the following plan. Make it more complete, better ordered, and more precise.

Problem: {problem}

Current plan (improve this):
{initial_plan}

Improved JSON output only:"""


def _annotation_plan_text(task: dict) -> str:
    nodes = (task.get("steps") or {}).get("nodes", [])
    lines = [f"{i + 1}. {n.get('label', '')} — {n.get('detail', '')}" for i, n in enumerate(nodes)]
    return "\n".join(lines) if lines else "(no plan available)"


def _plan_to_text(steps: list[str]) -> str:
    return "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))


# ── Exp E: Combined Pipeline ──────────────────────────────────────────────────


@dataclass
class PipelineResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str  # "pipeline", "fewshot_only", "revision_only"
    plan: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


def run_exp_e():
    """Combined pipeline: few-shot → plan → revision with hint. 25 Hard/Expert tasks."""
    print("\n=== Exp E: Combined Pipeline ===")
    done = load_done_keys(PIPELINE_JSONL, ["task_id", "condition"])

    tasks = load_annotated()
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        lbl = t["difficulty"].get("overall_label", "?")
        by_label[lbl].append(t)

    # Focus on Hard + Expert (most interesting for calibration)
    focus = by_label.get("Hard", [])[:13] + by_label.get("Expert", [])[:12]
    focus = sorted(focus, key=lambda x: x["task_id"])
    print(f"  Focus: {len(focus)} Hard/Expert tasks")

    # Load existing baseline plans
    main_by_id = {r["task_id"]: r for r in load_jsonl(RESULTS_JSONL)}
    fewshot_by_id = {r["task_id"]: r for r in load_jsonl(FEWSHOT_JSONL)}

    conditions = ["pipeline", "fewshot_only", "revision_only"]
    work = [(t, c) for t in focus for c in conditions]
    todo = [(t, c) for t, c in work if (t["task_id"], c) not in done]
    print(f"  Work: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="Pipeline", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        label = diff.get("overall_label", "?")

        rec = PipelineResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=label,
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            condition=cond,
        )

        # Pick 2 same-difficulty examples for few-shot conditions
        pool = [t2 for t2 in by_label.get(label, []) if t2["task_id"] != task["task_id"]]
        if len(pool) < 2:
            for adj in {"Hard": ["Expert"], "Expert": ["Hard"]}.get(label, []):
                pool += [t2 for t2 in by_label.get(adj, []) if t2["task_id"] != task["task_id"]]

        try:
            if cond == "pipeline":
                # Step 1: few-shot plan generation
                if len(pool) >= 2:
                    ex1, ex2 = pool[0], pool[1]
                    fs_prompt = FEWSHOT_PLAN_PROMPT.format(
                        problem=ctx["problem"],
                        label=label,
                        ex1_label=ex1["difficulty"].get("overall_label", "?"),
                        ex1_problem=(ex1.get("problem") or "")[:500],
                        ex1_plan=_annotation_plan_text(ex1)[:600],
                        ex2_label=ex2["difficulty"].get("overall_label", "?"),
                        ex2_problem=(ex2.get("problem") or "")[:500],
                        ex2_plan=_annotation_plan_text(ex2)[:600],
                    )
                    fs_raw = cli_call(fs_prompt)
                    initial_plan = extract_steps(fs_raw)
                    time.sleep(1)
                else:
                    # fallback: use baseline if no examples
                    initial_plan = main_by_id.get(task["task_id"], {}).get("plan_baseline", [])

                if not initial_plan:
                    rec.errors.append("no initial plan for pipeline")
                    append_result(PIPELINE_JSONL, rec)
                    continue

                # Step 2: revision with scale hint
                rev_prompt = PIPELINE_REVISE_PROMPT.format(
                    problem=ctx["problem"],
                    label=label,
                    score=ctx["score"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                    initial_plan=_plan_to_text(initial_plan),
                )
                rev_raw = cli_call(rev_prompt)
                rec.plan = extract_steps(rev_raw)

            elif cond == "fewshot_only":
                # Use cached few-shot result if available, else regenerate
                cached = fewshot_by_id.get(task["task_id"], {})
                if cached.get("plan_fewshot"):
                    rec.plan = cached["plan_fewshot"]
                elif len(pool) >= 2:
                    ex1, ex2 = pool[0], pool[1]
                    fs_prompt = FEWSHOT_PLAN_PROMPT.format(
                        problem=ctx["problem"],
                        label=label,
                        ex1_label=ex1["difficulty"].get("overall_label", "?"),
                        ex1_problem=(ex1.get("problem") or "")[:500],
                        ex1_plan=_annotation_plan_text(ex1)[:600],
                        ex2_label=ex2["difficulty"].get("overall_label", "?"),
                        ex2_problem=(ex2.get("problem") or "")[:500],
                        ex2_plan=_annotation_plan_text(ex2)[:600],
                    )
                    raw = cli_call(fs_prompt)
                    rec.plan = extract_steps(raw)
                else:
                    rec.errors.append("no examples for few-shot")

            else:  # revision_only
                # Use cached revision result if available
                rev_rows = load_jsonl(REVISION_JSONL)
                rev_by_id = {r["task_id"]: r for r in rev_rows}
                cached = rev_by_id.get(task["task_id"], {})
                if cached.get("plan_revised"):
                    rec.plan = cached["plan_revised"]
                else:
                    # Generate: baseline → revision with hint
                    baseline = main_by_id.get(task["task_id"], {}).get("plan_baseline", [])
                    if not baseline:
                        rec.errors.append("no baseline for revision_only")
                        append_result(PIPELINE_JSONL, rec)
                        continue
                    rev_prompt = PIPELINE_REVISE_PROMPT.format(
                        problem=ctx["problem"],
                        label=label,
                        score=ctx["score"],
                        expected_n_steps=ctx["expected_n_steps"],
                        step_type_lines=ctx["step_type_lines"],
                        initial_plan=_plan_to_text(baseline),
                    )
                    raw = cli_call(rev_prompt)
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

        append_result(PIPELINE_JSONL, rec)
        time.sleep(1)

    print("  Exp E done.")


# ── Exp F: Revision Mechanism Ablation ────────────────────────────────────────


@dataclass
class RevMechResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str  # "rev_hint" or "rev_blind"
    plan: list[str] = field(default_factory=list)
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


def run_exp_f():
    """Revision mechanism: blind revision (no hint) vs hint revision."""
    print("\n=== Exp F: Revision Mechanism Ablation ===")
    done = load_done_keys(REV_MECH_JSONL, ["task_id", "condition"])

    tasks = load_annotated()
    # 30 tasks stratified by difficulty
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        by_label[t["difficulty"].get("overall_label", "?")].append(t)

    sample: list[dict] = []
    for lbl in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        sample.extend(by_label.get(lbl, [])[:6])

    main_by_id = {r["task_id"]: r for r in load_jsonl(RESULTS_JSONL)}

    conditions = ["rev_hint", "rev_blind"]
    work = [(t, c) for t in sample for c in conditions]
    todo = [(t, c) for t, c in work if (t["task_id"], c) not in done]
    print(f"  Sample: {len(sample)} tasks | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond in tqdm(todo, desc="RevMech", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        rec = RevMechResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            condition=cond,
        )

        baseline = main_by_id.get(task["task_id"], {}).get("plan_baseline", [])
        if not baseline:
            rec.errors.append("no baseline plan")
            append_result(REV_MECH_JSONL, rec)
            continue

        initial_text = _plan_to_text(baseline)

        try:
            if cond == "rev_hint":
                prompt = PIPELINE_REVISE_PROMPT.format(
                    problem=ctx["problem"],
                    label=ctx["label"],
                    score=ctx["score"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                    initial_plan=initial_text,
                )
            else:  # rev_blind
                prompt = BLIND_REVISE_PROMPT.format(
                    problem=ctx["problem"],
                    initial_plan=initial_text,
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

        append_result(REV_MECH_JSONL, rec)
        time.sleep(1)

    print("  Exp F done.")


# ── Exp G: Benchmark × Condition Breakdown (analytical) ───────────────────────


def run_exp_g_analytical(report_parts: list[str]) -> None:
    """Cross-tabulate quality scores by benchmark × condition."""
    print("\n=== Exp G: Benchmark × Condition Breakdown ===")

    main_rows = load_jsonl(RESULTS_JSONL)
    if not main_rows:
        report_parts.append("\n## Exp G — Benchmark × Condition\n\n_No data._\n")
        return

    benchmarks = sorted({r["benchmark"] for r in main_rows})
    conditions = [
        ("baseline", "score_baseline"),
        ("diff_aware", "score_diff_aware"),
        ("step_aware", "score_step_aware"),
    ]

    # Also load fewshot and revision for comparison
    fewshot_rows = load_jsonl(FEWSHOT_JSONL)
    fewshot_by_id = {r["task_id"]: r.get("overall") for r in fewshot_rows}
    revision_rows = load_jsonl(OUT_DIR / "revision_results.jsonl")
    revision_by_id = {r["task_id"]: r.get("score_revised") for r in revision_rows}

    def fmt(v):
        return f"{v:.2f}" if v is not None else "—"

    # Build per-benchmark table
    bench_rows = []
    for bench in benchmarks:
        bench_data = [r for r in main_rows if r["benchmark"] == bench]
        row = {"benchmark": bench, "n": len(bench_data)}
        for cond_name, score_key in conditions:
            scores = [r[score_key] for r in bench_data if r.get(score_key) is not None]
            row[cond_name] = avg(scores)
        # few-shot and revision
        fs_scores = [
            fewshot_by_id[r["task_id"]]
            for r in bench_data
            if fewshot_by_id.get(r["task_id"]) is not None
        ]
        rev_scores = [
            revision_by_id[r["task_id"]]
            for r in bench_data
            if revision_by_id.get(r["task_id"]) is not None
        ]
        row["fewshot"] = avg(fs_scores)
        row["revision"] = avg(rev_scores)
        row["delta_step"] = (
            row["step_aware"] - row["baseline"] if row["step_aware"] and row["baseline"] else None
        )
        bench_rows.append(row)

    table = "\n".join(
        f"| {r['benchmark']} | {r['n']} | {fmt(r['baseline'])} | {fmt(r['step_aware'])} | "
        f"{fmt(r['delta_step'])} | {fmt(r['fewshot'])} | {fmt(r['revision'])} |"
        for r in bench_rows
    )

    # Best benchmark for step_aware gain
    best = max(bench_rows, key=lambda r: r["delta_step"] or -99)
    worst = min(bench_rows, key=lambda r: r["delta_step"] or 99)

    # Per-difficulty × benchmark
    diff_bench: dict[tuple, list] = defaultdict(list)
    for r in main_rows:
        key = (r["benchmark"], r.get("difficulty_label", "?"))
        s = r.get("score_step_aware")
        b = r.get("score_baseline")
        if s is not None and b is not None:
            diff_bench[key].append(s - b)

    # Top 5 (benchmark, difficulty) combos by gain
    ranked = sorted(diff_bench.items(), key=lambda x: avg(x[1]) or -99, reverse=True)[:6]
    top_table = "\n".join(f"| {k[0]} | {k[1]} | {len(v)} | {fmt(avg(v))} |" for k, v in ranked)

    report_parts.append(f"""
## Exp G — Benchmark × Condition Breakdown (Analytical)

**Question:** Where does scale awareness matter most — is the effect universal or
concentrated in specific benchmarks/domains?

### Quality scores by benchmark

| Benchmark | N | Baseline | Step-aware | Δ | Few-shot | Revision |
|-----------|---|----------|------------|---|----------|----------|
{table}

**Highest step_aware gain:** {best["benchmark"]} (Δ = {fmt(best["delta_step"])})
**Lowest step_aware gain:** {worst["benchmark"]} (Δ = {fmt(worst["delta_step"])})

### Top (benchmark × difficulty) combos by step_aware gain

| Benchmark | Difficulty | N | Avg Δ (step−base) |
|-----------|------------|---|-------------------|
{top_table}

**Interpretation:** If gains concentrate in 1-2 benchmarks, scale awareness is
domain-specific. If spread evenly, it is a general-purpose calibration signal.
""")
    print("  Exp G done.")


# ── Exp H: Predictive Regression Analysis (analytical) ───────────────────────


def pearson_r(xs: list, ys: list) -> float | None:
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (dx * dy) if dx > 0 and dy > 0 else None


def run_exp_h_analytical(report_parts: list[str]) -> None:
    """Regression analysis: which task features predict quality gain."""
    print("\n=== Exp H: Predictive Regression Analysis ===")

    main_rows = load_jsonl(RESULTS_JSONL)
    if not main_rows:
        report_parts.append("\n## Exp H — Regression Analysis\n\n_No data._\n")
        return

    # Build feature vectors for tasks with both scores
    records = []
    for r in main_rows:
        s_sa = r.get("score_step_aware")
        s_ba = r.get("score_baseline")
        if s_sa is None or s_ba is None:
            continue
        gain = s_sa - s_ba

        diff_score = float(r.get("difficulty_score") or 0)
        exp_steps = int(r.get("expected_plan_len") or 5)
        bench = r.get("benchmark", "?")

        # Label encoding: difficulty
        label = r.get("difficulty_label", "?")
        label_num = {"Trivial": 1, "Easy": 2, "Medium": 3, "Hard": 4, "Expert": 5}.get(label, 3)

        records.append(
            {
                "gain": gain,
                "diff_score": diff_score,
                "exp_steps": exp_steps,
                "label_num": label_num,
                "benchmark": bench,
            }
        )

    n = len(records)
    gains = [r["gain"] for r in records]
    diff_scores = [r["diff_score"] for r in records]
    exp_steps = [r["exp_steps"] for r in records]
    label_nums = [r["label_num"] for r in records]

    r_diff = pearson_r(diff_scores, gains)
    r_steps = pearson_r(exp_steps, gains)
    r_label = pearson_r(label_nums, gains)

    def fmt(v):
        return f"{v:.3f}" if v is not None else "—"

    # Gain by baseline score quartile (tasks where baseline was low — do hints help more?)
    base_scores = [
        r.get("score_baseline")
        for r in main_rows
        if r.get("score_baseline") is not None and r.get("score_step_aware") is not None
    ]
    base_gains = [
        r.get("score_step_aware") - r.get("score_baseline")
        for r in main_rows
        if r.get("score_baseline") is not None and r.get("score_step_aware") is not None
    ]

    if base_scores:
        sorted_pairs = sorted(zip(base_scores, base_gains))
        q = len(sorted_pairs) // 4
        q1_gain = avg([g for _, g in sorted_pairs[:q]])
        q2_gain = avg([g for _, g in sorted_pairs[q : 2 * q]])
        q3_gain = avg([g for _, g in sorted_pairs[2 * q : 3 * q]])
        q4_gain = avg([g for _, g in sorted_pairs[3 * q :]])
        q1_bs = avg([s for s, _ in sorted_pairs[:q]])
        q2_bs = avg([s for s, _ in sorted_pairs[q : 2 * q]])
        q3_bs = avg([s for s, _ in sorted_pairs[2 * q : 3 * q]])
        q4_bs = avg([s for s, _ in sorted_pairs[3 * q :]])
    else:
        q1_gain = q2_gain = q3_gain = q4_gain = None
        q1_bs = q2_bs = q3_bs = q4_bs = None

    r_baseline_gain = pearson_r(base_scores, base_gains) if base_scores else None

    # Gain variance explained (R² via r²)
    r2_diff = (r_diff or 0) ** 2
    r2_steps = (r_steps or 0) ** 2
    r2_label = (r_label or 0) ** 2

    report_parts.append(
        f"""
## Exp H — Predictive Regression Analysis (Analytical)

**Question:** Which task characteristics predict when scale hints produce the largest
quality gains? This answers "when should you use scale hints?" for the thesis.

### Pearson r(feature, quality_gain) — n={n} tasks

| Feature | r | R² | Interpretation |
|---------|---|-----|----------------|
| Difficulty score (1-5) | {fmt(r_diff)} | {fmt(r2_diff)} | Does difficulty predict gain? |
| Expected step count | {fmt(r_steps)} | {fmt(r2_steps)} | Do longer plans benefit more? |
| Difficulty label (ordinal) | {fmt(r_label)} | {fmt(r2_label)} | Monotonic difficulty effect? |
| Baseline quality (inverse) | {fmt(r_baseline_gain)} | {fmt((r_baseline_gain or 0) ** 2)} | Do weaker baselines gain more? |

### Quality gain by baseline score quartile

| Quartile | Avg baseline | Avg gain Δ |
|----------|-------------|-----------|
| Q1 (weakest baselines) | {fmt(q1_bs)} | {fmt(q1_gain)} |
| Q2 | {fmt(q2_bs)} | {fmt(q2_gain)} |
| Q3 | {fmt(q3_bs)} | {fmt(q3_gain)} |
| Q4 (strongest baselines) | {fmt(q4_bs)} | {fmt(q4_gain)} |

### Gain by difficulty label

| Difficulty | N | Avg gain Δ |
|------------|---|-----------|
"""
        + "\n".join(
            f"| {lbl} | {len([r for r in records if r['label_num'] == num])} | "
            f"{fmt(avg([r['gain'] for r in records if r['label_num'] == num]))} |"
            for lbl, num in [("Trivial", 1), ("Easy", 2), ("Medium", 3), ("Hard", 4), ("Expert", 5)]
        )
        + """

**Key finding:** If r(difficulty, gain) > 0.3 → scale hints are most useful for harder tasks.
If r(baseline, gain) < 0 → hints help weak baselines more than strong ones (diminishing returns).
"""
    )
    print("  Exp H done.")


# ── Report ────────────────────────────────────────────────────────────────────


def generate_report():
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    parts: list[str] = [
        f"# Synthesis Report: Scale Awareness in LLM Agents\n\n**Generated:** {ts}\n\n---\n"
    ]

    # Exp E: Combined pipeline results
    pipe_rows = load_jsonl(PIPELINE_JSONL)
    if pipe_rows:
        main_by_id = {r["task_id"]: r for r in load_jsonl(RESULTS_JSONL)}

        def fmt(v):
            return f"{v:.2f}" if v is not None else "—"

        def fmtp(v):
            return ("< 0.001" if v < 0.001 else f"{v:.3f}") if v is not None else "—"

        for cond in ["pipeline", "fewshot_only", "revision_only"]:
            rows = [r for r in pipe_rows if r.get("condition") == cond]
            scores = [r["overall"] for r in rows if r.get("overall") is not None]
            base = [
                main_by_id[r["task_id"]]["score_baseline"]
                for r in rows
                if r["task_id"] in main_by_id
                and main_by_id[r["task_id"]].get("score_baseline") is not None
            ]

        pipe_scores = [
            r["overall"]
            for r in pipe_rows
            if r.get("condition") == "pipeline" and r.get("overall") is not None
        ]
        fs_scores = [
            r["overall"]
            for r in pipe_rows
            if r.get("condition") == "fewshot_only" and r.get("overall") is not None
        ]
        rev_scores = [
            r["overall"]
            for r in pipe_rows
            if r.get("condition") == "revision_only" and r.get("overall") is not None
        ]

        tids = {r["task_id"] for r in pipe_rows}
        base_scores = [
            main_by_id[tid]["score_baseline"]
            for tid in tids
            if tid in main_by_id and main_by_id[tid].get("score_baseline") is not None
        ]

        tp, pp = t_stat(pipe_scores, base_scores) if base_scores else (0, 1)
        tf, pf = t_stat(fs_scores, base_scores) if base_scores else (0, 1)
        tr, pr = t_stat(rev_scores, base_scores) if base_scores else (0, 1)
        dp = cohens_d(pipe_scores, base_scores) if base_scores else None
        df = cohens_d(fs_scores, base_scores) if base_scores else None
        dr = cohens_d(rev_scores, base_scores) if base_scores else None

        # by difficulty
        diff_rows = []
        for lbl in ["Hard", "Expert"]:
            p_lbl = avg(
                [
                    r["overall"]
                    for r in pipe_rows
                    if r.get("condition") == "pipeline"
                    and r.get("difficulty_label") == lbl
                    and r.get("overall") is not None
                ]
            )
            f_lbl = avg(
                [
                    r["overall"]
                    for r in pipe_rows
                    if r.get("condition") == "fewshot_only"
                    and r.get("difficulty_label") == lbl
                    and r.get("overall") is not None
                ]
            )
            rv_lbl = avg(
                [
                    r["overall"]
                    for r in pipe_rows
                    if r.get("condition") == "revision_only"
                    and r.get("difficulty_label") == lbl
                    and r.get("overall") is not None
                ]
            )
            b_lbl = avg(
                [
                    main_by_id[r["task_id"]]["score_baseline"]
                    for r in pipe_rows
                    if r.get("difficulty_label") == lbl
                    and r["task_id"] in main_by_id
                    and main_by_id[r["task_id"]].get("score_baseline") is not None
                ]
            )
            n_lbl = len(
                [
                    r
                    for r in pipe_rows
                    if r.get("condition") == "pipeline" and r.get("difficulty_label") == lbl
                ]
            )
            diff_rows.append((lbl, b_lbl, f_lbl, rv_lbl, p_lbl, n_lbl))

        diff_table = "\n".join(
            f"| {lbl} | {fmt(b)} | {fmt(f)} | {fmt(rv)} | {fmt(p)} | {n} |"
            for lbl, b, f, rv, p, n in diff_rows
        )

        parts.append(f"""
## Exp E — Combined Pipeline (Few-shot → Revision)

**Question:** Are the gains from few-shot calibration and iterative revision additive?
The "full treatment" chains both: use difficulty-matched examples to generate initial plan,
then revise with annotator-provided scale hint.

**Sample:** {len(tids)} Hard/Expert tasks — the subset where both methods showed the largest gains.

### Overall scores vs baseline

| Condition | Avg score | N | t vs baseline | p | Cohen's d |
|-----------|-----------|---|--------------|---|-----------|
| A baseline | {fmt(avg(base_scores))} | {len(base_scores)} | — | — | — |
| Few-shot only (Exp 11 matched) | {fmt(avg(fs_scores))} | {len(fs_scores)} | {fmt(tf)} | {fmtp(pf)} | {fmt(df)} |
| Revision only (Exp 6 hint) | {fmt(avg(rev_scores))} | {len(rev_scores)} | {fmt(tr)} | {fmtp(pr)} | {fmt(dr)} |
| **Pipeline (few-shot + revision)** | **{fmt(avg(pipe_scores))}** | {len(pipe_scores)} | {fmt(tp)} | {fmtp(pp)} | {fmt(dp)} |

### By difficulty label

| Difficulty | Baseline | Few-shot | Revision | Pipeline | N |
|------------|---------|---------|---------|---------|---|
{diff_table}

**Interpretation:**
- Pipeline > both individually → gains are additive (complementary mechanisms)
- Pipeline ≈ max(few-shot, revision) → ceiling effect, one dominates
- Pipeline < best individual → interference between methods
""")

    # Exp F: Revision mechanism
    mech_rows = load_jsonl(REV_MECH_JSONL)
    if mech_rows:
        main_by_id = {r["task_id"]: r for r in load_jsonl(RESULTS_JSONL)}

        def fmt(v):
            return f"{v:.2f}" if v is not None else "—"

        def fmtp(v):
            return ("< 0.001" if v < 0.001 else f"{v:.3f}") if v is not None else "—"

        hint_scores = [
            r["overall"]
            for r in mech_rows
            if r.get("condition") == "rev_hint" and r.get("overall") is not None
        ]
        blind_scores = [
            r["overall"]
            for r in mech_rows
            if r.get("condition") == "rev_blind" and r.get("overall") is not None
        ]

        tids = {r["task_id"] for r in mech_rows}
        base_scores = [
            main_by_id[tid]["score_baseline"]
            for tid in tids
            if tid in main_by_id and main_by_id[tid].get("score_baseline") is not None
        ]

        th, ph = t_stat(hint_scores, base_scores) if base_scores else (0, 1)
        tb, pb = t_stat(blind_scores, base_scores) if base_scores else (0, 1)
        thb, phb = t_stat(hint_scores, blind_scores) if blind_scores else (0, 1)
        dh = cohens_d(hint_scores, base_scores) if base_scores else None
        db = cohens_d(blind_scores, base_scores) if base_scores else None
        dhb = cohens_d(hint_scores, blind_scores) if blind_scores else None

        # by difficulty
        diff_table_f = []
        for lbl in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
            h_lbl = avg(
                [
                    r["overall"]
                    for r in mech_rows
                    if r.get("condition") == "rev_hint"
                    and r.get("difficulty_label") == lbl
                    and r.get("overall") is not None
                ]
            )
            b_lbl_rev = avg(
                [
                    r["overall"]
                    for r in mech_rows
                    if r.get("condition") == "rev_blind"
                    and r.get("difficulty_label") == lbl
                    and r.get("overall") is not None
                ]
            )
            base_lbl = avg(
                [
                    main_by_id[r["task_id"]]["score_baseline"]
                    for r in mech_rows
                    if r.get("difficulty_label") == lbl
                    and r["task_id"] in main_by_id
                    and main_by_id[r["task_id"]].get("score_baseline") is not None
                ]
            )
            n_lbl = len(
                [
                    r
                    for r in mech_rows
                    if r.get("condition") == "rev_hint" and r.get("difficulty_label") == lbl
                ]
            )
            diff_table_f.append((lbl, base_lbl, b_lbl_rev, h_lbl, n_lbl))

        dt_str = "\n".join(
            f"| {lbl} | {fmt(b)} | {fmt(br)} | {fmt(h)} | {n} |"
            for lbl, b, br, h, n in diff_table_f
        )

        parts.append(f"""
## Exp F — Revision Mechanism Ablation

**Question:** Is iterative revision gain (Exp 10, d=1.69) driven by the *second pass*
itself (any revision improves plans), or by the *scale hint content* in the revision prompt?

**Conditions (n=30 stratified tasks):**
- Rev_hint: baseline plan → revise WITH scale hint (difficulty + step count + types)
- Rev_blind: baseline plan → revise WITHOUT hint ("improve this plan")
- Compare both vs A baseline

### Overall scores

| Condition | Avg score | N | t vs baseline | p | Cohen's d |
|-----------|-----------|---|--------------|---|-----------|
| A baseline | {fmt(avg(base_scores))} | {len(base_scores)} | — | — | — |
| Rev_blind (no hint) | {fmt(avg(blind_scores))} | {len(blind_scores)} | {fmt(tb)} | {fmtp(pb)} | {fmt(db)} |
| Rev_hint (with hint) | {fmt(avg(hint_scores))} | {len(hint_scores)} | {fmt(th)} | {fmtp(ph)} | {fmt(dh)} |

Rev_hint vs Rev_blind: t = {fmt(thb)}, p = {fmtp(phb)}, Cohen's d = {fmt(dhb)}

### By difficulty label

| Difficulty | Baseline | Rev_blind | Rev_hint | N |
|------------|---------|----------|---------|---|
{dt_str}

**Interpretation:**
- Rev_blind ≈ Rev_hint → second pass mechanism explains revision gain (hint is inert in revision)
- Rev_hint > Rev_blind (d > 0.3) → scale hint content causally drives revision improvement
- Both > baseline → revision helps regardless; hint is a bonus
""")

    # Analytical experiments
    run_exp_g_analytical(parts)
    run_exp_h_analytical(parts)

    SYNTHESIS_REPORT.write_text("".join(parts), encoding="utf-8")
    print(f"\n  Report written → {SYNTHESIS_REPORT}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "e"):
        run_exp_e()
    if mode in ("all", "f"):
        run_exp_f()

    print("\n=== Generating report ===")
    generate_report()
    print("Done.")
