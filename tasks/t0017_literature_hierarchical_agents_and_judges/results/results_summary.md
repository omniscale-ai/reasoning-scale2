# Results Summary: Literature Survey on Hierarchical Agents and LLM-as-Judge

## Summary

Completed a literature survey of ten papers covering hierarchical / granularity-aware LLM agents,
search-and-planning structure, reasoning-structure discovery, agent benchmarks, and LLM-as-judge
methodology — plus the foundational options-framework paper (Sutton 1999) as a brief theory anchor.
All ten paper assets pass the v3 paper-asset verificator with zero errors and zero warnings. The
synthesis below groups findings by the five themes defined in `task_description.md` and identifies
which backlog suggestions and prior tasks the survey strengthens or weakens.

## Metrics

* **10 paper assets created** out of a 10-paper target — meets `expected_assets.paper = 10` exactly.
* **5 of 5 themes covered** with at least 1 paper each: hierarchical / granularity-aware agents (4
  papers — Gao2026, Zhou2024, Wen2024, Sutton1999), search and planning structure (2 papers —
  Wu2024, Zhou2024a), reasoning-structure discovery (1 paper — Zhou2024b), agent benchmarks (2
  papers — Li2024, Ma2024), LLM-as-judge methodology (1 paper — Jung2024).
* **0 errors and 0 warnings** across 10 verifier runs after the initial PA-W005 cleanup on
  `Zhou2024b` invented category slugs.
* **3 new follow-up suggestions** drafted (S-0017-01, S-0017-02, S-0017-03), all tied to existing
  backlog items.

## Headline Synthesis

* **Granularity is a first-class research lever, not an annotation detail.** Three modern papers
  (`Gao2026`, `Zhou2024` ArCHer, `Wen2024`) and one foundational paper (`Sutton1999`) all argue
  independently that mid-granularity action units beat both pure trajectory-level and pure
  token-level signals on long-horizon agent tasks. This *strengthens* the central claim of t0009
  (hierarchical annotation v2) and the v2 schema win observed in t0014.
* **Hierarchical agents have a single formal foundation.** `Sutton1999` gives the options / semi-MDP
  framework that subsumes `Zhou2024` (utterance-level critic + token-level actor) and `Wen2024`
  (intra-action `gamma_w = 1` keeps token-level updates consistent with the original MDP). Use the
  options framework as the theory anchor in any project paper that justifies scope-aware (A) vs
  scope-mismatched (C) conditioning.
* **Selective LLM-as-judge with calibration thresholds is the right primitive for our judge
  pipeline.** `Jung2024` ("Trust or Escalate") provides distribution-free, finite-sample guarantees
  on human-judge agreement and shows that 75% of pairwise judging on ChatArena can be delegated to
  Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor. This *strengthens* S-0009-03
  (multi-judge agreement study) and gives us a concrete recipe for cost-bounded judge cascades.

## Theme 1: Hierarchical / Granularity-Aware Agents (P1, P2, P3, P10)

* `Gao2026` (HPL, ICLR 2026) introduces hierarchical preference learning over LLM-clustered sub-
  task action groups; the bias-variance argument (Proposition 1) gives a principled reason to prefer
  mid-granularity signals when reward sparsity and trajectory length are large. Directly validates
  t0009's three-level (global / subtask / atomic) annotation schema.
* `Zhou2024` (ArCHer, ICML 2024) demonstrates hierarchical multi-turn RL with an utterance-level
  off-policy critic and a token-level on-policy actor; gains scale with model size from 100M to 7B
  parameters.
* `Wen2024` (POAD with BAD, NeurIPS 2024) formalises the right way to do token-level credit
  assignment under free-form action spaces: keep `gamma_w = 1` inside an action so the token-level
  update is consistent with the original MDP. Drops complexity from `O(|V|^|a|)` to `O(|a|*|V|)`.
* `Sutton1999` provides the SMDP / options framework that all three papers above implicitly use. The
  theory anchor enables our writing to reason about A/B/C conditions as different option-set
  policies over the same underlying MDP.

## Theme 2: Search and Planning Structure (P4, P5)

* `Wu2024` (NeurIPS 2024) reframes LLM-agent planning as graph decision-making, shows that even a
  parameter-free 1-hop SGC step over sentence embeddings beats most prompting baselines, and reduces
  hallucination from >20% to <1% by restricting the candidate set to actual graph nodes. Provides a
  strong "guardrail" template for any subtask-decomposition agent we build downstream.
