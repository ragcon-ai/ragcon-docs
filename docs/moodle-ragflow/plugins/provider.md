# AI provider (RAGflow)

!!! info "Repository &amp; issue tracker"
    - **Repository:** [https://github.com/ragcon-ai/moodle-aiprovider_ragflow](https://github.com/ragcon-ai/moodle-aiprovider_ragflow){ target="_blank" rel="noopener" }
    - **Issues / bug tracker:** [https://github.com/ragcon-ai/moodle-aiprovider_ragflow/issues](https://github.com/ragcon-ai/moodle-aiprovider_ragflow/issues){ target="_blank" rel="noopener" }

**Component:** `aiprovider_ragflow` · **Release:** 0.5.0 · **Requires:** Moodle 5.0–5.2 · **Depends on:** — (root of the suite)

The RAGflow AI provider plugs into Moodle's core **AI subsystem** and connects Moodle's text AI
actions to an external [RAGflow](https://ragflow.io) instance. Answers are produced by a RAGflow
**chat assistant** over the OpenAI-compatible endpoint, so they are retrieval-augmented and grounded
in the assistant's knowledge base rather than a plain LLM. It is also the shared backend of the whole
suite: it hosts the chat engine, session/long-term memory, source citations and a secure download
proxy that the Tutor, Search and Helpdesk plugins consume. **Install and configure it first.**

## Features

- **Core AI actions:** serves `generate_text`, `summarise_text`, `explain_text`, each answered by the
  configured RAGflow assistant.
- **Assistant-driven model:** the assistant's own model and knowledge base are used; a live dropdown
  lists the tenant's assistants and annotates each with its knowledge-base document count (or "no
  knowledge base — LLM proxy only"), so you can pick a RAG assistant or use RAGflow as a plain LLM.
- **Knowledge-base scoping & metadata filtering:** answers can be filtered to *this Moodle* (course +
  site), the *whole KB*, or *external/shared* documents, and restricted to the current course or the
  user's enrolled courses via a document metadata field.
- **Source citations:** optionally returns the source documents behind an answer, built **from the
  model's own `[ID]` citations** (only the documents actually used). They are numbered per answer as
  `[answer.source]` (e.g. `[1.1]`, `[2.1]`), shown on a `Sources:` line at the end of the answer and as a
  linked list — linking to the Moodle activity when known, otherwise through a secure proxy.
- **Secure download proxy (`download.php`):** streams a RAGflow document server-side so the API key
  never reaches the browser; per-click **signed, time-limited** links (token mode) or **token-less**
  context-authorised links, with a strict content-type allowlist (`nosniff`, forced attachment for
  anything but PDF/PNG/JPEG/GIF/WebP/plain-text).
- **Conversation (session) memory:** for the Helpdesk drawer, RAGflow keeps the conversation so
  follow-ups have context and the transcript is restored on return.
- **Long-term memory:** optional per-user durable facts via RAGflow's native Memory API (opt-in, off
  by default; disabled in private/incognito mode; cleared with the user's data).
- **Answers in the user's Moodle language** (profile or course-forced language).
- **Per-user rate limiting** (20 requests/minute) and a **robust completion path** (120 s timeout,
  one retry on network/5xx, not on 4xx).
- **Diagnosable failures:** the real technical cause (HTTP status, RAGflow `{code, message}`,
  embedding/context-window errors) is surfaced to permitted users and to the [dashboard](dashboard.md);
  a coarse error type feeds usage analytics.
- **Usage events (metrics only, no content):** `chat_completed` / `chat_failed` / `search_performed`
  for the optional [dashboard](dashboard.md).
- **Scheduled task:** *Prune stale RAGflow conversation sessions* (daily) removes sessions unused past
  the retention period (default 30 days).

## Configuration

The provider is configured as an **AI-provider instance** (Moodle's AI subsystem), plus per-action
config. There is no classic settings page.

### Provider instance — *Site administration → AI → AI providers → RAGflow API provider*

| Setting | Type | Default | Meaning |
|---|---|---|---|
| **RAGflow API key** (`apikey`) | password (required) | — | Your RAGflow API key (RAGflow → *User settings → API*). Sent as the Bearer token and used to list assistants. |
| **RAGflow base URL** (`baseurl`) | URL (required) | — | Base URL of your RAGflow instance, e.g. `https://ragflow.example.com`. |
| **Download link lifetime (seconds)** (`tokenttl`) | integer | `60` (min 15) | How long a signed source/file download link stays valid. Links are minted on click, so a short lifetime is safe. |

The provider counts as *configured* only when both API key and base URL are set.

### Per-action config — *per Generate / Summarise / Explain text action*

| Setting | Type | Default | Meaning |
|---|---|---|---|
| **RAGflow chat assistant** (`chatid`) | select (live) / text (required) | — | The assistant to answer with. Its model and knowledge base(s) are used. Pick a KB assistant for RAG, or a KB-less one to use RAGflow as a plain LLM. |
| **System instruction** (`systeminstruction`) | textarea | action default | Instructions prepended as a system message to steer the response. |
| **Document source** (`datasource`) | select | `thismoodle` | `wholekb` (no filter), `thismoodle` (filter: course + site), or `external` (shared documents only). |
| **Restrict to course(s)** (`coursescope`) | select | off | `Current course` or `The user's enrolled courses`. Hidden for *whole KB* / *external*. |
| **Course metadata field** (`coursemetadatafield`) | text | `course_id` | RAGflow document metadata field holding the Moodle course id. |
| **Include sources** (`includesources`) | checkbox | off | Return source documents and append them as a linked list. |
| **Extra parameters (JSON)** (`extraparams`) | textarea | empty | Optional JSON merged into the request body (e.g. `{"extra_body": {"reference": true}}`). Validated as JSON. |

!!! note "Where the chat/drawer settings live"
    The Tutor block and Helpdesk placement each carry their **own** copy of the chat settings
    (assistant, greeting, memory, sources, …) — configured on those plugins, not here — while the
    provider hosts the shared engine that reads them. See the [Tutor](tutor.md) and
    [Helpdesk](helpdesk.md) pages.

## Capabilities

| Capability | Default roles | Purpose |
|---|---|---|
| `aiprovider/ragflow:viewerrordetails` | Manager, Teacher (site admins always) | See the **technical cause** of a failed chat (a *Details* disclosure). The cause can reveal server-side internals (e.g. a RAGflow embedding error or `HTTP 502`), so it is withheld from ordinary users — enforced server-side, `RISK_CONFIG`. |

## Privacy

By default the plugin stores **no personal data** in Moodle. Prompts (and, with long-term memory on,
the ongoing conversation and remembered facts) are **sent to and stored in RAGflow** (a third-party
processor). A small local table references RAGflow **conversation sessions** for the Helpdesk memory.
On user deletion, the plugin deletes those sessions and **forgets** the user's RAGflow memory. Users
can self-disable long-term memory via **private/incognito mode** in the chat.

See also: [Moodle version specifics](../moodle-version-notes.md) for `public/` layout and
version-guarded error handling.
