#!/usr/bin/env python3
"""
Collect 100 diversified tasks+solutions from multiple benchmarks and annotate
each with (a) difficulty level and (b) a step graph via Claude API.

Target sources (25 each):
  - FrontierScience-Olympiad  (openai/frontierscience, HuggingFace)
  - SWE-bench Verified        (princeton-nlp/SWE-bench_Verified, HuggingFace)
  - τ-bench                   (TIGER-Lab/tau-bench, HuggingFace)
  - WorkArena++               (ServiceNow-AI/workarena, HuggingFace)

Outputs:
  data/annotation_pilot/tasks_annotated.jsonl
  data/annotation_pilot/ANNOTATION_REPORT.md

Usage:
  python scripts/collect_and_annotate.py [--tasks-per-source 25] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parents[1]))

from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ANNOTATION_MODEL = "claude-sonnet-4-6"
MAX_ANNOTATION_TOKENS = 2048
OUT_DIR = Path("data/annotation_pilot")
TASKS_JSONL = OUT_DIR / "tasks_annotated.jsonl"
REPORT_MD = OUT_DIR / "ANNOTATION_REPORT.md"

COMMANDS_DIR = Path(".claude/commands")

# HuggingFace dataset identifiers
HF_DATASETS: dict[str, dict] = {
    "FrontierScience-Olympiad": {
        "hf_id": "openai/frontierscience",
        "split": "test",
        "cache_dir": "data/cache",
    },
    "SWE-bench Verified": {
        "hf_id": "princeton-nlp/SWE-bench_Verified",
        "split": "test",
        "cache_dir": None,
    },
    # tau-bench is not published on HuggingFace Hub.
    # Fallback: HumanEval (code generation with canonical solutions).
    "tau-bench": {
        "hf_id": "TIGER-Lab/tau-bench",
        "hf_id_candidates": ["TIGER-Lab/tau-bench", "tau-bench-org/tau-bench"],
        "hf_id_fallback": "openai_humaneval",
        "split": "test",
        "cache_dir": None,
    },
    # WorkArena++ requires a live ServiceNow instance — not on HuggingFace Hub.
    # Fallback: Mind2Web (web-navigation agent tasks with action traces).
    "WorkArena++": {
        "hf_id": "ServiceNow-AI/workarena",
        "hf_id_candidates": ["ServiceNow-AI/workarena", "ServiceNow-AI/workarena-plus"],
        "hf_id_fallback": "osunlp/Mind2Web",
        "split": "test",
        "cache_dir": None,
    },
}


# ---------------------------------------------------------------------------
# Task dataclass
# ---------------------------------------------------------------------------


@dataclass
class RawTask:
    task_id: str
    benchmark: str
    domain: str
    problem: str
    solution: str  # correct solution / patch / reference trajectory
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnnotatedTask:
    task_id: str
    benchmark: str
    domain: str
    problem: str
    solution: str
    metadata: dict[str, Any]
    difficulty: dict[str, Any] | None = None
    steps: dict[str, Any] | None = None
    annotation_model: str = ANNOTATION_MODEL
    annotated_at: str = ""
    token_usage: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Dataset loaders
# ---------------------------------------------------------------------------


def load_frontierscience(n: int, seed: int = 42) -> list[RawTask]:
    """Stratified by subject: ~n/3 from each of physics, chemistry, biology."""
    import random

    from datasets import load_dataset

    cfg = HF_DATASETS["FrontierScience-Olympiad"]
    ds = load_dataset(cfg["hf_id"], split=cfg["split"], cache_dir=cfg["cache_dir"])

    subjects = ["physics", "chemistry", "biology"]
    rng = random.Random(seed)
    tasks: list[RawTask] = []

    # Round-robin fill to handle uneven n
    buckets: dict[str, list] = {}
    for subj in subjects:
        buckets[subj] = [r for r in ds if str(r.get("subject", "")).lower() == subj]
        rng.shuffle(buckets[subj])

    per_subject = n // len(subjects)
    remainder = n % len(subjects)

    for i, subj in enumerate(subjects):
        take = per_subject + (1 if i < remainder else 0)
        sample = buckets[subj][:take]
        for row in sample:
            tid = str(row.get("task_group_id") or row.get("id") or f"fs_{len(tasks)}")
            problem = str(row.get("problem") or "")
            answer = str(row.get("answer") or row.get("ground_truth") or "")
            solution = (
                f"Ground truth answer: {answer}\n\n"
                "(Full derivation not provided; annotator should infer solution steps "
                "from the problem structure and the known correct answer.)"
            )
            tasks.append(
                RawTask(
                    task_id=f"fs_{tid}",
                    benchmark="FrontierScience-Olympiad",
                    domain=subj,
                    problem=problem,
                    solution=solution,
                    metadata={"subject": subj, "source_id": tid},
                )
            )
    return tasks[:n]


def load_swe_bench(n: int, seed: int = 42) -> list[RawTask]:
    """Stratified by repo: at most 2 tasks per repo to maximise diversity."""
    import random
    from collections import defaultdict

    from datasets import load_dataset

    cfg = HF_DATASETS["SWE-bench Verified"]
    ds = load_dataset(cfg["hf_id"], split=cfg["split"])

    rng = random.Random(seed)
    rows = list(ds)
    rng.shuffle(rows)

    # Group by repo, cap per-repo contributions
    MAX_PER_REPO = 2
    repo_counts: dict[str, int] = defaultdict(int)
    selected: list[dict] = []
    for row in rows:
        repo = str(row.get("repo") or "unknown")
        if repo_counts[repo] < MAX_PER_REPO:
            selected.append(row)
            repo_counts[repo] += 1
        if len(selected) >= n:
            break

    tasks: list[RawTask] = []
    for row in selected:
        iid = str(row.get("instance_id") or f"swe_{len(tasks)}")
        problem = str(row.get("problem_statement") or "")
        patch = str(row.get("patch") or row.get("solution") or "")
        repo = str(row.get("repo") or "")
        domain = repo.split("/")[-1] if repo else "software engineering"
        solution = f"Repository: {repo}\n\nCorrect patch (git diff):\n```diff\n{patch[:3000]}\n```"
        tasks.append(
            RawTask(
                task_id=f"swe_{iid}",
                benchmark="SWE-bench Verified",
                domain=domain,
                problem=problem[:2000],
                solution=solution,
                metadata={"repo": repo, "instance_id": iid},
            )
        )
    return tasks


def _load_humaneval_as_proxy(n: int, seed: int = 42) -> list[RawTask]:
    """HumanEval fallback: code generation tasks with canonical Python solutions."""
    import random

    from datasets import load_dataset

    ds = load_dataset("openai_humaneval", split="test", trust_remote_code=False)
    rows = list(ds)
    rng = random.Random(seed)
    rng.shuffle(rows)
    tasks: list[RawTask] = []

    for row in rows[:n]:
        tid = str(row.get("task_id") or f"he_{len(tasks)}")
        problem = str(row.get("prompt") or "")
        solution = (
            f"Canonical solution:\n```python\n{row.get('canonical_solution', '')}\n```\n\n"
            f"Test cases:\n```python\n{row.get('test', '')[:500]}\n```"
        )
        tasks.append(
            RawTask(
                task_id=f"he_{tid.replace('/', '_')}",
                benchmark="tau-bench",
                domain="code generation (HumanEval proxy — tau-bench unavailable on HF)",
                problem=problem,
                solution=solution,
                metadata={
                    "original_id": tid,
                    "proxy_for": "tau-bench",
                    "hf_source": "openai_humaneval",
                },
            )
        )
    return tasks


def load_tau_bench(n: int, seed: int = 42) -> list[RawTask]:
    """Try tau-bench on HuggingFace; fall back to HumanEval if unavailable."""
    import random

    from datasets import load_dataset

    cfg = HF_DATASETS["tau-bench"]
    tasks: list[RawTask] = []
    per_subset = max(1, n // 2)

    # Try native tau-bench first
    for candidate_id in cfg.get("hf_id_candidates", [cfg["hf_id"]]):
        for subset_name in ["retail", "airline"]:
            ds = None
            for split_name in [cfg["split"], "train", "validation"]:
                for name_kwarg in [{"name": subset_name}, {}]:
                    try:
                        ds = load_dataset(candidate_id, split=split_name, **name_kwarg)
                        break
                    except Exception:
                        continue
                if ds is not None:
                    break
            if ds is None:
                continue

            rows = list(ds)
            rng = random.Random(seed)
            rng.shuffle(rows)

            for row in rows[:per_subset]:
                tid = str(row.get("task_id") or row.get("id") or f"tau_{len(tasks)}")
                instruction = str(
                    row.get("instruction") or row.get("task") or row.get("problem") or ""
                )
                ref = (
                    row.get("actions")
                    or row.get("tool_calls")
                    or row.get("trajectory")
                    or row.get("solution")
                    or row.get("answer")
                    or ""
                )
                solution = (
                    json.dumps(ref, ensure_ascii=False, indent=2)
                    if isinstance(ref, (list, dict))
                    else str(ref)
                )
                tasks.append(
                    RawTask(
                        task_id=f"tau_{subset_name}_{tid}",
                        benchmark="tau-bench",
                        domain=f"customer service ({subset_name})",
                        problem=instruction[:2000],
                        solution=solution[:2000],
                        metadata={"subset": subset_name, "source_id": tid},
                    )
                )
        if tasks:
            break

    if not tasks:
        tasks = _load_humaneval_as_proxy(n=n, seed=seed)

    return tasks[:n]


def _load_mind2web_as_proxy(n: int, seed: int = 42) -> list[RawTask]:
    """Mind2Web fallback: web-navigation agent tasks with action traces."""
    import math
    import random
    from collections import defaultdict

    from datasets import load_dataset

    ds = load_dataset("osunlp/Mind2Web", split="train", trust_remote_code=False)
    rows = list(ds)
    rng = random.Random(seed)
    rng.shuffle(rows)

    # Stratify by subdomain for diversity
    subdomain_buckets: dict[str, list] = defaultdict(list)
    for row in rows:
        key = str(row.get("subdomain") or row.get("domain") or "general")
        subdomain_buckets[key].append(row)

    n_domains = len(subdomain_buckets)
    per_domain = max(1, math.ceil(n / n_domains))
    tasks: list[RawTask] = []

    for subdomain, bucket in sorted(subdomain_buckets.items()):
        for row in bucket[:per_domain]:
            if len(tasks) >= n:
                break
            tid = str(row.get("annotation_id") or f"m2w_{len(tasks)}")
            goal = str(row.get("confirmed_task") or row.get("task") or "")
            # action_reprs is a list of action strings
            action_reprs = row.get("action_reprs") or []
            solution = "Reference action trace:\n" + "\n".join(
                f"  {i + 1}. {a}" for i, a in enumerate(action_reprs[:20])
            )
            domain = str(row.get("subdomain") or row.get("domain") or "web")
            tasks.append(
                RawTask(
                    task_id=f"m2w_{tid}",
                    benchmark="WorkArena++",
                    domain=f"web agent / {domain} (Mind2Web proxy — WorkArena++ unavailable on HF)",
                    problem=goal,
                    solution=solution,
                    metadata={
                        "website": row.get("website", ""),
                        "subdomain": subdomain,
                        "proxy_for": "WorkArena++",
                        "hf_source": "osunlp/Mind2Web",
                    },
                )
            )
        if len(tasks) >= n:
            break

    return tasks[:n]


def load_workarena(n: int, seed: int = 42) -> list[RawTask]:
    """Try WorkArena++ on HuggingFace; fall back to Mind2Web if unavailable."""
    import math
    import random
    from collections import defaultdict

    from datasets import load_dataset

    cfg = HF_DATASETS["WorkArena++"]
    tasks: list[RawTask] = []

    for candidate_id in cfg.get("hf_id_candidates", [cfg["hf_id"]]):
        ds = None
        for split_name in ["test", "train", "validation"]:
            try:
                ds = load_dataset(candidate_id, split=split_name)
                break
            except Exception:
                continue
        if ds is None:
            continue

        rng = random.Random(seed)
        rows = list(ds)
        rng.shuffle(rows)

        type_buckets: dict[str, list] = defaultdict(list)
        for row in rows:
            ttype = str(row.get("task_type") or row.get("type") or "unknown")
            type_buckets[ttype].append(row)

        n_types = max(1, len(type_buckets))
        per_type = max(1, math.ceil(n / n_types))

        for ttype, bucket in sorted(type_buckets.items()):
            for row in bucket[:per_type]:
                if len(tasks) >= n:
                    break
                tid = str(row.get("task_id") or row.get("id") or f"wa_{len(tasks)}")
                problem = str(
                    row.get("goal")
                    or row.get("task")
                    or row.get("instruction")
                    or row.get("problem")
                    or ""
                )
                ref = (
                    row.get("solution")
                    or row.get("actions")
                    or row.get("steps")
                    or row.get("answer")
                    or ""
                )
                solution = (
                    json.dumps(ref, ensure_ascii=False, indent=2)
                    if isinstance(ref, (list, dict))
                    else str(ref)
                )
                tasks.append(
                    RawTask(
                        task_id=f"wa_{tid}",
                        benchmark="WorkArena++",
                        domain=f"enterprise UI ({ttype})",
                        problem=problem[:2000],
                        solution=solution[:2000],
                        metadata={"task_type": ttype, "source_id": tid},
                    )
                )
            if len(tasks) >= n:
                break
        break  # found a working dataset

    if not tasks:
        tasks = _load_mind2web_as_proxy(n=n, seed=seed)

    return tasks[:n]


# ---------------------------------------------------------------------------
# Annotation client (uses `claude` CLI — no API key needed)
# ---------------------------------------------------------------------------


class AnnotationClient:
    """Wraps ClaudeCLIClient for single-turn annotation calls."""

    def __init__(self, model_id: str = ANNOTATION_MODEL):
        import src.models.claude_cli_client as _cli_mod
        from src.models.claude_cli_client import ClaudeCLIClient

        # Patch timeout before instantiation
        _cli_mod.ClaudeCLIClient  # ensure loaded
        client = ClaudeCLIClient(model_id=model_id)
        client.MAX_RETRIES = 6
        client.RETRY_BASE_DELAY = 5.0
        self._client = client
        self.model_id = model_id
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def call(self, prompt: str) -> tuple[str, dict]:
        text, usage = self._client.complete(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_ANNOTATION_TOKENS,
        )
        self.total_input_tokens += usage.get("input_tokens", 0)
        self.total_output_tokens += usage.get("output_tokens", 0)
        return text, usage


# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------


def _load_skill_prompt(skill_name: str) -> str:
    """Load skill markdown, strip YAML frontmatter, return prompt body."""
    path = COMMANDS_DIR / f"{skill_name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {path}")
    text = path.read_text(encoding="utf-8")
    # Strip YAML frontmatter (--- ... ---)
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    return text.strip()


MAX_TASK_CHARS = 3000  # keep prompts well within CLI limits


def build_difficulty_prompt(task: RawTask) -> str:
    template = _load_skill_prompt("annotate-difficulty")
    problem = task.problem[:MAX_TASK_CHARS]
    solution = task.solution[:MAX_TASK_CHARS]
    arguments = f"PROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"
    return template.replace("$ARGUMENTS", arguments)


def build_steps_prompt(task: RawTask) -> str:
    template = _load_skill_prompt("annotate-steps")
    problem = task.problem[:MAX_TASK_CHARS]
    solution = task.solution[:MAX_TASK_CHARS]
    arguments = f"PROBLEM:\n{problem}\n\nSOLUTION:\n{solution}"
    return template.replace("$ARGUMENTS", arguments)


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------


def _extract_json(text: str) -> dict | None:
    """Extract the first valid JSON object from model output."""
    # Try direct parse first
    try:
        return json.loads(text.strip())
    except Exception:
        pass
    # Find ```json ... ``` or ``` ... ``` blocks
    for pattern in [r"```json\s*([\s\S]+?)```", r"```\s*([\s\S]+?)```"]:
        m = re.search(pattern, text)
        if m:
            try:
                return json.loads(m.group(1).strip())
            except Exception:
                pass
    # Find first { ... } spanning the whole remaining text
    m = re.search(r"\{[\s\S]+\}", text)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# Main annotation loop
# ---------------------------------------------------------------------------


def annotate_task(
    task: RawTask,
    client: AnnotationClient,
    dry_run: bool = False,
) -> AnnotatedTask:
    result = AnnotatedTask(
        task_id=task.task_id,
        benchmark=task.benchmark,
        domain=task.domain,
        problem=task.problem,
        solution=task.solution,
        metadata=task.metadata,
        annotated_at=datetime.now(UTC).isoformat(),
    )

    if dry_run:
        result.difficulty = {"overall_difficulty": 0, "overall_label": "DRY_RUN"}
        result.steps = {"graph_summary": {"total_nodes": 0, "comment": "DRY_RUN"}}
        return result

    total_usage: dict[str, int] = {"input_tokens": 0, "output_tokens": 0}

    # --- Difficulty annotation ---
    try:
        prompt = build_difficulty_prompt(task)
        text, usage = client.call(prompt)
        for k in total_usage:
            total_usage[k] += usage.get(k, 0)
        parsed = _extract_json(text)
        if parsed:
            result.difficulty = parsed
        else:
            result.errors.append(f"difficulty: could not parse JSON from response: {text[:200]}")
    except Exception as e:
        msg = str(e)
        result.errors.append(f"difficulty: {msg}")
        print(f"    [!] difficulty failed for {task.task_id[:40]}: {msg[:120]}")

    # Small delay to respect rate limits
    time.sleep(1.0)

    # --- Steps annotation ---
    try:
        prompt = build_steps_prompt(task)
        text, usage = client.call(prompt)
        for k in total_usage:
            total_usage[k] += usage.get(k, 0)
        parsed = _extract_json(text)
        if parsed:
            result.steps = parsed
        else:
            result.errors.append(f"steps: could not parse JSON from response: {text[:200]}")
    except Exception as e:
        msg = str(e)
        result.errors.append(f"steps: {msg}")
        print(f"    [!] steps failed for {task.task_id[:40]}: {msg[:120]}")

    result.token_usage = total_usage
    return result


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------


def load_done_ids(path: Path) -> set[str]:
    """Only mark a task as done if it has no errors and both annotations succeeded."""
    done: set[str] = set()
    if not path.exists():
        return done
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if not obj.get("errors") and obj.get("difficulty") and obj.get("steps"):
                    done.add(obj["task_id"])
            except Exception:
                pass
    return done


def append_result(path: Path, result: AnnotatedTask) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(result), ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def generate_report(results: list[AnnotatedTask], elapsed_s: float) -> str:
    from collections import Counter, defaultdict

    benchmarks = [r.benchmark for r in results]
    bench_counts = Counter(benchmarks)

    # Difficulty stats
    labels = [r.difficulty.get("overall_label", "?") for r in results if r.difficulty]
    label_counts = Counter(labels)
    difficulties = [r.difficulty.get("overall_difficulty", 0) for r in results if r.difficulty]
    avg_diff = sum(difficulties) / len(difficulties) if difficulties else 0

    # Per-benchmark difficulty
    bench_diff: dict[str, list[int]] = defaultdict(list)
    for r in results:
        if r.difficulty:
            bench_diff[r.benchmark].append(r.difficulty.get("overall_difficulty", 0))

    # Step type distribution
    type_counts: Counter = Counter()
    total_nodes = 0
    for r in results:
        if r.steps and "nodes" in r.steps:
            for node in r.steps["nodes"]:
                type_counts[node.get("type", "?")] += 1
                total_nodes += 1

    # Per-benchmark step summary
    bench_nodes: dict[str, list[int]] = defaultdict(list)
    for r in results:
        if r.steps and r.steps.get("graph_summary"):
            n = r.steps["graph_summary"].get("total_nodes", 0)
            bench_nodes[r.benchmark].append(n)

    # Error stats
    error_count = sum(1 for r in results if r.errors)
    total_input = sum(r.token_usage.get("input_tokens", 0) for r in results)
    total_output = sum(r.token_usage.get("output_tokens", 0) for r in results)

    # Per-task table
    rows_md = []
    for r in results:
        diff_score = r.difficulty.get("overall_difficulty", "?") if r.difficulty else "?"
        diff_label = r.difficulty.get("overall_label", "?") if r.difficulty else "?"
        n_nodes = r.steps.get("graph_summary", {}).get("total_nodes", "?") if r.steps else "?"
        n_bot = len(r.steps.get("bottleneck_node_ids", [])) if r.steps else "?"
        errs = "✗" if r.errors else "✓"
        rows_md.append(
            f"| `{r.task_id[:30]}` | {r.benchmark} | {r.domain[:20]} "
            f"| {diff_score} | {diff_label} | {n_nodes} | {n_bot} | {errs} |"
        )

    dim_names = [
        "domain_depth",
        "reasoning_complexity",
        "conceptual_leaps",
        "plan_length",
        "interdependence",
    ]
    dim_avgs: dict[str, list[float]] = defaultdict(list)
    for r in results:
        if r.difficulty and "dimensions" in r.difficulty:
            for dim in dim_names:
                v = r.difficulty["dimensions"].get(dim, {})
                if isinstance(v, dict):
                    score = v.get("score", None)
                else:
                    score = v
                if score is not None:
                    dim_avgs[dim].append(float(score))

    dim_rows = "\n".join(
        f"| {d} | {sum(vs) / len(vs):.2f} | {min(vs):.0f}–{max(vs):.0f} |"
        if vs
        else f"| {d} | — | — |"
        for d, vs in ((d, dim_avgs.get(d, [])) for d in dim_names)
    )

    # Proxy / availability notes
    proxy_tasks = [r for r in results if r.metadata.get("proxy_for")]
    proxy_lines = ""
    if proxy_tasks:
        proxy_map = {r.metadata["proxy_for"]: r.metadata.get("hf_source", "?") for r in proxy_tasks}
        proxy_lines = "\n### Data availability notes\n\n"
        for target, source in proxy_map.items():
            proxy_lines += (
                f"- **{target}** — not published on HuggingFace Hub at collection time; "
                f"replaced with **`{source}`** as domain proxy.\n"
            )
        proxy_lines += "\n"

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    report = f"""# Annotation Pilot Report

