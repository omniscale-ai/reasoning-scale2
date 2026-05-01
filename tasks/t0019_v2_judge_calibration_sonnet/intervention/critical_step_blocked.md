# Critical Step Blocked: claude-sonnet-4-6 Unavailable Within Budget

**Task**: t0019_v2_judge_calibration_sonnet **Date**: 2026-05-01 **Plan requirements affected**:
REQ-2 (substantive judge on Sonnet), REQ-3 (model-rotated judge on Sonnet), and by transitivity
REQ-4..REQ-12 (all metrics, asset, answer, charts depend on the two Sonnet runs)

## What Failed

Step 7 of `plan/plan.md` ("Run validation gate (limit=5)") fails with `RateLimitError 429` on every
single call to `claude-sonnet-4-6`. Five validation rows out of five came back as
`call-failure: RateLimitError`, total successful judgments `0`, total cost `$0.00`. The same code
path succeeds against `claude-haiku-4-5` immediately, so the failure is model-specific, not an
environment, network, or code defect.

The five outcome rows already on disk at `_outputs/substantive_outcomes.jsonl` document the failure.

## What Was Tried

1. **Anthropic Python SDK with default key** (`ANTHROPIC_API_KEY` from macOS keychain entry
   `Claude Code`, length 108, prefix `sk-ant-api03-`):
   * `claude-sonnet-4-6` → 429 RateLimitError on every call (request IDs in
     `_outputs/substantive_outcomes.jsonl`).
   * `claude-haiku-4-5` → succeeds immediately, billed normally.
   * `claude-sonnet-4-5` → 429 RateLimitError.
   * `claude-opus-4-5` → 429 RateLimitError.
   * `claude-3-5-sonnet-latest` → 404 NotFoundError (model not provisioned).
2. **SDK with retry/backoff** (5 attempts, 2 → 4 → 8 → 16 → 32 s, jittered): all five retries hit
   429 with no `retry-after` header — confirms the gate is a permission/quota cap, not a per-minute
   rate limiter.
3. **Lower concurrency** (`max_workers=1`, `15 s` sleep gap): 0/3 succeeded — same 429 pattern.
4. **`claude` CLI fallback** (`claude -p - --model claude-sonnet-4-6 --output-format json`): a
   single test call worked but spent **$0.16** (≈ 41 K cache-creation tokens at sonnet input rates).
   Projecting to the full pool of 110 calls (55 rows × 2 prompt variants) → ≈ **$17.60**, which
   exceeds the plan's $4.50 hard cap by 3.9×.
5. **`claude --bare`** (skips keychain reads): refuses to run with
   `Not logged in · Please run /login`, so it cannot bypass the OAuth-issued key.

## Root Cause

The API key surfaced by `security find-generic-password -l "Claude Code" -w` is an OAuth-issued
"Claude Code subscription" credential. It is provisioned with quota only for the model the IDE
client uses for its agent loop (haiku-4-5 in this environment). All Sonnet and Opus tiers return
`rate_limit_error` immediately, regardless of concurrency or pacing.

A standard project-issued `sk-ant-api03-...` key with paid Sonnet quota would resolve this
immediately, but no such key is present in `.env`, the keychain, or any other location I am allowed
to read.

## Why I Did Not Substitute a Different Model

The plan's Risks & Fallbacks table explicitly addresses this exact pre-mortem (rows in
`plan/plan.md` § Risks & Fallbacks):

> Pre-mortem failure: agent silently substitutes a different model after seeing the cost — Plan
> locks `JUDGE_MODEL_ID = "claude-sonnet-4-6"` as a constant and documents it as REQ-2/REQ-3; any
> deviation must produce an intervention file.

The whole experimental design is to test whether Sonnet-as-judge (a stronger judge family) erases
the +57 pp annotator gap that t0014's Haiku-as-judge produced. Re-running with Haiku-as-judge would
reproduce t0014, not test it. The implementation skill rule is also explicit:

> If a critical step becomes impossible (e.g., model checkpoint unavailable), the implementation
> agent must create an intervention file — not silently substitute a different approach.

Therefore I am halting and writing this file rather than swapping the judge model.

## What Human Action Is Needed

Pick one of the following and tell the orchestrator which to use:

1. **Provide a project Anthropic API key with Sonnet quota.** Export it as `ANTHROPIC_API_KEY` (or
   place it in `.env`) before resuming. Estimated total cost stays at the plan's $4.50 budget. This
   is the preferred resolution.
2. **Authorise raising the hard cap to ≈ $20.** This unblocks the `claude` CLI fallback path. If
   chosen, the agent should:
   * Update `BUDGET_CAP_USD` in `tasks/t0019_v2_judge_calibration_sonnet/code/constants.py` to
     `20.00` (and document the change in `results/results_summary.md`).
   * Replace the SDK call in `code/judge_runner.py` with a `subprocess.run(["claude", ...])` wrapper
     that parses `--output-format json`.
   * Re-run validation (`limit=5`) and verify per-call cost stays under $0.20 before launching the
     full pool.
3. **Cancel the task or replace it with a haiku-only variant.** If chosen, the orchestrator should
   mark the task `cancelled` and create a new task (e.g., `t0019b_v2_judge_calibration_haiku`) with
   the judge family explicitly changed; the agent must NOT silently flip Sonnet → Haiku here.

## State Preserved

* `code/` — full pipeline implemented per plan steps 1-6 (data loader, parser, stats helpers, judge
  runner with retry, two entry-point scripts).
* `_outputs/substantive_outcomes.jsonl` — five `call-failure` rows from the validation attempt.
  Preserved as evidence; the runner is idempotent so a successful retry will overwrite them cleanly.
* `data_loader` smoke-tested: loads 55 pool rows (12 v1-sonnet, 23 v2-haiku, 20 v2-sonnet).
* No charts, metrics, predictions asset, or answer asset were produced.

## Suggested Resume Command

After human action, the agent should resume with:

```bash
uv run python -m arf.scripts.utils.run_with_logs --task-id t0019_v2_judge_calibration_sonnet -- \
  uv run python -u -m tasks.t0019_v2_judge_calibration_sonnet.code.run_substantive --limit 5
```

and inspect 5 individual outcomes before lifting `--limit`.
