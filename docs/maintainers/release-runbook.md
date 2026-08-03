<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
# Maintainer runbook

Everything that is not automated, and the reasoning behind what is.

## One-time repository setup

Sections 4 and 5 need a browser login and cannot be automated.

Do these once, in order. Items 1–3 are required for releases to work at all.

1. **Enable Actions write access for releases.**
   Settings → Actions → General → Workflow permissions → **Read and write permissions**.
   The release workflow requests `contents: write`, `id-token: write` and
   `attestations: write` per-job, but the repository must permit it.

2. **Enable Pages.** Settings → Pages → Source → **GitHub Actions**. The `pages` workflow
   then serves `docs/` at `https://ankitkpandey1.github.io/handbooks/`.

3. **Set the repository description, topics and homepage.** These are the whole shop window
   and are empty by default:

   ```bash
   gh repo edit ankitkpandey1/handbooks \
     --description "Short technical handbooks with full source, reproducible builds and verifiable releases" \
     --homepage "https://ankitkpandey1.github.io/handbooks/" \
     --add-topic handbook --add-topic agent-engineering --add-topic reproducible-builds \
     --add-topic technical-writing --add-topic llm --add-topic pandoc
   ```

### 4. Zenodo, for DOIs

**What it is.** A free open-access repository run by CERN. Connected to a GitHub repository, it
archives each new release and mints a **DOI** — a permanent identifier such as
`https://doi.org/10.5281/zenodo.1234567`.

**Why bother.** Three reasons, in order of how much they actually matter here:

1. *Permanence.* A DOI keeps resolving if the repository is renamed, made private, deleted, or
   if GitHub itself goes away, because Zenodo holds its own copy of the artifact. The
   `releases/latest/download/` links are stable only while GitHub exists and the repo stays up.
2. *Citability.* A DOI can go in a reference list. A GitHub URL reads as a link; a DOI reads as
   a publication.
3. *Discoverability.* Zenodo records are indexed by OpenAIRE, DataCite and Google Scholar.

Worth being honest about the size of the win: the audience for these handbooks is engineers, not
academics, so this is mostly permanence insurance and credibility signalling. It costs about five
minutes.

**Steps.**

