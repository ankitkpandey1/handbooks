# Contributing

Contributions are welcome from humans and from agents. The rules below are the same for
both.

## The one rule that matters

**Claims carry evidence labels, and code carries authenticity labels.**

This is what separates these handbooks from a blog post, and it is the contribution
standard. If you add a sentence that asserts something about how a system behaves, label
where that came from. If you add a code listing, label whether it was executed, adapted, or
is illustrative. Follow the labelling scheme already used by the book you are editing — see
its "Scope and evidence labels" and "Code authenticity labels" sections.

An unlabelled claim will be asked for a label before merge. This is not pedantry: the
verification pipeline exists so that a reader can check the book, and an unsourced assertion
is the one thing the pipeline cannot check for them.

## Kinds of contribution

| I want to… | Do this |
|---|---|
| Fix a typo or a broken link | PR against the book's manuscript in `source/` |
| Correct a factual error | Open an **Erratum** issue, then PR |
| Challenge a claim | Open a **Claim challenge** issue. Evidence required, not vibes |
| Propose a new book | Open a **New book** issue before writing |
| Improve tooling or CI | PR against `scripts/` or `.github/` |
| Dump raw research | `drafts/<slug>/` — no review bar, no build contract |

## Before you open a pull request

```bash
scripts/verify-book.sh <slug>
```

CI runs the same command on the books your PR touches. For a Tier A book this runs the full
verifier suite; for Tier B it runs structural lint.

Then check:

- [ ] One book per PR. Do not touch two books in one change.
- [ ] Nothing under `books/<slug>/release/` is modified.
- [ ] No hash-pinned file is modified outside a proper edition bump (see [AGENTS.md](AGENTS.md)).
- [ ] New code files carry an SPDX header.
- [ ] Claims are labelled; listings are labelled.
- [ ] `scripts/build-index.py` re-run if you changed any `book.json`.

## Editions and versioning

Books use semantic versioning as editions, tagged `<slug>/v<major>.<minor>.<patch>`.

- **Patch** — typos, link fixes, clarifications that change no claim.
- **Minor** — new sections, corrected claims, new evidence.
- **Major** — restructuring, or a change that invalidates prior guidance.

**A published edition is never rewritten.** Corrections ship as a new edition with an
erratum entry. This is the reason the verification chain is worth anything: an edition's
hash means something because the edition does not move.

## Licensing

Prose is `CC-BY-4.0`, code is `Apache-2.0`. By opening a PR you license your contribution
under whichever governs the files you touched. No CLA. See [LICENSING.md](LICENSING.md).

## Tiers, and not overclaiming

New books start at **Tier B**: manuscript plus metadata, structural lint, built to
PDF/EPUB/HTML/Markdown by CI. That is a real, publishable, citable book.

**Tier A** additionally means: a source-contract manifest, a reproducibility package, an
external build receipt, and a verifier suite that binds the published PDF back to the exact
source that produced it. Tier A is expensive and is not the goal for most books.

Do not describe a Tier B book in Tier A language. The tier is declared in `book.json`,
printed on the cover, and shown in the catalogue. Honest assurance levels are the point.
