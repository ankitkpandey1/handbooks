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

Corrections ship as a new edition, never as an in-place edit of a published one. To cut
Edition 1.8.0:

1. Copy the manuscript to the new edition filename and edit it there.
2. Update the edition string everywhere `verify_release_metadata.py` checks for it:
   `README.md`, `source/BUILD_ENVIRONMENT.txt`, `source/canonical_source_manifest.json`,
   `source/framework_source_contract_manifest.json`, `source/reproduce_qa_evaluation.py`.
3. Add an edition-history entry (`verify_edition_history.py` enforces this).
4. Regenerate, do not hand-edit: `generate_environment_lock.py`,
   `extract_manuscript_code_blocks.py`, `generate_build_receipt.py`, then both
   `SHA256SUMS.txt` files.
5. Run `bash verify_release.sh`, then tag `agents-handbook/v1.8.0`.