**Generated:** {now}
**Annotation model:** `{ANNOTATION_MODEL}`
**Total tasks annotated:** {len(results)}
**Elapsed time:** {elapsed_s / 60:.1f} min
**Token usage:** {total_input:,} input / {total_output:,} output
**Annotation errors:** {error_count} / {len(results)} tasks

{proxy_lines}---

## 1. Dataset composition

| Benchmark | Tasks collected |
|-----------|-----------------|
{"".join(f"| {b} | {c} |" + chr(10) for b, c in sorted(bench_counts.items()))}
| **Total** | **{len(results)}** |

---

## 2. Difficulty distribution

| Label | Count |
|-------|-------|
{"".join(f"| {l} | {c} |" + chr(10) for l, c in sorted(label_counts.items(), key=lambda x: x[
                1
            ], reverse=True))}

**Average overall difficulty:** {avg_diff:.2f} / 5

### Per benchmark

| Benchmark | Avg difficulty | Min | Max |
|-----------|----------------|-----|-----|
{"".join(f"| {b} | {sum(vs) / len(vs):.2f} | {min(vs):.0f} | {max(vs):.0f} |" + chr(10) for b, vs in sorted(bench_diff.items()) if vs)}

---

## 3. Difficulty dimensions (all tasks)

| Dimension | Average | Range |
|-----------|---------|-------|
{dim_rows}

