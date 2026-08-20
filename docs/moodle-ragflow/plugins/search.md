# Search block

**Component:** `block_ragflowsearch` · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

A **knowledge-base search** block: users type a query and get back the most relevant source documents
(retrieval only, ranked by relevance), with links to the underlying files.

## Features

- Full-text/semantic search over a RAGflow dataset via the shared provider.
- Ranked results with a relevance score and source links (optionally via the signed Moodle proxy).
- Lightweight — no chat, just retrieval.

## Setup

1. [Set up RAGflow](../setup-ragflow.md) (provider) first.
2. Turn editing on → **Add a block** → *RAGflow Search*.
3. Configure which knowledge base/dataset the block searches.

## Capabilities

| Capability | Default | Purpose |
|---|---|---|
| `block/ragflowsearch:use` | Student, Teacher, Manager | Run searches |
| `block/ragflowsearch:addinstance` | Teacher, Manager | Add the block to a course |
