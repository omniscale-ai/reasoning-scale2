---
task_id: "t0029_rq1_discordance_rich_resample"
intervention_kind: "missing_credential"
created_at: "2026-05-03T10:35:00Z"
blocking_step: 9
blocking_step_name: "implementation"
status: "open"
---
# Missing ANTHROPIC_API_KEY blocks t0029 paid execution

## What is blocked

Step 9 (`implementation`) of t0029 cannot run. The harness is required to issue paired API calls to
`claude-sonnet-4-6` for arm A (Plan-and-Solve baseline) and arm B (scope-aware ReAct), and the
Anthropic Python SDK requires `ANTHROPIC_API_KEY` to be set in the process environment.

## Diagnosis

* Shell environment in the worktree does not export `ANTHROPIC_API_KEY`.
* Worktree has no `.env` file. The `.envrc` only chains `dotenv_if_exists`, so direnv has nothing to
  load.
* The user reports they do not have an Anthropic API key available for this project at this time.

## Why we cannot just switch model or provider

Brainstorm session 8 locked the design on `claude-sonnet-4-6` so that t0029's predictions remain
directly paired with t0027's existing 130 paired instances on the same model. Switching providers
(e.g., OpenAI) would break that pairing, invalidate the McNemar test as designed, and make the
already-spent t0027 budget unrecoverable for RQ1.

## What is preserved

* `plan/plan.md` is locked and unchanged. All pre-registered constants survive verbatim
  (`CUMULATIVE_TASK_CAP_USD = 35.00`, `BATCH_SIZE = 8`, `DISCORDANCE_TARGET = 30`,
  `T0029_SEED = 20260503`, sampling order `frontsci → taubench → SWE-bench`, McNemar exact-binomial
  with Bonferroni α = 0.025).
* `research/research_code.md` and the variant-labeling resolution (use t0028 task-description
  naming; isolate t0027 inversion in `load_t0027_paired.py`) are preserved.
* Step 9 status reverted from `in_progress` to `pending` so a future prestep can resume cleanly
  without log pollution.

## Resume conditions

The intervention is resolved when **all** of the following are true:

1. A valid `ANTHROPIC_API_KEY` is provisioned and reachable from the t0029 worktree environment
   (e.g., placed in `.env` and loaded by direnv, or exported in the shell that launches the
   harness).
2. The pre-registered $35 hard cap is still acceptable to the project owner.
3. No upstream changes have invalidated t0027's predictions (re-run the t0027 paired manifest if the
   t0027 results files have shifted).

To resume: run `prestep` for `implementation`, then proceed exactly per `plan/plan.md` Step by Step.

## Concurrent salvage work

A separate task (t0031, scoped at this intervention's filing time) runs no-new-API preliminary
salvage analyses on existing t0027 outputs. **t0031 is not a substitute for t0029.** It produces
"no-new-API preliminary evidence" only and does not deliver an RQ1 McNemar verdict.
