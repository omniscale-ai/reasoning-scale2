"""Import-only smoke tests: catch ImportError, instantiate dataclasses with stub values, no IO."""

from __future__ import annotations

import pytest

from tasks.t0026_phase2_abc_runtime_n147_for_rq1_rq5.code import (
    anthropic_shim,
    calibration,
    instance_loader,
    judge,
    main,
    mcnemar,
    metrics,
    paths,
    runner,
)


def test_modules_import_cleanly() -> None:
    assert paths.SEED == 20260502
    assert paths.N_TOTAL_TARGET == 147
    assert paths.MODEL_UNDER_TEST == "claude-sonnet-4-6"
    assert paths.JUDGE_MODEL_PRIMARY == "claude-sonnet-4-6"
    assert paths.JUDGE_MODEL_INTER == "claude-opus-4-7"
    assert paths.FORBIDDEN_HAIKU_MODEL_ID == "claude-haiku-4-5"


def test_cost_tracker_records_and_snapshots() -> None:
    tracker = anthropic_shim.CostTracker()
    tracker.record(model_id="claude-sonnet-4-6", prompt_tokens=1000, completion_tokens=500)
    snap = tracker.snapshot()
    assert snap["n_calls"] == 1
    assert snap["prompt_tokens"] == 1000
    assert snap["completion_tokens"] == 500
    expected = 1000 * 3.0 / 1_000_000.0 + 500 * 15.0 / 1_000_000.0
    assert abs(snap["cost_usd"] - expected) < 1e-12
    tracker.note_parse_failure()
    assert tracker.snapshot()["parse_failures"] == 1


def test_make_model_call_rejects_haiku() -> None:
    tracker = anthropic_shim.CostTracker()
    with pytest.raises(AssertionError):
        anthropic_shim.make_model_call(
            model_id=paths.FORBIDDEN_HAIKU_MODEL_ID,
            cost_tracker=tracker,
            max_tokens=64,
        )


def test_judge_outcome_rejects_haiku() -> None:
    instance = instance_loader.Instance(
        instance_id="stub-1",
        subset=paths.SUBSET_FRONTSCI,
        problem_text="What is 2+2?",
        gold={"solution": "Ground truth answer: 4"},
    )
    pred = judge.Prediction(
        instance_id="stub-1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_A,
        final_answer="The answer is 4.",
        final_confidence=0.9,
        cost_usd=0.0,
        trajectory_path=None,
    )
    tracker = anthropic_shim.CostTracker()
    with pytest.raises(AssertionError):
        judge.judge_outcome(
            instance=instance,
            prediction=pred,
            cost_tracker=tracker,
            model_id=paths.FORBIDDEN_HAIKU_MODEL_ID,
        )


def test_compute_program_truth_frontsci_substring_match() -> None:
    instance = instance_loader.Instance(
        instance_id="fs-1",
        subset=paths.SUBSET_FRONTSCI,
        problem_text="What is 2+2?",
        gold={"solution": "Ground truth answer: 4"},
    )
    pred_pass = judge.Prediction(
        instance_id="fs-1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_A,
        final_answer="After computation, the answer is 4.",
        final_confidence=None,
        cost_usd=0.0,
        trajectory_path=None,
    )
    pred_fail = judge.Prediction(
        instance_id="fs-1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_A,
        final_answer="I think the result is seven.",
        final_confidence=None,
        cost_usd=0.0,
        trajectory_path=None,
    )
    assert judge.compute_program_truth(instance=instance, prediction=pred_pass) is True
    assert judge.compute_program_truth(instance=instance, prediction=pred_fail) is False


def test_compute_program_truth_swebench_returns_none() -> None:
    instance = instance_loader.Instance(
        instance_id="swe-1",
        subset=paths.SUBSET_SWEBENCH,
        problem_text="Fix the bug.",
        gold={"repo": "x/y", "FAIL_TO_PASS": "[]"},
    )
    pred = judge.Prediction(
        instance_id="swe-1",
        subset=paths.SUBSET_SWEBENCH,
        variant=paths.VARIANT_A,
        final_answer="Patch applied.",
        final_confidence=None,
        cost_usd=0.0,
        trajectory_path=None,
    )
    assert judge.compute_program_truth(instance=instance, prediction=pred) is None


