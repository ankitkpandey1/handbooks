#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Builds the full Pages deployment: the generated docs/ catalogue plus a rendered,
# SEO-tagged HTML page for every published book, so books are readable directly on the
# site instead of only as release-asset downloads.
#
#   scripts/build-site.sh [outdir]
#
# outdir defaults to _site/ (repo root). It is populated with a copy of docs/ plus
# books/<slug>/index.html for every book whose book.json declares status "published".
# docs/ itself is never modified in place; only outdir is written to, and the two are
# distinct trees on purpose — docs/ is committed (it is the site's stable core, and CI
# checks it is current), the per-book HTML pages are rebuilt fresh from source on every
# deploy and are not committed.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$REPO/scripts/bookmeta.py"
INJECT="$REPO/scripts/site_inject.py"

OUT="${1:-$REPO/_site}"
if [[ "$OUT" != /* ]]; then
  OUT="$(pwd)/$OUT"
fi

echo "==> regenerating docs/ catalogue"
python3 "$REPO/scripts/build-index.py"

echo "==> staging docs/ -> $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"
cp -a "$REPO/docs/." "$OUT/"

for slug in $(python3 "$META" slugs); do
  status="$(python3 "$META" get "$slug" status)"
  if [[ "$status" != "published" ]]; then
    echo "==> skip $slug (status=$status, not hosted)"
    continue
  fi

  echo "==> building html for $slug"
  bash "$REPO/scripts/build-book.sh" "$slug" html

  BOOK="$REPO/books/$slug"
  SRC_HTML="$BOOK/build/$slug.html"
  [[ -f "$SRC_HTML" ]] || { echo "error: expected $SRC_HTML after build" >&2; exit 1; }

  DEST_DIR="$OUT/books/$slug"
  mkdir -p "$DEST_DIR"
  python3 "$INJECT" --slug "$slug" --in "$SRC_HTML" --out "$DEST_DIR/index.html"
done

echo "==> site staged in $OUT"
find "$OUT" -maxdepth 2 -type f | sort
