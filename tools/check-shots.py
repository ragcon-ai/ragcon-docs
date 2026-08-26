#!/usr/bin/env python3
"""Verify the screenshots are wired into the docs consistently with the manifest.

Checks (exit non-zero on any failure; suitable for CI):

1. Every ``<!-- shot:<id> -->`` marker in ``docs/**/*.md`` has a manifest entry, and every manifest shot
   has a marker -- except ``status: blocked-retired`` shots, which are withdrawn and must NOT have a marker.
2. Every ``captured-2x`` marker is directly followed by an image block whose file exists on disk.
3. The image path in the markdown equals the page-relative path to the manifest ``file``.
4. Alt text and caption match the manifest verbatim.
5. The markers without an image are exactly the ``blocked-ragflow`` shots (the RAGflow-UI setup shots).

Usage:  tools/check-shots.py [--marketplace PATH]
"""
import argparse
import glob
import os
import re
import sys

import yaml

DOCS_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(DOCS_REPO, "docs")
IMG_ROOT = os.path.join(DOCS_DIR, "moodle-ragflow", "img")
MARKER_RE = re.compile(r"<!--\s*shot:(\S+)\s*-->")
IMG_RE = re.compile(r"^!\[(?P<alt>.*)\]\((?P<path>[^)]+)\)\s*$")


def load_shots(marketplace):
    with open(os.path.join(marketplace, "screenshot-manifest.yml"), encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    shots = data["shots"] if isinstance(data, dict) else data
    return {s["id"]: s for s in shots}


def find_markers():
    """Return {shot_id: (relpath, lineno, lines)} for every marker in the docs."""
    out = {}
    for path in glob.glob(os.path.join(DOCS_DIR, "**", "*.md"), recursive=True):
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        for n, line in enumerate(lines):
            m = MARKER_RE.search(line)
            if m and line.strip().startswith("<!--"):
                out[m.group(1)] = (os.path.relpath(path, DOCS_REPO), n, lines, path)
    return out


def image_below(lines, marker_line):
    """Return (alt, path, caption) for the image block under the marker, or None."""
    for i in range(marker_line + 1, min(marker_line + 5, len(lines))):
        stripped = lines[i].strip()
        if stripped == "":
            continue
        if MARKER_RE.search(stripped):
            return None  # next marker -> this marker has no image of its own
        m = IMG_RE.match(lines[i])
        if m:
            caption = ""
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("*"):
                caption = lines[i + 1].strip().strip("*")
            return m.group("alt"), m.group("path"), caption
        return None  # other content first -> no image block
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--marketplace", default=os.path.expanduser("~/git/ragcon/moodle-marketplace"))
    args = ap.parse_args()

    shots = load_shots(args.marketplace)
    markers = find_markers()
    errors = []
    missing_image = []

    # 1a. Every marker has a manifest entry.
    for sid in markers:
        if sid not in shots:
            errors.append(f"marker shot:{sid} has no manifest entry")
    # 1b. Every non-retired manifest shot has a marker; retired shots must have none.
    for sid, shot in shots.items():
        retired = shot.get("status") == "blocked-retired"
        if retired and sid in markers:
            errors.append(f"retired shot {sid} still has a marker in {markers[sid][0]}")
        if not retired and sid not in markers:
            errors.append(f"manifest shot {sid} ({shot.get('status')}) has no marker in the docs")

    for sid, (rel, lineno, lines, abspath) in markers.items():
        shot = shots.get(sid)
        if not shot:
            continue
        status = shot.get("status")
        block = image_below(lines, lineno)
        if status == "captured-2x":
            if not block:
                errors.append(f"{sid}: captured-2x but no image block under the marker ({rel})")
                continue
            alt, path, caption = block
            # 2. file exists
            img_abs = os.path.normpath(os.path.join(os.path.dirname(abspath), path))
            if not os.path.exists(img_abs):
                errors.append(f"{sid}: image file missing: {path} ({rel})")
            # 3. path matches manifest 'file'
            expected = os.path.relpath(os.path.join(IMG_ROOT, shot["file"]), os.path.dirname(abspath))
            if path != expected:
                errors.append(f"{sid}: image path '{path}' != expected '{expected}' ({rel})")
            # 4. alt + caption verbatim
            if alt != shot["alt"]:
                errors.append(f"{sid}: alt mismatch\n     doc: {alt}\n     man: {shot['alt']}")
            if caption != shot["caption"]:
                errors.append(f"{sid}: caption mismatch\n     doc: {caption}\n     man: {shot['caption']}")
        else:
            # Not-yet-captured markers (blocked-ragflow, todo) are present but must have NO image yet.
            if block:
                errors.append(f"{sid}: {status} marker unexpectedly has an image block ({rel})")
            else:
                missing_image.append(sid)

    # 5. markers without an image are exactly the not-yet-captured shots (blocked-ragflow + todo).
    expected_no_image = sorted(
        sid for sid, s in shots.items() if s.get("status") in ("blocked-ragflow", "todo")
    )
    if sorted(missing_image) != expected_no_image:
        errors.append(
            "markers without an image differ from the not-yet-captured set:\n"
            f"     have: {sorted(missing_image)}\n"
            f"     want: {expected_no_image}"
        )

    captured = sum(1 for s in shots.values() if s.get("status") == "captured-2x")
    if errors:
        print(f"FAIL — {len(errors)} problem(s):")
        for e in errors:
            print("  -", e)
        return 1
    print(
        f"OK — {len(markers)} markers, {captured} images wired, "
        f"{len(expected_no_image)} awaiting capture (setup + dashboard re-work), search-03 retired."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
