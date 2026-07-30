<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
# Maintainer runbook

Everything that is not automated, and the reasoning behind what is.

## One-time repository setup

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

4. **Zenodo, for DOIs.** Sign in to [zenodo.org](https://zenodo.org) with GitHub, then
   Account → GitHub → flip the switch on `ankitkpandey1/handbooks`. Zenodo mints a DOI for
   every release **created after** the switch is on; earlier releases are not retroactively
   archived.

   Two things to know:

   - Zenodo reads `CITATION.cff` **only if `.zenodo.json` is absent**. If both exist,
     `.zenodo.json` wins and the CFF is silently ignored. This repo deliberately ships only
     `CITATION.cff`. Do not add `.zenodo.json` unless you intend it to take over.
   - Each release gets its own version DOI, plus a concept DOI that always resolves to the
     newest. Cite the concept DOI on a CV; cite the version DOI in a paper.

   Once the first DOI exists, add the badge to `README.md` and the DOI to `CITATION.cff`.

5. **Pin an ORCID.** Register at [orcid.org](https://orcid.org) and fill in the commented
   `orcid:` field in `CITATION.cff`. This is what makes the books aggregate under one
   identity across Zenodo, Crossref and any future publisher.

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
- No DOI yet — pending the Zenodo switch in step 4 above.
- No ORCID yet — pending step 5.
