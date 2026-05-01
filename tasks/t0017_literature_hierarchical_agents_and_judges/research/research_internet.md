---
spec_version: "1"
task_id: "t0017_literature_hierarchical_agents_and_judges"
research_stage: "internet"
searches_conducted: 12
sources_cited: 10
papers_discovered: 10
date_completed: "2026-05-01"
status: "complete"
---
## Task Objective

Resolve identity, fetch metadata, and download PDFs for the ten target papers (P1-P10) on
hierarchical / granularity-aware LLM agents and LLM-as-judge methodology. Internet research in this
task is bounded by the identity-resolution and download phases of the `/add-paper` skill — there is
no exploratory web search beyond what is needed to add the ten pre-specified papers.

## Gaps Addressed

The Gaps and Limitations section of `research_papers.md` flags two issues that internet research
addresses directly:

1. **No overlap with existing corpus** — Resolved by sourcing all ten papers from public arXiv,
   OpenReview, NeurIPS proceedings, and a public university course-page mirror. None needed any
   private or paywalled access.
2. **One paper has a parenthesised DOI** — Resolved by using a public mirror
   (`https://people.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf`) for
   `Sutton1999` while preserving the original DOI `10.1016/S0004-3702(99)00052-1` in `details.json`.
   The canonical slug utility's parentheses-rejection behaviour is unchanged; the `no-doi_` fallback
   is documented as the correct workaround.

## Search Strategy

**Sources searched**: arXiv, OpenReview (ICLR 2026 accepted papers), NeurIPS 2024 main track and
NeurIPS 2024 D&B track, ICML 2024 proceedings, CrossRef Works API, Semantic Scholar Graph API,
OpenAlex Works API, ScienceDirect article landing page, and a UMass public course mirror for the
1999 paper.

**Queries executed** (12 total):

*Hierarchical / granularity-aware agents thread (P1, P2, P3, P10):*

1. `"Hierarchical Preference Learning" "Long-Horizon LLM Agents" ICLR 2026 OpenReview`
2. `ArCHer "hierarchical multi-turn RL" language model agents arXiv 2402.19446`
3. `"Reinforcing LLM Agents" "Action Decomposition" POAD BAD NeurIPS 2024 arXiv 2405.15821`
4. `Sutton Precup Singh "options" "semi-MDP" temporal abstraction Artificial Intelligence 1999`

*Search and planning structure thread (P4, P5):*

5. `"Can Graph Learning Improve Planning" LLM agents NeurIPS 2024 arXiv 2405.19119`
6. `"LATS" "Language Agent Tree Search" Monte Carlo ICML 2024 arXiv 2310.04406`

*Reasoning structure discovery thread (P6):*

7. `SELF-DISCOVER reasoning structure compose modules NeurIPS 2024 arXiv 2402.03620`

*Agent benchmarks thread (P7, P8):*

8. `"Embodied Agent Interface" goal interpretation subgoal decomposition NeurIPS 2024 arXiv 2410.07166`
9. `AgentBoard progress rate subgoal annotation NeurIPS 2024 D&B arXiv 2401.13178`

*LLM-as-judge methodology thread (P9):*

10. `"Trust or Escalate" LLM judge provable guarantees human agreement Simulated Annotators arXiv 2407.18370`

*Identity follow-ups (after candidate IDs were known):*

11. `Sutton-Precup-Singh-AIJ99.pdf people.cs.umass.edu Barto course mirror`
12. `Wu graph learning planning author affiliation Semantic Scholar OpenAlex`

**Date range**: 1999 (the foundational options paper) and 2024-2026 (modern hierarchical-agent and
judge-methodology references). No restriction on author or country.

**Inclusion criteria**: A source must be (a) a peer-reviewed paper, an accepted conference paper, or
a foundational refereed-journal paper, (b) directly cover one of the five themes, and (c) be
retrievable via a public arXiv URL, conference proceedings page, or public university mirror.

## Key Findings

### All Ten Papers Were Retrievable as PDF Without Failure

