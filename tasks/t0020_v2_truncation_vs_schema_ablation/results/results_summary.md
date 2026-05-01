# Results Summary: v2 Truncation vs Schema Ablation

## Summary

Ran the third condition needed to decompose the +57 pp v2-tree-full vs v1-flat-truncated
acceptance-rate gap from t0014. Held the v2 tree schema constant and re-truncated the problem text
to 1500 chars in both the haiku annotator and haiku judge prompts. Result: the v2 tree schema
explains essentially all of the gap. The pure-schema effect is **+57 pp** (CI excludes 0); the
pure-text-length effect is **+5 pp** (CI straddles 0 and is not significant at n=20).

## Metrics

* **v1-flat-truncated accept rate**: **33%** (4 / 12), Wilson 95% CI [13.8%, 60.9%]
* **v2-tree-truncated accept rate**: **90%** (18 / 20), Wilson 95% CI [69.9%, 97.2%]
* **v2-tree-full accept rate**: **95%** (19 / 20), Wilson 95% CI [76.4%, 99.1%]
* **Pure-schema delta** (v2-tree-truncated − v1-flat-truncated): **+56.7 pp**, Newcombe-Wilson 95%
  CI [+22.5 pp, +77.5 pp]
* **Pure-text delta** (v2-tree-full − v2-tree-truncated): **+5.0 pp**, Newcombe-Wilson 95% CI
  [-15.0 pp, +25.5 pp]
* **Headline delta** (v2-tree-full − v1-flat-truncated): **+61.7 pp**, Newcombe-Wilson 95% CI
  [+28.4 pp, +81.6 pp]
* **Hierarchy completeness** under truncation: **100%** (20 / 20 rows produced complete trees)
* **Total spend**: **$2.93** ($1.55 annotator + $1.38 judge); under the $6 in-code combined cap

## Verification

* `verify_predictions_asset.py` on `v2-truncated-ablation` — PASSED (0 errors, 0 warnings)
* `verify_answer_asset.py` on `decomposition-v2-schema-vs-truncation` — PASSED (0 errors, 0
  warnings)
* `verify_task_metrics.py` — PASSED (registered metric `task_success_rate` used in three variants)
* `verify_task_results.py` — PASSED (all five mandatory result files present and valid)
* `verify_task_dependencies.py` — PASSED (no dependencies to verify)
