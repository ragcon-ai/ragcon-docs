# Usage dashboard

!!! info "Repository &amp; issue tracker"
    - **Repository:** [https://github.com/ragcon-ai/moodle-local_ragflowdashboard](https://github.com/ragcon-ai/moodle-local_ragflowdashboard){ target="_blank" rel="noopener" }
    - **Issues / bug tracker:** [https://github.com/ragcon-ai/moodle-local_ragflowdashboard/issues](https://github.com/ragcon-ai/moodle-local_ragflowdashboard/issues){ target="_blank" rel="noopener" }

**Component:** `local_ragflowdashboard` · **Release:** 0.5.3 · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

An admin-only report that visualises **how the suite is used**: request volume, success/failure rates,
latency and error breakdowns — plus an optional per-feature **debug capture** for diagnosis. It
observes the provider's usage events, so it is entirely optional and harmless if not installed. It also
ships `rfdsource_*` sub-plugins that give each feature its own dashboard section.

## Features

- **Dashboard page** at *Site administration → Reports → RAGflow Dashboard*, with a **view** selector
  ("All features" + one per installed source) and a **period** selector (7 / 14 / 30 / 90 days, default
  30). Controls reload the view over AJAX.
- **KPI cards:** Requests, Success rate (%), Failures, Average latency (ms).
- **Charts:** requests per day (successful vs failed), requests by feature (global view), and
  **failures by error type** (labelled, e.g. *RAGflow server error (5xx)*, *Query too long for
  embedding model*, *Rate limited*).
- **Recent-errors table:** most recent failures (50 global / 20 per feature) — time, feature, action,
  error type, latency.
- **Usage log — metrics only:** every usage event is stored **without message content** (safe for the
  standard log store).
- **Per-feature debug capture — content:** when an admin enables debug for a feature, the bounded
  request/response (question + answer/error, including the technical cause) is stored in a
  dashboard-owned, **admin-only** table and shown as a "Debug captures" table. Enable it only while
  diagnosing.
- **XML export** of the usage log (metrics only) for a date range, scoped to the current view.
- **Retention/purge task** (daily) removes log and debug rows older than the retention period.
- **Anonymisation** option stores rows without a user link (aggregate stats still work).

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

- **`local_ragflowdashboard_log`** — one row per usage event, **metrics only**: time, component, action,
  user id, course id, context id, success, error type, latency (ms), item count. Never stores content.
- **`local_ragflowdashboard_debug`** — request/response **content** (question + response), written
  **only** while a feature's debug toggle is on, truncated to the debug content limit. Written directly
  (never via events), so content never reaches the standard log store.

## Sub-plugins (`rfdsource_*`)

Each RAGflow feature contributes a dashboard section as a sub-plugin, shipped **inside** the dashboard
package: **RAGflow Tutor** (`rfdsource_tutor`), **RAGflow Helpdesk** (`rfdsource_helpdesk`), **RAGflow
Search** (`rfdsource_search`). Installing another `rfdsource_*` adds its section and debug toggle
automatically.

## Privacy

The dashboard stores usage metrics and (only while debug is enabled) bounded request/response content,
with full privacy export/deletion support. With **anonymise** on, rows carry no user link. Retention
purges old rows automatically.
