# Usage dashboard

**Component:** `local_ragflowdashboard` · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

An admin report showing **how the suite is used**: request volume, latency, success/failure rates and
error breakdowns — plus an optional per-component **debug capture** for diagnosis. It observes the
provider's usage events, so it is entirely optional and harmless if not installed.

## Features

- KPIs, per-day charts and a failures-by-error-type breakdown.
- Usage log — **metrics only, no message content** (safe for the standard log store).
- Optional **debug capture** per component (request/response content, including the technical error
  cause) stored in a dashboard-owned, admin-only table; enable it only while diagnosing.
- Retention task to purge old rows; anonymisation option.
- Ships `rfdsource_*` sub-plugins (helpdesk / search / tutor sources) **inside its own package**.

## Setup

1. Install after the provider (it consumes the provider's events).
2. Open **Site administration → Reports → RAGflow Dashboard**.
3. Configure retention / anonymisation and, if needed, toggle **debug** for a component.

## Capabilities

| Capability | Default | Purpose |
|---|---|---|
| `local/ragflowdashboard:view` | Manager (admin report) | View the dashboard, logs and debug captures |

## Settings

- **Retention (days)** — how long usage rows are kept.
- **Anonymise** — drop user identifiers from stored rows.
- **Debug detail max length** — cap on captured content size.
- **Debug per component** — enable request/response capture for a specific surface while diagnosing.
