<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
# Handbooks

Short technical handbooks. Each one is published with its full source, the tooling that built
it, and a way to check that the file you downloaded came from that source.

Read them at **[ankitkpandey1.github.io/handbooks](https://ankitkpandey1.github.io/handbooks/)**,
or download any format from the table below.

## Books

| Book | Tier | Edition | Download |
|---|:---:|:---:|---|
| **[Production Agent Engineering](books/agents-handbook)** — 181 pp. Architecture selection, harness and control-plane design, task contracts, context engineering, state and memory, security, durable execution, evaluation. | A | 1.8.0 | [PDF](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.pdf) · [EPUB](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.epub) · [HTML](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.html) · [Markdown](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agents-handbook.md) |

Those links always resolve to the newest edition, so they are safe to bookmark or cite. The
Markdown export is a single plain file, meant for pasting into a model's context — it is usually
the better choice for an agent than the PDF.

## Tiers

Books differ in how much you can verify about them, so the difference is labelled rather than
left to inference. The tier appears on the cover, in `book.json`, and in the catalogue.

**Tier A** — the published PDF is bound to the exact source that produced it. Ships a
source-contract manifest, a reproducibility package, an external build receipt, and a verifier
suite you can run offline. For `agents-handbook` that is 17 checks, covering section numbering,
edition history, the PDF text layer and navigation, source-to-PDF binding, embedded archive
identity, and exact reproduction of the synthetic evaluation.

**Tier B** — manuscript plus metadata, structurally linted and built to all four formats. No
verifier suite, no reproducibility package, no build receipt.

New books start at Tier B and graduate by adding verifiers. Most should stay at Tier B; Tier A is
worth the cost only when a book makes claims a reader would want to check mechanically. The
linter fails a Tier B book that borrows Tier A vocabulary.

## Checking a download

Release assets carry Sigstore-signed
[SLSA provenance](https://docs.github.com/en/actions/concepts/security/artifact-attestations),
which ties each file to the commit and workflow run that produced it:

```bash
gh attestation verify agents-handbook.pdf --repo ankitkpandey1/handbooks
sha256sum -c SHA256SUMS.txt
```

Needs GitHub CLI 2.60 or newer. Older versions fail with `unsupported tlog public key type:
PKIX_ED25519`, which is the CLI being unable to read Sigstore's current trust root — not a
problem with the artifact.

For a Tier A book you can check the artifact against the source itself, offline:

```bash
git clone https://github.com/ankitkpandey1/handbooks && cd handbooks
scripts/verify-book.sh agents-handbook
```

What that does *not* prove: builds are not byte-identical across machines. Pandoc is pinned by
version and SHA-256, but TeX Live and the fonts come from the distribution's current packages.
So the environment is attested, not reconstructed. What is verified is the canonical source, the
build inputs, the PDF's text and navigation properties, the embedded archive, and the external
receipt. The
[runbook](docs/maintainers/release-runbook.md#reproducibility-boundary-and-how-to-strengthen-it)
describes how to tighten this with a digest-pinned container, and why that has not been done yet.

## Working on a book

```bash
scripts/setup-toolchain.sh                     # pinned Pandoc and XeLaTeX (Debian/Ubuntu)
scripts/build-book.sh agents-handbook          # pdf, epub, html, md -> books/<slug>/build/
scripts/verify-book.sh agents-handbook --prose
```

CI is the build authority. Local builds are a convenience, and the scripts fail with a clear
message rather than a broken artifact if the toolchain is missing.

| Command | Purpose |
|---|---|
| `scripts/new-book.sh <slug> "Title"` | Scaffold a Tier B book. `--from-draft <slug>` promotes raw research |
| `scripts/build-book.sh <slug> [fmt…]` | Build any of `pdf` `epub` `html` `md` |
| `scripts/verify-book.sh <slug>` | Structural lint, then the book's own verifier suite |
| `scripts/lint-prose.sh <slug>` | [Vale](https://vale.sh/) house prose style |
| `scripts/build-index.py` | Regenerate `books.json` and the site |

Releases are cut by tag: `git tag <slug>/v<semver>`. The workflow refuses to publish if the tag
disagrees with the edition declared in `book.json`, or if the verifier suite fails.

## Layout

```
books/<slug>/     a book: book.json contract, source/, release/, its own AGENTS.md
drafts/<slug>/    raw research. no review bar, no build contract, no promises
_template/        scaffold for a new Tier B book
scripts/          the uniform interface — use these, not a book's internal scripts
styles/           Vale prose rules
docs/             generated site, plus maintainer runbooks
books.json        generated catalogue: editions, licences, asset URLs, digests, outlines
```

Agents should read [`AGENTS.md`](AGENTS.md) first — there is one at the root and one per book,
resolved nearest-first. The boundaries section matters: published artifacts and hash-pinned files
must not be edited.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Errata, claim challenges and new-book proposals are all
welcome, and there are issue templates for each.

One rule carries most of the weight: **claims carry evidence labels, and code listings carry
authenticity labels.** The point of publishing the verifiers is that a reader can check the book,
and an unsourced assertion is the one thing they cannot check. The linter reports label coverage
on every run — `agents-handbook` is currently at 81 of 81 substantial code blocks.

Unpolished research belongs in [`drafts/`](drafts/), which has no review bar at all. Research that
sits in a chat window until the tab closes is the failure this repository exists to prevent, and a
steep-looking pipeline is usually the reason.

## Licence

Prose is [CC-BY-4.0](LICENSE). Scripts, verifiers and build tooling are
[Apache-2.0](LICENSES/Apache-2.0.txt). The split is by file type, declared with SPDX headers;
[LICENSING.md](LICENSING.md) explains why the two are not applied to the same files.

To cite a book, use the "Cite this repository" button or [`CITATION.cff`](CITATION.cff). Releases
are not yet DOI-archived — [the runbook](docs/maintainers/release-runbook.md#4-zenodo-for-dois)
covers enabling that.

---

Maintained by Ankit Kumar Pandey — itsankitkp@gmail.com
