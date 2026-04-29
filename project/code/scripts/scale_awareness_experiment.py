#!/usr/bin/env python3
"""
Scale Awareness Experiment
==========================
Research question: does telling an agent where it stands in terms of task
difficulty / expected step structure help it produce better plans?

Three conditions per task:
  A. baseline    — agent sees only the problem
  B. diff_aware  — agent sees problem + difficulty label + per-dimension scores
  C. step_aware  — agent sees problem + difficulty + expected step count
                   and step type breakdown from the annotation graph

Metric: plan quality rated by Claude-as-judge (1-5), plus structural metrics
  (plan length vs expected, step type alignment).

Sample: 30 tasks stratified across benchmarks and difficulty levels.

Outputs:
  data/scale_awareness/results.jsonl
  data/scale_awareness/SCALE_AWARENESS_REPORT.md
"""

from __future__ import annotations

import json
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

# ── paths ────────────────────────────────────────────────────────────────────
ANNOTATION_JSONL = Path("data/annotation_pilot/tasks_annotated.jsonl")
OUT_DIR = Path("data/scale_awareness")
RESULTS_JSONL = OUT_DIR / "results.jsonl"
REPORT_MD = OUT_DIR / "SCALE_AWARENESS_REPORT.md"

N_SAMPLE = 9999  # all tasks
CLI_TIMEOUT = 180  # seconds per call
MAX_RETRIES = 4


# ── data structures ───────────────────────────────────────────────────────────
@dataclass
class TaskResult:
    task_id: str
    benchmark: str
    domain: str
    difficulty_label: str
    difficulty_score: float
    expected_plan_len: int  # from annotation plan_length score → mapped to steps
    expected_step_types: dict  # {"strategic":N, "conceptual":N, ...}

    plan_baseline: list[str] = field(default_factory=list)
    plan_diff_aware: list[str] = field(default_factory=list)
    plan_step_aware: list[str] = field(default_factory=list)

    score_baseline: float | None = None
    score_diff_aware: float | None = None
    score_step_aware: float | None = None

    judge_reasoning_baseline: str = ""
    judge_reasoning_diff_aware: str = ""
    judge_reasoning_step_aware: str = ""

    errors: list[str] = field(default_factory=list)


# ── helpers ───────────────────────────────────────────────────────────────────


def cli_call(prompt: str, retries: int = MAX_RETRIES) -> str:
    """Call claude -p - with retry."""
    last_err = ""
    for attempt in range(retries):
        try:
            r = subprocess.run(
                ["claude", "-p", "-"],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=CLI_TIMEOUT,
            )
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
            last_err = f"rc={r.returncode} stderr={r.stderr[:120]}"
        except subprocess.TimeoutExpired:
            last_err = "timeout"
        delay = 5 * (2**attempt)
        time.sleep(delay)
    raise RuntimeError(f"CLI failed after {retries} attempts: {last_err}")


def extract_steps(text: str) -> list[str]:
    """Parse plan JSON → list of action strings."""
    for pat in [r"```json\s*([\s\S]+?)```", r"```\s*([\s\S]+?)```"]:
        m = re.search(pat, text)
        if m:
            try:
                obj = json.loads(m.group(1))
                return [s["action"] for s in obj.get("steps", [])]
            except Exception:
                pass
    try:
        obj = json.loads(text)
        return [s["action"] for s in obj.get("steps", [])]
    except Exception:
        pass
    # regex fallback: numbered lines
    lines = re.findall(r"\d+\.\s+(.+)", text)
    return lines if lines else [text[:200]]


def extract_score(text: str) -> float | None:
    m = re.search(r"\b([1-5])(?:\.\d+)?\b", text)
    return float(m.group(1)) if m else None


def plan_length_score_to_steps(score: int) -> int:
    """Map annotation plan_length score (1-5) to expected step count midpoint."""
    return {1: 2, 2: 4, 3: 6, 4: 9, 5: 13}.get(score, 5)


