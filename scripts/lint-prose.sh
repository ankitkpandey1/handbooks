#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Prose linting via Vale. The supported entrypoint — prefer it over bare `vale`, because Vale 3
# has no per-path disable switch and the exclusions (raw promoted drafts, drafts/) are applied
# here as globs.
#
#   scripts/lint-prose.sh [<slug>] [--strict]
#
# With no slug, lints every book. --strict makes any alert fail the run; by default only errors
# do, so a suggestion never blocks a release.
#
# Vale is optional: if it is not installed this exits 0 with a note. Prose style is a quality
# signal, not a correctness gate, and a missing optional tool must not look like a failure.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$REPO/scripts/bookmeta.py"

SLUG=""
STRICT=0
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    -*) echo "error: unknown option '$arg'" >&2; exit 2 ;;
    *) SLUG="$arg" ;;
  esac
done

if ! command -v vale >/dev/null 2>&1; then
  echo "note: vale is not installed — skipping prose lint."
  echo "      install: https://vale.sh/docs/install   (or: brew install vale)"
  exit 0
fi

if [[ -n "$SLUG" ]]; then
  SLUGS=("$SLUG")
else
  # shellcheck disable=SC2207
  SLUGS=($(python3 "$META" slugs))
fi

FILES=()
for slug in "${SLUGS[@]}"; do
  book="$REPO/books/$slug"
  [[ -f "$book/book.json" ]] || { echo "error: no such book: $slug" >&2; exit 2; }
  src="$book/$(python3 "$META" get "$slug" canonical_source)"
  [[ -f "$src" ]] && FILES+=("$src")
  # Procedural content, if the book has any, is linted under the stricter STE-derived caps.
  if [[ -d "$book/source/procedures" ]]; then
    while IFS= read -r f; do FILES+=("$f"); done < <(find "$book/source/procedures" -name '*.md')
  fi
done

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "note: no manuscripts to lint"
  exit 0
fi

MIN="error"
[[ "$STRICT" -eq 1 ]] && MIN="suggestion"

echo "==> vale $(vale --version | head -1) over ${#FILES[@]} manuscript(s)"

# Never lint promoted raw material: it is unedited by definition.
set +e
vale --config="$REPO/.vale.ini" \
     --glob='!**/raw/**' \
     --minAlertLevel="$MIN" \
     "${FILES[@]}"
STATUS=$?
set -e

# Always show the full picture, including the alerts below the failure threshold, so the author
# can see the suggestions without them being able to break a build.
if [[ "$STRICT" -eq 0 ]]; then
  echo
  echo "==> full alert summary (informational; only errors fail this run)"
  vale --config="$REPO/.vale.ini" --glob='!**/raw/**' \
       --minAlertLevel=suggestion --output=line "${FILES[@]}" 2>/dev/null | sed 's|^'"$REPO"'/||' || true
fi

exit "$STATUS"
