# Content &amp; metadata

## What is indexed

Per course section, the connector turns supported modules into documents (see [How it
works](how-it-works.md) for the full table):

- **Resource** → the file itself (kept in its original format).
- **Page** → the page HTML.
- **Book** → all chapters, merged into one Markdown document.
- **Forum** → all discussions, as Markdown.
- **Assignment / Quiz** → the activity **description**, as Markdown.

**Not indexed:** `label` and `url` modules; student submissions, quiz questions, grades and messages;
and anything **empty** — an activity with no content (a forum with no discussions, or an assignment with
no description) produces no document.

Each document's **semantic identifier** is `Course fullname / Section name / File-or-activity name`, which
is what appears when RAGflow cites the document.

## Metadata on every document

The connector attaches a metadata record to each document. Downstream tools filter and display with these
fields; the **course scope** used by the Moodle plugins relies on `course_id` + `moodle_url`.

| Field | Meaning |
|---|---|
| `moodle_url` | Base URL of the source Moodle site. |
| `course_id` | Moodle course id. |
| `course_name` | Course full name. |
| `course_shortname` | Course short name. |
| `section_id` · `section_name` · `section_number` | The section (topic/week) the item is in. |
| `module_id` · `module_name` · `module_type` | The Moodle course module (its id, display name and type, e.g. `resource`). |
| `time_created` · `time_modified` | Module timestamps, where Moodle provides them. They are often **empty** — file resources and pages, for example, do not expose them. |
| `visible` | Whether the module is visible to students. |
| `groupmode` | The module's group mode. |

### Type-specific fields

| Type | Extra fields |
|---|---|
| **Resource** | `module_instance`, `file_url`, `file_name`, `file_size`, `file_type` (MIME). |
| **Page** | `module_instance`, `page_url`, `file_name`, `file_size`, `file_type`. |
| **Forum** | `forum_id`, `discussion_count`, `discussions[]` (per discussion: id, name, user id/name, timestamps). |
| **Book** | `book_id`, `chapter_count`, `chapters[]` (per chapter: id, title, filename, url, timestamps, size). |
| **Assignment / Quiz** | `activity_type`, `activity_instance`, `description`, `added`. |

!!! note "Visibility is recorded, not enforced"
    The connector **stores** `visible` but indexes visible and hidden modules alike (whatever the token
    user can read). If you need hidden material excluded, don't enrol the connector's user where it
    shouldn't see, or filter on `visible` downstream.

Next: [Sync behaviour](sync-behaviour.md) · [Using it with the Moodle RAGflow Suite](moodle-suite.md).