# ── prompts ───────────────────────────────────────────────────────────────────

PLAN_BASE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.

DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.

Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

The steps describe HOW to solve the problem, not the solution itself.
Actions must be plain English (no math, no symbols, no backslashes).

Problem: {problem}

JSON output only:"""


PLAN_DIFF_AWARE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.

DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.

Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

The steps describe HOW to solve the problem, not the solution itself.
Actions must be plain English (no math, no symbols, no backslashes).

SCALE CONTEXT (use to calibrate depth and number of steps):
- Overall difficulty: {label} ({score}/5)
- Domain knowledge required: {domain_depth}/5
- Reasoning complexity: {reasoning_complexity}/5
- Conceptual leaps needed: {conceptual_leaps}/5
- Expected plan length: {plan_length}/5
- Step interdependence: {interdependence}/5

Problem: {problem}

JSON output only:"""


PLAN_STEP_AWARE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.

DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.

Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

The steps describe HOW to solve the problem, not the solution itself.
Actions must be plain English (no math, no symbols, no backslashes).

SCALE CONTEXT:
- Overall difficulty: {label} ({score}/5)
- Expected total steps: ~{expected_n_steps}
- Expected step composition:
{step_type_lines}

Problem: {problem}

JSON output only:"""


JUDGE_PROMPT = """\
You are a plan quality evaluator. Rate the following plan for solving a given problem.

Problem:
{problem}

Plan to evaluate ({condition}):
{plan_text}

Rate the plan on a scale of 1 to 5:
  1 = completely wrong or useless
  2 = partially relevant but missing key steps
  3 = adequate, covers the main approach
  4 = good, well-structured and complete
  5 = excellent, optimal step decomposition

Respond with ONLY:
Score: X
Reasoning: one sentence

