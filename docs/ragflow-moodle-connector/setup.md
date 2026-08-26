# Set up the connector

Two things are needed: a **Moodle web-service token** for the connector to read with, and a **data source**
in RAGflow that uses it.

## Prerequisites

- A **Moodle** site (admin access to create a web service + token).
- A **RAGflow** instance with the Moodle connector (it ships with RAGflow).
- A **user account** in Moodle that is **enrolled in the courses you want to sync**. The connector sees
  exactly what this user sees — no more, no less.

## 1. Enable web services in Moodle

*Site administration → Advanced features* → enable **Enable web services**. Then
*Site administration → Server → Web services → Manage protocols* → enable **REST**.

## 2. The web-service token

Create a token that can read course contents and download files.

1. Define (or reuse) an **external service** that exposes the functions the connector calls:
   *Site administration → Server → Web services → External services* → add a service, then add these
   functions to it:
       - `core_webservice_get_site_info`
       - `core_course_get_courses`
       - `core_course_get_contents`
       - `mod_forum_get_forum_discussions`
2. Create the token: *Site administration → Server → Web services → Manage tokens* → **Create token** for
   the intended **user** on that **service**.

<!-- shot:connector-03 -->

!!! warning "The token acts as its user"
    The connector reads with this user's permissions and only sees the user's **enrolled courses**. Give it
    a dedicated account enrolled (e.g. as a non-editing teacher) in the courses to index, and the capability
    to **download course files**. Treat the token like a password — see [Security &amp;
    permissions](security.md).

!!! tip "Base URL"
    Use the site's base URL only — e.g. `https://moodle.example.edu`. **Do not** include `/webservice`,
    `/login` or a trailing path; the connector adds `/webservice/rest/server.php` itself.

## 3. Add the data source in RAGflow

In RAGflow, open *User settings → Data sources*, add a **Moodle** source and fill in:

<!-- shot:connector-02 -->

| Field | Value |
|---|---|
| **Instance URL** | The Moodle base URL (e.g. `https://moodle.example.edu`). |
| **Token** | The web-service token from step 2. |

RAGflow validates the token immediately (it calls `core_webservice_get_site_info`); a bad token or missing
web-service permissions are reported here — see [Troubleshooting](troubleshooting.md).

## 4. Bind it to a knowledge base and sync

Attach the data source to the **knowledge base** that should hold the Moodle content, then run the first
**sync**. The initial run is a **full load** of all enrolled courses; after that RAGflow syncs
**incrementally** and removes documents for items deleted in Moodle (**sync deleted files** is on for this
connector). See [Sync behaviour](sync-behaviour.md) for the details and scheduling.

Once the knowledge base has parsed content, any RAGflow assistant can use it — and, if you run the Moodle
plugins, so can they (see [Using it with the Moodle RAGflow Suite](moodle-suite.md)).
