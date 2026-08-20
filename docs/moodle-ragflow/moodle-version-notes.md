# Moodle version specifics

The RAGflow suite runs on **Moodle 5.0, 5.1 and 5.2 from a single codebase** (the `main` line of each
plugin). This page collects the behaviour that differs between those versions and the requirements to
be aware of.

## Supported versions at a glance

| Moodle | Supported | Web-root layout | AI error handling | Notes |
|---|---|---|---|---|
| **5.2** | ✅ | `public/` | `\core_ai\error\factory` | Reference version |
| **5.1** | ✅ | `public/` | `\core_ai\error\factory` | |
| **5.0** | ✅ | repo root (no `public/`) | legacy error array | Requires **PHP ≤ 8.3** (see below) |
| 4.5 and earlier | ❌ **not supported** | — | — | No `ai_providers` instance model (see below) |

All plugins declare `requires = 2025041400` (Moodle 5.0) and are verified green in CI on **5.0 and 5.2
× PostgreSQL and MariaDB**.

## The `public/` web root (Moodle 5.1+)

Moodle **5.1** moved all web-served code under a `public/` directory. This only affects the **install
path** of each plugin — the plugin code itself is identical:

| Plugin | Path on Moodle 5.0 | Path on Moodle 5.1+ |
|---|---|---|
| AI provider | `ai/provider/ragflow` | `public/ai/provider/ragflow` |
| Helpdesk placement | `ai/placement/ragflowhelpdesk` | `public/ai/placement/ragflowhelpdesk` |
| Tutor block | `blocks/ragflowtutor` | `public/blocks/ragflowtutor` |
| Search block | `blocks/ragflowsearch` | `public/blocks/ragflowsearch` |
| Dashboard | `local/ragflowdashboard` | `public/local/ragflowdashboard` |

If you install from a release ZIP through Moodle's plugin installer, Moodle places the files in the
correct location automatically. When installing manually, use the path for your Moodle version.

## AI error handling (version-guarded)

Moodle's AI subsystem changed how a provider returns action errors:

- **Moodle 5.1+** provides `\core_ai\error\factory`, which the provider uses to return structured
  error details (with an error source).
- **Moodle 5.0** has no error factory, so the provider returns the plain legacy error array
  (`success` / `errorcode` / `errormessage`), exactly as core's own providers do on 5.0.

The provider detects this at runtime, so the same code behaves correctly on every supported version.
The user-facing behaviour (and the capability-gated *Details* on a failed chat) is the same.

## PHP and database requirements

- **PHP:** Moodle 5.0 supports PHP **8.1–8.3 and rejects 8.4**. If you self-host with Docker or manage
  the PHP version yourself, **pin PHP 8.3** for a 5.0 site. Moodle 5.1/5.2 follow their own PHP support
  matrix. The suite has no PHP requirement beyond Moodle's own.
- **Database:** PostgreSQL or MariaDB/MySQL (the suite is verified on PostgreSQL and MariaDB). Day
  bucketing in the dashboard uses portable integer arithmetic for cross-database compatibility.

## Why Moodle 4.5 is not supported

The suite is built entirely on the **AI-provider instance model** introduced in Moodle **5.0**:

- Moodle 5.0 added the `ai_providers` table, so a provider is configured as one or more **instances**
  (base URL, API key, per-action config) via the AI subsystem, plus the provider form hook
  `after_ai_provider_form_hook`.
- Moodle **4.5 has no `ai_providers` table** and configures AI providers through admin settings
  (`settings.php` / `get_config`) instead — a fundamentally different configuration model.

Supporting 4.5 would require a parallel configuration layer that permanently diverges from the 5.0+
model, for little benefit (AI features are a 5.0+ concern). It is a deliberate decision not to support
Moodle 4.5 or earlier.

## Upgrading your Moodle across these versions

Because one plugin line serves 5.0–5.2, upgrading Moodle (e.g. 5.0 → 5.2) needs no different plugin
version — the same release keeps working. After any Moodle upgrade, run the standard Moodle upgrade so
the plugins' (unchanged) versions are re-checked and caches are purged.
