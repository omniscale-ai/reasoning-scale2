#!/usr/bin/env python3
"""
Diploma Experiments — Scale Awareness in LLM Agents
=====================================================

Five experiments extending the main A/B/C scale awareness study:

  Exp 1  — Blind re-scoring: re-judge existing plans without condition labels
            using a 4-criteria rubric (coverage/ordering/granularity/feasibility)
  Exp 2  — Ablation: 4 partial-hint conditions to isolate which component helps
            C1=label-only  C2=count-only  C3=types-only  C4=count+types
  Exp 3  — Self-calibration: model predicts its own difficulty/steps, then plans
            with that self-generated context (condition D)
  Exp 4  — Noise condition: wrong hint on Expert/Hard tasks (condition E)
  Exp 5  — Repeated sampling: 3 plans per condition on 24 Hard/Expert/Medium tasks

Outputs:
  data/scale_awareness/blind_scores.jsonl
  data/scale_awareness/ablation_results.jsonl
  data/scale_awareness/self_calibration.jsonl
  data/scale_awareness/repeated_sampling.jsonl
  data/scale_awareness/DIPLOMA_REPORT.md
"""

from __future__ import annotations

import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

# reuse helpers from main experiment
from scripts.scale_awareness_experiment import (
    PLAN_BASE,
    PLAN_STEP_AWARE,
    cli_call,
    extract_steps,
    load_annotated,
    plan_length_score_to_steps,
)

# ── paths ─────────────────────────────────────────────────────────────────────
OUT_DIR = Path("data/scale_awareness")
RESULTS_JSONL = OUT_DIR / "results.jsonl"  # existing A/B/C results
BLIND_JSONL = OUT_DIR / "blind_scores.jsonl"
ABLATION_JSONL = OUT_DIR / "ablation_results.jsonl"
SELFCAL_JSONL = OUT_DIR / "self_calibration.jsonl"
REPEATED_JSONL = OUT_DIR / "repeated_sampling.jsonl"
REPORT_MD = OUT_DIR / "DIPLOMA_REPORT.md"

# ── blind judge prompt (Exp 1 + shared by Exp 2-5) ───────────────────────────

BLIND_JUDGE_PROMPT = """\
Rate the following plan for solving this problem.

Problem:
{problem}

Plan:
{plan_text}

Rate each criterion from 1 to 5:
- Coverage (1-5): does the plan address all key aspects of the problem?
- Ordering (1-5): are steps in a logical, dependency-respecting sequence?
- Granularity (1-5): are steps at the right level of detail?
- Feasibility (1-5): are steps concrete and actionable?

Respond ONLY in this exact format:
Coverage: X
Ordering: X
Granularity: X
Feasibility: X
Overall: X
Reasoning: one sentence

Coverage:"""


def blind_judge(problem: str, plan_steps: list[str]) -> dict:
    """Run blind 4-criteria judge. Returns dict with scores and reasoning."""
    plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(plan_steps))
    text = cli_call(BLIND_JUDGE_PROMPT.format(problem=problem, plan_text=plan_text))
    result = {
        "coverage": None,
        "ordering": None,
        "granularity": None,
        "feasibility": None,
        "overall": None,
        "reasoning": "",
    }
    for key in ["coverage", "ordering", "granularity", "feasibility", "overall"]:
        m = re.search(rf"{key}:\s*([1-5])", text, re.IGNORECASE)
        if m:
            result[key] = float(m.group(1))
    m = re.search(r"Reasoning:\s*(.+)", text, re.IGNORECASE)
    if m:
        result["reasoning"] = m.group(1).strip()[:200]
    # fallback overall = mean of 4 criteria
    if result["overall"] is None:
        subs = [
            result[k]
            for k in ["coverage", "ordering", "granularity", "feasibility"]
            if result[k] is not None
        ]
        result["overall"] = round(sum(subs) / len(subs), 2) if subs else None
    return result


# ── ablation plan prompts (Exp 2) ─────────────────────────────────────────────

PLAN_LABEL_ONLY = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT: Difficulty: {label}

Problem: {problem}

JSON output only:"""

PLAN_COUNT_ONLY = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT: Expected steps: ~{expected_n_steps}

Problem: {problem}

JSON output only:"""

