# Usage dashboard

!!! info "Repository &amp; issue tracker"
    - **Repository:** [https://github.com/ragcon-ai/moodle-local_ragflowdashboard](https://github.com/ragcon-ai/moodle-local_ragflowdashboard){ target="_blank" rel="noopener" }
    - **Issues / bug tracker:** [https://github.com/ragcon-ai/moodle-local_ragflowdashboard/issues](https://github.com/ragcon-ai/moodle-local_ragflowdashboard/issues){ target="_blank" rel="noopener" }

**Component:** `local_ragflowdashboard` · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

An admin-only, **tabbed** report that visualises **how the suite is used**: status/health, request
volume, **token consumption**, raw API calls and error breakdowns — plus an optional per-feature **debug
capture** for diagnosis. It captures the provider's usage through an independent sink, so it is entirely
optional and harmless if not installed. It also ships `rfdsource_*` sub-plugins that give each feature its
own status checks and analytics.

## Features

The report opens at *Site administration → Reports → RAGflow Dashboard* and is organised into **tabs**. A
**view** selector (All features + one per installed source) and a **period** selector (today / 2 / 3 / 7 /
14 / 30 / 90 days, default **today**) filter the analytics tabs; controls reload over AJAX. Charts use
Moodle's built-in Chart API with a consistent palette (green = success, red = errors, blue for neutral
counts) and a colour-coded data table (a swatch per row) under each categorical chart.

- **Status** — is the provider configured and reachable, and is each configured instance (Tutor / Helpdesk
  / Search) correctly linked (assistant valid + bound, knowledge base parsed)? Each check is a collapsible
  row that shows the concrete **API call** used as proof and links to the relevant Moodle config page; a
  per-area refresh re-runs just that check.
- **Usage** — KPI cards (Requests, Success rate, Failures, Average latency), requests per day (successful
  vs failed), requests by feature, **Top 10 users**, requests **by user group** (trainers vs.
  students/users) and **by course**. Sections are collapsible — one open at a time, remembered across
  view/period changes.
- **Tokens** — chat **token consumption** (prompt / completion / total) as KPIs, per day, **by plugin** and
  **by provider instance**. See *What is counted* below.
- **API calls** — the raw RAGflow API-call log (one collapsible row per call) with a per-page selector
  (10 / 20 / 50), **paging**, a **live** auto-reload and **filters** (HTTP status, free text, date range).
  Off unless the raw-API-log toggle is on; the **API key is never logged**.
- **Errors** — **failures by error type** (labelled, e.g. *RAGflow server error (5xx)*, *Query too long for
  embedding model*, *Rate limited*) and a collapsible **recent-errors** list.
- **Export** — download the usage log (metrics only) for a date range, scoped to the current view.

Other: a **usage log — metrics only** (no message content, safe for the standard log store); an optional
**per-feature debug capture** (bounded request/response, admin-only, only while enabled); a daily
**retention/purge** task; and an **anonymisation** option (rows without a user link, aggregate stats still
work).

## What is counted (tokens)

!!! note "Token accounting — scope and no guarantee"
    Tokens are counted **for chat only** (search consumes none) and only for chats that use RAGflow's
    **OpenAI-compatible** endpoint. Chats with **session memory** use RAGflow's native endpoint, which
    **returns no token data**, so those turns are **not** counted. Counting **starts at installation**
    (there is no history), and the figures reflect what RAGflow reports — **provided without guarantee of
    completeness or accuracy**.

## Configuration

### Admin settings — *Site administration → Plugins → Local plugins → RAGflow Dashboard settings*

| Setting | Type | Default | Meaning |
|---|---|---|---|
| **Log retention (days)** (`retentiondays`) | integer | `90` | Delete log entries older than this many days. `0` = keep indefinitely. |
| **Anonymise log data** (`anonymize`) | checkbox | off | Store no user link (user id 0). Aggregate stats still work; per-user analysis / privacy export do not. |
| **Debug content limit (characters)** (`detailmaxlen`) | integer | `2000` | Max characters stored per captured question and response. |
| **Per-feature debug mode** (heading) | — | — | When enabled for a feature, the (bounded) request/response content is stored for troubleshooting — this captures user messages and answers, so enable only temporarily and mind data protection. |
| **Debug: {feature}** (`debug_<component>`) | checkbox | off | One toggle **per feature** owned by an installed source (Tutor / Helpdesk / Search, and any future `rfdsource_*`). When on, that feature's request/response content is captured. |

## Capabilities

| Capability | Default roles | Purpose |
|---|---|---|
| `local/ragflowdashboard:view` | Manager (admin report) | View the dashboard, logs, debug captures and export. Intentionally **not** granted to teaching roles, since the data reveals usage patterns. |

## Data model

- **`local_ragflowdashboard_log`** — one row per request, **metrics only**: time, component, action, user
  id, course id, context id, success, error type, latency (ms), item count, the **provider instance id**
  and the chat **token counts** (prompt / completion / total). Never stores message content.
- **`local_ragflowdashboard_debug`** — request/response **content** (question + response), written
  **only** while a feature's debug toggle is on, truncated to the debug content limit. Written directly, so
  content never reaches the standard log store.
- **`local_ragflowdashboard_apilog`** — the raw RAGflow API-call log (URL, JSON request, raw response,
  status, duration), written **only** while the raw-API-log toggle is on. The **API key is never stored**.

## Sub-plugins (`rfdsource_*`)

Each RAGflow feature contributes a dashboard section as a sub-plugin, shipped **inside** the dashboard
package: **RAGflow Tutor** (`rfdsource_tutor`), **RAGflow Helpdesk** (`rfdsource_helpdesk`), **RAGflow
Search** (`rfdsource_search`). Installing another `rfdsource_*` adds its section and debug toggle
automatically.

## Privacy

The dashboard stores usage metrics and (only while debug is enabled) bounded request/response content,
with full privacy export/deletion support. With **anonymise** on, rows carry no user link. Retention
purges old rows automatically.
