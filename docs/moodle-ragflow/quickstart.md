# Quickstart

Short, ordered checklists to get going fast. No screenshots — follow the linked full guide at the end of
each part for the detail. Navigation paths are shown as *Site administration → …*; where a direct link
exists it is given as a site-relative URL (prefix it with your Moodle address).

## Administrators

Set up the shared backend first, then switch on only the surfaces you want.

1. **Install the plugins** in dependency order — the **provider first**.
   *Site administration → Plugins → Install plugins* (`/admin/tool/installaddon/index.php`).
   Order: `aiprovider_ragflow` → Helpdesk / Tutor / Search → Dashboard *(optional)*.
2. **[Prepare RAGflow](setup-ragflow.md)** — connect your models (chat + embedding required; img2txt +
   rerank recommended) and set them as defaults, then create a dataset + assistant.
3. **Add the AI provider instance** — enter the base URL + API key.
   *Site administration → AI → AI providers* (`/ai/configure_providers.php`).
4. **Switch on the surfaces you want:**
      - Helpdesk drawer — *Site administration → AI → AI placements → RAGflow Helpdesk*.
      - Tutor block defaults — *Site administration → Plugins → Blocks → RAGflow Tutor*.
      - Search block defaults — *Site administration → Plugins → Blocks → RAGflow file search*.
      - Usage dashboard — *Site administration → Plugins → Local plugins → RAGflow Dashboard settings*.
5. **Review permissions** — *Site administration → Users → Permissions → Define roles*: who may see error
   details (`aiprovider/ragflow:viewerrordetails`), use the Helpdesk (`aiplacement/ragflowhelpdesk:use`),
   use/manage the Tutor (`block/ragflowtutor:*`) and view the dashboard (`local/ragflowdashboard:view`).
6. **Monitor** — the usage dashboard (`/local/ragflowdashboard/index.php`),
   *Site administration → Reports → RAGflow Dashboard*.

→ Full detail: [Administrator guide](guides/admin.md) · [Set up RAGflow](setup-ragflow.md) ·
[Security & data protection](security.md)

## Trainers

On a course you teach (with editing turned on):

1. **Add the Tutor** — turn editing on, then **Add a block → RAGflow Tutor**.
2. **Configure it** — pick an existing assistant / knowledge base, or *(if allowed)*
   **➕ Create new knowledge base** and give it a name.
3. **Build the knowledge base** — upload, re-process or delete documents in the block's knowledge-base
   panel; wait until files show **green (parsed)** before expecting answers.
4. *(optional)* **Add a Search block** — **Add a block → RAGflow file search**; choosing its knowledge base is
   admin-only, so ask your administrator to point it at the right one.
5. *(optional)* **Personalise** — edit the greeting and system instruction in the block configuration.

→ Full detail: [Trainer guide](guides/trainer.md)

## Students

No setup needed — just use what your course offers:

1. **Course tutor** — if your course page shows a **RAGflow Tutor**, open the chat and ask about the
   course material.
2. **Document search** — if there is a **RAGflow file search** box, type a query to find the matching files.
3. **Helpdesk** — if your site shows a **RAGflow Helpdesk** in the menu, use it for general questions.

→ Full detail: [Student guide](guides/student.md)
