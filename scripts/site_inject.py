#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Inject SEO head tags and a small top bar into a book's generic HTML build.

Used by scripts/build-site.sh. Takes the self-contained HTML5 file that
`scripts/build-book.sh <slug> html` produces and layers on:

  - <meta name="description">, a canonical link, Open Graph, a Twitter card, robots
  - a JSON-LD Book object
  - a small, unobtrusive top bar (inline CSS, no external assets) linking back to the
    catalogue and to the PDF/EPUB downloads

Everything injected is derived from books/<slug>/book.json; nothing here is hand-written
per book.

    site_inject.py --slug <slug> --in <path> --out <path>
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookmeta  # noqa: E402

OWNER_REPO = "ankitkpandey1/handbooks"
SITE = "https://ankitkpandey1.github.io/handbooks/"
RELEASES = f"https://github.com/{OWNER_REPO}/releases"
AUTHOR_NAME = "Ankit Kumar Pandey"

LICENSE_URLS = {
    "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/",
    "Apache-2.0": "https://www.apache.org/licenses/LICENSE-2.0",
}


def read_online_url(slug: str) -> str:
    return f"{SITE}books/{slug}/"


def latest_asset(slug: str, ext: str) -> str:
    return f"{RELEASES}/latest/download/{slug}.{ext}"


def book_jsonld(slug: str, meta: dict) -> dict:
    url = read_online_url(slug)
    book: dict = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": meta["title"],
        "description": meta.get("description", ""),
        "author": {"@type": "Person", "name": AUTHOR_NAME},
        "bookEdition": meta.get("edition", ""),
        "url": url,
    }
    if meta.get("subtitle"):
        book["alternateName"] = meta["subtitle"]
    if meta.get("language"):
        book["inLanguage"] = meta["language"]
    if meta.get("date"):
        book["datePublished"] = meta["date"]
    license_url = LICENSE_URLS.get(meta.get("licenses", {}).get("prose", ""))
    if license_url:
        book["license"] = license_url
    work_examples = []
    for fmt, encoding in (("pdf", "application/pdf"), ("epub", "application/epub+zip")):
        work_examples.append(
            {"@type": "Book", "encodingFormat": encoding, "url": latest_asset(slug, fmt)}
        )
    book["workExample"] = work_examples
    return book


def build_head_extra(slug: str, meta: dict, existing_head: str) -> str:
    e = html.escape
    title = meta["title"]
    subtitle = meta.get("subtitle", "")
    desc = meta.get("description", "")
    url = read_online_url(slug)
    full_title = f"{title} — {subtitle}" if subtitle else title

    jsonld_str = json.dumps(
        book_jsonld(slug, meta), indent=2, ensure_ascii=False
    ).replace("</", "<\\/")

    parts = [
        f'<meta name="description" content="{e(desc)}">',
        f'<link rel="canonical" href="{e(url)}">',
        '<meta name="robots" content="index,follow">',
        '<meta property="og:type" content="book">',
        f'<meta property="og:title" content="{e(full_title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{e(url)}">',
        '<meta property="og:site_name" content="Handbooks">',
        '<meta name="twitter:card" content="summary">',
    ]
    if not re.search(r'<meta\s+name=["\']author["\']', existing_head, re.I):
        parts.append(f'<meta name="author" content="{e(AUTHOR_NAME)}">')
    parts.append(f'<script type="application/ld+json">{jsonld_str}</script>')
    return "\n".join(parts)


TOPBAR_CSS = (
    '#hb-topbar{font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,'
    "Arial,sans-serif;background:#12222e;color:#e6edf3;padding:.6rem 1rem;display:flex;"
    "flex-wrap:wrap;gap:.4rem 1rem;align-items:center}"
    "#hb-topbar a{color:#e6edf3;text-decoration:none;opacity:.85}"
    "#hb-topbar a:hover{opacity:1;text-decoration:underline}"
    "#hb-topbar .hb-sep{opacity:.4}"
    "#hb-topbar .hb-title{font-weight:600;opacity:1;margin-right:.5rem}"
)


def build_topbar(slug: str, meta: dict) -> str:
    e = html.escape
    pdf = latest_asset(slug, "pdf")
    epub = latest_asset(slug, "epub")
    return (
        f"<style>{TOPBAR_CSS}</style>"
        '<div id="hb-topbar">'
        f'<span class="hb-title">{e(meta["title"])}</span>'
        f'<a href="{e(SITE)}">&larr; Handbooks catalogue</a>'
        '<span class="hb-sep">&middot;</span>'
        f'<a href="{e(pdf)}">Download PDF</a>'
        '<span class="hb-sep">&middot;</span>'
        f'<a href="{e(epub)}">Download EPUB</a>'
        "</div>"
    )


def inject(html_text: str, slug: str, meta: dict) -> str:
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html_text, re.S | re.I)
    if not head_match:
        raise SystemExit("error: input HTML has no <head>...</head>; is this pandoc standalone output?")
    existing_head = head_match.group(1)

    head_extra = build_head_extra(slug, meta, existing_head)
    html_text = html_text.replace("</head>", head_extra + "\n</head>", 1)

    body_match = re.search(r"<body[^>]*>", html_text, re.I)
    if not body_match:
        raise SystemExit("error: input HTML has no <body>; is this pandoc standalone output?")
    topbar = build_topbar(slug, meta)
    insert_at = body_match.end()
    html_text = html_text[:insert_at] + topbar + html_text[insert_at:]
    return html_text


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--in", dest="inp", required=True, type=Path)
    ap.add_argument("--out", dest="outp", required=True, type=Path)
    args = ap.parse_args(argv)

    meta = bookmeta.load(args.slug)
    src = args.inp.read_text(encoding="utf-8")
    out = inject(src, args.slug, meta)
    args.outp.parent.mkdir(parents=True, exist_ok=True)
    args.outp.write_text(out, encoding="utf-8")
    print(f"injected SEO head + top bar for {args.slug} -> {args.outp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
