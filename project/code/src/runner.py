from __future__ import annotations

from pathlib import Path

import yaml
from dotenv import load_dotenv
from tqdm import tqdm

from src.benchmarks.frontierscience import FrontierScienceLoader
from src.models.anthropic_client import AnthropicClient
from src.models.claude_cli_client import ClaudeCLIClient
from src.models.mock_client import MockClient
from src.pipeline.grader import Grader
from src.pipeline.planner import Planner
from src.pipeline.prober import Prober
from src.pipeline.revisor import Revisor
from src.pipeline.simulator import Simulator
from src.storage.repository import Repository
from src.storage.schema import ExperimentRun, SimulationMode


def load_config(config_path: str | Path) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def make_client(
    model_cfg: dict, use_mock: bool = False, use_cli: bool = False
) -> AnthropicClient | ClaudeCLIClient | MockClient:
    if use_mock:
        return MockClient(model_id=model_cfg["id"])
    if use_cli:
        return ClaudeCLIClient(model_id=model_cfg["id"])
    return AnthropicClient(model_id=model_cfg["id"])


class Runner:
    def __init__(self, config_path: str | Path):
        load_dotenv()
        self._cfg = load_config(config_path)
        self._exp_name = self._cfg["experiment"]["name"]
        self._seed = self._cfg["experiment"]["seed"]
        self._use_mock = self._cfg["experiment"].get("use_mock", False)
        self._use_cli = self._cfg["experiment"].get("use_cli", False)

        results_dir = Path("data/results") / self._exp_name
        self._repo = Repository(results_dir)

        # Clients
        sim_cfg = self._cfg["models"]["simulator"]
        judge_cfg = self._cfg["models"]["judge"]
        self._sim_client = make_client(sim_cfg, use_mock=self._use_mock, use_cli=self._use_cli)
        self._judge_client = make_client(judge_cfg, use_mock=self._use_mock, use_cli=self._use_cli)

        self._simulator = Simulator(self._sim_client)
        self._grader = Grader(self._judge_client)

        # Budget tracking
        self._total_cost_estimate = 0.0
        self._budget = self._cfg["costs"]["budget_usd"]
        self._warn_at = self._cfg["costs"]["warn_at_usd"]

    def run(self) -> None:
        # Load tasks
        loader = FrontierScienceLoader(cache_dir="data/cache")
        bench_cfg = self._cfg["benchmark"]
        tasks = loader.load(
            subjects=bench_cfg["subjects"],
            sample_per_subject=bench_cfg["sample_per_subject"],
            seed=self._seed,
        )
        print(f"Loaded {len(tasks)} tasks from {bench_cfg['source']} ({bench_cfg['track']} track)")

        modes = [SimulationMode(m) for m in self._cfg["pipeline"]["simulation_modes"]]
        probe_steps = self._cfg["pipeline"]["probe_at_steps"]
        context_modes = self._cfg["pipeline"].get("context_modes", ["full", "stripped"])
        test_models = self._cfg["models"]["test_subjects"]
        pipeline_cfg = self._cfg["pipeline"]

        total = len(tasks) * len(test_models) * len(modes) * len(probe_steps) * len(context_modes)
        pbar = tqdm(total=total, desc="Probes")

        for model_cfg in test_models:
            model_id = model_cfg["id"]
            client = make_client(model_cfg, use_mock=self._use_mock, use_cli=self._use_cli)
            planner = Planner(
                client,
                min_steps=pipeline_cfg["min_plan_steps"],
                max_steps=pipeline_cfg["max_plan_steps"],
            )
            prober = Prober(client)
            revisor = Revisor(client)

            # Build same-subject task index for "swapped" context_mode
            same_subject: dict[str, list] = {}
            for t in tasks:
                same_subject.setdefault(t.subject, []).append(t)

            for task in tasks:
                # Skip plan generation if all probes for this task are already done
                all_done = all(
                    self._repo.is_done(task.task_id, model_id, mode.value, step, ctx)
                    for mode in modes
                    for step in probe_steps
                    for ctx in context_modes
                )
                if all_done:
                    pbar.update(len(modes) * len(probe_steps) * len(context_modes))
                    continue

                # Generate plan once per task/model
                try:
                    plan = planner.generate(task, model_id)
                except Exception as e:
                    print(f"  [SKIP] Plan generation failed: task={task.task_id[:8]} err={e}")
                    pbar.update(len(modes) * len(probe_steps) * len(context_modes))
                    continue
                if not plan.parse_success or plan.num_steps < pipeline_cfg["min_plan_steps"]:
                    print(f"  [SKIP] Degenerate plan: task={task.task_id[:8]} model={model_id}")
                    pbar.update(len(modes) * len(probe_steps) * len(context_modes))
                    continue

                # Pick a swap partner (different task, same subject)
                swap_candidates = [
                    t for t in same_subject.get(task.subject, []) if t.task_id != task.task_id
                ]
                swap_task = swap_candidates[0] if swap_candidates else None

                for mode in modes:
                    sim_cache: dict[int, list] = {}

                    for probe_step in probe_steps:
                        if probe_step > plan.num_steps:
                            pbar.update(len(context_modes))
                            continue

                        if probe_step not in sim_cache:
                            steps_to_sim = [s for s in plan.steps if s.number < probe_step]
                            try:
                                sim_cache[probe_step] = self._simulator.simulate_steps(
                                    task, steps_to_sim, mode
                                )
                            except Exception as e:
                                print(
                                    f"  [SKIP] Simulation failed: task={task.task_id[:8]} step={probe_step} err={e}"
                                )
                                pbar.update(len(context_modes))
                                continue

                        sim_results = sim_cache[probe_step]

                        for ctx_mode in context_modes:
                            if self._repo.is_done(
                                task.task_id, model_id, mode.value, probe_step, ctx_mode
                            ):
                                pbar.update(1)
                                continue

                            try:
                                probe = prober.probe(
                                    task,
                                    plan,
                                    sim_results,
                                    probe_step,
                                    model_id,
                                    context_mode=ctx_mode,
                                    swap_task=swap_task if ctx_mode == "swapped" else None,
                                )
                            except Exception as e:
                                print(
                                    f"  [SKIP] Probe failed: task={task.task_id[:8]} step={probe_step} ctx={ctx_mode} err={e}"
                                )
                                pbar.update(1)
                                continue

                            self._repo.save_probe(probe)

                            if probe.gap_detected:
                                try:
                                    revision = revisor.revise(task, plan, probe, model_id)
                                    if revision:
                                        self._repo.save_revision(revision)
                                except Exception as e:
                                    print(
                                        f"  [SKIP] Revision failed: task={task.task_id[:8]} err={e}"
                                    )

                            run = ExperimentRun(
                                experiment_name=self._exp_name,
                                task=task,
                                plan=plan,
                                probes=[probe],
                                revisions=[],
                            )
                            self._repo.save_run(run)
                            pbar.update(1)

                        pbar.update(1)

        pbar.close()
        print(f"\nDone. Results saved to {self._repo._dir}")
