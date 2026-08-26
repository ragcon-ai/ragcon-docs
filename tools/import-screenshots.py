#!/usr/bin/env python3
"""Import RAGflow suite screenshots from the moodle-marketplace repo into these docs.

Source of truth is ``screenshot-manifest.yml`` in the marketplace checkout. For every shot with
``status: captured-2x`` this script

1. copies ``screenshots-staging/<file>`` -> ``docs/moodle-ragflow/img/<file>`` (filenames kept, so a
   re-captured image is later a one-file replace with no markdown change), and
2. idempotently inserts the image block directly under its ``<!-- shot:<id> -->`` marker in the target
   page, using the manifest's ``alt`` and ``caption`` verbatim and a page-relative image path.

Blocked shots (``blocked-ragflow`` setup-01..06, ``blocked-retired`` search-03) are left untouched -- their
markers stay in place without an image. Re-run any time; already-inserted blocks are skipped.

Usage:  tools/import-screenshots.py [--marketplace PATH] [--dry-run]
"""
import argparse
import os
import shutil
import sys

import yaml

DOCS_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def img_root_for(page):
    """Images live under each product's own tree: docs/<product>/img (product = page's top folder)."""
    product = page.split("/", 1)[0]
    return os.path.join(DOCS_REPO, "docs", product, "img")


def load_manifest(marketplace):
    path = os.path.join(marketplace, "screenshot-manifest.yml")
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def page_file(page):
    return os.path.join(DOCS_REPO, "docs", page)


def insert_block(page, marker_id, rel_img, alt, caption, dry_run):
    """Insert the image block under <!-- shot:marker_id --> if not already there. Returns action str."""
    fpath = page_file(page)
    with open(fpath, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    marker = f"<!-- shot:{marker_id} -->"
    try:
        i = next(n for n, ln in enumerate(lines) if ln.strip() == marker)
    except StopIteration:
        return f"MARKER MISSING in {page}"
    # Already inserted? Look at the next few non-empty lines for an image pointing at this file.
    for ln in lines[i + 1:i + 4]:
        if ln.lstrip().startswith("![") and os.path.basename(rel_img) in ln:
            return "skip (present)"
    block = ["", f"![{alt}]({rel_img})", f"*{caption}*"]
    # Keep a blank line before whatever followed the marker.
    if i + 1 < len(lines) and lines[i + 1].strip() != "":
        block.append("")
    if not dry_run:
        lines[i + 1:i + 1] = block
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
    return "inserted"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--marketplace", default=os.path.expanduser("~/git/ragcon/moodle-marketplace"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = load_manifest(args.marketplace)
    shots = manifest["shots"] if isinstance(manifest, dict) else manifest
    staging = os.path.join(args.marketplace, "screenshots-staging")
    copied = inserted = skipped = 0
    problems = []

    for shot in shots:
        if shot.get("status") != "captured-2x":
            continue
        rel_file = shot["file"]  # e.g. "dashboard/dashboard-01-status-tab.png"
        src = os.path.join(staging, rel_file)
        dst = os.path.join(img_root_for(shot["page"]), rel_file)
        if not os.path.exists(src):
            problems.append(f"SOURCE MISSING: {src}")
            continue
        if not args.dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        copied += 1
        rel_img = os.path.relpath(dst, os.path.dirname(page_file(shot["page"])))
        action = insert_block(
            shot["page"], shot["id"], rel_img, shot["alt"], shot["caption"], args.dry_run
        )
        if action == "inserted":
            inserted += 1
        elif action.startswith("skip"):
            skipped += 1
        else:
            problems.append(action)

    tag = "[dry-run] " if args.dry_run else ""
    print(f"{tag}copied {copied} image(s); inserted {inserted} block(s); {skipped} already present.")
    for p in problems:
        print("  !", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