---

## 4. Step graph structure

**Total nodes across all tasks:** {total_nodes}
**Avg nodes per task:** {total_nodes / len(results):.1f}

### Node type distribution

| Type | Count | % |
|------|-------|---|
{"".join(f"| {t} | {c} | {100 * c / total_nodes:.1f}% |" + chr(10) for t, c in type_counts.most_common()) if total_nodes else "| — | — | — |"}

### Avg nodes per task by benchmark

| Benchmark | Avg nodes |
|-----------|-----------|
{"".join(f"| {b} | {sum(vs) / len(vs):.1f} |" + chr(10) for b, vs in sorted(bench_nodes.items()) if vs)}

---

## 5. Per-task annotation table

> **Columns:** task_id · benchmark · domain · difficulty score (1–5) · difficulty label · total step nodes · bottleneck nodes · annotation OK?

| Task ID | Benchmark | Domain | Diff | Label | Nodes | Bottlenecks | OK |
|---------|-----------|--------|------|-------|-------|-------------|-----|
{"".join(r + chr(10) for r in rows_md)}

---

## 6. Next steps

- [ ] Manual review of all 100 annotations (spot-check difficulty labels and step graphs)
- [ ] Validate cross-benchmark difficulty calibration (are "Hard" tasks comparable across domains?)
- [ ] Use step graph node counts and types as features for the main reasoning-scale experiment
- [ ] Consider adding `difficulty` and `n_steps` fields to `BenchmarkTask` schema

