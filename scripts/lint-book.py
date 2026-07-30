#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Structural lint for any book, Tier A or B.

This is the baseline every book must pass. It deliberately does NOT check prose quality or
factual claims — it checks the things a machine can check and a reader would be misled by:
metadata validity, front-matter presence, heading structure, licence declaration, dead
internal links, and (for Tier A) that the assurance claims in book.json are backed by files
that actually exist.

    lint-book.py <slug> [--strict]

--strict promotes warnings to errors. CI uses --strict on pull requests.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookmeta  # noqa: E402

FRONT_MATTER_REQUIRED = ("title", "author", "lang")
FRONT_MATTER_RECOMMENDED = ("subtitle", "subject", "keywords", "rights", "date", "version")


FENCE = re.compile(r"^\s*(```+|~~~+)\s*(\S*)")
NEGATION = re.compile(
    r"\b(no|not|never|without|lacks?|absent|neither|nor|unlike|"
    r"does ?n[o']t|do ?n[o']t|is ?n[o']t|are ?n[o']t|cannot|can ?n[o']t)\b",
    re.IGNORECASE,
)


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    end = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not end:
        return "", text
    cut = 3 + end.end()
    return text[3 : 3 + end.start()], text[cut:]


def scan_fences(body: str) -> tuple[str, int, int, bool]:
    """Strip fenced code blocks from body.

    Returns (prose_only_body, fence_open_count, openings_without_a_language, unclosed).

    Stripping matters: manuscripts in this repo are full of shell and Python listings whose
    comment lines start with '#', which a naive heading scan reads as an h1. Line numbering
    is preserved by blanking stripped lines rather than deleting them.
    """
    out: list[str] = []
    fence: str | None = None
    opens = 0
    unlabelled = 0
    for line in body.split("\n"):
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                opens += 1
                if not m.group(2):
                    unlabelled += 1
                out.append("")
                continue
            out.append(line)
        else:
            # A closing fence must be at least as long as the opener and carry no info string.
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2):
                fence = None
            out.append("")
    return "\n".join(out), opens, unlabelled, fence is not None


def approved_labels(body: str, section: str) -> list[str]:
    """Pull the approved label set out of the manuscript's own labels section.

    The books declare their evidence and code-authenticity schemes in their own front
    sections, so the linter reads the scheme from the book rather than hard-coding one. A book
    that changes its labelling scheme automatically changes what the linter enforces.
    """
    sec = re.search(rf"^##+ {re.escape(section)}\s*$(.*?)(?=^#)", body, re.S | re.M)
    if not sec:
        return []
    out = []
    for raw in re.findall(r"^\s*[-*]\s+\*\*(.+?)\*\*", sec.group(1), re.M):
        out.append(re.split(r"\s+[-–—]\s+|:", raw)[0].strip())
    return [o for o in out if o]


