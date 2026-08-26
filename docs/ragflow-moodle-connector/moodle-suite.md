# Using it with the Moodle RAGflow Suite

The connector and the **[Moodle RAGflow Suite](../moodle-ragflow/index.md)** are separate products that fit
together well: the connector **fills** a RAGflow knowledge base from Moodle, and the suite's plugins
(Tutor, Search, Helpdesk) **query** that knowledge base from inside Moodle.

You do not need one to use the other — but combined, they give a course a tutor/search grounded in the
course's own Moodle material, kept up to date automatically.

## Course-scoped answers

Each connector document carries `course_id` and `moodle_url` in its metadata (see [Content &amp;
metadata](content-and-metadata.md)). That is exactly what the suite's **document source → *Moodle
Connector*** option filters on:

- In the **Tutor** or **Search** block (or a provider action), choose the *Moodle Connector* /
  *This Moodle* document source. The plugin then restricts retrieval to documents whose `course_id`
  matches the current course **and** whose `moodle_url` matches the site.
- The result: a block placed in a course answers **only from that course's** synced material, without a
  per-course knowledge base — one connector-filled knowledge base can serve every course.

So the typical pairing is:

1. **Connector** → sync the whole Moodle site into one RAGflow knowledge base.
2. **Suite** → point the Tutor/Search blocks at that knowledge base with the *Moodle Connector* source, and
   each course automatically scopes to its own content.

## A note on external sharing

The suite also offers an **External sharing** document source (documents flagged `external_sharing = 1`).
**The connector does not set that flag** — it writes `course_id` / `moodle_url` but not `external_sharing`.
If you want to use the external-sharing scope, that metadata has to be provided another way; the connector
alone enables the **course** scope, not the external-sharing scope.

## Which knowledge base?

Point the connector at the **same knowledge base** the plugins read from. The plugins select a knowledge
base (dataset) by id; the connector fills that dataset. Keep the embedding model consistent — a knowledge
base's embedding model is fixed at creation, so decide it before the first sync.

See the suite docs for the plugin side: [AI provider](../moodle-ragflow/plugins/provider.md) ·
[Tutor](../moodle-ragflow/plugins/tutor.md) · [Search](../moodle-ragflow/plugins/search.md).
