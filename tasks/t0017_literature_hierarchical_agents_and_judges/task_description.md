# Literature: Hierarchical Agents and LLM-as-Judge

## Motivation

The post-t0014 state of this project leaves several open questions that the existing literature
likely speaks to directly:

* The v2 schema win demonstrated that *annotation granularity* matters far more than the annotator
  model swap. Recent work on hierarchical / granularity-aware agents in RL and preference learning
  is the closest external analogue.
* Open suggestions about multi-judge agreement studies (S-0009-03) and calibration of LLM judges
  call for a direct read of the "Trust or Escalate" line of work on judges with provable agreement
  guarantees.
* Several agent-evaluation suggestions in the backlog target benchmarks we have not yet adopted;
  AgentBoard and Embodied Agent Interface are the canonical references to compare against.
* A short theory anchor in the options framework (Sutton, Precup & Singh 1999) is useful as the
  foundational reference for any hierarchical-action discussion in our own writing.

This task is a focused, single-pass literature survey: download, read, and summarize a curated set
of ten papers as paper assets, then stop. It is *not* an experiment, baseline, or brainstorm — its
only deliverable is the ten paper assets and a brief synthesis in `results_detailed.md`.

## Scope

Add the following ten papers as paper assets under `assets/paper/<paper_id>/`, each with
`details.json`, the canonical summary document, and the downloaded file (or a documented download
failure):

### Hierarchical / granularity-aware agents

* P1: *Solving the Granularity Mismatch: Hierarchical Preference Learning for Long-Horizon LLM
  Agents* — ICLR 2026.
* P2: *ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL* — ICML 2024.
* P3: *Reinforcing LLM Agents via Policy Optimization with Action Decomposition* — NeurIPS 2024.
* P10: *Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning*
  — Sutton, Precup & Singh, Artificial Intelligence 1999. Theory anchor for the options framework; a
  brief summary is sufficient.

### Search and planning structure

* P4: *Can Graph Learning Improve Planning in LLM-based Agents?* — NeurIPS 2024.
* P5: *LATS: Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models*
  — ICML 2024.

### Reasoning structure discovery

* P6: *SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures* — NeurIPS 2024.

### Agent benchmarks

* P7: *Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making* — NeurIPS 2024.
* P8: *AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents* — NeurIPS 2024 Datasets
  and Benchmarks.

### LLM-as-judge methodology

* P9: *Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement*.

## Approach

The task uses the standard `/add-paper` skill once per paper. For each paper:

* Resolve identity (DOI or arXiv ID), check no duplicate already exists in the project, gather full
  metadata (CrossRef + Semantic Scholar + OpenAlex), download the PDF, write `details.json`, read
  the paper, and write the canonical summary document with all nine mandatory sections.
* When download fails (paywall, no public version), still produce metadata and an abstract-based
  summary, with `download_status: "failed"` and a populated `download_failure_reason`.
* Run the paper-asset verificator after each addition.

After all ten papers are added, write a brief synthesis (`results_detailed.md`) grouping findings by
the five themes above and identifying which suggestions in our backlog the survey strengthens or
weakens. The synthesis should be at most one page; this task is not a meta-review.

## Expected Outputs

* `assets/paper/<paper_id>/` for each of the ten papers, passing `verify_paper_asset.py` with zero
  errors.
* `results/results_summary.md` and `results/results_detailed.md` — a short synthesis grouped by
  theme, with explicit pointers to the suggestions and prior tasks each paper informs.
* `results/suggestions.json` containing any new suggestions that emerge from the reading (likely
  experiment ideas connecting hierarchical-RL findings to our annotation/calibration agenda).

## Compute and Budget

No GPU compute. Costs are limited to API calls during paper download (CrossRef, Semantic Scholar,
OpenAlex are free) and any LLM-assisted summarization that runs through the standard agent context —
well under \$5 total.

## Dependencies

None. Literature surveys are independent and should run in isolation. The task does not block on any
in-flight work.

## Risks and Fallbacks

* *Paper unavailable for download* — proceed with abstract-based summary per the paper-asset
  specification. This is acceptable for at most two of the ten; if more fail, escalate to the
  researcher rather than producing many low-quality summaries.
* *DOI mismatch or duplicate detection* — if a paper is already in the project, skip it and note the
  existing `paper_id` in the synthesis.

## Verification Criteria

* `assets/paper/` contains exactly ten subfolders, each passing `verify_paper_asset.py`.
* Every paper asset has `summary_path` populated and the canonical summary document contains all
  nine mandatory sections.
* `results/results_detailed.md` references each of the ten papers by `citation_key` at least once.
* `results/suggestions.json` is valid even if empty (`{"suggestions": []}`).

## Cross-References

* **Source suggestion** — none. This task originates from the t0016 brainstorm follow-up, where the
  researcher requested a focused read on this slice of the literature.
* **Prior tasks whose findings this informs** — t0009 (hierarchical annotation v2), t0014 (v2
  annotator sonnet rerun), t0012 (phase-2 ABC smoke), and the open suggestions S-0009-03 (multi-
  judge agreement) and S-0009-04 (truncation/schema deconfound).