def test_calibration_ece_basic() -> None:
    confs = [0.1, 0.3, 0.5, 0.7, 0.9]
    outs = [False, False, True, True, True]
    result = calibration.compute_ece_10bin(confidences=confs, outcomes=outs)
    assert result.n_total == 5
    assert 0.0 <= result.ece <= 1.0
    assert len(result.bins) == 10


def test_mcnemar_exact_small_sample() -> None:
    result = mcnemar.mcnemar_paired(b=3, c=1)
    assert result.method == "exact_binomial"
    assert 0.0 < result.p_value <= 1.0
    pairwise = mcnemar.pairwise_mcnemar(
        success_first=[True, True, True, False, False],
        success_second=[False, True, True, True, True],
    )
    assert "p_value" in pairwise
    assert "discordant_b" in pairwise
    assert "discordant_c" in pairwise


def test_mcnemar_chi_squared_large_sample() -> None:
    result = mcnemar.mcnemar_paired(b=20, c=10)
    assert result.method == "chi_squared_continuity"
    assert 0.0 < result.p_value <= 1.0


def test_mcnemar_trivial_zero_discordant() -> None:
    result = mcnemar.mcnemar_paired(b=0, c=0)
    assert result.method == "trivial"
    assert result.p_value == 1.0


def test_metrics_compute_with_minimal_inputs() -> None:
    instance_a = instance_loader.Instance(
        instance_id="i1",
        subset=paths.SUBSET_FRONTSCI,
        problem_text="p",
        gold=None,
    )
    instance_b = instance_loader.Instance(
        instance_id="i2",
        subset=paths.SUBSET_TAUBENCH,
        problem_text="p",
        gold=None,
    )
    pred_a_v_a = judge.Prediction(
        instance_id="i1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_A,
        final_answer="x",
        final_confidence=None,
        cost_usd=0.001,
        trajectory_path=None,
    )
    pred_a_v_b = judge.Prediction(
        instance_id="i1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_B,
        final_answer="x",
        final_confidence=0.6,
        cost_usd=0.002,
        trajectory_path=None,
    )
    pred_a_v_c = judge.Prediction(
        instance_id="i1",
        subset=paths.SUBSET_FRONTSCI,
        variant=paths.VARIANT_C,
        final_answer="x",
        final_confidence=None,
        cost_usd=0.003,
        trajectory_path=None,
    )
    jr_pass = judge.JudgeResult(success=True, rationale="ok", raw_response="VERDICT: PASS")
    jr_fail = judge.JudgeResult(success=False, rationale="bad", raw_response="VERDICT: FAIL")
    judge_results: dict[str, dict[str, metrics.JudgePerInstance]] = {
        paths.VARIANT_A: {"i1": metrics.JudgePerInstance(sonnet=jr_pass, opus=None)},
        paths.VARIANT_B: {"i1": metrics.JudgePerInstance(sonnet=jr_pass, opus=jr_pass)},
        paths.VARIANT_C: {"i1": metrics.JudgePerInstance(sonnet=jr_fail, opus=None)},
    }
    out = metrics.compute_all_metrics(
        predictions_by_variant={
            paths.VARIANT_A: [pred_a_v_a],
            paths.VARIANT_B: [pred_a_v_b],
            paths.VARIANT_C: [pred_a_v_c],
        },
        judge_results=judge_results,
        manifest=[instance_a, instance_b],
    )
    assert out["success_rate_a"] == 1.0
    assert out["success_rate_b"] == 1.0
    assert out["success_rate_c"] == 0.0
    assert "rq5_strict_inequality_supported" in out
    assert out["bonferroni_alpha"] == 0.025
    assert out["efficiency_inference_cost_per_item_usd"] is not None


def test_main_arg_parser_accepts_flags() -> None:
    parser = main._make_arg_parser()
    args = parser.parse_args(["--smoke"])
    assert args.smoke is True
    args = parser.parse_args(["--build-manifest"])
    assert args.build_manifest is True
    args = parser.parse_args(["--preflight"])
    assert args.preflight is True
    args = parser.parse_args(["--full"])
    assert args.full is True


def test_runner_module_imports() -> None:
    assert hasattr(runner, "run_variant")
    assert hasattr(runner, "VariantRunSummary")