No download failed; every asset has `download_status: "success"` and at least one file in `files/`.
The arXiv-first identity resolution succeeded for the eight modern papers in a single pass. The two
pre-arXiv-era and not-yet-DOI-registered cases (`Sutton1999`, `Gao2026`) required one additional
source each: a UMass course mirror for `Sutton1999` and the OpenReview ICLR 2026 accepted-paper list
for `Gao2026`.

### Two Non-DOI Cases Were Anticipated and Handled by Specification

`Sutton1999` and `Gao2026` use the `no-doi_<Author><Year>_<slug>` fallback. The original DOI string
is preserved in `details.json` for `Sutton1999`. For `Gao2026` the DOI field is `null` and the `url`
field carries the OpenReview link. Both cases match the v3 paper-asset specification's explicit
guidance for non-DOI papers and were caught by the `/add-paper` skill's own identity resolution
phase rather than by trial-and-error.

### Author Country Resolution Has a Long Tail That Semantic Scholar Closes

Eight papers were straightforward; for `Wen2024` and `Wu2024` two co-authors had only first-author
institutions on arXiv, and Semantic Scholar filled the gap. Following the `/add-paper` rule, no
country was guessed when uncertain — the remaining unknowns are recorded as `null` in `details.json`
`country`. This produced one PA-W007 warning during a draft addition that was closed by adding
country codes for the remaining institutions.

## Methodology Insights

* The arXiv-first identity resolution is the most efficient path for 2024-2026 ML conference papers;
  CrossRef and Semantic Scholar are used to enrich rather than to bootstrap identity.
* For pre-2010 RL theory papers (`Sutton1999`), the search strategy must include both the canonical
  DOI on the publisher page and a public university course-page mirror, because the publisher PDF is
  paywalled.
* For very-recent conference papers (ICLR 2026, NeurIPS 2024), the venue's accepted-paper page is
  the canonical disambiguation source when arXiv has multiple versions or revisions.
* The per-paper agent benefits from full-PDF text extraction (via `pypdf`) over abstract-only
  summarisation when summarising older or theory-dense papers — for `Sutton1999` the resulting
  summary is materially better than the abstract-only path used for some papers in t0002.

## Discovered Papers

### [Gao2026]

* **Title**: Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
  Agents
* **Year**: 2026
* **Venue**: ICLR 2026
* **DOI**: none (not yet registered)
* **URL**: OpenReview ICLR 2026 accepted-paper page
* **Suggested categories**: `hierarchical-planning`, `granularity-conditioning`
* **Why download**: P1 of the survey; introduces hierarchical preference learning over LLM-clustered
  sub-task action groups; bias-variance argument (Proposition 1) directly justifies mid-granularity
  signals.

### [Zhou2024] (ArCHer)

* **Title**: ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL
* **Year**: 2024
* **Venue**: ICML 2024
* **DOI**: `10.48550/arXiv.2402.19446`
* **URL**: https://arxiv.org/abs/2402.19446
* **Suggested categories**: `hierarchical-planning`
* **Why download**: P2; demonstrates utterance-level off-policy critic + token-level on-policy
  actor; gains scale from 100M to 7B parameters.

### [Wen2024]

* **Title**: Reinforcing LLM Agents via Policy Optimization with Action Decomposition
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.15821`
* **URL**: https://arxiv.org/abs/2405.15821
* **Suggested categories**: `granularity-conditioning`, `hierarchical-planning`
* **Why download**: P3; formalises token-level credit assignment in free-form action spaces (POAD
  with BAD), keeping `gamma_w = 1` inside an action.

### [Wu2024]

* **Title**: Can Graph Learning Improve Planning in LLM-based Agents?
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.19119`
* **URL**: https://arxiv.org/abs/2405.19119
* **Suggested categories**: `hierarchical-planning`
* **Why download**: P4; reframes LLM-agent planning as graph decision-making; reduces hallucination
  from >20% to <1% by restricting candidates to actual graph nodes.

### [Zhou2024a] (LATS)

* **Title**: LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning
* **Year**: 2024
* **Venue**: ICML 2024
* **DOI**: `10.48550/arXiv.2310.04406`
* **URL**: https://arxiv.org/abs/2310.04406
* **Suggested categories**: `hierarchical-planning`, `agent-evaluation`
* **Why download**: P5; tree search expands fewer nodes than RAP and ToT at higher accuracy; useful
  as a strong planning baseline for the scope-aware (A) condition.