Score:"""


# ── sampling ──────────────────────────────────────────────────────────────────


def load_annotated() -> list[dict]:
    seen = {}
    with ANNOTATION_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                seen[obj["task_id"]] = obj
    return [
        v for v in seen.values() if not v.get("errors") and v.get("difficulty") and v.get("steps")
    ]


def stratified_sample(tasks: list[dict], n: int, seed: int = 42) -> list[dict]:
    """Sample n tasks, balanced across benchmarks and difficulty labels."""
    rng = random.Random(seed)
    by_bench: dict[str, list[dict]] = defaultdict(list)
    for t in tasks:
        by_bench[t["benchmark"]].append(t)

    benches = sorted(by_bench)
    per_bench = max(1, n // len(benches))
    sample: list[dict] = []

    for bench in benches:
        pool = sorted(by_bench[bench], key=lambda t: t["difficulty"]["overall_difficulty"])
        # spread across difficulty levels
        step = max(1, len(pool) // per_bench)
        chosen = [pool[i] for i in range(0, len(pool), step)][:per_bench]
        sample.extend(chosen)

    # fill remainder randomly
    remaining = [t for t in tasks if t not in sample]
    rng.shuffle(remaining)
    sample.extend(remaining[: n - len(sample)])
    rng.shuffle(sample)
    return sample[:n]


# ── experiment ────────────────────────────────────────────────────────────────


def run_task(task: dict) -> TaskResult:
    diff = task["difficulty"]
    steps = task.get("steps") or {}
    dims = diff.get("dimensions", {})
    nodes = steps.get("nodes", [])
    summary = steps.get("graph_summary") or {}

    def dim_score(name: str) -> int:
        v = dims.get(name, {})
        return int(v.get("score", 3)) if isinstance(v, dict) else int(v or 3)

    plan_len_score = dim_score("plan_length")
    expected_n_steps = plan_length_score_to_steps(plan_len_score)

    type_counts: dict[str, int] = Counter(n.get("type", "?") for n in nodes)
    step_type_lines = (
        "\n".join(f"  - {t}: ~{c} step(s)" for t, c in sorted(type_counts.items()))
        or "  - (no annotation available)"
    )

    result = TaskResult(
        task_id=task["task_id"],
        benchmark=task["benchmark"],
        domain=task["domain"],
        difficulty_label=diff.get("overall_label", "?"),
        difficulty_score=float(diff.get("overall_difficulty", 0)),
        expected_plan_len=expected_n_steps,
        expected_step_types=dict(type_counts),
    )

    problem = (task.get("problem") or "")[:2000]

    # ── A: baseline ──────────────────────────────────────────────────────────
    try:
        text = cli_call(PLAN_BASE.format(problem=problem))
        result.plan_baseline = extract_steps(text)
    except Exception as e:
        result.errors.append(f"baseline plan: {e}")

    time.sleep(1)

    # ── B: difficulty-aware ──────────────────────────────────────────────────
    try:
        text = cli_call(
            PLAN_DIFF_AWARE.format(
                problem=problem,
                label=diff.get("overall_label", "?"),
                score=diff.get("overall_difficulty", "?"),
                domain_depth=dim_score("domain_depth"),
                reasoning_complexity=dim_score("reasoning_complexity"),
                conceptual_leaps=dim_score("conceptual_leaps"),
                plan_length=plan_len_score,
                interdependence=dim_score("interdependence"),
            )
        )
        result.plan_diff_aware = extract_steps(text)
    except Exception as e:
        result.errors.append(f"diff_aware plan: {e}")

    time.sleep(1)

    # ── C: step-aware ────────────────────────────────────────────────────────
    try:
        text = cli_call(
            PLAN_STEP_AWARE.format(
                problem=problem,
                label=diff.get("overall_label", "?"),
                score=diff.get("overall_difficulty", "?"),
                expected_n_steps=expected_n_steps,
                step_type_lines=step_type_lines,
            )
        )
        result.plan_step_aware = extract_steps(text)
    except Exception as e:
        result.errors.append(f"step_aware plan: {e}")

    time.sleep(1)

    # ── Judge all three ──────────────────────────────────────────────────────
    for cond, plan_steps, score_attr, reasoning_attr in [
        ("baseline", result.plan_baseline, "score_baseline", "judge_reasoning_baseline"),
        ("diff_aware", result.plan_diff_aware, "score_diff_aware", "judge_reasoning_diff_aware"),
        ("step_aware", result.plan_step_aware, "score_step_aware", "judge_reasoning_step_aware"),
    ]:
        if not plan_steps:
            continue
        plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan_steps))
        try:
            judge_text = cli_call(
                JUDGE_PROMPT.format(
                    problem=problem,
                    condition=cond,
                    plan_text=plan_text,
                )
            )
            score = extract_score(judge_text)
            reasoning = re.sub(r".*?Reasoning:\s*", "", judge_text, flags=re.DOTALL).strip()[:200]
            setattr(result, score_attr, score)
            setattr(result, reasoning_attr, reasoning)
        except Exception as e:
            result.errors.append(f"judge {cond}: {e}")
        time.sleep(1)

    return result


# ── checkpointing ─────────────────────────────────────────────────────────────


def load_done(path: Path) -> dict[str, TaskResult]:
    done = {}
    if not path.exists():
        return done
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    obj = json.loads(line)
                    done[obj["task_id"]] = TaskResult(**obj)
                except Exception:
                    pass
    return done


def save_result(path: Path, result: TaskResult) -> None:
    with path.open("a") as f:
        f.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")


# ── report ────────────────────────────────────────────────────────────────────


def generate_report(results: list[TaskResult]) -> str:
    valid = [
        r
        for r in results
        if r.score_baseline is not None
        and r.score_diff_aware is not None
        and r.score_step_aware is not None
    ]

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0.0

    scores = {
        "baseline": [r.score_baseline for r in valid],
        "diff_aware": [r.score_diff_aware for r in valid],
        "step_aware": [r.score_step_aware for r in valid],
    }

    # Per-benchmark scores
    bench_scores: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for r in valid:
        bench_scores[r.benchmark]["baseline"].append(r.score_baseline)
        bench_scores[r.benchmark]["diff_aware"].append(r.score_diff_aware)
        bench_scores[r.benchmark]["step_aware"].append(r.score_step_aware)

    # Per-difficulty scores
    diff_scores: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for r in valid:
        diff_scores[r.difficulty_label]["baseline"].append(r.score_baseline)
        diff_scores[r.difficulty_label]["diff_aware"].append(r.score_diff_aware)
        diff_scores[r.difficulty_label]["step_aware"].append(r.score_step_aware)

    # Plan length calibration
    len_calib_rows = []
    for r in valid:
        for cond, plan in [
            ("baseline", r.plan_baseline),
            ("diff_aware", r.plan_diff_aware),
            ("step_aware", r.plan_step_aware),
        ]:
            len_calib_rows.append(
                {
                    "cond": cond,
                    "expected": r.expected_plan_len,
                    "actual": len(plan),
                    "diff_score": r.difficulty_score,
                }
            )

    def avg_len(cond):
        rows = [x for x in len_calib_rows if x["cond"] == cond]
        return avg([x["actual"] for x in rows])

    def len_error(cond):
        rows = [x for x in len_calib_rows if x["cond"] == cond]
        return avg([abs(x["actual"] - x["expected"]) for x in rows])

    # Per-task table
    task_rows = []
    for r in results:
        task_rows.append(
            f"| `{r.task_id[:28]}` | {r.benchmark[:22]} | {r.difficulty_label} "
            f"| {r.score_baseline or '?'} | {r.score_diff_aware or '?'} "
            f"| {r.score_step_aware or '?'} "
            f"| {len(r.plan_baseline)} | {len(r.plan_diff_aware)} | {len(r.plan_step_aware)} |"
        )

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    n_valid = len(valid)
    n_total = len(results)

    bench_table = ""
    for bench in sorted(bench_scores):
        bs = bench_scores[bench]
        bench_table += (
            f"| {bench} | {avg(bs['baseline']):.2f} "
            f"| {avg(bs['diff_aware']):.2f} "
            f"| {avg(bs['step_aware']):.2f} |\n"
        )

    diff_table = ""
    for label in ["Trivial", "Easy", "Medium", "Hard", "Expert"]:
        if label in diff_scores:
            ds = diff_scores[label]
            diff_table += (
                f"| {label} | {avg(ds['baseline']):.2f} "
                f"| {avg(ds['diff_aware']):.2f} "
                f"| {avg(ds['step_aware']):.2f} |\n"
            )

    # Effect size (simple mean diff)
    delta_diff = avg(scores["diff_aware"]) - avg(scores["baseline"])
    delta_step = avg(scores["step_aware"]) - avg(scores["baseline"])
    delta_diff_vs_step = avg(scores["step_aware"]) - avg(scores["diff_aware"])

    def sign(x):
        return "+" if x >= 0 else ""

    # Pre-compute finding sentences (inner string literals can't be f-strings inside an f-string)
    finding_diff = (
        f"- Scale context **improved** plan quality (B > A by {sign(delta_diff)}{delta_diff:.2f} pts on average)."
        if delta_diff > 0.1
        else f"- Scale context provided **no clear improvement** in plan quality (B vs A: {sign(delta_diff)}{delta_diff:.2f})."
    )
    finding_step = (
        f"- Step type hints further **improved** quality beyond difficulty labels alone (C > B by {sign(delta_diff_vs_step)}{delta_diff_vs_step:.2f})."
        if delta_diff_vs_step > 0.1
        else f"- Step type hints did **not** consistently improve over difficulty labels alone (C vs B: {sign(delta_diff_vs_step)}{delta_diff_vs_step:.2f})."
    )

    return f"""# Scale Awareness Experiment Report

