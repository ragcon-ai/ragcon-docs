# Usage dashboard: value at scale

The Tutor, Search and Helpdesk plugins and the AI provider deliver the AI features, and they are free.
The **Usage Dashboard** is the operations layer above them: it makes running the suite **measurable,
manageable and defensible**.

On a small pilot you may not need it. On a real, growing installation it is what turns *"we have an AI
assistant"* into *"we run AI responsibly — we know what it costs, we know it works, and we can prove it."*

This page is the business case. For the tabs, settings and data model, see the
[Usage dashboard reference](dashboard.md).

## What it solves — especially at scale

### See what your AI costs

Every chat answer spends tokens on your language model. Across many courses and users that cost adds up,
and without measurement you are flying blind. The **Tokens** tab reports token consumption per day, per
plugin and per provider instance, so you can justify a budget, spot a runaway course or user early, and
attribute cost to a faculty or department.

### Know every knowledge base still works

At scale, a course tutor's knowledge base may fail to parse, or an assistant may be deleted in RAGflow —
and the block quietly answers *"nothing found"*. Nobody can check hundreds of block instances by hand. The
**Status** tab verifies every reference with a traffic light, tells *misconfigured* apart from *RAGflow
unreachable*, and lets you refresh one area at a time. You find the broken one before a student reports it.

### Show adoption and return

The **Usage** tab shows request volume and success rate over time, broken down **by feature, by course, by
user group (trainers vs. students)** and the top users. That is the evidence a rollout needs: who uses the
AI, where it lands, and whether it is growing — so you can decide where to expand.

### Cut support time

When something breaks, *"the AI does not work"* is not a diagnosis. The **Errors** tab groups failures by
labelled cause (rate limited, query too long for the embedding model, RAGflow server error, …), the **API
calls** log shows the exact request and response, and an optional per-feature **debug capture** records a
bounded request/response while you investigate. Root cause in minutes, not a ticket tennis match.

### Oversight without storing user content

The usage log holds **metrics only — no message content**. Add optional **anonymisation**, a daily
**retention/purge** task, a full Privacy API provider and admin-only access, and you have real oversight
that your data-protection officer can sign off. For universities, public bodies and any GDPR-bound
institution, this is often the decisive point: you can supervise the AI **without** keeping what users
typed.

### Report to the institution

The **Export** tab downloads the usage log for any date range as **CSV, XML or PDF**, all views in one
file. That feeds institutional reporting, a board-ready PDF and chargeback figures per course or
department.

## Why larger installations feel it most

| At scale | Without the dashboard | With it |
|---|---|---|
| Many block instances and courses | knowledge bases fail silently | the **Status** traffic light finds them first |
| Many users | AI cost is unknown | **token** trends + top users |
| Institutional scrutiny (budget, privacy) | no evidence to show | **export** + **anonymisation** + metrics-only |
| A support desk | guesswork | **error types** + the **API log** |
| Several faculties | no way to attribute usage | **by-course / by-group** breakdowns |

## Honest limits

Token accounting is an **indicator, not a billing meter**. It counts **chat only** (search uses no tokens)
and only chats over RAGflow's OpenAI-compatible endpoint; chats that use session memory return no token
data and are not counted; counting **starts at installation**; and the figures reflect what RAGflow
reports, without guarantee. Read the token figures as **trends and anomaly signals**, not an invoice.

## Low risk to adopt

The dashboard is **optional** and reads the provider's usage through an independent sink, so the other
plugins work fully without it and nothing breaks if it is absent. It stores no message content by default,
and you can remove it at any time. Each installed feature adds its own status checks and analytics through
an `rfdsource_*` sub-plugin, so the picture stays complete as the suite grows.

---

See also: [Usage dashboard reference](dashboard.md) · [Security & data protection](../security.md)
