# Search block

**Component:** `block_ragflowsearch` · **Release:** 0.3.1 · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

A Moodle block that adds a search box to any page and searches one or more RAGflow **knowledge bases**
semantically, listing the matching source documents. It is **retrieval only — no LLM** (fast, cheap,
no hallucination, links to real documents). The search widget itself is hosted by the shared
[AI provider](provider.md); the block chooses the knowledge base and scope per instance.

## Features

- **Placeable on any page** (courses, the Dashboard, the front page, …).
- **Semantic search over one or more RAGflow datasets**, chosen per block instance.
- **Ranked results** with a relevance score and snippet, each linking to the source document through
  the provider's secure download proxy (the RAGflow API key never reaches the browser).
- **Scope: whole KB or current course** (course scope filters by a configurable metadata field; on
  pages without a course the whole KB is searched).
- **Login-gated** (no content for logged-out users or guests); **one instance per page**.
- **Helpful empty states:** a *not configured* hint for users who can add the block, and a
  *no knowledge bases available* message if the provider isn't enabled.

## Configuration

There is **no site-wide settings page** — all configuration is **per block instance**, and only **site
administrators** may set it (non-admins see an "only site administrators can choose the knowledge base"
message, and their saves cannot clear the choice).

### Per-instance block config (*Configure this RAGflow search block*)

| Setting | Type | Default | Meaning |
|---|---|---|---|
| **Knowledge base(s)** (`config_datasets`) | autocomplete (multiple) | none (required) | The RAGflow dataset(s) this block searches. Select one or more; the block does not search until at least one is chosen. |
| **Search scope** (`config_scope`) | select | `Whole knowledge base` | *Whole knowledge base* or *Current course only* (matched via the course metadata field). On pages without a course, the whole KB is searched. |
| **Course metadata field** (`config_coursefield`) | text | `course_id` | RAGflow document metadata field holding the Moodle course id. Only used when scope is *Current course only*. |

## Capabilities

| Capability | Default roles | Purpose |
|---|---|---|
| `block/ragflowsearch:addinstance` | Teacher, Manager | Add a search block to a page |
| `block/ragflowsearch:myaddinstance` | Authenticated user | Add the block to the Dashboard / My home |

!!! note
    Choosing the knowledge base and scope is restricted to **site administrators** (not a capability),
    because a dataset is a site-wide resource.

## Privacy

The block **stores no personal data**. Search queries are sent to the configured RAGflow service by
the [AI provider](provider.md) to retrieve matching documents; source links go through the provider's
secure proxy.
