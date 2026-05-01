# v2 Truncation vs Schema Ablation

## Motivation

The t0009 -> t0014 v2 upgrade changed two things at once:

1. **Schema**: flat list -> nested tree (global -> subtask -> atomic).
2. **Text completeness**: prompts moved from a 1500-char truncation to the full problem text.

On FrontierScience-Olympiad and WorkArena++, v2 saw +67% and +100% accept-rate deltas. Either the
truncation fix is doing the work (Xiong2024's prediction: longer context -> better calibration), or
the schema upgrade is doing the work, or both.

t0019 attacks the judge side of this question. **t0020 attacks the input side.** It runs a third
condition that holds the schema constant and reverts the truncation, so any drop relative to v2-full
isolates the truncation contribution.

This task covers `S-0009-04`.

## Scope

Run **one new annotation condition**: the v2 tree schema applied to the same instance pool as t0014,
but with the problem text truncated to **1500 characters** in both annotator and judge prompts
(matching the t0009 baseline exactly).

The result feeds a 3-way comparison with already-collected data:

| Condition | Schema | Text | Source |
| --- | --- | --- | --- |
| v1-flat-truncated | flat | 1500 chars | t0009 baseline |
| v2-tree-truncated | tree | 1500 chars | **this task** (new) |
| v2-tree-full | tree | full text | t0014 (existing) |

Effects decompose:

* `v2-tree-truncated - v1-flat-truncated` = pure schema effect (text held constant).
* `v2-tree-full - v2-tree-truncated` = pure text-length effect (schema held constant).
* The t0014 +57 pp delta = sum of the two.

## Deliverables

1. **Predictions asset** (`assets/predictions/v2_truncated_ablation/`): per-row annotator and judge
   outputs for the v2-tree-truncated condition. Same row pool as t0014 for paired comparison.
2. **Answer asset** addressing: "Of the t0014 +57 pp schema-only delta, how much is attributable to
   the schema upgrade vs the truncation fix, holding the other constant?"
3. **Reported metrics** with three explicit variants (one per row in the table above):
   * `accept_rate`
   * `accept_rate_stderr` (Wilson 95% CI)
   * `efficiency_inference_cost_per_item_usd`
   * `efficiency_inference_time_per_item_seconds`
4. **Decomposition table** in `results/results_detailed.md` showing the two isolated deltas with 95%
   CIs.

## Models and Configurations

* **Annotator**: claude-haiku-4-5 (matching t0009/t0014 baseline; haiku is cheap and used for the
  schema-effect reading).
* **Judge**: claude-haiku-4-5 with the t0014 original judge prompt (held constant; t0019 handles the
  judge-side calibration).
* Same instance pool as t0014 (subtract the 3 known sonnet-timeout rows so n is matched across
  conditions).

Total annotation calls: ~40 rows x 1 condition = **~40 haiku annotation calls**. Total judge calls:
~40 rows = **~40 haiku judge calls**.

## Cost Estimate

* Haiku input ~3k tokens per call x 80 calls = **~240k input tokens**.
* Haiku output ~500 tokens per call x 80 calls = **~40k output tokens**.
* At claude-haiku-4-5 pricing (approximately $0.80/M in, $4/M out): **about $0.36** haiku spend.
* Reserve for retry: **+$1**.
* Total: **~$1-2**.

## Decision Criteria

After this task:

* If `v2-tree-truncated - v1-flat-truncated >= +40 pp`, the schema upgrade is the dominant cause;
  Xiong2024's truncation hypothesis is rejected at this scale and the v2 schema deserves the
  headline.
* If `v2-tree-full - v2-tree-truncated >= +40 pp`, the truncation fix is the dominant cause; the v2
  schema wins per row roughly because v1 truncation was clipping the problem before the model could
  reason about it. The headline shifts from "tree schema helps" to "include the full problem".
* If both contributions are within +/-15 pp of each other, the two compose roughly additively and
  both must be retained for the schema-effect claim.

## Dependencies

None.

## Source Suggestion

`S-0009-04`.

## Risks and Fallbacks

* **Truncation alters which instances are answerable at all**: some FrontierScience-Olympiad
  problems may be unparseable when clipped to 1500 chars. Log per-row truncation impact (did the
  model receive a complete problem statement) and report n for each (truncated, full) split.
* **Haiku is too noisy at small n**: if accept-rate stderr exceeds +/-15 pp on the new condition,
  flag the result as inconclusive and mark the decomposition as "underpowered, needs n=80 to
  resolve". Do not over-claim from n=40.

## Verification Criteria

* Predictions asset passes `verify_predictions_asset.py`.
* Answer asset passes `verify_answer_asset.py`.
* `results/metrics.json` has the three variants with stderr.
* `results/results_detailed.md` contains the decomposition table and a paired-row check that the
  same instance ids appear in all three conditions.
* Cost in `results/costs.json` is at or below **$2**.
