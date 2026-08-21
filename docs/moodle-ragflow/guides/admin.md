# User guide — for administrators

This guide is for **Moodle site administrators** who install, configure and operate the RAGflow suite.
For teaching staff see the [trainer guide](trainer.md); for learners the [student guide](student.md).

## Your responsibilities

- Install the plugins and connect Moodle to your RAGflow instance (once, centrally).
- Choose which surfaces are available (Tutor blocks, Search blocks, the Helpdesk drawer).
- Manage permissions and monitor usage.

## 1. Install the plugins

Install in dependency order — the **AI provider first**, then the rest:

1. `aiprovider_ragflow` (provider — required by all others)
2. `aiplacement_ragflowhelpdesk`, `block_ragflowtutor`, `block_ragflowsearch`
3. `local_ragflowdashboard` (optional)

Use the correct path for your Moodle version (`public/…` on 5.1+) — the plugin installer handles this
automatically. See [Moodle version specifics](../moodle-version-notes.md).

## 2. Connect to RAGflow

Follow **[Set up RAGflow](../setup-ragflow.md)**: prepare a dataset + assistant in RAGflow, then add the
**RAGflow AI provider instance** in *Site administration → AI → AI providers* with your base URL and API
key. The provider is the shared backend for every other plugin.

## 3. Enable and configure the surfaces

| Surface | Where to configure | Key settings |
|---|---|---|
| **[Helpdesk drawer](../plugins/helpdesk.md)** | *AI → AI placements → RAGflow Helpdesk* | assistant, greeting, conversation memory (on), long-term memory (off), sources |
| **[Tutor block](../plugins/tutor.md)** | Block added per course; admin setting under *Blocks → RAGflow Tutor* | upload limit; per-block: assistant/KB, document source, sources |
| **[Search block](../plugins/search.md)** | Block added per page (admin-only config) | knowledge base(s), scope |
| **[Usage dashboard](../plugins/dashboard.md)** | *Plugins → Local plugins → RAGflow Dashboard settings* | retention, anonymise, debug per feature |

## 4. Permissions

- `aiprovider/ragflow:viewerrordetails` — who sees the **technical cause** of a failed chat (default
  Manager + Teacher; admins always). Keep it off for ordinary users, as it can reveal server internals.
- `aiplacement/ragflowhelpdesk:use` — who sees the Helpdesk drawer (default: any authenticated user).
- `block/ragflowtutor:*` — tutor use, add, edit content, change/create KB, manage files.
- `local/ragflowdashboard:view` — who sees the dashboard (default: Manager only).

## 5. Monitor and diagnose

Open *Reports → RAGflow Dashboard* for request volume, success/failure rates, latency and error types.
When diagnosing a specific feature, enable its **debug capture** temporarily to record the exact
request/response (including the technical error cause) — then turn it off again (it captures user
content). Mind data protection and the retention setting.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| *Unexpected response from RAGflow* + `HTTP 502/504` | RAGflow unreachable / down | Check the RAGflow service; confirm the base URL is reachable from the Moodle server |
| *Unexpected response* + `HTTP 401/403` | Bad API key | Regenerate the key in RAGflow, update the provider instance |
| Embedding / context-window error | Query too long for the embedding model | Use a larger-context embedding model |
| Empty answers, no sources | Dataset not parsed, or assistant not bound to it | Confirm parsing finished and the assistant is bound to the dataset |
| Helpdesk item not in the menu | Placement disabled or no assistant selected | Enable the placement and select an assistant |
| Answer claims the knowledge base is *"empty"* for a question that has no match | RAGflow assistant's **system prompt** (its default) mishandles no-hit questions | Adjust the assistant's prompt in RAGflow — see [Answer wording](#answer-wording-when-nothing-is-found) below |

### Answer wording when nothing is found

The wording of an answer — including what the assistant says when a question has **no relevant
matches** — comes from the **RAGflow assistant's own system prompt**, not from Moodle. RAGflow's default
prompt instructs the model to "list the knowledge-base entries", so on a question with no hits (for
example a greeting like *"Hallo"*) the model may wrongly claim the *knowledge base is empty*, even though
it contains documents — there were simply no matches for that question.

Assistants **created through the Tutor block** get a clean prompt automatically. An assistant you created
**manually in RAGflow** keeps RAGflow's default and may need adjusting. RAGflow **ignores prompt changes
made through its API** on an existing assistant, so edit it **in the RAGflow UI** (open the assistant →
*Prompt engine* → *System prompt*). A prompt that avoids the problem:

```
You are a helpful assistant. Answer the question using only the knowledge base below, and
reply in the same language as the question. Take the chat history into account.

Do not list or enumerate the knowledge-base entries — just give the answer.

If the knowledge base contains nothing relevant to the question, briefly say that nothing
was found for this question. Do NOT claim that the knowledge base is empty or has no
entries — there were simply no matches for this question.

Knowledge base:
{knowledge}
```

Keep the `{knowledge}` placeholder (RAGflow injects the retrieved content there), and do **not** add a
rule forbidding `[ID]` references — the source list relies on them. The prompt language does not dictate
the answer language (answers follow the question's language), so you can keep it in English or translate
it for your team.

## FAQ

**Do I need to run RAGflow myself?**
Yes — the suite is a client for a RAGflow instance (self-hosted or hosted). It does not bundle RAGflow.
You provide a reachable base URL and an API key.

**Is one provider instance enough for all plugins?**
Yes. Configure the provider once; the Helpdesk, Tutor and Search all use it. Each surface still selects
its own assistant/knowledge base.

**Where is data stored?**
Prompts (and, with long-term memory on, durable user facts) are sent to and stored in RAGflow — a
third-party processor. Moodle itself stores only usage metrics (and, only while debug is on, bounded
content). See each plugin's Privacy section.

**Which Moodle versions are supported?**
5.0, 5.1 and 5.2 from one plugin line. Moodle 4.5 and earlier are **not** supported. On Moodle 5.0, pin
**PHP 8.3** (5.0 rejects PHP 8.4). See [Moodle version specifics](../moodle-version-notes.md).

**Can teachers see the technical error details?**
Only if they hold `aiprovider/ragflow:viewerrordetails` (default Manager + Teacher). Ordinary users only
see the generic message. The gate is enforced server-side.

**How do I stop capturing user content?**
Turn off the per-feature debug toggle in the dashboard settings. Debug capture is off by default and
should only be enabled temporarily for diagnosis.
