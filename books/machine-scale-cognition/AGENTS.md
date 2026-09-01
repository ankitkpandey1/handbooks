# AGENTS.md — machine-scale-cognition

**Tier B.** Edition 2.0.0. See [`book.json`](book.json) for the machine-readable contract and
the repo root [`AGENTS.md`](../../AGENTS.md) for repo-wide rules.

Canonical source: `source/machine-scale-cognition.md`

## Commands

Run from the repo root:

```bash
scripts/verify-book.sh machine-scale-cognition            # structural lint (no toolchain needed)
scripts/build-book.sh machine-scale-cognition html md     # fast preview formats
scripts/build-book.sh machine-scale-cognition             # everything in book.json build.formats
```

## What Tier B means here

Structural lint plus a local experiment-artifact checker. There is **no** verifier suite binding the
published artifact to its source, no reproducibility package and no build receipt.

Do not describe this book as reproducible, byte-identical, or source-bound. The linter fails
the build if Tier A language appears in a Tier B manuscript, and that check exists because
overclaiming is the easiest way to destroy the credibility of the books that have earned the
claim.

## Graduating to Tier A

Only worth doing if the book makes claims a reader would want to verify mechanically. It
means adding: a canonical source manifest, a reproducibility package, an external build
receipt, and a verifier suite that binds the PDF to its source. Then set `"tier": "A"` and
declare `verify.entrypoint` in `book.json`. Use `books/agents-handbook/` as the reference
implementation.

## House rules

- Every claim carries an evidence label; every listing carries an authenticity label. The
  approved sets are defined in the manuscript's front sections.
- Published editions are immutable. Corrections ship as a new edition with an entry in the
  manuscript's "Edition history" section.
- British English (`lang: en-GB`).
