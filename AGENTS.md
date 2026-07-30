# AGENTS.md

Monorepo of short technical books ("handbooks"). One directory per book under `books/`.
Each book is self-contained and builds and verifies through a uniform interface.

## Repo map

- `books/<slug>/` — a book. `source/` holds the canonical manuscript, `release/` holds
  published artifacts, `build/` is transient local output.
- `books/<slug>/book.json` — the book's contract. Machine-readable. Single source of truth
  for title, tier, edition, licences, build formats and verify entrypoint.
- `drafts/<slug>/` — raw research with no build contract and no promises. Free to be messy.
- `_template/` — scaffold for a new Tier B book. Copied by `scripts/new-book.sh`.
- `scripts/` — uniform entrypoints. Use these, not a book's internal scripts.
- `books.json`, `docs/` — generated discovery surface. Regenerate, never hand-edit.

## Commands

```bash
scripts/new-book.sh <slug> "Title"        # scaffold a Tier B book from _template/
scripts/build-book.sh <slug> [fmt...]     # formats: pdf epub html md  (default: from book.json)
scripts/verify-book.sh <slug>             # structural lint + the book's own verifiers
scripts/build-index.py                    # regenerate books.json and docs/
```

`build-book.sh` needs `pandoc`; `pdf` additionally needs XeLaTeX. Neither is assumed
present — CI is the build authority. `scripts/setup-toolchain.sh` installs the pinned
toolchain (used by CI, works locally on Debian/Ubuntu).

## Tiers

- **Tier A** — full publication pipeline: source-contract manifests, build receipt,
  reproducibility package, verifier suite. Releases are immutable.
- **Tier B** — manuscript plus metadata. Structural lint only. This is the default for new
  books; a book graduates to Tier A by adding verifiers.

Never present a Tier B book as carrying Tier A assurance. The tier is stated in
`book.json` and on the book's cover.

## Boundaries

- **Never edit anything under `books/<slug>/release/`.** Published artifacts are immutable.
- **Never edit a file whose SHA-256 is pinned in a `SHA256SUMS.txt` or a `*_MANIFEST.json`**
  unless you are cutting a new edition and regenerating every manifest that pins it. For
  `agents-handbook` this includes the manuscript, everything in `source/`, and the book's
  own `README.md`.
- **Never hand-write or hand-edit a build receipt, manifest hash, or checksum file.**
  Regenerate them with the book's own generator scripts.
- **One book per pull request.** Do not touch two books in one change.
- Do not bump an edition number as a side effect of an unrelated change.
- Do not add a dependency to a book's `requirements.txt` without pinning it exactly.

## Conventions

- Release tags are `<slug>/v<semver>` — e.g. `agents-handbook/v1.7.0`. A tag push triggers
  the release workflow. Do not create tags without the slug prefix.
- Prose is `CC-BY-4.0`; code is `Apache-2.0`. New code files get an SPDX header. See
  [LICENSING.md](LICENSING.md).
- British English (`lang: en-GB`) in manuscripts, matching the existing books.
- Every factual claim in a manuscript carries an evidence label, and every code listing
  carries an authenticity label. See [CONTRIBUTING.md](CONTRIBUTING.md).
