---
spec_version: "2"
answer_id: "decomposition-v2-schema-vs-truncation"
answered_by_task: "t0020_v2_truncation_vs_schema_ablation"
date_answered: "2026-05-01"
---
# v2 schema vs truncation decomposition

## Question

How much of the +57 pp v2-tree-full vs v1-flat-truncated acceptance-rate gap on the matched t0014
pool is due to the v2 tree schema itself versus the full (untruncated) problem text?

## Answer

The v2 tree schema explains essentially all of the gap: switching from flat-v1 to tree-v2 while
holding the 1500-char truncation constant lifts the haiku judge accept rate from 33% to 90%, a +57
pp jump (95% Wilson CI on the difference: +23 pp to +77 pp). Adding the full untruncated problem
text on top of the v2 schema lifts accept from 90% to 95%, a further +5 pp (95% CI -15 pp to +26
pp), which is not statistically significant. The headline +62 pp v2-full vs v1-truncated gap is
therefore ~92% pure-schema and ~8% pure-text-length on the 20-row matched pool.

## Sources

* Task: `t0005_hierarchical_annotation_pilot_v1`
* Task: `t0009_hierarchical_annotation_v2`
* Task: `t0014_v2_annotator_sonnet_rerun`
* Task: `t0020_v2_truncation_vs_schema_ablation`