### [Zhou2024b] (SELF-DISCOVER)

* **Title**: SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2402.03620`
* **URL**: https://arxiv.org/abs/2402.03620
* **Suggested categories**: `hierarchical-planning`, `agent-evaluation`
* **Why download**: P6; structure (what to think about) beats wording (what words to use); JSON
  scaffold IMPLEMENT step is the largest single contributor in ablations.

### [Li2024]

* **Title**: Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2410.07166`
* **URL**: https://arxiv.org/abs/2410.07166
* **Suggested categories**: `agent-evaluation`
* **Why download**: P7; fine-grained error taxonomy (hallucination, affordance, missing/extra/wrong-
  order steps, precondition/effect errors) directly applicable to ABC-condition diagnostics.

### [Ma2024]

* **Title**: AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents
* **Year**: 2024
* **Venue**: NeurIPS 2024 Datasets and Benchmarks
* **DOI**: `10.48550/arXiv.2401.13178`
* **URL**: https://arxiv.org/abs/2401.13178
* **Suggested categories**: `agent-evaluation`, `benchmark-annotation`
* **Why download**: P8; introduces "progress rate" (Pearson rho > 0.95 vs humans across 1013
  environments); hard/easy split based on subgoal count.

### [Jung2024]

* **Title**: Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement
* **Year**: 2024 (arXiv); 2025 (ICLR Oral)
* **Venue**: ICLR 2025 Oral
* **DOI**: `10.48550/arXiv.2407.18370`
* **URL**: https://arxiv.org/abs/2407.18370
* **Suggested categories**: `uncertainty-calibration`, `agent-evaluation`
* **Why download**: P9; selective LLM judging with calibrated thresholds; 75% of pairwise judging on
  ChatArena delegated to Mistral-7B/GPT-3.5 while preserving an 80% human-agreement floor.

### [Sutton1999]

* **Title**: Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement
  Learning
* **Year**: 1999
* **Venue**: Artificial Intelligence (Elsevier)
* **DOI**: `10.1016/S0004-3702(99)00052-1` (parentheses force `no-doi_` fallback for the slug)
* **URL**: https://people.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf
* **Suggested categories**: `hierarchical-planning`, `granularity-conditioning`
* **Why download**: P10; theory anchor — options as `<I, pi, beta>` triples + SMDP equivalence +
  interruption + subgoal pseudo-rewards map onto the project's three-level hierarchy.

## Recommendations for This Task

1. Default future RL/options-theory references that may also have parenthesised DOIs to the
   `no-doi_` fallback rather than relaxing the `doi_to_slug` allowed-character set; the slug is
   purely a folder name and the DOI is preserved in `details.json`.
2. For ICLR/NeurIPS papers without registered DOIs, use OpenReview IDs or arXiv IDs to disambiguate
   the canonical version.
3. Run `meta.asset_types.paper.verificator` per paper after every addition; the verificator catches
   missing-country (PA-W007), invalid country code (PA-W010), and abstract-too-short (PA-W008)
   warnings that internet research can resolve cheaply.
4. Use `pypdf`-driven full-PDF text extraction for theory papers and pre-arXiv-era papers; the
   resulting summaries are materially better than the abstract-only path.

## Source Index

### [Gao2026]

* **Type**: paper
* **Title**: Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
  Agents
* **Year**: 2026
* **Venue**: ICLR 2026
* **DOI**: none (not yet registered)
* **URL**: OpenReview ICLR 2026 accepted-paper page
* **Peer-reviewed**: yes (ICLR 2026)
* **Relevance**: P1; bias-variance argument (Proposition 1) is the cleanest theoretical
  justification for mid-granularity preference signals on long-horizon tasks.

### [Zhou2024]

* **Type**: paper
* **Title**: ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL
* **Year**: 2024
* **Venue**: ICML 2024
* **DOI**: `10.48550/arXiv.2402.19446`
* **URL**: https://arxiv.org/abs/2402.19446
* **Peer-reviewed**: yes (ICML 2024)
* **Relevance**: P2; utterance-level off-policy critic + token-level on-policy actor; gains scale
  from 100M to 7B parameters.

