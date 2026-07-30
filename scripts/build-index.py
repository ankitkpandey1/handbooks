#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Regenerate the discovery surface from the books' own metadata.

Writes, all derived and never hand-edited:

    books.json          machine-readable catalogue — one fetch tells an agent everything
    docs/index.html     the human catalogue (GitHub Pages landing page)
    docs/llms.txt       agent-oriented pointer file
    docs/index.md       plain-text catalogue, for anything that would rather read Markdown

Everything comes from books/<slug>/book.json plus the manuscript outline, so the metadata
has exactly one home. Deterministic output: no timestamps, no network, so re-running on an
unchanged tree produces a byte-identical result and CI can assert the catalogue is current.

    scripts/build-index.py [--check]

--check exits non-zero if anything would change instead of writing.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookmeta  # noqa: E402

REPO = bookmeta.REPO
DOCS = REPO / "docs"
OWNER_REPO = "ankitkpandey1/handbooks"
SITE = "https://ankitkpandey1.github.io/handbooks/"
RELEASES = f"https://github.com/{OWNER_REPO}/releases"

TIER_BLURB = {
    "A": "Published PDF is cryptographically bound to the exact source that produced it. "
         "Ships a source-contract manifest, reproducibility package, external build receipt, "
         "and a verifier suite you can run offline.",
    "B": "Manuscript plus metadata, structurally linted and built to all four formats by CI. "
         "A real book with a lighter guarantee.",
}
FORMAT_PURPOSE = {
    "pdf": "reading",
    "epub": "e-readers",
    "html": "the web",
    "md": "agents and LLMs",
}


OUTLINE_LIMIT = 60


def outline(book_dir: Path, meta: dict, limit: int = OUTLINE_LIMIT) -> tuple[list[dict], int]:
    """Top-level structure of the manuscript, for the catalogue and for agents.

    Returns (items, total_headings). Items may be truncated at `limit`; the total is always
    reported so a consumer can tell the outline is partial rather than assuming it is whole.
    """
    src = book_dir / meta["canonical_source"]
    if not src.is_file():
        return [], 0
    text = src.read_text(encoding="utf-8")
    # Reuse the linter's fence-aware stripper so code comments never masquerade as headings.
    import importlib.util

    spec = importlib.util.spec_from_file_location("lintbook", REPO / "scripts" / "lint-book.py")
    lint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lint)
    _, body = lint.split_front_matter(text)
    prose = lint.scan_fences(body)[0]

    items: list[dict] = []
    total = 0
    for hashes, title in re.findall(r"^(#{1,2})\s+(.+)$", prose, re.MULTILINE):
        clean = re.sub(r"\s+", " ", title).strip()
        clean = re.sub(r"\\[A-Za-z]+\{?|\}", "", clean).strip()
        if not clean:
            continue
        total += 1
        if len(items) < limit:
            items.append({"level": len(hashes), "title": clean})
    return items, total


def latest_asset(slug: str, ext: str) -> str:
    return f"{RELEASES}/latest/download/{slug}.{ext}"


