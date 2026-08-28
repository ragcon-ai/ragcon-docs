# FAQ

Answers to recurring questions about the Moodle RAGflow suite. Missing something? Open an issue on the
relevant plugin's repository (linked at the top of each [plugin page](plugins/provider.md)), or see
[Help &amp; Support](../support.md).

## Answers, sources and language

??? question "Why does the Tutor sometimes say the answer isn't in the course materials?"

    That is intended. The Tutor answers **only** from the knowledge base for that course and will not invent
    a plausible-sounding answer when the materials don't cover the question — for a course tutor, declining is
    safer than guessing. If something *should* be answerable, add or re-process the relevant document (see
    [Tutor block](plugins/tutor.md)), or rephrase the question. A greeting or small-talk can trigger a similar
    line — see the next entry.

??? question "The assistant greets the user but adds *“The answer you are looking for is not found in the dataset!”* — even to a plain “hello”. Why?"

    That sentence comes from the **RAGflow assistant's own system prompt**, not from the plugin.
    RAGflow's *default* assistant prompt contains a fixed instruction along the lines of: *“When all
    dataset content is irrelevant to the question, your answer must include the sentence 'The answer you
    are looking for is not found in the dataset!'.”* A greeting matches nothing in the knowledge base, so
    the model both greets **and** appends that mandated sentence.

    This only happens when the block is pointed at an assistant that was **created in RAGflow's own web
    UI** (which seeds that default prompt). Knowledge bases/assistants **created from the block** get a
    clean prompt that does not force the sentence. The block's own *System instruction* setting cannot
    override it either: RAGflow's chat endpoint ignores a per-request system message — the assistant's
    stored prompt always wins.

    **Fix it one of two ways:**

    - **Recommended — use a block-created assistant.** In the block's *Knowledge base / assistant*
      setting choose **➕ Create new knowledge base …** and add the course documents there. The new
      assistant is given the clean prompt automatically.
    - **Or edit the existing assistant in RAGflow.** Open the assistant in RAGflow → *Prompt* and remove
      the “…must include the sentence …not found in the dataset!” clause (and clear *Empty response* if
      it is set). RAGflow only applies such prompt changes in its own UI; the plugin cannot rewrite an
      existing assistant's prompt through the API, which is why a block-created assistant is the simpler
      route.

    See [Tutor block → Knowledge base / assistant](plugins/tutor.md) for where the assistant is chosen.

??? question "Can I trust the sources listed under an answer?"

    The citations come from the **documents the model actually used** to write the answer (its own reference
    markers), not a separate keyword search — so the list reflects the real basis of the answer. As with any
    AI, open the linked source to confirm the detail that matters. Retrieval-only results in the
    [Search block](plugins/search.md) are even more direct: every hit is a real document you can open.

??? question "In which language does it answer?"

    In the user's **Moodle language**, taken from their profile or the course's forced language —
    independently of the language your documents are written in. You don't configure this per plugin.

??? question "Is my chat private — can teachers or admins read it?"

    Conversations are **per user**. The Helpdesk has a private/incognito mode and a *forget memory* control,
    and long-term memory is opt-in. The usage log stores **metrics only — no message content**. See
    [Security and data protection](security.md).

## Documents and understanding

??? question "What does “deep document understanding” mean?"

    RAGflow reads the **content** of your files, not just their titles: **OCR** turns scanned PDFs and
    photographed pages into text, **layout recognition** captures titles, tables, figures and reading order,
    and an optional **vision model** describes images and diagrams so their content becomes searchable. On
    RAGflow 0.25+ **MinerU** and **Docling** are additional parsing methods (formula and table recognition).
    The result: scans, images and tables become answerable, not just plain text. See
    [Document understanding](document-understanding.md).

??? question "Which file types can it read — and does it handle scans and images?"

    Common document formats (PDF, Word, PowerPoint, Excel, HTML, Markdown, plain text), plus scanned PDFs and
    images via OCR and — for the *content* of pictures and diagrams — an optional vision model. Whether image
    understanding is available depends on the RAGflow models your administrator has configured; see
    [Set up RAGflow](setup-ragflow.md) or ask your Moodle/RAGflow administrator.

??? question "I uploaded a document but the Tutor doesn't know it yet — why?"

    RAGflow **parses** each document first, which takes anywhere from seconds to minutes for a large scanned
    file. The knowledge-base panel shows a status indicator; the document is available once it turns
    **green**. See [Tutor block](plugins/tutor.md).