### [Wen2024]

* **Type**: paper
* **Title**: Reinforcing LLM Agents via Policy Optimization with Action Decomposition
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.15821`
* **URL**: https://arxiv.org/abs/2405.15821
* **Peer-reviewed**: yes (NeurIPS 2024)
* **Relevance**: P3; POAD with BAD; correct way to do token-level credit assignment in free-form
  action spaces (`gamma_w = 1` inside an action).

### [Wu2024]

* **Type**: paper
* **Title**: Can Graph Learning Improve Planning in LLM-based Agents?
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2405.19119`
* **URL**: https://arxiv.org/abs/2405.19119
* **Peer-reviewed**: yes (NeurIPS 2024)
* **Relevance**: P4; reframes LLM-agent planning as graph decision-making; reduces hallucination
  from >20% to <1% by restricting candidates to graph nodes.

### [Zhou2024a]

* **Type**: paper
* **Title**: LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning
* **Year**: 2024
* **Venue**: ICML 2024
* **DOI**: `10.48550/arXiv.2310.04406`
* **URL**: https://arxiv.org/abs/2310.04406
* **Peer-reviewed**: yes (ICML 2024)
* **Relevance**: P5; tree search expands fewer nodes than RAP and ToT at higher accuracy; strong
  planning baseline for the scope-aware (A) condition.

### [Zhou2024b]

* **Type**: paper
* **Title**: SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2402.03620`
* **URL**: https://arxiv.org/abs/2402.03620
* **Peer-reviewed**: yes (NeurIPS 2024)
* **Relevance**: P6; structure (what to think about) beats wording; JSON-scaffold IMPLEMENT step is
  the largest single contributor in ablations; transfers across model families.

### [Li2024]

* **Type**: paper
* **Title**: Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making
* **Year**: 2024
* **Venue**: NeurIPS 2024
* **DOI**: `10.48550/arXiv.2410.07166`
* **URL**: https://arxiv.org/abs/2410.07166
* **Peer-reviewed**: yes (NeurIPS 2024)
* **Relevance**: P7; fine-grained error taxonomy directly applicable to ABC-condition diagnostics.

### [Ma2024]

* **Type**: paper
* **Title**: AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents
* **Year**: 2024
* **Venue**: NeurIPS 2024 Datasets and Benchmarks
* **DOI**: `10.48550/arXiv.2401.13178`
* **URL**: https://arxiv.org/abs/2401.13178
* **Peer-reviewed**: yes (NeurIPS 2024 D&B)
* **Relevance**: P8; "progress rate" metric (Pearson rho > 0.95 vs humans across 1013 environments)
  with hard/easy split based on subgoal count; six-dimensional sub-skill scoring.

### [Jung2024]

* **Type**: paper
* **Title**: Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement
* **Year**: 2024 (arXiv); 2025 (ICLR Oral)
* **Venue**: ICLR 2025 Oral
* **DOI**: `10.48550/arXiv.2407.18370`
* **URL**: https://arxiv.org/abs/2407.18370
* **Peer-reviewed**: yes (ICLR 2025 Oral)
* **Relevance**: P9; selective LLM judging with calibrated thresholds and finite-sample,
  distribution-free guarantees on human agreement.

### [Sutton1999]

* **Type**: paper
* **Title**: Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement
  Learning
* **Year**: 1999
* **Venue**: Artificial Intelligence (Elsevier)
* **DOI**: `10.1016/S0004-3702(99)00052-1` (parentheses force `no-doi_` fallback for the slug)
* **URL**: https://people.cs.umass.edu/~barto/courses/cs687/Sutton-Precup-Singh-AIJ99.pdf
* **Peer-reviewed**: yes (Elsevier *Artificial Intelligence*)
* **Relevance**: P10; theory anchor — options as `<I, pi, beta>` triples + SMDP equivalence +
  interruption + subgoal pseudo-rewards map onto the project's three-level hierarchy.
