#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Uniform verification entrypoint for every book.
#
#   scripts/verify-book.sh <slug> [--strict] [--online] [--prose]
#
# Two layers run, in order:
#   1. Structural lint (every book): metadata validity, front matter, heading structure,
#      licence consistency, code-authenticity label coverage, tier honesty. No toolchain needed.
#   2. The book's own verifier suite, if book.json declares one (Tier A). This is the real
#      gate: for agents-handbook it is 17 checks binding the published PDF to its source.
#
# --strict  promotes warnings to failures
# --online  passes the book's declared online args, refetching pinned upstream sources
# --prose   additionally runs Vale prose linting (optional tool; see scripts/lint-prose.sh)
#
# If this fails, the change is wrong. Do not weaken a verifier to make a change pass.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$REPO/scripts/bookmeta.py"

SLUG="${1:-}"
if [[ -z "$SLUG" ]]; then
  echo "usage: scripts/verify-book.sh <slug> [--strict] [--online]" >&2
  echo "known slugs: $(python3 "$META" slugs | tr '\n' ' ')" >&2
  exit 2
fi
shift

STRICT=""
ONLINE=""
PROSE=""
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT="--strict" ;;
    --online) ONLINE="1" ;;
    --prose) PROSE="1" ;;
    *) echo "error: unknown option '$arg'" >&2; exit 2 ;;
  esac
done

BOOK="$REPO/books/$SLUG"
[[ -f "$BOOK/book.json" ]] || { echo "error: no such book: $SLUG" >&2; exit 2; }

TIER="$(python3 "$META" get "$SLUG" tier)"
echo "==> $SLUG (Tier $TIER): layer 1/2 — structural lint"
python3 "$REPO/scripts/lint-book.py" "$SLUG" $STRICT

# Prose style is opt-in: it is a quality signal, not a correctness gate, and it needs an
# optional external tool. Run it while writing, not as a release blocker.
if [[ -n "$PROSE" ]]; then
  echo "==> $SLUG: prose style (Vale)"
  bash "$REPO/scripts/lint-prose.sh" "$SLUG" $STRICT
fi

ENTRY="$(python3 "$META" get "$SLUG" verify.entrypoint)"
if [[ -z "$ENTRY" ]]; then
  if [[ "$TIER" == "A" ]]; then
    echo "error: Tier A book '$SLUG' declares no verify.entrypoint" >&2
    exit 1
  fi
  echo "==> $SLUG: layer 2/2 — no book-specific verifier declared (expected for Tier B)"
  exit 0
fi

if [[ ! -f "$BOOK/$ENTRY" ]]; then
  echo "error: verify.entrypoint '$ENTRY' declared but not found in books/$SLUG" >&2
  exit 1
fi

if [[ -n "$ONLINE" ]]; then
  # shellcheck disable=SC2207
  ARGS=($(python3 "$META" get "$SLUG" verify.online_args))
else
  # shellcheck disable=SC2207
  ARGS=($(python3 "$META" get "$SLUG" verify.args))
fi

echo "==> $SLUG: layer 2/2 — book verifier: $ENTRY ${ARGS[*]:-}"
( cd "$BOOK" && bash "$ENTRY" "${ARGS[@]:-}" )
echo "==> $SLUG: verification passed"