??? question "How do I keep the knowledge bases up to date?"

    Either manage documents in the block (upload / re-process / delete), or use the
    **[RAGflow Moodle Connector](../ragflow-moodle-connector/index.md)** to sync a Moodle course's content
    into the knowledge base automatically, so answers reflect the current materials without manual re-upload.

## Tutor, Search and Helpdesk

??? question "Why does RAGflow find more than Moodle's built-in search?"

    Moodle's search is built to find **courses and activities by name** — it matches keywords against
    titles, text fields, metadata and forum posts. It does not look **inside** your files.

    RAGflow reads the **content** of the documents themselves. Its DeepDoc engine applies **OCR** (so
    scanned PDFs and photographed pages become text), recognises **layout** (titles, tables, figures,
    equations and reading order) and captures **table structure**; an optional vision model even
    **describes images and diagrams**, so their content becomes searchable and can appear as a source.
    Retrieval then matches by **meaning** (embeddings, optional rerank), not exact keywords, and returns
    the supporting **passage and image** — which the Tutor and Helpdesk can turn into a cited answer.

    In short: Moodle's search finds *where* something is; RAGflow finds *what a document says*. See
    [Document understanding](document-understanding.md) for the details.

??? question "What's the difference between the Tutor and the Search block?"

    The **[Tutor](plugins/tutor.md)** *answers* questions in a chat, grounded in a course's knowledge base and
    with citations. The **[Search](plugins/search.md)** block only *finds* documents — a ranked list of
    sources with the matching passage, no generated answer. Use Search when you want the file; use the Tutor
    when you want an answer.

??? question "Tutor or Helpdesk — which one do I use?"

    The **[Tutor](plugins/tutor.md)** is per course, grounded in that course's materials, and lives on the
    course page. The **[Helpdesk](plugins/helpdesk.md)** is site-wide, answers from an organisation-wide
    knowledge base, and is reached from the site's user menu on every page.

??? question "The Search block returns nothing or very few results — is it broken?"

    Probably not. A **relevance floor** hides weak matches on purpose, so *“no strong match”* is a valid,
    honest result rather than a padded list. Try rephrasing or broadening the query; an administrator can tune
    the threshold and an optional rerank model per block — see [Search block](plugins/search.md).

## Setup and operation

??? question "If I point the provider's generate_text action at a RAGflow assistant, does that affect Moodle's built-in AI (editor, course assistant)?"

    Yes. Routing in Moodle's AI subsystem is by **action**, not by plugin: every `generate_text` /
    `summarise_text` / `explain_text` request that Moodle sends to the RAGflow provider — including Moodle's
    own placements (editor AI, course assistant) and any third-party AI placement — is answered by the
    assistant you configured for that action. If you don't want that, control it in the AI subsystem: disable
    the action on the provider instance (or don't make the provider available for that action), or turn the
    placement off. See [AI provider](plugins/provider.md) and [Security and data protection](security.md).

??? question "Do the Tutor and Search blocks go through Moodle's AI subsystem?"

    No. They use the provider's **connection** (base URL and API key) directly, with their **own per-block
    knowledge base and assistant** — not the core `generate_text` action. So a block's assistant/KB is
    independent of the provider's per-action configuration; changing one does not change the other. See
    [AI provider](plugins/provider.md).

??? question "Which RAGflow models do I need?"

    A **chat model** and an **embedding model** are required; an **img2txt (vision)** model is needed for
    image understanding, and a **rerank** model is optional. Your administrator sets these in RAGflow — see
    [Set up RAGflow](setup-ragflow.md) and the [RAGflow documentation](https://ragflow.io/).

??? question "What data leaves Moodle, and where is it stored?"

    The suite talks only to **your RAGflow instance** — one you run yourself, or one **RAGcon hosts for
    you** — never a shared third-party service. Documents, conversations and embeddings live in that RAGflow
    instance; the provider's usage log in Moodle holds **metrics only** (no message content). Either way the
    data stays under your (or your hosting provider's) control — see
    [Security and data protection](security.md), or ask [RAGcon support](../support.md) about hosting.

??? question "Do I need the RAGflow Moodle Connector?"

    No — it's optional. Without it you manage documents directly in the blocks. With it, a Moodle course's
    content is synced into the RAGflow knowledge base automatically, which is useful when the material changes
    often. See the [RAGflow Moodle Connector](../ragflow-moodle-connector/index.md).

??? question "Is the usage dashboard required?"

    No. The **[dashboard](plugins/dashboard.md)** is an optional add-on; the other four plugins
    (provider, tutor, search, helpdesk) work fully without it.
