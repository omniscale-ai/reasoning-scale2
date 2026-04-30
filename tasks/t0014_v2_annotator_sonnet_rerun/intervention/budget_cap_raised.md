---
task_id: "t0014_v2_annotator_sonnet_rerun"
date: "2026-04-30"
kind: "budget-cap-raise"
status: "approved"
---
# Intervention: Raise Annotator Budget Cap From $10 to $25

## Trigger

The first annotator run halted at row 52 of 115 with `total_cost_usd = $10.9175`, $0.92 over the $10
cap declared in `task.json` and originally set in `code/constants.py`
(`ANNOTATOR_BUDGET_CAP_USD = 10.00`). The empirical per-row cost of `claude-sonnet-4-6` invoked
through the Claude Code CLI on this prompt is **~$0.195/row**, roughly 4× the per-row figure used to
size the original $5 estimate ($5/115 ≈ $0.043/row). Cause: the CLI's cache-creation overhead on the
long v2 system prompt was not accounted for in the dry-run gate.

## Decision

User authorized raising `ANNOTATOR_BUDGET_CAP_USD` to **$25.00** to finish the remaining 52 rows.

* Headroom: $25 - $10.92 already spent = **$14.08** for the remaining 52 rows.
* Empirical projection: 52 × $0.195 ≈ **$10.14**. Comfortable inside the new cap.
* Worst case at +50% pricing variance: 52 × $0.30 = $15.60. Would exceed $25 only if every remaining
  row is significantly more expensive than the average so far. Acceptable risk.

## Trail

* Original cap: `task.json` `expected_cost_usd ~ $5`, hard cap `$10`.
* New cap: still applies only to t0014. Project-level budget unaffected.
* All 52 remaining rows must be annotated to satisfy plan REQ-1 ("exactly 115 rows"); a partial
  result would compromise the schema-vs-model deconfound.

## Implementation

* `code/constants.py` — `ANNOTATOR_BUDGET_CAP_USD: float = 25.00` (was 10.00).
* The annotator script restarts and resumes from the JSONL it left at row 52 (idempotent on
  `_pilot_row_index`).

This intervention is closed once the annotator finishes 115 rows and the `costs.json` final total is
recorded in `results/costs.json` with this intervention referenced.
