# User guide

Day-to-day use of the Moodle RAGflow Suite, once an administrator has [set it up](setup-ragflow.md).

## Asking the tutor (in a course)

1. Open the course page where the **RAGflow Tutor** block is shown.
2. Type your question in the drawer and send.
3. The answer is grounded in the course's uploaded documents; expand **Sources** to open the cited
   files.
4. Follow-up questions keep the topic in context.

!!! tip "Teachers: build the knowledge base"
    In the block's management view, upload the course materials you want the tutor to answer from and
    wait until parsing finishes. The tutor can only answer from documents that are parsed.

## Searching the knowledge base

1. Open a page with the **RAGflow Search** block.
2. Enter a query; results are the most relevant source documents, ranked by relevance.
3. Click a result to open the source file.

## Using the help drawer (helpdesk)

1. Open the help drawer (bottom-right, site-wide) where enabled.
2. Ask your question; answers come from the central help/FAQ knowledge base.
3. With memory enabled, follow-ups keep context within the conversation.

## When something goes wrong

If a chat shows *"Unexpected response from RAGflow"*:

- **Ordinary users:** try again shortly; the service may be temporarily unavailable. Contact your
  administrator if it persists.
- **Administrators / permitted staff:** expand **Details** under the error to see the technical cause
  (e.g. `HTTP 502` = RAGflow unreachable), or open **Reports → RAGflow Dashboard** for recent failures.
