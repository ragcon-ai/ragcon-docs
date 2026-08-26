# Security &amp; permissions

## The token defines the scope

The connector reads Moodle **as the token's user**. It can see exactly what that user can see — the user's
**enrolled courses** and the material in them — and nothing else. Choosing the right account is therefore
the main access-control decision:

- Use a **dedicated service account**, not a real person's login. Enrol it (e.g. as a **non-editing
  teacher**) in exactly the courses whose content should be searchable, and no others.
- Removing the account from a course, or disabling the account, stops new syncs and removes its documents
  on the next run.
- The account needs to **read course contents** and **download course files**; it does **not** need
  editing or admin rights.

## Treat the token like a password

A web-service token is a long-lived credential that grants that user's access. Store it only in the
RAGflow data source; rotate it if it may have leaked (*Manage tokens* → delete and re-create), and the data
source keeps working once you paste the new one.

## What data leaves Moodle

The connector copies the **content** it indexes (files, page/book/forum text, activity descriptions) and
its **metadata** (course, section, module, timestamps, and — for forums — discussion authors) into the
RAGflow knowledge base. Consider this when indexing courses with personal data:

- **Forum** documents include discussion titles and the **author name/id** of each discussion.
- **Files** are copied verbatim into RAGflow; anything inside them (including personal data) goes too.
- It does **not** copy student submissions, grades, quiz responses or private messages.

Once in RAGflow, the material is subject to RAGflow's own access controls and to whatever assistants or
plugins are pointed at that knowledge base — so scope the knowledge base and its consumers accordingly.

## Data protection checklist

- Index only courses you are cleared to make searchable.
- Prefer a **dedicated, least-privilege** service account.
- Be deliberate about **forums** (author names) and **files** (embedded personal data).
- Restrict who can query the resulting knowledge base in RAGflow.

The connector is open-source and part of RAGflow; its behaviour can be audited in the
[RAGflow repository](https://github.com/infiniflow/ragflow).
