"""Step 2: deterministic mapper from `steps.nodes` to global / subtask / atomic.

The mapper consumes one input row of the pilot JSONL file and emits a row of
the canonical dataset shape:

    {
      "task_id": str,
      "benchmark": str,
      "domain": str,
      "difficulty": dict,
      "problem": str,
      "hierarchy": {
        "global": str | None,
        "subtask": list[str],
        "atomic": list[str],
      },
      "gold_actions": {
        "global": str | None,
        "subtask": list[str],
        "atomic": list[str],
      },
      "annotation_model": str,
      "judge_verdict": None,
      "judge_notes": None,
      "hierarchy_completeness": bool,
    }

Mapper rules (see plan/plan.md `## Approach`):

* `global`: text from the lowest-id `strategic` node. If no strategic node
  exists, the first node by id; if no nodes, `None`.
* `subtask`: list of `conceptual` node labels in id order. If empty, falls back
  to `strategic` nodes beyond the first.
* `atomic`: `computational` and `verification` nodes concatenated in id order.

`hierarchy_completeness` is `True` iff `global is not None` and
`len(atomic) > 0`. It is `False` when the upstream LLM annotation failed
(rows with `steps is None`).
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0005_hierarchical_annotation_pilot_v1.code.constants import (
    ATOMIC_NODE_TYPES,
    NODE_TYPE_CONCEPTUAL,
    NODE_TYPE_STRATEGIC,
)


@dataclass(frozen=True, slots=True)
class HierarchyTriple:
    global_label: str | None
    subtask: list[str]
    atomic: list[str]


@dataclass(frozen=True, slots=True)
class GoldActionsTriple:
    global_label: str | None
    subtask: list[str]
    atomic: list[str]


def _safe_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _sort_nodes_by_id(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(nodes, key=lambda n: int(n.get("id", 0)))


def _node_label(node: dict[str, Any]) -> str | None:
    return _safe_str(node.get("label"))


def _node_detail(node: dict[str, Any]) -> str | None:
    return _safe_str(node.get("detail"))


def _build_hierarchy(*, nodes: list[dict[str, Any]]) -> HierarchyTriple:
    if not nodes:
        return HierarchyTriple(global_label=None, subtask=[], atomic=[])

    sorted_nodes = _sort_nodes_by_id(nodes)
    strategic_nodes = [n for n in sorted_nodes if n.get("type") == NODE_TYPE_STRATEGIC]
    conceptual_nodes = [n for n in sorted_nodes if n.get("type") == NODE_TYPE_CONCEPTUAL]
    atomic_nodes = [n for n in sorted_nodes if n.get("type") in ATOMIC_NODE_TYPES]

    if strategic_nodes:
        global_label = _node_label(strategic_nodes[0])
    else:
        global_label = _node_label(sorted_nodes[0])

    subtask_labels: list[str] = [
        label for n in conceptual_nodes if (label := _node_label(n)) is not None
    ]
    if not subtask_labels and len(strategic_nodes) > 1:
        subtask_labels = [
            label for n in strategic_nodes[1:] if (label := _node_label(n)) is not None
        ]

    atomic_labels: list[str] = [
        label for n in atomic_nodes if (label := _node_label(n)) is not None
    ]

    return HierarchyTriple(
        global_label=global_label,
        subtask=subtask_labels,
        atomic=atomic_labels,
    )


def _build_gold_actions(*, nodes: list[dict[str, Any]]) -> GoldActionsTriple:
    if not nodes:
        return GoldActionsTriple(global_label=None, subtask=[], atomic=[])

    sorted_nodes = _sort_nodes_by_id(nodes)
    strategic_nodes = [n for n in sorted_nodes if n.get("type") == NODE_TYPE_STRATEGIC]
    conceptual_nodes = [n for n in sorted_nodes if n.get("type") == NODE_TYPE_CONCEPTUAL]
    atomic_nodes = [n for n in sorted_nodes if n.get("type") in ATOMIC_NODE_TYPES]

    if strategic_nodes:
        global_detail = _node_detail(strategic_nodes[0]) or _node_label(strategic_nodes[0])
    else:
        global_detail = _node_detail(sorted_nodes[0]) or _node_label(sorted_nodes[0])

    subtask_details: list[str] = [
        detail
        for n in conceptual_nodes
        if (detail := (_node_detail(n) or _node_label(n))) is not None
    ]
    if not subtask_details and len(strategic_nodes) > 1:
        subtask_details = [
            detail
            for n in strategic_nodes[1:]
            if (detail := (_node_detail(n) or _node_label(n))) is not None
        ]

    atomic_details: list[str] = [
        detail for n in atomic_nodes if (detail := (_node_detail(n) or _node_label(n))) is not None
    ]

    return GoldActionsTriple(
        global_label=global_detail,
        subtask=subtask_details,
        atomic=atomic_details,
    )


def map_row(*, row: dict[str, Any]) -> dict[str, Any]:
    """Map one input pilot row to the canonical dataset shape."""

    steps = row.get("steps")
    if isinstance(steps, dict) and isinstance(steps.get("nodes"), list):
        nodes = list(steps["nodes"])
    else:
        nodes = []

    hierarchy = _build_hierarchy(nodes=nodes)
    gold_actions = _build_gold_actions(nodes=nodes)

    completeness = hierarchy.global_label is not None and len(hierarchy.atomic) > 0

    return {
        "task_id": row.get("task_id", ""),
        "benchmark": row.get("benchmark", ""),
        "domain": row.get("domain", ""),
        "difficulty": row.get("difficulty"),
        "problem": row.get("problem", ""),
        "hierarchy": {
            "global": hierarchy.global_label,
            "subtask": hierarchy.subtask,
            "atomic": hierarchy.atomic,
        },
        "gold_actions": {
            "global": gold_actions.global_label,
            "subtask": gold_actions.subtask,
            "atomic": gold_actions.atomic,
        },
        "annotation_model": row.get("annotation_model", ""),
        "judge_verdict": None,
        "judge_notes": None,
        "hierarchy_completeness": bool(completeness),
    }


def iter_mapped_rows(*, input_path: Path) -> Iterator[dict[str, Any]]:
    """Yield mapped rows for every line in the input JSONL file.

    Wraps each row in a try/except so a single bad row does not abort the run
    (per the Risks & Fallbacks section of the plan).
    """

    with input_path.open(encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                yield {
                    "task_id": f"_invalid_line_{line_number}",
                    "benchmark": "",
                    "domain": "",
                    "difficulty": None,
                    "problem": "",
                    "hierarchy": {"global": None, "subtask": [], "atomic": []},
                    "gold_actions": {"global": None, "subtask": [], "atomic": []},
                    "annotation_model": "",
                    "judge_verdict": None,
                    "judge_notes": f"json-decode-error: {exc}",
                    "hierarchy_completeness": False,
                }
                continue
            try:
                yield map_row(row=row)
            except (KeyError, TypeError, ValueError) as exc:
                yield {
                    "task_id": str(row.get("task_id", f"_invalid_line_{line_number}")),
                    "benchmark": str(row.get("benchmark", "")),
                    "domain": str(row.get("domain", "")),
                    "difficulty": row.get("difficulty"),
                    "problem": str(row.get("problem", "")),
                    "hierarchy": {"global": None, "subtask": [], "atomic": []},
                    "gold_actions": {"global": None, "subtask": [], "atomic": []},
                    "annotation_model": str(row.get("annotation_model", "")),
                    "judge_verdict": None,
                    "judge_notes": f"mapper-error: {exc}",
                    "hierarchy_completeness": False,
                }
