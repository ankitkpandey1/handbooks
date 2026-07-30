#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Shared accessors for books/<slug>/book.json.

Zero third-party dependencies on purpose: this must run on any Python 3.8+ without a
virtualenv, because it is the layer the shell entrypoints and CI both depend on.

Usage as a CLI (used by the bash entrypoints, which cannot parse JSON safely):

    bookmeta.py get <slug> <dotted.key> [default]
    bookmeta.py formats <slug>
    bookmeta.py slugs
    bookmeta.py validate <slug>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOKS = REPO / "books"

SCHEMA = "handbooks/book/v1"
VALID_TIERS = {"A", "B"}
VALID_STATUS = {"draft", "published", "deprecated"}
VALID_FORMATS = {"pdf", "epub", "html", "md"}
REQUIRED = ("schema_version", "slug", "tier", "status", "title", "edition", "canonical_source")


def book_dir(slug: str) -> Path:
    d = BOOKS / slug
    if not (d / "book.json").is_file():
        raise SystemExit(f"error: no book.json for slug '{slug}' (looked in {d})")
    return d


def load(slug: str) -> dict:
    return json.loads((book_dir(slug) / "book.json").read_text(encoding="utf-8"))


def slugs() -> list[str]:
    if not BOOKS.is_dir():
        return []
    return sorted(p.name for p in BOOKS.iterdir() if (p / "book.json").is_file())


def get(meta: dict, dotted: str, default=None):
    cur = meta
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def formats(meta: dict) -> list[str]:
    return get(meta, "build.formats", ["pdf", "epub", "html", "md"])


def validate(slug: str) -> list[str]:
    """Return a list of problems; empty means valid."""
    errors: list[str] = []
    d = book_dir(slug)
    meta = load(slug)

    for key in REQUIRED:
        if not get(meta, key):
            errors.append(f"book.json: missing required key '{key}'")

    if get(meta, "schema_version") != SCHEMA:
        errors.append(f"book.json: schema_version must be '{SCHEMA}'")
    if meta.get("slug") != slug:
        errors.append(f"book.json: slug '{meta.get('slug')}' does not match directory '{slug}'")
    if meta.get("tier") not in VALID_TIERS:
        errors.append(f"book.json: tier must be one of {sorted(VALID_TIERS)}")
    if meta.get("status") not in VALID_STATUS:
        errors.append(f"book.json: status must be one of {sorted(VALID_STATUS)}")

    edition = str(get(meta, "edition", ""))
    if edition and len(edition.split(".")) != 3:
        errors.append(f"book.json: edition '{edition}' is not <major>.<minor>.<patch>")

    bad = set(formats(meta)) - VALID_FORMATS
    if bad:
        errors.append(f"book.json: unknown build.formats {sorted(bad)}")

    src = get(meta, "canonical_source")
    if src and not (d / src).is_file():
        errors.append(f"canonical_source not found: {src}")

    for who in ("prose", "code"):
        if not get(meta, f"licenses.{who}"):
            errors.append(f"book.json: missing licenses.{who}")

    if not get(meta, "authors"):
        errors.append("book.json: at least one author is required")

    # Tier A must declare a verifier entrypoint that exists and is the release gate.
    if meta.get("tier") == "A":
        entry = get(meta, "verify.entrypoint")
        if not entry:
            errors.append("book.json: Tier A requires verify.entrypoint")
        elif not (d / entry).is_file():
            errors.append(f"verify.entrypoint not found: {entry}")
        if not get(meta, "assurance.reproducibility_boundary"):
            errors.append("book.json: Tier A requires assurance.reproducibility_boundary")

    return errors


def _main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]

    if cmd == "slugs":
        print("\n".join(slugs()))
        return 0
    if cmd == "get":
        slug, dotted = rest[0], rest[1]
        default = rest[2] if len(rest) > 2 else ""
        value = get(load(slug), dotted, default)
        if isinstance(value, (list, tuple)):
            print(" ".join(str(v) for v in value))
        elif isinstance(value, bool):
            print("true" if value else "false")
        elif isinstance(value, dict):
            print(json.dumps(value))
        else:
            print(value)
        return 0
    if cmd == "formats":
        print(" ".join(formats(load(rest[0]))))
        return 0
    if cmd == "validate":
        errors = validate(rest[0])
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1 if errors else 0

    print(f"error: unknown command '{cmd}'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
