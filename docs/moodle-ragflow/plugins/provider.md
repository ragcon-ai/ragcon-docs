# AI provider (RAGflow)

**Component:** `aiprovider_ragflow` · **Requires:** Moodle 5.0–5.2 · **Depends on:** — (this is the root)

The RAGflow AI provider is the backend for the whole suite. It plugs into Moodle's **AI subsystem**
as a provider instance and talks to your RAGflow instance for chat, source retrieval and (optionally)
server-side conversation memory. Every other plugin in the suite delegates to it, so it must be
installed and configured first.

## Features

- **Chat completions** against a RAGflow assistant, with a stateless mode and an optional
  **session-memory** mode (RAGflow keeps the conversation).
- **Source documents** returned with each answer, optionally streamed through a signed, time-limited
  Moodle proxy so the RAGflow API key never reaches the browser.
- **Answers in the user's Moodle language.**
- **Usage events** (metrics only — no message content) for the [dashboard](dashboard.md).
- **Diagnosable failures:** on error the real technical cause (HTTP status, RAGflow `{code, message}`,
  embedding errors) is surfaced to holders of `aiprovider/ragflow:viewerrordetails`.

## Setup

Configured as an AI-provider instance — see **[Set up RAGflow](../setup-ragflow.md)**.

## Capabilities

| Capability | Default | Purpose |
|---|---|---|
| `aiprovider/ragflow:viewerrordetails` | Manager, Teacher (admins always) | See the technical cause of a failed chat (may reveal server-side internals) |

## Privacy

Prompts (and, with memory enabled, the ongoing conversation and remembered facts) are sent to and
stored in the configured RAGflow service. See the plugin's Privacy summary in Moodle. Long-term
memory is **off by default** and opt-in.
