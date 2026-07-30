#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Installs the pinned build toolchain on Debian/Ubuntu (and in CI, which uses the same
# script so that "works in CI" and "works on my machine" mean the same thing).
#
#   scripts/setup-toolchain.sh [--no-latex] [--python-reqs <requirements.txt>]
#
# Reproducibility boundary, stated plainly:
#   * Pandoc is pinned to an exact version AND verified by SHA-256. Pandoc is the component
#     whose version most directly changes document output, so it is pinned hardest.
#   * TeX Live and fonts come from the distribution's current packages and are NOT pinned.
#     A different apt snapshot can therefore produce a non-identical PDF.
#   * Python packages are pinned exactly by the book's own requirements.txt.
#
# This is an attestable environment, not a reconstructive lock. It matches the claim the
# books already make in their own reproducibility-boundary sections: source, build inputs,
# text and navigation properties and the embedded archive are verified; byte-identical PDFs
# across differing dependency closures are not promised. For a stronger boundary, run the
# build inside a container pinned by digest — see docs/maintainers/release-runbook.md.
set -euo pipefail

PANDOC_VERSION="3.1.11.1"
PANDOC_DEB="pandoc-${PANDOC_VERSION}-1-amd64.deb"
PANDOC_URL="https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/${PANDOC_DEB}"
PANDOC_SHA256="ab0ac0aa1c3f9b23243d14e43023e06cbce51a52420aba17d27bd0d9c28f73ac"

WITH_LATEX=1
PY_REQS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-latex) WITH_LATEX=0; shift ;;
    --python-reqs) PY_REQS="${2:?--python-reqs needs a path}"; shift 2 ;;
    *) echo "error: unknown option '$1'" >&2; exit 2 ;;
  esac
done

SUDO=""
if [[ "$(id -u)" -ne 0 ]]; then
  command -v sudo >/dev/null 2>&1 || { echo "error: need root or sudo" >&2; exit 1; }
  SUDO="sudo"
fi

command -v apt-get >/dev/null 2>&1 || {
  echo "error: this script targets Debian/Ubuntu. On other systems install by hand:" >&2
  echo "       pandoc ${PANDOC_VERSION}, XeLaTeX, and the Noto/DejaVu fonts." >&2
  exit 1
}

echo "==> apt update"
$SUDO apt-get update -qq

echo "==> base tools"
$SUDO apt-get install -y --no-install-recommends ca-certificates curl python3 python3-pip

# --- pandoc, pinned and hash-verified -------------------------------------------------
if command -v pandoc >/dev/null 2>&1 && pandoc --version | head -1 | grep -q "$PANDOC_VERSION"; then
  echo "==> pandoc $PANDOC_VERSION already present"
else
  echo "==> pandoc $PANDOC_VERSION"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL "$PANDOC_URL" -o "$TMP/$PANDOC_DEB"
  echo "${PANDOC_SHA256}  $TMP/$PANDOC_DEB" | sha256sum -c - \
    || { echo "FATAL: pandoc checksum mismatch — refusing to install" >&2; exit 1; }
  $SUDO apt-get install -y "$TMP/$PANDOC_DEB"
fi

# --- XeLaTeX and the fonts the manuscripts ask for ------------------------------------
# The books select Noto Serif / Noto Sans / DejaVu Sans Mono, and load microtype, xurl,
# booktabs, longtable, tabularx, enumitem, fancyhdr, titlesec, listings, tcolorbox,
# needspace, ragged2e, etoolbox and the KOMA-Script scrartcl class. The package sets below
# cover all of those without pulling texlive-full.
if [[ "$WITH_LATEX" -eq 1 ]]; then
  echo "==> XeLaTeX, LaTeX packages, fonts"
  $SUDO apt-get install -y --no-install-recommends \
    texlive-xetex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-lang-english \
    lmodern \
    fonts-noto-core \
    fonts-dejavu-core \
    poppler-utils
else
  echo "==> skipping LaTeX (--no-latex); pdf builds will not work"
fi

# --- python dependencies for the verifier suites --------------------------------------
if [[ -n "$PY_REQS" ]]; then
  [[ -f "$PY_REQS" ]] || { echo "error: no such requirements file: $PY_REQS" >&2; exit 1; }
  echo "==> python deps from $PY_REQS"
  python3 -m pip install --quiet --break-system-packages -r "$PY_REQS" 2>/dev/null \
    || python3 -m pip install --quiet -r "$PY_REQS"
fi

echo
echo "==> toolchain ready"
printf '    pandoc  : %s\n' "$(pandoc --version 2>/dev/null | head -1 || echo MISSING)"
printf '    xelatex : %s\n' "$(xelatex --version 2>/dev/null | head -1 || echo 'MISSING (pdf disabled)')"
printf '    python  : %s\n' "$(python3 --version)"