**Generated:** {now}
**Model:** claude (CLI)
**Tasks evaluated:** {n_valid} / {n_total} fully scored

---

## Hypothesis

Does informing the agent about the task's difficulty scale and expected step
structure help it produce better plans?

Three conditions:
- **A · baseline** — agent sees only the problem
- **B · diff_aware** — agent sees problem + difficulty label + 5-dimension scores
- **C · step_aware** — agent sees problem + difficulty + expected step count + step type breakdown

---

## 1. Overall quality scores (Claude-as-judge, 1–5)

| Condition | Avg score | Δ vs baseline |
|-----------|-----------|---------------|
| A baseline    | {avg(scores["baseline"]):.2f} | — |
| B diff_aware  | {avg(scores["diff_aware"]):.2f} | {sign(delta_diff)}{delta_diff:.2f} |
| C step_aware  | {avg(scores["step_aware"]):.2f} | {sign(delta_step)}{delta_step:.2f} |

**B vs A:** {sign(delta_diff)}{delta_diff:.2f} &nbsp; **C vs A:** {sign(delta_step)}{delta_step:.2f} &nbsp; **C vs B:** {sign(delta_diff_vs_step)}{delta_diff_vs_step:.2f}

---

## 2. Scores by benchmark

| Benchmark | A baseline | B diff_aware | C step_aware |
|-----------|-----------|--------------|--------------|
{bench_table}
---

