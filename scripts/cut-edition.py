#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Cut a new edition of a Tier A book: the deterministic, text-only half.

A Tier A edition is not a version-string bump. The manuscript's SHA-256 is pinned in three
manifests and the external build receipt, several verifiers hard-code the edition they expect,
and the asset filenames appear in the manuscript body, the bundle scripts and the companion
package. Doing this by hand means missing one and failing the release gate late.

This script performs every change that needs no toolchain. The artifacts that require Pandoc,
XeLaTeX, Ghostscript and PyMuPDF are regenerated afterwards by scripts/regen-edition.sh.

    scripts/cut-edition.py --slug agents-handbook --to 1.8.0 \
        --title "Production Agent Engineering" \
        --source-name production_agent_engineering_edition_1_8.md \
        --asset-prefix Production_Agent_Engineering_Edition_1.8 \
        --date 2026-07-30 --changelog changelog.txt

Nothing here is idempotent by design: it transforms the current edition into the next one, and
refuses to run if the book already declares the target edition.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookmeta  # noqa: E402

MONTHS = ("January February March April May June July August September October November "
          "December").split()


def die(msg: str) -> None:
    raise SystemExit(f"cut-edition: {msg}")


def sub_once(text: str, pattern: str, repl: str, what: str, count: int = 0) -> str:
    """Substitute and assert something actually changed.

    The replacement is applied literally via a function, not as a template: manuscript text is
    full of LaTeX (\\Needspace, \\fancyhead) and re.sub would read those backslashes as escapes.
    """
    new, n = re.subn(pattern, lambda _match: repl, text, count=count, flags=re.M)
    if n == 0:
        die(f"expected to change {what} but pattern did not match: {pattern!r}")
    return new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--to", required=True, help="new edition, e.g. 1.8.0")
    ap.add_argument("--title", help="new book title (omit to keep the current one)")
    ap.add_argument("--subtitle", help="new subtitle (omit to keep)")
    ap.add_argument("--source-name", required=True, help="new canonical manuscript filename")
    ap.add_argument("--asset-prefix", required=True,
                    help="new release asset prefix, e.g. Production_Agent_Engineering_Edition_1.8")
    ap.add_argument("--date", required=True, help="ISO date for the new edition")
    ap.add_argument("--changelog", type=Path, required=True,
                    help="file of '- ' bullet lines for the new changelog entry")
    args = ap.parse_args()

    slug, new_ed = args.slug, args.to
    book = bookmeta.book_dir(slug)
    src_dir = book / "source"
    meta = bookmeta.load(slug)

    if meta["tier"] != "A":
        die(f"{slug} is Tier {meta['tier']}; this script is for Tier A editions")
    old_ed = meta["edition"]
    if old_ed == new_ed:
        die(f"{slug} already declares edition {new_ed}")

    old_src_name = Path(meta["canonical_source"]).name
    old_prefix = Path(bookmeta.get(meta, "release.canonical_pdf", "")).stem
    if not old_prefix:
        die("book.json has no release.canonical_pdf to derive the old asset prefix from")

    new_title = args.title or meta["title"]
    old_title = meta["title"]
    old_ed_short = ".".join(old_ed.split(".")[:2])   # 1.7.0 -> 1.7
    new_ed_short = ".".join(new_ed.split(".")[:2])
    d = datetime.date.fromisoformat(args.date)
    long_date = f"{d.day} {MONTHS[d.month - 1]} {d.year}"

    print(f"==> {slug}: edition {old_ed} -> {new_ed}")
    print(f"    title       : {old_title!r} -> {new_title!r}")
    print(f"    manuscript  : {old_src_name} -> {args.source_name}")
    print(f"    asset prefix: {old_prefix} -> {args.asset_prefix}")

    # ---------------------------------------------------------------- manuscript
    old_src = src_dir / old_src_name
    if not old_src.is_file():
        die(f"canonical source not found: {old_src}")
    text = old_src.read_text(encoding="utf-8")

    if args.title:
        text = sub_once(text, rf'^title:\s*".*?"$', f'title: "{new_title}"',
                        "front matter title", count=1)
        # The running head repeats the title on every page.
        text = sub_once(text, re.escape(old_title), new_title, "running head / body title")
    if args.subtitle:
        text = sub_once(text, r'^subtitle:\s*".*?"$', f'subtitle: "{args.subtitle}"',
                        "front matter subtitle", count=1)

    text = sub_once(text, r'^version:\s*".*?"$',
                    f'version: "Edition {new_ed}"', "front matter version", count=1)
    text = sub_once(text, r'^date:\s*".*?"$', f'date: "{long_date}"',
                    "front matter date", count=1)

    # The licence grant the reader sees must match the licence the repository grants.
    prose_licence = bookmeta.get(meta, "licenses.prose", "CC-BY-4.0")
    text = sub_once(
        text, r'^rights:\s*".*?"$',
        f'rights: "Copyright © {d.year} Ankit Kumar Pandey. '
        f'Licensed under {prose_licence}; code listings under '
        f'{bookmeta.get(meta, "licenses.code", "Apache-2.0")}."',
        "front matter rights", count=1)

    # The right-hand running head carries the edition. Scoped to the \fancyhead[R] declaration on
    # purpose: a blanket replacement of "Edition 1.7.0" would also rewrite the historical
    # changelog heading for that edition, producing a duplicate entry and an edition history that
    # no longer records what actually shipped.
    def head_repl(m: re.Match) -> str:
        return m.group(1) + f"Edition {new_ed}"

    text, n = re.subn(rf"(\\fancyhead\[R\]\{{[^}}]*?)Edition {re.escape(old_ed)}",
                      head_repl, text)
    if n != 1:
        die(f"expected exactly one edition string in the running head, changed {n}")

    # Asset filenames appear in the companion-package section and the worked-example section.
    text = text.replace(old_prefix, args.asset_prefix)

    # Changelog entry, newest first. verify_edition_history.py requires the exact heading form
    # "### Edition X.Y.Z - D Month YYYY" and a continuous descending sequence.
    bullets = args.changelog.read_text(encoding="utf-8").strip()
    if not bullets.startswith("-"):
        die("--changelog file must contain '- ' bullet lines")
    entry = f"### Edition {new_ed} - {long_date}\n\n{bullets}\n\n\\Needspace{{5\\baselineskip}}\n"
    text = sub_once(text, r"^## Changelog\n\n", f"## Changelog\n\n{entry}\n",
                    "changelog section", count=1)

    new_src = src_dir / args.source_name
    new_src.write_text(text, encoding="utf-8")
    if new_src != old_src:
        old_src.unlink()
    print(f"    wrote {new_src.relative_to(book)} ({len(text.splitlines())} lines)")

    # ---------------------------------------------------- edition strings elsewhere
    # Plain textual replacements across the bundle. Each target is listed explicitly so an
    # unexpected file never gets rewritten silently.
    def retext(rel: str, pairs: list[tuple[str, str]], required: bool = True,
               every: bool = False) -> None:
        """Apply literal replacements to one bundle file.

        `every=True` asserts that *each* pair matched, not merely that the file changed. Use it
        for targeted single-file edits. Without it, one matching pair masks the failure of the
        others — which is exactly how the escaped-dot regexes in verify_release_metadata.py were
        left on the previous edition while the file still reported as updated.
        """
        p = book / rel
        if not p.is_file():
            if required:
                die(f"expected file missing: {rel}")
            return
        body = p.read_text(encoding="utf-8")
        before = body
        unmatched = []
        for a, b in pairs:
            if a not in body:
                unmatched.append(a)
                continue
            body = body.replace(a, b)
        if every and unmatched:
            die(f"{rel}: these replacements found no match: {unmatched}")
        if body == before and required:
            die(f"no change made to {rel}; its edition references may have moved")
        p.write_text(body, encoding="utf-8")
        print(f"    updated {rel}")

    common = [
        (old_prefix, args.asset_prefix),
        (f"Publication_Build_Receipt_Edition_{old_ed_short}",
         f"Publication_Build_Receipt_Edition_{new_ed_short}"),
        (old_src_name, args.source_name),
        (f"Edition {old_ed}", f"Edition {new_ed}"),
        (f"Edition: {old_ed}", f"Edition: {new_ed}"),
        (f'"edition": "{old_ed}"', f'"edition": "{new_ed}"'),
    ]
    title_pair = [(old_title, new_title)] if args.title else []

    retext("README.md", common + title_pair)
    retext("AGENTS.md", common + title_pair)
    retext("verify_release.sh", common)
    retext("build_pdf_from_bundle.sh", common)
    retext("source/README.md", common + title_pair)
    retext("source/BUILD_ENVIRONMENT.txt",
           common + [(f"Build date: ", "Build date: ")])
    retext("source/build_pdf.sh", common)
    retext("source/extract_manuscript_code_blocks.py",
           [(f"'edition':'{old_ed}'", f"'edition':'{new_ed}'")])
    retext("source/canonical_source_manifest.json", common)
    retext("source/framework_source_contract_manifest.json", common)
    retext("source/source_contract_verification_receipt.json", common)
    retext("source/reproduce_qa_evaluation.py",
           [(f"evaluation in Edition {old_ed_short}", f"evaluation in Edition {new_ed_short}")])

    # Build date in BUILD_ENVIRONMENT.txt
    be = book / "source" / "BUILD_ENVIRONMENT.txt"
    be.write_text(re.sub(r"^Build date: .*$", f"Build date: {args.date}",
                         be.read_text(encoding="utf-8"), count=1, flags=re.M), encoding="utf-8")

    # ------------------------------------------------ verifiers that pin the edition
    # These hard-code what they expect, which is the point: they fail loudly when an edition is
    # cut without updating them. Update them deliberately here.
    old_minor, new_minor = old_ed_short.split(".")[1], new_ed_short.split(".")[1]
    # The patterns in this file are regex source, so the file literally contains a backslash
    # before each dot. In a raw f-string `\.` is that one backslash plus the dot; `\\.` would be
    # two backslashes and match nothing. every=True makes a mistake here fail loudly.
    old_esc = old_ed.replace(".", r"\.")
    new_esc = new_ed.replace(".", r"\.")
    retext("source/verify_release_metadata.py", [
        # The escaped edition token, however it is prefixed in the checks dict
        # ("Edition 1\.7\.0", "Edition: 1\.7\.0", '"edition": "1\.7\.0"').
        (old_esc, new_esc),
        # The shortened form used for the evaluation check.
        (rf"Edition 1\.{old_minor}", rf"Edition 1\.{new_minor}"),
        (f"edition_1_{old_minor}", f"edition_1_{new_minor}"),
        # The plain-text success message the script prints.
        (f"Edition {old_ed}", f"Edition {new_ed}"),
    ], every=True)

    # The stale-metadata guard should now also reject the edition we just superseded.
    vrm = book / "source" / "verify_release_metadata.py"
    body = vrm.read_text(encoding="utf-8")
    m = re.search(r"Edition 1\\\.\[(\d+)\]", body)
    if m:
        digits = m.group(1)
        superseded = old_ed_short.split(".")[1]
        if superseded not in digits:
            body = body.replace(f"Edition 1\\.[{digits}]", f"Edition 1\\.[{digits}{superseded}]")
            vrm.write_text(body, encoding="utf-8")
            print(f"    updated stale-edition guard to reject 1.[{digits}{superseded}]")

    # verify_edition_history.py keeps an explicit expected sequence, newest first.
    veh = book / "source" / "verify_edition_history.py"
    body = veh.read_text(encoding="utf-8")
    m = re.search(r"expected=\[([^\]]+)\]", body)
    if not m:
        die("could not find the expected edition list in verify_edition_history.py")
    versions = re.findall(r"'([\d.]+)'", m.group(1))
    if new_ed in versions:
        die(f"verify_edition_history.py already expects {new_ed}")
    versions.insert(0, new_ed)
    body = body.replace(m.group(0), "expected=[" + ",".join(f"'{v}'" for v in versions) + "]")
    body = re.sub(r"continuous from [\d.]+ through", f"continuous from {new_ed} through", body)
    veh.write_text(body, encoding="utf-8")
    print(f"    updated verify_edition_history.py expected sequence -> {versions[0]}..{versions[-1]}")

    # verify_companion_references.py skips filenames that belong to the current edition.
    retext("source/verify_companion_references.py", [(old_prefix, args.asset_prefix)])

    # Catch-all sweep for edition strings hard-coded anywhere else in the companion scripts.
    # An explicit per-file list is fragile: each missed occurrence costs a full PDF build before
    # the release gate reports it. verify_edition_history.py is excluded because the edition
    # numbers in its expected sequence are history and must not move.
    sweep_exclude = {"verify_edition_history.py"}
    for py in sorted(src_dir.glob("*.py")):
        if py.name in sweep_exclude:
            continue
        body = py.read_text(encoding="utf-8")
        updated = (body
                   .replace(f"'{old_ed}'", f"'{new_ed}'")
                   .replace(f'"{old_ed}"', f'"{new_ed}"')
                   .replace(f"Edition {old_ed_short}", f"Edition {new_ed_short}")
                   .replace(f"Edition {old_ed}", f"Edition {new_ed}"))
        if updated != body:
            py.write_text(updated, encoding="utf-8")
            print(f"    swept edition strings in source/{py.name}")

    # Generators stamp the edition into what they produce.
    retext("source/generate_build_receipt.py", [(f"'edition':'{old_ed}'", f"'edition':'{new_ed}'")])
    retext("source/generate_environment_lock.py", [(f"'edition':'{old_ed}'", f"'edition':'{new_ed}'")])

    # ------------------------------------------------------------------- book.json
    meta["edition"] = new_ed
    meta["date"] = args.date
    if args.title:
        meta["title"] = new_title
    if args.subtitle:
        meta["subtitle"] = args.subtitle
    meta["canonical_source"] = f"source/{args.source_name}"
    meta["release"]["canonical_pdf"] = f"{args.asset_prefix}.pdf"
    meta["release"]["extra_assets"] = [
        f"release/{args.asset_prefix}_Reproducibility_Package.zip",
        f"release/Publication_Build_Receipt_Edition_{new_ed_short}.json",
        f"{args.asset_prefix}_Full_Source.zip",
    ]
    (book / "book.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("    updated book.json")

    # Old release artifacts are superseded. They remain in git history and in the published
    # GitHub release, which is where an immutable edition belongs — the bundle always describes
    # the current edition only, exactly as the 1.7 bundle contained no 1.6 artifacts.
    removed = []
    for p in sorted((book / "release").glob("*")):
        if old_prefix in p.name or f"Edition_{old_ed_short}" in p.name:
            p.unlink()
            removed.append(p.name)
    for p in sorted(book.glob(f"{old_prefix}*")):
        p.unlink()
        removed.append(p.name)
    for name in removed:
        print(f"    removed superseded artifact {name}")

    print()
    print("==> text transforms complete. Artifacts still to regenerate (needs the toolchain):")
    print("      scripts/regen-edition.sh " + slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
