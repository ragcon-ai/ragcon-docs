# Set up RAGflow

This page connects Moodle to your RAGflow instance once, centrally. All suite plugins reuse this
provider, so you only do this setup a single time.

!!! info "What you need"
    - A reachable **RAGflow base URL** (e.g. `https://ragflow.example.org`).
    - A **RAGflow API key** (RAGflow → *API* → generate a key).
    - At least one RAGflow **assistant (chat)** bound to a **knowledge base / dataset** that contains
      your documents. See [Prepare a knowledge base](#1-prepare-a-knowledge-base-in-ragflow) below.

## Before you start: configure your models

<!-- shot:setup-01 -->
<!-- shot:setup-02 -->

New RAGflow accounts do **not** receive default models automatically — each account adds its **own**
models under *Model providers* (a **chat**, an **embedding** and, optionally, a **rerank** model) and then
picks defaults under *Set default models*. Do this **before** using the Moodle plugins.

!!! warning "The default embedding model matters"
    A knowledge base is embedded with your account's **current default embedding model** at the moment it
    is created — including knowledge bases the **Tutor block creates for you**. The plugins never hard-code
    an embedding model; they always use your account's current default. Therefore:

    - Set a **working** default embedding model in *Set default models* first.
    - The embedding model of an **existing** knowledge base **cannot be changed** afterwards — if it is
      wrong, recreate the knowledge base.
    - If the default is missing or points at an unconfigured provider, embedding/retrieval fails with
      *"Provider not found for model …"* (see the [admin FAQ](guides/admin.md#faq)).

## 1. Prepare a knowledge base in RAGflow

<!-- shot:setup-03 -->
<!-- shot:setup-04 -->
<!-- shot:setup-05 -->

In your RAGflow instance:

1. Create a **dataset** and upload the documents you want answers to draw from.
2. Wait until the documents are **parsed/embedded** (RAGflow shows the progress).
3. Create an **assistant (chat)** and bind it to that dataset.
4. Note the assistant so you can select it in Moodle.

!!! warning "Check the assistant's system prompt"
    RAGflow's **default** assistant prompt tells the model to "list the knowledge-base entries", which
    makes it wrongly answer *"the knowledge base is empty"* when a question has no matches (even though
    the dataset has content). If you create the assistant manually, replace its system prompt with a
    cleaner one — see [Answer wording when nothing is found](guides/admin.md#answer-wording-when-nothing-is-found)
    in the admin guide. (Assistants the Tutor block creates already get a clean prompt.)

!!! tip "Embedding model & context window"
    Retrieval embeds your query with the dataset's embedding model. Very long queries can exceed a
    small model's context window. The suite already keeps queries short, but choose an embedding
    model appropriate to your content.

## 2. Add the RAGflow AI provider in Moodle

<!-- shot:setup-06 -->
<!-- shot:setup-07 -->
<!-- shot:setup-08 -->
<!-- shot:setup-09 -->

1. Go to **Site administration → General → AI → AI providers** (Moodle's AI subsystem).
2. **Add** a new *RAGflow* provider instance.
3. Enter the **base URL** and **API key** from your RAGflow instance.
4. Configure the actions you want (chat, and optionally source display / memory) and select the
   **assistant** to use.
5. **Enable** the provider and save.

!!! success "Verify the connection"
    If the base URL or key is wrong, or RAGflow is unreachable, chats fail with *"Unexpected response
    from RAGflow"*. Administrators (and users with `aiprovider/ragflow:viewerrordetails`) see the
    **technical cause** under a *Details* disclosure — e.g. `HTTP 502` (RAGflow down) or an embedding
    error. Use that to diagnose the connection.

## 3. Enable the plugins you want

Each surface is enabled independently:

- **[Tutor block](plugins/tutor.md)** — add the *RAGflow Tutor* block to a course; teachers upload
  course documents into the block's own knowledge base.
- **[Search block](plugins/search.md)** — add the *RAGflow Search* block to a course or dashboard.
- **[Helpdesk placement](plugins/helpdesk.md)** — enable the placement under **AI → AI placements**;
  a help drawer appears site-wide.
- **[Usage dashboard](plugins/dashboard.md)** — view under **Site administration → Reports → RAGflow
  Dashboard**.

## 4. Permissions

- `aiprovider/ragflow:viewerrordetails` — who may see the **technical error cause** on a failed chat
  (default: Manager + editing Teacher; site admins always). Keep it off for ordinary users, since the cause
  can reveal server-side internals.
- Each surface has its own `:use` capability (e.g. `block/ragflowtutor:use`,
  `aiplacement/ragflowhelpdesk:use`) and management capabilities for editing knowledge bases.

## Troubleshooting

<!-- shot:setup-10 -->

| Symptom | Likely cause | What to check |
|---|---|---|
| *Unexpected response from RAGflow* + `HTTP 502/504` | RAGflow unreachable / down | Is the RAGflow service up? Base URL correct and reachable from the Moodle server? |
| *Unexpected response* + `HTTP 401/403` | Bad API key | Regenerate the key in RAGflow, update the provider instance |
| Embedding / context-window error | Query too long for the embedding model | Use a larger-context embedding model, or shorter documents/queries |
| No answers, empty sources | Dataset not parsed yet, or assistant not bound to the dataset | Confirm parsing finished; confirm the assistant is bound to the dataset |

Administrators can also open **Reports → RAGflow Dashboard** and enable a component's **debug capture**
to see the exact request/response of recent calls.
