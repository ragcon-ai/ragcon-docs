# Security & data protection

The RAGflow Moodle suite is built to Moodle's secure-coding standards and reviewed continuously. This
page is a transparency summary of the safeguards that are in place and the checks we run before every
release. It is intentionally written as a **checklist of what we verify and protect against** — it does
not contain any exploit-level detail.

## How we verify

Every plugin in the suite is checked, on each change, by:

- **moodle-plugin-ci** — the same pipeline the Moodle plugins directory uses: `phpcs` (Moodle coding
  standard), `phpmd`, `phpdoc`, `validate`, upgrade `savepoints`, Mustache, and `eslint`/`stylelint`,
  running on **Moodle 5.0 and 5.2 × PostgreSQL and MariaDB**.
- **Automated tests** — PHPUnit unit tests and Behat acceptance tests ship with every plugin and run in CI.
- **The Moodle plugin submission guideline checker** — run per plugin (0 blocking findings).
- **Periodic manual security audits** against the Moodle-specific checklist below.

## What we check and the safeguards in place

### Access control & permissions
- Every page and endpoint requires an authenticated session and an **explicit capability check**;
  site-wide administrative functions additionally require site-administrator rights.
- Capabilities are declared with appropriate **risk flags, role archetypes and context levels**, following
  the principle of least privilege.
- Web-service functions **validate the calling context** and enforce their capability before doing any work.

### Input & output handling
- All request input is read through Moodle's **typed parameter API** (`PARAM_*`); the code uses no raw PHP
  superglobals.
- All output is **HTML-escaped** — via Moodle's `s()`/`format_string()` helpers and auto-escaping
  templates — and AI answers are **sanitised server-side** (scripts/dangerous markup removed) everywhere
  they are displayed.
- Database access is **fully parameterised**; no SQL is built by string concatenation.

### Cross-site request forgery (CSRF)
- All state-changing actions run through Moodle's form and web-service framework, which enforces
  **session-key (`sesskey`) tokens**; any custom endpoint additionally requires a valid session key and
  capability.

### File handling & downloads
- Uploaded files pass Moodle's **size limits, antivirus scanning and filename sanitisation**.
- Document downloads use **short-lived, per-user signed tokens** (verified with constant-time comparison) or **context-authorised** links;
  content types are restricted and served as attachments with `nosniff`; a user can only reach documents
  that belong to the knowledge base their instance is actually configured for.

### Secrets & the external service
- The RAGflow **API key is stored server-side only**. It is never sent to the browser and never written to
  any log — the optional troubleshooting log records request/response bodies only, never credentials.
- Outbound calls go through Moodle's HTTP client to the **administrator-configured** RAGflow endpoint.

### Safe deserialisation & code execution
- Stored configuration is deserialised with a **strict allow-list** (plain data objects only); no
  untrusted input is ever deserialised.
- There is **no dynamic code execution** (no `eval`, no shell calls) — verified automatically.

### Abuse protection
- Chat requests are **rate-limited per user**.

### Privacy & data protection (GDPR)
- Every plugin implements Moodle's **Privacy API**. Locally stored data is **exportable and deletable per
  user**; data transmitted to the external RAGflow service (prompts, uploaded documents and their
  provenance) is **declared in Moodle's privacy registry**; and user deletion removes local records **and
  forgets the user's RAGflow memory**.
- The usage dashboard offers an **anonymisation** option and an automatic **retention/purge** task; its
  optional raw request/response capture is off by default and admin-only.

### AI-specific handling
- Model output is treated as **untrusted**: sanitised before storage or display and **never executed**.
  Source citations link only to validated URLs.

## Recommendations for administrators

- The Helpdesk chat is available to authenticated users by default — review your site's self-registration
  settings so the audience matches your intent.
- Enable the dashboard's raw API-call capture only while troubleshooting, and turn it off afterwards;
  anonymisation applies to newly captured rows.
- Configure the RAGflow endpoint over **HTTPS** to a trusted host.

## Reporting a security concern

If you believe you have found a security issue in any of these plugins, please report it **privately** to
**info@ragcon.ai** rather than opening a public issue, and do not include exploit details in public
channels. We will acknowledge and address verified reports promptly.
