<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
# drafts/

Raw research. **No review bar, no build contract, no promises.**

This directory exists because of a specific failure mode: you do a piece of real research in a
chat window, it is genuinely useful, and it dies there — because the alternative was a
publishing pipeline that looked too steep to climb that evening. Nothing here has to be good,
finished, labelled, or even coherent.

## The habit

```bash
mkdir -p drafts/<topic>
# paste the transcript, the notes, the half-formed conclusion. Commit.
git add drafts/<topic> && git commit -m "draft: <topic>"
```

That is the whole ritual. Anything at all is better than a closed tab.

Nothing under `drafts/` is linted, built, released, indexed in `books.json`, or shown on the
site. CI ignores it entirely.

## Promoting a draft to a book

When a draft turns out to be worth reading:

```bash
scripts/new-book.sh <book-slug> "Book Title" --from-draft <topic>
```

That scaffolds a Tier B book and copies the raw material into
`books/<book-slug>/source/raw/` so the provenance of the finished text stays visible. Then
write the real manuscript, labelling claims as you go — the raw material stays unlabelled and
is marked as such.

Not every draft should be promoted. Most will not be. That is the correct ratio.

## What belongs here

- Chat transcripts and research dumps
- Reading notes, link piles, half-finished arguments
- Experiment logs, dead ends, things that did not work
- Self-reflection notes and retrospectives

## What does not

- Anything that reads as a finished claim to an outside reader. Once it looks
  authoritative, it needs labels and a tier — make it a book.
- Secrets, credentials, tokens, internal or client-confidential material. This repository is
  public. Check before you paste.
