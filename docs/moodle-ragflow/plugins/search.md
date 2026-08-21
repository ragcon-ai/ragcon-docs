# Search block

!!! info "Repository &amp; issue tracker"
    - **Repository:** [https://github.com/ragcon-ai/moodle-block_ragflowsearch](https://github.com/ragcon-ai/moodle-block_ragflowsearch){ target="_blank" rel="noopener" }
    - **Issues / bug tracker:** [https://github.com/ragcon-ai/moodle-block_ragflowsearch/issues](https://github.com/ragcon-ai/moodle-block_ragflowsearch/issues){ target="_blank" rel="noopener" }

**Component:** `block_ragflowsearch` · **Release:** 0.3.2 · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

A Moodle block that adds a search box to any page and searches one or more RAGflow **knowledge bases**
semantically, listing the matching source documents. It is **retrieval only — no LLM** (fast, cheap,
no hallucination, links to real documents). The search widget itself is hosted by the shared
[AI provider](provider.md); the block chooses the knowledge base and scope per instance.

## Features

- **Placeable on any page** (courses, the Dashboard, the front page, …).
- **Semantic search over one or more RAGflow datasets**, chosen per block instance.
- **Ranked results** with a relevance score and snippet, each linking to the source document through
  the provider's secure download proxy (the RAGflow API key never reaches the browser).
- **Fewer, better matches** — a relevance floor, a relevance "cliff" and a result cap trim weak hits;
  **images/media** get their own group so they aren't lost; an **optional rerank model** sharpens
  precision further (see [Result quality](#result-quality-fewer-better-matches)).
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
| **Rerank model** (`config_rerankmodel`) | text | empty (off) | *Optional.* A RAGflow rerank model id (e.g. a bge-reranker configured in your RAGflow). When set, RAGflow reorders the candidates with a cross-encoder for markedly better precision. Empty = plain vector/keyword ranking. |

## Result quality (fewer, better matches)

The search is tuned to return a **short, relevant list** instead of a fixed number of hits. This needs
**no configuration** — the defaults are sensible; only the optional rerank model is a setting.

- **Relevance floor** — matches below a minimum score are dropped, so weakly related documents no longer
  clutter the list.
- **Relevance "cliff" + result cap** — once the scores fall away from the best hit (or the cap of 5 is
  reached) the list stops. A query with two strong matches returns two, not a padded eight.
- **Images & media handled separately** — images (and other media) embed with **low text similarity**, so
  a single floor would wrongly hide them. They get a **lower floor** and appear in their own **"Images &
  media"** group below the text results, rather than being dropped or diluting the text ranking.
- **Optional reranking** — set a **rerank model** (above) and RAGflow reorders the retrieved candidates
  with a cross-encoder. This is the single biggest precision gain: the truly relevant documents rise to
  the top and the tail is cut by the cliff. It is opt-in (needs a rerank model in your RAGflow) and adds a
  little latency.

**Benefits:** shorter, more trustworthy result lists; no irrelevant filler; images stay findable; and,
with reranking on, noticeably sharper ordering — all with sensible defaults out of the box.

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
