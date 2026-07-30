#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-manifest-only}"
bash "$ROOT/source/run_publication_checks.sh" \
  "$ROOT/release/Production_Agent_Engineering_2026_Edition_1.7.pdf" \
  "$ROOT/release/Production_Agent_Engineering_2026_Edition_1.7_Reproducibility_Package.zip" \
  "$ROOT/release/Publication_Build_Receipt_Edition_1.7.json" \
  "$MODE"
