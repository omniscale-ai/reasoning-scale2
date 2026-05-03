---
spec_version: "1"
task_id: "t0032_no_anthropic_rq1_path_decision"
research_stage: "internet"
searches_conducted: 3
sources_cited: 6
papers_discovered: 0
date_completed: "2026-05-03"
status: "complete"
---
## Task Objective

Decide the no-Anthropic execution path for RQ1 ("does Method B reduce overconfident wrong-action
errors vs Method A?") given that the project's `ANTHROPIC_API_KEY` is permanently unavailable. The
task must evaluate four required options — (a) existing-results-only verdict, (b) local/open-weight
rerun, (c) alternative paid provider, (d) project-level "underpowered, provider-blocked" stop —
against cost, statistical validity, and comparability with the t0027/t0028 arm labels. Internet
research here is narrow and scoped: published per-token pricing for non-Anthropic API providers, so
that option (c) carries a defensible USD point estimate rather than a hand-wave.

## Gaps Addressed

`research-papers` is **skipped** for this task per `step_tracker.json` step 4 (rationale: no
published-paper evidence is required to choose between (a)/(b)/(c)/(d) on this project's specific
data, which is N=130 paired-instance records and an internal power grid). Consequently
`research_papers.md` does not exist and there are no paper-research gaps to address. This section is
retained for spec conformance. The only external knowledge gap this internet scan needs to fill is:
**what would option (c) cost on the cheapest credible non-Anthropic provider, expressed as a
per-paired-instance USD point estimate** — **resolved** below in Cost and Resource Analysis.

## Search Strategy

**Sources searched**: provider pricing pages (OpenAI, Google AI for Developers), recent (2026)
third-party pricing roundups, the project's own `tasks/t0026.../results/costs.json` and
`tasks/t0027.../results/costs.json` for the realized Claude Sonnet per-instance cost shape that
anchors the per-pair extrapolation.

**Queries executed** (3 total):

1. `OpenAI GPT-5 GPT-4o API pricing per million tokens 2026`
2. `Google Gemini 2.5 Pro API pricing per million tokens 2026`
3. `Anthropic Claude Sonnet API pricing per million tokens 2026` (for cross-check against realized
   t0027 per-instance costs)

**Date range**: 2026 only — pricing for 2025 and earlier is stale.

**Inclusion criteria**: Must be the provider's own published list price or a reputable third-party
pricing tracker citing the provider; must be standard (non-batch, non-cached) input and output
rates; must be a model in the same approximate tier as Claude Sonnet 4.6 (used in t0027 arm B).
Excluded: open-weight self-hosted estimates (out of scope for option (c) which is defined as
"alternative paid provider"); enterprise tier or volume-discount quotes.

**Search iterations**: Single pass per provider was sufficient — published list prices for 2026-tier
models were unambiguous from the first authoritative result.

## Key Findings

### Non-Anthropic Provider List Prices (2026)

| Provider | Model | Input $/MTok | Output $/MTok | Notes |
| --- | --- | ---: | ---: | --- |
| OpenAI | GPT-5 | 1.25 | 10.00 | General-purpose tier |
| OpenAI | GPT-4o | 2.50 | 10.00 | Older multimodal tier |
| Google | Gemini 2.5 Pro | 1.25 | 10.00 | ≤200K context; ~2× above 200K |
| Anthropic (reference) | Claude Sonnet 4.6 | 3.00 | 15.00 | Used in t0027; included for cross-check only |

Sources: [OpenAI-Pricing-2026], [Google-Gemini-Pricing-2026], [Anthropic-Pricing-2026].

The cheapest credible non-Anthropic option in this tier is **GPT-5 or Gemini 2.5 Pro at $1.25 /
$10.00**, both of which are roughly **40% cheaper on input and 33% cheaper on output** than the
Claude Sonnet 4.6 prices used in t0027.

### Realized Per-Instance Cost Shape on Claude Sonnet 4.6

From `tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json`:

* `variant_b_agent_full`: **$9.4534** for 130 instances → **~$0.0727 per instance** (arm B)
* `variant_c_agent_full`: **$9.3392** for 130 instances → **~$0.0718 per instance** (arm C)

From `tasks/t0026_phase2_abc_paired_real_runs_full/results/costs.json`:

* `runs_variant_a_usd`: **$4.4659** for 130 instances → **~$0.0344 per instance** (arm A)

Combining: a realized **paired (A+B) instance** on Claude Sonnet costs roughly **$0.034 + $0.073 ≈
$0.107**. Adding judges scales this slightly (judges run on the same paired trace, dominated by the
agent-side decode). This is the anchor for the option (c) extrapolation.

### Hypothesis: Option (c) Per-Pair Cost on a Non-Anthropic Provider

Per-pair cost is dominated by output-token volume (each arm produces a multi-decision trace; arm B
by construction emits more tokens than arm A). Output prices on GPT-5 and Gemini 2.5 Pro are
**$10.00/MTok** vs Claude Sonnet's **$15.00/MTok** — a 33% reduction on the dominant cost driver. A
defensible point estimate is therefore:

* **Per-pair cost on GPT-5 or Gemini 2.5 Pro: ~$0.07 per paired instance** (≈ $0.107 × 0.67).

### Hypothesis: Option (c) Total Cost at the t0029 Admission Cap

t0029 fixed the no-Anthropic admission cap at the same N=130 paired instances that t0027 ran plus
the planned ~218 follow-on pairs that t0030 was meant to add (per the t0029 freeze). Treating the
upper bound as **218 new paired instances** (greenfield run, not a rerun) gives:

* **Total option (c) cost: ~$15-25** (point estimate **$16**), well inside the project's $26.54
  pre-warn budget headroom.

For a smaller, statistically targeted rerun limited to the 12 discordant pairs from t0031's no-API
salvage, the cost would be **<$2** — but this collapses the option-(c) into a discordance-only
resample, which Creative Thinking (step 11) will examine separately.

## Methodology Insights

* **Anchor option (c) cost on realized t0027 numbers**, not on token-count guesses. The per-instance
  dollars in `tasks/t0027/results/costs.json` already absorb retries, judge overhead, and tool-call
  density — no further modeling is needed.

* **Use the output-token list price as the dominant scaling factor**. Across all three providers in
  this tier, output is **8×-10×** input on a per-token basis, so the per-pair cost ratio between
  providers tracks the **output** price ratio almost exactly.

* **Do not credit batch or cached-input discounts** in the option (c) point estimate. t0027 ran
  online (no batching) and the next-arm rerun under option (c) would have to match that shape to be
  even arguably comparable. Batch pricing belongs in a follow-up cost-saver suggestion, not in the
  headline point estimate.

* **Comparability disclaimer is not a cost optimization** — option (c) is "GPT-5 plays arm B" or
  "Gemini 2.5 Pro plays arm B", which is a **different policy under the same arm label** as
  t0027/t0028. The cost number is honest; the comparability claim is what must be qualified in the
  answer asset, not the dollars.

## Discovered Papers

None. This was a pricing scan, not a literature search. `papers_discovered: 0` in frontmatter.

## Recommendations for This Task

1. Use **$0.07 per paired instance** as the option (c) point estimate, with a **$15-25** total-cost
   band over 218 paired instances. Cite the realized t0027 per-instance shape and the 2026 provider
   list prices.

2. State explicitly in the answer asset that option (c) **changes the policy that plays arm B**
   (GPT-5 or Gemini 2.5 Pro replaces Claude Sonnet 4.6). The arm **label** is preserved by
   construction; the **policy under the label** is not. Any RQ1 verdict from option (c) is a verdict
   on a new experiment, not a continuation of t0027.

3. Note that batch and cached-input discounts (50% and ~90% respectively, per [OpenAI-Pricing-2026]
   and [Google-Gemini-Pricing-2026]) could halve the option (c) cost but would also further erode
   comparability with t0027 (which ran online). Defer to creative thinking.

4. Drop self-hosted open-weight pricing from this scan — that is option (b), not option (c), and it
   has no published per-token list price to cite here.

## Source Index

### [OpenAI-Pricing-2026]

* **Type**: documentation
* **Title**: OpenAI API Pricing
* **Author/Org**: OpenAI
* **Date**: 2026
* **URL**: https://openai.com/api/pricing/
* **Peer-reviewed**: no
* **Relevance**: Provides the GPT-5 ($1.25/$10.00 per MTok) and GPT-4o ($2.50/$10.00 per MTok) list
  prices used to anchor the option (c) cost point estimate.

### [Google-Gemini-Pricing-2026]

* **Type**: documentation
* **Title**: Gemini Developer API Pricing
* **Author/Org**: Google AI for Developers
* **Date**: 2026
* **URL**: https://ai.google.dev/gemini-api/docs/pricing
* **Peer-reviewed**: no
* **Relevance**: Provides the Gemini 2.5 Pro list price ($1.25/$10.00 per MTok at ≤200K context,
  with batch and cached-input discounts) used as the second non-Anthropic anchor for option (c).

### [Anthropic-Pricing-2026]

* **Type**: documentation
* **Title**: Anthropic API Pricing — Claude Sonnet 4.6
* **Author/Org**: Anthropic
* **Date**: 2026
* **URL**: https://www.anthropic.com/pricing
* **Peer-reviewed**: no
* **Relevance**: Reference list price ($3.00/$15.00 per MTok) used only to cross-check the realized
  t0027 per-instance cost shape against published rates. Anthropic credentials themselves are
  unavailable to this project per the standing constraint.

### [t0026-Costs]

* **Type**: documentation
* **Title**: t0026_phase2_abc_paired_real_runs_full / results / costs.json
* **Author/Org**: Project (this repository)
* **Date**: 2026-04
* **URL**: tasks/t0026_phase2_abc_paired_real_runs_full/results/costs.json
* **Peer-reviewed**: no
* **Relevance**: Source of the realized arm A per-instance cost (~$0.0344) on Claude Sonnet 4.6 used
  to anchor the option (c) per-pair extrapolation.

### [t0027-Costs]

* **Type**: documentation
* **Title**: t0027_phase2_5_abc_rerun_with_fixed_b_and_c / results / costs.json
* **Author/Org**: Project (this repository)
* **Date**: 2026-04
* **URL**: tasks/t0027_phase2_5_abc_rerun_with_fixed_b_and_c/results/costs.json
* **Peer-reviewed**: no
* **Relevance**: Source of the realized arm B and arm C per-instance costs (~$0.0727 and ~$0.0718)
  used to compute the ~$0.107 paired-instance anchor.

### [t0029-Cap]

* **Type**: documentation
* **Title**: t0029 admission cap (locked when Anthropic API was lost)
* **Author/Org**: Project (this repository)
* **Date**: 2026-04
* **URL**: tasks/t0029_phase2_6_abc_more_pairs/task.json
* **Peer-reviewed**: no
* **Relevance**: Defines the ~218 paired-instance upper bound used in the option (c) total-cost
  band. Without this cap, option (c) cost has no defensible ceiling.
