# LLM Context Archives

Generated XML archives for pasting into ChatGPT, Gemini, Claude, and similar tools.

## Preset Archives

Curated presets that mix content from multiple aggregator types for specific use cases.

| Preset | Tokens | Best For |
|---|---:|---|
| [`project-overview`](project-overview.xml) | 3K | General orientation, quick status questions, and lightweight strategy chats. |
| [`full`](full.xml) | 22K | Deep project review, comprehensive planning, and long-context synthesis. |
| [`research-history`](research-history.xml) | 25K | Literature review continuity, methodology discussion, and prior-investigation lookup. |
| [`results-deep-dive`](results-deep-dive.xml) | 17K | Performance analysis, experiment comparison, and result interpretation. |
| [`roadmap`](roadmap.xml) | 8K | Deciding what to do next, prioritizing experiments, and planning follow-up work. |
| [`literature-and-assets`](literature-and-assets.xml) | 7K | Method discussion, resource selection, and related-work chats. |
| [`qa`](qa.xml) | 3K | Answer review, follow-up questioning, and project knowledge-base chats. |
| [`project-memory`](project-memory.xml) | 11K | Keeping a durable project memory in medium-size chat sessions. |

## Per-Type Archives

One file per aggregator type with complete untruncated data.

| Type | Tokens | Description |
|---|---:|---|
| [`tasks`](type-tasks.xml) | 12K | Complete task data with full descriptions, results summaries, dependencies, and status. |
| [`papers`](type-papers.xml) | 25K | Complete paper corpus with full summaries, metadata, and abstracts. |
| [`datasets`](type-datasets.xml) | 6K | Complete dataset inventory with full descriptions, access info, and sizes. |
| [`libraries`](type-libraries.xml) | 7K | Complete library registry with full descriptions, module paths, and entry points. |
| [`suggestions`](type-suggestions.xml) | 5K | Complete suggestion list with full descriptions, priority, and status. |
| [`metrics`](type-metrics.xml) | 496 | Complete metric definitions with full descriptions, units, and associated datasets. |
| [`categories`](type-categories.xml) | 1K | Complete category definitions with full detailed descriptions. |
| [`task-types`](type-task-types.xml) | 22K | Complete task type definitions with descriptions and instructions. |
| [`costs`](type-costs.xml) | 308 | Complete cost breakdown with budget, per-service, and per-task details. |

## Context Windows

* `131k-class` — up to 131,072 estimated tokens
* `200k-class` — up to 200,000 estimated tokens
* `1M-class` — up to 1,000,000 estimated tokens

Token counts are approximate and use the shared rule `1 token ~= 4 chars`.

## Project Overview

Compact starter context for general project chats.

* Preset id: `project-overview`
* Short label: `overview` (3K)
* Best for: General orientation, quick status questions, and lightweight strategy chats.
* File: [`project-overview.xml`](project-overview.xml)
* Size: 13.5 KiB (13,835 bytes; 13,799 chars)
* Estimated tokens: 3,449
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
* Short label: `full` (22K)
* Best for: Deep project review, comprehensive planning, and long-context synthesis.
* File: [`full.xml`](full.xml)
* Size: 86.2 KiB (88,222 bytes; 87,978 chars)
* Estimated tokens: 21,994
* Fits: 131k-class, 200k-class, 1M-class

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
* Short label: `research` (25K)
* Best for: Literature review continuity, methodology discussion, and prior-investigation
  lookup.
* File: [`research-history.xml`](research-history.xml)
* Size: 96.1 KiB (98,422 bytes; 98,222 chars)
* Estimated tokens: 24,555
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
* Short label: `results` (17K)
* Best for: Performance analysis, experiment comparison, and result interpretation.
* File: [`results-deep-dive.xml`](results-deep-dive.xml)
* Size: 66.4 KiB (67,972 bytes; 67,755 chars)
* Estimated tokens: 16,938
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
* Short label: `roadmap` (8K)
* Best for: Deciding what to do next, prioritizing experiments, and planning follow-up work.
* File: [`roadmap.xml`](roadmap.xml)
* Size: 32.7 KiB (33,528 bytes; 33,482 chars)
* Estimated tokens: 8,370
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
* Short label: `assets` (7K)
* Best for: Method discussion, resource selection, and related-work chats.
* File: [`literature-and-assets.xml`](literature-and-assets.xml)
* Size: 29.1 KiB (29,812 bytes; 29,759 chars)
* Estimated tokens: 7,439
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
* Short label: `qa` (3K)
* Best for: Answer review, follow-up questioning, and project knowledge-base chats.
* File: [`qa.xml`](qa.xml)
* Size: 13.5 KiB (13,835 bytes; 13,799 chars)
* Estimated tokens: 3,449
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
* Short label: `memory` (11K)
* Best for: Keeping a durable project memory in medium-size chat sessions.
* File: [`project-memory.xml`](project-memory.xml)
* Size: 41.8 KiB (42,843 bytes; 42,790 chars)
* Estimated tokens: 10,697
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
* Size: 45.5 KiB (46,545 bytes; 46,407 chars)
* Estimated tokens: 11,601
* Fits: 131k-class, 200k-class, 1M-class

### All Papers

Complete paper corpus with full summaries, metadata, and abstracts.

* Type id: `papers`
* File: [`type-papers.xml`](type-papers.xml)
* Size: 97.3 KiB (99,685 bytes; 98,982 chars)
* Estimated tokens: 24,745
* Fits: 131k-class, 200k-class, 1M-class

### All Datasets

Complete dataset inventory with full descriptions, access info, and sizes.

* Type id: `datasets`
* File: [`type-datasets.xml`](type-datasets.xml)
* Size: 22.6 KiB (23,168 bytes; 23,155 chars)
* Estimated tokens: 5,788
* Fits: 131k-class, 200k-class, 1M-class

### All Libraries

Complete library registry with full descriptions, module paths, and entry points.

* Type id: `libraries`
* File: [`type-libraries.xml`](type-libraries.xml)
* Size: 28.8 KiB (29,449 bytes; 29,365 chars)
* Estimated tokens: 7,341
* Fits: 131k-class, 200k-class, 1M-class

### All Suggestions

Complete suggestion list with full descriptions, priority, and status.

* Type id: `suggestions`
* File: [`type-suggestions.xml`](type-suggestions.xml)
* Size: 18.4 KiB (18,860 bytes; 18,860 chars)
* Estimated tokens: 4,715
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
* Size: 1.2 KiB (1,234 bytes; 1,234 chars)
* Estimated tokens: 308
* Fits: 131k-class, 200k-class, 1M-class
