#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Scaffolds a new Tier B book from _template/.
#
#   scripts/new-book.sh <slug> "Book title" [--from-draft <draft-slug>]
#
# The point of this script is that starting a book must cost about ten seconds. Research that
# stays in a chat window is research that is lost, and the usual reason it stays there is that
# the publishing pipeline looks too steep to climb. It is not: a Tier B book is a manuscript
# and a book.json, and CI does the rest.
#
# --from-draft moves an existing drafts/<slug>/ into the new book's source tree, so promoting
# a raw research dump is one command rather than a project.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$REPO/_template"

SLUG="${1:-}"
TITLE="${2:-}"
if [[ -z "$SLUG" || -z "$TITLE" ]]; then
  cat >&2 <<'USAGE'
usage: scripts/new-book.sh <slug> "Book title" [--from-draft <draft-slug>]

  slug   lowercase, digits and hyphens only. Becomes the directory name, the release tag
         prefix (<slug>/v1.0.0) and every download filename. Choose it once; changing it
         later breaks published links.

example:
  scripts/new-book.sh multiagent-handbook "Multi-Agent Systems in Practice"
  scripts/new-book.sh kernel-vuln-handbook "Kernel Vulnerability Research" --from-draft kernel-notes
USAGE
  exit 2
fi
shift 2

FROM_DRAFT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-draft) FROM_DRAFT="${2:?--from-draft needs a draft slug}"; shift 2 ;;
    *) echo "error: unknown option '$1'" >&2; exit 2 ;;
  esac
done

if [[ ! "$SLUG" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$ ]]; then
  echo "error: slug '$SLUG' must be lowercase alphanumeric with internal hyphens only" >&2
  exit 2
fi

DEST="$REPO/books/$SLUG"
if [[ -e "$DEST" ]]; then
  echo "error: books/$SLUG already exists" >&2
  exit 1
fi

DATE="$(date -u +%Y-%m-%d)"
YEAR="$(date -u +%Y)"

echo "==> creating books/$SLUG"
mkdir -p "$DEST/source" "$DEST/build"
touch "$DEST/build/.gitkeep"

subst() {
  sed -e "s|__SLUG__|$SLUG|g" \
      -e "s|__TITLE__|$TITLE|g" \
      -e "s|__DATE__|$DATE|g" \
      -e "s|__YEAR__|$YEAR|g" \
      -e "s|__FIRST_PART__|Orientation|g" "$1"
}

subst "$TEMPLATE/book.json"                > "$DEST/book.json"
subst "$TEMPLATE/source/__SLUG__.md"       > "$DEST/source/$SLUG.md"
subst "$TEMPLATE/AGENTS.md"                > "$DEST/AGENTS.md"
subst "$TEMPLATE/README.md"                > "$DEST/README.md"

# --- optionally absorb a draft ---------------------------------------------------------
if [[ -n "$FROM_DRAFT" ]]; then
  SRC_DRAFT="$REPO/drafts/$FROM_DRAFT"
  if [[ ! -d "$SRC_DRAFT" ]]; then
    echo "error: no drafts/$FROM_DRAFT" >&2
    exit 1
  fi
  echo "==> absorbing drafts/$FROM_DRAFT"
  mkdir -p "$DEST/source/raw"
  cp -r "$SRC_DRAFT/." "$DEST/source/raw/"
  cat >> "$DEST/source/$SLUG.md" <<EOF

# Appendix — raw research

Unedited source material for this book is preserved under \`source/raw/\`, promoted from
\`drafts/$FROM_DRAFT\` on $DATE. It is unlabelled and unreviewed. Claims in the body above
are labelled; claims in the raw material are not.
EOF
  echo "    raw material copied to books/$SLUG/source/raw/ (drafts/$FROM_DRAFT left in place)"
fi

# --- validate what we just produced ---------------------------------------------------
echo "==> validating"
if ! python3 "$REPO/scripts/bookmeta.py" validate "$SLUG"; then
  echo "error: scaffold is invalid — this is a bug in _template/ or in this script" >&2
  exit 1
fi
python3 "$REPO/scripts/lint-book.py" "$SLUG" || true

echo "==> refreshing catalogue"
python3 "$REPO/scripts/build-index.py" >/dev/null

cat <<EOF

==> books/$SLUG is ready.

Next:
  1. Write. The manuscript is books/$SLUG/source/$SLUG.md
     Keep claims labelled — that is the whole contribution standard.
  2. Check it:            scripts/verify-book.sh $SLUG
  3. Build it locally:    scripts/build-book.sh $SLUG html md
  4. When it is worth reading, set "status": "published" in books/$SLUG/book.json,
     bump "edition", then:
        python3 scripts/build-index.py
        git add -A && git commit -m "book: $SLUG v0.1.0"
        git tag $SLUG/v0.1.0 && git push origin main --tags

CI builds PDF, EPUB, HTML and single-file Markdown, signs them, and publishes them.
EOF
