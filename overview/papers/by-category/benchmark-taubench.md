# Papers: `benchmark-taubench` (1)

1 papers across 1 year(s).

[Back to all papers](../README.md)

---

## 2024 (1)

<details>
<summary>📝 tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World
Domains — Yao et al., 2024</summary>

| Field | Value |
|---|---|
| **ID** | `10.48550_arXiv.2406.12045` |
| **Authors** | Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan |
| **Venue** | arXiv preprint (preprint) |
| **DOI** | `10.48550/arXiv.2406.12045` |
| **URL** | https://arxiv.org/abs/2406.12045 |
| **Date added** | 2026-04-29 |
| **Categories** | [`benchmark-taubench`](../../../meta/categories/benchmark-taubench/), [`agent-evaluation`](../../../meta/categories/agent-evaluation/) |
| **Added by** | [`t0002_literature_survey_granularity_conditioning`](../../../overview/tasks/task_pages/t0002_literature_survey_granularity_conditioning.md) |
| **Full summary** | [`summary.md`](../../../tasks/t0002_literature_survey_granularity_conditioning/assets/paper/10.48550_arXiv.2406.12045/summary.md) |

tau-bench introduces a tool-agent-user interaction benchmark in two simulated customer-service
domains (retail and airline). The motivation is that prior tool-use benchmarks fail to test
two critical capabilities for production agents: dynamic interaction with a human user
(simulated here by another LLM) and adherence to domain-specific policy documents that
constrain allowable actions.

Methodologically, each task pairs a user-goal database state, an LLM-roleplayed user persona,
and a policy document. The agent conducts a multi-turn conversation, calls tools as needed,
and attempts to reach the goal state without policy violations. Evaluation compares the final
database state with the annotated goal. The novel pass^k metric runs `k` independent rollouts
and measures the fraction of tasks where every rollout succeeds — exposing inconsistency that
pass@1 hides.

The headline finding is that even state-of-the-art models (GPT-4o) achieve **under 50%
pass@1** and **pass^8 below 25% in retail**, indicating that current frontier agents are both
moderately-capable and substantially unreliable. The gap between pass@1 and pass^8 is the core
diagnostic.

For the granularity-aware hierarchical agents project, tau-bench is the canonical
request-vs-act benchmark — most of its failures stem from agents that proceed without
sufficient information rather than asking the simulated user. This makes tau-bench the primary
test bed for Metric 3. The project should also adopt the pass^k metric as a project-wide
reliability signal, especially in the Phase 4 paper-ready report where overall claims about
scope-conditioning gains must be robust to single-rollout luck.

</details>
