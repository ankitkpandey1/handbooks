#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Uniform build entrypoint for every book, Tier A or B.
#
#   scripts/build-book.sh <slug> [pdf|epub|html|md ...]
#
# With no formats, builds the formats declared in the book's book.json.
# Output lands in books/<slug>/build/.
#
# Tier A books own their PDF pipeline (attachment, linearisation, receipts); this script
# delegates to book.json's build.pdf_entrypoint when one is declared, and only falls back to
# a generic Pandoc invocation when it is not. The non-PDF formats are always generic: their
# purpose is reach (EPUB for devices, HTML for the web, single-file Markdown for agents),
# not typesetting fidelity.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$REPO/scripts/bookmeta.py"

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "usage: scripts/build-book.sh <slug> [pdf|epub|html|md ...]" >&2
  echo "known slugs: $(python3 "$META" slugs | tr '\n' ' ')" >&2
  exit 2
fi
shift

BOOK="$REPO/books/$SLUG"
[[ -f "$BOOK/book.json" ]] || { echo "error: no such book: $SLUG" >&2; exit 2; }

if ! python3 "$META" validate "$SLUG"; then
  echo "error: $SLUG has an invalid book.json; refusing to build" >&2
  exit 1
fi

FORMATS=("$@")
if [[ ${#FORMATS[@]} -eq 0 ]]; then
  # shellcheck disable=SC2207
  FORMATS=($(python3 "$META" formats "$SLUG"))
fi

SRC_REL="$(python3 "$META" get "$SLUG" canonical_source)"
SRC="$BOOK/$SRC_REL"
SRC_DIR="$(dirname "$SRC")"
OUT="$BOOK/build"
mkdir -p "$OUT"

TITLE="$(python3 "$META" get "$SLUG" title)"
EDITION="$(python3 "$META" get "$SLUG" edition)"
TIER="$(python3 "$META" get "$SLUG" tier)"
PDF_ENTRY="$(python3 "$META" get "$SLUG" build.pdf_entrypoint)"
DEFAULTS_REL="$(python3 "$META" get "$SLUG" build.pandoc_defaults)"

need() { command -v "$1" >/dev/null 2>&1 || { echo "error: '$1' not found. Run scripts/setup-toolchain.sh, or push and let CI build." >&2; exit 3; }; }

echo "==> $SLUG (Tier $TIER, edition $EDITION): building ${FORMATS[*]}"

for fmt in "${FORMATS[@]}"; do
  case "$fmt" in
    pdf)
      need pandoc
      need xelatex
      if [[ -n "$PDF_ENTRY" && -f "$BOOK/$PDF_ENTRY" ]]; then
        echo "--> pdf via the book's own pipeline: $PDF_ENTRY"
        ( cd "$BOOK" && bash "$PDF_ENTRY" "$OUT/$SLUG.pdf" )
      else
        echo "--> pdf via generic Pandoc/XeLaTeX"
        args=(--standalone --pdf-engine=xelatex --toc --toc-depth=2 --listings)
        [[ -n "$DEFAULTS_REL" && -f "$BOOK/$DEFAULTS_REL" ]] && args=(--defaults "$BOOK/$DEFAULTS_REL" --standalone)
        ( cd "$SRC_DIR" && pandoc "${args[@]}" "$SRC" -o "$OUT/$SLUG.pdf" )
      fi
      ;;
    epub)
      need pandoc
      echo "--> epub"
      ( cd "$SRC_DIR" && pandoc --from markdown+raw_tex --to epub3 \
          --standalone --toc --toc-depth=2 \
          --metadata "title=$TITLE" --metadata "version=$EDITION" \
          "$SRC" -o "$OUT/$SLUG.epub" )
      ;;
    html)
      need pandoc
      echo "--> html (single file, self-contained)"
      # --number-sections is deliberately absent: it is a boolean flag that takes no argument,
      # and section numbering is off by default, which is what the manuscripts want (they
      # number their own sections in the heading text).
      ( cd "$SRC_DIR" && pandoc --from markdown+raw_tex --to html5 \
          --standalone --embed-resources --toc --toc-depth=3 \
          --highlight-style=tango \
          --metadata "title=$TITLE" \
          "$SRC" -o "$OUT/$SLUG.html" )
      ;;
    md)
      # The agent-facing artifact: one plain GitHub-flavoured Markdown file, no LaTeX
      # rawtex noise, no front matter surprises. This is the format an agent should be
      # handed, and the one a human can paste into a chat.
      need pandoc
      echo "--> md (single-file agent export)"
      # No --standalone: a bare document body is exactly what an agent should receive.
      ( cd "$SRC_DIR" && pandoc --from markdown+raw_tex --to gfm \
          --wrap=none \
          "$SRC" -o "$OUT/$SLUG.md" )
      ;;
    *)
      echo "error: unknown format '$fmt' (want: pdf epub html md)" >&2
      exit 2
      ;;
  esac
done

echo "==> done. artifacts in books/$SLUG/build/:"
ls -lh "$OUT" | tail -n +2
