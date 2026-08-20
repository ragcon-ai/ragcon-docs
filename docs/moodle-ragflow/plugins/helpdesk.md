# Helpdesk placement

**Component:** `aiplacement_ragflowhelpdesk` · **Requires:** Moodle 5.0–5.2 · **Depends on:** `aiprovider_ragflow`

A site-wide **help drawer** (an AI *placement*) that answers from a central knowledge base — typically
your organisation's help/FAQ/support content. It appears across the site for users who may use it.

## Features

- Site-wide chat drawer driven by the shared provider engine (same UI as the tutor).
- Optional **conversation memory** (RAGflow session) so follow-up questions keep context.
- Source citations; answers in the user's Moodle language.

## Setup

1. [Set up RAGflow](../setup-ragflow.md) (provider) first, pointing at your help/FAQ dataset.
2. Enable the placement under **Site administration → General → AI → AI placements**.
3. Grant `aiplacement/ragflowhelpdesk:use` to the roles that should see the drawer.

## Capabilities

| Capability | Default | Purpose |
|---|---|---|
| `aiplacement/ragflowhelpdesk:use` | (configure per site) | See and use the help drawer |
