#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-manifest-only}"
bash "$ROOT/source/run_publication_checks.sh" \
  "$ROOT/release/Production_Agent_Engineering_Edition_1.8.pdf" \
  "$ROOT/release/Production_Agent_Engineering_Edition_1.8_Reproducibility_Package.zip" \
  "$ROOT/release/Publication_Build_Receipt_Edition_1.8.json" \
  "$MODE"
