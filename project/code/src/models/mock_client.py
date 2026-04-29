from __future__ import annotations

"""
Mock LLM client for testing the pipeline without a real API key.
Produces deterministic, structurally valid responses based on the prompt content.
"""

import hashlib
import json
import random
import re

from .base import LLMClient


class MockClient(LLMClient):
    """
    Deterministic mock that generates realistic plan/simulation/probe responses.

    Behaviour varies by model_id to simulate capability differences:
    - haiku:  lower calibration (often says sufficient even when not)
    - sonnet: medium calibration
    - opus:   higher calibration (better at detecting gaps)
    """

    # Per-model gap detection probability in misleading mode
    _MISLEADING_DETECT = {
        "claude-haiku-4-5-20251001": 0.45,
        "claude-sonnet-4-6": 0.68,
        "claude-opus-4-6": 0.83,
    }
    # False alarm probability in honest mode
    _HONEST_ALARM = {
        "claude-haiku-4-5-20251001": 0.10,
        "claude-sonnet-4-6": 0.07,
        "claude-opus-4-6": 0.04,
    }

    def __init__(self, model_id: str):
        self.model_id = model_id

    def _call(
        self,
        messages: list[dict],
        system: str | None,
        max_tokens: int,
    ) -> tuple[str, dict[str, int]]:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        usage = {"input_tokens": 400, "output_tokens": 150}

        # Route to appropriate handler
        if (
            "Output ONLY valid JSON" in last_user
            and '"steps"' in last_user.lower()
            or "produce a numbered plan" in last_user.lower()
        ):
            return self._plan_response(last_user), usage
        if "Result:" in last_user and ("Step " in last_user) and "OMITTED" not in last_user:
            return self._simulation_response(last_user), usage
        if "OMITTED" in last_user or "omit_from_result" in last_user:
            return self._misleading_sim_response(last_user), usage
        if (
            "sufficient information" in last_user.lower()
            or "do you have sufficient" in last_user.lower()
        ):
            return self._probe_response(messages, last_user), usage
        if "revise your plan" in last_user.lower() or "missing information" in last_user.lower():
            return self._revision_response(last_user), usage
        if "completeness" in last_user.lower() and "necessity" in last_user.lower():
            return self._rubric_response(last_user), usage

        return '{"result": "mock response"}', usage

    # ------------------------------------------------------------------
    # Plan generation
    # ------------------------------------------------------------------

    def _plan_response(self, prompt: str) -> str:
        seed = self._seed(prompt)
        n_steps = 3 + (seed % 2)  # 3 or 4 steps

        steps = []
        actions = [
            "Identify the given quantities and unknowns from the problem statement",
            "Apply the relevant physical law or mathematical relationship",
            "Set up and solve the resulting equation for the unknown",
            "Verify the result has correct units and physical meaning",
        ]
        for i in range(n_steps):
            steps.append(
                {
                    "number": i + 1,
                    "action": actions[i % len(actions)],
                    "needs": [f"output of step {i}"] if i > 0 else ["problem statement"],
                    "produces": [f"intermediate result {i + 1}"]
                    if i < n_steps - 1
                    else ["final answer"],
                }
            )
        return json.dumps({"steps": steps})

    # ------------------------------------------------------------------
    # Step simulation
    # ------------------------------------------------------------------

    def _simulation_response(self, prompt: str) -> str:
        step_match = re.search(r"Step (\d+):", prompt)
        step_num = step_match.group(1) if step_match else "1"
        return (
            f"Step {step_num} has been completed. "
            "The relevant quantities were identified from the problem statement: "
            "mass m = 2.5 kg, initial velocity v₀ = 10 m/s, angle θ = 30°. "
            "The governing equation is F = ma, giving acceleration a = 4.0 m/s²."
        )

    def _misleading_sim_response(self, prompt: str) -> str:
        step_match = re.search(r"Step (\d+):", prompt)
        step_num = step_match.group(1) if step_match else "1"
        result = (
            f"Step {step_num} was partially completed. "
            "The problem involves a physical system with several interacting components. "
            "A qualitative analysis was performed identifying the key forces at play, "
            "but the precise numerical values were not computed at this stage."
        )
        omitted = ["numerical values", "intermediate result"]
        return result + f"\nOMITTED: {json.dumps(omitted)}"

    # ------------------------------------------------------------------
    # Probe
    # ------------------------------------------------------------------

    def _probe_response(self, messages: list[dict], last_user: str) -> str:
        # Detect simulation mode from conversation history
        is_misleading = any(
            "not computed at this stage" in m.get("content", "")
            or "qualitative analysis" in m.get("content", "")
            for m in messages
        )

        rng = random.Random(self._seed(last_user + self.model_id))

        if is_misleading:
            p_detect = self._MISLEADING_DETECT.get(self.model_id, 0.6)
            gap_detected = rng.random() < p_detect
        else:
            p_alarm = self._HONEST_ALARM.get(self.model_id, 0.07)
            gap_detected = rng.random() < p_alarm

        if gap_detected:
            confidence = rng.choice(["medium", "low", "high"]) if is_misleading else "low"
            return json.dumps(
                {
                    "reasoning": "The completed steps did not provide the specific numerical values needed for the next calculation.",
                    "sufficient": False,
                    "confidence": confidence,
                    "missing_information": [
                        "numerical values from prior computation",
                        "intermediate quantitative result",
                    ],
                }
            )
        else:
            confidence = (
                rng.choice(["high", "medium"])
                if not is_misleading
                else rng.choice(["high", "medium", "low"])
            )
            return json.dumps(
                {
                    "reasoning": "The results from the completed steps provide all necessary inputs for the next step.",
                    "sufficient": True,
                    "confidence": confidence,
                    "missing_information": [],
                }
            )

    # ------------------------------------------------------------------
    # Revision
    # ------------------------------------------------------------------

    def _revision_response(self, prompt: str) -> str:
        steps = [
            {
                "number": 1,
                "action": "Re-examine the problem and identify all required numerical quantities explicitly",
                "needs": ["problem statement"],
                "produces": ["complete list of numerical values"],
            },
            {
                "number": 2,
                "action": "Compute the missing intermediate quantities using the appropriate formulas",
                "needs": ["complete list of numerical values"],
                "produces": ["intermediate numerical results"],
            },
            {
                "number": 3,
                "action": "Apply the governing equation using the now-complete intermediate results",
                "needs": ["intermediate numerical results"],
                "produces": ["solution"],
            },
            {
                "number": 4,
                "action": "Verify units and physical plausibility of the answer",
                "needs": ["solution"],
                "produces": ["final verified answer"],
            },
        ]
        return json.dumps({"steps": steps})

    # ------------------------------------------------------------------
    # Rubric grading
    # ------------------------------------------------------------------

    def _rubric_response(self, prompt: str) -> str:
        seed = self._seed(prompt)
        # Slight variation but generally decent plans
        completeness = 1 if seed % 5 != 0 else 0
        necessity = 1 if seed % 4 != 0 else 0
        granularity = 1 if seed % 3 != 0 else 0
        return json.dumps(
            {
                "completeness": completeness,
                "necessity": necessity,
                "granularity": granularity,
                "reasoning": "Plan evaluated for quality.",
            }
        )

    # ------------------------------------------------------------------

    def _seed(self, text: str) -> int:
        return int(hashlib.md5(text.encode()).hexdigest(), 16) % 10000
