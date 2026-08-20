# Tutor block

**Component:** `block_ragflowtutor` · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

A per-course **AI tutor** rendered as a chat drawer on the course page. Each block instance has its
**own knowledge base**: teachers upload course documents, and learners ask questions answered from
those documents (with source citations).

## Features

- Course-scoped chat drawer driven by the shared provider engine.
- Per-instance **knowledge base**: upload/manage files, watch parsing status, re-parse or delete.
- Source citations, optionally served through the signed Moodle proxy.
- Answers in the learner's Moodle language.

## Setup

1. [Set up RAGflow](../setup-ragflow.md) (provider) first.
2. Turn editing on in a course → **Add a block** → *RAGflow Tutor*.
3. In the block's management view, upload the course documents to build its knowledge base.
4. Wait for parsing to finish, then ask questions in the drawer.

## Capabilities

| Capability | Default | Purpose |
|---|---|---|
| `block/ragflowtutor:use` | Student, Teacher, Manager | Ask questions in the tutor |
| `block/ragflowtutor:createkb` / `:editkb` / `:managefiles` | Teacher, Manager | Create/manage the knowledge base and its files |
| `block/ragflowtutor:editcontent` | Teacher, Manager | Edit greeting / system instruction |
| `block/ragflowtutor:addinstance` | Teacher, Manager | Add the block to a course |