1. [zenodo.org](https://zenodo.org) → **Sign in with GitHub** → authorise.
2. **Account → GitHub** → find `ankitkpandey1/handbooks` → toggle **On**.
3. Create a release *after* the toggle is on.

**Zenodo only archives releases created after the switch is enabled.** Releases published before
that are not picked up retroactively. To give an existing edition a DOI, either cut a new patch
edition, or create a manual Zenodo deposit and upload the artifacts by hand.

**Two DOIs per project.** Each release gets a *version* DOI; there is also a *concept* DOI that
always resolves to the newest version. Put the concept DOI on a CV, profile or talk slide; cite a
version DOI when referring to a specific edition.

**The `.zenodo.json` trap.** Zenodo reads `CITATION.cff` **only when `.zenodo.json` is absent**.
If both exist, `.zenodo.json` wins and the CFF is ignored silently. This repository ships only
`CITATION.cff` deliberately. Do not add `.zenodo.json` unless you intend it to take over
completely.

**After the first DOI exists**, three things need updating, and until they are done the
repository must not claim to be DOI-archived:

- `CITATION.cff` — add `doi: "10.5281/zenodo.XXXXXXX"` (the concept DOI) at the top level.
- `README.md` — replace the "not yet DOI-archived" sentence, and optionally add the badge Zenodo
  provides on the record page.
- This runbook — clear the item from "Known outstanding items".

### 5. ORCID

**What it is.** A free, permanent 16-digit identifier for a person, such as
`0000-0002-1825-0097`. It distinguishes you from everyone with a similar name and aggregates your
published work under one identity.

**Why it matters here specifically.** These books are published under a personal identity that is
deliberately separate from any employer. An ORCID is what keeps the handbooks, any future papers,
and any Zenodo deposits attached to the same person regardless of which email address or
institution is current at the time. Without one, the author is a name string that search engines
have to guess about.

**Steps.**

1. Register at [orcid.org](https://orcid.org) — about three minutes.
2. Add the ORCID to the Zenodo account (**Account → Profile**), so deposits link to it
   automatically and appear on the ORCID record.
3. Fill in the commented `orcid:` field in `CITATION.cff`, in both the top-level `authors` block
   and the `preferred-citation` block.

## Cutting a release

```bash
# 1. Make the book agree with the edition you intend to publish.
#    The release workflow refuses to publish if the tag and book.json disagree.
python3 scripts/bookmeta.py get <slug> edition

# 2. Verify locally if you have the toolchain; otherwise let CI do it.
scripts/verify-book.sh <slug>

# 3. Refresh the catalogue and commit.
python3 scripts/build-index.py
git add -A && git commit -m "release: <slug> v<version>"

# 4. Tag. This is what triggers the release.
git tag <slug>/v<version>
git push origin main
git push origin <slug>/v<version>
```

To rehearse without publishing, run the `release` workflow via **workflow_dispatch** with
the slug: it builds, verifies and uploads a CI artifact but creates no release and signs
nothing.

## What the release workflow guarantees

- The book's verifier suite passes **before** anything is typeset. A failing verifier means
  no release, not a warning.
- The tag's version and `book.json`'s edition match. A release cannot be cut from a
  manuscript that declares a different edition.
- Every asset gets Sigstore-signed SLSA build provenance via
  `actions/attest-build-provenance`, binding its digest to this repository, this workflow and
  the exact commit. Readers verify with
  `gh attestation verify <file> --repo ankitkpandey1/handbooks`.
- Assets are published under stable unversioned names, so
  `/releases/latest/download/<slug>.pdf` is a permanent link across all future editions.
  Put *that* link on a CV or in a talk, never a version-specific one.

## Reproducibility boundary, and how to strengthen it

`scripts/setup-toolchain.sh` pins Pandoc to an exact version and verifies its SHA-256,
because Pandoc is the component whose version most directly changes document output. TeX Live
and fonts come from the current Ubuntu package set and are **not** pinned, so a different apt
snapshot can produce a non-identical PDF.

This matches what the books already claim about themselves and overclaims nothing. If you
want a stronger boundary, the upgrade path is a container pinned by digest:

```bash
# Resolve a digest, then use it in the workflow's `container:` key.
docker buildx imagetools inspect pandoc/latex:latest-ubuntu --format '{{.Manifest.Digest}}'
```

Add to the `build` job in `.github/workflows/release.yml`:

```yaml
container:
  image: pandoc/latex@sha256:<digest>
```

That buys a byte-reproducible environment inside a named digest — an honest and much stronger
claim than the current one. It costs the flexibility of installing per-book Python
requirements freely, so it is worth doing once the book count justifies it, not before.

## Correcting a published book

Published editions are immutable, and the verification chain is the reason. Every manuscript
hash is pinned in `SHA256SUMS.txt`, the source-contract manifest and the build receipt, and
bound into the PDF itself. Editing one line invalidates all of it.

So: corrections ship as a new edition. See the per-book `AGENTS.md` for the exact
regeneration sequence — for `agents-handbook` that is
[`books/agents-handbook/AGENTS.md`](../../books/agents-handbook/AGENTS.md).

## Known outstanding items

- **`agents-handbook` Edition 1.8.0 must fix the front-matter `rights:` field**, which still
  reads "All rights reserved" and contradicts the repository's CC-BY-4.0 licence. The
  structural linter warns about this on every run until it is fixed. See
  [LICENSING.md](../../LICENSING.md).
- **No DOI yet.** The Zenodo switch (section 4) has not been enabled, so `agents-handbook`
  v1.7.0 and v1.8.0 are not archived and have no DOI. `README.md` states this plainly rather
  than claiming otherwise; correct it once the first DOI exists.
- **No ORCID yet** — see section 5. The `orcid:` fields in `CITATION.cff` stay commented out
  until there is a real one; a placeholder ORCID is worse than none.