## 3. Scores by difficulty label

| Difficulty | A baseline | B diff_aware | C step_aware |
|-----------|-----------|--------------|--------------|
{diff_table}
---

## 4. Plan length calibration

| Condition | Avg plan length | Avg |expected − actual| |
|-----------|----------------|-------------------------------|
| A baseline    | {avg_len("baseline"):.1f} | {len_error("baseline"):.1f} |
| B diff_aware  | {avg_len("diff_aware"):.1f} | {len_error("diff_aware"):.1f} |
| C step_aware  | {avg_len("step_aware"):.1f} | {len_error("step_aware"):.1f} |

---

## 5. Per-task breakdown

| Task ID | Benchmark | Diff | A | B | C | len A | len B | len C |
|---------|-----------|------|---|---|---|-------|-------|-------|
{"".join(r + chr(10) for r in task_rows)}
---

## 6. Key findings

{finding_diff}
{finding_step}
- Plan length calibration {"improved" if len_error("step_aware") < len_error("baseline") else "did not clearly improve"} with scale context (|error| baseline={len_error("baseline"):.1f} → step_aware={len_error("step_aware"):.1f} steps).

---

*Generated by `scripts/scale_awareness_experiment.py`*
"""


# ── main ──────────────────────────────────────────────────────────────────────


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading annotated tasks...")
    tasks = load_annotated()
    print(f"  {len(tasks)} fully annotated tasks available")

    sample = stratified_sample(tasks, min(N_SAMPLE, len(tasks)))
    print(f"  Sampled {len(sample)} tasks")
    from collections import Counter

    comp = Counter(t["benchmark"] for t in sample)
    for b, c in sorted(comp.items()):
        print(f"    {b}: {c}")

    done = load_done(RESULTS_JSONL)
    to_run = [t for t in sample if t["task_id"] not in done]
    print(f"\n  Already done: {len(done)} | Remaining: {len(to_run)}")

    from tqdm import tqdm

    new_results: list[TaskResult] = []
    for task in tqdm(to_run, desc="Running", unit="task"):
        result = run_task(task)
        save_result(RESULTS_JSONL, result)
        new_results.append(result)

    # Reload all
    all_done = load_done(RESULTS_JSONL)
    all_results = list(all_done.values())

    print(f"\nTotal results: {len(all_results)}")
    errors = sum(1 for r in all_results if r.errors)
    print(f"Tasks with errors: {errors}")

    report = generate_report(all_results)
    REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Report: {REPORT_MD}")
    print("Done.")


if __name__ == "__main__":
    main()
