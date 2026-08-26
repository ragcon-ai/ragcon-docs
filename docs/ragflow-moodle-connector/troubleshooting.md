# Troubleshooting

The connector validates the token when you add the data source and again on every sync, so most problems
surface with a clear cause.

| Symptom | Likely cause | What to check |
|---|---|---|
| *Token is invalid or expired* | The web-service token is wrong, was reset, or the user was disabled | Re-create the token (*Server → Web services → Manage tokens*) and paste the new one into the data source. |
| *Insufficient permissions* / **accessexception** | Web services or the REST protocol are off, or the service is missing functions | Enable **web services** and the **REST** protocol; make sure the service used by the token includes `core_webservice_get_site_info`, `core_course_get_courses`, `core_course_get_contents`, `mod_forum_get_forum_discussions`. |
| **No courses found** / nothing gets indexed | The token user is **not enrolled** in any course | Enrol the token's user in the courses to index (e.g. as a non-editing teacher). Scope follows enrolment. |
| A course syncs but its **files are empty / missing** | The token user can read the course but not **download files** | Ensure the user has the capability to download course files; the connector appends the token to file URLs to fetch them. |
| A **forum** is empty | No discussions, or the user can't see them | Confirm the user can read the forum; empty forums produce no document. |
| **Assignments/Quizzes** have little content | Only the **description** is indexed | This is by design — submissions and questions are never read. |
| Changes in Moodle **don't appear** | Waiting for the next incremental sync, or `timemodified` didn't change | Trigger a sync; for a rebuild run a full **re-index**. Editing content bumps `timemodified`. |
| Deleted items **still appear** | Cleanup runs on the next sync | Run a sync; documents for deleted/unreachable modules are then removed. |
| Wrong base URL error | URL includes `/webservice` or `/login` | Use the **base URL only** (e.g. `https://moodle.example.edu`). |

Still stuck? Check the RAGflow **data-source sync logs** for the knowledge base — they record per-run
status and errors. Because the connector is part of RAGflow, connector bugs belong in the
[RAGflow issue tracker](https://github.com/infiniflow/ragflow/issues).
