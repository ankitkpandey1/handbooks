<!-- SPDX-License-Identifier: Apache-2.0 -->
## What this changes

<!-- One or two sentences. If it corrects a claim, link the erratum or claim-challenge issue. -->

## Checklist

- [ ] `scripts/verify-book.sh <slug>` passes locally, or CI is expected to run it
- [ ] **One book only.** This PR does not touch two books
- [ ] Nothing under `books/*/release/` is modified — published editions are immutable
- [ ] No hash-pinned file changed outside a proper edition bump (see [AGENTS.md](../AGENTS.md))
- [ ] New claims carry evidence labels; new code listings carry authenticity labels
- [ ] New code files carry an SPDX header
- [ ] `python3 scripts/build-index.py` re-run if any `book.json` changed

## Edition impact

<!-- Delete the lines that do not apply. -->

- **Patch** — typo, link, or clarification that changes no claim
- **Minor** — new section, corrected claim, or new evidence
- **Major** — restructuring, or invalidates prior guidance
- **None** — tooling or CI only