def code_label_findings(body: str, min_lines: int = 8) -> tuple[list[str], int, int]:
    """Check that substantial code blocks carry an authenticity label.

    The manuscripts assert "every substantial code block uses one of these labels"; this
    verifies the assertion instead of trusting it. A label is any bold lead-in within a few
    lines above the fence — deliberately looser than exact membership of the declared set,
    because legitimate variants exist (e.g. "Tested companion example - executed with ...").
    Membership drift is reported separately and only under --strict.
    """
    lines = body.split("\n")
    keys = [k.lower() for k in approved_labels(body, "Code authenticity labels")]

    fence = None
    start = 0
    blocks: list[tuple[int, int]] = []
    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence, start = m.group(1), i
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2):
            blocks.append((start, i))
            fence = None

    findings: list[str] = []
    substantial = 0
    drift = 0
    for s, e in blocks:
        if e - s - 1 < min_lines:
            continue
        substantial += 1
        window = "\n".join(lines[max(0, s - 8):s])
        bold = re.findall(r"\*\*(.+?)\*\*", window, re.S)
        if not bold:
            findings.append(
                f"code block at manuscript line ~{s + 1} ({e - s - 1} lines) has no "
                f"authenticity label in the 8 lines above it"
            )
        elif keys and not any(k in b.lower() for b in bold for k in keys):
            drift += 1
    return findings, substantial, drift


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    slug = argv[0]
    strict = "--strict" in argv

    errors: list[str] = []
    warnings: list[str] = []

    meta_errors = bookmeta.validate(slug)
    errors.extend(meta_errors)
    if meta_errors:
        # Without valid metadata the rest of the lint has nothing trustworthy to stand on.
        _report(slug, errors, warnings)
        return 1

    meta = bookmeta.load(slug)
    d = bookmeta.book_dir(slug)
    src_path = d / meta["canonical_source"]
    text = src_path.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)

    # --- front matter -----------------------------------------------------------------
    if not fm:
        errors.append("manuscript has no YAML front matter")
    else:
        for key in FRONT_MATTER_REQUIRED:
            if not re.search(rf"^{key}\s*:", fm, re.MULTILINE):
                errors.append(f"front matter: missing required field '{key}'")
        for key in FRONT_MATTER_RECOMMENDED:
            if not re.search(rf"^{key}\s*:", fm, re.MULTILINE):
                warnings.append(f"front matter: missing recommended field '{key}'")

        m = re.search(r"^version\s*:\s*\"?([^\"\n]+)", fm, re.MULTILINE)
        if m and meta["edition"] not in m.group(1):
            errors.append(
                f"front matter version '{m.group(1).strip()}' does not contain "
                f"book.json edition '{meta['edition']}'"
            )

        # The licence stated to the reader must match the licence the repo grants.
        rights = re.search(r"^rights\s*:\s*\"?([^\"\n]+)", fm, re.MULTILINE)
        prose_licence = bookmeta.get(meta, "licenses.prose", "")
        if rights and prose_licence:
            stated = rights.group(1)
            if "all rights reserved" in stated.lower() and prose_licence.startswith("CC-"):
                warnings.append(
                    f"front matter rights says 'All rights reserved' but book.json declares "
                    f"prose licence {prose_licence} — correct this in the next edition"
                )

    prose, fence_opens, unlabelled, unclosed_fence = scan_fences(body)

    # --- heading structure ------------------------------------------------------------
    headings = re.findall(r"^(#{1,6})\s+(.+)$", prose, re.MULTILINE)
    if not headings:
        errors.append("manuscript has no headings")
    else:
        prev = len(headings[0][0])
        for hashes, title in headings:
            level = len(hashes)
            if level > prev + 1:
                errors.append(f"heading level jumps from h{prev} to h{level}: '{title.strip()}'")
            prev = level

        seen: dict[str, int] = {}
        for _, title in headings:
            key = title.strip().lower()
            seen[key] = seen.get(key, 0) + 1
        for key, count in seen.items():
            if count > 1:
                warnings.append(f"duplicate heading appears {count}x: '{key}'")

    # --- fenced code blocks -----------------------------------------------------------
    if unclosed_fence:
        errors.append("a fenced code block is never closed — the manuscript ends inside a fence")
    if unlabelled:
        warnings.append(f"{unlabelled} of {fence_opens} code block(s) open without a language tag")

    # --- internal file links ----------------------------------------------------------
    for target in re.findall(r"\[[^\]]*\]\(\s*<?([^)>\s]+)>?\s*\)", prose):
        if re.match(r"(https?:|mailto:|#|ftp:|doi:)", target):
            continue
        clean = target.split("#")[0]
        if clean and not (d / clean).exists() and not (src_path.parent / clean).exists():
            warnings.append(f"internal link target not found: {clean}")

    # --- the contribution standard: labelled claims and labelled code ------------------
    ev_labels = approved_labels(body, "Scope and evidence labels")
    code_labels = approved_labels(body, "Code authenticity labels")
    if not ev_labels:
        warnings.append(
            "no 'Scope and evidence labels' section found — claims cannot be checked for "
            "labelling. Every book should declare its evidence scheme."
        )
    if not code_labels and fence_opens:
        warnings.append(
            f"{fence_opens} code block(s) but no 'Code authenticity labels' section declaring "
            f"what a label means"
        )

    label_findings, substantial, drift = code_label_findings(body)
    for f in label_findings:
        warnings.append(f)
    if substantial:
        note = f"{substantial - len(label_findings)}/{substantial} substantial code blocks labelled"
        if drift and strict:
            warnings.append(
                f"{note}; {drift} use a label variant outside the declared set "
                f"{code_labels} — confirm the variant is intended"
            )
        print(f"info  [{slug}] {note}", file=sys.stderr)

    # --- tier honesty -----------------------------------------------------------------
    # A Tier B book must not borrow Tier A's vocabulary. Disclaiming the property is fine and
    # in fact encouraged ("this book does NOT carry a reproducibility package"), so only
    # affirmative uses are flagged.
    if meta["tier"] == "B":
        for phrase in ("reproducibility package", "build receipt", "byte-identical",
                       "source-contract manifest", "verifier suite"):
            for sentence in re.split(r"(?<=[.!?])\s+|\n\n", prose):
                if phrase not in sentence.lower():
                    continue
                if NEGATION.search(sentence):
                    continue  # a disclaimer, not a claim
                warnings.append(
                    f"Tier B manuscript claims Tier A property ('{phrase}') — either remove "
                    f"the claim or graduate the book to Tier A: "
                    f"…{sentence.strip()[:90]}…"
                )
                break

    if meta["tier"] == "A":
        entry = d / bookmeta.get(meta, "verify.entrypoint", "")
        if entry.is_file():
            pass
        else:
            errors.append("Tier A verify.entrypoint is missing")
        for asset in bookmeta.get(meta, "release.extra_assets", []):
            if not (d / asset).exists():
                errors.append(f"declared release asset missing: {asset}")

    _report(slug, errors, warnings, strict)
    return 1 if errors or (warnings and strict) else 0


def _report(slug: str, errors: list[str], warnings: list[str], strict: bool = False) -> None:
    for w in warnings:
        print(f"warn  [{slug}] {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR [{slug}] {e}", file=sys.stderr)

    if errors:
        print(f"FAIL: {slug} has {len(errors)} error(s)", file=sys.stderr)
    elif warnings and strict:
        print(
            f"FAIL: {slug} has no errors, but --strict makes its {len(warnings)} "
            f"warning(s) fatal",
            file=sys.stderr,
        )
    elif warnings:
        print(f"OK: {slug} passes structural lint ({len(warnings)} warning(s))")
    else:
        print(f"OK: {slug} passes structural lint with no warnings")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
