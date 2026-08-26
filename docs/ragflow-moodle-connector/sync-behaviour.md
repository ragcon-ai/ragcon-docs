# Sync behaviour

RAGflow runs the connector on a schedule for the knowledge base it is bound to. There are three modes; you
normally only pick between a first full load and the ongoing incremental sync — the cleanup runs alongside.

## Full load

The first sync (and any manual **re-index**) is a **full load**: every supported module in every enrolled
course is fetched and indexed. Use this to seed a new knowledge base, or to rebuild it after big changes.

## Incremental sync

Routine syncs are **incremental**: the connector re-reads the course structure but only re-indexes modules
whose **`timecreated` / `timemodified`** (or a file's modification time) falls inside the sync window. New
and changed items are picked up; untouched items are left as they are. Because document ids are stable
(`moodle_<type>_<id>`), a changed item **replaces** its existing document instead of duplicating it.

## Removing deleted items (stale cleanup)

The data source has a **Sync deleted files** option; it is **off by default**. With it on, the connector
produces alongside each sync a lightweight **snapshot** of
the ids of every module that *could* be indexed (no downloads). RAGflow compares that list to what is in
the knowledge base and **deletes** any indexed document whose Moodle module no longer exists (or is no
longer reachable by the token user). So un-enrolling the connector's user from a course, or deleting an
activity, removes the corresponding documents on the next sync.

## What triggers a re-index of a single item

An item is re-indexed when its module or its file reports a newer `timemodified`. Editing a page or book,
posting to a forum, replacing a resource file, or changing an activity's description all bump the
timestamp and cause a refresh on the next incremental sync.

## Practical notes

- **Scope follows enrolment.** The set of indexed courses is exactly the token user's **enrolled** courses
  at sync time — enrol the user in a new course and it appears next sync; un-enrol and its documents are
  cleaned up.
- **Parsing is RAGflow's job.** The connector delivers the raw documents; RAGflow then parses/embeds them
  into the knowledge base with that KB's configured pipeline and embedding model.
- **Frequency** is set on the **data source** itself, not per knowledge base: the **Refresh Freq** field
  (in minutes) in the Moodle source's settings. Pick a cadence that matches how often your courses change —
  a short interval on a large site means syncs overlap or run into **Timeout Secs**.

See also: [How it works](how-it-works.md) · [Troubleshooting](troubleshooting.md).
