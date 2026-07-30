# Licensing

This repository mixes prose and code, so it uses two licences, split by file type.
This file is the authoritative statement.

| Content | Licence | SPDX identifier |
|---|---|---|
| Manuscripts, prose, figures, book metadata, documentation | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| Build scripts, verifiers, CI workflows, tooling, code listings in manuscripts | Apache License 2.0 | `Apache-2.0` |

Full texts are in [`LICENSES/`](LICENSES/). The root [`LICENSE`](LICENSE) file carries the
CC-BY-4.0 text because prose is the dominant content of this repository.

## Why split rather than dual-licence

Prose and code want different terms. CC licences are designed for creative works and carry
attribution mechanics suited to a book; the Apache 2.0 licence is designed for software and
carries a patent grant and a `NOTICE` mechanism. The Apache Software Foundation has also
raised a compatibility concern between Apache-2.0 and CC-BY over CC's "Effective
Technological Measures" clause, which is a further reason to keep the two licences on
*different files* rather than applying both to the same file.

## How to tell which licence applies to a file

Files carry an `SPDX-License-Identifier` header where the format allows one. Where it does
not (for example JSON manifests), the table above governs by file type.

```
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
```

## Code listings inside manuscripts

Code listings printed in a manuscript are licensed `Apache-2.0`, not `CC-BY-4.0`, even
though the surrounding prose is `CC-BY-4.0`. This is deliberate: it lets a reader lift a
listing into their own system without an attribution obligation on their source files.

## Contributions

By opening a pull request you agree to license your contribution under the licence that
governs the files you touched, as set out above. There is no separate CLA.

## Known discrepancy: Edition 1.7 of the Agent Engineering handbook

The front matter of `agents-handbook` Edition 1.7.0 reads:

```
rights: "Copyright © 2026 Ankit Kumar Pandey. All rights reserved."
```

That predates this licensing policy and contradicts it. The repository licensing above is
the operative grant — the copyright holder is the same person in both cases, and the grant
made here is deliberate and current.

Edition 1.7.0 is **not** being edited to correct the string, because the release is
immutable by design: the manuscript's SHA-256 is pinned in `SHA256SUMS.txt`,
`source/SHA256SUMS.txt`, `FULL_SOURCE_MANIFEST.json` and
`source/canonical_source_manifest.json`, and it is bound into the published PDF and
verified by `verify_pdf_binding.py`. Editing one line of prose would invalidate the whole
verification chain and the published build receipt.

The front matter is corrected in Edition 1.8.0. Tracked as an erratum.
