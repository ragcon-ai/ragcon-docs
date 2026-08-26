# Documentation writing style

The goal is that our docs read like Moodle's own user documentation: plain, direct and human.
This guide records the style of <https://docs.moodle.org> (analysed on the Quiz settings, Blocks and
AI subsystem pages) so we can write and maintain our pages in the same voice.

## The voice in one line

Short, plain sentences in the present tense. Say what a thing **is** and what it **does**, then how
to use it. No cleverness, no marketing, no jargon.

## 1. Person & voice

- **Describe features in plain third person, present tense:** "The Tutor block adds a chat drawer to a
  course page."
- **Write instructions and settings to the reader with "you" and the imperative:** "Choose an
  assistant.", "You can restrict results to the current course."
- Do not use a marketing "we"/"our" in feature text. Address the reader, or state the fact.
- Prefer the active voice ("The provider signs the link") over the passive ("The link is signed").

## 2. Tense

- Present simple for how things work. Use "will" only for a future outcome: "students will not be able
  to start a new attempt."

## 3. Sentences

- **One idea per sentence.** Aim for 12–20 words. If a sentence needs three commas or two dashes,
  split it.
- **Avoid em-dash sandwiches and stacked parentheses.** At most one aside per sentence.
- Cut nominalisations — use the verb. "configures" not "performs configuration of".

## 4. Describing a setting

Pattern: **condition + effect**, or **setting + plain verb + outcome**.

- "If enabled, the block owns the knowledge base and you manage its documents here."
- "**Download link lifetime** sets how long a signed download link stays valid."

## 5. Describing a feature

Pattern: **X is / does Y**, then the detail.

- "The Helpdesk is a site-wide help drawer. It answers from your organisation's knowledge base."

## 6. Terminology & capitalisation

- **Capitalise** Moodle feature and UI names and defined role labels: Course, Block drawer, Site
  administration, the Manager role.
- **Lowercase** generic roles in running prose: teachers, students, managers. Capitalise only when you
  name the specific Moodle role or label ("grant it to the Teacher role").
- Product terms: **RAGcon** (small c), **RAGflow**, **Moodle**. Frankenstyle component names in `code`.

## 7. Spelling & mechanics

- **British English:** organise, customise, authorise, behaviour, colour, licence (noun) / license
  (verb). (Our pages already lean British — keep it consistent.)
- **No contractions:** write "do not", "cannot", "will not".
- Sentence case for headings. Settings go in tables; procedures as numbered steps.

## 8. Notes, tips, warnings

- Use admonitions (`!!! note`, `!!! warning`) **sparingly**, for a genuine exception or caveat. Do not
  wrap ordinary content in a box.

## 9. Words and phrases to avoid → use instead

The clean-up list. The left column is the "AI-ish" tone we want out of our docs (all taken from our
current pages); the right column is the plain replacement.

| Avoid | Use instead |
|---|---|
| surfaces / a surface / it surfaces X | shows, displays, lists; a feature / an area |
| grounded in | based on, using |
| powers / drives (the plugins) | provides, runs; is the backend for |
| wires / wire the knowledge base | sets up / connects the knowledge base |
| seeds a provenance README | adds a small README |
| minted at click time | created when you click |
| a robust completion path | reliable requests (a timeout and one retry) |
| belt-and-braces | as an extra safeguard |
| curated (release notes) | written, selected |
| headroom / a cliff / the tail | spare version numbers / a sharp drop / the last few |
| leverage, utilise | use |
| seamless, powerful, robust, rich (as praise) | drop it, or state the concrete fact |
| under the hood | internally |
| em-dash — with a second clause — mid-sentence | two sentences |

## 10. Before / after (from our own pages)

- **Before:** "…answers students' questions grounded in a RAGflow knowledge base scoped to that course."
  **After:** "…answers students' questions using a RAGflow knowledge base for that course."
- **Before:** "It powers the Tutor, Helpdesk and Search plugins."
  **After:** "The Tutor, Helpdesk and Search plugins use it as their backend."
- **Before:** "a short-lived signed proxy link (minted at click time)."
  **After:** "a short-lived signed download link, created when you click."

## How to apply

When writing or editing a page: draft the fact, then read it aloud. If a phrase would sound odd spoken
to a colleague, replace it with the plain word. Run the list in section 9 over any new text.
