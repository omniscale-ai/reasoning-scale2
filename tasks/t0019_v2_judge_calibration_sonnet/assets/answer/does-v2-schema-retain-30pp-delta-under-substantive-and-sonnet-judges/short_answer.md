---
spec_version: "2"
answer_id: "does-v2-schema-retain-30pp-delta-under-substantive-and-sonnet-judges"
answered_by_task: "t0019_v2_judge_calibration_sonnet"
date_answered: "2026-05-01"
---
# Does v2 keep a 30+ pp delta under substantive and sonnet judges?

## Question

Does the v2 schema retain a 30+ pp accept-rate delta over v1 under a substantive judge and under a
sonnet judge, or is the +57 pp t0014 headline an artefact of haiku judge anchoring?

## Answer

The evidence is mixed. Under substantive-sonnet the schema-only delta is +24.6 pp and under
model-rotated-sonnet it is +37.3 pp, vs the t0014 baseline of +58.0 pp. The +57 pp headline does not
cleanly survive a stronger judge, but neither does it collapse below +30 pp on both configurations;
the answer depends on which sonnet judge configuration is treated as canonical.

## Sources

* Task: `t0005_hierarchical_annotation_pilot_v1`
* Task: `t0009_hierarchical_annotation_v2`
* Task: `t0014_v2_annotator_sonnet_rerun`
* Task: `t0015_correct_proxy_benchmark_labels`
