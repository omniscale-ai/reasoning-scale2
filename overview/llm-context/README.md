# LLM Context Archives

Generated XML archives for pasting into ChatGPT, Gemini, Claude, and similar tools.

## Preset Archives

Curated presets that mix content from multiple aggregator types for specific use cases.

| Preset | Tokens | Best For |
|---|---:|---|
| [`project-overview`](project-overview.xml) | 11K | General orientation, quick status questions, and lightweight strategy chats. |
| [`full`](full.xml) | 136K | Deep project review, comprehensive planning, and long-context synthesis. |
| [`research-history`](research-history.xml) | 108K | Literature review continuity, methodology discussion, and prior-investigation lookup. |
| [`results-deep-dive`](results-deep-dive.xml) | 119K | Performance analysis, experiment comparison, and result interpretation. |
| [`roadmap`](roadmap.xml) | 28K | Deciding what to do next, prioritizing experiments, and planning follow-up work. |
| [`literature-and-assets`](literature-and-assets.xml) | 19K | Method discussion, resource selection, and related-work chats. |
| [`qa`](qa.xml) | 18K | Answer review, follow-up questioning, and project knowledge-base chats. |
| [`project-memory`](project-memory.xml) | 23K | Keeping a durable project memory in medium-size chat sessions. |

## Per-Type Archives

One file per aggregator type with complete untruncated data.

| Type | Tokens | Description |
|---|---:|---|
| [`tasks`](type-tasks.xml) | 76K | Complete task data with full descriptions, results summaries, dependencies, and status. |
| [`papers`](type-papers.xml) | 61K | Complete paper corpus with full summaries, metadata, and abstracts. |
| [`datasets`](type-datasets.xml) | 15K | Complete dataset inventory with full descriptions, access info, and sizes. |
| [`libraries`](type-libraries.xml) | 30K | Complete library registry with full descriptions, module paths, and entry points. |
| [`answers`](type-answers.xml) | 8K | Complete question and answer corpus with full answer bodies. |
| [`suggestions`](type-suggestions.xml) | 21K | Complete suggestion list with full descriptions, priority, and status. |
| [`predictions`](type-predictions.xml) | 18K | Complete predictions inventory with full descriptions, metrics, and model references. |
| [`metrics`](type-metrics.xml) | 496 | Complete metric definitions with full descriptions, units, and associated datasets. |
| [`categories`](type-categories.xml) | 1K | Complete category definitions with full detailed descriptions. |
| [`task-types`](type-task-types.xml) | 22K | Complete task type definitions with descriptions and instructions. |
| [`costs`](type-costs.xml) | 799 | Complete cost breakdown with budget, per-service, and per-task details. |

## Context Windows

* `131k-class` — up to 131,072 estimated tokens
* `200k-class` — up to 200,000 estimated tokens
* `1M-class` — up to 1,000,000 estimated tokens

Token counts are approximate and use the shared rule `1 token ~= 4 chars`.

## Project Overview

Compact starter context for general project chats.

* Preset id: `project-overview`
* Short label: `overview` (11K)
* Best for: General orientation, quick status questions, and lightweight strategy chats.
* File: [`project-overview.xml`](project-overview.xml)
* Size: 42.0 KiB (43,058 bytes; 42,969 chars)
* Estimated tokens: 10,742
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |

## Full Project Context

Largest preset with detailed completed-task reports and the full project knowledge base.

* Preset id: `full`
* Short label: `full` (136K)
* Best for: Deep project review, comprehensive planning, and long-context synthesis.
* File: [`full.xml`](full.xml)
* Size: 534.8 KiB (547,667 bytes; 545,697 chars)
* Estimated tokens: 136,424
* Fits: 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Detailed results | Every available completed-task `results/results_detailed.md` file in full. |
| Planned tasks | All planned or active tasks with status, date, dependencies, short descriptions, and full long descriptions. |
| Questions and answers | All questions with full-answer bodies when available. |
| Papers | All papers with metadata and summary excerpts from paper summaries, full summaries, or abstracts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |

## Research History

Research-stage documents across completed tasks, plus core project context.

* Preset id: `research-history`
* Short label: `research` (108K)
* Best for: Literature review continuity, methodology discussion, and prior-investigation
  lookup.
* File: [`research-history.xml`](research-history.xml)
* Size: 423.0 KiB (433,106 bytes; 431,985 chars)
* Estimated tokens: 107,996
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Research documents | All available completed-task `research_papers.md`, `research_internet.md`, and `research_code.md` files in full. |

## Results Deep Dive

Completed-task result summaries plus all detailed results reports.

* Preset id: `results-deep-dive`
* Short label: `results` (119K)
* Best for: Performance analysis, experiment comparison, and result interpretation.
* File: [`results-deep-dive.xml`](results-deep-dive.xml)
* Size: 465.6 KiB (476,800 bytes; 474,916 chars)
* Estimated tokens: 118,729
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Detailed results | Every available completed-task `results/results_detailed.md` file in full. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |

## Roadmap

Project planning preset centered on upcoming tasks and open suggestions.

* Preset id: `roadmap`
* Short label: `roadmap` (28K)
* Best for: Deciding what to do next, prioritizing experiments, and planning follow-up work.
* File: [`roadmap.xml`](roadmap.xml)
* Size: 111.0 KiB (113,627 bytes; 113,483 chars)
* Estimated tokens: 28,370
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, short descriptions, and full long descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Suggestions | All open suggestions with priority, kind, source task, and description excerpts. |

## Literature and Assets

Paper summaries and reusable project assets without the heaviest task reports.

