<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
<div align="center">

# Handbooks

**Short technical handbooks, published with the full source and the tooling that built them.**

Every book ships as a PDF, an EPUB, an HTML page, and a single-file Markdown export —
and every download can be cryptographically traced back to the commit that produced it.

[![Latest release](https://img.shields.io/github/v/release/ankitkpandey1/handbooks?sort=semver&label=latest&color=123456)](https://github.com/ankitkpandey1/handbooks/releases/latest)
[![Verify](https://github.com/ankitkpandey1/handbooks/actions/workflows/pr-verify.yml/badge.svg)](https://github.com/ankitkpandey1/handbooks/actions/workflows/pr-verify.yml)
[![Pages](https://github.com/ankitkpandey1/handbooks/actions/workflows/pages.yml/badge.svg)](https://ankitkpandey1.github.io/handbooks/)
[![Prose CC-BY-4.0](https://img.shields.io/badge/prose-CC--BY--4.0-blue)](LICENSE)
[![Code Apache-2.0](https://img.shields.io/badge/code-Apache--2.0-blue)](LICENSES/Apache-2.0.txt)

[**Read online**](https://ankitkpandey1.github.io/handbooks/) ·
[**Download**](#the-books) ·
[**Verify a download**](#verify-what-you-downloaded) ·
[**Contribute**](CONTRIBUTING.md) ·
[**For agents**](#for-agents)

</div>

---

## Why this exists

Deep technical research usually happens in a conversation and then dies there — unshareable,
uncitable, and impossible to build on six months later. This repository is the other end of that
pipe: a place where research becomes a book with a permanent download link, a verifiable build,
and a version history.

It is built for two kinds of reader from the start: **people**, and the **agents people delegate
reading to**.

## The books

| Book | Tier | Edition | Formats |
|---|:---:|:---:|---|
| **[Production Agent Engineering in 2026](books/agents-handbook)**<br><sub>A production systems field manual for advanced engineers · 181 pp. · Architecture selection, harness design, task contracts, context engineering, security, durable execution, evaluation.</sub> | **A** | 1.7.0 | [PDF](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.pdf) · [EPUB](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.epub) · [HTML](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.html) · [MD](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.md) |

Those links always resolve to the newest edition — they never rot. Full catalogue with section
outlines and digests: **[`books.json`](books.json)** · browsable at
**[ankitkpandey1.github.io/handbooks](https://ankitkpandey1.github.io/handbooks/)**.

## What "Tier" means

Assurance, stated honestly rather than implied. Both tiers are real books; they make different
promises, and the tier is printed on the cover, declared in `book.json`, and shown in the
catalogue.

<table>
<tr><th align="left" width="90">Tier A</th><td>
The published PDF is cryptographically bound to the exact source that produced it. Ships a
source-contract manifest, a reproducibility package, an external build receipt, and a verifier
suite you can run offline — for <code>agents-handbook</code>, 17 checks covering section
numbering, edition history, PDF text layer and navigation, source-to-PDF binding, embedded
archive identity, and exact reproduction of the synthetic evaluation.
</td></tr>
<tr><th align="left">Tier B</th><td>
Manuscript plus metadata, structurally linted and built to all four formats by CI. No verifier
suite, no reproducibility package, no build receipt. A real book with a lighter guarantee.
</td></tr>
</table>

A Tier B book graduates to Tier A by adding verifiers. The linter fails a build if a Tier B
manuscript borrows Tier A vocabulary, because overclaiming is the fastest way to devalue the
books that earned the claim.

## Verify what you downloaded

Every release asset carries Sigstore-signed
[SLSA build provenance](https://docs.github.com/en/actions/concepts/security/artifact-attestations),
binding its digest to this repository, the workflow run, and the exact commit:

```bash
gh attestation verify agents-handbook.pdf --repo ankitkpandey1/handbooks
sha256sum -c SHA256SUMS.txt
```

For a Tier A book you can go further and check the artifact against its source, offline:

```bash
git clone https://github.com/ankitkpandey1/handbooks && cd handbooks
scripts/verify-book.sh agents-handbook
```

**Reproducibility boundary**, stated plainly: Pandoc is pinned by version *and* SHA-256; TeX Live
and fonts come from the distribution's current packages and are not pinned. So the build is
environment-attested, not byte-identical across differing dependency closures. What *is* verified:
the canonical source, the build inputs, the PDF's text and navigation properties, the embedded
archive, and the external receipt. See
[the runbook](docs/maintainers/release-runbook.md#reproducibility-boundary-and-how-to-strengthen-it)
for how to strengthen it.

## For agents

<table>
<tr><td width="180"><b>Read the book</b></td><td>
Prefer the single-file Markdown export over the PDF:
<code>releases/latest/download/&lt;slug&gt;.md</code>
</td></tr>
<tr><td><b>Read the catalogue</b></td><td>
<a href="books.json"><code>books.json</code></a> — every book, edition, licence, asset URL, digest
and section outline in one fetch. Also at
<a href="https://ankitkpandey1.github.io/handbooks/books.json">the site root</a>.
</td></tr>
<tr><td><b>Work in this repo</b></td><td>
<a href="AGENTS.md"><code>AGENTS.md</code></a> at the root, plus a nested one per book
(nearest-file-wins). Read the boundaries section before editing: published artifacts and
hash-pinned files are immutable.
</td></tr>
<tr><td><b>Pointer file</b></td><td>
<a href="https://ankitkpandey1.github.io/handbooks/llms.txt"><code>llms.txt</code></a>
</td></tr>
</table>

## Build a book

```bash
scripts/setup-toolchain.sh                      # pinned Pandoc + XeLaTeX (Debian/Ubuntu)
scripts/build-book.sh agents-handbook            # -> books/agents-handbook/build/
scripts/verify-book.sh agents-handbook --prose    # structural + verifiers + prose style
```

CI is the build authority; local builds are a convenience. One uniform interface covers every
book regardless of tier:

| Command | Does |
|---|---|
| `scripts/new-book.sh <slug> "Title"` | Scaffold a Tier B book (add `--from-draft <slug>` to promote raw research) |
| `scripts/build-book.sh <slug> [fmt…]` | Build `pdf` `epub` `html` `md` |
| `scripts/verify-book.sh <slug>` | Structural lint + the book's own verifier suite |
| `scripts/lint-prose.sh <slug>` | [Vale](https://vale.sh/) prose style |
| `scripts/build-index.py` | Regenerate `books.json` and the site |

## Repository layout

```
books/<slug>/          a book: book.json contract, source/, release/, its own AGENTS.md
drafts/<slug>/         raw research. no review bar, no build contract, no promises
_template/             scaffold for a new Tier B book
scripts/               uniform entrypoints — use these, not a book's internal scripts
styles/                Vale house prose style
docs/                  generated site + maintainer runbooks
books.json             generated machine-readable catalogue
```

## Contributing

Errata, claim challenges, and new-book proposals are all welcome —
[**CONTRIBUTING.md**](CONTRIBUTING.md).

The contribution standard is one rule: **claims carry evidence labels, and code listings carry
authenticity labels.** The verification pipeline exists so a reader can check the book, and an
unsourced assertion is the one thing it cannot check for them. This is enforced — the linter
reports label coverage on every run.

Raw, unpolished research goes in [`drafts/`](drafts/) with no review bar at all. That is
deliberate: an idea should never die because the publishing pipeline looked too steep.

## Licence and citation

Prose is [**CC-BY-4.0**](LICENSE); code, scripts and verifiers are
[**Apache-2.0**](LICENSES/Apache-2.0.txt). Split by file type via SPDX headers — rationale in
[LICENSING.md](LICENSING.md).

Cite via the "Cite this repository" button, or [`CITATION.cff`](CITATION.cff). Releases are
archived with a DOI.

---

<div align="center">
<sub>Maintained by <b>Ankit Kumar Pandey</b> · <a href="mailto:itsankitkp@gmail.com">itsankitkp@gmail.com</a></sub>
</div>
