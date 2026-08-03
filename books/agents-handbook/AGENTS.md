# AGENTS.md — agents-handbook

**Tier A.** Edition 1.8.0. See [`book.json`](book.json) for the machine-readable contract and
the repo root [`AGENTS.md`](../../AGENTS.md) for repo-wide rules.

Canonical source: `source/production_agent_engineering_edition_1_8.md` (~8,650 lines).

## Commands

```bash
bash build_pdf_from_bundle.sh            # Pandoc + XeLaTeX, then attach and linearise
bash verify_release.sh                   # all offline checks (manifest-only)
bash verify_release.sh online            # additionally refetch pinned upstream sources
```

From the repo root, prefer the uniform interface: `scripts/build-book.sh agents-handbook`
and `scripts/verify-book.sh agents-handbook`.

Requires Pandoc 3.1.11.1, XeLaTeX, Python 3.13 and `source/requirements.txt`. If those are
absent, do not attempt a local build — push and let CI build it.

## What the verifier suite checks

Release metadata consistency, source-contract manifest, manuscript examples, companion
references, section numbering, edition history, the deferred-approval application contract,
exact reproduction of the synthetic QA evaluation, PDF text layer, source-to-PDF binding,
PDF navigation, embedded-archive identity, build-receipt fields, in-memory Python
compilation of every companion script, and member checksums.

`verify_release.sh` is the gate. If it fails, the change is wrong — do not adjust the
verifier to make a change pass.

## Files you must not touch

Every file listed in `SHA256SUMS.txt` and `source/SHA256SUMS.txt` is hash-pinned, and those
hashes appear again in `FULL_SOURCE_MANIFEST.json`,
`source/canonical_source_manifest.json` and the published build receipt. In practice this
means:

- the manuscript,
- everything under `source/`,
- everything under `release/`,
- this book's `README.md`.

Editing any of them without regenerating every manifest that pins them breaks the chain and
fails CI. `AGENTS.md` and `book.json` are *not* pinned — they are safe to edit.

## Correcting the manuscript

Corrections ship as a new edition, never as an in-place edit of a published one. **Do not cut
an edition by hand.** The edition string is pinned in three manifests, the external receipt and
five verifiers and generators; missing one costs a full PDF build before the release gate says
so. Use the tooling:

```bash
# 1. Text transforms. No toolchain needed. Writes the new manuscript, rewrites every pinned
#    edition string, adds the changelog entry, updates book.json, removes superseded artifacts.
scripts/cut-edition.py --slug agents-handbook --to <version> \
  --source-name production_agent_engineering_edition_<major>_<minor>.md \
  --asset-prefix Production_Agent_Engineering_Edition_<major>.<minor> \
  --date <YYYY-MM-DD> --changelog <file of '- ' bullets>
# add --title / --subtitle only when they actually change

# 2. Edit the manuscript for the actual content change.

# 3. Derived artifacts. Needs Pandoc, XeLaTeX, Ghostscript, qpdf, pdftotext and PyMuPDF, so
#    push to an edition/** branch and let prepare-edition.yml do it, or run locally:
scripts/regen-edition.sh agents-handbook

# 4. Open a PR, merge, then tag.
git tag agents-handbook/v<version> && git push origin agents-handbook/v<version>
```

`regen-edition.sh` ends by running `verify_release.sh`, so a regeneration that does not verify
does not complete.

Two things the tooling guards, both learned by getting them wrong:

- The running-head edition string is replaced **in scope**, not globally. A blanket replacement
  also rewrites the historical changelog heading for the superseded edition, which produces a
  duplicate entry and destroys the edition history.
- Ghostscript runs **before** attachment, for compression only. Its `pdfwrite` device is a
  re-distiller and drops the `/FileAttachment` annotation that `verify_embedded_package.py`
  requires; `qpdf --linearize` does the linearisation afterwards.