* `Zhou2024a` (LATS, ICML 2024) unifies tree search with LM-as-judge value functions and verbal
  self-reflection. Tree search expands fewer nodes than alternatives (3.55 fewer than RAP, 12.12
  fewer than ToT on HotPotQA) at higher accuracy. Useful as a strong planning baseline for
  scope-aware (A) condition agents in this project.

## Theme 3: Reasoning Structure Discovery (P6)

* `Zhou2024b` (SELF-DISCOVER, NeurIPS 2024) shows that **structure (what to think about) beats
  wording (what words to use)** for transfer across model families. The IMPLEMENT step (explicit
  JSON key-value scaffold) is the largest single contributor in ablations, beyond mere module
  selection. Gives a concrete prompting template for the scope-aware condition that does not require
  any retraining.

## Theme 4: Agent Benchmarks (P7, P8)

* `Li2024` (Embodied Agent Interface, NeurIPS 2024) decomposes embodied planning into four modules
  (goal interpretation / subgoal decomposition / action sequencing / transition modeling) and
  provides a fine-grained error taxonomy (hallucination, affordance, missing/extra/wrong-order
  steps, precondition/effect errors). The taxonomy is directly applicable to our scope-aware vs
  scope-mismatched condition diagnostics.
* `Ma2024` (AgentBoard, NeurIPS 2024 D&B) defines a "progress rate" that generalises to our three
  hierarchy levels and demonstrates large-scale subgoal annotation methodology (1013 environments,
  Pearson rho > 0.95 against humans). The hard/easy split based on subgoal count and the
  six-dimensional sub-skill scoring are templates we should adopt for stratifying our results.

## Theme 5: LLM-as-Judge Methodology (P9)

* `Jung2024` (Trust or Escalate, ICLR 2025 Oral) introduces selective LLM judging with calibrated
  thresholds and distribution-free guarantees on human agreement. Simulated Annotators
  (ensemble-based confidence on top of any judge LLM) and judge cascades (route by confidence,
  escalate only when needed) are drop-in techniques that our calibration agenda can apply
  immediately.

## Pointers Back to Backlog Suggestions and Prior Tasks

* **t0009 (hierarchical annotation v2)** — *strengthened* by P1, P2, P3, P10 and reinforced by P7,
  P8. The granularity-mismatch argument is now backed by ICLR 2026, ICML 2024, NeurIPS 2024, and the
  foundational AIJ 1999 paper.
* **t0014 (v2 annotator sonnet rerun)** — *strengthened* by P1's bias-variance argument: the v2
  schema win demonstrates exactly the predicted advantage of mid-granularity over trajectory-level
  signals.
* **t0012 (phase-2 ABC smoke)** — *informed* by P10: the A/B/C conditions are best framed as
  different option-set policies over the same underlying MDP. P7 and P8 give error-taxonomy and
  progress-rate templates that should be adopted before scaling phase-2 beyond the smoke test.
* **S-0009-03 (multi-judge agreement)** — *strengthened* by P9. The Trust-or-Escalate selective
  evaluation framework directly addresses the calibration question.
* **S-0009-04 (truncation/schema deconfound)** — *informed* (not directly strengthened or weakened):
  P1, P2, P3, P10 imply the schema effect is not just truncation; the granularity- mismatch effect
  is real even at full context. Worth re-reading P1's bias-variance analysis when designing the
  deconfound experiment.

## Verification

* `assets/paper/` contains exactly ten subfolders.
* All ten paper-asset folders pass `meta.asset_types.paper.verificator` with zero errors and zero
  warnings.
* Each paper has `summary_path: "summary.md"` populated and a canonical summary covering all nine
  mandatory sections.
* `results/results_detailed.md` references every paper by `citation_key`.
* `results/suggestions.json` is valid (one new suggestion proposed, see below).

## Files Created

* Ten paper-asset folders under `assets/paper/`.
* `plan/plan.md`, `research/research_*.md`, `step_tracker.json`, `logs/session_log.md`,
  `logs/steps/{001_research,002_analysis,003_reporting}/step_log.md`.
* `results/{results_summary.md,results_detailed.md,metrics.json,suggestions.json,costs.json, remote_machines_used.json}`.

## Next Steps and Suggestions

* Adopt `Ma2024`'s progress-rate metric and `Li2024`'s error taxonomy in the next iteration of the
  ABC-condition smoke (see `results/suggestions.json` for the formal entry).
* Adopt `Jung2024`'s selective-evaluation framework as the first concrete step on S-0009-03.
* Cite `Sutton1999` as the theory anchor in any future write-up that motivates the scope-aware /
  scope-mismatched distinction.