PLAN_TYPES_ONLY = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT:
Expected step types:
{step_type_lines}

Problem: {problem}

JSON output only:"""

PLAN_COUNT_TYPES = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT:
- Expected total steps: ~{expected_n_steps}
- Expected step types:
{step_type_lines}

Problem: {problem}

JSON output only:"""

PLAN_NOISE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT (use to calibrate depth and number of steps):
- Overall difficulty: Easy (2/5)
- Expected total steps: ~3
- Expected step composition:
  - strategic: ~1 step(s)
  - computational: ~2 step(s)

Problem: {problem}

JSON output only:"""

# ── self-calibration predict prompt (Exp 3) ───────────────────────────────────

PREDICT_PROMPT = """\
Before planning, estimate the difficulty and structure of this problem.

Problem: {problem}

Respond ONLY as a JSON object — no explanation, no preamble:
{{
  "difficulty": <integer 1-5>,
  "n_steps": <integer, expected number of solution steps>,
  "step_types": {{
    "strategic": <integer>,
    "conceptual": <integer>,
    "computational": <integer>,
    "verification": <integer>
  }}
}}

JSON:"""

PLAN_SELF_AWARE = """\
You are ONLY a plan generator. You do NOT solve problems. You ONLY output JSON.
DO NOT calculate anything. DO NOT use LaTeX. DO NOT write explanations.
Output ONLY a JSON object with key "steps" containing 3 to 6 steps.
Each step: {{"number": int, "action": "plain English description", "needs": ["..."], "produces": ["..."]}}

SCALE CONTEXT (your own estimate):
- Estimated difficulty: {difficulty}/5
- Estimated total steps: ~{n_steps}
- Estimated step types:
{step_type_lines}

Problem: {problem}