def collect() -> dict:
    books = []
    for slug in bookmeta.slugs():
        problems = bookmeta.validate(slug)
        if problems:
            print(f"error: books/{slug}/book.json is invalid:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            raise SystemExit(1)

        meta = bookmeta.load(slug)
        d = bookmeta.book_dir(slug)
        formats = bookmeta.formats(meta)
        edition = meta["edition"]
        items, heading_total = outline(d, meta)

        books.append(
            {
                "slug": slug,
                "title": meta["title"],
                "subtitle": meta.get("subtitle", ""),
                "description": meta.get("description", ""),
                "tier": meta["tier"],
                "status": meta["status"],
                "edition": edition,
                "date": meta.get("date", ""),
                "language": meta.get("language", ""),
                "pages": meta.get("pages"),
                "authors": [a.get("name", "") for a in meta.get("authors", [])],
                "keywords": meta.get("keywords", []),
                "licenses": meta.get("licenses", {}),
                "source_path": f"books/{slug}",
                "canonical_source": f"books/{slug}/{meta['canonical_source']}",
                "release_tag": f"{slug}/v{edition}",
                "release_page": f"{RELEASES}/tag/{slug}/v{edition}",
                "downloads": {fmt: latest_asset(slug, fmt) for fmt in formats},
                "checksums": f"{RELEASES}/latest/download/SHA256SUMS.txt",
                "verify": {
                    "attestation": f"gh attestation verify {slug}.pdf --repo {OWNER_REPO}",
                    "full": f"scripts/verify-book.sh {slug}",
                    "verifier_count": bookmeta.get(meta, "assurance.verifier_count"),
                },
                "assurance": meta.get("assurance", {}),
                "outline": items,
                "outline_headings_total": heading_total,
                "outline_truncated": heading_total > len(items),
            }
        )

    return {
        "schema_version": "handbooks/catalogue/v1",
        "repository": f"https://github.com/{OWNER_REPO}",
        "site": SITE,
        "tiers": TIER_BLURB,
        "note": (
            "Generated by scripts/build-index.py from each book's book.json. Do not hand-edit. "
            "Download links always resolve to the newest published edition."
        ),
        "book_count": len(books),
        "books": books,
    }


# --------------------------------------------------------------------------------------
# renderers
# --------------------------------------------------------------------------------------

CSS = """
:root{--fg:#12222e;--muted:#5b6b78;--bg:#fff;--card:#f6f8fb;--line:#dfe6ee;--accent:#123456;--accentfg:#fff}
@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--muted:#9aa8b5;--bg:#0d1117;--card:#161b22;--line:#293341;--accent:#7aa7d4;--accentfg:#0d1117}}
*{box-sizing:border-box}
body{margin:0;padding:2.5rem 1.25rem 4rem;background:var(--bg);color:var(--fg);
 font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:56rem;margin:0 auto}
h1{font-size:2rem;letter-spacing:-.02em;margin:0 0 .35rem}
.tag{color:var(--muted);margin:0 0 2rem;font-size:1.05rem}
.book{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.4rem 1.5rem;margin:0 0 1.25rem}
.book h2{font-size:1.3rem;margin:0 0 .2rem}
.book h2 a{color:inherit;text-decoration:none}
.book h2 a:hover{text-decoration:underline}
.sub{color:var(--muted);margin:0 0 .9rem}
.meta{display:flex;flex-wrap:wrap;gap:.45rem;margin:0 0 1rem;font-size:.8rem}
.chip{background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:.15rem .6rem;color:var(--muted)}
.chip.tier{background:var(--accent);color:var(--accentfg);border-color:var(--accent);font-weight:600}
.dl{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 1rem}
.dl a{display:inline-block;padding:.4rem .8rem;border:1px solid var(--line);border-radius:8px;
 background:var(--bg);color:var(--fg);text-decoration:none;font-size:.88rem}
.dl a:hover{border-color:var(--accent)}
.dl a b{font-weight:600}
.dl a i{font-style:normal;color:var(--muted);font-size:.8rem}
details{font-size:.9rem;color:var(--muted)}
details summary{cursor:pointer;color:var(--fg)}
details ol{margin:.6rem 0 0;padding-left:1.3rem}
details li.l1{font-weight:600;color:var(--fg);margin-top:.4rem}
pre{overflow-x:auto;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:.7rem .9rem;font-size:.82rem}
table{border-collapse:collapse;width:100%;font-size:.9rem;display:block;overflow-x:auto}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--line)}
footer{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--line);color:var(--muted);font-size:.88rem}
a{color:var(--accent)}
"""


def render_html(cat: dict) -> str:
    e = html.escape
    out = [
        "<!-- Generated by scripts/build-index.py. Do not hand-edit. -->",
        '<!doctype html><html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>Handbooks</title>",
        '<meta name="description" content="Short technical handbooks with full source, '
        'reproducible builds and verifiable releases.">',
        f"<style>{CSS}</style></head><body><div class='wrap'>",
        "<h1>Handbooks</h1>",
        "<p class='tag'>Short technical handbooks, with the full source and the tooling that "
        "built them. For people, and for the agents people delegate reading to.</p>",
    ]

    for b in cat["books"]:
        out.append("<article class='book'>")
        out.append(
            f"<h2><a href=\"https://github.com/{OWNER_REPO}/tree/main/{e(b['source_path'])}\">"
            f"{e(b['title'])}</a></h2>"
        )
        if b["subtitle"]:
            out.append(f"<p class='sub'>{e(b['subtitle'])}</p>")

        chips = [f"<span class='chip tier'>Tier {e(b['tier'])}</span>",
                 f"<span class='chip'>Edition {e(b['edition'])}</span>"]
        if b.get("pages"):
            chips.append(f"<span class='chip'>{b['pages']} pp.</span>")
        if b.get("status") != "published":
            chips.append(f"<span class='chip'>{e(b['status'])}</span>")
        if b["licenses"].get("prose"):
            chips.append(f"<span class='chip'>{e(b['licenses']['prose'])}</span>")
        out.append(f"<div class='meta'>{''.join(chips)}</div>")

        if b["description"]:
            out.append(f"<p>{e(b['description'])}</p>")

        links = "".join(
            f"<a href=\"{e(url)}\"><b>{fmt.upper()}</b> <i>{FORMAT_PURPOSE.get(fmt, '')}</i></a>"
            for fmt, url in b["downloads"].items()
        )
        out.append(f"<div class='dl'>{links}</div>")

        out.append(
            "<details><summary>Verify this download</summary>"
            f"<pre>{e(b['verify']['attestation'])}\nsha256sum -c SHA256SUMS.txt</pre>"
            f"<p>Assurance: {e(TIER_BLURB.get(b['tier'], ''))}</p>"
        )
        boundary = b.get("assurance", {}).get("reproducibility_boundary")
        if boundary:
            out.append(f"<p><b>Reproducibility boundary.</b> {e(boundary)}</p>")
        out.append("</details>")

        if b["outline"]:
            items = "".join(
                f"<li class='l{i['level']}'>{e(i['title'])}</li>" for i in b["outline"]
            )
            more = ""
            if b.get("outline_truncated"):
                shown, total = len(b["outline"]), b["outline_headings_total"]
                more = (
                    f"<p>Showing {shown} of {total} sections — "
                    f"<a href=\"{e(b['downloads'].get('md', ''))}\">read the full text</a>.</p>"
                )
            out.append(
                f"<details><summary>Contents</summary><ol>{items}</ol>{more}</details>"
            )

        out.append("</article>")

    out.append(
        "<footer>"
        f"<p>Machine-readable catalogue: <a href=\"books.json\">books.json</a> · "
        f"agent pointers: <a href=\"llms.txt\">llms.txt</a> · "
        f"source: <a href=\"https://github.com/{OWNER_REPO}\">github.com/{OWNER_REPO}</a></p>"
        "<p>Prose CC-BY-4.0 · code Apache-2.0. Generated from each book's <code>book.json</code>.</p>"
        "</footer></div></body></html>"
    )
    return "\n".join(out) + "\n"


def render_llms_txt(cat: dict) -> str:
    lines = [
        "# Handbooks",
        "",
        "> Short technical handbooks published with full source, reproducible builds and "
        "verifiable releases. Each book ships a single-file Markdown export intended for "
        "direct consumption by language models — prefer it over the PDF.",
        "",
        f"Machine-readable catalogue with digests, outlines and asset URLs: {SITE}books.json",
        "",
        "## Books",
        "",
    ]
    for b in cat["books"]:
        md = b["downloads"].get("md")
        desc = b["subtitle"] or b["description"]
        lines.append(f"- [{b['title']} (Edition {b['edition']}, Tier {b['tier']})]({md}): {desc}")
    lines += [
        "",
        "## Notes for agents",
        "",
        f"- Full catalogue as JSON: [books.json]({SITE}books.json)",
        "- `Tier A` means the published artifact is verifiably bound to its source; "
        "`Tier B` means manuscript plus structural lint only. Do not describe a Tier B book "
        "in Tier A terms.",
        "- Every release asset carries Sigstore-signed SLSA provenance: "
        f"`gh attestation verify <file> --repo {OWNER_REPO}`.",
        "- Prose is CC-BY-4.0, code is Apache-2.0. Attribute the book and edition when quoting.",
        "",
        "## Optional",
        "",
        f"- [Repository]({cat['repository']}): manuscripts, verifiers and build tooling",
        f"- [Releases]({RELEASES}): every edition, every format",
    ]
    return "\n".join(lines) + "\n"


def render_index_md(cat: dict) -> str:
    lines = [
        "<!-- Generated by scripts/build-index.py. Do not hand-edit. -->",
        "# Handbooks",
        "",
        "Short technical handbooks with full source, reproducible builds and verifiable releases.",
        "",
        "| Book | Tier | Edition | Formats |",
        "|---|---|---|---|",
    ]
    for b in cat["books"]:
        fmts = " · ".join(f"[{f.upper()}]({u})" for f, u in b["downloads"].items())
        lines.append(f"| **{b['title']}** | {b['tier']} | {b['edition']} | {fmts} |")
    lines += [
        "",
        "## Tiers",
        "",
    ]
    for tier, blurb in cat["tiers"].items():
        lines.append(f"- **Tier {tier}** — {blurb}")
    lines += [
        "",
        "## Verify any download",
        "",
        "```bash",
        f"gh attestation verify <file> --repo {OWNER_REPO}",
        "sha256sum -c SHA256SUMS.txt",
        "```",
        "",
        f"Machine-readable catalogue: [books.json](books.json) · agent pointers: [llms.txt](llms.txt)",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv
    cat = collect()

    catalogue_json = json.dumps(cat, indent=2, ensure_ascii=False) + "\n"
    targets = {
        # Two copies on purpose: the root one is what a reader of the repo finds, the docs/
        # one is what the Pages site and llms.txt serve over HTTP. Same bytes.
        REPO / "books.json": catalogue_json,
        DOCS / "books.json": catalogue_json,
        DOCS / "index.html": render_html(cat),
        DOCS / "llms.txt": render_llms_txt(cat),
        DOCS / "index.md": render_index_md(cat),
        # Tell Pages not to run Jekyll over this directory.
        DOCS / ".nojekyll": "",
    }

    stale = []
    for path, content in targets.items():
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current != content:
            stale.append(path.relative_to(REPO))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

    if check:
        if stale:
            print("stale (run scripts/build-index.py):", file=sys.stderr)
            for p in stale:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"OK: catalogue current ({cat['book_count']} book(s))")
        return 0

    if stale:
        print(f"wrote {len(stale)} file(s) for {cat['book_count']} book(s):")
        for p in stale:
            print(f"  - {p}")
    else:
        print(f"OK: catalogue already current ({cat['book_count']} book(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