---

*This report was auto-generated by `scripts/collect_and_annotate.py`.*
"""
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks-per-source", type=int, default=25)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dry-run", action="store_true", help="Skip API calls, write dummy annotations")
    p.add_argument("--out-dir", type=Path, default=OUT_DIR)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    n = args.tasks_per_source

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    tasks_path = out_dir / "tasks_annotated.jsonl"
    report_path = out_dir / "ANNOTATION_REPORT.md"

    # ---- Collect tasks ----
    TOTAL_TARGET = n * 4  # 100 by default
    print(f"=== Collecting tasks (target: {TOTAL_TARGET}) ===")

    loaders = [
        ("FrontierScience-Olympiad", load_frontierscience),
        ("SWE-bench Verified", load_swe_bench),
        ("tau-bench", load_tau_bench),
        ("WorkArena++", load_workarena),
    ]

    # First pass: try each source
    source_tasks: dict[str, list[RawTask]] = {}
    for name, loader_fn in loaders:
        print(f"  Loading {name}...", end=" ", flush=True)
        try:
            tasks = loader_fn(n=n, seed=args.seed)
            print(f"{len(tasks)} tasks")
            source_tasks[name] = tasks
        except Exception as e:
            print(f"FAILED: {e}")
            source_tasks[name] = []

    # Rebalance: distribute shortfall from failed sources to successful ones
    loaded_counts = {k: len(v) for k, v in source_tasks.items()}
    total_loaded = sum(loaded_counts.values())
    shortfall = TOTAL_TARGET - total_loaded

    if shortfall > 0 and any(c < n for c in loaded_counts.values()):
        successful = [k for k, c in loaded_counts.items() if c >= n // 2]
        if successful:
            extra_per = max(1, shortfall // len(successful))
            print(f"\n  Rebalancing: {shortfall} missing tasks spread across {successful}")
            for name in successful:
                loader_fn = dict(loaders)[name]
                try:
                    extra = loader_fn(n=loaded_counts[name] + extra_per, seed=args.seed + 1)
                    source_tasks[name] = extra
                    print(f"    {name}: {loaded_counts[name]} → {len(extra)}")
                except Exception:
                    pass

    # Flatten and deduplicate by task_id
    seen_ids: set[str] = set()
    all_tasks: list[RawTask] = []
    for tasks in source_tasks.values():
        for t in tasks:
            if t.task_id not in seen_ids:
                seen_ids.add(t.task_id)
                all_tasks.append(t)

    # Final composition log
    from collections import Counter

    comp = Counter(t.benchmark for t in all_tasks)
    proxy_notes = {
        t.benchmark: t.metadata.get("hf_source", "") for t in all_tasks if "proxy_for" in t.metadata
    }
    print(f"\nFinal composition ({len(all_tasks)} tasks):")
    for bname, cnt in sorted(comp.items()):
        note = f"  [proxy: {proxy_notes.get(bname, '')}]" if bname in proxy_notes else ""
        print(f"  {bname}: {cnt}{note}")
    if not all_tasks:
        print("No tasks loaded. Exiting.")
        sys.exit(1)

    # ---- Annotate ----
    print("\n=== Annotating tasks ===")
    done_ids = load_done_ids(tasks_path)
    to_annotate = [t for t in all_tasks if t.task_id not in done_ids]
    print(f"  Already done: {len(done_ids)} | Remaining: {len(to_annotate)}")

    if not args.dry_run:
        import shutil

        if not shutil.which("claude"):
            print(
                "\nERROR: `claude` CLI not found in PATH.\n"
                "  This script uses the Claude Code CLI (no API key needed).\n"
                "  Make sure Claude Code is installed and `claude` is on PATH.\n"
                "  Use --dry-run to skip API calls."
            )
            sys.exit(1)

    client = AnnotationClient(ANNOTATION_MODEL)
    annotated_results: list[AnnotatedTask] = []

    t0 = time.time()
    for task in tqdm(to_annotate, desc="Annotating", unit="task"):
        result = annotate_task(task, client, dry_run=args.dry_run)
        append_result(tasks_path, result)
        annotated_results.append(result)

    elapsed = time.time() - t0

    # Reload all results — deduplicate by task_id, keep last (most recent) entry
    seen: dict[str, AnnotatedTask] = {}
    with tasks_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                seen[obj["task_id"]] = AnnotatedTask(**obj)
            except Exception:
                pass
    all_results = list(seen.values())

    print(f"\nTotal annotated: {len(all_results)}")
    if client.total_input_tokens:
        print(f"Tokens used: {client.total_input_tokens:,} in / {client.total_output_tokens:,} out")

    # ---- Report ----
    print("\n=== Generating report ===")
    report_md = generate_report(all_results, elapsed)
    report_path.write_text(report_md, encoding="utf-8")
    print(f"  Report written: {report_path}")
    print(f"  Results JSONL: {tasks_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