JSON output only:"""


# ── data structures ───────────────────────────────────────────────────────────


@dataclass
class BlindScore:
    task_id: str
    condition: str  # "baseline", "diff_aware", "step_aware"
    coverage: float | None = None
    ordering: float | None = None
    granularity: float | None = None
    feasibility: float | None = None
    overall: float | None = None
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class AblationResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    condition: str  # "C1","C2","C3","C4","E"
    plan: list[str] = field(default_factory=list)
    coverage: float | None = None
    ordering: float | None = None
    granularity: float | None = None
    feasibility: float | None = None
    overall: float | None = None
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class SelfCalResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    difficulty_score: float
    # Phase A — predictions
    predicted_difficulty: int | None = None
    predicted_n_steps: int | None = None
    predicted_step_types: dict = field(default_factory=dict)
    # Ground truth from annotation
    annotated_difficulty: float = 0.0
    annotated_n_steps: int = 0
    annotated_step_types: dict = field(default_factory=dict)
    # Phase B — plan D (with self-generated context)
    plan_self_aware: list[str] = field(default_factory=list)
    coverage: float | None = None
    ordering: float | None = None
    granularity: float | None = None
    feasibility: float | None = None
    overall: float | None = None
    reasoning: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class RepeatedResult:
    task_id: str
    benchmark: str
    difficulty_label: str
    condition: str  # "baseline" or "step_aware"
    sample_idx: int  # 0,1,2
    plan: list[str] = field(default_factory=list)
    coverage: float | None = None
    ordering: float | None = None
    granularity: float | None = None
    feasibility: float | None = None
    overall: float | None = None
    errors: list[str] = field(default_factory=list)


# ── generic checkpoint helpers ────────────────────────────────────────────────


def load_done_keys(path: Path, key_fields: list[str]) -> set[tuple]:
    """Return set of tuples of key_fields already processed."""
    done = set()
    if not path.exists():
        return done
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                done.add(tuple(obj[k] for k in key_fields))
            except Exception:
                pass
    return done


def append_result(path: Path, obj) -> None:
    with path.open("a") as f:
        f.write(json.dumps(asdict(obj), ensure_ascii=False) + "\n")


# ── helpers ───────────────────────────────────────────────────────────────────


def get_task_context(task: dict) -> dict:
    """Extract reusable fields from an annotated task dict."""
    diff = task["difficulty"]
    steps = task.get("steps") or {}
    dims = diff.get("dimensions", {})
    nodes = steps.get("nodes", [])

    def dim_score(name: str) -> int:
        v = dims.get(name, {})
        return int(v.get("score", 3)) if isinstance(v, dict) else int(v or 3)

    plan_len_score = dim_score("plan_length")
    expected_n_steps = plan_length_score_to_steps(plan_len_score)
    type_counts = Counter(n.get("type", "?") for n in nodes)
    step_type_lines = (
        "\n".join(f"  - {t}: ~{c} step(s)" for t, c in sorted(type_counts.items()))
        or "  - (no annotation available)"
    )

    return {
        "problem": (task.get("problem") or "")[:2000],
        "label": diff.get("overall_label", "?"),
        "score": diff.get("overall_difficulty", "?"),
        "expected_n_steps": expected_n_steps,
        "type_counts": dict(type_counts),
        "step_type_lines": step_type_lines,
    }


# ── Experiment 1: Blind Re-scoring ────────────────────────────────────────────


def run_exp1():
    """Re-judge all existing A/B/C plans with blind 4-criteria rubric."""
    print("\n=== Exp 1: Blind Re-scoring ===")
    done = load_done_keys(BLIND_JSONL, ["task_id", "condition"])

    # load existing results
    existing: dict[str, dict] = {}
    with RESULTS_JSONL.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                existing[obj["task_id"]] = obj

    tasks_conditions = [
        (tid, cond, obj)
        for tid, obj in existing.items()
        for cond in ["baseline", "diff_aware", "step_aware"]
    ]

    todo = [(tid, cond, obj) for tid, cond, obj in tasks_conditions if (tid, cond) not in done]
    print(f"  Already done: {len(done)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for tid, cond, obj in tqdm(todo, desc="Blind judging", unit="plan"):
        plan_key = f"plan_{cond}"
        plan_steps = obj.get(plan_key, [])
        problem = (obj.get("problem") or "")[:2000]

        rec = BlindScore(task_id=tid, condition=cond)
        if not plan_steps:
            rec.errors.append("no plan stored")
            append_result(BLIND_JSONL, rec)
            continue

        try:
            scores = blind_judge(problem, plan_steps)
            for k, v in scores.items():
                if hasattr(rec, k):
                    setattr(rec, k, v)
        except Exception as e:
            rec.errors.append(str(e))

        append_result(BLIND_JSONL, rec)
        time.sleep(1)

    print("  Exp 1 done.")


# ── Experiment 2 + 4: Ablation + Noise ────────────────────────────────────────


def run_exp2_and_exp4():
    """Ablation (C1-C4) on all tasks + noise condition (E) on Expert/Hard."""
    print("\n=== Exp 2+4: Ablation + Noise ===")
    done = load_done_keys(ABLATION_JSONL, ["task_id", "condition"])

    tasks = load_annotated()
    print(f"  {len(tasks)} annotated tasks")

    # Build work items
    work = []
    for t in tasks:
        ctx = get_task_context(t)
        label = t["difficulty"].get("overall_label", "?")
        for cond in ["C1", "C2", "C3", "C4"]:
            work.append((t, ctx, cond))
        if label in ("Expert", "Hard"):
            work.append((t, ctx, "E"))  # noise condition

    todo = [(t, ctx, cond) for t, ctx, cond in work if (t["task_id"], cond) not in done]
    print(f"  Work items: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, ctx, cond in tqdm(todo, desc="Ablation", unit="item"):
        rec = AblationResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=task["difficulty"].get("overall_label", "?"),
            difficulty_score=float(task["difficulty"].get("overall_difficulty", 0)),
            condition=cond,
        )

        # generate plan
        try:
            if cond == "C1":
                prompt = PLAN_LABEL_ONLY.format(problem=ctx["problem"], label=ctx["label"])
            elif cond == "C2":
                prompt = PLAN_COUNT_ONLY.format(
                    problem=ctx["problem"], expected_n_steps=ctx["expected_n_steps"]
                )
            elif cond == "C3":
                prompt = PLAN_TYPES_ONLY.format(
                    problem=ctx["problem"], step_type_lines=ctx["step_type_lines"]
                )
            elif cond == "C4":
                prompt = PLAN_COUNT_TYPES.format(
                    problem=ctx["problem"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                )
            else:  # E — noise
                prompt = PLAN_NOISE.format(problem=ctx["problem"])

            text = cli_call(prompt)
            rec.plan = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        time.sleep(1)

        # judge
        if rec.plan:
            try:
                scores = blind_judge(ctx["problem"], rec.plan)
                for k, v in scores.items():
                    if hasattr(rec, k):
                        setattr(rec, k, v)
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(ABLATION_JSONL, rec)

    print("  Exp 2+4 done.")


# ── Experiment 3: Self-calibration ────────────────────────────────────────────


def run_exp3():
    """Phase A: model predicts difficulty. Phase B: plans with own prediction."""
    print("\n=== Exp 3: Self-calibration ===")
    done = load_done_keys(SELFCAL_JSONL, ["task_id"])

    tasks = load_annotated()
    todo = [t for t in tasks if t["task_id"] not in {k[0] for k in done}]
    print(f"  {len(tasks)} tasks | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task in tqdm(todo, desc="Self-cal", unit="task"):
        ctx = get_task_context(task)
        diff = task["difficulty"]
        nodes = (task.get("steps") or {}).get("nodes", [])
        ann_types = dict(Counter(n.get("type", "?") for n in nodes))

        rec = SelfCalResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            difficulty_score=float(diff.get("overall_difficulty", 0)),
            annotated_difficulty=float(diff.get("overall_difficulty", 0)),
            annotated_n_steps=ctx["expected_n_steps"],
            annotated_step_types=ctx["type_counts"],
        )

        # Phase A: predict
        predicted = {}
        try:
            raw = cli_call(PREDICT_PROMPT.format(problem=ctx["problem"]))
            for pat in [r"```json\s*([\s\S]+?)```", r"```\s*([\s\S]+?)```"]:
                m = re.search(pat, raw)
                if m:
                    predicted = json.loads(m.group(1))
                    break
            if not predicted:
                predicted = json.loads(raw)
        except Exception:
            try:
                m = re.search(r"\{[\s\S]+\}", raw)
                if m:
                    predicted = json.loads(m.group(0))
            except Exception as e:
                rec.errors.append(f"predict parse: {e}")

        rec.predicted_difficulty = predicted.get("difficulty")
        rec.predicted_n_steps = predicted.get("n_steps")
        rec.predicted_step_types = predicted.get("step_types", {})

        time.sleep(1)

        # Phase B: plan with self-generated context
        if rec.predicted_difficulty and rec.predicted_n_steps:
            pred_type_lines = (
                "\n".join(
                    f"  - {t}: ~{c} step(s)" for t, c in sorted(rec.predicted_step_types.items())
                )
                or "  - (not predicted)"
            )
            try:
                text = cli_call(
                    PLAN_SELF_AWARE.format(
                        problem=ctx["problem"],
                        difficulty=rec.predicted_difficulty,
                        n_steps=rec.predicted_n_steps,
                        step_type_lines=pred_type_lines,
                    )
                )
                rec.plan_self_aware = extract_steps(text)
            except Exception as e:
                rec.errors.append(f"plan: {e}")

            time.sleep(1)

            if rec.plan_self_aware:
                try:
                    scores = blind_judge(ctx["problem"], rec.plan_self_aware)
                    for k, v in scores.items():
                        if hasattr(rec, k):
                            setattr(rec, k, v)
                except Exception as e:
                    rec.errors.append(f"judge: {e}")
                time.sleep(1)

        append_result(SELFCAL_JSONL, rec)

    print("  Exp 3 done.")


# ── Experiment 5: Repeated Sampling ───────────────────────────────────────────


def run_exp5():
    """3 plan samples per condition (A and C) on 24 Hard/Expert/Medium tasks."""
    print("\n=== Exp 5: Repeated Sampling ===")
    done = load_done_keys(REPEATED_JSONL, ["task_id", "condition", "sample_idx"])

    tasks = load_annotated()

    # Pick 8 Expert + 8 Hard + 8 Medium, sorted by task_id for reproducibility
    by_label: dict[str, list] = defaultdict(list)
    for t in sorted(tasks, key=lambda x: x["task_id"]):
        by_label[t["difficulty"].get("overall_label", "?")].append(t)

    sample_tasks: list[dict] = []
    for label, n in [("Expert", 8), ("Hard", 8), ("Medium", 8)]:
        sample_tasks.extend(by_label[label][:n])
    print(f"  Sampling {len(sample_tasks)} tasks (Expert/Hard/Medium × 8 each)")

    work = [
        (t, cond, idx)
        for t in sample_tasks
        for cond in ["baseline", "step_aware"]
        for idx in [0, 1, 2]
    ]
    todo = [(t, cond, idx) for t, cond, idx in work if (t["task_id"], cond, idx) not in done]
    print(f"  Work items: {len(work)} | Remaining: {len(todo)}")

    from tqdm import tqdm

    for task, cond, idx in tqdm(todo, desc="Repeated", unit="item"):
        ctx = get_task_context(task)
        diff = task["difficulty"]

        rec = RepeatedResult(
            task_id=task["task_id"],
            benchmark=task["benchmark"],
            difficulty_label=diff.get("overall_label", "?"),
            condition=cond,
            sample_idx=idx,
        )

        try:
            if cond == "baseline":
                prompt = PLAN_BASE.format(problem=ctx["problem"])
            else:
                prompt = PLAN_STEP_AWARE.format(
                    problem=ctx["problem"],
                    label=ctx["label"],
                    score=ctx["score"],
                    expected_n_steps=ctx["expected_n_steps"],
                    step_type_lines=ctx["step_type_lines"],
                )
            text = cli_call(prompt)
            rec.plan = extract_steps(text)
        except Exception as e:
            rec.errors.append(f"plan: {e}")

        time.sleep(1)

        if rec.plan:
            try:
                scores = blind_judge(ctx["problem"], rec.plan)
                for k, v in scores.items():
                    if hasattr(rec, k):
                        setattr(rec, k, v)
            except Exception as e:
                rec.errors.append(f"judge: {e}")
            time.sleep(1)

        append_result(REPEATED_JSONL, rec)

    print("  Exp 5 done.")


# ── Report ────────────────────────────────────────────────────────────────────


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
    return rows


def avg(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def t_stat(a: list, b: list) -> tuple[float, float]:
    """Welch's t-test, returns (t, p-approx via normal)."""
    import math

    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0
    m1, m2 = sum(a) / n1, sum(b) / n2
    s1 = math.sqrt(sum((x - m1) ** 2 for x in a) / (n1 - 1))
    s2 = math.sqrt(sum((x - m2) ** 2 for x in b) / (n2 - 1))
    se = math.sqrt(s1**2 / n1 + s2**2 / n2)
    if se == 0:
        return 0.0, 1.0
    t = (m1 - m2) / se
    # normal approx for p (two-tailed)
    z = abs(t)
    # simple erf approximation
    p = 2 * (1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
    return t, p


def cohens_d(a: list, b: list) -> float:
    import math

    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return 0.0
    m1, m2 = sum(a) / n1, sum(b) / n2
    s1 = sum((x - m1) ** 2 for x in a) / (n1 - 1)
    s2 = sum((x - m2) ** 2 for x in b) / (n2 - 1)
    sp = math.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    return (m1 - m2) / sp if sp else 0.0


def pearson_r(a: list, b: list) -> float:
    import math

    n = min(len(a), len(b))
    if n < 2:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((x - mb) ** 2 for x in b))
    return num / (da * db) if da * db else 0.0