* Preset id: `literature-and-assets`
* Short label: `assets` (19K)
* Best for: Method discussion, resource selection, and related-work chats.
* File: [`literature-and-assets.xml`](literature-and-assets.xml)
* Size: 76.2 KiB (78,024 bytes; 77,899 chars)
* Estimated tokens: 19,474
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Papers | All papers with metadata and summary excerpts from paper summaries, full summaries, or abstracts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |

## Questions and Answers

Question-centric preset with the full answer corpus and compact project state.

* Preset id: `qa`
* Short label: `qa` (18K)
* Best for: Answer review, follow-up questioning, and project knowledge-base chats.
* File: [`qa.xml`](qa.xml)
* Size: 68.9 KiB (70,524 bytes; 70,400 chars)
* Estimated tokens: 17,600
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with full-answer bodies when available. |

## Project Memory

Mid-size preset intended as a reusable working memory for ongoing chats.

* Preset id: `project-memory`
* Short label: `memory` (23K)
* Best for: Keeping a durable project memory in medium-size chat sessions.
* File: [`project-memory.xml`](project-memory.xml)
* Size: 89.9 KiB (92,052 bytes; 91,917 chars)
* Estimated tokens: 22,979
* Fits: 131k-class, 200k-class, 1M-class

### Included Types

| Included Type | Coverage |
|---|---|
| Project description | Full `project/description.md`. |
| Completed tasks | All completed tasks with `results_summary` excerpts and short descriptions. |
| Planned tasks | All planned or active tasks with status, date, dependencies, and short descriptions. |
| Questions and answers | All questions with short-answer coverage only. |
| Papers | The 20 most recent papers with metadata and summary excerpts. |
| Datasets | All datasets with access, size, source task, and description excerpts. |
| Libraries | All libraries with module paths, source task, and description excerpts. |
| Metrics | All registered metrics with units, value types, and description excerpts. |
| Suggestions | The top 20 open suggestions ordered by priority and date. |

## Per-Type Archive Details

### All Tasks

Complete task data with full descriptions, results summaries, dependencies, and status.

* Type id: `tasks`
* File: [`type-tasks.xml`](type-tasks.xml)
* Size: 296.2 KiB (303,331 bytes; 302,226 chars)
* Estimated tokens: 75,556
* Fits: 131k-class, 200k-class, 1M-class

### All Papers

Complete paper corpus with full summaries, metadata, and abstracts.

* Type id: `papers`
* File: [`type-papers.xml`](type-papers.xml)
* Size: 240.3 KiB (246,079 bytes; 244,954 chars)
* Estimated tokens: 61,238
* Fits: 131k-class, 200k-class, 1M-class

### All Datasets

Complete dataset inventory with full descriptions, access info, and sizes.

* Type id: `datasets`
* File: [`type-datasets.xml`](type-datasets.xml)
* Size: 58.1 KiB (59,526 bytes; 59,459 chars)
* Estimated tokens: 14,864
* Fits: 131k-class, 200k-class, 1M-class

### All Libraries

Complete library registry with full descriptions, module paths, and entry points.

* Type id: `libraries`
* File: [`type-libraries.xml`](type-libraries.xml)
* Size: 116.0 KiB (118,826 bytes; 118,481 chars)
* Estimated tokens: 29,620
* Fits: 131k-class, 200k-class, 1M-class

### All Answers

Complete question and answer corpus with full answer bodies.

* Type id: `answers`
* File: [`type-answers.xml`](type-answers.xml)
* Size: 31.3 KiB (32,061 bytes; 32,026 chars)
* Estimated tokens: 8,006
* Fits: 131k-class, 200k-class, 1M-class

### All Suggestions

Complete suggestion list with full descriptions, priority, and status.

* Type id: `suggestions`
* File: [`type-suggestions.xml`](type-suggestions.xml)
* Size: 83.0 KiB (85,022 bytes; 84,982 chars)
* Estimated tokens: 21,245
* Fits: 131k-class, 200k-class, 1M-class

### All Predictions

Complete predictions inventory with full descriptions, metrics, and model references.

* Type id: `predictions`
* File: [`type-predictions.xml`](type-predictions.xml)
* Size: 72.0 KiB (73,733 bytes; 73,619 chars)
* Estimated tokens: 18,404
* Fits: 131k-class, 200k-class, 1M-class

### All Metrics

Complete metric definitions with full descriptions, units, and associated datasets.

* Type id: `metrics`
* File: [`type-metrics.xml`](type-metrics.xml)
* Size: 1.9 KiB (1,986 bytes; 1,986 chars)
* Estimated tokens: 496
* Fits: 131k-class, 200k-class, 1M-class

### All Categories

Complete category definitions with full detailed descriptions.

* Type id: `categories`
* File: [`type-categories.xml`](type-categories.xml)
* Size: 4.7 KiB (4,765 bytes; 4,763 chars)
* Estimated tokens: 1,190
* Fits: 131k-class, 200k-class, 1M-class

### All Task Types

Complete task type definitions with descriptions and instructions.

* Type id: `task-types`
* File: [`type-task-types.xml`](type-task-types.xml)
* Size: 87.3 KiB (89,387 bytes; 89,306 chars)
* Estimated tokens: 22,326
* Fits: 131k-class, 200k-class, 1M-class

### Project Costs

Complete cost breakdown with budget, per-service, and per-task details.

* Type id: `costs`
* File: [`type-costs.xml`](type-costs.xml)
* Size: 3.1 KiB (3,197 bytes; 3,197 chars)
* Estimated tokens: 799
* Fits: 131k-class, 200k-class, 1M-class
