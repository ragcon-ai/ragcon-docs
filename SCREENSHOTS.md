# Screenshots — how they are added to these docs

This repo holds the **docs side** of the Moodle RAGflow screenshots. The full plan, the
**manifest** (shot list, IDs, captions, alt text, capture prep) and the marketplace
listing shotlists live in the sibling repo **[ragcon-ai/moodle-marketplace](https://github.com/ragcon-ai/moodle-marketplace)**
(`screenshot-manifest.yml`, `screenshot-plan.md`, `capture-log.md`, `checklist-round-2.md`).

## Where things go

- **Images:** `docs/moodle-ragflow/img/<group>/<group>-<nn>-<slug>.png`
  (groups: `hero`, `setup`, `provider`, `tutor`, `search`, `helpdesk`, `dashboard`, `guides`).
- **Markers:** every target location in the `.md` pages carries a
  `<!-- shot:<id> -->` comment (e.g. `<!-- shot:tutor-03 -->`). The **id** is
  `<group>-<nn>`; it is stable even if the slug is later refined.

## Naming

```
<group>-<nn>-<slug>.png      e.g. tutor-03-answer-with-sources-panel.png
```

No umlauts, no spaces, no dates or version numbers (git handles versioning). Replacing a
screenshot keeps the **same filename**, so the swap is a one-file commit with no Markdown change.

## Embedding a shot

At each `<!-- shot:<id> -->` marker, insert the image and its caption from the manifest:

```markdown
<!-- shot:tutor-03 -->

![<alt from manifest>](../img/tutor/tutor-03-answer-with-sources-panel.png)
*<caption from manifest>*
```

Screenshots are framed automatically (light + dark) via `docs/assets/extra.css`; the caption
is the emphasised line directly under the image. `mkdocs build --strict` fails on a missing
image file, so every embedded shot must have its PNG committed.

## Capture rules (summary — full version in the marketplace plan)

- UI language **English**; Moodle **Boost, light mode**.
- Viewport **1440 × 900**, zoom 100 %, DPR 2 → export ≤ **1600 px** wide, PNG, < 400 KB.
- **Redact:** mask API keys in the DOM before the shot; hosts as `moodle.example.org` /
  `ragflow.example.org`; demo names only (`Alex Trainer`, `Sam Student`); no real documents.
- `crop: element` = just the relevant card/form; `crop: viewport` only when the page context
  is the point.

> The screenshots currently under `screenshots-staging/` in the marketplace repo are a
> **discarded test run** (older plugin UI) and are not used.
