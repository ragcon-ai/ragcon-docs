# Moodle RAGflow Suite

The Moodle RAGflow Suite connects Moodle to a [RAGflow](https://ragflow.io) instance so teachers and
learners can ask questions and get answers grounded in your own documents (retrieval-augmented
generation). It is built on Moodle's **AI subsystem**: a single AI provider talks to RAGflow, and
several placements/blocks consume it.

## What's in the suite

| Plugin | Type | What it does |
|---|---|---|
| **[AI provider (RAGflow)](plugins/provider.md)** | `aiprovider_ragflow` | The backend. Configured as an AI-provider instance; handles chat, search, sources and (optional) conversation memory against RAGflow. **Required by all the others.** |
| **[Tutor block](plugins/tutor.md)** | `block_ragflowtutor` | A per-course tutor chat with its own knowledge base (upload course documents, ask questions). |
| **[Search block](plugins/search.md)** | `block_ragflowsearch` | A knowledge-base search box that returns ranked source documents. |
| **[Helpdesk placement](plugins/helpdesk.md)** | `aiplacement_ragflowhelpdesk` | A site-wide help drawer (bottom-right) answering from a central knowledge base. |
| **[Usage dashboard](plugins/dashboard.md)** | `local_ragflowdashboard` | Admin KPIs, charts and logs of usage and failures (metrics only; optional debug capture). |

## Requirements

- **Moodle 5.0, 5.1 or 5.2** (PHP 8.1–8.3; PostgreSQL or MariaDB/MySQL) — see
  [Moodle version specifics](moodle-version-notes.md).
- A reachable **RAGflow instance** and an **API key** (self-hosted or hosted). The suite is a client
  for RAGflow — it does not bundle or run RAGflow itself.
- Ability to install plugins (site administrator).

## Install order (important)

The provider is a dependency of every other plugin, so install it **first**:

1. `aiprovider_ragflow` (the provider)
2. `aiplacement_ragflowhelpdesk`, `block_ragflowtutor`, `block_ragflowsearch` (in any order)
3. `local_ragflowdashboard` (optional; consumes the provider's usage events)

## Next steps

1. **[Set up RAGflow](setup-ragflow.md)** — connect Moodle to your RAGflow instance and create an
   assistant + knowledge base.
2. Enable the plugins you want (tutor, search, helpdesk, dashboard).
3. See the user guides for day-to-day use — for
   **[administrators](guides/admin.md)**, **[trainers](guides/trainer.md)** and
   **[students](guides/student.md)**.