def generate_diploma_report() -> str:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    # ── load data ──────────────────────────────────────────────────────────────
    original = load_jsonl(RESULTS_JSONL)  # A/B/C from main experiment
    blind = load_jsonl(BLIND_JSONL)  # Exp 1
    ablation = load_jsonl(ABLATION_JSONL)  # Exp 2+4
    selfcal = load_jsonl(SELFCAL_JSONL)  # Exp 3
    repeated = load_jsonl(REPEATED_JSONL)  # Exp 5

    # ── Exp 1: blind vs original correlation ──────────────────────────────────
    # build lookup: task_id+condition → blind overall
    blind_lookup = {(r["task_id"], r["condition"]): r.get("overall") for r in blind}
    # match with original scores
    orig_scores_by_cond = defaultdict(list)
    blind_scores_by_cond = defaultdict(list)
    for r in original:
        for cond, orig_key in [
            ("baseline", "score_baseline"),
            ("diff_aware", "score_diff_aware"),
            ("step_aware", "score_step_aware"),
        ]:
            orig_s = r.get(orig_key)
            blind_s = blind_lookup.get((r["task_id"], cond))
            if orig_s is not None and blind_s is not None:
                orig_scores_by_cond[cond].append(orig_s)
                blind_scores_by_cond[cond].append(blind_s)

    all_orig = [s for v in orig_scores_by_cond.values() for s in v]
    all_blind = [s for v in blind_scores_by_cond.values() for s in v]
    r_corr = pearson_r(all_orig, all_blind)

    # blind scores by condition
    blind_avgs = {
        cond: avg(blind_scores_by_cond[cond]) for cond in ["baseline", "diff_aware", "step_aware"]
    }

    # ── Exp 2: ablation table ─────────────────────────────────────────────────
    ablation_by_cond: dict[str, list] = defaultdict(list)
    for r in ablation:
        s = r.get("overall")
        if s is not None:
            ablation_by_cond[r["condition"]].append(s)

    # baseline from blind scores
    abl_baseline_avg = blind_avgs.get("baseline") or avg(ablation_by_cond.get("baseline", []))

    # ── Exp 3: self-calibration ───────────────────────────────────────────────
    cal_rows = [
        r
        for r in selfcal
        if r.get("predicted_difficulty") is not None and r.get("annotated_difficulty") is not None
    ]
    diff_mae = (
        avg([abs((r["predicted_difficulty"] or 0) - r["annotated_difficulty"]) for r in cal_rows])
        if cal_rows
        else None
    )
    step_mae = (
        avg(
            [
                abs((r.get("predicted_n_steps") or 0) - r.get("annotated_n_steps", 0))
                for r in cal_rows
                if r.get("predicted_n_steps")
            ]
        )
        if cal_rows
        else None
    )

    # Condition D vs A/C
    selfcal_overall = [r.get("overall") for r in selfcal if r.get("overall") is not None]
    selfcal_avg = avg(selfcal_overall)

    # ── Exp 4: noise condition ────────────────────────────────────────────────
    noise_rows = [r for r in ablation if r["condition"] == "E"]
    noise_scores = [r.get("overall") for r in noise_rows if r.get("overall") is not None]
    noise_avg = avg(noise_scores)

    # For comparison, baseline blind scores on same tasks
    noise_task_ids = {r["task_id"] for r in noise_rows}
    baseline_noise_scores = [
        blind_lookup.get((tid, "baseline"))
        for tid in noise_task_ids
        if blind_lookup.get((tid, "baseline")) is not None
    ]
    baseline_noise_avg = avg(baseline_noise_scores)
    step_aware_noise_scores = [
        blind_lookup.get((tid, "step_aware"))
        for tid in noise_task_ids
        if blind_lookup.get((tid, "step_aware")) is not None
    ]
    step_aware_noise_avg = avg(step_aware_noise_scores)

    # ── Exp 5: repeated sampling / variance ───────────────────────────────────
    rep_by_cond: dict[str, list] = defaultdict(list)
    for r in repeated:
        s = r.get("overall")
        if s is not None:
            rep_by_cond[r["condition"]].append(s)

    # variance and CI per condition
    def var_and_ci(vals):
        if len(vals) < 2:
            return None, None
        m = sum(vals) / len(vals)
        s = math.sqrt(sum((x - m) ** 2 for x in vals) / (len(vals) - 1))
        ci = 1.96 * s / math.sqrt(len(vals))
        return s, ci

    rep_baseline_std, rep_baseline_ci = var_and_ci(rep_by_cond["baseline"])
    rep_step_std, rep_step_ci = var_and_ci(rep_by_cond["step_aware"])
    rep_t, rep_p = t_stat(rep_by_cond["step_aware"], rep_by_cond["baseline"])
    rep_d = cohens_d(rep_by_cond["step_aware"], rep_by_cond["baseline"])

    # overall main experiment stats with significance
    main_baseline = [r["score_baseline"] for r in original if r.get("score_baseline")]
    main_step_aware = [r["score_step_aware"] for r in original if r.get("score_step_aware")]
    main_t, main_p = t_stat(main_step_aware, main_baseline)
    main_d = cohens_d(main_step_aware, main_baseline)

    def fmt(v, decimals=2):
        return f"{v:.{decimals}f}" if v is not None else "—"

    def pfmt(p):
        if p is None:
            return "—"
        if p < 0.001:
            return "< 0.001"
        if p < 0.01:
            return f"{p:.3f}"
        return f"{p:.2f}"

    def sign(x):
        return "+" if x is not None and x >= 0 else ""

    abl_c_avg = avg(ablation_by_cond.get("step_aware_check", []))  # not collected separately

    report_lines = f"""# Diploma Report: Scale Awareness in LLM Agents

**Generated:** {now}
**Tasks in main experiment:** {len(original)}

---

## Overview

This report consolidates five experiments extending the main A/B/C scale awareness study.

| Condition | Description |
|-----------|-------------|
| A baseline    | Problem only |
| B diff_aware  | Problem + difficulty label + 5-dim scores |
| C step_aware  | Problem + difficulty + step count + type breakdown |
| C1 label-only | Problem + difficulty label only |
| C2 count-only | Problem + expected step count only |
| C3 types-only | Problem + step type breakdown only |
| C4 count+types| Problem + count + types (no label) |
| D self-aware  | Problem + model's own difficulty/step prediction |
| E noise       | Problem + deliberately wrong hint (Expert/Hard tasks) |

---

## Experiment 1 — Blind Re-scoring

Re-judged all 3×{len(original)} existing plans with a blind 4-criteria rubric
(coverage / ordering / granularity / feasibility). Condition labels hidden from judge.

### Pearson r (original holistic score vs blind rubric overall)

r = **{fmt(r_corr)}** across all {len(all_orig)} scored plan pairs.
{"✅ Strong correlation — original scores are reliable." if r_corr is not None and r_corr > 0.7 else "⚠️  Moderate correlation — original scores have some judge-label bias." if r_corr is not None and r_corr > 0.5 else "❗ Weak correlation — original scoring was affected by seeing condition labels."}

### Blind average scores by condition

| Condition | Blind avg (4-criteria) | Original avg |
|-----------|----------------------|--------------|
| A baseline   | {fmt(blind_avgs.get("baseline"))} | {fmt(avg(main_baseline))} |
| B diff_aware | {fmt(blind_avgs.get("diff_aware"))} | {fmt(avg([r.get("score_diff_aware") for r in original if r.get("score_diff_aware")]))} |
| C step_aware | {fmt(blind_avgs.get("step_aware"))} | {fmt(avg(main_step_aware))} |

---

## Experiment 2 — Ablation: Which Component Drives the Gain?

Each of 4 partial-hint conditions tested on all {len(load_annotated())} tasks.
Plans judged with blind rubric.

| Condition | Avg score | Δ vs A baseline |
|-----------|-----------|-----------------|
| A baseline    | {fmt(abl_baseline_avg)} | — |
| C1 label-only | {fmt(avg(ablation_by_cond.get("C1", [])))} | {sign((avg(ablation_by_cond.get("C1", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C1", [])) else None)}{fmt((avg(ablation_by_cond.get("C1", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C1", [])) else None)} |
| C2 count-only | {fmt(avg(ablation_by_cond.get("C2", [])))} | {sign((avg(ablation_by_cond.get("C2", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C2", [])) else None)}{fmt((avg(ablation_by_cond.get("C2", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C2", [])) else None)} |
| C3 types-only | {fmt(avg(ablation_by_cond.get("C3", [])))} | {sign((avg(ablation_by_cond.get("C3", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C3", [])) else None)}{fmt((avg(ablation_by_cond.get("C3", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C3", [])) else None)} |
| C4 count+types| {fmt(avg(ablation_by_cond.get("C4", [])))} | {sign((avg(ablation_by_cond.get("C4", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C4", [])) else None)}{fmt((avg(ablation_by_cond.get("C4", [])) - abl_baseline_avg) if abl_baseline_avg and avg(ablation_by_cond.get("C4", [])) else None)} |

---

## Experiment 3 — Self-Calibration

Model predicts difficulty and step structure before planning, then plans using
its own prediction (condition D).

### Prediction accuracy ({len(cal_rows)} tasks with predictions)

| Metric | Value |
|--------|-------|
| Difficulty MAE (predicted vs annotated, 1-5 scale) | {fmt(diff_mae)} |
| Step count MAE (predicted vs annotated) | {fmt(step_mae)} |

### Plan quality: self-generated context (D) vs annotator context (C)

| Condition | Avg score |
|-----------|-----------|
| A baseline    | {fmt(avg(main_baseline))} |
| C step_aware  | {fmt(avg(main_step_aware))} |
| D self_aware  | {fmt(selfcal_avg)} |

---

## Experiment 4 — Noise Condition

Wrong hint ("Easy, ~3 steps") applied to {len(noise_rows)} Expert/Hard tasks.

| Condition | Avg score | N |
|-----------|-----------|---|
| A baseline (same tasks) | {fmt(baseline_noise_avg)} | {len(baseline_noise_scores)} |
| C step_aware (same tasks)| {fmt(step_aware_noise_avg)} | {len(step_aware_noise_scores)} |
| E noise (wrong hint)     | {fmt(noise_avg)} | {len(noise_scores)} |

{"❗ Wrong hints hurt performance (E < A) — model uses hint content semantically." if noise_avg is not None and baseline_noise_avg is not None and noise_avg < baseline_noise_avg else "ℹ️  Wrong hints did not consistently hurt vs baseline — model may partially ignore hints." if noise_avg is not None else "No noise data yet."}

---

## Experiment 5 — Repeated Sampling (Variance Estimation)

3 independent plan samples per condition on 24 Medium/Hard/Expert tasks.

| Condition | Avg score | Std dev | 95% CI |
|-----------|-----------|---------|--------|
| A baseline  | {fmt(avg(rep_by_cond["baseline"]))} | {fmt(rep_baseline_std)} | ±{fmt(rep_baseline_ci)} |
| C step_aware| {fmt(avg(rep_by_cond["step_aware"]))} | {fmt(rep_step_std)} | ±{fmt(rep_step_ci)} |

**Welch's t-test (step_aware vs baseline):** t = {fmt(rep_t)}, p = {pfmt(rep_p)}, Cohen's d = {fmt(rep_d)}

---

## Summary: Main Experiment Statistical Validation

| Metric | Value |
|--------|-------|
| C step_aware avg | {fmt(avg(main_step_aware))} |
| A baseline avg   | {fmt(avg(main_baseline))} |
| Δ (C − A)        | {sign(avg(main_step_aware) - avg(main_baseline) if main_step_aware and main_baseline else None)}{fmt(avg(main_step_aware) - avg(main_baseline) if main_step_aware and main_baseline else None)} |
| t-statistic      | {fmt(main_t)} |
| p-value          | {pfmt(main_p)} |
| Cohen's d        | {fmt(main_d)} |
| Judge reliability (Pearson r) | {fmt(r_corr)} |

---

*Generated by `scripts/run_diploma_experiments.py`*
"""
    return report_lines


# ── main ──────────────────────────────────────────────────────────────────────


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exp",
        type=int,
        nargs="+",
        default=[1, 2, 3, 5],
        help="Which experiments to run (1=blind, 2=ablation, 3=selfcal, 5=repeated)",
    )
    parser.add_argument(
        "--report-only", action="store_true", help="Skip experiments, just regenerate report"
    )
    args = parser.parse_args()

    if not args.report_only:
        if 1 in args.exp:
            run_exp1()
        if 2 in args.exp:
            run_exp2_and_exp4()
        if 3 in args.exp:
            run_exp3()
        if 5 in args.exp:
            run_exp5()

    print("\n=== Generating diploma report ===")
    report = generate_diploma_report()
    REPORT_MD.write_text(report, encoding="utf-8")
    print(f"Report: {REPORT_MD}")
    print("All done.")


if __name__ == "__main__":
    main()
