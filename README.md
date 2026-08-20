# RAGcon Documentation

Source for the RAGcon documentation site, built with [MkDocs](https://www.mkdocs.org/) +
[Material](https://squidfunk.github.io/mkdocs-material/) and published to GitHub Pages.

**Live site:** https://docs.ragcon.ai/

## Structure

Each RAGcon product is a top-level folder under `docs/` and a nav block in `mkdocs.yml`:

```
docs/
├─ index.md               # RAGcon docs home
└─ moodle-ragflow/        # section 1: the Moodle RAGflow plugin suite
   ├─ index.md
   ├─ setup-ragflow.md    # shared setup (done once)
   ├─ plugins/*.md        # one page per plugin
   └─ user-guide.md
```

Add a new product by creating `docs/<product>/…` and a nav block. See below for how builds stay
scoped as the repo grows.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve      # http://127.0.0.1:8000
mkdocs build --strict
```

## Publishing

`.github/workflows/deploy.yml` builds the site and deploys it to GitHub Pages on every push to
`main` that touches documentation (`paths:` filter on `docs/**`, `mkdocs.yml`, `requirements.txt`).
Enable Pages once under **Settings → Pages → Source: GitHub Actions**.

### Keeping builds scoped per section

The path filter already means non-doc changes don't rebuild. As more products/teams are added and
want fully independent pipelines, either:

- split `deploy.yml` into per-section, path-filtered jobs, or
- move a product's docs into its own repo and trigger a rebuild here via `repository_dispatch`
  (the [multirepo](https://github.com/jimporter/mike) growth path — same Markdown, no rewrite).
