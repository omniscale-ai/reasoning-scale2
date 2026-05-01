# Plan: Literature Survey on Hierarchical Agents and LLM-as-Judge

## Objective

Add ten curated papers as paper assets and produce a one-page synthesis grouped by five themes
(hierarchical / granularity-aware agents, search-and-planning structure, reasoning-structure
discovery, agent benchmarks, LLM-as-judge methodology) so downstream tasks can ground design choices
in current literature rather than re-deriving them.

## Approach

For each paper run the standard `/add-paper` skill once: resolve identity (DOI or arXiv ID), collect
metadata (CrossRef + Semantic Scholar + OpenAlex), download the PDF, write `details.json`, read the
paper, write the canonical summary with all nine mandatory sections, and run
`verify_paper_asset.py`. After all ten paper assets exist, write a short synthesis grouped by the
five themes and identify which backlog suggestions the survey strengthens or weakens.

## Cost Estimation

Free metadata APIs and local PDF processing only. No paid LLM calls beyond the agent context that
runs the skill. Total well under \$5.

## Step by Step

1. **Research.** Add P1-P10 as paper assets. Each paper goes through identity resolution, metadata
   collection, PDF download, summary authoring, and per-asset verification. Papers can be added in
   parallel because each lives in its own asset folder.
2. **Analysis.** Write `results/results_summary.md` (synthesis grouped by five themes, with pointers
   to the prior tasks and suggestions each paper informs) and `results/results_detailed.md`
   (extended notes plus a per-paper one-liner referencing the citation key).
3. **Reporting.** Populate task-level scaffold (plan, research, step tracker, step logs, session
   log, suggestions, costs, remote_machines_used). Run paper-asset, log, step-tracker, and
   task-complete verificators. Commit, push, open PR, run pre-merge verificator, merge.

## Remote Machines

None. Literature surveys run in the local agent context.

## Assets Needed

* CrossRef, Semantic Scholar, OpenAlex (free public APIs).
* Public arXiv mirror plus venue/author webpages for the paywalled paper (Sutton, Precup & Singh
  1999).

## Expected Assets

* `paper`: 10.

## Time Estimation

About one hour of agent wall-clock when the ten paper-asset additions run in parallel.

## Risks & Fallbacks

* *Paper unavailable for download* — proceed with abstract-based summary per the paper-asset
  specification. Acceptable for at most two of ten; otherwise escalate.
* *DOI-to-slug fails* (e.g. parentheses in older Elsevier DOIs) — fall back to the
  `no-doi_<Author><Year>_<slug>` format and store the original DOI string in `details.json`.

## Verification Criteria

* `assets/paper/` contains exactly ten subfolders, each passing the paper-asset verificator with
  zero errors.
* Every paper asset has `summary_path` populated and a canonical summary covering all nine mandatory
  sections.
* `results/results_detailed.md` references each of the ten papers by `citation_key` at least once.
* `results/suggestions.json` is valid (empty list permitted).
